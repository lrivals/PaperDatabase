---
id: arxiv-2403.02886-revisiting-confidence-estimation-reliable-failure
title: "Revisiting Confidence Estimation: Towards Reliable Failure Prediction"
year: 2024
backend: grobid
---

## Abstract

Reliable confidence estimation is a challenging yet fundamental requirement in many risk-sensitive applications. However, modern deep neural networks are often overconfident for their incorrect predictions, i.e., misclassified samples from known classes, and out-of-distribution (OOD) samples from unknown classes. In recent years, many confidence calibration and OOD detection methods have been developed. In this paper, we find a general, widely existing but actually-neglected phenomenon that most confidence estimation methods are harmful for detecting misclassification errors. We investigate this problem and reveal that popular calibration and OOD detection methods often lead to worse confidence separation between correctly classified and misclassified examples, making it difficult to decide whether to trust a prediction or not. Finally, we propose to enlarge the confidence gap by finding flat minima, which yields state-of-the-art failure prediction performance under various settings including balanced, long-tailed, and covariate-shift classification scenarios. Our study not only provides a strong baseline for reliable confidence estimation but also acts as a bridge between understanding calibration, OOD detection, and failure prediction. The code is available at https://github.com/Impression2805/FMFP.

## 1. INTRODUCTION

D EEP neural networks (DNNs), especially vision models, have been widely deployed in safety-critical applications such as computer-aided medical diagnosis [1], [2], autonomous driving [3], [4], and robotics [5]. For such applications, besides the prediction accuracy, another crucial requirement is to provide reliable confidence for users to make safe decisions. For example, an autonomous driving car should rely more on other sensors or trigger an alarm when the detection network is unable to confidently predict obstructions [3], [6]. Another example is the control should be handed over to human doctors when the confidence of a disease diagnosis network is low [1]. Unfortunately, modern DNNs are generally overconfident for their false predictions, i.e., assign high confidence for misclassified samples from training classes and out-of-distribution (OOD) samples from unknown classes [7], [8], [9], [10]. The overconfident issue makes DNNs untrustworthy, bringing great concerns when deploying them in practical applications.

In recent years, many confidence estimation approaches have been proposed to enable DNNs to provide reliable confidence for their predictions. Most of those methods focus on two specific tasks, i.e., confidence calibration, and OOD detection. (1) Confidence calibration alleviates the overconfidence problem and reflects the predictive uncertainty by matching the accuracy and confidence scores [11]. One category of approaches [12], [13], [14], [15], [16], [17], [18], [19], [20], [21] aim to learn well-calibrated models during training. Another class of approaches [7], [22], [23], [24], [25], [26] use post-processing techniques to calibrate DNNs.

(2) OOD detection focuses on judging whether an input sample is from unseen classes based on model confidence. Most existing methods tackle OOD detection problem in a post-hoc manner [27], [28], [29], [30], [31], [32], and other works focus on learning a model with better OOD detection ability at training time [33], [34], [35], [36]. If we focus on the progress made in confidence calibration and OOD detection, it seems that the confidence estimation of DNN is well-solved because both the confidences of in-distribution (InD) and OOD samples are well-calibrated.

In this paper, we study a natural but ignored question: can we use calibrated confidence to detect misclassified samples by filtering out low-confidence predictions? This, perhaps, is the most direct and practical way to evaluate the reliability of the estimated confidence. Actually, this problem is studied in the literature as failure prediction (or misclassification detection) [8], [39], [40], whose purpose is to detect erroneously classified natural examples from seen class (e.g., misclassified samples in test set). In practice, for a deployed system, most of the inputs are from seen classes, and misclassification errors widely exist. Therefore, failure prediction is a highly practical and valuable tool for developing reliable and trustworthy machine learning systems [40]. However, compared with the widely studied confidence calibration and OOD detection, there are few works for failure prediction. e n e r g y e n e r g y Fig. 1: A comparison of (a) AURC (↓) and (b) AUROC (↑). We observed that many popular confidence calibration and OOD detection methods are useless or harmful for failure prediction. We propose a simple flat minima based method that can yield state-of-the-art failure prediction performance. ResNet110 [37] on CIFAR-10 [38].

We revisit current confidence estimation approaches from the perspective of failure prediction motivated by the following reasons: Firstly, calibration and failure prediction both focus on in-distribution data from known classes and share the same motivation that enables the model to provide reliable confidence to make safe decisions. From a practical perspective, with a calibrated classifier in hand, one natural way to verify its trustworthiness is to filter out predictions with low confidence. Secondly, existing OOD detection methods aim to separate InD samples from OOD samples by assigning high confidence for InD samples and low confidence for OOD samples. However, in practice, misclassified samples should also have low confidence so that be separated from correct samples. In other words, OOD detection and failure prediction should be considered in a unified manner and a good confidence estimator should help detect both the OOD and misclassified InD samples. Thirdly, calibration and OOD detection have drawn significant attention from the machine learning community [13], [14], [15], [7], [41], [18], [11], [27], [28], [29], [30], [31], [32], [33], [34], [35], [42]. However, there are few works for failure prediction, which is a practical, important, yet somewhat under-appreciated area of research that represents a natural testbed to evaluate the reliability of the estimated confidence of a given method. Revisiting confidence estimation methods from the perspective of failure prediction not only helps us understand the effectiveness of existing methods but also benefits the investigation of failure prediction.

Although common wisdom in the community suggests that the estimated confidence via calibration or OOD detection methods could be useful for failure prediction, we find a surprising pathology: many popular calibration and OOD detection methods (including both training-time [12], [13], [14], [15], [43], [33], [34] and post-processing [7], [27], [29], [31], [32] methods) are more of a hindrance than a help for failure prediction, as shown in Fig. 1. Empirical study shows that calibration methods often reduce overconfidence by simply aligning the accuracy and average confidence, and OOD detection methods lead to under-confident correctly classified InD samples. Consequently, correctly classified and misclassified samples would be worse separated, which is harmful for detecting misclassified samples based on the confidence of predictions.

Finally, how can we improve the failure prediction performance of DNNs? On the one hand, failure prediction requires better discrimination between the confidence of correctly classified and misclassified examples, which would increase the difficulty of changing the correctly classified samples to be incorrect due to the larger confidence margins. Interestingly, this is closely related to the notion of "flatness" in DNNs, which reflects how sensitive the correctly classified examples become misclassified when perturbing model parameters [44], [45], [46], [47]. On the other hand, we observed an interesting reliable overfitting phenomenon that the failure prediction performance can be easily overfitted during the training of a model. Inspired by the natural connection between flat minima and confidence separation as well as the effect of flat minima for overfitting mitigation, we propose a simple hypothesis: flat minima is beneficial for failure prediction. We verify this hypothesis through extensive experiments and propose a simple flat minima based method that can achieve state-of-the-art confidence estimation performance.

In summary, our contributions are as follows:

•

We rethink the confidence reliability of confidence calibration and OOD detection methods by evaluating them on the challenging and practical failure prediction task. Surprisingly, we find that they often have negative effect on failure prediction.

•

We provide detailed analysis and discussion on calibration and OOD detection for failure prediction from the perspective of proper scoring rules and Bayesoptimal reject rules, respectively.

•

We reveal an interesting reliable overfitting phenomenon that the failure prediction performance can be easily overfitting. This phenomenon exists in different model and dataset settings.

•

We propose to find flat minima to significantly reduce the confidence of misclassified samples while maintaining the confidence of correct samples. To this end, a simple flat minima based technique is proposed.

•

Extensive experiments in balanced, long-tailed, and covariate-shift classification scenarios demonstrated that our method achieves state-of-the-art confidence estimation performance.

This paper extends our previous conference publication [48] mainly in five aspects: (1) We show novel insight into the behavior of popular OOD detection methods for failure prediction based on comprehensive experiments. (2) We provide more theoretical perspectives based on proper scoring rules and Bayes-optimal reject rules for the failures of calibration and OOD detection methods in detecting misclassified instances. (3) We provide theoretical analysis on the benefit of flat minima for improving confidence estimation based on PAC-Bayes framework. (4) We design more challenging and realistic benchmarks, i.e., confidence estimation under longtailed and covariate-shift scenarios, in which our method also establishes state-of-the-art performance. (5) Experiments on standard OOD detection benchmarks demonstrate the strong OOD detection ability of our method. In conclusion, we rethink the reliability of current calibration and OOD detection methods from the perspective of failure prediction. Our finding is important because it allows us to better assess recently reported progress in the area of confidence estimation. Finally, we provide a strong and unified baseline that can improve calibration and detect both misclassified and OOD samples.

The remainder of this paper is organized as follows: Section 2 presents the problem formulation and background of confidence calibration, OOD detection and failure prediction, respectively. Section 3 evaluates and analyzes the effect of popular calibration, and OOD detection methods for failure prediction. Section 4 shows that failure prediction can be significantly improved by finding the flat minima in balanced, long-tailed and covariate-shift classification scenarios. Section 5 provides concluding remarks.

## 2. PROBLEM FORMULATION AND BACKGROUND

Multi-class classification. Considering a K-class classification task, let (X, Y ) ∈ X × Y be jointly distributed random variables, where X ⊂ R d denotes the in-distribution feature space and Y is the label space. Specifically, Y = {e 1 , ..., e K } where e k ∈ {0, 1} K is the one-hot vector with 1 at the kth index and 0 otherwise. We are given labeled samples D = {(x i , y i )} n i=1 drawn i.i.d. from (X, Y ) with density p(x, y). We assume that labels are drawn according to the true posterior distribution

