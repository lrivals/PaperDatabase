---
id: 2026-korotetskyi-volumetric-texture-analysis-unsupervised-ink
title: "Volumetric Texture Analysis for Unsupervised Ink Detection in Herculaneum Papyri"
year: 2026
backend: pymupdf
---

Volumetric Texture Analysis for

Unsupervised Ink Detection in Herculaneum Papyri

Oleksandr Korotetskyi1,2 and Michal Haindl2

## Abstract

The Herculaneum papyri, carbonised by the 79 AD eruption of Mount Vesuvius, can be imaged by X-ray micro-CT, yet their carbon-based ink is nearly iso-attenuating with the carbonised substrate and usually leaves no hight contrast in the reconstructed volume. State-of-the-art ink readers are supervised neural networks trained against labour-intensive labels and tuned on cropped regions of each segment; their letterby-letter legibility is uneven and they oﬀer little explainability. Motivated by the community’s call for a clearer understanding of the patterns underlying ink detection, we present a deterministic, training-free alternative that treats the unwrapped depth slab as a genuine 3-D signal. Three established texture descriptors — ﬁfirst-order statistics, Laws’ texture energy and block spatial autocorrelation — are lifted to volumetric form and evaluated both individually as stand-alone ink responses and jointly as a per-voxel mean fusion; the resulting volumetric response is projected to 2-D under a per-specimen depth prior, smoothed by a soft Markov random ﬁfield and binarised at an adaptive per-specimen threshold. Across 25 manually annotated Greek-letter specimens of Scroll 5 (PHerc. 172), under a δ-pixel exclusion band around the ink-mask contour, the best single descriptor reaches a mean Matthews correlation coeﬃcient (MCC) of 0.374, strictly positive on every specimen. Run on the full segment, the same operator also surfaces partially recognisable text whose letters match the community ink-prediction of a neighbouring segment that overlaps with the analysed segment in volume. The pipeline is thus oﬀered as a deterministic, explainable complementary signal that, in favourable cases, supervised neural detectors may consume as an additional input or weak label.

Keywords: Herculaneum papyri, PHerc. 172, X-ray micro-CT, unsupervised ink detection, volumetric texture analysis, 3-D block autocorrelation, 3-D Laws’ texture energy, 3-D ﬁfirst-order statistics, peak-anchored normal depth prior, soft Markov random ﬁfield, adaptive threshold, per-voxel evidence map, Vesuvius Challenge

1Faculty of Information Technology, Czech Technical University in Prague, Thákurova 9, 160 00 Prague 6, Czech Republic, 2Institute of Information Theory and Automation, Czech Academy of Sciences, Pod Vodárenskou věží 4, 182 08 Prague 8, Czech Republic

Correspondence korotole@cvut.cz,haindl@utia.cas.cz

## 1. Introduction

The Herculaneum scrolls — approximately 1 800 papyrus rolls excavated in 1752 from the Villa of the Papyri and carbonised by the pyroclastic surge that accompanied the 79 AD eruption of Mount Vesuvius — are too brittle to unroll physically (Fig. 1). Each sheet is itself a two-layer composite: a recto side with horizontal ﬁfibres and a verso side with vertical ﬁfibres laid on top of each other (Vesuvius Challenge organizers, 2023); the rolled scroll therefore exhibits an alternating horizontal/vertical ﬁbre pattern between successive wraps in the µCT volume, and ink sits as a thin layer on the recto surface.

**Figure 1** – Carbonised Herculaneum papyrus scrolls, images courtesy of the Vesuvius Challenge (Handmer et al., 2023; Vesuvius Challenge, 2025b). Left: photograph with a 15-cm ruler for scale. Right: exemplary internal structure revealed by X-ray micro-CT, showing the tightly wrapped papyrus laminae.

Modern µCT scanning, combined with virtual unwrapping (Seales et al., 2016), provides a non-invasive route to the underlying text: the scanned volume is segmented into a thin sheet that follows the papyrus surface and re-projected as a stack of co-registered depth layers. The remaining and dominant diﬃculty is ink detection: the iron-free, soot-and-gum carbon ink used in the ﬁfirst century has nearly the same X-ray attenuation as the carbonised substrate, so direct intensity thresholding is error-prone. The community-driven Vesuvius Challenge1 has accelerated progress on this problem with a series of supervised deep models that have recovered legible Greek text from previously unreadable scrolls (Farritor, 2023; Friedman et al., 2023, 2024; Nader, 2023; Roth and Nowak, 2025). A structural drawback of the supervised paradigm remains: the trained models are opaque — the patterns they exploit are not yet understood — their letter legibility is uneven across glyphs, they depend on scarce labour-intensive ground truth, and they have yet to be scaled from cropped regions to whole scrolls (Vesuvius Challenge, 2025a). We investigate whether established texture-analysis methods, lifted into 3-D, retain methodological relevance for volumetric ink detection. We treat the unwrapped depth slab as a genuine 3-D signal and let every per-voxel descriptor act in 3-D, so that stroke continuity across the z-axis is captured directly inside the operator support. We make the following contributions:

1https://scrollprize.org; the EduceLab-Scrolls dataset (Parsons et al., 2023) is the publicly released subset on which the work below is performed.

(1) Peak-anchored normal depth prior. A peak-driven envelope clipped to the surrounding mean-curve local minima intensiﬁes the operator response inside the depth window where the ink signal is most concentrated — relevant where segment volumes overlap and several papyrus sheets coexist within the same crop (Section 4.3). (2) Volumetric texture descriptors. Three well-established pixel-level operators (Haralick, 1979; Haralick et al., 1973; Laws, 1980) are lifted to act in 3-D, so that ink-stroke continuity along the z-axis is captured within each operator’s own support (Section 4.4). (3) Per-specimen adaptive threshold. An upper-tail oﬀset of each prediction’s own intensity statistics, accommodates the between-specimen drift of the prediction-intensity distribution without manual tuning (Section 4.5).

