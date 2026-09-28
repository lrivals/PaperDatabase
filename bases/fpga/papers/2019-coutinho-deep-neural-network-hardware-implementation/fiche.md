---
id: 2019-coutinho-deep-neural-network-hardware-implementation
fiche: done
date: 2026-09-26
---

# Deep Neural Network Hardware Implementation Based on Stacked Sparse Autoencoder

Maria G. F. Coutinho, Matheus F. Torquato, Marcelo A. C. Fernandes, 2019, IEEE Access 7, 40674-40694. https://doi.org/10.1109/ACCESS.2019.2907261
Type : article de journal (IEEE Access, relu par les pairs)

## Problème

Les DNN ont un coût de calcul élevé qui freine leur usage applicatif, surtout sur de gros
volumes de données (§I). Les implantations FPGA antérieures d'autoencodeurs empilés (SSAE)
passent par OpenCL / HLS, jugées moins efficaces, ou ne concernent que de petits
autoencodeurs de reconstruction (§II). Les auteurs proposent une implémentation RTL de la
phase feedforward d'un **Stacked Sparse Autoencoder** utilisé comme **classifieur**.

## Méthode

- Réseau : SSAE entraîné hors ligne sous Matlab (couches cachées = encodeurs de sparse AE
  pré-entraînés sans supervision, puis couche softmax supervisée, §III-A). Seule
  l'inférence est implantée. Architecture de validation **784-100-50-10** (§V-D).
- **Réseau systolique** : un PE par neurone, entrées sérialisées, PE en parallèle (§IV-A1,
  Fig. 3). Une seule fonction d'activation par couche, par table (ROM 2^16 entrées : sigmoïde
  sur 13 bits, exponentielle du softmax sur 57 bits, §IV-A3).
- **Virgule fixe** (§IV-A) : entrées 1.12 (13 bits, non signées), poids cachés et biais
  5.12 (17 bits), poids de sortie 7.12 (19 bits).
- Deux variantes :
  - **Proposition 1** : poids fournis en flux (pas de mémoire de poids), donc même matériel
    réutilisable pour un autre problème sans reconfiguration ; débit limité par le nombre
    G de flux de poids parallèles (§IV-A, §V-B1, Eq. 28-33) ;
  - **Proposition 2** : poids stockés en ROM dans chaque PE ; débit fixé par le chemin
    critique ; reconfiguration nécessaire pour changer de problème (§IV-B).
- Modèles analytiques de ressources (régressions linéaires par PE, Eq. 10-26), de débit
  (Eq. 7, 31, 34), de performance (Eq. 33, 37) et de puissance dynamique (régressions sur
  mesures, Eq. 38-49), extrapolés à d'autres FPGA (Table 3, Table 4).
- Toolflow : RTL (§II, §VI) ; langage non précisé dans le texte extrait.

## Plateforme et implémentation

- Virtex-6 **XC6VLX240T-1FF1156**, kit ML605 (§V-D, Fig. 30).
- Proposition 1 : 220 multiplieurs (28,65 %), 37 796 cellules logiques (15,67 %)
  (Table 12). Proposition 2 : 220 multiplieurs (28,65 %), 24 399 cellules logiques
  (10,12 %) (Table 14). Les multiplieurs sont vraisemblablement des DSP48 (220/768 = 28,65 %,
  et 768 = `n max Mult` du XC6VLX240T en Table 3) ; LUT et BRAM : n/r (les auteurs
  donnent des « logic cells »).
- Temps (proposition 1, G = 1, Q = 800) : t_rc = 10 ns, délai initial 2,4 ms, t_ff = 0,8 ms
  (Table 13).
- Puissance : **puissance dynamique** « mesurée » (Tables 6, 7, 9, 10, 13, 15), méthode
  non décrite dans le texte extrait (outil ou instrument ?) → portée `unspecified`. Il ne
  s'agit en aucun cas de la puissance de la carte.
- Code / bitstream : non publiés ; une vidéo de démonstration de la proposition 2 est citée
  ([35], §V-D).

## Résultats

- Précision MNIST (10 000 images de test) : **93,38 %** sur FPGA contre 93,4 % sous Matlab
  (flottant 64 bits) ; MSE entre sorties 2,1 × 10⁻⁶ (§V-D1). Valable pour les deux
  propositions (§V-D2).
