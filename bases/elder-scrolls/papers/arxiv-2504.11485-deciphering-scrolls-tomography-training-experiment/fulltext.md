---
id: arxiv-2504.11485-deciphering-scrolls-tomography-training-experiment
title: "Deciphering scrolls with tomography: A training experiment"
year: 2025
backend: pymupdf
---

Deciphering scrolls with tomography: A training experiment

Sonia Foschiatti1

sonia.foschiatti@univie.ac.at

Axel Kittenberger1

axel.kittenberger@univie.ac.at

Otmar Scherzer1,2,3

otmar.scherzer@univie.ac.at

1Faculty of Mathematics University of Vienna Oskar-Morgenstern-Platz 1 A-1090 Vienna, Austria

2Johann Radon Institute for Computational and Applied Mathematics (RICAM) Altenbergerstraße 69 A-4040 Linz, Austria

3Christian Doppler Laboratory for Mathematical Modeling and Simulation of Next Generations of Ultrasound Devices (MaMSi) Oskar-Morgenstern-Platz 1 A-1090 Vienna, Austria

## Abstract

The recovery of severely damaged ancient written documents has proven to be a major challenge for many scientists, mainly due to the impracticality of physical unwrapping them. Non-destructive techniques, such as X-ray computed tomography (CT), combined with computer vision algorithms, have emerged as a means of facilitating the virtual reading of the hidden contents of the damaged documents. This paper proposes an educational laboratory aimed at simulating the entire process of acquisition and virtual recovery of the ancient works. We have developed an experimental setup that uses visible light to replace the detrimental X-rays, and a didactic software pipeline that allows students to virtually reconstruct a transparent rolled sheet with printed text on it, the wrapped scroll.

## 1. Introduction

In recent years there has been a growing interest in the recovery of ancient written documents that have been damaged by time, inadequate storage conditions, chemical corrosion, and misguided attempts to open them. For instance, papyrus sheets, produced from the papyrus plant, were a widely used writing surface for documents in antiquity. However, the surviving scrolls and fragments require specific climatic conditions for their preservation. High levels of humidity can cause severe deformations in their layers, altering the written content. In such cases, physical unwrapping is not feasible as it increases the risk of permanent damage. Moreover, for other materials such as parchment, wood, and bamboo, the physical cleaning processes can lead to material degradation and require a substantial time investment.

Recent advancements in the field of computer science, particularly in the areas of image processing and computer vision, have paved the way for virtual restoration of damaged documents avoiding physical unwrapping, a process called virtual unwrapping. The term "virtual unwrapping", adopted from [15], refers to the use of software to reveal on a computer screen words and texts hidden for centuries, thereby making the content accessible to all. Virtual reconstructions are based on data acquired through various tomography modalities. The term "tomography" derives from the Greek word "tomos", meaning "slice", and can be defined as a method of imaging by sections using any type of penetrating wave. The employment of X-ray tomography in the recovery of ancient manuscripts can be attributed to the non-destructive and non-invasive nature of X-ray radiation. Its application to paleontology and archaeology can be traced back to the early 20th century, as evidenced by the use of these imaging techniques to reveal ancient texts buried in altars, or rolled silver scrolls, sealed letters, damaged manuscripts from ancient libraries, and carbonized scrolls that have been discovered in the Villa of the Papyri near Herculaneum, Italy [8].

In this note, we present a didactic experiment for the virtual restoration of text printed on a transparent scroll. Drawing inspiration from the intriguing archaeology application, we have developed an educational laboratory for teaching X-ray tomographic reconstruction of written documents. This initiative is particularly well-suited for undergraduate courses in applied mathematics, physics, or archaeology, as well as Maker Fairs or science communication workshops. As previously stated, X-ray tomography is

a well-established imaging technique that, in the field of archaeology, allows scientists to read hidden text without damaging the actual document. In our experimental setup, we employ visible light as a surrogate to simulate the potentially detrimental X-rays. This approach is based on the premise that the propagation characteristics of electromagnetic waves, despite their different wavelengths, can be described by analogous mathematical formalism. Within our experimental framework, the wrapped scrolls are composed of transparent cellulose acetate sheets, which exhibit minimal interaction with visible light. The idea of employing a transparent film and the light as an illumination source to simulate X-ray tomography in an educational setting was initially proposed by Kittenberger et al. [6].

