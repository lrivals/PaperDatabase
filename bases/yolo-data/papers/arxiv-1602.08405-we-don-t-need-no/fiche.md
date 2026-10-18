---
id: arxiv-1602.08405-we-don-t-need-no
fiche: done
date: 2026-10-18
---

# We don't need no bounding-boxes: Training object class detectors using only human verification

Dim P Papadopoulos, Jasper R R Uijlings, Frank Keller, Vittorio Ferrari, 2016, arXiv preprint. https://arxiv.org/abs/1602.08405
Type : preprint non relu par les pairs

## Problème

Dessiner une boîte englobante est lent et coûteux : 42 s par boîte avec contrôle qualité pour ILSVRC sur Mechanical Turk, 26 s sans (§1, §5.1). Les deux stratégies existantes sont limitées : l'apprentissage faiblement supervisé (labels d'image seuls) donne des détecteurs à environ la moitié du mAP de la supervision complète, et l'active learning demande encore de dessiner beaucoup de boîtes, d'où un gain de temps modeste (§1). Les auteurs veulent entraîner un détecteur sans jamais faire dessiner de boîte : l'annotateur ne fait que vérifier des boîtes proposées par l'algorithme.

## Méthode

Entrée : images avec labels de classe au niveau image. Sortie : une boîte par classe par image et un détecteur (§5.1). Boucle en trois étapes (§3, Fig. 1) :
- (A) réentraîner le détecteur, uniquement sur les boîtes vérifiées positives ; fonds échantillonnés parmi les propositions d'IoU dans [0, 0.5) avec elles (§3.2) ;
- (B) relocaliser : le détecteur score les propositions (EdgeBoxes) et la mieux notée devient la détection de l'image (§3.3) ;
- (C) vérification humaine de la détection (§3.1).

Initialisation D0 par MIL faiblement supervisé multi-fold avec score d'objectness ; arrêt quand deux relocalisations successives coïncident, en général sous 10 itérations (§4.2). Détecteur : Fast R-CNN, AlexNet (VGG16 en §5.4), sans régression de boîte pendant les itérations (§4.1).

Protocole de vérification (§3.1, Fig. 2) :
- Oui/Non : l'annotateur répond Oui si IoU avec la vérité (cachée) >= 0,5, sinon Non.
- Variante YPCMM : Yes / Part / Container / Mixed / Missed, diagnostic du type d'erreur.

Le signal sert deux fois (§3.3) :
- une image positivement vérifiée sort de la boucle ;
- une détection négative réduit l'espace de recherche. Option Neg : retirer la seule proposition rejetée. Option ExtNeg : retirer toutes les propositions d'IoU >= 0,5 avec elle. YPCMM : retirer selon le type d'erreur, avec tolérance IoA 0,9.

## Plateforme et implémentation

Sans objet (pas de matériel embarqué). Détecteur Fast R-CNN + EdgeBoxes, AlexNet ou VGG16. Annotateurs : cinq personnes de l'université, interface plein écran, touches "1"/"0" pour Oui/Non (§5.3). Code publié : n/r (non mentionné dans le texte lu).

## Résultats

