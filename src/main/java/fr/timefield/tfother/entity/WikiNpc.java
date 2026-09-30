package fr.timefield.tfother.entity;

import fr.timefield.tfother.TFother;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import vazkii.patchouli.api.PatchouliAPI;

/** Stationary, invulnerable NPC that opens an in-game Patchouli wiki when talked to. */
public abstract class WikiNpc extends StaticNpc {
    private final ResourceLocation book;
    private final String greetKey;

    protected WikiNpc(EntityType<? extends WikiNpc> type, Level level, String bookId, String greetKey, ChatFormatting nameColor) {
        super(type, level, nameColor);
        this.book = ResourceLocation.fromNamespaceAndPath(TFother.MODID, bookId);
        this.greetKey = greetKey;
    }

    @Override
    protected InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (hand != InteractionHand.MAIN_HAND) {
            return InteractionResult.PASS;
        }
        if (player instanceof ServerPlayer serverPlayer) {
            serverPlayer.sendSystemMessage(Component.literal("<").append(getDisplayName()).append("> ")
                    .append(Component.translatable(greetKey).withStyle(ChatFormatting.WHITE)));
            PatchouliAPI.get().openBookGUI(serverPlayer, book);
        }
        return InteractionResult.sidedSuccess(level().isClientSide);
    }
}
