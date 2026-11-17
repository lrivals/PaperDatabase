---
id: 2004-seales-digital-restoration-volumetric-scanning
title: "Digital Restoration Using Volumetric Scanning"
year: 2004
backend: pymupdf
---

Digital Restoration Using Volumetric Scanning

W. Brent Seales seales@uky.edu

Yun Lin ylin@netlab.uky.edu

Laboratory for Advanced Networking

Computer Science Department

University of Kentucky Lexington, Kentucky 40506

## Abstract

In this paper we present a new, nondestructive method for revealing inaccessible text buried within damaged books and scrolls. The method is based on volumetric scanning followed by data modeling and physically-based simulation. We show by experiment that it is possible to recover readable text from objects without physically opening or damaging them. In handling damaged collections, conservators often face a choice between two frustrating alternatives: indeﬁfinite preservation without analysis, or irreversible physical harm for the sake of potential discovery. We believe that this work creates a new opportunity that embraces both the need to preserve and the possibility for complete analysis.

Categories and Subject Descriptors

I.7.0 [Document and Text Processing]: General

General Terms

Algorithms, Experimentation

Keywords

Volumetric scanning, restoration, preservation, digital unwrapping

INTRODUCTION Digitization has become essential as a way to preserve, disseminate, and even restore damaged objects. Preservation alone is a primary motivation for digitization: unexpected accidents and disasters in museums and libraries justify the need for vigilant and redundant preservation eﬀorts. Of course, as technologies rapidly develop, preservation is only the start of what is now possible once a collection has been digitized.

Preservation via digitization when objects are amenable to high quality digitization has become commonplace. Familiar examples include digitization of the pages of a book

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, to republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. JCDL’04, June 7–11, 2004, Tucson, Arizona, USA.

## (préambule)

**Figure 1:** This manuscript, which is part of the Cotton collection at the British Library, was damaged by ﬁre and water.

or a manuscript and creation of image sequences of sculptures as they are rotated in front of a camera. Objects that are damaged or contain portions that are impossible to capture with a camera or a scanner are largely ignored in most preservation eﬀorts, however. In fact, there is a class of objects whose precise contents remain a mystery. Although such artifacts may contain a surprising text or a previously unknown marking or illustration, the combination of damage and fragility stands guard over such secrets.

This work addresses damaged, fragile objects that sit on shelves behind other more accessible things in conservators’ archives. In many cases these objects are wrecks and are diﬃcult if not impossible to digitize. Figure 1 shows a damaged manuscript from the Cotton collection [20, 21]. Most of the manuscripts in this collection that suﬀered the ﬂames (and the water used to extinguish them) were physically dismantled and painstakingly reassembled. The one shown above was set aside as a reminder of the mess they became after being ravaged by the elements. Other examples include once-soggy books with pages now stuck together, book bindings made from layers of cannibalized texts (who knows which text?), carbonized scrolls from lava ﬂflows that could easily be mistaken for chunks of coal. Is there any hope of recovering usable information from such objects?

We believe there is potential for some amazing discoveries from damaged collections based on volumetric digitization

followed by physically-based methods for restoration. These techniques, which we will describe more fully in subsequent sections, follow a progression of work aimed at enhancing readability by manipulating digitized representations.

Digitization and subsequent enhancement work began as strictly an image-based (2D) operation [7, 11, 15, 24]. Such approaches assume ﬂat objects (which is not always a guarantee) and apply digital image processing algorithms to improve image quality. Follow-on methods that use 3D acquisition [4] can apply 3D model-based restoration techniques [23, 13, 8]. The availability of 3D representations has encouraged the development of restoration algorithms for very speciﬁc situations, such as methods for removing distortions due to page curl [13, 8], or ﬁxing the typical concave shape distortion that occurs on pages near a book’s binding [23]. These techniques share the common assumption that the page surface has a regular shape (e.g., cylindrical).

