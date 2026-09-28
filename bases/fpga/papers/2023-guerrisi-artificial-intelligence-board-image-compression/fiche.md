---
id: 2023-guerrisi-artificial-intelligence-board-image-compression
fiche: done
date: 2026-09-26
---

# Artificial Intelligence Based On-Board Image Compression for the Φ-Sat-2 Mission

Giorgia Guerrisi, Fabio Del Frate, Giovanni Schiavon, 2023, IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 16, 8063-8075. https://doi.org/10.1109/JSTARS.2023.3296485
Type : article de journal (open access CC BY 4.0 ; métadonnées issues de l'export IEEE Xplore)

## Problème

Les satellites d'observation de la Terre produisent plus de données que la liaison
descendante n'en transmet. Compresser à bord par IA économiserait bande passante et stockage
(Abstract, §I). La littérature sur la compression par DL d'images de télédétection ne dit
presque rien de la plateforme à bord (§I). Les auteurs veulent aussi mesurer ce que coûte la
migration d'un modèle du sol vers l'environnement embarqué, en précision et en temps
(§I, Abstract).

## Méthode

- **Autoencodeur convolutif (CAE)**. L'encodeur compte 10 convolutions 3 × 3 à leaky ReLU
  (16, 32, 64 puis 128 filtres, stride alterné 1/2) et se termine par un flatten de 8 192
  unités. Le décodeur est symétrique, en convolutions transposées. Entrée 256 × 256 × 1 : le
  taux de compression vaut 65 536 / 8 192 = 8 (§II-A, §III-A, Fig. 2).
- **Découpage** : l'encodeur tourne à bord, le décodeur au sol ; le vecteur compressé est en
  float16 (§II-A, §III-A).
- **Données** : 10 acquisitions Sentinel-2 L1C (6 d'entraînement, 4 de validation), converties
  pour simuler la caméra Φ-Sat-2 (bandes, résolution, SNR, FTM). 48 640 patches 256 × 256
  (§II-B, §III-A, Table I).
- **Entraînement** : perte SSIM, Adam, TensorFlow 2.1 (§III-A).
- **Déploiement** : conversion OpenVINO puis exécution de l'encodeur sur **Intel Movidius
  Myriad 2 (VPU)**, reliée **en USB** à une machine locale ; comparaison avec un GPU GTX 1650 et
  un CPU i7-6700 (§III-C, §III-D).
- **Métrique applicative** : une segmentation de bâtiments par UNet (Inria Aerial) est
  comparée sur images originales et reconstruites, par nombre d'objets et distance de Hamming
  (§III-E).

## Plateforme et implémentation

- **Aucun FPGA.** La plateforme cible est la VPU Myriad 2, retenue pour Φ-Sat-1 et Φ-Sat-2 et
  testée en radiation au CERN (§III-C). Les FPGA ne sont cités qu'en travaux liés : [17], qui
  combine CNN et JPEG sur Zynq-7020 et Zynq MPSoC avec un taux de compression de 2 (§IV).
- Encodeur de 2,4 MB, mis à jour possible en vol (§IV).
- **Puissance** (Table V) : VPU 1,4 W, GPU 83 W, CPU 45,5 W. Méthode de mesure n/r →
  `power_scope: unspecified`.
- Précision numérique sur la VPU : n/r. Code non publié.

## Résultats

| Mesure | GPU GTX 1650 | VPU Myriad 2 | CPU i7-6700 | Source |
|---|---|---|---|---|
| Temps d'encodage d'une acquisition | 0,95 s | 10,92 s | 1,9 s | Table V, §III-C |
| Puissance | 83 W | 1,4 W | 45,5 W | Table V |
| « Energy efficiency » (GFLOPS/W) | 0,011 | 0,058 | 0,010 | Table V |
| SSIM moyen (validation) | 0,9651 | 0,9647 | n/r | §III-B, §III-C |

- SSIM de test à l'entraînement : 0,9766, avec une MSE d'environ 2e-4 (Table II).
- Face à JPEG 2000 au même taux (×8), le CAE fait mieux sur les 3 images de validation :
  0,977 contre 0,944, 0,990 contre 0,983, 0,956 contre 0,947 (Table IV).
- Segmentation : même nombre de bâtiments détectés (11 et 11, 20 et 20, Table VI) ; distance
  de Hamming entre masques de 0,016 et 0,014, et au plus environ 8,5 % des pixels sur les
  patches (§III-E, Fig. 17).

→ reportés dans `benchmarks.csv` : 3 lignes (encodeur CAE sur Myriad 2, GTX 1650 et i7-6700,
Table V). `confidence: medium` (tableaux reconstruits par Docling avec OCR). Le SSIM est
reporté ×100 dans `accuracy_value`.

## Limites et critique

- **VPU dix fois plus lente que le GPU** (10,92 contre 0,95 s). Les auteurs l'expliquent
  d'abord par le transfert USB, sans le mesurer à part (§III-D). Le temps sur VPU mêle donc
  calcul et interface, ce qui n'est pas représentatif d'un système de vol intégré.
- **« Energy efficiency »** : le calcul est donné (FLOPS / W), mais pas le nombre de FLOP du
  modèle. Il n'y a pas d'énergie par image, seulement une puissance sans méthode de mesure.
- **Taux de compression fixé par l'architecture** (bottleneck flottant de 8 192) et
  **sans codage entropique** : ×8 seulement, loin des codecs appris à hyper-prior (voir F-LIC,
  `2022-sun-f-lic-fpga-learned-image`). Comparaison avec JPEG 2000 sur 3 images seulement.
- **Données simulées** à partir de Sentinel-2 : le jeu représentatif de Φ-Sat-2 n'existe pas
  encore (§IV).
- La segmentation (Inria, RGB à 0,3 m) ne porte pas sur les mêmes données que la compression
  (monobande Sentinel-2 simulé) : le transfert du résultat reste à établir.
- Aucun FPGA : la comparaison se limite à un GPU desktop et à un CPU.

## Pertinence pour la thèse

C'est un cas d'usage réel et spatial d'**autoencodeur convolutif sur images en embarqué**, sur
une VPU et non sur un FPGA. Il fournit une baseline de plateforme à battre : 1,4 W, environ
11 s par acquisition, SSIM de 0,96 au taux ×8. Il montre aussi que la migration vers le
matériel embarqué coûte surtout du temps, pas de la précision (écart de SSIM de 0,0004). Porter
ce même CAE sur une FPGA durcie ou spatialisable (Zynq, Kintex) et le comparer à la Myriad 2
à mesure de puissance égale serait une contribution nette. Les auteurs citent un seul travail
FPGA ([17], ×2).

## Gaps identifiés

- Gap « autoencodeurs sur FPGA appliqués aux images » : **confirmé**. Même la mission de
  référence de compression d'images par autoencodeur tourne sur VPU, pas sur FPGA.
- Comparaison VPU / FPGA / GPU embarqué pour un même autoencodeur d'images : absente.
- Compression apprise à bord avec codage entropique (hyper-prior) sur plateforme embarquée :
  absente (F-LIC le fait sur une grosse FPGA au sol).

## Statut de lecture

Papier complet (`fulltext.md` en entier, extraction GROBID). **Tableaux I, II, IV, V et VI
reconstruits par Docling avec OCR** ; ceux de la Table V sont cohérents avec le texte (1,4 W,
83 W, 10,92 s). La Table III (métriques de test) n'a pas de corps : ses PSNR sont n/r. La
fin de §III-B est tronquée : la définition du temps de traitement sur GPU est coupée.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de mesure séparée du
transfert USB ; la comparaison avec F-LIC ; la non-représentativité du temps VPU pour un
système intégré.
