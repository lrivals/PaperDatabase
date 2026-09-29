---
id: arxiv-2011.10671-review-comparative-probabilistic-object-detection
title: "A Review and Comparative Study on Probabilistic Object Detection in Autonomous Driving"
year: 2020
backend: grobid
---

## Abstract

Capturing uncertainty in object detection is indispensable for safe autonomous driving. In recent years, deep learning has become the de-facto approach for object detection, and many probabilistic object detectors have been proposed. However, there is no summary on uncertainty estimation in deep object detection, and existing methods are either built with different network architectures and uncertainty estimation methods, or evaluated on different datasets with a wide range of evaluation metrics. As a result, a comparison among methods remains challenging, as does the selection of a model that best suits a particular application. This paper aims to alleviate this problem by providing a review and comparative study on existing probabilistic object detection methods for autonomous driving applications. First, we provide an overview of practical uncertainty estimation methods in deep learning, and then systematically survey existing methods and evaluation metrics for probabilistic object detection. Next, we present a strict comparative study for probabilistic object detection based on an image detector and three public autonomous driving datasets. Finally, we present a discussion of the remaining challenges and future works. Code has been made available at https://github.com/asharakeh/pod_compare.git.

Fig. 1: A conceptual illustration of probabilistic object detection in an urban driving scenario. Each object is classified with a classification probability, and its bounding box is predicted with a confidence interval. The RGB camera image is from the BDD100k dataset [18].

(especially deep learning) have been widely applied to safetycritical computer vision problems [2], efforts to improve a network's self-assessment ability, reliability and interpretability with uncertainty estimation are steadily increasing [3], [4].

In this paper, we focus on object detection, one of the most important perception problems in autonomous driving. An object detector is targeted to jointly classify and localize relevant traffic participants from on-board sensor data (e.g. RGB camera images, LiDAR and Radar points) in a frame-byframe manner. When modeling probability in object detection, we need to estimate the probability an object belongs to the classes of interest (also called semantic uncertainty as introduced in [5]), as well as the probability distribution and the confidence interval of bounding box (i.e. spatial uncertainty [5]), as shown conceptually in Fig 1 . In recent years, deep learning has become the de-facto approach in object detection, and many methods of modeling uncertainties in deep neural networks have been proposed [6]- [17]. However, to our knowledge, there is no work that provides a summary on uncertainty estimation in deep object detection, making it difficult for researchers to enter this field. Besides, existing probabilistic object detection models are often built with different network architectures, different uncertainty modeling approaches, and different sensing modalities. They are also tested on different datasets with a wide range of evaluation metrics. As a result, a comparison among methods remains challenging, as does the selection of the model that best suits a particular application.

## Contributions

In this work, we systematically review the uncertainty estimation approaches that have been applied to deep object detectors, and conduct a comparative study for autonomous driving applications. First, we provide an overview of generic uncertainty estimation in deep learning (Sec. II). We summarize four practical uncertainty estimation methods, discuss the types of uncertainty that can be modelled in perception problems, and introduce common metrics to quantify uncertainties. Next, we survey existing methods and the evaluation metrics designed specifically for probabilistic object detection (Sec. III). We then present a strict comparative study for probabilistic object detectors (Sec. IV). Based on the one-stage 2D image detector RetinaNet [19], we benchmark several practical uncertainty estimation methods on three public autonomous driving datasets, namely, the KITTI object detection benchmark [20], the BDD100k Diverse Driving Video Database [18], and the Lyft Perception Dataset [21]. In addition, we compare how uncertainties behave in RGB camera images and LiDAR point clouds, as camera and LiDAR sensors have very different sensing properties and observation noise. Finally, we present a discussion of the remaining challenges in probabilistic object detection (Sec. VI). Open source code for benchmarking probabilistic object detection is made available at: https://github.com/asharakeh/pod_ compare.git.

## II. B U E D L

This section presents background knowledge of general uncertainty estimation in deep learning. First, Sec. II-A defines the notation and problem formulation for predictive probability estimation in deep learning. Then, Sec. II-B introduces Bayesian Neural Networks (BNNs), which provide a natural interpretation of uncertainty estimation in deep learning. Based on the BNN framework, Sec. II-C decomposes predictive uncertainty into epistemic and aleatoric uncertainty, which will be widely used in this paper. Afterwards, Sec. II-D introduces four practical methods for uncertainty estimation in the literature, namely, Monte-Carlo Dropout, Deep Ensembles, Direct Modeling, and Error Propagation. Finally, Sec. II-E summarizes common evaluation metrics used in uncertainty estimation. Interested readers can also find a short summary of existing uncertainty estimation benchmarks in Appx. D.

### A. Notation and Problem Formulation

Denote a labeled training dataset of 𝑁 data pairs as D = {x 𝑛 , y 𝑛 } 𝑁 𝑛=1 , where x 𝑛 is an input data sample in the domain X, and y 𝑛 its corresponding target value in the domain Y. In classification, a target label can be one of the 𝐶 classes, 𝑦 ∈ {1, . . . , 𝐶}. In regression, a target value is usually a continuous vector with 𝐷 dimensions denoted by y ∈ R 𝐷 . In supervised learning, we aim to learn a model 𝑓 W : X → Y parametrized with weights W ∈ W from the training dataset D, where W is the domain of weights. The model maps an input sample x to its corresponding output target value y via the model output prediction ŷ. Usually, deep neural networks are interpreted as point estimators with deterministic network weights W, and provide deterministic output predictions denoted by ŷ = 𝑓 (x, W). We expand the network output definition to encompass a predictive probability distribution denoted by 𝑝(y|x, D).

### B. Bayesian Neural Networks

Bayesian Neural Networks (BNNs) [22], [23] provide a natural interpretation of uncertainty estimation in deep learning, by inferring distributions over a network's weights W. Given a data sample x, BNNs produce the predictive distribution 𝑝(y|x, D) by integrating over all values of network weights:

𝑝(y|x, D) = ∫ 𝑝(y|x, W) 𝑝(W|D)dW.(1)

In this equation, 𝑝(y|x, W) represents the observation likelihood, and 𝑝(W|D) represents the weight posterior distribution over the dataset. Modeling the observation likelihood is usually straight-forward by Direct Modeling (cf. Sec. II-D3). However, analytically calculating the posterior distribution is intractable due to its high dimensionality and multi-modality (often in a space of millions of weight parameters) [24]. Multiple techniques for generating approximate solutions of the posterior distribution have been proposed [25]- [34]. Still, it is reported that approximation techniques in BNNs are highly sensitive to hyper-parameters, and hard to scale to large datasets and network architectures [33].

### C. Epistemic and Aleatoric uncertainty

Based on the BNN framework, predictive uncertainty in deep neural networks can be decomposed into epistemic uncertainty and aleatoric uncertainty [35]. Epistemic, or model uncertainty, indicates how certain a model is in using its parameters W to describe an observed dataset, and can be expressed by 𝑝(W|D) in Eq. 1. For instance, detecting an unknown object which is not present in the training dataset is expected to show high epistemic uncertainty. Aleatoric, or data uncertainty, reflects observation noise inherent in sensor measurements of the environment, and can be modeled by 𝑝(y|x, W) in Eq. 1. For example, detecting a distant object with only sparse LiDAR reflections, or using RGB cameras during a night drive should produce high aleatoric uncertainty.

Capturing both types of uncertainty in a perception system is crucial for safe autonomous driving, as epistemic uncertainty displays the capability of a model in fitting training data, while aleatoric uncertainty reflects sensor limitations in changing environments.

In addition to object detection, which we will explicitly introduce in Sec. III, epistemic and aleatoric uncertainties have been estimated in different components of autonomous driving such as semantic segmentation [36]- [38], optical flow [39], [40], depth estimation [35], [41]- [43], visual odometry [44]- [46], image annotation [47]- [50], visual tracking [51], trajectory prediction [52]- [55] and end-to-end perception [56]- [58]. Tab. VI in the appendix lists several uncertainty estimation applications in autonomous driving. Beyond epistemic and aleatoric uncertainty, Czarnecki et al. [59] define seven sources of perceptual uncertainty to be considered for the development and operation of a perception system, which is explained in Appx. A in detail.

### D. Practical Methods for Uncertainty Estimation

In the following, we summarize four practical methods for predictive uncertainty estimation in deep learning: Monte Carlo Dropout (MC-Dropout), Deep Ensembles, Direct Modeling, and Error Propagation. MC-Dropout and Deep Ensembles are used to model epistemic uncertainty, while Direct Modeling is used to capture aleatoric uncertainty. Error Propagation can be used to capture either epistemic or aleatoric uncertainty depending on its focus.

### 1) Monte-Carlo Dropout

The MC-Dropout method proposed by Gal et al. [60] links dropout-based neural network training to Variational Inference (VI) in Bayesian Neural Networks (BNNs). They show that training a network with Stochastic Gradient Descent (SGD) with dropout is equivalent to optimizing a posterior distribution that approximates Eq. 1. The method is later extended in [61] to find the optimal dropout rate by treating the dropout probability as a hyperparameter. During test time, samples from the approximate posterior distribution are generated by performing inference multiple times with dropout enabled. Let 𝑇 be the total number of feed-forward passes with dropout, and W 𝑡 be a sample of network weights after dropout. The predictive probability can be approximated from 𝑇 generated samples as:

𝑝(y|x, D) ≈ 1 𝑇 𝑇 ∑︁ 𝑡=1 𝑝(y|x, W 𝑡 ).(2)

For classification, Eq. 2 corresponds to averaging the 𝑇 number of predicted classification probabilities, such as softmax scores. For regression, this equation can be viewed as a mixture of distribution with 𝑇 equally-weighted components.

In this case, the sample mean and variance can be used to describe the predictive probability distribution. In general, MC-Dropout provides a practical way to perform approximate inference in Bayesian Neural Netowrks (BNNs), and is scalable to large datasets and network architectures such as in image classification [47] or semantic segmentation [42], [62]. However, MC-Dropout requires multiple stochastic runs during test time, usually 10 to 50 runs as shown in [60], making it still infeasible for real-time critical systems due to high computational cost.

### 2) Deep Ensembles

The method proposed by Lakshminarayanan et al. [63] estimates predictive probability using an ensemble of networks, where the outputs from each network are treated as independent samples from a mixture model. Each network in the ensemble uses the same architecture, but is trained with randomly shuffled training data using a different initialization of its parameters. Let 𝑀 be the number of networks in an ensemble, {W 𝑚 } 𝑀 𝑚=1 their weights, and 𝑝(y|x, W 𝑚 ) a prediction from the 𝑚-th network. The predictive probability is approximated by a uniformly-weighted mixture model with 𝑀 components, given by:

𝑝(y|x, D) ≈ 1 𝑀 𝑀 ∑︁ 𝑚=1 𝑝(y|x, W 𝑚 ). (3

)

The equation is similar to Eq. 2, as MC-Dropout can also be interpreted as an ensemble of networks [63]. In practice, an ensemble of 5 networks has been shown to be sufficient to approximate predictive probabilities [63], [64]. Although easy to implement, the computation and memory costs of deep ensembles scale linearly with the number of networks both during training and inference, limiting its applicability for large network architectures, as discussed in [42].

