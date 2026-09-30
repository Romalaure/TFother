# -*- coding: utf-8 -*-
"""Content of the in-game wikis opened by the TFother NPCs.

Each entry is a list of text blocks (Patchouli formatting: $(l)bold$(), $(li) bullet,
$(br) line break). gen_books.py paginates the blocks automatically.
Sources: tensura.wiki.gg and minecolonies.com/wiki (summarised and translated).
"""

B = "$(l)"
E = "$()"


def li(*items):
    return "".join("$(li)" + i for i in items)


# ---------------------------------------------------------------------------
# TENSURA
# ---------------------------------------------------------------------------

TENSURA_RACES = [
    # id, name, icon, difficulty, mp, ap, hp, alignment, description, ability, evolution
    ("human", "Humain", "minecraft:iron_sword", "Difficile", "50 - 70", "760 - 1 140", "20", "Aucun",
     "Race faible mais nombreuse, qui compte sur la technique plutôt que la force. Peu de magicules : on mise surtout sur les Battlewills.",
     "Aucune.",
     li("Humain Éclairé : 100 000 EP ou Harvest Festival", "Vampire : consommer 5 Zane Blood")),
    ("elf", "Elfe", "minecraft:oak_sapling", "Difficile", "320 - 600", "600 - 800", "20", "Aucun",
     "Race sprite descendant des élémentaires du vent, très douée pour la magie élémentaire.",
     "Aucune. Plus de chances d'obtenir un esprit du Vent.",
     li("Elfe Éclairé : 100 000 EP ou Harvest Festival")),
    ("dwarf", "Nain", "minecraft:iron_pickaxe", "Difficile", "80 - 120", "720 - 1 080", "24", "Aucun",
     "Race sprite descendant des élémentaires de la terre, dotée d'une volonté immense.",
     "Aucune. Plus de chances d'obtenir un esprit de la Terre.",
     li("Nain Éclairé : 100 000 EP ou Harvest Festival")),
    ("merfolk", "Homme-poisson", "minecraft:tropical_fish", "Intermédiaire", "400 - 600", "500 - 600", "24", "Aucun",
     "Race sprite descendant des élémentaires de l'eau, redoutable dans l'eau.",
     "Respiration aquatique innée. Plus de chances d'obtenir un esprit de l'Eau.",
     li("Homme-poisson Éclairé : 100 000 EP ou Harvest Festival")),
    ("beastfolk", "Homme-bête", "minecraft:bone", "Facile", "300 - 600", "1 500 - 2 500", "22", "Aucun",
     "Peut passer librement de sa forme animale à une forme humaine. Physique et régénération hors normes.",
     "Transformation bestiale.",
     li("Seigneur Bête : 100 000 EP ou Harvest Festival")),
    ("harpy", "Harpie", "minecraft:feather", "Facile", "1 500 - 2 500", "300 - 600", "30", "Majin",
     "Proche des hommes-bêtes, spécialisée dans le combat aérien.",
     "Se propulse avec ses ailes et plane comme avec des élytres.",
     li("Reine Harpie : 200 000 EP")),
    ("goblin", "Gobelin", "minecraft:rotten_flesh", "Difficile", "700", "300", "12", "Aucun",
     "Demi-humains sprites, descendants de nains et d'oni.",
     "Aucune. Plus de chances d'obtenir un esprit du Feu.",
     li("Hobgobelin : 2 000 EP ou Harvest Festival")),
    ("lizardman", "Homme-lézard", "minecraft:turtle_scute", "Intermédiaire", "100 - 200", "600 - 800", "24", "Aucun",
     "Peuple écailleux descendant des dragons. Ses pieds palmés l'avantagent en terrain humide.",
     "Aucune.",
     li("Dragonewt : consommer 10 Dragon Essence ou Harvest Festival")),
    ("ogre", "Ogre", "minecraft:blaze_powder", "Facile", "300 - 600", "1 500 - 2 500", "26", "Aucun",
     "Race sprite descendant des élémentaires du feu, aux capacités physiques immenses.",
     "Aucune. Plus de chances d'obtenir un esprit du Feu.",
     li("Kijin : obtenir un esprit ou Harvest Festival", "Ogre Éclairé : 100 000 EP")),
    ("orc", "Orc", "minecraft:porkchop", "Intermédiaire", "50 - 100", "400 - 600", "28", "Aucun",
     "Hommes-bêtes ayant perdu la capacité de changer de forme. Plus forts que la moyenne.",
     "Aucune.",
     li("Orc Supérieur : 5 000 EP ou Harvest Festival")),
    ("slime", "Slime", "minecraft:slime_ball", "Extrême", "200 - 500", "200 - 500", "10", "Majin",
     "Race spectrale sans ambition, passive mais impitoyable une fois provoquée. La race de Rimuru !",
     "Super saut chargé. Réduit de 50 % les dégâts physiques subis (ne se cumule pas avec les résistances physiques).",
     li("Slime de Métal : consommer 100 Magic Ore avec Absorb & Dissolve", "Slime Démon : s'éveiller (Vrai Seigneur Démon / Vrai Héros)")),
    ("wight", "Wight", "minecraft:skeleton_skull", "Difficile", "2 000 - 3 000", "100 - 500", "20", "Majin",
     "Mort-vivant squelettique demi-spirituel, très affaibli par le soleil.",
     "Les morts-vivants sont passifs. Au soleil : Fragilité, Faiblesse, Fatigue, Lenteur III et brûlure (un casque évite la brûlure, pas sous un toit ni sous la pluie).",
     li("Roi Wight (Wight King)")),
    ("ghoul", "Goule", "minecraft:spider_eye", "Difficile", "2 000 - 3 000", "1 000 - 2 000", "14", "Majin",
     "Mort-vivant affamé, point de départ de la lignée des vampires.",
     "Aucune.",
     li("Vampire : consommer 1 Zane Blood ou Harvest Festival")),
    ("lesser_daemon", "Démon Mineur", "minecraft:crying_obsidian", "Facile", "5 000 - 6 000", "2 000 - 3 000", "40", "Majin",
     "Le plus bas rang des démons, né dans le Royaume Démoniaque.",
     "Vol créatif (non affecté par Magic Jamming). Sans nom ni éveil, l'EP est plafonné dans le monde physique.",
     li("Démon Supérieur : 20 000 EP ou Harvest Festival")),
    ("giant", "Géant", "minecraft:iron_block", "Facile", "6 000 - 8 000", "4 000 - 6 000", "50", "Majin",
     "Peut changer de taille à volonté, devenant immense et bien plus fort.",
     "Changement de taille.",
     li("Géant Ancien : 300 000 EP + 20 Ancient Debris")),
]


