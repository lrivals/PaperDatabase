---
id: 2021-nikolaou-energy-water-related-parameters-tomato
fiche: done
date: 2026-10-29
benchmarks: none
---

# Energy and Water Related Parameters in Tomato and Cucumber Greenhouse Crops in Semiarid Mediterranean Regions. A Review, Part II: Irrigation and Fertigation

Georgios Nikolaou, Damianos Neocleous, Anastasis Christou, Polycarpos Polycarpou, Evangelini Kitta, Nikolaos Katsoulas, 2021, Horticulturae 7(12):548 (venue déduite du DOI, `metadata.json` la porte à `null`). https://doi.org/10.3390/horticulturae7120548
Type : article de synthèse (review) en revue ; relecture par les pairs non vérifiée ici.

## Problème

Les recettes d'irrigation et de fertigation de la littérature viennent du nord de l'Europe et conviennent mal aux serres méditerranéennes semi-arides ; les auteurs font le point sur la gestion de l'eau et des nutriments pour tomate et concombre (abstract, #000.0).

## Méthode

Revue narrative (pas de protocole de recherche décrit) : programmation de l'irrigation (minuterie, impulsions, boucle fermée, ET par Penman-Monteith, bac Classe A), qualité de l'eau et salinité (FAO), eaux non conventionnelles, fertigation en sol (bilan NF = (NR - SC + SM)100/UE) et hors-sol (solutions nutritives, Tables 9 et 10).

## Plateforme et implémentation

Sans objet (revue). Aucun code ni bitstream.

## Résultats