### 3) Direct Modeling

Direct Modeling assumes a certain probability distribution over the network outputs, and uses the network output layers to directly predict parameters for such a distribution. Unlike Bayesian Neural Networks which perform marginalization over weights W (Eq. 1), Direct Modeling uses point estimates of these weights to generate the predictive probability distribution 𝑝(y|x, D) through 𝑝(y|x, W).

The most common way to estimate the classification probability of the class 𝑐 is by the softmax score 𝑝(𝑦 = 𝑐|x, W) = ŝ𝑐 , which is equivalent to a multinomial mass function. As for the regression probability, Gaussian distributions [35], [40] or Gaussian Mixture Models (GMM) [15], [65] are often used. For instance, it is often assumed that the target value 𝑦 in an one-dimensional regression problem is Gaussian distributed, given by: 𝑝(𝑦|x, W) = N 𝑦| μ(x, W), σ2 (x, W) . Here, the mean, μ(x, W), is the network standard prediction i.e. μ(x, W) = 𝑓 (x, W). The variance, σ2 (x, W), is also predicted by the network with an additional output layer.

Training the network is achieved by maximum likelihood estimates, where W are optimized to minimize the negative log likelihood 𝐿 (x, W) =log 𝑝(𝑦|x, W) . When using the softmax function for classification, 𝐿 (x, W) is widely known as the cross-entropy loss. When using the Gaussian distribution for regression, the negative log likelihood can be written as:

𝐿(x, W) = 𝑦 -μ(x, W) 2 2 σ2 (x, W) + log σ2 (x, W) 2 . (4

)

This function can be viewed as the standard 𝐿 2 loss being weighted by the inverse of the predicted variance σ2 (x, W), and regularized with the log σ2 (x, W) term. Instead of using the standard softmax with the cross-entropy loss, Kendall et al. [35] combine the softmax function with a Gaussian distribution to estimate classification uncertainty, by assuming that each element in the softmax logit vector is independently Gaussian distributed, with its mean and variance directly predicted by the network output layers (More detailed explanation can be found in Appx. B). Furthermore, several works propose to estimate higher-order conjugate priors in addition to directly predicting the output probability distributions [24], [66], [67]. Finally, Gustafsson et al. [68] use a deep neural network to directly predict the conditional target density of an energy-based model. Since Direct Modeling estimates uncertainty via single forward pass, it is much more efficient than MC-Dropout or Deep Ensembles. However, the network's output layers and the loss function need to be modified for uncertainty estimation. It has also been shown to produce miscalibrated probabilities in classification [60], [69] and regression [70].

### 4) Error Propagation

Error Propagation approximates variances (or uncertainty) in each activation layer, and then propagates variances through the whole network from input layers to output layers. For example, Postels et al. [37] view dropout and batch normalization as a noise-injection procedure to learn uncertainty during training and propose to approximate dropout error as a covariance matrix in the noisy layers. They then propagate the error through the downstream activation layers in closed-form. In this way, the method replaces the time-consuming MC-Dropout [60] using a single inference, significantly reducing the computation time. Similarly, Gast et al. [40] convert a standard activation layer such as ReLu into an uncertainty propagation layer by matching its first and second-order central moments. Due to the computational efficiency at inference and limited modifications required for training, Error Propagation appeals to practitioners with real-world applications.

### E. Uncertainty Evaluation

When evaluating the quality of uncertainty, one needs to study the probability distributions that capture this uncertainty. Evaluating predicted probability distributions has been extensively studied in the context of pure inference problems [71], [72], and more recently in the context of machine learning applications [73], [74]. Geinting et al. [75] contend that the goal of a predicted probability distribution is to maximize the sharpness around the correct ground truth target, subject to calibration. Calibration [70], [76] is a joint property of the estimated predicted distribution as well as the correct ground truth events or values that materialized, and reflects their statistical consistency [75]. In simple terms, if a well-calibrated distribution assigns a 0.8 probability to an event (e.g. recognizing cars in object detection), the event should occur around 80% of the time. Sharpness on the other hand quantifies the concentration of the predictive distribution around the true materialized ground truth target and is a property of the predictive distribution only. As an example, if the correct ground truth class is "car", the predicted probability distribution should ideally assign a probability of 1 to the car category.

In the context of machine learning, good predicted probability distributions need to be sharp, but ideal predicted probability distributions should be both sharp and well-calibrated [75].

### 1) Measuring Calibration

A calibration plot is a common tool to evaluate the calibration of distributions generated from a probabilistic model. It draws the predicted probability from a model on the horizontal axis and its corresponding empirical probability on an evaluation dataset on the vertical axis, as shown in Fig. 2. A wellcalibrated deep network produces a diagonal line. However, Guo et al. [69] and Kuleshov et al. [70] have empirically identified the over-or under-confident uncertainty in many classification and regression problems, and propose propose uncertainty recalibration techniques improve uncertainty estimation.

To draw a calibration plot for an evaluation dataset with the size 𝑁 𝑒𝑣 𝑎𝑙 , the network needs to run probabilistic predictions for all data samples. The predicted probabilities from the

### Empirical probability

### Perfectly calibrated

Under-confident Over-confident Fig. 2: A calibration plot. The horizontal axis represents the predictive probability, and the vertical axis the empirical probability. A miscalibrated network can make over-confident or under-confident predictions, as indicated in blue and orange curves, respectively.

network, denoted by 𝑝, are partitioned into 𝑇 intervals (or quantiles), i.e. 0 < 𝑝 1 < ... < 𝑝 𝑡 < ... < 1. They correspond to the values in the horizontal axis of Fig. 2. In each interval, the normalized empirical frequency denoted by p𝑡 is calculated by comparing predictions with ground truths. An empirical frequency corresponds to a value in the vertical axis of Fig. 2. Drawing the calibration plots for regression probability distributions is more complicated, requiring the evaluation of cumulative distribution functions. We refer the reader to the work of Kuleshov [70] for a detailed description of how to draw calibration plots for regression predictive distributions.

From the calibration plot we can derive several evaluation metrics. For example, Expected Calibration Error (ECE) [69] measures the weighted absolute error between the actual calibration curve and the optimal calibration curve (i.e. the diagonal line). A ECE score is given by: ECE = 𝑇 𝑡=1 𝑁 𝑡 𝑁 𝑒𝑣 𝑎𝑙 | 𝑝 𝑡 -p𝑡 |, where 𝑝 𝑡 is the predicted probability from a network, p𝑡 the empirical frequency, and 𝑁 𝑡 the number of samples in the 𝑡-th interval, 𝑇 𝑡=1 𝑁 𝑡 = 𝑁 𝑒𝑣 𝑎𝑙 . An ECE score ranges between [0, 1] with smaller values indicating better uncertainty calibration performance. A regression alternative to ECE that can be extracted from regression calibration plots has been presented by Kuleshov in [70]. Besides ECE, Average Calibration Error (ACE) and Maximum Calibration Error are also common metrics. ACE calculates the absolute error averaged over all intervals equally, while the Maximum Calibration Error finds the maximum absolute error in all intervals. Finally, Kumar et al. [76] proposed the Marginal Calibration Error (MCE) metric, as an extension of ACE. While ACE considers the uncertainty calibration quality only on an object ground truth category, MCE measures the uncertainty of a classifier's predicted distribution over all categories of interest.

### 2) Proper Scoring Rules

Unfortunately, measuring calibration is not enough to determine the quality of output probability distributions; we are required to also evaluate its sharpness, which we have described as the concentration of probability mass assigned by output probability distributions around the correct ground truth targets. We can evaluate both calibration and sharpness of probability distributions by using proper scoring rules. A scoring rule 𝑆( 𝑝(y|x, D), y 𝑛 ) is a function that maps a predicted probability distribution and the correct ground truth target to single scalar value. A lower value of a scoring rule usually signifies predicted probability distributions that are closer to the data generating distribution from which the ground truth target is sampled. A proper scoring rule is a scoring rule that is only minimized if the predicted probability distribution is exactly equal to the distribution that generated the correct ground truth target. Note that we do not need access to the "theoretical" data generating distribution to compute a scoring rule, we only require a single sample from this distribution which is readily available in dataset D. In addition, proper scoring rules have been shown in [77] to be sum of terms relating to calibration as well as sharpness, and as such proper scoring rules are capable of considering both when evaluating predictive distributions [78]. For more thorough arguments on the importance of using proper scoring rules for evaluating predicted probability distributions, we refer the reader to [74], [75], [77]- [79]. We now present two common proper scoring rules used in machine learning literature for evaluating predicted probability distributions [63], [64]. Negative Log Likelihood (NLL). NLL is a proper scoring rule to measure the quality of predicted probability distributions of a test dataset with 𝑁 𝑡𝑒𝑠𝑡 data points. NLL is calculated as:

NLL = -1 𝑁 𝑡𝑒𝑠𝑡 𝑁 𝑡𝑒𝑠𝑡 𝑛=1 log 𝑝(y 𝑛 |x 𝑛 , D)

, where x 𝑛 is a test data point, and y 𝑛 its corresponding ground truth label. NLL ranges in (-∞, +∞), with a lower NLL score indicates a better fitting predictive distribution for that specific ground truth label. NLL has been extensively used in machine learning literature for evaluating output probability distributions for regression [63] and classification [64] tasks. Brier Score (BS). A Brier Score [71] is another common proper scoring rule used to measure the quality of output probability distributions specifically in classification. The Brier score is calculated by the squared error between a predictive probability from the network and its one-hot encoded ground truth label. Given 𝑁 𝑡𝑒𝑠𝑡 number of test data samples, for a classification problem with 𝐶 number of classes, a Brier Score is given by: BS = 1 𝑁 𝑡𝑒𝑠𝑡 𝑁 𝑡𝑒𝑠𝑡 𝑛=1 𝐶 𝑐=1 ( ŝ𝑛,𝑐 -𝑦 𝑛,𝑐 ) 2 , where ŝ𝑛,𝑐 is a predicted classification score for the 𝑐-th class, such as the softmax score, and 𝑦 𝑛,𝑐 is ground truth label ("1" if the ground truth class is 𝑐 and "0" otherwise). Brier scores range between 0 and 1, with lower values indicating better uncertainty estimation. We will use NLL, Brier Score, alongside calibration errors for evaluating both regression and classification probability distributions of in-distribution detection results predicted by our probabilistic detectors in Sec. IV-D. It is noteworthy to mention that there exist several non-proper scoring metrics to measure the magnitude of uncertainty, such as Mutual Information, Shannon Entropy, and Total Variance. Interested readers can find additional non-proper scoring metrics in Appx. C.

## III. P O D

As defined in [5], probabilistic object detection aims to accurately detect objects, while estimating the semantic (category classification) and spatial (bounding box regression) uncertainties in each detection. In this section, we provide a systematic summary of probabilistic object detection using deep learning approaches. We start with a background introduction of generic object detection (Sec. III-A), and then summarize each probabilistic object detection method in detail (Sec. III-B). Afterwards, we list several common evaluation metrics and discuss their properties (Sec. III-C).

