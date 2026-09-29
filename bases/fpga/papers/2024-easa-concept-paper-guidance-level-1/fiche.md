---
id: 2024-easa-concept-paper-guidance-level-1
fiche: done
date: 2026-09-29
benchmarks: none
---

# Concept Paper: Guidance for Level 1 & 2 Machine Learning Applications

EASA (European Union Aviation Safety Agency), 2024, « Concept Paper, Issue 02 » (auteurs du document : G. Soudain, programme IA de l'EASA, relecture F. Triboulet, approbation A. Leroy ; l'agence est l'auteur institutionnel). Pas de DOI ni d'URL dans `metadata.json`.
Type : document réglementaire / guidance d'une autorité (ni article relu par les pairs, ni preprint). Non contraignant : « anticipated MOC » destinés à préparer de futures règles (Part-AI, RMT.0742, Annexe 1). Le champ `type` de `metadata.json` reste `null` (aucune valeur de l'énumération ne convient).

## Problème

Comment démontrer l'aptitude à la certification d'un système aéronautique embarquant du machine learning, alors que l'assurance de développement classique (exigences, V-cycle, couverture du code) ne s'applique pas à un modèle appris (Foreword ; §B.6.1). Les auteurs listent les difficultés : sources d'incertitude propres au ML, complétude et représentativité des données, compromis biais-variance, robustesse, « boîte noire », autorité partagée humain-IA (§B.1). Le périmètre de cette Issue 02 est limité : IA de niveau 1 (assistance) et 2 (coopération/collaboration), apprentissage supervisé, plus un premier jeu d'objectifs non supervisés ; apprentissage par renforcement et niveau 3 exclus (§B.3, §C.1).

## Méthode

Le document propose un cadre en quatre blocs (Fig. 2-3, §B.2) : (1) analyse de fiabilité (« trustworthiness analysis ») : caractérisation de l'application (CO-01 à CO-06, classification 1A/1B/2A/2B par CL-01, Table 2), évaluation de sûreté (SA-01 à SA-03), sécurité de l'information (IS-01 à IS-03, menaces evasion / poisoning / oracle, rapport ENISA) et évaluation éthique (ET-01 à ET-08, grille ALTAI) ; (2) « AI assurance », dont la « learning assurance » en W (Fig. 11-13) : exigences et ODD (DA-01 à DA-10), gestion des données (DM-01 à DM-08), apprentissage (LM-01 à LM-16), implémentation et vérification du modèle d'inférence (IMP-01 à IMP-12), gestion de configuration (CM-01), qualité (QA-01), réutilisation, COTS et transfert d'apprentissage (RU-01 à RU-03), modèles de substitution (SU-01, SU-02), explicabilité de développement (EXP-01 à EXP-09) ; (3) facteurs humains (explicabilité opérationnelle EXP-10 à EXP-19, teaming HF-01 à HF-34) ; (4) atténuation du risque résiduel (SRM-01, SRM-02 : monitoring de sortie et passivation avec repli sur un système classique) ; plus une section organisation (ORG-01 à ORG-08, exemple des DOA).

Points techniques utiles au sujet : l'ODD (domaine de conception opérationnelle) du constituant ML raffine le domaine opérationnel (DA-03, Fig. 14-16) ; les jeux train / validation / test doivent être indépendants (DM-06, MOC DM-07-5) ; bornes de généralisation quantifiables (LM-04, borne de type VC, avec la remarque que pour de gros réseaux elles sont souvent trop larges, d'après le rapport CoDANN cité) ; stabilité du modèle défini par ‖x'−x‖<δ ⇒ ‖f(x')−f(x)‖<ε (Annexe 3, définitions) ; stabilité et robustesse vérifiées au niveau du modèle entraîné puis du modèle d'inférence (LM-12, LM-13, IMP-09, IMP-10) ; passage de l'estimation de l'erreur à une probabilité de mode de défaillance (MOC SA-01-7 et SA-01-8).

