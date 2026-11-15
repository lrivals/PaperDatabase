---
id: arxiv-2606.29085-complete-virtual-unwrapping-reading-rolled
title: "Complete virtual unwrapping and reading of a rolled Herculaneum papyrus"
year: 2026
backend: pymupdf
---

Complete virtual unwrapping and reading of

a rolled Herculaneum papyrus

Giorgio Angelotti1*, Stephen Parsons1,2, Federica Nicolardi1,3, Youssef Nader1,

Sean Johnson1, David Josey1, Paul Henderson1,4, Hendrik Schilling1, Johannes Rudolph1, Forrest McDonald1, Elian Rafael Dal Prá1, Paul Tafforeau5,

Alessandro Mirone5, C. Seth Parker2, Jan Paul Posma1, Benjamin Kyles1, Claudio Vergara1,3, Alessia Lavorante1,3, Rossella Villa1,6, Maria Chiara Robustelli1,3, Marzia D’Angelo1,3, Gianluca Del Mastro1,7, Michael McOsker1,8, Kilian Fleischer1,9,

Christy Chapman1,2, Nat Friedman1, W. Brent Seales1,2

1Vesuvius Challenge, San Francisco, CA, USA; 2EduceLab, University of Kentucky, Lexington, KY, USA; 3Università degli Studi di Napoli Federico II, Napoli, Italy; 4University of Glasgow, Glasgow, UK; 5ESRF,

Grenoble, France; 6Università di Salerno, Salerno, Italy; 7Università

degli Studi della Campania Luigi Vanvitelli, S. Maria Capua Vetere, Italy; 8University College London, London, UK; 9Universität Tübingen,

Tübingen, Germany.

*Corresponding author(s). E-mail(s): giorgio@scrollprize.org

## Abstract

The carbonized papyri from Herculaneum preserve the only large-scale library to survive from classical antiquity, but many unopened rolls remain unread because physical opening risks irreversible damage [1]. X-ray computed microtomography (µCT) and virtual unwrapping offer a non-invasive route to their texts, yet previous work on sealed Herculaneum scrolls has recovered only localized readings or limited surface regions. Here, using high-resolution phase-contrast µCT acquired on the BM18 beamline at the European Synchrotron Radiation Facility (ESRF), together with improved computational unrolling and machine learning, we achieve the complete virtual unwrapping and reading of PHerc. 1667 under explicit coverage and papyrological-review criteria. This makes PHerc. 1667 the first Herculaneum papyrus to be fully digitally unrolled and read for extended scholarly study without physical opening. In PHerc. Paris 4, the optimized scan protocol makes ink directly visible in the tomographic volume, allowing three-dimensional ink segmentation and independent validation of surface-conditioned ink recovery. In PHerc. 139, we recover title and author-attribution evidence identifying the scroll as Philodemus, On Gods, Book 8. These results move virtual unwrapping of the Herculaneum scrolls beyond isolated demonstrations towards a scalable framework for systematic recovery of the still-unopened library.

The Herculaneum papyri present one of the longest-standing access problems in the study of the ancient world. Discovered in the eighteenth century in the Villa of the Papyri, they are the only surviving large-scale library from classical antiquity[1]. Carbonized by the eruption of Mount Vesuvius in AD 79, the rolls survived in a form that made reading and preservation fundamentally opposed: physical opening could reveal text, yet also irreversibly damage the material. Earlier campaigns of mechanical opening revealed extraordinary texts, especially Epicurean works, but also demonstrated the destructive cost of direct intervention. Hundreds of rolls and multi-layer roll fragments therefore remain sealed, with their contents preserved yet inaccessible[1].

A non-invasive route to these texts is provided by X-ray µCT combined with virtual unwrapping, in which the internal sheet geometry is reconstructed, flattened into a readable domain and examined for traces of writing[2–8]. Herculaneum material is difficult for X-ray µCT because the carbonized papyrus support is radiographically similar to many carbon-based inks, yielding weak stroke–substrate contrast. The problem is compounded by variation in ink recipe, contaminants, deposit morphology and preservation, which means that writing may be expressed as faint metallic contrast, surface relief or subtle textural signal rather than by a single uniform signature. Earlier phase-contrast µCT studies reported candidate text signals in sealed Herculaneum material, but they did not establish a reproducible route from whole closed samples to scroll-scale scholarly reading[9, 10]. Subsequent work showed that useful signals may arise from metallic components in some inks, from hyperspectral contrast in opened material, or from fine surface deformations associated with ink on fragments[11–13]. What was missing was an end-to-end route from whole sample to readable surface: a coupled method that integrates optimized synchrotron imaging, geometric reconstruction, ink recovery and papyrological review.

