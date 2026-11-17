---
id: 2026-pellerano-rectina-m3-m4-dense-ink
title: "Rectina m3 and m4, dense ink readers for Herculaneum papyri rebuilt on current renders"
year: 2026
backend: pymupdf
---

evilaliv3/vesuvius-challenge-pipeline · results/db27c806-rectina · not yet published · last updated 10 November 2026

Rectina m3 and m4, dense ink readers for Herculaneum papyri rebuilt on current renders

Giovanni Pellerano

Milano, Italy giovanni.pellerano@evilaliv3.org

## Abstract

Rectina m3 and m4 are the second pair of checkpoints of the Rectina ink reader, the villa hybrid 3D/2D network trained from random weights on dense composite labels. They were retrained on villa main with bicubic renders of the 87 training segments, a revisit cap of 0.5 in the sampler and a masked, clipped gamma augmentation, in one chain: the stages s1 (78125 iterations at 128 px), ft116k (12000) and s2 (40000) give m3, and the stages s3 (30000 iterations at 256 px) and s4 (20000 at 384 px), continued from the weights of m3, give m4. These changes were made together, there is one seed per checkpoint and no ablation, so no result is attributed to any of them. On the fourteen evaluation units m4 scores above Reader v3 in AUC on 10 of 14 (mean difference +0.0056, median +0.0049) and above Reader v2 on 11 of 14 (mean difference +0.0175, median +0.0159); m3 scores above Reader v2 on 9 of 14 (mean difference +0.0072) and above Reader v3 on 6 of 14 (mean difference -0.0047). On the six control units outside the training segments m4 is above Reader v3 on 4 of 6 (median +0.0008) and above Reader v2 on 5 of 6 (median +0.0115). Differences of a few thousandths are below what this work can resolve with one seed. Weights and model cards are published in the model repository [1].

## I. Introduction

The organisers of the Vesuvius Challenge state the last of the three problems of reading a scroll as “detecting or segmenting the ink signal on, or near, the recovered writing surface” and add that “The subtle differences that distinguish ink from papyrus must be teased out of data like this” [3]. A detector that answers this must say, for each point of a segmented surface, whether it carries ink. The readers that exist for the scrolls of the open data [4] are Reader v2 [5] and Reader v3 [6], and Rectina m1 and m2, described in an earlier article [2], were compared with them.

The engine is not ours: the scan data and the labels of the organisers, the ink detection code of villa with its model, training and render tools [7], and the two readers with which we compare. The training in stages on larger tiles follows Reader v3, which in the words of its README is “Reader V3 is Reader v2 trained further on larger tiles, 30k iterations at 256 px and then 20k at 384 px”, and for which “The architecture, the training data and the labels stayed the same” [6]. What is ours, as the files of this work show: the evaluation on units outside the training segments, the render recipe with its patch, the checks of the comparison and the chain that releases the checkpoints. Rectina m3 and m4 were trained again from random weights on the current villa main, with the surfaces of all 87 training segments rendered again, so that they differ from Rectina m1 and m2 in several things at once (the renders, a revisit cap in the sampler, a masked and clipped gamma

augmentation and the version of the training code, section II). We make no claim that any one of these changes explains a result: there is one training seed for each checkpoint and no ablation. Rectina m3 is the model after the first three stages, Rectina m4 the model after two more. This article gives the recipe of the training, the measurement, and the comparison of each of the two checkpoints with Reader v2 and Reader v3, on eight held-out units and on six control units, with the same scores on the same units.

The tables and the controls are the results. Rectina m4 scores above Reader v3 on 6 of 8 of the held-out units (median gain +0.0065), on the six controls on 4 of 6 (median +0.0008) and on the four with organisers’ labels on 2 of 4 (median - 0.0002). Against Reader v2 the counts of Rectina m4 are 6 of 8 on the held-out units, 5 of 6 on the controls and 3 of 4 on the four controls with organisers’ labels. Descriptively, over all fourteen units, Rectina m4 scores above Reader v3 on 10 of 14 with a median difference of +0.0049, and Rectina m3 scores above Reader v2 on 9 of 14 with a median difference of +0.0089; against Reader v3 the count of Rectina m3 is 6 of 14, with a median difference of -0.0077.

Not claimed: a new architecture (the model is the one of villa), a result on any scroll beyond the fourteen units, a calibrated probability, or a difference between two recipes. Each checkpoint comes from one training seed, no test is corrected for multiple comparisons and none is run in this article, and the scores of different readers are not calibrated against each other.

