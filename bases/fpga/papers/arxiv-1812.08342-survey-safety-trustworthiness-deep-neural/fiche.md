---
id: arxiv-1812.08342-survey-safety-trustworthiness-deep-neural
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Survey of Safety and Trustworthiness of Deep Neural Networks: Verification, Testing, Adversarial Attack and Defence, and Interpretability

Xiaowei Huang, Daniel Kroening, Wenjie Ruan, James Sharp, Youcheng Sun, Emese Thamo, Min Wu, Xinping Yi, 2018, arXiv preprint (version portant la mention Dstl, © Crown copyright 2020). https://arxiv.org/abs/1812.08342
Type : preprint non relu par les pairs (survey, pas de DOI dans `metadata.json`)

## Problème

Les DNN dépassent l'humain sur plusieurs tâches, mais leur déploiement dans des systèmes critiques (voitures autonomes, diagnostic médical) soulève des inquiétudes de sûreté et de confiance (§1). Les auteurs posent « Trustworthiness = Certification + Explanation » (§1) : la confiance repose sur une certification avant déploiement (démontrer à une autorité, par ex. l'EASA, que le produit satisfait des exigences) et sur une explication du comportement pendant la vie du produit. Le verrou : les DNN sont des boîtes noires sans fondements rigoureux, et les techniques classiques de vérification et de test logiciel ne s'appliquent pas directement (§1.1). Le survey recense 202 papiers, dont la plupart postérieurs à 2017 (Résumé, Fig. 1).

## Méthode

