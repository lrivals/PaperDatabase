---
id: arxiv-2303.06999-identifying-label-errors-object-detection
title: "Identifying Label Errors in Object Detection Datasets by Loss Inspection"
year: 2023
backend: grobid
---

## Abstract

Labeling datasets for supervised object detection is a dull and time-consuming task. Errors can be easily introduced during annotation and overlooked during review, yielding inaccurate benchmarks and performance degradation of deep neural networks trained on noisy labels. In this work, we introduce a benchmark for label error detection methods on object detection datasets as well as a theoretically underpinned label error detection method and a number of baselines. We simulate four different types of randomly introduced label errors on train and test sets of well-labeled object detection datasets. For our label error detection method we assume a two-stage object detector to be given and consider the sum of both stages' classification and regression losses. The losses are computed with respect to the predictions and the noisy labels including simulated label errors, aiming at detecting the latter. We compare our method to four baselines: a naive one without deep learning, the object detector's score, the entropy of the classification softmax distribution and a probability margin based method from related work. We outperform all baselines and demonstrate that among the considered methods, ours is the only one that detects label errors of all four types efficiently, which we also derive theoretically. Furthermore, we detect real label errors a) on commonly used test datasets in object detection and b) on a proprietary dataset. In both cases we achieve low false positives rates, i.e., we detect label errors with a precision for a) of up to 71.5% and for b) with 97%. Figure 1. Example image from the Pascal VOC 2007 test dataset with two labeled boats marked by the blue boxes and multiple unlabeled boats.

## 1. Introduction

Nowadays, the predominant paradigm in computer vision is to learn models from data. The performance of the model largely depends on the amount of data and its quality, i.e. the diversity of input images and label accuracy [10,17,18,21,23]. Deep neural networks (DNNs) are particularly data hungry [34]. In this work, we focus on the case of object detection where multiple objects per scene belonging to a fixed set of classes are annotated via bounding boxes [9,30].

In many industrial and scientific applications, the labeling process consists of an iterative cycle of data acquisition, labeling, quality assessment, and model training. Labeling data is costly, time consuming and error prone, e.g. due to inconsistencies caused by multiple human labelers or a change in label policy over time. Therefore, at least a partial automation of the label process is desirable. One research direction that aims at this goal is automated label error de-tection [8,27,32]. The extent to which noisy labels affect the model performance is studied by [1,38]. Wu et al. [38] observe that the model is able to tolerate a certain amount of missing annotations in training data without losing too much performance on Pascal VOC and Open Images V3 test sets. In contrast, Buttner et al. [1] show that inaccurate labels in terms of annotations size in training data yields to significant decrease of test performance for calculus detection on bitewing radiographs. Other methods model label uncertainty [26,31] or improve robustness w.r.t. noisy labels [2,11,24,43].

Up to now, automated detection of label errors has received less attention. There exist some works on image classification datasets [27,28,35], one work on semantic segmentation datasets [32] and some works for object detection [16,22]. Label errors may affect generalization performance, which makes their detection desirable [28]. Furthermore, there is business interest in improving and accelerating the review process by partial automation.

Here, we study the task of label error detection in object detection datasets by a) introducing a benchmark and b) developing a detection method and compare it against four baselines. We introduce a benchmark by simulating label errors on the BDD100k [41] and EMNIST-Det [30] dataset. The latter is a semi-synthetic dataset consisting of EMNIST letters [5] pasted into COCO images [25] of which we expect to possess highly accurate labels. The types of label errors that we consider are missing labels (drops), correct localization but wrong classification (flips), correct classification but inaccurate localization (shifts), and labels that actually represent background (spawns). We address the detection of these errors by a novel method based on monitoring instance-wise object detection loss. We study the effectiveness of our method in comparison to four baselines. Then, we demonstrate for commonly used object detection test datasets, such as BDD100k [41], MS-COCO [25], Pascal VOC [9] and Kitti [12], and also for a proprietary dataset on car part detection that our method detects label errors by reviewing moderate sample sizes of 200 images per dataset. Our contributions can be summarized as follows: a) we introduce a novel method based on the instance-wise loss for detecting label errors in object detection, b) we introduce a benchmark for identifying four types of label errors on BDD100k and EMNIST-Det, and c) we apply our method to detect label errors in commonly used and proprietary object detection datasets and manually evaluate the error detection performance for moderate sample sizes.

## 2. Related Work

The influence of noisy labels in the training as well as in the test data is an active and current research topic. The labels for commonly used image classification datasets are noisy [28] and this also applies to object detection. Figure 1 shows an image from the Pascal VOC 2007 test dataset containing just two labeled boats, but clearly more can be seen.

For the task of image classification, some learning methods exist that are more robust to label noise [13-15, 19, 27, 29, 37, 40, 42]. Also the task of label error detection has been tackled in [4,28] and theoretically underpinned in [27]. Chen et al. [4] filter whole samples with noisy labels but individual label errors are not detected. Northcutt et al. present label errors in image classification datasets and study to which extent they affect benchmark results [28] followed by the introduction of the task of label error detection [27]. The latter introduces a confident learning approach, assuming that the label errors are image-independent. Then, the joint distribution between the noisy and the true labels with class-agnostic label uncertainties is estimated and utilized to find label errors. This method allows to find label errors on commonly used image classification (i.e. MNIST or ImageNet) and sentiment classification datasets (Amazon Reviews), resulting in improved model performance by re-training on cleaned training data. This line of works has been recently extended to the task of multi-label classification in [35], where a single object is shown per image but may carry multiple labels.

