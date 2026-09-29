---
id: 2012-nectoux-pronostia-experimental-platform-bearings-accelerated
fiche: done
date: 2026-09-29
benchmarks: none
---

# PRONOSTIA: An Experimental Platform for Bearings Accelerated Degradation Tests

Patrick Nectoux, Rafael Gouriveau, Kamal Medjaher, Emmanuel Ramasso, Bechir Chebel-Morello, Noureddine Zerhouni, Christophe Varnier, 2012, IEEE International Conference on Prognostics and Health Management (PHM). DOI : n/r
Type : conférence (IEEE PHM 2012) — article de jeu de données

## Problème

Tester des méthodes de pronostic demande des données de dégradation réelles jusqu'à la panne, qui
exigent des essais accélérés ; peu de plateformes publient leurs données (§I, §II). Les bancs de
roulements existants utilisent souvent des défauts initiés artificiellement (électroérosion).

## Méthode

Ce que l'article **définit** :

- **Banc PRONOSTIA** (FEMTO-ST, département AS2M, Besançon) pour dégrader des roulements à billes
  jusqu'à la panne **en quelques heures** (§III) :
  - partie rotative : moteur asynchrone de 250 W et réducteur, vitesse d'arbre < 2000 tr/min ;
  - charge radiale par vérin pneumatique amplifiée par un bras de levier, jusqu'à la charge
    dynamique maximale du roulement (4000 N) (§III-B) ;
  - mesures : force radiale, vitesse et couple à 100 Hz ; **deux accéléromètres** (horizontal et
    vertical, à 90°) à **25,6 kHz** ; sonde de température PT100 à 10 Hz ; acquisition LabVIEW
    (§III-C).
- Dégradation « naturelle » : aucun défaut initié, et un roulement dégradé présente souvent
  plusieurs types de défauts à la fois (billes, bagues, cage) (§II-B).
- **Challenge IEEE PHM 2012** (§V) : 3 conditions opératoires (1800 tr/min et 4000 N ;
  1650 tr/min et 4200 N ; 1500 tr/min et 5000 N) ; **6 roulements** d'apprentissage menés jusqu'à la
  panne (2 par condition) et **11 roulements de test** tronqués dont il faut prédire la RUL (Table I) ;
  durées de vie de 1 h à 7 h.
- **Score** : erreur en pourcentage %Er = 100 × (RUL réelle − RUL estimée)/RUL réelle ; précision
  Aᵢ = exp(−ln 0,5 · Er/5) si Er ≤ 0 (prédiction tardive, pénalisée plus fort) et
  exp(+ln 0,5 · Er/20) si Er > 0 ; score final = moyenne sur les 11 roulements (Eq. 1-3).

## Plateforme et implémentation

Banc physique ; données publiées sur le site du challenge (URL FEMTO-ST citée en §V-C, à vérifier,
le lien d'origine pouvant avoir changé).

## Résultats

Observations qualitatives sur les données (§IV) : certaines dégradations sont monotones et
prévisibles (PSD, facteur K ; Fig. 8-9), d'autres **brutales** (Fig. 10-11) ; le bruit varie selon
les essais ; les signatures fréquentielles théoriques (BPFI, BPFO) et la loi L10 ne correspondent
pas aux durées observées (§IV-D). Aucune ligne dans `benchmarks.csv`, conformément au profil pour
les papiers de jeux de données (`benchmarks: none`).

## Limites et critique

- Très peu d'essais d'apprentissage (6) pour une dispersion de durées de vie de 1 à 7 h : RUL très
  difficile à estimer (reconnu en §V-B).
- Conditions constantes pendant chaque essai ; la variation en ligne des conditions n'est
  qu'annoncée en perspective (§VI).
- La troisième condition (5000 N) dépasse la charge dynamique maximale de 4000 N citée en §III-B :
  accélération extrême, représentativité industrielle discutable (déduit).
- Pas de DOI dans les métadonnées ; lien de téléchargement d'origine susceptible d'être périmé.
- Aucune caractérisation chiffrée des données (nombre de fichiers, durées exactes) dans le texte.

## Pertinence pour la thèse

Article de référence du jeu **PRONOSTIA / FEMTO** (roulements, vibrations à 25,6 kHz), à citer pour
toute expérience de pronostic de roulements. Les trois conditions opératoires fournissent un
découpage naturel en tâches pour un scénario de CL par changement de régime (domaine incrémental),
et la dégradation brutale de certains roulements est un cas type de dérive abrupte (déduit). La
fréquence d'échantillonnage (25,6 kHz) et la taille des fenêtres imposent un prétraitement
(features, PSD) avant tout modèle embarqué (déduit).

## Gaps identifiés

- Pas de scénario de conditions variables au sein d'un même essai (§VI).
- Pas de protocole standard de CL entre conditions opératoires sur PRONOSTIA.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Table I partiellement fusionnée (répartition des
roulements de test reconstituée : 11 au total selon §V-B) ; figures non disponibles.
Déduit et non affirmé par les auteurs : dépassement de charge en condition 3, usage en scénario CL,
contraintes de prétraitement embarqué.
