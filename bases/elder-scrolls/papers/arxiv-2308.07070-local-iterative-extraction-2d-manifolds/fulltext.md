---
id: arxiv-2308.07070-local-iterative-extraction-2d-manifolds
title: "A Local Iterative Approach for the Extraction of 2D Manifolds from Strongly Curved and Folded Thin-Layer Structures"
year: 2023
backend: pymupdf
---

A Local Iterative Approach for the Extraction of 2D Manifolds

from Strongly Curved and Folded Thin-Layer Structures

Nicolas Klenert , Verena Lepper, and Daniel Baum

## (préambule)

**Fig. 1:** Extraction of three pieces of a 2000-year-old, folded silver sheet from the Museum Varusschlacht im Osnabr¨ucker Land, Germany. Left: Volume rendering of the folded silver sheet. Middle: Three 2D manifolds extracted from the silver sheet. Right: The corresponding flattened silver pieces rendered with thin-volume rendering [16]. Colors indicate correspondence.

## Abstract

Ridge surfaces represent important features for the analysis of 3-dimensional (3D) datasets in diverse applications and are often derived from varying underlying data including flow fields, geological fault data, and point data, but they can also be present in the original scalar images acquired using a plethora of imaging techniques. Our work is motivated by the analysis of image data acquired using micro-computed tomography (µCT) of ancient, rolled and folded thin-layer structures such as papyrus, parchment, and paper as well as silver and lead sheets. From these documents we know that they are 2-dimensional (2D) in nature. Hence, we are particularly interested in reconstructing 2D manifolds that approximate the document’s structure. The image data from which we want to reconstruct the 2D manifolds are often very noisy and represent folded, densely-layered structures with many artifacts, such as ruptures or layer splitting and merging. Previous ridge-surface extraction methods fail to extract the desired 2D manifold for such challenging data. We have therefore developed a novel method to extract 2D manifolds. The proposed method uses a local fast marching scheme in combination with a separation of the region covered by fast marching into two sub-regions. The 2D manifold of interest is then extracted as the surface separating the two sub-regions. The local scheme can be applied for both automatic propagation as well as interactive analysis. We demonstrate the applicability and robustness of our method on both artificial data as well as real-world data including folded silver and papyrus sheets.

Index Terms—Ridge surface, crease surface, 2D manifold extraction, fast marching, virtual unfolding, historical documents.

INTRODUCTION

With the advances in imaging techniques in recent decades, a new era in the analysis of historical written and decorated documents has begun. Instead of physically investigating the often very fragile documents, which bears the risk of damaging or even destroying them, the documents are instead imaged and virtually analyzed [8, 9, 17, 26, 29, 30, 34, 36, 41, 42]. One important step in this process is the reconstruction of the geometry of the thin-layer document described by, for example, the medial surface of the writing material. For rolled or simply folded documents, the geometry reconstruction can often be done in 2D cross-sections of the image data, resulting in 1-dimensional (1D) contours for each cross-section. The contours of consecutive cross-sections can then be concatenated to form a 2D manifold describing the document’s structure [8,30,34,36]. However, many historical documents show a more complex folding structure, that is, they are folded along at least two different directions [8,9,41]. Such documents are usually either only reconstructed piece-wise [41], that is,

• Nicolas Klenert and Daniel Baum are with Zuse Institute Berlin. E-mail: {klenert | baum}@zib.de. • Verena Lepper is with ¨Agyptisches Museum und Papyrussammlung. E-mail: v.lepper@smb.spk-berlin.de.

Manuscript received xx xxx. 201x; accepted xx xxx. 201x. Date of Publication xx xxx. 201x; date of current version xx xxx. 201x. For information on obtaining reprints of this article, please send e-mail to: reprints@ieee.org. Digital Object Identifier: xx.xxxx/TVCG.201x.xxxxxxx

not in their entirety, or the reconstructed documents might be subject to strong deformations [8]. A notable exception is the recent work on unfolding letters [9]. But even for rolled documents, the cross-sectional approach does not always work, for example in case of deformations due to buckling perpendicular to the folding direction [28,29].

In this work, we address the limitations posed by previous analysis methods for folded historical documents by tackling the reconstruction of the 2D manifold directly in 3D. Since we know that the historical documents which motivated this work were open, orientable 2D manifolds before being folded, we are particularly interested in methods that allow the extraction of 2D manifolds with such properties. For this, we carefully analyzed previous methods for ridge-surface extraction for their suitability regarding the geometric reconstruction of 2D manifolds of historical documents. Among the previous works, we identified the one by Algarni and Sundaramoorthi [1] as the most promising one for our purpose. Similarly to their method, we employ fast marching to compute optimal paths. However, as our modifications to the algorithm of Algarni and Sundaramoorthi are extensive, we consider our proposed method a novel method for extracting 2D manifolds. In fact, all steps of their algorithm have been either modified or replaced:

• The overall global approach was replaced by a local one that besides enabling the reconstruction of 2D manifolds from strongly curved and folded structures also improves the performance.

• The algorithm for ridge extraction was improved to compute the optimum instead of an approximation.

• For the calculation of the ridge surface, a novel idea and imple-

mentation details are presented.

• Our method does not use cubical complexes and thus is easier to implement and modify to yield subvoxel precision.

• The surface generated by our algorithm is guaranteed to be an orientable 2D manifold. Their method only guarantees the creation of a complex which is homotopy-equivalent to a point, that is, it is retractable. More details can be found in Sect. S1 of the Supplementary Material.

In summary, our main contributions can be described as follows:

• A novel method for the extraction of 2D manifolds from (µ)CT scans of thin and highly curved documents that is less prone to noise than previous methods based on differential operators like the Hessian. It also does not make use of scale-space approaches that may distort the data and may lead to topological changes in order to be robust against noise.

• The resulting surface is guaranteed to be an orientable 2D manifold without any constraints on the input data or parameters, and small holes as well as small surface patches are less likely to occur. Both properties are important for historical documents to make their full contents accessible.

• Our local, iterative scheme enables straightforward integration of user input, allowing the extraction of 2D manifolds from even very challenging data for which a full automation is not yet possible. At the same time, it supports easy fine-tuning of the parameters.

• Our novel methods are rigorously mathematically defined in a continuous setting for easy implementation and modification.

The rest of the paper is structured as follows. Previous methods are described in Sect. 2. The proposed algorithmic pipeline is then presented in Sect. 3, followed by a short description of the most important implementation details in Sect. 4. In Sect. 5, we present the results for several artificial and real data sets and analyze the robustness of the tested methods w.r.t. noise and other challenging image characteristics. Our findings are then discussed in Sect. 6 and conclusions as well as ideas for future work are presented in Sect. 7.