This work aims at contributing to several sub-problems of the community-curated open ink-detection agenda (Vesuvius Challenge, 2025a) — whole-segment application, interpretable voxel-level patterns and training-free maps that can serve as input or weak labels for supervised pipelines.

## 2. Related work

Virtual unwrapping and Herculaneum imaging. The virtual-unwrapping pipeline of Seales et al. (Seales et al., 2016) is the methodological ancestor of the Vesuvius Challenge: it produced the ﬁfirst computer-assisted reading of an intact scroll (the En-Gedi biblical fragment). Mocella et al. (Mocella et al., 2015) reported that X-ray phase-contrast imaging recovers individual letters inside rolled Herculaneum fragments. The EduceLab-Scrolls dataset (Parsons et al., 2023) provides the public scroll volumes, surface meshes and depth-layer renderings on which our work and the wider community operate. The geometric diﬃculty of Herculaneum imaging is exempliﬁed by Henderson (Henderson, 2025), who illustrates how the compressed and distorted spiral of PHerc. Paris 4 and the breaks and falsely-joined sheets of current automatic segmentations stand apart from earlier unwrapping benchmarks on simpler targets — folded papyri or documents with well-spaced windings (Klenert et al., 2025; Kulagin et al., 2024; Mahnke et al., 2020; Polevoy et al., 2022). Our paper is downstream of segmentation: we operate on the depth-layer stack of a region for which a ground-truth surface mesh has already been produced and a ﬂflattened Z×Y×X slab is available, and we focus on extracting the ink signal inside that slab.

Deep ink detection in the Vesuvius Challenge. The Vesuvius Challenge organised the supervised deep-learning eﬀort on the Herculaneum corpus around three annual cycles. The 2023 Grand- Prize submission by Nader, Farritor and Schilliger (Friedman et al., 2023; Nader et al., 2024) ﬁfixed the canonical recipe (Fig. 2) — a video-style transformer (TimeSformer) backbone trained against IR-derived labels and ensembled with a 3-D ResNet-101 and an I3D head — and recovered the ﬁfirst sustained passages of Greek text from Scroll 1. The 2024 cycle (Friedman et al., 2024) concentrated on automating the surrounding pipeline rather than replacing the underlying detection backbone. In 2025 the focus shifted to PHerc. 172 (Scroll 5), the same data on which the present article operates: by early 2026 about 70% of Scroll 5 had been digitally unwrapped (Vesuvius Challenge Team, 2025, 2026), and the $60 000 First Title Prize was awarded to Roth and Nowak for recovering the work’s title from inside the still-rolled scroll using a custom MiniUNETR architecture (Roth and Nowak, 2025). Scroll 5’s ink is reported unusually dense and exhibits plate-like surfaces shared with Scroll 4, tantalizingly similar to Scroll 1’s “crackle”

feature (Vesuvius Challenge Team, 2025), motivating training-free baselines that do not depend on scroll-speciﬁc labelled volumes.

**Figure 2** – Supervised ink-detection paradigm of the Vesuvius Challenge. A ﬂflattened papyrus fragment (a) is imaged in two modalities: an X-ray micro-CT volume (b) from which a virtually unwrapped surface mesh (c) is extracted (magenta), and an infrared photograph (e) of the same physical fragment. A detector is trained on paired patches: the input (d) is the W ×H×D slab of surface voxels around the mesh in (c); the supervisory label (g) is the binary ink mask obtained by thresholding the registered IR photograph (f). Our work bypasses this label-acquisition path entirely and operates only on inputs of the form (d). Image reproduced from the Vesuvius Challenge tutorial materials (Vesuvius Challenge, 2025a).

Volumetric segmentation tooling. The Vesuvius Challenge ecosystem authors segmentations through domain-speciﬁc desktop tools built on the EduceLab .volpkg layout: Volume Cartographer (VC) (Parker and EduceLab, 2016) and its maintained fork VC3D (Schilling et al., 2025). Crackle Viewer (Schilliger, 2023) is the companion ink-labelling tool presented alongside Thaumato Anakalyptor (Schilliger, 2024), run on ﬂflattened scroll-segmentation outputs. General-purpose volume renderers (ParaView, 3-D Slicer) render the raw scalar ﬁfield per voxel without surfaceaware abstractions. Our pipeline consumes the surface-volume output of VC3D/Thaumato and operates one stage downstream, on the per-feature volumetric cubes into which that surface is recast.

## 3. Data

Data used in the preparation of this article were obtained from the Vesuvius Challenge — CT Scans of Herculaneum Papyri (Angelotti et al., 2025), building on the EduceLab-Scrolls eﬀort (Parsons et al., 2023). We work speciﬁcally with the Scroll 5 (PHerc. 172) segment 20241108120732, distributed under the Creative Commons Attribution–NonCommercial 4.0 (CC BY-NC 4.0) license (Vesuvius Challenge, 2025b). The ﬂflattened layer stack was produced by the Thaumato Anakalyptor virtual-unwrapping pipeline of Schilliger (Schilliger, 2024), which ﬁts a sheet through the µCT volume and re-samples it as a stack of co-registered depth slices. After virtual unwrapping the segment is rendered as a stack of 65 co-registered depth layers, each a single-channel 8-bit image of size 4771×7414

