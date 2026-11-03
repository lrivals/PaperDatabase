---
id: 2020-restuccia-modeling-analysis-bus-contention-hardware
fiche: done
date: 2026-11-03
benchmarks: none
---

# Modeling and Analysis of Bus Contention for Hardware Accelerators in FPGA SoCs

Francesco Restuccia, Marco Pagani, Alessandro Biondi, Mauro Marinoni, Giorgio Buttazzo, 2020, LIPIcs, Volume 165, ECRTS 2020 165, 12:1-12:23. https://doi.org/10.4230/LIPICS.ECRTS.2020.12
Type : conférence (ECRTS 2020, relu par les pairs)

## Problème

Les accélérateurs matériels (HA) d'un SoC FPGA sont prévisibles en isolation, mais la contention sur le bus AXI vers la DRAM partagée (interconnects en arbre, arbitrage round-robin) est la principale source d'imprévisibilité de leur temps de réponse (§1). Les auteurs veulent borner le pire cas de cette contention pour des HA derrière une hiérarchie d'interconnects de profondeur arbitraire (Abstract, §1).

## Méthode

- Modèle fin du bus AXI et des interconnects (§3) : tâches matérielles périodiques (N transactions lecture/écriture, burst B, φ transactions en attente), interconnect round-robin de granularité φ_I, délais de propagation et temps de maintien, délais PS/contrôleur mémoire agrégés (d_PS read/write, DDR non modélisé finement, §3.3).
- Analyse de temps de réponse (§4) : borne du temps d'une transaction sans contention (Lemmes 1-2, Éq. avec L niveaux hiérarchiques) ; deux bornes du nombre de transactions interférentes (par arbitrage, Lemmes 3-6 : interférence directe et indirecte ; par périodicité, Lemme 7) combinées par min (Lemme 8) ; Algorithme 1 pour le coût de contention par niveau ; R_z = C_z + N·d_NoCont + d_interf (Éq. 4, §4.5).
- Hypothèses : arbitrage round-robin (Xilinx Interconnect et SmartConnect), traitement en ordre, FIFO jamais saturées, un seul port FPGA-PS (§2, §3). Pas de modèle des pipelines (pire cas où les transactions sont espacées).
- Validation expérimentale (§5) avec IP maison : générateur de trafic « GHW-task » cycle-précis et timer multicanal, ILA pour les traces (§5.1).

## Plateforme et implémentation

- Puces : Zynq-7020 et Zynq UltraScale+ ZCU102 ; un port HP (HP0) du FPGA-PS ; seuls les résultats ZCU102 sont rapportés, la Zynq-7000 étant dite « comparable » (§5).
- Horloges : FPGA 100 MHz ; PS à 1,2 GHz (§5.1). Le §1 cite 650 MHz pour la Zynq-7000.
- Outil : Vivado 2018.2. Ressources FPGA (LUT/DSP/BRAM) : n/r.
- Puissance : n/r (non mesurée).
- Code / bitstream : non publiés (aucun lien dans le texte).

## Résultats

