---
id: 2025-wu-adaptive-continual-learning-method-nonstationary
fiche: done
date: 2026-09-29
benchmarks: none
---

# An Adaptive Continual Learning Method for Nonstationary Industrial Time Series Prediction

Mengqing Wu, Xiaofeng Zhou, Shuai Li, Haibo Shi, 2025, IEEE Transactions on Industrial Informatics. https://doi.org/10.1109/TII.2024.3468433
Type : article de journal

## Problème

Les modèles de prévision de séries temporelles industrielles se dégradent quand les
conditions opératoires changent. Réentraîner sur tout l'historique coûte en calcul et en
stockage ; le fine-tuning sur les seules données nouvelles provoque l'oubli catastrophique
(Abstract, §I). Les méthodes de CL à distillation de logits (DER…) s'appliquent mal à la
régression, dont la sortie est continue (§III-A).

## Méthode

Rejeu enrichi pour la régression, sur un encodeur TS2Vec modifié (§III, Fig. 4) :

- **Hint-based learning** (§III-A) : le buffer stocke (x, y, z) avec z la représentation
  intermédiaire de l'encodeur. Perte = L_cur + α·MSE(f(x_m), y_m) + β·MSE(h(x_m), z_m)
  + γ·MSE(h_{t−1}(x_t), h_t(x_t)) (Eq. 5-8) ; inspiré de FitNets (Romero) et de SER.
- **Double buffer** (§III-B, Fig. 3, Alg. 1) : buffer standard (réservoir) pour les tâches
  passées, et petit *soft buffer* de C échantillons du batch courant dont l'erreur varie peu
  (LP = |ε_t − ε_{t−1}|), réinjectés avec le batch suivant.
- **TimeRelu** (§III-C, Eq. 10) : ReLU dont la pente et le seuil sont produits par des
  petits réseaux à partir de features temporelles (minute, heure, jour…) ; remplace toutes
  les ReLU du TCN.
- **Métriques** (§IV-A1, Eq. 11-15) : erreur moyenne, forgetting measure, backward et
  forward transfer adaptés à une erreur (plus bas = mieux).
- **Données** : NREL Solar Power (PV 70 MW, pas 5 min, 105 120 points ; 5 tâches
  chronologiques de 20 000 points + 5120 points de méta-test) (§IV-A) ; broyage-classification
  minier réel (tâches = débit d'alimentation 330, 340, 350 t/h en février 2023 ; méta-test
  320 t/h en mars 2023 ; scénario domain-incremental) (§IV-B1). Fenêtre 20, horizon 10.
- **Comparaisons** : MAS, SI, ER, DER, MIR, CLS-ER, SER, fine-tune, single-task, multi-task
  (§IV-A2).

## Plateforme et implémentation

- Portable AMD R7-6800H, 16 Go RAM, NVIDIA RTX 3060 6 Go ; PyTorch (§IV). Aucune exécution
  embarquée.
- Précision numérique, taille du buffer en octets, mémoire, énergie : n/r.
- Code : non publié.

## Résultats

Tables I à VI absentes ou sans corps à l'extraction : **aucune valeur d'erreur n'est
disponible dans le texte**. Constats qualitatifs des auteurs :
- Meilleure erreur moyenne et moins d'oubli sur les données solaires, forward transfer
  perfectible (Table II, §IV-A2) ; méthode la plus basse en erreur moyenne tout au long de la
  séquence (Fig. 7).
- Rejeu > régularisation (MAS, SI) sur les deux jeux (§IV-A2, §IV-B2).
- Ablation solaire : TimeRelu contribue le plus (Table III) ; ablation broyage : soft buffer
  → erreur moyenne, hints → oubli, TimeRelu → forward transfer (Table VI).
- Sur le broyage, l'apprentissage mono-tâche garde la meilleure MSE moyenne (§IV-B2).
- Seule valeur chiffrée : l'entraînement cumulatif prend 507,6 s sur la dernière tâche
  solaire ; la méthode proposée est plus lente que les autres méthodes de CL (Fig. 13).

→ aucune ligne dans `benchmarks.csv` : les tableaux de résultats ne sont pas dans le texte
extrait et le texte ne donne aucune erreur chiffrée (`benchmarks: none`).

## Limites et critique

- **Tâches découpées à la main** (blocs chronologiques, paliers de débit), sans détection de
  transition ni analyse du type de dérive — reconnu par les auteurs (§V).
- TimeRelu exploite des features calendaires : pertinent pour le solaire, très périodique,
  mais cela mélange adaptation au temps et apprentissage continu ; l'ablation lui attribue
  l'essentiel du gain solaire (Table III), ce qui relativise l'apport CL (déduit).
- Définitions de bornes discutables : le fine-tune est présenté comme « upper limit for new
  tasks » et le single-task comme « upper limit for all tasks » (§IV-A2).
- DER++ apparaît en Fig. 8 mais pas dans la liste des méthodes comparées (§IV-A2).
- Jeu de broyage privé : non reproductible ; un seul méta-test par jeu.
- Coût mémoire des buffers annoncé (§IV-C) mais le passage est tronqué à l'extraction.

## Pertinence pour la thèse

Confirme, sur des séries temporelles industrielles en régression, que le rejeu bat MAS et SI
(§IV-A2, §IV-B2), et propose une façon de faire du rejeu « à la DER » en régression (stocker
la représentation intermédiaire plutôt que les logits). C'est un contrepoint à la
régularisation pure envisagée pour le MCU : le coût d'un buffer (x, y, z) sur quelques ko de
RAM reste à évaluer (déduit). Sans chiffres extraits, la fiche ne permet pas de comparaison
quantitative.

## Gaps identifiés

- Détection automatique des transitions de tâches en prévision industrielle (§V).
- Coût mémoire d'un rejeu à représentations intermédiaires sur MCU.
- Comparaison rejeu vs régularisation à budget mémoire égal en régression.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables I et II absentes, Tables III à VI sans
corps ; Algorithm 1 et §IV-C (mémoire) partiellement tronqués. Pour les chiffres, relire le
PDF ou repasser l'extraction des tableaux (Docling).
Déduit et non affirmé par les auteurs : la part de TimeRelu dans le gain CL, le coût
mémoire sur MCU.