## II. Starting point

The starting point is the ink detection code of the villa repository, at the main branch (commit 7e6b82164) with one patch of 3 files (24 insertions and 4 deletions) that adds the revisit cap to the sampler, a weighted draw of the patches whose power is the key physical_weight_power of the fixed scroll prior, and that masks and clips the two gamma calls of the default ink preset. The settings of every stage are listed in appendix A. The readers against which we compare are the published Reader v2 and Reader v3.

## III. Surfaces and renders

The models read a stack of 17 depth layers of the scroll volume and return one probability for every pixel of the surface of the stack. The surfaces of the 87 training segments were rendered again with the main renderer of villa, with bicubic interpolation: 63 of them had been rendered with villa

already, and 24 were rendered anew because the earlier binary was about 1.5 voxels of level 0 off at level 2. The units used to score the models are cut from the volumes on windows that were fixed from the labels before any map existed.1 The eight held-out units are read on the new renders of the training volumes, and the six controls on volumes rendered again with the current binary.

IV. Labels and validation The training labels are the labels of the earlier build, unchanged: 87 segments from 8 scrolls. According to the label source column of the manifest of the set, 59 of them carry the shift corrections made in the label shift study of October (42 by the exact placement on the main scroll, 9 by the exact placement on 0009B, 6 by an exact placement with a residual and 2 by native placement), and 28 use the published labels. The fourteen units used to score the models here were kept out of every training set of these models and were not realigned: the offset census of their labels classed all of them at low confidence, so none was moved.2 Validation uses the 3 validation masks of the label set, with 32 batches per evaluation, and the checkpoint of each stage is its last step, not selected on the validation set.

A model free measurement on the unit w00, made from the meshes of the organisers, placed its stored label between 7.06 and 7.44 pixels from the mesh placement, the value depending on the convention. Shifting the label to the mesh placement (7.06 pixels in rows and columns) changed the AUC of w00 by +0.0022 for Rectina m4, +0.0010 for Rectina m3 and - 0.0006 for Reader v3, and shifting it to the offset found by the census of the models (2.01 pixels in rows and 8.63 in columns) changed it by +0.0040, +0.0031 and +0.0024 in the same order. These changes are far below the differences interpreted in this article, and the training labels were left as they were.

The placement of the training labels was checked on a sample of segments. Of the 87 segments, 13 can be checked at all (8 with published labels and 5 with corrected labels), because the organisers publish no raw label raster for the others; the sample held 11 segments. The declared strict estimator classed 11 of the 11 as unknown, because the labelled area of the organisers is too sparse for it. A second estimator, a Dice scan inside the organisers’ labelled area declared after the first result, found the stored labels of the corrected segments at the placement of the meshes, the largest displacement being 0.735 pixels, and classed 2 of them as aligned. For the segments with published labels the check gives no answer, so that whether those labels are shifted is not established here.

The scan data were obtained from the Vesuvius Challenge data server (dl.ash2txt.org) under the data licence of the Vesuvius Challenge (LICENSE.txt).

V. Training recipe The recipe is given as the stages in which the models were trained and the setting of each stage. A setting that is not

1Windows: the windows table of the bench, fixed before any map existed; the table of the units is units.csv of the study.

2The eight held-out units are the validation-only units of the windows table of the bench, listed in the file units.csv of the study.

repeated in a stage is the one of the stage before it. Stages s1, ft116k and s2 give Rectina m3; stages s3 and s4 follow it, starting from the weights of the end of s2, and give Rectina m4. Each value was read by a tool from the configuration file that was used, and the table of appendix A gives the source of each value.

Stage s1 trains for 78125 iterations with a batch of 64 patches per step drawn from 8 scrolls by the quotas of the fixed scroll prior, patches of 17 planes by 128 by 128 pixels, a learning rate of 0.01 and a warmup of 1000 steps. Stage ft116k continues from the weights of s1 for 12000 iterations, and stage s2 from the weights of ft116k for 40000 iterations, with the same patch size and batch. Stage s3 continues for 30000 iterations on patches of 256 pixels with a batch of 10 and a learning rate of 0.003, and stage s4 for 20000 iterations on patches of 384 pixels with the same batch and learning rate. Settings common to the stages: optimizer SGD, mixed precision, seed 42, weight decay 3e-05, label smoothing of the binary cross entropy of 0.5, 32 validation batches per evaluation, and a revisit cap of 0.5 in all stages. The training patches carry a masked, clipped gamma augmentation and the sampler a revisit cap, the two changes of the patch of section II.

