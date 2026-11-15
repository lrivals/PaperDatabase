---
id: 2024-perino-frontiers-digital-restoration-hidden-texts
title: "New Frontiers in the Digital Restoration of Hidden Texts in Manuscripts: A Review of the Technical Approaches"
year: 2024
backend: pymupdf
---

Citation: Perino, M.; Pronti, L.; Moffa,

C.; Rosellini, M.; Felici, A.C. New

Frontiers in the Digital Restoration of

Hidden Texts in Manuscripts: A

Review of the Technical Approaches.

Heritage 2024, 7, 683–696. https://

doi.org/10.3390/heritage7020034

Academic Editor: Maurizio Aceto

Received: 20 December 2023

Revised: 22 January 2024

Accepted: 22 January 2024

Published: 3 February 2024

Correction Statement: This article

has been republished with a minor

change. The change does not affect

the scientific content of the article and

further details are available within the

backmatter of the website version of

this article.

Licensee MDPI, Basel, Switzerland.

This article is an open access article

distributed under the terms and

conditions of the Creative Commons

Attribution (CC BY) license (https://

creativecommons.org/licenses/by/

4.0/).

heritage

Review New Frontiers in the Digital Restoration of Hidden Texts in Manuscripts: A Review of the Technical Approaches

Michela Perino 1,* , Lucilla Pronti 2 , Candida Moffa 3, Michela Rosellini 4 and Anna Candida Felici 3

Opera del Vocabolario Italiano, National Research Council of Italy (OVI-CNR), 50141 Firenze, Italy National Laboratories of Frascati, National Institute for Nuclear Physics (INFN), 00044 Frascati, Italy; lucilla.pronti@lnf.infn.it Department of Basic and Applied Sciences for Engineering (SBAI), Sapienza University of Rome, 00161 Rome, Italy; candida.moffa@uniroma1.it (C.M.); annac.felici@uniroma1.it (A.C.F.) Department of Classics, Sapienza University of Rome, 00185 Rome, Italy; michela.rosellini@uniroma1.it * Correspondence: michela.perino@cnr.it

## Abstract

The digital restoration of historical manuscripts centers on deciphering hidden writings, made imperceptible to the naked eye due to factors such as erasure, fading, carbonization, and aging effects. Recent advancements in modern technologies have significantly improved our ability to unveil and interpret such written cultural heritage that, for centuries, had remained inaccessible to contemporary understanding. This paper aims to present a critical overview of state-of-the-art technologies, engaging in discussions about perspectives and limitations, and anticipating future applications. Serving as a practical guide, this work seeks to assist in the selection of techniques for digitally restoring ancient writings. Additionally, potential and challenges associated with integrating these techniques with advanced machine-learning approaches are also outlined.

Keywords: multispectral imaging; hyperspectral imaging; macro-XRF; X-ray tomography; infrared thermography; terahertz; photoacoustic imaging; synchrotron radiation; PIXE

## 1. Introduction

Over the centuries, the discovery of indecipherable manuscripts has been far from an uncommon occurrence. The legibility of such documents is often compromised by a range of factors, including the manuscript’s usage, storage conditions, natural disasters, the manufacture of writing support material, and the composition of ink. Technical approaches focused on physical–chemical methods aim to improve the readability of such texts and make manuscripts accessible to scholars nowadays. Since the 1990s, emphasis has been placed on non-invasive and imaging technologies, as well as on the use of portable instrumentation. These innovations resulted in an ever-increasing number of research projects of national and international prominence, most of these focused on specific categories of texts, like palimpsests, i.e., manuscripts reused in which traces of their earlier forms are barely visible. Notably, pioneering contributions include the case studies of the palimpsests of Archimedes (1999–2008) and St. Catherine’s Monastery in the Sinai (2011–2016). More recently, two Advanced Grants from the European Research Council (ERC) have brought to the forefront the challenge of restoring indecipherable manuscripts with advanced imaging techniques: the “PAGES” project (AdG 2019 n◦882588—Priscian’s Ars Grammatica in European Scriptoria) aims to read palimpsests containing erased medieval copies of the Priscian’s Ars Grammatica; on the other hand, the “GreekSchools” project (AdG 2019 n◦885222) focuses on the recovery of the philosophical texts concealed in the carbonized papyri of Herculaneum. Moreover, new projects dedicated to the study and digital acquisition of ancient manuscripts propose the development of innovative solutions for their 3D visualization (i.e., the Codex4D project [1]).