Finally, we briefly summarize sensing modalities and use cases for existing probabilistic object detection methods in Sec. III-D and Sec. III-C, respectively.

### A. Introduction

In general, state-of-the-art object detectors are not designed to capture reliable predictive uncertainty. They predict bounding box regression variables without any uncertainty estimation, and usually classify objects with softmax scores, which may not necessarily represent reliable classification uncertainties (as discussed in [60]). As a result, most object detectors are deterministic. They only predict what they have seen, but not how uncertain they are about it. In this regard, probabilistic object detectors are targeted to predict reliable uncertainties both in object classification and bounding box regression tasks.

### B. Methodology

Probabilistic object detectors usually extend the network architectures described in the previous section (Sec. III-A) to predict probability distributions describing the category as well as the bounding box of objects in the scene [5]. Fig. 3 provides an overview of the general building blocks used to perform probabilistic object detection, which mainly consists of a base network, a detection head, and a post-processing stage. Note that both one stage and two stage approaches can be extended to predict uncertainty in a similar manner, so as 2D and 3D object detection. Therefore, we do not distinguish between the two for the remainder of this paper.

A base network (Fig. 3, Left) maps sensor inputs to highlevel feature maps, which will be further processed by a detection head. Probabilistic object detectors usually adapt base networks from well-studied deterministic object detectors to capture epistemic uncertainty using Deep Ensembles or MC-Dropout [8], [80]- [83]. Typical base networks include VGG [84], ResNet [85], Inception [86], to name a few. A detection head (Fig. 3, Middle) takes the feature maps from the base network as inputs and predicts probabilistic detection outputs. Deep Ensembles [80], [82] and MC-Dropout [6], [7], [13], [17], [81]- [83] are usually used to model epistemic uncertainty in the detection head. On the other hand, the Direct Modeling approach, introduced in Sec. II, models aleatoric uncertainty by introducing additional output layers to the detection head for estimating the variance of output bounding boxes [8], [9], [11]- [17], [31], [80], [81], [83], [87]- [91] or the variance of output logits [12], [87]. It has to be noted that the variance of the logits does not need to be estimated for generating a categorical distribution describing object categories; any detector that employs softmax as an output layer while learning with cross-entropy loss captures aleatoric uncertainty in classification. Finally, a post-processing stage is used to suppress or merge redundant detection outputs as is common in deterministic object detectors. Tab. I summarizes the post-processing step in state-of-the-art probabilistic object detectors. The majority of methods employ the standard Non-Maximum Suppression (NMS), because it is a common component from deterministic object detectors, upon which probabilistic object detectors are built. Other methods [15], [16], [88] modify NMS to take into account spatial uncertainty when deciding which redundant detection to remove,

Clustering Redundancy Elimination Logit Mean Logit Var Bbox Mean Bbox Var Preprocessing • MC-Dropout • Ensembles • Direct Modeling • MC-Dropout • Ensembles • NMS • Sample Statistics • Gaussian Mixture • Bayesian Inference

Sampling and Softmax [0.9, 0.1] [0.9, 0.1] Fig. 3: Illustration of the key building blocks usually present in state-of-the-art probabilistic object detectors, including the base network, detection head and post-processing stages. A list of possible variants of each building block is also presented bellow the architectural diagram. The output detections on 2D images are visualized as category probabilities (orange), a bounding box mean (red), and the 95% confidence iso-contours of the bounding box corner covariance matrices (green).

or replace NMS with Bayesian Inference [13] to include information from all redundant detection outputs. Finally, [6], [7], [87] take the benefits of redundant detection outputs to compute sample statistics of probability distributions, instead of directly-modeling the output probability and discarding redundant detections. The following section summarizes each state-of-the-art probabilistic object detector in detail. They are grouped based on what kinds of uncertainty are modelled, namely, epistemic uncertainty, aleatoric uncertainty, or both. Tab. I provides an overview of all methods we have reviewed.

### 1) Probabilistic Object Detectors with Epistemic Uncertainty

Several works model epistemic uncertainty with the MC-Dropout approach. Miller et al. [6] estimate the classification epistemic uncertainty by modifying SSD [92] deterministic backend. SSD's detection head is modified with dropout layers to generate samples during test time with dropout inferences. At the post-processing step, output samples from multiple stochastic MC-Dropout runs are gathered, after performing the NMS operation on each stochastic run independently. Those redundant detections from multiple inferences are then clustered using spatial affinity. For every cluster, the categorical probability distribution of a single object is modeled using Eq. ( 2). The same architecture is used in [7] for studying the effect of various clustering techniques on the quality of epistemic uncertainty in the object classification task. It was concluded that simple clustering techniques such as Basic Sequential Algorithmic Scheme (BSAS) provides higher quality uncertainty values, when compared to more complicated clustering techniques such as the Hungarian algorithm. The successive work by Miller et al. [82] avoid the clustering process when computing classification epistemic uncertainty. They build two detectors based on the Faster-RCNN [93] and SSD [92] architectures, each generates multiple samples at a certain anchor grid location by the MC-Dropout inference. For each detector separately, samples are used to compute the mean of the softmax classification output at every anchor location using Eq. 2 or Eq. 3. Uncertainty is then modeled using the entropy of the probability estimates from the softmax classification output. Finally, redundant detections are merged via the standard NMS operation. Experimental results show that deep ensembles outperform the MC-Dropout from a single model on the two studied architectures, in terms of the predictive uncertainty estimation. Finally, Feng et al. [10] use MC-Dropout [60] and Deep Ensemble [63] methods to estimate epistemic uncertainty for the category classification only. The classification uncertainty is employed to train a 3D LIDAR object detector in an active learning framework. Dropout layers are used only in the detection head of the proposed 3D detection architecture, and the standard NMS operation is used at the post-processing step.

### 2) Probabilistic Object Detectors with Aleatoric Uncertainty

Most probabilistic object detectors use the Direct Modeling approach introduced in Sec. II to estimate aleatoric uncertainty. These detectors are often built following four steps 1) selecting a deterministic object detector as the basic network, 2) assuming a certain probability distribution in its outputs, 3). using additional layers at the detection head to regress probability parameters, and 4) training the modified detector by incorporating uncertainty in the loss function. The Direct Modeling approach has been used in various object detection architectures, including SSD [87], Faster-RCNN [9], [12], [14], FCOS [94], Point-RCNN [89], and PIXOR [11]. The softmax function is widely used to estimate classification probability, which corresponds to a multinomial mass function. Le et al. [87] and Feng et al. [12] assume a Gaussian distribution on the logit vectors, which is then transformed to a categorical distribution through the monte-carlo sampling process described in [35]. As for the regression probability, a majority of works assume that each bounding box regression variable is independent and follows a simple probability distribution, such as a univariate Gaussian distribution, Laplace distribution, or a combination of both (Huber mass function) [9], [13], [15], [88]. The regression variables usually include the bounding box centroid positions, extents (length, width, height), and orientations. Though this probability assumption is simple and straight-forward, it ignores correlations among regression variables, and may not fully reflect the complex uncertainties of bounding boxes, especially when objects are occluded. Instead, Pan et al. [89] transform the regression variables back to the eight-corner representation for 3D bounding boxes, and directly learn the corner uncertainty; Meyer et al. [15] place a mixture of Gaussians on each regression variable; Harakeh et al. [13] learn a multivariate Gaussian distribution with the full covariance matrix for regression variables. The recent work by He et al. [95] propose a more generic probability distribution which considers both correlations and multi-modal behaviours. They use a multi-variate mixture of Gaussians to describe 2D bounding boxes, and show its superiority to univariate Gaussian, multi-variate Gaussian, and a univariate mixture of Gaussian.

Training probabilistic object detectors to predict aleatoric uncertainty is usually achieved by minimizing the Negative Log Likelihood (NLL), resulting in the well-known crossentropy loss for classification, and the attenuated regression loss (Eq. 4) for bounding box regression with Gaussian distributions. In contrast, [14], [16] introduce a probability distributions related to the ground truth bounding box parameters, and minimize the Kullback-Leibler divergence between the predictive probability distribution and the prior distribution. In this way, the predictive uncertainty is regularized with the groundtruth probability distribution, which results in more stable training and improved detection when compared to standard negative log likelihood loss [16], [96].

In addition to the standard Non-Maximum Suppression (NMS) operation, some works leverage aleatoric uncertainty at the post-processing step to merge duplicate detections. For instance, Meyer et al. [15] propose to group detections using mean-shift clustering over corners, and combine the bounding box uncertainty and classification scores in an uncertaintyaware NMS frawework. Similarly, Choi et al. [88] design a detection criterion that considers both regression and classification uncertainty. This criterion is used to rank detections while performing the standard NMS.

Instead of the Direct Modeling method, a unique approach based on output redundancy is proposed in [87] to model aleatoric uncertainty for both category classification and bounding box regression. This output redundancy method replaces the standard NMS with spatial clustering, and uses the Intersection-Over-Union (IOU) metric as a measure for detection affinity. Two probability distribution describing each output detection can then be generated by computing the sample mean of the softmax output for the category, and the sample mean and variance of cluster members for the output bounding box. Though the output redundancy method has been shown in [13] to produce lower quality uncertainty estimates than the Direct Modeling method (measured with PDQ), it is time-efficient, and requires only small modifications to the original deterministic detection network.

### 3) Probabilistic Object Detectors with both Aleatoric and Epistemic Uncertainties

Aleatoric and epistemic uncertainties are jointly estimated mainly by the Direct Modeling approach together with the MC-Dropout or Deep Ensembles approaches. Given the detection samples from 𝑇 stochastic runs of dropout inference (or 𝑀 models in an network ensemble), and assuming that bounding boxes are Gaussian distributed, the mean and variance of a bounding box regression variable can be computed by an uniformly-weighted Gaussian mixture model. Using the same notation from Sec. II-A, we have:

μ(x) = 1 𝑇 𝑇 ∑︁ 𝑡=1 μ(x, W 𝑡 ) (5) σ2 (x) = σ2 𝑒 (x) + σ2 𝑎 (x) (6) σ2 𝑒 (x) = 1 𝑇 𝑇 ∑︁ 𝑡=1 μ(x, W 𝑡 ) 2 -μ(x) 2 (7) σ2 𝑎 (x) = 1 𝑇 𝑇 ∑︁ 𝑡=1 σ2 (x, W t )(8)