Most recently we have seen methods emerge to tackle digital restoration of manuscripts that have become warped and crinkled in arbitrary ways from age and deterioration [4, 5, 6]. In our previous work, we developed an acquisition system to capture both the texture and 3D geometry of manuscripts with arbitrary shape [4, 5]. Using 3D geometry we developed a restoration method for digital ﬂflattening based on physically-based simulation [6].

This progression has led us to consider impenetrable objects, which present major problems for digitization [22, 17, 16, 18, 19]. We need more powerful approaches to digitize, manipulate and enhance such objects. Most of these objects are fragile and cannot sustain physical manipulation without serious risk of further damage. The condition of the material is brittle, folded, rolled-up, and prohibits a clear view of most of the text. The idea of opening a digital representation instead of the physical piece in order to provide a reading of previously inaccessible text is intriguing, and provides an alternative for conservators who normally must choose between preservation (with no analysis) or physical destruction for the sake of analysis.

In the following sections we present the details of our approach, which can be divided into three key stages: volumetric scanning, segmentation, and restoration via physicallybased simulation. In Section 2, we discuss Computed Tomography (CT), a volumetric digitization approach commonly applied in medical applications. This non-invasive X-ray technology provides a way to digitize the complete volume of a closed object. Following CT digitization, we apply segmentation and surface generation to construct a textured mesh model in preparation for the restoration simulation. In Section 3, we describe the constrained, physically-based simulation process, which is devised to unroll a digital representation of surface just as one might unfurl a blanket or a ﬂag. The physical basis of this algorithm makes it promising as an approach for surface restoration. We conclude with experimental results and a few summary remarks.

3D ACQUISITION A digital version of an object will never replace the original, but can enable subsequent manipulations that prove to be very powerful. Digitization must be viewed as a continuous process where important collections are periodically revisited as technology changes. Emerging high-resolution volumetric digitization technologies enable new kinds of analysis.

Volumetric Digitization Impenetrable and extremely friable objects make digitization diﬃcult or impossible for traditional acquisition approaches like structured light, stereo reconstruction, ﬂatbed scanning, etc. We need to employ an acquisition technique that can nondestructively penetrate objects. Computed Tomography (CT), a widely used technique in medical applications, is one such technology. CT scans use X-rays with an energy ranging from 20 keV up to 120 keV. X-rays with such a high energy can penetrate most substances. Since different elements have diﬀerent scattering cross-sections, and diﬀerent materials have diﬀerent atomic densities, these variances result in variance of X-ray absorption. As X-rays pass through the material of interest, the variation in material properties that each ray encounters on its path is detected and then reﬂected as an attenuation value in the CT data. By taking advantage of this feature, we can use CT scans to distinguish between materials, such as pigment versus paper versus papyrus.

Ink that contains metal is a good example of a substance that will respond well in a CT scan because of the large diﬀerence in radio-density between the metals and vellum or papyrus. Iron-gall ink was very widely used because of its permanence and availability [9, 10]. Unlike carbon inks, which smudge and fade over relatively short periods of time, iron-gall ink does not easily smudge or rub oﬀ. Careful analysis of samples of iron-gall ink from various ancient scrolls reveals the presence of ferric gallic acid complexes or iron pyrogallol complexes [10]. We believe that pigments such as iron-gall will respond very well in CT scans.

While pigment response is one important issue, a second is scan resolution. Computed Tomography resolution is measured in terms of planar resolution and distance between slices. The following factors are important in determining how to capture ﬁne detail during digitization:

• Material thickness and the distance between layers: If the material is thinner than the CT resolution and the layers are attached without enough space between them, it may not be possible to resolve those layers in the volumetric data.

• Stroke size: If the strokes of the text are narrower than the CT resolution or the size of the text is too small, it may not be possible to resolve the details of the text in the volumetric data.

With ﬁfiner resolution, reliable segmentation becomes possible. Current state-of-the-art medical CT scanners support a spatial resolution of 0.5 mm. This resolution can help recover substantial amounts of information. Custom scanners, which we have used on preliminary results, are capable of resolutions to 5 microns, which is more than enough to capture the smallest text [12].

