package fr.timefield.tfother.entity;

import fr.timefield.tfother.TFother;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import vazkii.patchouli.api.PatchouliAPI;

/** Stationary, invulnerable NPC that opens an in-game Patchouli wiki when talked to. */
public abstract class WikiNpc extends PathfinderMob {
    private final ResourceLocation book;
    private final String greetKey;

    protected WikiNpc(EntityType<? extends WikiNpc> type, Level level, String bookId, String greetKey, ChatFormatting nameColor) {
        super(type, level);
        this.book = ResourceLocation.fromNamespaceAndPath(TFother.MODID, bookId);
        this.greetKey = greetKey;
        setInvulnerable(true);
        setPersistenceRequired();
        setCustomName(type.getDescription().copy().withStyle(nameColor));
        setCustomNameVisible(true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return PathfinderMob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.0D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(1, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(2, new RandomLookAroundGoal(this));
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

    @Override
    public boolean removeWhenFarAway(double distance) {
        return false;
    }

    @Override
    public boolean isPushable() {
        return false;
    }

    @Override
    protected void doPush(Entity entity) {
    }

    @Override
    public boolean canBeLeashed() {
        return false;
    }
}