where μ(x, W 𝑡 ) = 𝑓 (x, W 𝑡 ) and σ2 (x, W 𝑡 ) are the predicted mean and variance of the bounding box or classification logit vector outputs of sample 𝑡 ∈ [1 . . .𝑇]. Furthermore, σ2 𝑒 (x) is the epistemic component of uncertainty, and is estimated as the sample variance using 𝑇 output samples, and σ2 𝑎 (x) is the aleatoric component of uncertainty, and can be computed as the average of 𝑇 predicted variance estimates σ2 (x, W 𝑡 ). Note that the final mean μ(x) and variance σ2 (x) do not depend on the weights W, because this variable is marginalized using averaging over 𝑇 samples. For more details on the uniformlyweighted Gaussian mixture model in Eq. ( 6)-( 8), we refer the reader to [63]. While all existing works use the output layers to directly model aleatoric uncertainty, they are different in epistemic uncertainty estimation. For example, Feng et al. [8] add dropout layers and perform multiple inferences only in the detection head of a Faster-RCNN object detector to estimate uncertainty for both category and bounding box of objects in the scene. Wirges et al. [17] follow the same network metaarchitecture, and study the effect of adding dropout layers in either the base network or the detection head. Harakeh et al. [13] modify a 2D image detector based on RetinaNet [19], and incorporate MC-Dropout in the detection head. Kraus et al. [81] extend a Yolov3 network, and add dropout inference after each convolutional layer in both the base network and the detection head. As for the post-processing step, [8], [81], [97] use standard NMS. Harakeh et al. [13] replace it with Bayesian inference, which combines all information from redundant detections to generate the final output. Prior to the Bayesian inference step, a Gaussian mixture model is used to fuse epistemic and aleatoric uncertainty estimates per anchor. This method is shown to provide a large increase in uncertainty quality compared to the methods using standard NMS.

### C. Evaluation Metrics

