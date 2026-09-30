package fr.timefield.tfother.tiplouf.voice;

import com.mojang.logging.LogUtils;
import de.maxhenkel.voicechat.api.ForgeVoicechatPlugin;
import de.maxhenkel.voicechat.api.VoicechatConnection;
import de.maxhenkel.voicechat.api.VoicechatPlugin;
import de.maxhenkel.voicechat.api.VoicechatServerApi;
import de.maxhenkel.voicechat.api.VolumeCategory;
import de.maxhenkel.voicechat.api.audiochannel.AudioPlayer;
import de.maxhenkel.voicechat.api.audiochannel.EntityAudioChannel;
import de.maxhenkel.voicechat.api.events.EventRegistration;
import de.maxhenkel.voicechat.api.events.MicrophonePacketEvent;
import de.maxhenkel.voicechat.api.events.VoicechatServerStartedEvent;
import de.maxhenkel.voicechat.api.events.VoicechatServerStoppedEvent;
import de.maxhenkel.voicechat.api.opus.OpusDecoder;
import de.maxhenkel.voicechat.api.opus.OpusEncoder;
import fr.timefield.tfother.TFother;
import fr.timefield.tfother.entity.TiploufNpc;
import fr.timefield.tfother.tiplouf.Conversations;
import fr.timefield.tfother.tiplouf.OpenAiClient;
import fr.timefield.tfother.tiplouf.TiploufConfig;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.server.ServerLifecycleHooks;
import org.slf4j.Logger;

/**
 * Simple Voice Chat plugin: Tiplouf hears the players he talks with and answers aloud.
 *
 * <p>The microphone of a player in a conversation is recorded; when they stop talking, the recording is
 * transcribed (in French) and handled like a chat question. Answers are synthesized and played from
 * Tiplouf's position, for that player only.
 */
@ForgeVoicechatPlugin
public final class TiploufVoicePlugin implements VoicechatPlugin {
    private static final Logger LOGGER = LogUtils.getLogger();

    /** Voice chat audio: 48 kHz, 16-bit, mono, 20 ms frames. */
    private static final int SAMPLE_RATE = 48000;
    /** The end of a question: this long without microphone packets. */
    private static final long SILENCE_MS = 700;
    private static final int MIN_SAMPLES = SAMPLE_RATE * 2 / 5;
    private static final int MAX_SAMPLES = SAMPLE_RATE * 30;
    /** Below this loudness (RMS, out of 32768) the recording is noise, not speech. */
    private static final double MIN_RMS = 150;
    /** After Tiplouf finishes talking, the microphone is ignored a little longer so his echo is not heard. */
    private static final long ECHO_MS = 400;
    private static final String TRANSCRIPTION_PROMPT = "Conversation en français avec Tiplouf, un pingouin, "
            + "sur le mod Minecraft Tensura : Rimuru, slime, magicules, EP, compétence unique, compétence ultime, "
            + "seigneur démon, vrai héros, Veldora, Charybdis, Orc Lord, Hinata, Shizu, Gazel, Harvest Festival.";

    private static volatile VoicechatServerApi api;
    private static volatile VolumeCategory category;
    private static final Map<UUID, Recording> RECORDINGS = new ConcurrentHashMap<>();
    private static final Map<UUID, AudioPlayer> PLAYING = new ConcurrentHashMap<>();
    private static final Map<UUID, Long> DEAF_UNTIL = new ConcurrentHashMap<>();
    private static final ScheduledExecutorService SCHEDULER = Executors.newSingleThreadScheduledExecutor(r -> {
        Thread thread = new Thread(r, "Tiplouf voice");
        thread.setDaemon(true);
        return thread;
    });

    static {
        SCHEDULER.scheduleWithFixedDelay(TiploufVoicePlugin::checkSilence, 100, 100, TimeUnit.MILLISECONDS);
    }

    private static final class Recording {
        final OpusDecoder decoder;
        final List<short[]> frames = new ArrayList<>();
        int samples;
        long lastPacket = System.currentTimeMillis();

        Recording(OpusDecoder decoder) {
            this.decoder = decoder;
        }
    }

    @Override
    public String getPluginId() {
        return TFother.MODID;
    }

