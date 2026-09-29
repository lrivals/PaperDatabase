# Carte des gaps — stage

Zones non couvertes et verrous repérés dans le corpus. Mis à jour par `/paper-gaps` à partir
des fiches `done` et de `benchmarks.csv`. Chaque gap cite les `paper_id` qui l'étayent et
distingue ce qui est lu de ce qui est déduit.

Format d'une entrée :

```
### <intitulé du gap>
- Constat : ce que montre le corpus (paper_id, section source).
- Ce qui manque : la question laissée ouverte.
- Statut : hypothèse (déduite de la bibliographie de départ) | étayé (fiches done).
- Piste : expérience ou lecture pour le confirmer.
```

---

Mise à jour du 29/09/2026 (1er passage) : **56 fiches `done` sur 56**, **100 lignes** dans
`benchmarks.csv` (35 papiers).

**Réserve générale.** Le corpus est la bibliographie du stage, donc petit et orienté vers la
question « EWC INT8 sur MCU » ; l'absence d'un travail dans la base ne prouve pas son absence dans
la littérature. Un gap est `étayé` quand une ou plusieurs fiches le constatent explicitement
(section citée) ; il reste `hypothèse` quand il ne repose que sur l'absence de papiers ou sur une
déduction.

- Effectifs par axe : `cl-methods` 27, `tinyml-odl` 12, `surveys` 10, `quantization` 10,
  `pdm-rul` 10, `anomaly-detection` 9, `drift-detection` 6, `datasets` 6.
- `benchmarks.csv` : 64 lignes `high`, 36 `medium`, aucune `low` ; 15 lignes sur MCU (7 papiers) ;
  50 lignes d'apprentissage continu, dont 6 en régression (toutes de Shah 2025, sur GPU).
- Neuf fiches sans ligne volontairement (jeux de données, références de méthode, chiffres absents).

---

### Régularisation anti-oubli (EWC, SI, MAS) exécutée sur MCU
- Constat : aucun travail du corpus n'exécute une régularisation de type EWC sur microcontrôleur.
  Les systèmes CL sur MCU utilisent le rejeu latent (arxiv-2110.10486, §2-4), le méta-CL avec
  rejeu compressé (arxiv-2311.11420), ou n'ont aucun mécanisme anti-oubli
  (arxiv-2103.08295, §IV). Le survey d'entraînement embarqué ne recense aucune régularisation
  (arxiv-2212.00824, §2.6 et §7) ; les travaux CL-PdM à régularisation tournent sur GPU
  (2022-maschler, §4 ; 2025-shah, §5.4) ; Hurtado ne cite aucun CL-PdM embarqué
  (arxiv-2301.12467, §6.1).
- Ce qui manque : coût mémoire (Fisher + ancre = 2 × taille des poids entraînés), temps de calcul
  de la Fisher et de la pénalité, et oubli mesuré sur un Cortex-M.
- Statut : étayé (constat explicite de arxiv-2212.00824 §7 et de plusieurs sections « Gaps »).
- Piste : EWC restreint aux couches mises à jour (sparse update, arxiv-2403.19076 §IV-B) sur
  STM32, comparé au rejeu latent de arxiv-2110.10486 au même budget de RAM.

### Importances et ancres en précision réduite (INT8)
- Constat : les papiers de quantification traitent poids et activations, jamais les tenseurs
  auxiliaires d'un algorithme de CL (arxiv-1712.05877 ; arxiv-2106.08295). L'entraînement d'un
  graphe INT8 déforme le rapport ‖W‖/‖G‖ d'un facteur s⁻², corrigé par QAS
  (arxiv-2403.19076, §IV-A), ce qui concerne aussi une Fisher calculée sur gradients INT8 (déduit).
  L'accumulation g·Δθ de SI est sensible à l'arrondi (arxiv-1703.04200, déduit).
- Ce qui manque : format et échelle de stockage de la Fisher et de θ*, effet de la quantification
  des importances sur l'oubli.
