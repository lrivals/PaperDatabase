---
id: arxiv-2409.13537-shizishangpt-agricultural-large-language-model
fiche: done
date: 2026-11-03
---

# ShizishanGPT: An Agricultural Large Language Model Integrating Tools and Resources

Shuting Yang, Zehui Liu, Wolfgang Mayer, 2024, arXiv preprint. https://arxiv.org/abs/2409.13537
Type : preprint non relu par les pairs

## Problème

Les LLM généralistes manquent de connaissances spécialisées en agriculture (surtout sur les cultures, notamment le maïs) : connaissances non mises à jour, pas d'accès à des outils de prédiction (génétique, phénotype), réponses jugées imprécises ou refusées (Abstract, §1, Fig. 1). Les auteurs veulent un système de questions-réponses agricole qui combine LLM, RAG et outils.

## Méthode

Système modulaire sur architecture agent ReAct + RAG (§2.1, §3.2, §3.3), cinq modules (§3.4) :
- module générique basé sur GPT-4 (analyse de la question) ;
- module de recherche web (type Google), injecté dans le prompt ;
- module de récupération : base vectorielle de plus de mille documents agricoles (sélection, découpage et modèle d'embedding : n/r) ;
- module graphe de connaissances AgriKG (entités : classification des cultures, climat, ravageurs) ;
- module d'outils externes : prédiction de phénotype du maïs (ResNet), prédiction de valeur d'enrichissement de promoteurs (riz/maïs), et une liste de modèles (croissance, choix variétal, suivi ravageurs, alerte météo, marché), dont seuls les deux premiers sont décrits avec une architecture (§3.3, §3.4).
Les prompts sont construits par extraction de mots-clés et de verbes d'action de la requête (§3.1). Si le premier outil échoue, l'agent ré-analyse et enchaîne d'autres outils (§3.2). Aucun garde-fou ni validation humaine n'est décrit.

## Plateforme et implémentation

Plateforme matérielle : n/r (pas de puce, de latence, de puissance ni de coût d'inférence). LLM : GPT-4 (version n/r). Code, jeu de données et poids annoncés publics : https://github.com/Zaiwen/CropGPT (Abstract) ; non vérifié ici.

## Résultats

Jeu d'évaluation : 100 paires question-réponse créées pour l'étude (questions amorcées à la main, étendues avec ChatGPT, filtrées à la main ; réponses issues de sites agricoles professionnels) (§4). Pas de split.
- Scores automatiques (Table 1, BLEU/ROUGE/GLEU) : ShizishanGPT 0.88 / 0.79 / 0.85, composite 0.923 ; ChatGPT-4 0.876, Claude 0.857, WenXinYiYan 0.818, ZhiPuAI 0.815 (composite).
- Évaluation humaine (Table 2, 0-10, pondération 50 % exactitude, 30 % professionnalisme, 20 % fluidité, au moins 3 évaluateurs en aveugle, §4.2) : ShizishanGPT 9.65 (exactitude 9.8, professionnalisme 9.5, fluidité 9.5) ; GPT4 9.29, Claude 9.26, WenXinYiYan 9.11, ZhiPuAI 8.94.
- Ablation (Table 3, total) : sans RAG 9.21 ; sans outils 9.37 ; sans AgriKG 9.50 (exactitude et professionnalisme légèrement meilleurs sans AgriKG) ; sans recherche 9.44.
→ reportés dans `benchmarks.csv` : 6 lignes proposées (Table 1 composite, Table 2 total, 4 ablations Table 3), plateforme `n/r`, métriques de QA et non de vision. Les baselines (GPT4, Claude…) ne sont pas ajoutées, ce sont d'autres modèles ; elles sont citées en colonne `baseline`.

## Limites et critique

- Jeu de test de 100 questions généré avec ChatGPT, non indépendant (§5) ; couverture limitée (maïs, riz) ; pas d'intervalles de confiance, pas de test de significativité, écarts de 0.3 à 0.4 point sur 10.
- Évaluateurs aveugles à la source, mais leur nombre et leur accord inter-évaluateurs ne sont pas donnés (n/r).
- BLEU/ROUGE/GLEU mesurent le recouvrement lexical, que les auteurs jugent eux-mêmes limité (§4.1) ; la formule du score composite n'est pas donnée. Les valeurs de Table 1 (BLEU 0.88) sont très élevées pour une QA ouverte, sans explication (déduit : réponses de référence possiblement proches des sources du RAG, fuite possible, non vérifiée).
- Incohérence interne : le texte de §4.3 donne 9.1 en fluidité pour le système complet, alors que Table 2 et Table 3 donnent 9.5 ; la pondération redonne bien 9.65 avec 9.5.
- Baselines non appariées : GPT4/Claude/etc. sont sans RAG ni outils ; la comparaison mesure la présence de ressources, pas l'architecture. Pas de baseline GPT-4 + RAG seul ni de comparaison avec un système existant (Shennong, §2.2).
- Pas de mesure de latence, de coût, de taux d'hallucination, ni de sécurité. Aucun garde-fou ni validation humaine des actions : ce sont des outils de prédiction, pas des actionneurs.
- Métadonnées (3 auteurs) marquées « à vérifier à la main » à l'ingestion.

## Pertinence pour la thèse

Axe `llm-agent` (SerreIA : agent LLM avec validation humaine). Apport : patron d'architecture agent ReAct + RAG + graphe de connaissances + outils spécialisés, et protocole d'évaluation de QA agricole (scores automatiques et humains en aveugle, ablation par module). Utile comme exemple de base vectorielle de littérature pour alimenter les consignes de culture. Laisse ouvert l'essentiel du projet : cibler une serre (tomate, laitue, basilic, fraise) plutôt que le maïs en génétique, agir sur un système physique, garde-fous, preuves citées, validation humaine, évaluation sur des consignes chiffrées. Faible niveau de preuve (preprint, jeu auto-généré) : à citer comme illustration, pas comme référence de performance.

## Gaps identifiés

- Aucune évaluation d'un agent LLM agricole sur des consignes chiffrées vérifiables (T°, VPD, EC/pH) par espèce et stade.
- Pas de garde-fous ni d'humain dans la boucle dans les agents LLM agricoles de ce papier ; pas de mesure des erreurs dangereuses.
- Pas de benchmark public de QA agricole non généré par LLM.

## Statut de lecture

papier complet : `fulltext.md` lu en entier (Abstract, §1-§6, légendes et Tables 1-3). Extraction grobid, `ok: true`, aucun tableau signalé sans corps ; les chiffres des Tables 1-3 concordent avec le texte, sauf l'écart de fluidité signalé (§4.3 contre Tables 2-3). Code non consulté. Figure 2 (architecture) : légende vide dans l'extraction, architecture lue dans §3.3-§3.4.
Ce qui suit est déduit et non affirmé par les auteurs : la fuite possible entre références et base RAG, le caractère non apparié des baselines, l'absence de garde-fous (silence du papier).