RELATED WORK

Our work is motivated by the analysis of 3D image data of strongly curved and folded, written and decorated, historical documents. In the volumetric image data, the documents are usually represented as thinlayer structures, which often resemble ridges or valleys that are also called creases. Since they represent important features for the analysis of 3D data, they have raised a great interest in many visualization applications [13,20,21,31–33].

Early definitions of such extremal structures in the context of image analysis were given in the works by Haralick [14], Koenderink and van Doorn [23], and Eberly et al. [11]. A good summary of these early definitions is given by Schultz et al. [35]. In their work, they also showed that when extracting crease surfaces, which are 2D manifolds in 3D space, it is important to consider degeneracies of the Hessian. Moreover, they presented an efficient algorithm for the extraction of crease surfaces that outperformed previous methods, both in terms of accuracy and speed. Based on the work by Schultz et al. [35], Barakat et al. first presented an efficient rendering approach for crease surfaces [7]. Later, they proposed an efficient meshing scheme intertwining ridge point sampling and meshing to yield accurate approximations of crease surfaces [6]. For the efficient and more robust sampling of locations of points on the crease surface, they make use of the scale-space particle sampling approach presented by Kindlmann et al. [22].

In contrast to the methods described above, which all make use of the Hessian, Algarni and Sundaramoorthi [1] developed an approach based on optimal paths [37] in combination with a topological reduction of a volume to a retractable surface. Their method requires a single seed point, which can often be computed automatically. In extensive tests, they showed that their approach is more accurate and produces less holes than the one by Schultz et al. [35].

For completeness, Poisson reconstruction [18] and medial surface extraction [3] methods should also be mentioned, since both of these approaches allow the generation of surfaces. However, just like the isosurface computation, the Poisson reconstruction method yields only closed surfaces, or in the case of screened Poisson reconstruction [19], also surfaces reaching the boundary of the domain itself. In our data, the boundary of our surface lies in the domain and is not known beforehand. Medial surface methods, on the other hand, do not guarantee to produce 2D manifolds. Since the surfaces we want to extract are usually open 2D manifolds, neither of the two approaches is applicable to our usecase and data.

Apart from the more methodologically oriented works described above, recently, a processing pipeline for the automatic unfolding of folded letters was presented [9]. Their pipeline combines many processing steps in a sophisticated way but their surface reconstruction step does not guarantee a 2D manifold. They also make some assumptions, for example, that the thickness of the writing material should not vary too much, which cannot be guaranteed in our application, in particular in case of papyrus but also folded silver sheets.

We closely investigated and assessed the methods mentioned above for their suitability to extract 2D manifolds from 3D image data of historical, written documents. As result of this assessment, we develop a new algorithmic pipeline that is described in the next section and compared to other methods in Sect. 5.

ALGORITHMIC PIPELINE

In this section, we motivate and describe in detail each processing step of the proposed algorithm. Note that this description is for a continuous setting and that we use the term surface for a set of points that are almost everywhere equivalent to a 2D manifold. Details regarding the implementation in the discrete setting are provided in Sect. 4.

Problem Statement

Let Ω⊆R3 be a domain containing a 2D orientable manifold MR. Let also p : Ω→[0,1] be a probability field, where p(x) tells us how likely it is for MR to contain point x. Given the probability field, we try to reconstruct MR. For a given manifold MR, the best possible probability field would be the characteristic function

popt(x) :=

if x ∈MR, otherwise.

In this case, MR could be directly extracted from popt. In real-world applications, however, such a probability field is not realistic. Instead, the probability field p can be quite blurry, with large values near MR, and may also contain a lot of inhomogeneous noise. For all examples used in this work, the probability field p is derived from the volumetric input data by clamping the image values to a user-defined range with linear mapping inside the range. For the real-world data, the volumetric input data are given by the intensity values of the µCT scans.

Overview of the Algorithmic Pipeline

The algorithmic pipeline can now be summarized as follows. Let S be a set of seed points for which we assume that they are on or close to the orientable 2D manifold MR that we are looking for. Also, let MR∗ be an empty surface. Then, for each s ∈S , we do the following:

1. Compute optimal paths within the probility field p w.r.t. some cost function cfm (see Sect. 3.3) with a user-defined maximum distance starting from s, generating a connected region I≤˜t around the seed point, using fast marching in p. Fast marching determines for each point inside this region a distance and a time value.

2. Compute isosurface I˜t of the generated time field t with the smallest time value ˜t such that I˜t contains a point with distance to s larger than a user-defined value (Fig. 2B). Select the connected component S˜t of I˜t that fully contains I≤˜t.

3. Label S˜t with two labels, S˜t,1 and S˜t,2, such that the 1D contour on S˜t separating the two labels lies in MR. For this, two poles

s

−→

I˜t

−→

−→

S˜t,1

−→

S˜t,2

−→

## (préambule)

**Fig. 2:** Illustration of the proposed method for a single seed point s. (A) Image data showing a smooth thin-layer structure with some noise and the seed point s for fast marching. (B) Time field t resulting from fast marching starting in s. The lines from near the seed point in both directions illustrate the flooding sets to identify starting points for the labelling of the isocontour of the time field. (C) The length field of the computed optimal paths that was used for the labeling and the labeled isocontour I˜t, which here is equivalent to S˜t. (D) Propagation of the isocontour labels S˜t,1 and S˜t,2 to its enclosed region, the interface of which represents part of the desired manifold MR.

are generated on S˜t that are flooded w.r.t. the generated distance mapped to S˜t (Fig. 2C).

4. Propagate the two labels starting from S˜t to the inside of region I≤˜t, resulting in a labelling of I≤˜t with two distinct labels (Fig. 2D).

## 5. Extract the surface patch M separating the previously generated labels for I≤˜t.

## 6. Merge the surface patch M into MR∗.

In our implementation (Sect. 4), we do not merge the local surface patches but instead the local, labeled regions, taking into account the time values. Also, we implemented an automatic, iterative seed point generation step to automate the extraction of MR. Hence, in general, only an initial single seed point is required.

A suitable approach to reconstruct MR from the probability field p is the extraction of its 2D ridge structures (ridge surfaces). In the following, we turn to the problem of extracting ridge surfaces from p. To define a ridge surface, we first define ridge points akin to the height definition of Eberly et al. [11].

3.1. Definition Ridge Point Let (M,g) be an n-dimensional Riemannian manifold with M ⊂Rn denoting the differentiable manifold and g the Riemanian metric, which induces the local norm on the tangent bundles of the manifold. Further, let f : M →R be a continuous function. A point x ∈M is called a ridge point of type n −l for some l ∈N,l ≤n, if there exists an ε > 0, an exponential map expx : En →M with En := {y ∈TxM | |y|x < ε}, and a linear l-dimensional subspace Tl of TxM such that for all y ∈Ed := En ∩Tl it holds that f(x) > f(expx(y)).