For object detection, Wu et al. [38] as well as Xu et al. [39] study how noisy training labels affect the model performance, observing that the model is reasonably robust when dropping labels. To counter label errors in object detection, methods that model label uncertainty [26,31] or more robust object detectors have been developed [1,11,20,24,39,43]. Buttner et al. [1] simulate label errors and introduce a co-teaching approach for more robust training with noisy training data. For the task of label error detection, Koksal et al. [22] simulate different types of label errors in video sequences. Predictions and labels of consecutive frames are compared and then manually reviewed to eliminate erroneous annotations. Hu et al. [16] introduce a probability differential method (PD) to identify and exclude annotations with wrong class labels during training.

For semantic segmentation, a benchmark is introduced by Rottmann and Reese [32] to detect missing labels. For this purpose, uncertainty estimates are used to predict for each false positive connected component whether a label error is present or not. Detection is performed by considering the discrepancy of the given (noisy) label and the corresponding uncertainty estimate.

Our work introduces the first benchmark with four types of label errors for label error detection methods on object detection datasets as well as a label error detection method (that detects all four types of label errors) and a number of baselines. The label error detection methods simulate a) different types of label errors and detect these with the help of a tracking algorithm [22] for images derived from video sequences or b) class-flips and identify these via a probability differential (PD) [16], where, however, the focus is on training. For our benchmark, we randomly simulate four types of label errors and detect them simultaneously with a new and four baseline methods, including PD. In our method, the discrepancy between the prediction or expectation of the network and the actual labels is used to find label errors. This discrepancy is determined by the classification and regression loss from the first and second stage of the detector. This allows to find not only simulated but also real label errors on commonly used object detection test datasets.

## 3. Label Error Detection

In this section we describe our label error benchmark as well as the setup and evaluation for real label errors on commonly used object detection test datasets and a proprietary dataset. We describe which datasets are used, which types of label errors are considered and the way we simulate label errors inspired by observations that we made in commonly used datasets and by related work. We then introduce our detection method as well as four additional baseline methods. This is complemented with evaluation metrics used to compare the methods with each other on our label error benchmark and the evaluation procedure for commonly used test datasets where we manually review the findings of our method for moderate sample sizes.

### 3.1. Label Error Benchmark

In the following, we distinguish between the label error benchmark and the detection of real label errors, where in the former, label errors are simulated (and therefore known) and the performance of the five different methods are evaluated automatically. In the latter case, label errors are not simulated but real and therefore automated evaluation is impossible as the real label errors are unknown. To enable a reliable evaluation, only datasets containing almost no real label errors are used for the benchmark. We observe that commonly used datasets in object detection, such as MS-COCO, Pascal VOC or Kitti, contain significant amounts of label errors, thus they are not suitable for the benchmark. Nevertheless, to demonstrate the performance of our instance-wise loss method on these datasets, a moderate sample size of 200 label error proposals are manually reviewed and counted for each dataset.

#### 3.1.1. Datasets

For our benchmark we use the semi-synthetic EMNIST-Det dataset and BDD100k, referred to as BDD. EMNIST-Det consists of 20,000 training and 2,000 test images. To have the best possible labels for BDD, we filter the training and validation split, such that we only use daytime images with clear weather conditions. This results in 12,454 training images and the validation split is split into equally-sized test and validation sets, each consisting of 882 images.

#### 3.1.2. Simulated Label Errors

We consider four different types of label errors: missing labels (drops), correct localization but wrong classification (flips), correct classification but inaccurate localization (shifts), and labels that actually represent background (spawns). Any dataset is equipped with a set of G labels, i.e. Y = {b (i) : i = 1, ..., G} where each label is a tuple b (i) = (x (i) , y (i) , w (i) , h (i) , c (i) ) containing the box center (x (i) , y (i) ), the box extent (w (i) , h (i) ) and a class index c (i) from the set of classes {1, ..., C}. Let I = {1, . . . , G} be the set of indices of all boxes b (i) ∈ Y, i = 1, . . . , G. We now describe all types of label errors applied to Y and we make the assumption that a single label is only perturbed by one type of label error instead of multiple types. We choose a parameter γ ∈ [0, 1] representing the relative frequency of label errors.

Drops For dropping labels, we randomly choose a subset

I d of I with cardinality |I d | = ⌊ γ 4 • G⌋. We drop all labels Y d = {b (i) : i ∈ I d } and denote I \d = I\I d . Analogously, Y \d = Y \ Y d .

Flips For flipping class labels, we randomly choose a subset

I f of I \d with cardinality |I f | = ⌊ γ 4 • G⌋ and copy Ỹf = Y f = {b (i) : i ∈ I f }.

Then, we randomly flip the class of every label in Ỹf to a different label. We denote

I \f = I \d \ I f and Y \f = (Y \d \ Y f ) ∪ Ỹf .

Shifts To insert shifts, we change the localization of labels. We randomly choose a subset I sh of I \f with cardinality Spawns For spawning labels, we randomly choose a subset I sp of I \sh with cardinality |I sp | = ⌊ γ 4 •G⌋ and copy Ỹsp = Y sp = {b (i) : i ∈ I sp }. Then, we assign every label b(i) ∈ Ỹsp randomly to another image. Since in our experiments all images in a dataset have the same resolution, this ensures that objects do not appear in unusual positions or outside of an image. For instance, a car in BDD is more likely to be found on the bottom part of the image rather than in the sky. We denote the set of noisy labels as Ỹ = Y \sh ∪ Ỹsp .