Many of the advances required to address this problem were developed through the Vesuvius Challenge, an open-science effort launched in 2023 that brought together our research team, academic collaborators and an online distributed community of contributors. That programme established that text could be recovered from unopened or still-rolled Herculaneum material and progressively extended the readable extent of individual rolls[14–17]. The Vesuvius Challenge also made the problem public through a deliberately hybrid model of competition and collaboration. The 2023 Grand Prize established multi-column reading from PHerc. Paris 4[17], while open Kaggle competitions on ink detection[18] and surface detection[19] expanded the methodological base for two bottlenecks: ink recovery and surface extraction. Subsequent Vesuvius Challenge milestones included non-invasive recovery of the title of PHerc. 172[20] and semi-automated digital unwrapping of the lower approximately 70% of that scroll[21].

These advances form the immediate foundation for the present work: not another local detection of possible ink, but a scroll-scale workflow for turning closed or still-rolled Herculaneum material into inspectable scholarly surfaces.

Here we show that such a workflow can recover ancient text at scale, subject to the coverage and validation criteria specified below. By combining optimized high-resolution synchrotron µCT with moderate phase contrast, advanced large-volume tomographic reconstruction[22], semi-automated virtual unwrapping and deep neural networks, we recover text from three closed or still-rolled Herculaneum rolls in complementary evidential

regimes. We report complete virtual unwrapping of the preserved writing surface of PHerc. 1667 and complete papyrological reading of the text revealed throughout the preserved roll portion catalogued under this inventory number. We also recover title and authorattribution evidence in PHerc. 139, identifying the roll as Philodemus, On Gods, Book 8. In PHerc. Paris 4, the optimized scan provides a distinct evidential mode: ink is directly visible in the tomographic volume and can be segmented in three dimensions rather than inferred only from a surface-conditioned model. Together, these results move virtual unwrapping of the Herculaneum scrolls from proof-of-concept demonstrations towards a scalable research framework for recovering the unopened library.

Technical strategy

The workflow couples optimized tomography, surface reconstruction, surface-conditioned rendering and ink recovery. At the voxel sizes required for intact Herculaneum rolls, image quality is not determined by nominal sampling alone: densely packed carbonized fibers can reduce effective layer separability, while strong phase effects and weak absorption contrast can either obscure or reveal writing depending on sample geometry and ink recipe[14]. The optimized scan regime used here was selected to balance layer separation, ink visibility and manageable scan time; acquisition parameters are given in Methods and Extended Data Table 1. This optimized scanning approach is the result of an extensive series of imaging tests to optimize the energy range, the resolution level, the scanning geometry, and the level of phase-contrast. Results of these tests are presented in Extended Data.

Virtual unwrapping converts the tomographic volume into an inspectable writing surface. A learned recto-surface segmentation model provides volumetric cues, but the final surface is represented as an explicit quadrilateral mesh. The mesh is extracted, manually corrected where necessary, locally re-optimized and parameterized into a low-distortion near isometric two-dimensional domain. This explicit mesh representation prevents the reading from being tied to a single rendered image. Any point on the flattened surface has corresponding three-dimensional coordinates in the CT volume, allowing reviewers to inspect the underlying papyrus layer, assess local geometric reliability and distinguish surface-placement errors from ink-interpretation errors[2–8, 23].

Ink recovery uses two related but distinct regimes. In most sealed-scroll regions, ink remains too subtle for direct volumetric segmentation and is enhanced on surfaceconditioned renderings using models trained from fragment-derived supervision and conservative sealed-scroll pseudo-labels. These models are used as visibility amplifiers for expert inspection, not as autonomous reading systems: they are not trained on character identities, words, transcriptions, OCR targets or lexical labels. PHerc. Paris 4 is treated separately because the optimized scan makes ink-bearing deposits directly visible in the volume, allowing three-dimensional segmentation of ink and projection of that segmentation onto the flattened surface[3, 14]. This volumetric segmentation provides an independent test of whether surface-conditioned ink recovery corresponds to physically visible, surface-associated deposits; the result is presented below as an imaging-validation case.

I

II

III

10 cm

## (préambule)

**Fig. 1** | Scroll-scale virtual unwrapping of PHerc. 1667. a, Photograph of the sealed Herculaneum roll PHerc. 1667. b, Transverse tomographic section (isotropic voxel size 2.4 µm) showing the nested internal wrap structure of the carbonized papyrus. c, Longitudinal tomographic slice showing the layered structure along the scroll axis. d, Surface-conditioned rendering of the reconstructed writing surface after virtual unwrapping and ink enhancement, displayed in three consecutive bands of the flattened parameter domain (I-III). Black background corresponds to regions outside the preserved writing surface or to physically absent or damaged substrate. Within the grey papyrus surface, dark strokes indicate the scholar-facing ink rendering used for papyrological inspection. The figure summarizes the transition from a sealed physical roll to a continuous inspectable writing surface. Scale bars as shown.

