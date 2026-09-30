package fr.timefield.tfother.client;

import fr.timefield.tfother.TFother;
import fr.timefield.tfother.entity.TiploufNpc;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;

/** Renders Tiplouf with the player model (slim arms) and his skin. */
public class TiploufRenderer extends HumanoidMobRenderer<TiploufNpc, PlayerModel<TiploufNpc>> {
    private static final ResourceLocation TEXTURE = ResourceLocation.fromNamespaceAndPath(TFother.MODID, "textures/entity/tiplouf.png");

    public TiploufRenderer(EntityRendererProvider.Context context) {
        super(context, new PlayerModel<>(context.bakeLayer(ModelLayers.PLAYER_SLIM), true), 0.5F);
    }

    @Override
    public ResourceLocation getTextureLocation(TiploufNpc entity) {
        return TEXTURE;
    }
}