- Statut : hypothèse (déduction à partir de papiers qui n'étudient pas le cas).
- Piste : EWC avec Fisher et ancre en INT8 (échelle par couche) contre FP32, sur un scénario
  C-MAPSS ou PRONOSTIA ; mesurer BWT et mémoire.

### Entraînement en précision réduite sur MCU pour l'apprentissage continu
- Constat : l'apprentissage sur MCU se fait en FP32 (arxiv-2103.08295, §III ;
  2022-gimenez, §3.3 ; arxiv-2110.10486, étage adaptatif en FP32). Le seul entraînement INT8 du
  corpus (QAS + mise à jour parcimonieuse, arxiv-2403.19076, Table VII) vise le transfert sur une
  tâche, sans mesure d'oubli.
- Ce qui manque : mise à jour INT8 dans un scénario séquentiel, avec métrique d'oubli.
- Statut : étayé (arxiv-2103.08295 §V « 8-bit » en perspective ; arxiv-2403.19076 §IV).
- Piste : reproduire QAS sur un petit réseau de RUL, puis ajouter une pénalité EWC.

### Apprentissage continu pour la régression et la RUL
- Constat : deux travaux CL-RUL seulement. Maschler discrétise la RUL en trois classes pour
  pouvoir régulariser (2022-maschler, §3, Table 2) ; Shah reste en régression mais en
  task-incremental avec une tête par tâche (2025-shah, §3.2). Les métriques d'oubli (BWT, FWT,
  forgetting) sont définies pour la classification (arxiv-1706.08840 ;
  arxiv-1902.00829 propose des ratios) ; Besnard donne un taux d'oubli en MSE
  (2024-besnard, Eq. 1). Le CL pour la prévision de séries temporelles manque de benchmark commun
  (2024-besnard, §3.3 ; arxiv-2301.12467, §6.3).
