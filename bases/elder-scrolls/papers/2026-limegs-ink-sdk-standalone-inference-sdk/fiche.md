---
id: 2026-limegs-ink-sdk-standalone-inference-sdk
fiche: done
date: 2026-11-17
benchmarks: none
---

# ink-sdk: standalone inference SDK for Vesuvius ink-detection models with receipts and a liveness gate

LimeGS, 2026, GitHub (commit 19d39cbea8, 2026-11-17). https://github.com/LimeGS/ink-sdk/tree/19d39cbea85bca74a30e496b0488575f55f6d88d
Type : dépôt GitHub communautaire du Vesuvius Challenge (`repo`), non relu par les pairs ; contenu auto-déclaré par l'auteur (README.md + document de conception `docs/superpowers/specs/2026-10-23-ink-sdk-design.md`, en espagnol). Pas de DOI ni d'arXiv. Même auteur que `2026-limegs-winding-field-continuous-winding-coordinate`.

## Problème

Les lecteurs d'encre du Vesuvius Challenge (Reader v2/v3, Argus, Rectina, TRACE, Hecate, TimeSformer, Studio…) ont chacun leur runner, leur normalisation, leur échelle d'entrée et leur sens de lecture de la pile de couches ; les faire tourner sur un segment arbitraire est source d'erreurs silencieuses. Le document de conception cite un cas : le même checkpoint canonique 2,4 µm donne r = 0,079 contre la carte communautaire avec un runner générique (clip 0-200 / 200, rééchantillonnage en profondeur), contre r = 0,885 avec son propre runner (design §4, `#006.0`). Le dépôt vise donc une interface commune (entrée, sortie, traçabilité) sans uniformiser le prétraitement, et une preuve explicite qu'une carte n'est pas vide (README, design §1, §4).

## Méthode

Pas de nouveau modèle : un SDK d'inférence seule (« No training, fine-tuning, OCR or scientific evaluation », README, `#000.0`). Principes (design §4-§6, §11) :

- **Profils de modèles** (TOML, un par checkpoint, digest sha256 obligatoire : sans digest, pas de run) et **adaptateurs par recette** (ink9um, canonical2um, hecate ; plus v8in, studio, timesformer ajoutés dans le README). Le prétraitement reste celui de chaque recette (« estandarizar la interfaz, nunca el preprocesamiento », `#006.0`).
- **Profils listés au README** (`#000.2`, `#000.3`) : famille `ink_9um` à 17 couches (seeds 42/43 du modèle public, Reader v2, Reader v3, Argus V2 = Reader v3 affiné sur scans natifs, dense-native, TRACE v3B, Rectina m4), toutes lues dans les deux sens de profondeur ; `canonical_2um` (62 couches, 2,399 ± 0,05 µm, sens avant seul) ; Hecate 2,4 et 9,6 µm (64 et 16 couches, sortie 2D ou 3D) ; TimeSformer (26 couches, transfert « expérimental ») ; v8-in et trois graines A-hn (24 couches) ; Studio (U-Net 3D résiduel de 223 M de paramètres, 16 plans, tuilage pas 64 + fenêtre de Hann, carte primaire inversée, `#001.0`).
- **Entrées** : soit un volume de surface déjà rendu, soit un maillage tifxyz + CT OME-Zarr local rendu par `vc_render_tifxyz` (VC3D / volume-cartographer), à l'échelle native puis mise à l'échelle par pooling par axe (2,4 → 9,6 µm) ; rééchantillonnage XY de 8,64 vers 9,36 µm seulement avec un drapeau explicite (design §6.1.1, §7.2, `#017.1`). Les échelles incompatibles sont rejetées avant chargement des poids (9,6 vers 2,4 jamais ; Hecate 9,6 refuse 9,362 µm car 2,48 % > 2 %).
- **Ordre de profondeur** : le modèle peut lire la pile dans les deux sens ; le SDK écrit `forward`, `reverse` et `mean`, la carte primaire étant `forward` par défaut. README : le même modèle (Reader v3) « voit les lettres dans un ordre de profondeur et est aveugle dans l'autre, et les deux cartes passent la liveness gate » (`#000.0`) : la porte ne détecte donc pas un mauvais sens de lecture. Sans ombilic, le sens de normale vient de l'heuristique de centroïde du renderer et le reçu marque `reading_orientation=unverified` (design §6.1.1).
- **Liveness gate** (design §11, `#022.1`) : seuils portés de `lane_liveness.py` de Campaign X, évalués par carte : p99 − p50 >= 0,05 ; écart-type >= 0,02 ; fraction des pixels à moins de 0,05 de 0,5 <= 0,90 ; verdict EMPTY s'il n'y a aucun pixel valide  ; DEGENERATE (déduit : seuil violé). Sur carte primaire EMPTY ou DEGENERATE : sortie CLI code 3, fichier `LANE_NOT_USABLE`, carte et reçu conservés ; `--on-degenerate warn` pour continuer ; l'API Python lève `DegenerateMapError`. Pour le 9 µm, plan entier utilisé car le plancher de non-encre 0,25 est une sortie légitime.
- **Reçus** : `INK_SDK_RECEIPT.json` (profil, checkpoint et digest, échelle, rendu, statistiques p50/p90/p99/max, liveness, quantification, environnement Python/torch/CUDA/VILLA, commande exacte) et `RENDER_RECEIPT.json` (hash de x/y/z.tif et meta.json, hash du CT, sha256 du binaire de rendu, orientation, rognage) ; champ `non_claims` : « un mapa de probabilidad no es OCR ni prueba de tinta/letras » (`#022.2`, README `#001.2` : « The receipt is the source of truth »).
- **Règle PHerc. 0306B** : produit pixel à pixel de TRACE v3B et A-hn (moyenne de trois affinages de v8-in), recette de Warner et Bodill ; chiffres des « records » de ces auteurs sur PHerc. 0841 : AUC 0,874 avec 6,1 % de faux positifs (TRACE v3B × A-hn), 0,871 / 5,9 % (TRACE v3B × v8-in), contre 0,840 / 12,1 % pour v8-in seul (README, `#001.1`). Rapportés, non mesurés par ink-sdk.

