---
id: 2015-allegra-virtual-unrolling-x-ray-computed
title: "Virtual unrolling using X-ray computed tomography"
year: 2015
backend: pymupdf
---

VIRTUAL UNROLLING USING X-RAY COMPUTED TOMOGRAPHY

D. Allegra∗, E. Ciliberto‡, P. Ciliberto∗, F.L.M. Milotta∗, G. Petrillo†, F. Stanco∗, C. Trombatore†

University of Catania ∗Dipartimento di Matematica e Informatica, Viale A. Doria no. 6, 95125 Catania, Italy

{allegra, milotta, fstanco} @dmi.unict.it, p.ciliberto@studium.unict.it † Dipartimento di Scienze Mediche Chirurgiche e Tecnologie Avanzate, Via S. Soﬁa, Catania, Italy

‡ Dipartimento di Scienze Chimiche, Viale A. Doria no. 6, 95125 Catania, Italy

## Abstract

In recent years the virtual restoration of ancient papyri has become an important research challenge. This is because the papyrus degradation is often very serious, so physical analysis could damage the artifact. In this paper we address the problem of virtual unrolling to read papyrus scroll by avoiding a dangerous physical unrolling. To this aim we propose a virtual restoration method based on software manipulation of X-ray tomographic images. To test the proposed approach, a realistic papyrus model has been made using the ancient method and pigments compatible with the Egyptian use. The stack of 259 slices, obtained through X-Ray Tomography device, has been processed in order to obtain a digital unrolled papyrus that is quite similar to the hypothetical unrolled sheet.

Index Terms— Virtual unrolling, X-ray CT, Papyrus, Scroll.

## 1. INTRODUCTION

Image processing techniques have been successfully applied in many ﬁfields related to Cultural Heritage [1–7] and can be also exploited in virtual restoration and preservation of ancient artifacts like parchments or papyri as part of the “Archeomatica Project” [8].

Papyrus is one of the oldest media to store text and images. Papyri were employed to record historical events, business transactions or even trivial events. Examples of typical use are related to the classical period of Egyptian civilization (Fig. 7(a)). Many ancient artifacts of this type are discovered during archeological excavation, nevertheless is not always possible to unroll the scrolls and read their contents. The physical unrolling can be difﬁcult for several reasons, such as scroll fragility, stuck sheets or even the presence of parasites and worms that have destroyed the paper. The classical approach is to carefully remove one by one each layer of papyrus and recompose this kind of puzzle over a ﬂat plane. This is an invasive method and it is no recommended by the recent trend of the restoration theory.

For this reason, it is necessary to investigate new techniques to analyze the content of papyrus scrolls that preserve the cultural heritage. This technique is called Virtual Unrolling. It is an algorithmic procedure which allows to obtain a digital version of an unrolled papyrus by starting from a digital and noninvasive acquisition of the original scroll. In this work, we present a method to perform virtual unrolling which exploits X-ray tomographic images. To perform data acquisition a GE Optima 660 system is employed. This device performs the Computed Tomography (CT) and provides a stack of slices of the scanned object. Despite Computed Tomography is mainly used for medical purpose, we exploited it to produce a cross-section view of the papyrus scroll. Hence, the scanned papyrus is represented as a stack of gray-scale images, where each slice appears as spiral (Figs. 5(a) and 6(a)). To distinguish among different kinds of materials (e.g., paper, ink, air) we consider the different X-ray reactions. In particular, ink has a higher response than paper, that result in a higher gray intensity. In order to make our study-case realistic, we realized a papyrus substrate made by the original method described by Plinius the Elder and we painted a hieroglyph inscription of Thutmosis III using pigments and binders according to Egyptian techniques, that is ochres with natural glue. These pigments, used to make our realistic-model, are visible with X-ray Computed Tomography. However other kinds of pigments exist and not all are visible using X-ray. To deal with these cases other technology should be exploited (e.g., nuclear magnetic resonance based on 13C nucleos).

