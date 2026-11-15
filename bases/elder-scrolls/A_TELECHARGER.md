# Elder-scrolls — articles à télécharger manuellement

État au 2026-11-15 (mis à jour après réception de 9 PDF). Copie de travail du doc partagé
<https://claude.ai/artifact/WKPXpWQHNtfWwSnFnenRaR>.

## Mode d'emploi

8 articles restent à récupérer à la main : 2 sous paywall probable, 1 dont seul l'erratum
a été reçu, 5 rapports Zenodo restreints. 9 PDF sont déjà dans `inbox/`, en attente
d'ingestion.

1. Télécharger le PDF depuis le lien DOI (navigateur, accès institutionnel). Aucun
   contournement de paywall.
2. Le déposer dans `bases/elder-scrolls/inbox/` sous le nom de la colonne « Fichier ».
   Le fichier de métadonnées correspondant (`<même nom>.meta.json`, construit depuis
   OpenAlex) y est déjà.
3. `bin/pdb ingest` depuis `bases/elder-scrolls/`, puis `/paper-fiche <paper_id>`.

## Reste à télécharger

### Sous paywall probable

| Titre | Année | Venue | DOI | Fichier |
|---|---|---|---|---|
| Virtual unrolling and information recovery from scanned scrolled historical documents (cité par 5 papiers de la base) | 2013 | Pattern Recognition | [10.1016/j.patcog.2013.06.015](https://doi.org/10.1016/j.patcog.2013.06.015) | `j.patcog.2013.06.015.pdf` |
| Revealing hidden text in rolled and folded papyri | 2017 | Applied Physics A | [10.1007/s00339-017-0808-6](https://doi.org/10.1007/s00339-017-0808-6) | `s00339-017-0808-6.pdf` |
| Fully Automatic Virtual Unwrapping Method for Documents Imaged by X-Ray Tomography (ICDAR 2024, LNCS 14806, chap. 14) | 2024 | LNCS (Springer) | [10.1007/978-3-031-70543-4_14](https://doi.org/10.1007/978-3-031-70543-4_14) | `978-3-031-70543-4_14.pdf` |

Pour le chapitre ICDAR 2024 : le fichier reçu (`978-3-031-70543-4_24`, 1 page) est le
*Correction to* (chapitre 24, erratum des remerciements), pas l'article. Il faut le
chapitre 14 lui-même. Dans `978-3-031-70543-4_14.meta.json`, prénoms et noms de Petr Kulagin
et Dmitry Polevoy étaient inversés : corrigé le 2026-11-15.

### Rapports Zenodo restreints ou sous embargo

Fichiers non publics : « Request access » sur la page Zenodo, ou écrire aux auteurs.
Rapports de la communauté, non relus par les pairs.

| Titre | Auteurs | Publié | Accès | DOI | Fichier |
|---|---|---|---|---|---|
| Auditing the evaluation pipeline of a machine learning benchmark: data, code and results | Sedat Golgiyaz | 2026-08-12 | restreint | [10.5281/zenodo.21907639](https://doi.org/10.5281/zenodo.21907639) | `zenodo.21907639.pdf` |
| 2-D Texture-Based Ink Detection in Herculaneum Papyri: a Case Study | Oleksandr Korotetskyi, Michal Haindl | 2026-06-12 | embargo jusqu'au 2035-06-29 | [10.5281/zenodo.20649794](https://doi.org/10.5281/zenodo.20649794) | `zenodo.20649794.pdf` |
| Improved Ink Detection Generalization Across Herculaneum Papyrus Fragments | Adam Dzieszkowski | 2026-03-19 | restreint | [10.5281/zenodo.19103724](https://doi.org/10.5281/zenodo.19103724) | `zenodo.19103724.pdf` |
| Novel Findings in Ink Detection for Carbonized Herculaneum Papyri Using Machine Learning | Adam Dzieszkowski | 2026-03-16 | restreint | [10.5281/zenodo.19054054](https://doi.org/10.5281/zenodo.19054054) | `zenodo.19054054.pdf` |
| Cross-Resolution Ink Signal Analysis and Consensus Filtering for Herculaneum Scroll CT Data | Adam Dzieszkowski | 2026-02-23 | restreint | [10.5281/zenodo.18742319](https://doi.org/10.5281/zenodo.18742319) | `zenodo.18742319.pdf` |

## Reçus le 2026-11-15, dans `inbox/`, à ingérer

| Titre | Année | Venue | DOI | Fichier | Remarque |
|---|---|---|---|---|---|
| From damage to discovery via virtual unwrapping: Reading the scroll from En-Gedi | 2016 | Science Advances | [10.1126/sciadv.1601247](https://doi.org/10.1126/sciadv.1601247) | `sciadv.1601247.pdf` | |
| Ancient Greek text concealed on the back of unrolled papyrus revealed through shortwave-infrared hyperspectral imaging | 2019 | Science Advances | [10.1126/sciadv.aav8936](https://doi.org/10.1126/sciadv.aav8936) | `sciadv.aav8936.pdf` | article + Supplementary Materials (14 p.) |
| Revealing metallic ink in Herculaneum papyri | 2016 | PNAS | [10.1073/pnas.1519958113](https://doi.org/10.1073/pnas.1519958113) | `pnas.1519958113.pdf` | |
| New Frontiers in the Digital Restoration of Hidden Texts in Manuscripts: A Review of the Technical Approaches | 2024 | Heritage (MDPI) | [10.3390/heritage7020034](https://doi.org/10.3390/heritage7020034) | `heritage7020034.pdf` | |
| Robust Virtual Unrolling of Historical Parchment XMT Images | 2018 | IEEE TIP 27(4):1914–1926 | [10.1109/tip.2017.2783626](https://doi.org/10.1109/tip.2017.2783626) | `tip.2017.2783626.pdf` | année corrigée (2017 = mise en ligne) |
| Layered Surface Detection for Virtual Unrolling | 2018 | ICPR | [10.1109/icpr.2018.8545715](https://doi.org/10.1109/icpr.2018.8545715) | `icpr.2018.8545715.pdf` | |
| Ink Detection from Carbonized Herculaneum Papyri using Deep Learning | 2023 | ICCIT (IEEE) | [10.1109/iccit60459.2023.10441240](https://doi.org/10.1109/iccit60459.2023.10441240) | `iccit60459.2023.10441240.pdf` | |
| Sub-terahertz Radar Imaging of Ancient Herculaneum Papyrus Scrolls reveals Adhesion to Substrate after Unrolling | 2025 | IRMMW-THz (IEEE) | [10.1109/irmmw-thz61557.2025.11319600](https://doi.org/10.1109/irmmw-thz61557.2025.11319600) | `irmmw-thz61557.2025.11319600.pdf` | résumé étendu, 2 p. |
| Ink in Herculaneum: A Survey of Recent Perspectives | 2021 | Brill (chapitre 3 d'un ouvrage collectif) | [10.1163/9789004444805_005](https://doi.org/10.1163/9789004444805_005) | `9789004444805_005.pdf` | |

Métadonnées issues d'OpenAlex et de Zenodo, non vérifiées (sauf titres, années et
venues des 9 PDF reçus, contrôlés sur la première page).