Segmentation and Surface Generation Volumetric digitization establishes a 3D space of intensity samples (voxels) in which to deﬁne a surface mesh. Since the volume is not structured, the goal of the segmentation step of the processing is to deﬁne a surface through the voxel set that matches the surfaces of the substrate material present in the scan. If the surface is positioned correctly (i.e., where the material is) and if the surface is textured with the correct values (i.e., voxels that represent ink response), we can

create a surface that shows ink/paper response. The definition of the 3D structure of the surface and the texture at each point on that surface is the ﬁfirst problem to solve, followed by the unwrapping problem (in Section 3), which is the “straightening out” of the potentially rolled up surface structure so that it can be read as a coherent sheet.

We build the 3D surface to coincide with the layers of material (e.g., papyrus) on which the ink response will lie. We apply a segmentation procedure to generate a surface mesh from the volumetric data consisting of the following steps:

1. Thresholding: We choose suitable threshold values empirically for each speciﬁc case in order to segment a voxel set into two categories: material voxels versus empty space. Since dense material absorbs X-rays, the voxels representing material are brighter than those corresponding to empty space. Because of the basic principles of the Fourier slice theorem and the associated reconstruction algorithms on which CT technology is founded, there may be noise in voxels near sharp edges, e.g., near the surface of the material. In fact, the CT scanner produces a density measure that is essentially a “transparency” value. This makes a surface that cuts through the data seem more like a translucent slice that must be adjusted to tune the image formed on that slice. In order to support more accurate texture evaluation from CT data, we have implemented a multi-layered texture approach that uses a number of voxel layers in the proximity of a desired surface point in order to generate a texture value. In practice we tune the multi-layered textures much like one adjusts a confocal microscope by moving a narrow surface, or “focal plane”, up and down to tune structures coming in an out of focus.

2. Surface mesh and layered texture generation: We deﬁne the surface as a texture-mapped mesh. The mesh separates the space in which it is embedded (the 3D voxel set) into inner and outer regions. The mesh resolution is controllable and may be chosen according to the availability of computer resources and the tradeoﬀbetween eﬃciency and accuracy.

Each texture triangle of each texture layer is generated from the voxels that lie along the 3D normal to the corresponding 3D mesh triangle. Distance along that normal (in either the positive or negative direction) gives a deﬁnition of distinct texture layers. We can tune the number of layers and the distance of each layer from the mesh (considered to be the base surface) along the normal direction to get the best texture results. Along with the distance metric for texture layer deﬁnition, we apply a third control in order to ﬁfilter the voxel set to overcome noise. For example, we have used weighted-mean-ﬁfilters, max/min ﬁfilters, etc. A non-weighted mean ﬁfilter assigns equal importance to voxels in a deﬁned neighborhood and computes the texture by averaging the intensities of all voxels within the neighborhood range.

To summarize, we have implemented three levels of control in generating the textured surface from the mesh that is embedded in the segmented voxel set. We deﬁne the number of layers, the distance between each layer, and the ﬁfilter

(including an algorithm and neighborhood) to apply in calculating a texture element at each point in each layer from the voxel set. This gives a number of options for creating a family of readable, enhanced surface textures from the raw CT voxel set.

PHYSICALLY-BASED SIMULATION Segmentation and texture calculation is data-driven. The properties of the voxels determine the 3D location and structure of the material surface in the data. For the kinds of objects we envision, such as damaged books with pages stuck together and rolled-up papyrus, the surface will likely have a shape that will make it hard to read the text. We address this problem via simulation using a physically-based mass-spring system [1, 2, 3]. The goal is to take the surface shape and its texture as it emerges from the data and “ﬂflatten” or “unroll” it onto a ﬂat page. This requires some user involvement and thus is a top-down process aided by the constraints of the simulation.

