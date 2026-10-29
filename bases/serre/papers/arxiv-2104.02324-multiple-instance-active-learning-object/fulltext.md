---
id: arxiv-2104.02324-multiple-instance-active-learning-object
title: "Multiple instance active learning for object detection"
year: 2021
backend: grobid
---

## Abstract

Despite the substantial progress of active learning for image recognition, there still lacks an instance-level active learning method specified for object detection. In this paper, we propose Multiple Instance Active Object Detection (MI-AOD), to select the most informative images for detector training by observing instance-level uncertainty. MI-AOD defines an instance uncertainty learning module, which leverages the discrepancy of two adversarial instance classifiers trained on the labeled set to predict instance uncertainty of the unlabeled set. MI-AOD treats unlabeled images as instance bags and feature anchors in images as instances, and estimates the image uncertainty by re-weighting instances in a multiple instance learning (MIL) fashion. Iterative instance uncertainty learning and re-weighting facilitate suppressing noisy instances, toward bridging the gap between instance uncertainty and imagelevel uncertainty. Experiments validate that MI-AOD sets a solid baseline for instance-level active learning. On commonly used object detection datasets, MI-AOD outperforms state-of-the-art methods with significant margins, particularly when the labeled sets are small. Code is available at https://github.com/yuantn/MI-AOD.

## 1. Introduction

The key idea of active learning is that a machine learning algorithm can achieve better performance with fewer training samples if it is allowed to select which to learn. Despite the rapid progress of the methods with less supervision [21,20], e.g., weak supervision and semi-supervision, active learning remains the cornerstone of many practical applications for its simplicity and higher performance.

In the computer vision area, active learning has been widely explored for image classification (active image classification) by empirically generalizing the model trained on the labeled set to the unlabeled set [9,30,18,39,4,24,36,25,34]. Uncertainty-based methods define various metrics for selecting informative images and adapting trained models to the unlabeled set [9]. Distribution-based approaches [30,1] aim at estimating the layout of unlabeled images to select samples of large diversity. Expected model change methods [8,15] find out samples that can cause the greatest change of model parameters or the largest loss [42].

Despite the substantial progress, there still lacks an instance-level active learning method specified for object detection (i.e., active object detection [42,43,2]), where the instance denotes the object proposal in an image. The objective goal of active object detection is to select the most informative images for detector training. However, the recent methods tackled it by simply summarizing/averaging instance/pixel uncertainty as image uncertainty and unfortunately ignored the large imbalance of negative instances in object detection, which causes significant noisy instances in the background and interferes with the learning of image uncertainty, Fig. 1(a). The noisy instances also cause the inconsistency between image and instance uncertainty, which hinders selecting informative images.

In this paper, we propose a Multiple Instance Active Object Detection (MI-AOD) approach, Fig. 1(b), and target at selecting informative images from the unlabeled set by learning and re-weighting instance uncertainty with discrepancy learning and multiple instance learning (MIL). To learn the instance-level uncertainty, MI-AOD first defines an instance uncertainty learning (IUL) module, which leverages two adversarial instance classifiers plugged atop the detection network (e.g., a feature pyramid network) to learn the uncertainty of unlabeled instances. Maximizing the prediction discrepancy of two instance classifiers predicts instance uncertainty while minimizing classifiers' discrepancy drives learning features to reduce the distribution bias between the labeled and unlabeled instances.

To establish the relationship between instance uncertainty and image uncertainty, MI-AOD incorporates a MIL module, which is in parallel with the instance classifiers. MIL treats each unlabeled image as an instance bag and performs instance uncertainty re-weighting (IUR) by evaluating instance appearance consistency across images. During MIL, the instance uncertainty and image uncertainty are forced to be consistently driven by a classification loss defined on image class labels (or pseudo-labels). Optimizing the image-level classification loss facilitates suppressing the noisy instances while highlighting truly representative ones. Iterative instance uncertainty learning and instance uncertainty re-weighting bridge the gap between instance-level observation and image-level evaluation, towards selecting the most informative images for detector training.

The contributions of this paper include:

(1) We propose Multiple Instance Active Object Detection (MI-AOD), establishing a solid baseline to model the relationship between the instance uncertainty and image uncertainty for informative image selection.

(2) We design instance uncertainty learning (IUL) and instance uncertainty re-weighting (IUR) modules, providing effective approaches to highlight informative instances while filtering out noisy ones in object detection.

(3) We apply MI-AOD to object detection on commonly used datasets, improving state-of-the-art methods with significant margins.

