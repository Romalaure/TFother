package fr.timefield.tfother.client;

import com.mojang.blaze3d.vertex.PoseStack;
import fr.timefield.tfother.entity.SlimeNpc;
import net.minecraft.client.model.SlimeModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.SlimeOuterLayer;
import net.minecraft.resources.ResourceLocation;

/** Renders the NPC with the vanilla slime model at size 2. */
public class SlimeNpcRenderer extends MobRenderer<SlimeNpc, SlimeModel<SlimeNpc>> {
    private static final ResourceLocation TEXTURE = ResourceLocation.withDefaultNamespace("textures/entity/slime/slime.png");
    private static final float SIZE = 2.0F;

    public SlimeNpcRenderer(EntityRendererProvider.Context context) {
        super(context, new SlimeModel<>(context.bakeLayer(ModelLayers.SLIME)), 0.25F * SIZE);
        addLayer(new SlimeOuterLayer<>(this, context.getModelSet()));
    }

    @Override
    protected void scale(SlimeNpc entity, PoseStack poseStack, float partialTick) {
        poseStack.scale(0.999F, 0.999F, 0.999F);
        poseStack.translate(0.0F, 0.001F, 0.0F);
        poseStack.scale(SIZE, SIZE, SIZE);
    }

    @Override
    public ResourceLocation getTextureLocation(SlimeNpc entity) {
        return TEXTURE;
    }
}
