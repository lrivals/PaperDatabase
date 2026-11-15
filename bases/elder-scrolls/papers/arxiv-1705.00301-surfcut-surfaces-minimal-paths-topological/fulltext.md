---
id: arxiv-1705.00301-surfcut-surfaces-minimal-paths-topological
title: "SurfCut: Surfaces of Minimal Paths From Topological Structures"
year: 2017
backend: pymupdf
---

SurfCut: Surfaces of Minimal Paths From

Topological Structures

Marei Algarni and Ganesh Sundaramoorthi

## Abstract

We present SurfCut, an algorithm for extracting a smooth, simple surface with an unknown 3D curve boundary from a noisy 3D image and a seed point. Our method is built on the novel observation that certain ridge curves of a function deﬁned on a front propagated using the Fast Marching algorithm lie on the surface. Our method extracts and cuts these ridges to form the surface boundary. Our surface extraction algorithm is built on the novel observation that the surface lies in a valley of the distance from Fast Marching. We show that the resulting surface is a collection of minimal paths. Using the framework of cubical complexes and Morse theory, we design algorithms to extract these critical structures robustly. Experiments on three 3D datasets show the robustness of our method, and that it achieves higher accuracy with lower computational cost than state-of-the-art.

Index Terms—Segmentation, surface extraction, minimal paths, computational topology, cubical complex, Morse-Smale complex

!

INTRODUCTION M

INIMAL path methods [1], built on the Fast Marching algorithm [2] (see also [3]), have been widely used in computer vision. They provide a framework for extracting continuous curves from possibly noisy images. For instance, they have been used in edge detection [4] and object boundary detection [5], mainly in interactive settings as they typically require user deﬁned seed points. Because of their ability to provide continuous curves, robust to clutter and noise in the image, generalizations of these techniques to extract the equivalent of edges in 3D images, which form surfaces, have been attempted [6], [7]. These methods apply to extracting a surface with a boundary that forms a curve, possibly in 3D, which we call a free-boundary. Extraction of surfaces with free-boundary is important because many edges form these surfaces, and edges are fundamental structures that are prevalent in images. Some applications include medical datasets (e.g., lung ﬁssures, walls of heart ventricles) [8] and scientiﬁc imaging datasets (e.g., fault surfaces in seismic images, an important problem in the oil industry) [9]. In [8] an alternative method to extract such surfaces, based on the theory of minimal surfaces [10], is provided. However, existing approaches to surface extraction for surfaces with free-boundary have a limitation - they require the user to provide the boundary of the surface or other user laborious input.

In this paper, we use the Fast Marching algorithm and techniques from computational topology to create an algorithm for extracting the boundary of a surface from a 3D image and a single seed point, and an algorithm to extract the surface. Our main idea is to use Fast Marching to “smooth” a local (possibly noisy) likelihood map of the surface in a way that is guaranteed to preserve locations of critical structures, and then extract the structures with methods, built from computational topology, that guarantee correct topology. We show that the resulting structures correspond to the surface

M. Algarni and G. Sundaramoorthi are with KAUST (King Abdullah University of Science & Technology), Thuwal, Saudi Arabia. Email: {marei.algarni, ganesh.sundaramoorthi}@kaust.edu.sa

of interest, and the surface is a collection of minimal paths. Our method is applicable to any imaging modality, and can be used to extract any simple surface with boundary from an image that contains noisy local measurements (possibly an edge map) of the surface. We demonstrate the method on two applications - fault extraction from seismic images, and lung ﬁssure extraction from CT.

Our contributions are: 1. We introduce the ﬁfirst algorithm, to the best of our knowledge, to extract a closed 3D space curve forming the boundary of a surface from a single seed point. It is based on extracting critical structures from a distance produced by Fast Marching. 2. We introduce a new algorithm, based on extracting a critical structure of the FM distance, to extract a surface given its boundary and a noisy image. It produces a topologically simple surface whose boundary is the given space curve. The surface is shown to be formed from minimal paths. Both boundary and surface extraction have O(N log N) complexity, where N is the number of pixels. 3. We provide a fully automated algorithm using the algorithms above to extract all such surfaces from a 3D image. 4. We test our method on challenging datasets, and we quantitatively out-perform comparable state-of-theart in free-boundary surface extraction.

Related Work

Active surface methods [11], [12], [13], based on level set methods [14], their convex counterparts [15], graph cut methods [16], [17], and other image segmentation methods partition the image into volumes and the surfaces enclose these volumes. These methods have been used widely in segmentation. However, they are not applicable to our problem since we seek a surface, whose boundary is a 3D curve, that does not enclose a volume nor partition the image.

Our method uses the Fast Marching (FM) Method [2]. This method propagates an initial surface (e.g., a seed point) in an image in the direction of the outward normal with speed proportional to a function deﬁned at each pixel of

the image. The end result is a distance function, which gives the shortest path length (measured as a path integral of the inverse speed) from any pixel to the initial surface. The method is known to have better accuracy than discrete algorithms based on Dijkstra’s algorithm. Shortest paths from any pixel to the initial surface can be obtained from the distance function [1] (see also [18]). This has been used in 2D images to compute edges in images. A limitation of this approach is that it requires the user to input two points - the initial and ending point of the edge. In [4], the ending point is automatically detected. These methods are not directly applicable to extracting a surface forming an edge in 3D.

Attempts have been made to use minimal paths to obtain edges that form a surface. In [7], [19], minimal paths are used to extract a surface edge with a cylindrical topology, a topology different from our problem. The user inputs the two boundary curves (in parallel planes) of the cylinder and minimal paths joining the two curves are computed conveniently using the solution of a regularized transport partial differential equation. Surface extraction with less intensive user input was attempted in [6]. There, a patch of a sheet-like surface is computed with a user provided seed point and a bounding box, with the assumption that the patch slices the box into two pieces. The algorithm extracts a curve that is the intersection of the surface patch with the bounding box using the distance function to the seed point obtained with Fast Marching. Once this boundary curve is obtained, the patch is computed using [19]. The obvious drawbacks of this method are that only a patch of the desired surface is obtained, and a bounding box, which may be cumbersome to obtain, must be given by the user.

Another approach to obtaining a surface along image edges from its boundary is minimal surfaces [8], [20]. The minimal weighted area simple surface interpolating the boundary is obtained by solving a linear program. Faster implementations for minimal surfaces are explored in [8], using algorithms for the minimum cost network ﬂflow problem (e.g., [21], [22], [23], [24]). This signiﬁcantly speeds up the approach, although it requires an initial surface, and the algorithm is dependent on it. The main drawback of minimal surfaces is that the user must input the boundary of the surface, which our method addresses. It is also computationally expensive as we show in experiments.

An approach for surface extraction that does not require user input is [25]. There, a matrix based on the local smoothed Hessian matrix of the likelihood is used to generate a ridge in the image near the desired surface. Then surface normals based on the matrix are computed, which are used to generate several surfaces. This method is convenient since it is fully automated. This approach has been tailored to seismic images for extracting fault surfaces [9], and it is the state-of-the-art in that ﬁfield. Our method also smooths the likelihood, but in a way that preserves locations of critical structures, resulting in a more accurate surface. Also, our extraction of the critical structures, by using tools from computational topology, guarantees a simple surface topology.

