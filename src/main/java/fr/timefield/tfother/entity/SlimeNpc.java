package fr.timefield.tfother.entity;

import net.minecraft.ChatFormatting;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;

/** Slime NPC that opens the official Tensura wiki. */
public class SlimeNpc extends WikiNpc {
    public static final String WIKI_URL = "https://tensura.wiki.gg/";

    public SlimeNpc(EntityType<? extends SlimeNpc> type, Level level) {
        super(type, level, WIKI_URL, "message.tfother.slime.greet", ChatFormatting.AQUA);
    }
}
