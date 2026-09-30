package fr.timefield.tfother.tiplouf;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.mojang.logging.LogUtils;
import fr.timefield.tfother.TFother;
import fr.timefield.tfother.entity.TiploufNpc;
import fr.timefield.tfother.tiplouf.voice.VoiceSupport;
import java.time.LocalDate;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.regex.Pattern;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.ServerChatEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import org.slf4j.Logger;

/**
 * Chat conversations with Tiplouf.
 *
 * <p>Right-clicking Tiplouf starts a conversation: the player's chat messages are then sent
 * privately to Tiplouf (not broadcast) until they say goodbye, walk away or stay idle. With Simple Voice
 * Chat, the player can also ask aloud and Tiplouf reads his answers (see {@link VoiceSupport}).
 */
@EventBusSubscriber(modid = TFother.MODID)
public final class Conversations {
    private static final Logger LOGGER = LogUtils.getLogger();
    private static final double MAX_DISTANCE = 12.0D;
    private static final int MAX_QUESTION_LENGTH = 300;
    private static final int MAX_ANSWER_LENGTH = 400;
    private static final Pattern GOODBYE = Pattern.compile(
            "^\\s*(au revoir|aurevoir|bye|salut tiplouf|a\\+|ciao|merci,? au revoir|stop|fin)(,? tiplouf)?\\s*[.!]*\\s*$",
            Pattern.CASE_INSENSITIVE);

    private static final String SYSTEM_PROMPT = """
            Tu es Tiplouf, un petit pingouin bleu fier et enjoué, PNJ du serveur Minecraft Timefield \
            (modpack NeoForge 1.21.1). Tu aides les joueurs sur le mod Tensura: Reincarnated et ses addons.

            Règles :
            - Réponds toujours en français, en 1 ou 2 phrases courtes (3 au maximum si c'est indispensable). \
            Va droit au but : donne directement l'information utile, sans reformuler la question, sans \
            introduction ni conclusion, sans formule de politesse.
            - Texte brut uniquement : pas de markdown, pas de titres, pas de gras. Le chat Minecraft ne les affiche pas.
            - Appuie-toi UNIQUEMENT sur les extraits de la base de connaissances fournis avec la question. \
            Si la réponse n'y est pas, dis honnêtement que tu ne sais pas et conseille le wiki Tensura en jeu \
            ou le staff. N'invente jamais de recette, de chiffre, de drop ni de lieu.
            - Les recettes de craft sont visibles dans JEI (touche R sur un objet pour ses recettes, U pour ses \
            usages). Pour un craft classique, renvoie vers JEI. Détaille surtout comment obtenir les objets rares : \
            monstres qui les lâchent, coffres, minerais, stations spéciales, évolutions, conditions.
            - Donne les noms d'objets, compétences et monstres tels qu'ils apparaissent en jeu (en anglais), \
            avec le nom français entre parenthèses s'il est connu.
            - Si la question ne concerne pas Tensura, réponds très brièvement et gentiment, puis ramène la \
            conversation vers Tensura.
            - Personnalité : tu es serviable et un peu fanfaron, tu glisses rarement un « plouf ! ». \
            Ne te présente pas à chaque message.
            """;

    private static final Map<UUID, Conversation> CONVERSATIONS = new ConcurrentHashMap<>();
    private static final Map<UUID, Usage> USAGE = new ConcurrentHashMap<>();

    private static final class Conversation {
        final UUID npc;
        final ResourceKey<Level> dimension;
        final Deque<JsonObject> history = new ArrayDeque<>();
        volatile long lastActivity = System.currentTimeMillis();
        volatile boolean pending;

        Conversation(TiploufNpc npc) {
            this.npc = npc.getUUID();
            this.dimension = npc.level().dimension();
        }
    }

    private static final class Usage {
        LocalDate day = LocalDate.now();
        int count;
        long lastQuestion;
    }

    private Conversations() {
    }