Results

The Results are organized around three questions. First, can an intact Herculaneum roll be completely unwrapped and read? The presented work on PHerc. 1667 addresses this question. Second, can ink recovery be independently checked against ink that is directly visible in the CT volume? The recent scan of PHerc. Paris 4 provides this imaging-validation

case. Third, can virtual unwrapping recover paratextual evidence sufficient to identify a sealed work? PHerc. 139 provides this title-identification case.

Complete unwrapping and reading of an unopened papyrus: PHerc. 1667

PHerc. 1667 provides the principal complete-unwrapping result of this work (Fig. 1). The sealed object is shown in Fig. 1a, while transverse and longitudinal tomographic sections reveal the dense nested architecture of the carbonized papyrus layers (Fig. 1b,c). Fig. 1d shows the corresponding surface-conditioned rendering after virtual unwrapping and ink enhancement: the reconstructed writing surface is displayed in three consecutive bands of the flattened parameter domain, with dark strokes indicating the scholar-facing ink signal used for papyrological inspection. The reconstructed surface contains 22 columns or column-equivalents over approximately 860 cm2 of preserved writing surface; black regions mark areas outside the preserved surface or physically absent or damaged substrate.

This is a complete reconstruction and ink-enhanced rendering of the preserved writing surface assigned to PHerc. 1667, rather than a selected local region. We use “complete virtual unwrapping” in a bounded geometric sense: the preserved surface included in the claim is represented by an approved mesh, can be inspected in the CT volume and is rendered in the flattened coordinate domain. We use “complete reading” in a corresponding papyrological sense: the transcription is restricted to image-supported preserved text visible in the renderings; restoration of letters corresponding to physically lost substrate is indicated by the use of square brackets in accordance with established papyrological convention; uncertain letters are marked with an underdot. The complete reading covers all image-supported preserved text, with untranscribed material restricted to the surviving portions of the first three text columns, amounting to 33 cm2, where the fragmentary state of the physical object does not permit a secure interpretation of the visible ink traces. The full papyrological transcription and uncertainty markings are provided in Methods.

Volumetric validation of ink recovery: PHerc. Paris 4

PHerc. Paris 4 tests whether surface-conditioned ink recovery corresponds to physically visible structures in the CT volume. In the optimized high-resolution BM18 scan of PHerc. Paris 4, thanks to phase retrieval, ink-bearing strokes appear as bright, surface-associated deposits with apparent cross-sectional thicknesses of approximately 10–20 µm (Fig. 2 and Extended Data Fig. 3).

These deposits are directly visible in the volume, can be segmented in three dimensions and then projected onto the flattened surface, where they coincide with the Vesuvius Challenge Grand Prize Banner region (Fig. 3), the first multi-line reading from a stillrolled Herculaneum papyrus[15–17]. This provides an independent physical validation case showing that, under at least one optimized scan regime and ink preservation state, the surface-conditioned ink signal corresponds to directly visible surface-associated deposits.

**Fig. 2** | Volumetric ink segmentation in PHerc. Paris 4 and projection onto the unwrapped surface. a, Phase-retrieved tomographic cross-section using 2.4 µm isotropic voxel size through a visible ink-bearing surface deposit, with a representative apparent thickness measurement. b, The same cross-section with the segmented ink mask overlaid in red. c, Flattened surface-conditioned rendering of an ink-bearing region before projection of the volumetric segmentation, showing the underlying papyrus texture and writing traces.

Identification of a sealed work from title evidence: PHerc. 139

PHerc. 139 provides a separate title-identification result. In a title-bearing region of the reconstructed surface, we recover author, work-title and book-number evidence (Fig. 4). The title-bearing sequence is read as

Φ̣ι[λοδ]ή̣μου περὶθεῶν Η̅ that is, “Philodemus, On Gods, Book 8”. The overlined Η is interpreted as the book-number indication.

The book number is written here on the same line as the title, despite the more commonly attested practice in titles from Herculaneum, where the title and book number appear on two separate lines. A similar layout is now documented in the final title of the unopened

**Fig. 3** | PHerc. Paris 4, comparison with 2023 data. a, 2023 Grand Prize winning Ink Detection Model [16, 17] on a virtually unwrapped portion of PHerc. Paris 4 on the 7.91 µm pixel size volume of PHerc. Paris 4 from the EduceLab-Scrolls dataset [3] b, 3D ink segmentation enhanced alpha composite rendering against the BM18 2.4 µm data. The second confirms the reading from the 2023 Vesuvius Challenge. Zoom-in lenses highlight the difference in data quality.

