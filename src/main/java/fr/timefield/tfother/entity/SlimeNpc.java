package fr.timefield.tfother.entity;

import net.minecraft.ChatFormatting;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;

/** Slime NPC that opens the in-game Tensura wiki. */
public class SlimeNpc extends WikiNpc {

    public SlimeNpc(EntityType<? extends SlimeNpc> type, Level level) {
        super(type, level, "tensura", "message.tfother.slime.greet", ChatFormatting.AQUA);
    }
}