Computational Topology Our method is a discrete algorithm and is based on the framework of cubical complexes [26], [27]. This framework

allows for performing operations analogous to topological operations in the continuum. It has been used for thinning surfaces in 3D based on their geometry [28] to obtain skeletons (or medial representations [29], [30], [31]) of geometrical shapes. This theory guarantees correct topology of extracted structures. Our novel algorithms use concepts from cubical complex theory. In contrast to [28], our method is designed to robustly extract ridges of a function or data deﬁned on a surface (deﬁned by Fast Marching), rather than geometrical properties of a surface.

Our method uses a topological construction called the Morse complex [32] from Morse theory to extract ridges on a manifold. There is a large literature that aims to compute the Morse complex and an extension called the Morse-Smale Complex, from discrete data [33], [34], [35], [36]. Roughly, these Morse complexes describe the behavior of the gradient ﬂflow of a function within regions. We use cubical complexes to construct the Morse complex since they are naturally suited for image data, deﬁned on grids. Conceptually, our algorithm for the Morse complex appears similar to [35], even though the technical details and notions of discrete topology are different. Our contribution is not to provide another algorithm for the Morse complex, but to use the Morse complex for the purpose of free-boundary surface extraction from images.

Extensions to Conference Paper A preliminary version of this manuscript has appeared in [37]. In this version, we have derived the theoretical foundations: 1) we provide analytical arguments to show that our algorithms correctly capture the surface of interest by relating it to constructions in Morse theory, and 2) we relate the surface extracted to minimal paths by showing the surface is formed by collections of minimal paths, thus inheriting known regularity properties from such paths. We extended our ridge extraction algorithm to better deal with extraneous structures. We have also extended our experiments to more datasets, including medical data, and extended the quantitative comparison to minimal surface approaches.

Overview of Method

Our algorithm consists of the following steps (see Figure 1): i) Weighted Distance to Seed Point Computation: From a given seed point on the surface, the Fast Marching algorithm is used to propagate a front to compute shortest path distance from any point in the image to the seed point (Section 3.1). ii) Ridge Curve Extraction: At samples of the propagating front, the ridge curves of the Euclidean path distance of minimal paths to the seed point are computed (Section 3.2). These curves lie on the surface of interest. iii) Surface Boundary Detection: At snapshots, a graph is formulated from curves from the previous step, and is cut along locations where the Euclidean distance between points on adjacent curves are small, resulting in the outer boundary of the surface (Section 3.4). iv) Surface Extraction: Finally, the desired surface with boundary obtained from the last step is computed (Section 4).

Our method requires notions from topology, which we review next. We then proceed to our algorithm.

Front Propagation Ridge Extraction

Boundary Extraction

## (préambule)

**Fig. 1:** Overview of SurfCut. Starting from a seed point on the surface, a front is propagated (top, left), ridges are extracted (top, right), a cut is performed forming the boundary (bottom, left), and the surface is extracted..

TOPOLOGICAL PRELIMINARIES

In this section, we present theory and notions from topology and computational topology that will be relevant in subsequent sections in designing and justifying our novel algorithms for surface extraction.

Topological Structures

Our algorithms extract topological structures from functions deﬁned on the image domain and manifolds embedded in the image. We give formal deﬁnitions for these topological structures, ridges and valleys, and then the Morse complex.

Critical Structures Intuitively, ridge points of a function deﬁned on a manifold correspond to local maxima when restricted to sub-spaces of directions rather than the whole space of possible directions. Similarly, valley points correspond to local minima of a function when restricted to sub-spaces of directions. We now give more formal deﬁnitions. We consider functions h : M ⊂Rn →R, deﬁned on a n −1 dimensional manifold. For a point x ∈M, we denote TxM to be the tangent space of M at x, which consists of all valid directions at the point x on M. We ﬁfirst deﬁfine the critical points of h as the points p on M where the gradient vanishes, i.e., ∇h(p) = 0. Note that the gradient refers to the intrinsic gradient ∇h(x) ∈TxM, i.e., it is deﬁned by the relation dh(x) · v = ∇h(x) · v for all v ∈TxM where dh(x) · v denotes the directional derivative of h at x and the right hand side is the usual Euclidean dot product. Ridges and valleys are formally deﬁned by [38] as follows.

Deﬁnition 1 (Ridge and Valley). Let h : M ⊂Rn →R where M is an n −1 dimensional manifold. Let λ1 ≤· · · ≤λn−1 and e1, . . . , en−1 ∈TxM, be eigenvalues and eigenvectors of the Hessian Hh(x) at x ∈M. Let k < n −1.

A point x ∈M is a n−1−k dimensional ridge point of h if λk < 0 and ∇h(x) · em = 0 for m = 1, . . . , k.

**Fig. 2:** Illustration of some ascending and descending manifolds of a one-dimensional function.

A point x ∈M is a n −1 −k dimensional valley point of h if λn−k > 0 and ∇h(x) · em = 0 for m = n −k, . . . , n −1.

The conditions above ensure zero derivatives in a subspace of directions, and the conditions on the Hessian ensure the function is concave (for ridges) and convex (for valleys) in the appropriate subspace. Differentiability in the deﬁnition is not needed, and there are more generic conditions for continuous functions, e.g., that the function value is higher at the ridge point than other points in a subneighborhood corresponding to a subspace of directions.

Morse Complex

Our algorithms for extracting the previous structures do not directly use the differential deﬁnitions above, as they are not robust to noise in the image. We will design our algorithms based on topological constructions in Morse theory [39]. We introduce basic notions from that literature, and the exact relation to ridges and valleys will be left to subsequent sections when we specify our algorithms. We deﬁfine the ascending and descending manifolds of a critical point as all points on a path along the negative (positive, respectively) gradient direction that leads to the given critical point. A path on a manifold M is a mapping γ : [0, ∞) →M. A gradient path is speciﬁed by the differential equation γ′(t) = ±∇h(γ(t)), where h is some function deﬁned on M. Formally, the ascending and descending manifolds of a critical point p of h are deﬁned as follows [32].

Deﬁnition 2 (Ascending and Descending Manifolds). Let h : M →R be a function and p be a critical point of h. The ascending manifold at p is

A(p) = {x ∈M : there exists γ : [0, ∞) →M such that

γ(0) = x, γ(∞) = p, γ′(t) = −∇h(γ(t))}. (1)

The descending manifold at p is

D(p) = {x ∈M : there exists γ : [0, ∞) →M such that

γ(0) = x, γ(∞) = p, γ′(t) = ∇h(γ(t))}. (2)

For instance, consider the function h : R2 →R deﬁned by h(x, y) = x2 + y2. Its ascending manifold at the critical point 0 is A(0) = R2 as all negative gradient paths lead to the origin. Note also that D(0) = 0. See Figure 2 for a visualization in the one-dimensional case.

cubical complex not cubical complex free 1D faces free 2D faces

