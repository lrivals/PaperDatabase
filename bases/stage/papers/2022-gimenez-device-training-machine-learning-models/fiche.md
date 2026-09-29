---
id: 2022-gimenez-device-training-machine-learning-models
fiche: done
date: 2026-09-29
---

# On-Device Training of Machine Learning Models on Microcontrollers with Federated Learning

Nil Llisterri Giménez, Marc Monfort Grau, Roger Pueyo Centelles, Felix Freitag, 2022, Electronics. https://doi.org/10.3390/electronics11040573
Type : article de journal

## Problème

Le TinyML sépare l'entraînement (sur PC) de l'inférence (sur MCU) : le modèle déployé est
statique et ne peut s'adapter aux données de terrain. Les auteurs entraînent un réseau **de zéro
sur le microcontrôleur** et étendent cet entraînement par apprentissage fédéré, dont l'usage sur
MCU était très peu étudié (§1, §2).

## Méthode

- Application de détection de mots-clés (KWS) : enregistrement d'une seconde à 16 kHz
  (16 bits, 32 Ko), MFCC à 13 coefficients sur 50 trames = vecteur de 650 valeurs (§3.2).
- **Réseau** : MLP 650-25-3 (16 325 poids, 28 biais), float32, soit 65 412 octets en RAM ;
  initialisation aléatoire à chaque démarrage (§3.3).
- **Entraînement en ligne**, échantillon par échantillon, rétropropagation avec erreur
  quadratique, taux d'apprentissage 0,6, momentum 0,9 ; label donné par le bouton pressé
  (§3.4-3.5).
- **Apprentissage fédéré** : FedAvg sur 3 cartes, serveur Python sur PC relié en série USB ;
  un tour fédéré toutes les n époques locales ; échantillons pré-enregistrés rejoués depuis le
  serveur pour la reproductibilité (§3.6-3.7).
- Jeu de données propre (2 puis 3 mots-clés, 180 échantillons chacun, publié) ; expériences
  sur la fréquence des tours fédérés, la taille de la couche cachée (5 à 25) et des données
  non-IID (un mot-clé par carte) (§4).

## Plateforme et implémentation

- **Arduino Nano 33 BLE Sense** (FPU, 256 Ko de SRAM, 1 Mo de Flash) (§3.3) ; puce nRF52840
  (Cortex-M4) non nommée dans le texte (déduit de la carte).
- Mémoire : buffer audio 32 Ko + poids 65 Ko + variations de poids (momentum) 65 Ko + statique
  ≈ 48 Ko → **210 Ko sur 262 Ko (80,2 %)** ; chaque neurone caché coûte ≈ 5,2 Ko (§4.4).
- Temps : passe avant 3-4 ms, rétropropagation 9-10 ms (§5).
- Communication : ≈ 130 Ko par client et par tour ; modèle serveur → client ≈ 5,5 s, client →
  serveur ≈ 1,8 s, limité par le buffer série de 64 octets (§4.3, §5).
- Énergie : n/r. Code et données publiés : https://github.com/NilLlisterri/TinyML-FederatedLearning
  (§3.6, §4.1).

## Résultats

- La perte d'entraînement décroît avec les époques sur chaque carte seule (§4.2, Fig. 5b) ;
  **aucune précision de classification n'est rapportée**, seulement des courbes de perte.
- Tours fédérés plus fréquents → perte plus vite réduite (tous les 2 contre tous les 30
  époques) (§4.3, Fig. 6), mais temps d'entraînement accru : 309 s sans tour fédéré, 401 s
  avec 12 tours, 1253 s avec 120 tours pour 120 échantillons (Table 1).
- Couches cachées plus grandes → perte réduite plus tôt (§4.4, Fig. 7).
- Non-IID : le modèle global renvoyé a une forte perte sur le mot-clé local ; des tours à chaque
  époque aident (§4.5, Fig. 8).

→ reportés dans `benchmarks.csv` : 2 lignes (latence passe avant 3-4 ms et rétropropagation
9-10 ms sur Arduino Nano 33 BLE Sense ; borne haute retenue, §5, `medium`).

## Limites et critique

- **Pas de métrique de précision** : impossible de juger la qualité du KWS appris ; la perte
  d'entraînement seule ne dit rien de la généralisation.
- Tâche jouet (2-3 mots-clés, un locuteur, 360-540 échantillons).
- Liaison série USB, sans radio : les temps de communication et l'absence de mesure d'énergie
  ne reflètent pas un déploiement IoT réel (BLE, LoRa discutés sans mesure, §5).
- Float32 et pas de quantification pendant l'entraînement.
- Pas de mesure de l'oubli : le réseau est réinitialisé à chaque démarrage et les mots-clés
  sont alternés, pas appris en séquence.

## Pertinence pour la thèse

Référence utile pour le **budget mémoire de l'entraînement sur Cortex-M4** : le texte donne une
décomposition claire (poids + tampon de momentum = 2 × taille du modèle, plus les buffers
d'entrée) et un ordre de grandeur de latence (≈ 13 ms par pas d'apprentissage pour ≈ 16 k
paramètres). Il montre qu'un MLP float32 de 65 Ko est entraînable sur 256 Ko de SRAM, ce qui
situe la marge disponible pour stocker en plus une matrice de Fisher (une valeur par poids,
≈ 65 Ko de plus en float32, déduit) dans un EWC embarqué.

## Gaps identifiés

- Entraînement sur MCU en précision réduite (INT8) : non traité.
- Apprentissage fédéré + CL sur MCU (non-IID = dérive entre clients) : oubli non mesuré.
- Énergie de l'entraînement sur l'appareil et de la communication radio : non mesurée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Table 1 extraite ; figures non disponibles (les
résultats de perte sont graphiques).
Déduit et non affirmé par les auteurs : puce nRF52840, coût mémoire d'une Fisher pour ce modèle.