One example per label error type is shown in Fig. 2. Note that the number of labels G is unchanged as the number of drops and spawns is the same.

### 3.2. Baseline Methods

The four baselines that we compare our instance-wise loss method with are based on a) inspecting the labels without the use of deep learning, b) the box-wise detection score c) the classification entropy of the two-stage object detectors and d) the probability differential from [16].

Naive Baseline We introduce a naive baseline to show the significant improvement of deep learning in label error detection for object detection over manual label review. We assume that all label errors can be smoothly found by taking a single look at all existing noisy labels and the (actually unknown) drops, i.e. by performing ⌊(1 + γ 4 ) • G⌋ operations. This simplified assumption is of course unrealistic, however the corresponding results can serve as a lower bound for the effort of manual label review.

Detection Score Baseline The detection score baseline works as follows: For a given image from the set of all images of the dataset z ∈ Z, a neural network predicts a fixed number N 0 of bounding boxes for the first stage B0,z = {(x (i) , ŷ(i) , ŵ(i) , ĥ(i) , ŝ(i) 0 ) : i = 1, . . . , N 0 }, where x(i) , ŷ(i) , ŵ(i) , ĥ(i) represent the localization and ŝ(i) 0 ∈ [0, 1] the objectness score. Then, we add the boxes of the labels as proposals for the second stage to ensure that at least one prediction exists for each label, which is particularly important for the detection of spawns. For this purpose, each ground truth label from Y is assigned with a detection score of ŝ0 = 1. After adding the labels to B0,z , only those N 1 boxes that remain after classindependent non-maximum suppression (NMS) and score thresholding on ŝ0 with s ϵ ≥ 0, get into the second stage B1,z = {(x (i) , ŷ(i) , ŵ(i) , ĥ(i) , ŝ(i) 0 ) : i = 1, . . . , N 1 }. After box refinement and classification as well as NMS on the detection score ŝ(i) 2 , N 2 label error proposals remain. Here, ŝ(i)

2 is the detection score of the detection head and unlike ŝ(i) 0 , ŝ(i) 2 represents not only the presence of an object, but also takes the class probabilities of the predicted object into account. The remaining

N 2 label error proposals B2,z = {(x (i) , ŷ(i) , ŵ(i) , ĥ(i) , ŝ(i) 2 , p(i) 1 , . . . , p(i) C ) : i = 1, . . . , N2

}, are defined by the localization (x (i) , ŷ(i) , ŵ(i) , ĥ(i) ), the detection score ŝ(i) 2 and the class probabilities

p(i) 1 , . . . , p(i) C .

The predicted class is given by ĉ(i) = arg max k=1,...,C p(i) k . Score thresholding is omitted here, or the score τ used for this is equal to 0, since τ > 10 -4 would suppress most of the label error proposals that detect spawns. The detection score of these proposals is mostly very close to zero unless a second true label is nearby. After inferring each image z ∈ Z as described above, we get label error proposals for the whole dataset by z∈Z B2,z .

### Entropy Baseline

The entropy baseline follows the same procedure, only the NMS in the first and second stage are based on the respective box-wise entropy rather than the detection score.

Probability Differential Baseline For the PD baseline from Hu et al. [16], we do not add the boxes of the labels as proposals. Furthermore, score thresholding and NMS is not applied, such that every box b ∈ B0,z also remains in B2,z . After assigning every label with sufficiently overlapping predictions, the probability differential (PD) for every label b ∈ Y with class c and the m assigned predictions b(i) (i = 1, . . . , m) is defined as:

P D(b) = m i=1 1+ max k∈{1,...,C}\{c} p(i) k -p(i) c 2m

. The PD of a label is in [0, 1] and intuitively, the more the probabilities of the predictions and the class of the label differ (higher PD) the more likely a label error is present. Note that drops are always overlooked.

### 3.3. Instance-wise Loss Method

Our method to detect the introduced label error types (Sec. 3.1) is based on an instance-wise loss for two-stage object detectors. The NMS is no longer based on the detection score or the entropy, but on the box-wise loss of the respective stage. Every prediction b0 ∈ B0,z is assigned with a region proposal loss (L RPN ), which is the sum of a classification (binary cross-entropy) and regression (smooth-L1) loss for the labels and the prediction itself. The computation of the loss is identical to the one in training. Since not all labels are associated with a proposal after the first stage, i.e. the model may predict only background near a label, we add the labels themselves to the set of label error proposals. After box refinement and classification, every box b1 ∈ B1,z is assigned with a region of interest loss (L ROI ), which is the sum of a classification (cross entropy) and regression (smooth-L1) loss for the labels and the prediction itself. Then L RPN and L ROI are summed up to obtain an instance-wise loss score. A sketch of our method is shown in Fig. 3. We can find the dropped blue label for "N" since the predictions near the object should have a high detection score, resulting in a high first stage classification loss. The spawned red label is assigned with a high classification loss from the first and second stage, since the assigned predictions should have a score close to zero in the first stage and an almost uniform class distribution in the second stage. Whether the yellow label is a flip is irrelevant for the first stage, since the loss should be small either way. If the box is classified correctly according to the associated label, there is a large classification loss for a flip and a small one otherwise. The shifts are addressed by the first and second stage regression loss.