## VI. Measurement

The maps of every model were produced on graphics processors of remote machines, and the scores were computed on CPU from those maps; no read of any model on CPU enters a table. Each model reads every unit with 7 starts of 17 consecutive planes of the stack.

During this work comparisons were run against other published readers. This article reports the comparison of Rectina m3 and Rectina m4 with Reader v2, the earlier published reader, and with Reader v3, the published reader of the project.

We score every reader with the area under the ROC curve of its ink probability against the organiser mask of the unit, taken on the window of the unit that was fixed from the labels before any map existed. The eight held-out units fall in two energy blocks: 6 units scanned at 116 keV and 2 units scanned at 113 keV.3 Each of the tables in the sections that follow gives for all fourteen units, in three blocks, three measures of the two readers it compares (the AUC, the AUC on thin strokes and false ink at 80 per cent recall) and, under the units, the mean and the median of each measure. For every stage the checkpoint is the last step of the stage (ckpt_040000 for Rectina m3 and ckpt_020000 for Rectina m4, as named in the manifests of the release packages), and no checkpoint was selected on the validation set; the paired differences of this article are descriptive, not confirmatory, and no test is run.

## VII. Results for Rectina m3 against Reader v2 and Reader

Rectina m3 is the checkpoint at the end of stage s2 of the chain (stages s1, ft116k and s2). Table I gives for all fourteen units, in three blocks, three measures of Reader v3 and Rectina

3Energy blocks: the volume named in the file units.csv of the study, whose name carries the energy.

m3 (the AUC, the AUC on thin strokes and false ink at 80 per cent recall) and, under the units, the mean and the median of each measure over the fourteen units; Table II gives the same for Reader v2 and Rectina m3. The text below gives, for the eight held-out units, the mean, the median and the number of units on which Rectina m3 scores above each reader in AUC.

Over the eight held-out units the mean score is 0.8547 for Reader v3, 0.8421 for Reader v2 and 0.8532 for Rectina m3, and the medians are 0.8503, 0.8435 and 0.8569. Rectina m3 scores above Reader v3 on 4 of 8 units, the median difference is -0.0033 and the mean difference is -0.0015; against Reader v2 it scores above on 6 of 8 units, with a median difference of +0.0115 and a mean difference of +0.0111. In the 116 keV block (6 units) the count above Reader v3 is 4 and above Reader v2 it is 4, and in the 113 keV block (2 units) the counts are 0 and 2.

Over all fourteen units Rectina m3 is above Reader on 6 14, the mean difference is -0.0047 and difference is -0.0077; units where it is below Reader v3 are 0343, 0841 w00, 1447 w058, 1447 w060, 0009B·125754, 0009B·140325, 0500P2·055229, 0500P2·055230. Against Reader v2 it is above on 9 of 14, the mean difference is +0.0072 and the median difference is +0.0089; the units where it is below Reader v2 are 0343, 0841 w00, 1447 w058, 0009B·140325, 0343P·233748-0.

On the thin strokes the mean AUC over the fourteen units is 0.8595 for Reader v2, 0.8706 for Reader v3 and 0.8666 for Rectina m3. At the threshold that marks 80 per cent of the ink pixels of each unit, Rectina m3 marks less blank papyrus as ink than Reader v3 on 6 of 14 units (mean share 0.2525 against 0.2458, median 0.2510 against 0.2673) and less than Reader v2 on 11 of 14 (mean share of Reader v2 0.2704). The false ink at 90 per cent recall and the share of blank pixels lit are in Table VI of appendix B.

Rectina m3 was trained once, with seed 42, and no repeat of the training exists, so that the spread between two runs of the same configuration is not measured here. The comparison is between single runs, and the differences above concern these checkpoints and not the recipe.

### A. The controls

The control units were scored on the whole box of the unit, against the raw organiser labels, with the same scorer.4 The overlap check of the eight held-out units, which compares their identifiers with the names of the 87 training segments, finds 0 of them there; the six controls were not checked again for this work, and the check of the earlier Rectina article, which compares the keys of the segments and not neighbouring areas of one volume, was not repeated. Four of the controls carry the labels of the organisers: ag1, ag2 and w00, drawn by hand by the organisers, and 0343, whose labels are the mask of the approved letters, which we know through the image of the announcement. The other two, w058 and w060, carry labels made by members of the community; the header of their block in Table I says that they are information only, which means that

