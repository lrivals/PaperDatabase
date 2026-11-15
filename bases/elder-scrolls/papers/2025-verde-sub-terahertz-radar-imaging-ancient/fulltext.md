---
id: 2025-verde-sub-terahertz-radar-imaging-ancient
title: "Sub-terahertz Radar Imaging of Ancient Herculaneum Papyrus Scrolls reveals Adhesion to Substrate after Unrolling"
year: 2025
backend: pymupdf
---

## Abstract

A frequency-modulated continuous-wave (FMCW) radar at 300 GHz mounted on a robotic arm has been used to image unrolled papyrus scrolls of the Hellenistic and early romanimperial age, recovered from the ashes of the volcanic eruption of 79 AD which buried Herculaneum and Pompeii. After their discovery at the mid of the 18th century, most of the scrolls were unrolled and glued on paperboard, mounted in wooden frames and, subsequently, in metal frames. The conservation challenge requires to map the adhesion points to the paperboard before intervention. Using Principal Component Analysis applied to the THz radar waveform raster, we have classified most pixels into “adhering” or “not-adhering”, also validating the classification with a ground truth experiment in one case. An explanation based on multiple scattering events of the PCA results is provided.

## I. INTRODUCTION

ERAHERTZ radars represent a promising new instrumentation class for imaging in the sub-millimeter wave range. High frequency circuits up to 0.3 THz are now available at silicon or silicon-germanium foundries. Integrated frequency multipliers and patch antennas can now be conveniently employed to obtain compact and low-cost radar chips. One of the notable advantages of THz circuits is the high absolute bandwidth which can be more than 50 GHz at 0.3 THz. In the frequency-modulated continuous-wave (FMCW) radar architecture, this high bandwidth translates into a high Zresolution smaller than the wavelength (i.e. less than 1 mm) [1]. High numerical aperture lenses can be used to match this resolution with optically thin focal planes, thereby enabling the analysis of thin samples, for example paper sheets, mail and, in this case, unrolled papyrus scrolls.

The Plinian volcanic eruption of Mount Vesuvius in 79 AD covered the town of Hercolaneum with pyroclastic materials, preserving many objects of daily life in ancient Rome from degradation [2]. In the 18th century, a papyrus scroll collection containing philosophy writings was discovered, carefully unrolled and subsequently glued on either wooden or cardboards and stored in wooden or metallic frames [3]. It was partly deciphered, but a large part of the collection is still to be unrolled and/or deciphered, and the already-unrolled scrolls must be preserved.

Attempts to detect textual portions inside unopened papyrus scrolls without unrolling them have been made with X-ray phase-contrast tomography [4]. THz-time-domain imaging has been used to study papyrus phantoms [5]. THz radar imaging, however, may also be used to assess the preservation state and

guide conservation interventions. We then analysed through a sub-THz radar (TeraScan Arm 300 by Lytid sas, France) some unrolled papyrus fragments kept in the National Library ‘Vittorio Emanuele III’ of Naples, Italy, in the framework of the ERC Advanced Grant 885222-GreekSchools.

## II. RESULTS

The 0.3 THz FMCW radar had a bandwidth of 27 GHz and a pair of Teflon lenses with focal length f=37 mm and diameter D = 45 mm (N.A.>0.5) enabling measurement of thin layers. The digital ranging (Z) resolution was 0.35 mm, and the optical focal plane thickness can be estimated around 2 mm. Radar images were obtained by scanning a robotic arm (TeraArm by Lytid sas) in the X and Y directions with steps of 1 mm in backscattering configuration. For optimal signal intensity and contrast, the working distance was kept slightly smaller than the focal length of the lens. The real sub-surface distance (in nondestructive testing, this quantity is the Z-position of the focal plane with respect to the main physical surface of the sample) varied from -5 mm to +5 mm in different measurements. Areas of approximately 100x100 mm2 were investigated in approximately 2 hours, which is an acceptable time for the

Federica Verde1, Sofia Ceccarelli2, Valeria Giliberti3, Francesco Vitucci4, Costanza Miliani2,

