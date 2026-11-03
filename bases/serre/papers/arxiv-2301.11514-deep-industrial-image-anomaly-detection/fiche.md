---
id: arxiv-2301.11514-deep-industrial-image-anomaly-detection
fiche: done
date: 2026-11-03
benchmarks: none
---

# Deep Industrial Image Anomaly Detection: A Survey

Jiaqi Liu, Guoyang Xie, Jinbao Wang, Shangnian Li, Chengjie Wang, Feng Zheng, Yaochu Jin, 2023, Machine Intelligence Research vol. 21, no. 1, pp. 104-135, 2024. https://doi.org/10.1007/s11633-023-1459-z (arXiv 2301.11514)
Type : survey publié en revue (Machine Intelligence Research, selon le `journal_ref` arXiv) ; la version lue est le texte arXiv, pas la version éditeur.

## Problème

Les auteurs posent que l'inspection industrielle manuelle souffre de fatigue (faux positifs), de coût et de problèmes de santé (§1), et que la détection d'anomalies d'image (IAD) par apprentissage profond n'est pas encore adaptée à l'usine. Les surveys précédents sont jugés limités : moins de jeux de données (20 ici contre 9 et 7), métriques image seulement, peu de profondeur sur le deep learning (Table 1, §1). Ils listent des verrous : jeux de données issus de labos et non de lignes réelles, absence de jeu multi-domaines, absence de métrique unifiée image/pixel, et pertes mal conçues pour exploiter à la fois quelques anomalies étiquetées et les données non étiquetées (§1).

## Méthode

Revue de littérature (pas de méthode nouvelle), organisée par architecture et niveau de supervision.
- Non supervisé (§2), « feature embedding » : teacher-student (MKD, STPM, RD4AD, AST…), classification à une classe (Patch SVDD, CutPaste, MemSeg…), carte de distribution (normalizing flows : DifferNet, CS-Flow, CFlow-AD, FastFlow, AltUB), banque de mémoire (SPADE, PaDiM, PatchCore, CFA, FAPM, N-pad).
- Non supervisé, reconstruction : autoencodeurs et VAE (RIAD, DRAEM, DSR, NSA, SSPCAB), GAN, transformers (ADTR, InTra, UniAD), diffusion (AnoDDPM).
- Supervisé / semi-supervisé (§3), puis « réglage industriel » (§4) : few-shot et zero-shot (RegAD, WinCLIP, MAEDAY), apprentissage avec bruit, 3D, synthèse d'anomalies.
- Datasets (Table 7, 21 jeux listés), métriques (Table 8) et comparaison des performances sur MVTec AD (Tables 9-10, §6). Pas de toolflow.

## Plateforme et implémentation

Sans objet : aucune plateforme matérielle, ni latence, ni puissance mesurée. Code : les auteurs renvoient à une liste de ressources (https://github.com/M-3LAB/awesome-industrial-anomaly-detection, Abstract) ; pas de code d'expérience propre, sauf des valeurs « reproduites » pour le pixel AU-PR (Table 10, marquées *, source [184]).

## Résultats

Tous les chiffres sont repris des articles originaux (légende Table 9 : « All results are reported from the original papers »). Ordres de grandeur lus dans les tableaux (à vérifier, voir Statut de lecture) :
- Image AUROC moyen sur MVTec AD : PatchCore 0.992, CFA 0.993, N-pad 0.994, FastFlow 0.994, MemSeg 0.994, AST 0.992 (Table 9). Pixel AUROC : N-pad 0.988, MemSeg 0.988, FastFlow+AltUB 0.988 (Table 10).
- Pixel AU-PR (reproduit par les auteurs) : DREAM+SSMCTB 0.705, DSR 0.702, DREAM 0.684 contre PatchCore 0.561 (Table 10, partie AU-PR ; lignes à valeurs PatchCore/SPADE/RD4AD fusionnées par l'extraction, donc fragiles).
- Constats des auteurs (§6) : l'ensemblisme améliore fortement l'état de l'art ; un module de segmentation (U-Net de MemSeg, DRAEM) aide classification et segmentation ; l'AU-PR est plus informatif que l'AU-ROC pour la segmentation ; les méthodes par reconstruction sont les plus adaptées à la segmentation ; l'écart few-shot / classique se réduit.
→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey (règle de la skill) : les chiffres sont ceux de travaux cités, sans protocole commun ni mesure de matériel. `benchmarks: none`.

## Limites et critique

- Agrégation de chiffres rapportés par des papiers différents (« reported from the original papers ») : protocoles, backbones, résolutions et seeds non harmonisés ; aucune latence, mémoire ou puissance. Les auteurs le reconnaissent en §7 (vitesse d'inférence et taille de modèle ignorées).
- Saturation de MVTec AD : les moyennes image AUROC sont à 0.99 pour de nombreuses méthodes (Table 9), peu discriminant ; eux-mêmes notent que les écarts réels sont sur le pixel AU-PR (§6). Déduit : le classement du haut de tableau relève du bruit.
- Les jeux de données sont surtout synthétiques ou de laboratoire (§1, §5) : validité externe limitée ; l'affirmation « plus de 97 % de précision » (§1) ne vaut que sur ces benchmarks.
- Le survey reconnaît que les méthodes de bruit n'ont pas été validées sur de vrais jeux industriels (§4.2).
- Aucun jeu de plantes ni de feuilles n'est traité ; la transférabilité aux feuilles est une déduction de cette fiche, non une affirmation des auteurs.
- Extraction : Table 6 reconstruite par PyMuPDF ; Tables 2, 4, 8 sans corps ; Tables 9-10 partiellement lisibles, lignes parfois fusionnées.

## Pertinence pour la thèse

Pertinence pour SerreIA (axes `surveys` et `anomaly`) : carte du domaine pour la question « la détection d'anomalies non supervisée (PatchCore) fonctionne-t-elle sur des feuilles ? » (profile.md). Apports : taxonomie des familles (mémoire / flows / teacher-student / reconstruction), constat que les banques de mémoire (PatchCore) sont les plus performantes en image AUROC (§2.1.4 : « currently the most effective »), alternatives à étudier (reconstruction pour la segmentation, few-shot et zero-shot WinCLIP/RegAD pour peu d'images saines, §4.1), et le point sur les métriques (AU-PR pixel). Ouvert : aucun résultat sur feuilles, domaine de fond non maîtrisé, coût edge (RPi/Hailo) non mesuré ; appel explicite des auteurs à des modèles légers (§7), mais sans chiffres.

## Gaps identifiés

- Aucune évaluation d'IAD sur images de plantes ou de feuilles de serre (hors périmètre du survey) : à tester avec PatchCore sur PlantVillage / PlantDoc.
- Aucune mesure de latence, mémoire ou puissance pour l'IAD sur edge (RPi 5, Hailo-8L) ; les auteurs le signalent comme direction future (§7).
- Few-shot / zero-shot IAD (RegAD, WinCLIP, MAEDAY) : pas de comparaison sur un fond de serre variable.
- Seuillage et calibration des scores d'anomalie : non traités.

## Statut de lecture

Papier complet : `fulltext.md` lu en entier (grobid). Avertissements d'extraction : Table 6 reconstruite par PyMuPDF (à vérifier) ; Tables 2, 4 et 8 sans corps extrait (leur contenu n'est pas lu, seul le texte de §2 résume les méthodes) ; Tables 9-10 : colonnes par classe parfois décalées ou fusionnées, seules les moyennes citées ci-dessus sont utilisées.
Déduit et non affirmé par les auteurs : saturation de MVTec AD, transférabilité aux feuilles, absence de comparabilité des chiffres entre papiers.