Based on the papers reviewed, there seems to be little agreement on how to evaluate probabilistic object detectors. Tab. I lists the evaluation metrics for each probabilistic object detection method in the literature, where it can be seen that each method uses different evaluation metrics, ranging from simple true positive and false positive counts [87] to complex metrics such as Probability-based Detection Quality (PDQ) [5]. The following section summarizes the common evaluation metrics, and discusses their properties when evaluating probabilistic object detection. [88] 2019 C BDD [18], KITTI [20] A Direct Modeling Uncertainty-aware NMS AP Feng et al. [11] 2019 L KITTI [20], NuScenes [

### 1) Precision, Recall and the F1-Score

In the context of object detection, only predictions above a predefined classification score threshold, 𝛿 𝑐𝑙𝑠 , are considered for evaluation. They are further divided into True Positives (TP) and False Positives (FP), based on their Intersection over Union (IOU) scores with ground truth objects. Detections above a certain pre-defined IOU threshold, 𝛿 𝑖𝑜𝑢 , are considered as True Positives if they share the same class labels as the ground truth objects. Detections that are misclassified, or have an IOU below the 𝛿 𝑖𝑜𝑢 , are considered False Positives. False Negatives (FN) are further defined as the ground truth bounding boxes, which are either missed or not associated with predictions due to low IOU scores. The counts of TP and FP were used in [87] to evaluate their proposed probabilistic object detector. TP and FP scores were also used to construct the Receiver Operating Characteristic (ROC) curves in [7], [90]. Based on TP, FP, and FN, one can derive Precision, Recall, and the F1-Score as: Precision = TP/(TP + FP), Recall = TP/(TP + FN), F1-Score = 2 • Precision • Recall/(Precision + Recall). Precision, recall and F1 metrics are used in [6], [9] to estimate probabilistic object detector performance. One major issue of the above-mentioned evaluation metrics is that they do not take into account the values of the predicted uncertainty when determining if a detection is correct. As an example, a bounding box is considered correct if it achieves an IOU ≥ 𝛿 𝑖𝑜𝑢 with a groundtruth box, a rule that does not depend on the bounding box's predicted uncertainty in any way, rendering the uncertainty prediction irrelevant to the evaluation.

### 2) Mean Average Precision

Average Precision (AP) was proposed by Everingham et al. [102] to evaluate the performance of object detectors. It is defined as the area under the continuous precision-recall (PR) curve, approximated through numeric integration over a finite number of sample points [102]. Mean AP (mAP) is the average of all AP values computed for every object category found in the test dataset. It can also be averaged across multiple IOU thresholds 𝛿 𝑖𝑜𝑢 ∈ [0.5, . . . , 0.95] as proposed in [98], a measure referred to as COCO mAP. Though mAP is the standard evaluation metric in object detection, it does not take the predictive uncertainties into account. In fact, if two probabilistic object detectors predict bounding boxes with the same mean values but wildly different covariance matrices, they will have the same mAP performance. Nevertheless, the majority of recent work on probabilistic object detection [9], [12], [14]- [17], [88], [90], [91], [94] still use mAP as the only metric to provide a quantitative assessment of their proposed methods, emphasizing a secondary effect of accuracy improvement when integrating probabilistic detection methods, instead of focusing on the correctness of the output distribution. This leads to the need of better and more consistent metrics, which we highlight in Sec. V.

### 3) Probability-based Detection Quality

Hall et al. [5] proposed the Probability-based Detection Quality (PDQ) as a metric to measure the quality of 2D probabilistic object detection on images. PDQ was later used by [13], [82] for uncertainty evaluation. PDQ is designed to jointly evaluate semantic uncertainties and spatial uncertainties in image-based object detection. The semantic uncertainties are evaluated by matching the predicted classification scores with the ground truth labels for each object instance in images. The spatial uncertainties are encoded by covariance matrices, by assuming a Gaussian distribution on the top-right or the bottomleft corner of a bounding box. The optimal PDQ is achieved, when a predicted probability correlates the prediction error, for example, when a large spatial uncertainty correlates with an inaccurate bounding box prediction. PDQ assigns every ground truth an optimal corresponding detection using the Hungarian algorithm, removing the dependency on IOU thresholding that is required for mAP. Furthermore, PDQ measures the probability mass assigned by the detector to true positive detection results, and is evaluated at a single classification score threshold requiring practitioners to filter low scoring output detection results prior to evaluation. PDQ assumes 2D Gaussian corner distributions and cannot evaluate methods assuming a Laplace distribution such as [15], [16]. Finally, because of how the spatial quality is defined, PDQ can only be computed for 2D probabilistic detection results defined in image space, with no straightforward extensions available for 3D probabilistic object detectors.

### 4) Minimum Uncertainty Error

The Uncertainty Error (UE) was first proposed by Miller et al. [7] to evaluate probabilistic object detectors. UE can be thought of as the probability that a simple threshold-based classifier makes a mistake when classifying output detections into true positives and false positives using their predicted spatial uncertainty estimates. UE ranges between 0 and 0.5, and as the uncertainty error approaches 0.5, using the predicted uncertainty estimates to separate true positives from false positives is no better than a random classifier. The best uncertainty error achievable by a detector over all possible thresholds is called the Minimum Uncertainty Error (MUE), and is used to compare probabilistic object detectors in [7], [13]. Similar to mAP, MUE requires an IOU threshold 𝛿 𝑖𝑜𝑢 to determine which detections are counted as true positives, and is therefore threshold-dependant. Furthermore, MUE is not affected by the scale of uncertainty estimates. In other words, rescaling or shifting the uncertainty values for all detections with the same value results in a constant MUE score. Therefore, MUE is only capable of providing information on how well the estimated uncertainty can be used to separate true positives from false positives, but not on the quality of estimated uncertainty.

### 5) Jaccard IoU

Recently, Wang et al. [90] propose Jaccard IoU (JIoU) as a probabilistic generalization of IoU. Unlike IoU which simply compares the (deterministic) geometric overlap between two bounding boxes, JIoU measures the similarity of their spatial distributions. Such distributions can be predicted by probabilistic object detection networks, or by inferring the uncertainties inherent in ground truth labels (which serve as the "references of probability distribution") [90]. In fact, JIoU simplifies to IoU when bounding boxes are assumed to follow simple uniform distributions. Similar to IoU, JIoU ranges within [0, 1]. It is maximized only when two bounding boxes have the same locations, same extents, as well as same spatial distributions. In general, JIoU provides a natural extension of IoU to evaluate probabilistic object detection. It also considers ambiguity and uncertainty inherent in ground truth labels, which are ignored by other evaluation metrics such as mAP and PDQ. However, a separate model is needed to approximate ground truth spatial uncertainty in the labeling process, which has only been proposed for LiDAR point cloud [90], [110]. Therefore, the use of JIoU is limited to evaluating LiDARbased probabilistic object detection to date.

### 6) Proper Scoring Rules

To our surprise, none of the previous work on probabilistic object detectors use proper scoring rules for evaluating the quality of their predicted probability distributions. This observation was also noted in the recent work of Harakeh and Waslander [111], where it was argued that proper scoring rules are essential for a theoretically sound evaluation of predicted distributions from probabilistic object detectors. It was also shown in [111] that mAP, MUE, and PDQ are not proper scoring rules. For our experiments in Sec. IV-D, we will use NLL as a proper scoring rule for evaluating the quality of predicted category and bounding box probability distributions.

### D. Sensor Modalities

Different sensors have different sensing properties and observation noises, and thus can affect the behaviours of aleatoric uncertainty in probabilistic object detection. Most studies to date employ LiDARs [8]- [11], [15]- [17], [80], [89] and RGB cameras [6], [7], [13], [14], [65], [81]- [83], [87], [105] in probabilistic object detection. Only Dong et al. [91] propose to model uncertainty in radar sensors. The LiDAR-based networks often deal with 3D detection for single object class or a few object classes, such as "Car", "Cyclist" and "Pedestrian". In comparison, the camera-based approaches focus on the multi-class 2D detection with more diverse classes. For example, Harakeh et al. [13] evaluate 2D probabilistic object detection with ten common road scene object categories in the BDD dataset [18], as well as 80 object categories in the COCO dataset [98].

### E. Applications and Use Cases of Predictive Uncertainty

The behaviours of epistemic and aleatoric uncertainties in a network are studied in [8], [17], [81], [83]. These works verify that epistemic uncertainty is related to the detections different from the training samples (open-set detections), whereas aleatoric uncertainty reflects complex noises inherent in sensor observations such as distance and occlusion. In addition, Bertoni et al. [83] study the task ambiguity in depth estimation with monocular images, and Wang et al. [90] study the uncertainty inherent in ground truth labels for LiDARbased object detection. Epistemic uncertainty is applied to detect out-of-distribution (OOD) objects in [6]. They find that thresholding the classification uncertainty captured by MC-Dropout reduces detection errors for OOD objects when compared to the standard softmax confidence. Epistemic uncertainty is also used in [10] to select unseen samples in an active learning framework, in order to train LIDAR 3D object detectors with minimal human labeling effort. Aleatoric uncertainty is mainly used to improve detection accuracy. This can be achieved by directly modeling uncertainty in the training loss (e.g. the attenuated regression loss shown in Eq. 4) [9], [12], [14], [89], such that networks learn to handle noisy data and enhance the robustness. It can also be achieved by incorporating uncertainty in the post-processing step when merging duplicate detections. For example, Choi et al. [88] rank detections during NMS based on location uncertainty in addition to classification scores. Meyer et al. [15] adapt the IoU threshold when merging detections to their location uncertainty instead of a pre-defined value for all detections. Finally, thresholding aleatoric uncertainty has been shown to effectively remove False Positive samples in [87].

## IV. C S

A major challenge for new researchers and practitioners entering the probabilistic object detection domain is the lack of a consistent benchmark among methods presented in literature. This problem is evident when looking at Tab. I, where one can see that it is uncommon for state-of-the-art methods to use the same dataset and evaluation metric combinations, leading to difficulty in determining which method works best for autonomous driving. In this section, we attempt to alleviate this problem by performing a comparative study of the performance of common modifications described in Sections II and III that are used to extend deterministic object detectors to predict probability distributions. By using the same base network, datasets, and multiple evaluation metrics, we aim to have a controlled setup to perform a fair comparison. Specifically, we focus on 2D image-based detection for seven object categories. All networks are trained on the large-scale BDD100K dataset [18], and evaluated on the BDD100K, KITTI [20], and Lyft [21] The same setting has been implemented in [8]. BayesOD + Dropout performs MC-Dropout during inference, and then associates detections by a Gaussian Mixture Model to fuse aleatoric and epistemic uncertainty estimates according to Eq. 5 and Eq. 6. This method has been implemented previously in [13].

Additionally, we train independent Loss Attenuation models to construct deep ensembles [63]. We provide two implementations to fuse detections from ensemble results: Pre-NMS Ensembles fuse detections before the NMS step, and Post-NMS Ensembles performs data association and fusion after the NMS step. These ensemble + loss-attenuation approaches have not been attempted in literature, and can be considered a direct application of the uncertainty estimation mechanisms in [63] to the object detection problem.

### B. Experimental Setup

Recent work on evaluating uncertainty estimates of deep learning models for classification tasks [64]

### C. Training and Inference

For all probabilistic object detectors mentioned above, we follow the training setup proposed in the original RetinaNet paper [19], using the authors' original open source implementation provided by the Detectron2 [112] 2D object detection library. More specifically, we use RetinaNet with a Resnet-50 backbone and a feature pyramid network (FPN). We train all models on the BDD training dataset split using a batch size of 4 for 90𝑘 iterations using stochastic gradient descent with 0.9 momentum. We use a base learning rate of 0.0025 which is dropped by a factor of 10 at 60, 000 and then at 80, 000 iterations. For methods requiring dropout, the dropout rate of 0.1 is selected. We find out that using higher dropout rates resulted in up to 10% drop in mAP when compared to the original RetinaNet model. During inference, we use an NMS threshold of 0.5 for methods requiring NMS. For methods requiring data association, we use the Basic Sequential Algorithmic Scheme (BSAS) with a spatial affinity threshold of an IOU of 0.9 as recommended in [7]. For methods requiring dropout, we perform 10 stochastic dropout runs, as suggested by [35]. Since the deep ensemble method is computationally very expensive, we use an ensemble of 5 independently trained but identical models, the minimum number recommended in [63].

### D. Experimental Results and Discussions

This section shows the key experimental results and findings from our proposed probabilistic object detectors. We first summarize the evaluation results in scenarios with and without dataset shift, and then list our findings with in-depth discussions.

### General Results and Evaluation Metrics

Tab. III presents the results of our comparative experiments on BDD validation data split without dataset shift, where metrics are averaged over the seven dynamic object categories of interest. We quantify the performance of probabilistic object detection using the mean Average Precision (mAP) Even though we train our probabilistic object detectors using BDD data, probabilistic object detectors are seen to have lower NLL scores on KITTI than on the BDD validation dataset, implying higher confidence in correct detections. However, Fig. 5 (left) shows that the classification marginal calibration error increases to similar values on both KITTI and Lyft when compared to the marginal calibration error on the BDD validation set. We conclude that although our probabilistic object detectors provide sharper categorical distributions on KITTI compared to BDD, the distributions of KITTI detections are worse calibrated than those of BDD detections. Fig. 6 (left) also shows that the classification minimum uncertainty error follows the same trend as the classification Negative Log Likelihood in Fig. 4 (left) for all evaluated probabilistic object detectors. Regarding on the uncertainty estimation in regression, the right plots from Fig. 4, Fig. 5, and Fig. 6 show that regression metrics have little difference under dataset shift. The reason for this phenomenon might be that we only evaluate well-localized regression outputs, where regressed bounding boxes are required to achieve an IOU ≥ 0.7 with ground truth boxes.

Finally, looking at the runtime of each probabilistic object detector in the last column of Tab. III, we notice that all probabilistic extensions necessarily introduce a drop in frame rate when compared to deterministic RetinaNet. However, the drop introduced by methods that estimate aleatoric uncertainty such as Loss Attenuation is much lower than the drop introduced by parameter-sampling methods that estimate epistemic uncertainty (MC-Dropout and Deep Ensembles).

### Comparison of each method and discussions

In the following, we compare each probabilistic object detection methods in detail, and highlight the most prominent takeaways from our comparative studies. We would like to note that unless stated otherwise, conclusions made in this section are specific to our experimental setup, where we used a single-stage probabilistic object detector that is trained on autonomous driving datasets. We leave a more general comparative study on 3D object detection and LiDAR point cloud as an interesting future work.

1. Using mAP as the only evaluation metric is not sufficient for quantifying the quality of predicted uncertainty in probabilistic object detectors. It is important to emphasize this point due to the widespread practice of using only mAP as an evaluation metric when comparing state-of-the-art probabilistic object detection (See Tab. I). mAP is clearly not related to the quality of uncertainty estimates provided by probabilistic object detectors, a quality that can be quantitatively observed in Tab. IV. In this Output Redundancy are two orders of magnitude larger than all other implemented probabilistic detectors. This observation is consistent when looking at results under dataset shift in Fig. 4, where regression NLL values of Black Box and Output Redundancy are seen to be around ∼ 10 3 on BDD, KITTI, and Lyft data while the remaining probabilistic detectors have a regression NLL values that is closer to 10 1 . In addition, Fig. 5 shows that the regression calibration error of both Black Box and Output Redundancy is around 0.04, on par with the best calibrated method, BayesOD, on the BDD dataset. However, the regression calibration error is seen to increase as the magnitude of the dataset shift increases, where Black Box and Output Redundancy become the methods with the highest regression calibration error on the Lyft dataset.

Tab. II shows that the common design decision in both Black Box and Output Redundancy is the lack of Direct Modeling of uncertainty in their detection head. Instead, both Black Box and Output Redundancy methods use redundant output detections to compute estimates of the sample covariance for regression output. Theoretically, a sample covariance matrix in would require 2 independent output boxes to be estimate, and much more if this estimation is to be reliable. In addition, sample covariance estimates are highly sensitive to outliers [113]. Spatial clustering approaches used by the Black Box and Output Redundancy by definition need to sacrifice localization accuracy to obtain larger cluster sizes, increasing the probability of having outliers as cluster members. The Black Box method uses a low number of redundant boxes that are clustered after the non-maximum suppression (NMS) stage for spatial uncertainty estimation, which is seen in Table III as a higher regression NLL than that of Output Redundancy. On the other hand, Output Redundancy uses a large number of redundant output boxes collected before NMS, resulting in a better regression NLL at the expense of a much worse classification NLL, because low scoring detections are included in averaging their classification scores. For these reasons, we recommend the Direct Modeling approach for explicitly estimating the uncertainty of regressed bounding boxes when designing probabilistic object detectors.

#### 3. Estimating classification variance using Loss Attenuation offers no improvement in the quality of predictive uncertainty over baseline classification from deterministic

RetinaNet. Unlike the benefits offered by directly modeling the spatial uncertainty, we found little benefits from modeling the classification variance using the formulation proposed by Kendall et al. [35] (and introduced in Sec. II-D3). Tab. III shows that methods that explicitly estimate the variance of class logit vectors output by the network prior to the softmax output layer, such as Loss Attenuation, have the same classification NLL scores as the vanilla network softmax classification output distribution when tested with no dataset shift. Under dataset shift, modeling the variance parameters for the logit vector results in mixed results when looking at NLL in Fig. 4, where Loss Attenuation showing a lower NLL value on the KITTI dataset but higher NLL on the Lyft dataset when compared to deterministic RetinaNet. On the other hand, Fig. 5 and6 show that Loss Attenuation does have a lower classification calibration error and a lower classifica- tion minimum uncertainty error (MUE) on all three datasets when compared to deterministic RetinaNet. It should be noted that the improvement in performance observed using Loss Attenuation under domain shift is not substantial enough to validate the modifications to deterministic RetinaNet required to enable Direct Modeling of classification uncertainty. As a conclusion, we find that Direct Modeling of the variance of the logit vectors does not offer improvement over learning with cross-entropy in the deterministic RetinaNet model.

### Classification Regression

### Classification Regression

### Classification Regression

#### 4. Bayesian inference provides better spatial uncertainty

qualities when compared to standard NMS. This phenomenon has been previously shown in [13], which employs Bayesian inference to fuse information from cluster members instead of selecting the detection with the highest score in the standard NMS. Tab. II shows that BayesOD follows the same probabilistic detection architecture as Loss Attenuation, with the only difference that BayesOD replaces NMS with the Bayesian Fusion. Tab. III shows that with this simple change, BayesOD gains 3% in PDQ and reduces the regression NLL by 2.24 points compared to Loss Attenuation. Similarly, Fig. 5 shows that BayesOD has the lowest regression calibration error among all methods. Fig. 6 shows that BayesOD is the only method with a regression minimum uncertainty error substantially lower than 0.48, implying that the regression entropy output from BayesOD can be used to distinguish false positive detections from true positive detections. Unfortunately, the improvement in spatial uncertainty estimation performance comes at a cost to runtime. However, the difference of mAP is only within 2 -3% range. Fig. 4 shows that ensemble methods do not provide a substantial improvement in the quality of predicted uncertainty estimates compared to a single model, when evaluated using classification and the regression NLL. The same conclusion can be reached by observing calibration and MUE results in Fig. 5 and Fig. 6, respectively, where methods using ensembles exhibit similar performance to a single model trained with Loss Attenuation. On the other hand, Fig. 4, Fig. 5, and Fig. 6 show Loss Attenuation + Dropout and BayesOD + Dropout models to have a worse performance when compared to models trained with no dropout on NLL, calibration errors, and MUE respectively.

The reason behind the lack of significant improvement from Ensembles can be explained by looking at the size of the training dataset. As Kendall et al. suggested in [35], epistemic uncertainty can be explained away under large data situations such as our training on 70 K frames from the BDD dataset. MC-Dropout on the other hand has been shown to significantly under-perform ensembles and other methods on simple predictive uncertainty estimation tasks such as classification in [64], [114]. These results from literature also translate to our results on probabilistic object detection, where Dropout enabled Loss-Attenuation and BayesOD models are shown to provide worse predictive uncertainty when compared to their Dropout-free counterparts. One final disadvantage of these sampling-based methods is how computationally expensive both MC-Dropout and ensemble-based methods are, with both methods having the slowest runtimes in Tab. III. We therefore conclude that the current methods used for epistemic uncertainty estimation do not provide enough improvement in the quality of estimated uncertainty to justify their high computational cost.

### E. Aleatoric Uncertainty in Camera and LiDAR Perception

RGB camera images and LiDAR point clouds are two dominant sensing modalities in autonomous driving. They have unique sensing properties and observation noise characteristics, which fall in the category of aleatoric uncertainty. In this section, we compare aleatoric uncertainty in image perception by common front-view RGB images, and LiDAR perception by Bird's Eye View representation. To do this, we conduct experiments on the "Car" objects in the KITTI dataset [20]. We collect 2D image detections from the RetinaNet (Loss Attenuation) introduced in Sec. IV-A, as well as their associated 3D LiDAR detections from ProbPIXOR [11] [115], or LiDAR points onto front-view for 3D detection [15]. We leave a comparative study for uncertainty modelling in these methods as an interesting future work.

## V. C F W

In this section, we discuss several challenges and directions for future work in probabilistic object detection.

### A. Efficient Epistemic Uncertainty Estimation

Based on the papers reviewed, explicitly modelling epistemic uncertainty in probabilistic object detection usually requires a sampling mechanism such as MC-Dropout or Deep Ensembles, which are highly time-consuming and memory-intensive. For example, running MC-Dropout with 10 inferences has a speed of 2 -3 FPS in Tab. III, which is challenging for online autonomous driving. Recently, several works attempt to estimate epistemic uncertainty without sampling. For example, Postel et al. [37] propose to approximate epistemic uncertainty by an error propagation method. Furthermore, Sensoy et al. [24] and Amini et al. [67] have shown that it is possible to directly predict the high-order conjugate priors of network output distributions (a Dirichlet prior for the multinomial distribution in classification [24], and a Inverse-Gamma prior for the Gaussian distribution in regression), which are used to estimate epistemic uncertainty from single-shot inference based on evidential deep learning perspective. Incorporating Error Propagation in probabilistic object detectors would be an interesting direction of future work.

### B. Aleatoric Uncertainty Decomposition

Aleatoric uncertainty, defined as the observation noise inherent in sensor measurements, can be decomposed into several sources. For example, aleatoric uncertainty arises from varied weather conditions (e.g. consider night-time, fog, or rain scenarios in camera perception), sensor precision and quality, as well as data annotation errors or ambiguity (e.g. labeling a car with a mountain bike on its roof only as "Car" class, instead of as "Car" and "Bike" objects). Czarnecki et al. [59] defined seven sources of uncertainty a perception module can model during the model development and operation (cf. Appx. A. However, current probabilistic object detectors only model aleatoric uncertainty as a whole. It is an interesting future research direction to decompose aleatoric uncertainty and model each source of uncertainty separately. In this way, the uncertainty interpretability and detection performance may be potentially improved.

### C. Uncertainty Propagation to Downstream Modules

The majority of works in probabilistic object detection focus on how to leverage uncertainty to improve the detection accuracy, especially in terms of Average Precision (AP), as we have discussed in Sec. III-C. However, object detection is only a building block in the long signal processing chain of the self-driving vehicle autonomy stack. Propagating the frame-by-frame detection uncertainties to the sequential downstream modules is expected to improve both the safety and robustness of the system as a whole. For example, multitarget tracking, an essential autonomous driving task, could benefit from estimated localization uncertainty of detected objects, which can be used to bootstrap object states in multitarget trackers based on Bayesian filtering [116]. Another task that could benefit from uncertainty estimates from object detection is the object-based simultaneous localization and mapping [117], where the predicted mean and covariance matrices from bounding boxes can be used as measurement updates. Finally, using uncertainty estimates from probabilistic object detection for behavior prediction of multiple agents in road scenes [118] or for driver assistance system [119] could be another interesting directions. We encourage further research on methods to incorporate predicted uncertainty from probabilistic object detection into the various tasks required by autonomous vehicles.

### D. Better Evaluation of Probabilistic Object Detection

We have shown in Sec. IV that mean Average Precision (mAP) does not consider the quality of bounding box uncertainty in comparing probabilistic object detectors. Two objects with the same mean but different covariance matrices for their output bounding boxes will yield the same mAP. Following the work in [111], we recommend researchers to evaluate probabilistic object detection using proper scoring rules for a theoreticallysound evaluation as well as calibration errors for better insight on calibration quality of predicted probability distributions. In addition, PDQ can be useful for analyzing probabilistic object detectors, as it provides a summary of performance as a single scalar. One should note however that PDQ is not a proper scoring rule [111] and should not be used by itself to rank probabilistic object detectors.

Beyond proper scoring rules, we argue that probabilistic object detection should be evaluated in context of the full autonomous vehicle stack (i.e. from perception and prediction to planning and action). It is a difficult task that requires access to an autonomous vehicle platform and a complete software stacks [120], [121] that support the integration of uncertainty estimates from probabilistic detectors in subsequent tasks. In this case, building autonomous vehicle simulators with high fidelity could help (e.g. [122], [123]). It is an important and challenging future research direction to build such a simulator that could take the predictive uncertainty from probabilistic object detectors as inputs, and evaluate probabilistic detection in a full software stack with novel metrics.

### E. Ground Truth Uncertainty for Datasets

Current open datasets in object detection (e.g. KITTI [20] and Waymo [109]) only provide ground truth boxes and object categorizes, which can be used to train deterministic object detectors. However, those datasets do not provide information to reflect the ambiguity of human annotations (which can be categorized into aleatoric uncertainty), and thus no ground truth information is available that can directly supervise the training of predictive uncertainty in probabilistic object detection. Ground truth uncertainty can be generated during the manual annotation process of object detection datasets, by quantifying the disagreement between different human annotators on the category and the bounding box location of the same object in the scene. Unfortunately, generating accurate ground truth uncertainty will require multiple iterations of labeling, a process that is expensive and time consuming. Recently, [90], [110] make the first step to infer the label uncertainty with bounding boxes from LiDAR point clouds, with the help of a generative model. It would be an interesting direction to explore more alternative methods to generate ground truth uncertainty from a dataset, and benchmark probabilistic object detection. VI. C In this work, we present a survey and comparative study on probabilistic object detection using deep learning approaches in the field of autonomous driving. First, we provide a background knowledge of practical uncertainty estimation methods in deep learning. Next, we systematically summarize existing methods in probabilistic object detection, and evaluate uncertainty estimation methods on an one-stage 2D image detector on three standard autonomous driving datasets. Finally, we discuss challenges and open questions in this research field. Open source code for benchmarking probabilistic object detection is made available at: https://github.com/asharakeh/pod_ compare.git. We hope that our survey and the benchmarking code will become a useful tool for researchers and practitioners in developing robust perception in autonomous driving. R A This supplementary material to the main paper is structured as follows: Appx. A introduces epistemic and aleatoric uncertainty in details, as well as another uncertainty categorization based on the development and operation of a perception system. Appx. B explains how to estimate classification uncertainty with a distribution in softmax logits. Appx. C lists several common non-proper scoring metrics to quantify uncertainty estimates, and Appx. D discusses several uncertainty estimation benchmarks. After introducing generic object detection in Appx. E, the datasets used in our experiments are compared in Appx. F.

### A. Epistemic and Aleatoric Uncertainty

In Sec. II-C, we have introduced that predictive uncertainty can be decomposed into epistemic uncertainty and aleatoric uncertainty following the Bayesian Neural Network framework. Fig. 8 shows an example of epistemic and aleatoric uncertainties in visual semantic segmentation, and Tab. VI lists several uncertainty estimation applications in autonomous driving. Note that although epistemic and aleatoric uncertainty are defined in the context of Bayesian Neural Networks, the two types of uncertainty can be captured by non-Bayesian methods such as Deep Ensembles and Direct Modelling as well (cf. Sec. II-D). Furthermore, both types of uncertainty are not mutually exclusive [35]; explicitly modeling only one may result in a predictive probability that reflects the properties of the other type of uncertainty as well.

### 1) Another Uncertainty Categorization Method

Beyond epistemic and aleatoric uncertainty, Czarnecki et al. [59] define seven sources of perceptual uncertainty to be considered for the development and operation of a perception system (such as object detection, semantic segmentation etc.), as shown by Fig. 9. During development, there exists uncertainty when defining the perception problems (U1), collecting and annotating data with selected scenarios (U2-U5), as well as training the model (U6). During operation, an additional type of uncertainty arises due to distribution shift between the training and testing data splits (U7).

Taking object detection as an example. Conceptual uncertainty (U1) would occur when defining class labels (e.g. shall we distinguish between "Cars" and "Vans", or regard them as "Vehicles"?). Due to the limitation of weather conditions or locations when recording data, the training dataset could not cover all driving scenarios, which introduces U2 and U3 uncertainties. Labeling the bounding box in a RGB camera image captured during night drive is difficult due to low illumination (U4 uncertainty), and depending on the expertise of annotators, the quality of such bounding box label is different (U5 uncertainty). The network architecture has an impact on how an object detector fits the training dataset, resulting in U7 uncertainty. Finally, employing the object detector trained with highway datasets to urban scenarios would cause the domain shift problem, and result in U7 uncertainty.

### B. Estimating Classification Uncertainty with Softmax Logits

Instead of the common way of using the standard softmax function with the cross-entropy loss, Kendall et al. [35]

### Development Operation

Fig. 9: Uncertainty categorization according to the procedure of developing and deploying a perception system. Seven distinct sources of uncertainty are defined. Adapted from [59].

combine the softmax function with a Gaussian distribution to estimate classification uncertainty. Classification uncertainty is learnt by assuming that each element in the softmax logit vector is independently Gaussian distributed, with its mean and variance directly predicted by the network output layers. A softmax logit is the unnormalized log probability output the model before the softmax function. Let a softmax logit regression variable for the class 𝑐 be 𝑙 𝑐 , its distribution is given in the form:

𝑝(𝑙 𝑐 |x, W) = N 𝑙 𝑐 | μ𝑐 (x, W), σ2 𝑐 (x, W)

, where μ𝑐 (x, W), σ2

𝑐 (x, W) refer to the predicted mean and variance of [35] propose to sample the softmax logit based on the predicted Gaussian distribution via the re-parametrization trick, and then transform the sampled softmax logit into the softmax score to calculate a standard classification loss, such as the cross-entropy loss or the focal loss [19].

### C. Additional Scoring Metrics For Evaluating Uncertainty In Literature

The following section introduces several common evaluation methods for uncertainty estimation. Several benchmarks based on those evaluation methods are discussed in Appx. D.

### 1) Shannon Entropy

Shannon Entropy (SE) is a common evaluation metric to estimate the quality of predictive uncertainty for classification tasks [60]. For a class label 𝑦 of 𝐶 classes, the SE, H , is measured by:

H (𝑦|x, D) = - 𝐶 ∑︁ 𝑐=1 𝑝(𝑦 = 𝑐|x, D) log 𝑝(𝑦 = 𝑐|x, D) .(9)

SE reaches a minimum value when the network is certain in its prediction, i.e. 𝑝(𝑦 = 𝑐|x, D) = 0 or 1, and maximum when the prediction follows an uniform distribution, i.e. 𝑝(𝑦 = 𝑐|x, D) = 1 𝐶 .

### 2) Mutual Information

Another common evaluation metric for measuring the quality of uncertainty in classification tasks is Mutual Information (MI). A practical MI formulation was introduced in [60], which measures the information gain of the predictive probability, when introducing the posterior distribution of model parameters W:

I (𝑦, W|x, D) = H (𝑦|x, D) -E 𝑝 (W | D) H (𝑦|x, W) ,(10)

where E[•] is the expectation operation, and H (𝑦|x, W) is the conditional Shannon Entropy with respect to W, given by:

H (𝑦|x, W) = - 𝐶 ∑︁ 𝑐=1 𝑝(𝑦 = 𝑐|x, W) log 𝑝(𝑦 = 𝑐|x, W) .(11)

The first term on the right-hand side of Eq. 10 is calculated using Eq. 9. The expectation in the second term is approximated by averaging the network's predictions with the network's weight samples (e.g. sampled from the MC-Dropout [60] or the Deep Ensembles [63] approaches). Different from SE which directly measures the predictive uncertainty, MI captures the variations within a model brought by the network's weights W. Therefore, it reflects the model uncertainty. An MI score ranges between [0, 1], with a larger value indicating higher uncertainty.

### 3) Error Curve

This method proposed by Ilg et al. [39] measures how predictive uncertainty matches true prediction errors. It assumes that a well-estimated predictive uncertainty should correlate with the true error, and by gradually removing the predictions with the highest uncertainty, the average errors in the rest of the predictions will decrease. To draw an error curve, a model makes predictions with the uncertainty estimates through a test dataset. Those predictions are ranked according to their uncertainties, such as the Shannon Entropy or Mutual Information scores in classification, and predicted variances in regression. The error curve reports the percentage of removed testing samples according to their uncertainty ranking on the horizontal axis, and the averaged errors in the rest of the predictions on the vertical axis (such as the cross entropy errors in classification, and mean squared errors in regression).

### 4) Total Variance (TV)

The metric proposed by Feng et al. [8] is designed to measure the dispersion of a probability distribution in regression tasks, by calculating the trace of its covariance matrix, i.e. summing up all variances in the diagonal line of the covariance matrix. A TV score ranges within [0, +∞), with a larger value indicating higher uncertainty. Note that TV only quantifies the variance in each regression variable, and ignores the correlations among regression variables.

### D. Benchmarking Uncertainty Estimation Methods

Previous works have evaluated and compared existing uncertainty estimation methods mainly in open-world scenarios. In this setting, the test data distribution is different from the training dataset (also known as domain shift), or there exist objects which a perception module has never seen before (also known as out-of-distribution). This setting is of great interest from the practical perspective of applications such as autonomous driving. Snoeck et al. [64] conduct a largescale study to benchmark classification uncertainty estimation, including image classification using MNIST, ImageNet [135] and CIFAR [136] datasets, as well the text and ad-click classification. They compare softmax output, MC-dropout [60],

Furthermore, Fig 10 also shows that the empirical cumulative distribution function (CDF) of the greyscale intensity values of images from the KITTI dataset is much closer to the CDF of BDD than the CDF of Lyft, suggesting a smaller domain shift from BDD to KITTI than that from BDD to Lyft. The CDF plots in Fig 10 provide insight on the lack of exposure compensation in the Lyft dataset, where ∼ 60% of pixels have an intensity greater than 250, and are therefore very bright (see Fig 10). The dataset

Deep Ensembles [63], temperature scaling (as the post-hoc calibration tool) [69], as well as several Bayesian inference approaches under the domain shift setting. Filos et al. [137] benchmark uncertainty estimation methods in the medical image application (diabetic retinopathy diagnosis). Blum et al. [62] build the Fishyscapes dataset to benchmark uncertainty estimation methods in semantic segmentation for anomaly detection. The dataset is based on Cityscapes [127], which is a popular semantic segmentation dataset for urban autonomous driving.

### E. Detailed Introduction of Generic Object Detection

Object detection is a multi-task problem that requires to jointly recognize objects with classification scores, and localize objects with tightly fitting bounding boxes. State-of-the-art object detectors using deep learning can follow one-stage, two-stage, or the recently-proposed sequence-to-sequence-mapping detection pipelines. In the one-stage object detection pipeline, a deep learning model is employed to directly map the input data to bounding boxes and classification scores in a single shot (e.g. YOLO [138], SSD [92], and RetinaNet [19]). In contrast, the two-stage object detection pipeline extracts several classagnostic object candidates called regions of interests (ROIs) or region proposals (RPs) in the first stage, and refines their class and bounding box attributes in the second stage. Those ROI can be extracted by non-deep learning approaches such as clustering [139] and voting [140], or by a neural network such as a Region Proposal Network (RPN) in the Faster-RCNN architecture [93]. While common object detectors require prior anchors and output post-processing stage such as Non-Maximum Suppression (NMS) to suppress duplicate detections. Usually, both one-stage and two-stage pipelines require a prior anchor grid and an output post-processing stage such as Non-Maximum Suppression (NMS) to suppress duplicate detection results. Recently, Tian et al. [141] propose an anchor-free detector by estimating objects at every pixel, and designing a center-ness loss to allow efficient training of such formulation. Carion et al. [142] take a more drastic approach to avoid prior anchor grid, by reformulating the object detection task as a sequence-to-sequence mapping problem, leading to Detection Transformers (DETR). DETR directly maps a sequence of query points into objects in the scene without the prior anchor grid. The method also avoids duplicate detections through training with the optimal positive-negative sample assignment, obviating the need of a post-processing step such as NMS. While the standard 2D convolution is the dominant method to process RGB camera images, there are several methods to process point clouds from LiDAR and Radar sensors, as well as pseudo point cloud from Stereo cameras. Those point clouds can be projected onto 2D feature maps, and processed by standard 2D CNNs [104], [143]- [145]. They can also be discretized in voxel [146]- [150] and processed through 3D CNN with sparse convolution operations [148], or processed in the continuous vector space without voxelization using the Point-Net based backbone [151]- [153]. For a more detailed summary we refer interested readers to [80] for object detection in 3D point clouds, and [154] for object detection in 2D images.

### F. Experimental Setup: Datasets and Dataset Shift

Recent work on evaluating uncertainty estimates of deep learning models for classification tasks [64] suggests the necessity of uncertainty evaluation under dataset shift. In this regard, we chose three common object detection datasets with RGB camera images for autonomous driving, in order to evaluate and compare our probabilistic object detectors: shift from BDD to Lyft is further amplified as 2D bounding boxes are directly labeled on images for the BDD dataset, whereas 2D bounding boxes are generated by projecting 3D labels in the Lyft dataset. In summary, both KITTI and Lyft data is naturally shifted from the data in the BDD dataset, with KITTI having a lower magnitude of shift when compared to Lyft.

## Figures et tableaux

**Fig. 4** , Fig.4, Fig.5, and Fig.6show bar plots of the regression and classification NLL, calibration errors, and minimum uncertainty errors[13] respectively. Those uncertainty estimation values are averaged over the Car and Person categories from the BDD validation, KITTI, and Lyft datasets. For evaluating calibration performance, we use the Marginal Calibration Error (MCE) metric for category classification and Expected Calibration Error (ECE) for bounding box regression (both metrics have been introduced in Sec. II-E1). Regarding on the uncertainty estimation in classification, Fig.4 (left)shows that all probabilistic object detectors exhibit a lower classification NLL scores on KITTI, but higher classification NLL scores on Lyft when compared to those on BDD. Even though we train our probabilistic object detectors using BDD data, probabilistic object detectors are seen to have lower NLL scores on KITTI than on the BDD validation dataset, implying higher confidence in correct detections. However, Fig.5(left) shows that the classification marginal calibration error increases to similar values on both KITTI and Lyft when compared to the marginal calibration error on the BDD validation set. We conclude that although our probabilistic object detectors provide sharper categorical distributions on KITTI compared to BDD, the distributions of KITTI detections are worse calibrated than those of BDD detections. Fig.6(left) also shows that the classification minimum uncertainty error follows the same trend as the classification

**Fig. 4:** Bar plots of the Negative Log Likelihood of the category classification and bounding box regression probabilistic output for various probabilistic detection methods implemented with the RetinaNet architecture as a backend.

**Fig. 5:** Bar plots of the calibration errors of the category classification and bounding box regression probabilistic output for various probabilistic detection methods implemented with the RetinaNet architecture as a backend.

**Fig. 6:** Bar plots of the minimum uncertainty errors for the category classification and bounding box regression probabilistic output for various probabilistic detection methods implemented with the RetinaNet architecture as a backend.

compromised. 5. The performance gains in the quality of predictive uncertainty when using sampling-based epistemic uncertainty estimation methods does not justify their computational cost when compared to aleatoric uncertainty estimation methods. Tab. III and Tab. IV show Loss Attenuation and BayesOD to exhibit a mAP drop when MC-Dropout is added to model epistemic uncertainty. On the other hand, both Pre-NMS and Post-NMS variants of ensembles are seen to provide a slight improvement to mAP both for evaluation without dataset shift in Tab. III and for evaluation with dataset shift in Tab. IV.

**Fig. 7:** (a). The heatmaps of regression aleatoric uncertainties in image detections and LiDAR detections. (b). An illustration of object detections in RGB camera images and LiDAR point clouds in the bird's eye view.

**Fig. 8:** Fig.8: An illustration of epistemic and aleatoric uncertainty in semantic segmentation on the CamVid dataset[125]. The epistemic uncertainty is measured by the Mutual Information, and the aleatoric uncertainty by the Shannon Entropy. Uncertainty estimation networks are adapted from Postel et al.[37]. The different behaviours of epistemic vs aleatoric uncertainty can be observed in (d) and (e). For example, the aleatoric uncertainty is more related to the object boundary, whereas the epistemic uncertainty is affected by the prediction inaccuracy (the front car marked with circle in the image is badly-segmented, and depicts high epistemic uncertainty in (e)).

**Fig. 10:** Sample images from BDD, Lyft and KITTI datasets showing differences in aspect ratios, camera view points, and scene appearance between the three datasets. Top Right: Plot of the empirical cumulative distribution function (CDF) of the grayscale intensity values of all images in BDD, KITTI, and Lyft datasets. The CDF of KITTI is much closer to that of BDD than the CDF of Lyft.

**TABLE I:** A summary of probabilistic object detectors.

    Reference | Year Sensor † Dataset | Unc. Type ‡ | Modeling | Post-processing | Evaluation Metrics
     |  |  |  | Method |  | 
    Feng et al. [8] | 2018 L | KITTI [20] | E+A | MC-Dropout, | NMS | F-1 Score
     |  |  |  | Direct Modeling |  | 
    Feng et al. [9] | 2018 L | KITTI [20] | A | Direct Modeling | NMS | mAP
    Le et al. [87] | 2018 C | KITTI [20] | A | Direct Modeling, | NMS, Output Statistics | True Positive/False Positive
     |  |  |  | Output |  | count
     |  |  |  | Redundancy |  | 
    Miller et al. [6] | 2018 C | COCO [98], SceneNet | E | MC-Dropout | NMS, Clustering | Precision and Recall,
     |  | RGB-D [99], QUT |  |  |  | Absolute Open-set Error,
     |  | Campus Dataset [100] |  |  |  | F1-Score
    Choi et al. |  |  |  |  |  | 

[figure sans légende identifiée] Sec. IV-D presents the main experimental results and our conclusions. Finally, Sec. IV-E compares the behaviours of aleatoric uncertainties in an image and a LiDARbased object detectors.

    A. Our Probabilistic Object Detectors
    For a fair evaluation, we re-implement the various uncertainty
    estimation mechanisms described in Sec. III-B using a 2D
    image-based object detector, RetinaNet [19], as the basic net-
    work. The new network models the bounding box parameters
    as multivariate Gaussians with a diagonal covariance matrices,
    and uses the softmax function to predict the parameters of cate-
    gorical distributions for object classification. The probabilistic
    extensions to RetinaNet are summarized in Tab. II.
    To extend RetinaNet for modeling aleatoric uncertainty,
    we implement three different approaches: Loss Attenuation,
    BayesOD, and Output Redundancy, which are summarized in
    rows 1 -3 of Tab. II. Loss Attenuation uses Direct Modeling
    for estimating the uncertainty in regression and classification
    outputs, by predicting the means and variances for bounding
    box regression variables and softmax logits. The network is
    trained using the attenuated regression losses as well as the
    modified classification loss to learn softmax logit variances
    required
    to formulate BayesOD from Loss Attenuation, comparing
    the performance of the two provides insights on how useful
    Bayesian inference is when compared to standard NMS. The
    final approach for estimating aleatoric uncertainty is Output
    Redundancy, which leaves the base network and detection
    head of the deterministic RetinaNet model intact, and only
    modifies the post-processing step to cluster redundant output
    detections (Sec. III-B2). To estimate category and bounding
    box uncertainty, Output Redundancy extracts sample statistics
    from clusters of output detections, avoiding the auxiliary
    variance predictions used in most probabilistic object detection
    approaches.
    To model epistemic uncertainty, methods proposed in [6], [7]
    are implemented by incorporating dropout into the detection
    head of a deterministic RetinaNet model. We follow the
    implementation described in [7] which clusters output after the
    NMS step, treating the object detector as a Black Box (row
    8 of Tab. II). Since the Black Box and Output Redundancy
    implementations do not explicitly model the variance param-
    eters of the bounding box output of RetinaNet, comparing the
    quality of their bounding box output uncertainty to methods
    that use Direct Modeling of the variance parameters should
    provide an indicator on the value of Direct Modeling in
    probabilistic object detection.

**TABLE II:** A summary of uncertainty modeling methods used for the Base Network, Detection Head, and Post-processing stages of each of our implemented probabilistic object detectors.

    Method | Unc. Type ‡ | Base Network | Detection Head | Post-processing
    1. Output Redundancy | A | Unmodified | Unmodified | Data Association → Sample Statistics
    2. Loss Attenuation | A | Unmodified | Reg and Cls variance | NMS
    3. BayesOD | A | Unmodified | Reg and Cls variance | Data Association → Bayesian Fusion
    4. Loss Attenuation + Dropout | A + E | Unmodified | Reg and Cls variance, MC-Dropout | NMS
    5. BayesOD + Dropout | A + E | Unmodified | Reg and Cls variance, MC-Dropout | Data Association → Bayesian Fusion
    6. Pre-NMS Ensembles | A + E | Ensembles | Reg and Cls variance, Ensembles | Data Association → Gaussian Mixture → NMS
    7. Post-NMS Ensembles | A + E | Ensembles | Reg and Cls variance, Ensembles | NMS → Data Association → Gaussian Mixture
    8. Black Box | E | Unmodified | MC-Dropout | NMS → Data Association → Gaussian Mixture
    ‡ A: Aleatoric uncertainty, E: Epistemic uncertainty |  | 
    layers with two extensions: Loss Attenuation + Dropout and | 
    BayesOD + Dropout. Loss Attenuation + Dropout extends | 
    Loss Attenuation by performing multiple stochastic MC- | 
    Dropout runs during inference, followed by the standard NMS. | 

Berkeley Deep Drive 100K (BDD) Dataset [18], the KITTI autonomous KITTI[20] dataset and 5, 000 randomly chosen frames from the Lyft[21] autonomous driving dataset. The results on Lyft and KITTI are then compared against the results on the BDD validation dataset. Here, we only evaluate on the Car and Person object classes, as they are the only two classes that have the same definition in all three datasets. More detailed information on three datasets as well as the dataset shift from BDD to KITT and BDD to Lyft can be found in Appx. F.

    driving dataset [20], and the Lyft autonomous
    driving dataset [21]. All presented probabilistic object detec-
    tors are trained using the official training frames of BDD to
    detect seven common dynamic object categories relevant to
    autonomous driving: Car, Bus, Truck, Person, Rider, Bicycle,
    and Motorcycle. The detectors are then evaluated across all
    three datasets to quantify the uncertainty estimation quality
    with or without dataset shift.
    Evaluation without Dataset Shift: First, we conduct com-
    parative experiments without dataset shift, by testing the
    probabilistic object detectors on the official BDD validation

**TABLE III:** An evaluation with no dataset shift by testing detectors on the BDD validation dataset. Results are averaged over all seven dynamic object categories.

    Method | BDD | KITTI | Lyft
    Deterministic RetinaNet (Baseline) | 40.63 | 37.11 | 5.33
    Output Redundancy | 38.75 | 34.99 | 5.21
    Loss Attenuation | 41.09 | 39.15 | 5.96
    BayesOD | 41.33 | 39.32 | 6.01
    Loss Attenuation + Dropout | 40.39 | 38.90 | 5.97
    BayesOD + Dropout | 40.52 | 38.99 | 5.98
    Pre-NMS Ensembles | 41.85 | 39.50 | 5.953
    Post-NMS Ensembles | 41.95 | 39.52 | 5.949
    Black Box | 40.53 | 37.01 | 5.231

**TABLE IV:** Mean average precision (mAP) results of evaluation under dataset shift. The mAP scores are computed using the car and pedestrian categories on the BDD, Lyft, and KITTI datasets.

    estimated
    category and bounding box distributions of true positive de-
    tections, which have IOU > 0.7 scores with ground truths in
    the scene. This IOU threshold of 0.7 was chosen following
    the standard threshold set by the KITTI and BDD datasets
    when evaluating 2D object detection. Tab. III also shows the
    runtime of each probabilistic object detection method on a
    machine with an Nvidia Titan V GPU and Intel i3770k CPU,
    in order to show the potential for deploying those methods on
    autonomous vehicles.
    The first row of Tab. III shows that our deterministic RetinaNet
    baseline achieves 28.62% mAP, an acceptable value that
    conforms to the 28% -30% mAP range reported by baselines
    provided in the original BDD dataset paper [18]. We notice
    that all implemented probabilistic extensions to RetinaNet are
    less than 2% mAP difference compared to the deterministic
    baseline. On the other hand, Tab. IV presents the mAP of
    the implemented probabilistic object detectors under dataset
    shift, evaluated only on the Car and Person categories on the
    BDD validation, KITTI, and Lyft datasets. Tab. IV shows that
    when we only consider the Car and Person categories for our
    evaluation, all detection methods show an increase of mAP
    values from ∼ 28% to ∼ 40% on the BDD dataset, because
    detecting two object categories is easier than seven categories.

III shows mAP to be correlated to the classification Negative Log Likelihood (NLL). As an example, the method that achieves the lowest mAP in Tab. III, Output Redundancy, is seen to have the highest classification NLL and as such the worst classification performance. On

the other hand, Tab. III shows mAP to have no correlation to the regression NLL. As an example, Tab. III shows that Black Box has a regression NLL that is two orders of magnitude larger than other probabilistic detectors, while still performing on par with other probabilistic object detectors on mAP. Unlike mAP, we notice a direct correlation between PDQ and regression NLL, where the lowest PDQ is achieved by methods with the highest regression NLL (Black Box and Output Redundancy), while the highest PDQ is achieved by the methods with the lowest regression NLL. However,

the magnitude of increase in PDQ between probabilistic object detectors is not proportional to the magnitude of decrease in regression

table ,

    the mAP scores among differ-
    ent probabilistic object detection methods are comparable,
    with only 2 -3% mAP differences. However, the uncertainty
    scores (such as regression NLL) vary significantly, indicating
    very different uncertainty estimation performance. Taking a
    closer look at the performance of BayesOD and Pre-NMS
    ensembles, the table shows that BayesOD outperforms Pre-
    NMS ensembles on regression NLL, classification NLL and
    PDQ, but under-performs the same method in mAP, resulting
    in different rankings of BayesOD and Pre-NMS ensembles.
    Since mAP is important for evaluating the performance of
    deterministic object detectors, we argue that a good proba-
    bilistic object detector should maintain competitive mAP when
    compared to deterministic counterparts. Therefore, we suggest
    that researchers use proper scoring rules such as NLL as well
    as calibration errors for comparing and ranking probabilistic
    object detectors.
    2.

Estimating spatial uncertainty through Loss Attenuation is essential for high quality predictive distributions in our

**TABLE V:** The Pearson Correlation Coefficients (PCC) between aleatoric uncertainties and detection distances and occlusions, produced by a 2D image object detector and a 3D LiDAR object detector.

**TABLE VI:** The applications of uncertainty estimation in autonomous driving and example references.

    Problem | Example Reference | Year | Unc. Type | Dataset
    Camera pose estimate | Kendall et al. [44] | 2016 | E | Cambridge Landmarks [124]
    Semantic segmentation | Kendell et al. [36] | 2017 | E | CamVid [125], SUN RGB-D [126],
     |  |  |  | Pascal-VOC [102]
    Image annotation | Mackowiak et al. [48] | 2018 | E | Cityscapes [127]
    Optical flow | Ilg et al. [39] | 2018 | E+A | KITTI [20], MPI-Sintel Flow [128]
    Learning by demonstration | Choi et al. [65] | 2018 | A | US Highway 101 [129]
    of driving control |  |  |  | 
    End-to-end driving | Michelmore et al. [57] | 2019 | E | CARLA Simulation [130]
    Trajectory prediction | Hu et al. [52] | 2020 | A | Self-recorded data
    Depth completion | Walz et al. [41] | 2020 | A | Gated2Depth [131]
    Visual tracking | Danelljan et al. [51] | 2020 | A | OTB100 [132], UAV123 [133], NFS [134] and
     |  |  |  | four others
    the softmax logit. Training this softmax logit is different from |  | 
    the normal regression variable shown in Eq. 4, as there are |  | 
    only ground truth for object categories. In this regard, Kendall |  | 
    et al. |  |  |  | 

autonomous driving dataset [20] contains has 80, 000 image frames at a 1280 × 720 resolution, with 70, 000/10, 000 training/validation data split. The BDD dataset was recorded in North America with diverse scene types such as city streets, residential areas, and highways, and in diverse weather conditions. The dataset contains an equal number of frames recorded during daytime and nighttime. 7, 481 image frames at a resolution of 1242 × 375. The dataset was recorded in Europe, only in clear weather and in daytime hours.

autonomous driving dataset [21] has 158, 757 image frames at a 1224 × 1024 resolution. The Lyft Dataset was recorded in a single city (Palo Alto) in the US, and only contains 3D bounding box annotations. We generate 2D bounding box annotations for objects in the scene by projecting 3D bounding boxes using the Lyft Dataset API. Similar to KITTI, the Lyft dataset was captured during daytime and in clear weather. Both KITTI and Lyft have a different camera view point, image resolution, and image quality compared to BDD, which is visible when looking at example images from the three datasets inFig 10.