**Fig. 3:** [Left two images]: Illustration of faces that form a cubical complex (left) and faces that do not form a cubical complex (0,1,2-faces are marked in red, green and orange). The missing 1-face and 0-faces circled in blue on the right are not in the complex, but they are sub-faces of other faces in the set. [Right two images]: Example of 1-face, 0-face free pairs, and 2-face, 1-face free pairs (circled in blue).

The ascending manifolds of local minima decompose the manifold M into disjoint sets. Similarly, the descending manifolds of all local maxima decomposes the manifold M into disjoint open sets. The latter decomposition forms the Morse complex of h, and the former is the Morse complex of −h. We will use the Morse complex in future sections.

Cubical Complexes Theory

We now introduce notions from cubical complex theory, which is the basis for our algorithms in future sections. This theory deﬁnes topological notions (and computational methods) for discrete data that are analogous to topological notions in the continuum. The notion of free pairs, i.e., those parts of the data that can be removed without changing topology of the data, is pertinent to our algorithms. Since the algorithms we deﬁfine require the extraction of lower dimensional structures (ridge curves from surfaces, and valley surfaces from volumes), it is important that the algorithms are guaranteed to produce lower dimensional structures with correct topology. The theory of cubical complexes (e.g., [27], [28]) guarantees such lower dimensional structures are generated with homotopy equivalence to the original data.

Our data (either a curve, surface or volume) will be represented discretely by a cubical complex. A cubical complex consists of basic elements, called faces, of d-dimensions, e.g., points (0-faces), edges (1-faces), squares (2-faces) and cubes (3-faces). Formally, a d-face is the cartesian product of d intervals of the form (a, a + 1) where a is an integer. We can now deﬁfine a cubical complex (see Fig. 3) as follows.

Deﬁnition 3. A d-dimensional cubical complex is a ﬁfinite set of faces of d-dimensions and lower such that every sub-face of a face in the set is contained in the set.

Our algorithms consist of simplifying cubical complexes by an operation that is analogous to the continuous topological operation called a deformation retraction, i.e., the operation of continuously shrinking a topological space to a subset. For example, a punctured disk can be continuously shrunk to its boundary circle. Therefore, the boundary circle is a deformation retraction of the punctured disk, and the two are said to be homotopy equivalent. We are interested in an analogous discrete operation, whereby faces of the cubical complex can be removed while preserving homotopy equivalence. Free faces (see Fig. 3), deﬁned in cubical complex theory, can be removed simplifying the cubical

complex, while preserving a discrete notion of homotopy equivalence. These are deﬁned formally as:

Deﬁnition 4. Let X be a cubical complex, and let f, g ⊂X.

g is a proper face of f if g̸ = f and g is a sub-face of f. g is free for X, and the pair (g, f) is a free pair for X if f is the only face of X such that g is a proper face of f. If g is not free, it is called isthmus.

The deﬁnition provides a constant-time operation to check whether a face is free. For example, if a cubical complex X is a subset of the 3-dim complex formed from a 3D image grid, a 2-face is known to be free by only checking whether only one 3-face containing the 2-face is contained in X.

In the next section, we construct cubical complexes for the evolving front produced from the Fast Marching algorithm, and retract this front by removing free faces to obtain a lower dimensional ridge curve that lies on the surface that we wish to obtain. We also retract a volume to obtain a valley, which forms the surface of interest.

SURFACE BOUNDARY EXTRACTION

In this section, we present our algorithm for extracting the boundary curve of a free-boundary surface from a possibly noisy local likelihood map of the surface deﬁned in a 3D image. The algorithm consists of retracting the fronts (closed surfaces) generated by the Fast Marching algorithm to obtain ridge curves on the surface of interest. We therefore review Fast Marching in the ﬁfirst sub-section before deﬁning our novel algorithms for surface extraction.

Fronts Localized to the Surface With Fast Marching

We use the Fast Marching Method [2] to generate a collection of fronts that grow from a seed point and are localized to the surface of interest. We denote by φ : Ω⊂R3 →R+, a possibly noisy function deﬁned on each pixel of the given image grid. It has the property that (in the noiseless situation) a small value of φ(x) indicates a high likelihood of the pixel x belonging to the surface of interest.

Fast Marching solves, with complexity O(N log N) where N is the number of pixels, a discrete approximation to U : Ω⊂R3 →R+, the solution of the eikonal equation:

|∇U(x)| = φ(x) x ∈Ω\{p} U(p) = 0 (3)

where ∇denotes the spatial gradient (partials in all coordinate directions), and p ∈Ωdenotes an initial seed point. For our situation, p will be required to lie somewhere on the surface of interest. The function U at a pixel x is the weighted minimum path length along any path from x to p, with weight deﬁned by φ. U is called the weighted distance. Minimal paths can be recovered from U by following the gradient descent of U from any x to p. A front (a closed surface, which we hereafter refer to as a front to avoid confusion with the free-boundary surface) evolving from the seed point at each time instant is equidistant (in terms of U) to the seed point and is iteratively approximated by Fast Marching. As noted by [1], a positive constant added to the right hand side of (3) may be used to induce smoothness

of paths. The front, evolving in time, moves in the outward normal direction with a speed proportional to 1/φ(x). Fronts can be alternatively obtained by thresholding U at the end of Fast Marching. The solution of (3) is continuous, and can be approximated as smooth since the solution is a viscosity solution [40], and so a limit of smooth functions.

Contours on the Surface from Front Ridges

If we choose the seed point p to be on the free-boundary surface of interest, the front generated by Fast Marching will travel the fastest when φ is small (i.e., along the surface) and travel slower away from the surface, and thus the front is elongated along the surface at each time instant (see Figure 4). Our algorithm is based on the following observation: points along the front at a time instant that have traveled the furthest (with respect to Euclidean path length), i.e., traveled the longest time, compared to nearby points, lie on the surface of interest. This is because points traveling along locations where φ is low (on surface) travel the fastest, tracing out paths that have large arc-length.

This property can be more easily seen in the 2D case (see Figure 4): suppose that we wish to extract a curve rather than a surface from a seed point, using Fast Marching to propagate a front. At each time, the points on the front that travel the furthest with respect to Euclidean path length lie on the 2D curve of interest. This has been noted in 2D by [4]. In 3D (see Figure 4), we note this generalizes to ridge points of Euclidean minimal path length UE (deﬁned next) are on the surface of interest. The Euclidean minimal path length UE is deﬁned as follows. Deﬁfine a front F = ∂{x ∈Ω: U(x) ≤ D} where ∂denotes the boundary operator. The function UE : F →R+ is such that UE(x) is the Euclidean path length of the minimal weighted path (w.r.t to the distance U) from x to p.

Computationally, UE is easy to obtain by keeping track of another function UE : Ω→R+ in Fast Marching for U. One follows the ordered traversal of points according to Fast Marching in solving for U, and simultaneously updates the value of UE based on a discretization of (3) with φ chosen equal to 1. This gives the Euclidean length of minimal paths determined from U.

The fact that ridge points lie on the surface is visualized in the right of Figure 4. Points on the intersection of the surface and the front are such that in the direction orthogonal to the surface, the minimal paths have Euclidean lengths that decrease. This is because φ becomes large in this direction, thus minimal paths travel slower in this region, so they have lower Euclidean path length. Along the surface, at the points of intersection of the surface and front, the path length may increase or decrease, depending on the uniformity of φ on the surface. This implies points on the intersection of the front and surface are ridge points of UE|F.

