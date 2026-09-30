package fr.timefield.tfother.entity;

import net.minecraft.ChatFormatting;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;

/** Bob, NPC that presents the in-game MineColonies wiki. */
public class BobNpc extends WikiNpc {

    public BobNpc(EntityType<? extends BobNpc> type, Level level) {
        super(type, level, "minecolonies", "message.tfother.bob.greet", ChatFormatting.GOLD);
    }
}
