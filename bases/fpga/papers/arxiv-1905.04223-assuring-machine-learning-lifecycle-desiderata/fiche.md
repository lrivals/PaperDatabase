---
id: arxiv-1905.04223-assuring-machine-learning-lifecycle-desiderata
fiche: done
date: 2026-09-29
benchmarks: none
---

# Assuring the Machine Learning Lifecycle: Desiderata, Methods, and Challenges

Rob Ashmore, Radu Calinescu, Colin Paterson, 2019, arXiv preprint. https://arxiv.org/abs/1905.04223
Type : preprint non relu par les pairs (survey ; la mention de venue n'apparaît pas dans le texte extrait).

## Problème

Utiliser du ML dans des systèmes critiques pour la sûreté exige des preuves (« assurance
evidence ») que le composant ML est adapté à son usage et bien intégré, de quoi construire
des assurance cases (§1). Les surveys existants se limitent à un type de ML, à une étape du
cycle de vie ou à une technique (vérification formelle, interprétabilité, RL sûr) et ne
traitent pas l'assurance de bout en bout (§3). Les auteurs proposent un survey couvrant
tout le cycle de vie du ML.

## Méthode

Survey structuré, sans expérience. Cycle de vie en quatre étapes (Fig. 1, §1) : Data
Management, Model Learning, Model Verification (les trois formant le « ML workflow »), puis
Model Deployment. Pour chaque étape (§4 à §7) : artefacts d'entrée et de sortie, activités,
**desiderata d'assurance**, méthodes existantes (tableaux 1, 3, 5, 7), défis ouverts
(tableaux 2, 4, 6, 8, identifiants DM01-DM11, ML01-ML10, MV01-MV08, MD01-MD06).

- Data : Relevant, Complete, Balanced, Accurate (§4.3). Distinction utile entre espace
  d'entrée I, domaine opérationnel O, domaine de défaillance F (état du système, p. ex. objectif
  fissuré) et domaine adverse A (§4.4.2).
- Learning : Performant, Robust, Reusable, Interpretable (§5.3).
- Verification : Comprehensive, Contextually Relevant, Comprehensible (§6.3) ; tests
  normaux vs de robustesse, couverture de données et de modèle, vérification formelle (SMT,
  interprétation abstraite AI², VoRF pour forêts aléatoires) (§6.4).
- Deployment : Fit-for-Purpose, Tolerated, Adaptable (§7.3). Quatre types de monitoring :
  entrées, environnement, **internes du modèle (protection contre les SEU)**, sorties (§7.2.2).

## Plateforme et implémentation

Sans objet (survey). Aucun matériel, code ou bitstream. Une seule mention matérielle : les
représentations numériques différentes entre étapes changent précision et énergie, d'où le
besoin de tests sur la cible (« on-target testing », §7.4.1).

## Résultats

Pas de mesure. Principaux apports, tous issus du texte :
- Cadre de desiderata par étape (§4.3, §5.3, §6.3, §7.3) et catalogue de 4 tableaux de
  méthodes ; 35 défis ouverts identifiés (Tables 2, 4, 6, 8).
- Constat que les méthodes de vérification formelle sont peu nombreuses, limitées aux
  réseaux de neurones et peu contextualisées ; les méthodes de test dominent (§6.5).
- Côté déploiement : le WCET d'un réseau n'ajoute pas de difficulté particulière car l'effort de calcul
  est quasi indépendant de l'entrée (§7.4.1) ; architectures tolérant les sorties erronées
  (moniteur de sortie, agrégateur de modèles « indépendants » à la n-version, commutateur
  vers une valeur sûre ou la dernière bonne) (§7.4.2) ; mise à jour par état sûr, double
  canal live/backup, ou hot code loading (§7.4.3).
→ reportés dans `benchmarks.csv` : aucune ligne (survey, aucun chiffre matériel).
`benchmarks: none` dans le front-matter.

## Limites et critique

- Survey de 2019 : ne couvre ni les normes (IEC 61508, ISO 26262, DO-178C…)
  ni leur application au ML, ni les travaux ultérieurs (ISO/IEC TR 5469, prédiction
  conforme, OOD moderne). Il ne traite pas l'assurance du système complet (§7, hors périmètre
  déclaré).
- Aucun critère de sélection de la littérature ni méthodologie de revue systématique
  décrits dans le texte lu, malgré l'adjectif « comprehensive » (déduit).
- Le déploiement matériel est à peine évoqué : rien sur les FPGA ni sur la quantification
  comme risque pour la preuve d'assurance, sauf la remarque sur les numériques et le SEU (§7.2.2, §7.4.1).
- Pas d'exemple d'assurance case complet ni de cas industriel évalué ; la validité des
  desiderata reste conceptuelle.
- Les tableaux 1, 3, 5, 7 sont extraits en pièces (cases ✔/★ mal alignées) : leur contenu
  fin n'est pas exploitable, seul le texte l'est.

## Pertinence pour la thèse

Axe `safety-certification`, cœur du sujet. Fournit un vocabulaire et une grille pour bâtir
l'argumentaire d'assurance d'un YOLO sur FPGA : desiderata de données (Complete sur les
domaines O, F, A ; pertinent pour des personnes en zone dangereuse avec EPI, éclairage,
occlusions), vérification (couverture, robustesse), et surtout étape Deployment : moniteur
de sortie, détection de distribution shift (MD01), redondance de modèles (MD05), commutateur
vers repli sûr, surveillance des internes contre les SEU, WCET, enregistrement pour enquête
post-incident (MD02). Reste ouvert pour la thèse : traduire ces desiderata en exigences
vérifiables par une norme (IEC 61508 / ISO/IEC TR 5469) et les instancier sur un
accélérateur FPGA (déterminisme, quantification, fautes matérielles).

## Gaps identifiés

- Lien entre desiderata d'assurance ML et preuves au niveau matériel FPGA (quantification,
  SEU dans les poids/config, HLS) : non traité ici.
- Défis MD01 (distribution shift en temps réel), MD03 (mesure de confiance), MD04
  (moniteur souple) : à croiser avec les travaux OOD / prédiction conforme sur embarqué.
- Indépendance de modèles entraînés sur les mêmes données (MD05) : intérêt pour une
  redondance sur FPGA (diversité de modèles ou de quantification), non étudié.
- Aucun cas sur la détection de personnes en milieu industriel.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, 516 lignes ; extraction GROBID `ok`). Défauts
d'extraction : la section 2 (présentation du cycle de vie) est rattachée à l'introduction ;
les tableaux 1, 3, 5, 7 sont des fragments, seul leur libellé de méthode est lisible ;
Table 6 lisible, Tables 2, 4, 8 reconstituées à partir du texte et des sections « Figures et tableaux ».
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de méthodologie de revue
systématique ; les limites liées aux normes ultérieures à 2019 ; le total de 35 défis
(comptage DM01-11, ML01-10, MV01-08, MD01-06) ; les liens avec le cas YOLO / FPGA.