The mapping that unwraps a given surface plays a significant role in the quality of the resulting texture. We have pursued the mapping problem by using mass-spring systems [5, 4, 1, 2]. Speciﬁcally, the restoration makes use of a physically based modeling approach, which uses physical principles for realistic simulation of complex physical processes. The restoration can be characterized as an operation on a 3D model that produces a new 3D model subject to a number of constraints. The physical forces for ﬂattening/unrolling are formulated mathematically to simulate ﬂattening/unrolling of a semi-rigid material. This mass-spring framework is general in that the material properties in the simulation can be adjusted to approximate the properties of the actual object.

The mass-spring particle system is deﬁned by a set of points, or particles, which have mass, position, velocity, and respond to forces, but have no spatial extent. In order to perform ﬂflattening or unrolling, the mass-spring particle system incorporates springs that connect adjacent particles, which are commonly known as structural springs. Particles that connect diagonally to neighbors are called shearing springs. With the springs attaching particles, each particle is subjected to a set of internal forces Fint imposed by the springs and external forces Fext such as gravity or collision.

Modeling and Solving The motion of the particles are governed by the classic second order Newtonian equation: f = ma. The state of each particle can be described by a 6-dimensional vector [x1, x2, x3, v1, v2, v3], where [x1, x2, x3] and [v1, v2, v3] represent a particle’s position and velocity at a given instant in time. Suppose F denotes the resultant force applied to a given particle. Let X, V denote the particle’s position vector and velocity vector, respectively. The following relationships then hold, from Newton’s law:

˙X = V ˙V = F

m

where ˙X, ˙V are the time derivatives of X, V .

The motion of the particle system can be simulated by state transitions, modeled as two initial value ordinary differential equation (ODE) problems:

˙X = V X(t0) = X0

**Figure 2:** (Left) This screen shot illustrates manipulation of a surface obtained from a CT dataset. (Right) Folds and creases can be represented by locked particles (gravity force is downward).

˙V = F

m V (t0) = V0

F = Fint + Fext

The internal forces are imposed by the springs connecting particles when the two particles move from their rest length. These forces are governed by the equation for the ideal Hookian spring and act to keep the particles together. The springs give the surface material its elastic (or rigid) coherence.

To ﬂflatten a surface, we apply a downward force (i.e., gravity) G = [0, 0, g] and force a collision with a plane. If the collision is modeled as purely elastic, the new velocity after collision becomes Vnew = Vold −2(Vold · N)N, where N is the normal to the collision plane. When colliding against the ground plane, the new velocity is Vnew = [v1, v2, −v3] with Vold = [v1, v2, v3].

To speed up the stabilization of the system, a coeﬃcient of restitution kr ∈[0, 1] is used such that Vnew = Vold −(1+ kr)(Vold · N)N. The value of the coeﬃcient kr = 0 adjusts the degree to which the material “sticks” to the collision plane. Note that kr = 1 is exactly the pure elastic collision. We select the value for kr empirically; a value such as kr = 0.1 has given reasonable results in our test cases. With the state initialized as [X0, V0], the ﬂflattening process becomes a calculation of the subsequent sequence of the states according to the ODEs, which can be approximated using a simple Euler method or a fourth order Runge-Kutta integrator.

We ﬂflatten a crumpled surface mesh using this simulation framework by building the particle system based on the mesh generated in Section 2.2, and applying the deﬁned gravity to allow it to drop, relax against the collision (ground) plane, and achieve a stable state.

Constrained Dynamics For surfaces that are rolled, folded, or wrapped, such as a scroll, we use constrained dynamics to perform an unrolling operation followed by ﬂflattening (Section 3.1). The idea for unrolling is that the description of the system includes particles and forces together with additional path constraints

for some speciﬁc subset of particles. The point is to make particles obey the laws of physics and at the same time satisfy the speciﬁed path constraints [14, 25]. We enforce the constraint, deﬁned below within the context of the particle system, on particles along a surface edge to simulate holding on and letting the rest of the surface drop and unroll. The constraint is formulated using the energy function C(X), which reaches zero when the constraints are satisﬁed. In our unrolling simulation, we deﬁne C(X) = ˙X = 0. To implement the constraint, constraint forces ˜F need to be computed for each constrained particle so that it obeys the constraint:

