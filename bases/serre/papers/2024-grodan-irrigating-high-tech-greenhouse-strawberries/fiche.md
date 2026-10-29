---
id: 2024-grodan-irrigating-high-tech-greenhouse-strawberries
fiche: done
date: 2026-10-29
benchmarks: none
---

# Irrigating high-tech greenhouse grown strawberries (whitepaper)

Grodan (ROCKWOOL), 2024 (mars), livre blanc industriel, sans DOI ni URL dans `metadata.json`.
Type : rapport / littérature grise **d'un fabricant de laine de roche**, non relu par les pairs ;
les essais cités (Wageningen University Research 2022, Delphy ISFC 2022) ne sont pas détaillés.

## Problème

Transposer à la fraise hors-sol sous serre (propagation puis culture sur dalle) la logique de
pilotage de l'irrigation de la tomate : déclencher l'irrigation sur la teneur en eau du substrat
(WC %) et piloter l'EC, plutôt que sur un calendrier (000.0, 004.0).

## Méthode

Principes affichés : consignes d'irrigation qui tiennent compte de la météo ; le drainage est un
résultat, non un but ; EC du substrat la plus basse quand le rayonnement est maximal ; stabilité
de WC % et EC d'un jour à l'autre ; pilotage génératif/végétatif (004.0). Suivi par sonde GroSens
(WC %, EC, température du substrat) dans le bloc puis dans la dalle (003.0). Propagation :
irrigation par marée (ebb-flood), qui garde les collets secs (réduit Phytophthora) (001.0).

## Plateforme et implémentation

Capteur GroSens (propriétaire Grodan), substrat laine de roche Grodan (blocs + dalles), cv Favori
dans les essais (figures, 006.0). Pas de code ni de données publiés.

## Résultats

Aucun résultat quantifié comparatif : seulement des consignes et deux courbes illustratives sur 7 jours
(Fig. 1, 2) montrant WC % et EC stables (006.0, 008.0). Tableau 1 (plages génératif/végétatif,
tomate/fraise) : **corps non extrait** (légende seule, 009.0) ; ses valeurs sont inconnues.
→ reportés dans `benchmarks.csv` : aucune ligne (pas de mesure de modèle ; `benchmarks: none`).

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| fraise | propagation (blocs) | EC de la solution de saturation | n/r | 1,0 à 4,0 (plage essayée) | mS/cm | blocs saturés à la transplantation, EC variable pour piloter le développement | 2024-grodan#001.0 |
| fraise | propagation (blocs) | WC % déclenchant l'irrigation | n/r | « minimal (60 %) or maximum (40 %) » | % | irrigation suivante retardée jusqu'à ce que WC % atteigne la cible ; libellé du papier incohérent (min 60 > max 40) | 2024-grodan#001.0 |
| fraise | propagation (blocs) | WC % après irrigation | ≈ 85 | n/r | % | chaque irrigation re-sature le bloc, puis baisse lente | 2024-grodan#001.0 |
| fraise | culture (dalle) | WC %, EC, temp. du substrat | n/r | n/r | n/r | stables sur 7 j ; valeurs du Tableau 1 non extraites | 2024-grodan#009.0 |
| fraise | tous | EC du substrat vs rayonnement | EC minimale au rayonnement maximal (qualitatif) | n/r | n/r | principe de pilotage | 2024-grodan#004.0 |

Écart avec SerreIA : `recettes.yaml` ne contient pas la fraise (tomate, laitue, basilic) ; seuls
les emplacements en substrat ont `humidite_sol` (tomate 40-75 %, sondes capacitives), sans équivalence
démontrée avec le WC % d'une sonde laine de roche (étalonnage et substrat différents). Le papier ne
donne aucune plage fraise exploitable (Tableau 1 manquant) : pas de recette fraise à en tirer.

## Pour SerreIA (méthode, à titre d'idée)

- Logique à reprendre : déclenchement de l'irrigation sur seuil de teneur en eau (type hystérésis
  bas/haut), re-saturation puis décroissance, plutôt que sur horloge (001.0) ; `rules.py` /
  `recettes.yaml` (`humidite_sol`).
- Principe EC bas quand le rayonnement est haut (004.0) : règle candidate pour la zone hydro,
  à valider en simulation (`sim/`), pas en dur.
- Piège : une sonde de WC % n'est pas transférable entre substrats ; valeurs du livre blanc propres à
  la laine de roche Grodan et à son capteur. Source commerciale, à recouper avec de la littérature
  évaluée avant d'écrire une recette fraise.

## Limites et critique

Source industrielle avec intérêt commercial (affirmations « 50 % d'eau en moins » etc., 005.0, non
étayées ici). Aucune méthodologie d'essai, aucun rendement chiffré malgré « dramatic improvements in
yield » (002.0). Texte extrait lacunaire (phrases coupées, « Thankfully there is another way of
thinking »), Tableau 1 absent. Les seuils WC % sont contradictoires dans le libellé.

## Pertinence pour la thèse

Pertinence limitée et indirecte pour SerreIA : confirme la stratégie WC %/EC pour fraise et tomate
sur substrat, mais sans valeurs de consigne fiables. Axes : climate-control, crop-practices.

## Gaps identifiés

Consignes fraise (WC %, EC, pH par stade) issues de sources évaluées ; correspondance WC % laine
de roche / `humidite_sol` des sondes capacitives.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction grobid ok). Tableau 1 sans corps extrait :
valeurs manquantes. Déduit, non affirmé par le papier : l'écart avec SerreIA, la règle EC/rayonnement
comme règle de contrôleur, l'inversion probable min/max des seuils WC %.
