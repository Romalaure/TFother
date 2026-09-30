# TFother

Mod NeoForge 1.21.1 pour le serveur Timefield. Ajoute des PNJ qui ouvrent un wiki intégré en jeu (livre Patchouli, sans lien internet) quand on leur parle (clic droit), et Tiplouf, un PNJ IA qui répond aux questions sur Tensura dans le chat ou à voix haute (Simple Voice Chat).

| PNJ | ID | Apparence | Rôle |
|---|---|---|---|
| Slime | `tfother:slime` | Slime | Wiki Tensura (`tfother:tensura`) |
| Bob | `tfother:bob` | Villageois | Wiki MineColonies (`tfother:minecolonies`) |
| Tiplouf | `tfother:tiplouf` | Joueur (skin Tiplouf) | IA qui répond aux questions sur Tensura et ses addons |

Les PNJ sont immobiles, invincibles (sauf en créatif) et persistants. Ils apparaissent via leur œuf (onglet créatif « Œufs d'apparition ») ou `/summon`.

Le mod doit être installé côté serveur **et** client. Dépendance : **Patchouli**. Optionnel : **Simple Voice Chat**.

## Tiplouf (PNJ IA)

Clic droit sur Tiplouf pour démarrer une conversation : les messages du joueur dans le chat lui sont alors envoyés en privé (ils ne sont pas diffusés aux autres joueurs). La conversation s'arrête quand le joueur dit « au revoir », s'éloigne de plus de 12 blocs ou ne dit rien pendant 2 minutes.

Les appels à l'API OpenAI sont faits uniquement par le serveur. Configuration dans `config/tfother-tiplouf.toml` (créé au premier lancement) :

| Clé | Défaut | Rôle |
|---|---|---|
| `api.apiKey` | vide | Clé API OpenAI. Tant qu'elle est vide, Tiplouf ne répond pas. |
| `api.chatModel` | `gpt-5-nano` | Modèle qui rédige les réponses. |
| `api.reasoningEffort` | `minimal` | À vider pour un modèle sans raisonnement (ex. `gpt-4o-mini`). |
| `api.embeddingModel` | `text-embedding-3-small` | Recherche dans la base de connaissances (vide = recherche par mots-clés). |
| `conversation.dailyQuestionsPerPlayer` | 50 | Limite de questions par joueur et par jour (0 = illimité). |
| `conversation.cooldownSeconds` | 3 | Délai minimum entre deux questions. |

Le fichier est une config COMMON et n'est pas envoyé aux clients : la clé reste sur le serveur.

### Chat vocal (Simple Voice Chat)

Si [Simple Voice Chat](https://modrinth.com/plugin/simple-voice-chat) est installé (dépendance optionnelle), on peut aussi parler à Tiplouf à voix haute pendant une conversation :

- Le micro du joueur est enregistré ; après 0,7 s de silence (ou en relâchant le push-to-talk), l'audio est transcrit en français (`/audio/transcriptions`) et traité comme une question écrite. La transcription s'affiche dans le chat (`[Toi (vocal) → Tiplouf]`).
- Tiplouf lit ses réponses à voix haute (`/audio/speech`) depuis sa position, uniquement pour le joueur concerné (et aussi pour les questions écrites, si le joueur a le chat vocal). Le volume se règle dans la catégorie « Tiplouf » du menu du chat vocal.
- Pendant la conversation, la voix du joueur n'est pas diffusée aux autres joueurs (`voice.privateVoice`). Le micro est ignoré pendant que Tiplouf parle, pour qu'il ne s'entende pas lui-même.

| Clé | Défaut | Rôle |
|---|---|---|
| `voice.enabled` | `true` | Active la voix (sans effet si Simple Voice Chat est absent). |
| `voice.privateVoice` | `true` | La voix du joueur en conversation n'est pas envoyée aux autres. |
| `voice.transcriptionModel` | `gpt-4o-mini-transcribe` | Reconnaissance vocale (ou `whisper-1`, `gpt-4o-transcribe`). |
| `voice.speechModel` | `gpt-4o-mini-tts` | Synthèse vocale. Vide = Tiplouf ne parle pas. |
| `voice.speechVoice` | `fable` | Voix de Tiplouf. |
| `voice.speechInstructions` | voix de pingouin en français | Ton de la voix (`gpt-4o-mini-tts` uniquement). |

### Base de connaissances

Tiplouf répond à partir de `src/main/resources/data/tfother/tiplouf/knowledge.json`, généré depuis les jars du modpack : wikis Patchouli (Tensura Wiki, Elite Tensura, Mortal Cultivation, wiki Tensura de TFother), descriptions des compétences, races et enchantements, objets et comment les obtenir (butin des monstres, coffres, minerais, stations spéciales), zones d'apparition des monstres et structures.

Après une mise à jour des mods Tensura ou du wiki Tensura de TFother :

```sh
python tools/tiplouf/build_knowledge.py
```

L'outil détecte les mods liés à Tensura dans `https://timefield.tidic.fr/res/mods.json` et met les jars en cache dans `tools/tiplouf/.cache/`. Au démarrage, le serveur calcule les embeddings de la base (une seule fois, quelques centimes) et les garde dans `config/tfother/tiplouf-embeddings.bin`.

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

1. Créer une classe qui étend `WikiNpc` (id du livre + clé de message), et ajouter le livre dans `books_content.py`. Pour un PNJ sans livre, étendre `StaticNpc`.
2. L'enregistrer dans `TFother` (entité, attributs, œuf, onglet créatif).
3. Ajouter son renderer dans `client/TFotherClient`.
4. Ajouter les traductions dans `assets/tfother/lang/` et le modèle de l'œuf dans `models/item/`.