The intuition behind our method is that a sufficiently well-specified and fitted model has small expected loss on data sampled during training. Sufficient data sampling and moderate label error rates lead to label errors giving rise to outlier losses which are identified as proposals. We show that our method separates correct from incorrect labels for a classification model p trained with the cross entropy loss ℓ CE . C (1 -2κ), we obtain strict separation of the loss function

ℓ CE ( p(x)∥f (x)) < -log(1 -p F -κ) < -log(κ + pF C-1 ) < ℓ CE ( p(x)∥ y)(1)

for any incorrect label y ̸ = f (x) with probability 1 -δ over chosen training data and with probability 1 -2ε κ 2 over the choice of x.

We include a proof of this statement in the supplementary material. The PAC-learnability assumption [33] yields rigorous bounds for the deviation of the model p from the label distribution p which contains label flips. Conditioned to the events of drawing correct versus drawing incorrect labels, these bounds carry over to the cross entropy. These bounds separate the two events with certain probability given in the statement above.

### 3.4. Evaluation Metrics

Ignoring that natural label errors exist in EMNIST-Det and BDD, we benchmark the five methods introduced in above by means of our label error simulation. To this end, we take the label error proposals of the respective method and the set of original labels Y and decide for every proposal whether it is a label error, which corresponds to a true positive (TP l ), or no label error, which corresponds to a false positive (FP l ). Label errors that are not detected are called false negatives (FN l ). A proposal of a label error detector is a TP l if the IoU between the proposal under consideration and a noisy label on the image is greater or equal to a threshold 1 ≥ α > 0.

Here, the noisy label categorizes what type of label error is detected by the proposal. If the IoU is less than α, the proposal is a FP l . After determining this for each proposal from the dataset, the area under the receiver operator characteristic curve (AUROC , see [6]) and F 1 values, which is the harmonic mean of precision and recall (see [7]), is calculated according to the decision between TP l and FP l . F 1 values are determined with thresholding on the score of the respective method (loss/detection score/entropy/PD). We always choose the optimal threshold, i.e. the threshold at which the F 1 value is maximized (max F 1 ). Note, since the naive baseline considers images and thus label error proposals in random order, the associated AUROC values are always 0.5.

### 3.5. Detection of Real Label Errors

For commonly used datasets we proceed as follows. We consider for each dataset 200 proposals of our method with highest loss and manually flag them as TP l or FP l , based on the label policy corresponding to the given dataset. Note that we can still compute precision values but we are not able to determine AUROC or max F 1 values as the number of total label errors is unknown. Since several label errors can be detected with one proposal, precision describes the ratio of proposals with at least one label error and the total number of proposals considered, i.e. 200.

## 4. Numerical Results

In this section we study label error detection performance on our label error benchmark as well as for real label errors in

### 4.1. Implementation Details

We implemented our benchmark and methods in the open source MMDetection toolbox [3]. Our models are based on a Swin-T transformer and a ResNeSt101 backbone, both with a CascadeRoIHead as the object detection head, with a total number of trainable parameters of approx. 72M and 95M. As hyperparameters for the label error benchmark we choose relative frequency of label errors γ = 0.2, the value for score thresholding after the first stage s ϵ = 0.25, the value for score thresholding after the second stage τ = 0 and the IoU -value α = 0.3 from which a proposal for a label error is considered a TP l . We show performance results for the respective models and for each dataset in Tab. 1. The upper half shows results on original (mAP 50 ) and noisy training data (mAP * 50 ), for which γ = 0.2 also holds. With sufficient training data and a moderate label error rate (γ = 0.2), the models still generalize well, resulting in mAP values comparable to models trained without simulated label errors. Thus, to make benchmarks evaluations trustworthy, whether already published or still under development, in particular the underlying test datasets should contain as few label errors as possible. The bottom half of Tab. 1 presents the performance of the models that we use for predicting label errors on real datasets. All models have been trained and evaluated on the original datasets (without any label modification).

Datasets For the detection of real label errors we use the same split for BDD as introduced in Sec. 3

Loss -AUROC : 0.963 Detection Score -AUROC : 0.768 Entropy -AUROC : 0.717 PD -AUROC : 0Loss -max F1 : 0.566 Detection Score -max F1 : 0.311 Entropy -max F1 : 0.222 PD -max F1 : 0.527 Number of Label Errors (a) Original training data Loss -AUROC : 0.922 Detection Score -AUROC : 0.892 Entropy -AUROC : 0.694 PD -AUROC : 0Loss -max F1 : 0.360 Detection Score -max F1 : 0.317 Entropy -max F1 : 0.183 PD -max F1 : 0.347 Number of Label Errors (b) Noisy training data with γ = 0.2

### 4.2. Benchmark Results for Simulated Label Errors

Table 1 shows that although 20% of the training labels are modified, the performance in terms of mAP 50 to mAP * 50 only decreases by a maximum of 1.2 percent points (pp) for EMNIST-Det and 3.9 pp for BDD. In both cases, the performance decreases more for the backbone containing more trainable parameters (ResNeSt101). This is consistent with the results for image classification from Northcutt et al. [28].

