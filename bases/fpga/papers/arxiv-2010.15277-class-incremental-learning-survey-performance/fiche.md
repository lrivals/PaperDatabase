---
id: arxiv-2010.15277-class-incremental-learning-survey-performance
fiche: done
date: 2026-09-29
benchmarks: none
---

# Class-incremental learning: survey and performance evaluation on image classification

Marc Masana, Xialei Liu, Bartlomiej Twardowski, Mikel Menta, Andrew D. Bagdanov, Joost van de Weijer, 2020, arXiv preprint. https://arxiv.org/abs/2010.15277
Type : preprint non relu par les pairs (arXiv, pas de DOI dans les métadonnées)

## Problème

L'apprentissage incrémental de réseaux profonds souffre d'oubli catastrophique. Le cas class-IL (pas de task-ID à l'inférence, toutes les classes vues doivent être discriminées) est plus dur que le task-IL et n'avait pas de comparaison expérimentale large et équitable (§1, §2.4). Les auteurs identifient quatre causes d'oubli : dérive des poids, dérive des activations, confusion inter-tâches, biais de récence des tâches (§2.4). Motivations pratiques citées : mémoire limitée, confidentialité des données, coût énergétique du réentraînement (§2.1).

## Méthode

Survey plus évaluation expérimentale de treize méthodes de class-IL (offline, architecture fixe, entraînées de zéro), classées en trois familles (§3) :
- régularisation : poids (EWC, PathInt, MAS, RWalk) et données/distillation (LwF, LwM, DMC, GD) ;
- rehearsal avec exemplars (iCaRL, EEIL, mémoire fixe ou croissante ; échantillonnage random, herding, entropy, distance) ;
- correction du biais de récence (iCaRL, EEIL, BiC, LUCIR, IL2M).
Baselines : finetuning FT, FT+, FT-E (avec exemplars), freezing FZ, FZ-E, Joint (borne supérieure) (§5.4).
Protocole : cadre commun FACIL (mêmes découpages, mêmes graines, PyTorch), sélection d'hyperparamètres par le Continual Hyperparameter Framework, métrique principale = précision moyenne sur les tâches vues, 10 runs sur CIFAR-100 et 5 runs pour les autres scénarios (§5.1, §5.3, §5.5).
Jeux de données : CIFAR-100, six jeux fine-grained (Flowers, Scenes, Birds, Cars, Aircraft, Actions), VGGFace2, ImageNet et ImageNet-Subset (§5.2). Réseaux : ResNet-32 et ResNet-18 principalement, puis AlexNet, VGG-11, GoogleNet, MobileNet (§5.6, §6.8).
Toolflow FPGA : sans objet.

## Plateforme et implémentation

Sans objet : pas de cible matérielle, pas de mesure de latence ni de puissance (seul le temps par epoch de RPS est donné, Table S3, matériel n/r). Implémentation PyTorch ; code publié : cadre FACIL, https://github.com/mmasana/FACIL (§1). Pas de bitstream.

## Résultats

Chiffres de précision moyenne (%) ; aucune ligne dans `benchmarks.csv` (survey d'algorithmes sans mesure matérielle, `benchmarks: none`).
- Sans exemplars, CIFAR-100 (10/10), ResNet-32, class-IL, après 10 tâches : FT+ 10,1 ; LwF 30,2 ; LwM 21,9 ; EWC 13,1 ; MAS 13,9 (Table 2). LwF est la meilleure méthode sans exemplars (§8).
- Avec 2 000 exemplars (mémoire fixe), après 10 tâches : FT-E 37,9 ; LwF-E 30,8 ; EWC-E 28,1 ; LwM-E 37,4 (Table 2). FT-E surpasse plusieurs méthodes plus complexes (§6.1). Joint : 66,3 (Table S2).
- Biais de récence (CIFAR-100 5/20, ResNet-32, 2 000 exemplars) : FT-E 40,9 ; iCaRL 43,5 ; EEIL 47,6 ; BiC 45,7 ; LUCIR 47,3 ; IL2M 45,6 (§6.2).
- Scénario CIFAR-100 (10/10) mémoire fixe : BiC 42,0 ; EEIL 41,9 ; IL2M 41,8 ; GD 43,7 (44,6 avec données externes) ; GDumb 19,8 (Table S2). Scénario (11/50-5) : BiC 47,0 (Table S2).
- Exemplars : passer de 10 à 20 exemplars/classe apporte +6,2 points sur BiC, de 20 à 40 +4,8 points au prix d'une mémoire doublée (§6.3). Random et herding sont proches ; la différence n'est significative que pour LwF-E et EEIL sur 10 tâches (Table S6).
- Gros décalage de domaine (six jeux fine-grained) : aucune méthode ne dépasse nettement FT-E (§6.6, Fig. 10). Petit décalage (VGGFace2, 25 tâches de 40 classes) : LUCIR 73,0 ; EWC-E 70,0 contre LwF-E 43,5 (§6.6, Table S7 reconstruite par Docling, à vérifier).
- ImageNet (25/40), ResNet-18, 20 exemplars/classe : BiC 32,4 ; iCaRL 30,2 ; LwF-E 19,8 (§6.9).
- Architectures : le classement des méthodes change selon la présence de connexions résiduelles ; MobileNet reste compétitif (§6.8).
- Les méthodes online (ER, MIR, GDumb) donnent des résultats proches de FT-E en offline (§6.5).
→ reportés dans `benchmarks.csv` : aucune ligne (survey sans mesure matérielle).

## Limites et critique

- Uniquement de la classification d'images sur GPU, réseaux ResNet/AlexNet/VGG/MobileNet standard : rien sur la détection d'objets, ni sur les contraintes embarquées (mémoire, énergie, quantification, entraînement sur cible). MobileNet n'est mentionné que comme « pouvant tourner sur appareil limité » (§6.8), sans mesure.
- Exclut par construction les méthodes online, à architecture croissante, pré-entraînées ou non mûres (§2.3), c'est-à-dire une bonne part de ce qui est utilisable sur du matériel contraint. Chiffres absolus modestes (par exemple 37,9 % pour FT-E après 10 tâches sur CIFAR-100) : le class-IL sans pré-entraînement reste loin de Joint (66,3).
- Les exemplars stockent des images : coût mémoire et confidentialité (§2.1) ; le survey ne chiffre pas l'empreinte mémoire en octets au-delà du nombre d'exemplars.
- Le classement des méthodes dépend du scénario et de l'architecture (§6.4, §6.8) : pas de vainqueur universel. Écarts-types élevés (souvent jusqu'à 2 à 3 points, davantage pour certaines méthodes de régularisation, Table S2) : de petits écarts ne sont pas concluants.
- Les tableaux S7 (Docling) et l'ensemble des Tables S8 à S10 ne sont pas exploitables dans le texte extrait : à ne pas citer sans vérification.
- Preprint arXiv 2020, antérieur aux méthodes récentes à base de modèles pré-entraînés/prompts et aux classifieurs légers type SLDA/HDC : état de l'art à compléter (déduit).

## Pertinence pour la thèse

Référence de cadrage pour l'axe `continual-learning` : vocabulaire (task-IL vs class-IL, task-recency bias, exemplars, herding), protocole d'évaluation (average accuracy, hyperparamètres sans accès aux tâches futures) et résultat utile : un baseline simple (finetuning avec exemplars) est difficile à battre, ce qui plaide pour des schémas simples et peu coûteux sur FPGA. Le constat sur le biais de récence et la correction de la couche de sortie (BiC, IL2M, NME d'iCaRL) suggère des mécanismes légers implémentables en matériel. Rien sur la sûreté : l'oubli catastrophique est un risque pour un système certifiable (un réseau qui évolue après validation), point que le papier ne traite pas. Reste ouvert : apprentissage incrémental sur cible FPGA, en détection (YOLO) et non en classification, coût mémoire des exemplars sur puce, et compatibilité avec une certification (modèle figé vs évolutif).

## Gaps identifiés

- Apprentissage incrémental sur FPGA / SoC : coût matériel des exemplars, de la distillation et de la correction de biais non chiffré dans ce survey.
- Class-IL pour la détection d'objets (YOLO) et non la classification (le survey ne mentionne la détection qu'en §4).
- Évaluation des méthodes de class-IL sous contrainte de sûreté : comment vérifier ou certifier un modèle qui apprend en ligne ; monitoring de la dérive.
- Comparaison avec méthodes légères (SLDA, HDC, prototypes) hors du périmètre du survey.

## Statut de lecture

papier complet : fulltext.md lu de bout en bout (§1 à §8, annexes A et B, tableaux S1 à S7). Extraction : backend grobid ok ; Table S5 et S7 reconstruites par Docling (chiffres à vérifier, S7 ne contient que FZ-E, LwF-E, LwM-E, iCaRL (EWC-E et LUCIR sont donnés seulement dans le texte)) ; Tables S8 à S10 et le corps des figures non extraits ; texte de la conclusion coupé en fin de §8 (sous forme fragmentée dans « Figures et tableaux »).
Ce qui suit est déduit et non affirmé par les auteurs : l'intérêt d'un baseline simple pour le FPGA ; le lien avec la certification ; l'absence de méthodes récentes (SLDA, HDC, pré-entraînement) ; le caractère non comparable des résultats avec des systèmes embarqués.