4Control windows: the windows table of the bench, rows of kind control, scorer thmb7 on the raw organiser labels, whole box.

their labels are not those of the organisers and that they stay out of the sentence below, while they are counted in the Mean and Median rows of the tables. The eight held-out units are different in kind: they are segments of scrolls that were used in training, and the header of their block calls them held-out segments of training scrolls with our validation labels. The six control volumes were rendered again with the current binary for the reads of the new checkpoints, while the controls of Reader v2 and Reader v3 were read on earlier renders, so the two sides of the control comparison do not share the same input.

On the six control units Rectina m3 scores above Reader v3 on 2 of 6 with a median difference of -0.0077, and above Reader v2 on 3 of 6 with a median difference of -0.0022. On the four controls with organisers’ labels (ag1, ag2, w00, 0343), a subset of the six, the split following from who made the labels of each unit, a fact about the data and not a choice made on the scores (both counts are given because the split was not fixed before the scores), the mean score is 0.8736 for Reader v3, 0.8596 for Reader v2 and 0.8639 for Rectina m3, and the medians are 0.8784, 0.8588 and 0.8628. Rectina m3 scores above Reader v3 on 2 of 4 of these units, the median difference is -0.0074 and the mean difference is -0.0097; against Reader v2 it scores above on 2 of 4, with a median difference of +0.0040 and a mean difference of +0.0043.

## VIII. Results for Rectina m4 against Reader v2 and Reader

Rectina m4 is the checkpoint at the end of stage s4, reached from the weights of Rectina m3 through the stages s3 and s4. Table III gives for all fourteen units, in three blocks, three measures of Reader v3 and Rectina m4 (the AUC, the AUC on thin strokes and false ink at 80 per cent recall) and, under the units, the mean and the median of each measure over the fourteen units; Table IV gives the same for Reader v2 and Rectina m4. The text below gives, for the eight held-out units, the mean, the median and the number of units on which Rectina m4 scores above each reader in AUC.

Over the eight held-out units the mean score is 0.8547 for Reader v3, 0.8421 for Reader v2 and 0.8637 for Rectina m4, and the medians are 0.8503, 0.8435 and 0.8621. Rectina m4 scores above Reader v3 on 6 of 8 units, the median difference is +0.0065 and the mean difference is +0.0090; against Reader v2 it scores above on 6 of 8 units, with a median difference of +0.0249 and a mean difference of +0.0216. In the 116 keV block (6 units) the count above Reader v3 is 5 and above Reader v2 it is 4, and in the 113 keV block (2 units) the counts are 1 and 2.

Over all fourteen units Rectina m4 is above Reader v3 on 10 of 14, the mean difference is +0.0056 and the median difference is +0.0049; the units where it is below Reader v3 are 0343, 0841 ag2, 0009B·140325, 0500P2·055229. Against Reader v2 it is above on 11 of 14, the mean difference is +0.0175 and the median difference is +0.0159; the units where it is below Reader v2 are 0841 ag2, 0009B·172639, 0343P·233748-0. On the thin strokes the mean AUC over the fourteen units is 0.8595 for Reader v2, 0.8706 for Reader v3 and 0.8764 for

**Fig. 1.** Control unit 0343. Left, Reader v3 (AUC 0.9078); centre, Rectina m3 (AUC 0.8911); right, the red difference between the two maps. Each map is stretched between its own percentiles, the panels are shown at the full resolution of the file.

**Fig. 2.** Control unit 0841 ag1. Left, Reader v3 (AUC 0.8513); centre, Rectina m3 (AUC 0.8532); right, the red difference between the two maps. Each map is stretched between its own percentiles, the panels are shown at the full resolution of the file.

**Fig. 3.** Control unit 0841 ag2. Left, Reader v3 (AUC 0.8297); centre, Rectina m3 (AUC 0.8390); right, the red difference between the two maps. Each map is stretched between its own percentiles, the panels are shown at the full resolution of the file.

**Fig. 4.** Control unit 0841 w00. Left, Reader v3 (AUC 0.9055); centre, Rectina m3 (AUC 0.8723); right, the red difference between the two maps. Each map is stretched between its own percentiles, the panels are shown at the full resolution of the file.

**Fig. 5.** Control unit 1447 w058. Left, Reader v3 (AUC 0.8610); centre, Rectina m3 (AUC 0.8520); right, the red difference between the two maps. Each