pixels. Layer index ℓ∈{0, ... , 64} runs from the shallow side of the papyrus surface through the substrate to the deep side. A ﬁfiner point shapes every depth-axis interpretation in the rest of the paper. The Thaumato pipeline tiles the raw µCT volume into 3-D Grid Cells of 5003 voxels, extracts a surface PointCloud, partitions it into local sheet patches with Mask3D (Schult et al., 2023), and resolves the global sheet topology through a custom Random-Walk procedure over an overlap-weighted patch graph, propagating per-patch winding numbers from a seed patch (Schilliger, 2024). One consequence follows: the depth axis ℓis a normal-coordinate sample along the inferred sheet, not a physical µCT z, so layer-to-layer geometry is locally Euclidean but globally curved. Alongside the depth stack, the segment ships with a composite.jpg image, a single-channel max-projection composite over the depth stack, released alongside the segment (Angelotti et al., 2025) as a 2-D orientation view of the unwrapped sheet. The representative data are depicted in Fig. 3.

**Figure 3** – Three views of segment 20241108120732 as released by the Vesuvius Challenge (Angelotti et al., 2025). Left: depth layer ℓ= 32 in its native orientation. Centre: the segment’s composite.jpg. Right: reference ink prediction (inverted, bright = predicted ink) with the 25 manually located 512 × 512 glyph crops overlaid as red boxes. CT-background pixels of the left and centre panels are painted white for legibility on the page.

For quantitative evaluation we use 25 single-glyph crops of Scroll 5. The Greek-letter assignment of each crop is approximate, based on our best reading of the reference prediction, and serves only as a convenience label. The reference ink evidence for the entire segment2 is the prediction ﬁle (4864 × 7424 px), released by the Vesuvius Challenge alongside the segment. The depth layers themselves are stored at 4771×7414 px, so the prediction has a small ∼93×10 px padding overshoot that we trim before re-sampling the prediction onto the layer grid by nearest-neighbour interpolation. Per-glyph 512×512 binary masks are then cropped out of the re-sampled prediction at manually recorded (x, y) oﬀsets. No part of the dataset is split into training/validation/test sets because the pipeline contains no trainable parameters; the entire dataset is used at evaluation time.

2https://dl.ash2txt.org/full-scrolls/Scroll5/PHerc172.volpkg/paths/20241108120732/

## 4. Methodology

We characterise the per-layer ink/papyrus separability of the corpus, evaluate each 3-D texture descriptor individually, and combine them into a deterministic ink-detection chain (depth prior, adaptive threshold, fusion).

### 4.1. Pixel intensity distributions: ink vs. papyrus

The supervised community prediction (Section 3) collapses the 65-layer parallelepiped to a single 2-D map; pooled across the 25 specimens the ink/papyrus contrast is concentrated near the centre and vanishes at the slab boundaries (Fig. 4, Table 1). We quantify separability per layer by the standardised mean gap d′ and the ℓ1-overlap OL1 between the two pooled densities ^pp,ℓ and ^pi,ℓ,

d′(ℓ) = |µi(ℓ) −µp(ℓ)|

σpool(ℓ) , σpool(ℓ) =

q

 σi(ℓ)2 + σp(ℓ)2, OL1(ℓ) =

b=0

min

 ^pp,ℓ(b), ^pi,ℓ(b)

.

A narrow band of central layers around the peak at ℓ= 31 carries the visible separation (d′ >0.3 for ℓ∈[27, 32]; peak d′(31)=0.42, OL1(31)=0.79, mean gap ∆µ(ℓ)=|µi(ℓ)−µp(ℓ)|=11.4 grey levels at ℓ= 31). At the shallow side and deep boundaries the gap collapses (∆µ(0) = 1.9, ∆µ(64) = 0.6), d′ contracts by 5–17× and OL1 saturates above 0.96. Equivalently, the nonoverlapping mass 1−OL1 drops from 21% at the centre to 3–4% at the surfaces — statistically indistinguishable for any practical intensity threshold. The supervised ground truth therefore describes ink only as it appears near the central layer.

**Figure 4** – Pooled pixel-intensity densities at the centre depth ℓ= 31 for ink (orange, dashed) and papyrus (blue), averaged over the 25 annotated specimens. The visible ink lobe of this layer ﬂattens into the papyrus mode at the surfaces (Table 1).

The ink-detection techniques therefore must (i) operate on layers where the ink signal is actually present and (ii) zero its support elsewhere; the peak-anchored normal prior of Section 4.3 is exactly this per-specimen restriction.

ℓ · · · · · ·

µp · · · 146.9 149.2 151.9 155.1 158.2 160.8 162.2 162.0 160.2 157.1 153.3 149.7 146.8 144.9 144.3 144.5 145.2 146.1 146.8 · · · µi · · · 151.0 153.8 157.3 161.2 165.4 169.3 172.0 172.9 171.6 168.2 163.1 157.5 152.7 149.2 147.5 147.1 147.6 148.5 149.3 · · · d′ · · · 0.173 0.190 0.214 0.243 0.284 0.337 0.387 0.420 0.422 0.395 0.343 0.279 0.218 0.166 0.130 0.109 0.103 0.103 0.105 · · · OL1 · · · 0.926 0.921 0.910 0.893 0.872 0.843 0.815 0.793 0.787 0.805 0.832 0.862 0.888 0.908 0.923 0.932 0.936 0.936 0.940 · · ·

**Table 1** – Per-layer ink/papyrus separation across the central depth window ℓ∈[23, 41], pooled over 25 specimens, according to deﬁnitions in Eq. (1).

### 4.2. Ink sources across volume

An unwrapped Herculaneum segment is rarely a single ﬂat sheet: the Thaumato stitching procedure assembles volume chunks that can include the recto face, the verso face directly above or below it, and bleed-through from neighbouring windings. Each of those physical surfaces sits at a diﬀerent depth inside the 65-layer "cube" and constitutes a distinct plausible source of inkshaped evidence.