C(X) = ˙X = 0 ⇒˙C(X) = ¨ X = 0 (1)

By substituting ¨ X = F + ˜ F m into the equation above where F is the resultant force calculated in Section 3.1, we get

˜F = F.

In addition, we need to enforce the requirement that ˜F satisfy the law of conservation of energy. This means that the application of constraint forces cannot increase or reduce the energy of the particle system.

The kinetic energy for a particle is E = m

2 ˙X · ˙X. Its time derivative is ˙E = m ¨ X · ˙X = F · ˙X + ˜F · ˙X for the constrained particle set, and this equation shows the change of the energy that is brought about by both F and ˜F. Imposing ˜F without changing the energy means that ˜F · ˙X = 0. A key point is that any constrained particle must satisfy C(X) = ˙X = 0, which results in ˜F · ˙X = 0. Therefore the constraint forces ˜F = F are valid. The constraint force

˜F is added to each particle on the edge that is held when computing forces.

Integrated Restoration System We have developed a software system that integrates functions of ﬂflattening and unrolling based on mass-spring surface simulation. The system imports segmented 3D mesh and texture structures from the voxel data and allows a user to unroll/ﬂflatten the mesh interactively. It has the following features:

• Display control: The process of unrolling/ﬂflattening is visually presented. View angle and distance can be

**Figure 3:** Top (a): Rolled canvas strip in CT scanner. (b): One slice from CT-scan of canvas strip. (c): Digital photo of original, unrolled test strip. Center (d,e,f): Three progressive views of the digital unwrapping. Bottom (g): Unrolled result. (h): Thresholded result.

adjusted at any time and the user can choose to view the mesh and textured representations of the object.

• Particle control: An arbitrary subset of particles to be constrained can be chosen by the user at any time. Constrained particles are marked in red; other particles are blue.

• Object manipulation: The object can be translated, rotated and scaled to facilitate restoration.

• Simulation properties control: Simulation parameters, such as the integration methods (Euler, Midpoint and Runge-Kutta methods) and the time step length can be modiﬁed by the user at any time.

**Fig. 2** shows two screen snapshots of the restoration software interface. The main viewing window shows the 3D surface and texture. The controls give the user the ability to set the camera parameters (the point of view), the properties of the simulation, and path constraints on speciﬁc surface points. The screenshot on the left shows voxel data from a CT scan of a canvas strip (discussed in the next section) along with a number of simulation options on the left panel (particle lock, damping, integrator method, etc.). The screenshot on the right shows voxel data generated from our simulator, and the display window shows how particles can be locked at any point along the surface to enforce creases,

stiﬀedges, etc. In this case we added an impulse to the material hanging below the highest fold to make the surface “wave”. The graphical user interface in this case shows the “camera options” panel that controls the user’s point of view.

EXPERIMENTAL RESULTS We have implemented these algorithms in software and have completed a series of tests using replicas and two different CT scanners in order to generate voxel sets. Prior to these experiments we conducted a set of simulations [22] to develop software and to control and measure issues related to distortion, segmentation, and scanner resolution.

**Fig. 3** shows the scan of the canvas experiment via the UK Medical Center’s CT Scanner. In this experiment, we created a series of test strips with a variety of pigments (oil-based paint) and at varying degrees of resolution. The scanner response to paint on the canvas appears as bright spots in the slice shown in Fig. 3 (b). The object pictured in the viewport of our software in Fig. 2 (left) is the segmented, textured surface from one of the canvas test strip trials.

The steps of the restoration applied to an example canvas strip are shown in Fig. 3. The top row (a) shows the rolled up original in the CT scanner. The top center shows how one slice appears from the dataset generated by the CT scanner. The bright spots along the canvas surface are re-

