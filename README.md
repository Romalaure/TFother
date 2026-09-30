# TFother

Mod NeoForge 1.21.1 pour le serveur Timefield. Ajoute des PNJ qui ouvrent un wiki officiel quand on leur parle (clic droit).

| PNJ | ID | Apparence | Wiki |
|---|---|---|---|
| Slime | `tfother:slime` | Slime | https://tensura.wiki.gg/ |
| Bob | `tfother:bob` | Villageois | https://minecolonies.com/wiki/ |

Les PNJ sont immobiles, invincibles (sauf en créatif) et persistants. Ils apparaissent via leur œuf (onglet créatif « Œufs d'apparition ») ou `/summon`.

Le mod doit être installé côté serveur **et** client.

## Build

```sh
./gradlew build
```

Le jar est généré dans `build/libs/`.

## Ajouter un PNJ

1. Créer une classe qui étend `WikiNpc` (URL + clé de message).
2. L'enregistrer dans `TFother` (entité, attributs, œuf, onglet créatif).
3. Ajouter son renderer dans `client/TFotherClient`.
4. Ajouter les traductions dans `assets/tfother/lang/` et le modèle de l'œuf dans `models/item/`.