    @Override
    public void registerEvents(EventRegistration registration) {
        registration.registerEvent(VoicechatServerStartedEvent.class, TiploufVoicePlugin::onStarted);
        registration.registerEvent(VoicechatServerStoppedEvent.class, event -> onStopped());
        registration.registerEvent(MicrophonePacketEvent.class, TiploufVoicePlugin::onMicrophone);
    }

    static boolean isReady() {
        return api != null;
    }

    private static void onStarted(VoicechatServerStartedEvent event) {
        VoicechatServerApi serverApi = event.getVoicechat();
        category = serverApi.volumeCategoryBuilder()
                .setId("tiplouf")
                .setName("Tiplouf")
                .setDescription("Voix du PNJ Tiplouf")
                .build();
        serverApi.registerVolumeCategory(category);
        api = serverApi;
        LOGGER.info("[Tiplouf] Simple Voice Chat detected, voice questions enabled");
    }

    private static void onStopped() {
        api = null;
        PLAYING.values().forEach(AudioPlayer::stopPlaying);
        PLAYING.clear();
        RECORDINGS.values().forEach(r -> r.decoder.close());
        RECORDINGS.clear();
        DEAF_UNTIL.clear();
    }

    /** Runs on the voice chat network thread for every microphone packet. */
    private static void onMicrophone(MicrophonePacketEvent event) {
        VoicechatConnection sender = event.getSenderConnection();
        if (api == null || sender == null || !TiploufConfig.VOICE_ENABLED.get()
                || !(sender.getPlayer().getPlayer() instanceof ServerPlayer player)) {
            return;
        }
        UUID id = player.getUUID();
        if (!Conversations.isListening(id)) {
            return;
        }
        if (TiploufConfig.VOICE_PRIVATE.get()) {
            event.cancel();
        }
        byte[] data = event.getPacket().getOpusEncodedData();
        if (data.length == 0 || PLAYING.containsKey(id) || System.currentTimeMillis() < DEAF_UNTIL.getOrDefault(id, 0L)) {
            return;
        }
        Recording recording = RECORDINGS.computeIfAbsent(id, key -> new Recording(api.createDecoder()));
        synchronized (recording) {
            if (recording.decoder.isClosed()) {
                return;
            }
            short[] frame = recording.decoder.decode(data);
            recording.frames.add(frame);
            recording.samples += frame.length;
            recording.lastPacket = System.currentTimeMillis();
            if (recording.samples >= MAX_SAMPLES && RECORDINGS.remove(id, recording)) {
                SCHEDULER.execute(() -> finish(id, recording));
            }
        }
    }

    private static void checkSilence() {
        long now = System.currentTimeMillis();
        RECORDINGS.forEach((id, recording) -> {
            if (now - recording.lastPacket > SILENCE_MS && RECORDINGS.remove(id, recording)) {
                finish(id, recording);
            }
        });
    }

    private static void finish(UUID id, Recording recording) {
        short[] audio;
        synchronized (recording) {
            recording.decoder.close();
            audio = new short[recording.samples];
            int pos = 0;
            for (short[] frame : recording.frames) {
                System.arraycopy(frame, 0, audio, pos, frame.length);
                pos += frame.length;
            }
        }
        if (audio.length < MIN_SAMPLES || rms(audio) < MIN_RMS || !Conversations.acceptsVoiceQuestion(id)) {
            return;
        }
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        if (server == null) {
            return;
        }
        OpenAiClient.transcribe(toWav16k(audio), TRANSCRIPTION_PROMPT)
                .handle((text, error) -> {
                    String question = error == null ? filterHallucination(text) : null;
                    if (error != null || !question.isEmpty()) {
                        server.execute(() -> Conversations.onVoiceQuestion(server, id, question, error));
                    }
                    return null;
                });
    }

    /** On silence or noise, transcription models sometimes produce these video subtitle credits. */
    private static String filterHallucination(String text) {
        String lower = text.toLowerCase(Locale.ROOT);
        if (lower.contains("amara.org") || lower.contains("sous-titr") || lower.contains("merci d'avoir regardé")) {
            return "";
        }
        return text.strip();
    }