Architectures with fewer trainable parameters seem more suitable for handling label errors in the training data, possibly due to the network having less capacity to overfit the label errors. Figure 4 shows exemplary plots for AUROC and F 1 curves for the Swin-T backbone and BDD. On the two left plots we show results based on original training data and the two right plots based on noisy training data. The ranking of the methods is not identical everywhere: in terms of AUROC , loss (our method) is superior, followed by de-tection score, then entropy (our baselines) and finally PD. In terms of max F 1 , PD outperforms the detection score and the entropy but is inferior compared to the loss. Because AUROC considers rates and (max) F 1 considers absolute values and the number of label error proposals varies widely (PD = number of labels G, here 17,064; others > 80,000), the methods behave very differently with respect to AUROC and max F 1 . However, our loss method outperforms all other methods on both metrics. Note, that the small step in the upper right of each of the AUROC plots are the false negatives according to the label errors (FN l ), i.e. the simulated label errors that are not found by the methods. This number of FN l is vanishingly small in relation to all simulated label errors, with the exception of PD as the method is not able to detect drops. The generally observed behavior for BDD also does not change when looking at the results for the ResNeSt101 backbone in Tab. data, but inferior in terms of max F 1 . For PD, the AUROC seems to be rather stable comparing the two backbones, but the max F 1 is superior for Swin-T.

### 4.3. Evaluation for Real Label Errors

We now aim at detecting real instead of simulated label errors. The considered real-world datasets apart from BDD (VOC, COCO, Kitti, CE) are more similar in complexity to BDD than to EMNIST-Det. For BDD we observed in Sec. 4.2 that the loss method for the Swin-T backbone seems to be more stable according to label errors in the training data, as especially the max F 1 values for the loss and noisy labels are superior for Swin-T than for ResNeSt101. As we suspect label errors in the VOC, COCO, Kitti and CE training datasets, we use the Swin-T backbone to detect as many label errors as possible. Furthermore, we showed in Tab. 2 that the loss method outperforms the detection score, entropy and PD in each presented experiment, hence we detect label errors using only the loss method in the following. Since we manually look at all proposals individually and we are not able to look at all proposals (i.e. about 265,000 for VOC), we categorize the top-200 proposals into TP l or FP l . If a TP l is found we also note which type of label error is present and if we are not sure whether the proposal is TP l or FP l , we conservatively interpret it as FP l . The results are summarized in Tab. 3. For BDD, there are at least 34 label errors, which mostly consist of flips. Since Kitti consists of image sequences, it happens that one label error appears on several consecutive frames. When this happens, it usually affects objects that are visible on previous frames but are covered by, for instance, a bus for several frames but are still labeled. Label error proposals that fall into "Don't Care" areas are not considered. In total, we find 96 label errors with a precision of 47.5% on Kitti. As COCO and VOC consist of images of different everyday scenes that really differ from image to image, the variability of the representation of objects is very high in these two datasets. Since a label error proposal is enforced for each label, this also applies to the labels that are classified as background.

In a usual test setting, these labels would have been false negatives of the model, i.e. overlooked labels. The resulting loss is so high that these proposals end up in the reviewed top-200 proposals. Nevertheless, 50 label errors can be detected on COCO and 23 on VOC. When dealing with these two datasets, we noticed that drops are the most present label error type, although we did not find any among the top-200 proposals. We use this knowledge to restrict the proposals to those that have a class-independent IoU with the labels of the image of less than α. Using this subset and re-reviewing the top-200 proposals, we are able to find 125 drops with a precision of 61.0% for COCO and 175 drops with a precision of 71.5% for VOC. For the calculation of the precision see Sec. 3.5. Prior knowledge about the label quality of the dataset and the types of label errors that occur helps to detect a specific type of label error. From the high precisions for VOC and COCO, we conclude that our method can help to correct the label errors resulting in cleaner benchmarks. Exemplary label errors for the above datasets are shown in Fig. 5. The first proposal detects a shift, the second a flip, the third and fourth a spawn and the remaining proposals detect drops. For CE, we filter the proposals by drops, resulting in 194 detected drops with a precision of 97%.

## 5. Conclusion

In this work, we introduced a benchmark for label error detection for object detection datasets. We for the first time simulated and evaluated four different types of label errors on two selected datasets. We also developed a novel method based on instance-wise loss scoring and compare it with four baselines. Our method prevails by a significant margin in experiments on our simulated label error benchmark. In our experiments with real label errors, we found a number of label errors in prominent datasets as well as in a proprietary production-level dataset. With the evaluation for individual label error types we can detect real label errors on commonly used test datasets in object detection with a precision of up to 71.5%. Furthermore, we presented additional findings. Models with less parameters are more robust to label errors in training sets while models with more parameters suffer more. We make our code publicly available at GitHub.

### Supplementary Material

Proprietary Dataset An exemplary test image including labels for the proprietary dataset (CE) is shown in Fig. 6. The labels divide the car into parts, such as the two wheels "WheelFrontRight" and "WheelRearRight" as well as doors, roof, etc. The example also includes a drop with the missing mirror "MirrorRight".

### Dataset Dependent Parameters for Training

The dataset-dependent hyperparameters for training are stated in Tab. 4. The original images from EMNIST-Det have an image resolution of 320 × 320 pixels, i.e., we do not artificially scale them to a higher image resolution. The BDD images also contain many small labels while having a high original resolution (1280 × 720), which is a challenging setup. To get the best possible label error detection, we keep this high resolution and rescale the images to 1333 × 800 pixels. Kitti, COCO, VOC and CE are each rescaled to an image resolution of 1000 × 600 pixels. The batch size for all datasets is in the range of 4-24, the initial learning rate is either 0.02 or 0.01 depending on the dataset, and the number of training iterations is in the range of 24,000-250,000. All numbers apply to the Swin-T backbone except the numbers ( * ) for the training iterations of EMNIST-Det and BDD, which apply to the ResNeSt101 backbone. All other hyperparameters are identical for the different architectures. The files for the configurations used in training, also containing the precise values of the above hyperparameters, are published with the code on GitHub.