**TABLE I** Three measures of Rectina m3 against Reader v3 on the fourteen units: the AUC, the AUC on thin strokes and false ink at 80 per cent recall. The cell of

Rectina m3 gives in parentheses the signed difference against Reader v3. The rows Mean and Median are taken over all fourteen units; the block of the

community labels is information only.

AUC on thin strokes: the rank AUC of the central 80 per cent of each stroke against blank pixels at least 207 um from any label, the band between not false ink at 80 per cent recall: the share of blank pixels marked as ink at the threshold that recalls 80 per cent of the ink pixels, where less is better. For the controls the AUC is taken against the far negatives of the bench; for the held-out units against all blank pixels of the validation mask. The better value of each pair in bold; a green triangle pointing up before Rectina m3 where it is better, a red triangle pointing down where it is worse.

**Fig. 6.** Control unit 1447 w060. Left, Reader v3 (AUC 0.7842); centre, Rectina m3 (AUC 0.7777); right, the red difference between the two maps. Each

Rectina m4. At the threshold that marks 80 per cent of the ink pixels of each unit, Rectina m4 marks less blank papyrus as ink than Reader v3 on 10 of 14 units (mean share 0.2315 against 0.2458, median 0.2425 against 0.2673) and less than Reader v2 on 11 of 14 (mean share of Reader v2 0.2704). The false ink at 90 per cent recall and the share of blank pixels lit are in Table VI of appendix B.

Rectina m4 was trained once, with seed 42, and no repeat of the training exists, so that the spread between two runs of the

same configuration is not measured here. The comparison is between single runs, and the differences above concern these checkpoints and not the recipe.

### A. The controls

The control units were scored on the whole box of the unit, against the raw organiser labels, with the same scorer.5 The

5Control windows: the windows table of the bench, rows of kind control, scorer thmb7 on the raw organiser labels, whole box.

**TABLE II** Three measures of Rectina m3 against Reader v2 on the fourteen units, in the format of Table I. The cell of Rectina m3 gives in parentheses the signed

difference against Reader v2. The rows Mean and Median are taken over all fourteen units; the block of the community labels is information only.

0.7777 (+0.0000)

AUC on thin strokes: the rank AUC of the central 80 per cent of each stroke against blank pixels at least 207 um from any label, the band between not false ink at 80 per cent recall: the share of blank pixels marked as ink at the threshold that recalls 80 per cent of the ink pixels, where less is better. For the controls the AUC is taken against the far negatives of the bench; for the held-out units against all blank pixels of the validation mask. The better value of each pair in bold; a green triangle pointing up before Rectina m3 where it is better, a red triangle pointing down where it is worse.

overlap check of the eight held-out units, which compares their identifiers with the names of the 87 training segments, finds 0 of them there; the six controls were not checked again for this work, and the check of the earlier Rectina article, which compares the keys of the segments and not neighbouring areas of one volume, was not repeated. Four of the controls carry the labels of the organisers: ag1, ag2 and w00, drawn by hand by the organisers, and 0343, whose labels are the mask of the approved letters, which we know through the image of the announcement. The other two, w058 and w060, carry labels made by members of the community; the header of their block in Table III says that they are information only, which means that their labels are not those of the organisers and that they stay out of the sentence below, while they are counted in the Mean and Median rows of the tables. The eight held-out units are different in kind: they are segments of scrolls that were used in training, and the header of their block calls them heldout segments of training scrolls with our validation labels. The six control volumes were rendered again with the current binary for the reads of the new checkpoints, while the controls of Reader v2 and Reader v3 were read on earlier renders, so the two sides of the control comparison do not share the same input.

On the six control units Rectina m4 scores above Reader v3 on 4 of 6 with a median difference of +0.0008, and above Reader v2 on 5 of 6 with a median difference of +0.0115. On the four controls with organisers’ labels (ag1, ag2, w00, 0343), a subset of the six, the split following from who made the

labels of each unit, a fact about the data and not a choice made on the scores (both counts are given because the split was not fixed before the scores), the mean score is 0.8736 for Reader v3, 0.8596 for Reader v2 and 0.8735 for Rectina m4, and the medians are 0.8784, 0.8588 and 0.8831. Rectina m4 scores above Reader v3 on 2 of 4 of these units, the median difference is -0.0002 and the mean difference is -0.0001; against Reader v2 it scores above on 3 of 4, with a median difference of +0.0148 and a mean difference of +0.0139.

## IX. Usage