**Figure 5** – Per-letter XZ cross-section collage for 1-pi. Left: the segment-mean curve µ(z) (red) and per-layer variance σ2(z) (teal) on twin axes; detected cluster centres drawn as magenta verticals with their z label. Right: raw µCT cross-sections of the 512×65 X-by-Z slab at Y -stride 32 (16 panels, turbo colourmap, pixel intensity ﬂoored at 1). Ticks above each panel mark the detected cluster centres. The dominant central cluster (z⋆=29) sits at the peak of µ(z); the two ﬂanking clusters (z = 14 and z = 49) correspond to other pieces of papyrus visible as faint bright stripes.

For 1-pi, three clusters at z =14, z =29 and z =49 line up with the faint curved bright stripes, visible in the raw XZ cross-sections (Fig. 5). Each sheet must be treated as a separate candidate depth window, operating voxelwise on the full cube and then choosing one source per specimen or region; this is done accroding to the depth-prior construction outlined in Section 4.3. Across the 25 specimens the peak detector ﬁfinds one surface in 7 cases, two in 13 and three in 5.

### 4.3. Peak-anchored normal depth prior

The prior is derived from the raw µCT volume I ∈{0, ... , 255}D×H×W ; the depth weight it produces is then applied to whichever feature volume is being projected. The intuition is simple: the prior is re-centred on the layer at which the raw slab’s intensity is at the same time strongest and most spatially coherent, and clipped to the surrounding mean-curve dip so it does not bleed into neighbouring sheets. Concretely, for each layer z we form the min–max normalised layer mean

eµz = µz −minz µz maxz µz −minz µz

, µz = HW

x,y

I(x, y, z),

together with the standard von Neumann 4-neighbour coherence cz deﬁned on the indicator of the per-layer 75-th percentile, and pick the coherence-weighted argmax

ℓ0 = arg max z eµz · cz.

The support interval [zL, zR] is read oﬀthe layer-mean curve as the nearest local minima on either side of ℓ0 (extended to the cube boundaries when no interior minimum exists), and the symmetric normal envelope

w(z) = exp

 −(z −ℓ0)2/(2σ2)

 · ⊮[zL ≤z ≤zR], σ=15,

is the depth weight. The indicator zeros w outside the support interval, so the normal envelope centred at ℓ0 contributes only inside the mean-curve dip. The dispersion σ = 15 is intentionally larger than the typical peak half-width on the corpus, so that the per-specimen support interval [zL, zR] carries the depth selection, and the Gaussian only smoothly tapers the weight near the bracket edges. Algorithm 1 summarises the procedure.

Algorithm 1 Peak-anchored normal depth prior (per specimen).

Require: raw µCT volume I ∈{0, ... , 255}D×H×W , dispersion parameter σ Ensure: depth weights {wz}D−1

z=0 , centre ℓ0, support interval [zL, zR]

1: µz ← HW

P

x,y I(x, y, z)

2: qz ←75-th percentile of I(·, ·, z); Az ←⊮[I(·, ·, z) > qz]

3: cz ←4-neighbour pair density of Az

4: eµz ←(µz −minz µz)/ max(maxz µz −minz µz, ϵ)

5: ℓ0 ←arg maxz eµz · cz

6: zL ←largest i < ℓ0 with µi ≤µi±1 (else 0)

7: zR ←smallest i > ℓ0 with µi ≤µi±1 (else D−1)

8: wz ←exp  −(z −ℓ0)2/(2σ2)

 · ⊮[zL ≤z ≤zR]

9: return {wz}, ℓ0, zL, zR

For multi-sheet specimens (Section 4.2) the single-peak arg max of Eq. (3) generalises in the implementation to a prominence-ﬁfiltered set of peaks of the same proﬁle eµz·cz. Only the highestprominence peak is used from that set; secondary peaks are not consumed and are reported as audit candidates.

### 4.4. Volumetric texture descriptors

**Figure 6** – 3-β slab, 3-D block autocorrelation (b =2) above T =155.

We deﬁfine three texture descriptors that act on the volumetric µCT cube directly, in 3-D, so the pixel values’ co-variation along z and the spatial coherence of an ink stroke across consecutive layers enter the operator response inside its own support. Per-layer 2-D analogues of the same operators run on the projected output, not on the voxel grid, and are therefore outside the scope of this volumetric study. Acting in 3-D gives direct access to ﬁbre orientation, stroke-thickness variation across z, and the spatial distribution of anomalous-intensity voxels inside the slab (Fig. 6); the 2-D-projected per-operator panels of Fig. 7 preserve the magnitude of the response but ﬂflatten its spatial alignment along z. Ground-truth ink masks for this corpus are, however, supplied only in 2-D, so any quantitative evaluation against them requires a 2-D projection of the volumetric prediction and a binarisation step before per-pixel MCC can be computed; Sections 4.5 and 4.6 deﬁfine that threshold and projection.

Throughout this section I ∈{0, ... , 255}D×H×W denotes the single-channel 8-bit µCT slab and F3D a generic 3-D feature volume of the same shape. Fig. 7 shows the per-operator response on a representative specimen (compared to the raw z-mean) collapsed to 2-D.

(a) Raw z-mean (jet) (b) ACF3D (b =2) (c) FOS3D (w =5) (d) LTE3D

LL (k =7)

**Figure 7** – Per-voxel response of the three 3-D texture operators on specimen 10-γ, 2- D-projected and shown next to the raw-intensity baseline. (a) Raw µCT z-mean under the same projection; (b) ACF3D

b=2; (c) FOS3D (w = 5); (d) LTE3D

LL (k = 7). All panels use the per-specimen peak-anchored normal projection of Section 4.3 (ℓ0 = 30, σ = 15, support interval [21, 38]), jet-mapped after 2–98% percentile clipping (blue →red as evidence rises).

