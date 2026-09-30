package fr.timefield.tfother.entity;

import net.minecraft.ChatFormatting;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.Level;

/** Bob, NPC that presents the official MineColonies wiki. */
public class BobNpc extends WikiNpc {
    public static final String WIKI_URL = "https://minecolonies.com/wiki/";

    public BobNpc(EntityType<? extends BobNpc> type, Level level) {
        super(type, level, WIKI_URL, "message.tfother.bob.greet", ChatFormatting.GOLD);
    }
}
