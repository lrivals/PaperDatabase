---
id: arxiv-2509.18610-singer-onboard-generalist-vision-language
fiche: done
date: 2026-10-01
---

# SINGER: An Onboard Generalist Vision-Language Navigation Policy for Drones

Maximilian Adang, JunEn Low, Ola Shorinwa, Mac Schwager, 2025, arXiv preprint. https://arxiv.org/abs/2509.18610
Type : preprint non relu par les pairs

## Problème

Navigation de drone guidée par langage naturel en monde ouvert (open-vocabulary), avec uniquement capteurs et calcul embarqués. Les auteurs identifient trois verrous : rareté des démonstrations de vol à grande échelle, exigences de contrôle temps réel pour stabiliser un drone, absence d'estimation de pose externe fiable (Abstract, §I). Les approches existantes diffusent les commandes depuis un poste externe, exigent une pose externe, ou sont limitées à une trajectoire / un environnement (SOUS-VIDE) (§II).

## Méthode

Trois composants (§I, §IV, §V) :
- Simulateur photoréaliste FiGS (3D Gaussian Splatting) enrichi d'un champ sémantique CLIP distillé dans le 3DGS (§IV-B).
- Expert : arbres RRT* inversés dans le temps, un arbre par objet sémantique, trajectoires sans collision ; vol de ces trajectoires par un MPC robuste simulé (ACADOS), avec randomisation de domaine (masse et coefficient de poussée à ±30 %, pose et vitesse perturbées toutes les 2 s) (§IV-C, §IV-D).
- Politique visuomotrice légère (SV-Net de SOUS-VIDE) entraînée par imitation : l'entrée n'est pas le RGB mais les logits de CLIPSeg (requête texte + image) convertis en carte de chaleur sémantique ; réseau d'historique (masse, poussée) puis extracteur de caractéristiques et tête d'action, sortie en poussée collective et vitesses angulaires (body rates) à 20 Hz. Score de similarité normalisé par le maximum vu pendant le vol (pseudo-mémoire) (§V).
- Jeu de données : environ 1650 trajectoires, 15 requêtes sémantiques, 5 scènes 3DGS intérieur / extérieur, 907 440 paires observation-action (§V). Entraînement sur RTX 4090 + i9-14700.
- Déploiement : CLIPSeg (CLIP ViT-B/16, 86 M de paramètres) tracé en ONNX et exécuté via CUDA ONNX Runtime, de façon asynchrone par rapport à la politique à 20 Hz (§V). Pas de quantification déclarée.

## Plateforme et implémentation

- Drone Lumenier Cine-whoop 5 pouces, contrôleur Pixracer R15 Pro, calculateur NVIDIA Jetson Orin Nano 8 Go, caméra ZED Mini utilisée en RGB monoculaire (VGA 672 x 376, résolution minimale pour limiter la charge), ARK Flow (flux optique + télémètre) (§VI-C). Gamme de puissance : Jetson (quelques W à ~10 W, déduit ; le papier ne donne aucune valeur).
- Chaîne de traitement d'image à 12-13 Hz, dominée par CLIPSeg ; CLIPSeg seul à 3 Hz sans optimisation, jusqu'à 12 Hz avec ONNX (§V, §VI-C). Grille de 42 x 24 patches 16 x 16.
- Puissance, latence, mémoire, consommation énergétique, autonomie : n/r.
- Code ou modèle publiés : non mentionnés dans le texte extrait (n/r).

## Résultats

Hardware, scénario le plus dur (3 requêtes inconnues, environnement inconnu, bureau factice, 6 expériences x 5 essais = 30 essais), succès = sous-métrique du but (§VI-D, Fig. 5) :
- SINGER (north vrai fourni en externe) : < 1 m du but 76,67 % (23/30), arrêt au-delà 6,67 % (2/30), collisions 16,67 % (5/30) ; la requête est toujours gardée dans le champ de vue.
- Baseline (CLIPSeg + centrage du masque + PD de cap, vitesse constante) : < 1 m 53,33 % (16/30), arrêt court 3,33 % (1/30), collisions 26,67 % (8/30), requête perdue 16,67 % (5/30).
- SINGER entièrement embarqué (sans north externe, magnétomètre) : < 1 m 66,67 % (20/30), collisions 16,67 % (5/30), 6/30 échecs par mauvaise requête suivie ; la baseline ne fonctionne pas du tout dans ces conditions.
- Résumé des auteurs : +23,33 % d'atteinte, +16,67 % de requête dans le champ de vue, -10 % de collisions (Abstract).
- Simulation : 90 expériences x 10 essais, 6 environnements, 9 requêtes ; facile : but atteint 73 %, < 1 m 92,7 % ; moyen et difficile : chiffres seulement en Fig. 4 (barres), non extraits, donc non reportés (§VI-D).