## Plateforme et implémentation

Matériel : aucun matériel de référence déclaré (n/r) ; CPU/CUDA/MPS au choix (`device`), batch 1 par défaut, bf16 ; le doc note qu'un batch 4 vide la carte sur un GPU de 6 Go (mesure de Campaign X, citée, non reproduite ; design §13, `#024.0`). Logiciels : Python 3.11+, numpy, pydantic, typer, zarr, tifffile ; torch en extras ; checkout de ScrollPrize/villa (`koine_machines.inference.infer`, branche `merge-ink-pipelines`) pour les profils 9 µm ; `hecate.py` et le loader canonique vendorisés ; rendu Linux/AppImage seulement (design §10, `#021.0`). Code : licence MIT, https://github.com/LimeGS/ink-sdk ; poids : non redistribués, `ink-sdk fetch` (opt-in, sha256 pinned) les télécharge depuis Hugging Face / GitHub release ; licences variables (Rectina m4 et Studio : poids CC BY-NC 4.0 ; TRACE v3B : CC BY-NC-SA 4.0) (README `#001.0`, `#000.4`). Le dépôt n'a lui-même pas d'entraînement.

## Résultats

Aucun résultat scientifique : le dépôt le dit (inference only, no scientific evaluation). Seuls chiffres présents :

- Un run « réel » sur PHerc0841 w00 (Reader v3, donnée publique non vue par les modèles 9 µm), crop de 1024 px au plus d'encre labellisée ; deux sens de profondeur, un lisible et un aveugle, les deux ALIVE ; aucune métrique (README, `#000.0`).
- Rectina m4 vs Reader v3 (chiffres de la carte du modèle, pas d'ink-sdk) : 14 unités tenues à l'écart ou de contrôle, AUC moyenne +0,0056, supérieure sur 10 sur 14 ; mais avec le lecteur propre de l'auteur (moyenne de sept fenêtres de 17 couches sur une pile de 23, deux vues, quatre réseaux décalés) ; le profil ink-sdk n'utilise qu'une fenêtre : « the card's numbers are not reproduced by a default run » (README, `#000.4`).
- Gains de la règle 0306B ci-dessus (`#001.1`).
- Un décalage d'échelle 8,64 → 9,36 µm coûte environ 4 % de corrélation (mesure Campaign X, design §7.2, `#017.1`), r = 0,079 vs 0,885 (design §4, `#006.0`). Tests prévus (corrélation >= 0,999 vs runners de Campaign X), non rapportés comme exécutés (design §14-§15).

→ reportés dans `benchmarks.csv` : aucune ligne. Chiffres soit empruntés à d'autres projets (AUC de cartes de modèles, runs de Campaign X), soit des critères d'acceptation de tests ; aucun n'est une mesure d'ink-sdk. `benchmarks: none`.

## Limites et critique

- Dépôt communautaire non relu, un auteur, chiffres auto-déclarés. Document de conception daté du 2026-10-23, « propuesta v2 para aprobar… no hay código de producto todavía » (design, en-tête) ; le README du 2026-11-17 liste ~20 profils au lieu des 5 de v0 : le périmètre a changé sans que le design soit mis à jour (déduit : le design et le README ne se recoupent pas).
- Aucune évaluation : le SDK n'établit ni qualité de lecture ni comparaison entre modèles. La « battery » multi-profils × sens de profondeur et l'ensemble z-score sont mentionnés dans le README mais leurs pages (« Model notes », « Status and limits ») ne sont pas dans le PDF.
- La liveness gate teste la forme de la distribution (étendue, variance, fraction de pixels proches de 0,5), pas la présence d'encre : une carte non vide d'artefacts ou lue dans le mauvais sens passe (le README le montre : carte aveugle ALIVE). Seuils « calibrés » sur Campaign X, sans courbe ni jeu de calibration publié ; le seuil 0,9 peut rejeter une carte légitime en zone peu encrée (déduit).
- Reproductibilité : les reçus tracent tout, mais le déterminisme n'est garanti qu'avec `--deterministic` (adaptateur in-process) ; 9 µm et Hecate tournent en sous-processus, tolérance allclose 1e-3, GPU différents seulement p50/p99 ± 0,02 et Pearson >= 0,99 (design §13, `#024.0`). Pesos : le dense-native est reconstruit par `fetch` et son digest dépend de la version de torch (README, `#000.4`).
- Disparités de comparaison entre profils : normalisations, fenêtres (16 à 64 couches), échelles (2,4 / 9,6 / 8,64 µm) et sens de lecture varient ; aucune pondération commune. Les profils TimeSformer sont « experimental transfer » ; TRACE v3B sans gain connu à 8,64 µm (README, `#001.2`).
- Sortie quantifiée uint8 en amont pour le 9 µm et Hecate : le SDK reconvertit en float32, sans gagner de résolution (design §11, §16).
- Dépendances : villa non packagé (`koine_machines` hors PyPI), rendu Linux uniquement, poids sous licences non commerciales pour plusieurs profils.

## Pertinence pour le thème de la base

Axes : détection d'encre (ink-detection), validation et faux positifs (validation-fp), transfert de domaine (domain-transfer, par la matrice d'échelles).