Toolflow, quantification, mapping FPGA : sans objet (pas de méthode d'accélération).

## Plateforme et implémentation

Sans objet : document normatif, pas de plateforme matérielle mesurée. Puce, fréquence, ressources, puissance : n/r. Code / bitstream : sans objet. Les trois études de cas d'aviation (Annexe 2) sont décrites sans mesure matérielle ; le cas Visual Landing System (Daedalean) précise que les essais en vol de la référence citée (FAAVLS) ont tourné sur du matériel COTS non certifié (GPU), pas sur du matériel de production (§F.2.1.3.3).

## Résultats

Pas de résultats expérimentaux au sens des articles de la base. Ce que le document établit :

- **Limites d'acceptation initiales** : en supervisé, l'EASA n'acceptera d'abord que des constituants sans élément IDAL A ou B (SWAL 1 ou 2, AL 1, 2 ou 3) ; en non supervisé, seulement IDAL D / SWAL 4 / AL 5 ; pas de réduction de niveau d'assurance à l'intérieur d'un constituant ML (Foreword ; §B.4 ; MOC SA-01-1). Les objectifs de la modulation par niveau (Chapitre D, tableaux d'applicabilité) ne figurent pas dans le texte extrait (voir Statut de lecture).
- **Apprentissage en ligne exclu** : le modèle doit être « gelé » à l'approbation ; « online learning (also known as continual or adaptive learning) … will not be accepted by EASA at this stage » (§C.1 ; MOC LM-02).
- **Matériel** : pour l'implémentation, les FPGA, ASIC et architectures COTS sont couverts par les guides existants (AMC 20-152A pour les produits) ; en revanche « GPUs and other AI accelerators » ont des spécificités non couvertes (interférences complexes, pipelining non déterministe) et demanderont des guides propres ; pour les multicœurs, AMC 20-193 (MOC IMP-05).
- **Optimisations post-entraînement** : pruning et quantification qui modifient le comportement doivent être traités dans le processus d'apprentissage (LM-06) ; en implémentation, seules les optimisations sans effet sur comportement et performance sont admises (choix de l'arithmétique en virgule fixe, Winograd) (§C.3.1.7.2, MOC IMP-04-2). La préservation des propriétés du modèle après conversion / optimisation / implémentation doit être vérifiée, avec méthodes formelles « expected to be necessary » (IMP-06) ; les méthodes formelles sont jugées prometteuses mais limitées à des évaluations locales (§C.3.1.6).
- **Surveillance à l'exécution** : le système doit surveiller que ses entrées restent dans l'ODD, en plage et en distribution (EXP-05), que ses sorties respectent les bornes de performance (EXP-06) et un niveau de confiance (EXP-04, EXP-07) ; pour les images, un discriminateur OoD est cité (MOC SA-01-3 ; cas VLS avec la méthode ODIN, §F.2.1.3.1). Au-delà, repli sur un système classique (SRM-02).
- **Enregistrement des données** d'exploitation pour l'évaluation de sûreté continue et l'enquête (EXP-09, SA-02).
- Table 4 (changement de plateforme d'inférence) : IMP-01 à IMP-11, CM-01, QA-01 applicables, LM-xx sans changement attendu ; le corps du tableau a été reconstruit par PyMuPDF, non fiable à la cellule.

→ reportés dans `benchmarks.csv` : aucune ligne (document normatif sans mesure ; `benchmarks: none`). Seul chiffre d'exploitation (Table 17, gain de 4,6 à 6,1 % sur un critère de réseau pour l'estimation de montée/descente EUROCONTROL) : hors sujet FPGA, non repris.

## Limites et critique

