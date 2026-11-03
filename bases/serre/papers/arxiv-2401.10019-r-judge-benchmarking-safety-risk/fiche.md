---
id: arxiv-2401.10019-r-judge-benchmarking-safety-risk
fiche: done
date: 2026-11-03
---

# R-Judge: Benchmarking Safety Risk Awareness for LLM Agents

Tongxin Yuan, Zhiwei He, Lingzhong Dong, Yiming Wang, Ruijie Zhao, Tian Xia, Lizhen Xu, Binglin Zhou, Fangqi Li, Zhuosheng Zhang, Rui Wang, Gongshen Liu, 2024, arXiv preprint. https://arxiv.org/abs/2401.10019 (arXiv 2401.10019 ; pas de DOI)
Type : preprint non relu par les pairs

## Problème

Les évaluations de sécurité des LLM portent sur le contenu généré (offensant, illégal, biaisé), pas sur le comportement d'un agent qui agit dans un environnement interactif (§1). Les moniteurs LLM existants (ToolEmu, AgentMonitor) supposent que le LLM sait repérer une action risquée dans une trajectoire multi-tours utilisateur / agent / environnement, ce qui n'a jamais été mesuré (§1). Les auteurs posent la question : un LLM est-il conscient des risques (« risk awareness ») quand on lui donne l'enregistrement d'une interaction d'agent ?

## Méthode