4.4.1. 3-D autocorrelation. The 3-D block-based autocorrelation function (ACF) tiles the cube into disjoint b×b×b blocks and, for every oﬀset (k, l, m)∈[0, b)3, computes a per-block circular autocorrelation: each block is multiplied element-wise by the copy of itself shifted by (k, l, m) with wrap-around at the block boundary, and the resulting scalar is stored back at the in-block position (k, l, m). For a block B with corner xB = (zB, yB, xB),

(5) ACF3D

b (B; k, l, m) = b3

d ∈[0,b)3

I(xB+d) I

 xB+((d+(k, l, m))mod b)

, 0 ≤k, l, m < b,

where modb is applied componentwise. Each b3 block thus reports its own internal correlation structure. We use b =2 exclusively: it probes the ∆z =1 inter-layer lag — the immediate continuity that distinguishes an ink ﬁbre from acquisition noise — without averaging ink-and-substrate together inside the same block, which is what happens at larger b once the block straddles the full ∼3-voxel stroke thickness.

4.4.2. 3-D ﬁfirst-order statistics. The ﬁfirst-order-statistics (FOS) energy is the local mean of the squared signal over a w ×w window. With the slab rescaled to eI = I/255 ∈[0, 1] for numerical stability, the volumetric counterpart on a box of side w is

FOS3D(x, y, z) = w3

(i,j,k) ∈Bw(x,y,z)

eI(i, j, k)2,

where Bw(x, y, z) ⊂Z3 is the w×w×w voxel box centred on (x, y, z). We use w =5: the 3-D box averages out small CT noise without erasing the strokes, which are typically 3–6 layers thick.

4.4.3. 3-D Laws texture energy. The 3-D Laws texture energy (LTE) on the L⊗L⊗L kernel (LTE3D LL henceforth) is the triple outer product of the length-k binomial smoothing kernel Lk (for k = 7, L7 = (1, 6, 15, 20, 15, 6, 1)):

KLLL(i, j, m) = Lk(i) Lk(j) Lk(m), i, j, m ∈{0, ... , k−1},

which we convolve with the (normalised) volume I and whose absolute response is reported. k =7 is the smallest odd length that captures three full intra-stroke layers on each side of a voxel. The isotropic 3-D kernel responds to ink strokes whose energy is distributed across several depth layers.

### 4.5. Adaptive threshold

The fused prediction ^Is (Section 4.6) drifts from specimen to specimen, so a ﬁfixed cut-oﬀat T =128 — the midpoint of the 8-bit intensity range [0, 255] — over- or under-ﬁres depending on the specimen. We binarise instead at the per-specimen oﬀset

Ts = µ(^Is) + k σ(^Is), k = 0.5,

with k =0.5 chosen so the accepted-pixel fraction (22–28% on the empirically right-skewed predictions) matches the observed per-crop ink coverage |Ms|/|s|=0.27±0.07. A small fraction of pixels (pit edges, inclusion grains, surface damage, acquisition speckle) sit far above the prediction’s upper tail and would bias µ(^Is) and σ(^Is) upward if allowed into the pool. We strip them with a one-dimensional Reed–Xiaoli (RX) anomaly ﬁfilter — a scalar Mahalanobis distance from the prediction mean,

z(x, y) = |^Is(x, y) −µ(^Is)| / σ(^Is),

— and recompute Ts on the pixels whose RX score is at or below the 99-th percentile Q99 of z:

Ts = µ

 ^Is, KRX

 + 0.5 σ

 ^Is, KRX

, KRX = {(x, y) : z(x, y) ≤Q99}.

The trim removes the bright micro-specks without ever masking the classiﬁer itself: Ts is computed on KRX but the binarisation rule^Is ≥Ts is applied to every pixel of the prediction.

### 4.6. Volumetric Fusion

Each operator captures a diﬀerent aspect of the local stroke signal (energy, low-pass smoothness disturbance, short-range z-coherence); a per-voxel mean fusion exploits this complementarity by averaging the three feature volumes after min–max normalisation, in order to intensify potential ink/papyri dissimilarity:

F3D(x) =  g FOS3D(x) + g LTE3D,LL(x) + g ACF

3D b=2(x)

, eX(x) = X(x) −min X max X −min X .

The fused volume is projected to 2-D by the per-column maximum of the depth-weighted response,

^Is(x, y) = max z F3D(x, y, z) w(z),

with w(z) the peak-anchored Gaussian envelope of Section 4.3; the result is smoothed by ten iterations of a soft Markov-random-ﬁfield (MRF) posterior smoother (closed-form per-step iteratedconditional-modes (ICM) update on a Gaussian MRF with a quadratic smoothness prior (Besag, 1986), β =2.5, 4-connected) and binarised at Ts. Figure 8 summarises the end-to-end chain.

## 5. Evaluation

We benchmark each individual 3-D operator and the three-operator fusion against the 25 supervised reference masks of Section 3. The protocol below ﬁxes the evaluation metric and

**Figure 8** – End-to-end 3-D pipeline: raw µCT cube →three volumetric texture descriptors →per-voxel mean fusion →peak-anchored normal depth projection →soft MRF posterior smoother →adaptive threshold Ts.

the boundary-handling convention; the headline result and a sensitivity sweep over the buﬀer width follow.

### 5.1. Protocol

For every specimen s we compare the thresholded fused score^Is to the manual mask Ms, both co-registered at layer-stack resolution. Pixels within δ = 4 px of any ground-truth (GT) contour (outer letter boundary and interior holes, e.g. the loops of β, ρ, α, δ) are excluded; the choice of δ is motivated and swept in Section 5.3. Hole pixels themselves are treated as background ground truth: a positive prediction inside a β-loop counts as a false positive. The headline metric is the Matthews correlation coeﬃcient (Matthews, 1975), robust to ink/non-ink imbalance and zero for random noise.

