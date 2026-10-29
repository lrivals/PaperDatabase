---
id: 2024-jain-design-implementation-iot-automated-ec
fiche: done
date: 2026-10-29
benchmarks: none
---

# Design and Implementation of an IoT-based automated EC and pH Control System in an NFT-based Hydroponic Farm

Swati Jain, Mandeep Kaur, 2024, Engineering, Technology & Applied Science Research 14(1), 13078–13081. https://doi.org/10.48084/etasr.6393
Type : article de journal (court, 4 pages)

## Problème

Aucune solution unique ne régule à la fois EC et pH d'une ferme NFT ; les travaux antérieurs ignorent le type d'eau (rapport TDS/EC) et le volume de la cuve (2024-jain#001.4). Objectif : un algorithme combiné, indépendant de la taille de la cuve (taille saisie dans l'application, volume courant mesuré aux ultrasons).

## Méthode

- NodeMCU (ESP8266) lisant capteurs ultrason (niveau), TDS et pH, relais commandant 4 pompes : eau, solution nutritive concentrée, pH+ et pH− (2024-jain#001.4, 2024-jain#005.2).
- EC : régulée via le TDS, TDS = X × EC avec X = 0,550 pour l'eau douce à 300–350 µS/cm ; Tableau I : X = 0,5 (eau distillée), 0,55 (eau douce), 0,55–0,75 (eau naturelle) (2024-jain#004.0). Volume courant déduit du niveau ultrason (éq. 2). TDS < borne basse → volume de nutriments éq. (3) ; TDS > borne haute → volume d'eau éq. (4), cible TT = milieu de la plage ; durée de pompe = volume / débit (éq. 5, 6) (2024-jain#004.1). Les équations ne sont pas extraites dans le texte : formes exactes `n/r` ici.
- pH : acide pH 3 et base pH 9,5, concentrés dilués 10:1 ; dose = dose recommandée constructeur × volume courant (éq. 7), durée = dose / débit de pompe (éq. 8) (2024-jain#005.0). Une seule injection calculée, pas d'impulsions répétées avec attente décrites.
- Plages idéales saisies par l'utilisateur via une application mobile (2024-jain#005.4).

## Plateforme et implémentation

NodeMCU ; capteurs ultrason, TDS, pH (modèles `n/r`) ; petit système NFT intérieur : cuve d'irrigation, 4 réservoirs et 4 pompes (2024-jain#005.2). Cuve 50 l, hauteur 50 cm, débit pompe nutriments 0,6 l/min, solution concentrée 2000 ppm (Table II, 2024-jain#011.0). Code non publié. Pas de FPGA ni de mesure de puissance.

## Résultats

- Essai de 10 jours, plage TDS 750–850 ppm, plage pH 6,0–6,5 (2024-jain#005.3, 2024-jain#005.4).
- TDS résultant moyen 801,4 ppm ; pH résultant moyen 6,26, « dans la plage » (2024-jain#005.4).
- Table II (10 mesures) : après action, TDS résultant 784–832 ppm (ex. 745 → 792 ppm, pompe nutriments 206,25 s) (2024-jain#011.0). Tableau à corps PyMuPDF/Grobid, non revérifié visuellement.
- Exemple pH : 5,93 < min → pompe base 11,45 s → pH 6,12 (2024-jain#005.2). Le Tableau III (pH) n'est pas extrait.
→ reportés dans `benchmarks.csv` : aucune ligne (régulation de procédé, pas de mesure de modèle ; `benchmarks: none`).

## Limites et critique

- Petite validation : une seule installation, 10 jours, mesures « à des moments aléatoires », aucun témoin (manuel ou PID), pas d'écart-type ni de temps de réponse.
- Les mesures semblent prises après dosage ; rien sur le temps de mélange ni sur le délai avant relecture.
- Aucune discussion de dérive/étalonnage des sondes pH et TDS, de compensation en température, ni de sécurité (dosage excessif, panne de capteur, plafonds de durée de pompe) : `n/r` dans l'article.
- Contrôle en boucle ouverte sur la dose calculée (modèle de dilution parfait), sans rebouclage décrit.
- Aucune mesure de rendement de plante.

## Pour SerreIA

- Fichiers concernés : `edge/controller/rules.py` (`ph`, `ec`, `_dose_ready`), `edge/controller/serre.yaml` (pompes : impulsion 2 s pH−, 3 s nutriments, mélange 600/900 s), `edge/controller/recettes.yaml`, firmware `firmware/src/solution/main.cpp` (EZO-EC I²C, DS18B20 pour compensation de température).
- Comparaison (déduit de la lecture du code SerreIA, pas affirmé par les auteurs) : SerreIA dose par impulsions fixes puis attend le mélange et une nouvelle mesure avant la suivante (`_dose_ready`) ; Jain & Kaur calculent une dose unique proportionnelle à l'écart et au volume, donc plus rapide mais sans garde-fou de mélange ni de plafond. Garder les impulsions : l'approche du papier n'est pas validée pour la sécurité.
- Idée reprenable : dimensionner la durée d'impulsion selon le volume de cuve (niveau ultrason) et le débit de pompe (durée = dose / débit), plafonnée par `duree_max_s`, pour que la même règle serve des cuves de tailles différentes (2024-jain#004.1, 2024-jain#005.0). À tester dans `sim/`.
- Cible EC : le papier vise le milieu de la plage (TT = 800 ppm) ; SerreIA agit aux bornes. Option : viser le milieu pour réduire les oscillations.
- Correction par l'eau claire quand EC > max : le papier la déclenche automatiquement (pompe d'eau) alors que SerreIA ne fait qu'alerter (`ec.nutriments`) ; piste, derrière validation humaine (2024-jain#011.0).
- Conversion TDS/EC : X dépend de l'eau (0,5 à 0,75, Tableau I, 2024-jain#004.0) ; SerreIA lit l'EC directement (EZO-EC), donc inutile, mais piège si l'on compare à des consignes en ppm (800 ppm ≈ 1,45 mS/cm avec X = 0,55, calcul déduit).
- Métrique de validation proposée : fraction du temps dans la plage pH/EC, nombre d'impulsions par jour, dépassement après dosage (le papier ne rapporte que les moyennes).
- Pièges : étalonnage et dérive des sondes non traités ici ; ne pas conclure que l'algorithme est robuste.

## Gaps identifiés

- Étalonnage et dérive des sondes pH/EC, et leur effet sur le dosage automatique (non traité).
- Comparaison dosage proportionnel vs impulsions vs PID/flou sur mêmes conditions.

## Statut de lecture

papier complet (4 pages, `fulltext.md` lu entièrement ; extraction grobid ; équations 1 à 8 et Tableau III non extraits).
Déduit et non affirmé par les auteurs : comparaison avec le code SerreIA, conversion ppm → mS/cm, remarques sur l'absence de témoin et de rebouclage.