## 2. Related Work

### 2.1. Active Learning

Uncertainty-based Methods. Uncertainty is the most popular metric to select samples for active learning [31], which can be defined as the posterior probability of a predicted class [17,16], or the margin between the posterior probabilities of the first and the second predicted class [14,28]. It can also be defined upon entropy [32,26,14] to measure the variance of unlabeled samples. The expected model change methods [29,33] utilized the present model to estimate the expected gradient or prediction changes [8,15] for sample selection. MIL-based methods [33,13,40,6] selected informative images by discovering representative instances. However, they are designed for image classification and not applicable to object detection due to the challenging aspect of crowded and noisy instances [38,37].

Distribution-based Methods. These methods select diverse samples by estimating the distribution of unlabeled samples. Clusters [27] were applied to build the unlabeled sample distribution while discrete optimization methods [11,7,41] were employed to perform sample selection. Considering the distances to the surrounding samples, the context-aware methods [12,3] selected the samples that can represent the global sample distribution. Core-set [30] defined active learning as core-set selection, i.e., choosing a set of points such that a model learned on the labeled set can capture the diversity of the unlabeled samples.

In the deep learning era, active learning methods remain falling into the uncertainty-based or distribution-based routines [18,39,4]. Sophisticated methods extended active learning to the open sets [24], or combined it with selfpaced learning [36]. Nevertheless, it remains questionable whether the intermediate feature representation is effective for sample selection. The learning loss method [42] can be categorized as either uncertainty-based or distributionbased. By introducing a module to predict the "loss" of the unlabeled samples, it estimates sample uncertainty and selects samples with large "loss" like hard negative mining.

### 2.2. Active Learning for Object Detection

Despite the substantial progress of active learning, few methods are specified for active object detection, which faces complex instance distributions in the same images and are more challenging than active image classification. By simply sorting the loss predictions of instances to evaluate the image uncertainty, the learning loss method [42] specified for image classification was directly applied to object detection. The image-level uncertainty can also be estimated by the uncertainty of a lot of background pixels [2]. CDAL [1] introduced spatial context to active detection and selected diverse samples according to the distances to the labeled set. Existing approaches simply used instance-/pixellevel observations to represent the image-level uncertainty. There still lacks a systematic method to learn the image uncertainty by leveraging instance-level models [44,45].

f 1 f 2 f 1 f 2 f 1 f 2 f 1 f 2 f mil Re-weighting f mil f mil f 1 f 1 f 2 f 2 Selected Instance

## 3. The Proposed Approach

### 3.1. Overview

For active object detection, a small set of images X 0 L (the labeled set) with instance labels Y 0 L and a large set of images X 0 U (the unlabeled set) without labels are given. For each image, the label consists of bounding boxes (y loc x ) and categories (y cls x ) for objects of interest. A detection model M 0 is firstly initialized by using the labeled set {X 0 L , Y 0 L }. With the initialized model M 0 , active learning targets at selecting a set of images X 0 S from X 0 U to be manually labeled and merging them with

X 0 L for a new labeled set X 1 L , i.e., X 1 L = X 0 L ∪ X 0 S .

The selected image set X 0 S should be the most informative, i.e., can improve the detection performance as much as possible. Based on the updated labeled set Xfoot_0 L , the task model is retrained and updated to M 1 . The model training and sample selection repeat some cycles until the size of labeled set reaches the annotation budget.

Considering the large number 1 of instances in each image, there are two key problems for active object detection: (1) how to evaluate the uncertainty of the unlabeled instances using the detector trained on the labeled set; (2) how to precisely estimate the image uncertainty while filtering out noisy instances. MI-AOD handles these two problems by introducing two learning modules respectively. For the first problem, MI-AOD incorporates instance uncertainty learning, with the aim of highlighting informative instances in the unlabeled set, as well as aligning the distributions of the labeled and unlabeled set, Fig. 2(a). It is motivated by the fact that most active learning methods remain simply generalizing the models trained on the labeled set to the unlabeled set. This is problematic when there is a distribution bias between the two sets [10]. For the second problem, MI-AOD introduces MIL to both the labeled and unlabeled set to estimate the image uncertainty by re-weighting the instance uncertainty. This is done by treating each image as an instance bag while re-weighting the instance uncertainty under the supervision of the image classification loss. Optimizing the image classification loss facilitates highlighting truly representative instances belonging to the same object classes while suppressing the noisy ones, Fig. 2(b).