A ridge point of type n−l is thus a point on the n-dimensional manifold M that is a local maximum in l independent directions. And the set of ridge points of type n−l forms an (n−l)-dimensional manifold. We call a 2D manifold of ridge points a ridge surface. For the problem stated in Sect. 3.1, we have n = 3, l = 1, and the ridge points we are interested in are of type 2.

Assuming that a surface that fits well to the probability field coincides with a prominent ridge surface of that field, methods for calculating ridge surfaces by computing the Hessian for each point can be used. However, since the Hessian is very sensitive to noise, another approach was utilized by Algarni and Sundaramoorthi [1] based on the fast marching method to find optimal paths through the probability field. The idea of their approach is that the ridge points of type 1 of some function d on the fast marching front are points of the surface MR we are looking for. Here, the value of d for a point x is defined as the length of an optimal path from x to some start point, where the optimal path was generated by the fast marching method. Thus, instead of calculating ridge points of type 2 in R3, the ridge points of type 1 on a surface S in R3 are calculated.

Optimal Path Computation by Fast Marching

We use the extended real numbers R := R ∪{−∞,+∞} and write

f(∞) = y for any set Y and any function f : R →Y if the limit limu→∞f(u) = y exists. Furthermore, for some closed volume C ⊂R3, let n(x) be the normal of the surface δC at point x ∈δC.

3.2. Definition Eikonal Equation [39] Let Ω⊆R3 be an open set, S ⊆Ωthe set of starting points, t : Ω→R and cfm : Ω→[0,∞]. The classical eikonal equation is known as

|∇t(x)| = cfm(x) ∀x ∈Ω,

t(x) = 0 ∀x ∈S .

The fast marching method [37] finds an approximate solution t to this equation given a cost function cfm. As all variations of the algorithm are using the causality property, better known as the upwind condition [38], the solution is calculated from the starting points s ∈S outwards into the domain Ω, creating one or multiple fronts of points for which a possible value t(x) is calculated.

The time field t can then be seen as the time the fast marching algorithm took to march from a point in S to point x, which is the minimal amount of time required, given the cost function. Note that as t can be interpreted as the time of arrival for an optimal path, which starts from s and is created by fast marching, the maximal integral curves of ∇t represent the optimal paths themselves (see, e.g., [24] for a definition of maximal integral curves). We assume the length of an optimal path to be given by d(x) and we say that the distance between x and S is d(x).

Given a probability field p : Ω→[0,1] ⊂R, we solve the eikonal equation (Definition 3.2) with cost function cfm : Ω→[0,∞],

cfm(x) :=

