---
id: 2005-lin-opaque-document-imaging-building-images
title: "Opaque Document Imaging: Building Images of Inaccessible Texts"
year: 2005
backend: pymupdf
---

Opaque Document Imaging: Building Images of Inaccessible Texts

Yun Lin Computer Science Department

University of Kentucky Lexington, Kentucky 40506

ylin@netlab.uky.edu

W. Brent Seales Computer Science Department

University of Kentucky Lexington, Kentucky 40506

seales@netlab.uky.edu

## Abstract

This paper introduces a method for building a readable image of an opaque, rolled or folded text from a volumetric, penetrating scan. The problem is framed by localizing, constructing, and manipulating an image induced by a surface embedded in a 3D voxel space. There are two central contributions that lead to the demonstrated results. First is an energy-based texture formation algorithm, which is a function of voxel intensities and the geometry of the embedded surface. Second is a regularization algorithm based on a constrained mapping of the embedded surface to a regularized image plane. The mapping preserves angles and lengths, which minimizes the distortion of text in the image. The experimental results show readable images derived from custom, high resolution (X-ray-based) CT scans of rolled papyrus and ink samples. These methods are signiﬁcant for scholars seeking to study inaccessible texts, and may lead to viable techniques for scanning everyday opaque objects (books) without opening them.

Introduction

Many important documents exist that cannot easily be opened and digitized. Opacity defeats human eyes and conventional cameras. The goal of this work is to construct a readable image of such documents without the need to open or touch them. A prominent example (Fig. 1) is found in the Egyptian papyrus collection at the British Museum, which holds a number of texts like the one shown. Some of these texts have not been opened because of the difﬁculty in physically unwinding the deteriorating material. A more practical if futuristic goal is to build images of the pages of books without opening them.

We develop an approach to this problem based on a 3D voxel set obtained from non-invasive penetrating scans (e.g., CT scans) followed by careful analysis of that data. The space of voxel samples reduces the document’s opacity

## (préambule)

**Figure 1.** This papyrus scroll is part of the British Museum’s Egyptian papyrus collection and has yet to be transcribed because of the difﬁculty in unrolling the material.

to an intensity ﬁfield, creating an interesting imaging challenge: segmentation, texture generation, 3D-to-2D mapping. While this is an unusual document processing problem since the voxel space is created from technologies more familiar to the medical imaging community, the resulting scan can be used to derive images of document surfaces that reveal features such as ink and ﬁfiber.

We focus in this paper on the post-scan methods necessary to produce an image of the surface of such documents. This image is reconstructed from the voxel set and is extracted through the opaque object without ever exposing those surfaces to a traditional camera or scanner. These methods are necessary but not sufﬁcient for success. The digitization output from a scan must ﬁfirst contain a signal at a resolution and a contrast that enables differentiation between the document substrate and the ink with which it was written to be distinguishable from air, water, and other materials present. Our experimental work with real scans has given us some conﬁdence that there are methods available

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:17:05 UTC from IEEE Xplore. Restrictions apply.

**Figure 2.** The papyrus scroll (left, viewed from the end) was entombed in the town of Herculaneum, buried under the same Mount Vesuvius where lava ﬂowed that destroyed Pompeii in 79 A.D. Efforts to unroll the text produce results (center) but also result in damage. A more bizarre example is the scroll in situ which remains unread within the Belgrade Mummy (right).

and emerging to improve the probability that such scans can be generated for a large class of documents for which opacity currently reigns.

The ultimate goal is to perform a complete analysis of authentic ancient documents, such as the second example shown in Fig. 2. The Herculaneum collection [9] is a set of scrolls found in Italy buried as a result of the lava ﬂflow that destroyed the town of Pompeii. Although the scrolls have proven to be a very signiﬁcant ﬁfind, many remain unread because of the degrees of damage and decay that prevent their safe and complete analysis. For scrolls that have been opened, multi-spectral analysis [6] and conventional image processing methods have revealed signiﬁcant previously unknown texts. These kinds of documents represent a serious challenge to which we hope the work presented here can ultimately be applied.

The remainder of this paper develops the methods for recovering images from volumetric scans of documents. The next section provides technical context by highlighting selected related work. Section 3.1 develops the overall framework and 3.2 focuses on a method for segmenting the voxel set with an initial surface estimate subject to an optimization process. This slice-based starting point is reﬁned with an energy model that is an extension of active contours, and ultimately leverages the volumetric-to-2D mapping in order to position the embedded surface correctly within the voxel set. Sections 3.3, 3.4, and 3.5 provide greater detail about how the embedded surface, once segmented and localized, can be unwrapped subject to a set of constraints that favor the behavior of rigid material such as papyrus. In Section 3.6, we discuss an initial exploration of texture-guided contouring. Finally we conclude with results from papyrus objects we constructed and had scanned.