In this paper, we propose a method to perform a semiautomatic virtual unrolling. To unroll the entire papyrus scroll, the operator has to select two points only once. The other steps of the procedure are automatic. The main aim of the automated procedure is to identify the path that should be followed to completely unroll papyrus. Unfortunately, the low resolution of employed device (e.g., 1 or 2 pixels for the sheet thickness) is a limit. In many cases two or more papyrus layers touch each other or there is some interruption. Our idea is to select a single good slice, that is a slice with the minimal number of the aforementioned problems, and com-

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:19:51 UTC from IEEE Xplore. Restrictions apply.

pute its path. Finally, we use this good slice path to estimate all the other paths.

The paper is organized as follows: Section 2 contains references to related works and state-of-the-art methods. In Section 3 we report several useful technical speciﬁcations about device used for CT acquisition; the proposed algorithm for virtually unrolling is presented in Section 4. Experimental settings and results are shown in Section 5. Finally, we report conclusions about our work in Section 6.

## 2. RELATED WORKS

Physical unrolling is not simple, in fact when papyrus scrolls is very fragile there is a high risk to damage it. In the 1980s “Oslo unrolling method” was been applied in an attempt to unroll two Herculaneum scrolls, but the result was a partial destruction of them, that is an irreversible loss of the cultural heritage [9,10]. After this event, all further attempts to physically unrolling papyri or parchments had been abandoned in favor of digital techniques that could analyze scrolls without opening them.

Some researcher take into account the possibility to use X-ray computed tomography (CT) to analyze the rolled parchments and papyri [11–14]. In particular, archaeological site of Hercolanum is rich of carbonized parchments which are impossible to unroll.

In the last years virtual unrolling problem has been addressed using better CT devices with respect on works of some decades ago [15,16]. In [15] the authors employ a high resolution device which use X-ray Micro Computed Tomography to perform virtual unrolling. This device produces a 3D model of scanned papyrus with almost well-spaced sheet layers. Graph Cut algorithm is used for segmentation, moreover the high resolution and 3D model allows to solve the problem of touching points between adjacent sheet layers (ill-spaced spirals) using a simple sliding window strategy. When the papyrus cross-section are ill-spaced because of the device resolution or serious artifact damage, some different approach is required. In [14] authors propose a method where a manually operation is performed. The user select the ill-spaced spiral regions and manually made them well-spaced.

In this paper, we present a novel semi-automated method to solve virtual unrolling issue. Despite the aforementioned approaches, our algorithm does not use 3D scans at high resolution, but low resolution images only. It includes a single user-guided step, where the operator selects the start point of the spiral path and the end one in a single slice. The userguided step is necessary because of the low resolution device. Afterwards the path is automatically detected for all the slices. Due to the low device resolution, critical ill-spaced scenarios cannot be treated. To perform virtual unrolling we use morphological operator, so that a simple and efﬁcient algorithm is guaranteed. This solution also ﬁt the problem of interrupted paths and mild ill-spaced spirals. The proposed

algorithm presents a good tradeoff between device cost (e.g., high resolution devices are relatively more expensive than low resolution devices), neatness and quality of results.

## 3. X-RAY COMPUTED TOMOGRAPHY

Computed Tomography (CT) is a technique that produces tomographic images, or simply “slice”, of an object or a human body by using X-ray. This technology is used in medical context to view the inner parts of a patient body. We use the GE Optima 660 device for CT acquisition of our study-case papyrus Fig. 2. According to technical speciﬁcations, minimal isotropic spatial resolution of this device is 0.35 mm and it can provide until to 128 distinct projection measurements per rotation. Moreover, application software provided with GE Optima 660 has an utility function that, through a path selected point-by-point by user, can perform a roughly virtual unroll of papyrus. However, this is an error-prone procedure, that could introduce artifacts and missing parts in the virtually unrolled version of the papyrus (Fig.1).

**Fig. 1.** Utility function of application software provided with GE Optima 660. On the left the papyrus section is manually drawing. On the right the result shows missing parts.

