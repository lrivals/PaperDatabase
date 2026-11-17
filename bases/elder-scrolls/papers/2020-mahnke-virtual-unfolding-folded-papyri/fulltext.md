---
id: 2020-mahnke-virtual-unfolding-folded-papyri
title: "Virtual unfolding of folded papyri"
year: 2020
backend: pymupdf
---

Journal

Available online

ScienceDirect www.sciencedirect.com

Short communication

Heinz-Eberhard Mahnke a,b,c,∗, Tobias Arlt d, Daniel Baum e, Hans-Christian Hege e, Felix Herter e, Norbert Lindow e, Ingo Manke c, Tzulia Siopi a, Eve Menei g, Marc Etienne h, Verena Lepper a,f

a Ägyptisches Museum Papyrussammlung, Berlin, Germany b Freie Universität Berlin, Berlin, Germany c Helmholtz-Zentrum Berlin, Berlin, Germany d Technische

Universität Berlin, Berlin, Germany e Zuse-Institut Berlin, Berlin, Germany f Humboldt-Universität zu Berlin, Berlin, Germany g Visiting Conservator, Paris, France h Musée du Louvre, Paris, France

i n f o r t i c l e

Historique de l’article : Rec¸

u le f´evrier Accepté

le juillet Disponible

sur Internet le

July

Keywords :

non-destructive

b s t r c t

The historical importance of ancient manuscripts is unique since they provide information about the

of ancient cultures. Often texts are hidden in rolled or folded documents. Due to recent improvements

in sensitivity and resolution, spectacular disclosures of rolled hidden texts were possible

revealing text on folded manuscripts is even more challenging. Manual

is often too risky in view of the fragile condition of fragments, as it can lead to the total loss of

document. allows for virtual unfolding and enables non-destructive access to hidden

texts. We have recently the procedure and tested unfolding algorithms a mockup sample.

Here, we present results on unfolding from the papyrus collection

Musée du Louvre, among them objects folded along lines. In one

the packages, the ﬁfirst identiﬁcation of a word was achieved, the Coptic word for “Lord”.

2019 Les Auteurs. Publi´e par Elsevier Masson SAS. Cet article est publi´e en Open Access sous licence CC