- Proposition 1 (G = 1, Q = 800) : **1,25 k images/s**, t_ff 0,8 ms, P_d 0,003 W mesurée
  (0,0047 W estimée) (Table 13).
- Proposition 2 (Q = 800) : **25 k images/s**, t_ff 0,04 ms, t_c 45 ns, P_d 0,112 W mesurée
  (0,110 W estimée) (Table 15). Le texte (§V-D2) donne des valeurs un peu différentes :
  t_PE 48 ns, t_ff 0,03 ms, 26 000 images/s ; les lignes reprennent la Table 15 (Docling),
  avec `confidence: medium`.
- Extrapolations (pas des mesures) : > 1 TOPS projeté sur Virtex UltraScale VU440 pour la
  proposition 1 avec η ≥ 0,3 (§V-B1, Fig. 20, Table 4) ; 711 GOPS pour la proposition 2
  (Table 17).
- Comparaisons (Tables 16-17) : proposition 2 ≈ 116× plus rapide et ≈ 11× plus économe que
  le SSAE OpenCL sur Stratix V de [5] ; ≈ 1784× plus rapide que DLAU [14] sur XC7Z020 ;
  4,11× Caffeine et 11,5× Zhang et al. (FPGA'15) en GOPS.

→ reportés dans `benchmarks.csv` : **2 lignes** — proposition 1 (G = 1) et proposition 2,
SSAE 784-100-50-10, XC6VLX240T, MNIST, Tables 12-15.

## Limites et critique

- **Comparaisons très biaisées** (Tables 16-17) :
  - réseaux différents (3072-2000-750-10 sur CIFAR-10 pour [5], 784-256-256-10 pour [14])
    face à des débits calculés par les équations des auteurs, avec des paramètres Q et G
    choisis ;
  - GOPS projetés sur un FPGA hypothétique à 10 000 PE (VU440) comparés à des GOPS
    **mesurés** de CNN (Caffeine, Zhang 2015) : un MLP dense et un CNN n'ont ni la même
    intensité arithmétique ni les mêmes contraintes mémoire (déduit) ;
  - la « puissance » de [5] et [14] est vraisemblablement une puissance carte ou puce
    totale, face à une puissance **dynamique** de quelques mW ici : le gain de 1000× en
    puissance n'a pas de sens physique (déduit).
- Réseau minuscule (MLP de 3 couches sur MNIST, 93,4 % de précision, nettement sous un CNN).
  L'« autoencodeur » n'est qu'une méthode d'entraînement : le matériel est un MLP
  feedforward, sans décodeur ni reconstruction.
- Puissance dynamique seule, méthode non décrite ; pas de puissance statique ni carte.
- Écarts entre texte et tableaux (48 vs 45 ns, 26 000 vs 25 000 images/s).
- Pas de comparaison avec un CPU, un GPU ou un MCU pour le même réseau.
- Code non publié.

## Pertinence pour la thèse

Pour l'axe `autoencoder-fpga`, c'est un contre-exemple instructif : le titre annonce un
autoencodeur, mais seul l'encodeur empilé sert de classifieur MLP sur MNIST. Il ne dit rien
sur la reconstruction d'images, la détection d'anomalies ou la compression sur FPGA. Intérêt
limité aux idées d'implémentation : réseau systolique neurone par PE, activation par ROM,
poids en flux pour réutiliser le matériel (proche d'une idée utile pour un apprentissage
continu où les poids changent, déduit).

## Gaps identifiés

- Confirme le gap connu : les « autoencodeurs sur FPGA » d'images se réduisent souvent à des
  MLP sur MNIST ; aucune reconstruction d'image ni détection d'anomalies visuelles.
- Réutilisation du matériel avec des poids en flux (proposition 1) : piste pour la mise à
  jour des poids en ligne, non explorée par les auteurs (pas d'entraînement embarqué).
- Pas de protocole de puissance comparable (dynamique seule contre carte chez les autres).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). La plupart des tableaux sont reconstruits par
Docling (Tables 1-6, 12-17 : chiffres à vérifier ; Tables 16 et 17 très désorganisées) ;
Tables 7-11 sans corps exploitable ; plusieurs équations (6, 10-11, 41-46) tronquées.
Déduit et non affirmé par les auteurs : multiplieurs = DSP48 ; non-sens de la comparaison
de puissance ; non-comparabilité MLP / CNN en GOPS ; intérêt des poids en flux pour
l'apprentissage continu.
