---
id: arxiv-2411.01118-variational-autoencoders-source-data-reduction
fiche: done
date: 2026-09-29
---

# Variational Autoencoders for At-Source Data Reduction and Anomaly Detection in High Energy Particle Detectors

Alexander Yue, Haoyi Jia, Julia Gonski, 2025, Machine Learning: Science and Technology 6, 035017. DOI 10.1088/2632-2153/adf0c0 ; https://arxiv.org/abs/2411.01118
Type : article de journal (version arXiv lue).

## Problème

Dans les détecteurs de physique des hautes énergies, la lecture en amont (front-end) doit réduire un débit énorme sous des contraintes de latence de 25 ns (croisement de faisceaux à 40 MHz), de ressources et de radiations (§1, §2). Les auteurs veulent qu'un même VAE fasse la compression à la source et la détection d'anomalies (défauts de capteur), sans traitement supplémentaire.

## Méthode

- Jeu simulé « smart pixel » : plus de 500 000 traces de pions, matrice 21 x 13 pixels, 8 tranches de temps (§2). Le VAE reçoit 53 des 105 entrées (13 pixels x 4 tranches + y0) et reconstruit les 105 (§3).
- Architecture : encodeur (couche cachée 24, latent 8), décodeur 24-48-64 ; quantification à 8 bits en QAT, élagage à 0,4 de sparsité (§3). Seul l'encodeur est embarqué ; score d'anomalie = KLD « clipée » (somme des moyennes latentes), sans échantillonnage (§2).
- Deux scénarios d'entrée : 4 bits (basse précision) et 10 bits (haute précision) (§2). Synthèse hls4ml (reuse factor 1, io_parallel) pour estimer latence et ressources (§3).
- Comparaison à un classifieur embarqué haut/bas pT (2 couches, 10 bits) qui filtre à la source (§3.2). Anomalies synthétiques : pixel mort, pixel bruyant, ligne morte (§4).

## Plateforme et implémentation

- Cible : n/r. La synthèse hls4ml chiffre des LUT, DSP et FF « d'un FPGA » ; la cible visée est un ASIC ou un FPGA embarqué (eFPGA) résistant aux radiations (§1). Aucun FPGA précis, aucune fréquence, aucune puissance (« à évaluer », Conclusion).
- Encodeur : < 25 ns, ≈ 30 000 LUT et < 700 DSP dans les deux scénarios (§3) ; valeurs détaillées Table 1.
- Code/bitstream : non mentionnés.

## Résultats

- Reconstruction : erreur moyenne sur la charge totale 15,3 % (10 bits) et 8,5 % (4 bits) (§3.1).
- Table 1 (VAE embarqué + classifieur hors puce contre classifieur embarqué) : latence 15 ns contre 25 ns (10 bits) et 15 contre 20 ns (4 bits) ; rejet du fond à SE = 98 % : 25 % contre 18 % (10 bits), 10 % contre 7 % (4 bits) ; taille transmise 7,6 % contre 82 % (10 bits), 15,4 % contre 93 % (4 bits). Assignation des colonnes haute/basse précision déduite (l'en-tête extrait est tronqué) : cohérente avec les 15,4 % et 21 %/10 % du texte (§3.2).
- Anomalies, SE pour 90 % de rejet du fond (Table 2, reconstruit par PyMuPDF, à vérifier) : pixel mort 10 %, ligne morte 12,9 %, pixel bruyant 58,5 % (4 bits) ; 10,8 %, 17,0 %, 22,7 % (10 bits). Avec 1 % des traces les plus anormales transmises brutes, taille 16,4 % (Fig. 5).
→ reportés dans `benchmarks.csv` : 4 lignes (VAE et classifieur, 10 et 4 bits), fournies dans `bench_rows.csv` ; `latency_ms` = latence de l'encodeur seul (15 ns = 0,000015 ms). Métrique : rejet du fond à SE = 98 %.

## Limites et critique

- Données simulées uniquement, anomalies synthétiques simples ; aucun résultat matériel réel, ni puissance, ni FPGA identifié : estimation de synthèse.
- Détection d'anomalie faible pour pixel mort (10 % de SE à 90 % de rejet, quasiment le hasard, Table 2) ; les auteurs notent qu'elle est anticorrélée à la qualité de reconstruction (§4).
- Compression avec perte : erreur moyenne de 8,5 à 15,3 % sur la charge ; effet sur l'analyse physique jugé via une seule tâche de classification.
- Comparaison à un seul classifieur embarqué ; pas de compression classique (aveu en Conclusion).
- Domaine très éloigné de l'imagerie : le VAE traite 105 valeurs, pas une image.

## Pertinence pour la thèse

Exemple d'autoencodeur à faible latence compilé par hls4ml (axe `autoencoder-fpga`, hors imagerie) : compression et score d'anomalie issu de l'espace latent, principe repris en surveillance à l'exécution (moniteur OOD embarqué). Illustre la contrainte de latence déterministe stricte et la prise en compte des radiations, mais sans mesure de robustesse. Ne traite pas de personnes, d'YOLO ni de certification.

## Gaps identifiés

- Autoencodeurs/VAE sur FPGA en physique des particules surtout ; pas de transfert vers l'image (gap déjà identifié).
- Aucune mesure de puissance ni de tolérance aux radiations du VAE malgré la motivation.
- KLD clipée comme score d'anomalie : à comparer aux moniteurs OOD classiques sur des cas de sûreté.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Table 1 : en-tête de scénario tronqué à l'extraction ; Table 2 reconstruit par PyMuPDF (chiffres recoupés avec la légende de la Fig. 5). Fig. 2 à 5 non disponibles en dehors des légendes. Déduit et non affirmé par les auteurs : affectation haute/basse précision des colonnes de la Table 1 ; « cible FPGA » (la synthèse hls4ml sert de proxy pour eFPGA/ASIC).