→ reportés dans `benchmarks.csv` : 5 lignes (3 essais matériel, 2 débits CLIPSeg). Pas de FLOPs, ni de puissance : `power_w` à n/r.

## Limites et critique

- Évaluation matérielle faible en effectifs : 30 essais par bras, 3 requêtes, un seul bureau factice, sans intervalles de confiance ; différences (23 vs 16 succès) à interpréter prudemment.
- Baseline minimale, écrite par les auteurs (le papier la dit « minimal implementation ») ; pas de comparaison avec VLFly, GRaD-Nav++ ou FAn (cités en §II comme exigeant une pose externe).
- Le résultat « fully onboard » repose sur un north vrai externe pour la comparaison principale ; sans lui, le magnétomètre dégrade (66,67 %).
- Pas d'évitement d'obstacles explicite : les auteurs reconnaissent que c'est la limite principale (§VI-D, §VII). Résolution réduite (VGA) et segmentation instable image par image.
- Aucune mesure de puissance, énergie, latence de bout en bout, utilisation GPU ou mémoire du Jetson : la dimension « IA embarquée » est affirmée par le débit (12 Hz) seulement. Débit du pipeline perception (12-13 Hz) inférieur à la boucle de commande (20 Hz) : le découplage asynchrone n'est pas évalué en termes de latence.
- Métrique (taux d'atteinte sous le mètre) non comparable aux métriques de détection (mAP) ni aux benchmarks FPGA de la base.
- Comparaison déduite (non faite par le papier) : le même ViT-B/16 sur Jetson Orin Nano à 12 Hz reste loin de la gamme nano-drone (mW) ; ce travail relève de la gamme Jetson.

## Pertinence pour la thèse

Cas de référence de politique end-to-end langage-conditionnée entièrement embarquée sur Jetson Orin Nano (axe tracking-navigation), avec le goulot identifié : le modèle de fondation de perception (CLIPSeg / ViT-B/16, 86 M de paramètres), pas la politique de contrôle. Point d'entrée pour une question de co-design perception-contrôle (débit du VLM, latence, énergie, sécurité de vol), et pour la transposition d'un tel front-end sur FPGA / accélérateur à faible puissance, que le papier n'aborde pas. Complète la référence de latence perception → contrôle de la base (vol agile en gamme Jetson, Kaufmann / Loquercio).

## Gaps identifiés

- Aucun VLM / CLIP embarqué sur drone n'est caractérisé en puissance, énergie ou latence ; un front-end CLIPSeg quantifié ou porté sur FPGA / NPU reste à faire (lien drone-fpga et system-codesign).
- Pas de métrique système (autonomie, vitesse de vol sûre) liée au débit de perception (12 Hz) ni à la consommation.
- Évitement d'obstacles et robustesse à l'occultation ou aux petits objets non traités.
- Reproductibilité : code, jeu de données de 907 k échantillons et poids non mentionnés.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, y compris les références). Attention : `extraction.backend` = `pymupdf` et `extraction.ok` = `false` : texte possiblement mal découpé ; les figures (Fig. 4 simulation par difficulté, Fig. 5 matériel) ne sont pas extraites, seuls les chiffres du texte sont repris. Aucun tableau de résultats dans l'extraction.
Déduit, non affirmé par les auteurs : la gamme de puissance du Jetson ; l'absence de quantification (non mentionnée, pas déclarée comme absente) ; l'absence de publication du code (non mentionnée dans le texte lu) ; le rattachement des 30 essais aux « < 1 m » comme critère de succès principal (le texte parle aussi d'un but à 2 m).
