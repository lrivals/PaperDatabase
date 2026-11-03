---
id: arxiv-2610.29503-hard-soft-real-time-dnn
fiche: done
date: 2026-11-03
benchmarks: none
---

# Hard and Soft Real-Time DNN Inference Scheduling on Heterogeneous Multi-Accelerator Systems via Reinforcement Learning

Francesco Giulio Blanco, Enrico Russo, Giuseppe Ascia, Davide Patti, Maurizio Palesi, 2026, arXiv preprint. https://arxiv.org/abs/2610.29503
Type : preprint non relu par les pairs

## Problème

Ordonnancer sur un système multi-accélérateurs hétérogène (6 accélérateurs DNN) un mélange de tâches DNN dures périodiques (HRT, deadlines à garantir au pire cas) et de requêtes douces apériodiques (SRT) venant de plusieurs clients (§1, §2). Les ordonnanceurs statiques garantissent les HRT mais s'adaptent mal ; les ordonnanceurs adaptatifs (dont RL) améliorent l'usage mais sans garantie HRT (§1). Une politique apprise ne peut pas être crue pour la sûreté (§1).

## Méthode

Séparer sûreté et performance (§3). Hors ligne : ordonnancement de référence HRT seul, fondé sur les WCET profilés (incluant les coûts de transfert), sur l'hyperpériode, avec contrôle d'admission (§3.1). En ligne : un ordonnanceur périodique (T_S = 5 ms) propose un préfixe d'ordonnancement candidat ; une couche de sûreté déterministe le valide par un critère suffisant de « remplacement de préfixe préservant l'ordonnançabilité » fondé sur des coupes par machine (Définitions 1-6, Théorème 1, §4) ; sinon repli sur la portion correspondante du plan de référence, travail SRT du préfixe rejeté abandonné (§5.1). L'ordonnanceur est un acteur-critique DDPG à réseaux GRU, qui émet une priorité temporelle et M scores d'accélérateur par sous-tâche ; récompense à 4 termes (deadline, marge, équilibre QoS par client, pénalité HRT µ = 30) (§5.3, Éq. 1-7). Le cadre est indépendant de la politique (§3). Preuve formelle fournie ; code déclaré open source (https://github.com/BlancoFrancescoGiulio/retnas, §1).

## Plateforme et implémentation

Pas de FPGA ni de matériel réel : simulateur au niveau couche, 6 accélérateurs DNN modélisés (3 de type Eyeriss, row-stationary, et 3 de type Simba, weight-stationary ; 2 petits et 1 grand par famille), avec latences profilées par couche et par accélérateur (§6.1). Charges : AlexNet, InceptionV3, ResNet50 (classification), YOLO-v2 (détection) (§6.1). Arrivées SRT en loi de Pareto (modèle de Da Costa et al.), d = 40 ms ou 10 ms. Puissance : n/r. Ressources FPGA : n/r. Les latences profilées proviennent d'un outil non nommé dans le texte (n/r). Code : publié (lien ci-dessus, non vérifié).

## Résultats

Tout est mesuré en simulation, pas de FPGA (§6). Politique entraînée à d = 10 ms (note 3, §6.3).
- Taux de succès SRT H_S : 98,29 % à d = 40 ms (suivi de SSML 96,75 %, client-aware 92,70 %) ; 81,41 % à d = 10 ms contre 59,50 % (client-aware) et 50,74 % (FF+TC/TCSD), soit +21,91 points (§6.3, Fig. 6).
- Pire client min_k H_S^k : 90,32 % à 40 ms ; 62,05 % à 10 ms contre 30,19 % (client-aware), PREMA 3,39 %, SSML 1,94 %, plusieurs à 0,00 % ; +31,86 points (§6.3, Fig. 7).
- Aucun job HRT admis ne manque sa deadline dans toutes les expériences certifiées ; les auteurs précisent que ce n'est qu'une validation de l'implémentation, la garantie venant du Théorème 1 (§6.1).
- Ablation sans enveloppe de sûreté : la politique atteint 99,8 % de satisfaction HRT et 81,4 % SRT, mais « 99,8 % n'est pas une garantie » ; la plupart des baselines perdent beaucoup de HRT (Fig. 10, §6.3).
- Surcharge de l'ordonnanceur : GRU de taille cachée 192, 592 cycles par sous-tâche sur le plus petit accélérateur ; avec N_max = 64, τ_policy = 37 888 cycles = 37,9 µs à 1 GHz, soit 0,76 % de la période (§6.3, chunk 2610.29503#026.0). Certification en O(N).
- Sensibilité à T_S (d = 10 ms) : H_S de 73,73 / 76,84 / 69,45 / 74,96 / 81,40 / 71,12 % pour T_S = 0,5 / 1 / 1,25 / 2,5 / 5 / 10 ms avec la politique entraînée à 5 ms (§6.3). 20 plans de référence alternatifs : H_S entre 80,39 et 81,93 % (§6.3).
- Taux de repli : faible pour la méthode (valeurs lues dans la Fig. 9 : 0,0 % à 40 ms, 0,1 % à 10 ms, extraction de figure à vérifier).
→ reportés dans `benchmarks.csv` : aucune ligne (voir ci-dessous).

Pas de ligne de benchmark : les métriques sont des taux de respect de deadline obtenus en simulation, sans FPS, GOPS, latence mesurée, puissance ni ressources FPGA, sur une plateforme simulée qui n'est pas une puce identifiable. Elles n'entrent dans aucune colonne comparable de `benchmarks.csv`.

## Limites et critique

- Évaluation uniquement en simulation, avec des latences profilées ; pas de plateforme réelle, pas de FPGA. Les WCET de la référence sont les latences profilées : la méthode de borne (mesure ou analyse) et sa sûreté ne sont pas discutées (déduit : dans la section lue, aucune analyse d'interférence mémoire n'est faite).
- L'hypothèse sur C_{u,m} englobe les transferts de données ; les interférences de bus et mémoire entre accélérateurs ne sont pas modélisées (§2.1, déduit pour l'absence d'interférence).
- La garantie HRT est un test suffisant, donc conservateur ; en cas de repli, la marge du plan de référence n'est pas récupérée (§5.1). Le coût en SRT n'est pas quantifié en dehors des taux de repli.
- Les baselines non natives HRT sont enveloppées dans la même couche de sûreté : la comparaison porte sur la qualité de la politique sous enveloppe, mais ces variantes ne sont pas les algorithmes d'origine (§6.2). Certaines adaptations (SSML uniprocesseur, CD-MSA) sont des réimplémentations des auteurs.
- La politique est entraînée à d = 10 ms puis testée aussi à 40 ms (note 3) ; 97,43 % si entraînée directement à 40 ms (Fig. 7 légende). Résultats sur une seule charge de travail, sans barres d'erreur mentionnées (n/r).
- Cible : accélérateurs ASIC type Eyeriss/Simba, pas FPGA ; le transfert au FPGA (reconfiguration partielle, DPU) est non traité. Pas de pertes d'exécution anormales (fautes, dérive temporelle) : l'axe « défaillance temporelle » est supposé borné par WCET.
- La politique RL est elle-même un réseau, mais non analysé pour la sûreté : la sûreté ne repose pas sur elle (point fort architectural).
- Preprint non relu par les pairs.

## Pertinence pour la thèse

Apport à l'axe sûreté et temps réel : patron d'architecture « optimiseur appris, enveloppe déterministe certifiée » (safety envelope / repli sur plan de référence) directement transposable à un moniteur ou à un ordonnancement de pipeline de vision sur SoC FPGA multi-accélérateurs, avec garantie indépendante de la politique (Théorème 1) et surcharge bornée de l'ordonnanceur (0,76 % de T_S). Le papier montre qu'un composant appris peut cohabiter avec une exigence de déterminisme sans être certifié lui-même, ce qui répond en partie à la tension apprentissage embarqué / certification. Ce qu'il laisse ouvert : pas de FPGA, pas de modèle d'interférence mémoire (voir gap WCET), pas de lien avec la détection de personnes ni avec les sorties anticipées.

## Gaps identifiés

- Garantie HRT conditionnée à des WCET supposés sûrs : combiner ce type d'enveloppe avec une analyse d'interférence mémoire/bus mesurée sur SoC FPGA (axe timing-analysis).
- Aucun ordonnancement HRT/SRT de DNN validé sur FPGA réel avec accélérateurs hétérogènes (DPU + logique custom) dans ce papier.
- Évaluation de la perte de qualité de service due au repli (non quantifiée hors taux).

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction grobid ok). Section 6 non détectée par l'extraction (rattachée à la section 5, chunks 2610.29503#023-026) : texte présent et lu. Les chiffres des figures (Fig. 5-10) viennent de texte de figure extrait, de qualité variable : les valeurs citées sont celles du corps de texte. Table 2 (travaux liés) tronquée à l'extraction, non exploitable.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de modèle d'interférence mémoire, l'absence de barres d'erreur, la transposabilité au FPGA et à la vision, et l'absence d'analyse de sûreté du réseau RL lui-même.