Benchmark Results for Individual Simulated Label Error Types In our experiments, all label errors occur simultaneously, but the evaluation can also be conditioned on the individual label error types. For drops or flips we consider only the false positives according to ỹ, i.e. all boxes that have a maximum class-wise IoU of less than α(= 0.3) with all noisy labels of the associated image. Then, we can calculate AUROC and max F 1 values on this subset. We do the same for the shifts, except that we only consider the true positives according to Ỹ. For the spawns, we must consider both true positives and false positives according to Ỹ, since the predicted class, that overlaps sufficiently with the spawned label, can be the same as the class of the spawn itself.

The benchmark results for individual simulated label errors are stated in Tab. 5. For drops, the detection score and instance-wise loss perform similarly well, with the AUROC values differing by at most 1.92 pp and a minimal AUROC of 91.72%. The difference in the max F 1 values is more pronounced, with the loss at EMNIST-Det outperforming the detection score by 3.03 to 6.56 pp. For BDD, the detection score of Swin-T is superior to the loss by up to 9 pp, whereas the loss for ResNeSt101 outperforms the detection score by up to 10.22 pp. The entropy reaches a maximum of 88.22%/56.70% AUROC / max F 1 for EMNIST-Det and 73.14%/7.11% for BDD, which is far from the numbers achieved for the loss and the detection score. PD is not able to detect drops, as the bounding boxes of the labels are also the label error proposals itself.

A similar behavior can be observed for the flips, where the AUROC values for loss and detection score only differ by a maximum of 1.64 pp. In terms of max F 1 the loss outperforms the detection score and entropy in every case. PD performs inferior in terms of AUROC compared to the loss, but in terms of max F 1 PD outperforms the loss for BDD based on both backbones trained on noisy data.

For the shifts, the detection score and PD have similar performance as the naive baseline in terms of AUROC and all max F 1 values are < 14%. Except for BDD trained on noisy data, where entropy performs superior to the loss, loss outperforms all baselines.

For the spawns, the detection score performs similar compared to the shifts. PD performs well especially in terms of max F 1 , where PD even outperforms the loss for RestNeSt101 on BDD with noisy training data by 20.16 pp, otherwise loss is superior to PD. In the cases where entropy outperforms loss, the difference is at most 5.44 pp in terms of AUROC and 3.69 pp in terms of max F 1 .

The detection score can neither reliably detect the shifts nor the spawns, whereas the entropy cannot detect the drops and flips well, especially for complicated problems such as BDD. PD cannot reliably detect the shifts and is not able to detect drops by design. All in all, the loss method is the only one of those presented that can detect all four different types of label errors efficiently. 6 shows mAP , AUROC and max F 1 values for different noise intensities for Swin-T on the BDD training dataset. In our experiments, it makes no difference whether the labels of the training data contain 5% or 20% noise, the mAP is between 50.2% and 50.4%, where the model has an mAP of 52.1% due to training on the original training data. All mAP evaluations are based on the test data with original and thus unmodified labels.

### Different Noise Intensity in Training Table

On the one hand, the AUROC /max F 1 values decrease with increasing noise intensity by 3.69/20.62 pp for loss, by 2.31/3.88 pp for entropy and by 3.01/17.94 pp for PD, respectively. For the detection score, on the other hand, the AUROC value increases by 12.39 pp from 76.82% to 89.21% and the max F 1 value increases only marginally by 0.54 pp to 31.68%. Nevertheless, the loss outperforms the detection score/entropy/PD in every case by at least 3. 40 The mAP increases the more images are used for training and the less label errors exist in the training data. Here, the model trained on 6,227 and unmodified labels (γ = 0) has a 0.8 points higher mAP than the model trained on 12,454 images with γ = 0.2. In this case, after comparing the performances, it is worth to review and improve the underlying labels instead of labeling new images and add them to the training set.

The AUROC values increase as the number of images increases with γ = 0. With γ = 0.2, the values for loss and entropy decrease as the number of images increases. The max F 1 values decrease independently of γ with increasing number of images for loss and entropy, whereas the values increase for detection score. The decrease in AUROC and max F 1 values for loss and entropy could be due to overfitting of the model. For PD, AUROC and max F 1 values remain almost constant for the respective datasets. However, the loss always outperforms all baselines in terms of AUROC and max F 1 . All AUROC /max F 1 evaluations are based on the test data with γ = 0.2 and thus on the identical label basis as for Tab. 2.

Real Label Errors Further detected real label errors are presented in Fig. 7. The top row shows examples for BDD, where all found label errors are flips, except for the third proposal from the right. This proposals can be interpreted as two label errors. Either the "car" label on the "bus" is wrong (spawn) and the bus was forgotten to be labeled (drop), or the

-p F 1 -p F -κ p F C-1 p F C-1 + κ Figure 8

. Illustration of the probabilistic statement about predicted confidences conditioned to correct and incorrect given labels. PAC learning leads to concentration of the confidences around 1 -pF and p F C-1 , respectively. The separation on the confidences carries over to the cross entropy loss. and the corresponding label y.

