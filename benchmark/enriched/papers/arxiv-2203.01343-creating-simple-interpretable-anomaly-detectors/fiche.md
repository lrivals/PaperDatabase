---
id: arxiv-2203.01343-creating-simple-interpretable-anomaly-detectors
fiche: done
date:
---

# Creating Simple, Interpretable Anomaly Detectors for New Physics in Jet Substructure

Layne Bradshaw, Spencer Chang, Bryan Ostdiek, 2022, arXiv preprint. https://doi.org/10.1103/physrevd.106.035014
Type : preprint non relu par les pairs

## Problème

Quel verrou le papier attaque-t-il, tel que les auteurs le posent.

## Méthode

Architecture, quantification, stratégie de mapping sur le FPGA, post-traitement (NMS…).
Toolflow employé.

## Plateforme et implémentation

Puce exacte, fréquence, ressources consommées, mémoire. Code ou bitstream publiés ? Où ?

## Résultats

Les chiffres, avec la section ou le tableau source. Baseline de comparaison.
→ reportés dans `benchmarks.csv` : <lignes ajoutées>

## Limites et critique

Comparaisons biaisées, métriques non comparables d'un papier à l'autre, conditions de mesure
non précisées, absence de reproductibilité. Ce que le papier ne mesure pas.

## Pertinence pour la thèse

Ce que ce travail apporte à l'axe visé, et ce qu'il laisse ouvert.

## Gaps identifiés

Points à reporter dans `gaps.md`.

## Statut de lecture

Résumé seul | sections lues : <liste> | papier complet.
Ce qui suit est déduit et non affirmé par les auteurs : <…>

## Lecture automatique

Critical reading note (based only on the supplied passages): The paper adapts the method of Faucett et al. for mapping a network's decisions onto physical observables, applying it to convolutional-autoencoder anomaly detection in jet substructure. It proposes two surrogate strategies that use a small number of high-level observables. The first, a high-level neural network, regresses the autoencoder output directly. The second, a paired neural network, learns the difference between the autoencoder's outputs on a pair of events. The abstract claims that both strategies match the autoencoder's background decision ordering, that both independently select the same six high-level observables, and that both perform similarly to the autoencoder as anomaly detectors across several signals. This suggests that learning to order background events carries over to ordering signal events. Per the section list, there is also a comparison with Isolation Forests and an ablation using only prime EFPs. Limitations of this extraction: the supplied passages contain only the abstract, the table of contents, and author emails. They include no numerical results: no AUC or decision-ordering values, no names for the six observables, and no dataset or signal details. The paper reports no FPGA, hardware, latency, power, or resource measurements, so the 'autoencoder-fpga' axis tag looks wrong and should be removed or confirmed by hand. The extraction is also flagged ok=false, with a warning that section IV was merged into the previous section. Because no measured hardware or quantitative benchmark result was supplied, no benchmark rows are produced.
