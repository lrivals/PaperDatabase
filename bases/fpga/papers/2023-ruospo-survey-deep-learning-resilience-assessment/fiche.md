---
id: 2023-ruospo-survey-deep-learning-resilience-assessment
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Survey on Deep Learning Resilience Assessment Methodologies

Annachiara Ruospo, Ernesto Sanchez, Lucas Matana Luza, Luigi Dilillo, Marcello Traiola, Alberto Bosio, 2023, Computer (IEEE) 56(2), 57-66. DOI 10.1109/MC.2022.3217841 ; https://doi.org/10.1109/MC.2022.3217841
Type : article de revue (magazine IEEE Computer, format court, relu par les pairs).

## Problème

Les réseaux profonds sont utilisés dans des domaines critiques (avionique, robotique, imagerie médicale, automobile), et leur résilience, c'est-à-dire leur capacité à tolérer des fautes matérielles, dépend de toute la pile matérielle et logicielle. L'évaluer est coûteux ; le papier passe en revue les méthodologies d'évaluation de fiabilité, centrées sur l'injection de fautes (fault injection, FI) (Abstract, introduction). Question d'acceptation soulevée : un classifieur passant de 90 % à 88 % à cause d'une faute est-il acceptable ? Les métriques doivent donc être choisies avec soin (introduction).

## Méthode

Survey (pas d'expérience propre). Cadre : FI = injecter des fautes, exécuter l'inférence, comparer à une référence « golden » (Background). Deux niveaux : application (neurones, poids, canaux ; neurone crash ou byzantin) et système complet (DNN + matériel, avec un élément de calcul qui porte de nombreux neurones). Modèles de fautes : stuck-at et bit-flip, jugés insuffisants pour les technologies submicroniques profondes mais largement utilisés (Background). Classification en quatre familles (Fig. 1, « FI Methodologies ») : simulation logicielle, simulation matérielle (RTL/porte), à base de plateforme (FPGA, GPU, CPU), à base de radiation. Comparaison qualitative selon huit critères (coût, effort de développement, exactitude, contrôlabilité, observabilité, répétabilité, disponibilité précoce, temps de FI) (Table 1).

## Plateforme et implémentation

Sans objet (survey). Aucune mesure propre ; code, bitstream : sans objet.

## Résultats

Le survey ne rapporte pas de résultats propres ; principaux constats (Table 1 et Discussion) :
- Simulation logicielle : coût faible, exactitude faible, contrôlabilité et observabilité hautes ; la plus utilisée car rapide et facile (§ Software-level).
- Simulation matérielle (RTL/porte) : exactitude moyenne à haute, mais temps long ; un petit CNN à sept couches simulé en RTL demande environ 25 min par inférence, et les études matérielles se limitent à de petits réseaux (classifieur à six couches entièrement connectées, CNN à sept couches) (§ Discussion). Les outils commerciaux de FI (Z01X, Xcelium) visent le test de fabrication, mal adaptés aux campagnes fonctionnelles sur DNN (§ Hardware-level).
- À base de plateforme (FPGA, GPU, CPU) : coût moyen à élevé, effort de développement le plus haut, exactitude faible à moyenne, portabilité ; exemples : FireNN, qui exploite la reconfigurabilité du FPGA pour imiter des fautes, TensorRT sur GPU Volta (§ Platform-based).
- Radiation : exactitude la plus élevée (« very high »), mais coût élevé, contrôlabilité faible, répétabilité moyenne à faible car les composants irradiés ne sont pas toujours réutilisables (Table 1 ; § Radiation-based).
- Défis (§ Open challenges) : les campagnes d'injection dans la mémoire de configuration de FPGA SRAM ne se généralisent pas d'un composant à l'autre (résultats variables sur 16 Xilinx Artix-7 et 10 Lattice iCE40, la température influence les résultats) ; modèles de fautes plus riches à étudier ; méthodes hybrides (cross-layer) à développer ; injection statistique nécessaire car l'exhaustif est hors de portée.
→ reportés dans `benchmarks.csv` : aucune ligne (survey, pas de mesure propre ; règle de la procédure). `benchmarks: none`.

## Limites et critique

- Format magazine court (10 pages) : survey plutôt qualitatif, sans revue systématique explicite (critères de sélection non donnés, bien que le texte se dise « systématique ») ; Table 1 en notes qualitatives (low/medium/high), non chiffrées.
- Sélection de travaux surtout issue du groupe des auteurs (Ruospo, Matana Luza, etc.) ; couverture des travaux FPGA (SEU dans la configuration mémoire, TMR) limitée à quelques exemples.
- Aucune discussion des métriques de résilience normalisées (le point soulevé en introduction sur 90 % contre 88 % n'est pas résolu), ni des mesures de mitigation (TMR, ECC, sélection de bits critiques) : c'est un survey de l'évaluation, pas de la protection.
- Rien sur la certification (IEC 61508, ISO 26262) ni sur la mise en dossier des résultats de FI.
- Ne couvre pas explicitement les réseaux quantifiés/binarisés déployés sur FPGA, alors que la quantification est signalée comme influençant la résilience (§ Software-level).

## Pertinence pour la thèse

Axe sûreté/fiabilité. C'est une cartographie utile pour choisir une stratégie de fiabilité d'un accélérateur YOLO sur FPGA : simulation logicielle pour repérer les couches et bits critiques tôt, simulation RTL pour les petits blocs, injection dans le bitstream de la mémoire de configuration pour l'exactitude sur la vraie cible, radiation pour la validation finale. La Table 1 permet d'argumenter une méthodologie hybride. Elle laisse ouverts : la résilience de détecteurs de grande taille (YOLO), les réseaux quantifiés, la traduction des résultats de FI en argument de sûreté certifiable et les métriques d'acceptation. Deux co-auteurs (Matana Luza, Dilillo) sont au LIRMM (Montpellier), et Bosio à l'École Centrale de Lyon (notices auteurs) : piste pour la liste de labos.

## Gaps identifiés

- Évaluation de résilience aux fautes (SEU, FI) d'un détecteur de type YOLO quantifié sur FPGA : le survey ne cite que des classifieurs de petite taille en simulation matérielle.
- Métriques et critères d'acceptation de la dégradation, reliés à des exigences de sûreté (SIL/PL).
- Variabilité entre composants et effet de la température sur l'injection dans la mémoire de configuration FPGA.

## Statut de lecture

Papier complet (fulltext.md lu en entier, extraction GROBID ; Table 1 lue, Fig. 1 non lisible en texte ; références numérotées non détaillées ici). Déduit et non affirmé par les auteurs : l'absence de revue systématique explicite (critères de sélection non donnés dans le texte), l'absence de couverture de la mitigation et de la certification.