The rough intuition for this statement is that a probably approximate correct learner [33] (PAC-learner) p has probabilistic bounds for having predictive distribution close to the data-generating distribution p. Therefore, sufficient data sampling and empirical loss minimization will lead to statistical concentration of confidences p around p. If p does not suffer from too strong label noise, we obtain separation between confidences on incorrect and confidences on correct labels. This separation then carries over to the negative log-likelihood (i.e., cross entropy) loss by monotony.

We assume data points (x, y) ∼ p following some noisy data generating distribution p, where x ∼ P x follows a marginal distribution P x . In practice, training and test data originate from the same data pool and we do not see any reason to assume that they follow different labeling procedures. However, it is sufficient to require that for testing data (x, y), x follows the same marginal distribution x ∼ P x . Our proof builds on the existence of a true labeling function f : x → y and the assumption that the data distribution p introduces stochastic flips of labels that occur with a fixed uniform rate p F ∈ [0, 1). This flip probability p F uniformly distributed over all C -1 incorrect classes which are not f (x) leads to the following constraints on p when conditioned to x:

on test data pairs (x, y). We show that the loss is above a certain threshold if an incorrect label is given and below some threshold in case of a correct, non-flipped label. Nonoverlapping intervals indicate that the statistical separation between losses given correct and false labels seen in our experiments can be explained theoretically. We assume PAC-learnability for the proof. This assumption can be justified via the error decomposition of empirical risk minimization for the KL divergence over the hypothesis space H with training data {(x 1 , y 1 ), . . . , (x n , y n )}:

where H = -C c=1 p(c|x)•log(p(c|x)) is the entropy of the data generating distributionfoot_1 . The first term is the model misspecification error given by H . In practice, we assume an expressive DNN with a large amount of capacity (appealing to universal approximation) which allows for this error to be negligible. In particular, in this case, no restrictions need to be made in the choice of H . The second term measures the error of the learning algorithm w.r.t. an empirical risk minimizer h. Similarly to the term, an expressive DNN trained to convergence leads to small contributions by this term. Lastly, the third term is the sampling error made as compared to the loss D(p∥h) in the true distribution. The third term can be controlled by application of concentration inequalities and chaining under certain assumptions (see [36]) which is why the sum of the three terms can be made smaller than some fixed ε > 0 given sufficient amount of data.

p(f (x)|x) := 1 -p F , p(y|x) := p F /(C -1) (2) ∀y ̸ = f (x). A statistical model p = p(y|x) PAC-learns classification on samples of the (noisy) data generating distribution p = p(y|x). In the present treatment, we assume PAClearning with respect to the Kullback-Leibler (KL) divergence D KL (p(•|x)∥ p(•|x)) = -log d p(y|x) dp(y|x) p(y|x) dy. In the following our goal is to show probabilistic statements about the cross entropy loss ℓ CE ( p(x)∥y) := -C c=1 y c • log( p c (x))

for any incorrect label y ̸ = f (x) with probability 1 -δ over chosen training data and with probability 1 -2ε κ 2 over the choice of x.

Proof. We aim at bounding max y=1,...,C |p(y|x) -p(y|x)| by the total variation distance. PAC-learnability asserts that given enough data, the p-distributions illustrated in Fig. 8 are concentrated around 1 -p F for true labels and pF C-1 for incorrect labels. In particular, PAC-learnability implies

i.e., p(y|x) < κ + pF C-1 and we have ℓ CE ( p(x)∥y) > -log κ + pF C-1 . Finally, we obtain separability of losses with true versus false labels in probability if

1-p F -κ > κ+ p F C -1 ⇐⇒ p F < C -1 C

(1-2κ). (10)

## Figures et tableaux

**Figure 2.** Examples of the different types of simulated label errors. The images are from the EMNIST-Det test dataset [30].

1 Figure 3. Figure 3. Visualization of our instance-wise loss method for detecting label errors. The red label indicates a spawn, the blue one a drop and the yellow one a correct label.

Proposition 1 ( Statistical Separation of the Cross Entropy Loss). Let training and testing labels be given under a stochastic flip in p(•|x) with probability p F . A correct label y = f (x) is given by a true labeling function f and has probability p(f (x)|x) = 1 -p F . Incorrect labels y ̸ = f (x) are drawn with probability p( y|x) = p F /(C -1). Let the label distribution p(•|x) be PAC-learnable by the hypothesis space of p(•|x) w.r.t. D KL (to precision ε and confidence 1 -δ) and let κ > 0. If p F < C-1

**Figure 4.** The two left plots in (a) show evaluations based on the predictions of a model trained on original training data and the two right ones in (b) based on noisy training data with γ = 0.2. The number of considered label error proposals depends on threshold τ .

**Figure 5.** Visualization of detected label errors in real test datasets. The top row of images depicts the label error proposals and the bottom row the corresponding labels from the dataset. The image pairs belong from left to right in steps of two to BDD, Kitti, COCO and VOC.

**Figure 6.** Example image from the CE test data with labels and a missing "MirrorRight".

**Figure 7.** Visualization of further detected real label errors in test datasets for BDD (top), COCO (center) and VOC (below).

Dℓℓ (p∥ p) := E x∼px [D KL (p(•|x)∥ p(•|x))] CE ( p(x j )∥y j ) -inf h∈H ℓ CE (h(x j )∥y j ) CE (h(x j )∥y j ) -H(p(•|x)) < ε