Related Work

The methods for acquiring penetrating data scans such as CT and micro-CT are well-known in contexts such as medical imaging and non-destructive evaluation [12]. These techniques have also been used as the basis for postprocessing analysis, such as work with fossils [16] and recent scans of mummies. Document processing in these contexts has been much less studied, although we are aware of two interesting cases. The Belgrade Mummy contains a papyrus scroll in situ that remains unread (Fig. 2, right). It was detected from CT analysis but there are no direct techniques available for providing a reading. A second example is the study of cuneiform text (written on clay tablets) using CT [2].

In terms of document imaging as a means for preservation, restoration and enhancement, digitization and subsequent enhancement work was initially an image-based (2D) operation [8, 15, 18]. These approaches require planar objects and improve image quality through digital image processing. Methods using 3D acquisition or an approximation [22] and those using model-based techniques [17] have solved problems such as distortion removal due to page curl.

The technical framework we present in the next sections uses energy-based methods [13, 21, 1] for surface localization and texture creation. The constrained 3D-to-2D mapping is implemented to approximate a conformal map [11, 10, 5], designed to reduce distortion.

Framework

The input to the processing framework is voxel data from a custom CT scanner, which can digitize to resolutions of 5 microns. Volumetric data from this scanner is the basis of our analysis, which we treat as a cuboid of aligned

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:17:05 UTC from IEEE Xplore. Restrictions apply.

voxels in the x, y, z directions. Unstructured voxels represent density values, and ink and document substrate can be distinguished from empty space by intensity variations in the voxel set. Interior information, opaque and impenetrable under normal imaging conditions, is revealed by crosssectional slices in the volume. Examination of only slices through this set yields limited information since the meaningful data is a function of the document’s surface shape and the ink on that surface.

The goal is to construct a mapping relating the voxel space to a two dimensional “image plane”. Given this mapping, pixel values on the image plane can be deﬁned, through the inverse mapping, as a function of the intensities of the enveloping voxel set. A key problem is to position a surface to lie precisely in the 3D voxel set at the edge of the document to reveal intensity variations related to ink.

We build an optimization algorithm to correctly localize the surface within the voxel set. This algorithm takes advantage of volumetric-to-2D mapping as well as texture image analysis. Certain low-level image features like sharpness and continuity can be used to evaluate the quality of an image that results from a particular 3D surface location. These feature measures are simpler to apply in 2D, leveraging the inverse mapping to re-position the embedded surface. Highlevel pattern recognition techniques may also be integrated to enhance the automatic process of the texture evaluation, helping to improve surface accuracy.

Optimization Algorithm

The iterative optimization used to position the surface within the voxel set is designed to satisfy certain constraints and is evaluated by an energy value. Lower energy values better meet the constraints. The initial condition comes from high level analysis (e.g., user selecting initial point positions) to give an initial estimate of the surface from which texture is induced. The cooperative procedure unites several terms: Surface smoothness constraints, low level feature processing in the voxel space, and feature/pattern analysis in the 2D mapped space. This cooperative approach is an extension of the active contour models formulated in [13, 1].

The algorithm detects salient contours in individual 2D slices of the voxel set. These contours, connected across slices, form an initial surface embedded in 3D from which the optimization process begins.

The steps of the algorithm to localize this surface proceed as follows:

1. Initialize and optimize a mapping M1 from a 3D volume to a surface. An optimal mapping is acquired by minimizing the energy E1, where E1 is deﬁned as:

E1(V, S) = I(V, S) + C(S)

E1 is a function of the volume V and a surface S. It is a linear combination of an Image component I(V, S), which evaluates how well the surface locates the intensity features contained in the volume, and a Shape component C(S), which evaluates the smoothness of the surface.

2. Based on the chosen surface within the volume, a ﬁfilter is applied on V and S that produces a texture map T1.

F(S, V ) = T1

The surface is represented as a triangulated mesh, and its triangular components map to R2, where the texture map T1 is deﬁned, without inheriting any adjacency relationships. We call it a nonregularized texture map.

3. Approximate a conformal map M2 that transforms the 3D textured mesh S to a 2D planar surface U and thus induces a texture map T2, which we call regularized.

M2(S, T1) = U + T2

T2 represents the “image” of the information carried on the surface of the document in the scan.

## 4. Calculate the energy E2 for T2:

E2(T2) = P(T2) + R(T2)

P represents a generalized image processing function evaluating low-level features of an image. R represents a generalized function based on advanced pattern analysis techniques. The surface is optimized iteratively through steps 2,3,4. During each iteration the surface position is updated along its normal direction.

## 5. Return U, T2.

This outline shows how to calculate a regularized image of the surface of a document represented by the voxel set. In the following subsections, we detail each step.

2 1 2Dimensional Active Contour

We deﬁne a mapping M1 that maps a solid V to a piecewise smooth surface S and a texture map T1 as follows:

M1 : V →S + T1

V : R3 →R S : [0, 1] × [0, 1] →R3

T1 : R2 →R

V can be viewed as a three-dimensional image. S is a triangular surface embedded in V . It is mapped to a 2D space by mapping each triangular component independently. T1 maps each point within it to an intensity value.

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:17:05 UTC from IEEE Xplore. Restrictions apply.

We take advantage of cross-sections to deﬁne an initial surface by approximating 2D salient contours. Optimization follows and in this phase optimization is only performed based on raw volume data and the surface, ignoring the texture for the moment. We deﬁne a local optimal mapping M1 as minimizing the energy function E1, where E1 is deﬁned as:

E1(V, S) =

 1

0 (I(V (x, y, z), S(u, v)) +C(S(u, v)))dudv I(V, S) = −α|∇V (x, y, z)|2

C(S) = βu|Su(u, v)|2 + βv|Sv(u, v)|2

+λu|Suu(u, v)|2 + λv|Svv(u, v)|2

+λuv|Suv(u, v)|2

(1)

I(V, S) calculates the gradient of the surface with respect to the volume, which attracts the surface to contours with large intensity gradients. C(S) is a measure of the smoothness of the surface. It is a combination of 5 components, which are ﬁfirst-order and second-order partial derivatives along u, v directions. These components correspond to continuity, curvature and twist. For surfaces approximated by ﬁfinite elements decided by a set of points {p(i, j)|0 < i < m −1, 0 < j < n −1} where m, n are sampling resolutions along u, v directions, the derivatives are approximated at each control point as follows:

Su(u, v) = pi,j −pi−1,j Sv(u, v) = pi,j −pi,j−1 Suu(u, v) = pi−1,j −2pi,j + pi+1,j Svv(u, v) = pi,j−1 −2pi,j + pi,j+1

Suv(u, v) = (pi,j −pi−1,j)

−(pi,j−1 −pi−1,j−1)

(2)

The values of βu, βv determine the elasticity of the surface, while λu, λv determine the rigidity along the u, v direction respectively. λuv is used to adjust the resistance to surface twists.

We solve the optimization problem by using a greedy algorithm, which is an extension of planar active contouring [19] to 2 1

2 dimensions: points move on the discrete grid to any position within a deﬁned planar neighborhood while the constrained energy functional is built in three dimensional sense. Boundary points are ﬁfixed in cases the surface to ﬁt is not closed.

This algorithm is semi-automated in that a user can interfere with the active contour by setting points to be ”snakeable” or ”movable”.

Regularization

The mapping that unwraps the embedded surface plays a signiﬁcant role in the quality of the resulting texture. We

Greedy Algorithm for 2 1

2 active contouring Initialize α ij, βu ij, βv ij, λu ij, λv ij, λuv ij for each point pij loop

loop for each row j in v direction

loop for each column i in u direction

Emin = BIG if the point pij is ”snakeable”

loop for each grid cell p′

ij in its neighborhood calculate E(V, S) according to Equation 1, 2 update pij = p′

ij where p′

ij minimizes E(V, S) /* allow to form corners*/ loop over all points

calculate curvature at each point relax λu,λv values at points with local curvature maxima above a threshold. until the surface becomes stable indicated

by the number of points moved less than a threshold

expect to apply such a mapping to an arbitrarily shaped surface representing a document. The goal is to introduce as little distortion as possible to the text that may be present in the document. Thus we seek a map from the embedded surface S to a planar surface U, which converts the nonregularized texture map T1 to a regularized texture map T2. We deﬁne the mapping as follows:

Given: a 3D triangulated surface mesh S embedded in R3:

S = {Xj|j = 1 . . . n} Xj = △(Pj0, Pj1, Pj2), Pi ∈R3

The mesh S is composed of n triangles. Xj represents the jth triangle with its vertexes deﬁned in 3D space as Pj0, Pj1, Pj2.

Find: a mapping M2 that maps S to a planar surface U deﬁned in R2:

U = {xj|j = 1 . . . n} xj = △(pj0, pj1, pj2), pi ∈R2