Heritage 2024, 7, 683–696. https://doi.org/10.3390/heritage7020034 https://www.mdpi.com/journal/heritage

The initial step in digital restoration involves selecting the optimal spectral range in which the ink stands out against the support. The choice of the equipment is influenced by factors, such as the physical–chemical composition of both the writing support and ink, as well as issues hindering readability, like carbonization, stains, mechanical erasure, and natural fading. The groundwork for a critical review of the field has been established through prior studies. Tonazzini et al., 2019 [2], explored some of the most widely used techniques for paintings and manuscripts, while Orazi 2020 [3] delved specifically into mid-wave infrared reflectography and thermography.

The aim of this work is to provide a comprehensive overview of various technical approaches employed to enhance the readability of historical writings, discussing both the drawbacks and potential applications of well-known and lesser-known methods. In the second paragraph, we deal with the critical issue of library accessibility, a fundamental consideration in designing measurement sessions. Subsequently, the work is divided into eight paragraphs, each dedicated to a specific technique, outlining both the theory and application scope. For the lesser-known technologies, future application scenarios are envisioned. Furthermore, challenges of combining imaging techniques with modern machine-learning approaches are also outlined.

## 2. Accessibility of Libraries and Best Practices

The accessibility of libraries and conservation institutes is one of the fundamental issues in the digital restoration of manuscripts. In the case of non-portable technologies, such as synchrotron radiation, institutions may send the manuscript to a specific facility. However, even though almost all technologies are portable, they need specific conditions to be used in situ; for instance, a space dedicated to performing scientific measurements, as a dark room, is necessary for the use of ultraviolet (UV) light. Usually, these requirements need to be presented in advance to the libraries through a plan, in order to reach an agreement on insurance and storage policies for both manuscripts and equipment, hours of work, types of analysis, and staff involved.

As preserving the integrity of the manuscript poses a crucial condition, several precautions must be observed to guarantee both the effectiveness of the measurement session and the safeguarding of the artefact. A single sheet of parchment can be easier to manage than a codex; in most cases, the manuscript’s binding holds tight the pages, preventing the book from opening fully. Libraries often provide scholars with tools for handling manuscripts. Alternatively, some tutorials (e.g., the instructions of Collapsible Book Cradle by Tara O’Brien) describe how to create different supports to adapt to the opening of a codex while preserving its integrity. After determining the optimal opening angle of the codex, it is essential to maintain page stability throughout the session. Various options are available for achieving this, e.g., coated lead weights or transparent polypropylene/polyester strips, which are the most widely adopted commercial alternatives. During measurements, dust or residues of various materials may accidentally cover the writing, and they can provoke light absorbance/reflections during the measurements; a fine, soft-bristled, conservatorapproved brush can help remove them.

## 3. UV Photography

UV photography was the first technique used to recover invisible text, and has been used since the 1920s, when Wood’s lamps went on the market, nowadays substituted by LEDs.

Two techniques are the most used in UV photography: UV-induced visible fluorescence and UV-reflected imaging.

UV-induced visible fluorescence (UVIVF), or UV-fluorescence (UVF), relies on the properties of certain materials to absorb ultraviolet (UV) radiation and consequently emit visible light. The phenomenon known as fluorescence can reveal details by highlighting differences in fluorescence between various substances. Indeed, by exciting in the UV range, parchment or paper supports show intense fluorescence (with a blue/green color) whereas the imprint of the lost ink appears as darker areas. The image acquired by using a

digital camera thus captures a high contrast between the two parts, allowing the reading of the lost text.

UVF was applied by Pottier et al., 2019, on 132 medieval parchment manuscripts made illegible after a fire in the Chartres library in France [4]. The advantages of UVF are the low-cost equipment, including a standard digital camera and lens, the rapidness of image acquisition, and the uncomplicated image treatment.

On the other hand, the UV-reflected (UVR) technique examines how the material reflects UV radiation by mounting a UV filter on the camera. For example, it is useful for identifying white pigments like titanium white and zinc white, which show a strong UV absorbance band [5]. Typically, UVR requires the use of specially developed lenses for UV photography and the removal of the internal UV-IR blocking filter from the digital camera. Cameras designed specifically for UVR are also employed.

According to Cosentino 2015 [5], both UVF and UVR methods are rarely conclusive; rather, they serve as the initial step toward implementing other techniques.

