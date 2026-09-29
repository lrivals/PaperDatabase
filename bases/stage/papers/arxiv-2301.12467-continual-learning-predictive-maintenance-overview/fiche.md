---
id: arxiv-2301.12467-continual-learning-predictive-maintenance-overview
fiche: done
date: 2026-09-29
---

# Continual Learning for Predictive Maintenance: Overview and Challenges

Jhair Hurtado, Alain Salvati, Andrea Cossu, Antonio Carta, Davide Bacciu, 2023, Intelligent Systems with Applications. https://doi.org/10.1016/j.iswa.2023.200251
Type : article de journal (survey / position paper)

## Problème

Les modèles de maintenance prédictive (PdM) sont entraînés sur une distribution figée,
souvent simulée ou limitée, alors que les machines, les capteurs et l'environnement dérivent :
la performance chute faute d'adaptation (Abstract, §1). Symétriquement, l'apprentissage
continu (CL) est évalué sur des benchmarks synthétiques (splits aléatoires de jeux connus)
éloignés du terrain (§1). Double objectif : apporter le CL à la PdM, et la PdM au CL comme
source de scénarios réalistes (§1).

## Méthode

Survey en sept parties, sans expérience :

- **PdM** (§2) : diagnostic (détection, localisation) vs pronostic (RUL) (§2.1) ; modèles
  classiques (DT, kNN, SVM/SVR) et neuronaux (ANN, AE, CNN, RNN/LSTM, DBN, GAN) (§2.2) ;
  jeux publics (Table 1 : roulements dont Lessmeier 2016 et PRONOSTIA, batteries, Microsoft
  PdM, Turbofan/C-MAPSS, Backblaze…). D'après Diallo et al. (2021), seuls Turbofan et
  Backblaze remplissent les critères d'un benchmark (§2.3). Critère ajouté par les auteurs :
  un jeu doit contenir **plusieurs distributions** (§2.3).
- **Environnements non stationnaires** (§3) : typologie de Quiñonero-Candela (covariate,
  prior probability, domain drift, sample selection bias), dérive abrupte / graduelle,
  permanente / transitoire / récurrente (§3.1) ; détection de dérive fondée sur la
  performance (FLORA, DDM, EDDM, ADWIN, DDD) ou sur la distribution (ITA, PCA, VAE) (§3.2).
- **CL** (§4) : quatre régimes de disponibilité des données (nulle, limitée, partielle,
  totale, Fig. 5) ; pipeline en quatre modules (collecte, modélisation, **détection de
  dérive**, mise à jour, Fig. 6) ; méthodes classiques actives / passives (§4.1) et
  profondes : régularisation (EWC, SI, MAS, LwF), architecture (PNN, HAT, masques),
  mémoire (iCaRL, GEM, rejeu génératif, prompts L2P/DualPrompt) (§4.2).
- **Applications réelles** (§5) : embarqué (Pellegrini 2020, latent replay sur Android ;
  Hayes & Kanan 2022), MLOps (CLaaS), scénarios Blurry / i-Blurry (§5.1-5.3).
- **CL pour la PdM** (§6.1) : cinq travaux recensés — Maschler 2020 (EWC sur Turbofan),
  Maschler 2021 (EWC, Online EWC, SI + LSTM sur batteries Li-ion), Chen 2022 (iCaRL/LUCIR à
  double bloc résiduel), Gori 2022 (LSTM + divergence KL, turbomachines), Tercan 2022 (MAS,
  moulage par injection).
- **Proposition de benchmark** (§7) : découper chaque classe en **concepts** répartis entre
  tâches (au lieu des splits aléatoires NI/NIC), première tâche volumineuse
  (pré-entraînement) ; exemple Backblaze : capacité du disque = concept, modèle = classe
  (§7.3, Fig. 7).

## Plateforme et implémentation

Sans objet : aucune implémentation, aucune plateforme. Code : aucun.

## Résultats

Aucun résultat chiffré propre : survey sans expérience. Aucune ligne dans `benchmarks.csv`
(les chiffres des travaux cités ne sont pas repris).

Constats des auteurs :
- Les travaux CL-PdM recensés n'utilisent que la **régularisation** ; le rejeu, « significantly
  more effective », reste à évaluer en PdM (§6.3).
- Le pré-entraînement vaut mieux que l'entraînement à partir de zéro quand les données sont
  rares (Maschler 2020, 2021 ; Tercan 2022) (§6.2).
- Aucun benchmark CL adapté à la PdM n'existe (§6.3, §8).

## Limites et critique

- Survey « brief » assumé (§1, §2) : pas de méthode de recherche bibliographique décrite
  (requêtes, bases, critères d'inclusion), donc couverture non vérifiable.
- La section CL-PdM (§6.1) ne compte que cinq articles, sans tableau comparatif de leurs
  résultats ni de leurs protocoles.
- **Contraintes embarquées quasi absentes** : l'edge n'apparaît qu'en perspective (§6.3
  « On the edge prediction ») et via Pellegrini 2020 (smartphone). Aucun mot sur les MCU, la
  mémoire en ko, la quantification ou l'énergie (déduit de la lecture complète).
- La proposition de benchmark (§7) reste conceptuelle : ni jeu construit, ni protocole de
  découpage, ni expérience de validation.
- Détection de dérive et CL sont présentés comme modules d'un même pipeline (Fig. 6), mais
  aucun travail couplant les deux en PdM n'est cité.

## Pertinence pour la thèse

Référence de cadrage du stage : c'est le survey qui pose explicitement l'intersection CL ×
PdM, avec la typologie des dérives (§3.1) et le pipeline détection de dérive → mise à jour
(Fig. 6), qui correspond au fil conducteur de la base. Il justifie le choix d'une méthode par
régularisation (seule famille testée en PdM, §6.1) tout en signalant le rejeu comme piste. Il
laisse entièrement ouvert le volet embarqué (MCU, INT8, énergie), ce qui situe l'apport d'un
EWC INT8 sur MCU (déduit).

## Gaps identifiés

- Pas de benchmark CL pour la PdM avec dérive intra-classe (concepts) : proposition non
  réalisée (§7).
- CL-PdM limité à la régularisation ; rejeu et architectures non évalués (§6.3).
- CL pour réseaux récurrents sur séries temporelles de capteurs sans benchmark (§6.3).
- Aucun travail CL-PdM sur MCU ni en précision réduite (déduit de §6.1).
- Couplage détection de dérive → déclenchement de la mise à jour non évalué en PdM (déduit).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Ligatures en partie perdues à l'extraction
(« classi cation ») ; formules de §7.1 illisibles (symboles perdus) ; Table 1 extraite.
Déduit et non affirmé par les auteurs : l'absence des contraintes MCU/INT8/énergie, l'absence
de travail couplant détection de dérive et CL en PdM, le lien avec EWC INT8.
