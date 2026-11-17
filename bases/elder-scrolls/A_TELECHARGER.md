# Elder-scrolls — articles à télécharger manuellement

État au 2026-11-17 (8 PDF reçus le 17 novembre, dans `inbox/` ; les 9 du 15 novembre sont ingérés et fichés). Copie de travail
du doc partagé <https://claude.ai/artifact/WKPXpWQHNtfWwSnFnenRaR>.

## Mode d'emploi

7 articles restent à récupérer à la main : 2 sous paywall probable et 5 rapports Zenodo
restreints. 8 PDF reçus le 17 novembre attendent l'ingestion.

1. Télécharger le PDF depuis le lien DOI (navigateur, accès institutionnel). Aucun
   contournement de paywall.
2. Le déposer dans `bases/elder-scrolls/inbox/` sous le nom de la colonne « Fichier ».
   Le fichier de métadonnées correspondant (`<même nom>.meta.json`, construit depuis
   OpenAlex) y est déjà pour les 7 articles restants.
3. `bin/pdb ingest` depuis `bases/elder-scrolls/`, puis `/paper-fiche <paper_id>`.

## Reste à télécharger

### Sous paywall probable

| Titre | Année | Venue | DOI | Fichier |
|---|---|---|---|---|
| Virtual unrolling and information recovery from scanned scrolled historical documents (titre présent dans le texte de 12 papiers de la base) | 2013 | Pattern Recognition | [10.1016/j.patcog.2013.06.015](https://doi.org/10.1016/j.patcog.2013.06.015) | `j.patcog.2013.06.015.pdf` |
| Fully Automatic Virtual Unwrapping Method for Documents Imaged by X-Ray Tomography (ICDAR 2024, LNCS 14806, chap. 14) | 2024 | LNCS (Springer) | [10.1007/978-3-031-70543-4_14](https://doi.org/10.1007/978-3-031-70543-4_14) | `978-3-031-70543-4_14.pdf` |

Pour le chapitre ICDAR 2024 : le fichier reçu (`978-3-031-70543-4_24`, 1 page) est le
*Correction to* (chapitre 24, erratum des remerciements), pas l'article. Il faut le
chapitre 14 lui-même. Dans `978-3-031-70543-4_14.meta.json`, prénoms et noms de Petr Kulagin
et Dmitry Polevoy étaient inversés : corrigé le 2026-11-15.

### Rapports Zenodo restreints ou sous embargo

Fichiers non publics : « Request access » sur la page Zenodo, ou écrire aux auteurs.
Rapports de la communauté, non relus par les pairs. Trois sont du même auteur (Dzieszkowski) :
une seule demande peut suffire.

| Titre | Auteurs | Publié | Accès | DOI | Fichier |
|---|---|---|---|---|---|
| Auditing the evaluation pipeline of a machine learning benchmark: data, code and results | Sedat Golgiyaz | 2026-08-12 | restreint | [10.5281/zenodo.21907639](https://doi.org/10.5281/zenodo.21907639) | `zenodo.21907639.pdf` |
| 2-D Texture-Based Ink Detection in Herculaneum Papyri: a Case Study | Oleksandr Korotetskyi, Michal Haindl | 2026-06-12 | embargo jusqu'au 2035-06-29 | [10.5281/zenodo.20649794](https://doi.org/10.5281/zenodo.20649794) | `zenodo.20649794.pdf` |
| Improved Ink Detection Generalization Across Herculaneum Papyrus Fragments | Adam Dzieszkowski | 2026-03-19 | restreint | [10.5281/zenodo.19103724](https://doi.org/10.5281/zenodo.19103724) | `zenodo.19103724.pdf` |
| Novel Findings in Ink Detection for Carbonized Herculaneum Papyri Using Machine Learning | Adam Dzieszkowski | 2026-03-16 | restreint | [10.5281/zenodo.19054054](https://doi.org/10.5281/zenodo.19054054) | `zenodo.19054054.pdf` |
| Cross-Resolution Ink Signal Analysis and Consensus Filtering for Herculaneum Scroll CT Data | Adam Dzieszkowski | 2026-02-23 | restreint | [10.5281/zenodo.18742319](https://doi.org/10.5281/zenodo.18742319) | `zenodo.18742319.pdf` |

## Reçus le 2026-11-17, dans `inbox/`, à ingérer

PDF et `.meta.json` déposés (métadonnées OpenAlex pour Baum 2017, relevées sur la première page pour les autres). Reste
`bin/pdb ingest`, puis `/paper-fiche` pour chacun. Années corrigées : Wang 2022 et
Mahnke 2020 (2021 et 2019 = mise en ligne).

| Titre | Auteurs | Année | Venue | DOI | Fichier |
|---|---|---|---|---|---|
| Revealing hidden text in rolled and folded papyri | D. Baum, N. Lindow, H.-C. Hege et al. | 2017 | Applied Physics A 123:171 | [10.1007/s00339-017-0808-6](https://doi.org/10.1007/s00339-017-0808-6) | `s00339-017-0808-6.pdf` |
| Opaque Document Imaging: Building Images of Inaccessible Texts | Y. Lin, W. B. Seales | 2005 | ICCV | [10.1109/iccv.2005.182](https://doi.org/10.1109/iccv.2005.182) | `iccv.2005.182.pdf` |
| Digital Restoration Using Volumetric Scanning | W. B. Seales, Y. Lin | 2004 | ACM/IEEE JCDL | [10.1145/996350.996380](https://doi.org/10.1145/996350.996380) | `996350.996380.pdf` |
| Virtual unfolding of folded papyri | H.-E. Mahnke, T. Arlt, D. Baum et al. | 2020 | J. Cultural Heritage 41:264–269 | [10.1016/j.culher.2019.07.007](https://doi.org/10.1016/j.culher.2019.07.007) | `j.culher.2019.07.007.pdf` |
| Virtual unrolling using X-ray computed tomography | D. Allegra, E. Ciliberto, P. Ciliberto et al. | 2015 | EUSIPCO | [10.1109/eusipco.2015.7362908](https://doi.org/10.1109/eusipco.2015.7362908) | `eusipco.2015.7362908.pdf` |
| Apocalypto: Revealing the unreadable | D. Mills, O. Samko, P. Rosin et al. | 2012 | Proc. SPIE 8506, 85060A | [10.1117/12.928917](https://doi.org/10.1117/12.928917) | `12.928917.pdf` |
| Virtual unrolling technology based on terahertz computed tomography | T. Wang, K. Wang, K. Zou et al. | 2022 | Optics and Lasers in Eng. 151:106924 | [10.1016/j.optlaseng.2021.106924](https://doi.org/10.1016/j.optlaseng.2021.106924) | `j.optlaseng.2021.106924.pdf` |
| Synchrotron X-ray Mapping of Xenon Sorption in Carbon Ink on Papyrus | H. Hoffmann, T. Arlt, A. Hilger et al. | 2025 | ChemRxiv (préprint) | [10.26434/chemrxiv-2025-x4zvc](https://doi.org/10.26434/chemrxiv-2025-x4zvc) | `chemrxiv-2025-x4zvc.pdf` |

Le préprint Hoffmann 2025 est distinct du rapport Zenodo déjà ingéré
(`2026-hoffmann-xenon-contrast-carbon-ink-tomography`, DOI 10.5281/zenodo.23164128).

Le PDF « Unlocking history through automated virtual unfolding » (Dambrogio 2021) reçu
le même jour est déjà dans la base (`2021-dambrogio-unlocking-history-through-automated-virtual`,
même DOI) : non redéposé.

## Reçus le 2026-11-15 : ingérés et fichés

Plus rien à faire : fiche `done` pour chacun.

| Titre | Année | Venue | paper_id |
|---|---|---|---|
| From damage to discovery via virtual unwrapping: Reading the scroll from En-Gedi | 2016 | Science Advances | `2016-seales-damage-discovery-virtual-unwrapping-reading` |
| Ancient Greek text concealed on the back of unrolled papyrus revealed through shortwave-infrared hyperspectral imaging | 2019 | Science Advances | `2019-tournie-ancient-greek-text-concealed-back` |
| Revealing metallic ink in Herculaneum papyri | 2016 | PNAS | `2016-brun-revealing-metallic-ink-herculaneum-papyri` |
| New Frontiers in the Digital Restoration of Hidden Texts in Manuscripts: A Review of the Technical Approaches | 2024 | Heritage (MDPI) | `2024-perino-frontiers-digital-restoration-hidden-texts` |
| Robust Virtual Unrolling of Historical Parchment XMT Images | 2018 | IEEE TIP 27(4) | `2018-liu-robust-virtual-unrolling-historical-parchment` |
| Layered Surface Detection for Virtual Unrolling | 2018 | ICPR | `2018-dahl-layered-surface-detection-virtual-unrolling` |
| Ink Detection from Carbonized Herculaneum Papyri using Deep Learning | 2023 | ICCIT (IEEE) | `2023-mou-ink-detection-carbonized-herculaneum-papyri` |
| Sub-terahertz Radar Imaging of Ancient Herculaneum Papyrus Scrolls reveals Adhesion to Substrate after Unrolling | 2025 | IRMMW-THz (IEEE) | `2025-verde-sub-terahertz-radar-imaging-ancient` |
| Ink in Herculaneum: A Survey of Recent Perspectives | 2021 | Brill (chapitre d'ouvrage) | `2021-damiani-ink-herculaneum-survey-recent-perspectives` |

Métadonnées des articles restants issues d'OpenAlex et de Zenodo, non vérifiées.