    static void speak(ServerPlayer player, TiploufNpc npc, String text) {
        VoicechatServerApi serverApi = api;
        if (serverApi == null || TiploufConfig.SPEECH_MODEL.get().isBlank()) {
            return;
        }
        VoicechatConnection connection = serverApi.getConnectionOf(player.getUUID());
        if (connection == null || !connection.isInstalled() || connection.isDisabled()) {
            return;
        }
        UUID id = player.getUUID();
        de.maxhenkel.voicechat.api.Entity entity = serverApi.fromEntity(npc);
        OpenAiClient.speech(text)
                .thenAccept(pcm -> play(serverApi, id, entity, toShorts48k(pcm)))
                .exceptionally(e -> {
                    LOGGER.warn("[Tiplouf] Speech synthesis failed: {}", e.getMessage());
                    return null;
                });
    }

    private static void play(VoicechatServerApi serverApi, UUID id, de.maxhenkel.voicechat.api.Entity entity,
                             short[] audio) {
        if (api != serverApi || !Conversations.isListening(id)) {
            return;
        }
        EntityAudioChannel channel = serverApi.createEntityAudioChannel(UUID.randomUUID(), entity);
        if (channel == null) {
            return;
        }
        channel.setCategory(category.getId());
        channel.setDistance(32F);
        // Conversations are private: only this player hears Tiplouf's answer.
        channel.setFilter(listener -> listener.getUuid().equals(id));
        OpusEncoder encoder = serverApi.createEncoder();
        AudioPlayer player = serverApi.createAudioPlayer(channel, encoder, audio);
        player.setOnStopped(() -> {
            PLAYING.remove(id, player);
            DEAF_UNTIL.put(id, System.currentTimeMillis() + ECHO_MS);
            if (!encoder.isClosed()) {
                encoder.close();
            }
        });
        AudioPlayer previous = PLAYING.put(id, player);
        if (previous != null) {
            previous.stopPlaying();
        }
        // What the player said while the answer was generated is dropped too, it may be the echo of a previous one.
        Recording recording = RECORDINGS.remove(id);
        if (recording != null) {
            synchronized (recording) {
                recording.decoder.close();
            }
        }
        player.startPlaying();
    }

    static void forget(UUID id) {
        AudioPlayer player = PLAYING.remove(id);
        if (player != null) {
            player.stopPlaying();
        }
        Recording recording = RECORDINGS.remove(id);
        if (recording != null) {
            synchronized (recording) {
                recording.decoder.close();
            }
        }
        DEAF_UNTIL.remove(id);
    }

    private static double rms(short[] audio) {
        double sum = 0;
        for (short s : audio) {
            sum += (double) s * s;
        }
        return Math.sqrt(sum / audio.length);
    }

    /** 48 kHz samples to a 16 kHz 16-bit mono WAV file, plenty for speech and 3 times smaller. */
    private static byte[] toWav16k(short[] audio) {
        int samples = audio.length / 3;
        ByteBuffer wav = ByteBuffer.allocate(44 + samples * 2).order(ByteOrder.LITTLE_ENDIAN);
        wav.put("RIFF".getBytes()).putInt(36 + samples * 2).put("WAVE".getBytes())
                .put("fmt ".getBytes()).putInt(16).putShort((short) 1).putShort((short) 1)
                .putInt(16000).putInt(16000 * 2).putShort((short) 2).putShort((short) 16)
                .put("data".getBytes()).putInt(samples * 2);
        for (int i = 0; i < samples; i++) {
            wav.putShort((short) ((audio[3 * i] + audio[3 * i + 1] + audio[3 * i + 2]) / 3));
        }
        return wav.array();
    }

    /** 24 kHz little-endian PCM from the speech endpoint to 48 kHz samples (linear interpolation). */
    private static short[] toShorts48k(byte[] pcm) {
        ByteBuffer in = ByteBuffer.wrap(pcm).order(ByteOrder.LITTLE_ENDIAN);
        int samples = pcm.length / 2;
        short[] out = new short[samples * 2];
        for (int i = 0; i < samples; i++) {
            short current = in.getShort(2 * i);
            short next = i + 1 < samples ? in.getShort(2 * i + 2) : current;
            out[2 * i] = current;
            out[2 * i + 1] = (short) ((current + next) / 2);
        }
        return out;
    }
}