We now give an analytic argument that common points to the surface and the front are ridge points.

Proposition 1. Suppose S ⊂Ωis a smooth surface and p ∈S. Consider the front F = {U = D} and suppose x ∈S ∩F then x is a ridge point of UE : F →R, where UE(y) is deﬁned as the Euclidean length of the minimal path from y to p. We assume that locally φ is larger on S than points not on S.

**Fig. 4:** [Top left]: The evolving Fast Marching (FM) front at two different time instances in orange and white. The function 1/φ evaluated at x is the likelihood of surface passing through x, and is visualized (red - high values, and blue - low values). The fronts are localized near the surface of interest. Ridge points of UE, the Euclidean path length of minimal weighted paths, lie on the surface of interest. [Top right]: This is more easily seen in 2D where the local maxima of the Euclidean path length (red balls) of minimal paths (dashed) are seen to lie on the curve of interest. The green contour is a snapshot of the front. [Bottom]: Schematic in 3D with front (blue), surface (green), and several minimal paths (orange). Orthogonal to the surface where the surface intersects the front, the Euclidean path length decreases. Along the surface, the path lengths may increase or decrease. This indicates ridge points.

**Fig. 5:** Schematic of quantities in the proof of Proposition 1.

Proof. Let x ∈S ∩F and let N be a normal vector to S at x. We choose a neighborhood Vx ⊂Ωaround x so that S is approximately ﬂat and φ is approximated as

φ(x) =

x /∈S ∩Vx x ∈S ∩Vx

,

where K1 > K2 > 0, which are constants. Let us consider a point y = x + εN, where ε > 0 is small, and the minimal path from y to p (see Figure 5). We note that minimal paths within Vx\S will be straight lines as φ is uniform in that region. For ε > 0 small enough, we can ﬁfind q ∈S on the minimal path from x to p so that the minimal path from y to p is the straight line path from y to q appended to the minimal path from q to p. We note that if we let ℓ= |x −q| then

U(x) = U(q) + K2ℓ.

Also,

U(y) = U(q) + K1

ℓ2 + ε2,

and any point z on the line between y and q will have

U(z) = U(q) + tK1

ℓ2 + ε2

where t ∈(0, 1). If we search for the point z on the line between q and y on the front F, which has U(z) = U(x), we ﬁfind that

t = K2

ℓ √

ℓ2 + ε2 < 1.

Therefore, the Euclidean length of the minimal path from z to p is

UE(z) = K2

ℓ+ len(γq,p)

where len(γq,p) is the length of the minimal path from q to p. Notice this has less length than the path from x to p, which is UE(x) = ℓ+ len(γq,p). Therefore, UE(z) < UE(x). So moving in the direction N along F reduces the Euclidean length of minimal paths. This same argument holds for any z within Vx along the direction −N from x. This implies that x ∈F ∩S is a one-dimensional ridge point of UE.

This tells us that points of the front that are on the surface must be ridge points, and so we restrict our attention to ridge points on the front as possible points on the surface.

Ridge Curve Extraction Using the Morse Complex

Since computing ridges directly from Deﬁnition 1, using differential operators, is sensitive to noise, scale spaces [41], [42] are often used. However, that approach, while being more robust to noise, may distort the data, and it is often difﬁcult to obtain a connected curve as the ridge. Therefore, we derive a robust method by making use of the Morse complex and cubical complex theory to extract the ridge of interest from the data UE. Cubical complex theory guarantees the correct topology of the desired ridge (as a 1-dimensional closed curve). Relation Between Ridges and Morse Complex: In the following proposition, we note that certain ridges of a smooth function can be computed by computing ascending manifolds. We assume that M is a 2-manifold.

Proposition 2. Boundaries of ascending manifolds of h are ridges of h.

Proof. Suppose that x ∈∂A(p1) then for any neighborhood Vx sufﬁciently small around x, we have that ∂A(p1) ∩Vx divides Vx, i.e., Vx = [Vx ∩A(p1)] ∪[Vx ∩A(p2)] (p1̸ = p2) for the case when Vx intersects two ascending manifolds. Note that −∇h(y) · N2 > 0 for y ∈Vx ∩A(p2) where N2 is the inward normal to ∂A(p2) when Vx is small enough. If this were not the case, then paths following the negative gradient would intersect the boundary ∂A(p2), which is not the case since they ﬂflow into p2. By a similar argument, −∇h(y) · N2 < 0 for y ∈Vx ∩A(p1). Since the function h is assumed smooth and thus the gradient is continuous, we must have that ∇h(x) · N2 = 0. Further, the function is decreasing away from x along the directions ±N2 as points in Vx\{x} belong to ascending manifolds. Therefore, the point x is a local maximum in the direction N2. Ridges satisfy this property. Hence, boundaries of the ascending manifolds are ridges.

Algorithm for Ridges via Morse Complex: Next, we specify a discrete algorithm to determine the Morse complex of −UE|F. The boundaries of ascending manifolds can then be used to extract the relevant ridge. We retract the front to the ridge curve by an ordered removal of free faces based on lowest to highest ordering based on UE|F.

Given a front F, obtained by thresholding the distance U, the two-dimensional cubical complex CF of the front is constructed as follows. Let Zn = {0, 1, . . . , n −1} be a sampling of a coordinate direction of the image. Then

CF contains all 2-faces f in Z3

n between any 3-faces g1, g2 with the property that one of g1, g2 has all its 0-sub-faces with U < D and one does not.

Each face f of CF has cost equal to the average of UE over 0-sub-faces of f.

Our algorithm for Morse complex extraction and boundaries of the ascending manifolds is given in Algorithm 1. The algorithm creates holes at local minima of the function UE|F deﬁned on 1-faces by removing the adjacent 2-faces. It then removes free faces in increasing order of UE|F so as to preserve homotopy equivalence. The removed points associated with a local minimum form the ascending manifold for the local minimum. The faces that cannot be removed without breaking homotopy equivalence, i.e., the isthmus faces, form the boundaries of the ascending manifolds. The algorithm removes all 2-faces and preserves only isthmus 1-faces, and hence the remaining structure of CF is one dimensional. Further, since the algorithm preserves homotopy equivalence, the remaining structure at the end of the algorithm is connected. This is a clear advantage over computation of ridges from differential operators, which does not guarantee connectedness. A heap is used to keep track of the faces in order. The computational complexity of this extraction is therefore O(N log N) where N is the number of pixels, an over-estimate since the faces in the complex are signiﬁcantly lower than the number of pixels.

Ideally, in the case of clean data φ, the function UE deﬁned on the front would have a rather simple topology, indeed a volcano structure (see left image in Fig. 6), where the ridge separates the inside of the volcano from the outside. The two minimum of UE on each side of the ridge would correspond to points away from the surface in the direction of the surface normal. In this case, the previous algorithm would produce the inside of the volcano, and the outside as two components of the complex, and the boundary between them as the ridge, as desired. However, due to noise other ridge structures besides the main ridge of interest can be extracted.

