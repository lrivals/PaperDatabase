---
id: arxiv-2406.12346-certification-hybrid-architectures-analysing-interference
fiche: done
date: 2026-11-03
benchmarks: none
---

# Towards the Certification of Hybrid Architectures: Analysing Interference on Hardware Accelerators through PML

Benjamin Lesage, Frédéric Boniol, Kevin Delmas, Adrien Gauffriau, Alfonso Mascarenas-Gonzalez, Claire Pagetti, 2024, arXiv preprint. https://arxiv.org/abs/2406.12346 (pas de DOI)
Type : preprint non relu par les pairs

## Problème

Les plateformes hybrides (cœurs généralistes + accélérateurs : GPU, NPU, FPGA SoC) doivent être certifiées avant embarquement avionique. Les objectifs EASA AMC20-152A (matériel électronique aéroporté, COTS) et AMC20-193 (processeurs multi-cœurs) s'y appliquent, mais la méthodologie PHYLOG et son langage PML ont été conçus pour des multi-cœurs. Question posée : PML peut-il modéliser des accélérateurs, et faut-il l'étendre ? (§I, §VI-A)

## Méthode

Papier de position, sans implémentation ni mesure.
- Rappel de PHYLOG (patrons d'argumentation dérivés d'AMC20-193, 8 activités ; §II) et de PML (DSL embarqué dans Scala : composants initiateurs / cibles / transporteurs, transactions ; §III).
- §V : lecture d'AMC20-152A pour les accélérateurs (COTS vs custom, dispositif simple vs complexe) ; 4 activités proposées (évaluer chaque dispositif, maîtriser les cœurs complexes par benchmarks de stress, rester dans les limites du fabricant, qualifier COTS et microcode ; §V-B).
- §VI : taxonomie des accélérateurs selon 3 dimensions : (1) unitaire vs parallèle (nombre d'applications simultanées) ; (2) couplage : 4 catégories (étroitement couplé, passif = cible, semi-actif = initiateur DMA-like, actif = initiateur autonome) avec le gabarit de modèle PML de chacune ; (3) couches applicatives (runtime, pilotes).
- 14 exemples : TI Keystone, Jetson AGX Xavier (GPU Volta), NVDLA (passif, small, large), NXP i.MX 8M Plus (NPU VIP8000), Zynq-7000 (ports PL-PS), CUDA, NEON, OpenVX.
Pas de toolflow.

## Plateforme et implémentation

Aucune implémentation ni plateforme évaluée : les plateformes sont des exemples de modélisation (Xavier, NVDLA, i.MX 8M Plus, Zynq-7000 XC7Z000-série ; la légende de la Fig. 14 écrit « ZYNQ-A7000 », probablement une coquille). Fréquence, ressources, puissance : n/r. Code ou modèles PML publiés : non indiqué dans le texte.

## Résultats

Aucun résultat quantitatif. Résultats qualitatifs :
- Les accélérateurs entrent dans la classe « dispositif complexe » d'AMC20-152A et dans le champ d'AMC20-193 (§VIII).
- PML est jugé assez générique pour modéliser des accélérateurs ; un accélérateur unitaire est modélisé comme initiateur unique, au prix d'une abstraction conservatrice qui doit être garantie par la plateforme (un seul utilisateur du GPU ; Example 7, §VIII).
- Cas d'un FPGA SoC (Example 10, §VI-C) : le modèle dépend de ce qui est configuré dans la PL ; chaque dispositif configuré doit être modélisé selon les catégories, les ports PS-PL (GP, HP, ACP) sont des transporteurs et des canaux d'interférence potentiels (l'ACP peut causer du cache trashing sur le processeur).
- Le NVDLA (soft IP, source ouvert) se prête mieux à l'analyse que les COTS (NPU i.MX 8M Plus, GPU Volta) peu documentés (§VIII, Examples 4-6).
→ reportés dans `benchmarks.csv` : aucune ligne (papier conceptuel, aucune mesure) ; `benchmarks: none`.

## Limites et critique

- Pas de validation : aucun cas d'étude analysé, aucune interférence calculée ni mesurée. Les modèles sont des schémas simplifiés.
- Les abstractions conservatrices (initiateur unique) coûtent en performance, mais ce coût n'est pas chiffré ; le papier le reconnaît sans le mesurer (§VIII).
- Passage à l'échelle non traité : nombre d'initiateurs élevé, incertitude sur l'allocation threads-cœurs (§VIII). Pistes seulement (symétries des SM, Example 8).
- Isolation par SM du GPU Volta reposant sur un support non documenté (Example 8) : non vérifiée.
- Orienté avionique (EASA) ; applicabilité aux normes industrielles (IEC 61508, ISO 13849) de la thèse non discutée. FPGA traité en un seul exemple, sans exemple de DPU / accélérateur dataflow synthétisé.
- Preprint, auteurs rattachés à PHYLOG : auto-positionnement.

## Pertinence pour la thèse

Apport pour l'axe sûreté / certification et le volet « interférences » (WCET, contention) du sujet ARCYS : cadre pour argumenter AMC20-193 sur un SoC FPGA (Zynq : DPU en PL = accélérateur semi-actif ou actif, ports HP/ACP = canaux d'interférence, runtime Vitis AI = dimension 3). Utile comme grille de classification d'un accélérateur de détection, mais sans méthode quantitative. Lien avec les papiers de contention de bus (Restuccia) et de WCET de CNN sur FPGA déjà dans la base (déduit).

## Gaps identifiés

- Modèle d'interférence PML (ou équivalent) d'un DPU / accélérateur dataflow HLS sur Zynq UltraScale+ / Kria : non traité.
- Quantification du coût de performance des abstractions conservatrices (accélérateur unitaire).
- Correspondance AMC20-152A / AMC20-193 avec les normes hors avionique (IEC 61508) pour un détecteur YOLO sur FPGA.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID ok ; la section V n'était pas détectée, son texte est rattaché à la fin de la section IV, lu et traité comme §V ; figures non lues, seules leurs légendes l'ont été).
Déduit et non affirmé par les auteurs : lien DPU / Zynq avec les catégories 3-4 ; pertinence pour la thèse et lien avec les papiers Restuccia ; « ZYNQ-A7000 » probable coquille de Zynq-7000.
