# Veille communauté — dépôts du canal « show and tell » (Discord Vesuvius Challenge)

Mis à jour le 2026-11-17. Les dépôts ci-dessous sont **ingérés dans le corpus** (type
`repo`, sauf Rectina : article de 17 pages hébergé sur GitHub, type `preprint`). Pour
chaque dépôt, le PDF ingéré est le README et les documents techniques principaux, rendus au
commit indiqué dans le bandeau du PDF (images omises). Tout est **non relu par les pairs et
auto-déclaré**. Fiche, chiffres et passages : `papers/<id>/fiche.md`, `bin/pdb bench --paper <id>`,
`bin/pdb search "…" --paper <id>`.

Extraction : PyMuPDF (`ok: false`). Les corps des tableaux markdown sont souvent aplatis,
donc les lignes de `benchmarks.csv` viennent surtout de la prose (`confidence: medium`).

Non consulté : <https://journal.vesuvius.alive.monster/>, refusé par le réseau de la session
cloud (proxy 403).

## Dépôts

| paper_id | Dépôt (commit) | Étape | Résultat principal (auto-déclaré) | Réserve majeure |
|---|---|---|---|---|
| `2026-nexusai-kevin-vesuvius-ink-bench-volumetric-ink` | [nexusai-kevin/vesuvius-ink-bench](https://github.com/nexusai-kevin/vesuvius-ink-bench) (6bd16ff) | encre volumique 2,4 µm, inférence basse VRAM | AUC 0,9546 PHercParis4 ; 83 M voxels/s, ~2,5 Gio (RTX 5080) | seuil optimal choisi sur les labels d'évaluation ; une ROI ; fuite possible |
| `2026-ruiconte-ink-swarm-argus-v1-v2` | [ruiconte/ink-swarm](https://github.com/ruiconte/ink-swarm) (d38015a) | encre `ink_9um`, Argus V1/V2 | V2 : AUC 0,928 vs 0,922 Reader V3 (PHerc0841 natif, 3 fenêtres) | écarts minces, pas d'IC ; V2 moins bon sur masques officiels |
| `2026-pellerano-rectina-m3-m4-dense-ink` | [evilaliv3/…/db27c806-rectina](https://github.com/evilaliv3/vesuvius-challenge-pipeline/tree/7cb4e44/results/db27c806-rectina) (7cb4e44) | encre dense, Rectina m3/m4 | m4 : AUC moy. 0,8637 vs 0,8547 Reader v3 (8 unités) ; > v3 sur 10/14 | une graine, pas d'ablation ; gain sous le bruit annoncé (0,013) |
| `2026-snyder-scroll-label-snap-snapping-approximate` | [aqsnyder/scroll-label-snap](https://github.com/aqsnyder/scroll-label-snap) (e03c4c0) | qualité des labels de surface (snapping) | géométrie : 90 % de préférence ; **encre : original préféré 75 vs 31** (pré-enregistré) | résultat négatif sur l'encre ; test de dérive circulaire |
| `2026-de-vore-vesuvius-ply-layers-separating-pressed` | [Victoria-TechNexus/vesuvius-ply-layers](https://github.com/Victoria-TechNexus/vesuvius-ply-layers) (9267573) | séparation des couches pressées par plis recto/verso | 99,6 % sur papyrus vs 82,0 % (segment officiel) | métrique de brillance favorable ; une couche, Paris 4 |
| `2026-betka-herculex-virtual-unwrapping-whole-herculaneum` | [adambetka2/HerculeX](https://github.com/adambetka2/HerculeX) (eace0b2) | chaîne complète, enroulement par optimisation entière | 8 rouleaux, 69 290 cm² ; ~2 h CT → feuillet (M1 Pro) | aucune vérification de spire sur les 8 rouleaux |
| `2026-limegs-winding-field-continuous-winding-coordinate` | [LimeGS/winding-field](https://github.com/LimeGS/winding-field) (1e27244) | champ continu de numéro d'enroulement + banc gelé | dérive intrafibre 0,155 feuillet (0,5–1,5 mm) → 1,336 (30–45 mm) | couverture 36,8 % ; décompte physique non démontré |
| `2026-gilman-spiral-fit-inputs-first-windings` | [Ahggggg/spiral-tracks-four-scrolls](https://github.com/Ahggggg/spiral-tracks-four-scrolls) (b6062e1) | entrées de spiral fit pour 4 rouleaux | fit de 8 000 pas sur 1203/1218/1545/0846B, 4,34 USD ; snap 89–100 % | aucune lettre ; snap = cohérence avec m7, pas exactitude |
| `2026-gilman-first-letters-clean-sheets-173` | [Ahggggg/first-letters-clean-sheets](https://github.com/Ahggggg/first-letters-clean-sheets) (978e8d5) | 173 patchs mono-feuille sur 13 rouleaux | 355 cm², tracés sur portable ; aucune lettre | monocouche non prouvée ; score on-sheet AUC 0,875 |
| `2026-de-meij-pherc-0306b-winding-w040-row` | [daviddemeij/pherc0306b-partial-letters-w040](https://github.com/daviddemeij/pherc0306b-partial-letters-w040) (9aee0e6) | lettres trouvées, PHerc. 0306B w040 | 5 lettres (χ, θ sûres ; π, λ, γ incertaines), reconstruction ScrollFiesta indépendante | labels posés sur les cartes du modèle ; pas de métrique |

## Lecture transversale (déduit)

- **Encre.** Trois nouveaux lecteurs (Argus, Rectina m3/m4, banc ink-bench) annoncent des
  gains sur Reader V3 de l'ordre de 0,005–0,01 AUC, sans intervalle de confiance, sur des
  unités, résolutions et labels différents : **non comparables entre eux** ni avec
  arxiv-2603.27698 / arxiv-2308.05070. Deux contrôles à reprendre : l'ordre de profondeur
  inversé (AUC → 0,5 attendu, ink-swarm) et la face aveugle (de Meij).
- **Résultat négatif utile.** Le snapping améliore la géométrie des labels mais dégrade
  la lisibilité de l'encre (test pré-enregistré, scroll-label-snap).
- **Géométrie sans vérité terrain.** HerculeX, winding-field, spiral-tracks et
  first-letters produisent beaucoup de surface sur des rouleaux sans maillage publié, mais
  aucun ne sait mesurer la « bonne spire » hors des 3–4 rouleaux de référence : gap à
  reporter dans `gaps.md`.
- **Lettres.** Seul le dépôt de Meij revendique des lettres (PHerc. 0306B w040) ; les 12
  enroulements de spiral-tracks et les 355 cm² de first-letters n'en montrent aucune.