Fortunately, we can simplify the extracted collection of ridges from the previous algorithm by applying the algorithm iteratively. We construct a new complex with a 2face for each ascending manifold computed, and a 1-face connecting 2-faces if two corresponding ascending manifolds have intersecting boundaries. Each 1-face in this new complex is assigned a value to be the average of 1-faces in the common boundary between ascending manifolds. The Morse complex of this simpliﬁed complex is then computed, and the process is repeated until only one loop remains. The algorithm is given in Algorithm 2. Figure 7 shows an example run through this algorithm.

Algorithm 1 Morse Complex Extraction

1: procedure MORSE COMPLEX(CF , UE) 2: ▷CF = cubical 2-complex, UE = cost on 1-faces in CF 3: id ←0 4: Create heap of 1-faces ordered by UE (min at top) 5: repeat 6: Remove 1-face g from heap 7: if g is a subset of two faces f1 and f2 in CF then 8: Remove g, f1, f2 from CF 9: l(f1) ←l(f2) ←id, id ←id + 1 10: ▷new id for ascending manifold; hole at local min 11: else if (g, f) is a free pair in CF then 12: Remove g, f from CF 13: l(f) ←l(fadj) where fadj ⊃g and fadj /∈CF 14: ▷labels face same as adjacent face containing g 15: else if (f, g) is a free pair in CF then 16: Remove g, f from CF 17: else if g is isthmus then 18: l(g) = {l(f1), l(f2)} where f1, f2 ⊃g 19: ▷label is unordered list 20: end if 21: until heap is empty 22: return CF , l ▷Ridges, labels for 2-faces, ridges 23: end procedure

Algorithm 2 Highest Ridge Curve Extraction

1: procedure HIGHESTRIDGE(CF , UE) 2: ▷CF cubical 2-complex of Fast Marching front 3: ▷Euclidean trajectory length UE deﬁned on 1-faces 4: repeat 5: ( C′

F , l ) = MORSE COMPLEX ( CF , UE ) 6: Create 2-cubical complex C′′

F with 7: a 2-face f for each unique 2-face id in l 8: a 1-face g for each unique 1-face id in l 9: g joins f1 and f2 if l(g) = {l(f1), l(f2)} 10: for g each 1-face in C′′

F do 11: R = {g′ ∈C′

F : l(g′) = l(g)} ▷a ridge 12: U ′

E(g) ←average of UE along R 13: end for 14: CF ←C′′

F , UE ←U ′

E 15: until no degree three 1-faces in C′

16: return C′

17: end procedure

**Fig. 6:** [1st image]: Front color coded with Euclidean path length UE (top view). Red indicates high values. The bottom view (not shown) is a symmetric ﬂflip. Topologically, UE forms a volcano structure (ridge, i.e., top of volcano, is darkest red), and inside the volcano is blue. [Subsequent images]: Illustration of iterations (from left to right) of Algorithm 1 on noise-less data to obtain the ridge curve (white) on the Fast Marching front (green) by computing the Morse complex of UE. The ridge curve lies on the surface of interest (red).

**Fig. 7:** Illustration of Algorithm 2 operating on noisy data to obtain the highest ridge.

**Fig. 8:** [Left]: Ridge curve (white) extraction by retracting the Fast Marching front at two instants. [Right]: An example cut (red) of ridge curves, forming the surface boundary. Notice that the cut matches with the end of high 1/φ (bright areas).

An example of ridge curves detected for multiple fronts is shown in Figure 8. This procedure of retracting the Fast Marching front to form the main ridge is continued for different fronts of the form {U < D} with increasing D. This forms many curves on the surface of interest. In practice, in our experiments, D is chosen in increments of ∆D = 20, until the stopping condition is achieved, and this typically results in 10 −20 ridge curves extracted. The next subsection describes the stopping criteria.

Stopping Criteria and Surface Boundary Extraction

To determine when to stop the process of extracting ridge curves, and thus obtain the outer boundary of the surface of interest, we make the following observation. Parts of the curves generated from the previous section move slowly, i.e., become close together with respect to Euclidean distance at the boundary of the surface. This is because the speed function 1/φ becomes small outside the surface. Hence, for the curves ci generated, we aim to detect the locations where the distance between points on adjacent curves becomes small. To formulate an algorithm robust to noise, we formulate this as a graph cut problem [16].

We deﬁfine the graph G as follows:

vertices V are 0-faces in all the 1-complexes ci formed from ridge extraction

edges E are (v1, v2) where v1, v2 ∈V are such that v1, v2 are connected by a 1-face in some ci or v1 is a 0face in ci and v2 is the closest (in terms of Euclidean distance) 0-face in ci+1 to v1 a cost |vj −vk| is assigned to each edge (vj, vk) where vj and vk belong to different ci (so that the min cut will be where adjacent curves are close)

for edges (vj, vk) such that vj and vk belong to the same ci, the cost is the minimum Euclidean distance between segment (vj, vk) and segments on ci+1 the source is the seed point p, and the sink is the last ridge curve cl We wish to obtain a cut of G (separating G into two disjoint sets) with minimum total cost deﬁned as the sum of

all costs along the cut. In this way, we obtain a cut of the ridge curves along locations where the distance between adjacent ridge curves is small. The process of obtaining ridge curves from the Fast Marching front is stopped when the cost divided by the cut size is less than a pre-speciﬁed threshold. This cut then forms the outer boundary of the surface. The computational cost of the cut (compared to other parts of the algorithm) is negligible as the graph size is typically less than 0.5% of the image. Figure 8 shows an example of a cut that is obtained. Figure 11 shows a synthetic example.

We now present our algorithm for surface extraction. Given the surface boundary curve determined from the previous section, we provide an algorithm that determines a surface going through locations of small φ and whose boundary is the given curve. Our algorithm uses the cubical complex framework and has complexity O(N log N).

Valley Extraction Algorithm and Rationale

We show now that the surface of interest lies in a valley of U : Ω→R+, the weighted minimal path length.

Proposition 3. Suppose S ⊂R3 is a smooth surface and p ∈S. Let φ : Ω⊂R3 →R+ be a function with low values on S and higher values outside (locally). Then S is a valley of U, where U is the solution of the eikonal equation with U(p) = 0.

Proof. We show that for x ∈S, U decreases away from x in the direction ±N, the normals to the surface at x. For a small enough neighborhood Vx around x, we may assume that S is ﬂat and that φ is approximated by

φ(x) =

x /∈S ∩Vx x ∈S ∩Vx

,

where K1 >> K2 > 0. We also assume (for now) that x close enough to p so that p lies in Vx. In this case, we see that

U(x) ≈U(p) + K2|x −p| = LK2,

as the minimal path from p to x is approximately a straight line path on the surface, as the surface is nearly ﬂat in Vx. Let y = x±εN for ε > 0 sufﬁciently small. We now consider the minimal path from y to p. Note outside the surface, the path must be nearly a straight line as φ is constant. Similarly, on the surface the minimal path must be a straight line. We see that the minimal path is a straight line between y and some point z on the line joining x to p and then the straight line between z and p (see Figure 9). Therefore,

U(y) = min

ℓ K2(L −ℓ) + K1

