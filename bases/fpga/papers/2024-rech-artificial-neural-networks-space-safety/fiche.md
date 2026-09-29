---
id: 2024-rech-artificial-neural-networks-space-safety
fiche: done
date: 2026-09-29
benchmarks: none
---

# Artificial Neural Networks for Space and Safety-Critical Applications: Reliability Issues and Potential Solutions

Paolo Rech, 2024, IEEE Transactions on Nuclear Science 71(4), 377-404. https://doi.org/10.1109/TNS.2024.3349956
Type : article de journal (survey / tutoriel, relu par les pairs)

## Problème

Les réseaux de neurones profonds sont utilisés dans des applications critiques (automobile, aérospatial), mais leur fiabilité face aux fautes transitoires d'origine radiative est difficile à évaluer : logiciel complexe (centaines de couches), matériel parallèle ou accélérateur embarqué COTS dont l'architecture interne est mal documentée, sortie probabiliste (§I). Les composants durcis aux radiations assez puissants pour exécuter des DNN n'existent pas encore (§I). L'article vise à résumer la méthodologie expérimentale (faisceaux, injection de fautes) et les résultats disponibles, puis à en déduire des solutions de durcissement efficaces (§I).

## Méthode

Survey de méthodologie plus qu'étude expérimentale nouvelle (les données citées viennent des travaux de l'auteur et d'autres, Table III dont le corps n'est pas extrait).
- Rappels : DNN/CNN, accélérateurs (GPU, FPGA, EdgeAI/Coral TPU), effets des radiations (SDC, DUE, taxonomie fault/error/failure d'Avizienis) (§II).
- Distinction des erreurs SDC tolérables et critiques (misdetection, faux positif, misclassification) via précision/rappel et un seuil de Jaccard T_J = 0,5 (§II-C).
- Méthodes d'évaluation : essais terrain, faisceaux (neutrons, protons, ions lourds), injection de fautes aux niveaux circuit, RTL, microarchitecture, logiciel, approches hybrides (§III, §V) ; métriques : section efficace, FIT, MTBF, AVF, PVF, MIBF/MEBF/MWBF (§III-C).
- Conseils pratiques de montage de faisceau (hôte, watchdogs logiciel et matériel, journalisation, temps de setup < 10 % du temps d'exécution du DUT) (§IV-A).
- Durcissement : réplication sélective, ABFT, contrôle de plage au max-pooling, cohérence temporelle inter-images, RP-DWC, BIST, réduction du nombre de classes, fault-aware training (§VI).
- Toolflow : sans objet.

## Plateforme et implémentation

Sans objet (pas d'implémentation propre). Plateformes citées : GPU, FPGA (pipeline complet ou réseau systolique, SRAM ou flash), Coral TPU, NeuroShield, VPU Myriad (§II-B, §IV-C). Puissance : n/r. Code : les scripts de banc de test et benchmarks radiation sont publiés dans le dépôt UFRGS CAROL radiation benchmarks (§IV, réf. [121]) ; pas de bitstream.

## Résultats

Résultats rapportés (issus de la littérature, pas de mesure nouvelle de l'auteur) :
- ECC SECDED sur GPU : réduit le taux d'erreur d'un ordre de grandeur mais peu efficace contre les misclassifications des CNN (§II-B, §VI).
- Sur FPGA : une implémentation en pipeline complet est particulièrement sensible aux neutrons ; réduire la précision et simplifier la sigmoïde réduit le taux d'erreur ; un réseau systolique permet des modèles plus grands mais une corruption du circuit fausse toutes les convolutions mappées dessus (§IV-C.1).
- EdgeAI (NeuroShield, TPU) : taux d'erreur plus faible que les GPU, modèle d'erreur plus simple (§IV-C.1). VPU Myriad : pas de latchup jusqu'à un LET effectif de 110 MeV·cm²/mg, section efficace SEFI d'environ 1e-4 cm²/composant (§IV-C.3).
- Injection de fautes : un bit-flip logiciel simple est irréaliste ; l'injection RTL précise d'un petit CNN de type LeNet peut demander des centaines d'années (§V) ; l'injection microarchitecturale prédit le taux de SDC à un ordre de grandeur près sur ARM (§V-B).
- Durcissement : ABFT/smart pooling détecte jusqu'à 85 % des erreurs critiques (§VI-A), cohérence temporelle environ 70 % avec faux positifs (§VI-A), RP-DWC 75 % de détection en moyenne pour moins de 20 % de surcoût (§VI-B), fault-aware training jusqu'à un ordre de grandeur de fautes critiques en moins, surcoût quasi nul (§VI-C). Ces chiffres sont rapportés par l'auteur depuis d'autres travaux (GPU en majorité).
- Repère normatif : ASIL D exige moins de 10 FIT (§III-C ; le texte écrit « ISO2626-2 », probablement ISO 26262, coquille de l'article).
→ reportés dans `benchmarks.csv` : aucune ligne (survey sans mesure propre, `benchmarks: none`).

## Limites et critique

- Le centre de gravité est le GPU et les neutrons ; les données FPGA sont brèves et qualitatives (§IV-C.1). Rien sur les DPU/toolflows modernes (Vitis AI, FINN) ni sur la détection YOLO en configuration FPGA.
- Le corps de la Table III (inventaire des jeux de données) n'est pas extrait : impossible de vérifier quels travaux couvrent les FPGA.
- Les taux de détection des solutions de durcissement sont des chiffres de travaux différents, sur des réseaux, modèles de fautes et plateformes différents : non comparables entre eux (déduit).
- Les solutions de durcissement sont validées sur GPU/ARM ; le transfert vers FPGA (SEU en mémoire de configuration, TMR, scrubbing) n'est pas traité au-delà d'une mention de l'injection de fautes sur SRAM FPGA (§V) et d'une ABFT légère pour FPGA (§VI-A).
- Le survey ne traite pas la certification (normes IEC 61508 ou ISO 13849, argumentaire d'assurance) : il ne parle que de fiabilité matérielle aux radiations et de la seule métrique FIT/ASIL. Il ne traite ni le TID ni le SEL (§II-C). L'aspect probabiliste du DNN est constaté, non traité (§VII).
- Avis de l'auteur : la communauté radiation doit conduire la recherche en fiabilité ML (§VII) ; point de vue à pondérer.

## Pertinence pour la thèse

Référence de fond pour l'axe `safety-certification` (sûreté matérielle des accélérateurs DNN) : vocabulaire (SDC critique vs tolérable, DUE, cross section, FIT, AVF/PVF), critère de criticité pour la détection d'objets (seuil de Jaccard sur les boîtes) transposable à un YOLO de détection de personnes, et catalogue de mitigations à faible surcoût (ABFT, contrôle de plage, cohérence temporelle inter-images, fault-aware training) qui convient à un flux vidéo de surveillance. Il pose aussi que la réplication totale est coûteuse et que l'ECC ne suffit pas. Le contexte spatial est éloigné, mais la démarche (faisceau + injection + analyse applicative) reste valable pour la qualification d'un accélérateur FPGA. Reste ouvert : le cas FPGA (SEU en mémoire de configuration, TMR sélectif, DPU), le lien avec les exigences de certification industrielle (SIL/PL) et le cas YOLO.

## Gaps identifiés

- Données de sensibilité aux radiations et aux SEU pour des accélérateurs YOLO/DPU sur FPGA (sinon surtout GPU).
- Critères de criticité d'erreur adaptés à la détection de personnes (miss d'une personne vs faux positif) reliés aux niveaux SIL/PL.
- Transfert de l'ABFT, de la cohérence temporelle et du fault-aware training vers des réseaux quantifiés sur FPGA, et comparaison au TMR.
- Lien entre métriques radiation (FIT, cross section) et argumentaire de certification industrielle.

## Statut de lecture

papier complet (fulltext.md lu de bout en bout, sections I à VII). Corps de la Table III non extrait (avertissement d'extraction) : non lu. Figures lues via légendes seulement.
Ce qui suit est déduit et non affirmé par les auteurs : la non-comparabilité entre chiffres de durcissement de travaux différents ; les lacunes FPGA, certification et YOLO listées ci-dessus ; la lecture de « ISO2626-2 » comme ISO 26262.