Q = (Q 1 , ..., Q K ) ∈ ∆ K where Q k := P(Y = e k |X) and ∆ K is the probability simplex ∆ K = {(p 1 , ..., p K ) ∈ [0, 1] K : k p k = 1}.

A DNN classifier f predicts the class of an input example x:

f (x) = arg max k=1,...,K p k (x), p k (x) = exp(z k (x))/ K k ′ =1 exp(z k ′ (x)),(1)

where z k (x) is the logits output of the network with respect to class k, and p k (x) is the probability (softmax on logits) of x belonging to class k. The classification risk on classifier f can be defined with respect to the 0-1 loss as:

R 0-1 (f ) = E p(x,y) [I(f (x) ̸ = y)],(2)

where I is the indicator function. The Bayes-optimal classifier f * can be defined as follows: Definition 1. (Bayes-optimal classifier) The Bayes-optimal solution of multi-class classification,

f * = arg min f R 0-1 (f )

can be expressed as f * (x) = arg max y∈Y P(y|x).

In practice, the risk in Eq. ( 2) is not straightforward to minimize because the number of training samples is finite and minimizing the zero-one loss is known to be computationally infeasible. Therefore, we often minimize an empirical surrogate risk [49], [50]. Specifically, let ℓ be a surrogate loss (e.g., the log-loss), based on the empirical risk minimization approach [50], the following empirical surrogate risk is minimized: R ℓ

(f ) = 1 n n i=1 [ℓ(f (x), y)],

where regularization can be added to avoid overfitting. At inference time, ŷ = f (x) can be returned as the predicted class and the associated probabilistic score p ŷ (x), i.e., the maximum softmax probability (MSP), can be viewed as the predicted confidence. Besides directly using MSP as confidence, other score functions (e.g., entropy, energy score [29] or maxlogit score [32]) can also be used.

### 2.1. Confidence Calibration

Confidence calibration focuses on InD samples and aims to calibrate the confidence of a model to indicate the actual likelihood of correctness [7]. For example, if a calibrated model predicts a set of inputs to be class y with 40% probability, then we expect 40% of the inputs indeed belong to class y. Formally, denote the score S = f (X) with S = (S 1 , ..., S K ) ∈ ∆ K the random vector describing the scores output by the probabilistic classifier f , then we state: Problem 1. (Calibrated). A classifier giving scores s = (s 1 , ..., s k ) is jointly calibrated if among instances getting score s, the class probabilities are equal to s:

P(Y = e k |S = s) = s k for k = 1, ..., K.(3)

In practice, it is challenging to estimate the probability of Y conditioned on S because the number of samples is limited [51]. Therefore, in the machine learning community, the commonly used notion of calibration is a weaker definition [7]: if among instances for which the confidence score of the predicted class is s, the probability that the prediction is correct is s:

P(Y = e arg max(s) | max(S) = s) = s.

The most commonly used calibration estimator is the Expected Calibration Error (ECE) [52], which approximates the miscalibration by binning the confidence in [0, 1] under M equally-spaced intervals i.e., {B m } M m=1 . Then the miscalibration is estimated by taking the expectation of the mismatch between the accuracy and averaged confidence in each bin:

ECE = M m=1 |Bm| n |acc(B m ) -conf(B m )|,

where n is the number of all samples. Alternatives to ECE include the negative log-likelihood (NLL) and Brier score [53].

### Improving calibration. Many strategies have been proposed

to address the miscalibration of modern DNNs. (1) One category of approaches [12], [13], [14], [15], [16], [17], [18], [19] aim to learn well-calibrated models during training. For example, several works [14], [54], [55] found that the predicted scores of DNNs trained with mixup [56] are better calibrated. Muller et al. [13] showed the favorable calibration effect of label smoothing. Mukhoti et al. [17] demonstrated that focal loss [57] can automatically learn well-calibrated models. (2) Another class of approaches [7], [22], [23], [24], [25], [26] rescale the predictions in a post-hoc manner. Among them, temperature scaling (TS) [7] is an effective and simple technique, which has inspired various post-processing approaches [58], [59], [24].

Empirical studies of calibration. In addition to the calibration strategies, there have been some empirical studies on calibration [7], [41], [60], [11]. For instance, Ovadia Reliable Conf Estimation Fig. 2: Calibration reduces the mismatch between confidence and accuracy, and OOD detection distinguishes OOD samples from InD samples. They share the same motivation to provide reliable confidence for trustworthy AI. In practice, both OOD and misclassified samples are failure sources and should be rejected together.

et al. [41] studied the calibration under distribution shift and empirically found the generally existing performance drop of different calibration methods under distribution shift. Minderer et al. [11] found that the most recent nonconvolutional models [61], [62] are well-calibrated, suggesting that architecture is an important factor of calibration.

### 2.2. OOD Detection

The goal of OOD detection is to reject OOD samples from InD samples at test time. Formally, we have an InD joint distribution D XinYin , where X in ∈ X and Y in ∈ Y are random variables. We also have an OOD joint distribution D XoutYout , where X out ∈ R d \ X and Y out / ∈ Y. At test time, we encounter a mixture of InD and OOD joint distributions:

D XY = π in D XinYin + (1 -π in )D XoutYout ,

### and can only observe the marginal distribution

D X = π in D Xin + (1 -π in )D Xout ,

where the π in ∈ (0, 1) is an unknown prior probability. Remark 1. Consistent with the mainstream of existing works [8], [32], [29], [63], [64]

(g) = π in E p(x|in) [I(g(x) = 0)] + (1 -π in )E p(x|out) [I(g(x) = 1)].(4)

The above definition indicates that the risk of OOD detection arises from rejecting inlier (seen classes) samples as outlier (unseen classes), and accepting outlier samples as inlier. It is worth mentioning that the risk in Eq. ( 4) can not be optimized directly because a common assumption is that OOD samples only encounter in inference stage and be unavailable in training stage, making OOD detection a challenging task.

Common metrics for OOD detection are the false positive rate at 95% true positive rate (FPR95), the area under the receiver operating characteristic curve (AUROC) and the area under the precision-recall curve (AUPR) [8]. For example, AUROC is a threshold-independent metric reflecting the ranking performance between inlier and outlier samples.

Improving OOD detection. OOD detection has attracted a surge of interest in two directions, i.e., post-hoc and trainingtime regularization. (1) Some works focus on designing more effective scoring functions for detecting OOD samples, such as ODIN score [27], Mahalanobis distance score [28], Energy score [29], GradNorm score [30], ReAct [31] and MLogit score [32]. (2) Other methods [33], [34], [35], [67], [68] address the OOD detection problem by training-time regularization. For example, Hendrycks et al. [33] leveraged outlier samples to train OOD detectors. Wei et al. [34] shows logit normalization can mitigate the overconfidence issue for OOD samples.

### 2.3. Failure Prediction

Failure prediction, also known as misclassification detection [8], [69] or selective classification [70], [71], focuses on distinguishing incorrect (D × Xin ) from correct (D ✓ Xin ) predictions based on their confidence ranking. Intuitively, if the associated confidence of each misclassified sample is lower than that of any correctly classified samples, we can successfully predict each error made by the classification model. Problem 3. (Failure Prediction). For a classifier f trained on the training data which is drawn i.i.d. from an InD joint distribution D XinYin , given the score function s and a predefined threshold δ, the aim of failure prediction is to reject the misclassified InD samples based on the following decision function g : X → {0, 1} such that for any test data x drawn from the InD D Xin : g(x) = 1 (correct, x ∈ D ✓ Xin ) if s(x) ≥ δ and g(x) = 0 (misclassified, x ∈ D × Xin ) otherwise. Definition 3. (Risk of Failure Prediction). Given a classifier f and a decision function g, the risk of failure prediction is where c ∈ (0, 1) is the reject cost. Similarly, the risk in Eq. ( 5) can not be optimized directly because DNNs often have near perfect training accuracy and there are few misclassified training samples. Common metrics for failure prediction include the area under the risk-coverage curve (AURC), the normalized AURC (E-AURC) [72], [69], the FPR95, AUROC, AUPR-Success (AUPR-S) and AUPR-Error (AUPR-E) [8]. Particularly, it has been shown [73] that minimizing the AURC metric is equivalent to minimizing R f p (f, g).

R f p (f, g) = E p(x|in) [c • I(g(x) = 0) + I(f (x) ̸ = y) • I(g(x) = 1)],(5)

Improving failure prediction. For DNNs, Hendrycks et al. [8] firstly established a standard baseline for failure prediction by using MSP. Trust-Score [74] adopts the similarity between the classifier and a nearest-neighbor classifier as a confidence measure. Some works formulate failure prediction as a supervised binary classification problem. Specifically, Con-fidNet [40], [10] and SS [75] train auxiliary models to predict confidence by learning the misclassified samples in training set. More recently, Qu et al. [76] proposed a meta-learning framework that constructs virtual training and testing sets to train an auxiliary model. However, those methods may fail when the model has a high training accuracy, in which few or even no misclassified examples will exist in training set. CRL [69] improves failure prediction by regularizing the model to learn an ordinal ranking relationship based on the historical correct rate. OpenMix [39] demonstrates that using the easily available outlier samples coming from non-target classes properly can remarkably help failure prediction. For regression tasks like super-resolution and depth estimation in the field of image enhancement and translation, Upadhyay et al. [77] proposed BayesCap that learns a Bayesian identity mapping for a frozen model in post-hoc manner.

## 3. DOES CALIBRATION AND OOD DETECTION HELP FAILURE PREDICTION?

In recent years, there has been a surge of research focused on alleviating the overconfidence problem of modern DNNs, and existing methods do help calibration and OOD detection of DNNs. In this section, we empirically investigate the reliability of estimated confidence for failure prediction.