xj represents planar triangle and its 2D vertices pj0, pj1, pj2 are 2D parameterized.

Constraint: M2 should minimize some deﬁned distortion.

Let ∼denote the surface deformation relationship. A distortion measure between S and one of its deformations S′ (i.e. S′ ∼S) is deﬁned as a function ξ taking two mesh instances as input, and returning a real value:

ξ : H × H →R S, S′ ∈H

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:17:05 UTC from IEEE Xplore. Restrictions apply.

An optimal map M2 is determined based on the exact definition of how to evaluate the amount of distortion given a surface mesh and one of its deformations.

Conformal Mapping

A mapping M that maps a (u, v) domain to a surface is said to be conformal if for each (u, v), the tangent vectors to the iso-u and iso-v curves passing through M(u, v) are orthogonal and share the same normal. It can be formulated as:

N(u, v) × ∂M

∂u (u, v) = ∂M

∂v (u, v)

where N(u, v) is a normalized surface normal at point M(u, v).

The piecewise conformal map based on the Riemann Mapping Theorem has been used as a way to ﬂflatten and map convoluted cortical surfaces [11, 10]. Conformality of a mapping equivalently means angle preservation and any angle between two vectors on the parameter plane will be preserved through the mapping. A crucial consideration in using piecewise conformal mapping techniques, which are made of local approximations to the Cauchy-Riemann equation, is the computational complexity and ultimately, the metric distortion introduced in the mapping. Harmonic maps are often considered in place of conformal maps because they are easy to compute, at least in approximation. With given boundary mapping (convex) conditions, a unique harmonic map can be found by minimizing the Dirichlet energy [7].

Mass-Spring System

We approximate a conformal mapping by using massspring system simulation. The mass-spring system is a ﬁfinite element method [3, 4]. A surface mesh, modeled as a mass-spring system, can perform realistically when simulation principles are founded on physical laws and constraints.

A mass spring system is composed of a ﬁfinite set of particles and springs that assemble the particles together to make a sheet. The particles have mass, position, velocity, and respond to forces, but have no spatial extent. The particles are subject to internal and external forces and their motion are governed by the classic second order Newtonian equation: f = ma. The internal forces are imposed by the Hookian springs and external forces can be customized for different simulation purposes like a rigid force to hold one edge of a surface. The accumulated energy of the whole system is the summation of the potential energy of each spring e:

ξ = 1



e

K|l′(e) −l(e)|2

where l(e) is the rest length of a spring while l′(e) is its length during deformation. K is the spring stiffness constant. The spring is made more realistic with spring damping taken into account. An optimal mapping is achieved when the system reaches equilibrium status with minimal potential energy.

This surface parameterization method has an important advantage over other methods: arbitrary surfaces can be handled, including rolled, folded, or wrapped surfaces. We use constrained dynamics to perform a combination of unrolling and ﬂflattening operations. The virtual unrolling ”holds” one edge of the surface and let the rest fall down under simulated gravity. The idea is that additional path constraints are enforced on some subset of the particles and the performance of the constrained particles obey the physical laws and at the same time satisfy the speciﬁed path constraints [4, 20].

The mass-spring system strives to maintain the length of each edge while performing mapping by deformation. For a triangle, when its three sides are preserved, its three angles are also preserved. Since the spring system minimizes edge lengths globally, i.e., the length summation of all edges, it approximates but does not produce a strict conformal mapping.

Texture-guided contouring

We assume the surface, when positioned correctly in the voxel set, will induce a texture map T2 that contains high and low frequency components. In addition it likely contains patterns that can be modeled within the context of the object’s historical and cultural milieu. Based on these considerations, the surface location by active contouring and the induced texture are ﬁfixed, and further optimization is achieved by adding texture constraints that ultimately result in optimization directly over the texture.

Our framework includes the possibility to apply advanced pattern analysis based on a priori knowledge of the document. Currently we use general low-level feature analysis as a starting point. Speciﬁcally, we implemented a sharpness measure as a texture constraint. Because of the basic principles of the Fourier slice theorem and the associated reconstruction algorithms on which CT technology is founded, there may be noise in voxels near sharp edges like the surface of the material. In fact, the CT scanner produces a density measure that is essentially a “transparency” value. This makes a surface that cuts through the data seem more like a translucent slice that must be adjusted to tune the image formed on that slice. We employ a sharpness measure [14] based on frequency domain analysis and entropy evaluation.

The texture image T(i, j) is transformed to a frequency map f(i, j) by applying fast Fourier transform (FFT). The

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:17:05 UTC from IEEE Xplore. Restrictions apply.