BY-NC-ND (http://creativecommons.org/licenses/by-nc-nd/4.0/).

Introduction

collections writings globe, ﬁfinds scrolls, packages, sorts fragments, scrunched papyri, even disposed documents ﬁfilling material. successful unravelling imprinted into metallic foils lead silver scroll, resolving power unrolconvincingly demonstrated. inks contain metal ions, iron gall increased produce

distinguish organic base material like parchment papyrus. parchment, recovery scroll, matter badly scroll had distorted compressed, now successfully achieved cases [3–5]. Even carbonized papyri, Herculaneum papy-

∗Corresponding author. Helmholtz-Zentrum GmbH, Hahn-Meitner-Platz Berlin, Germany. Adresse

e-mail : hemahnke@zedat.fu-berlin.de (H.-E. Mahnke).

rus,

successfully identiﬁed [6]. These assumed identiﬁed phase [7]. The fact Herculaneum admixtures amounts lead [8], leaves open possibility visibility tomograms carbonized base due admixtures. recovery texts scrolls “normal” though even more challenging. types techniques known [9]. While simple cess

scrolls, perpendicular more complicated. investigation liberal arts oriented ERC-funded project called “Localizing Years History. Texts Scripts Island”, conducted Ägyptisches Museum Papyrussammlung Berlin. project intends combine hidden knowledge, languages scripts, including hieroglyphs, Hieratic, Demotic, Aramaic, Greek, Arabic, distributed spread out over collections institutions different countries. result international cooperation,

Authors. Published Elsevier Masson SAS. open access under CC BY-NC-ND license (http://creativecommons.org/licenses/bync-nd/4.0/).

Box Louvre awaiting

unrolling.

discovered within collection Musée du Louvre related Island near Aswan (see 1). They appeared appropriate candidates applying approach.

Research aim

approximately perpendicular straightforward. Before applying developed technique real, objects, we have recently according so-called “magic fold” special purposes [9]. Since demonstration emphasis put algorithmic procedure, prepared highest possible highly absorbing cinnabar minium (red) ink. objective investigation apply cedure real object successful result. ﬁfinal objective, course, identify recover but full words after unfolding, otherwise accessible. Three objects, within collection Musée du Louvre, appeared appropriate candidates, them appearing

2).

Material methods

3.1. objects

Following successful demonstration algorithmic virtual procedure searched suitable objects collection Ägyptisches Museum Papyrussammlung well Musée du Louvre, département des Antiquités égyptiennes. registry book department, objects recorded entered collection They originate French excavations conducted Ch. Clermont-Ganneau objects speciﬁed labelled L Louvre El preceding number. collection consisting “three tin boxes containing debris papyrus” (El a, b, c), another tin box mentioned same kind but smaller dimensions (El 228). these boxes preserved original containers labels El

b El c, originally labelled numbers E E accessed. studied

Photographs packages: L/El227b/1-pC, (b) L/El227b/4-pG, (c)

L/El227b/2-pU.

belong box labelled El b E resp. They selected visual inspection check if sizes conditions suited setup.

3.2. ﬂfluorescence

decisive test determine whether tomography chance distinguishing base material detection high Z-material objects, indicator metal-ion-containing ink. Therefore, experiment prior tomography, objects tested presence Fe, XGLab Elio portable ﬂfluorescence (pXRF) 1mm beam spot Centre de Recherche de Restauration des Musées de France (C2RMF). since Fe frequent impurity (e.g. sand dust), often chemical form ochre, detection Fe necessarily proof presence containing Fe (for details see [11]). Three specimens showed variations intensities Fe characteristic ﬂfluorescence depending position. Because that, these

L/El227b/4-pG papyrus: section, (b–d) successive unfolding, (e) magniﬁed 2D-projection letters.

selected micro-computed (CT) setup Helmholtz Zentrum Berlin. CT consists Hamamatsu tube W anode. accelerating voltage applied go up kV. packages, accelerating voltage kV used. source spot size distance detector plate allowed resolution size down m. specimens positioned plastic beakers, secured against motions air-cushioned plastic foils, beaker then mounted onto turning table CT setup. then processed Amira software [12].

3.3.

Here, brieﬂy summarize method unfolding. Details previous [10]. Virtual done major steps. major step, unfolded until geometrically process may require several steps. Then, second major step, unrolled, substantially simpler than step normally done directly. step omitted directly unfold second step.

algorithm describe here, assume either principle

unfolded applying series steps. Crumpled example, cannot unfolded approach. We start describing single step. step done slice-by-slice fashion. slices we choose orientation axis. each slice, then contours, inner outer contour. While inner mainly deﬁnes unfolding, outer helps decide certain parts moved transformation 3). inner positioned presumably straight before folding. Often, medial axis respective slice good choice. done ﬂflattening inner straight while maintaining spacing points inner ﬂflattening process. transforming respect inner contour, use algorithm idea moving squares [13]. This algorithm takes input set control points consisting source points equal number target points. application, source target points deﬁned inner points curved inner contour, respectively. transformation transforming source points target points. transformation done way locally deformed little possible, resulting as-rigid-as-possible transformation [13]. outer helps algorithm decide certain parts moved to. particularly important areas

Illustration ﬂflattening algorithm. each voxel mesh (left), corresponding point unrolled mesh (middle) thickness sampled surface normal (right).

come very close areas would otherwise far apart. Although done slice slice, we do manually draw inner outer contours each slice. Instead, we take advantage