### 5.2. Headline result

Across the 25 annotated Greek-letter specimens the mean MCC of the 3-operator stack of Eq. (11) is MCC=+0.3643 (median +0.3861, top +0.523 on 17-η). Among the individual descriptors, ACF3D

b=2 is the strongest single operator on the corpus (mean +0.3743, median +0.3917) and on its own even narrowly outperforms the three-operator fusion — both mean and median best each specimen-by-specimen comparison fall to it in 16/25 specimens (Table 2). Per-specimen glyph predictions are visualised across the full corpus in Fig. 9.

### 5.3. Boundary buﬀer sensitivity

The buﬀer width δ = 4 px is picked a priori to absorb the small residual contour uncertainty of the supervised reference masks (which are themselves per-pixel network predictions and are unlikely to be pixel-perfect along the ink stroke) plus Thaumato’s trilinear-interpolation sampling error (Schilliger, 2024). To verify that the headline number is not an artefact of that choice we sweep δ∈{0, 2, 4, 8, 12} px under the otherwise unchanged headline pipeline (Table 3).

**Table 2** – Per-specimen MCC of each individual 3-D operator and the 3-operator fusion under the headline pipeline of Section 5.1 (each column runs the same projection + MRF + adaptive Ts pipeline with its own input volume; Ts column reports the fusion threshold).

Sorted by descending fusion MCC.

FOS3D LTE3D

LL ACF3D

b=2 Fusion Specimen MCC Ts MCC Ts MCC Ts MCC Ts 7-η +0.490 85.8 +0.510 109.6 +0.533 103.5 +0.515 99.0 17-η +0.500 96.3 +0.521 119.6 +0.522 110.1 +0.523 109.2 8-τ +0.443 86.1 +0.452 109.4 +0.476 103.1 +0.458 98.6 9-υ +0.453 86.3 +0.463 110.3 +0.472 103.7 +0.465 99.6 18-σ +0.384 93.6 +0.414 118.4 +0.450 113.4 +0.422 107.6 20-ν +0.448 102.4 +0.442 126.4 +0.441 116.0 +0.444 114.8 10-γ +0.425 100.2 +0.440 121.4 +0.447 110.9 +0.441 110.4 15-υ +0.440 91.0 +0.445 115.3 +0.436 102.7 +0.442 102.8 3-β +0.415 89.3 +0.430 111.4 +0.442 97.2 +0.432 100.1 11-χ +0.389 89.1 +0.410 113.1 +0.427 101.0 +0.412 102.1 21-δ +0.355 88.5 +0.383 117.7 +0.411 107.4 +0.386 106.6 16-ρ +0.404 91.5 +0.399 116.9 +0.391 108.9 +0.401 105.6 1-π +0.395 91.9 +0.395 111.7 +0.397 99.5 +0.398 101.9 2-κ +0.356 104.8 +0.378 123.4 +0.392 104.9 +0.377 110.9 19-σ +0.377 107.0 +0.370 130.1 +0.378 119.4 +0.373 120.0 14-ω +0.339 105.0 +0.347 124.5 +0.363 101.3 +0.351 111.2 25-π +0.318 93.6 +0.335 114.3 +0.349 94.5 +0.336 102.8 13-µ +0.297 88.9 +0.292 114.1 +0.328 107.9 +0.304 102.1 4-λ +0.294 75.2 +0.323 97.1 +0.326 89.1 +0.320 86.5 24-δ +0.298 98.8 +0.287 120.1 +0.275 110.3 +0.288 109.4 5-α +0.230 80.2 +0.242 105.5 +0.254 96.3 +0.244 95.9 22-ι +0.186 96.9 +0.202 123.2 +0.248 111.4 +0.210 111.3 12-λ +0.195 83.5 +0.208 108.5 +0.224 101.4 +0.211 97.4 23-α +0.182 93.3 +0.194 117.3 +0.217 108.9 +0.198 106.3 6-β +0.155 86.6 +0.152 108.8 +0.159 98.4 +0.156 97.3

Mean +0.351 92.2 +0.361 115.5 +0.374 104.9 +0.364 104.4 Median +0.377 91.5 +0.383 115.3 +0.392 103.7 +0.386 102.8

The dependence is monotone: removing the buﬀer entirely penalises the model for the residual stroke-shape mismatch of the reference mask and costs ∼0.02 on the mean; widening the buﬀer to 12 px gains ∼0.03 but pushes the model towards losing its physical anchor.

δ (px) Fusion mean MCC Fusion median MCC

+0.3421 +0.3604 +0.3537 +0.3728 +0.3643 +0.3889 +0.3813 +0.4117 +0.3926 +0.4324

**Table 3** – Boundary-buﬀer sensitivity of the headline Fusion MCC across the 25 specimens. Headline pipeline of Section 5.2 held ﬁfixed; only δ varied.

(a) 7-η (b) 17-η (c) 8-τ (d) 9-υ (e) 18-σ

(f) 20-ν (g) 10-γ (h) 15-υ (i) 3-β (j) 11-χ

(k) 21-δ (l) 16-ρ (m) 1-π (n) 2-κ (o) 19-σ

(p) 14-ω (q) 25-π (r) 13-µ (s) 4-λ (t) 24-δ

(u) 5-α (v) 22-ι (w) 12-λ (x) 23-α (y) 6-β