**Figure 1.** The Greek phantom scroll.

The present educational experiment further extends the ideas outlined in [6], using a setup comprising a light source, a stepper motor and a digital camera. To simulate the ancient writings, a Greek text from Homer’s Hymni Homerici XV (VII-VI century BC) and a Latin text from Lucrezio’s De Rerum Natura have been printed on a transparent film (see Figure 1). The objective of this experiment is twofold: firstly, to stimulate undergraduate students’ or amateurs’ interest in the fascinating field of applied mathematics, which intersects pure mathematics, computer science, numerical analysis and physics; and secondly, to provide instructors with an inspiring application of X-ray tomography that can be used to develop students’ problem-solving abilities and scientific thinking.

The Archeolab website (https://csc1.gitlab.io/archeolab/) has been developed as a virtual guide to assist students and instructors in the reconstruction of their own scrolls. It provides documentation of the Python and Matlab code, in addition to the theoretical foundations.

## 2. X-ray tomography in a nutshell

X-ray computed tomography (abbreviated as X-ray CT) is a non-destructive imaging technique used to visualize the internal structure of an object. The key observation granting the success of this approach is that different materials exhibit differed absorption and scattering properties when interacting with X-rays. They pass through the majority of materials (e.g., most of the objects are transparent to them), enabling the clear identification of internal structures of interest through contrast imaging and algorithms. From a physical point of view, in the electromagnetic spectrum X-rays are characterised by shorter wavelengths than visible light, ranging between 10 nanometers and 10 picometers.

From a mathematical perspective, the problem of recovering the attenuation coefficients of an object is formulated as the problem of determining a function from the knowledge of its line integrals. The first solution to this problem was proved by Johann Radon, an Austrian mathematician who derived the first reconstruction formula in his 1917 paper [13].

The first documented application was by Bracewell in radioastronomy in 1956 [1], who sought to reconstruct a map of the solar microwave emissions from a series of radiation measurements across the solar surface. In the same years, the the South African-American physicist Allan M. Cormack made a significant contribution to the field of cancer treatment by radiation therapy. In 1955, he spent a day and a half a week at Groote Schuur Hospital in Cape Town, South Africa. During this period, he observed the planning of radiotherapy treatments, and recognized the importance of determining the attenuation coefficient of the object. During his sabbatical year at Harvard in 1956, he derived a mathematical theory for image reconstruction. Subsequent to his return to South Africa in 1957, he proceeded to test his theory on a 5-cm-thick disk measuring 20 cm in diameter composed by different materials in order to simulate the skull. Thanks to its radial symmetry, only one measurement at one angular position was needed, and the attenuation coefficient was calculated applying the formulas derived by Allan M. Cormack.

The development of the first clinical CT scanner was initiated in 1967 by Godfrey N. Hounsfield at the Central Research Laboratories EMI in England. Hounsfield, independently of Cormack, deduced that X-ray measurements of a body taken from different directions would allow the reconstruction of its internal structure. In 1979 Allan M. Cormack and Godfrey N. Hounsfield were jointly awarded the Nobel Prize in Physiology and Medicine for their seminal contributions (see [5] for the complete history).

In the field of archaeology, the detrimental X-rays are employed to examine scrolls without the need for invasive physical interaction, thereby preserving their integrity. An X-ray experiment comprises a source, a detector, and the object to be imaged. During the scanning process, a source emits one or more thin X-ray beams, modelled as straight lines. When the beams encounter the object, their intensity decreases as they interact with its electrons. Detectors placed opposite the sources measure the intensity diminution. In CT, each X-ray image captured at a fixed angle is called a projection. A series of projection data is acquired by rotating the X-ray sources and detectors around the body, which is motionless. By acquiring a sufficient number of projections, it is possible to reconstruct multiple cross-sections, or slices, of the three-dimensional object, resulting in a volumetric representation of the body called volumetric data or volumetric image. The information regarding location and intensity is saved in a single unit called a voxel, which represents the three-dimensional counterpart of the two-dimensional pixel. The slices represent a map of the spatial distribution of the attenuation coefficient of the object.

The process of extracting hidden text from volumetric X-ray CT scans of the objects of interest using computer vision algorithms is often referred to as a software pipeline or workflow. To illustrate this process, we will refer to a successful application of the virtual pipeline, the digital reconstruction of the En-Gedi scroll presented in [15]. In 1970, several fragments of carbonized parchment were unearthed at the archaeological site of En-Gedi, west of the Dead Sea, in an altar. These fragments are pieces of charcoal, some of which have undergone disintegration and deterioration due to human interaction and other agents over time. The data collected are volumetric X-ray micro-CT scans which provide high-resolution greyscale cross-sections of the body. These images facilitate the distinction of the internal layers of the scroll. The team led by Professor W. B. Seales developed a virtual pipeline with the objective of recovery the concealed text of the scrolls without altering them. The full process consists of the following four steps: segmentation, flattening, texturing, and merging. The initial step, segmentation, involves the identification of layers in each slice of the volume (e.g., the isolation of thin, warped regions of interest). This operation poses a significant challenge due to the presence of noisy measurements in the scans derived from the animal’s skin. The result of this initial phase is a segmented surface representing a layer of the scroll. The subsequent step is texturing, which consists in assigning the intensity values to the corresponding points on the segmented surface. The subsequent step is flattening, and consists in mapping the three dimensional wrapped segmented surface onto a two-dimensional image. Finally, the different segments of the flat surface obtained from the slices are merged to create an image of the entire readable scroll.

Virtual extraction of hidden information often requires user interaction during the segmentation step, a process that could be time-consuming in the long term. A novel approach to overcome this difficulty involves automated segmentation in conjunction with Machine Learning algorithms. In March 2023, the same research group initiated a challenge to develop a fully automated virtual pipeline to disclose ancient carbonized scrolls [17]. The Vesuvius Challenge is a Machine Learning and computer vision competition, with the objective of developing an automated software pipeline capable of reading the hidden text of

ancient carbonized scrolls discovered near Herculaneum, Italy. Let us travel back in time to the thriving years of Roman empire when a cataclysmic event happens. In 79 AD there was a devastating eruption of Mount Vesuvius; the towns of Herculaneum and Pompeii along with their buildings and palaces were covered by pyroclastic flow, reaching depths of up to 30 meters. Among them was the villa of Lucio Calpurnius Piso Pontifex, the father-in-law of Julius Caesar, buried under the ashes. The luxurious villa, known as the Villa of the Papyri, contains the only complete library of the Greco-Roman world that has survived to the present day. For centuries, the villa and the other building remained noiselessly concealed beneath the ashes, their existence obscured, until the mid-eighteenth century. Around the year 1750 AD, an Italian farmer, while digging a well, uncovered marble pavements, opening the way to possibly groundbreaking archaeological discoveries. The first excavations on the site were conducted by the Swiss architect Karl Weber between 1750 and 1765, employing tunnels. During these excavations around 1,800 carbonized scrolls were disinterred, referred to as the Herculaneum papyri. Ingenuous attempts to open them caused the irremediable loss of ancient books along with their content. It seemed that the text of those manuscripts would have been undisclosed for centuries. Fortunately, the advancements in science and technology have allowed us to aspire to reveal once and for all the concealed text of the Herculaneum papyri. The same group led by Professor Seales conducted X-ray data acquisition from 2010 to 2020 using different X-ray CT machines, collecting the volumetric images in the EduceLab dataset. The acquired data encompasses two types of imaging: besides the volumetric X-ray micro-computed tomography, employed to image the entire collection (e.g., intact scrolls and detached scroll fragments), it includes spectral imaging of surface fragments, used to detect the presence of exposed ink on the surface [12].

Many amateurs and scientists have participated in the challenge, which has captured the attention of the media and the general public. In 2024, a significant discovery was made by the 21-year-old computer scientist Luke Farritor, who was able to identify the word πoρφνραζ meaning "violet" (color or tissue). Another recent discovery from the Herculanei scroll is a newly deciphered passage from a scroll written by Philodemus of Gadara, which reveals details about the lost tomb of the Greek philosopher Plato [16]. It is still possible to take part in the challenge, and rich prizes are awarded each month for relevant contributions to the software pipeline.

## 3. Experimental setup

The groundbreaking discoveries and achievements that have followed the development of X-ray CT have motivated us to develop a didactic laboratory that allows students and amateurs to tackle the same problem that Johann Radon, Allan M. Cormack and Godfrey N. Hounsfield solved with a focus on the archaeological application.

In the preliminary part of the laboratory, the acquisition of X-ray projections of an ancient written document is simulated. In out setup, we consider two phantoms, representing the scrolls, composed of thin cellulose acetate (CA) sheets, each of size 21 cm x 15 cm. To simulate the text of Herculanean scrolls, Greek and Latin texts have been selected for printing. The first phantom features text from Hymni Homerici XV - In Herculem, verses 1-3:

῾Ηρακλέα Διὸς υἱὸν ἀείσομαι, ὃν μέγ’ ἄριστον γείνατ’ ἐπιχθονίων Θήβῃς ἔνι καλλιχόροισιν ᾿Αλκμήνη

μιχθεῖσα κελαινεφέϊ Κρονίωνι

ὃς πρὶν μὲν κατὰγαῖαν ἀθέσφατον ἠδὲθάλασσαν πλαζόμενος πομπῆισιν ὕπ᾿Εὐρυσθῆος ἄνακτοςπολλὰμὲν

αὐτὸς ἔρεξεν ἀτάσθαλα, πολλὰδ᾿

ἀνέτλη·νῦν δ᾿ἤδη κατὰκαλὸν ἕδος νιφόεντος ᾿Ολύμπουναίει τερπόμενος καὶἔχει καλλίσφυρον ῞Ηβην.

The second phantom features text from De Rerum Natura by Lucretius, verses 72-74:

Ergo vivida vis animi pervicit, et extra

processit longe flammantia moenia mundi

atque omne immensum peragravit mente animoque

unde refert nobis victor quid possit oriri,quid nequeat, finita potestas denique

The original texts can be found in [4].

**Figure 2.** The experimental setup (top: schematic, bottom: our build).

The experimental setup consists of an Arduino, a breadboard, a computer, a digital camera, a Fresnel lens, hook-and-loop tape, a paper sheet, a projector, a stepper motor, and mounting structures for the lens and paper sheet. In this case, the structures were constructed using cardboard and wooden beams (see Figure 2). To avoid fused layers in the reconstruction, the hook-and-loop tape is applied to the phantoms, which are then wrapped. The phantoms are mounted on a pulley, which is screwed onto the axle of a NEMA 17 stepper motor. This is either glued to a base or clamped in a vice to provide a stable vertical axis of rotation, oriented orthogonally to the stage. The complete setup is illustrated in Figure 2.

The structure is illuminated by a projector, with a 30 cm x 30 cm PMMA Fresnel lens placed at a distance determined by the lens’s focal length (60 cm in this case). The use of a Fresnel lens serves to mitigate the parallax effect, which otherwise leads to the formation of significant artifacts in the reconstruction. A white paper acts as the canvas for the experiment. On the opposite side of the canvas, a digital camera is positioned as the detector. A USB cable connects a personal computer and the board controller, with the Arduino controlling the motor stepper via an A4988 driver. The computer controls the Arduino and the digital camera, which is connected to it via a USB cable, using the Canon Hack Development Kit (CHDK) [2]. All the relevant scripts can be found at https://gitlab.com/csc1/archeolab/.

The experiment starts with the acquisition of the projection data. The CA phantoms are rotated at a frame rate of 0.44 fps around 360◦, for a total of 30 minutes for 800 shots. The total number of projections acquired is N = 800. In this particular instance, the remote-shoot function of the CHDK is used to transfer the images to the PC.

## 4. The virtual unwrapping

In the subsequent stage of the practical laboratory session, students will be instructed in the utilization of the virtual pipeline employed for the reconstruction of the contents of the transparent scrolls. The main algorithms employed in this process are the Filtered Back Projection algorithm and the Maximum Intensity Projection (MIP) method. The only manual step required by the user is the definition of a set of control points, termed ’individuals’, describing a first rough approximation of the spiral-shaped layer of the scroll, which is subsequently optimized to obtain the best fit. The measurements are derived from the projections of the transparent scroll on the canvas (see Figure 3).

The virtual workflow commences with the determination of the axis of rotation of the scroll with the call of the script guiAxisFinder. After loading the projections, the GUI (graphical user interface) takes the first image at index i and its 180° counterpart. Subsequently, the images undergo a series of pre-processing

**Figure 3.** Projection on the white screen.

steps (i.e., cropped based on a central point, rotated and cut). In the ideal case, where the center and the axis of rotation are configured correctly, the first image and the second flipped should overlap perfectly, resulting in a uniformly black image. However, in practice, the user observes green and red regions in the plotted image, which correspond to negative and positive pixel intensity differences between the two images, respectively. The process of minimizing these differences serves to converge to the actual rotation axis.

Following this step, the projections are associated with the correct rotation axis, loaded and elaborated to obtain a stack of pre-processed projections. At this point, Filtered Back-Projection is performed, with the stack of pre-processed projections from the previous step serving as the input. The iradon function is then applied with linear interpolation and the Ram-Lak filter as options, which are more suitable for edge detection. The iradon function in MATLAB is available in the Image Processing Toolbox, in Python in the skimage library. The result of this step is a stack of cross-sections of the original scroll, where the layers of the scroll can be seen (see Figure 4). After Filtered Back-Projection, a mask is implemented to remove artifacts from the central and external regions of the slices.

Subsequently, the script guiSegment is invoked to perform manual segmentation. The user then inserts a set of initial control points on a selected cross-section of the scroll, drawing a spiral-shaped curve that follows the layers of the scroll. A genetic algorithm is then employed to optimize the manual segmentation. Subsequently, a cubic smoothing spline through the control points is calculated and sampled to obtain a set of points for plotting.

The final step involves the implementation of the Maximum Intensity Projection (MIP) method, which reveals the hidden text of the scroll. The MIP method selects the maximum intensity value I(x, y, z) from the voxels V (x, y, z) for a fixed pair of coordinates (x, y):

MIP(x, y) = max

I(x, y, z). (4.1)

This method projects the maximum intensity values onto a plane, thereby facilitating the visualization of

**Figure 4.** Cross-section of the transparent scroll (inverted) with a segmented path.

**Figure 5.** 3-D view of the Greek phantom scroll.

the text. The reconstruction of the Greek and Latin transparent scroll is shown in Figure 6 and 7, and a three dimensional view of the Greek scroll in Figure 5. Despite the presence of artifacts, most of the Greek and Latin letters are legible without the application of any post-processing steps.

As illustrated in the figures, characters of greater dimensions exhibit less blurring compared to smaller ones. This disparity can be attributed to the location of words in the internal layer, which may have been more susceptible to interference from the external writings during the reconstruction process.

## 5. Laboratory Description

The material presented in this note may be adapted for a demonstration intended to undergraduate students enrolled in courses related to applied mathematics or physics. The educational experiment has been designed to develop and strengthen the mathematical intuition of tomography modeling, a process that necessitates active student participation. The experimental phase of the activity can be structured in two formats: a group activity or as an instructor demonstration.

In the first scenario, students are tasked with constructing part of the setup using provided instructions

**Figure 6.** Reconstruction (right, inverted) of the Greek scroll (left).

**Figure 7.** Reconstruction (right, inverted) of the Latin scroll (left).

and recording the projections. It is recommended that the instructor undertake a preliminary trial of the experiment. It is strongly advised that the experiment is performed in advance, as this will provide a general overview of the materials and time required to prepare it. Furthermore, it is essential that the instructor is familiar with the code, which can be incorporated into the course’s theoretical material. Within the group framework, each team can be assigned a transparent phantom containing either the

same sentences or different ones to introduce more variety in the results.

In the second framework, the instructor will conduct the experiment, with the assistance of a laboratory technician if needed to facilitate the setup assembly. The acquisition of the projections is expected to take approximately 30 minutes, during which time the instructor may introduce the mathematical model of X-ray tomography or explain the virtual pipeline and the code. A concise overview of the mathematical model of X-ray with a summary of the relevant notions is provided in the last section of this contribution. The documentation of the virtual pipeline is available in the form of a Matlab workflow or a Jupyter Notebook on the webpage https://gitlab.com/csc1/archeolab/. Subsequent to the acquisition of the projections, the students will utilize the code and adhere to the implemented workflow, adjusting the parameters and control points as required.

Following the completion of the virtual unwrapping, students may be requested to write a report or a presentation that summarizes the results obtained, the observations made, the difficulties encountered, and possible improvements. The report could be structured like a scientific article including the following sections: Introduction, Methods, Results, Discussion and Conclusion. The Introduction should provide an overview of the experiment and its objectives. In the Methods section, students should detail the experimental setup and the algorithms that were utilized. The subsequent section is dedicated to the description of the results, including the reconstructed scrolls. The final sections summarizes the

experimental outcomes, the problems experienced, and gives suggestions for potential improvements and future directions.

## 6. Expected Results and Conclusion

The proposed training experience serves as a valuable resource for instructors in addressing the complexity of the subject matter as well as in the abstract modeling of physical phenomena.

We proceed to analyze the potential outcomes of the two frameworks described. From a didactic perspective, we anticipate significant interaction among students and instructors, with the latter posing questions and exploring diverse methodologies. The presentation component or the final report constitutes a pivotal element of the laboratory, offering valuable feedback to the instructor concerning the students’ comprehension of the subject and the evaluation of their problem-solving skills.

The reconstruction of the text is deemed successful when the resulting images clearly display the text, with the majority of letters being legible (see Figures 6 and 7). Characters within the internal layers are expected to be more blurred compared to the external layers, due to light bending effects. The cross-sections obtained through the reconstruction process are expected to reveal the layers of the phantom, thereby enabling students to comprehend the structure and depth of the text. It is expected that not all groups will possess the capability to fully reconstruct the transparent scroll. Therefore, a database containing tuned images is included to serve as a model for the expected reconstruction and to assist groups lacking this capability in performing the virtual reconstruction.

In the second framework, upon the completion of the experiment by the instructor, students are tasked with processing the projections and constructing their own reconstructed text. Also in this case, the report or presentation will reflect the assimilation of the theory, and outline the encountered challenges, the results obtained, and the mathematical model employed. Indeed, at the end of the experimental laboratory, students should be able to provide clear explanations of the experiment, results obtained, and ability to connect these to the theoretical framework. From a theoretical standpoint, it is expected that students will grasp the fundamentals of X-ray tomography and its significance in the domain of archaeology. In both workshops, students have the opportunity to sharpen their problem-solving skills, whether individually or collectively. Moreover, the final discussion will contribute to promote peer instruction, an effective learning methodology substantiated by current educational studies.

In summary, this note has proposed a simulated recovery of hidden text in ancient papyrus scrolls, utilizing an educational setting to illustrate the principles of X-ray tomography and the development of a rudimentary virtual pipeline for hidden text recovery. It provides detailed instructions for constructing the experimental setup and conducting the experiment, ensuring its reproducibility in scientific events, and educational laboratories. The scripts developed for the virtual reconstruction have been implemented on Matlab and Jupiter Notebook with documentation available at https://csc1.gitlab.io/archeolab/. Finally, a training activity have been proposed, which can be adapted to the audience and the goals of the instructor.

### A. The mathematical model of X-ray tomography

In this section, the mathematical model of X-ray tomography is described. This model is based on the computerized transverse axial (CTA) scanners, where three-dimensional objects are modeled as a collection of two-dimensional reconstructed slices. As text references for undergraduate students, we suggest The Mathematics of Medical Imaging of Timothy Feeman [3] and The Radon Transform and Medical Imaging

of Peter Kuchment [7]. For advanced undergraduate and graduate students, the classical textbook The Mathematics of Computerized Tomography of Frank Natterer [9] is recommended.

The plane R2 is considered with points denoted by the coordinates (x, y). The object is described by a bounded, connected subset of the plane, denoted by Ω. The X-ray attenuation coefficient is modeled by a function f : R2 →R, (x, y) 7→f(x, y), which is compactly supported in Ω. In this setting, it is assumed that the geometry of the experiment is the parallel beam geometry (i.e., each source has a corresponding detector that measures the attenuation of the emitted beam, and all the beam lines are parallel). In modern application, the fan beam geometry is more frequently employed than the parallel beam geometry. In this case, a source emits several X-ray beams in different directions contained in a plane, and an array of detectors registers their variations in intensity.

The intensity of the X-ray beam, denoted by I, is defined as the quantity of radiation per unit area, the latter measured on a plane perpendicular to the X-ray beam. The source point is denoted by P0 = (x0, y0) and the detector point by P1 = (x1, y1). Let L be the line through P0 and P1 with parametrization γ given by

γ(t) = (x0, y0) + t(cos θ, sin θ),

where θ ∈[0, 2π) and t ∈R. Here, S1 denotes the unit sphere in R2 and is intended as the set of all unitary directions. Conventionally, the center of rotation is the origin (0, 0), and sources and detectors rotate around it.

The physical law that enables to combine the information about the intensity variation of the radiation and the unknown attenuation coefficient f is known as the Beer-Lambert law. This law states that the intensity variation at a point of the object lying on the X-ray beam, denoted by γ(t), is directly proportional to the X-ray intensity at a specific point and path length. The standard formula for this law is expressed as follows:

I(t + ∆t) −I(t) ≃−f(t)I(t)∆t.

The function f(t) = f(γ(t)) represents the attenuation coefficient at position γ(t). If the limit of the parameter increment ∆t goes to zero in equation (A.1), under the assumption that the initial intensity, denoted by I0, at the source position P0 for t = t0 is known, the following initial value problem is obtained:

(

dI

dt (t) = −f(t)I(t) t ∈R, I(t0) = I0.

The solution I to this problem is given by the exponential function

I = I0 exp



−

L

fdl



,

where dl is the arc length element and L is the X-ray beam. Equation (A.2) is consistent with the physical experiment, since the intensity I(t) at a position P1 for t = t1 is always smaller or equal to the initial intensity I0. Applying the logarithm on (A.2), and denoting with I1 = I(t1) the recorded intensity at position P1, the X-ray projection formula is obtained:

p(t1) = −log

I1

I0



=

L

f(x, y)dl.

In the plane the projection is formally known as the Radon Transform. It is defined as the line integral of the attenuation coefficient f along an X-ray beam L:

Rf(L) =

L

f(x, y)dl.

To represent lines, the so-called normal parametrization is introduced, defined as follows: for t ∈R,

γ(t) = (s cos θ −t sin θ, s sin θ + t cos θ)

(see Figure 8). Here, the variable s is called affine parameter, denoting the oriented distance of the line L

from the origin, while the variable θ is the counter-clockwise rotation of the line L with respect to the x-axis. A useful expression that connects the variables x, y, s, θ is the following formula, called the normal equation:

s = x cos θ + y sin θ.

Under the normal parametrization, the Radon transform in the plane of a line L characterized by the parameters (s, θ) corresponds to the projection p(s, θ). It has the formula

p(s, θ) =

Z +∞

−∞

f(γ(t))|γ′(t)|dt

=

Z +∞

−∞

f(s cos θ −t sin θ, s sin θ + t cos θ)dt,

and

Rf(s, θ) = p(s, θ).

In dimension higher than two, the Radon transform integrates along hyperplanes and not lines (see [9] for more about the X-ray transform). A pivotal quantity associated with the Radon transform is the

**Figure 8.** Normal parametrization of lines.

sinogram, representing the projection data at each angle, denoted by the variable θ, and distance from the

origin, denoted by the variable s. The name "sinogram" derives from the observation that a fixed point of the object traces out a sinusoidal curve in the sinogram.

The objective is to recover the function f from the knowledge of the projections p(s, θ), subject to the variation of the parameters (s, θ). The back projection method can be regarded as a first naive reconstruction technique. This method involves back-projecting each projection onto the plane to recover the value of the function f at a specific point (x, y). This operation gives rise to the adjoint Radon transform, also known as the back-projection operator:

B[Rf(s, θ)](x, y) =

Z 2π

Rf(s, θ)dθ,

that can be equivalently express in terms of the projection:

B[p(s, θ)](x, y) =

Z 2π

Z +∞

−∞

f(s cos θ −t sin θ, s sin θ + t cos θ)dtdθ.

Here, the definition from reference [10, Equ. (2.5)] is used. The inner integral determines the projection p(s, θ), which corresponds to a unique point (s, θ) in the sinogram. The back-projection operation involves the summation of ray-projections over all ray-paths through a given point (x, y). The Back-Projection technique was originally introduced by Oldendorf [11] in the context of X-ray tomography. However, the reconstruction of the function f is not optimal due to the fact that the summation of projections is applied not only to points of high density, but also to other points of the object. This results in the presence of star artifacts in the reconstruction and a blurred background. Furthermore, the Back-Projection method smoothens the edges. Examples can be found in [3].

The Back-Projection formula can be improved by integrating a filtering operation prior to back-projected. This approach, called Filtered Back-Projection, involves the application of a filter to the projections, enabling the enhancement or reduction of high frequencies in the Fourier domain, which are known to be associated with edge detection.

Let us begin with the definition of the two-dimensional Fourier transform of the function f(x, y) given by

Ff(kx, ky) = 1

2π

R2 f(x, y)e−i(kxx+kyy)dxdy.

The reconstruction formula presented here is based on the application of the Fourier Slice Theorem, which states that the one-dimensional Fourier transform of the Radon transform, the projection, with respect to the affine parameter s is equal to the two-dimensional Fourier transform of the function f [10]:

Ff(σθ) = √

2π FsRf(σ, θ),

where

FsRf(σ, θ) = √

2π

R

e−isσRf(s, θ)ds.

To derive the the Filtered Back-Projection formula, commence with representing the attenuation coefficient f in terms of its 2-D Fourier transform:

f(x, y) = 1

2π

R2 Ff(kx, ky) · ei(kxx+kyy)dkxdky.

In this representation, the function f is expanded as a superposition of sinusoidal waves, encoded in the complex exponential. The parameters kx and ky represent the Fourier parameters along the directions x and y, respectively. By switching to polar coordinates in equation (A.12), thanks to the symmetry of the Radon transform, one can derive

f(x, y) = 2(2π)

Z 2π

R

Ff(σθ) · eiσ(x cos θ+y sin θ)|σ|dσdθ.

Since the value of k ranges from −∞to +∞, the inner integral has the form of a one-dimensional Fourier transform. Hence, by (A.10) and (A.5)

f(x, y) = 1

4π

Z 2π

√

2π

R

FsRf(σ, θ) · eiσs|σ|dσdθ.

At this point, the inner integral is the inverse Fourier transform F−1

σ of the function FsRf(σ, θ)|σ| with respect to the parameter σ, while the outer integral is the back-projector operator (A.7). Therefore, a formula for the Filtered Back-Projection is derived:

f(x, y) = 1

4π B(F−1 σ (|σ|FsRf(σ, θ))).

The function |σ| is referred to as a ramp filter. In practice, the acquired data is subject to noise, which typically exhibits a high-frequency component in the Fourier domain. Consequently, it is common to apply a low-pass filter to the ramp filter, a function that attenuates the high-frequency contributions.

In the experiment, the Ram-Lak filter was used. This filter was first introduced by G. N. Ramachandran and A. V. Lakshminarayanan in 1971 [14]. This type of filter is applied to the ramp filter in the Fourier domain yielding the function |σ| if σ ≤1, and 0 otherwise (see also [3]).

Acknowledgements

This research was funded in whole or in part by the Austrian Science Fund (FWF) SFB 10.55776/F68 “Tomography Across the Scales”, project F6801. For open access purposes, the authors have applied a

The financial support by the Austrian Federal Ministry for Digital and Economic Affairs, the National Foundation for Research, Technology and Development and the Christian Doppler Research Association is gratefully acknowledged.