## 4. Multispectral Imaging (MSI) and Hyperspectral Imaging (HSI)

Multispectral imaging (MSI) is a widely employed technique with a rich history of application in the case of erased and partially legible texts. More precisely, in MSI, a series of images are captured in different spectral ranges with the use of bandpass filters or similar systems (Figure 1). The difference between this technique and photography with a common camera lies in the ability to select the radiation coming from the object, isolating single portions of the spectral range. For instance, in the case of dark spots covering the text, it is sometimes possible to select some spectral ranges in which they are transparent, allowing the ink to stand out [6].

**Figure 1.** (a) Photography of Parch. 38 belonging to the collection of the Library of the Department of History, Anthropology, Religions, Art History, Media and Performing Arts of Sapienza University of Rome; MSI with a UV source and filters at (b) 470 nm; (c) 500 nm; (d) 532 nm; (e) 600 nm; (f) 680 nm; (g) 700 nm; and (h) 750 nm. Reproduced under the terms of Creative Commons Attribution License 4.0 from [6].

Initial applications in the field involved the restoration of the illegible fragments of the Dead Sea scrolls [7,8] and the Petra Church scrolls [8,9], which had suffered from extreme degradation and a darkening of the parchment; in 1999, a similar technique was successfully applied to the reading of the carbonized Herculaneum papyri [10,11]. In all these works, the text contrast improves by selecting images in the infrared band, which are obtained through illumination using visible and infrared lamps.

Currently, two main MSI systems are utilized for text restoration. The first approach entails illuminating the manuscript with various sources, ranging from ultraviolet to

infrared, while selectively filtering wavelengths using camera-mounted filters [6,12–16]. The second system directly employs narrow-band light-emitting diodes (LEDs) to capture images across distinct spectral bands [17–22].

While multispectral imaging typically captures 10–20 images at specific discrete wavelengths, hyperspectral imaging (HSI) collects hundreds of images across a continuous spectrum of wavelengths. Despite their higher spectral resolution, HSI scanning systems tend to have a lower spatial resolution than that of MSI [23]. At present, there are fewer applications of hyperspectral imaging for illegible manuscripts, and they include medieval palimpsests [24,25]; manuscripts corrupted with accidents such as ink bleeding, ink corrosion, and the foxing age-related process of deterioration [26]; concealed parchments recycled in bookbinding [27]; Herculaneum carbonized papyri [28].

Advanced techniques in fluorescence hyperspectral imaging include the use of lasers as exciting sources such as laser-induced fluorescence (LIF). This technique has led to significant results for hidden texts in mural painting [29] and could be potentially useful for hidden inks [30].

In the case of overlapping writings, such as palimpsests, it may not always be feasible to identify a specific spectral range where the “upper text” becomes transparent with MSI, allowing the “undertext” to become legible. Recent works have focused on the leveraging of generative adversarial networks (GANs) [31] or deep learning-based semantic segmentation to disentangle complex nodes of overlapping letters (Figure 2) [32].

**Figure 2.** Examples of the prediction of a semantic segmentation model applied on a synthetic dataset of overlapping handwritten letters. In the top panels is the segmentation of complex combinations of A + C and D + E; in the bottom panels is the segmentation of complex combinations of B + C and A + D. To enhance visualization and explore potential patterns in noise residuals, the authors employ a min–max scaling technique for the color palette representation of predicted segmentation masks. Consequently, white pixels in each panel indicate zero flux, while black pixels represent the maximum flux in the mask. To facilitate a fair comparison between different masks and identify significant signals amidst noise residuals, histograms illustrate the distribution of maximum fluxes in each panel. Reproduced under the terms of Creative Commons Attribution License 4.0 from [32].

## 5. Macro X-ray Fluorescence (XRF) Imaging

X-ray fluorescence (XRF) is one of the most used techniques for the characterization of inks in manuscripts [33–35]. Although the technique is not sensitive to materials with low atomic numbers (for example carbon ink), it has been revealed to be suitable for the detection of iron-based materials, i.e., iron gall ink, and pigments composed of chemical elements with medium/high atomic numbers (i.e., mercury, lead, and copper). The development of high-performing scanning systems has enabled us to carry out macro XRF (MA-XRF)