ℓ2 + ε2

where ℓis the length of the segment between x and z. The minimizer is ℓ= ε/

√

1 −r2, where r = K2/K1 < 1. This yields that

U(y) = LK2 − ε √

1 −r2 K2 + ε

√

2 −r2 √

1 −r2 K1

= LK2 + ε √

1 −r2 [K1

2 −r2 −K2] > LK2,

**Fig. 9:** Quantities deﬁned in the proof of Proposition 3.

where the last inequality follows from the fact that √

2 −r2 > 1 and K1 > K2. Therefore, U(y) > U(x) and so we see a local minimum in the direction N, which implies x lies in a 2-d valley of U. We may now apply the same argument using x to play the role of p, and show that all points in a neighborhood of x on the surface are on a valley. We may continue in this way to show all points on the surface are on the valley.

Algorithm: We can use the above fact to design an algorithm for extracting the surface. We may perform a deformation retraction of V0 = {U ≤T(0)} where T(0) is chosen to enclose the entire surface, and T(t) is a decreasing function of t. At each time, the points of the level set Lt = {U = T(t)} that retain the homotopy equivalence to Vt are removed from Vt. We further impose that the boundary of the surface must not be removed from Vt. This way, all points that are on the surface are retained. One can show this with an inductive argument. Assume for a given time t, the union of all retained sets is a 2-dim set St−(t−is just before t) that is on the surface, and so Vt−= St−∪{U ≤T(t)}. Note that the latter set in the union is a volume. A point x ∈∂St−with U(x) = T(t) cannot be removed. Since x is on the surface, which by the proposition is a valley point, the normal to the surface at x is tangent to Lt, and U is strictly increasing along the normal. Therefore, removing point x disconnects Vt−, not preserving homotopy equivalence. Therefore, Vt = St ∪{U < T(t)} where St contains all points on ∂St−.

This procedure can be accomplished with an analogous algorithm in the discrete case. We retract the cubical complex of the image with the constraint that the boundary curve 1-faces cannot be removed. We accomplish this retraction by an ordered removal of free faces based on weighted path length U. The algorithm is described in Algorithm 3. Figure 10 shows the evolution from Algorithm 3 to extract the surface from the data used in Figure 8. Figure 11 shows a synthetic example of the evolution of this algorithm.

Valley: Surface of Minimal Paths

We now relate the valley that is extracted by our algorithm to minimal paths. We show that the valley, and thus the surface extracted, is a surface formed from a collection of minimal paths to p. First, we show that the gradient path starting from a point in the valley stays in the valley.

Proposition 4. Suppose x ∈M is a valley point of h : M →R, then the path γ determined by the gradient descent of h with initial condition x lies on the valley of h containing x.

Algorithm 3 Surface Extraction from Boundary of Surface

1: procedure VALLEYEXTRACT(CI, U, ∂S) 2: ▷CI = cubical 3-complex of image, U = FM distance 3: ▷∂S = boundary of surface (1-complex) 4: Create heap of 2-faces ordered by U (max at top) 5: repeat 6: Remove 2-face g from heap 7: if (g, f) is a free pair in CI for some f then 8: Remove f and g from CI 9: else if (f, g) is a free pair in CI for some f and g ∩∂S = ∅then 10: Remove f and g from CI 11: end if 12: until heap is empty 13: return CI ▷2-cubical complex of Valley 14: end procedure

**Fig. 10:** Illustration of valley extraction by Algorithm 3, which retracts the volume while preserving 1-faces on the surface boundary (red). This gives the surface of interest.

Proof. For simplicity, we assume M = R3 and that the valley is two-dimensional. By deﬁnition of a 2D valley in R3, we have that ∇h(x) · Nx = 0 and N T

x Hh(x) · Nx > 0 for some unit direction Nx ∈R3 where Hh denotes the Hessian. For every neighborhood Vx of x sufﬁciently small, there exists y ∈Vx such that ∇h(y) · Ny = 0 and N T

y Hh(y) · Ny > 0 for some Ny. If that were not the case, then x would be a isolated critical point, which is not the case. By smoothness of h, N is a smooth function. Let S be the points the satisfy the conditions on the gradient and Hessian in Vx.

We consider the path γ deﬁned by the gradient descent of h starting from x. Then by deﬁnition of γ and Taylor expansion of h,

∇h[γ(∆t)] ≈∇h[x−∆t∇h(x)] ≈∇h(x)−∆tHh(x)·∇h(x).

Taking the dot product of the above with Nγ(∆t) ≈Nx, by a Taylor expansion, we have

∇h[γ(∆t)] · Nγ(∆t) ≈−∆tN T

x Hh(x) · ∇h(x).

Note that N T

x Hh(x) = λN T

x with λ > 0 since Nx is an eigenvector of Hh(x) by deﬁnition of valley. Since N T

x ∇h(x) = 0 by the deﬁnition of valley, we have that ∇h[γ(∆t)]·Nγ(∆t) ≈0. Also, N T

γ(∆t)Hh[γ(∆t)]·Nγ(∆t) > 0 as γ(∆t) ∈Vx. Therefore, γ(∆t) is also in the valley, and thus continuing this way, we can show that the path γ formed from the gradient descent is also in the valley.

Using the last property, we can show the surface extracted by our algorithm is a collection of minimal paths to p.

Ridges Final Cut Surface

Removal of Faces in Image (Algorithm 3) to Extract Surface →

**Fig. 11:** Synthetic example of extracting a sphere with top cut such that the boundary is four arcs. The image (not shown) is a noisy image of the cut sphere with holes. Ridge curves are extracted via Algorithm 1 (top left). The ﬁfinal cut of ridge curves (top, middle left), the ﬁfinal surface extracted via Algorithm 2 (top, middle right), and the ground truth (top, right) are shown. Snapshots in the removal of faces in Alg. 2 are shown (bottom), resulting in the surface (right).

Proposition 5. Suppose V is a valley of U, the solution of the eikonal equation, containing the seed point p used to deﬁfine U. Then V is a union of minimal paths to p.

Proof. Let x ∈V then the path γx formed from the gradient descent of U starting from x stays in V by Proposition 4. The path γx is also a minimal path since gradient paths of U are minimal paths. Note that γx ends at p. Therefore, we see that V is the union of γx over all x.

EXPERIMENTS

Supplementary video are available1. We qualitatively and quantitatively assess our method by comparing against competing algorithms.

Datasets and Parameters

We evaluate our method on three datasets of 3D images.

Synthetic Dataset: We construct a synthetic dataset consisting of 20 different surfaces with boundary at three different image resolutions, 100×100×100, 500×500×500 and 800 × 800 × 800. Each of the surfaces have different 3D boundary curves of different shape, and surfaces that have various degrees of coarse and ﬁfine features. Example surfaces are shown in Fig. 12. The images are formed by setting pixels not within distance 1 to the surface to 1 and all other pixels to 0. The surfaces meshes are downsampled for the lower resolution images. Noise with level σ = 0.1 is then added to the images.

