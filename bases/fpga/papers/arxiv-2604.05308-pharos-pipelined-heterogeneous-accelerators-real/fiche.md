---
id: arxiv-2604.05308-pharos-pipelined-heterogeneous-accelerators-real
fiche: done
date: 2026-11-03
---

# PHAROS: Pipelined Heterogeneous Accelerators for Real-time Safety-critical Systems With Deadline Compliance

Shixin Ji, Jinming Zhuang, Sarah Schultz, Zhuoping Yang, Xingzhen Chen, Zheng Dong, Alex K Jones, Yihui Ren, Peipei Zhou, 2026, arXiv preprint (2604.05308). https://arxiv.org/abs/2604.05308
Type : preprint non relu par les pairs. Le texte ne mentionne aucune venue (la mention DAC 2026 d'OpenAlex n'est pas confirmée par le texte).

## Problème

Les accélérateurs hétérogènes spatialement partitionnés (HA) sont conçus pour le débit ou la QoS (latence au 99e centile), sans support matériel de prévisibilité, sans exploration d'espace de conception (DSE) orientée temps réel ni analyse d'ordonnançabilité (§1, §2). Les auteurs visent la conformité aux échéances en temps réel souple (SRT : toute tâche a un temps de réponse borné, pas de job abandonné) pour des systèmes critiques (exemple : transport intelligent).

## Méthode

- Architecture (§3.1-3.2) : plusieurs accélérateurs de flot de données indépendants, dataflow output-stationary avec tuilage, double buffering, DMA dédiés vers DDR ; contrôle décentralisé, chaque accélérateur a un ordonnanceur sur puce (table de configuration, table de progression, pool de jobs) en FIFO ou EDF. Ordonnanceur : < 25 octets par entrée, < 1 µs de tri (§3.2).
- Topologie pipeline (§3.3) : un job finit tous ses segments sur un accélérateur avant le suivant, sans retour ; la théorie temps réel de [5] donne alors : SRT-ordonnançable ssi utilisation u_k <= 1 pour chaque accélérateur, en FIFO comme en EDF (éq. 2-3).
- Préemption (§3.4) : intra-couche, à la fin de la tuile courante (sauvegarde des sorties partielles en DDR, état dans la table de progression) ; WCET = exécution + surcharge = tuile + store + load (éq. 4-5). Préemption seulement en EDF.
- DSE (§4) : partition des ressources, affectation des couches consécutives, paramètres du réseau de PE (A,B,C,X,Y,Z) ; objectif min(max u_k) ; recherche par faisceau (beam search). Latences estimées par le modèle de performance de CHARM [3].

## Plateforme et implémentation

Prototype sur Versal VCK5000 (AIE + fabric), dataflow et contrôle adaptés de CHARM (§5.1). Fréquence, ressources consommées (LUT/DSP/BRAM/AIE) : n/r. Puissance : n/r. Code ou bitstream : non mentionnés (non publiés d'après le texte). Les WCET des éq. 4-5 sont issus du modèle CHARM, pas d'une borne mesurée (§5.1).

## Résultats

- Charges (§5.1) : PointNet, Point Transformer (2 blocs), MLP-Mixer (2 blocs), Res-MLP (4 blocs), DeiT-T (2 blocs) tronqués. Latences sur accélérateur unique : 0.23, 0.99, 0.30, 0.38, 0.14 ms (§5.1).
- Tasksets de 2 tâches (un modèle nuage de points + un modèle image), périodes variées ; baseline : DSE guidé par le débit (CHARM), avec FIFO sans/avec polling et EDF (§5.2). max_M = 4, B = 8.
- 49 tasksets ordonnançables contre 13 pour le DSE débit sur PointNet + Bert-B, soit 3.76x (Fig. 1, §1). Sur les 6 combinaisons : 2.28x, 2.28x, 1.44x, 2.25x, 2.17x, 2.10x de solutions faisables de plus que le meilleur baseline TG+FIFO avec polling (§5.2, Fig. 6).
- Utilisation maximale moyenne meilleure de 3.7 %, 4.6 %, -2.4 %, 6.2 %, 3.9 %, 5.1 % ; pire pour PointNet+DeiT-T à B = 8 (suboptimalité), +0.07 % à B = 16 et +3.5 % à B = 32 (§5.2).
- Préemption 10x moins fréquente en SG+EDF qu'en TG+EDF (simulation, §5.2). EDF meilleur en temps de réponse sans surcharge ; avec surcharge, encore meilleur dans 81 %, 80 %, 61 % des designs Point Transformer (§5.3) ; aucune politique dominante.
- Beam search B = 8 : force brute 13.3x (> 500 s) et 117.2x (> 5000 s) plus longue, pour 2.3 % de mieux sur max(util) (§5.4).
- Aucune mesure de FPS, puissance ou précision.
→ reportés dans `benchmarks.csv` : 5 lignes (latences de référence à accélérateur unique, §5.1, confidence medium). Les résultats d'ordonnançabilité sont des comptes de designs, pas des benchmarks au sens du schéma.

## Limites et critique

- Preprint, pas de venue confirmée par le texte ; code et bitstream non publiés.
- Charges tronquées (2 blocs), modèles de transformeurs / nuages de points, aucun détecteur de type YOLO ; pas de CNN.
- Les latences et WCET viennent du modèle CHARM ; l'écart modèle / matériel n'est pas rapporté ici. Le caractère pire cas des WCET n'est pas démontré par mesure (préemption modélisée avec les maxima). Tasksets : ordonnançabilité des baselines TG et SG+EDF jugée par simulation (> 100 périodes), SG+EDF sans garantie à cause de la surcharge.
- Théorie SRT seulement (temps de réponse borné, mais pas d'échéance dure) : insuffisant pour un système de sécurité à échéance dure. Le papier le dit (HRT mentionné comme perspective).
- Hypothèse : tâche = séquence de couches (pas de parallélisme intra-couche des transformeurs, §5.5). Interférences mémoire (DDR partagée, DMA entrelacés) non modélisées dans les WCET.
- Baseline unique (CHARM DSE) ; pas de comparaison avec MESC, ART, DERCA, à architecture accélérateur unique, sauf discussion qualitative (§2).
- Aucun Jetson/GPU comme baseline.

## Pertinence pour la thèse

Axe timing-analysis : exemple de lien entre théorie d'ordonnancement et DSE d'accélérateurs, avec préemption matérielle et bornes de temps de réponse, directement utile aux questions ARCYS (délai de bout en bout, WCET, Lauer). Axe safety-certification : conformité aux échéances comme propriété de sûreté. Limites pour nous : cible Versal AIE (pas Zynq/Kria, pas de YOLO), SRT et non HRT, pas d'interférences mémoire.

## Gaps identifiés

- Analyse de temps de réponse avec interférences DDR réelles pour accélérateurs multiples sur SoC FPGA.
- Ordonnançabilité temps réel dur (HRT) pour des détecteurs de type YOLO avec préemption matérielle.
- Écart modèle / mesure des WCET d'accélérateurs DNN.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction grobid ok, aucun tableau : les résultats sont dans des figures, dont les valeurs ne sont pas dans le texte).
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de code publié (simplement non mentionné), la pertinence pour ARCYS, l'absence de modélisation des interférences DDR (aucune mention dans le texte), la remarque sur l'écart modèle / matériel.