fact successive slices very and, thus, contours successive slices very similar. We therefore adjust contours those slices contours do match structures slice well. those slices actually deﬁned contours, contours linearly interpolated, thus deﬁning new outer inner contours each slice. mentioned before, usually need do several steps. each step, choose slice orientation axis. Finally, after several steps, transformed looks roll, although roll might even highly distorted regions. If reached stage, turn second major step, step. step, done per slice, unrolreally done 3D. this, create surface mesh positioned passes through center sheet represents its medial surface. create medial surface mesh, contours few slices. fact, minimize manual labor, aim deﬁning contours few slices possible. slice orientation choose plane axis sheet rolled. tool automatically ensures contours same number points. Thus, slices, i-th points correspond each other. therefore easy create mesh connecting corresponding points. already mentioned, we want minimize number slices manually draw contours. therefore take advantage fact sheet successive slices looks very similar. Hence, draw (or modify) contours those slices longer ﬁts sheet. those slices, contours linearly interpolated, thus yielding each slice. These interpolated contours, show well sheet matched whether additional contours need deﬁned. They generate mesh. mesh deﬁned exclusively contours manually drawn corrected. contours needed, last slice. Once satisﬁed coincidence contours sheet, perform actual unrolling. this, ﬂflatten mesh into plane. ﬂflattening, try minimize distortions. is, try preserve distances neighbored mesh vertices mapping them into plane. We use approach resembles massspring model [14,15], with additional constraint deformation process cells mesh must remain convex. mesh then create unrolled thin volume. depth

represents thickness sheet will speciﬁed user. detail, whole process works follows (see 4): First, bounding box mesh computed. box then

sampled same voxel size original tomogram.

each sampling point inside mesh, grid cell

point lies determined parameters bilinear

interpolation computed. cell parameters compute corresponding point mesh. addition,

surface normal point

normal vectors vertices cell. Finally, voxel size determine values points both directions normal, mesh middle. sampling stopped if sampling point outside tomogram closer another point mesh than original one. If case, value unwrapped thin set user-deﬁned padding value. After generating thin unwrapped visualize classical [16]. Brieﬂy, each point screen, corresponding view ray computed. ray sampled through image. user-deﬁned color map, called transfer function, assigns each sampling point color transparency value according value point. create ﬁfinal image, colors transparency values accumulated order appearance ray until either combined color fully opaque end reached. These accumulated colors then generate ﬁfinal image.

Results discussion

Since L/El227b/1-pC rather fragile, secured Japanese tissue, seen photograph 2a. then revealed object L/El227b/1-pC 5, a section through projection shown. clearly readable, pjoe[is] pjoe[is . . .], with last brackets missing. translated “the Lord” “oh Lord” vocative if perhaps short prayer. Since occupies area sheet, tempted speculate perhaps more however detected more speciﬁc speculation, additional text, but invisible tomography, could “Lord” could ferrous ink.

next L/El227b/4-pG 2b even more fragile,

apparently less layers. shows section (cf. description above) unfolding done. indicated arrows, successive unfolds needed layer. Although sheet highly damaged holes missing ﬁfibers, few identiﬁed.

L/El227b/1-pC papyrus: section, (b) 2D-projection showing a Coptic “Lord”.

L/El227b/2-pU “magic like” packaged, cuts through volume.

third L/El227b/2-pU rather compact appears well. shows different cuts through volume. Due distortions simple Ref. preliminary extraction representation gives

indication letters, although fractions uncovered black identiﬁed photo 2c). probably means case, dealing carbon does give

Conclusions outlook

We have successfully proposed algorithmic approaches able virtually unroll addition, we succeeded revealing hidden identifying real papyrus package. We also unfold lines. best knowledge, achieved two-ply ﬁfiber structures make difﬁcult identify individual layers. hand, tracking ﬁfibers helps needed algorithmic procedure, could helpful future unfolding. examples clearly indicate limit imaging approach absorption seem partially there absorption-based objects type, development suitable imaging techniques imperative – ject currently working on.

Funding