### 3.2. Instance Uncertainty Learning

Label Set Training. Using the RetinaNet as the baseline [19], we construct a detector with two discrepant instance classifiers (f 1 and f 2 ) and a bounding box regressor (f r ), Fig. 3(a). We utilize the prediction discrepancy between the two instance classifiers to learn the instance uncertainty on the unlabeled set. Let g denote the feature extractor parameterized by θ g . The discrepant classifiers are parameterized by θ f1 and θ f2 and the regressor by θ fr . Θ = {θ f1 , θ f2 , θ fr , θ g } denotes the set of all parameters, where θ f1 and θ f2 are independently initialized.

In object detection, each image x can be represented by multiple instances {x i , i = 1, ..., N } corresponding to the feature anchors on the feature map [19]. N is the number of the instances in image x. {y i , i = 1, ..., N } denote the labels for the instances. Given the labeled set, a detection model is trained by optimizing the detection loss, as

argmin Θ l det (x) = i FL(ŷ f1 i , y cls i ) + FL(ŷ f2 i , y cls i ) + SmoothL1(ŷ fr i , y loc i ) ,(1)

where FL(•) is the focal loss function for instance classification and SmoothL1(•) is the smooth L1 loss function for bounding box regression [19]. Maximizing Instance Uncertainty. Before the labeled set can precisely represent the unlabeled set, there exists a distribution bias between the labeled and unlabeled set, especially when the labeled set is small. The informative instances are in the biased distribution area. To find them out, f 1 and f 2 are designed as the adversarial instance classifiers with larger prediction discrepancy on the instances close to the boundary, Fig. 2(a). The instance uncertainty is defined as the prediction discrepancy of f 1 and f 2 .

ŷf1 i = f 1 (g(x i )), ŷf2 i = f 2 (g(x i )) and ŷfr i = f r (g(x i ))

To find out the most informative instances, it requires to fine-tune the network and maximize the prediction discrep-ancy of the adversarial classifiers, Fig. 3(b). In this procedure, θ g is fixed so that the distributions of both the labeled and unlabeled instances are fixed. θ f1 and θ f2 are fine-tuned on the unlabeled set to maximize the prediction discrepancies for all instances. At the same time, it requires to preserve the detection performance on the labeled set. This is fulfilled by optimizing the following loss function, as

argmin Θ\θg L max = x∈X L l det (x) - x∈X U λ • l dis (x),(2)

where

l dis (x) = i |ŷ f1 i -ŷf2 i |(3)

denotes the prediction discrepancy loss. ŷf1 i , ŷf2 i ∈ R 1×C are the instance classification predictions of the two classifiers for the i-th instance in image x, where C is the number of object classes in the dataset, and λ is a regularization hyper-parameter determined by experiment. As shown in Fig. 2(a), the informative instances with different predictions by the adversarial classifiers tend to have larger prediction discrepancy and larger uncertainty.

Minimizing Instance Uncertainty. After maximizing the prediction discrepancy, we further propose to minimize the prediction discrepancy to align the distributions of the labeled and unlabeled instances, Fig. 3(c). In this procedure, the classifier parameters θ f1 and θ f2 are fixed, while the parameters θ g of the feature extractor are optimized by minimizing the prediction discrepancy loss, as

argmin θg L min = x∈X L l det (x) + x∈X U λ • l dis (x). (4)

denote the prediction results (classification and localization) for the instances. y cls i and y loc i denote the ground-truth class label and bounding box label, respectively.

By minimizing the prediction discrepancy, the distribution bias between the labeled set and the unlabeled set is minimized and their features are aligned as much as possible.

In each active learning cycle, the max-min prediction discrepancy procedures repeat several times so that the instance uncertainty is learned and the instance distributions of the labeled and unlabeled set are progressively aligned. This actually defines an unsupervised learning procedure, which leverages the information (i.e., prediction discrepancy) of the unlabeled set to improve the detection model.

### 3.3. Instance Uncertainty Re-weighting

With instance uncertainty learning, the informative instances are highlighted. However, as there is a lot of instances (∼100k) in each image, the instance uncertainty may be not consistent with the image uncertainty. Some instances of high uncertainty are simply background noise or hard negatives for the detector. We thereby introduce an MIL procedure to bridge the gap between the instance-level and image-level uncertainty by filtering out noisy instances.

Multiple Instance Learning. MIL treats each image as an instance bag and utilizes the instance classification predictions to estimate the bag labels. In turn, it re-weights the instance uncertainty scores by minimizing the image classification loss. This actually defines an Expectation-Maximization procedure [35,5] to re-weight instance uncertainty across bags while filtering out noisy instances.