- Ce qui manque : EWC en régression (Fisher d'une perte gaussienne), métrique d'oubli standard en
  régression, scénario domain-incremental sans identité de tâche.
- Statut : étayé.
- Piste : EWC sur la RMSE de C-MAPSS, ordre FD001 → FD003 → FD002 → FD004, oubli mesuré en ratio
  de RMSE (2024-besnard Eq. 1) et en score asymétrique.

### Protocole CL standard sur les jeux de pronostic
- Constat : les jeux de référence sont décrits sans scénario séquentiel (2008-saxena ;
  2012-nectoux ; 2016-lessmeier). Leurs conditions opératoires fournissent des tâches naturelles
  (C-MAPSS : 1 ou 6 conditions, 1 ou 2 modes ; PRONOSTIA : 3 conditions ; Paderborn : 4). Shah
  propose des séquences C-MAPSS et batteries « as benchmarks » (2025-shah, §5.3) ; Hurtado propose
  un découpage par concepts non réalisé (arxiv-2301.12467, §7).
- Ce qui manque : ordres de tâches, métriques et nombre de runs fixés, avec bornes (fine-tuning,
  joint training).
- Statut : étayé.
- Piste : adopter les séquences de Shah (Table 2), plusieurs graines, bornes joint / fine-tune,
  pour pouvoir comparer EWC à Online EWC (2022-maschler, Table 4).

### Dérive intra-classe et domaine incrémental plutôt que nouvelles classes
- Constat : la plupart des méthodes de CL du corpus sont évaluées en task- ou class-incremental
  sur images (arxiv-1902.00829 ; arxiv-1910.14481 ; arxiv-2112.04215 ; arxiv-2012.06002 ;
  arxiv-2401.01010, nouvelles classes de produits). En PdM, la dérive est surtout un changement de
  régime ou une usure au sein d'une même classe (arxiv-2301.12467, §7.3). EWC échoue quand la
  dérive entre tâches est forte (arxiv-2312.10549, §3.3.1). L'écart défauts artificiels → réels
  coûte ≈ 30 points de précision (2016-lessmeier, Tables 9 et 11).
- Ce qui manque : évaluation des régularisations sous dérive progressive, sans frontière de tâche.
- Statut : étayé.
- Piste : scénario d'usure progressive (PRONOSTIA) avec Online EWC déclenché par un détecteur de
  dérive (voir le gap suivant).

### Détection de dérive qui déclenche une consolidation, pas une réinitialisation
- Constat : les détecteurs du corpus réinitialisent ou réapprennent le modèle à la détection
  (2004-gama, §3 ; 2006-baena-garcia, §3.2 ; arxiv-2007.05432, §4.3). Seul Aljundi déclenche une
  mise à jour d'importances MAS sur un plateau de la perte (arxiv-1812.03596, §3). Hurtado place
  détection et mise à jour dans un même pipeline sans l'évaluer en PdM (arxiv-2301.12467, Fig. 6).
- Ce qui manque : un couplage détecteur → recalcul de la Fisher / consolidation EWC, évalué sur des
  séries de capteurs.
- Statut : étayé.
- Piste : comparer plateau de perte (Aljundi), DDM/EDDM, KSWIN et Page-Hinkley comme déclencheurs
  de consolidation sur un même scénario.

### Détecteurs de dérive : fausses alarmes et délai jamais mesurés sur données de pronostic
- Constat : DDM et EDDM sont évalués sur données synthétiques et ELEC2, sans délai de détection
  (2004-gama, §4 ; 2006-baena-garcia, §4) ; EDDM multiplie les détections sur données bruitées
  (2006-baena-garcia, Table 1, Gauss) ; KSWIN a plus de faux positifs que de vrais
  (arxiv-2007.05432, Table 2). Le test MMD n'est pas évalué en flux (2012-gretton, §6).
- Ce qui manque : taux de fausses alarmes et délai sur séries de vibrations ou C-MAPSS, et coût
  embarqué de chaque détecteur.
- Statut : étayé.
- Piste : banc de détecteurs sur PRONOSTIA (dérive d'usure) et Paderborn (changement de
  condition), sur un Cortex-M.

### Coût embarqué rarement mesuré (énergie, puissance, latence)
- Constat : `power_w` vaut `n/r` dans 96 lignes sur 100 et `latency_ms` dans 80. Seules deux
  sources donnent une puissance (arxiv-2110.10486, portée `chip` ; 2019-benatti, portée
  `unspecified`). Plusieurs papiers dits « on-device » n'ont aucune mesure sur appareil
  (2024-rub, §IV ; 2025-karim, §IV). Besnard réclame des métriques de coût pour le CL
  (2024-besnard, §3.3).
- Ce qui manque : énergie par mise à jour et par inférence, mesurée et avec sa portée.
- Statut : étayé.
- Piste : mesurer l'énergie d'un pas d'EWC selon la méthode de Tiwari (1994-tiwari, §II-IV :
  coût par noyau × nombre d'exécutions).

### Régularisation contre rejeu à budget mémoire égal, en kilo-octets
- Constat : Hurtado juge le rejeu plus efficace (arxiv-2301.12467, §6.3) ; Wu constate rejeu > MAS
  et SI en régression industrielle (2025-wu-adaptive, §IV) ; les budgets de rejeu sont exprimés en
  images ou en % du jeu, pas en Ko (arxiv-1611.07725 ; 2024-rub). Aucun papier ne compare les deux
  familles au même budget de RAM sur MCU (arxiv-2311.11420 et arxiv-2110.10486, sections « Gaps »).
- Ce qui manque : courbe oubli / mémoire pour EWC, rejeu latent et rejeu distillé.
- Statut : étayé (absence constatée dans plusieurs fiches), à confirmer hors corpus.
- Piste : même réseau, même budget (par exemple 64 Ko), trois stratégies, sur C-MAPSS.

### Détection d'anomalies légère et adaptative pour l'embarqué
- Constat : PCA et Isolation Forest restent proches des réseaux profonds pour un coût dérisoire
  (2023-belay, Table 2) ; les détecteurs performants sont lourds (2019-su, GRU 500 et flow ;
  arxiv-1711.00614, LSTM-VAE) ou visuels (arxiv-2401.01010) ; TinyOL n'adapte que la dernière
  couche d'un autoencodeur (arxiv-2103.08295). iForest et Mahalanobis sont statiques
  (2008-liu, §6 ; 1936-mahalanobis, §4).
- Ce qui manque : détecteur léger (AE réduit, Mahalanobis à covariance en ligne, iForest réduit) qui
  s'adapte à la dérive sur MCU, avec seuil adaptatif (POT : 2019-su §4.4 ; seuil par régime :
  arxiv-1711.00614 §IV-B).
