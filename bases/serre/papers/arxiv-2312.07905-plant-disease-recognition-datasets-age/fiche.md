---
id: arxiv-2312.07905-plant-disease-recognition-datasets-age
fiche: done
date: 2026-10-29
benchmarks: none
---

# Plant Disease Recognition Datasets in the Age of Deep Learning: Challenges and Opportunities

Mingle Xu, Ji Eun Park, Jaehwan Lee, Jucheng Yang, Sook Yoon, 2023, arXiv preprint. https://arxiv.org/abs/2312.07905
Type : preprint non relu par les pairs (pas de DOI)

## Problème

Deux questions posées par les auteurs : comment différencier les datasets de maladies des plantes
pour choisir les datasets publics adaptés à une application, et quelles caractéristiques un dataset
doit avoir pour donner de bonnes performances en conditions réelles (2312.07905#000.0).

## Méthode

Survey, sans expérience propre. Les auteurs proposent une taxonomie des datasets (Table 1) :
objectif applicatif, modalité d'entrée, acquisition (capteur et plateforme, §2.3), variation des
images (§2.4), découpage train/val/test (§2.5) et stratégie d'annotation (§2.6). Ils recensent
ensuite des datasets publics d'images RGB (§3, Table 3) : culture, nombre de classes et d'images,
fond (simple/moyen/complexe), tâche (classification, détection, segmentation) et performance
officielle (2312.07905#009.0, 2312.07905#009.1). Le recensement n'est pas exhaustif, de l'aveu des
auteurs (2312.07905#009.0). Pas de matériel : section « Plateforme et implémentation » sans objet.

## Plateforme et implémentation

Sans objet (pas d'implémentation). Liste des datasets publiée sur GitHub par les auteurs, lien non
reproduit dans le texte lu (2312.07905#009.1).

## Résultats

Pas de résultat expérimental propre. Constats du survey :
- Les images RGB prises à la main dominent les datasets publics (2312.07905#009.0).
- Performances officielles élevées sur la plupart des datasets, sauf quand le fond change : un
  modèle entraîné sur PlantVillage (fond simple) chute sur FieldPV, 0,720 Acc officielle ; même
  situation sur FieldPlant, 0,144 mAP (2312.07905#009.2, 2312.07905#022.2, 2312.07905#022.3).
- Aucun dataset n'est utilisé et comparé par la majorité des travaux, sauf PlantVillage
  (2312.07905#009.2).
- Table 3, lignes utiles à SerreIA : PlantVillage, 14 cultures, 38 classes, 54 305 images, fond
  simple ; PlantDoc (version classification), 13 cultures, 27 classes, 2 598 images, fonds
  complexe+moyen+simple ; PlantDoc (version détection `obj`), mêmes effectifs ; CCMT, 4 cultures,
  22 classes, 24 881 images, fond moyen. Performance officielle « N.A » pour ces quatre
  (2312.07905#022.2).
→ reportés dans `benchmarks.csv` : aucune ligne (survey ; les chiffres sont ceux de travaux cités).

## Limites et critique

- Recensement partiel, centré sur les datasets les plus utilisés ou récents (2312.07905#009.0).
- Table 3 ne donne ni licence, ni résolution, ni conditions d'éclairage, ni appareil : les licences
  et les conditions d'usage sont absentes du texte lu (aucune occurrence de « licen* »).
- Aucune culture de la Table 3 n'est fraise, salade ou aromatique (lu dans la table) ; tomate :
  TaiwanTomato (622 images), plus PlantVillage et PlantDoc.
- Les performances officielles de la Table 3 ne sont pas comparables entre datasets (métriques et
  protocoles différents : AUROC, F1, Acc, mAP).
- Les biais de PlantVillage et PlantDoc ne sont pas analysés en détail : le survey ne retient que
  le fond (simple/complexe) et l'effondrement sur FieldPV. Le reste (fond uniforme, doublons) est
  déduit, voir « Pour SerreIA ».
- Preprint, avis normatifs des auteurs (« nous soutenons que… ») sans validation expérimentale.

## Pertinence pour la thèse

Cette base sert SerreIA, pas une thèse : voir « Pour SerreIA ». Le papier donne le cadre pour
choisir des datasets et décrire l'écart labo/terrain, et des règles de découpage et d'annotation
pour les images propres.

## Pour SerreIA

**Datasets de la revue utiles.** Datasets déjà utilisés par SerreIA, tels que décrits en Table 3
(2312.07905#022.2) :
- PlantVillage : 54 305 images, 38 classes, fond simple (laboratoire). Utile pour l'entraînement,
  mais ne représente pas la serre.
- CCMT : 24 881 images, 22 classes, fond moyen (organes déplacés sur fond simplifié, en plein
  champ, par définition de la revue, 2312.07905#009.1).
- PlantDoc : 2 598 images, 27 classes, fonds mélangés (complexe, moyen, simple) ; la revue liste
  deux versions, classification et détection (`PlantDocObj`), donc des boîtes existent. C'est le
  seul des trois à porter l'annotation par boîtes selon la revue, ce qui sert au détecteur de
  feuilles.
- Autres datasets de la table, à examiner comme compléments hors domaine : FieldPV (665 images,
  14 cultures, fond moyen+simple) comme jeu de test labo vers terrain ; PDD271 (2 710 images,
  271 classes) ; TaiwanTomato (622 images, 6 classes). Ces deux derniers sont déduits utiles par
  nous, la revue ne les recommande pas.
- Espèces visées plus tard (fraise, salades, aromatiques) : aucune dans la Table 3. Les images
  propres sont donc nécessaires pour elles (constat de lecture de la table).
- Licence : non rapportée par la revue ; à vérifier dataset par dataset sur les sources originales.
- Conditions serre : la taxonomie distingue laboratoire, serre et champ comme environnements
  (Table 1) mais la Table 3 ne signale aucun dataset « serre » en tant que tel.

**Biais et pièges connus.**
- Fond : un modèle appris sur PlantVillage (fond simple) s'effondre quand le fond varie, cas
  FieldPV et FieldPlant (2312.07905#009.2). Un modèle entraîné sur images à environnement contrôlé
  a de faibles performances sur environnement non contrôlé (2312.07905#006.1). Cohérent avec
  l'écart PlantVillage/CCMT vers PlantDoc mesuré en phase 1 de SerreIA.
- Découpage aléatoire : plusieurs images d'une même observation presque identiques peuvent se
  retrouver en train et test, ce qui surestime la performance (2312.07905#007.1). Recommandé :
  découper par lieu et par date, voire par photographe (2312.07905#007.2). Déduit : pour PlantVillage
  (plusieurs vues d'une même feuille, non dit dans la revue) c'est un risque ; vérifier le
  dédoublonnage de SerreIA, qui a déjà écarté des groupes contradictoires.
- Bruit d'annotation : trois experts n'atteignent que 85,9 % de précision moyenne sur 999 images de
  blé ; le bruit en validation fausse le choix des hyperparamètres (2312.07905#008.1). Ce chiffre
  concerne le blé, pas PlantDoc ; PlantDoc et ses étiquettes plus fines sont déduits sensibles au
  même problème, sans mesure dans la revue.
- Variations intra-classe (stade de croissance) et inter-classe faibles (maladies voisines) rendent
  la classification difficile (2312.07905#006.1).

**Recommandations pour les images propres de la serre.**
- Protocole d'acquisition : enregistrer des métadonnées (lieu/zone de la serre, date et heure,
  espèce, stade) : la revue demande lieu et horodatage pour permettre des tests de généralisation
  spatiale et temporelle (2312.07905#011.0). Varier échelles, points de vue et recto/verso de la
  feuille (2312.07905#013.0). Prises répétées dans le temps d'une même plante pour suivre
  l'apparition des symptômes et l'alerte précoce (2312.07905#013.0). Documenter le fond : classer
  chaque image en simple/moyen/complexe comme la revue (2312.07905#006.2). Caméra fixe ou sur bras
  mobile en serre, jugée avantageuse par les auteurs (2312.07905#005.0).
- Jeu de test : constituer un jeu hold-out séparé par zone, par date et par session de prise de vue
  (2312.07905#007.1, 2312.07905#007.2), pas par tirage aléatoire d'images.
- Annotation : commencer par un niveau image, puis boîtes pour le détecteur ; les annotations
  partielles sont admises (images non annotées, ou quota par classe) (2312.07905#008.0). Pour les
  boîtes, fixer à l'avance un niveau unique (global, local ou semi) par maladie : la revue
  recommande une stratégie adaptative par maladie et note l'incohérence entre annotateurs
  (2312.07905#008.4, 2312.07905#008.5). Règles EEP : une annotation par motif visuel, tout motif
  annoté, localisation précise (2312.07905#008.3). Vote de plusieurs experts ; PCR comme
  vérité terrain si possible (2312.07905#008.2).
- Passage à l'échelle : la revue cite le crowdsensing, avec annotation communautaire, pour
  augmenter la variété (2312.07905#014.0) ; peu réaliste pour SerreIA, déduit.
- Jeux de test de « défi » : séparer les espèces ou zones vues en entraînement, tester une maladie
  nouvelle (reconnaissance en ensemble ouvert) (2312.07905#011.1), ce qui rejoint le rejet hors
  distribution de SerreIA.

## Gaps identifiés

- Aucun dataset public de maladies de fraise, salade ou aromatiques dans cette revue : à chercher
  ailleurs (`/paper-discover`).
- Licences des datasets : non traitées par les revues ; à documenter à part.
- Dataset serre avec fonds contrôlés et métadonnées lieu/date : non recensé.

## Statut de lecture

Sections lues : résumé, §2.3 à §2.6, §3, §4.1 à §4.5 et Table 3, via passages (`pdb search`/`show`
et lecture ciblée de `fulltext.md`) ; pas toute la lecture linéaire du papier. Extraction GROBID ok.
Déduit et non affirmé par les auteurs : tous les liens vers SerreIA, la sensibilité de PlantDoc au
bruit d'annotation, le risque de doublons dans PlantVillage, l'utilité de FieldPV/PDD271/TaiwanTomato,
l'irréalisme du crowdsensing pour SerreIA, et la mention « pas de licence » (absence dans le texte lu).