Chiffres utiles, tous rapportés d'autres travaux cités par la revue :
- EC de la solution nutritive tomate hors-sol, Europe du Nord : 2,60 dS/m (A) et 1,6 (B), pH 5,6 (Table 9, #026.0).
- EC de la solution nutritive tomate, climat méditerranéen, par stade I à V : 2,80 / 2,50 / 2,40 / 2,40 / 2,30 dS/m, pH 5,6 à tous les stades (Table 10, #027.0). Stades : I = solution de départ, II à V = grappes florales 1-3, 3-5, 5-10, >10 (légende de Fig., #018.0).
- Régulation en boucle fermée sur l'EC du drainage maintenue à 3 ± 0,8 dS/m, tomate (Neto et al., §2, #002.1).
- Fréquence : sur laine de roche, 5 à 6 arrosages par heure, jusqu'à 30 par jour en été méditerranéen ; fréquence plus élevée avec de plus petites doses recommandée en perlite (§2, #004.1, #004.2).
- Hors-sol ouvert méditerranéen : 30 à 35 % de la solution drainée (§5.2, #012.1).
- Salinité (FAO) : seuil sans perte de rendement tomate 1,7 dS/m en eau (ECw) et 2,5 en extrait de saturation (ECe) (Table 5, #024.0, corps du tableau mal aligné, seule la colonne 100 % est lue). En hors-sol, une eau jusqu'à 4,0 dS/m a eu un effet positif sur photosynthèse, croissance et goût (§3, #005.2). Limites EC de l'eau d'apport : 1,0 dS/m (drain ouvert), <0,5 (semi-fermé ou fermé) (§3, #005.3).
- Économies de 30 à 80 % d'eau et de nutriments sur tomate hors-sol avec plateforme edge/cloud (Zamora-Izquierdo et al., §2, #002.1).
- ET tomate sous serre à Chypre : 743 mm/cycle (Table 1, #020.0) ; 557 mm à Almería, cycle automne-printemps (§2, #002.2). Cycle usuel : 34 semaines tomate (§2, #002.2).
→ reportés dans `benchmarks.csv` : aucune ligne (revue, pas de mesure de modèle).

## Limites et critique

- Revue narrative : valeurs de seconde main, sans méthode de sélection ; les conditions (cultivar, substrat, climat) manquent souvent.
- Table 2 sans corps extrait ; Table 4 (WUE) largement vide et Table 5 mal alignée dans l'extraction : ne pas s'en servir sans l'image du tableau.
- Les EC de Tables 9 et 10 sont celles de la solution nutritive apportée, pas de la zone racinaire ni du drainage : ne pas les comparer directement à une plage « optimale » de substrat.
- Aucune consigne de déclenchement de l'irrigation chiffrée (seuil de teneur en eau du substrat, drainage cible en %, VPD) en dehors de la fréquence sur laine de roche et du drainage 30-35 % observé.
- Les recettes sont pour tomate et concombre ; rien sur laitue, basilic, fraise.

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| tomate | I (solution de départ) | EC solution nutritive | 2,80 | n/r | dS/m | hors-sol, climat méditerranéen | 2021-nikolaou#027.0 |
| tomate | II (grappes 1-3) | EC solution nutritive | 2,50 | n/r | dS/m | idem | 2021-nikolaou#027.0 |
| tomate | III (grappes 3-5) | EC solution nutritive | 2,40 | n/r | dS/m | idem | 2021-nikolaou#027.0 |
| tomate | IV (grappes 5-10) | EC solution nutritive | 2,40 | n/r | dS/m | idem | 2021-nikolaou#027.0 |
| tomate | V (grappes >10) | EC solution nutritive | 2,30 | n/r | dS/m | idem | 2021-nikolaou#027.0 |
| tomate | tous (Europe du Nord) | EC solution nutritive | 2,60 (A) ; 1,6 (B) | n/r | dS/m | hors-sol, systèmes ouvert (A) et fermé (B) du Nord ; A et B non définis dans l'extrait lu | 2021-nikolaou#026.0 |
| tomate | tous | pH solution nutritive | 5,6 | n/r | - | hors-sol, Tables 9 et 10 | 2021-nikolaou#027.0 |
| tomate | tous | EC du drainage (consigne de boucle fermée) | 3 | ± 0,8 | dS/m | régulation citée de Neto et al. | 2021-nikolaou#002.1 |
| tomate | tous | EC eau d'apport / extrait de saturation sans perte de rendement | ECw 1,7 ; ECe 2,5 | n/r | dS/m | FAO, culture en sol | 2021-nikolaou#024.0 |
| tomate | tous | EC eau d'apport (limite) | n/r | 1,0 (drain ouvert) ; <0,5 (semi-fermé/fermé) | dS/m | limite d'EC de l'eau brute | 2021-nikolaou#005.3 |
| tomate | tous | fréquence d'irrigation | n/r | 5-6 par heure, jusqu'à 30 par jour | arrosages | laine de roche, été méditerranéen | 2021-nikolaou#004.1 |
| tomate | tous | fraction drainée | n/r | 30-35 | % de la solution apportée | hors-sol ouvert, constat méditerranéen | 2021-nikolaou#012.1 |
| tomate | tous | humidité du substrat, pH, T, HR | n/r | n/r | n/r | non traités par l'article | - |

**Écart avec SerreIA** (`edge/controller/recettes.yaml`, tomate-standard) : pH 5,8-6,3 contre 5,6 dans les deux tables (écart de 0,2 à 0,7, à justifier ou à abaisser). EC : croissance 2,0-3,0, floraison et fructification 2,5-3,5. Les tables de l'article donnent, pour la solution apportée, 2,3 à 2,8 dS/m en climat méditerranéen, avec une EC qui **décroît** avec le stade (2,80 vers 2,30), et 1,6 à 2,6 en Europe du Nord. SerreIA monte au contraire l'EC en floraison-fructification, et sa borne haute 3,5 dépasse toute valeur de solution des Tables 9 et 10 ; elle ne se retrouve que dans la fenêtre du drainage (3 ± 0,8 = 2,2 à 3,8, #002.1).

**Trancher l'EC tomate (jugement déduit, non affirmé par les auteurs).** Cet article ne cite pas le guide UF/IFAS et ne contient pas la plage 0,8-2,0 ; il ne permet donc pas de la juger directement. Ce qu'il établit : (1) une EC de solution de 2,3-2,8 est la pratique méditerranéenne en hors-sol, ce qui est au-dessus de 0,8-2,0 et dans la partie basse de 2,0-3,5 ; (2) la consigne 3,5 n'a pas de support pour la solution apportée, mais s'accorde avec un drainage visé à 3 ± 0,8 ; (3) en sol (ECe seuil 2,5), des EC élevées coûtent du rendement (#024.0). Proposition : distinguer dans `recettes.yaml` l'EC de la solution apportée (2,3-2,8, décroissante après la grappe 1) de l'EC du drainage ou du substrat (jusqu'à 3,8), et ne pas utiliser 3,5 comme borne de solution. La plage 0,8-2,0 reste à confronter à la source UF/IFAS (pas dans cette base) : elle correspond plutôt au bas de l'échelle du Nord (1,6, Table 9 B).

Pour le contrôleur : l'article soutient des arrosages fréquents en petites doses plutôt qu'un arrosage unique en fin de cycle de séchage (#004.2, #002.0), et le suivi du drainage (EC) comme boucle de rétroaction (#002.1). Piège : l'ET ne se transpose pas d'un site à l'autre (743 mm à Chypre contre 557 mm à Almería, #020.0, #002.2).

## Gaps identifiés

- Consigne de déclenchement de l'irrigation chiffrée (teneur en eau du substrat, drainage cible en %) absente de l'article.
- Aucune consigne de laitue, basilic ou fraise ; EC à trancher avec une source dédiée (UF/IFAS, Sonneveld et Voogt cité [77] non présent dans la base).

## Statut de lecture

Sections lues par recherche ciblée et lecture partielle de `fulltext.md` (§1 à §6, Tables 1, 2, 5, 7, 9, 10) ; non intégral au sens strict (tableaux 3, 4, 6, 8 non exploités). Le tableau 2 est sans corps extrait ; Tables 4 et 5 mal alignées.
Déduit et non affirmé par les auteurs : le jugement sur l'EC de SerreIA, la comparaison avec 0,8-2,0 (non présent dans l'article), le caractère « décroissant » comme tendance de recette (lue sur Table 10), la lecture de la colonne 100 % de Table 5.