Banc : PASCAL VOC 2007, trainval réduit à 3550 images (sans les images n'ayant que des instances difficiles et tronquées), test 4952 images, mAP VOC07 ; CorLoc = % d'images où la boîte retournée a IoU >= 0,5 (§5.1).

Temps de vérification mesurés (§5.3) :

| Tâche | Temps moyen par vérification |
|---|---|
| Oui/Non | 1,6 s |
| YPCMM | 2,4 s |
| Oui/Non, cas limite (IoU proche de 0,5) | 2,2 s (Fig. 6b) |
| Dessin d'une boîte (ILSVRC, repris de [50]) | 26 s sans contrôle qualité, 42 s avec (§5.1) |

Ces 26 s et 42 s ne sont pas mesurés par les auteurs sur VOC. Ils les jugent représentatifs (§5.1).

Boucle simulée (§5.2, Fig. 5), CorLoc de départ 43 % (MIL) :

| Usage du signal | CorLoc final | Vérifications par image |
|---|---|---|
| (I) réentraînement seul | 82 % | environ 4 |
| (II) + retrait des Neg | 92 % | 1,6 à 2 pour atteindre 82 % |
| (III) + retrait des ExtNeg | 95 % | 1,6 à 2 pour atteindre 82 % |
| (IV) YPCMM | 96 % | 2,5 en moyenne |

Humains réels, Oui/Non contre YPCMM (§5.3, Fig. 8) :
- Oui/Non : CorLoc 83 %, mAP 45 %, 5,8 h.
- YPCMM : CorLoc 81 %, mAP 45 %, 7,7 h.
- Les auteurs retiennent Oui/Non. YPCMM demande moins de vérifications mais plus de temps total.

Qualité de l'annotateur (§5.3) :
- Erreurs : 14,8 % des jugements Oui sont faux et 8,5 % des jugements Non sont faux. Léger biais d'indulgence par rapport au seuil IoU 0,5.
- Les erreurs se concentrent sur les petits objets : 48 % d'entre elles concernent des objets de moins de 10 % de l'image (Fig. 6c).
- Les annotateurs divergent sur les cas limites (IoU environ 0,5).
- Les erreurs humaines baissent le CorLoc par rapport à la simulation, mais le mAP reste comparable (§5.3).

Comparaisons (§5.3) :

| Méthode | CorLoc | mAP | Temps d'annotation |
|---|---|---|---|
| MIL faiblement supervisé (initialisation) | 43 % | 27 % | 0 |
| Cinbis et al. [9] | 52,0 % | 30,2 % | n/r |
| Bilen et al. [5] | 43,7 % | 27,7 % | n/r |
| Wang et al. [60] | 48,5 % | 31,6 % | n/r |
| Vérification Oui/Non (AlexNet) | 83 % | 45 % | 5,8 h |
| Supervision complète (boîtes dessinées) | n/r | 51 % | 33 h (à 26 s) ou 53 h (à 42 s) |

- Facteur de réduction du temps : 6× à 9× (§5.3).
- À temps égal de 5,8 h, la supervision complète n'atteint que 33 % de mAP (26 s) ou 30 % (42 s) (§5.3).

Table 1 (mAP, Oui/Non contre supervision complète FS ; corps de tableau reconstruit par PyMuPDF, à vérifier) :

| Réseau | Jeu | Oui/Non | FS |
|---|---|---|---|
| AlexNet | réduit | 45 % | 51 % |
| AlexNet | complet (5011) | 50 % | 55 % |
| VGG16 | réduit | 55 % | 61 % |
| VGG16 | complet (5011) | 58 % | 66 % |

- Les valeurs 45/51 (§5.3) et 58/66 (§5.4) recoupent le texte. Les autres valeurs ne reposent que sur le tableau.
- Les auteurs disent atteindre environ 90 % du mAP de la supervision complète (§5.4).

→ reportés dans `benchmarks.csv` : 7 lignes proposées (agent principal à ajouter) : Oui/Non AlexNet réduit, YPCMM AlexNet réduit, Oui/Non AlexNet complet, Oui/Non VGG16 réduit, Oui/Non VGG16 complet, CorLoc Oui/Non, MIL initial.

## Limites et critique

- Un seul jeu (VOC 2007, 20 classes, objets plutôt grands), un seul détecteur ancien (Fast R-CNN, AlexNet/VGG16). Aucun résultat avec un détecteur de type YOLO.
- Une boîte par classe par image : la boucle ne trouve ni les instances multiples ni les objets supplémentaires. Les images sans objet de la classe ne sont pas traitées, car les labels d'image sont supposés connus. Le mAP de test reste calculé avec toutes les instances, mais l'entraînement n'en voit qu'une par image (§5.1).
- Le coût d'une boîte dessinée (26 s / 42 s) vient d'ILSVRC et de [50], pas d'une mesure sur VOC. Le facteur 6×-9× repose donc sur cette hypothèse. Le coût des labels d'image n'est pas compté dans le temps d'annotation (déduit : le texte ne le chiffre pas).
- Temps humain mesuré sur cinq annotateurs de l'université, non sur du crowdsourcing. La qualité des annotateurs non experts n'est pas testée.
- La vérification est à seuil IoU 0,5 (critère PASCAL) : les boîtes retenues sont lâches. Les auteurs notent un biais d'indulgence ; les erreurs sont surtout sur les petits objets (48 % sous 10 % de l'image). Un seuil plus strict (IoU 0,75, exigence du mAP COCO) n'est pas étudié.
- Écart résiduel de 6 à 8 points de mAP avec la supervision complète (Table 1). Les boîtes finales ne sont pas affinées par régression pendant les itérations (§4.1).
- Preprint, code n/r. Légende de la Table 1 brouillée à l'extraction (valeurs "57 %", "55 %", "50 %" dans la légende) : les valeurs du tableau sont à vérifier sur le PDF.