imaging, discovering hidden texts on the basis of their elemental composition [36–41]. MA-XRF imaging has proven to be a successful approach when dealing with books made from recycled parchments that have suffered from darkening (Figure 3). Since iron-based inks were the most used writing materials during the Middle Ages [42], MA-XRF could map iron and other elements constituting the inks (e.g., calcium, zinc, copper, and manganese) for reconstructing the text, without any mechanical treatment of the books. This is possible because the support materials (i.e., parchment, papyri, and paper) are completely transparent to X-rays.

**Figure 3.** Distribution maps of calcium, iron, mercury L-lines and lead L-lines of parchment recycled into bookbinding. Reproduced under the terms of the Creative Commons Attribution 4.0 International License from [43].

Another application of MA-XRF imaging involves writings covered by a pictorial layer. The recovery of the text is possible because the chemical elements of the painting are different from those used for the hidden text [18,43]. Michelin et al., 2021 [44], reveal with MA-XRF the retouched secret correspondence of French Queen Marie Antoinette. The study demonstrates that macroscopic elemental mapping combined with principal component analysis (PCA) can be a powerful tool for unraveling the superimposition of iron gall inks when they have distinct elemental compositions.

More recently, MA-XRF has revealed the presence of ruling lines lead-drawn by ancient scribes for the layout of Greek papyrus rolls. This discovery defines the experimental proof that slanted text columns were an esthetic choice of scribes [45].

## 6. X-ray Tomography

XRF is limited to direct application on a specific page, necessitating the book to be opened. In cases where opening the book is infeasible, X-ray computed tomography (XCT) can be utilized as an alternative method.

In XCT, the image contrast mechanism is based on differential X-ray absorption within a compound object. Micro-computed tomography (micro-CT or micro-XCT) is a variant of XCT that generates significantly higher-resolution images of objects. One of the main experiments in the field is the first “virtual unwrapping” of the En-Gedi scroll, one of the oldest Hebrew Pentateuch scrolls [46]. The ink composition, which likely contains metal, has a density that can be detected using micro-CT. This technique enables the reading of text that is concealed within the charred scroll (Figure 4).

