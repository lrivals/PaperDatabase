---
id: arxiv-2603.27698-ink-detection-surface-topography-herculaneum
fiche: done
date: 2026-11-15
---

# Ink Detection from Surface Topography of the Herculaneum Papyri

Giorgio Angelotti, Federica Nicolardi, Paul Henderson, W. Brent Seales, 2026, Scientific Reports (2026). https://doi.org/10.1038/s41598-026-58467-1 (arXiv 2603.27698)
Type : journal (Scientific Reports, 2026, selon la mention arXiv ; la version lue est celle d'arXiv).

## Problème

L'encre carbonée sur papyrus carbonisé n'offre presque aucun contraste d'absorption en CT. Les auteurs testent l'« hypothèse morphologique » : le dépôt d'encre modifie le micro-relief de surface assez pour distinguer encre et papyrus, indépendamment de la composition (Introduction). Trois questions : la topographie seule suffit-elle à haute résolution latérale ? comment la performance évolue-t-elle quand on dégrade l'échantillonnage ? le signal appris sur certains papyrus se généralise-t-il à un papyrus non vu ?

## Méthode

- Signal exploité : **topographie de surface seule** (cartes de hauteur), sans image de contraste ni texture visible. La rugosité seule (filtrage) ne sépare pas l'encre ; le modèle exploiterait un signal composite : rugosité + déformations de pression liées au dépôt d'encre, dans des motifs de forme que l'analyse de profil classique saisit mal (Discussion, lu des auteurs, formulé comme interprétation). Les cartes brutes sont dominées par l'inclinaison/courbure de la surface et par les fibres (Fig. 2) ; aucune correction de plan ou d'inclinaison (Méthodes).
- Entrées : cartes de hauteur 2D, normalisées [0,1], uint16 ; trous de reconstruction (NaN) comblés par inpainting de Telea (~1,7 % des pixels). Régions d'environ 1,5 mm de côté.
- Labels : masques **manuels** tracés dans GIMP sur photos en fond clair co-recalées (biais possible sur les bords flous, erreurs de recalage).
- Modèle : nnU-Net 2D, hyperparamètres par défaut, perte Dice + entropie croisée, Adam, lr 1e-3, augmentations (flips, rotations, intensité, déformations élastiques), arrêt anticipé.
- Protocole : validation croisée 5-fold sur 14 échantillons (16 lettres) ; modèles séparés par résolution (appariés) ; un modèle 0,34 µm testé sur entrées dégradées (moyenne par blocs n×n, n de 2 à 32, puis suréchantillonnage bilinéaire) ; « voxel isotrope » émulé par binning de z (Δz = Δx) ; leave-one-papyrus-out à 0,34 µm. Tests de Friedman, Page, Wilcoxon-Holm.

## Plateforme et implémentation

- Source des données : **profilométrie optique 3D confocale** (Sensofar S lynx 2), **pas un scan CT** : échantillonnage latéral 0,34 µm, sensibilité verticale 8 nm. Pas d'énergie keV (sans objet). Matériaux : fragments ouverts mécaniquement (scorze) de PHerc. 248 (Philodème, De pietate) et PHerc. 250 (De rhetorica I), et morceau PHerc. 500P2 ; 14 régions / 16 lettres.
- Évaluation : validation croisée par échantillon (régions de mêmes papyrus potentiellement dans l'entraînement) ; seul le leave-one-papyrus-out tient un papyrus entier à l'écart (4-5 échantillons par papyrus).
- Matériel de calcul et temps : n/r.
- Code : n/r (nnU-Net public, mais pas de code du papier). Données, labels, splits et configs : « seront publiés dans un dépôt public à la publication » ; sur demande jusqu'alors (Data Availability). Pas de lien.

## Résultats

- Topographie seule, 0,34 µm, 5-fold : Dice médian 0,890 [0,864 ; 0,905], moyenne 0,881 ± 0,039 (Table 1).
- Résolution (modèles appariés) : 0,817 à 0,68 µm ; 0,754 à 1,02 µm ; 0,586 à 1,36 µm ; ~0,47-0,52 à ≥ 2,04 µm, plateau, 0,467 à 10,88 µm (Table 1). Seules les tailles ≤ 1,02 µm dépassent la référence Dice = 0,70. Friedman χ² = 88,34, p = 1,01e-15 ; Page L = 3848.
- Modèle 0,34 µm sur entrées dégradées : 0,899 à 0,34 µm, 0,881 à 0,68 µm (meilleur que le modèle apparié à 0,68 µm), 0,758 à 1,02 µm, 0,494 à 2,04 µm, 0,029 à 3,40 µm, ~0 au-delà (Table 1) : effondrement net au-delà de ~1-2 µm.
- Z-binning (Δz = Δx) : écart de Dice médian ≤ 0,026 vs hauteur continue (Table 1) ; la quantification verticale n'est pas le goulot.
- Leave-one-papyrus-out : Dice moyen poolé 0,691 ; médiane 0,757 (PHerc. 248), 0,817 (PHerc. 250), 0,475 (PHerc. 500P2) (Table 2). Transfert hétérogène.
- Contrôle d'artefact : le masque des pixels manquants ne recoupe pas l'encre (Dice 0,032) ; manquants 1,65 % dans l'encre vs 1,77 % dans le papyrus (Résultats).
→ reportés dans `benchmarks.csv` : 21 lignes (9 modèles appariés, 9 modèle 0,34 µm sur entrées dégradées, 3 leave-one-papyrus-out ; Dice médian ; z-binning et moyennes non reportés, voir Table 1).

## Limites et critique

- Très petit jeu : 14 échantillons, 3 papyrus (4-5 par papyrus) ; puissance statistique limitée, surtout aux grossiers (les auteurs).
- Pas de volume CT : la dégradation par moyenne de blocs + interpolation ne reproduit pas la PSF/MTF d'un scanner, ni le bruit, les effets de volume partiel, la reconstruction ; les seuils (~1 µm) ne se transposent pas tels quels aux scans 8-9 µm du Vesuvius Challenge (déduit : ces scans sont à un ordre de grandeur au-dessus du seuil trouvé ici, et le papier ne dit pas si le micro-relief survit en CT).
- Surface exposée et non dans un rouleau fermé ; la surface visée en CT est un feuillet interne, non accessible à une mesure de relief libre.
- Labels dérivés de photos (bords flous) ; une seule architecture et un seul régime d'entraînement.
- Validation croisée par échantillon et non par papyrus pour les résultats principaux : le 0,89 n'est pas un score à rouleau tenu à l'écart ; le score tenu à l'écart (0,691 ; 0,475 sur PHerc. 500P2) est nettement plus bas.
- Confusions possibles non écartées : biais de reconstruction de hauteur corrélés à l'optique de surface (les auteurs, travaux futurs) ; fibres et courbure dominent le signal brut.
- Pas de test placebo ni d'incertitude/calibration ; pas de comparaison avec une baseline classique (ex. rugosité seule : mentionnée comme insuffisante, sans chiffre).

## Pertinence pour la thèse

Répond directement à la question « quel signal d'encre » : le papier montre qu'un signal de **topographie de surface** à 0,34 µm discrimine l'encre (Dice ≈ 0,89), qu'il est concentré aux échelles fines et qu'il tombe sous Dice 0,70 au-delà d'environ 1 µm effectif (Table 1). Implication pour la chaîne CT : à 8-9 µm, ce signal morphologique pur ne devrait pas survivre ; il faudrait soit une résolution effective ≲ 1 µm (hors de portée des scans actuels), soit s'appuyer sur d'autres signaux (texture, contraste de phase). Appui pour la question « quelle part du signal d'encre survit à 8-9 µm », mais comme borne indirecte, sans CT. Résultat utile pour la distillation/super-résolution : le modèle entraîné fin dégrade mieux que le modèle entraîné grossier jusqu'à ~1 µm (0,881 vs 0,817 à 0,68 µm), argument pour un enseignant haute résolution. Reste ouvert : transfert au CT réel, rouleau tenu à l'écart.

## Gaps identifiés

- Aucune mesure en volume CT réel (8-9 µm, 2,4 µm, synchrotron) du signal morphologique ; seuil ≈ 1 µm non vérifié sur de vraies PSF.
- Généralisation inter-papyrus faible et instable (0,475 sur PHerc. 500P2) ; pas d'étude des causes (encre, état de conservation).
- Pas de validation placebo, d'incertitude ni de baseline classique sur la topographie.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : backend `pymupdf`, `extraction.ok` à `false`, aucune section détectée : le texte est lisible mais le découpage en sections est absent ; Tables 1 et 2 reconstruites en texte plat (colonnes collées), recoupées avec le texte (valeurs 0,890 / 0,691 / 0,757 / 0,817 / 0,475 concordantes), mais colonne par colonne à vérifier (`confidence` high retenu car recoupé en partie).
Déduit, non affirmé par les auteurs : l'écart avec les scans CT 8-9 µm du Vesuvius Challenge ; l'argument pour un enseignant haute résolution ; l'absence d'évaluation à rouleau tenu à l'écart pour les scores principaux (le protocole décrit est par échantillon).