## Pertinence pour la thèse

- ANNOTER : alternative « vérifier plutôt que dessiner ». Une vérification oui/non coûte 1,6 s contre 26 à 42 s pour une boîte dessinée, soit 16 à 26 fois moins par décision. Il faut en moyenne environ 2 à 4 vérifications par image, d'où 5,8 h contre 33 à 53 h pour 3550 images (§5.3).
- AUTO-ÉTIQUETER : c'est un schéma de pré-annotation avec humain dans la boucle. Le détecteur propose une boîte, l'humain valide ou rejette, le modèle se réentraîne sur les boîtes validées. Le pendant moderne est un détecteur ou un modèle fondation proposant des boîtes, avec un contrôle humain de type oui/non.
- Dans quel cas l'appliquer : labels de classe au niveau image disponibles ou peu chers, un objet dominant par image et par classe, et un budget d'annotation serré. À éviter : scènes denses à multi-instances, objets très petits (taux d'erreur de vérification élevé), exigence de boîtes précises (IoU supérieur à 0,5).
- Pour YOLO : l'idée est transposable (les boîtes validées deviennent des labels au format YOLO). Ce n'est pas testé ici : aucun résultat sur un détecteur YOLO, ni sur VisDrone ou COCO.
- Chiffre à retenir : 45 % de mAP contre 51 % en supervision complète (AlexNet), et 58 % contre 66 % (VGG16, jeu complet), avec 5,8 h d'annotation.

## Gaps identifiés

- Vérification oui/non avec instances multiples : aucun protocole ici ; il faudrait savoir quand s'arrêter dans une image.
- Seuil de vérification IoU 0,5 contre mAP strict (0,5:0,95) : effet du seuil sur la précision des labels non étudié.
- Aucune mesure sur un détecteur moderne (YOLO) ni sur des jeux à petits objets (VisDrone). À rapprocher de l'axe auto-labelling (SAM, Grounding DINO + vérification).
- Coût de la vérification en crowdsourcing et fiabilité des non-experts : non mesurés.

## Statut de lecture

papier complet (fulltext.md lu en entier ; backend grobid). Table 1 reconstruite par PyMuPDF : valeurs à vérifier ; les valeurs 45/51 et 58/66 sont aussi dans le texte. Figures 5, 6 et 8 non lisibles : seuls les chiffres du texte sont repris.
Ce qui suit est déduit et non affirmé par les auteurs : le rapport « 16 à 26 fois » (1,6 s contre 26-42 s) ; l'ordre de grandeur « 2 à 4 vérifications par image » rapproché de 5,8 h ; la transposabilité à YOLO ; le fait que le coût des labels d'image n'est pas compté.