- Non contraignant et provisoire : les MOC sont dits « anticipated », appelés à évoluer avec MLEAP et les normes EUROCAE/SAE WG-114/G-34 (§B). Aucun MOC abouti pour plusieurs objectifs difficiles (généralisation en particulier).
- Écrit pour l'aviation : les domaines (aéronavigabilité, ATM/ANS, maintenance, formation, aérodromes, environnement) ne couvrent ni l'industrie ni la vidéosurveillance. La transposition à un secteur industriel dangereux (IEC 61508, ISO 13849) est une inférence de cette fiche, non affirmée par le document.
- Peu de contenu spécifique matériel : l'implémentation FPGA est traitée par renvoi à AMC 20-152A ; aucune guidance sur la quantification du CNN, la vérification de l'équivalence numérique modèle entraîné / bitstream, la tolérance aux SEU ou l'usage de HLS. Les objectifs IMP-06 et IMP-07 restent génériques.
- Bornes de généralisation : le document reconnaît lui-même que les bornes disponibles pour de gros réseaux sont trop larges (MOC LM-04), donc l'objectif clé pour le lien performance-sûreté n'a pas de moyen de conformité praticable aujourd'hui pour des CNN de détection.
- Exemples d'application peu détaillés et souvent renvoyés à des rapports externes (CoDANN, FAAVLS, EUROCONTROL) non lus ; le document précise qu'un cas d'usage n'a pas vocation à remplir tous les objectifs (§F.1). Le cas de vision (Visual Landing System) tourne sur GPU COTS.
- Des extraits utiles (Chapitre D, tableaux 11 et suivants, plusieurs tableaux d'objectifs par niveau) manquent à l'extraction (voir Statut de lecture).

## Pertinence pour la thèse

Cœur du sujet « IA embarquée sécuritaire certifiable » : c'est le cadre de référence le plus concret d'une autorité de certification pour un réseau appris, mais pour l'aviation. Apports directs :
- Structure d'un dossier d'assurance à viser : ODD, exigences sur les données (DQR), jeux indépendants, vérification de stabilité et de robustesse, modèle d'inférence vérifié sur la plateforme cible (environnement #1 : constituant intégré sur la cible, §C.3.1.8.3), traçabilité, configuration.
- Le FPGA est présenté comme cible relativement couverte par la guidance existante (DO-254 / AMC 20-152A), le GPU non : argument favorable à la thèse (à sourcer : MOC IMP-05).
- Cadre d'un moniteur à l'exécution (ODD, OoD, confiance, repli passivation) : point d'entrée pour les gaps « surveillance à l'exécution » sur FPGA.
- Contraintes fortes pour les autres axes : apprentissage continu embarqué exclu à ce stade (limite pour l'axe continual-learning) ; non supervisé (autoencodeurs) limité aux niveaux de criticité les plus faibles (DAL D) ; toute quantification / pruning est un événement à justifier (LM-06, IMP-04, IMP-06).
- Cas YOLO vidéosurveillance : le CNN de détection sur images est l'exemple type (VLS, extraction de la géométrie de piste, incertitudes aléatoire et épistémique, discriminateur OoD) ; ET-03 (RGPD) et ET-05 (information sur les données personnelles enregistrées) sont pertinents pour la détection de personnes (déduit par transposition de contexte).
Ce que le document laisse ouvert : lien avec les normes IEC 61508 / ISO 13849 / ISO/IEC TR 5469, fiabilité matérielle (SEU, TMR), preuve d'équivalence après quantification sur FPGA.

## Gaps identifiés

- Aucune méthode d'assurance « learning assurance » démontrée sur un détecteur d'objets quantifié (YOLO) déployé sur FPGA : le seul cas image du document (piste d'atterrissage) est validé sur GPU COTS.
- Vérification de préservation des propriétés (IMP-06) après quantification / compilation FPGA : méthodes formelles citées comme prometteuses mais locales, pas de MOC.
- Bornes de généralisation exploitables pour de gros CNN (LM-04) : manquantes selon le document lui-même.
- Apprentissage continu / en ligne certifiable : explicitement hors périmètre (LM-02), donc question ouverte pour la thèse.
- Correspondance entre objectifs EASA et normes industrielles (IEC 61508, ISO 13849, ISO/PAS 8800) : non traitée.
- Moniteur OoD / incertitude implémenté sur FPGA avec temps de réponse borné : le document exige la fonction (EXP-05 à EXP-07) mais pas de mise en œuvre matérielle.

## Statut de lecture

papier complet : `fulltext.md` lu en entier (5326 lignes). Extraction Grobid : texte parfois désordonné (fragments de chapitres hors ordre, chapitre D et Annexes partiellement absents, en-têtes « Proprietary document » répétés). Les « tableaux sans corps extrait » de `metadata.json` (Tables 1, 2, 3, 5, 6, 7, 10, 12 à 15, 17, et des figures) n'ont pas de contenu ; en particulier le Chapitre D (tableaux de modulation des objectifs selon DAL/SWAL et niveau d'IA) est absent, donc l'applicabilité objectif par objectif selon le niveau d'assurance n'a pas été lue. Table 4 : reconstruit par PyMuPDF, chiffres à vérifier. Numérotation des sections de l'extraction parfois décalée (« Section C.x » reconstruite d'après le contexte).
Ce qui suit est déduit et non affirmé par les auteurs : la transposition au cas industriel / vidéosurveillance et à YOLO sur FPGA ; l'idée que le FPGA est « favorable » (le document dit seulement que FPGA, ASIC et COTS sont couverts par les guides existants) ; l'identification de gaps.