Seismic Dataset: Seismic images are formed from measurements of seismic pulses reﬂected back from the earth’s sub-surface. They are 3D images, and are used to measure geological structures. We have a dataset of three volumes with dimensions 463 × 951 × 651. The goal is to extract fault surfaces, which form free-boundary surfaces within the volume. Faults may have signiﬁcant curvature, and the boundaries are non-planar. The images are cluttered and

1. https://sites.google.com/site/surfacecut/pami

**Fig. 12:** Example surfaces in our synthetic dataset. Each surface has a different boundary curve, and the surfaces are of different shape, exhibiting various degrees of randomness.

noisy, and faults can be found by locating discontinuities, which is difﬁcult due to subtle edges. Each image consists of multiple faults. We have obtained ground truth segmentations (human annotated) of two faults within each image for each slice.

Lung CT Dataset: We use a dataset of 10 3D computed tomography (CT) of the lung of cancer patients from the Cancer Imaging Archive (TCIA) [43]. Each image has size 512 × 512 × Z, where Z varies between 300 and 700, depending on the patient. Our goal is to segment lung ﬁssures (e.g., [44], [45]), which are the boundaries between sections of the lung. They are very thin, subtle structures, and form free-boundary surfaces. Each of the lung ﬁssures in each image is human annotated, for every slice.

Parameters: Our algorithm, given the local surface likelihood φ, requires only one parameter, the threshold on the cut cost. In all experiments, we choose this to be T = 5. This is not sensitive to the data (see Supplementary).

Evaluation Methodology

We validate our results with quantiﬁcation measures for both the accuracy of the surface boundary and the surface using quantities analogous to the precision, recall and Fmeasure. We represent the surface and its boundary as voxels. Let Sr denote the surface returned by an algorithm and let Sgt be the ground truth surface. Denote by ∂Sr and ∂Sgt the respective boundaries. We deﬁfine

N(r →gt) = |{v ∈Sr : dSgt(v) < ε}| N(gt →r) = |{v ∈Sgt : dSr(v) < ε}|

PS = N(r →gt)/|Sr|, RS = N(gt →r)/|Sgt|,

FS = 2PSRS/(PS + RS)

GT Cov. = (N(r →gt) + N(gt →r))/(|Sr| + |Sgt|)

where dS(v) denotes the distance between v and the closet point to S using Euclidean distance, |·| denotes the number of elements of the set, and ε > 0. The precision measures how close the returned surface matches to the ground truth surface. The recall deﬁned above measures how close the ground truth matches to the surface. The F-measure provides a single quantity summarizing both precision and recall. GT-Cov. is another metric summarizing both the precision and recall. All quantities are between 0 and 1 (higher is more accurate). The precision and recall are similar to accuracy and completness for closed surfaces in evaluating

**TABLE 1:** Comparison of methods for surface extraction given the surface boundary on the synthetic dataset. Speed (in seconds), surface precision (P), recall (R), F-measure (F), and ground truth covering (GT-cov) are reported. Higher P, R, F, GT-Cov. indicate better ﬁdelity to the ground truth.

100 × 100 × 100 pixel images

Method Time GT-Cov. R LP 0.93±0.01 0.94±0.01 0.91±0.02 0.96±0.01 MCNF 0.92±0.01 0.90±0.01 0.93±0.01 0.92±0.02 0.95±0.02 0.95±0.02 0.96±0.02 0.94±0.03

500 × 500 × 500 pixel images

Method Time GT-Cov. R LP >24hr NA NA NA NA MCNF 0.94±0.01 0.92±0.01 0.94±0.01 0.93±0.01 0.96±0.01 0.96±0.01 0.97±0.01 0.94±0.01

800 × 800 × 800 pixel images

Method Time GT-Cov. R LP >24hr NA NA NA NA MCNF >24hr NA NA NA NA 0.96±0.01 0.97±0.01 0.98±0.01 0.95±0.02

stereo reconstruction algorithms [46]. We similarly deﬁfine precision P∂S, recall R∂S and F-measure for ∂Sr and ∂Sgt using the same formulas but with the surfaces replaced with their boundaries. We set ε = 3 to account for inaccuracies in the human annotation.

Evaluation

Synthetic Data: Surface Extraction Given Boundary We ﬁfirst evaluate three methods for surface extraction given a 3D-boundary curve of the surface, discrete-minimal surface computed with linear programming (LP) [8], discreteminimal surface approximated with Minimum-Cost Network Flow (MCNF) [8], [21], [23], [24], and our surface extraction, described in Section 4. We use Gurobi’s state-ofthe-art linear programming implementation, to implement LP. We use the Lemon library [47] to implement MCNF. There are no other methods that solve this problem. We choose φ to be the image. All methods are provided the ground truth 3D boundary curves. We evaluate the methods in terms of computational time, and in terms of surface accuracy. A summary of results are provided in Table 1. Average of results over all the images are provided. Our method is computationally faster than all other methods at all resolutions. LP is unable to perform in a reasonable time frame for images sizes above 1003, and MCNF is unable to perform for image sizes above 5003. At all resolutions, our method is faster. Speeds are reported on a single Pentium 2.3 GHz processor. The accuracy of our method is also the highest on all measures, but all have similar accuracies. The advantage of our method is clearly speed, and ability to deal with high resolution images. Note that the analysis was not extended to the real datasets as they have high resolution, making it too computationally expensive to test, and downsampling the images destroys the structures to be extracted.

Seismic Data: Surface and Boundary Extraction We now compare against the competing method for free boundary surface extraction. To the best of our knowledge,

**Fig. 13:** Quantitative Analysis of Smoothing Parameter Boundary (left) and surface (right) F-measure versus smoothing degradations for our method and [25].

Crease Surface (for increasing smoothing parameter →)

**Fig. 14:** Qualitative Analysis of Smoothing Parameter. Results displayed by varying the parameter in φ (larger towards the right). Surfaces extracted by Crease surfaces and our method are displayed with the ground truth.

there is no other general algorithm that extracts both the boundary of the free-surface and the surface given a seed point. Therefore, we compare our method in an interactive setting and automated setting (with seed points automatically initialized) to Crease Surfaces [25]. It computes the smoothed Hessian of φ, and computes a modiﬁed matrix based on the relative difference in the ﬁfirst and second highest eigenvalues. It then forms the surface by determining locations where the eigenvector aligns with the gradient, and constructs connected surfaces. In an interactive setting, we choose the surface returned by [25] that is near to the user provided seed point (and best ﬁts ground truth) to provide comparison to our method. In an automated setting, we use a seed point extraction algorithm (described later) to initialize our surface extraction.

We choose φ(x) to be the semblance measure in [9]; this along with [25] is state-of-the-art for seismic data.

Robustness to Smoothing Degradations: The semblance φ contains a smoothing parameter, which must be tuned to achieve a desirable segmentation. Therefore, it is important that the surface extraction algorithm be robust to changes in the parameter of the likelihood. Thus, we evaluate our algorithm as we vary the smoothing parameter. The smoothing parameter is varied from σ = 0, 2, 3, . . . , 14. We initialize our algorithm with a user speciﬁed seed point. Quantitative results are shown in Figure 13, where we plot the F-measure versus the smoothing amount both in terms of surface and boundary measures. Some visual results of the surfaces are shown in Fig. 14. Notice our method degrades only gradually and maintains consistently high accuracy in both measures in contrast to [25].