work funded European Research Council (ERC)project “Localizing Years History. Texts Scripts Island Egypt” [Project ID funded under H2020-EU.1.1.]. initial phase, supported Beauftragte der Bundesregierung für Kultur Medien (BKM) Germany.

Acknowledgement

We thank Kristin Mahlow Johannes Müller (Museum für Naturkunde, Berlin) acquiring “GE Phoenix Nanotom S” magic attempts Papyrussammlung. We are grateful Leif Glaser (DESY, Hamburg) who wrote cinnabar minium mockup, Frank Kutz Philipp Hoelzmann (FU FB Geo TOPOI) help Niton pXRF, Eric Laval who let us check Louvre objects C2RMF its ELIO pXRF.

Références

D. Neuber, C. Reinhart, Moderne Computertomographie erlaubt virtuelle Entschlüsselung einer antiken, geheimnisvollen Bleischriftrolle

der Mandäer, Giesserei-Rundschau 59:5/6 http://www.voeg.at/upload/editor/File/archiv/2012/5-6/Giesserei 2012/ 5.pdf. G.H. Barfod, J.M. Larsen, A. Lichtenberger, R. Raja, Revealing complexly silver scroll Jerash advanced imaging software, Sci. Rep. [3] D. Mills, O. Samko, P.L. Rosin, K. Thomas, T. Wess, G.R. Davis, Apocalypto: reveaunreadable Proc. SPIE Developments VIII, 85060A, [4] O. Samko, Y.-K. Lai, D. Marshall, P.L. Rosin, information recovery scanned scrolled historical documents, Pattern Recognit. 248–259, [5] W.B. Seales, C.S. Parker, M. Segal, E. Tov, P. Shor, Y. Porath, damage discovery via unwrapping: reading scroll En-Gedi, Sci. Adv.

e1601247, V. Mocella, E. Brun, C. Ferrero D. Delattre, Revealing Herculaneum

phase-contrast imaging, Nat. Commun. [7] John Banhart, Advanced Methods Materials Research Engineering, Published Oxford Scholarship Online: May ISBN DOI: 10.1093/acprof:oso/9780199213245.001.0001. E. Brun, M. Cotte, J. Wright, M. Ruat, P. Tack, L.V.C. Ferrero, D. Delattre, V. Mocella, Revealing metallic Herculaneum papyri, PNAS 3751–3754, [9] M. Krutzsch, Falttechniken alt¨agyptischen Handschriften, Archiv für Papyrusforschung, Beiheft “Ägypten lesbar machen – die klassische Konservierung”, pp. 71–83. D. Baum, N. Lindow, H.-C. Hege, V. Lepper, T. Siopi, F. Kutz, K. Mahlow, Mahnke, Revealing hidden papyri, Appl. Phys. [11] T. Christiansen, D. Buti, K. NicoleDalby, P.E. Lindelof, K. Ryholt, A. Vila, Chemical characterization black red inks inscribed papyri: Tebtunis temple library, J. Archaeol. Sci. Rep. 208–219, D. Stalling, M. Westerhoff, H.-C. Hege, Amira: A highly interactive visual analysis, in: D. Charles, C.R. Hansen, Johnson (Eds.), Visualization Handbook, chapter Elsevier, B978-012387582-2/50040-X, pp. 749–767. S. Schaefer, T. McPhail, J. Warren, deformation moving squares, ACM Trans. Graph. (TOG) 533–540, 1145/1141911.1141920. X. Provot, Deformation constraints mass-spring model describe rigid cloth behavior, in: Proc. Graphics Interface ‘95. Canadian Human-Computer Communications Society, pp. 147–154, ISBN: ISSN: 0713- M.S. Brown, W. Brent Seales, Document restoration shape: general deskewing algorithm arbitrarily warped documents Proc. Eighth IEEE International Conference

Computer Vision (ICCV), vol. IEEE, pp. 367–374, J. Beyer, M. Hadwiger, H. Pﬁster, State-of-the-art survey GPU-based large-scale visualization, Comput. Graph. Forum 13–37,