### 3.1. Experimental Setup

Datasets and network architectures. We thoroughly conduct experiments on benchmark datasets CIFAR-10 and CIFAR-100 [38], and large-scale ImageNet [78] dataset. In terms of network architectures, we consider a range of models: PreAct-ResNet110 [37], WideResNet [79], DenseNet [80] for experiments on CIFAR-10 and CIFAR-100. For ImageNet, we used ResNet-18 and ResNet-50 [81] models, respectively.

Evaluation metrics. We adopt the standard metrics in [8], [72], [69] to measure failure prediction: AURC, E-AURC, AUROC, FPR95, AUPR-S and AUPR-E. Lower values of AURC, E-AURC, FPR95 and higher values of AUROC, AUPR-S, AUPR-E indicate better failure prediction ability. In addition, we emphasize that test accuracy is also important since we can not sacrifice the original task performance to improve the quality of confidence estimation. Appendix provides detailed definitions of these metrics.

Implementation details. All models are trained using SGD with a momentum of 0.9, an initial learning rate of 0.1, and a weight decay of 5e-4 for 200 epochs with the mini-batch size of 128 on CIFAR-10 and CIFAR-100. The learning rate is reduced by a factor of 10 at 100, and 150 epochs. We employ a standard data augmentation scheme, i.e., random horizontal flip and 32 × 32 random crop after padding with 4 pixels on each side. For each experiment, the mean and standard deviation over three random runs are reported.

Evaluated confidence estimation methods. (1) We evaluate various calibration methods including popular trainingtime regularization like mixup [14], label-smoothing (LS) [13], focal loss [57], L p norm [82] and post-hoc method TS [7]. Those methods have been verified to be effective in addressing the miscalibration problem of DNNs. (2) We evaluate various OOD detection methods including trainingtime regularization like LogitNorm [34], outlier exposure (OE) [33] and post-hoc methods like ODIN [27], energy [29], ReAct [31], MLogit [32]. Many of those methods have recently been proposed and have shown strong OOD detection performance. Supp.Material provides the introduction and hyperparameter setting for each method.

### 3.2. Experimental Results

In our experiments, we confirmed the positive confidence calibration effects of mixup [14], LS [13], Focal [57] and L p norm [82]. For example, on CIFAR-100, with focal loss, the ECE (%) can be reduced from 14.98 to 5.66 for ResNet110 and from 8.00 to 1.35 for DenseNet. These observations are consistent with that in [14], [57]. Similarly, in our experiments, the evaluated OOD detection methods [33], [34], [29], [27], [32] are indeed effective for detecting OOD samples.

### Popular calibration methods can harm failure prediction.

In practice, users would naturally expect that the calibrated confidence can be used to filter out low-confidence predictions in risk-sensitive applications. However, if we shift focus to Table 1, it is evident that those methods generally lead to worse failure prediction performance under various metrics. For example, when training with mixup and LS on CIFAR-10/ResNet110, the AURC (↓) increases 6.75 and 16.37 percentages, respectively. As for post-hoc calibration technique, TS [7] calibrates probabilities by learning a single scalar parameter T for all classes on a hold-out validation set. In our experiments, using validation set and test set to learn the parameter T are denoted as TS-valid and TSoptimal, respectively. Table 2 shows that TS has negligible improvement for failure prediction. Those results are counterintuitive as we expect those methods, which successfully calibrate the confidence, could be useful for failure prediction. Similarly, those post-hoc OOD detection methods like ODIN, energy, ReAct and MLogit also have negative effect on failure prediction task. This means that those OOD detection methods make it harder to distinguish incorrect from correct predictions based on their confidence ranking.

Selective risk analysis. To make intuitive sense of the effect of those methods on failure prediction, Fig. 3 plots the riskcoverage curve. Specifically, the selective risk is the empirical loss or error rate that trusts the prediction, while coverage is the probability mass of non-rejected predictions [72], [69].

Intuitively, a better failure predictor should have low risk at a given coverage. As can be seen from Fig. 3, the baseline has the lowest risks compared to other calibration and OOD detection methods, which indicates that using the confidence output by those methods would, unfortunately, increase the risk when making decisions.

### The same observations generalize to large-scale dataset.

Here we verify our observation that those popular calibration and OOD detection methods often harm failure prediction on ImageNet [78] dataset, which comprises 1000 classes and over 1.2 million images. We train ResNet-18 and ResNet-50 [81] that achieve 70.20% and 76.14% top-1 classification accuracy, respectively. As shown in Fig. 4, similar negative effect can be observed: those widely acknowledged calibration and OOD detection methods yield worse failure prediction performance than baseline.

d ϕ (S, Q) := s ϕ (S, Q) -s ϕ (Q, Q).(6)

A scoring rule is said proper if its divergence is always nonnegative, and strictly proper if additionally d ϕ (S, Q) = 0 implies S = Q. For instance, log-loss is a strictly proper scoring rule [84], while focal loss is not strictly proper [85]. Then, we present the scoring rule decomposition as follows: Proposition 1. (Calibration-Discrimination Decomposition).

Let C be the jointly calibrated scores i.e., C k = P(Y = e k |S = s) for k = 1, ..., K. the divergence of strictly proper scoring rules can be decomposed as [84], [86], [51]:

E[d ϕ (S, Y )] = E[d ϕ (S, Q)] Epistemic + E[d ϕ (Q, Y )] Aleatoric = E[d ϕ (S, C)] Calibration + E[d ϕ (C, Q)] Grouping + E[d ϕ (Q, Y )] Aleatoric ,(7)

where the expectation is taken over Y ∼ Q and X. The final term, aleatoric loss (also known as irreducible loss), is due to inherent uncertainty that exists when assigning a deterministic label to a sample. The epistemic loss is due to the model not being Bayes-optimal classifier. The epistemic loss can be further decomposed into calibration and grouping loss. Specifically, calibration loss measures the difference between estimated score S and the proportion of positives among instances with the same calibrated score C; Grouping loss describes that many instances with the same confidence score S while having different true posterior probabilities Q.

Intuitively, grouping loss captures the discrimination ability of confidence score for separating samples.

Ideally, the model should be well calibration and with high discrimination. However, discrimination and calibration do not necessarily keep pace, and many popular methods ignore the discrimination part. Popular calibration methods such as mixup [14], LS [13], Focal [57] and L p norm [82] typically improve calibration by penalizing the confidence of the whole example set to a low level. However, this will lead to undesirable effects: erasing important information about the hardness of samples [87], which is useful for keeping the discrimination ability. This is also evident from Fig. 5: the average confidence of correctly classified samples is obviously reduced during training, making it harder to separate correctly classified and misclassified examples. Besides, the confidence distribution in Fig. 5 (Right) also shows that better calibration may lead to worse discrimination: following the definition of grouping loss, we estimate the density of instances with the same confidence score of 0.95, and mark the results in orange (for LS) and blue bars (for baseline). We observe that although LS leads to calibrated confidence, it unfortunately increases the grouping loss (less discrimination). As a result, correct and wrong samples are hard to separate according to the confidence ranking. Actually, calibration measures an aggregated mismatch between the average accuracy and confidence, without considering the confidence separation between correct and wrong predictions. While the discrimination alone does not equal to failure prediction because a score estimator with high discrimination may assign high confidence for misclassified samples while low confidence for correctly classified samples. Therefore, based on proper score decomposition, good calibration and discrimination are necessary and sufficient characteristics of accurate probabilistic estimation. Section 4 will show that our method can achieve both good failure prediction and calibration performance.