frequency spectrum is normalized as follows:

fnorm(i, j) = |f(i, j)| 

(i,j)

|f(i, j)|

The resulting frequency presentation can be viewed as a distribution. The method is based on the assumption that as the image gets blurred, the low frequencies become outstanding due to a drop in high frequencies. The goal is to favor sharpness, where the distribution is closer to uniform leading to higher entropy E:

E = −



(i,j)

(fnorm(i, j) · log2fnorm(i, j))

We set E2 = −E which is the value to optimize by iteration through steps 2,3,4 in the algorithm presented in Section 3.1. After each loop, the surface S is updated along the normal in a limited neighborhood, yielding a new surface S′:

S′ = S + ∆S (S′(u, v) −S(u, v)) × N(u, v) = 0

where N(u, v) is a unit normal of the surface at point S(u, v). A texture map T ′

1 is generated for S′ in step 2 and a regularized texture T ′

2 is induced by unwrapping and ﬂflattening S′ in step 3. If its texture evaluation energy E′

2 is reduced, the update S′ is accepted.

For documents with ink on both sides, as we will show in our results, and for problems that simply require expert top-down knowledge, the texture evaluation component can be supplied by a more sophisticated analysis or by a person to get a better result.

Experimental Results

We have implemented the key algorithms outlined above and have conducted a series of tests on replicas and experimental artifacts scanned using customized CT scanners. Before these experiments we conducted a set of simulations to explore important issues related to distortion, segmentation, and scanner resolution.

In the ﬁfirst testing phase, we scanned and processed regularly shaped canvas scrolls and irregular papyrus scrolls. Motivated by that success, we created a set of replicas from papyrus and ink and embedded them in polyurethane plastic. Fig. 3 shows two such objects: a papyrus strip rolled, and a papyrus strip connected into a Mobius band. The lettering was created from an Iron Gall ink mixture.

We scanned the sphere at a resolution of approximately 12 microns per voxel with a custom CT-scanner. Fig. 3 shows an example slice taken from the CT scan data of each example sphere. The cross-section of the rolled sample

clearly shows the wraps of the papyrus. The cross-section of the Mobius band shows the geometry that arises from just the cross-sectional information.

Fig 4 shows the results of applying the processing framework to these samples. In the case of the rolled sample, the textured mesh is shown, as a result of optimization of the ﬁfirst mapping M1, subject to unrolling in the mass-spring system simulator. The text in inner layers is impossible to read without regularization. The ﬁfinal texture T2 is shown below, directly above an image of the original papyrus before it was encased. The legible text reads ”Educe: Enhanced Digital Unwrapping for Conservation and Exploration”.

Similarly, the Mobius strip is shown as it is processed in the mass-spring simulation. Note that the papyrus has ink (locally) on both sides. It is difﬁcult to discriminate any discernible information from this voxel set. To obtain cross sections of the strip so as to facilitate the 2 1

2 active contouring, we varied the 2D slicing direction. The optimal embedded surface mapped from the volume is as shown in Fig. 4 with the ﬁfinal texture T2 shown at the bottom. It is clear that bleed-through is present in this voxel set, showing the importance of spatial resolution in the input CT scan.

In each of these examples it is very difﬁcult to extract any meaningful (readable) information from the scans without a framework for regularizing the textures guided by the location of the substrate material (papyrus) in the scans.

Conclusions

We have shown how to build a texture of the surface of an opaque document from its CT scan. The resulting texture reveals features such as readable text and substrate ﬁfiber. Our experimental results were obtained from noninvasive CT scans of the samples, demonstrating the potential application of our algorithms to more difﬁcult but important cases such as ancient scrolls and damaged books. The post-processing algorithms presented here are a necessary though not sufﬁcient step toward the goal of reading texts, books, and documents from volumetric scans. We anticipate improvements in scanning technologies in the areas of resolution and sensitivity to materials, which together with work such as ours will move forward the analysis of documents from penetrating scans.

Acknowledgements

We gratefully acknowledge support for this work under NSF grants IIS-9817483 and ANI-0121438. We thank the following collaborators for their roles in this work: Kevin Donohue, Ivan George, Joe Gray, Jim Grifﬁoen, David Jacobs, and Tim Vetters.

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:17:05 UTC from IEEE Xplore. Restrictions apply.

**Figure 3.** (a) The rolled papyrus sample encased in a polyurethane sphere. (b) One of the scanned CT slices of the rolled sample. (c) The papyrus Mobius band sample. (d) One of the scanned CT slices of the Mobius band.