Proposition 1 ( Statistical Separation of the Cross Entropy Loss). Let training and testing labels be given under a stochastic flip in p(•|x) with probability p F as above, let the label distribution p(•|x) be PAC-learnable by the hypothesis space of p(•|x) w.r.t. D KL (to precision ε and confidence 1 -δ) and let κ > 0. If p F < C-1 C (1 -2κ), we obtain strict separation of the loss function ℓ CE ( p(x)∥f (x)) < -log(1 -p F -κ) < -log(κ + pF C-1 ) < ℓ CE ( p(x)∥ y)

E 2 ≤ 2 κ 2 E 2 ( 7 ) x∼px [D KL (p(•|x)∥ p(•|x))] < ε (6)with probability 1 -δ over the choice of training data. Let κ > 0. From this PAC result, we derive bounds for the probability of max y=1,...,C |p(y|x) -p(y|x)| exceeding κ via the total variation distance. We haveP x (∥p(•|x) -p(•|x)∥ TV ≥ κ) ≤ P x ( 2D KL (p(•|x)∥ p(•|x)) ≥ κ) ≤ P x D KL (p(•|x)∥ p(•|x)) ≥ κ 2 x∼px [D KL (p(•|x)∥ p(•|x))] < 2ε κwith probability 1 -δ over the choice of training data. Here, the first inequality is the application of Pinsker's inequality and the third due to the Markov inequality. Assume that we are given a correct label y for x, then with probability 1 -δ over training data and with probability 1 -2ε κ 2 over sampling x, we have that |p(y|x) -p(y|x)| = |(1 -p F ) -p(y|x)| ≤ max y |p(y|x) -p(y|x)| ≤ ∥p(•|x) -p(•|x)∥ TV < κ.

( 8 ) This implies p(y|x) > 1-p F -κ and therefore, by monotony of the logarithm ℓ CE ( p(y|x)∥y) < -log(1 -p F -κ). Similarly, if y is any incorrect label, we have the probabilistic statement|p(y|x) -p(y|x)| = p F C -1 -p(y|x) ≤ max y |p(y|x) -p(y|x)| < κ,

**Table 1.** Validation of object detection performance on our datasets.

    Dataset | Backbone | mAP 50 mAP | ( * ) 50
    EMNIST-Det | Swin-T | 98.2 | 98.0
    EMNIST-Det ResNeSt101 | 96.4 | 95.2
    BDD | Swin-T | 52.1 | 50.3
    BDD | ResNeSt101 | 56.8 | 52.9
    COCO | Swin-T | 54.1 | 
    Kitti | Swin-T | 38.6 | 
    VOC | Swin-T | 83.3 | 
    CE | Swin-T | 70.0 | 

[figure sans légende identifiée] AUROC and max F 1 values for the joint evaluation of all label error types, i.e. when all label error types are present simultaneously, in Sec. 4.2. For the latter, we show how many real label errors we can detect among the top-200 proposals for each real-world dataset in Sec. 4.3.

**Table 2.** .1 as well as VOC, COCO, Kitti and CE. The training data for VOC consists of "2007 train" + "2012 trainval" and we predict label errors on the "2007 test"-split. COCO is trained on the train split and label errors are predicted on the validation split from 2017. For Kitti we use a scene-wise split, resulting in 5 scenes Label error detection experiments with two different backbones; higher values are better. Bold numbers indicate the highest AUROC or max F1 per experiment and underlined numbers are the second highest.

    AUROC | max F 1

**Table 3.** Categorization of the top-200 proposals for real label errors with the loss method for the Swin-T backbone. ( * ) indicates the evaluation of proposals based on the detection of drops.

[figure sans légende identifiée] /21.68/35.71 pp in terms of AUROC and by at least 4.29/17.64/0.38 pp in terms of max F 1 . All AUROC /max F 1 evaluations are based on the test data with

**Table 4.** Training hyperparameters for the Swin-T and the ResNeSt101 ( ( * ) ) backbone. γ = 0.2 and thus on the identical label basis as for Tab. 2.Different Amount of Training Images Table7shows mAP , AUROC and max F 1 values for different amounts of training images for Swin-T on BDD. Therefore, the subsets with fewer images are always included in the subsets with more images and the identically sized subsets with different noise intensities contain the same images.

    Dataset | Batch Size Image Resolution # Training Iterations Learning Rate
    EMNIST-Det | 24 | 300 × 300 | 24,000/48,000 ( * ) | 0.02
    BDD | 4 | 1333 × 800 | 150,000/250,000 ( * ) | 0.01
    Kitti | 6 | 1000 × 600 | 70,000 | 0.01
    COCO | 12 | 1000 × 600 | 250,000 | 0.02
    VOC | 6 | 1000 × 600 | 70,000 | 0.02
    CE | 4 | 1000 × 600 | 200,000 | 0.01

**Table 5.** AUROC and max F1 values for loss, detection score (Score), entropy and PD for all dataset-backbone-training label combinations; higher values are better. Bold numbers indicate the highest AUROC or max F1 per experiment and underlined numbers are the second highest.

    AUROC | max F 1

**Table 6.** Validation of object detection performance and label error detection experiments for different noise for training Swin-T on BDD; higher values are better. Bold numbers indicate the highest AUROC or max F1 per experiment and underlined numbers are the second highest.

    count as spawns resulting in three label errors for this single
    proposal.

**Table 7.** Validation of object detection performance and label error detection experiments for different noise and number of images for training Swin-T on BDD; higher values are better. Bold numbers indicate the highest AUROC or max F1 per experiment and underlined numbers are the second highest.
