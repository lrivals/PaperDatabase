---
id: arxiv-2601.08308-agriagent-contract-driven-planning-capability
fiche: done
date: 2026-11-03
---

# AgriAgent: Contract-Driven Planning and Capability-Aware Tool Orchestration in Real-World Agriculture

Bo Yang, Yu Zhang, Yunkui Chen, Lanfei Feng, Xiao Xu, Nueraili Aierken, Shijian Li, 2026, arXiv preprint. https://arxiv.org/abs/2601.08308 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Les agents LLM agricoles appliquent un paradigme d'exécution unique à des tâches de complexité très variable et à des outils souvent incomplets ; les plans implicites en langage naturel produisent des étapes manquantes, des dépendances fausses et des erreurs en cascade sur les tâches longues et multimodales (Abstract, §1).

## Méthode

Architecture à deux niveaux avec un routeur selon la complexité (§3.1).
- System-1 (voie rapide) : modèles par modalité (AgriGPT, AgriGPT-VL, AgriGPT-Omni) avec RAG partagé (dense, sparse, graphe), réponses fusionnées par AgriGPT-Omni (§3.2).
- System-2 (tâches complexes) : plan en DAG dont chaque nœud porte but, entrées/sorties, contraintes et exigences de preuve (§3.3.1) ; « need contracts » au niveau capacité (schémas, préconditions, critères de qualité, §3.3.2) ; génération et révision du plan par débat entre agents superviseurs (critique, défense, révision, §3.3.3) ; ToolHub avec fiches d'outils et appariement TDI (index de descriptions) + TOCI (§3.3.4) ; ToolMaker qui génère, teste et enregistre un outil quand aucun ne convient (§3.3.5) ; exécution avec validation de schéma, traces et agrégation de preuves (§3.3.6).

## Plateforme et implémentation

Matériel, puissance, latence : n/r. Modèles de base évalués : Qwen2.5-7B/14B, Qwen3-8B/32B, LLaMA3-8B, AgriGPT-8B (Table 2). Code et données : annoncés « après acceptation », donc non publiés (Abstract).

## Résultats

- ToolMaker : 380 générations réussies sur 392 (96,94 %) ; échecs attribués par les auteurs à l'environnement externe (Table 4, §4.3).
- Planification par contrats : meilleure que react et plan-and-execute selon les auteurs, sur métriques programmatiques et juge LLM (Table 1, §4.3). Corps de Table 1 absent du texte extrait : aucun chiffre repris.
- ToolHub : Hit@1/3/5 stables quand le nombre d'outils croît (jusqu'à 506 outils, dérivés de ToolHop), alors que all-in-prompt et top-k se dégradent (Table 2, §4.3). Le corps de Table 2 est illisible (colonnes fusionnées, intitulés de colonnes perdus) : non repris.
- System-1 : meilleur que CoT et ToT à toutes les échelles (Table 3, §4.2). Corps absent : aucun chiffre.
→ reportés dans `benchmarks.csv` : 1 ligne proposée (ToolMaker, 96,94 %), non écrite par cette tâche ; voir le CSV du scratchpad.

## Limites et critique

- Jeu System-2 de 1 000 tâches construit par les auteurs, non publié ; lien avec les 392 tentatives de la Table 4 non précisé. Pas de baseline pour ToolMaker.
- Métriques en partie jugées par un LLM, « approximate proxies » de l'aveu des auteurs (§4.1) ; aucune évaluation humaine, aucun test sur système physique réel malgré le titre « real-world ».
- Coût et latence du débat multi-agents non mesurés ; les auteurs reconnaissent le surcoût sur tâches longues et la dépendance au respect des schémas pour les petits modèles (Limitations).
- Aucune garde-fou ni validation humaine pour des actions sur actionneurs : les « contrats » vérifient le format et les preuves, pas la sécurité physique (déduit, non affirmé).
- Code et données non disponibles.

## Pertinence pour la thèse

Axe `llm-agent` de SerreIA. Apport : un patron de plan vérifiable (DAG + contrats avec préconditions, contraintes et critères de succès, preuves jointes) transposable à un agent qui propose des actions sur la serre, et le routage simple/complexe pour limiter le coût. Ne traite ni actionneurs, ni consignes de culture, ni humain dans la boucle : les garde-fous du projet restent à concevoir. Le lien avec le contrôle climatique est inféré, non traité par le papier.

## Gaps identifiés

- Agents LLM agricoles évalués sur actionneurs réels avec validation humaine : absent.
- Garde-fous de sécurité physique (bornes de consignes, preuves) pour contrats d'outils : absent.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction grobid, ok). Tables 1 et 3 sans corps extrait ; corps de Table 2 illisible ; seule Table 4 est exploitable (recoupée par §4.3).
Ce qui suit est déduit et non affirmé par les auteurs : absence de garde-fous physiques et de validation humaine ; pertinence pour le contrôle climatique.