def race_entry(r):
    rid, name, icon, diff, mp, ap, hp, align, desc, ability, evo = r
    return {
        "id": rid, "name": name, "icon": icon,
        "text": [
            desc,
            li(B + "Difficulté" + E + " : " + diff, B + "PV" + E + " : " + hp,
               B + "MP" + E + " : " + mp, B + "AP" + E + " : " + ap, B + "Alignement" + E + " : " + align),
            B + "Capacité raciale" + E + "$(br)" + ability,
            B + "Évolution" + E + evo,
        ],
    }


TENSURA = {
    "name": "Wiki Tensura",
    "subtitle": "Tensura: Reincarnated",
    "landing_text": "Bienvenue, voyageur réincarné ! Je suis le Slime et voici tout ce qu'il faut savoir sur $(l)Tensura: Reincarnated$() : races, EP, compétences, esprits, boss et éveils.$(br2)Choisis une catégorie pour commencer.",
    "model": "patchouli:book_blue",
    "categories": [
        {
            "id": "debuter", "name": "Débuter", "icon": "tensura:magic_stone",
            "description": "Les premiers pas dans ce monde : choix de la race, premiers équipements et progression.",
            "entries": [
                {"id": "premiers_pas", "name": "Premiers pas", "icon": "minecraft:compass", "text": [
                    "À ta première connexion, un menu te propose de choisir ta $(l)race$(). Chaque race rend la progression plus ou moins difficile (voir la catégorie Races).",
                    "Tu reçois aussi une $(l)compétence unique$() (Unique Skill) au hasard dès le départ.",
                    "Pour devenir plus fort, il faut tuer des monstres : chaque kill te donne de l'$(l)EP$() et augmente tes magicules maximum. Plus le monstre est fort, plus tu gagnes d'EP.",
                    "Ouvre ton menu de personnage avec la touche $(l)B$() pour voir tes stats, ta race et tes compétences.",
                ]},
                {"id": "equipement", "name": "Premier équipement", "icon": "tensura:smithing_bench", "text": [
                    "En tuant des monstres, tu obtiens du $(l)Monster Leather$() (cuir de monstre). Il sert à fabriquer une armure qui évolue quand tu gagnes de l'EP.",
                    "Pour la fabriquer, il faut un $(l)Smithing Bench$() : 2 fers, 3 papiers, 1 table de craft et 2 planches.",
                    "Voir aussi l'entrée $(l)Évolution de l'équipement$() dans la catégorie Mécaniques.",
                ]},
                {"id": "minerai_magique", "name": "Minerai magique", "icon": "tensura:magic_ore", "text": [
                    "Après le diamant, l'étape suivante est le $(l)Magic Ore$(). Il se trouve entre les couches $(l)-25 et -31$() (le mieux : -29).",
                    "Il faut une $(l)pioche en netherite$() pour le miner (ou une pioche en os de dragon avec Ice and Fire). Fortune est vivement conseillé.",
                    "Prévois environ 19 obsidiennes : 10 pour le portail du Nether, 4 pour la table d'enchantement et 5 pour le $(l)Kiln$().",
                    "Fonds le minerai magique dans le Kiln pour obtenir des lingots de $(l)Low Magisteel$(), la base de l'équipement de milieu de jeu.",
                ]},
                {"id": "progression", "name": "Progression", "icon": "minecraft:experience_bottle", "text": [
                    B + "Milieu de partie" + E + "$(br)Monte ton équipement en Magisteel et vise tes évolutions. Les piglins, piglins zombies et wither squelettes du Nether donnent un bon EP.",
                    "Récupère des esprits à l'$(l)Arbre du Labyrinthe$() et apprends la compétence $(l)Sage$() (maîtriser 20 magies ou Battlewills) pour progresser plus vite.",
                    B + "Fin de partie" + E + "$(br)Fais ton éveil après $(l)1 million d'EP$() ou plus. Pour les boss de fin, vise environ $(l)2 millions d'EP$() et des compétences maîtrisées.",
                    B + "Farm d'EP" + E + li("Farm d'endermen dans l'End (AFK)", "Chasse aux Sissie dans les océans", "Combats de boss"),
                ]},
            ],
        },
        {
            "id": "mecaniques", "name": "Mécaniques", "icon": "minecraft:clock",
            "description": "EP, magicules, aura, utilisation des compétences, évolution de l'équipement et parchemins.",
            "entries": [
                {"id": "ep", "name": "EP, Magicules et Aura", "icon": "minecraft:nether_star", "text": [
                    "L'$(l)EP$() (Existence Points) mesure la puissance d'une créature : c'est la somme de tes $(l)Magicules (MP)$() et de ton $(l)Aura (AP)$(). L'EP sert à évoluer, s'éveiller et apprendre certaines compétences.",
                    B + "Gain" + E + "$(br)Par défaut, tu gagnes $(l)3 %$() de l'EP du monstre tué. Si tu es bien plus fort que lui, le gain baisse de 1 % par multiple d'écart (réduction max 90 %).",
                    B + "Répartition" + E + li("Non-Majin : 2/3 en Aura, 1/3 en Magicules", "Majin : 2/3 en Magicules, 1/3 en Aura"),
                    B + "Mort" + E + "$(br)Chaque mort te fait perdre $(l)5 %$() de ton EP (réglable par gamerule).",
                ]},
                {"id": "magicules", "name": "Régénérer ses magicules", "icon": "tensura:low_quality_magic_crystal", "text": [
                    "La régénération de magicules est fixe par défaut. Elle augmente avec la gravure (engraving) $(l)Magicule Absorption$() sur l'armure, ou dans certains lieux :",
                    li("Dimensions : Enfer (Hell) et Labyrinthe", "Biomes : Barren Lands et Ancient Forest"),
                    B + "Recharge complète instantanée" + E + li("Manger un Magic Crystal avec Absorb & Dissolve ou Predator", "Activer Beast Transformation", "Mourir (déconseillé : perte d'EP)"),
                ]},
                {"id": "competences", "name": "Utiliser ses compétences", "icon": "minecraft:enchanted_book", "text": [
                    B + "Apprendre" + E + "$(br)Une compétence non apprise est grisée dans le menu. Équipe-la dans un emplacement et active-la avec sa touche : chaque essai rapproche de l'apprentissage. À $(l)100 points$(), elle est apprise.",
                    "Chaque essai a $(l)10 %$() de chances d'échouer : tu perds 1 à 3 points et subis Cécité, Paralysie ou Folie.",
                    "Apprendre coûte des MP max : $(l)100$() pour une Common Skill, $(l)1 000$() pour une Extra Skill. Sage, Great Sage, Mathematician et Cook accélèrent l'apprentissage.",
                    B + "Maîtrise" + E + "$(br)Utiliser une compétence donne des points de maîtrise (sans échec). Toucher une cible donne x3, tuer x5. Certains modes demandent la maîtrise complète.",
                    B + "Presets" + E + "$(br)9 presets de 3 compétences (27 au total). Change de preset avec $(l)Alt + molette$() ou Alt + numéro.",
                    B + "Modes" + E + "$(br)Change le mode d'une compétence avec $(l)Alt + touche de l'emplacement$().",
                    B + "Dans le menu" + E + li("Clic gauche : équiper", "Clic droit : voir les infos", "Clic molette : retirer"),
                    B + "Filtres de recherche" + E + li("f:learned / f:learning", "f:mastered / f:unmastered", "f:toggleable / f:toggledon", "f:oncooldown / f:offcooldown", "f:active / f:passive"),
                ]},
                {"id": "evolution_equipement", "name": "Évolution de l'équipement", "icon": "tensura:monster_leather_chestplate_a", "text": [
                    "Le Monster Leather et le Magisteel $(l)évoluent$() : utilise-les ou porte-les en tuant des créatures pour leur donner de l'EP.",
                    B + "Monster Leather" + E + li("D → C : 2 500 EP", "C → B : 5 000 EP", "B → A : 8 000 EP", "A → Special A : 80 000 EP"),
                    B + "Magisteel" + E + li("Low → High : 18 000 EP", "High → Pure : 52 000 EP", "Pure → Adamantite : 225 000 EP", "Adamantite → Hihi'irokane : 750 000 EP"),
                    "Le $(l)Mithril$() passe en Adamantite (225 000 EP) puis Hihi'irokane. L'$(l)Orichalcum$() passe directement en Hihi'irokane (750 000 EP).",
                ]},
                {"id": "parchemins", "name": "Parchemins de réinitialisation", "icon": "tensura:race_reset_scroll", "text": [
                    B + "Skill Reset Scroll" + E + "$(br)Papier + lingot de Pure Magisteel + lingot d'Orichalcum + Magic Stone + Monster Leather (A). Réinitialise toutes tes compétences sauf les intrinsèques de ta race. Attention : il ne redonne pas de compétence unique !",
                    B + "Race Reset Scroll" + E + "$(br)Papier + lingot de Mithril + Monster Leather (A) + Magic Stone. Réinitialise stats, nom, éveil, esprits, résistances et race.",
                    B + "Character Reset Scroll" + E + "$(br)Papier + lingot de Pure Magisteel + Magic Stone + Monster Leather (A). Remet tout à zéro, comme une nouvelle réincarnation.",
                    B + "Magie Reincarnation" + E + "$(br)Permet de rechoisir sa race en gardant compétences non intrinsèques, esprits, éveil et 75 % de ses MP/AP max. Maîtrisée, elle débloque les races non standard.",
                ]},
                {"id": "alignement", "name": "Alignement : Saint et Majin", "icon": "minecraft:totem_of_undying", "text": [
                    B + "Saint (Holy)" + E + "$(br)Obtenu en atteignant la 3e évolution d'une race non Majin (Human Saint, Elf Saint, Mystic Oni, Spirit Boar, True Dragonewt...). Nom de race en jaune.",
                    "Un Saint ne peut plus devenir Majin, ni Vrai Seigneur Démon (sauf alignement Chaos via la compétence Reverser).",
                    B + "Majin" + E + "$(br)Monstre intelligent. Nom de race en violet. On le devient en commençant avec une race Majin, avec un Marionette Heart, en mourant d'empoisonnement aux magicules ou (5 %) au Demon Lord Haki.",
                    "Certaines évolutions rendent Majin : Vampire, Wicked Oni, Orc Lord. Un Majin de naissance ne peut pas devenir Vrai Héros.",
                    B + "Bonus communs" + E + li("Plus besoin d'air sous l'eau", "La faim ne descend pas sous 18"),
                ]},
            ],
        },
        {
            "id": "races", "name": "Races", "icon": "minecraft:player_head",
            "description": "Les races jouables au départ, leurs statistiques et leur première évolution.",
            "entries": [
                {"id": "apercu", "name": "Aperçu des races", "icon": "minecraft:book", "text": [
                    "Chaque race a ses stats de départ (PV, MP, AP), une difficulté et une ligne d'évolutions. Les races marquées $(l)Majin$() gagnent surtout des magicules.",
                    B + "Lignées d'évolution" + E + li("Humain → Éclairé → Saint → Divin", "Gobelin → Hobgobelin → ... → Oni Divin", "Homme-lézard → Dragonewt → Vrai Dragonewt → Dragon Divin", "Orc → Orc Supérieur → Orc Lord → Orc Disaster", "Slime → Slime de Métal → Slime Démon → Dieu Slime", "Goule → Vampire → ... → Vampire Divin", "Démon Mineur → Supérieur → Archi → Seigneur Démon"),
                    "Beaucoup d'évolutions peuvent aussi être obtenues pendant un $(l)Harvest Festival$() (voir Éveils).",
                ]},
            ] + [race_entry(r) for r in TENSURA_RACES],
        },
        {
            "id": "capacites", "name": "Compétences et magie", "icon": "minecraft:enchanted_book",
            "description": "Types de compétences, magie aspectuelle et spirituelle, Battlewills et compétences utiles.",
            "entries": [
                {"id": "types", "name": "Types de compétences", "icon": "minecraft:writable_book", "text": [
                    "Les compétences sont des formules gravées dans l'âme. Il en existe plusieurs rangs :",
                    li(B + "Intrinsèques" + E + " : liées à ta race", B + "Common" + E + " : coût 100 MP max", B + "Extra" + E + " : coût 1 000 MP max", B + "Unique" + E + " : très puissantes (Great Sage, Predator...)", B + "Ultimate" + E + " : le sommet", B + "Résistances" + E + " : deviennent des Nullifications à l'éveil"),
                    B + "Compétences utiles" + E + li("Magic Sense : vision nocturne et voir les monstres à travers les murs", "Corrosion : manger 100 chairs putréfiées", "Poison : manger 100 yeux d'araignée", "Sage : maîtriser 20 magies/Battlewills"),
                ]},
                {"id": "magie", "name": "Magie", "icon": "minecraft:blaze_rod", "text": [
                    B + "Magie aspectuelle" + E + "$(br)Écoles : Feu, Eau, Terre, Vent, Espace, Explosion, Foudre, Glace, Gravité, Renforcement, Soin, Illusion, Mental, Barrière et divers (Reincarnation, Analyze, Flight...).",
                    B + "Magie spirituelle" + E + "$(br)Obtenue grâce aux $(l)esprits$(). Rangs : Lesser, Intermediate, Greater. Exemples : Fire Bolt, Hellfire, Megiddo, Darkness Cannon.",
                    B + "Invocation" + E + "$(br)Summon Medium Elemental, Summon Greater Elemental, Summon Hound Dog.",
                ]},
                {"id": "battlewills", "name": "Battlewills", "icon": "tensura:battlewill_manual", "text": [
                    "Les Battlewills sont des arts de combat qui utilisent l'aura. On les apprend avec des $(l)Battlewill Manuals$(), trouvés dans les coffres qui contiennent des pommes dorées (temples du désert, donjons à spawner...).",
                    B + "Mêlée" + E + " : Aura Slash, Aura Sword, Heavy Slash, Roaring Lion Punch...",
                    B + "Projectiles" + E + " : Magic Bullet, Ogre Flame, Ogre-sword Cannon...",
                    B + "Utilitaires" + E + " : Air Flight, Aura Shield, Instant-move, Formhide...",
                ]},
            ],
        },
        {
            "id": "esprits", "name": "Esprits et Labyrinthe", "icon": "minecraft:amethyst_shard",
            "description": "L'Arbre du Labyrinthe, le Colosse Élémentaire et la prière pour obtenir des esprits.",
            "entries": [
                {"id": "labyrinthe", "name": "L'Arbre du Labyrinthe", "icon": "minecraft:oak_log", "text": [
                    "L'$(l)Arbre du Labyrinthe$() apparaît rarement dans les $(l)Ancient Forest$(). Un nain cartographe de niveau maître vend une carte qui y mène.",
                    "Il faut au moins $(l)8 000 EP$() pour entrer, sinon l'empoisonnement aux magicules te tue et t'expulse (sans perte d'EP). Les magicules s'y régénèrent plus vite.",
                    "À l'intérieur, le $(l)Colosse Élémentaire$() garde le passage. Que tu le battes ou que tu meures, tu pourras ensuite aller prier. Le vaincre donne un bloc de Pure Magisteel (qui permet de le réinvoquer).",
                ]},
                {"id": "priere", "name": "Prier pour un esprit", "icon": "minecraft:soul_lantern", "text": [
                    "Monte jusqu'au cercle de prière et reste $(l)accroupi 20 secondes$() sur le chemin de prière.",
                    B + "Chances" + E + li("Lesser : 40 %", "Medium : 20 %", "Greater : 10 %", "Lord : 1 % (si tu as déjà un Medium ou Greater de l'élément)"),
                    "Ensuite, $(l)20 minutes$() de recharge. Prier trop tôt te renvoie à l'entrée. Commande : $(l)/tensura get spirit cooldown$().",
                    "Bonus raciaux (Lesser garanti, Medium et Greater x2) : Nain → Terre, Elfe → Vent, Homme-poisson → Eau, Gobelin et Ogre → Feu.",
                ]},
                {"id": "rangs", "name": "Rangs et éléments", "icon": "minecraft:glow_berries", "text": [
                    li(B + "Lesser" + E + " : la manipulation de l'élément + un sort", B + "Medium" + E + " : plusieurs sorts, invocable", B + "Greater" + E + " : tous les sorts, invocable, requis pour le Vrai Héros", B + "Lord" + E + " : très rare, équivalent au Greater"),
                    B + "Sorts Medium / Greater" + E + li("Feu : Fire Bolt, Fire Breath / Flare Circle, Hellfire", "Eau : Acid Rain, Water Cutter / Blizzard, Megiddo", "Terre : Earth Spikes, Earth Storm / Earth Jail, Magma Surge", "Vent : Lightning Lance, Wind Blade / Aerial Blade, Electro Blast"),
                    li("Espace : Gate, Shrink, Teleport / Swipe", "Lumière : Solar Beam, Solar Wave / Solar Flare, Solar Rain", "Ténèbres : Dark Cube, Shadow Bind / Darkness Cannon, True Darkness"),
                    "Voir tes esprits : $(l)/tensura get spirit$().",
                ]},
            ],
        },
        {
            "id": "boss", "name": "Boss", "icon": "minecraft:wither_skeleton_skull",
            "description": "Les boss du milieu et de la fin de partie, comment les trouver et ce qu'ils donnent.",
            "entries": [
                {"id": "orc_lord", "name": "Orc Lord", "icon": "minecraft:porkchop", "text": [
                    "Boss du début du milieu de partie. Invoque des orcs et ses attaques infligent $(l)Corrosion$(), qui détruit l'armure.",
                    "Butin : Royal Blood et viande. Tu peux y apprendre la compétence Corrosion.",
                    B + "Orc Disaster" + E + "$(br)Si un Orc Lord gagne $(l)200 000 EP$() (en lui faisant tuer des subordonnés à fort EP), il évolue en Orc Disaster, un boss de fin de partie.",
                ]},
                {"id": "shizu", "name": "Shizu et Ifrit", "icon": "minecraft:blaze_powder", "text": [
                    "Boss de fin de milieu de partie. La 1re phase est simple ; en « mourant », Shizu libère $(l)Ifrit$(), très résistant aux attaques physiques.",
                    "Utilise des compétences qui contournent ou dégradent les résistances, ou de la magie.",
                    "Butin : drops d'Ifrit, puis Shizu donne l'$(l)Anti-Magic Mask$() et son schéma.",
                ]},
                {"id": "supermassive_slime", "name": "Supermassive Slime", "icon": "tensura:slime_core", "text": [
                    "Peut apparaître à la place d'un slime normal. Inflige des dégâts de corrosion : une résistance ou nullification à la corrosion le rend inoffensif.",
                    "Il a Ultraspeed Regen : attaque ses PV spirituels ou applique Severance.",
                    "Butin : Slime Core et Slime Chunk. Nourris un slime avec des Slime Cores pour avoir ton propre Supermassive Slime !",
                ]},
                {"id": "charybdis", "name": "Charybdis", "icon": "tensura:charybdis_core", "text": [
                    "Trouve un $(l)Charybdis Core$() dans une Charybdis Cave. Pose-le et tue des monstres autour pour le charger en EP, puis clic droit pour invoquer Charybdis.",
                    "Astuce : invoque-la dans une grotte pour qu'elle ne s'envole pas, ou utilise une attaque à distance puissante.",
                    "Butin : schéma de Charybdis Scalemail, écailles et viande de Charybdis.",
                ]},
                {"id": "gazel", "name": "Gazel Dwargo", "icon": "minecraft:netherite_axe", "text": [
                    "Le roi des nains. Il faut $(l)100 de réputation$() positive (commerce, protéger les nains) ou négative (les attaquer).",
                    "La réputation négative est plus rapide mais ne permet qu'un seul combat et bloque le commerce. La positive permet de l'affronter à volonté et baisse les prix.",
                    "Entre dans son arène par le Royal Warp Pad des villages nains. Butin : son arme Rhuk et un Battlewill exclusif.",
                ]},
                {"id": "hinata", "name": "Hinata Sakaguchi", "icon": "minecraft:golden_sword", "text": [
                    "Boss de fin de partie qui invoque tous les Greater Spirits. $(l)Fault Field$() la rend intouchable sauf dégâts spirituels, spatiaux ou mentaux.",
                    "Attention à $(l)Disintegration$() : tue instantanément si elle touche. Elle a énormément de résistances, privilégie les compétences Bypass/Degrade.",
                    "Butin possible : ses armes et l'armure Holy Armorments.",
                ]},
            ],
        },
        {
            "id": "eveils", "name": "Éveils", "icon": "minecraft:dragon_egg",
            "description": "Devenir Vrai Seigneur Démon ou Vrai Héros, et le Harvest Festival.",
            "entries": [
                {"id": "seigneur_demon", "name": "Vrai Seigneur Démon", "icon": "minecraft:wither_rose", "text": [
                    B + "Graine" + E + "$(br)Un $(l)Majin$() avec $(l)200 000 EP$() obtient la Demon Lord Seed.",
                    B + "Âmes" + E + "$(br)Avec la graine, tuer des créatures donne des âmes : $(l)2 000 EP = 1 âme$().",
                    B + "Éveil" + E + "$(br)À $(l)10 000 âmes$(), un bouton apparaît dans le menu de statut. À 20 000 âmes, l'éveil est forcé.",
                    B + "Effets" + E + li("EP x3", "Stats des subordonnés PNJ doublées", "Évolution de ta race", "Résistances → Nullifications"),
                ]},
                {"id": "harvest_festival", "name": "Harvest Festival", "icon": "minecraft:hay_block", "text": [
                    "L'éveil en Vrai Seigneur Démon déclenche un $(l)Harvest Festival$() de 3 minutes, qui touche les subordonnés dans un rayon de 30 blocs.",
                    li("1re minute : pas de compétences, vision et mouvements limités", "2e minute : tu tombes en sommeil", "3e minute : tes subordonnés dorment aussi"),
                    "$(l)Mourir pendant le Festival fait perdre toutes tes âmes !$() Mets-toi en sécurité avant.",
                ]},
                {"id": "vrai_heros", "name": "Vrai Héros", "icon": "minecraft:turtle_egg", "text": [
                    B + "L'Œuf du Héros" + E + "$(br)Obtiens les 5 Greater Spirits de base (Feu, Eau, Vent, Terre, Espace) + un Greater de Lumière ou de Ténèbres. Tu ne dois pas être Majin de naissance. Tu gagnes aussi Eye Of Truth.",
                    "5 % de chances d'être $(l)Béni$() en se réincarnant avec une race non Majin : l'œuf est alors obtenu immédiatement.",
                    B + "Éclosion" + E + "$(br)Régénère des PV en étant sous 25 % de tes PV max, contre un boss valide avec au moins $(l)400 000 EP$() et sous 50 % de ses PV.",
                    B + "Boss valides" + E + li("Wither, Ender Dragon", "Elemental Colossus, Charybdis, Akash", "Ifrit, Sylphide, Undine, War Gnome", "Orc Lord, Orc Disaster, Supermassive Slime", "Dragons, Gorgon, Hydra, Dread Lich (Ice and Fire)"),
                    B + "Effets" + E + li("EP x3", "Résistances → Nullifications", "Unpredictability : ignore esquives et critiques"),
                ]},
            ],
        },
        {
            "id": "monde", "name": "Le monde", "icon": "minecraft:grass_block",
            "description": "Biomes, dimensions et règles de jeu particulières.",
            "entries": [
                {"id": "biomes", "name": "Biomes", "icon": "minecraft:oak_sapling", "text": [
                    "Tensura ajoute 8 biomes. Chacun demande un minimum de magicules pour y entrer sans $(l)empoisonnement aux magicules$().",
                    B + "Surface" + E + li("Ancient Forest : forêt dense, abrite l'Arbre du Labyrinthe", "Miasmic Plains : marais brumeux, les morts-vivants n'y brûlent pas", "Barren Lands", "Desert of Death"),
                    B + "Enfer (Hell)" + E + li("Underworld Barrens", "Underworld Red Sands", "Underworld Sands", "Underworld Spikes"),
                ]},
                {"id": "hardcore", "name": "Races hardcore", "icon": "minecraft:skeleton_skull", "text": [
                    "Si la gamerule des races hardcore est activée :",
                    li("Slime : aveugle au départ, il faut Magic Sense", "Homme-lézard : affaibli dans le froid", "Homme-poisson : suffoque hors de l'eau", "Wight, Goule, Vampire : brûlent au soleil même avec un casque", "Orc Lord / Disaster : Faim III / V"),
                    "Un joueur nommé ne peut alors plus s'éveiller.",
                ]},
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# MINECOLONIES
# ---------------------------------------------------------------------------

MC = "minecolonies:"

MINECOLONIES = {
    "name": "Wiki MineColonies",
    "subtitle": "Le guide de Bob",
    "landing_text": "Salut, moi c'est $(l)Bob$() ! Tu veux fonder ta propre colonie ? Ce livre t'explique tout : fonder la colonie, construire les bâtiments, s'occuper des citoyens et comprendre les systèmes.$(br2)Commence par la catégorie $(l)Débuter$().",
    "model": "patchouli:book_brown",
    "categories": [
        {
            "id": "debuter", "name": "Débuter", "icon": MC + "supplycampdeployer",
            "description": "Fonder ta colonie et les premières étapes de construction.",
            "entries": [
                {"id": "fonder", "name": "Fonder sa colonie", "icon": MC + "supplycampdeployer", "text": [
                    "Le plus simple est de commencer avec un $(l)Supply Camp$() (ou $(l)Supply Ship$()). Il donne gratuitement l'Hôtel de ville, le $(l)Build Tool$() et des ressources.",
                    "Fabrique-le et fais clic droit directement sur le sol ou l'eau (sans le Build Tool).",
                    li("Camp : zone plate et dégagée de 16x17 minimum, sans trou ni fleurs ni herbes", "Bateau : étendue d'eau d'au moins 32x20"),
                    "Un seul Supply Camp/Ship par monde ! S'il refuse de se poser, décale-le bloc par bloc.",
                    "Récupère l'Hôtel de ville et le Build Tool dans le coffre de la structure.",
                ]},
                {"id": "hotel_de_ville", "name": "Placer l'Hôtel de ville", "icon": MC + "blockhuttownhall", "text": [
                    "Choisis bien l'emplacement : il faut une zone assez plate d'au moins $(l)8x8 chunks$(). Le chunk de l'Hôtel de ville devient le $(l)centre définitif$() de la colonie (rayon protégé de 4 chunks).",
                    "Rassemble avant : bois, pierre, charbon, fer, ficelle, cuir, laine, pousses, fleurs et nourriture.",
                    "Place le bloc avec le Build Tool (aperçu 3D, flèches pour déplacer, + et - pour la hauteur), valide, puis fais clic droit dessus et signe le $(l)Settlement Covenant$(). Tes 4 premiers citoyens arrivent peu après.",
                ]},
                {"id": "colonie_abandonnee", "name": "Colonies abandonnées", "icon": MC + "blockhutcitizen", "text": [
                    "En explorant, tu peux trouver des $(l)colonies abandonnées$() générées dans le monde. En réclamer une évite le Supply Camp.",
                    "Trouve l'Hôtel de ville et clique sur « Create new colony ». Ensuite, va sur chaque bloc de bâtiment et clique sur « Reactivate » pour le rattacher à ta colonie. Tu peux aussi les réparer.",
                ]},
                {"id": "etapes", "name": "Les étapes clés", "icon": MC + "blockhutbuilder", "text": [
                    B + "1. Cabane du Bâtisseur" + E + "$(br)Rien ne se construit sans Bâtisseur. Pose la cabane, puis dans son menu : Build Options → Build Building. Monte-la vite au niveau 2.",
                    B + "2. Logement" + E + "$(br)Construis la $(l)Taverne$() (4 lits, attire des visiteurs), puis des $(l)Résidences$() pour augmenter la population.",
                    B + "3. Nourriture" + E + "$(br)Le $(l)Pêcheur$() est le plus rapide au début. Ajoute un $(l)Réfectoire$() pour nourrir tout le monde.",
                    B + "4. Bois" + E + "$(br)La cabane du $(l)Forestier$() fournit le bois.",
                    B + "5. Mine" + E + "$(br)La $(l)Mine$() fournit pierre et minerais, essentiels aux améliorations.",
                    B + "6. Logistique" + E + "$(br)$(l)Entrepôt$() + $(l)Coursier$() : les objets circulent tout seuls entre les bâtiments.",
                    B + "7. Développement" + E + li("Tour de garde contre les raids", "Hôpital contre les maladies", "Scierie pour l'artisanat", "Un seul ouvrier par cabane : multiplie-les", "Améliore au niveau 5 pour travailler plus vite"),
                ]},
            ],
        },
        {
            "id": "base", "name": "Bâtiments de base", "icon": MC + "blockhutbuilder",
            "description": "Hôtel de ville, Bâtisseur, logement, entrepôt et coursiers.",
            "entries": [
                {"id": "townhall", "name": "Hôtel de ville", "icon": MC + "blockhuttownhall", "text": [
                    "Le cœur de la colonie. Son menu gère les permissions des joueurs, le recrutement, les logements et affiche le bonheur de la colonie.",
                    "Le bloc ne peut être fabriqué qu'après avoir posé celui du Supply Camp.",
                    "Son niveau agrandit le territoire (voir Frontières) et débloque d'autres fonctions.",
                ]},
                {"id": "builder", "name": "Cabane du Bâtisseur", "icon": MC + "blockhutbuilder", "text": [
                    "Le Bâtisseur doit d'abord construire sa propre cabane. Ensuite il construit tout : bâtiments, décorations, tes propres schémas.",
                    "Il ne peut construire ou améliorer un bâtiment $(l)qu'au niveau de sa propre cabane$() : améliore-la en premier.",
                    "Il demande les matériaux au fur et à mesure. Onglet « Required Resources » : ce qui manque est en rouge. S'il semble bloqué, rappelle-le (Recall) et vérifie la liste.",
                ]},
                {"id": "tavern", "name": "Taverne", "icon": MC + "blockhuttavern", "text": [
                    "Loge $(l)4 citoyens$() (non améliorable en lits) et attire des $(l)visiteurs$(). Tu peux les recruter en leur donnant les objets demandés. Ne les attaque pas, ils se défendent !",
                    "Monte jusqu'au niveau 3 maximum : plus de visiteurs et de meilleure qualité. Une seule taverne par colonie.",
                ]},
                {"id": "residence", "name": "Résidence", "icon": MC + "blockhutcitizen", "text": [
                    "Les citoyens y dorment la nuit. Chaque niveau ajoute $(l)1 lit$() (5 au niveau 5).",
                    "Une fois les 4 premiers citoyens logés, un lit libre fait arriver un nouveau citoyen. Tu peux aussi recruter à la Taverne.",
                    "Le niveau de la résidence limite les compétences max de ses habitants. Au-delà de 25 citoyens, il faut les recherches Outpost, Hamlet, Village puis City à l'Université.",
                ]},
                {"id": "warehouse", "name": "Entrepôt et Coursiers", "icon": MC + "blockhutwarehouse", "text": [
                    "L'$(l)Entrepôt$() est le stockage central, dans des $(l)Racks$(). Chaque niveau permet 2 coursiers de plus (10 au niveau 5) et plus de stockage.",
                    "Le $(l)Coursier$() fait la navette entre l'entrepôt et les cabanes. Chaque coursier a sa cabane. Niveau de la cabane = piles transportées (2, 3, 4, 5, puis illimité).",
                    "L'Agilité du coursier le fait courir plus vite, son Adaptabilité lui fait visiter plus de cabanes par trajet.",
                ]},
            ],
        },
        {
            "id": "production", "name": "Production", "icon": MC + "blockhutfarmer",
            "description": "Nourriture, bois, minerais et ressources naturelles.",
            "entries": [
                {"id": "fisher", "name": "Pêcheur", "icon": MC + "blockhutfisherman", "text": [
                    "Besoin d'une canne à pêche et d'une étendue d'eau d'au moins $(l)7x7 et 2 de profondeur$() près de la cabane.",
                    "Les niveaux augmentent la portée et le butin (prismarine, éponges...). Les trésors ne sortent que dans les biomes océaniques.",
                ]},
                {"id": "farmer", "name": "Fermier", "icon": MC + "blockhutfarmer", "text": [
                    "Cultive blé, carottes, pommes de terre, betteraves, melons, citrouilles et la plupart des cultures moddées. Donne-lui une houe, une hache et la graine voulue.",
                    "Pose des blocs $(l)Field$() (épouvantail) dans les champs et mets la graine dans leur menu. Une seule action par champ et par jour, le cycle jour/nuit doit être actif.",
                    "Il fabrique aussi graines, bottes de foin et terre stérile si tu lui apprends les recettes.",
                ]},
                {"id": "forester", "name": "Forestier", "icon": MC + "blockhutlumberjack", "text": [
                    "Coupe les arbres dans un rayon d'environ 150 blocs, sauf ceux dans un schéma de bâtiment ou qui ont de la cobblestone posée dessous. Tu peux définir une zone de coupe.",
                    "Il lui faut une $(l)hache$() pour les troncs et une $(l)houe$() pour les feuilles.",
                ]},
                {"id": "mine", "name": "Mine", "icon": MC + "blockhutminer", "text": [
                    "Le Mineur creuse un puits, puis des galeries. Chaque niveau permet de descendre d'un palier :",
                    li("Cuivre : Y 48", "Fer : Y 16", "Or : Y -16", "Diamant : bedrock"),
                    "Tu peux limiter la profondeur dans les réglages. Tu peux aussi y embaucher un $(l)Carrier$() pour une Carrière à la place du mineur.",
                ]},
                {"id": "plantation", "name": "Plantation et Compost", "icon": MC + "blockhutplantation", "text": [
                    "Le $(l)Planteur$() cultive canne à sucre, cactus, bambou, cacao, lianes, algues, baies lumineuses, plantes du Nether... sur des champs construits par le Bâtisseur.",
                    "Le $(l)Composteur$() transforme les déchets organiques en compost ou en terre dans des Compost Barrels (1 par niveau).",
                ]},
            ],
        },
        {
            "id": "artisanat", "name": "Artisanat et cuisine", "icon": MC + "blockhutsawmill",
            "description": "Ateliers qui fabriquent les objets demandés par la colonie.",
            "entries": [
                {"id": "principe", "name": "Fonctionnement", "icon": MC + "blockhutsawmill", "text": [
                    "Les artisans ne fabriquent que sur $(l)demande$() d'un autre ouvrier et s'ils ont les matériaux.",
                    "Il faut leur $(l)apprendre les recettes$(). Nombre de recettes selon le niveau :",
                    li("Niv. 1 : 10", "Niv. 2 : 20", "Niv. 3 : 40", "Niv. 4 : 80", "Niv. 5 : 160"),
                ]},
                {"id": "sawmill", "name": "Scierie", "icon": MC + "blockhutsawmill", "text": [
                    "Le $(l)Charpentier$() fabrique les objets faits d'au moins 75 % de bois, sans lingot, pierre, redstone ni ficelle. Il fait aussi les Racks et les blocs Domum Ornamentum en bois.",
                ]},
                {"id": "stonemason", "name": "Tailleur de pierre", "icon": MC + "blockhutstonemason", "text": [
                    "Fabrique les recettes en pierre, andésite, diorite, granite, quartz, briques du Nether, prismarine, grès, blackstone, basalte... (sans lingot ni redstone).",
                ]},
                {"id": "blacksmith", "name": "Forgeron", "icon": MC + "blockhutblacksmith", "text": [
                    "Fabrique outils, armures, épées et boucliers vanilla (pas d'arcs ni de redstone). Au niveau 5, il apprend les 9 recettes en netherite.",
                ]},
                {"id": "smeltery", "name": "Fonderie", "icon": MC + "blockhutsmeltery", "text": [
                    "Le $(l)Fondeur$() fond les minerais en lingots, avec Fortune (niveau du bâtiment - 1). Plus le niveau est haut, plus il utilise de fourneaux et plus il a de chances de doubler ou tripler les lingots.",
                ]},
                {"id": "cuisine", "name": "Réfectoire et Cuisine", "icon": MC + "blockhutcook", "text": [
                    "Au $(l)Réfectoire$() (Dining Hall), le Serveur cuit la nourriture et nourrit les citoyens affamés. Il lui faut ingrédients et combustible.",
                    "À la $(l)Cuisine du Chef$(), le Chef prépare les plats élaborés sur demande, pour garder le Réfectoire approvisionné. La Boulangerie complète avec les produits boulangers.",
                ]},
                {"id": "enchanter", "name": "Tour de l'Enchanteur", "icon": MC + "blockhutenchanter", "text": [
                    "L'Enchanteur crée des livres enchantés avec des $(l)Ancient Tomes$(), en observant les autres ouvriers pour gagner de l'expérience. Niveau du bâtiment = niveau max des enchantements.",
                    "Il fabrique aussi des parchemins de téléportation vers la colonie (papier, boussole et Build Tool).",
                ]},
            ],
        },
        {
            "id": "defense", "name": "Défense", "icon": MC + "blockhutguardtower",
            "description": "Gardes, casernes, entraînement et raids.",
            "entries": [
                {"id": "guardtower", "name": "Tour de garde", "icon": MC + "blockhutguardtower", "text": [
                    "Emploie et loge $(l)1 garde$(). Il patrouille autour de la tour : 80 blocs au niveau 1, jusqu'à 200 au niveau 5.",
                    "Les tours rassurent les citoyens (bonheur) et, près de la frontière, agrandissent le territoire.",
                ]},
                {"id": "barracks", "name": "Caserne", "icon": MC + "blockhutbarracks", "text": [
                    "La meilleure défense : chaque $(l)Barracks Tower$() loge 1 garde par niveau (5 max). Les casernes officielles ont 4 tours, soit $(l)20 gardes$().",
                    B + "Types de gardes" + E + li("Chevalier : mêlée, épée (+ bouclier, armure)", "Archer : distance, arc", "Druide : lance des potions"),
                    "Au niveau 3, tu peux engager des espions qui font briller les raiders.",
                ]},
                {"id": "entrainement", "name": "Entraînement", "icon": MC + "blockhutcombatacademy", "text": [
                    "L'$(l)Académie de combat$() forme des chevaliers (épée + bouclier, sur des mannequins : citrouille sur une botte de foin) et le $(l)Stand de tir$() forme des archers (arc, sur des blocs Cible).",
                    "Ils montent de niveau sans risquer de mourir. 1 élève par niveau du bâtiment. Les élèves ne défendent pas la colonie.",
                ]},
                {"id": "raids", "name": "Raids", "icon": "minecraft:iron_axe", "text": [
                    "Les raids arrivent au $(l)début de la nuit$(). Un message indique leur direction et une barre montre la progression. Les citoyens rentrent chez eux.",
                    B + "Type selon le biome" + E + li("Taïga : Nordiques", "Désert : Momies (les Pharaons peuvent lâcher un sceptre)", "Grande étendue d'eau : Pirates (bateau avec spawners à casser)", "Jungle : Amazones", "Ailleurs : Barbares"),
                    "Les raiders cassent les blocs, posent des échelles et traversent la lave : les pièges ne marchent pas. Survivre sans perte donne un bonus de bonheur.",
                ]},
            ],
        },
        {
            "id": "citoyens", "name": "Citoyens", "icon": "minecraft:bread",
            "description": "Nourriture, sommeil, bonheur, équipement et compétences des citoyens.",
            "entries": [
                {"id": "nourriture", "name": "Nourriture", "icon": "minecraft:bread", "text": [
                    "Chaque citoyen a une barre de $(l)saturation$(). Quand elle baisse, il va au Réfectoire. À 0, il arrête de travailler, ralentit et réclame à manger.",
                    "Un citoyen bien nourri guérit deux fois plus vite et progresse mieux.",
                    "Les citoyens exigent une nourriture de $(l)qualité$() selon le niveau de leur résidence. La nourriture vanilla est pénalisée : vise les plats MineColonies.",
                    "Chaque culture MineColonies pousse dans un type de biome (froid, tempéré, humide, sec). Certains plats demandent des échanges avec d'autres colonies.",
                ]},
                {"id": "sommeil", "name": "Sommeil et logement", "icon": "minecraft:red_bed", "text": [
                    "La nuit, les citoyens dorment dans leur lit. S'ils n'y arrivent pas pendant 3 jours, ils sont malheureux.",
                    "Les sans-abri se regroupent à l'Hôtel de ville et sont contrariés au bout de deux semaines.",
                    "À plus de $(l)100 blocs$() de leur travail, ils se plaignent : échange leurs lits.",
                    "Avec au moins un homme et une femme, des enfants peuvent naître. Ils héritent en partie des compétences des adultes de leur maison.",
                ]},
                {"id": "bonheur", "name": "Bonheur", "icon": MC + "blockhutmysticalsite", "text": [
                    "Le bonheur dépend de 3 facteurs : $(l)sécurité$(), $(l)logement$() et $(l)saturation$().",
                    li("Bien manger", "Maison au-dessus du niveau 2.5", "Au moins 2 gardes pour 3 citoyens, et des tours près des maisons"),
                    "Baissent le bonheur : mort d'un citoyen (deuil), blessure, maladie, pas de maison, chômage, rien à faire au travail.",
                    "Une colonie heureuse donne de meilleurs nouveaux citoyens. Le $(l)Site Mystique$() augmente le bonheur global.",
                ]},
                {"id": "equipement", "name": "Équipement des ouvriers", "icon": "minecraft:iron_pickaxe", "text": [
                    "Le niveau de la cabane limite les outils utilisables :",
                    li("Bois / or : niveau 0", "Pierre : niveau 1", "Fer : niveau 2", "Diamant : niveau 3", "Netherite : niveau 4"),
                    "Les enchantements autorisés augmentent aussi avec le niveau. Les armures des gardes suivent le même principe (cuir au niv. 1, jusqu'à netherite au niv. 5).",
                ]},
                {"id": "competences", "name": "Compétences", "icon": "minecraft:experience_bottle", "text": [
                    "Chaque métier a une compétence $(l)principale$() (en vert à l'embauche) et $(l)secondaire$() (en jaune). Plus elles sont hautes, plus l'ouvrier est rapide et efficace.",
                    "Elles augmentent en travaillant, mais sont plafonnées par le niveau de la maison :",
                    li("Maison niv. 0 : 10", "Niv. 1 : 20", "Niv. 2 : 30", "Niv. 3 : 40", "Niv. 4 : 50", "Niv. 5 : 99"),
                    "Pluie, neige, nuit ou mort d'un citoyen la veille : les ouvriers ne travaillent pas.",
                ]},
                {"id": "sante", "name": "Hôpital et Cimetière", "icon": MC + "blockhuthospital", "text": [
                    B + "Hôpital" + E + "$(br)Le Soigneur guérit les malades (1 lit par niveau).",
                    li("Grippe : carotte + pomme de terre", "Rougeole : pissenlit, algue, coquelicot", "Variole : fiole de miel + pomme dorée"),
                    B + "Cimetière" + E + "$(br)Le Fossoyeur récupère les objets des citoyens morts et tente de les ressusciter (chance faible, augmentée par le Site Mystique et les totems).",
                ]},
                {"id": "education", "name": "Éducation", "icon": MC + "blockhutlibrary", "text": [
                    li(B + "École" + E + " : le Professeur augmente l'Intelligence des enfants (2 par niveau). Le papier accélère.", B + "Bibliothèque" + E + " : les adultes y étudient l'Intelligence (2 par niveau). Papier et livres accélèrent."),
                    "L'Intelligence accélère la progression de toutes les autres compétences.",
                ]},
            ],
        },
        {
            "id": "systemes", "name": "Systèmes", "icon": MC + "clipboard",
            "description": "Demandes, outils du maire, territoire, recherche et quêtes.",
            "entries": [
                {"id": "demandes", "name": "Demandes", "icon": MC + "clipboard", "text": [
                    "Quand un citoyen a besoin d'un objet, il cherche dans son inventaire, sa cabane et ses racks, puis fait une $(l)demande$(). Si l'objet est à l'Entrepôt, un Coursier le livre.",
                    "Sinon, les artisans qui savent le fabriquer s'en chargent, en demandant eux-mêmes les ingrédients (bûches → planches → escaliers...).",
                    "Si personne ne peut, le citoyen affiche une $(l)roue rouge$() : parle-lui pour voir ce qu'il veut, puis donne-le-lui ou mets-le à l'Entrepôt.",
                ]},
                {"id": "outils", "name": "Outils du maire", "icon": MC + "resourcescroll", "text": [
                    B + "Clipboard" + E + "$(br)Accroupi + clic droit sur l'Hôtel de ville pour la lier. Montre toutes les demandes non traitées par les coursiers.",
                    B + "Resource Scroll" + E + "$(br)Accroupi + clic droit sur une cabane de Bâtisseur. Montre les matériaux manquants (rouge : personne ne l'a, vert : tu l'as).",
                    B + "Builder's Goggles" + E + "$(br)Portées sur la tête, elles montrent un aperçu fantôme des constructions en cours.",
                ]},
                {"id": "frontieres", "name": "Territoire et protection", "icon": MC + "blockhuttownhall", "text": [
                    "La colonie démarre avec un rayon de $(l)4 chunks$() autour de l'Hôtel de ville. Construire des bâtiments l'agrandit (max 20 chunks). Les tours de garde agrandissent le plus.",
                    "Dans le territoire, seul le propriétaire peut casser ou poser des blocs (ajoute des joueurs dans les permissions de l'Hôtel de ville). Les explosions y sont désactivées.",
                ]},
                {"id": "recherche", "name": "Recherche", "icon": MC + "blockhutuniversity", "text": [
                    "À l'$(l)Université$(), les Chercheurs débloquent des améliorations. 4 arbres : Civil, Combat, Technologie et Déblocages.",
                    "Chaque colonne d'un arbre demande l'Université au niveau correspondant (colonne 3 = niveau 3). Les coûts sont pris dans ton inventaire.",
                    "La recherche se fait en temps réel ; dès le niveau 3, une partie avance même hors ligne. 1 chercheur par niveau.",
                ]},
                {"id": "quetes", "name": "Quêtes", "icon": "minecraft:writable_book", "text": [
                    "Les citoyens te proposent des $(l)quêtes$() : dialogues, livraisons, constructions, blocs à casser ou poser, monstres à tuer, recherches...",
                    "Certaines forment une chaîne (le tutoriel, que tu peux passer). Les récompenses sont des objets.",
                    "Le $(l)Quest Log$() (lié à la colonie par clic droit sur une cabane) suit tes quêtes.",
                ]},
            ],
        },
    ],
}

BOOKS = {"tensura": TENSURA, "minecolonies": MINECOLONIES}