Specifically, we add an MIL classifier f mil parameterized by θ f mil in parallel with the instance classifiers, Fig. 4. The image classification score ŷcls i,c for multiple instances in an image is calculated as

ŷcls i,c = exp(ŷ f mil i,c ) c exp(ŷ f mil i,c ) • exp (ŷ f1 i,c + ŷf2 i,c )/2 i exp (ŷ f1 i,c + ŷf2 i,c )/2 ,(5)

where

ŷf mil = f mil (g(x)

) is an N × C score matrix, and ŷf mil i,c is the element in ŷf mil indicating the score of the i-th instance for class c. According to Eq. ( 5), the image classification score ŷcls i,c is large only when x i belongs to class c (the first term in Eq. ( 5)) and its instance classification scores ŷf1 i,c and ŷf2 i,c are significantly larger than those of others (the second term in Eq. ( 5)).

Considering that the image classification scores of the instances from other classes/backgrounds are small, the image classification loss l imgcls is defined as

l imgcls (x) = - c y cls c log i ŷcls i,c +(1 -y cls c ) log(1 - i ŷcls i,c ) ,(6)

where y cls c ∈ {0, 1} denotes the image class label, which can be directly obtained from the instance class label y cls i in the labeled set. Optimizing Eq. ( 6) drives the MIL classifier to activate instances with large MIL score (ŷ f mil i,c ) and large classification outputs (ŷ f1 i,c + ŷf2 i,c ). The instances with small MIL scores will be suppressed as background. The image classification loss is firstly applied in the label set training to get the initial model, and then used to re-weight the instance uncertainty in the unlabeled set.

Uncertainty Re-weighting. To ensure that the instance uncertainty is consistent with the image uncertainty, we assemble the image classification scores for all classes to a score vector w i and re-weight the instance uncertainty as

ldis (x) = i |w i • (ŷ f1 i -ŷf2 i )|,(7)

where w i = ŷcls i . We then update Eq. ( 2) to

argmin Θ\θg Lmax = x∈X L l det (x)+l imgcls (x) - x∈X U λ• ldis (x),(8)

where Θ = Θ∪{θ f mil }. By optimizing Eq. ( 8), the discrepancies of instances with large image classification scores are preferentially estimated, while those with small classification scores are suppressed. Similarly, Eq. ( 4) is updated to

argmin θg,θ f mil Lmin = x∈X L l det (x) + l imgcls (x) + x∈X U λ • ldis (x) + l imgcls (x) .(9)

In Eq. ( 9), the image classification loss is applied to the unlabeled set, where the pseudo image labels are estimated using the outputs of the instance classifiers, as

y pseudo c = 1 max i ŷf1 i,c + ŷf2 i,c 2 , 0.5 ,(10)

where 1(a, b) is a binarization function. When a > b, it returns 1; otherwise 0. Eq. ( 10) is defined based on that instance classifiers can find true instances but are easy to be confused by complex backgrounds. We use the maximum instance score to predict pseudo image labels and leverage MIL to reduce background interference. According to Eqs. ( 5) and ( 6), the image classification loss ensures the highlighted instances are representative of the image, i.e., minimizing the image classification loss bridges the gap between the instance uncertainty and image uncertainty. By iteratively optimizing Eqs. ( 8) and ( 9), informative object instances in the same class are statistically highlighted, while the background instances are suppressed.

### 3.4. Informative Image Selection

In each learning cycle, after instance uncertainty learning (IUL) and instance uncertainty re-weighting (IUR), we select the most informative images from the unlabeled set by observing the top-k instance uncertainty defined in Eq. (3) for each image, where k is a hyper-parameter. This is based on the fact that the noisy instances have been suppressed and the instance uncertainty becomes consistent with the image uncertainty. The selected images are merged into the labeled set for the next learning cycle.

## 4. Experiments

### 4.1. Experimental Settings

Datasets. The trainval sets of PASCAL VOC 2007 and 2012 datasets which contain 5011 and 11540 images are used for training. The VOC 2007 test set is used to evaluate mean average precision (mAP). The MS COCO dataset contains 80 object categories with challenging aspects including dense objects and small objects with occlusion. We use the train set with 117k images for active learning and the val set with 5k images for evaluating AP.