The checkpoints are released with model cards in the model repository [1], Rectina m3 in the folder m3 and Rectina m4 in the folder m4. They are read with the reader of the earlier Rectina article [2], which reads 17 consecutive planes of the stack of a surface and slides a square patch over rows and columns; the patch is 128 pixels for Rectina m3 and 384 pixels for Rectina m4, the crop size of the last stage of each. The reads of this article used 7 starts of 17 planes for Rectina m3 and 7 for Rectina m4, on graphics processors. Not tested for these checkpoints: the public reader of the earlier article, reads on CPU, other renders of the same surfaces as input, and scales other than the 9 um class of the training data.

## X. Limits

The score is our own metric, the area under the curve of a probability map against a mask, and it is not the metric of any

**Fig. 7.** Control unit 0343. Left, Reader v3 (AUC 0.9078); centre, Rectina m4 (AUC 0.9064); right, the red difference between the two maps. Each map is stretched between its own percentiles, the panels are shown at the full resolution of the file.

**Fig. 8.** Control unit 0841 ag1. Left, Reader v3 (AUC 0.8513); centre, Rectina m4 (AUC 0.8598); right, the red difference between the two maps. Each map is stretched between its own percentiles, the panels are shown at the full resolution of the file.

**Fig. 9.** Control unit 0841 ag2. Left, Reader v3 (AUC 0.8297); centre, Rectina m4 (AUC 0.8214); right, the red difference between the two maps. Each map is stretched between its own percentiles, the panels are shown at the full resolution of the file.

**Fig. 10.** Control unit 0841 w00. Left, Reader v3 (AUC 0.9055); centre, Rectina m4 (AUC 0.9064); right, the red difference between the two maps. Each

**Fig. 11.** Control unit 1447 w058. Left, Reader v3 (AUC 0.8610); centre, Rectina m4 (AUC 0.8616); right, the red difference between the two maps. Each

**TABLE III** Three measures of Rectina m4 against Reader v3 on the fourteen units: the AUC, the AUC on thin strokes and false ink at 80 per cent recall. The cell of

Rectina m4 gives in parentheses the signed difference against Reader v3. The rows Mean and Median are taken over all fourteen units; the block of the

community labels is information only.

AUC on thin strokes: the rank AUC of the central 80 per cent of each stroke against blank pixels at least 207 um from any label, the band between not false ink at 80 per cent recall: the share of blank pixels marked as ink at the threshold that recalls 80 per cent of the ink pixels, where less is better. For the controls the AUC is taken against the far negatives of the bench; for the held-out units against all blank pixels of the validation mask. The better value of each pair in bold; a green triangle pointing up before Rectina m4 where it is better, a red triangle pointing down where it is worse.

**Fig. 12.** Control unit 1447 w060. Left, Reader v3 (AUC 0.7842); centre, Rectina m4 (AUC 0.7900); right, the red difference between the two maps. Each

contest. On the held-out units it is computed on one window per unit, and the choice of the window changes it; on the control units it is computed on the whole box. The labels of the controls are of three kinds that should not be mixed in a reading: human labels of the organisers for ag1, ag2 and w00, the mask of the approved letters for 0343, which we know only through the announcement image and therefore only as that image shows it, and labels of the community for w058 and w060. None of them is a reference of the same standing as the

others. The 113 keV block holds two units of a single scroll scanned at another energy than the other six, so its counts are small and support no statement about energy.

Each checkpoint was trained once, and no repeat of the training exists, so that the spread between two runs of the same configuration is not measured here. The noise that was measured is the noise of one validation balanced accuracy evaluation on the earlier chain that used the stages s3 and s4: a standard deviation of 0.01346 at s3 and 0.01298 at s4,

**TABLE IV** Three measures of Rectina m4 against Reader v2 on the fourteen units, in the format of Table III. The cell of Rectina m4 gives in parentheses the signed

difference against Reader v2. The rows Mean and Median are taken over all fourteen units; the block of the community labels is information only.

0.8383 (-0.0000) AUC on thin strokes: the rank AUC of the central 80 per cent of each stroke against blank pixels at least 207 um from any label, the band between not false ink at 80 per cent recall: the share of blank pixels marked as ink at the threshold that recalls 80 per cent of the ink pixels, where less is better. For the controls the AUC is taken against the far negatives of the bench; for the held-out units against all blank pixels of the validation mask. The better value of each pair in bold; a green triangle pointing up before Rectina m4 where it is better, a red triangle pointing down where it is worse.