**Fig. 2.** (a) GE Optima 660 device used for Computed Tomography (CT) acquisition; (b) Particular of our study-case papyrus during calibration phase before CT acquisition.

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:19:51 UTC from IEEE Xplore. Restrictions apply.

## 4. PROPOSED METHOD

The images we get from X-ray CT represent the papyrus section, so these look like as spirals. For each papyrus section, the start and ﬁfinal point of the spiral should be identify in order to build an array of ordered pixel. Unfortunately, it is not easy to sort the points which compose the slice, because of the low resolution and some papyrus overlapping sheets. For this reason, we decided to use a single section proﬁle to estimate all the other ones, assuming that there are few differences between a couple of adjacent sections. The algorithm consists of three main steps.

### 4.1. Step 1: Slice selection

As ﬁfirst step the algorithm selects a good slice which respects the following criteria:

• The spiral path should be almost entirely detected through a raw segmentation.

• Low number of overlapping sheets into the slice. To satisfy ﬁfirst criteria the skeleton branch-points are detected using morphological operators [17]. Speciﬁcally, the following image segmentation is performed:

• Gamma transformation with γ = 2 and contrast stretching in order to highlighted the papyrus section;

• Otsu thresholding to get a raw segmentation;

• Morphological skeletonization to detect a ﬁfirst raw path;

• Morphological branch-points detection to identify sheets overlaps; If a sheets overlap exists, then it produces a branch-point into the skeleton. Of course, not all the branch-points indicate a sheets overlap, since they could be image artifacts or papyrus creases. However we prefer a slice with a low number of branch-points in order to minimize the probability that an overlap occurs.

To satisfy the second criteria the number of skeleton points is counted for each papyrus slice and the average number is computed. Skeletons with too few points are related to slice poorly deﬁfinite, while skeletons with too many points could be affected by noise. Hence a slice with a number of skeleton points nearest to the average value is preferable.

To combine these two criteria, both branch-points number and skeleton points number are normalized by dividing by the respective maximum value. So, a pair of the aforementioned normalized values (bi, si) is assigned to each slice xi. Finally, we choose the slice with the minimum Euclidean distance from the point (0, A), where A is the normalized average number of skeleton points.

### 4.2. Step 2: Slice reconstruction

Once a good slice has been identiﬁed, its spiral path must be rebuilt. First, we apply the preprocessing described above.

Then the branch-points and their 3 × 3 neighbourhoods are removed from the skeleton in order to disconnect the ramiﬁcations. Now the end-points are detected using the proper morphological operator. The end-points are pixels that identify a skeleton interruption.

The user selects the start point and the ﬁfinal point of the spiral. This is the single user-guided operation of the algorithm. Starting from the initial point, the 3×3 neighbourhood is taken into account for each pixel according the following rules:

• If into 3 × 3 neighbourhood there is a pixel which is a not visited skeleton point and it is not an end-point, then this pixel is added to an array of visited points. You move on this new point and the algorithm continues.

• If into 3 × 3 neighbourhood there is a not visited skeleton point, which is an end-point, then a break has been reached. To rebuild the missing path, the intensity grey value of the contrast stretched image is used (e.g., Fig. 5(b) and Fig. 6(b)). Speciﬁcally, the pixel of maximum value is selected. However the 3 × 3 neighbourhood is weighted through a probability 3 × 3 mask. There is a mask for each possible direction in 3 × 3 neighbourhood, so there are eight masks. Two of these masks are shown in Fig. 3. For example if the last movement has been along the top direction we use the mask in Fig. 3(a) to weigh the neighbourhood. These eight probability masks are based on a derivative of gaussian ﬁfilter and weighs more the pixels along the last direction of movement. When a new end-points is reached two skeleton parts are reconnected.

• The algorithm ends when the ﬁfinal point is reached.

0,185 0,215 0,185

0,108 0,108 0,108

0,039 0,013 0,039

0,108 0,185 0,215

