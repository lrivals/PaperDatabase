---
id: 2012-mills-apocalypto-revealing-unreadable
title: "Apocalypto: Revealing the unreadable"
year: 2012
backend: pymupdf
---

Apocalypto: Revealing the unreadable

David Mills1, Oksana Samko2, Paul Rosin2, Kate Thomas3, Tim Wess3, Graham Davis1

Keywords: tomography; microtomography; parchment; iron gall ink; x-ray; virtual unrolling

## Abstract

Stored in various public archives and private collections around the world, there are untold numbers of documents whose content is lost to memory and history. They cannot be read by normal means, because the parchment and paper they are written on has degraded; any attempt to handle or process the document for reading will at the very least cause it permanent damage.

One of the prime catalysts of document degradation is the iron gall ink used in their writing; this provides a contrast for X-Ray imaging. The low attenuation produced by the tiny quantities of iron and other metals in the inks requires a system with a very high contrast ratio and excellent immunity from artifacts to enable ink imaging. The new generation XMT TDI scanner being developed at Queen Mary fulﬁlls these criteria.

A 3D volumetric dataset produced by XMT scanning the document is modeled and digitally re-created, producing a readable image of the text. The post-processing is performed in six stages, noise removal, data segmentation, surface construction, ﬂflattening, data projection and image generation.

The scanning process takes upwards of a day, so it is important that the documents are not damaged by long exposure to the X-Ray ﬂflux. Investigations ongoing and due to be be published have shown no detectable extra damage to either old or modern scanned parchment.

## 1. INTRODUCTION

Parchment and iron gall ink have been used for centuries in the western world as primary non-volatile data storage in the legal and ecclesiastical sectors1-2. It is truthful to say that the history of the western world is written on parchment. Parchment is still used today to record British Acts of Parliament.

Parchment is an animal-derived material composed primarily of collagen. It di'ers from leather in that it is not stabilized by tanning, this leaves parchment much more sensitive to the ambient environment.

The principal component of parchment is collagen in the form of a triple helix backbone with various sidechains3. The structure is stabilised by hydrogen bonding and van der Waals interactions between side-chains. Many processes can denature the side-chains leading to a change or loss of the stabilising bonds, converting an ordered collagen structure into disordered gelatin. This change at the microscopic level is observed as shrinkage and increased fragility of the macroscopic parchment object. As damage compounds upon damage, a parchment object can eventually become unusable. If the object is a scroll or piece of folded parchment, degradation can cause the layers to adhere to each other rendering the object solid and unreadable5.

Iron gall ink is an iron-tannin complex pigment long known for its permanence and water resistance. The recipe and method of production of ink varied from producer to producer and over time, the only constants being a source of iron and a source of tannin4 (often derived from oak trees and oak apples). Under certain conditions excess Fe2+/3+ and copper ions in the ink on a document can catalyse the denaturing reactions in collagen, greatly speeding up the degradation of parchment in the area around script6. However, it is the presence of iron and other metals that provide the contrast required for X-Ray imaging.

The School of Medicine and Dentistry at Queen Mary University of London (formerly: London Hospital Medical College), is the birthplace of X-Ray microtomography7, and has been at the forefront of developing extremely high dynamic range scanners8 and development of the time-delay integration (TDI) technique as a

1. Institute of Dentistry. Queen Mary University of London. London E1 4NS. 2. School of Computer Science & Informatics. CardiﬀUniversity, Cardiﬀ, Wales. 3. School of Optometry and Vision Sciences, CardiﬀUniversity, Cardiﬀ, Wales.

Developments in X-Ray Tomography VIII, edited by Stuart R. Stock,

077171

GO

B Srnrn

means of eliminating ring artifacts (allowing increased signal to noise ratio) and increasing image ﬁfield size beyond the physical dimensions of the CCD sensor9. The combination of TDI scanning and high dynamic range camera gives images with random noise levels similar to those obtained by synchrotron XMT, but free from artifacts and with a larger ﬁfield of view (but much slower of course). These series of scanners are being used for imaging in a wide variety of ﬁfields including in-house dental research, paleontology, medicine, biology and engineering.

## 2. THE NORFOLK RECORD OFFICE SCROLL

