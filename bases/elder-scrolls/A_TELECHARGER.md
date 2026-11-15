# Elder-scrolls — articles à télécharger manuellement

État au 2026-11-15. Copie de travail du doc partagé
<https://claude.ai/artifact/WKPXpWQHNtfWwSnFnenRaR>.

## Mode d'emploi

24 articles restent à récupérer à la main : 4 en libre accès mais bloqués aux
téléchargements automatiques, 8 sous paywall probable, 5 rapports Zenodo restreints, et 7
trouvés par la deuxième recherche (citations du corpus).

1. Télécharger le PDF depuis le lien DOI (navigateur, accès institutionnel). Aucun
   contournement de paywall.
2. Le déposer dans `bases/elder-scrolls/inbox/` sous le nom de la colonne « Fichier ».
   Le fichier de métadonnées correspondant (`<même nom>.meta.json`, construit depuis
   OpenAlex) y est déjà.
3. `bin/pdb ingest` depuis `bases/elder-scrolls/`, puis `/paper-fiche <paper_id>`.

## Libre accès, bloqués au téléchargement automatique

| Titre | Année | Venue | DOI | Fichier | Blocage |
|---|---|---|---|---|---|
| From damage to discovery via virtual unwrapping: Reading the scroll from En-Gedi | 2016 | Science Advances | [10.1126/sciadv.1601247](https://doi.org/10.1126/sciadv.1601247) | `sciadv.1601247.pdf` | Cloudflare |
| Ancient Greek text concealed on the back of unrolled papyrus revealed through shortwave-infrared hyperspectral imaging | 2019 | Science Advances | [10.1126/sciadv.aav8936](https://doi.org/10.1126/sciadv.aav8936) | `sciadv.aav8936.pdf` | Cloudflare |
| Revealing metallic ink in Herculaneum papyri | 2016 | PNAS | [10.1073/pnas.1519958113](https://doi.org/10.1073/pnas.1519958113) | `pnas.1519958113.pdf` | HTTP 403 |
| New Frontiers in the Digital Restoration of Hidden Texts in Manuscripts: A Review of the Technical Approaches | 2024 | Heritage (MDPI) | [10.3390/heritage7020034](https://doi.org/10.3390/heritage7020034) | `heritage7020034.pdf` | HTTP 403 |

## Sous paywall probable

| Titre | Année | Venue | DOI | Fichier |
|---|---|---|---|---|
| Virtual unrolling and information recovery from scanned scrolled historical documents (cité par 5 papiers de la base) | 2013 | Pattern Recognition | [10.1016/j.patcog.2013.06.015](https://doi.org/10.1016/j.patcog.2013.06.015) | `j.patcog.2013.06.015.pdf` |
| Revealing hidden text in rolled and folded papyri | 2017 | Applied Physics A | [10.1007/s00339-017-0808-6](https://doi.org/10.1007/s00339-017-0808-6) | `s00339-017-0808-6.pdf` |
| Robust Virtual Unrolling of Historical Parchment XMT Images | 2017 | IEEE TIP | [10.1109/tip.2017.2783626](https://doi.org/10.1109/tip.2017.2783626) | `tip.2017.2783626.pdf` |
| Layered Surface Detection for Virtual Unrolling | 2018 | ICPR | [10.1109/icpr.2018.8545715](https://doi.org/10.1109/icpr.2018.8545715) | `icpr.2018.8545715.pdf` |
| Fully Automatic Virtual Unwrapping Method for Documents Imaged by X-Ray Tomography | 2024 | LNCS (Springer) | [10.1007/978-3-031-70543-4_14](https://doi.org/10.1007/978-3-031-70543-4_14) | `978-3-031-70543-4_14.pdf` |
| Ink Detection from Carbonized Herculaneum Papyri using Deep Learning | 2023 | ICCIT (IEEE) | [10.1109/iccit60459.2023.10441240](https://doi.org/10.1109/iccit60459.2023.10441240) | `iccit60459.2023.10441240.pdf` |
| Sub-terahertz Radar Imaging of Ancient Herculaneum Papyrus Scrolls | 2025 | IRMMW-THz (IEEE) | [10.1109/irmmw-thz61557.2025.11319600](https://doi.org/10.1109/irmmw-thz61557.2025.11319600) | `irmmw-thz61557.2025.11319600.pdf` |
| Ink in Herculaneum: A Survey of Recent Perspectives | 2021 | Brill | [10.1163/9789004444805_005](https://doi.org/10.1163/9789004444805_005) | `9789004444805_005.pdf` |

## Rapports Zenodo restreints ou sous embargo

Fichiers non publics : « Request access » sur la page Zenodo, ou écrire aux auteurs.
Rapports de la communauté, non relus par les pairs.

| Titre | Auteurs | Publié | Accès | DOI | Fichier |
|---|---|---|---|---|---|
| Auditing the evaluation pipeline of a machine learning benchmark: data, code and results | Sedat Golgiyaz | 2026-08-12 | restreint | [10.5281/zenodo.21907639](https://doi.org/10.5281/zenodo.21907639) | `zenodo.21907639.pdf` |
| 2-D Texture-Based Ink Detection in Herculaneum Papyri: a Case Study | Oleksandr Korotetskyi, Michal Haindl | 2026-06-12 | embargo jusqu'au 2035-06-29 | [10.5281/zenodo.20649794](https://doi.org/10.5281/zenodo.20649794) | `zenodo.20649794.pdf` |
| Improved Ink Detection Generalization Across Herculaneum Papyrus Fragments | Adam Dzieszkowski | 2026-03-19 | restreint | [10.5281/zenodo.19103724](https://doi.org/10.5281/zenodo.19103724) | `zenodo.19103724.pdf` |
| Novel Findings in Ink Detection for Carbonized Herculaneum Papyri Using Machine Learning | Adam Dzieszkowski | 2026-03-16 | restreint | [10.5281/zenodo.19054054](https://doi.org/10.5281/zenodo.19054054) | `zenodo.19054054.pdf` |
| Cross-Resolution Ink Signal Analysis and Consensus Filtering for Herculaneum Scroll CT Data | Adam Dzieszkowski | 2026-02-23 | restreint | [10.5281/zenodo.18742319](https://doi.org/10.5281/zenodo.18742319) | `zenodo.18742319.pdf` |

## Deuxième recherche : cités par ou citant le corpus

Ajoutés le 2026-11-15. Le premier est cité par 5 papiers de la base.

| Titre | Auteurs | Année | Venue | DOI | Fichier | Accès |
|---|---|---|---|---|---|---|
| Opaque document imaging: building images of inaccessible texts | Yun Lin, W. Brent Seales | 2005 | ICCV | [10.1109/iccv.2005.182](https://doi.org/10.1109/iccv.2005.182) | `iccv.2005.182.pdf` | paywall IEEE |
| Digital restoration using volumetric scanning | W. Brent Seales, Yun Lin | 2004 | ACM/IEEE JCDL | [10.1145/996350.996380](https://doi.org/10.1145/996350.996380) | `996350.996380.pdf` | paywall ACM |
| Virtual unfolding of folded papyri | H.-E. Mahnke, T. Arlt, D. Baum et al. | 2019 | J. Cultural Heritage | [10.1016/j.culher.2019.07.007](https://doi.org/10.1016/j.culher.2019.07.007) | `j.culher.2019.07.007.pdf` | Elsevier ; copie possible au Helmholtz-Zentrum Berlin |
| Virtual unrolling using X-ray computed tomography | D. Allegra, E. Ciliberto, P. Ciliberto et al. | 2015 | EUSIPCO | [10.1109/eusipco.2015.7362908](https://doi.org/10.1109/eusipco.2015.7362908) | `eusipco.2015.7362908.pdf` | actes souvent libres (eurasip.org) |
| Apocalypto: revealing the unreadable | D. Mills, O. Samko, P. L. Rosin et al. | 2012 | Proc. SPIE | [10.1117/12.928917](https://doi.org/10.1117/12.928917) | `12.928917.pdf` | paywall SPIE |
| Virtual unrolling technology based on terahertz computed tomography | T. Wang, K. Wang, K. Zou et al. | 2021 | Optics and Lasers in Eng. | [10.1016/j.optlaseng.2021.106924](https://doi.org/10.1016/j.optlaseng.2021.106924) | `j.optlaseng.2021.106924.pdf` | paywall Elsevier |
| Synchrotron X-ray Mapping of Xenon Sorption in Carbon Ink on Papyrus | H. Hoffmann, T. Arlt, A. Hilger et al. | 2025 | ChemRxiv (préprint) | [10.26434/chemrxiv-2025-x4zvc](https://doi.org/10.26434/chemrxiv-2025-x4zvc) | `chemrxiv-2025-x4zvc.pdf` | libre accès, hôte chemrxiv.org non autorisé ici |

Métadonnées issues d'OpenAlex et de Zenodo, non vérifiées.