Active Learning Settings. We use the RetinaNet [19] with ResNet-50 and SSD [23] with VGG-16 as the base detector. For RetinaNet, MI-AOD uses 5.0% of randomly se-lected images from the training set to initialize the labeled set on PASCAL VOC. In each active learning cycle, it selects 2.5% images from the rest unlabeled set until the labeled images reach 20.0% of the training set. For the largescale MS COCO, MI-AOD uses only 2.0% of randomly selected images from the training set to initialize the labeled set, and then selects 2.0% images from the rest of the unlabeled set in each cycle until reaching 10.0% of the training set. In each cycle, the model is trained for 26 epochs with the mini-batch size 2 and the learning rate 0.001. After 20 epochs, the learning rate decreases to 0.0001. The momentum and the weight decay are set to 0.9 and 0.0001 respectively. For SSD, we follow the settings in LL4AL [42] and CDAL [1], where 1k images in the training set are selected to initialize the labeled set and 1k images are selected in each cycle. The learning rate is 0.001 for the first 240 epochs and reduced to 0.0001 for the last 60 epochs. The mini-batch size is set to 32 which is required by LL4AL.

We compare MI-AOD with random sampling, entropy sampling, Core-set [30], LL4AL [42] and CDAL [1]. For entropy sampling, we use the averaged instance entropy as the image uncertainty. We repeat all experiments for 5 times and use the mean performance. MI-AOD and other methods share the same random seed and initialization for a fair comparison. λ defined in Eqs. ( 2), ( 4), ( 8) and ( 9) is set to 0.5 and k mentioned in Sec. 3.4 is set to 10k.

### 4.2. Performance

PASCAL VOC. In Fig. 5, we report the performance of MI-AOD and compare it with state-of-the-art methods on a TITAN V GPU. Using either the RetinaNet [19] or SSD [22] detector, MI-AOD outperforms state-of-the-art methods with large margins. Particularly, it respectively outperforms state-of-the-art methods by 18.08%, 7.78%, and 5.19% when using 5.0%, 7.5%, and 3. Ablation study on IUR. "wi" is the wi in Eq. (7). "Set" denotes the sample set for IUR. X and XL denote the whole sample set and the labeled set, respectively. mAP, which significantly outperforms CDAL by 3.20%. The improvements validate that MI-AOD can precisely learn instance uncertainty while selecting informative images. When using the SSD detector, MI-AOD outperforms state-of-the-art methods in almost all cycles, demonstrating the general applicability of MI-AOD to object detectors.

MS COCO. MS COCO is a challenging dataset for more categories, denser objects, and larger scale variation, where MI-AOD also outperforms the compared methods, Fig. 5. Particularly, it respectively outperforms Core-set and CDAL by 0.6%, 0.5%, and 2.0%, and 0.6%, 1.3%, and 2.6% when using 2.0%, 4.0%, and 10.0% labeled images.

### 4.3. Ablation Study

IUL. As shown in Tab. 1, with IUL, the detection performance is improved up to 70.06% in the last cycle, which outperforms the Random method by 2.97% (70.06% vs. 67.09%). In Tab. 2, IUL also significantly improves the image classification performance with active learning on CIFAR-10. Particularly when using 2.0% samples, it improves the classification performance by 7.06% (58.07% vs. 51.01%), demonstrating the effectiveness of the discrepancy learning module for instance uncertainty estimation.

IUR. In Tab. 1, IUL achieves comparable performance with the method using the random image selection strategy in the early cycles. This is because there are significant noisy instances that make the instance uncertainty inconsistent with image uncertainty. After using IUR to re-weight instance uncertainty, the performance at early cycles is improved by 5.04%∼17.09% in the first three cycles (row 4 vs. row 1 in Tab. 3). In the last cycle, the performance is improved by 1.28% (68.48% vs. 67.20%) in comparison with IUL and 1.39% in comparison with the Random method (68.48% vs. 67.09%). As shown in Tab. 3, image classification score ŷcls i is the best re-weighting metric (row 4 vs. others). Interestingly, when using 100.0% images for training, the detector with IUR outperforms the detector without IUR by 1.09% (78.37% vs. 77.28%). These results clearly verify that the IUR module can suppress the interfering instances while highlighting more representative ones, which can indicate informative images for detector training.

Hyper-parameters and Time Cost. The effects of the regularization factor λ defined in Eqs. ( 2), ( 4), ( 8) and ( 9) and the valid instance number k in each image for selection are shown in Tab. 4. MI-AOD has the best performance when λ is set to 0.5 and k is set to 10k (for ∼100k instances/anchors in each image). Tab. 5 shows that MI-AOD costs less time at early cycles than CDAL.