0,039 0,108 0,185

0,013 0,039 0,108

**Fig. 3.** (a) The probability mask for the top direction; (b) The probability mask for the top-right direction. The other masks can be obtained with by rotating these matrices.

### 4.3. Step 3: Unrolling

The last step is the papyrus virtual unrolling. For each slice we select the sequence of pixel whose coordinates are stored in the vector of visited points of the adjacent slice. For each coordinate the pixels of maximum intensity along the direction of the gradient is chosen. Indeed paper and text of image have a higher intensity than background. Hence for each slice, we obtain a new vector of visited points, that is a string of ordered pixels (e.g., in Fig. 4). By stacking all this string we get the image of the virtually unrolled papyrus. This method can

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:19:51 UTC from IEEE Xplore. Restrictions apply.

be applied because a starting visited points vector has been computed in step 2 for the selected good slice. According to resolution we suggest to take into account 3 or 5 pixels along gradient direction.

**Fig. 4.** A scheme of the process pipeline.

## 5. EXPERIMENTAL RESULTS

To test the proposed approach a set of 259 slices of a single rolled papyrus has been used. The original size of the slice image is 512 × 512, but a facultative crop to 175 × 175 has been performed in order to remove empty area. Using the aforementioned criteria, a good slice has been automatically selected. The best slice among our case-study set has 0 branch-points and a number of skeleton points very close to average number. In Fig. 5 you can see the processing step for the selected slice.

(c)

(d) (e) (f)

**Fig. 5.** (a) Original cropped image; (b) Contrast enhancement of image (a); (c) Morphological skeletonization of image (b); (d) Morphological branch-points detection for image (c). Since no branch-points has been detected, it appears totally black; (e) Morphological end-points detection for the image (c); (f) The reconstructed papyrus proﬁle.

However, to show the overlap problem a bad slice example has been reported in Fig. 6. In Fig. 6(d) the branch-points

pixel locate on the overlapping area can be seen.

(c)

(d) (e)

**Fig. 6.** (a) Original cropped image; (b) Contrast enhancement of image (a); (c) Morphological skeletonization of image (b); (d) Morphological branch-points detection for the image (c); (e) Morphological end-points detection for the image (c).

In Fig. 5(f) the reconstructed path after the step 2 is shown. Finally, using the array of visited points each of 259 spirals can be unrolled. To compute the path of each slice by using the known path of the adjacent one we use the following strategy: for each coordinate in the visited points array (known path), we take into account 3 pixels of the adjacent slice along the gradient direction and choose the maximum value to compute the new path. This method is valid because there are some slight difference between two adjacent slices. By merging all the processed slices the image of unrolled papyrus is built. This result can be seen in Fig. 7(b). In Fig. 8 a comparison between the original version and the virtual unrolled one is shown and the common symbols are boxed.

## 6. CONCLUSION

In this paper, we propose a method for ancient papyrus virtual unrolling. This work is motivated by the criticality of physical unrolling, because of the high risk to damage the cultural heritage. To solve this problem a X-Ray Computed Tomography device has been employed to scan artifact. The input of the proposed algorithm is a stack of slices obtained from a single CT acquisition. Through mathematical morphology the spiral path of a good slice is rebuilt, and it is used as prototype path for every other slices. Despite the low resolution of tomographic images the experimental results show that this approach is valid, since many symbols of the original papyrus become visible after the virtual unrolling. In the future works we plan to improve the algorithm for low resolution images and to address the problem of strong ill-spaced sections using high resolution devices.

Authorized licensed use limited to: ISAE. Downloaded on November 17,2026 at 20:19:51 UTC from IEEE Xplore. Restrictions apply.

**Fig. 7.** (a) The original study-case unrolled papyrus; (b) A virtually unrolled version of the papyrus through the proposed algorithm.

**Fig. 8.** A comparison between the original unrolled studycase papyrus (a) and a false color image of virtually unrolled papyrus (b). Common symbols are highlighted.
