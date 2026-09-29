---
id: 2023-belay-unsupervised-anomaly-detection-iot-multivariate
fiche: done
date: 2026-09-29
---

# Unsupervised Anomaly Detection for IoT-Based Multivariate Time Series: Existing Solutions, Performance Analysis and Future Directions

Mohammed Ayalew Belay, Sindre Stenen Blakseth, Adil Rasheed, Pierluigi Salvo Rossi, 2023, Sensors. https://doi.org/10.3390/s23052844
Type : article de journal (survey + comparaison expérimentale)

## Problème

Les capteurs IoT industriels produisent des séries temporelles multivariées massives et non
étiquetées ; la détection d'anomalies doit traiter à la fois les motifs temporels (intra-capteur) et
les dépendances entre capteurs, sans labels (Abstract, §1).

## Méthode

- **Revue** (§2-3) : types d'anomalies (ponctuelle, contextuelle, collective) ; trois approches
  (reconstruction, prédiction, compression) et trois familles :
  - classiques : VAR, cartes de contrôle (Hotelling T², MCUSUM, MEWMA), PCA et SSA, clustering
    (k-means, DBSCAN, OC-SVM), Isolation Forest ;
  - réseaux profonds : RNN/LSTM/GRU (prédiction), CNN/TCN, autoencodeurs (MLP, convolutif, VAE),
    GAN, graphes (GDN, MTAD-GAT), Transformers ;
  - composites : LSTM-AE, EncDec-AD, LSTM-VAE, OmniAnomaly, MSCRED, ConvLSTM, DAGMM, USAD, DeepSVDD.
- **Évaluation propre de 13 méthodes** (§4-5) sur SWaT (traitement d'eau, 51 canaux, 36 attaques,
  rééchantillonné à 1 min) et SMD (une seule entité) ; normalisation min-max, fenêtres glissantes ;
  précision, rappel, F1, AUC, AUPR, temps d'entraînement et de test. Hyperparamètres décrits en §5
  (AE à 3 couches et latent 16 ; LSTM/GRU 3 × 64 avec 120 pas d'historique ; IF à 100 arbres).

## Plateforme et implémentation

Entraînement sur Google Colab Pro, GPU NVIDIA T4 ; PyTorch, TensorFlow, scikit-learn (§4.2). Aucune
implémentation embarquée. Code : non publié (n/r).

## Résultats

F1 / AUPR (Tables 2-3) :

| Méthode | SWaT F1 | SWaT AUPR | SMD F1 | SMD AUPR |
|---|---|---|---|---|
| PCA | 0,781 | 0,730 | 0,439 | 0,477 |
| Isolation Forest | 0,762 | 0,766 | 0,401 | 0,405 |
| MLP-AE | 0,764 | 0,738 | 0,504 | 0,507 |
| LSTM (prédiction) | 0,782 | **0,777** | 0,551 | 0,535 |
| **ConvLSTM** | **0,782** | 0,765 | **0,606** | **0,593** |
| USAD / DAGMM / MAD-GAN | 0,758 / 0,752 / 0,716 | ≈ 0,70 | 0,173 | 0,47-0,55 |

- Sur SWaT, toutes les méthodes sont « in the same ballpark » : moins de 0,17 d'écart d'AUPR et
  moins de 0,06 d'AUC ; environ 60 % des anomalies sont détectées sans faux positif, le reste
  (anomalies collectives) échappe à toutes (§5).
- ConvLSTM offre le meilleur compromis ; PCA et IF sont très rapides (entraînement < 1 s sur SWaT)
  et restent proches des réseaux profonds ; les GAN sont instables (§5).

→ reportés dans `benchmarks.csv` : 4 lignes (ConvLSTM sur SWaT et SMD, MLP-AE sur SMD, Isolation
Forest sur SWaT ; F1, Tables 2-3), `high`.

## Limites et critique

- Évaluation sur **une seule entité** de SMD (§4.1) et SWaT rééchantillonné à 1 min : comparaison
  difficile avec OmniAnomaly (Su 2019), qui évalue les 28 entités avec point-adjust.
- Anomalies de valeurs suspectes : VAE et PCA ont des métriques **identiques** sur SWaT, et USAD,
  DAGMM, MAD-GAN ont exactement P = 0,095, R = 1,000, F1 = 0,173 sur SMD, c'est-à-dire un détecteur
  qui déclare tout anormal (déduit) : réglage de seuil défaillant plutôt que limite des méthodes.
- SMD décrit avec 33 métriques (§4.1) mais 38 canaux dans la Table 1.
- Protocole de seuil non précisé pour chaque méthode ; une seule exécution, sans écart-type.
- Pas de mesure mémoire ni de coût d'inférence embarqué, alors que le titre vise l'IoT.

## Pertinence pour la thèse

Survey récent et pratique sur la détection d'anomalies multivariée non supervisée, avec une
comparaison chiffrée qui montre que PCA et Isolation Forest restent compétitifs face à des réseaux
profonds, pour un coût dérisoire : argument pour des détecteurs légers sur MCU (déduit). Il liste
les cartes de contrôle (CUSUM, Hotelling T²) et le PCA avec seuil χ², références statistiques que
la base couvre aussi (Page, Mahalanobis). La détection en flux (« real-time ») est identifiée comme
un défi ouvert (§6).

## Gaps identifiés

- Détection d'anomalies multivariée en flux, avec mise à jour, sur dispositifs contraints (§6).
- Comparaison des détecteurs légers (PCA, IF, AE réduit) en mémoire et énergie sur MCU.
- Anomalies collectives et contextuelles mal détectées par toutes les méthodes testées (§5).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 2-3 lisibles (une cellule décalée pour IF sur
SMD, lue comme P 0,263, R 0,839, F1 0,401) ; §1.2 (contributions) tronqué ; figures non
disponibles.
Déduit et non affirmé par les auteurs : seuil défaillant pour USAD/DAGMM/MAD-GAN, argument MCU.