- **Passerelle entre lecteurs déjà fichés** : le profil `ink_9um@argus-v2` exécute Argus V2 de `2026-ruiconte-ink-swarm-argus-v1-v2` ; `ink_9um@rectina-m4` exécute Rectina m4 de `2026-pellerano-rectina-m3-m4-dense-ink` (avec l'avertissement que la carte du modèle n'est pas reproduite par le lane standard) ; `canonical_2um` est le même checkpoint que `2026-nexusai-kevin-vesuvius-ink-bench-volumetric-ink` (r152 3ddec v2 l5 epoch13). Un banc commun de ces lecteurs sur un segment est donc possible avec une seule interface, ce que ces trois dépôts ne font pas (déduit).
- **Même auteur que `2026-limegs-winding-field-continuous-winding-coordinate`** : le SDK normalise l'étape lecteur comme winding-field normalise le champ d'enroulement ; les deux privilégient des reçus reproductibles et refusent les chiffres sans protocole (rapprochement par l'auteur, déduit).
- **Sens de profondeur** : la preuve d'un modèle aveugle dans un sens appuie l'exigence de lire en `forward` et `reverse` (et de ne pas supposer l'orientation de la normale) pour toute comparaison entre lecteurs.
- **Faux positifs** : la règle 0306B (produit de deux lecteurs) divise par ~2 le taux de faux positifs sur PHerc. 0841 selon les records des auteurs (12,1 % → 5,9-6,1 %), piste pour la question « comment prouver qu'une lettre est réelle ».
- Laisse ouvert : aucun score, aucune évaluation à l'aveugle, pas de lien entre liveness et lecture réelle.

## Gaps identifiés

- Aucune comparaison quantitative, sur un même segment et mêmes labels, des lecteurs que le SDK sait exécuter (Reader v3, Argus V2, Rectina m4, TRACE v3B, Hecate, Studio) : le SDK en fournirait l'outil.
- Gate de vie : pas de test sur cartes à mauvais sens de lecture, pas de seuils validés.
- Effet du sens de profondeur et de la normale sans ombilic : mesuré sur un seul run, sans métrique.
- Perte de 4 % de corrélation à 8,64 µm : mesure de Campaign X non publiée ici.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction `pymupdf`, `ok: false`, ligatures perdues sur quelques mots : texte lisible mais à contrôler).
Déduit et non affirmé par les auteurs : l'équivalence de checkpoint avec vesuvius-ink-bench ; l'identité d'Argus V2 et de Rectina m4 avec les papiers fichés ; le décalage entre design (5 profils) et README (~20) ; l'insuffisance de la gate pour détecter un mauvais sens de lecture (le README le montre, sans le formuler ainsi) ; le risque de rejet d'une carte légitime peu encrée. Les pages « Model notes », « Status and limits », « Troubleshooting » ne sont pas dans le document. Aucune figure (images omitted).
