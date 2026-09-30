package fr.timefield.tfother.entity;

import fr.timefield.tfother.tiplouf.Conversations;
import net.minecraft.ChatFormatting;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/** Tiplouf, AI NPC that answers questions about the Tensura mods in the chat. */
public class TiploufNpc extends StaticNpc {

    public TiploufNpc(EntityType<? extends TiploufNpc> type, Level level) {
        super(type, level, ChatFormatting.AQUA);
    }

    @Override
    protected InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (hand != InteractionHand.MAIN_HAND) {
            return InteractionResult.PASS;
        }
        if (player instanceof ServerPlayer serverPlayer) {
            Conversations.start(serverPlayer, this);
        }
        return InteractionResult.sidedSuccess(level().isClientSide);
    }
}
