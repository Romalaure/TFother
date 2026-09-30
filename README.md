# TFother

Mod NeoForge 1.21.1 pour le serveur Timefield. Ajoute des PNJ qui ouvrent un wiki intégré en jeu (livre Patchouli, sans lien internet) quand on leur parle (clic droit).

| PNJ | ID | Apparence | Livre |
|---|---|---|---|
| Slime | `tfother:slime` | Slime | Wiki Tensura (`tfother:tensura`) |
| Bob | `tfother:bob` | Villageois | Wiki MineColonies (`tfother:minecolonies`) |

Les PNJ sont immobiles, invincibles (sauf en créatif) et persistants. Ils apparaissent via leur œuf (onglet créatif « Œufs d'apparition ») ou `/summon`.

Le mod doit être installé côté serveur **et** client. Dépendance : **Patchouli**.

## Build

```sh
./gradlew build
```

Le jar est généré dans `build/libs/`.

## Modifier les wikis

Le texte des livres est dans `tools/books/books_content.py` (résumé en français de tensura.wiki.gg et minecolonies.com/wiki). Après modification :

```sh
python tools/books/gen_books.py      # régénère les JSON Patchouli (pagination automatique)
python tools/books/check_icons.py <minecraft-resources.jar> <tensura.jar> <minecolonies.jar>
```

Ne pas éditer à la main les JSON générés dans `patchouli_books/`.

## Ajouter un PNJ

1. Créer une classe qui étend `WikiNpc` (id du livre + clé de message), et ajouter le livre dans `books_content.py`.
2. L'enregistrer dans `TFother` (entité, attributs, œuf, onglet créatif).
3. Ajouter son renderer dans `client/TFotherClient`.
4. Ajouter les traductions dans `assets/tfother/lang/` et le modèle de l'œuf dans `models/item/`.
