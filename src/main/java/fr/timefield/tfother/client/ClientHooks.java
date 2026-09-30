package fr.timefield.tfother.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.ConfirmLinkScreen;

/** Client-only helpers; only referenced behind a level().isClientSide check. */
public final class ClientHooks {
    private ClientHooks() {
    }

    public static void openWiki(String url) {
        ConfirmLinkScreen.confirmLinkNow(Minecraft.getInstance().screen, url);
    }
}