about 0.013. It is not an AUC noise, and the AUC noise of the means over the fourteen units was not measured, so differences of a few thousandths in AUC must not be read as a result and no ranking of models is drawn from them.6

The chain of this article differs from the chain of Rectina m1 and m2 in several things at once (the renders, the revisit cap, the masked gamma, the version of the training code and a fresh s1), so no change in the numbers can be attributed to a single cause. The control volumes of the new checkpoints were rendered again with the current binary, while Reader v2 and Reader v3 were read on earlier renders, so the two sides of the control comparison do not share the same input; the unit 0343 differs from its old render for a cause that was not proven.

The training labels were not realigned in this build. The sample check of the placement covers 11 of 87 segments, and only 13 of them can be checked at all; for the 28 segments with published labels the check gives no answer, and the corrected labels are confirmed where they can be measured. Nothing is known from this sample about the scrolls whose raw labels the organisers do not publish. The sources of the label set and the rule that turned them into masks are not recorded in a pinned file of this work.

Two further models, M7 and M8, were trained with windows recentred on the surface and are not part of the check-

6Source: file c- v a l - n o i s e . c sv study, column ba_single_eval_sd_est, taken on the chain that trained the earlier checkpoints with the same stages.

points of this article. On the 7 held-out units that the first was read on, its mean AUC is 0.8548 against 0.8554 for Rectina m3, and on the 7 units read for the second its mean AUC is 0.8513 against 0.8673 for Rectina m4: the recentred windows gave no gain.

Combinations of the readers were also scored (appendix B). They are descriptive: over the 19 combinations that include Rectina m4, the largest mean AUC gain against Rectina m4 alone is +0.0039, and the number of units above Rectina m4 stays between 2 and 12 of fourteen, so that no combination is claimed to be better than Rectina m4 alone.

## XI. Release

Rectina m3 is the checkpoint of the last step of stage s2 (ckpt_040000) and Rectina m4 the checkpoint of the last step of stage s4 (ckpt_020000). The models are published in the repository evilaliv3/rectina on Hugging Face, Rectina m3 in the folder m3 and Rectina m4 in the folder m4, with their model cards; the earlier checkpoints m1 and m2 stay in their folders. The weights and the model cards are released under CC BY-NC 4.0 for non-commercial research use with attribution, and the code of the recipe under MIT. This article makes no claim beyond the model cards. Data terms: the data of the Vesuvius Challenge are subject to its data licence (dl.ash2txt.org LICENSE.txt). The figure panels show the human ink labels of the evaluation units only through the maps they are compared with, and the model maps, with attribution to their authors; they are published on the author’s

own responsibility as figures of this work. No panel shows the surface texture of any scroll, and no figure shows PHerc0826; the figures of the unit group 1447 are maps of the same two control units that the earlier Rectina article showed. This article and its folder hold no data volumes and no label files.

Appendix A The recipe table

step setting value source s1 iterations stage configuration s1.json s1 batch size stage configuration s1.json s1 patch size (z, y, x) [17, 128, 128] stage configuration s1.json s1 learning rate stage configuration s1.json s1 warmup steps stage configuration s1.json s1 validation every stage configuration s1.json s1 checkpoint saved every stage configuration s1.json s1 start random weights stage configuration; declaration s1 per-scroll quotas of the batch "0009B": 8, "0139": 12, "0172": 11, "0343P": 5, "0500P2": 7, "0814": 7, "1667": 8, "Paris4": 6

stage configuration s1.json

ft116k iterations stage configuration ft116k.json ft116k batch size stage configuration ft116k.json ft116k patch size (z, y, x) [17, 128, 128] stage configuration ft116k.json ft116k learning rate stage configuration ft116k.json ft116k warmup steps stage configuration ft116k.json ft116k validation every stage configuration ft116k.json ft116k checkpoint saved every stage configuration ft116k.json ft116k start weights of s1 (weights only) stage configuration; declaration ft116k per-scroll quotas of the batch "0009B": 18, "0139": 20, "0814": 2, "1667": 16, "Paris4": 8

stage configuration ft116k.json

s2 iterations stage configuration s2.json s2 batch size stage configuration s2.json s2 patch size (z, y, x) [17, 128, 128] stage configuration s2.json s2 learning rate stage configuration s2.json s2 warmup steps stage configuration s2.json s2 validation every stage configuration s2.json s2 checkpoint saved every stage configuration s2.json s2 start weights of ft116k (weights only) stage configuration; declaration s2 per-scroll quotas of the batch "0009B": 8, "0139": 12, "0172": 11, "0343P": 5, "0500P2": 7, "0814": 7, "1667": 8, "Paris4": 6