Revue de littérature structurée en quatre volets, après préliminaires formels (§2) et définition de propriétés de sûreté (§3) :
- Propriétés (§3) : robustesse locale, atteignabilité des sorties (*output reachability*), propriété d'intervalle, propriété lipschitzienne, avec leurs relations (Fig. 5).
- Vérification (§4) : classée par type de garantie : déterministe (SMT/SAT : Reluplex, Planet, encodage SAT de réseaux binarisés ; MILP), borne approchée (interprétation abstraite AI2, optimisation convexe, analyse d'intervalles ReluVal, FastLin/CROWN), bornes convergentes (DLV, DeepGame, DeepGO, DeepTRE), garanties statistiques (CLEVER). Complexité NP-complète (§4.5). Comparaison en Table 1.
- Test (§5) : critères de couverture (neurones, safety coverage, extensions de neuron coverage, MC/DC pour DNN, projection quantitative, surprise coverage), génération de tests (mutation d'entrées, fuzzing, exécution concolique, GAN, analyse différentielle), test par mutation de modèles. Comparaison en Table 2. Le lien avec DO-178C, MC/DC et niveaux ASIL est fait en §5 et §5.1.7.
- Attaques et défenses (§6) : L-BFGS, FGSM, JSMA, DeepFool, C&W, transformations naturelles, perturbations universelles ; défenses (adversarial training, distillation, transformations d'entrée, détection de région adverse) et défenses certifiées. Table 3.
- Interprétabilité (§7) : visualisation, ranking (LIME, Integrated Gradients, LRP, DeepLIFT, GradCAM, SHAP, TCAV, L2X), saliency maps, modèles simplifiés (règles, arbres, automates), théorie de l'information (information bottleneck).
- Défis futurs (§8) : métriques de distance proches de la perception humaine, systèmes à composants appris (assurance compositionnelle), OOD et surveillance à l'exécution (§8.8), humain dans la boucle.

## Plateforme et implémentation

Sans objet : survey purement logiciel et théorique. Aucune cible matérielle (FPGA, GPU, MCU), aucune mesure de puissance ou de ressources. Code / bitstream : sans objet. Seul contact avec le matériel : la vérification de réseaux binarisés par SAT (§4.1.1, Narodytska et al.) et la mention des problèmes de virgule flottante dans les solveurs (§4.2).

## Résultats

Pas de résultat expérimental propre : c'est une revue. Chiffres notables : 202 papiers surveillés (Résumé, §1) ; réseaux vérifiables de « quelques milliers » de neurones cachés par les méthodes à borne approchée, jusqu'à 10 000 (§4.2, §4.3) ; les méthodes complètes (Pulina et Tacchella) validées sur des réseaux de moins de 10 neurones (§4.1.1) ; DLV passe à l'échelle jusqu'à VGG16 (§4.3.1). Ces chiffres sont ceux des travaux cités, pas des mesures des auteurs.
→ reportés dans `benchmarks.csv` : aucune ligne (survey sans mesure matérielle, et règle « ne rien ajouter pour un survey »).

## Limites et critique

- Date : arrêté fin 2018 (papier daté 2018, version révisée avec contenu jusqu'à 2020). Ne couvre ni les détecteurs d'objets (YOLO) ni la vérification/test des réseaux quantifiés en entier à part la brève mention des réseaux binarisés (§4.1.1). Presque tout est illustré sur MNIST, CIFAR10, ImageNet en classification (Table 3) ; détection et segmentation sont marginales (§6.4, §8.3).
- Les techniques de vérification formelle ne passent pas à l'échelle de réseaux modernes (§4.3, §8.5) ; la couverture de neurones est jugée insuffisamment validée (§8.6). Ce sont les auteurs eux-mêmes qui le disent : ces méthodes ne fournissent pas aujourd'hui de preuve d'assurance recevable.
- Aucune mise en correspondance systématique avec les normes de sûreté (IEC 61508, ISO 26262, DO-178C ne sont cités que ponctuellement, §5) ; l'idée « Trustworthiness = Certification + Explanation » est un cadrage des auteurs, pas une définition normative.
- Point à vérifier sur les sources : le texte extrait est incomplet à quelques endroits (voir Statut de lecture), donc certaines sous-sections ne sont pas lisibles.
- Biais possible : forte présence de travaux de leur propre groupe (DLV, DeepGame, DeepGO, DeepConcolic).
- Prise en compte du *hardware* absente : aucune discussion de la fiabilité matérielle (SEU, fautes) ni du déterminisme d'exécution.

## Pertinence pour la thèse

Axe `surveys` (les axes de `base.json` ne rangent pas ce papier sous `safety-certification` par la règle lexicale, mais c'est son objet). Bonne carte d'entrée du vocabulaire « sûreté du ML » pour la thèse « IA embarquée sécuritaire certifiable » : il distingue vérification formelle, test structurel (MC/DC adapté aux DNN), défenses adverses (volet *security*, secondaire dans le profil) et explicabilité. §8.8 justifie directement la surveillance à l'exécution et la détection OOD pour un YOLO de vidéosurveillance en zone dangereuse ; §8.7 (assurance de systèmes à composants appris, cas d'assurance) donne le cadre pour un dossier de certification. Laisse ouvert tout ce qui est propre à l'embarqué : vérification de réseaux quantifiés/INT8 déployés sur FPGA, équivalence modèle-flot HLS/bitstream, fiabilité matérielle, détection d'objets.

## Gaps identifiés

- Vérification formelle et test structurel de détecteurs d'objets (YOLO) et non seulement de classifieurs : quasi absents de ce survey.
- Vérification de l'équivalence entre le modèle vérifié (flottant) et l'implémentation quantifiée sur FPGA (seuls les réseaux binarisés sont traités, §4.1.1).
- Lien entre critères de couverture DNN (neuron, MC/DC-like) et exigences d'une norme applicable (IEC 61508 / ISO 13849) : évoqué pour DO-178C et ASIL seulement (§5, §5.1.7).
- Surveillance à l'exécution et OOD sur cible embarquée : identifiés comme défi ouvert (§8.8), sans solution.

## Statut de lecture

papier complet : `fulltext.md` lu en entier (1305 lignes), extraction Grobid. Réserves d'extraction : les sections 2 et 6 ne sont pas détectées (leur texte est rattaché à la section précédente) ; sous-sections manquantes ou tronquées dans le texte extrait : §6.2.3 (titre sans contenu), §7.3.2 à §7.4 (méthodes de saliency et *influence functions*, seulement une formule résiduelle), fin de §7.6.3 ; les Tables 1 à 3 sont sans corps fiable (Table 1 en particulier : coches non extraites). Ce qui suit est déduit et non affirmé par les auteurs : la pertinence pour la thèse, le constat d'absence de YOLO / détection d'objets et de matériel, la critique sur le biais d'auto-citation.