**Figure 4:** Top (a): One CT-scan slice from a scan of a papyrus scroll. (b): Digital photo of original, unrolled scroll with scanned section marked. (c): Close-up of the scanned region. Center (d/e): Two views of the particle system simulation as the surface and texture are “unrolled”. (f): Detail view of educed information after CT-scan and virtual unrolling. The resulting image is very close to the original image (directly above). Bottom (g): Unrolled strip inset over digital photo of unrolled original.

sponses to pigment. The top right image gives scale and the control image. The medical scanner used in this experiment is tuned to healthcare applications and produces at best a resolution of 1-2 millimeters per voxel. The center row of Fig. 3 shows three successive steps of the simulated unrolling. The particles along the top edge of the segmented surface are locked, and gravity (down) forces the strip to unfurl. The bottom row shows what we obtain from the unrolled texture. We must emphasize that we are able to obtain the representation in the bottom row without ever touching the rolled canvas replica.

**Fig. 4** shows a more challenging example with real materials using a high resolution scanner. The papyrus replica was rolled and scanned at a resolution of approximately 12 microns per voxel with a custom-built CT-scanner. The top left image in Fig. 4 shows how the papyrus appears in a representative slice. Note the irregularities of the surface shape and the changes in contrast along the papyrus crosssection from the pigmentation. The control images (Fig. 4, top right) show the original for comparison and a detail view. The center row shows two representative views during the unwrapping along with a detail view of the control area that is identiﬁed in the top row. Note the agreement of the recovered patch (center, right) with the detail view of the control image (top, right). The wavy line below the symbol in the upper left corner is pronounced, and the CT data shows the underlying ﬁfibers of the papyrus as well. The scale of this detail view is about the width of two ﬁngers - clearly the scanner resolution at 12 microns is suﬃcient to achieve a very detailed reading. The bottom row shows the complete strip recovered from the voxel set, digitally unwrapped and superimposed on a control image of the original scroll. Alignment is good and resolution is well beyond the level necessary to see the detailed symbols. The unrolled strip represents a swath about two inches wide and eleven inches long through the scroll. We emphasize that we obtained the digitally unrolled swath shown in Fig. 4 purely from CT data, without physically opening the scroll.

CONCLUSIONS We have presented a new approach to the problem of analyzing damaged and inaccessible objects. This class of objects includes damaged books, manuscripts, scrolls, and other impenetrable items that traditionally have been either preserved for preservation’s sake or destroyed for the sake of physical analysis. Our method is based on nondestructive volumetric scanning followed by segmentation, surface modeling and simulation. We have shown that for a range of pigments and materials there is now a reasonable hope that we can reveal new information from a damaged collection without the need to radically alter its physical condition. We ﬁfind this idea of opening a digital representation instead of the physical one in order to reveal information to be very exciting.

Our experimental work presented in this paper demonstrates the major aspects of the framework: acquisition, segmentation and restoration via simulation. We use Computed Tomography (CT) for digitization, and note that CT scanners already exist that can provide high resolution scans (on the order of microns) and can respond to a number of pigments and materials that are widely available in collections. Volumetric scanning is clearly an area for future exploration: resolution is crucial to support subsequent pro-

cessing, and the volume of data produced at high resolutions is a computational challenge.

Our segmentation and manipulation framework, implemented in a working software system, provides the user with the capability to explore the information encoded in a volumetric scan. In particular, the ability to deﬁne layered textures and to interactively apply path constraints to the unrolling simulation is novel and substantially improves the analysis capabilities of the user. As techniques for digitization and analysis continue to be perfected, our goal is to enable the discovery and recovery of knowledge buried inside damaged collections.

ACKNOWLEDGMENTS We gratefully acknowledge support for this work under NSF grants IIS-9817483 and ANI-0121438. We thank Joe Gray for custom CT scans and tests, and Ivan George for access to the UK CT scanner. Thanks to artist Tim Vetters for making replicas for experiments. Finally, we thank David Jacobs and Kevin Donohue for collaboration and insight.
