---
id: arxiv-1708.02750-extreme-clicking-efficient-object-annotation
fiche: done
date: 2026-10-05
benchmarks: none
---

# Extreme clicking for efficient object annotation

Dim P Papadopoulos, Jasper R R Uijlings, Frank Keller, Vittorio Ferrari, 2017, arXiv preprint (ICCV 2017 d'après la littérature, non indiqué dans `metadata.json`). https://arxiv.org/abs/1708.02750
Type : preprint non relu par les pairs

## Problème

Dessiner une boîte englobante « à l'ancienne » (clic sur un coin imaginaire, glisser vers le coin opposé, ajuster les côtés) est lent : 35 s par boîte de qualité pour ILSVRC (Abstract, §1). Les auteurs l'expliquent par le changement de tâche permanent (3 sous-tâches) et par l'imagerie mentale (rectangle et coins imaginaires, souvent hors de l'objet) (§1).

## Méthode

- **Extreme clicking** : l'annotateur clique 4 points physiques de l'objet (haut, bas, gauche, droite), dans n'importe quel ordre ; la boîte en est déduite. Pas de rectangle, pas d'ajustement, pas de bouton « submit » (§1, §3.1).
- **Consigne** : image + nom de classe ; cliquer les 4 points sur la partie visible d'un objet de cette classe ; durée suggérée 10 s au total, borne issue d'un petit pilote (§3.1). Une seule instance annotée par classe et par image (§5).
- **Formation** (§3.2, Fig. 2-3) : lecture des consignes, puis test de qualification de 5 images de la même classe, avec retour détaillé. Les images de qualification viennent d'un autre dataset que celui annoté et ont un masque de segmentation vérité terrain. Zone acceptée pour chaque clic : pixels du masque à moins de 10 px en y du point extrême, plus tout pixel à moins de 10 px d'eux (tolérance dedans et dehors). Réussite si les 4 clics des 5 images sont dans les zones ; échec : test répétable sans limite ; un annotateur qualifié ne repasse jamais le test.
- **Annotation et contrôle qualité** (§3.3) : lots de 10 images de la même classe (évite la relecture du nom de classe et le changement de tâche) ; une « golden question » (image d'évaluation avec masque vérité terrain) cachée dans chaque lot ; l'annotateur qui échoue dessus ne peut pas soumettre. Aucun rejet a posteriori.
- **Bonus segmentation** (§4, §6) : les 4 points initialisent GrabCut (modèle d'apparence de l'objet via contour estimé par chemin de plus forte réponse de contours, squelette fixé à « objet », potentiel de paire fondé sur les réponses de contours). Hors du cœur de la base.

## Plateforme et implémentation

Crowdsourcing sur Amazon Mechanical Turk (§5). Paiement 0,15 $ par lot de 10 images, soit environ 7,7 $/h d'après leurs temps ; coût total 147 $ (VOC 2007 trainval, 5011 images) et 167 $ (VOC 2012 train, 5717 images) (légende Table 3, §5). Code ou outil publiés : non mentionnés dans le texte lu (n/r).

## Résultats

**Coût d'annotation**
- Référence « classique » : 25,5 s (dessin) + 9,0 s (vérification) = 34,5 s par boîte (médianes de Su et al. pour ILSVRC) ; avec rejets et redessin, 55 s ; en moyenne au lieu de médiane, 117 s (§2). La vérification n'est pas incluse dans les 7 s d'extreme clicking, mais le contrôle qualité est assuré par la golden question.
- Extreme clicking : 7,0 s par boîte sur VOC 2007 (14,3 h pour le dataset) et 7,2 s sur VOC 2012 (16,8 h), contre 70,0 h et 79,8 h au tarif 34,5 s ; gain 5x (Table 1, §5.1).
- Par clic : ~2,5 s pour le premier (recherche visuelle de l'objet), ~1,5 s pour les suivants (§5.2).
- Alternatives (Table 2, VOC 2007 ; corps du tableau reconstruit par PyMuPDF : à vérifier) : vérification de boîtes générées [47] 4,5 s par boîte, 81 % à IoU>0,5, mAP 50 (AlexNet) / 58 (VGG16) ; WSOL [5] 0 s, mAP 35 / 35 ; dessin de [54] 12,3 s avec 71 % à IoU>0,7 (sous-ensemble ILSVRC non précisé). Le texte confirme : vérification 1,6x plus rapide, 97 % corrects vs 81 %, mAP +6 à +8 pour les clics ; WSOL ~35 % vs 66 % (§5.1).

**Qualité**
- Accord entre experts PASCAL (GT Boxes vs boîtes ajustées aux segmentations GT « SegBoxes ») : 88 % mIoU, 93 % des boîtes à IoU>0,7 sur VOC 2007 (§5.1).
- Extreme clicks vs GT SegBoxes, VOC 2007 : mIoU 88, IoU>0,7 92 %, IoU>0,5 98 % ; PASCAL GT : 88 / 93 / 98. VOC 2012 : 87 / 91 / 95 pour les clics, 87 / 90 / 96 pour GT (Table 1).
- Extreme clicks vs GT Boxes, VOC 2007 : mIoU 88, IoU>0,7 94 %, IoU>0,5 97 % (Table 2).
- Repère : perturber chaque coordonnée des GT Boxes de 4 px donne aussi 88 % mIoU (§5.1).
- Détecteur Fast R-CNN entraîné sur boîtes extreme clicking vs GT : identique (VOC 2007 : 56 AlexNet, 66 VGG16 ; VOC 2012 : 52 / 62) (Table 1).

**Ablation formation / contrôle qualité** (200 images VOC 2007, Table 3 ; corps du tableau non extrait, chiffres tirés du texte) : sans test de qualification 75,4 % mIoU ; avec 85,7 % ; avec contrôle qualité en plus 87,1 % (§5.2). Le test de qualification pèse donc +10,3 pts, la golden question +1,4 pt.

**Segmentation** : GrabCut optimisé depuis boîtes GT 74,4 % mIoU (VOC 2007) / 71,0 % (VOC 2012) ; avec les points extrêmes 78,1 % / 72,7 % (§6.1). DeepLab-VGG16 sur VOC 2012 : vérité terrain 59,9, segments issus des boîtes 55,8, segments issus des clics 58,4 mIoU (Table 4, §6.3).

→ reportés dans `benchmarks.csv` : aucune ligne. Le schéma (plateforme FPGA, FPS, quantification) ne s'applique pas à un protocole d'annotation ; `benchmarks: none` au front-matter. Les chiffres utiles sont ci-dessus et dans les chunks `1708.02750#014.1`, `#014.2`, `#026.0`.

## Limites et critique

- Les 7 s sont mesurées sur AMT pour VOC (20 classes, objets souvent grands, une instance par classe et par image) ; non testé sur des scènes denses, des objets petits, occultés, tronqués ou des foules : l'annotation « toutes les instances » n'est pas mesurée (§5).
- La référence de 34,5 s est issue d'un autre papier (ILSVRC, [62]) et non remesurée par les auteurs ; elle exclut les rejets (55 s avec). Le facteur 5x dépend donc de ce choix, et le 7 s n'inclut pas de vérification séparée (le contrôle est la golden question, sans rejet a posteriori).
- Qualité mesurée contre PASCAL GT, lui-même bruité (88 % d'accord entre experts) : « aussi bon que GT » signifie « dans le bruit d'accord des experts ». Pas d'accord inter-annotateurs entre travailleurs AMT rapporté (déduit : les mesures sont contre GT uniquement).
- Table 2 et Table 3 : corps reconstruits ou non extraits, chiffres de Table 3 repris du texte. Comparaison avec [54] approximative (sous-ensemble ILSVRC non précisé).
- Détecteurs anciens (Fast R-CNN, AlexNet/VGG16) ; aucun test avec un détecteur de type YOLO.
- Preprint ; code non mentionné.

## Pertinence pour la thèse

Réponse pour CONSTRUIRE/ANNOTER un dataset de détection (axes `annotation`, `datasets`) : la référence « comment annoter des boîtes vite et bien ».
- **Quand l'appliquer** : annotation manuelle de boîtes serrées pour un nouveau dataset YOLO, une instance à la fois, par crowdsourcing ou en interne ; classes aux extrémités bien définies. Les 4 clics se convertissent directement en (xmin, ymin, xmax, ymax) puis en bbox normalisée YOLO (cx, cy, w, h) (déduit, non dit par les auteurs).
- **Recette transférable** : (1) clics sur extrémités plutôt que dessin de rectangle (~5x moins cher) ; (2) consigne courte ; (3) test de qualification de 5 images avec retour automatique, tolérance de 10 px, répétable (le facteur le plus utile : +10 pts mIoU) ; (4) lots monoclasse de 10 images ; (5) une golden question par lot, sans rejet a posteriori ; (6) mesurer la qualité par IoU>0,5 / >0,7 et mIoU contre un jeu de référence, sachant qu'un accord d'experts de ~88 % mIoU est le plafond réaliste.
- **PRÉTRAITER / AUGMENTER** : sans objet direct. En revanche, les 4 points fournissent des contours exploitables pour pseudo-masques (lien avec l'axe `auto-labelling`).
- **Ordre de grandeur de budget** : 14-17 h et ~150-170 $ pour ~5000 images VOC (une instance par classe).
- Laisse ouvert : scènes denses (VisDrone, CrowdHuman), petits objets, OBB, annotation multi-instances, contrôle qualité avec des modèles actuels.

## Gaps identifiés

- Coût et qualité de l'annotation de boîtes pour petits objets / scènes denses / images aériennes : non couverts ici.
- Pas de mesure de l'accord inter-annotateurs entre travailleurs crowdsourcés ni d'effet du bruit résiduel sur un détecteur YOLO moderne.
- Comparaison extreme clicking vs pré-annotation automatique (SAM, pseudo-labels) à chercher ailleurs dans la base (axe `auto-labelling`).

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction grobid). Table 2 : corps reconstruit par PyMuPDF, à vérifier. Table 3 : corps non extrait, chiffres repris du texte (§5.2).
Ce qui suit est déduit et non affirmé par les auteurs : conversion des 4 clics en format YOLO ; gain de +10,3 et +1,4 pts calculé par différence ; absence d'accord inter-annotateurs AMT (non rapporté) ; venue ICCV 2017 (connaissance externe, non vérifiée dans le texte).