x ood  misInD  ood  correct  correct  ② ② ① in) | (x p in) | (x p out) | (x p

Fig. 6: Illustration of the misalignment between the rejection rules of failure prediction and OOD detection.

#### 3.3.2. Discussion on OOD detection for Failure Prediction

In safety-sensitive applications, both OOD and misclassified InD samples result in significant loss, and therefore should be rejected and handed over to humans. However, as shown in Section 3.2, OOD detection methods often make it harder to detect misclassified samples. To further understand the negative effectiveness of OOD detection methods for failure prediction, we revisit the reject rules of Bayes-optimal classifier for failure prediction and OOD detection, respectively. Proposition 2. (Bayes-optimal Reject Rule for Failure Prediction). For the risk of failure prediction R f p (f, g) in Definition 3, the optimal solution g * of minimizing R f p (f, g) is given by Chow's rule [88], [89]:

g * (x) = I(max y∈Y P(y|x) ≥ 1 -c),(8)

where c ∈ (0, 1) is the reject cost. This rule can not be directly used because the true posterior probability P(y|x) is unknown in practice.

Proposition 3. (Bayes-optimal Reject Rule for OOD Detection). For the risk of OOD detection R ood (g) in Definition 2, the optimal solution g * of minimizing R ood (g) is:

g * (x) = I([p(x|in)/p(x|out)] > [(1 -π in )/π in ]),(9)

where π in ∈ (0, 1) is the mixture ratio of InD and OOD data of the unknown distribution.

Misalignment of Reject Regions. As can be observed from Proposition 2 and Proposition 3, the Bayes-optimal reject rule for failure prediction is based on maximum class-posterior probability max y∈Y P(y|x), while OOD detection rejects samples with small density ratio p(x|in)/p(x|out). Fig. 6 presents an illustration of the reject regions in the case of two Gaussian classes (with the same variance) in R. Specifically, misclassified InD samples are located in the confused region between different classes where the maximum class-posterior probability is low. Based on the Bayes-optimal reject rule, the reject region is Ω misInD . As for OOD samples, they have no information in the training set and can be noise or semanticshifted examples from new classes [90], [91], [92], [93]. The common character of OOD samples is that they are far from the known classes' centroids [94], as shown in region ➀ and ➁ in Fig. 6. Based on the Bayes-optimal reject rule, the reject region Ω ood is located on the two sides (➁) and around the origin (➀). Particularly, the OOD reject region ➀ is overlapped with Ω misInD . Therefore, the MSP score, which rejects the region between two classes, could serve as a strong, common baseline for both misclassification and OOD detection [8].

To detect those OOD samples located in ➁, MSP is incompetent because those regions have high MSP score, as shown by the red dotted line in Fig. 6. This situation is exactly opposite to the failure prediction. Proposition 3 indicates that the density ratio of InD and OOD is the optimal rule for detecting OOD samples, which can be observed in Fig. 6. To this end, many popular OOD detection methods perform density estimation explicitly or implicitly [63]. For example, Outlier Exposure (OE) [33] performs similarly to the binary discrimination between InD and OOD data, and Bayes-optimal solution of Energy-based OOD detection criterion [29] is equivalent to the Bayes-optimal reject rule stated in Proposition 3 [63]. However, to separate InD and OOD, binary discrimination would compress the confidence distribution of correct and incorrect InD samples, and the density based rule like energy score is unsuitable for detection misclassified samples. Therefore, OOD detection methods often harm failure prediction.

## 4. FINDING FLAT MINIMA FOR RELIABLE CONFI-DENCE ESTIMATION

As reported in Section 3, none of those popular calibration and OOD detection methods seem to address failure prediction problem (stably) better than simple baseline [8].

In this section, we answer the following two fundamental questions: (1) Does there exist a more principled and hasslefree strategy to improve failure prediction? (2) Is it possible that the performance of calibration, OOD detection, and failure prediction be improved concurrently?

### 4.1. Motivation and Methodology

#### 4.1.1. Motivation

Connection between flat minima and confidence separation. Confidence separability between correct and incorrect samples is crucial for failure prediction. Let's consider how confidence separability affects the confidence robustness of correct samples: For a correctly classified sample, to become misclassified, it must reduce the probability on the ground truth class and increase its probability on another (wrong) class. During this process, the confidence margin plays a crucial role: a larger confidence margin could make it harder to change the predicted class label. Interestingly, flatness of a model reflects how sensitive the correctly classified samples become misclassified when perturbing the weights of a model [44], [45], [46]. As illustrated in Fig. 8, with flat minima, a correct sample is difficult to misclassify under weight perturbations and vice versa. Therefore, we conjecture that the confidence gap between correct and incorrect samples of a flat minima is larger than that of a sharp minima.

Representation learning and Uncertainty. Misclassification with high confidence means that the sample is mapped into the density region of a wrong class. This is often attributed to spurious correlations appearing in the sample and the wrong class. Flat minima have been theoretically proved to result in invariant and disentangled representations [95], which is effective for spurious representations mitigation [96]. Therefore, with fewer spurious or irrelevant representations, the misclassified sample would be near the decision boundary with low confidence and less activated for wrong classes. Besides, it has been shown that flat minima correspond to regions in parameter space with rich posterior uncertainty [97]. Therefore, flat minima has the advantage of indicating the uncertainty of an input.

### Reliable overfitting phenomenon.

As shown in Fig. 9, we observed an interesting phenomenon that the AUROC can be easily overfitting during the training of a model. Gradient update θ ← θ -α∇L(θ + ε) if i ≥ S and mod(i, c) = 0 then θ t FMFP ← θFMFP t-1 ×s+θ t s+1 else i + +

Concretely, the test accuracy continually increases while the AUROC decreases at the last phases, making it difficult for failure prediction. We term this phenomenon as "reliable overfitting", which exists on different model and dataset settings and is somewhat similar to the robust overfitting [98] in adversarial robustness literature [99]. Since flat minima has been verified to be effective for alleviating robust overfitting [100], [101], we expect it could also benefit failure prediction.

#### 4.1.2. Methodology

There are several methods have been proposed to seek flat minima for DNNs [45], [46], [102], [103]. We select stochastic weight averaging (SWA) [45] and sharpness-aware minimization (SAM) [46] as two representative methods due to the simplicity for proofs-of-concept. Specifically, SWA simply averages multiple parameters of the model along the training trajectory as follows:

θ t SWA = θ SWA t-1 × s + θ t s + 1 ,(10)

where s denotes the number of past checkpoints to be averaged, t is the training epoch, θ is the current weights, θ SWA is the averaged weights. While SAM finds the flat minima by directly perturbing the weights. Specifically, denote the batch-size by m, and the loss computed on the batch data is L = 1 n n j=1 ℓ CE ((x, y); θ), where ℓ CE is crossentropy loss. Then, the optimization objective of SAM is: (11) where ρ ≥ 0 is a given neighborhood. In practice, to efficiently seek the worst-case perturbation, Eq. ( 11) can be approximated by a first-order Taylor expansion of L(θ + ϵ * (θ)) w.r.t. θ around 0 as follows:

min θ L(θ + ϵ * (θ)), where ϵ * (θ) ≜ arg max ||ϵ||2≤ρ L(θ + ϵ),

ϵ * (θ) ≜ arg max ||ϵ|| 2 ≤ρ L(θ + ϵ) ≈ arg max ||ϵ|| 2 ≤ρ (L(θ) + ϵ ⊤ ∇ θ L(θ)) = arg max ||ϵ|| 2 ≤ρ ϵ ⊤ ∇ θ L(θ) ≈ ρ ∇ θ L(θ) ∥∇ θ L(θ)∥ . (12

)

Although the SWA and SAM find flat minima based on different mechanisms, we find they both improve the failure prediction performance. This also motivates us to combine them to get better performance. We refer to the combination of them as FMFP (Flat Minima for Failure Prediction). Algorithm 1 gives pseudo-code for the full FMFP algorithm, which is plug-and-play and can be implemented by a few lines of code.

#### 4.1.3. Theoretical Analysis

In Section 3.3, we show the Bayes-optimal reject rules for failure prediction and OOD detection, and the misalignment of reject regions. Different from existing works which focus on designing various post-hoc scores (e.g., energy score [29], maxlogit score [32], ConfidNet score [40]), a principled and fundamental approach is to learn a Bayes-like classifier. In the following, we demonstrate that the Bayes classifier prefers flat minima based on the PAC Bayesian framework.

PAC-Bayes [104] is a general framework to understand generalization for many machine learning algorithms. Given a prior distribution P and a posterior distribution Q over the classifier weights w, the PAC-Bayes framework bounds the generalization error on the expected error of classifier f w with respect to the KL divergence between the posterior and the prior distributions. Formally, considering a posterior distribution Q of the form w + v, where v is a random variable. Then, we have the following theorem: Theorem 1. (PAC-Bayesian Bound [104], [105]). For any δ > 0, with probability at least 1 -δ over the draw of n training samples, the expected error of f w+v can be bounded as:

E v [L(f w+v )] ≤ E v [ L(f w+v )] + 4 1 n KL(Q||P ) + ln 2n δ ,(13)

where E v [L(f w+v )] is the expected loss, E v [ L(f w+v )] is the empirical loss, and their difference yields the generalization error. Following [105], [100], we choose the perturbation v to be a zero mean spherical Gaussian with variance σ 2 in every direction, and further set σ = α||w||, which makes the second term in Eq. ( 13) become a constant 4

1 n 1 2α + ln 2n δ . Then, substitute E v [ L(f w+v )] with L(f w ) + E v [ L(f w+v )] -L(f w ) ,

the expected error of classifier can be bounded (w.p. 1 -δ over the training data) as follows:

E v [L(f w+v )] ≤ L(f w ) + E v [ L(f w+v )] -L(f w ) + 4 1 n 1 2α + ln 2n δ ,(14)

where E v [ L(f w+v )] -L(f w ) , which is exactly the expectation of the flatness of weight loss landscape, bounds the generalization gap. Therefore, flat minima technique optimizes the flatness E v [ L(f w+v )] -L(f w ) to control the above PAC-Bayes bound, leading to reduced generalization gap and more Bayes-like classifier.

Based on Bayes-optimal reject rules, the Bayes-like classifier learned by flat minima can improve both failure prediction and OOD detection. Specifically, both the performance of (1) maximum class-posterior reject rule (e.g., MSP score) and (2) density reject rule (e.g., energy score) can be boosted, which will be verified by our experiments.

### 4.2. Experiments

Experimental setup. We conduct experiments on CIFAR-10, CIFAR-100, and Tiny-ImageNet [106] with various network architectures. For comparison methods, we mainly compare our method with baseline [8] and CRL [69], which is the stateof-the-art approach for failure prediction that outperforms representative bayesian methods [107], [108]. For CRL, our implementation is based on the official open-sourced code.

For SWA and FMFP, the cyclical learning rate schedule is used as suggested in [45]. For experiments on CIFAR-10 and CIFAR-100, checkpoints at the 120-th epoch of the baseline models are used as the initial point of SWA and FMFP.

Flat minima improves failure prediction. Comparative results are summarized in Table 3 and Table 4. We observe that flat minima based methods: SAM, SWA, and FMFP (ours) consistently outperform the strong baseline, CRL [69] and the state-of-the-art failure prediction method OpenMix [39] on various metrics. Particularly, FMFP generally yields the best results. For example, in the case of ResNet110, our method has 3.94% and 2.47% higher values of AUROC on CIFAR-10 and CIFAR-100, respectively.

Visualization. In Fig. 10, we observe that correct predictions and erroneous predictions of baseline model overlap severely, TABLE 5: Comparison with other methods using VGG-16.

Results with " † " and " * " are from [40] and [76], respectively. making it difficult to distinguish them. Our method remarkably shifts the errors' confidence distributions to smaller values and maintains the confidence of correct samples, which helps to filter out misclassification based on confidence. To be more illustrative, Fig. 11 presents some examples of misclassified samples on CIFAR-10 and their corresponding confidence distribution. Ours outputs much lower confidence on the erroneously predicted class. Besides, the risk-coverage curves in Fig. 12 show that our method consistently has the lowest risks at a given coverage.

### Method

Comparison with ConfidNet and its variants. ConfidNet [40], [10] is a failure prediction method that leverages misclassified samples in training set to train an auxiliary model for confidence estimation. SS [75] improves the generalizability of the auxiliary model via steep slope loss. Qu et al [76] leveraged a meta-learning framework to train the auxiliary model. The performance of those methods is sensitive to the number of misclassified instances in training set. This issue could be mitigated by leveraging a held-out validation set to train the auxiliary model, as in [110]. In this paper, we compare those methods on CIFAR-10 and CIFAR-100 with VGG-16 [111] following the setting in those works [10], [75], [76]. As shown in Table 5, our method consistently outperforms ConfidNet, MCDropout [107] and Trust-Score [74]. Moreover, compared with ConfidNet which is a twostage training method and MCDropout which involves sampling many (e.g., 100) times to obtain Bayesian inference uncertainty, our method is much simpler and more efficient.

Flat minima mitigates the reliable overfitting. Fig. plots the AUROC curves during training. Although the failure prediction performance can be improved by early stopping, the classification accuracy of early checkpoints are much lower (Fig. 9). We can clearly observe that with flat minima, reliable overfitting has been diminished significantly, and the AUROC curves robustly improved until the end. Besides, flat minima can further lead to better classification accuracy, avoiding the trade-off between failure prediction and classification accuracy when applying early stopping.

### Comparison of different weights averaging strategies.

Recently, weight averaging has been a popular way to obtain flat minima. For example, Wortsman et al. [112] proposed model soups technique that averages the weights of fine-tuned large pre-trained models. Here we verify the effectiveness of uniform soup and greedy soup [112]. Different from [112] that averages the weights of multiple models fine-tuned with different hyperparameter configurations, we average the model in the later stage of training i.e., the models after 100 epochs are averaged. As reported in Table 6:

(1) Both uniform and greedy weight average strategies are effective for improving confidence estimation. (2) Uniform soup yields slightly worse accuracy but better confidence estimation performance than the greedy strategy. This is reasonable because the greedy strategy emphasizes accuracy, while a model with higher accuracy may suffer from the reliable overfitting problem, as shown in Fig. 9.

(3) Our method performs better than uniform and greedy strategies.

### 4.3. Failure Prediction in Long Tailed Recognition

Existing confidence estimation methods are typically evaluated on balanced training sets. However, the class distributions in real-world settings often follow a long-tailed distribution, in which the head classes have much more training samples than that of the tail classes [116], [113], [117].

For example, the class distribution of a disease diagnosis is often long-tailed, i.e., the normal samples are more than the disease samples. In such failure-sensitive applications, reliable confidence estimation is especially crucial.

Experimental setup. We use two popular long-tailed classification datasets, CIFAR-10-LT and CIFAR-100-LT [116], which are sampled from the original CIFAR dataset over exponential distributions. Following [113], the default imbalance ratio ρ = 100 is used and the network is ResNet-32.

Our experiments build on code provided by [115].

The challenge of long-tailed failure prediction. We first examine the performance of CRL on long-tailed setting. Specifically, CRL has been demonstrated to be a strong failure prediction method on balanced datasets. However, as shown in Table 7, CRL often results in worse performance in both failure prediction and classification accuracy. Moreover, this challenge can not be solved by combining CRL with state-ofthe-art long-tailed recognition methods LA [113], CDT [114] and VS [115]. Why does CRL fail on long-tailed recognition? An intuitive explanation is that the tail classes are not well learned by the model, and are thus more likely to result in low confidence predictions like the misclassified samples. In Fig. 14, we compare our method (VS based) with TLC under the same experimental setup. The results of TLC and others are from [118]. As can be observed, our method has consistently better failure prediction performance.

### Main results. As can be observed in

### 4.4. Failure Prediction under Covariate-Shifts

Existing confidence estimation works mainly consider the case where the input distribution is static. However, in realworld applications, the deployed systems are running in non-stationary and changing environments and may encode inputs subject to various kinds of covariate-shifts [41]. Take the autonomous driving systems as an example: surrounding environments can be easily changed, e.g., weather change from sunny to cloudy then to rainy [119]. The model still needs to make reliable decisions under these domain shift conditions. Therefore, it becomes necessary to evaluate the confidence estimation performance under covariate-shifts.

Experimental setup. The model is trained on CIFAR-10/100 using the default training setup described in Section 4.2 and evaluated on corrupted dataset CIFAR-10/100-C [120]. Specifically, the corruption dataset contains copies of the original validation set with 15 types of corruptions of algorithmically generated corruptions from noise, blur, weather, and digital categories. Each type of corruption has five levels of severity, resulting in 75 distinct corruptions.

Main results. Fig. 15 shows how the averaged results of 15 types corruptions changed when increasing the corruption severity. The average results for all 75 corruptions are reported in Table 8. As can be seen, our method consistently performs better than baseline and CRL. Fig. 16 plots the AUROC value of failure prediction on the most severe level-5 corruptions. Firstly, we can observe that all the evaluated methods suffer from a varying degree of performance drop compared with the results on the clean test set. This indicates that the predictions under covariate-shifts are less trustworthy. Secondly, our method outperforms CRL and remarkably improves the performance of baseline. For instance, for the model trained on CIFAR-10, our method has 13.05% higher values of AUROC under "defocus" corruption.

### 4.5. Flat Minima Also Improves OOD Detection

A good confidence estimator should help separate both the OOD and misclassified InD samples from correct predictions. Therefore, besides failure prediction, we explore the OOD detection ability of the proposed flat minima base method.

Experimental setup. The InD dataset is CIFAR-10 and CIFAR-100. For the OOD datasets, we follow recent works that use six common benchmarks as follows: Textures [121], SVHN [122], Place365 [123], LSUN-C, LSUN-R [124] and iSUN [125].

During training, the model only sees InD data. At test time, we encounter a mixture of InD and OOD data. For example, the model only sees training set of CIFAR-10 during training; at test time, a mixture of the test set of CIFAR-10 and one OOD dataset. We use the standard metrics in [8] to measure the quality of OOD detection: AUROC, AUPR and FPR95. Supp.Material provides detailed information of the OOD datasets and definitions of the evaluated metrics.

Main results. We report the averaged OOD detection performance over six OOD test datasets in Table 9. The results show that our method can achieve state-of-the-art performance on different datasets and networks. In addition, since our flat minima based method is a training-time technique, it can combine with any other post-processing OOD detection methods such as energy and MLogit to get higher OOD detection performance. To gain further insights, Fig. 17 compares the softmax score histogram distributions of baseline and our method on CIFAR-10 with ResNet110. It is obvious that our method makes the scores more distinguishable between InD and OOD, enabling more effective OOD detection.

## 5. CONCLUDING REMARKS

Reliable confidence estimation could benefit a wide range of risk-sensitive fields that range from health care (e.g., clinical decision making) to transportation (e.g., autonomous driving), and to business applications. In this paper, with rigorous comprehension and extensive experiments, we rethink the reliability of both calibration and OOD detection methods in

The λ ∈ [0, 1] is a random parameter sampled as λ ∼ Beta(α, α) for α ∈ (0, ∞). Thulasidasan et al. [14] empirically found that mixup can significantly improve confidence calibration of DNNs. Similar calibration effect of mixup has been verified in natural language processing tasks [54]. In our experiments, we follow the setting in [14] to use α = 0.2.

Label Smoothing. Label Smoothing (LS) is commonly used as regularization to reduce overfitting of DNNs. Specifically, when training the model with empirical risk minimization, the one-hot label y (i.e. the element y c is 1 for ground-truth class and 0 for others) is smoothed by distributing a fraction of mass over the other non ground-truth classes:

y i = 1 -ϵ, if i = c, ϵ/(K -1), otherwise. (19

)

where ϵ is a small positive constant coefficient for smoothing the one-hot label, and K is the number of training classes. Recently, Muller et al. [13], [14] showed the favorable calibration effect of LS. It has been shown that an ϵ ∈ [0.05, 0.1] performs best for calibration. Therefore, ϵ = 0.05 is used in our experiments.

Focal Loss. Focal Loss [57] modifies the standard cross entropy loss by weighting loss components of samples in a mini-batch according to how well the model classifies them:

L f := -(1 -pi,yi ) γ log pi,yi ,(20)

where γ is a strength coefficient. Intuitively, with focal loss, the gradients of correctly classified samples are restrained and those of incorrectly classified samples are emphasized. Mukhoti et al. [17] demonstrated that focal loss can automatically learn well-calibrated models. We set the hyperparameter γ = 3 following the suggestion in [17].

L p Norm. Recently, Joo et al. [82] explored the effect of explicit regularization strategies (e.g., L p norm in the logits space) for calibration. Specifically, the learning objective is:

L L P (x, y) := L CE (x, y) + λ∥f (x)∥,(21)

where f (x) donates the logit of x, and λ is a strength coefficient. Although being simple, L p norm (e.g., L 1 norm) can provide well-calibrated predictive uncertainty [82]. We use the L 1 norm, which is effective for calibration, as shown in [82], and λ = 0.01 is used in our experiments.

LogitNorm. Wei et al., [34] thought that the increasing norm of the logit during training leads to the overconfident output.

Therefore, they proposed LogitNorm to enforce a constant vector norm on the logits:

L LogitNorm := -log exp(f y /(τ ∥f ∥)) k i=1 exp(f i /(τ ∥f ∥)) ,(22)

where τ denotes the temperature parameter that modulates the magnitude of the logits. Experiments shown that Logit-Norm can produce highly distinguishable confidence scores between ID and OOD data. In our experiments, we use the official open-sourced code in [34].

OE. OE [33] uses auxiliary outliers to help detect OOD inputs by assigning low confidence for the outliers. Specifically, the following objective is minimized:

E D train in [ℓ CE (f (x), y)] + λ E Dout [ℓ OE (f ( x))],(23)

where λ > 0 is a penalty hyper-parameter, and ℓ OE is defined by Kullback-Leibler (KL) divergence to the uniform distribution: ℓ OE (f (x)) = KL(U (y)∥f (x)), in which U(•) denotes the uniform distribution. In our experiments, we use the official open-sourced code in [33].

ODIN. ODIN [27] leverages temperature scaling and input perturbations to separate the softmax score distributions between ID and OOD samples. In our experiments, we set the temperature scaling value to 1000.

energy. Liu et al., [29] found that energy scores better distinguish ID and OOD samples than the widely used softmax scores. Specifically, energy score is computed as:

E(x; f ) := -τ log K i=1 exp(f i (x)/τ ),(24)

where τ denotes the temperature parameter and K is the number of classes. In our experiments, we set the temperature scaling τ to 1.

ReAct. To detect OOD samples, ReAct [31] truncates the high activations during test time. By rectifying the activations, the outsized contribution of hidden units on OOD output can be attenuated, resulting in a stronger separability from ID data.

In our experiments, we set the rectification percentile to 90.

MLogit. MLogit [32] uses the maximum logit score as the confidence, which outperform the maximum softmax score for OOD detection.

CRL. Moon et al., [69] proposed CRL to improve the confidence reliability by reflecting the historical correct rate from the view of training dynamics. The training objective of CRL is as follows:

L CRL (x i , x j ) := max(0, -g(c i , c j )(κ i , κ j ) + |c i -c j |) (25) where c i ∈ [0, 1] is the proportion of correct prediction events of x i over the total number of examinations, and κ i denotes a confidence function (e.g., the maximum class probability, negative entropy, and margin). In our experiments, the implementation is based on the official open-sourced code.

OpenMix. Inspired by the success of Outlier Exposure [33] in OOD detection, OpenMix [39] exploits the easily available outlier samples, i.e., unlabeled samples coming from nontarget classes, for helping detect misclassification errors.

Specifically, it introduces two strategies, named learning with reject class and outlier transformation to improve the failure prediction ability of DNNs.

## APPENDIX C EXPERIMENTAL DETAILS

For SWA and FMFP, the cyclical learning rate schedule is used as suggested in [45]. For experiments on CIFAR-10 and CIFAR-100, checkpoints at 120-th epoch of the baseline models are used as the initial point of SWA and FMFP. For experiments on Tiny-ImageNet [106], the models (ResNet-18 and ResNet-50) are trained from sketch using SGD with a momentum of 0.9, an initial learning rate of 0.1, and a weight decay of 5e-4 for 90 epochs with the mini-batch size of 128.

The learning rate is reduced by a factor of 10 at 40, and 70 epochs. Checkpoints at 50-th epoch of the baseline models are used as the initial point of SWA and FMFP. The details of the OOD datasets used for OOD detection are as follows.

• Textures [121] is an evolving collection of textural images in the wild, consisting of 5640 images, organized into 47 items.

• SVHN [122] contains 10 classes comprised of the digits 0-9 in street view, which contains 26,032 images for testing.

• Place365 [123] consists in 1,803,460 large-scale photographs of scenes. Each photograph belongs to one of 365 classes.

• LSUN [124] has a test set of 10,000 images of 10 different scene categories. Following existing works, we construct two datasets, LSUN-C and LSUN-R, by randomly cropped and downsampling LSUN test set, respectively.

• iSUN [125] is a ground truth of gaze traces on images from the SUN dataset. The dataset contains 2,000 images for the test.

## Figures et tableaux

**Fig. 3:** Comparison of risk-coverage curves. At a given coverage, the lower risk is better. ResNet110 on CIFAR-10.

**Fig. 4:** 3. 3 Further Fig.4: Large-scale experiments on ImageNet[78].

**Fig. 5:** Average confidence of correct samples during training and confidence distribution of correct and misclassified samples. ResNet110 on CIFAR-10.

**Fig. 7** (ResNet110 on CIFAR-10) confirms that those OOD detection methods lead to more overlap between misclassified and correctly classified InD data compared with baseline, i.e., standard training with MSP confidence score.

**Fig. 7:** Due to the misalignment of reject regions, OOD detection methods often lead to worse confidence separation between correct and misclassified InD samples.

**Fig. 8:** An intuitive relationship between flatness and failure prediction. The stability of predictions to parameter perturbations can be seen as a confidence margin condition. This inspires us to improve failure prediction by finding flat minima.

**Fig. 9:** Reliable overfitting phenomenon. Test accuracy continually increases while the AUROC decreases at the last phases. ResNet110 on CIFAR-10.

**Fig. 10:** Fig.10: Our method leads to a better separation between the confidence distribution of correct and misclassified samples, which significantly improves the failure prediction performance.

**Fig. 11:** Predictive distribution on misclassified samples.

**Fig. 12:** Comparison of risk-coverage curves on CIFAR-100.

13

**Fig. 13:** Flat minima can effectively mitigate the reliable overfitting problem, and the AUROC curves continually improved until the end. ResNet110 on CIFAR-10.

**Fig. 14:** Fig.14: Comparison with the results in[118].

**Fig. 15:** Failure prediction under covariate-shift: averaged results of 15 types corruptions under different levels of severity on (a) CIFAR-10 and (b) CIFAR-100 with ResNet110.

**Fig. 16:** AUROC (%) on distribution shift scenarios. CIFAR-10-C and CIFAR-100-C are corruption datasets that contain 15 types of corruption, each with 5 levels of severity. The figure shows the performance on each type of corruption under the severity level of 5. Our method significantly improves the AUROC values of the strong baseline and CRL.

**Fig. 17:** Confidence distribution of InD and OOD samples.

**TABLE 1:** Failure prediction performance on CIFAR-10 and CIFAR-100. AURC and E-AURC values are multiplied by 10 3 for clarity, and all remaining values are percentage. The means and standard deviations over three runs are reported.

    Network | Method |  |  |  | CIFAR-10 |  |  |  | CIFAR-100 |  | 
     | baseline [8] | 9.52 | 7.87 | 43.33 | 90.13 | 99.17 | 40.09 94.30 89.05 | 49.71 | 65.65 | 84.91 | 93.65 | 65.77 73.30
     | mixup [14] | 16.27 | 14.84 | 40.71 | 86.21 | 98.45 | 39.45 94.69 87.39 | 53.38 | 62.95 | 84.60 | 93.27 | 64.38 75.08
     | LS [13] | 25.89 | 23.96 | 45.98 | 81.41 | 97.48 | 37.89 93.86 110.60 71.98 | 64.62 | 82.40 | 90.79 | 63.97 73.53
     | Focal [17] | 9.89 | 7.98 | 41.40 | 90.66 | 99.16 | 43.71 93.87 89.70 | 49.78 | 65.94 | 84.63 | 93.64 | 64.96 73.11
    ResNet110 | Lp [15] | 13.13 | 11.14 | 43.68 | 88.15 | 98.82 | 42.46 93.76 122.37 74.71 | 66.79 | 82.08 | 90.15 | 65.75 70.76
     | LogitNorm [34] 12.57 | 9.79 | 56.27 | 88.82 | 98.96 | 38.72 92.64 118.00 73.45 | 73.09 | 79.56 | 90.54 | 58.73 71.68
     | OE [33] | 10.10 | 8.11 | 46.89 | 90.02 | 99.14 | 43.45 93.76 103.06 56.76 | 71.11 | 83.81 | 92.62 | 63.97 71.16
     | ODIN [27] | 20.82 | 19.16 | 59.32 | 79.45 | 97.99 | 28.49 94.30 167.53 127.71 79.64 | 68.95 | 84.11 | 46.94 73.30
     | energy [29] | 15.13 | 13.47 | 53.89 | 84.72 | 98.59 | 33.00 94.30 128.66 88.85 | 73.54 | 76.80 | 88.73 | 55.02 73.30
     | ReAct [31] | 17.67 | 16.01 | 69.70 | 79.86 | 98.33 | 21.50 94.30 128.02 88.20 | 81.21 | 74.87 | 88.93 | 48.84 73.30
     | MLogit [32] | 14.93 | 13.27 | 53.01 | 85.00 | 98.61 | 34.15 94.30 125.38 85.57 | 70.61 | 77.73 | 89.12 | 57.16 73.30
     | baseline [8] | 4.76 | 3.91 | 30.15 | 93.14 | 99.59 | 42.03 95.91 46.84 | 27.01 | 56.64 | 88.50 | 96.79 | 62.85 80.76
     | mixup [14] | 5.30 | 4.76 | 29.68 | 90.79 | 99.51 | 38.29 96.71 46.91 | 29.84 | 56.05 | 87.61 | 96.51 | 60.42 82.51
     | LS [13] | 17.24 | 16.40 | 34.78 | 83.59 | 98.31 | 39.86 95.92 55.35 | 36.00 | 57.55 | 86.82 | 95.71 | 61.93 80.99
     | Focal [17] | 5.65 | 4.83 | 32.94 | 92.20 | 99.50 | 40.01 95.98 49.34 | 29.21 | 58.63 | 87.70 | 96.53 | 61.65 80.62
    WRN-28-10 | Lp [15] | 6.14 | 5.24 | 33.18 | 91.90 | 99.46 | 42.24 95.79 57.18 | 36.23 | 57.32 | 86.68 | 95.66 | 62.13 80.25
     | LogitNorm [34] 5.81 | 4.78 | 46.06 | 91.06 | 99.50 | 35.69 95.50 72.05 | 48.52 | 66.32 | 82.23 | 94.17 | 55.64 79.11
     | OE [33] | 4.83 | 3.92 | 38.78 | 93.09 | 99.53 | 44.10 95.53 58.05 | 34.29 | 62.96 | 86.36 | 95.88 | 61.39 79.01
     | ODIN [27] | 20.37 | 19.53 | 62.04 | 74.70 | 97.99 | 22.11 95.91 72.58 | 52.54 | 65.22 | 81.02 | 93.77 | 52.98 80.76
     | energy [29] | 6.91 | 6.06 | 39.13 | 90.47 | 99.37 | 37.02 95.91 57.30 | 37.27 | 64.15 | 85.05 | 95.58 | 55.75 80.76
     | ReAct [31] | 5.36 | 4.52 | 31.60 | 92.16 | 99.53 | 40.77 94.78 57.02 | 36.98 | 62.33 | 85.43 | 95.60 | 58.06 80.76
     | MLogit [32] | 6.85 | 6.01 | 37.01 | 90.60 | 99.38 | 38.05 95.91 56.07 | 36.03 | 61.57 | 85.62 | 95.72 | 58.08 80.76
     | baseline [8] | 5.66 | 4.27 | 38.64 | 93.14 | 99.55 | 41.96 94.78 66.11 | 37.25 | 62.79 | 86.20 | 95.43 | 62.19 76.96
     | mixup [14] | 9.55 | 8.24 | 37.21 | 89.87 | 99.14 | 41.42 94.92 63.76 | 37.30 | 63.94 | 86.09 | 95.61 | 61.78 77.82
     | LS [13] | 20.31 | 18.80 | 41.77 | 82.79 | 98.03 | 38.74 94.56 71.37 | 41.85 | 64.44 | 85.47 | 94.84 | 62.30 76.71
     | Focal [17] | 6.70 | 5.03 | 37.97 | 92.74 | 99.47 | 45.99 94.29 69.83 | 38.69 | 64.98 | 86.07 | 95.22 | 62.44 76.11
    DenseNet | Lp [15] | 13.45 | 11.69 | 41.88 | 87.45 | 98.77 | 41.63 94.14 81.66 | 46.67 | 66.09 | 84.85 | 94.15 | 63.04 74.74
     | LogitNorm [34] 10.89 | 8.78 | 56.59 | 88.70 | 99.07 | 36.45 93.59 116.35 76.48 | 74.81 | 78.14 | 90.32 | 55.59 73.13
     | OE [33] | 8.23 | 6.48 | 45.86 | 91.44 | 99.33 | 42.51 94.14 86.96 | 48.29 | 70.39 | 84.25 | 93.90 | 61.91 73.51
     | ODIN [27] | 15.37 | 13.97 | 61.77 | 82.02 | 98.54 | 26.03 94.78 110.50 80.71 | 76.37 | 75.71 | 90.14 | 48.78 76.96
     | energy [29] | 8.60 | 7.20 | 51.31 | 89.21 | 99.25 | 33.81 94.78 100.13 70.34 | 74.46 | 78.03 | 91.38 | 51.02 76.96
     | ReAct [31] | 7.80 | 6.40 | 55.06 | 89.93 | 99.33 | 32.06 94.78 135.73 105.94 86.93 | 68.05 | 87.28 | 36.69 76.96
     | MLogit [32] | 8.38 | 6.98 | 48.96 | 89.57 | 99.27 | 35.49 94.78 96.69 | 66.90 | 70.52 | 79.14 | 91.78 | 53.91 76.96

**TABLE 2:** Temperature scaling can hardly improve failure prediction. The metric used is AUROC.

    Method |  | CIFAR-10 |  |  | CIFAR-100 | 
     | ResNet WRNet DenseNet ResNet WRNet DenseNet
    baseline | 90.76 | 93.24 | 92.87 | 85.00 | 87.75 | 86.46
    TS-valid | 89.15 | 92.30 | 91.05 | 84.66 | 87.55 | 85.82
    TS-optimal 90.88 | 93.47 | 93.11 | 85.01 | 87.77 | 86.48

**TABLE 3:** Confidence estimation performance on CIFAR-10 and CIFAR-100. AURC and E-AURC values are multiplied by 10 3 for clarity, and all remaining values are percentage. The means and standard deviations over three runs are reported. 30±1.04 65.03±0.70 86.63±0.28 94.91±0.13 66.02±0.67 74.01±0.10 10.13±0.20 10.49±0.00 37.62±0.04 OpenMix [39] 73.84±1.31 41.79±0.77 65.22±1.35 85.83±0.22 94.80±0.10 62.87±1.20 75.77±0.35 11.54±0.26 10.62±0.13 36.54±0.35 SAM 74.09±0.53 40.39±0.70 65.61±0.19 86.08±0.20 94.96±0.09 63.61±0.23 75.19±0.17 10.24±0.18 10.36±0.13 36.71±0.31 SWA 69.01±0.96 36.51±0.32 64.00±0.91 86.72±0.26 95.48±0.02 64.63±1.53 75.61±0.40 4.40±0.33 8.49±0.06 33.94±0.34 ours 67.

    Network | Method

08±1.23 34.55±0.33 61.49±1.47 87.38±0.21 95.71±0.05 66 84±0.90 27.01±1.23 56.64±1.33 88.50±0.44 96.79±0.14 62.85±1.04 80.76±0.18 7.10±0.20 7.95±0.08 28.21±0.12 CRL [69] 42.38±0.41 23.71±0.18 57.09±2.02 89.01±0.23 97.21±0.01 62.09±1.63 81.31±0.28 3.54±0.20 6.95±0.02 26.53±0.09 OpenMix [39] 39.61±0.54 23.56±0.50 55.00±1.29 89.06±0.11 97.25±0.06 62.16±0.80 82.63±0.06 3.16±0.50 6.71±0.09 24.93±0.25 SAM 42.43±0.07 24.76±0.28 57.50±1.54 88.62±0.26 97.09±0.03 61.62±1.46 81.80±0.13 5.23±0.09 7.15±0.02 26.54±0.11 SWA 38.10±0.29 20.82±0.42 57.51±0.42 89.69±0.23 97.57±0.05 62.34±0.97 82.00±0.07 7.10±0.07 6.83±0.04 26.32±0.10

     | baseline [8] | 66.11±1.56 37.25±1.03 62.79±0.83 86.20±0.04 95.43±0.14 62.19±0.52 76.96±0.20 8.00±0.20 9.16±0.05 33.70±0.16
     | CRL [69] | 61.93±1.97 33.89±0.96 62.83±1.67 87.01±0.13 95.86±0.13 63.01±1.07 77.27±0.40 4.76±0.24 8.18±0.13 32.04±0.48
    DenseNet | OpenMix [39] 53.83±0.93 29.98±0.20 62.22±1.15 87.45±0.18 96.40±0.04 61.42±1.27 78.97±0.31 4.25±0.38 7.62±0.15 29.92±0.34
     | SAM | 59.51±0.58 32.21±0.45 61.84±0.79 87.44±0.17 96.08±0.05 63.64±0.12 77.56±0.15 6.09±0.15 8.25±0.10 31.77±0.28
     | SWA | 56.16±2.25 30.26±0.70 61.96±1.73 87.70±0.13 96.34±0.11 62.87±1.57 78.13±0.64 4.28±0.42 7.50±0.17 30.44±0.60
     | ours | 53.17±1.

70 28.93±0.95 61.43±2.69 87.82±0.22 96.53±0.12

**TABLE 4:** Confidence estimation on Tiny-ImageNet dataset. ] 124.54±0.97 53.13±0.12 62.45±0.68 86.49±0.11 92.54±0.04 75.10±0.57 65.92±0.43 10.13±0.42 15.76±0.14 CRL [69] 118.05±1.88 49.55±0.75 60.65±1.85 86.62±0.37 93.10±0.09 75.47±1.30 65.39±0.51 7.56±0.64 14.69±0.09 ours 107.

    Network | Method | AURC↓ | E-AURC↓ | FPR95↓ | AUROC↑ | AUPR-S↑ | AUPR-E↑ | ACC↑ | ECE↓ | NLL↓
     | baseline [8 |  |  |  |  |  |  |  |  | 
    ResNet-18 |  |  |  |  |  |  |  |  |  | 

01±1.17 46.88±0.89 62

39±0.07 4.79±0.20 13.17±0.05 ResNet-50 baseline[8] 119.01±3.19 53.05±1.04 63.56±0.20 86.22±0.20 92.66±0.18 73.74±0.61 65.96±0.61 10.14±0.10 15.41±0.26 CRL [69] 110.80±2.33 48.27±1.21 62.01±0.35 87.02±0.18 93.38±0.19 74.15±0.26 66.79±0.31 7.35±0.29 14.23±0.19 ours 98.

43±1.17 42.55±0.89 60.71±1.38 87.71±0.27 94.28±0.11 74.19±0.75 68.49±0.10 4.85±0.20 12.57±0.05

65 36.41±0.45 61.58±0.94 87.47±0.12

     |  | CIFAR-10 | 
     | AURC↓ | E-AURC↓ | FPR95↓ | AUROC↑
    baseline [8] † | 12.66±0.61 8.71±0.50 49.19±1.42 91.18±0.32
    MCDropout [107] † | 13.31±2.63 9.46±2.41 49.67±2.66 90.70±1.96
    Trust-Score [74] † | 17.97±0.45 14.02±0.34 54.37±1.96 87.87±0.41
    ConfidNet [40] † | 11.78±0.58 7.88±0.44 45.08±1.58 92.05±0.34
    SS [75]* | - | - | 44.69 | 92.22
    DeepEnsembles [109]* | - | - | 45.63±0.23 92.15±0.03
    ConfidNet+Meta [76]* | - | - | 44.56±0.21 92.31±0.02
    ours | 6.31±0.18 4.41±0.15 38.48±1.30 93.56±0.26
    Method |  | CIFAR-100 | 
     | AURC↓ | E-AURC↓ | FPR95↓ | AUROC↑
    baseline [8] † | 113.23±2.98 51.93±1.20 66.55±1.56 85.85±0.14
    MCDropout [107] † | 101.41±3.45 46.45±1.91 63.25±0.66 86.71±0.30
    Trust-Score [74] † | 119.41±2.94 58.10±1.09 71.90±0.93 84.41±0.15
    ConfidNet [40] † | 108.46±2.62 47.15±0.95 62.70±1.04 87.17±0.21
    ours | 73.44±0. |  |  | 

**TABLE 6:** Comparison of weights averaging strategy for obtaining flat minima. The model is ResNet110.

    Method |  | CIFAR-10 | 
     | AURC↓ E-AURC↓ | FPR95↓ | AUROC↑ | ACC↑
    baseline | 9.52±0.49 7.87±0.49 43.33±0.59 90.13±0.46 94.30±0.06
    Uniform | 5.46±0.32 3.92±0.20 40.04±3.44 93.65±0.19 94.52±0.26
    Greedy [112] 5.59±0.31 4.15±0.23 41.59±2.46 93.14±0.02 94.68±0.15
    ours | 5.33±0.15 3.71±0.11 39.37±0.77 94.07±0.09 94.36±0.09
    Method |  | CIFAR-100 | 
     | AURC↓ E-AURC↓ | FPR95↓ | AUROC↑ | ACC↑
    baseline | 89.05±1.39 49.71±1.23 65.65±1.72 84.91±0.13 73.30±0.25
    Uniform | 70.32±0.78 37.18±0.46 63.64±0.53 86.74±0.34 75.39±0.36
    Greedy [112] 70.54±0.98 37.54±0.39 64.52±0.30 86.62±0.25 75.44±0.33
    ours | 67. |  | 

08±1.23 34.55±0.33 61.49±1.47 87.38±0.21 75.60±0.39

**TABLE 7:** Failure prediction performance in long-tailed recognition. 13±3.30 38.38±2.00 69.77±0.60 84.52±0.46 79.02±0.63 10.21±0.48 347.43±6.98 129.07±0.86 76.47±1.71 78.46±0.07 41.69±0.70 27.93±0.23 + CRL [69] 63.81±1.55 38.83±0.64 63.05±2.18 85.30±0.43 78.50±0.65 5.70±0.20 345.05±9.21 125.64±3.83 76.19±0.98 78.74±0.58 41.58±0.90 27.50±0.73 + ours 47.

    Method |  |  | CIFAR-10-LT |  |  |  |  | CIFAR-100-LT | 
     | AURC↓ | E-AURC↓ | FPR95↓ | AUROC↑ | ACC↑ | ECE↓ | AURC↓ | E-AURC↓ | FPR95↓ | AUROC↑ | ACC↑ | ECE↓
    LA [113] | 62. |  |  |  |  |  |  |  |  |  | 

78±0.06 29.33±0.15 65.73±2.18 86.41±0.13 81.42±0.10 7.09±0.20 312.64±7.49 114.87±4.89 74.56±0.74 80.02±0.59 44.12±0.34 23.73±0.21 CDT [114] 69.57±1.25 44.55±0.92 71.20±0.28 83.76±0.27 78.48±0.14 17.13±0.11 339.71±8.46 127.40±0.95 79.00±0.66 78.27±0.28 42.40±0.99 34.11±0.52 + CRL [69] 69.92±1.86 43.94±1.03 70.67±0.52 83.91±0.16 78.09±0.35 17.31±0.35 343.88±1.43 131.31±4.69 78.17±0.43 77.88±0.63 42.36±0.55 33.89±0.42 + ours 50.

77±0.69 33.02±0.85 66.31±1.13 85.57±0.50 81.76±0.21 13.85±0.09 313.76±0.76 116.76±2.77 75.15±1.32 79.64±0.43 44.22±0.28 30.97±0.31

    VS [115] | 58.45±2.67 37.19±2.09 70.15±2.08 84.47±0.56 80.11±0.41 12.51±0.23 343.48±6.20 129.50±1.23 77.25±0.63 78.20±0.18 42.20±0.86 31.03±0.33
    + CRL [69] 62.06±0.97 39.88±0.61 67.19±2.05 83.98±0.01 79.69±0.20 11.06±0.64 345.06±7.08 128.35±3.60 77.44±0.81 78.29±0.46 41.88±0.47 30.73±0.81
    + ours | 43.34±1.

55 27.93±1.46 65.60±1.63 86.21±0.54 82.97±0.16 9.66±0.27 308.28±9.88 116.69±3.48 75.38±0.29 79.49±0.40 44.89±0.93 27.02±0.90

     | 86 90 | higher is better | 80 85 | lower is better | Focal Loss OLTR
    AUROC (%) | 74 78 82 |  | FPR95 (%) | 70 75 65 | LDAM-DRW τ-norm cRT RIDE TLC
     | 70 |  |  | 60 | ours
     |  | CIFAR-10-LT | CIFAR-100-LT |  | CIFAR-10-LT | CIFAR-100-LT

**Table 7** 

    , our method
    remarkably improves those long-tailed recognition methods
    in terms of failure prediction. For example, on CIFAR-10-LT
    with VS, ours achieves 4.57% lower average FPR95 (↓) and
    1.74% higher average AUROC (↑) without degrading the
    original classification accuracy. Recently, Li et al. proposed an
    evidence-based uncertainty technique named TLC [118] that
    outperforms many other methods for long-tailed recognition.

**TABLE 8:** Failure prediction performance under covariateshifts. We report the averaged results for 15 kinds of corruption under five different levels perturbation severity.

    Method | AUROC↑ | E-AURC↓ | FPR95↓
     | ResNet WRN DenseNet ResNet WRN DenseNet ResNet WRN DenseNet
     |  | CIFAR-10-C |  | 
    baseline [8] 79.92 83.34 81.82 | 82.61 63.42 | 71.95 | 70.23 64.48 68.56
    CRL [69] | 82.57 85.86 83.86 | 68.82 48.44 | 61.87 | 68.26 62.86 66.93
    ours | 85.20 88.10 85.69 | 52.50 37.15 | 50.56 | 64.36 57.38 63.83
     |  | CIFAR-100-C |  | 
    baseline [8] 77.39 79.70 75.86 | 128.06 105.69 127.13 | 76.70 72.77 76.88
    CRL [69] | 79.00 80.71 78.15 | 117.24 96.67 112.59 | 74.68 71.13 75.25
    ours | 80. |  |  | 

56 82.68 79.29 99.74 82.24 103.51 73.05 69.87 73.59

**TABLE 9:** OOD detection performance. All values are percentages and are averaged over six OOD test datasets.

    Method | FPR95↓ | AUROC↑ | AUPR↑
     | ResNet WRN DenseNet ResNet WRN DenseNet ResNet WRN DenseNet
     | InD: CIFAR-10 | 
    baseline [8] | 51.69 40.83 48.60 | 89.85 92.32 91.55 | 97.42 97.93 98.11
    LogitNorm [34] 29.72 12.97 19.72 | 94.29 97.47 96.19 | 98.70 99.47 99.11
    ODIN [27] | 35.04 26.94 30.67 | 91.09 93.35 93.40 | 97.47 97.98 98.30
    energy [29] | 33.98 25.48 30.01 | 91.15 93.58 93.45 | 97.49 98.00 98.35
    MLogit [32] | 34.61 26.72 30.99 | 91.13 93.14 93.44 | 97.46 97.78 98.35
    CRL [69] | 51.18 40.83 47.28 | 91.21 93.67 92.37 | 98.11 98.67 98.35
    ours | 39.50 26.83 35.12 | 93.83 96.22 94.88 | 98.73 99.23 98.95
    ours+energy | 24. |  | 

71 10.37 15.85 95.75 98.08 96.99 99.10 99.59 99.34 InD: CIFAR-100

    baseline [8] | 81.68 77.53 77.03 | 74.21 77.96 76.79 | 93.34 94.36 93.94
    LogitNorm [34] 63.49 57.38 61.56 | 82.50 86.60 82.10 | 95.43 96.80 95.16
    ODIN [27] | 74.30 76.03 69.44 | 76.55 79.57 80.53 | 93.54 94.59 94.78
    energy [29] | 74.42 74.93 68.36 | 76.43 79.89 80.87 | 93.59 94.66 94.86
    MLogit [32] | 74.45 75.27 69.85 | 76.61 79.75 80.48 | 93.66 94.67 94.77
    CRL [69] | 81.67 79.08 75.77 | 72.72 76.81 76.41 | 92.69 94.22 93.85
    ours | 80.19 70.98 79.06 | 72.92 81.54 71.30 | 92.94 95.71 91.89
    ours+energy | 70.69 54.20 68.56 | 80.22 88.46 79.81 | 94.97 97.38 94.53
