---
id: 2024-aggarwal-chameleon-dual-memory-replay-online
fiche: done
date: 2026-09-29
---

# Chameleon: Dual Memory Replay for Online Continual Learning on Edge Devices

Shivam Aggarwal, Kuluhan Binici, Tulika Mitra, 2024, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 43(6). https://ieeexplore.ieee.org/document/10375748/ (DOI n/r)
Type : article de journal. Code annoncé : https://github.com/ecolab-nus/Chameleon (Abstract).

## Problème

Un réseau déployé en périphérie doit apprendre en continu, en une passe, d'un flux non i.i.d. (domain-incremental, préférences de l'utilisateur) sans oublier (catastrophic forgetting). Les méthodes par replay (ER, DER, Latent Replay) exigent de gros tampons ; l'EdgeTPU n'a que 8 Mo de SRAM et les accès DRAM coûtent ~120x plus d'énergie que l'on-chip (§I, chiffres cités par les auteurs). Ils visent une précision élevée avec quelques centaines de Ko en mémoire on-chip.

## Méthode

- Double tampon de replay de latent activations (couche 21 sur 27 de MobileNetV1, §V-A) : short-term (ST, on-chip, 10 échantillons, mis à jour à chaque batch, échantillonnage par affinité utilisateur + incertitude via les logits, Eq. 2-4) et long-term (LT, off-chip, mis à jour tous les 10 batchs, échantillonnage par prototypes de classe et divergence KL, Eq. 5-6, classes équilibrées) (§III).
- Entraînement : partie basse gelée, une seule étape forward/backward par échantillon, apprentissage de la partie haute g_phi (§III-B).
- Chameleon-Accel (§IV) : accélérateur FPGA (FP, BP, WU), et modèle analytique du coût calcul/transfert/BRAM (Eq. 7-21) pour choisir la couche latente et la taille des tampons ; portage également simulé sur un template EdgeTPU (uSystolic-Sim, PE 64x64, 8 Mo, 400 MHz, INT8 partie fixe, BFP16 pour les dernières couches) et exécuté sur Jetson Nano (PyTorch, batch 8).
- Évaluation : CORe50 et OpenLORIS-Object, Domain-IL, trois schémas de préférence utilisateur ; baselines EWC++, LwF, SLDA, GSS, ER, DER, Latent Replay (§V-A).

## Plateforme et implémentation

- FPGA : Zynq UltraScale+ MPSoC ZCU102, Vitis HLS / Vivado 2021.2 (C++), 150 MHz, FP16 (§IV-A). Table I des ressources (MobileNetV1, couche 21) citée mais son corps n'est pas dans le texte extrait : LUT/DSP/BRAM `n/r`.
- Les couches sont exécutées séquentiellement, un seul layer à la fois ; ping-pong IFM/OFM ; hôte CPU pour les transferts (§IV-A).
- Puissance : seule l'énergie par image est donnée (Table VI) ; la méthode de mesure et la portée (puce/carte) ne sont pas décrites dans le texte lu : `power_w` `n/r`.
- Code : GitHub ecolab-nus/Chameleon annoncé (Abstract) ; bitstream non mentionné.

## Résultats

- Précision, CORe50 (Table VI/II) : Chameleon-Accel 79.48 ± 0.99 % Acc_all avec Ms=0.3 Mo + Ml=3.2 Mo ; Latent Replay 79.07 % avec 48 Mo ; SLDA 77.20 % avec 1.2 Mo ; JOINT (borne haute) 81.48 % (Table II). Les lignes Chameleon de la Table II sont vides à l'extraction.
- À budget mémoire faible, Chameleon dépasse Latent Replay de ~7-8 % (texte §V-B ; la valeur exacte du tableau manque).
- Schéma 3, CORe50 (Table III) : Acc_all 73.79 %, Acc_pref 91.48 % (vs Latent Replay 72.47 / 86.84, SLDA 73.66 / 84.58).
- Ablation (Table V) : LT seul 69.64 / 87.16 ; ST seul 66.11 / 90.93 ; les deux 73.79 / 91.48.
- Coût matériel (Table VI, par image) : ZCU102 Chameleon-Accel 413 ms / 1.22 J contre Latent Replay 2788 ms / 8.62 J (6.75x latence, 7x énergie, Fig. 15 / §V-D). Jetson Nano : Chameleon 33 ms / 0.31 J, Latent Replay 115 ms / 1.14 J, SLDA 69 ms / 0.68 J. EdgeTPU simulé : Chameleon 47 ms, SLDA 554 ms (11.7x).
- Le GPU est plus rapide que le FPGA (batch, FP efficace), les auteurs le disent (§V-D).
→ reportés dans `benchmarks.csv` (via `bench_rows.csv`) : 4 lignes (ZCU102 Chameleon-Accel et Latent Replay ; Jetson Nano Chameleon-Accel et Latent Replay).

## Limites et critique

- Latence FPGA de 413 ms par image : très loin du temps réel vidéo ; FP16, exécution couche par couche, sans optimisation avancée (aveu §V-D). Le FPGA est ici un support d'analyse (« exploration »), non une solution compétitive ; le GPU Jetson Nano est 12x plus rapide (Table VI, calcul déduit).
- EdgeTPU : simulateur (uSystolic-Sim), pas de mesure réelle ; énergie EdgeTPU non donnée dans le tableau lu.
- Mesure d'énergie FPGA/Jetson non décrite (portée puce/carte inconnue) ; batch 1 sur FPGA contre batch 8 sur Jetson : comparaison non à iso-conditions.
- Baselines relancées par les auteurs, avec des tampons et couches latentes choisis par eux ; Table II incomplète à l'extraction (ligne Chameleon vide), Table I absente.
- Classification d'objets (CORe50, 50 classes ; OpenLORIS) : pas de détection ni de YOLO. Domain-IL avec noms de classes connus, pas de nouvelles classes ; aucune garantie de sûreté ni évaluation de l'oubli en situation de danger.
- Modèle analytique validé qualitativement (Fig. 15 : transfert proche, calcul divergent marginalement), pas d'erreur chiffrée.

## Pertinence pour la thèse

Sur l'axe apprentissage continu embarqué : montre un replay de latent activations exploitant la hiérarchie mémoire d'un FPGA, avec un modèle analytique de coût réutilisable pour dimensionner un replay sur SoC FPGA. Pour la thèse (IA sécuritaire certifiable), c'est surtout un contre-exemple : un modèle qui change en ligne pose des problèmes de certification (déterminisme, traçabilité, revalidation) que l'article n'aborde pas (inférence de ma part). Le mécanisme pourrait servir à adapter la détection de personnes à un site donné, mais sur la couche haute seulement.

## Gaps identifiés

- Apprentissage continu sur FPGA pour de la détection d'objets (YOLO), pas seulement la classification.
- Réalisation FPGA à faible latence (< quelques dizaines de ms) et quantification INT8 pour l'entraînement.
- Continual learning compatible avec la certification (gel, revalidation, bornes sur l'oubli) : non traité.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Manques d'extraction : Table I (ressources FPGA) absente, ligne Chameleon de la Table II vide, énergie EdgeTPU absente du tableau VI extrait. Table VI à confiance moyenne (extraite ligne à ligne, cohérente avec le texte : 6.75x, 7x, 11.7x, 2.1x, 3.5x).
Déduit et non affirmé par les auteurs : le rapport 12x Jetson/FPGA, l'inadéquation au temps réel vidéo, la lecture certification.
