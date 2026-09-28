# Carte des gaps

Zones non couvertes et verrous repérés dans le corpus. Mis à jour par `/paper-gaps` à partir
des fiches `done` et de `benchmarks.csv`. Chaque gap cite les `paper_id` qui l'étayent et
distingue ce qui est lu de ce qui est déduit.

Format d'une entrée :

```
### <intitulé du gap>
- Constat : ce que montre le corpus (paper_id, section source).
- Ce qui manque : la question laissée ouverte.
- Statut : hypothèse (déduite de la bibliographie de départ) | étayé (fiches done).
- Piste : expérience ou lecture pour le confirmer.
```

---

Carte initiale du 28/09/2026 : **aucune fiche `done` propre à cette base**. Les gaps
ci-dessous viennent de l'état de l'art de départ ([docs/etat-de-l-art.md](docs/etat-de-l-art.md)),
rédigé à partir de résumés seuls. Tous ont le statut **hypothèse**, jusqu'au premier `/paper-gaps`.

### Décalage algorithme / matériel
- Constat : les YOLO drone SOTA (tête P2, têtes Transformer, CBAM : TPH-YOLOv5, Drone-YOLO)
  sont évalués sur GPU de bureau ; les implémentations FPGA trouvées restent sur
  YOLOv3/v4-tiny (Calì et al. 2025, Yu & Bouganis 2020).
- Ce qui manque : le portage d'une tête P2 ou d'un bloc d'attention sur FPGA embarqué.
- Statut : hypothèse.
- Piste : fiches SATAY, arxiv-2607.13106 (DPU-aware attention), Calì et al.

### Quantification et petits objets
- Constat : aucune étude trouvée qui mesure l'effet de l'INT8/INT4 sur le mAP_small de VisDrone ;
  chez Calì et al., le rappel chute (38,44 % → 17,16 %) après pruning, à vérifier.
- Ce qui manque : une mesure du mAP_small en fonction de la précision numérique.
- Statut : hypothèse.
- Piste : Drone-YOLO-nano / YOLOv8n-P2 INT8 (Vitis AI, KV260) contre Jetson Orin Nano.

### Haute résolution et mémoire on-chip
- Constat : le tiling de type SAHI et la tête P2 produisent de grandes feature maps.
- Ce qui manque : un travail FPGA sur la pression BRAM qui en résulte.
- Statut : hypothèse.
- Piste : fiches SAHI, SATAY (streaming on-chip).

### Métriques non comparables
- Constat : on trouve à la fois de l'IoU mono-objet (DAC-SDC, SkyNet), du mAP multi-classe
  (VisDrone) et des FPS sans puissance mesurée à la carte.
- Ce qui manque : un protocole commun.
- Statut : hypothèse (partiellement lu : fiche 2021-xu-dac-sdc, copiée de la base FPGA).
- Piste : colonne `power_scope` de benchmarks.csv à remplir systématiquement.

### Métrique système absente
- Constat : les papiers YOLO/FPGA donnent des FPS et des FPS/W, sans effet sur l'autonomie ni
  sur la vitesse de vol sûre ; MAVBench et le roofline F-1 fournissent ce cadre.
- Ce qui manque : traduire les FPS d'un accélérateur en vitesse de vol sûre.
- Statut : hypothèse.
- Piste : accélérateur de Calì et al. passé dans F-1/Skyline (arxiv-2204.10898).

### Fiabilité des accélérateurs YOLO sur FPGA embarqué
- Constat : les erreurs transitoires (mémoire de configuration, BRAM) ne sont traitées dans aucun
  travail YOLO/drone trouvé ; Ahmed & Jenihhin 2022 propose un modèle cross-layer.
- Ce qui manque : l'injection de fautes sur un accélérateur de détection pour drone.
- Statut : hypothèse.
- Piste : lire Ahmed & Jenihhin ; LIRMM (labs.md).

### Pas de comparaison entre gammes de puissance
- Constat : nano (GAP8, mW), FPGA (W) et Jetson (~10 W) ne sont jamais comparés sur la même
  tâche de détection ; sur nano-drone, la détection tourne à environ 1 à 10 Hz.
- Ce qui manque : un banc unifié.
- Statut : hypothèse.
- Piste : fiches PULP-DroNet, Lamberti 2023, BlankSkip, TinyissimoYOLO.

### Apprentissage continu à bord du drone
- Constat : rien trouvé ; cela ne prouve pas que le sujet n'existe pas.
- Statut : hypothèse.
- Piste : `/paper-discover "continual learning UAV onboard"`.

### Contre-drone : évalué sur GPU de bureau
- Constat : presque tous les détecteurs anti-drone (YOLOv4 élagué, F-YOLOv7, YOLO-GCOF, YOLOv9
  amélioré) sont évalués sur GPU de bureau ; un seul travail FPGA-SoC trouvé (Nguyen et al.,
  JRTIP 2024), en accès fermé.
- Ce qui manque : un détecteur anti-drone mesuré sur matériel embarqué (FPS, puissance carte).
- Statut : hypothèse (liste 3 de l'état de l'art de départ).
- Piste : YOLOv8n ou YOLOv3-tiny entraîné sur Det-Fly, INT8 sur KV260, contre Jetson.

### Fusion multi-capteurs contre-drone sur matériel embarqué
- Constat : Svanström et al. (ICPR 2020) montrent que la fusion visible, thermique et
  acoustique réduit les fausses alarmes ; aucune implémentation embarquée trouvée.
- Ce qui manque : un pipeline de fusion sous contrainte de puissance.
- Statut : hypothèse.
- Piste : fiche arxiv-2007.07396.

### Air → air : coût mémoire du mouvement multi-frame
- Constat : en air → air, les méthodes les plus précises exploitent le mouvement sur plusieurs
  frames (Dogfight : I3D sur des cuboïdes de 8 frames ; Guo et al. 2024 ; arxiv-2411.02582). La
  plupart des travaux anti-drone supposent un capteur au sol (sol → air).
- Ce qui manque : une architecture FPGA qui tienne ce tampon temporel en mémoire on-chip.
- Statut : hypothèse.
- Piste : fiches Dogfight (arxiv-2103.17242) et Guo (arxiv-2312.11008) ; dataset Det-Fly.