**Figure 9** – 5 × 5 collage of the 25 specimens, each tile showing the binarised prediction ^Is ≥Ts of the best-performing method for that specimen across {FOS3D, LTE3D

LL, ACF3D

b=2, Fusion} (per-row winner of Table 2), sorted by descending best MCC. Each tile is shown inverted (black = predicted ink, white = background) with the manual ink-mask contour overlaid in red (1 px) and the δ = 4 boundary band overlaid in semi-transparent bright yellow.

## 6. Ablations

The headline of Section 5.2 owes its number to two ingredients acting together: the three 3- D operators and the per-specimen peak-anchored normal depth prior that selects which layers they speak from. Beyond the 512×512 glyph crops on which it is calibrated, the per-specimen prior

is not guaranteed to remain as eﬀective at the segment scale: a full Thaumato segment spans a much wider range of papyrus-surface topology — locally varying sheet orientation, multiple overand under-lapping wraps, and stitching artefacts (Section 3) — and the mean-curve peak that anchors the prior on a clean glyph is no longer the dominant signal across such a heterogeneous region. To stress-test that limitation we keep ACF3D

b=2 — the strongest single operator on the corpus (Table 2) — and replace the prior with a uniform per-column maximum inside a manually chosen depth window (shallow [0, 20], middle [21, 43], deep [44, 64], covering all 65 layers without overlap).

Shallow band (ℓ∈[0, 20], 21 layers, Ts =140)

Middle band (ℓ∈[21, 43], 23 layers, Ts =145)

Deep band (ℓ∈[44, 64], 21 layers, Ts =142)

**Figure 10** – ACF3D

b=2 grayscale prediction on the full 4771×7414 segment under three contiguous depth bands.

Figures 10 and 11 visualise the resulting full-segment ACF3D

b=2 predictions in grayscale and jet. The middle band recovers the substrate slab around the nominal ink layer ℓ≈31; the shallow and deep bands expose ink-shaped responses on over- and under-lapping sheets that the headline’s central support interval correctly suppresses for per-letter benchmarking but which the community ink-prediction ﬁle — committed to a single depth window — cannot report. Speciﬁcally, running the same ACF3D

b=2 pipeline on a 3573×736 wide band across the shallow window ℓ∈[0, 21] of the segment surfaces a partially recognisable text fragment that does not belong to this segment prediction at all: it belongs to a neighbouring segment whose physical surface overlaps in the (x, y) plane but lives at a diﬀerent depth along the unwrapped normal. The recognised letters match the community ink-prediction of that neighbouring segment, not of the segment whose volume actually produced the ACF response (Fig. 12). The community prediction of the segment we operate on contains no recognisable symbols in this region.

## 7. Discussion

The headline result is the best-single-operator MCC = 0.374 across 25 Greek-letter specimens under the protocol of Section 5.1. ACF3D

b=2 alone narrowly edges the three-operator fusion

Shallow band (ℓ∈[0, 20], 21 layers, Ts =140)

Middle band (ℓ∈[21, 43], 23 layers, Ts =145)

Deep band (ℓ∈[44, 64], 21 layers, Ts =142)

**Figure 11** – Jet panel of the same three ACF3D

b=2 predictions above the per-band adaptive threshold. Several of the ink-shaped responses surfaced by the shallow and deep bands do not appear in the community ink-prediction ﬁle released alongside the segment.

**Figure 12** – Top: ACF3D

b=2 grayscale on ℓ∈[0, 21]. Middle: the same in jet above the adaptive threshold. Bottom: matching spatial crop of the community prediction for neighbouring segment 20241108111522 (inverted, black = predicted ink).

(+0.364). The cross-band ablation of Fig. 11 shows that ink-shaped evidence still surfaces with the depth prior disabled, isolating the operator-level contribution from the prior.

Letter shapes diﬀer from neural-network predictions. The reference contours of Fig. 9 come from a supervised network prediction, not from manual letter traces. The deterministic panels recover the contoured letter region but rarely the exact shape pixel-for-pixel: on clean specimens our strokes are sharper or thinner than the network contour, on others the surfaced ink falls slightly outside it; in some cases (e.g. 16-ρ) the network prediction itself overlaps actual void (damaged region) inside the contoured area, so it is not a per-pixel-MCC-optimal target; this is consistent with the supervised network ﬁtting its predictions to canonical Greek-letter shapes rather than to per-voxel ink evidence alone. Section 5.3 quantiﬁes the mismatch.

Cost of the 2-D projection. The per-column max projection of Eq. 12 retains stroke magnitude but discards the per-voxel z-alignment, conﬂating ink-bearing ﬁfibres with oﬀ-surface anomalous voxels at the same (x, y); the MCC against 2-D masks therefore underestimates the volumetric evidence the descriptors actually recover.

Where the method still fails. The lower-tail specimens of Table 2 — 4-λ, 22-ι, 24-δ, 12-λ, 23-α, 6-β — coincide with locally deformed substrate; the operators recover only the parts of the letter that lie on intact papyrus, being prone to capturing noise.

Cross-segment and cross-scroll transfer. Within Scroll 5 (PHerc. 172) the pipeline transfers without re-tuning and locates the silhouettes of glyphs already present in the community inkprediction across a diverse set of segments. Applied to Scroll 1 (PHerc. Paris 4) the same stack does not yield comparable results: only rare, fragmentary parts of the predicted silhouettes appear, almost exclusively at the ink/papyrus boundary. We treat the Scroll 1 outcome as a negative result. The pipeline is therefore positioned as an exploratory, complementary signal — open to further reﬁnement, not a universal Herculaneum papyri reader.

Position relative to the open ink-detection sub-challenges. Returning to the open ink-detection agenda (Vesuvius Challenge, 2025a): the criterion of reverse-engineerable voxel-level patterns is met by construction — the pipeline is composed exclusively of closed-form descriptors, a deterministic depth prior and a soft MRF posterior smoother. Whole-segment application is exercised by the three-band experiment of Section 6, which scales to the full 4771×7414 ﬂflattened sheet without per-spec retuning. The training-free evidence-map criterion is addressed indirectly through the deterministic per-pixel signal that a supervised pipeline can consume as an additional input or as a weak label. Absolute model performance is the one open-agenda criterion this work does not attempt to solve in isolation.

