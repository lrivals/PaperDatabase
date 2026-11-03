---
id: arxiv-2405.14411-large-language-models-explainable-decisions
fiche: done
date: 2026-11-03
benchmarks: none
---

# Large Language Models for Explainable Decisions in Dynamic Digital Twins

Nan Zhang, Christian Vergara-Marcillo, Georgios Diamantopoulos, Jingran Shen, Nikos Tziritas, Rami Bahsoon, Georgios Theodoropoulos, 2024, arXiv preprint. https://arxiv.org/abs/2405.14411 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Les décisions autonomes d'un jumeau numérique dynamique piloté par les données (DDT, cadre DDDAS) sont difficiles à comprendre : elles demandent des connaissances techniques et métier, et sont exprimées en mesures de capteurs peu lisibles (§1). Les auteurs veulent savoir si un LLM peut fournir des explications en langage naturel de ces décisions, pour que les utilisateurs les comprennent et leur fassent confiance (§1, Abstract).

## Méthode

- Architecture de référence où le LLM est une couche intermédiaire entre le DDT et l'humain, et non le décideur (§2, §3). Quatre rôles selon qui décide (§3.1) : le DDT (le LLM est interprète externe, sans intrusion), l'humain (dialogue bidirectionnel : état du système, traduction d'instructions en commandes de simulation what-if, retour des décisions), le LLM (planificateur boîte noire, Chain-of-Thought suggéré), ou une décision collaborative.
- Seul le premier cas est expérimenté : le DDT décide, le LLM explique (§3.1, §4).
- Cas d'étude agricole : flotte de drones à deux résolutions (survey haute altitude basse résolution, inspection ciblée). La ferme est une grille de tuiles ; un indice de confiance par tuile α_i = |µ_Good(V_i) − µ_Bad(V_i)|, calculé sur le NDVI moyen avec fonctions d'appartenance floues (Eq. 1-2, §4.1). Une tuile est à inspecter si α_i < T_α. Le replanning fait un what-if par drone candidat : seuls ceux dont la batterie prédite dépasse T_b sont retenus, puis le Δt minimal (Δt = t_rem + t_disp + t_insp) est choisi (§4.1). L'Algorithm 1 n'est pas présent dans le texte extrait.
- Explication : RAG (LangChain), `gpt-4-turbo-2024-04-09` et `text-embedding-ada-002`. Base de connaissances = le texte du papier avant §4 (.tex) plus une description du JSON des résultats ; contexte = états des drones et résultats de simulation JSON (§4.2). Prompts contraints à 50-70 mots.
- Pas de quantification ni de toolflow FPGA (sans objet).

## Plateforme et implémentation

Pas de matériel embarqué : LLM via API OpenAI (cloud), orchestration LangChain ; aucune puce, fréquence, puissance ou ressource rapportée (n/r). Pas de simulateur complet ni de déploiement terrain (§5). Code publié : https://github.com/explainable-digital-twins/RAG-DDDAS (note de bas de page, §4.2) ; lien non vérifié par nous.

## Résultats

Démonstration qualitative sur deux scénarios, aucune métrique (§4.2, Fig. 3) :
- Scénario 1 : le DDT envoie le Drone 1 (Δt 38,50, batterie prédite 50) alors que le Drone 2 a un Δt plus faible (25,29) mais une batterie prédite de 10 < T_b = 15. Le LLM relie correctement le symbole T_b à sa définition du modèle de planification, bien que la simulation ne le décrive pas.
- Scénario 2 : le DDT choisit un drone occupé (Drone 3, Δt 21,61, batterie 73) plutôt qu'un drone prêt (Drone 1, Δt 44,94). Le LLM répond au « pourquoi aucun drone ne part maintenant ? » (Answer 1) et explique le rôle de T_b (Answer 2).
- Hallucination relevée par les auteurs : « Other drones have higher Δt or are busy » (Answer 2) ; l'état busy n'intervient pas dans l'algorithme de planification (§4.2).
- Explications adaptables à des profils (agriculteur, IT, agronome, Fig. 2) : affirmé, non évalué ; modèles d'utilisateur renvoyés au travail futur.
→ reportés dans `benchmarks.csv` : aucune ligne (pas de résultat quantitatif ni de plateforme matérielle ; benchmarks: none).

## Limites et critique

- Preuve de concept : 2 scénarios, aucune évaluation systématique (fidélité, taux d'hallucination, évaluation par des experts), reconnue par les auteurs (§5).
- Fuite de contexte probable (déduit) : la base RAG contient le texte du papier décrivant le modèle de planification, donc la bonne réponse est largement fournie ; la généralisation à un système réel et documenté de façon moins ordonnée n'est pas testée.
- Les explications sont a posteriori, produites sur un JSON de sortie : aucune garantie qu'elles reflètent le calcul réel du DDT (déduit). L'hallucination observée en est un exemple.
- LLM propriétaire et cloud : dépendance réseau et à un fournisseur, non discutée (déduit).
- Dimensions du problème (grille de tuiles, 3 drones) minuscules ; paramètres a1, b1, a2, b2, T_α non donnés dans le texte extrait.
- Pas de comparaison avec un autre LLM, un autre RAG ou un gabarit déterministe d'explication.

## Pertinence pour la thèse

Axes confirmés : `llm-agent` et `iot-greenhouse` (jumeau numérique). Pour SerreIA : patron de couche d'explication RAG par-dessus un contrôleur à règles (décisions du contrôleur et seuils déjà structurés en JSON), qui s'appose à l'agent LLM avec validation humaine, avec un LLM interprète sans autorité de décision (le rôle « DDT décide » correspond au contrôleur à règles de SerreIA). Utile comme garde-fou de transparence et comme exemple de défaut (hallucination d'une condition absente de l'algorithme). Hors sujet direct : contexte drone/NDVI, pas de serre, pas d'edge, aucun chiffre réutilisable.

## Gaps identifiés

- Évaluation systématique de la fidélité des explications LLM d'un contrôleur (mesure d'hallucination, vérification automatique contre le journal de décision).
- Explications avec LLM local/edge (RPi 5) plutôt qu'API cloud.
- Explication de décisions de contrôle climatique en serre (pas seulement drone/NDVI).

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID, ok). La section 4 n'a pas été détectée comme section numérotée (son texte est rattaché à §3) et l'Algorithm 1 est absent du texte extrait. Fig. 3 reconstruite à partir de fragments de texte.
Ce qui suit est déduit et non affirmé par les auteurs : fuite de contexte RAG ; explications non garanties fidèles au calcul ; dépendance cloud ; équivalence avec le contrôleur à règles de SerreIA.
