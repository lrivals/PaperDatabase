---
id: 2024-rub-continual-incremental-learning-tinyml-device
fiche: done
date: 2026-09-29
---

# A Continual and Incremental Learning Approach for TinyML On-Device Training Using Dataset Distillation and Model Size Adaption

Marcus Rüb, Philipp Tuchel, Axel Sikora, Daniel Mueller-Gritschneder, 2024, 2024 IEEE 7th International Conference on Industrial Cyber-Physical Systems (ICPS). DOI n/r
Type : conférence

## Problème

L'entraînement sur l'appareil (MCU) ne peut pas stocker les jeux de données complets ; les
méthodes d'apprentissage continu qui évitent l'oubli catastrophique sont souvent gourmandes
en mémoire (§I). Les auteurs cherchent un apprentissage incrémental sobre en mémoire et en
calcul pour le TinyML.

## Méthode

Cycle en cinq étapes (§III-B, Fig. 1) :

1. **Distillation de données** : chaque sous-ensemble arrivant est condensé en quelques
   images synthétiques par *distribution matching* (Zhao & Bilen [11]/[12]) avec DSA ;
   seules les images distillées des pas précédents sont conservées (§III-B1).
2. **Entraînement** sur les données distillées de tous les pas (§III-B2, §IV-A).
3. **Validation** sur le test de tous les pas vus (§III-B3).
4. **Agrandissement du modèle** si la précision est sous un seuil A_standard :
   ConvNetD2 → D3 → D4 (§III-B4, §IV-A).
5. Acquisition du pas suivant (§III-B5).

Réseaux : ConvNet à 2, 3 ou 4 blocs (8, 64, 128 kernels), GroupNorm, ReLU, average pooling ;
distillation toujours faite avec ConvNetD4 (§IV-A). Scénarios : MNIST rotations croissantes
(10 pas, 10 images/classe ≈ 1,7 %), CORe50 NIC (79 pas, 400 images ≈ 0,3 %), Speech Commands
class-incremental (35 pas, 20 IPC ≈ 0,8 %), HAR (8 pas, 10 IPC ≈ 4,68 %), CIFAR10
class-incremental (10 pas, 50 IPC ≈ 1 %) (§IV-A1 à A5). Comparaisons : modèle adaptatif,
plus grand modèle fixe (D4), entraînement cumulatif (tout le jeu), et fine-tuning naïf
(« catastrophic forgetting ») (§V-A).

## Plateforme et implémentation

- **Aucune exécution sur MCU** : les expériences ne décrivent ni puce, ni carte, ni
  framework embarqué ; le coût est exprimé en FLOPs relatifs par époque (§IV-A, §V).
- Précision numérique : n/r. Mémoire RAM/Flash : n/r (seule la taille du jeu distillé en % du
  jeu d'origine est donnée). Latence, énergie : n/r.
- La distillation elle-même (descente de gradient sur les images synthétiques) n'est pas
  chiffrée ni située (appareil ou serveur) (déduit : non précisé).
- Code : non publié.

## Résultats

Tableaux I, III et V absents de l'extraction, II et IV sans corps : les chiffres viennent du
texte (§V).

| Jeu | Cumulatif (fin / moyenne) | Plus grand modèle | Adaptatif | FLOPs adaptatif | Naïf |
|---|---|---|---|---|---|
| CIFAR10 | 85,4 / 47,8 | 57,7 / 35,6 | 58,2 / 35,9 | 43 % | 10 / 10 |
| CORe50 | 55,3 / 36,5 | « slightly lower » n/r | n/r | 49 % | 3,7 / 3,6 |
| Speech Commands | 95 / 45,6 | ≈ 70 (n/r exact) | ≈ 70 (n/r exact) | 36 % | 3,8 / 2,9 |
| MNIST rotations | 98,8 / 78,8 | ≈ 92 (n/r exact) | ≈ 92 (n/r exact) | 36 % | 60,1 / 66,2 |
| HAR | 83,1 / 43,1 | mi-60 (n/r) | mi-60 (n/r) | ≈ 1/3 | 15 / 12,5 |

(§V-B à V-F ; précisions en %.) Sur CORe50, la méthode conserve « over 78 % » de la précision
cumulative (§IV-A2). Mémoire du rejeu : ≈ 1 % du jeu d'origine (§V-G, §VI).

→ reportés dans `benchmarks.csv` : 2 lignes (CIFAR10, modèle adaptatif et plus grand modèle
fixe, §V-B, `medium`). Les autres jeux n'ont pas de valeur exacte dans le texte extrait.

## Limites et critique

- **Titre « on-device training » sans aucune mesure sur appareil** : ni MCU, ni RAM, ni
  latence, ni énergie ; les FLOPs relatifs ne disent rien du coût de la distillation, qui
  est lui-même un problème d'optimisation coûteux.
- Terminologie incohérente : « baseline » désigne le fine-tuning naïf en §IV-A et
  l'entraînement cumulatif en §V-A ; SGD momentum puis « Adam Optimizer » dans le même
  paragraphe (§IV-A).
- Chiffres de synthèse contradictoires : perte de 1 % (Abstract), 0,4 % (§VI), et sur
  CORe50 2,8 % (§V-G) — mesurés contre le plus grand modèle fixe, pas contre l'entraînement
  cumulatif, dont l'écart réel est de 27 points sur CIFAR10 (85,4 vs 58,2).
- Comparaison à CWR/LwF/EWC reprise d'un autre papier [5], à 128×128 contre 64×64 ici,
  avec un modèle différent (§II) : non comparable.
- Stocker des images distillées reste une forme de rejeu (mémoire de données synthétiques) :
  le « sans mémoire » est relatif.
- Aucun jeu de maintenance prédictive, alors que la PdM est citée en motivation (Abstract).
- Le seuil A_standard qui déclenche l'agrandissement n'est pas donné.

## Pertinence pour la thèse

Illustre une piste « rejeu compressé » pour l'apprentissage continu en TinyML, alternative à
la régularisation type EWC : la mémoire de rejeu tombe à ≈ 1 % du jeu (§VI). Mais sans mesure
sur MCU ni séries temporelles de capteurs industriels (HAR mis à part, converti en
spectrogrammes), il ne permet pas de situer le coût réel face à un EWC INT8 sur Cortex-M
(déduit). La croissance de modèle est intéressante pour un budget Flash contraint, mais
suppose de pouvoir réentraîner depuis zéro sur l'appareil.

## Gaps identifiés

- Coût embarqué (RAM, énergie, temps) de la distillation de données sur MCU : non mesuré.
- Rejeu par données distillées sur séries temporelles de PdM (vibrations, RUL) : non testé.
- Comparaison directe distillation vs régularisation (EWC/SI) à budget mémoire égal.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables I, III, V absentes et Tables II, IV sans
corps à l'extraction : chiffres repris du texte seulement ; Fig. 2 non disponible.
Déduit et non affirmé par les auteurs : distillation non située (appareil ou serveur),
écart réel au cumulatif, non-comparabilité avec [5].