roll PHerc. 172 (Φιλο̣δήμο̣υ̣ Πε̣ρὶ| κα̣κ̣ιῶν Α̣̅, Philodemus, On vices book 1)[20]. The title was written by the same scribe who copied the text.

The presence of Philodemus’ name, by far the most extensively attested Epicurean philosopher in the Herculaneum library (I BCE), allows us to assign the scroll to the 1st century BC-1st century AD (with a terminus ante quem of 79 AD). More importantly, this discovery informs us for the first time that Philodemus’ work On Gods comprised at least eight books. Until now, only the first book was known, preserved in PHerc. 26 (Φιλοδήμ[ου | Περὶθεῶν̣ | Α̅, Philodemus, On gods book 1), together with other theological works by the same author known under different titles.

The PHerc. 139 result is important because title-bearing regions can identify sealed books even when continuous prose reading remains incomplete. The workflow therefore recovers not only passages of text, but also library metadata: author, work title and book number.

In addition to the end title, the portions of text recovered thus far preserve a number of terms and expressions that provide insight into the treatise theological concerns: χωρὶϲ

**Fig. 4** | Title and author-attribution evidence in PHerc. 139. a, Surface-conditioned rendering of the title-bearing region of PHerc. 139. b, The ink-enhanced signal shown in black against the papyrus texture. The visible title and author-attribution sequence identifies the roll as Philodemus, On Gods, Book 8. Scale bar, 5 mm.

προνο[ί]α̣ϲ̣ (”without providence”), ἀόρατα (”invisible entities”), καὶτὸκατ̣ὰ̣ φύϲιν (”according to nature”), καὶπάν̣τ̣α̣ χωρὶϲ πόνων (”and everything free from troubles”), νοερόν (“intellectual”). The images which supported the reading are provided in the corresponding order in the Supplementary Information.

Discussion

These results mark a transition in the virtual recovery of the Herculaneum library. What had previously been demonstrated in local regions, selected banners or partial scroll surfaces is shown here to operate across the preserved writing surface of an intact roll, while also yielding independent volumetric validation and title-level identification in separate samples. They move the programme from localized breakthroughs and partial-scroll demonstrations towards an end-to-end workflow for complete unwrapping and reading. The results from PHerc. 1667 provide the strongest test of that pipeline so far, showing that scroll-scale virtual

unwrapping and complete reading of a still-sealed scroll are achievable. The recovered titleand-attribution evidence from PHerc. 139, after the recovery of the title-and-attribution from PHerc. 172[21], adds a second kind of payoff: the method can identify works and authors, not only recover running prose. The PHerc. Paris 4 scan adds a third, imagingspecific payoff, because directly visible three-dimensional ink segmentation can ground and audit surface-conditioned ink recovery.

This workflow does not imply that all sealed Herculaneum rolls are automatically readable. Performance depends on scroll general preservation state, scan quality, layer separation, deformation, local ink contrast and surface preservation.

Two bottlenecks remain dominant. The first is geometric. Even strong surfaceprediction networks can fail in highly compressed regions, where mergers, holes and sheet switches destabilize surface estimation. The second is radiometric. Ink segmentation remains weak, varies across ink recipes and local degradation states, and is further modulated by scan conditions and diffusion of the X-rays by the samples in case of large and compacted parts. These difficulties are not independent. Better geometry produces more legible surface-conditioned views, whereas better legibility improves both expert transcription and the supervision available for ink detection. For this reason, progress depends on treating scanning, learned surface and ink models, geometric reconstruction and scholar-facing image formation as a coupled system.

Future gains will depend partly on improved control of effective resolution and on a better account of how morphology, phase effects and absorption together contribute to ink visibility. The present results are best understood as operating in a mixed-signal regime, rather than as reading topography alone[13]. Higher-resolution and better-tuned scans should reduce ambiguity in both layer separation and ink detectability, especially in the most compressed regions. More robust tracing networks and hybrid neural tracers that predict or refine sheet trajectories while enforcing local surface continuity and neighbouring-wrap consistency should reduce the manual burden of correction and neighbour transfer[8, 24]. The latter could be achieved by improving the accuracy of annotations used to train the machine learning models or relying on self-supervised methods. Additional fragment-to-scroll supervision, together with conservative pseudo-label expansion on intact rolls, should strengthen ink models across a wider range of ink recipes without sacrificing trustworthiness.

None of these remaining challenges alters the main conclusion. The key transition marked by the present work is therefore from exceptional local recovery to systematic scrollscale recovery. The remaining challenge is not whether sealed Herculaneum texts can be read non-invasively, but how broadly, robustly and efficiently the workflow can be extended across the still-unopened library.
