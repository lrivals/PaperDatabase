---
id: arxiv-2408.00331-decider-leveraging-foundation-model-priors
fiche: done
date: 2026-11-03
benchmarks: none
---

# DECIDER: Leveraging Foundation Model Priors for Improved Model Failure Detection and Explanation

Rakshith Subramanyam, Kowshik Thopalli, Vivek Narayanaswamy, Jayaraman J Thiagarajan, 2024, arXiv preprint (2408.00331). https://arxiv.org/abs/2408.00331
Type : preprint non relu par les pairs. OpenAlex signale une publication à ECCV 2024 (LNCS, DOI 10.1007/978-3-031-72986-7_27) ; le texte de `fulltext.md` ne le confirme pas (aucune mention d'ECCV), donc venue, DOI et type restent inchangés.

## Problème

Détecter à l'avance qu'un classifieur d'images déployé va se tromper, pour pouvoir corriger ou déférer à un humain (Abstract, §1). Les auteurs ciblent les échecs dus à la violation des hypothèses de distribution : décalages d'entrée (corruptions, domaines), corrélations spurieuses, déséquilibre de classes (§3, Fig. 1). Les scores classiques (MSP, entropie, énergie) et les ensembles (GDE) s'appuient sur les mêmes caractéristiques visuelles, donc sur les mêmes biais que le classifieur (§4.1). Ils veulent aussi expliquer l'échec en termes d'attributs lisibles (Abstract, §4.6).

## Méthode

- Un LLM (GPT-3) liste offline K attributs visuels par classe (« List visually descriptive attributes of <CLASS> », §4.3 ; nombre d'attributs par jeu de données en annexe : 25 à 100).
- Le « Prior Induced Model » (PIM) φ a la même architecture que le classifieur F (ResNet-18, ResNet-50 pour CelebA) mais prend en entrée les features de la couche 1 de F et projette dans l'espace latent de CLIP (ViT-B/32) ; ses logits sont l'agrégation (moyenne ou max par classe) des cosinus entre l'image et les embeddings textuels des attributs (§4.2, §4.4, §5.1).
- Entraînement de φ : entropie croisée + CutMix + AugMix, avec surpondération des instances où F et φ divergent (§4.4).
- Score d'échec : entropie croisée entre p(F) et q(φ), PIM en référence (§4.5). Seuil τ calé pour que la part de succès prédits approche la précision de validation (§3).
- Explication : poids appris par attribut qui minimisent la KL entre φ pondéré et F ; les attributs « éteints » indiquent ceux que F n'utilise pas (§4.6, §6, Fig. 5).
- Baselines : MSP, entropie, énergie, GDE (5 graines) (§5.2). Métriques : rappel d'échec (FR), rappel de succès (SR), MCC (§5.3).

## Plateforme et implémentation

Aucune plateforme matérielle : pas de FPGA, Jetson ni MCU ; GPU, latence, puissance et précision numérique `n/r`. Le PIM exige à l'inférence la passe de F plus celle de φ ; coût de calcul non mesuré. Code publié : https://github.com/kowshikthopalli/DECIDER/ (Abstract).

## Résultats

Classification d'images uniquement (pas de détection d'objets). Toutes les valeurs ci-dessous viennent du texte ou des tables d'annexe.

- CIFAR100 propre : MCC 0,5292 (max), contre 0,514 pour la meilleure baseline ; FR 0,7933, SR 0,7474 (§5.4). CIFAR100-C (sévérité 4) : MCC 0,4015 contre 0,3766 (entropie) ; FR 0,8448, SR 0,5506 (§5.4).
- CelebA (moyenne) : MCC 0,4928, FR 0,5443, SR 0,9701 (§5.4). Cats vs Dogs (déséquilibré, max) : MCC 0,5532 contre 0,3428 (énergie), SR > 0,94 (§5.4). Waterbirds : MCC 0,4598 (§5.4, début du passage tronqué dans l'extraction).
- PACS, DomainNet, ImageNet-Sketch : seuls des diagrammes (Fig. 4) ; valeurs de PACS en annexe (Tables 9, 10). Elles montrent un gain net quand F et PIM sont calés sur Photo (ex. Photo : MCC 0,7082 contre 0,4965 pour l'entropie, Table 9), mais un calage sur Sketch donne SR très bas (0,12 à 0,18) sur Art Painting et Photo pour des FR de 0,92 à 0,98 (Table 10) : détecteur quasi tout-rejet, MCC 0,12 à 0,21.
- Robustesse aux attributs (Waterbirds, Table 1) : MCC 0,45 (DECIDER), 0,34 (attributs hors sujet), 0,33 (attributs retirés), 0,28 (entropie).
- Choix de couche : les couches 1 et 2 de ResNet-18 donnent les meilleurs MCC ; les couches profondes dégradent (§7, Fig. 6b). ViT-B/16 sur Waterbirds : MCC 0,4235 (couche 1, max) contre 0,2970 (couche 9) et 0,1656 (énergie) (Table 6).
- CLIP zéro-shot à la place du PIM : mauvaise détection (§7, Table 3 en annexe, non reproduite dans `fulltext.md`).
→ reportés dans `benchmarks.csv` : aucune ligne (voir Limites).

## Limites et critique

- Aucune ligne de benchmark : le papier ne rapporte ni plateforme, ni FPS, ni puissance ; ses métriques (FR, SR, MCC) sont des qualités de détecteur d'échec, sans équivalent dans le schéma de `benchmarks.csv`.
- Classification seulement, petites images et ResNet-18/50 ; pas de détection d'objets, donc pas de notion de faux négatif critique (objet manqué), qui est l'enjeu du draft ARCYS.
- Surcoût à l'inférence : un second réseau (PIM) plus la similarité à K×C embeddings textuels ; non chiffré. Peu compatible tel quel avec un budget FPGA ; KGFP le reproche à DECIDER (KGFP, §2 ; sa phrase d'ouverture décrit pourtant DECIDER comme « a separate classifier », ce qui simplifie le PIM guidé par CLIP).
- Dépend d'un LLM propriétaire (GPT-3) et de CLIP pour fabriquer les attributs ; la qualité du moniteur dépend d'attributs non audités, ce qui pose un problème d'assurance (§7 ne teste que 5 attributs ajoutés ou retirés, sur un seul jeu).
- Le seuil est calé sur une précision de validation supposée valide sur la cible ; sous fort décalage (calage sur Sketch, Table 10) le détecteur devient quasi tout-rejet. Aucun intervalle de confiance, graines uniques pour les MCC.
- Comparaisons : baselines limitées (MSP, entropie, énergie, GDE), sans méthodes plus récentes ou apprises (confidence learning, ConfidNet) ; les chiffres de PACS, DomainNet et ImageNet-Sketch ne sont lisibles qu'en figure.
- Preprint non relu par les pairs dans cette version (la publication ECCV n'est pas confirmée par le texte).

## Pertinence pour la thèse

Axe `failure-prediction`. DECIDER est un représentant de la prédiction d'échec par désaccord entre le modèle et une version « débiaisée » guidée par un modèle de fondation, avec explication en attributs. KGFP (arxiv-2603.25499) le cite comme le plus proche voisin : DECIDER exige la similarité avec des embeddings textuels d'attributs par classe à l'inférence, alors que KGFP n'utilise que l'alignement angulaire avec des features visuelles génériques (KGFP, §2). Pour le cas YOLO en zone dangereuse, il montre l'idée mais ne traite ni détection, ni faux négatifs sur personnes, ni contrainte temps réel ou FPGA ; sert de point de comparaison (méthode, métriques FR/SR/MCC) et de contre-exemple de coût.

## Gaps identifiés

- Prédiction d'échec par désaccord avec un second modèle (PIM, ensembles) dont le coût matériel n'est jamais mesuré, aucune implémentation FPGA.
- Prédiction d'échec évaluée en classification, pas pour la détection d'objets (faux négatif critique).
- Audit et assurance des attributs fournis par un LLM, dans un cadre certifiable.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction GROBID : les images de figures sont des chaînes illisibles, ignorées ; §2 et §4 non détectées par l'extraction mais leur texte est présent ; tableaux 3 à 5, 7 et 8 absents du texte). Les valeurs de PACS, DomainNet, ImageNet-Sketch en Fig. 3-4 ne sont pas lisibles.
Ce qui suit est déduit et non affirmé par les auteurs : le surcoût d'inférence (seule la structure à deux réseaux est décrite) ; la pertinence pour YOLO, le caractère tout-rejet du détecteur calé sur Sketch (déduit de FR/SR de Table 10) ; l'absence de comparaison à des méthodes récentes.
