---
id: arxiv-1907.06119-understanding-deep-learning-techniques-image
fiche: done
date:
---

# Understanding Deep Learning Techniques for Image Segmentation

Swarnendu Ghosh, Nibaran Das, Ishita Das, Ujjwal Maulik, 2019, arXiv preprint. https://doi.org/10.1145/3329784
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

Critical reading note — Ghosh, Das, Das & Maulik (2019), 'Understanding Deep Learning Techniques for Image Segmentation', arXiv:1907.06119, DOI 10.1145/3329784.

Nature of the paper: this is a survey and tutorial, not an experimental paper. Its stated contribution (Abstract, Contribution) is an intuitive, low-math explanation of deep segmentation methods drawn in one common diagram style. It covers FCN/GAP, DeepMask/SharpMask, the R-CNN family, DeepLab (atrous convolutions, spatial pyramid pooling, dense CRF), CRF-as-RNN and deep parsing networks, PSPNet, RefineNet, convolutional autoencoders (transposed convolution, unpooling, U-Net, SegNet with forwarded pooling indices), GANs, ConvLSTM and attention models, JULE and other unsupervised or self-supervised methods, and interactive methods (two-stream fusion, Deep Extreme Cut, Polygon-RNN). Table 1 lists datasets and Table 2 sorts methods by supervision, learning type and modules.

Numbers in the passages: all accuracy figures are quoted from the cited original works, not measured by the survey authors:
- FCN on PASCAL VOC 2011: pixel accuracy 90.3%, mean IoU 62.7%.
- SharpMask vs DeepMask on COCO: average recall 39.3 vs 36.6.
- RefineNet vs DeepLab-v2 on Person-Part: IoU 68.6 vs 64.9.
- U-Net mean IoU: 0.9203 on PhC-U373 and 0.7756 on DIC-HeLa.
- SegNet on CamVid: mIoU 60.10, vs 53.88 for DeepLab-LargeFOV, 49.83 for FCN and 59.77 for DeconvNet.
- Deep Extreme Cut on PASCAL: mIoU 80.3.
The survey does not say how these were computed (for example, which split or protocol), and they mix metrics that can't be compared directly.

Hardware relevance: none. No passage mentions an FPGA or other hardware platform, quantization, throughput, latency, power or resource use. The automatic 'autoencoder-fpga' axis seems to have been triggered only by the word 'autoencoder'. The FPGA part is wrong and should be removed or corrected when the paper-fiche is written.

Extraction caveats: the metadata is flagged for manual checking, and numbered sections were not detected. As a result, most of the body is labelled '(préambule)' or mislabelled '6. Normalization : The outputs can be normalized with another simple softmax function.', and the Table 2 check-marks lost their column alignment.

Rows: none were produced. There is no measured hardware result to record, and turning numbers from cited works into benchmark rows would credit results to the wrong paper. For any of the figures above, go back to the original paper instead (e.g. SegNet [9], U-Net [177], FCN [130]).