stage configuration s2.json

s3 iterations stage configuration s3.json s3 batch size stage configuration s3.json s3 patch size (z, y, x) [17, 256, 256] stage configuration s3.json s3 learning rate stage configuration s3.json s3 warmup steps stage configuration s3.json s3 validation every stage configuration s3.json s3 checkpoint saved every stage configuration s3.json s3 start weights of s2 (weights only) stage configuration; declaration s4 iterations stage configuration s4.json s4 batch size stage configuration s4.json s4 patch size (z, y, x) [17, 384, 384] stage configuration s4.json s4 learning rate stage configuration s4.json s4 warmup steps stage configuration s4.json s4 validation every stage configuration s4.json s4 checkpoint saved every stage configuration s4.json s4 start weights of s3 (weights only) stage configuration; declaration s3 and s4 per-scroll quota of the batch (ratio scale)

"0009B": 1, "0139": 3, "0172": 1, "0343P": 1, "0500P2": 1, "0814": 1, "1667": 1, "Paris4": 1

stage configuration s3.json

all stages revisit cap (physical weight power of the fixed scroll prior)

stage configuration; patch

all stages optimizer sgd stage configuration all stages scheduler diffusers_cosine_warmup stage configuration all stages weight decay 3e-05 stage configuration all stages mixed precision fp16 stage configuration all stages seed stage configuration all stages validation batches per evaluation stage configuration all stages label smoothing of the BCE loss stage configuration all stages augmentation preset default stage configuration all stages training code villa main, commit 7e6b82164, plus a patch of 3 files (24 insertions, 4 deletions)

declaration; patch file

all stages patch sha256, first 12 hex c5622564771a patch hash file all stages renders of the training segments bicubic, villa main renderer; 87 segments label set manifest release checkpoint released as Rectina m3 ckpt_040000 (last step of s2) release package manifest release checkpoint released as Rectina m4 ckpt_020000 (last step of s4) release package manifest

Appendix B Further measures and combinations

**Table VI** gives the mean over the fourteen units of the five measures of the four models, including the false ink at 90 per cent recall and the share of blank pixels lit that the sections of results leave out.

**Table VII** gives, for the combinations of Rectina m3 and Rectina m4 with the readers, the mean over the fourteen units of the AUC, of the false ink at 90 per cent recall and of the share lit, the mean paired difference in AUC against Rectina m4 alone and against Reader v3, and the number of units on which the combination scores a higher AUC than that reference. A combination is the weighted mean of the maps of its members, the weights being written in the first column (m3 and m4 are Rectina m3 and Rectina m4, v2 and v3 the readers). The combinations are exploratory, and they were not chosen to be reported.

Appendix C Triptychs of the held-out units

Each figure shows one held-out unit as three panels side by side: Reader v3, the model and the red difference of the two maps. The panels are the files of full resolution, shown reduced on the page and enlarged without loss in the file. Figures 13 to 20 are Rectina m3 and the figures after them Rectina m4.

Appendix D

Provenance

Every number of the text is read from a table written by a tool. The scores of Rectina m3 and Rectina m4 against Reader v2 and Reader v3 are read from the files of scores of the pairs of the study, control-units.csv (sha256 beginning 7057d8bf53c2) and heldout- units.csv (sha256 beginning 040c511f603e), columns auc, thin80_core_auc, fa80, fa90 and lit_blank. The settings of the recipe are read from the five stage configuration files (digest of the five beginning 26b809aa0554) and the patch from m5m6-training.patch (sha256 beginning c5622564771a); the label sources from the manifest of the set; the check of the placement of the labels from offsets.csv and inventory.csv of the sample check; the offset of w00 from the files of the label offset study and its AUC scan; the noise statement from c-val-noise.csv. In the study the checkpoint of Rectina m3 was called M5 and that of Rectina m4 M6; the names appear only in paths. The short codes of the held-out units in the tables stand for the following unit identifiers: 0009B·172639 is 20250510172639; is 20250919125754; is 20250919133208; is 20250919140325; is 20250716055229; is 20250716055230; is 20250904233748- 0_b2; 0343P·172054-1 is 20250905172054-1_b2. A checker recomputes every macro of numbers.tex from these files and compares it with its value.
