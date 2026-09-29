---
id: 2018-halme-review-vision-safety-systems-human
fiche: done
date: 2026-09-29
---

# Review of vision-based safety systems for human-robot collaboration

Roni-Jussi Halme, Minna Lanz, Joni Kämäräinen, Roel Pieters, Jyrki Latokartano, Antti Hietanen, 2018, Procedia CIRP 72, 111-116. DOI 10.1016/j.procir.2018.03.043
Type : article de journal (Procedia CIRP, actes de conférence CIRP CMS 2018 à ma connaissance, non affirmé par le texte).

## Problème

Les systèmes de sécurité par vision pour la collaboration humain-robot (HRC) sont peu standardisés et peu présents dans le commerce (SafetyEYE est cité comme le plus courant, §1). Les auteurs évaluent la maturité industrielle des méthodes selon la flexibilité d'usage, la vitesse du système et le niveau de collaboration (Résumé).

## Méthode

Revue de littérature narrative (méthode de sélection des articles n/r). Cadre normatif : ISO 10218-1/2 et ISO/TS 15066, avec les quatre modes collaboratifs (arrêt contrôlé de sécurité, guidage manuel, surveillance de vitesse et de séparation, limitation de puissance et de force) (§2). Taxonomie de Bdiwi et al. en 4 niveaux d'interaction et fonctions de sécurité associées, utilisée pour classer 15 méthodes (§2, Table 1). Sections thématiques : distance points-obstacles, évitement de collision, reconnaissance d'intention, fusion de capteurs, visualisation des zones de sécurité (§3).

## Plateforme et implémentation

Sans objet (revue). Aucune plateforme matérielle FPGA ; capteurs cités : Kinect/RGB-D, TOF, stéréo, caméras 2D, projecteurs (Table 1). Latences citées ponctuellement (distance à ≈ 300 Hz par Flacco et al., suivi à 30 Hz par Morato et al., contrôle des lignes projetées à ≈ 50 Hz par Vogel et al., §3), toutes rapportées de travaux cités, non mesurées ici.

## Résultats

- Table 1 : 15 méthodes, avec capteur, fonction de sécurité, état de zone du robot, distance de séparation, présence d'une application industrielle démontrée. Seul SafetyEYE est commercial et certifié (Table 1).
- Défis identifiés : occultations (réduites par multi-capteurs/fusion), sensibilité des caméras 2D à la lumière et à la poussière, collision surveillée seulement au niveau de l'outil, latences de perception et inertie du robot non traitées (§4).
- Constat : peu de vrais scénarios collaboratifs, environnements construits et statiques (§5).
- Survey : pas de ligne dans `benchmarks.csv` (aucune mesure propre des auteurs).

## Limites et critique

- Revue courte (6 pages), datée de 2018 : antérieure aux détecteurs profonds (YOLO) et aux normes plus récentes ; aucun détecteur de personnes appris n'est évalué (Kinect/skeleton et zones plutôt).
- Aucune méthode de sélection, pas de critères quantitatifs (précision de détection, taux de fausse alarme, latence de bout en bout comparables).
- Aucun lien à des niveaux d'intégrité de sécurité (SIL, PL) ni à la certification d'un module de vision, hormis la mention de SafetyEYE ; les normes de sûreté fonctionnelle générales (IEC 61508, ISO 13849) ne sont pas discutées.
- Contexte robot collaboratif en atelier, pas surveillance de personnes dans un secteur industriel dangereux avec caméras fixes.

## Pertinence pour la thèse

Donne le cadre normatif et fonctionnel du cas d'application (détection de personnes en zone industrielle, fonctions de sécurité : arrêt, zones, distance de séparation) et les exigences à faire porter à un détecteur : temps de réaction, occultations, fiabilité en poussière/lumière. Utile pour formuler les exigences de sûreté du YOLO embarqué ; ne traite pas FPGA ni certification de l'IA.

## Gaps identifiés

- Aucun détecteur de personnes appris (type YOLO) validé selon un niveau de sûreté dans ces systèmes de vision ; les solutions certifiées (SafetyEYE) sont propriétaires, à capteurs 3D dédiés.
- Latence de bout en bout et occultation non caractérisées de façon comparable.
- Liaison entre exigences ISO 10218 / TS 15066 et exigences sur un réseau de neurones à établir.

## Statut de lecture

Papier complet (fulltext.md lu en entier, dont Table 1 mise en page approximative). Déduit et non affirmé par les auteurs : type de venue (Procedia CIRP, `metadata.json` dit `journal`), absence de discussion des normes générales de sûreté fonctionnelle, comparaison avec l'état de l'art actuel.