Bukreeva et al., 2016 [47], applied X-ray phase-contrast tomography (XPCT) to reveal carbon-based ink within the Herculaneum papyrus scrolls, buried and carbonized in the eruption of Mount Vesuvius in 79 A.D. As shown in this study, standard XCT is unsuitable for distinguishing carbon fiber-based papyrus from carbon-based ink used to write on papyrus. Contrast was only achieved by capturing the phase modulation induced by the object in a coherent or partially coherent beam [47]. The study unveils, for the first time, textual portions inside the rolled-up scrolls from the Herculaneum collectionexpanding on the groundwork laid by Mocella et al., in 2015 [48]. Their pioneering work not only showcased the benefits of employing XPCT but also shed light on the challenges associated with virtually unrolling the Herculaneum papyri. In 2023, Dr. Brent Seales and his team launched the “Vesuvius Challenge”, a machine learning and computer vision competition aiming to read the X-ray scans of scrolls performed by EduceLab. The challenge in comprehending the text content arises from the intricate geometric structure of the carbonized scroll. The authors identify three key phases that lead to the reading of rolled papyri: scanning, segmentation and flattening, and ink detection. The latter occurs after the identification and flattening of the layers of papyrus, leveraging the 3D scans of the scroll (https://scrollprize.org/ (accessed on 24 January 2023).

**Figure 4.** Complete virtual unwrapping of the En-Gedi scroll. Reproduced under the terms of Creative Commons Attribution Non-Commercial License 4.0 from [46].

In the last few years, the use of X-ray tomography for manuscript digitization has thus encouraged the development of algorithms to virtually unroll and unfold manuscripts that are too fragile and damaged to open [49–54]. In 2014, Ecole Polytechnique Fédérale de Lausanne (EPFL) and Ca’ Foscari University of Venice promoted the European project “Time Machine”, aimed at reading and digitizing a huge number of documents in diverse

types of formats using a compact, laboratory-based radiology system [55,56].

## 7. Infrared Thermography (IRT)

Pulsed IRT is a type of thermography where a pulsed heat source is used for external heating; the IR radiation emitted from the sample surface is recorded as a thermogram. This

technique has proven to be useful, especially for the inspection of subsurface elements [3]. In their work, Mercuri et al., 2013 [57], employed IRT to reveal fragments that had been inserted beneath the paper (Figure 5).

**Figure 5.** (a) Photograph of the paper guard of a seventeenth-century book; (b) a contrasted thermogram recorded just after the light pulse revealed a first written fragment concealed beneath the paper guard; (c) a contrasted thermogram recorded 300 ms after the light pulse revealed a second written fragment that belongs to a deeper subsurface, glued just beneath the previous one. Reproduced with permission from [3]; published by Taylor & Francis Ltd., 2020.

Pulsed IRT was also employed to reveal text beneath water stains in a thirteenthcentury manuscript [58]. According to Orazi 2020 [3], the IRT technique relies on different temperature values between the inked and non-inked areas originating from thermal contrast, making the text more readable.

## 8. Terahertz (THz) Imaging

Terahertz (THz) radiation, with its deep penetration capabilities, allows for nonionizing and non-invasive analysis. The successful acquisition of spectra has been achieved for writing materials such as iron gall inks, carbon-based inks, and traditional pigments commonly employed in manuscripts [59–67].

Due to the minimal attenuation provided by manuscript supports, THz radiation is advantageous for recovering hidden texts [68]. The versatility of sources and measurement geometry allows for a wide range of portable approaches.

The transmission configuration can be valuable in imaging single-sheet manuscripts and recovering underdrawings beneath ink layers [69,70] or seals [71] and detecting indentations, sieve lines, hidden watermarks or stains and alterations in aged materials [65,72,73].

THz reflection geometry is ideal for imaging layered archival documents. THz signals reveal signatures corresponding to reflections from various layers, allowing examinations of internal structures in optically opaque objects. The method is known as “time-of-flight”, and the pulse sequence provides information on the depth, position, and thickness of the inner layers [65].

Thus, it can resolve text from several layers of writing on papyrus and paper [16,60,74] and text on both sides of a single sheet [75], and reveal concealed writing under burned carbon black [65].

A THz tomosynthesis method based on a filtered back-projection algorithm allowed the recovery of graphite characters on paper up to the 50th layer [76], and the enhancement of the contrast for multiple-layered writings was successfully obtained [77,78] (Figure 6).

THz confocal microscopy has been recently applied to works of art [79] and has been able to reveal different inks used for music notes and pentagrams of a parchment manuscript [68].

The use of more powerful sources (i.e., quantum cascade lasers or Gunn diodes) combined with tomography can recover depth information overcoming possible limitations in the reflection mode [77].

THz cameras have already provided great advantages for imaging purposes in terms of discriminating between different materials, and they allow the real-time monitoring of the conservation state of artworks in a short amount of time [80,81].

**Figure 6.** (a) THz images from 25 layers of letters written with black gel pen on paper present excellent consistency and high contrast. The proposed methodology named pulse neighborhood average imaging (PNAI) can eliminate letter superpositions, and the quality of the resulting THz images is comparable with that of optical images of the letter on single sheets of paper. Images are normalized separately with the mean value set to 0.4. (b) The estimated signal-to-noise ratio (SNR) of THz signals for each layer and (c) the evaluation of THz image quality using the peak SNR obtained by various imaging algorithms highlighting that the PNAI method provides a substantial improvement in image contrast. Reproduced under the terms of Creative Commons Attribution Non-Commercial License 4.0 from [78].

## 9. Photoacoustic Imaging

Photoacoustic imaging applied to hidden text is a new research frontier. This technique is based on the absorption of pulsed light (i.e., laser sources) by a material, which determines the thermoelastic expansion of the surrounding environment and, consequently, a rapid pressure variation. The latter effect spreads as acoustic waves [82]. In the field of imaging applied to cultural heritage, the frequency range of the detected photoacoustic signals is in the ultrasonic interval (from a few up to several tens of MHz). As already demonstrated by the technologies that do not use visible light as a source, the main advantage of this technique is to provide high optical absorption contrast in an opaque matrix. Photoacoustic imaging takes advantage of light scattering, which enables the excitation of a broad volume, independent of the directions of the interacting photons [82]. Photoacoustic imaging has been demonstrated to be a good tool for the individuation of subsurface structures/underdrawings on pictorial tests [83] and for monitoring laser cleaning interventions [84]. Still, good results have been obtained from hidden texts of layered documents, both on single-sided printed paper sheets and in overlapping texts [85] (Figures 7 and 8).

These first experimental studies demonstrate the high potential of photoacoustic signals in revealing hidden text in multi-layered documents, by performing high spatial resolution and good contrast levels. Since the application of the photoacoustic effect in cultural heritage is still under study, multi-wavelength imaging setups and further geometrical, optical, and acoustic parameter configurations could provide promising developments in this context [85].

**Figure 7.** Photoacoustic imaging of a layered document with non-overlapping text; (a) representation of the sample; (b) photoacoustic images through top (XY) and side views (XZ; YZ). Reproduced with permission from [85];published by John Wiley & Sons Ltd., 2019.

**Figure 8.** Photoacoustic imaging of a layered document with overlapping text; (a) representation of the sample; (b) top view of a photoacoustic image; (c–g) individual reconstructions of five sequential pages. Reproduced with permission from [85]; published by John Wiley & Sons Ltd., 2019.

## 10. Not-Conventional Sources (Synchrotron Radiation, Ion Beam Analysis (IBA) and Neutron)

To reveal texts by detecting the distribution of an element, a powerful technique is the SR-based MA-XRF, which involves synchrotron radiation (SR) as an X-ray source. The use of SR permits a higher incident flux, flux density, and collimation, resulting in short acquisition times, as well as high-contrast and high-spatial-resolution images with respect to those obtained with conventional MA-XRF [27,86–94]. As a synchrotron X-ray technique, we also mention synchrotron X-ray diffraction, which has demonstrated high efficiency for the detection of minerals contained in pigments or inks [95,96] and for studying the support structure (i.e., parchment, paper, and papyrus) of inked regions [97,98].

In the infrared region, synchrotron infrared microspectroscopy has been used to study inks and ink–paper material interactions in order to investigate the presence of iron gall ink in degradation processes [93,99]; these studies may also be promising as mapping techniques.

Other non-conventional sources used for the elemental analyses of manuscripts are ion beams. Among the techniques utilizing ion beam analysis (IBA), there is the particleinduced X-ray emission (PIXE) [100]. This technique shows strong potential for the analysis

of manuscripts damaged by iron gall ink corrosion; indeed, PIXE mapping proves to be able to recognize heterogeneities of the elemental distributions of inks [101–103].

Finally, few studies have been reported about the use of neutron sources for the analysis of manuscripts and inks [104]. The interaction of neutrons with matter provides information about the elemental compositions of the inks. The advantage is that the captured and emitted particles are both highly penetrating and are used for the identification of major, minor, trace, and rare elements [105]. However, the possibility to detect hidden text is still not investigated, to the authors’ knowledge.

Although the use of non-conventional sources has many advantages for the detection of ink traces, generally, they are generated by particle accelerators, and this means that the artifact must be transported in the laboratory. However, for the PIXE technique, in recent years, a new portable particle accelerator has been developed [106], opening up new perspectives in the field.

## 11. Conclusions

In recent years, the digital restoration of historical manuscripts has emerged as a widely explored topic, as evident in the increasing number of related research projects and scientific publications.

This review comprehensively delves into various technologies, ranging from more conventional and well-known approaches like UV photography, multispectral and hyperspectral imaging techniques, infrared thermography, and X-ray tomography to less conventional yet promising methods such as terahertz and photoacoustic imaging, along with the utilization of synchrotron radiation, ion beams and neutron sources. A noteworthy advance among these unconventional methods is the ongoing evolution of technology, enhancing the portability of these techniques and thereby unlocking new potential applications in the digital restoration of manuscripts.

Notably, the ongoing strides in machine learning methods mark a significant advancement in addressing challenges related to the complex issue of ink detection, particularly in the case of palimpsests and carbonized papyri.

Author Contributions: Conceptualization, M.P.; methodology, M.P. and L.P.; writing—original draft preparation, M.P., L.P. and C.M.; writing—review and editing, M.P., L.P., C.M. and A.C.F.; supervision, A.C.F. and M.R. All authors have read and agreed to the published version of the manuscript.

Funding: This research received no external funding.

Data Availability Statement: Data sharing is not applicable.

Acknowledgments: We express our sincere gratitude to the ERC-PAGES project (AdG 2019 n◦882588) for its research support in the execution of this work. We heartily thank Anne-Sophie Gagnal, Pascaline Todeschini, Lise Marandet and Audrey Monet of the “Atelier de conservation-restauration du Service de Coopération Documentaire Interuniversitaire” of Université Paul Valéry- Montpellier 3 for their invaluable conservation expertise.

Conflicts of Interest: The authors declare no conflicts of interest.
