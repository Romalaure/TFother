package fr.timefield.tfother.tiplouf.voice;

import fr.timefield.tfother.entity.TiploufNpc;
import fr.timefield.tfother.tiplouf.TiploufConfig;
import java.util.UUID;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.fml.ModList;

/**
 * Entry point to Tiplouf's voice from the rest of the mod.
 *
 * <p>Simple Voice Chat is optional: this class never touches its API, so it can be loaded without the
 * mod. Everything that does lives in {@link TiploufVoicePlugin}, only reached once the mod is known to
 * be present.
 */
public final class VoiceSupport {
    private static final boolean LOADED = ModList.get().isLoaded("voicechat");

    private VoiceSupport() {
    }

    /** True when Simple Voice Chat is running and Tiplouf's voice is enabled. */
    public static boolean isAvailable() {
        return LOADED && TiploufConfig.VOICE_ENABLED.get() && TiploufVoicePlugin.isReady();
    }

    /** Reads Tiplouf's answer aloud to the player, if they have the voice chat. */
    public static void speak(ServerPlayer player, TiploufNpc npc, String text) {
        if (isAvailable()) {
            TiploufVoicePlugin.speak(player, npc, text);
        }
    }

    /** Drops the player's recording and stops Tiplouf talking to them. */
    public static void forget(UUID player) {
        if (LOADED) {
            TiploufVoicePlugin.forget(player);
        }
    }
}
