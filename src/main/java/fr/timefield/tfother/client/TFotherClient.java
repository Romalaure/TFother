package fr.timefield.tfother.client;

import fr.timefield.tfother.TFother;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

@EventBusSubscriber(modid = TFother.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class TFotherClient {
    private TFotherClient() {
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(TFother.SLIME.get(), SlimeNpcRenderer::new);
        event.registerEntityRenderer(TFother.BOB.get(), BobNpcRenderer::new);
    }
}
