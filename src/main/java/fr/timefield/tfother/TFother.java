package fr.timefield.tfother;

import fr.timefield.tfother.entity.BobNpc;
import fr.timefield.tfother.entity.SlimeNpc;
import fr.timefield.tfother.entity.WikiNpc;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(TFother.MODID)
public class TFother {
    public static final String MODID = "tfother";

    private static final DeferredRegister<EntityType<?>> ENTITIES = DeferredRegister.create(Registries.ENTITY_TYPE, MODID);
    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MODID);

    public static final DeferredHolder<EntityType<?>, EntityType<SlimeNpc>> SLIME = ENTITIES.register("slime",
            () -> EntityType.Builder.of(SlimeNpc::new, MobCategory.MISC)
                    .sized(1.04F, 1.04F)
                    .clientTrackingRange(10)
                    .build(MODID + ":slime"));

    public static final DeferredHolder<EntityType<?>, EntityType<BobNpc>> BOB = ENTITIES.register("bob",
            () -> EntityType.Builder.of(BobNpc::new, MobCategory.MISC)
                    .sized(0.6F, 1.95F)
                    .eyeHeight(1.62F)
                    .clientTrackingRange(10)
                    .build(MODID + ":bob"));

    public static final DeferredItem<DeferredSpawnEggItem> SLIME_SPAWN_EGG = ITEMS.register("slime_spawn_egg",
            () -> new DeferredSpawnEggItem(SLIME, 0x5FB8E6, 0xBFE9FF, new Item.Properties()));

    public static final DeferredItem<DeferredSpawnEggItem> BOB_SPAWN_EGG = ITEMS.register("bob_spawn_egg",
            () -> new DeferredSpawnEggItem(BOB, 0x8B5A2B, 0xF2C94C, new Item.Properties()));

    public TFother(IEventBus modBus) {
        ENTITIES.register(modBus);
        ITEMS.register(modBus);
        modBus.addListener(this::registerAttributes);
        modBus.addListener(this::addCreative);
    }

    private void registerAttributes(EntityAttributeCreationEvent event) {
        event.put(SLIME.get(), WikiNpc.createAttributes().build());
        event.put(BOB.get(), WikiNpc.createAttributes().build());
    }

    private void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.SPAWN_EGGS) {
            event.accept(SLIME_SPAWN_EGG);
            event.accept(BOB_SPAWN_EGG);
        }
    }
}