- Profilage de l'AXI SmartConnect (§5.2, chunk 046.0) : d_addr_Int = 12, d_data_Int = 11, d_bresp_Int = 9 cycles ; temps de maintien t_addr = t_data = t_bresp = 1 cycle ; d_PS read = 50 cycles, d_PS write = 40 cycles (estimés sans charge mémoire sur les processeurs, §5.2). Mesures observées sur les deux plateformes.
- Réseau plat, 4 GHW-tasks, 1 requête de burst 16 mots de 32 bits : les temps de réponse maximaux mesurés restent sous la borne (Fig. 4, §5.3, chunk 028.1). Valeurs chiffrées de la Fig. 4 : n/r de façon fiable (voir Limites).
- Réseau hiérarchique, 4 GHW-tasks, 3 interconnects : mesures sous la borne (Fig. 7, §5.3). Trace ILA (Fig. 6, Zynq-7020, chunk 047.0) : τ3 subit 7 requêtes interférentes ; premier mot de donnée à t=274, transaction terminée à t=292 (l'unité de temps de la trace n'est pas précisée dans le texte extrait).
- Chiffres orphelins dans le texte extrait d'une figure sans légende identifiée : écriture 280 (mesuré) / 756 (borne) ; lecture 350 / 866 (cycles d'horloge). Le texte n'indique pas s'il s'agit de la Fig. 4 ou de la Fig. 7 : donnée de confiance faible, à revérifier sur l'image avant tout usage.
- Charge synthétique (§5.4, Fig. 8) : N ∈ {4, 8, 16, 24} tâches, M ∈ {1, 2, 4, 8} interconnects, 50 000 jeux de tâches par densité ρ, φ_i = 6, B = 16, φ_I = 1. Résultat qualitatif : plus d'interconnects permet plus de tâches et peut améliorer le taux d'ordonnançabilité en plaçant près de la racine les tâches à faible marge ; valeurs de la Fig. 8 : n/r.
- Baseline de comparaison : aucune autre analyse (les travaux cités ne traitent qu'un seul interconnect, §6).
→ reportés dans `benchmarks.csv` : aucune ligne (benchmarks: none). Le papier ne rapporte ni fps, ni gops, ni puissance, ni précision, ni ressources ; ses mesures sont des délais de bus en cycles d'horloge sur des IP de test, sans modèle de réseau ni dataset. Les colonnes de `benchmarks.csv` (§7) ne s'y prêtent pas (`latency_ms` serait une conversion non rapportée).

## Limites et critique

- Bornes validées seulement sur des scénarios de pire cas fabriqués (GHW-tasks) et quatre tâches ; pas de cas d'usage avec un vrai accélérateur de réseau de neurones (une étude de cas est annoncée dans l'introduction §1 mais n'apparaît pas dans le texte de §5).
- Pessimisme de la borne non quantifié dans le texte (rapport borne/mesure illisible sans les figures) ; pas de pipelining modélisé (§3.1, §7).
- Un seul port FPGA-PS, round-robin, FIFO supposées non saturées ; le contrôleur DDR est une boîte noire dont d_PS est estimé sans charge CPU (§3.3, §5.2) : hors de ce cadre, la borne n'est pas garantie.
- Dépend de la version du SmartConnect/Vivado 2018.2 ; valeurs de profilage non transposables aux Versal/Kria sans re-profilage (déduit).
- Pas de code publié : reproductibilité faible.

## Pertinence pour la thèse

Base d'analyse temporelle d'un chemin FPGA-DRAM partagé : fournit une borne de pire cas du délai d'un accélérateur (donc d'un détecteur YOLO) soumis à l'interférence d'autres maîtres AXI, composant du délai de réaction de bout en bout (WCET, interférences) du profil. Il laisse ouvert la contention au niveau du contrôleur DDR, la charge CPU, l'application à un DPU/accélérateur CNN réel et l'usage de la borne dans un dossier de certification.

## Gaps identifiés

- Borne de contention AXI appliquée à un accélérateur CNN/YOLO réel (DPU, Kria/Versal), avec comparaison borne contre mesure.
- Modèle du contrôleur DDR et de la charge CPU concurrente (d_PS mesuré à vide seulement).
- Stratégie d'allocation des tâches sur l'arbre d'interconnects (laissée en travaux futurs, §5.4).

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction grobid ok). Les figures 4 à 8 ne sont pas lisibles dans le texte : leurs valeurs ne sont pas reprises, sauf les quatre chiffres orphelins signalés ci-dessus (confiance faible, figure sans légende identifiée, avertissement d'extraction).
Ce qui suit est déduit et non affirmé par les auteurs : la non-transposabilité aux plateformes récentes ; l'absence de code publié (aucun lien dans le texte) ; l'attribution de la Fig. 4 ou 7 aux chiffres orphelins (non faite).