Graziano Ranocchia2,5 and Michele Ortolani1,3 1Sapienza University of Rome, Department of Physics, 00185 Rome, Italy 2CNR – Istituto di Scienze del Patrimonio Culturale, 80134 Naples, Italy 3Istituto Italiano di Tecnologia, Center for Life Neuro and Nano Sciences, 00161 Rome, Italy 4Crisel Instruments srl, 00167 Rome, Italy 5University of Pisa, Dipartimento di Filologia, Letteratura e Linguistica, 56126 Pisa, Italy.

Sub-terahertz Radar Imaging of Ancient Herculaneum Papyrus Scrolls

reveals Adhesion to Substrate after Unrolling

T

**Fig. 1.** Picture of the 0.3 THz FMCW radar and Teflon lenses mounted on a robotic arm (TeraArm 300 by Lytid sas), installed at the Officina dei Papiri of the National Library in Naples, Italy, and used to image an unrolled papyrus scroll more than 2000 years old.

Authorized licensed use limited to: ISAE. Downloaded on November 15,2026 at 20:02:05 UTC from IEEE Xplore. Restrictions apply.

proposed application (a major fragment, slightly larger than a DIN A4 paper sheet, can be investigated in one working day).

The typical noise floor was -30 dB from the main scattering peak, always located close to Z=0.

The acquired radar waveforms have been pre-processed and only the central portion was analyzed (100 Z-slices corresponding to 35 mm of total depth range). A principal Component Analysis (PCA) was applied to simultaneously analyze the entire waveform of all pixels in the image, and the first two components were considered. The first component PC1 is the average scattering cross-section vs. Z, showing a peak at Z=0 that represents the main physical interface between paperboard and air, while the second component PC2 is found to change sign approximately at Z=0. Therefore, the weight of PC2 represents the amount of scattering with longer delay than

the central PC1 peak (main physical surface) compared to the scattering with shorter delay.

A simple way to represent the PCA and derive relevant information for conservators to classify the pixels in two clusters according to their PC1 and PC2 weights. The K-means algorithm was used, and two clusters were obtained in Fig. 2(c). The blue and red pixels in Fig. 2(b) correspond to the best Kmeans classification. Remarkably, the map in Fig. 2(b) mostly shows red and blue areas elongated in the longitudinal direction perpendicular to the scroll rolling direction (horizontal direction in Fig. 2). This suggests that the THz radar imaging is capable to identify areas of the unrolled papyrus that share similar mechanical and substrate-adhesion features, even if these areas do not show any clear difference in the visible image of Fig. 2(a), as expected. A visual inspection was carried out as “ground truth” to identify the attached and detached areas of the papyrus from the paperboard. From the comparison of visual inspection with the results reported in Fig.2(b), it turned out that blue pixels (high PC1 weight, i.e. high scattering cross section) correspond to the detached areas. On the other hand, red pixels in Fig. 2(b) include all firmly adhering areas (although not necessarily glued, as the actual glued portions are extremely small if compared to the papyrus area and now it does not seem that we can classify them separately). It is likely that the detached papyrus portions will scatter more the 0.3 THz radiation than the firmly attached portions. By observing Fig, 2(c), where the broader distribution of PC2 weights for the blue cluster (not adhering) than for the red cluster (adhering) is reported, we hypothesize that it is due to an increased variety of multiple scattering events between the detached papyrus and the paperboard in the not-adhering areas.

The PCA results are relevant for conservation efforts, as the adhesion of papyrus areas to the paperboard could be analyzed automatically by non-expert personnel trained to use the preconfigured THz imaging radar. The aim is to monitor the preservation state, avoid complete detachment, and follow possible changes of adhesion with time and with changes in environmental parameters.

## III. SUMMARY

Sub-terahertz (0.3 THz) radar imaging of unrolled papyrus scrolls has revealed relevant information for their conservation, obtained by a Principal Component Analysis of the FMCW radar waveforms.