## 8. Limitations and future work

The headline result notwithstanding, the present unsupervised pipeline carries several acknowledged drawbacks, discussed below alongside the future-work directions they motivate.

Single scroll. As reported above, the pipeline was evaluated on multiple segments of Scroll 5 (PHerc. 172), where it attained moderately strong results conditional on the quality of the upstream segmentation, and on several segments of Scroll 1 (PHerc. Paris 4), where its performance degraded extremely. Behaviour on the remaining Herculaneum scrolls is unknown, so the generality of the approach cannot be assessed without further experiments.

Narrow feature stack. The fusion uses three volumetric descriptors. Beyond multi-resolution 3- D Laws kernels and ACF block sizes outside the tested b =2, other volumetric texture families — 3-D Gabor ﬁfilters, 3-D local binary patterns, 3-D causal autoregressive (CAR) predictive-surprise

volumes, structure-tensor descriptors and learned-dictionary responses — are natural candidates worth trying to analyze the volumetric ink signal from diﬀerent perspectives. Pre-segmentation application. The descriptors act on voxel patterns directly, with no dependence on a virtual-unwrapping step. Running the pipeline on the raw µCT "unwrapped" volume, before segmentation, may surface ink-shaped evidence that informs the segmentation itself rather than consuming its output. Substrate-failure recovery. Specimens on locally deformed substrate lose recall in proportion to substrate damage. A ﬁfiner-grained substrate reconstruction — e.g. a polynomial sheet ﬁt per detected papyrus surface — could make this damage explicit and tolerable. Ink/ﬁbre disentanglement. The present descriptors respond to papyrus ﬁfibres as well as to ink traces; separating the two responses is a clear direction for future work. Hybrid supervised priors. The fused 3-D volume and the per-band predictions are per-voxel signals available before any thresholding step. Conditioning a supervised network on those signals instead of the raw layer stack is the quite interesting possibility for hybridisation.

## 9. Conclusions

We presented a fully unsupervised, deterministic, label-free volumetric ink-detection pipeline for µCT-imaged Herculaneum papyri. Three contributions support the headline result:

(1) Three volumetric texture descriptors — 3-D ﬁfirst-order energy, 3-D Laws LL energy and 3-D block autocorrelation at b =2 — that act jointly along the depth axis inside their own support. (2) A peak-anchored normal depth prior whose centre is the coherence-weighted argmax of the fused volume and whose support is clipped to the surrounding mean-curve local minima, replacing a population-average ink layer with a per-specimen one. (3) A per-specimen adaptive threshold Ts = µ(^Is) + 0.5 σ(^Is) computed on the prediction’s own intensity distribution after a Reed–Xiaoli 1% outlier trim.

Across 25 Scroll 5 (PHerc. 172) specimens, ACF3D

b=2 leads at mean MCC=+0.374 (top +0.533 on 7-η); the three-operator fusion follows at +0.364. On the full segment across shallow, middle and deep depth bands, the same operator surfaces partially recognisable text matching the community ink-prediction of a neighbouring, overlapping segment. This deterministic, training-free per-voxel evidence map can serve supervised detectors as an explainable auxiliary input or weak label, and as a reproducible baseline for future Herculaneum ink-detection work.

## 10. Acknowledgements

The authors thank the Vesuvius Challenge community and the EduceLab-Scrolls team for releasing the µCT data of Scroll 5 (PHerc. 172) (Angelotti et al., 2025; Parsons et al., 2023) under CC BY-NC 4.0 (Vesuvius Challenge, 2025b), on which our experiments are run, and the Faculty of Information Technology of the Czech Technical University in Prague and the Institute of Information Theory and Automation of the Czech Academy of Sciences for institutional support.

## 11. Funding

The ﬁfirst author received only the standard doctoral stipend for full-time PhD students from the Czech Technical University in Prague, Faculty of Information Technology. No external project funding was used for the speciﬁc work reported here.

## 12. Conﬂict of interest disclosure

The authors declare no ﬁnancial conﬂicts of interest in relation to the content of the article.

## 13. Author contributions (CRediT)

O. Korotetskyi: Software, Validation, Formal analysis, Investigation, Methodology, Data curation, Writing — original draft, Writing — review and editing, Visualization. M. Haindl: Conceptualization, Project administration, Theoretical guidance and advisory input, Supervision, Funding acquisition.

## 14. Use of generative AI

The authors disclose that large language models (speciﬁcally, the Claude family of models from Anthropic) were used as drafting assistants for translation, LaTeX formatting, and for code review during the development of the accompanying software. All AI-generated text, code, and equations were veriﬁed by the authors against source data and the underlying scripts before inclusion; no ﬁfigures, photographs, or illustrations in this article were generated by AI. No bibliographic references were sourced from AI without independent veriﬁcation of the DOI and the cited claim. The authors take full responsibility for the content of the article.

## 15. Data, script, code, and supplementary information availability

Scripts, code, conﬁguration ﬁfiles, supplementary information, images and per-specimen output archives are available at https://github.com/korotole/vtfid and https://doi.org/10. 5281/zenodo.20766169 (Korotetskyi & Haindl, 2026). The data related to Scroll 5 / PHerc. 172 are released by the Vesuvius Challenge as part of the EduceLab-Scrolls dataset (Parsons et al., 2023) under CC BY-NC 4.0; access via https://scrollprize.org/data (Vesuvius Challenge, 2025b).
