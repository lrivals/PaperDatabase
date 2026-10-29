---
id: 2021-fuentes-open-set-self-across-domain
fiche: done
date: 2026-10-29
---

# Open Set Self and Across Domain Adaptation for Tomato Disease Recognition With Deep Learning Techniques

Alvaro Fuentes, Sook Yoon, Taehyun Kim, Dong Sun Park, 2021, Frontiers in Plant Science 12. https://doi.org/10.3389/fpls.2021.758027
Type : article de journal (relu par les pairs)

## Problème

Les systèmes de reconnaissance de maladies perdent en performance sur de nouvelles fermes et des données jamais vues (Abstract, #000.0). Les auteurs posent le diagnostic comme un problème « open set » : à l'inférence, une région doit être rangée dans une classe connue ou déclarée « inconnue », pour éviter un faux diagnostic et recommander une procédure supplémentaire (§General Settings, #007.0). L'inconnu n'existe que dans le domaine cible (une autre ferme).

## Méthode

Deux modules (Fig. 4, #033.0) :
- Détecteur de boîtes : « Filter Bank v2 » = Faster R-CNN avec ResNet-50 + FPN, suivi d'un banc de CNN par classe qui vérifient chaque ROI (§Bounding Box Detection, #010.0 ; §Implementation).
- Adaptation open set : extracteur ResNet-50 pré-entraîné ImageNet, classifieur Gs (classes connues) + Gn (contrôle) ; la classe « background » (zones de fond de la serre) sert d'instances négatives, entraînées avec L_s + L_n (Éq. 2, #011.0). Puis adaptation à la ferme cible : F_s et G gelés, un second extracteur F_t est entraîné, sortie = concaténation de Gs et Gt (Éq. 3, #011.0). Source : lot 64, 30 000 itérations, lr 0,001 ; cible : lot 64, 30 000 itérations, lr 0,0001 (#023.0).
- Niveau d'ouverture (Scheirer) : openness = 1 − 2 × train/(test+cible) (formule telle qu'extraite ; la racine de Scheirer est peut-être perdue) ; valeurs testées 0 (fermé), 33, 62, 73 % (§Known and Unknown Classes, #007.0, #020.0).
- Métriques (Saito, Bucci) : OS* (exactitude normalisée sur les classes connues), UNK (exactitude sur la classe inconnue), OS (moyenne sur K+1 classes), HOS = moyenne harmonique de OS* et UNK, qui pénalise un écart connu/inconnu (Éq. 7-9, #014.0).

## Plateforme et implémentation

Pas de cible matérielle : n/r (aucune latence, fps, puissance, quantification). Entraînement GPU non précisé. Code publié : non mentionné dans le texte lu (n/r).

## Résultats

Jeu : dataset tomate des auteurs (Corée du Sud), 12 maladies/ravageurs/carences + feuilles saines + fond, trois fermes F1, F2, F3 (#016.0). Six transferts : F1→F2, F1→F3, F2→F1, F2→F3, F3→F1, F3→F2.
- Détecteur : mAP@0,5 = 94,76 %, +1,8 point sur Filter Bank (Fuentes 2018) sur ce jeu ; détecteur entraîné et validé sur tout le jeu, toutes fermes confondues (Table 3, #025.0).
- Adaptation : en fermé (0 %), meilleur cas F1→F2 : 94,30 % (OS*). L'exactitude baisse avec l'ouverture, pour OS*, OS et UNK ; l'inconnu est toujours moins bien reconnu que le connu ; F1→F3 et F3→F1 sont les plus durs (ferme moderne vs traditionnelle) ; F1→F2 et F2→F3 les meilleurs (#025.2, #027.0).
- Tables 4, 5, 6 (OS*, OS, HOS par ouverture et transfert) : corps non extrait ; seule valeur chiffrée dans le texte : 94,30 %. Les chiffres en mode ouvert (33/62/73 %) ne sont donc pas disponibles ici.
→ reportés dans `benchmarks.csv` : 2 lignes proposées à l'agent principal (détecteur ; OS* fermé F1→F2).

## Limites et critique

- Chiffres en mode ouvert absents de l'extraction ; le texte dit seulement « decay » sans valeur (#025.2, #027.0).
- Le « domaine cible non étiqueté » (§Open Set Domain Adaptation) cohabite avec un entraînement cible « avec classes connues et inconnues » (#023.0) et une perte CE sur y_p (Éq. 3) : la nature de la supervision cible (pseudo-étiquettes ? étiquettes ?) n'est pas claire. Déduit : l'inconnu est probablement étiqueté en cible.
- « Inconnu » = classes de maladie retirées de l'entraînement source puis présentes en cible ; ce n'est pas du hors-distribution générique (autre plante, image sans feuille).
- Pas de comparaison à une baseline open set (OSBP, etc.) ni à du fermé avec seuil de confiance ; pas de calibration (ECE) ; pas d'intervalle de confiance (moyenne de 3 essais seulement).
- Les classes connues/inconnues et les ouvertures dépendent du choix de classes (Table 2, sans corps).
- Détecteur évalué sans séparation par ferme : pas de test hors domaine pour le détecteur.
- Pas de contrainte de ressources : détecteur à deux étages + banc de CNN, lourd pour un Hailo-8L (déduit).

## Pertinence pour SerreIA

Voir « Pour SerreIA » ci-dessous. Pour la base : référence directe sur le rejet de l'inconnu et l'écart de domaine entre fermes, sur tomates en serre (axes disease-classif, domain-shift, calibration-decision).

## Pour SerreIA

Ce que le projet peut reprendre :
- **Classe « background/négatif » explicite** : le classifieur apprend des régions de fond de serre comme classe négative (Gn, L_n ; #011.0). C'est la version apprise de l'idée « remplacement de fond » jamais testée (`data/backgrounds/` absent) : au lieu d'effacer le fond, apprendre à le rejeter. À greffer dans `vision/models/multihead.py` (tête de rejet) et dans `vision/datasets/prepare.py` / `build_yolo_dataset.py` (crops de fond, hard negatives issus des faux positifs de YOLOv8n sur images saines, 42 %).
- **Classe « unknown » apprise** plutôt qu'un seuil de confiance : à comparer, dans `vision/eval/decision_search.py`, à un seuil sur la confiance calibrée (`vision/eval/temperature.py`) pour réduire les fausses alertes à rappel donné.
- **Protocole de test inter-domaine à ouverture variable** : retirer 0/33/62/73 % des classes de l'entraînement, mesurer OS*, UNK, HOS (#014.0). À ajouter à `vision/eval/metrics.py` et `cross_domain_eval.py` : HOS résume en un chiffre le couple rappel-classes-connues / rejet-inconnu, là où le rappel PlantDoc 0,986 avec spécificité 0,50 cache l'effondrement du rejet.
- **Expérience à faire** : entraîner EfficientNet-B0 PlantVillage+CCMT avec une classe fond/inconnu (crops de fond de serre + feuilles d'espèces absentes), tester sur PlantDoc et mesurer spécificité, F1 classe, HOS et ECE avant/après ; puis la même chose en cascade avec YOLOv8n (faux positifs sur images saines). Métrique de décision : HOS ou spécificité à rappel fixé.
- **Mode d'emploi du rejet** : « classe inconnue → procédure supplémentaire » (#007.0) correspond à la validation humaine de l'agent LLM : une sortie « inconnu » déclenche la revue.

Comparabilité des chiffres : **non comparables**. Jeu tomate propre aux auteurs (Corée, trois serres, caméras variées), pas PlantVillage/PlantDoc ; le test est en transfert entre fermes avec adaptation sur la cible (non étiquetée selon le texte), donc ni sans accès à la cible ni « sur PlantDoc sans adaptation » comme SerreIA. Métriques différentes (OS*, HOS, mAP@0,5 contre rappel, précision, F1, ECE). Le 94,76 % (détecteur) est mesuré sur le jeu entier, ferme mélangées : même défaut de flatterie que le 0,956 de YOLOv8n. Le 94,30 % est en fermé (ouverture 0 %), le chiffre le plus favorable. Seul point commun : la direction de l'effet (baisse entre domaines, rejet de l'inconnu plus dur que la reconnaissance du connu), qui concorde avec la spécificité de 0,50 de SerreIA. Ressource : détecteur à deux étages, pas de mesure edge ; effet sur Hailo-8L inconnu.

## Gaps identifiés

- Aucun chiffre open set en serre sur un jeu public (PlantDoc) ni avec baseline open set classique.
- Rejet de l'inconnu : jamais couplé à la calibration (ECE) ni à une quantification INT8 / NPU.
- Peu de travaux comparent classe fond apprise, remplacement de fond et seuil calibré sur une même évaluation hors domaine.

## Statut de lecture

Sections lues : Abstract, Open Set Domain Adaptation (méthode), Evaluation Metrics, Experimental Results, Conclusion, table 3 ; lecture ciblée par recherche et plages de lignes, pas de lecture intégrale (Introduction et Related Works non lues). Extraction grobid ok ; Tables 2, 4, 5, 6 sans corps : chiffres open set indisponibles.
Déduit et non affirmé par les auteurs : nature de la supervision cible, lourdeur pour Hailo-8L, concordance avec la spécificité de SerreIA, mise en correspondance fond appris / remplacement de fond.