- Tâche « agent safety monitor » : le LLM reçoit un enregistrement R = (instruction utilisateur, [(pensée, action, retour d'environnement)]) et produit une analyse puis un label binaire safe / unsafe (§2, Éq. 2).
- Benchmark R-Judge : 569 enregistrements, 5 catégories (program, IoT, software, web, finance), 27 scénarios, 10 types de risque, 52,7 % d'enregistrements unsafe, 2,6 tours et 206 mots en moyenne (§3.4). Sources : 414 attaques par injection de prompt indirecte (InjecAgent) ; 155 risques non intentionnels (81 ToolEmu, 24 AgentMonitor, 55 construits à la main) (§3.4). Étiquettes et descriptions de risque (schéma Motivation / Trigger / Outcome, §A.3) rédigées par 6 annotateurs, qui sont aussi des auteurs (§C). Règle de curation : même si l'utilisateur demande l'action risquée, l'agent doit demander confirmation, sinon unsafe (§B.2).
- Deux tests en série (§3.5) : jugement de sécurité (F1, Recall = détection des cas unsafe, Spécificité = cas safe) contre le label du consensus humain ; identification du risque (« Effectiveness », 0 à 100) notée par un GPT-4 qui compare l'analyse du modèle à la description humaine. Accord GPT-4 / humains : PCC moyen 0,91 sur 50 cas unsafe (§4.2).
- 11 LLM en Zero-Shot-CoT (GPT-4o, ChatGPT, Llama-2, Llama-3, Vicuna, Mistral) ; analyses : ajout des types de risque au prompt, Few-Shot-CoT à 2 exemples, comparaison Llama vs Llama Guard (§4-5).

## Plateforme et implémentation

Sans objet matériel : évaluation de LLM (API pour les modèles GPT, poids ouverts pour les autres), matériel, latence, puissance et quantification : n/r. Données publiées : https://github.com/Lordog/R-Judge (Résumé). Détails d'hyperparamètres et de coûts renvoyés à l'annexe F, absente du texte extrait.

## Résultats

- Jugement de sécurité, F1 sur l'ensemble (Zero-Shot-CoT, Table 1) : GPT-4o 74,45 ; Llama-3-8B-Instruct 61,01 ; Llama-2-13b-chat 54,80 ; Llama-2-7b-chat 53,74 ; ChatGPT 44,96 ; Vicuna et Mistral entre 16,93 et 29,33. Score aléatoire : 51,32 (Table 1). Seul GPT-4o dépasse l'aléatoire dans les deux tests (§4.3) ; l'abstract dit que « no other models significantly exceed the random » alors que Llama-3-8B, Llama-2-13b et Llama-2-7b sont au-dessus de 51,32 dans la Table 1 (écarts de 2 à 10 points).
- Par origine du risque (Table 1) : GPT-4o F1 72,19 (attaques intentionnelles, Spec 42,06) et 80,90 (risques non intentionnels, Spec 89,09). Plusieurs modèles ont un Recall élevé et une Spécificité très basse (Llama-2-7b : Recall 91,50, Spec 7,48 sur les attaques), c'est-à-dire qu'ils disent « unsafe » presque partout.
- Prompts (Table 2) : ajouter les types de risque n'aide que ChatGPT (F1 44,96 vers 70,57) et dégrade GPT-4o (74,45 vers 71,16) ; Few-Shot-CoT n'améliore pas globalement (GPT-4o 74,19 ; ChatGPT 20,06 ; Llama-3-8B 42,63 ; Llama-2-13b 60,27).
- Fine-tuning (Table 3, prompt avec types de risque) : Meta-Llama-Guard-2-8B F1 71,84 (Recall 74,00, Spec 64,31) contre 55,81 pour Meta-Llama-3-8B-Instruct ; LlamaGuard-7b F1 0,66 (Recall 0,33, Spec 100) contre 24,14 pour Llama-2-7b-chat (§5.2).
- Étude de cas GPT-4o (§5.3, qualitative, pas de mesure) : échecs en simulation de scénario, adaptabilité aux conditions, alignement sur le consensus humain.
→ reportés dans `benchmarks.csv` : lignes proposées par l'agent (13), non écrites dans le CSV à ce stade : 11 LLM de la Table 1 (F1 « All », Zero-Shot-CoT) + LlamaGuard-7b et Meta-Llama-Guard-2-8B (Table 3, F1). Les lignes de la Table 2 et les chiffres Recall / Spec ne sont pas reportés (colonne métrique unique : F1).

## Limites et critique

- Petit jeu (569 cas) : 414 viennent d'InjecAgent, soit 72,8 % (414 sur 569, calculé) ; le reste est mêlé de cas retouchés (cas « safe » fabriqués en remplaçant l'action risquée d'un cas ToolEmu unsafe, §3.3), d'où un risque d'artefacts de construction.
- Annotateurs = auteurs (6 personnes, §C) ; l'accord inter-annotateurs sur les labels n'est pas chiffré dans le texte lu. Le choix « l'agent doit toujours demander confirmation » (§B.2) est une convention forte qui pénalise des actions parfois acceptables.
- Le test d'identification repose sur un GPT-4 comme juge, validé sur 50 cas seulement (PCC 0,91, §4.2), et GPT-4o est évalué par un juge de la même famille.
- Chiffres de la Table 1 non strictement cohérents avec d'autres endroits : la Table 2 donne d'autres Effect pour GPT-4o (88 contre 93 / 78 selon le sous-ensemble) ; la Table 3 donne F1 24,14 pour Llama-2-7b-chat contre 53,74 en Table 1 (prompt avec types de risque contre Zero-Shot-CoT : déduit, la Table 3 ne le précise pas pour cette ligne mais c'est cohérent avec 55,81 de Llama-3-8B dans la Table 2). Légendes des Tables 4 et 5 décalées dans le texte extrait.
- L'effet « fine-tuning aide » compare Llama Guard à son modèle de base, mais Llama Guard est un autre modèle avec d'autres données ; les auteurs spéculent sur la cause (§5.2). Une seule exécution par configuration, aucune variance ni intervalle de confiance rapportés (n/r).
- Le moniteur juge des traces enregistrées, hors boucle : pas de mesure de la latence ni du coût d'un moniteur en ligne, ni de l'efficacité réelle à bloquer des actions.
- Pas de baseline non LLM (règles, listes d'actions interdites) alors qu'elles sont la solution naturelle pour un système physique ; déduit, non affirmé par les auteurs.

## Pertinence pour la thèse

Base serre, axe `llm-agent` (agent LLM dont les actions sur la serre sont validées par un humain, garde-fous). Apport : (1) un cadre pour évaluer un moniteur de sécurité d'agent, avec des catégories directement transposables (IoT : smart home, traffic control ; risques physiques, pertes de données, dommages matériels) ; (2) un résultat négatif utile : sans fine-tuning, les LLM de petite taille (7 à 13 B), seuls envisageables en local, ne distinguent presque pas safe d'unsafe (Table 1), donc ne pas leur confier la validation seule ; (3) la règle « demander confirmation même si l'utilisateur le demande » (§B.2) justifie la validation humaine du projet. Reste ouvert (déduit) : aucun scénario agricole ou de serre (irrigation, chauffage, nutriments), pas d'évaluation de garde-fous déterministes en amont du LLM, pas de mesure sur actionneurs réels.

## Gaps identifiés

- Aucun benchmark de sécurité d'agent pour la conduite d'une serre (actionneurs, consignes hors plage, pompes, dosage pH/EC) : à créer à partir des 10 types de risque de R-Judge.
- Comparaison garde-fous à règles vs moniteur LLM sur des traces d'actions de serre : non traitée.
- Coût et latence d'un moniteur LLM local (Raspberry Pi 5) : n/r dans le papier.

## Statut de lecture

papier complet : `fulltext.md` lu en entier (extraction grobid, `extraction.ok` vrai). Annexes D.1 (formules des métriques), F (hyperparamètres, coûts, versions de modèles) et la Table 5/8/9 absentes ou sans corps dans le texte extrait (avertissement « Table 5 sans corps extrait ») : non lues. Tables 1 à 3 lues dans le texte extrait ; leurs colonnes ne sont pas toutes alignées (Table 1 : seul F1 est donné pour « All »).
Ce qui suit est déduit et non affirmé par les auteurs : que « unsafe » est la classe positive du F1 (le texte dit seulement que Recall mesure les cas unsafe, §4.1) ; l'explication des écarts Table 1 / Table 3 pour Llama-2-7b ; l'absence d'intervalles de confiance (non vue dans le texte extrait) ; toute la section Pertinence (transposition à la serre) ; l'absence de baseline à règles.