( 1−p(x)

p(x) if p(x)̸ = 0,

∞ otherwise.

Note that the starting points S should lie in the manifold MR.

Bundling of Optimal Paths If S contains exactly one point s, then the region I≤˜t := {x ∈Ω| t(x) ≤˜t} is connected for any ˜t ∈[0,∞]. However, the isosurface I˜t := {x ∈Ω| t(x) = ˜t} is not necessarily connected. Let S˜t be the connected component of the isosurface I˜t which encloses I≤˜t, and let S≤˜t be the closed volume of S˜t. Thus, we have I≤˜t ⊆S≤˜t.

For our case, we are mostly interested in isosurfaces of t and integral curves of ∇t. An isosurface I˜t gives us the front of the fast marching algorithm at time ˜t and an integral curve for some point in I˜t follows the fronts It′ of the fast marching algorithm through time t′. Integral curves of ∇t can be seen as an “orthogonal” element of the isosurfaces of t in the sense that the normalized tangent of the integral curve of any point x with t(x) = ˜t is the same as the normal of the isosurface I˜t at x.

Due to the upwind condition of the fast marching algorithm, s is the only local minimum of the time field. Together with the fact that for any point x on I≤˜t and any u ∈R, any integral curve Γx : T →I≤˜t with Γx(u) ∈I˜t must have as tangent vector Γ′x(u) = ∇t(x) a vector with a direction pointing to the outside of I≤˜t (again because of the upwind condition), a maximal integral curve can only start at s, that is, T = [−∞,umax],umax ∈R and Γx(−∞) = s. If the integral curve ends in a local maximum, the same reasoning can be applied to show that umax = ∞is the case. Otherwise Γx(umax) ∈I˜t, that is, it can only end on I˜t, with umax ∈R.

The other direction also holds: No integral curve on I≤˜t can pass through a local maximum or a point x on I˜t, as the gradient at a local maximum is 0 and the gradient at x on I˜t is the normal of I˜t at x.

With these properties in mind, we are able to define a mapping from I˜t to I≤˜t, that also defines a non-overlapping partition. A new partition, which we will call flooding sets, are created by slight modifications of the mapping induced partition. These flooding sets will allow us to project labels from S˜t to S≤˜t and vice versa.

3.3. Definition Integral Curve End Mapping Let Ω⊆R3 be open, C ⊂Ωbe a smooth, compact manifold with a boundary, and t : Ω→R a differentiable function. We define a mapping on C:

ζ(x) := Γx(umax) ∀x ∈C

with Γx : [umin,umax] ⊆R →C being the maximal integral curve of ∇t.

The integral curve for each point x is unique and well defined, because the solution t of the eikonal equation is differentiable and bounded on all compact sets. The uniqueness and existence is a classical result from the theory of ordinary differentiable equations [4, p. 305]. In consequence, the mapping ζ is also well defined.

3.4. Theorem Integral Curve End Mapping Induced Relation Let Ω, t, C and ζ be the same as in Definition 3.3. Also, let

n(x) = ∇t(x)

|∇t(x)|

for all x ∈δC with ∇t(x)̸ = 0. Then the following statements hold:

1. ζ induces an equivalence relation,

2. the surjective image of ζ is δC∪E, where E are the local maxima in C regarding t, and

3. for any x ∈δC ∪E, we have ζ(x) = x.

For the proof, see Sect. S4 of the Supplementary Material.

The partition defined through ∼ζ depends on since the local maxima bundle multiple sets together into one. This can be seen in the image on the right, in which all integral curves on the left side end in the local maximum and, thus, belong to one equivalence class as long as the local maximum is contained in C.

One can observe that not only I≤˜t but also S≤˜t for any ˜t ∈R is a valid choice for C. Thus, given a labeling of δS≤˜t ∪E = S˜t ∪E, we are able to label S≤˜t by giving all elements in the equivalence class the same label. However, our aim is to create a partition of S≤˜t with representatives only in S˜t. To achieve this, we can combine equivalence classes with an element in E with another class with an element in S˜t.

Our solution is to use a flooding algorithm and map integral curves which end in a local maximum to another nearby integral curve which ends in S˜t. We call the partition obtained from the flooding algorithm starting at point x the flooding set of x. If no local maximum exists in S≤˜t, then this is equal to the inverse image ζ −1(x).

Ridge Curve Extraction

Given a surface MR and a discrete probability field

pdisc(x) :=

y1 if x ∈MR, y2 otherwise,

with y1 > y2 and y1,y2 ∈[0,1], Algarni and Sundaramoorthi [1] proved that points of MR must be ridge points in S˜t w.r.t. the distance field d. Furthermore, we assume MR to intersect S˜t such that S˜t \MR are two connected components, S˜t,1 and S˜t,2, and S˜t ∩MR is a closed contour on S˜t (see Fig. 2). This condition allows us to describe a robust labeling algorithm for S˜t, and we say that the surface MR intersects S˜t fully. Thus, we search S˜t for closed contours containing ridge points w.r.t. the

distance field d. Such a closed contour will simply be called a (1D) ridge in S˜t.

A classic hierarchical watershed algorithm on the distance field of the fast marching evaluated on S˜t can be used to find such ridges. However, we found that in practice, a flooding algorithm creates better and more stable results. Given a closed surface S˜t ⊂Ωand two starting points u1,u2 ∈S˜t on the surface, we split the surface into two parts S˜t,1 and S˜t,2. The set S˜t,1 contains all points x on S˜t for which the minimal cost of a path from x to u1 is less than a minimal cost path from x to u2. The set S˜t,2 is defined similarly. The cost of a path γ : [0,1] →S˜t from x to y, that is γ(0) = x and γ(1) = y holds, is defined by

crc(γ) := max

z∈[0,1]d(z).

To find the two points u1 and u2 on the surface, we make use of the flooding sets of t as well as the structure tensor of the 3D probability field p at the given seedpoint. Let A be the structure tensor at the seedpoint s for which the fast marching created the given closed surface S˜t as a part of an isosurface. Let v1 be the eigenvector of the structure tensor with the largest eigenvalue. We set u′

1 := s + λ v1 |v1| and u′

2 := s−λ v1

|v1| for a user-defined constant λ. In practice, λ depends on the thickness of the layers, the distance between layers of the probability field and the curvature of the manifold. If u′

1 is on or outside of the surface S˜t, we define u1 to be the point on the surface which is between s and u′

1. Otherwise, if u′ 1 is inside of the surface S˜t, we start a flooding algorithm at u′

1, which prefers the highest possible time values t. The first point of S˜t which is flooded by the algorithm is defined as the point u1. In other words, u1 ∈S˜t ∩F(u′

1), where F(u′ 1) is the flooding set of u′

## 1. We define u2 analogously.

Extraction and Merging of Surface Patches

Given a closed surface and a partition of the surface into two pieces, one may also partition the inside of the surface by following the flooding sets. Let Ω⊆R be a domain, S˜t ⊆Ωa closed surface and S˜t,1,S˜t,2 a partition of the surface into two parts. Then, we have a partition of the inner volume given by the flooding sets, their representatives and the labeling of the surface.

Since S˜t,1 and S˜t,2 are retractable and as union homeomorphic to a sphere, each of them is homeomorphic to a disk. As the front of integral curves can only change their topology through time by the existence of a local maximum – ‘splitting’ the front – and flooding sets always relate the integral curves ending at the local maximum to a neighboring integral curve, the topology of the front of flooding sets does not change until it contracts to the single seed point. Thus, the partitions of the volume S˜t are homeomorphic to a solid sphere. The border between the two components defines the surface patch of interest and is guaranteed to be a 2D manifold and in fact homeomorphic to a disc.

Our calculations are based on the assumption that the surface MR intersects S˜t fully. In consequence, the value of ˜t cannot be chosen too high as the front of the fast marching algorithm would otherwise grow further outside beyond the surface itself. Thus, the surface patch generated by S˜t is only a part of the whole 2D manifold MR we try to reconstruct. Instead of extracting multiple surface patches and merging them, we merge the two components of S≤˜t for all seed points (Fig. 3). The manifold MR is then given by the interface between these two components.

Let S := {s0,s1,...,sn} ⊂R3, n ∈N be a finite list of seed points. For each seed point si ∈S , we obtain for all points x ∈S≤˜t a time ti(x) and a label li(x) ∈{2i+1,2i+2} that encodes to which seed point and component, S˜t,1 or S˜t,2, the point belongs. For any other point y /∈S≤˜t, we define ti(y) := ∞and li(y) := 0. We also define the dominant seed point of a point x ∈R3 to be the seed point with the smallest arrival time

dsp(x) := argmin

i=0,...,n

ti(x).

In the case that there is more than one seed point with smallest arrival time, any one can be chosen. The resulting time and label fields are

**Fig. 3:** Comparison of global vs. local, iterative approach. Top row: Time fields of the fast marching method are shown using the viridis colormap. Bottom row: Label fields resulting from our approach. From the interface between the labels, the manifold to be reconstructed is computed. (A) Illustration of the global approach with a single seed point, as proposed by Algarni and Sundaramoorthi [1]. The 2D manifold of the strongly curved and folded structure cannot be fully reconstructed. (B) A single local step starting from the same seed point as in A. (C) Two more seed points were added. (D) Full reconstruction of the manifold after four additional seed points have been added.

then defined to coincide with the dominating seed point

tΣ(x) := tdsp(x)(x) and lΣ(x) := ldsp(x)(x).

Note that the choice of the labels allows us to find the dominating seed point through the label value itself, as it holds true that

dsp(x) =

lΣ(x)−1



.

Each seed point has its own two labels and we also have a label for the background. To generate a merged surface, we must cast these 2n+ 2 labels to only two (the background label is excluded here). For this, we want to define an equivalence relation ∼2 between labels. Let µ be a measure (see for example [5, p. 41-42]) and i, j ∈{0,...,n} arbitrarily chosen but fixed. Furthermore let Lpq := l−1

i (2i+ p)∩l−1

j (2j +q) for any p,q ∈{1,2} and crel := µ(L11)+ µ(L22)−µ(L12)−µ(L21). We set the relations

2i+1 ∼2 2j +1 and 2i+2 ∼2 2j +2 if crel > 0, 2i+1 ∼2 2j +2 and 2i+2 ∼2 2j +1 if crel < 0.

Note that we do not set any relations if crel = 0. The relation ∼2 is reflexive as L11 > 0, L22 > 0, L12 = 0 and L21 = 0 holds for i = j, and symmetric by definition. We furthermore enforce the transitivity, that is, if k1 ∼2 k2 and k2 ∼2 k3, then we also set k1 ∼2 k3 for all k1,k2,k3 ∈{1,...,2n+2}. Thus, the relation is an equivalence relation.

The seed points i and j have an overlap if and only if µ(L11) + µ(L12)+ µ(L21)+ µ(L22) > 0. In the edge case that the seed point i and j have an overlap but crel is 0 we may assume the patch generation to contain errors. Otherwise if all seed points are connected via overlap and the patch generation does not contain an error, the relation ∼2 has at most two equivalence classes. If the generated surface is nonorientable, the relation has exactly one class. As we are interested in surfaces which can be unfolded, we may assume the relation to have two equivalence classes. Thus, we are able to switch the labels 2i+1 and 2i+2 for all i ∈{0,...,n} such that crel is always positive. This simplifies our relation ∼2 as now it is completely described by

2i+1 ∼2 2j +1∧2i+2 ∼2 2j +2 ∀i, j ∈{0,...,n}, or alternatively

∀k1,k2 ∈{1,...,2n+2} : k1 ∼2 k2 ⇔k1 ≡k2 (mod 2) .

Together with the background label, we now have 3 labels but are only interested in the shared border of the two labels 1 and 2, disregarding the border with the background label.

Seed Point Neighbors Merging patches by the use of a label field sidesteps many specialized operations on surfaces, however it creates another problem: the creation of unwanted surfaces. The image on the right gives an example which showcases a label field with two labels and a manifold (black curve) which could have created such a label field. However, one can

see that the border between the labels not only includes the manifold itself (black curve), but that there is a second border between the same labels.

To solve this, we make use of the fact that the border between the two labels shall only describe a surface if the seed points responsible for the labels are neighbors. The intuition is that a neighbor relationship between seed points describes which seed points are near each other on the manifold such that labels from another layer do not interfere with the current layer.

Let S := {s0,s1,...,sn}, n ∈N again be a finite set of seed points. We define a neighborhood graph G with vertices S . The points si ∈S and sj ∈S are adjacent to each other in G if and only if

δLsi ∩δLsj̸ = /0 with

δLsi := {x ∈R3 | ∃ε > 0,y1,y2 ∈Uε(x) such that

lsi(y1) = 2i+1 and lsi(y2) = 2i+2}

and δLsj analogously. Then δLsi is the set of border points between the two labels of the seed point si and two seed points are connected exactly when they have a border point in common.

IMPLEMENTATION Fast Marching. We implemented the classical fast marching algorithm [37]. If the upwind condition is broken in 3D, we reduce the dimension of the update step, similar to the work by Deschamps and Cohen [10] to guarantee that the upwind condition holds. As the values of the solution t can become huge, we update the values depending on the mean of all neighboring values. This is numerically more stable. The Euclidean length d of the optimal paths can be calculated at the same time as t. Fast marching is done on t but the same update steps for t are also applied to d, with the only difference that d has as cost function the constant function cd(x) = 1. Our stopping criteria for the fast marching front is specified by a user-defined upper bound for the path length d. The fast marching is stopped when the first value higher than that is encountered. The choice of d is related to the average thickness of the thin-layer structure that we are interested in. As a rule of thumb, it should be at least 5 to 10 times the thickness. However, the choice of d mainly influences the performance in terms of run time, not quality. When d becomes too large, run time might increase drastically. Flooding. In Sect. 3.5, we use a standard flooding algorithm over voxels. Given a set of voxels V, the algorithm greedily takes the voxel neighboring a voxel in V with the highest time value and inserts it into V. This is repeated until a voxel is found which is at the border of S≤˜t. The same algorithm is used with faces instead of voxels to label S˜t given two faces on S˜t to grow out from. Instead of the time values, the distance values generated by the fast marching method are used. Flooding could also be used to find the labels of the voxels in S≤˜t in Sect. 3.6, however, it is faster to go the other direction and propagate the labels from the outside to the inside, that is, starting from S˜t, using the time values again. To do this, we insert all voxels at the border, which are already labeled, in a sorted set V, take the voxel with the highest time value out of the sorted set and insert all its neighbors which are not yet labeled into V. This is repeated until V is empty and therefore all voxels in S≤˜t are labeled.

Automation. We implemented a simple, iterative approach to automatically add further seed points. Given a surface and the seed points which were used to construct the surface, we want to generate new seed points. This could be done by generating points on the boundary of the surface, but small inconsistencies of the ridge curve extraction might occur. However, these inconsistencies tend to vanish when moving only a slight distance away from the surface boundary. Therefore, a more stable method is to set seed points some distance away from the boundary of the surface. Furthermore, if an already generated seed point is near the boundary of the surface, the fast marching algorithm did not prefer growing in the direction of the boundary. Therefore, we may assume to have reached the end of the 2D manifold we want to extract. In summary, we can automate the generation of seed points by finding points on the surface that are a specific distance away from the boundary (10% of the marching distance in our case) and are far away from all seed points (30-50% of the marching distance is often a good value). If no such point exists, the automation stops and we assume that the whole surface was extracted. Iterative Construction. Note that even though we defined the relation of different labels in Sect. 3.6 explicitly, they can be calculated iteratively by adding one seed point after another to the set S . Hence, we only need to save the global time field t, the global label field l, the neighboring graph and the constructed surface of the current set of seed points. Given a new seed point, the time and label fields as well as the neighborhood graph are updated and the newly created patch is merged with the surface. For this, a modified marching cubes algorithm [15] can be used to generate triangle meshes based on Sect. 3.6 and Sect. 3.7. The new triangles are then concatenated to the surface. Old appendages of the surface that were created by voxels for which the times were updated, are deleted. The modified marching cubes algorithm [15] allows the handling of a background label. Alternatively, by changing the labeling of a voxel from the background label to one of the other two labels, depending which label appears the most in the neighboring voxels, the classical marching cubes algorithm [25] can be used instead. Neighborhood Graph. The update of the neighborhood graph is done by checking for common border points of the newly added seed point and the old seed points. As we work with voxels, our border points are faces between the two labels generated from the seed points. Given the transitivity rule of the label relation as well as our assumption of an orientable surface, we make use of the simplified description of label relation and switch the labels of the newly added seed point such that the relation holds. Furthermore, as we discretize the volume in voxels, we work with a finite number of elements. Thus, the sets L11, L12, L21 and L22 are also finite. Also, as all volume elements are of equal size, we can therefore use the cardinality of the sets themselves as the measure µ. In the marching cubes step of generating the surface, we only generate a triangle inside a cube if the vertices of the cube contain both labels 1 and 2 and only if the dominating seed points of the vertices are connected by the graph G.

RESULTS

In this section, we present results for both artificial and real data. In order to compare our method with one of the state-of-the-art methods in ridge surface extraction [35], we tested both approaches on the same data. Note that we tried to optimize the results of the method by Schultz et al. [35] by testing different strength parameter values. Shown are always what we considered as the best results using their method.

We also present a qualitative comparison with the letter unfolding pipeline [9]. Note that a quantitative comparison is not possible, since the mesh generated by the pipeline does not represent a real surface mesh but rather a graph. Seen as a surface mesh, faces overlap and intersect, and no possible orientation (even for small areas) can be found. Thus, a topological analysis is impossible and we are also unable to show the mesh in two different colors. See Sect S2 in the Supplementary Material for more information. Also, we remark that their method takes 6 minutes to segment our simple surface dataset. For more information, we refer to Sect. S2 in the Supplementary Material.

We also do not include the algorithm of Algarni and Sundaramoorthi [1] in our quantitative comparison, as their method generates many

1 (data) 2 ([35]) 3 (ours)

E

F

G

**Fig. 4:** Reconstruction of a simple plane with different types and degrees of noise shown in the first column. Comparison between Schultz et al.’s method [35], shown in the second column, and ours, shown in the third column. (A) Original scalar image showing a clear ridge. (B) Gaussian noise (10%) added to A. (C) Gaussian filtered image from B. (D) Simplex noise (30%) added to A. (E) Simplex noise (50%) added to A. (F) Warping of image A with strength 2. (G) Warping of image A with strength 4.

non-manifold points. Since both their and our methods make use of fast marching to calculate optimal paths and extract surfaces containing these optimal paths, the generated surfaces are comparable if the right conditions for their algorithm were met and was also done only locally (see Fig. 3). We were also able to improve the performance of their algorithm to reduce the time needed for a patch from over 15 minutes to a few seconds in the case of the silver sheet. For a more detailed description, we again refer to Sect. 1 of the Supplementary Material.

The probability fields necessary for our method were generated by normalizing the image data to [0,1] ⊂R. The surface meshes shown in this section should be orientable and are therefore always colored with two colors, blue for one side of the mesh and green for the other side. This allows to easily distinguish the two sides and to make artifacts in the reconstruction more apparent. Note that the orientation of all meshes was made consistent as a post-processing step after reconstruction. For the visualization of the surface meshes, we deliberately used triangle normals in Fig. 6 and Fig. 7 to give the user a visual feedback of the mesh resolution and quality.

All computations were carried out on a desktop PC with the following configuration: CPU: Intel Core i9-10980XE; GPU: Nvidia GeForce RTX 3090, 24 GiB VRAM; Memory: 128 GiB DDR4.

Artificial Data Artificial data was used to provide a ground truth for the surface reconstruction, which is not available for the real-world data.

Plane The images used to compare Schultz et al.’s algorithm and our method are visualized in Column 1 of Fig. 4. Sect. 3 of the Supplementary Material contains a description on how they were created. From top to bottom the files are called: original, g10, g10.gf100, s30, s50, ws200.gf100 and ws400.gf100. Column 2 of Fig. 4 shows the results by applying Schultz et al.’s method, while in column 3 our results are shown. Notice the degenerate case of A2. This is a known behaviour of Schultz et al.’s method for synthetic data [35]. For real world data, or in our case, synthetic data with noise, such degeneracy is highly unlikely to occur. The results of the quantitative analysis can also be found in Sect. S3 of the Supplementary Material.

Our algorithm always creates a surface that is topologically equivalent to a plane, while the method by Schultz et al. shows some artifacts like a triangle soup (B2) and different degrees of holes (D2-G2), only sometimes generating a valid 2D manifold. Our topological analysis

A (data) B ([9]) C ([35]) D (ours)

**Fig. 5:** Reconstruction of a simply folded plane that was slightly warped (A). Comparison between Dambrogio et al.’s method [9], shown in B, Schultz et al.’s method [35] (C), and ours (D). In B, many holes and one additional surface patch near the folding edge can be seen. In C, only holes at the folding edge are present, but multiple additional surface patches near the folding edge were created. Only our method recreates a topologically correct surface without any additional surface patches.

confirms that. While our method is robust against all types of noise, the result is for low noise images not as precise as their method. We assume that this is mainly due to the fact that we have not implemented sub-voxel accuracy. However for images with strong noise and especially for warped images (which most closely represents our papyrus data), our method creates more accurate surfaces. Also, our method usually creates slightly larger surfaces, reaching out to the very boundary, thereby sometimes resulting in strongly bent surfaces. Last but not least, for low noise images Schultz et al.’s method is slightly faster. However, the performance is highly variable and strongly depends on the strength value. As this value has to be experimentally found (ranging from 150 to 12,000 for this dataset), the real time cost is much higher. Our algorithm in contrast shows similar time cost for all test data.

Simply Folded Sheet

In the second artificial test case, we folded a plane once, added Gaussian blurring to it to simulate a thin-layer structure and slightly warped the

**Fig. 6:** Reconstruction of the Stanford Dragon. Left: Result from the method by Schultz et al. [35]. Right: Our method. The green ellipses highlight regions where the method by Schultz et al. had difficulties while our algorithm did not show any artifacts in the reconstruction.

data. The data as well as the results using Dambragio et al.’s pipeline, Schultz et al.’s method and ours are shown in Fig. 5. In Fig. 5A we show a cross-section through the data. In B, the result of the pipeline by Dambragio et al. is shown. It has a lot of holes and a small wrong patch was calculated near the ridge. This artifact is also visible in C, which shows the result of Schultz et al.’s method. The patches near the ridge are more pronounced. The folding edge is also leaky, but in general the result shows a lot fewer holes than B. Our method in D creates a surface that is topologically equivalent to a plane, in particular, it does not contain any holes and consists of only one patch.

Dragon

As a third artificial test data set, we used the Stanford Dragon [40]. Similarly to the previous data, the surface was sampled on a uniform grid, here of dimensions 841 × 599 × 388, and smoothed with a Gaussian filter, resulting in a smooth thin-layer structure. No noise was added, but since the dragon shows different degrees of geometrical intricacies, we found it a good test case. Both algorithms were applied to the image data and were able to reconstruct the original surface, as can be seen in Fig. 6, first row. However, the algorithm by Schultz et al. created artifacts, some of which are highlighted in the figure. Our algorithm, which used 820 automatically placed seed points in addition to the first manually placed one, did not create any artifacts.

Real-World Data

The real data shown in this section motivated the work. Computation of the 2D manifold from the set of seed points took 3 minutes for the papyrus data.

Complexly Folded Silver Sheet

Here, we analyzed a µCT scan with dimensions 375×271×614 of a 2000-year-old complexly folded silver sheet (data courtesy by Christiane Matz and Stefan Burmeister from VARUSSCHLACHT im Osnabr¨ucker Land gGmbH, Museum und Park Kalkriese). A volume rendering of the folded sheet together with three pieces that were reconstructed with the proposed method are shown in Fig. 1. Note that in order to visualize the flattened pieces, the extracted 2D manifold meshes were drastically simplified using the algorithm by Garland and Heckbert [12], subsequently flattened into the 2D plane utilizing quasi-isometric flattening proposed by Ambellan et al. [2], and finally visualized with the thin-volume rendering by Herter et al. [16]. Simplification was done for two purposes. First, it made the flattening more robust. Second, and more importantly, in order to visualize the ornaments that are impressed into the silver sheet, the approximating surfaces should not follow the impressed ornaments but be smooth in these regions. Otherwise, the ornaments would be flattened away. A simple way to create a smooth mesh that does not follow the ornamental details is achieved using standard mesh simplification methods.

In Fig. 7, we compare the results of the surface reconstruction using the method by Schultz et al. and our method. Their global approach, that computes all ridge surfaces in the image data, worked remarkably well for the silver sheet. Nevertheless, many floating triangles and triangle patches can be observed in Fig. 7 when zooming in to the electronic version of the paper. Many of these triangles could be removed easily. However, as is indicated by the color change of the surface shown in Fig. 7A,B, wrong connections occurred resulting in a surface mesh that was not orientable anymore, which is a requirement for the subsequent unfolding step. Identifying and removing these connections to end up with an orientable 2D manifold might be very tedious. With our method, we have full control over the reconstruction

**Fig. 7:** Comparison of reconstruction results for the folded silver sheet shown in Fig. 1. (A) Complete reconstruction of the silver sheet using Schultz et al.’s method. (B) Reconstruction of three pieces of the silver sheet using our method. (C+D) Zoom-in to the rectangular region of A+B, respectively. Note the color flip in A+C in the highlighted region. This shows that the extracted surface mesh is not orientable anymore but instead contains a (wrong) connection changing the orientation.

process that is visually supported. One of the three pieces of the sheet was fully automically reconstructred starting from a single seed point. The other two pieces were semi-automatically reconstructed by letting the automatic reconstruction only run for a few steps after which the result was visually checked. This way, we guided the algorithm when the automatic processing made a mistake by removing automatically placed seed points and adding manual ones if needed.

Doubly Folded Papyrus

Here, we analyze a µCT data set with dimensions 454 × 107 × 374 of an ancient papyrus package ([26], Greek papyrus; data courtesy by Eve Menei and Marc Etienne, Mus´ee du Louvre, Paris). The package is folded twice in orthogonal directions. Physically opening it will most likely result in damaging the precious object. Therefore, a virtual unfolding (Fig. 8) is necessary to access the writing.

Since papyrus consists of two layers of papyrus fibers that are oriented orthogonal to each other and then pressed to form the papyrus document, the reconstruction of the document structure is particularly challenging, since these two layers often separate from each other and have a high variability in thickness and intensity. This is especially true for old papyrus and is also present in the data analyzed here. Therefore, it comes as no surprise that the pipeline by Dambragio et al. fails to generate one connected surface, missing a substantial amount of papyrus (Fig. 9, first row). The method by Schultz et al. fails to reconstruct a 2D manifold (Fig. 9, second row). Instead, the separate layers of the papyrus document are locally reconstructed with many connections between these two layers. As can be seen in Fig. 9, third row, our algorithm successfully reconstructs an orientable 2D manifold. In order to achieve this, we had to modify the image data by setting the scalar values in regions where the folded document came too close to itself to 0. Note that the same modified image data field was used for all approaches.

DISCUSSION

In this section, we discuss the results of comparing our novel approach for 2D manifold extraction from thin-layer structures with three other state-of-the-art approaches [1,9,35].

Regarding methods based on the Hessian, we compared our method with the one by Schultz et al. [35]. In agreement with previous work [1], we found that the approach based on the Hessian is not robust to noise (see Paragraph 5.1.1 and Sect. S2 in the Supplementary Material). Furthermore, we showed that it has problems with strongly curved, thinlayer structures (see Paragraphs 5.2.1, 5.2.2). In all real test cases, their method, even though not being developed for such data, did remarkably well. In particular, we were surprised how well it worked on the silver

sheet data. However, we could also clearly show its limitations w.r.t. the characteristics of the data that motivated our work. Even though improvements have been made in terms of speed and robustness [6] compared to the method by Schultz et al., we still consider the latter method as representative for the Hessian approach.

The optimal-path approach, on the other hand, as used by Algarni and Sundaramoorthi [1] and in this work, can deal better with strong noise. Unfortunately, the approach presented by Algarni and Sundaramoorthi [1] does also not fulfill the requirements for the virtual unfolding of ancient documents, motivating this work. We observed several problems for the type of data we were dealing with. First, their approach makes use of one fast marching solution for the entire data field. This has two implications. (1) As the domain Ωis therefore the upper bound for the number of elements for the fast marching algorithm, the performance is O(nlogn), with n being the number of voxels Ωis discretized in. This is noteworthy as complexly folded thin-layer structures necessitate high-resolution image data to allow differentiation between different layers and, hence, n can be very large. (2) As we illustrated in Fig. 3, a global front is not able to follow thin-layer structures which are folded tightly back to themselves, as it will take a shortcut to the next layer instead of following the ridge. Yet, this is exactly what we often have to deal with in case of historical, written documents. Second, their approach does not guarantee that the manifold MR intersects S˜t as a closed 1D manifold. Therefore, the identification of the ridge points on S˜t is unstable and can result in incorrectly extracted ridge surfaces (see Sect. S1 in the Supplementary Material). We also found the ridge-curve extraction method using a recursive watershed approach utilized by Algarni and Sundaramoorthi [1] not stable enough for our data. This is particularly true for papyrus, which often differs too much from a clear ridge structure. Third, the cubical complex reduction of the volume to calculate the surface is not guaranteed to be a 2D manifold. Thus, their approach to extract a surface from a closed ridge line was not viable in our case (see Sect. S1 in the Supplementary Material). To render the approach of optimal paths more suitable for the type of data we have to deal with, we replaced all steps of the algorithm of Algarni and Sundaramoorthi [1]. The resulting algorithmic pipeline has the following properties: (1) it is faster; (2) it creates a surface that is guaranteed to be an orientable 2D manifold; (3) it is viable for highly curved surfaces; (4) it allows adjusting the local parameters to the data, that is, to the denseness of the folded layers as well as the strength of the folding; (5) for very challenging data, it allows the ridge surface to be extracted partially or even completely user-driven, thus giving the user full control over the extraction process.

Finally, we compared our method with the one proposed by Dambrogio et al. [9] for unfolding letters. This very interesting approach seems to be rather specific to the problem of unfolding letters. Limitations are that is assumes a rather similar thickness of the document to be unfolded. This assumption holds true for letters but not for papyrus documents and silver sheets. Nevertheless, their algorithm also did remarkably well on both real datasets. But none of the resulting reconstructed meshes was a 2D manifold and large parts were missing in the initial reconstructed mesh (see Sect. S3 in the Supplementary Material). In particular, the presence of an abundance of non-manifold vertices, edges and faces leads to many problems when trying to post-process the data with state-of-the-art mesh operations.

In terms of our own method, a few things are worth mentioning. As each seed point only affects the resulting surface locally and our algorithm can be implemented iteratively, addition, deletion and modification of seed points can be implemented in such a way that these operations are very fast. In our test cases, it took approximately 0.2 seconds to add one seed point and update the surface. Of course, this time depends on the distance fast marching is allowed to march, and hence, the distance should not be too large. However, empirically, we observed that as long as the distance is a few times larger than the thickest layer of the structure (10 times seems a good heuristic), the parameter does not have a big influence on the quality of the generated surface. Yet, the time performance gets worse for larger values of the parameter and the patches themselves are bigger. For all our datasets, we used the default distance. Finally, we would like to remark that our

**Fig. 8:** Doubly folded papyrus document. (A) Volume rendering of the µCT image of the document, also showing the position of the cross-section depicted in B. (B) Cross-section of the µCT scan shown in A. (C) Volume rendering and extracted 2D manifold mesh. (D) Thin-volume rendering [16] of the flattened papyrus document. Note the writing on the papyrus document.

**Fig. 9:** Comparison of reconstruction results for the folded papyrus document shown in Fig. 8. First row: Method by Dambrogio et al. [9]. Note that the surface is not orientable at all, hence there is only one color. Second row: Method by Schultz et al. [35]. Third row: Our method, resulting in a fully orientable 2D manifold.

algorithm is stable under the location of the starting seed point, which in our case is set manually.

Regarding locality vs. globality, our method can be considered as being in-between the methods based on the Hessian (e.g. [35]), which is a very local one, and a purely global one as proposed by Algarni and Sundaramoorthi [1]. We can adjust the degree of locality depending on the characteristics of the thin-layer structures by changing the maximal distance that the fast marching is allowed to march. The maximal distance parameter as well as a custom cost function per seed point gives us a lot of flexibility that might be needed for the challenging data we deal with. Even more flexibility is provided through the combination of automation and visual interaction allowed by our approach.

FUTURE WORK AND CONCLUSION

The biggest memory and performance bottleneck in our current method are the label and time fields. For large image data, these fields are also large and this results in many cache misses. A method to merge surface patches directly could therefore render these fields obsolete. Furthermore, the consideration made in Sect. 3.7 would not be necessary, allowing for greater marching distances for strongly rolled structures. Last but not least, it would also allow the creation of unorientable 2D manifolds, one limitation our method is currently facing.

A more sophisticated watershed ridge curve extraction in Sect. 3.5 may allow to discern between different equally important ridge contours. This information could be used to decide if the front of the fast marching algorithm took a shortcut to another layer or if intersecting or tangentially connected surfaces inside the marched volume exist. A possible generalization could also allow the construction of a surface and a graph with information of their non-manifold connections, allowing the use of graph cut algorithms or similar, to globally find the best possible 2D manifold or to allow intersecting surfaces. Furthermore, artifacts on the border of the surface (seen, e.g., in Fig. 4) are results of our method trying to maximize the length of the optimal paths. Another

ridge curve extraction approach could mitigate this bias.

Automation can also be approved upon. We believe that a hybrid approach based on both optimal paths and the Hessian could create even better results. One could use as probability field p(x) the probability of a point to be a ridge point defined by the Hessian. This might have the advantages of both worlds, the accuracy of the Hessian approach together with the guarantees of the optimal path approach. A different option would be to place seed points dependent on the Hessian.

Last but not least, anisotropic fast marching [27] might also increase performance and quality of our algorithm, however some questions have to be answered beforehand. How can one calculate the Euclidean distance efficiently while calculating the time field, for example. A further problem is that the anisotropic fast marching algorithm uses stencils reaching over many voxels wide (dependent on the given tensor). This allows the front to “jump over” some high cost voxels, for example, in densely folded areas. Hence, anisotropic fast marching makes it difficult to work with a non-constant scalar field.

Another remaining limitation of all currently available methods is the extraction of surfaces for tangentially connected structures. The separation of such structures will also be subject to future work.

In this paper, we have developed a local optimal path approach for extracting smooth, simple surfaces in noisy 3D data sets. Our novel method is able to extract such surfaces given highly complexly folded and rolled thin-layer structures while taking up to only a single seed point as input. In contrast to other methods, our approach guarantees the construction of an orientable 2D manifold, which is a requirement of many virtually unfolding methods. Furthermore, the locality of our method and, hence, the assignability of local volumes to a seed point enables user interaction and modification of the generated surface, resulting in a semi-automatic workflow that allows one to address even very challenging data.

SUPPLEMENTAL MATERIALS

All synthetic data for the Plane test case (Paragraph 5.1.1, Sect. 3 of the Supplementary Material) used to do the quantitative evaluation of the methods, including the Excel sheet containing the analysis results of Fig. 4, are available on figshare at https://doi.org/10.6084/ m9.figshare.23600115, released under a CC BY 4.0 license.

ACKNOWLEDGMENTS

This work was supported by the German Research Foundation (DFG) through grants BA 5042/2-1 and LE 1837/2-1 awarded to Daniel Baum and Verena Lepper, respectively. We would like to thank Christiane Matz and Stefan Burmeister from VARUSSCHLACHT im Osnabr¨ucker Land gGmbH, Museum und Park Kalkriese, for providing the folded silver sheet, and Eve Menei and Marc Etienne, Mus´ee du Louvre, Paris for providing the papyrus document. Image acquisitions of the silver sheet and the papyrus document were funded by the VolkswagenStiftung (Az 92029) and the European Research Council (Project ”ELEPHANTINE”, ID 637692), respectively. We would like to express

our great thanks to Amanda Ghassaei, one of the corresponding authors of the letter unfolding paper [9], for her great support when running out data sets with their algorithm. Many thanks also to our colleague Ben Schmitt for getting the letter unfolding approach running on our computers and applying it to the various simple data, as well as our colleague Finn Schw¨orer for implementing most scripts to export our data sets to files compatible with the methods we tested our algorithm against.