- Statut : hypothèse (déduit de l'absence de tels travaux dans le corpus).
- Piste : comparer AE INT8, Mahalanobis et iForest réduit sur features vibratoires, en mémoire et
  en énergie.

### Données réelles run-to-failure et conditions variables
- Constat : C-MAPSS est simulé (2008-saxena, §III-V) ; PRONOSTIA garde des conditions constantes
  par essai (2012-nectoux, §VI) ; Paderborn fournit des états figés, sans run-to-failure
  (2016-lessmeier, §4-5) ; Helwig simule des défauts réversibles (2015-helwig, §III). Berghout
  réclame des données réelles et hétérogènes (2022-berghout, §6.1).
- Ce qui manque : jeu public avec dégradation réelle sous conditions changeantes.
- Statut : étayé.
- Piste : chercher des jeux plus récents (XJTU-SY, cité par 2022-berghout §4.5) avec
  `/paper-discover datasets`.

### Évaluations non comparables d'un papier à l'autre
- Constat :
  - le point-adjust gonfle les F1 de détection d'anomalies (2019-su, §5.1) ;
  - la RUL est évaluée en MSE sans score asymétrique ni comparaison externe (2021-kang, §5) ;
  - les coefficients du score C-MAPSS divergent selon les sources (2008-saxena Fig. 9 ; 2025-shah
    Eq. 34 ; 2022-berghout Eq. 2) ;
  - plusieurs résultats reposent sur un seul run ou sans écart-type (2025-shah ; 2022-maschler ;
    2025-wu-adaptive) ;
  - des chiffres se contredisent entre texte et tableaux (2025-shah Table 29 ; 2016-lessmeier
    Table 11 ; 2019-benatti §I contre Abstract ; 2023-belay Table 3).
- Ce qui manque : protocole commun (métriques, graines, bornes) avant toute comparaison chiffrée.
- Statut : étayé.
- Piste : vérifier la formule du score C-MAPSS dans le PDF de 2008-saxena avant de la citer ;
  toujours rapporter RMSE et score, sur plusieurs graines.

### Code rarement publié
- Constat : 16 fiches notent un code non publié, dont tous les travaux CL-PdM
  (2022-maschler ; 2025-shah ; 2025-wu-adaptive ; 2024-rub) et TinyOL (arxiv-2103.08295) ; les
  codes publiés viennent surtout de la vision (arxiv-2112.04215 ; arxiv-2401.01010 ;
  arxiv-2403.19076) ou de systèmes MCU (arxiv-2311.11420 ; 2022-gimenez ; arxiv-1801.06601).
- Ce qui manque : implémentations de référence réutilisables pour le CL sur séries de capteurs.
- Statut : étayé.
- Piste : publier le code du stage (EWC INT8) avec les séquences de tâches, pour combler ce vide.

### Apprentissage continu non supervisé sur signaux de capteurs
- Constat : les approches de CL sans labels (arxiv-1910.14481 ; arxiv-2112.04215 ;
  arxiv-2401.01010) sont évaluées sur images ; MAS peut calculer ses importances sans labels
  (arxiv-1711.09601) et EWC reste compétitif avec une perte auto-supervisée
  (arxiv-2112.04215, §6.2).
- Ce qui manque : CL auto-supervisé ou non supervisé sur vibrations, où les labels de défaut sont
  rares.
- Statut : hypothèse.
- Piste : EWC ou MAS dont les importances sont calculées sur la perte de reconstruction d'un
  autoencodeur de vibrations.