Robustness to Noise: In applications, the image may be distorted by noise (this is the case in seismic images where

**Fig. 15:** Quantitative Analysis of Noise Degradations Boundary (left) and surface (right) F-measure versus the noise degradation plots for our method and [25].

Crease Surface (for increasing noise →)

**Fig. 16:** Qualitative Analysis of Noise Degradations. Results displayed by varying the additive noise to φ (larger towards the right). Surfaces extracted by Crease surfaces and our method are displayed with the ground truth.

the SNR may be low), and thus we evaluate our algorithm as we add noise to the image, and we ﬁx the smoothing parameter of the semblance φ(x) to the one with highest F-measure in the previous experiment. We choose noise levels as follows: σ2 = 0, 0.05, . . . , 0.5. Quantitative results are shown in Figure 15, and some visualizations of the surfaces are shown in Fig. 16. Results show that our method consistently returns an accurate result in both measures, and degrades only slightly.

Slice-wise Validation: We now show some visual validation of our method by showing that the surface intersects with slices of the image in locations where there is a fault, and thus the value of φ is low. This is shown in Figure 17.

Robustness to Seed-Point Location: We demonstrate that our surface extraction method is robust to the choice of the seed point location. To this end, we randomly sample 30 points (with high local likelihood) from the ground truth surface. We use each of the points as seed points to initialize our algorithm. We measure the boundary and surface accuracy for each of the extracted surfaces. Results are displayed in Figure 18. They show our algorithms consistently returns a boundary and surface of similar accuracy regardless of the seed point location.

Analysis of Automated Algorithm: Even though our contribution is in the surface and boundary extraction from a seed point, we show with a seed point initialization, our method can be automated. We initialize our algorithm with a simple automated detection of seeds points. We extract seed points by ﬁfinding extrema of the Hessian and then running a piece-wise planar segmentation of these points using RANSAC [48] successively; the point on each of the segments located closest to other points on the segment are seed points. This operates under the assumption that the

**Fig. 17:** Slice-wise Validation on Seismic Data: [Left column]: Slices corresponding to x-y, x-z, and y-z planes, [Middle, left]: Local surface likelihood (1/φ), [Middle right]: Intersection of SurfCut result (green) with slice, [Right column]: surface from SurfCut at certain viewpoint.

**Fig. 18:** Robustness to Seed Point Choice: [Left]: A visualization of the seed points chosen. [Right]: Boundary F-measure versus various seed point indices. The same boundary and surface accuracy is maintained no matter the seed point location.

surfaces are roughly planar. If not, there could possibly be redundant seed points on the same surface, which would result in repetitions in surfaces in our ﬁfinal output. This could easily be ﬁfiltered out. We run our boundary curve extraction followed by surface extraction for each of the seed points on the original datasets. We compare to [25]. There are 6 ground truth surfaces in this dataset. Our algorithm correctly extracts 6 surfaces, while [25] extracts 4 surfaces (2 pairs of faults are merged together each as a single connected component). Results on a dataset are visualized in Figure 19 (each connected component in different color). Notice that Crease Surfaces has holes, captures clutter, and connects separate faults.

Computational Cost: We analyze run-times on a dataset of size 463 × 951 × 651. The run-time of our algorithm depends on the size of the surface. To extract one surface, our algorithm takes on average 10 minutes (9 minutes for the boundary extraction and 1 minute for the surface extraction). Automated seed point extraction takes about 3

**Fig. 19:** Example result in an automated setting. [Left]: Result by Crease Surfaces, which contains holes and incorrectly detects clutter (top, red) due to noise in the data. [Right]: Results of SurfCut, which extracts the correct number of surfaces and produces smooth simple surfaces.

minutes. Therefore, the total cost of our algorithm for extracting 6 faults is about 1 hour. We note that after seed point extraction, the computation of surfaces can be parallelized. In comparison, [25] takes about Pentium 2.3 GHz processor. 2 hours on the same dataset. Speeds are reported on a single

Lung CT Data: Surface and Boundary Extraction

We now compare to Crease Surfaces for the Lung CT dataset. We compare the methods under the settings described in the previous section. For medical data, we modify the matrix based on the Hessian in Crease Surfaces to another matrix based on closeness to a plate-like structure as common in lung ﬁssure detection [45], [49], [50]. State-ofthe-art methods in ﬁssure extraction use a method similar to Crease surfaces to extract the surface. We choose φ to be the plate-ness measure in our method. Quantitative results on the entire dataset are summarized in Table 2. Both in terms of surface and boundary accuracy, our method is more accurate with respect to all measures. Visual validation of our method on slice-wise views of the surface and image is shown in Fig. 20. Some visualizations of the surface results are shown in Fig. 21. Various slices are shown to help visualize features of the image. Crease surface generates surfaces with incorrect holes and many times cannot capture the entire ﬁssure, hence low recall and precision on the boundary metrics. SurfCut does not contain any holes and accurately captures very ﬁfine and thin structures near the boundaries of the ﬁssures.

CONCLUSION

We have provided a general method for extracting a smooth simple (without holes) surface with unknown boundary in a 3D image with noisy local measurements of the surface, e.g., edges. Our novel method takes as input a single seed point, and extracts the unknown boundary that may lie in 3D. It then uses this boundary curve to determine the entire surface efﬁciently. We have demonstrated with extensive

**TABLE 2:** Quantitative Evaluation on Lung Dataset. Comparison of methods in terms of surface and boundary accuracy. Precision (P), recall (R), F-measure (F), and ground truth covering (GT-cov) are reported. Higher P, R, F, GT- Cov. indicate better ﬁdelity to the ground truth.

Surface accuracy Method GT-Cov. R Crease Surfaces 0.76±0.08 0.70±0.10 0.67±0.11 0.91±0.06 0.91±0.04 0.87±0.06 0.86±0.06 0.95±0.02

Boundary accuracy Method GT-Cov. R Crease Surfaces 0.70±0.11 0.72±0.08 0.69±0.10 0.71±0.12 0.86±0.04 0.86±0.06 0.85±0.06 0.87±0.05

**Fig. 20:** Slice-wise Validation in Lung CT Dataset. [Top]: Various slices of an image of a patient, [Bottom]: Surface generated with SurfCut intersected with the slice above (green) superimposed on the slice. Notice the structure of interest is a subtle thin lines in the slices (top).

experiments on noisy and corrupted data with possible interruptions that our method accurately determines both the boundary and the surface, and the method is robust to seed point choice. In comparison to an approach which extracts connected components of edges in 3D images, our method is more accurate in both surface and boundary measures. The computational cost of our algorithm is less than competing approaches.

A limitation of our method (as with competing methods) is extracting intersecting surfaces. Our boundary extraction method may extract boundaries of one or both of the surfaces depending on the data. However, if given the correct boundary of one of the surfaces, our surface extraction produces the relevant surface. This limitation of our boundary extraction is the subject of future work. This is important in seismic images, where surfaces can intersect.

ACKNOWLEDGMENTS

This work was supported by KAUST OCRF-2014-CRG3- 62140401, and the Visual Computing Center at KAUST.