    /** Called when a player right-clicks Tiplouf. */
    public static void start(ServerPlayer player, TiploufNpc npc) {
        Conversation existing = CONVERSATIONS.get(player.getUUID());
        if (existing != null && existing.npc.equals(npc.getUUID())) {
            existing.lastActivity = System.currentTimeMillis();
            say(player, npc, Component.translatable("message.tfother.tiplouf.still_here"));
            return;
        }
        if (!OpenAiClient.isConfigured()) {
            say(player, npc, Component.translatable("message.tfother.tiplouf.not_configured"));
            return;
        }
        CONVERSATIONS.put(player.getUUID(), new Conversation(npc));
        say(player, npc, Component.translatable("message.tfother.tiplouf.greet"));
        player.sendSystemMessage(Component.translatable(VoiceSupport.isAvailable()
                        ? "message.tfother.tiplouf.hint_voice" : "message.tfother.tiplouf.hint")
                .withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
    }

    /** True while the player is in a conversation that has not timed out. Safe from any thread. */
    public static boolean isListening(UUID playerId) {
        Conversation conv = CONVERSATIONS.get(playerId);
        return conv != null
                && System.currentTimeMillis() - conv.lastActivity <= TiploufConfig.CONVERSATION_TIMEOUT_SECONDS.get() * 1000L;
    }

    /** Whether a spoken question is worth transcribing (not while an answer is pending or over the daily limit). */
    public static boolean acceptsVoiceQuestion(UUID playerId) {
        Conversation conv = CONVERSATIONS.get(playerId);
        if (conv == null || conv.pending || !isListening(playerId)) {
            return false;
        }
        Usage usage = USAGE.get(playerId);
        int daily = TiploufConfig.DAILY_QUESTIONS_PER_PLAYER.get();
        return usage == null || daily <= 0 || !usage.day.equals(LocalDate.now()) || usage.count < daily;
    }

    /** A spoken question, transcribed. Called on the server thread. */
    public static void onVoiceQuestion(MinecraftServer server, UUID playerId, String question, Throwable error) {
        ServerPlayer player = server.getPlayerList().getPlayer(playerId);
        Conversation conv = CONVERSATIONS.get(playerId);
        if (player == null || conv == null) {
            return;
        }
        TiploufNpc npc = activeNpc(player, conv);
        if (npc == null) {
            CONVERSATIONS.remove(playerId);
            return;
        }
        if (error != null) {
            LOGGER.warn("[Tiplouf] Transcription for {} failed: {}", player.getGameProfile().getName(), error.getMessage());
            say(player, npc, Component.translatable("message.tfother.tiplouf.error"));
            return;
        }
        handle(player, npc, conv, question, true);
    }

    @SubscribeEvent(priority = EventPriority.HIGH)
    public static void onChat(ServerChatEvent event) {
        ServerPlayer player = event.getPlayer();
        Conversation conv = CONVERSATIONS.get(player.getUUID());
        if (conv == null) {
            return;
        }
        TiploufNpc npc = activeNpc(player, conv);
        if (npc == null) {
            // The player left: this message is a normal chat message.
            CONVERSATIONS.remove(player.getUUID());
            return;
        }
        event.setCanceled(true);
        handle(player, npc, conv, event.getRawText().strip(), false);
    }

    /** Tiplouf, if the player is still talking with him: close enough and not idle for too long. */
    private static TiploufNpc activeNpc(ServerPlayer player, Conversation conv) {
        TiploufNpc npc = findNpc(player, conv);
        long timeout = TiploufConfig.CONVERSATION_TIMEOUT_SECONDS.get() * 1000L;
        if (npc == null || player.distanceTo(npc) > MAX_DISTANCE || System.currentTimeMillis() - conv.lastActivity > timeout) {
            return null;
        }
        return npc;
    }

    private static void handle(ServerPlayer player, TiploufNpc npc, Conversation conv, String question, boolean spoken) {
        player.sendSystemMessage(Component.translatable(spoken ? "message.tfother.tiplouf.you_voice"
                        : "message.tfother.tiplouf.you", question)
                .withStyle(ChatFormatting.GRAY));
        if (GOODBYE.matcher(question).matches()) {
            CONVERSATIONS.remove(player.getUUID());
            say(player, npc, Component.translatable("message.tfother.tiplouf.bye"));
            return;
        }
        ask(player, npc, conv, question);
    }

    private static void ask(ServerPlayer player, TiploufNpc npc, Conversation conv, String question) {
        if (conv.pending) {
            say(player, npc, Component.translatable("message.tfother.tiplouf.busy"));
            return;
        }
        Usage usage = USAGE.computeIfAbsent(player.getUUID(), id -> new Usage());
        long now = System.currentTimeMillis();
        if (!usage.day.equals(LocalDate.now())) {
            usage.day = LocalDate.now();
            usage.count = 0;
        }
        int daily = TiploufConfig.DAILY_QUESTIONS_PER_PLAYER.get();
        if (daily > 0 && usage.count >= daily) {
            say(player, npc, Component.translatable("message.tfother.tiplouf.limit"));
            return;
        }
        if (now - usage.lastQuestion < TiploufConfig.COOLDOWN_SECONDS.get() * 1000L) {
            say(player, npc, Component.translatable("message.tfother.tiplouf.cooldown"));
            return;
        }
        usage.count++;
        usage.lastQuestion = now;
        conv.lastActivity = now;
        conv.pending = true;

        if (question.length() > MAX_QUESTION_LENGTH) {
            question = question.substring(0, MAX_QUESTION_LENGTH);
        }
        String finalQuestion = question;
        List<JsonObject> history = List.copyOf(conv.history);
        String playerName = player.getGameProfile().getName();
        UUID playerId = player.getUUID();
        MinecraftServer server = player.server;
        player.sendSystemMessage(Component.translatable("message.tfother.tiplouf.thinking")
                .withStyle(ChatFormatting.DARK_AQUA, ChatFormatting.ITALIC));

        // Search with the previous question too, so that follow-ups ("and where do I find it?") keep their subject.
        String searchQuery = history.stream()
                .filter(m -> m.get("role").getAsString().equals("user"))
                .reduce((a, b) -> b)
                .map(m -> m.get("question").getAsString() + "\n" + finalQuestion)
                .orElse(finalQuestion);

        // Any failure (network, API, knowledge base) must end up in deliver(), never crash the server.
        CompletableFuture.supplyAsync(() -> KnowledgeBase.search(searchQuery, TiploufConfig.CONTEXT_CHUNKS.get()))
                .thenCompose(search -> search)
                .thenCompose(extracts -> OpenAiClient.chat(buildMessages(history, extracts, playerName, finalQuestion)))
                .handle((answer, error) -> {
                    server.execute(() -> deliver(server, playerId, conv, finalQuestion, answer, error));
                    return null;
                });
    }

    private static JsonArray buildMessages(List<JsonObject> history, List<KnowledgeBase.Chunk> extracts,
                                           String playerName, String question) {
        JsonArray messages = new JsonArray();
        messages.add(message("system", SYSTEM_PROMPT));
        for (JsonObject m : history) {
            messages.add(message(m.get("role").getAsString(), m.get("content").getAsString()));
        }
        StringBuilder prompt = new StringBuilder("Extraits de la base de connaissances :\n");
        if (extracts.isEmpty()) {
            prompt.append("(aucun extrait trouvé)\n");
        }
        for (int i = 0; i < extracts.size(); i++) {
            KnowledgeBase.Chunk c = extracts.get(i);
            prompt.append('[').append(i + 1).append("] ").append(c.title()).append(" (").append(c.source()).append(")\n")
                    .append(c.text()).append("\n\n");
        }
        prompt.append("Question de ").append(playerName).append(" : ").append(question);
        messages.add(message("user", prompt.toString()));
        return messages;
    }

    private static void deliver(MinecraftServer server, UUID playerId, Conversation conv, String question,
                                String answer, Throwable error) {
        conv.pending = false;
        conv.lastActivity = System.currentTimeMillis();
        ServerPlayer player = server.getPlayerList().getPlayer(playerId);
        if (player == null) {
            return;
        }
        TiploufNpc npc = findNpc(player, conv);
        if (error != null || answer == null) {
            LOGGER.warn("[Tiplouf] Question from {} failed: {}", player.getGameProfile().getName(),
                    error == null ? "no answer" : error.getMessage());
            say(player, npc, Component.translatable("message.tfother.tiplouf.error"));
            return;
        }
        String text = clean(answer);
        say(player, npc, Component.literal(text));
        if (npc != null) {
            VoiceSupport.speak(player, npc, text);
        }

        JsonObject q = message("user", question);
        q.addProperty("question", question);
        conv.history.addLast(q);
        conv.history.addLast(message("assistant", text));
        while (conv.history.size() > TiploufConfig.HISTORY_TURNS.get() * 2) {
            conv.history.removeFirst();
        }
    }

    private static String clean(String answer) {
        String text = answer.replaceAll("\\*\\*|__|`|^#+\\s*", "")
                .replaceAll("(?m)^#+\\s*", "")
                .replaceAll("\\n{3,}", "\n\n")
                .strip();
        return text.length() > MAX_ANSWER_LENGTH ? text.substring(0, MAX_ANSWER_LENGTH) + "…" : text;
    }

    private static JsonObject message(String role, String content) {
        JsonObject m = new JsonObject();
        m.addProperty("role", role);
        m.addProperty("content", content);
        return m;
    }

    private static TiploufNpc findNpc(ServerPlayer player, Conversation conv) {
        ServerLevel level = player.server.getLevel(conv.dimension);
        if (level == null || level != player.serverLevel()) {
            return null;
        }
        Entity entity = level.getEntity(conv.npc);
        return entity instanceof TiploufNpc npc && npc.isAlive() ? npc : null;
    }

    private static void say(ServerPlayer player, TiploufNpc npc, Component text) {
        Component name = npc != null ? npc.getDisplayName()
                : Component.translatable("entity.tfother.tiplouf").withStyle(ChatFormatting.AQUA);
        player.sendSystemMessage(Component.literal("<").append(name).append("> ")
                .append(text.copy().withStyle(ChatFormatting.WHITE)));
    }

    @SubscribeEvent
    public static void onServerStarted(ServerStartedEvent event) {
        CompletableFuture.runAsync(KnowledgeBase::load)
                .thenCompose(v -> KnowledgeBase.prepareEmbeddings())
                .exceptionally(e -> {
                    LOGGER.error("[Tiplouf] Knowledge base initialization failed", e);
                    return null;
                });
    }

    @SubscribeEvent
    public static void onServerStopped(ServerStoppedEvent event) {
        CONVERSATIONS.clear();
        USAGE.clear();
    }

    @SubscribeEvent
    public static void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        CONVERSATIONS.remove(event.getEntity().getUUID());
        VoiceSupport.forget(event.getEntity().getUUID());
    }
}