### 4.4. Model Analysis

Visualization Analysis. In Fig. 6, we visualize the learned and re-weighted uncertainty and image classification scores of instances. The heatmaps are calculated by summarizing the uncertainty scores of all instances. With only IUL, there exist interference instances from the background (row 1) or around the true positive instance (row 2), and the results tend to miss the true positive instances (row 3) or instance parts (row 4). MIL can assign high image classification scores to the instances of interesting while suppressing backgrounds. As a result, IUR leverages the image classification scores to re-weight instances towards accurate instance uncertainty prediction.

Statistical Analysis. In Fig. 7, we calculate the number of true positive instances selected in each active learning cycle. It can be seen that MI-AOD significantly hits more true positives in all learning cycles. This shows that the proposed MI-AOD approach can activate true positive objects better while filtering out interfering instances, which facilities selecting informative images for detector training.

## 5. Conclusion

We proposed Multiple Instance Active Object Detection (MI-AOD) to select informative images for detector training by observing instance uncertainty. MI-AOD incorporates a discrepancy learning module, which leverages adversarial Unlabeled Image IUL IUR ˆcls y

## Figures et tableaux

**Figure 1.** Comparison of active object detection methods. (a) Conventional methods compute image uncertainty by simply averaging instance uncertainties, ignoring interference from a large number of background instances. (b) Our MI-AOD leverages uncertainty re-weighting via multiple instance learning to filter out interfering instances while bridging the gap between instance uncertainty and image uncertainty. (Best viewed in color)

**Figure 2.** MI-AOD illustration. (a) Instance uncertainty learning (IUL) utilizing two adversarial classifiers. (b) Instance uncertainty reweighting (IUR) using multiple instance learning. Bigger symbols ("+" and "-") indicate larger weights. (Best viewed in color)

**Figure 3.** Network architecture for instance uncertainty learning. (a) Label set training. (b) Maximizing instance uncertainty by maximizing classifier prediction discrepancy. (c) Minimizing instance uncertainty by minimizing classifier prediction discrepancy.

**Figure 4.** Network architecture for instance uncertainty re-weighting. (a) Label set training. (b) Re-weighting and maximizing instance uncertainty. (c) Re-weighting while minimizing instance uncertainty.

**Figure 5.** Performance comparison of active object detection methods. (a) On PASCAL VOC using RetinaNet. (b) On PASCAL VOC using SSD. (c) On MS COCO using RetinaNet.

[figure sans légende identifiée] .18 56.94 64.44 67.70 69.58 70.67 72.12

**Figure 6.** Figure 7. Figure 6. Visualization of learned and re-weighted instance uncertainty and image classification score. (Best viewed in color)

**Table 1.** Module ablation on PASCAL VOC. The first line shows the result of the baseline method with random image selection. "Max Unc." and "Mean Unc." respectively denote that the image uncertainty is represented by the maximum and averaged instance uncertainty.

    10.0% samples.

**Table 2.** The effect of IUL for active image classification. Experiments are conducted on CIFAR-10 using the ResNet-18 backbone while the images are randomly selected in all cycles.

    w i Set | mAP (%) on Proportion (%) of Labeled Imgs. 5.0 7.5 10.0 12.5 15.0 17.5 20.0
    1 | ∅ 30.09 49.17 55.64 60.93 64.10 65.77 67.20
    ŷf1 i | ∅ 31.67 50.67 55.93 60.78 64.17 66.22 67.30
    1 X L 42.52 54.08 57.18 63.43 65.04 66.74 68.32
    ŷcls i | X 47.18 57.12 60.68 63.72 66.10 67.59 68.48

Table

[figure sans légende identifiée] 1 10k 47.18 57.30 64.93 67.40 69.63 70.53 71.62 0.5 10k 47.18 58.41 64.02 67.72 69.79 71.07 72.27 0.2 10k 47.18 58.02 64.44 67.67 69.42 70.98 72.06 0.5 N 47.18 58.03 63.98 66.58 69.57 70.96 72.03 0.5 10k 47.18 58.41 64.02 67.72 69.79 71.07 72.27 0.5 100 47.18 58.74 63.62 67.03 68.63 70.26 71.47 0.5 1 47.18 57.58 61.74 64.58 66.98 68.79 70.33

**Table 4.** Performance under different hyper-parameters.

**Table 5.** Comparison of time cost on PASCAL VOC.