A small (100 x 10 mm) parchment scroll was obtained from the Norfolk Record O(ce⇤conservation teaching collection, this is shown in Figure 1. The ink was known to be iron gall, the parchment was dated to around 1850 and had been tightly rolled and dehydrated. The dryness of the parchment precluded unrolling it without causing damage. An initial X-Ray survey of the scroll showed a metal foil along one edge, as well as a number of high-Z inclusions either in the ink or as dust trapped and adhering to the parchment surface.

**Figure 1.** The Norfolk Record Oﬃce scroll, as photographed at time of donation

The scroll was sealed in a polypropylene tube with an internal diameter slightly larger than the external diameter of the scroll. This was then stored at 22 ºC to acclimatise and allow the parchment to relax into the container dimensions. The total scanning time was 36 hours; a total of 7707 projections were recorded at a voxel size of 15 microns . Reconstruction was performed with a GPU implementation of the cone beam ﬁfiltered back-projection algorithm.

Exploration of the dataset using TomView and Drishti conﬁrmed we had successfully detected the ink and that artifacts from the foil strip were minimal, see Figure 2. The very tight rolling of the scroll did not lend itself to easy manual text extraction using the aforementioned tools; the data was passed to colleagues at Cardi' University to produce a virtual unrolled scroll.

Approximately one week of processing with in-house developed tools was required by the Cardi' team to produce a ﬂat, unrolled, readable image of the scroll, this is shown in Figure 3. The most challenging part of the virtual unrolling is segmentation; tracking the surface of the parchment as it curves, deciding where one

⇤Norfolk Record Oﬃce The Archive Centre Martineau Lane Norwich NR1 2DQ

-.

rÖG;

>ó:Ltí.!.`4?ñ: .fir cÁ31

**Figure 2.** Ink detected on the Norfolk Record Oﬃce scroll

**Figure 3.** The “virtual unrolled” Norfolk Record Oﬃce scroll

surface ends and another starts when surfaces are touching; a combination of automatic methods and manual intervention succeeded in segmenting the data correctly. A full description of this work will be presented in a forthcoming paper.

After the virtual unrolling results were obtained, it was decided to seek the advice of a specialist parchment conservator to determine the feasibility of physically unrolling the parchment to conﬁrm the interpretation of the writing. Permission for this was granted by the Norfolk Record O(ce. The scroll was treated in the conservation studio at Camberwell†, humidiﬁed, unrolled, ﬂflattened and mounted for display. The images clearly show the successful extraction of text from a damaged parchment scroll with no prior knowledge of the content.

## 3. DAMAGE INVESTIGATIONS

It is of supreme importance to the archives and libraries submitting objects to be scanned that the scanning process causes no damage. XMT when applied to non-living samples is for the most-part a non-invasive, nondestructive technique. However, the energy contained in any X-Ray photons absorbed by the sample has to go somewhere; it can either heat the sample or directly drive chemical processes in the sample. Neither of these options is ideal when dealing with fragile, degraded and environmentally sensitive materials like parchment.

The most obvious (and damaging) ways in which X-Ray photons can cause chemical interactions in the parchment are via direct leakage of the collagen helix, or production of free radicals that then go on to attack the collagen. Free radical production is minimized in dry samples; visible darkening seen after a 6 hour scan of a

†Camberwell College, University of the Arts, London

7." L, PIY-iy 71-?"02 51-,1774V--t7",`),),-- ,,y) iv), 1/7) 41,,,ty-- Ì,J,...2.(1/,19-fr / 12,7 p iry ,z-4 a -,9-,,-..--- ,--- 6 / / 74', rj)4,41),) II //?2/ #41,2,/fry0 r)",),-14y /WV/0'V r" t

124-0-17.-0 7,-029 , Jr_ flow i.0.----/ti_y)9.,Ì.,-,-..)-7.7-77/4,27,--d ,.24,0- 4".7,,wwv A,

?) rktgy,77),,,9- 417v -.").>-(y--,12//

\ -

2-, ,1144,0-PV/1.-Wika)y71.-iF /0W/

f

jzati.-7,1 '7 0 .-/-;---23-P)-2) 7/9 r6,71/

WOO -

**Figure 4.** The physically unrolled Norfolk Record Oﬃce scroll

water saturated parchment test sample has not been observed in any subsequent scans of dry (native state, not dehydrated) material.

Preliminary studies have indicated that the magnitude of X-Ray damage on dry collagen samples is very limited6. This was ascertained using samples subjected to highly focused X-Ray beams, where multiple exposures at speciﬁc sites showed no or minimal degradation of the di'raction signal. Further studies have been conducted to determine the optimal conditions under which the XMT procedure should be carried out. In addition to X-Ray di'raction studies both, Fourier transform-infrared spectroscopy (FTIR) and biochemical analysis studies have been utilised. Principal Component Analysis of the FTIR spectra demonstrated no visible alteration in the collagen signal when comparing native parchment samples to parchment samples exposed to a dose of X-Rays. These structural studies have been complemented by cross-biochemical analyses where preliminary studies have demonstrated no visible alteration within the collagen on exposure to a dose of X-Rays. Further studies are being investigated and are due to be published.

## 4. FURTHER WORK

Until recently document scans were performed on our MuCAT2 scanner, a device optimised for hard tissue scanning and with a restricted ﬁfield of view. Completion of the new equiangular scanning geometry MuCAT3 system10 will enable the scanning of signiﬁcantly larger objects and allow more time to be devoted to scanning material for the Apocalypto Project.

We are undertaking outreach work to archives and libraries to introduce the technique to archivists and conservators with the aim of establishing a continuous supply of material for imaging, thereby allowing heritage researchers virtual access to unreadable and degraded materials.

## 5. ACKNOWLEDGMENTS

This work is funded by the Engineering and Physical Sciences Research Council EP/G007845/1.

We wish to thank Spectral Instruments Inc and Physik Instrumente GmbH & Co. KG for their help and assistance with development of the scanning hardware. Ajay Limaye for the Drishti volume exploration software.

Antoinette Curtis and John Alban at the Norfolk Record O(ce for donating the parchment samples and informative discussions. Special thanks and acknowledgement is given to Stephen Figaro for technical support and Meagen Smith for conservation support and consultancy.
