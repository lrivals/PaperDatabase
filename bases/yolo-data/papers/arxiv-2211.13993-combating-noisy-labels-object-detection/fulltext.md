---
id: arxiv-2211.13993-combating-noisy-labels-object-detection
title: "Combating noisy labels in object detection datasets"
year: 2022
backend: grobid
---

Abstract-The quality of training datasets for deep neural networks is a key factor contributing to the accuracy of resulting models. This effect is amplified in difficult tasks such as object detection. Dealing with errors in datasets is often limited to accepting that some fraction of examples are incorrect, estimating their confidence, and either assigning appropriate weights or ignoring uncertain ones during training. In this work, we propose a different approach. We introduce the Confident Learning for Object Detection (CLOD) algorithm for assessing the quality of each label in object detection datasets, identifying missing, spurious, mislabeled, and mislocated bounding boxes and suggesting corrections. By focusing on finding incorrect examples in the training datasets, we can eliminate them at the root. Suspicious bounding boxes can be reviewed to improve the quality of the dataset, leading to better models without further complicating their already complex architectures. The proposed method is able to point out nearly 80% of artificially disturbed bounding boxes with a false positive rate below 0.1. Cleaning the datasets by applying the most confident automatic suggestions improved mAP scores by 16% to 46%, depending on the dataset, without any modifications to the network architectures. This approach shows promising potential in rectifying state-of-the-art object detection datasets.

Index Terms-object detection, data cleansing, data quality

## I. INTRODUCTION

Machine learning methods have been widely used for image analysis in recent years. Deep learning (DL), specifically deep neural networks (DNNs), are the typical choice for solving these tasks. Generally speaking, DNN models outperform competing deterministic algorithms. However, the quality of the training datasets has a significant impact on the results of DL algorithms [1]. The eventual correctness of the algorithm depends on the size and quality of such datasets, which can contain hundreds of thousands of annotated images. Due to the importance of such datasets in different sectors, various organizations create them through the collection and tagging of data.

The bulk of training datasets that are freely accessible may only be utilized for non-commercial purposes. Therefore, enterprises must often prepare them on their own. The created datasets are labeled either automatically or by crowdsourcing [2]. Frequently, enterprises hire a third party to verify the label's quality. This third party is often made up of inexperienced workers, so the accuracy of tagging is lacking. Willers et al. [3] demonstrated that the labeling quality is one of the primary reasons for the reliability decline of DL algorithms. We also assessed the influence of label quality on model quality (see Sec. V).

There are many causes of labeling errors, also referred to as label noise. For example, insufficient information in the images to properly identify objects or different opinions of individual annotators [4]. In such cases, detecting label noise may be a good first step to improving the instructions for annotating images, thus contributing to the higher quality of resulting datasets.

The usage of DL algorithms in safety-critical applications (especially for object detection problems in autonomous driving vehicles) requires proving that the training dataset is free of defects and legal constraints. The quality of the training dataset needs to be assured, and therefore, formal methods for proving the trustworthiness of training data need to be included in the development life cycle of object detectors. Moreover, the numerous safety concerns for AI systems point to the necessity of assessing the labeling accuracy of training datasets, but the existing safety standards very weakly address the problem of data labeling quality. ISO/DIS 21448 [5] requires identifying the possible source of limitations for each stage of development of machine learning models and defining corresponding countermeasures. However, the standard recommends only performing a review for the data labeling process. ISO/TR 4804:2020 [6] specifies that a labeling quality report should be provided during the development of the dataset. UL 4600 [7] suggests that perception shall map sensor inputs to the perception ontology with acceptable performance and requires an acceptably low incidence of mislabeled training and validation data. This standard also requires arguments that machine learning training and testing datasets should have an acceptable level of integrity and quality of data labels. However, there are no standardized protocols for label review.

Labeling noise is seldom assessed in real-world settings. But even in parts meant for testing and validation, the error rate in well-known datasets can reach 10% [8]. This error rate may drastically reduce the maximum accuracy of DL algorithms. Furthermore, with such a high rate of labeling errors, it follows that algorithms shouldn't be expected to achieve the maximal accuracy possible. While there are training methods that are designed to offset the impact of the labeling noise in detection problems, such methods usually are not able to directly assess the quality of the labels.

In this paper, we introduce Confident Learning for Object Detection (CLOD). We present an overview of CLOD in Fig. 1. This work builds on confident learning (CL) [9], [10], one of the state-of-the-art techniques for detecting noisy labels in classification tasks. We also extend the method for the evaluation of image recognition datasets from [1] toward the object detection task. To the best of our knowledge, this is the first time the CL technique is applied to object detection to find all types of label issues. Our extensive assessment revealed that the proposed CLOD method can very effectively detect incorrect annotations. As such, this approach can be used in automated evaluation of the quality of object detection datasets.

The main contributions of this paper are the following:

1) We introduce the CLOD algorithm based on confident learning. To the best of our knowledge, it is the first model-agnostic method that focuses on the detection of erroneous labels in object detection datasets, as existing methods focus mainly on offsetting the label noise in the training process. 2) We provide an extensive empirical evaluation using two state-of-the-art datasets: COCO and Waymo using wellknown DNN architectures: Faster R-CNN, RetinaNet and YOLO.

3) We present examples from these two datasets that the proposed method marked as suspicious, revealing that even commonly used datasets can contain erroneous annotations. 4) We experimentally confirm that correction of the automatically identified noisy labels significantly improves the performance of the object detector in comparison to training on noisy data.

II. RELATED WORK Recently, a lot of research focused efforts on labeling noise. The easiest way to assess a training dataset's quality is to thoroughly tag it several times using multiple annotators. The labels that each annotator assigned to each image may then be compared to spot errors. [11] introduced inter-annotator agreement measures that may be used to gauge the degree of agreement among a set number of annotators when assigning category labels. However, because this approach requires annotating the dataset more than once, this significantly raises preparation costs.

There are also fully automated methods dealing with noise in object detection datasets. These studies, however, focus on implementing adaptive, noise-tolerant DL algorithms rather than attempting to quantify the number of false labels discovered. Therefore, it is impossible to utilize these methods to check the correctness of training datasets supplied by an external source. Such methods are only suitable for the training of models on noisy datasets. We present an overview of these methods in the following subsections.

### A. Weighting noisy samples

Reed et al. proposed a modification to the loss function [12] that lowers the impact of labels that might be inaccurate. The authors claim that this technique also permits the use of datasets whose labels are not known in their entirety. The authors tested this method in both image recognition and object detection.

Goldberger and Ben-Reuven developed the S-Model architecture [13] by adding another softmax layer to the DNN model for classification tasks. The authors assume a particular distribution of noise and use the expectation-maximization method.

Different weights are given to the input images by the MentorNet classifier network presented by Jiang et al. [14]. In successive iterations of the algorithm, it gives lower weights to the images whose labels are assigned with low probability. As a result, such images effectively stop contributing to the learning process. The iterative cross-validation approach [15] described in a more recent work identifies which photos from the training classification dataset should be deleted in the following iteration. However, the removed samples are not corrected after detection. The authors demonstrate how a DNN trained with such recurrent pruning performs better.

### B. Ignoring possibly-incorrect labels

[16] introduced co-teaching for classification. This approach utilizes two DNNs to determine whether an image has been erroneously tagged by sharing training datasets. From each mini-batch, the algorithm uses only a fraction of examples with the lowest loss on one network to train the other network. In [17], authors introduce a modification to coteaching [16] to treat objects independently within an image. Standard co-teaching forces one to ignore the whole image as being noisy. In their solution, the authors only select affected annotations in the image. The idea is not to ignore entire images because of a few incorrect annotations.

Another work [18] proposes an additional layer in the Faster R-CNN network to separate errors in the location of the bounding box from the errors in the label. The authors showed that this approach directly separates the erroneous areas from the correct ones. For this, they use the Cross-Iteration Noise Judgment technique. This method assumes that the percent of noisy labels is constant, thus discarding a predefined number of images. Such an assumption cannot be made a priori in real data.

Unfortunately, none of the methods described above can point out if the images were properly tagged or whether they had any atypical content, making the detection task more difficult and degrading the DNN's effectiveness. The goal of these techniques is to elevate the final accuracy of DNNs either by rejecting training samples or lowering their weight in the training process. Even if they select image labels as potentially invalid, they do that for a given constant fraction of examples given as parameters, while this fraction may vary between datasets [8] and should be treated as unknown.

### C. Automatic correction of annotations

A two-step algorithm was proposed in [19] for noise mitigation in object detection datasets. The authors suggest performing class-agnostic bounding box correction, which optimizes the noisy ground-truth boxes regardless of class labels. Then, in the second step, labels are corrected. Both steps adjust all annotations without selecting the incorrect ones. Eventually, this method gradually modifies the training set toward better outcomes of trained DNN models.

In [20], Wang et al. adopted teacher-student networks to mitigate label noise. The method considers network predictions as statistical measurements of the correct bounding boxes. A teacher network is trained on noisy labels, and its outputs are used to estimate the correct bounding boxes to train the student network.

### D. Confident learning-based methods

In computer vision, the detection of erroneous annotations as the main problem to be solved has been addressed so far only for the image recognition problem. The confident learning (CL) introduced in [9] is a promising approach. The method uses N-fold cross-validation, as in [15], but only once rather than repeatedly. CL chooses each class's probability cutoffs separately. The cutoffs decide whether a particular sample can be confidently categorized. If an image is incorrectly yet confidently categorized, it is viewed as incorrectly labeled. Such examples are deleted from the dataset to improve performance. A DNN model is then created using the newly filtered data. The designers of the CL technique used the ResNet-50 architecture to assess the approach's efficacy using a dataset artificially affected by relatively high (20-70%) mislabel probability. Unfortunately, the authors presented no records of how many incorrect images CL eliminated from the dataset. The method, like in the majority of earlier works presented in this section, focuses on improving the final DNN model's classification performance. This approach results in larger improvements than all the other techniques examined here. A recent work [10] adapts CL to multi-label classification tasks. However, it also does not report how many noisy labels were detected. Instead, it only measures the improvement of the classifier's performance. [8] presents examples of how known image datasets have been analyzed using the CL approach. The researchers chose suspicious images and manually checked them to find incorrect labeling. They found that the state-of-the-art datasets for image recognition contain between 0.15 and 10% images with incorrect labels. This is a noteworthy discovery, given that the examined reference databases should be devoid of such errors. Such a significant fraction of wrong labels makes questionable some popular competitions among classifier algorithms that frequently reach accuracy above 99%. Moreover, the number of verified noisy labels in this investigation was only a small part of the initial CL predictions. It suggests that further balancing accuracy versus recall can enhance the performance of the label noise detection with CL.

In [1], Popowicz et. al utilized CL with multiple DNN models to increase the ability to detect noisy labels in image classification datasets. They introduced a parameter, which adjusts the sensitivity of noise detection and proposed using multiple DNN models to increase the detection reliability. This paper was the first work concentrating not on the accuracy of DNN trained on a cleaned dataset, but on the actual detecting capability of the CL technique.

Finally, Tkachenko et. al [21] presented a method for calculating box quality scores in object detection. This is achieved by weighting three kinds of scores: overlook score (object not annotated), badloc score (imprecise bounding box) and swap score (wrong class label). This method does not consider spurious bounding boxes. Authors evaluate ObjectLab and other methods by gauging their performance on a per image basis, i.e. they calculated the image annotation quality by aggregating quality scores of all corresponding boxes. We compared ObjectLab to CLOD by considering the quality of individual bounding boxes in sec. V-E.

## III. CONFIDENT LEARNING

Confident learning (CL) points out suspicious labels by assuming class-conditional noise and estimating the joint probability distribution between noisy and correct labels. This section summarizes the multi-label CL method, as introduced in [10].

For each possible label m, each input example x i in the noisy dataset X is assigned a noisy binary label y m i . It sets

y m i = 1 if x i

has the noisy label m, else y m i = 0. Using modelpredicted label probabilities p m i , the self-confidence score s m i is calculated as

s m i = y m i p m i + (1 -y m i )(1 -p m i )(1)

for each example i and label m ∈ 1, . . . M . Next, the algorithm aggregates self-confidence scores using one of the proposed pooling methods. The authors report that the exponential moving average works well, when compared to other considered pooling methods, thus we use it in this work. For š1 i ≥ . . . ≥ š1 M denoting sorted values s m i the aggregated score s * i is defined as

s * i = S M i where S t i = š1 i if t = 1 αš t i + (1 -α)S t-1 i if t > 1 (2

)

where α is a parameter. The authors of multi-label CL show that a value of α = 0.8 gives good results. Such a formulation makes the aggregated label quality score s * i most heavily influenced by the lowest values of s m i . Similarly to the original CL method [9], the suspected labels may be selected by using the rank-and-prune approach, i.e., by selecting a given fraction of examples with the lowest values of the aggregated self-confidence score s * i .

## IV. CONFIDENT LEARNING FOR OBJECT DETECTION (CLOD)

Existing CL methods cannot directly analyze an object detection dataset. Assigning a set of labels to an example (image) does not take into account bounding boxes. We propose a method for applying CL for the object detection task to generate box quality scores and correction suggestions.

For each image x in the noisy dataset X an object detection model is used to obtain labeled bounding boxes through inference. As the samples are later processed by the CL algorithm, the predictions should be out-of-sample to avoid bias caused by overfitting. Original and model-predicted (MP) boxes are then clustered with the following rules. 1. The clustering is based on a distance threshold. 2. The clustering distance between two boxes a and b is calculated as 1 -IoU (a, b), where IoU is intersection over union. 3. Each cluster must contain only boxes related to the same image.

For clustering of the bounding boxes, we propose agglomerative clustering with single linkage [22]. We then perform reduction, processing each such cluster separately. Fig. 2 provides an overview of the method and Alg. 1 describes the reduction procedure.

From does not contain any boxes from the original noisy dataset, the cluster represents background.

Then elements of the P′ k row are calculated. P′ k,m is equal to the maximum score of model-predicted boxes of label m in current cluster, or 0 if there are no such boxes. Same as in the case of Y ′ k,M +1 , P′ k,M +1 is equal to 1 if the row contains only zeros and 0 otherwise. This element represents the modelpredicted score of background.

Data: C X k , C P k Result: Y ′ k , P′ k for m in 1..M do Y ′ k,m = 1 if m is in labels of C X k else 0; end Y ′ k,M +1 = 1 if M m=1 Y ′ k,m = 0 else 0; for m in 1..M do P′ k,m = max(scores of P′ k where label is m); end P′ k,M +1 = 1 if M m=1

P′ k,m = 0 else 0; This approach can also be extended to formulating suggestions for correcting annotations. In the case of missing, mislabeled, and mislocated annotations, the model predictions that are part of the cluster can be considered suggestions.

## V. EXPERIMENTS

We conducted five experiments to examine the effectiveness of CLOD. The experiments are varied to assess different aspects of this method. We used multiple datasets (see Sec. V-A) and model architectures (see Sec. V-B). We also considered both artificial noise (see Sec. V-C) and real-world noisy labels present in the analyzed datasets.

### A. Datasets

We used Common Objects in Context (COCO) 2017 and Waymo Open Dataset v1.4.0. This choice was dictated by the prominence of COCO in the evaluation of object detection models and the popularity of Waymo in the autonomous vehicle field, which is the main interest of our research team. Please note that the original Waymo dataset was published in the form of an annotated multi-camera video sequences. From each sequence, we extracted 10 front camera frames, equally spaced in time, to work with still images. We also used the Sama-Coco dataset [23] as a human-revised variant of COCO. It is worth noticing that the authors of Sama-Coco added more than 200k object annotations to the original dataset. That means that in their opinion 25% of the annotations are missing from the original dataset. Nevertheless, many of them refer to very small objects and it strongly depends on the labeling policy whether they should be annotated or not.

Additionally, we created a variant of the Waymo dataset in which, due to resource constraints, 12% of the dataset images were manually reviewed by our team. Please refer to Tab. I for details about the datasets.

### B. DNN architectures

We selected three DNN architectures for the experiments. They were Faster R-CNN [24], RetinaNet [25] and YOLO [26]. The choice was dictated by the fact that these are stateof-the-art solutions for object detection. They provide enough variation to evaluate the algorithm's independence on the type of network used to generate predictions. We provide training parameters for these models in Tab. II.

### C. Artificial noise

In some of the experiments, we used artificial label noise. It can be added on-demand and with granular control over its parameters. Moreover, the knowledge of which bounding boxes were disturbed enabled us to thoroughly evaluate our method. To calculate the exact number of true and false positives and negatives we would have to assume that the original dataset was flawless. However, since we are adding high-amplitude noise to already noisy examples only false positive counts should be slightly biased.

We selected five noise types that imitate real-world annotation noise [17], [18], [27]. Uniform label noise was created by changing the labels of bounding boxes to ones selected randomly from the set of labels, with equal probability. Location noise was a disturbance to the location of boxes by selecting a random angle and moving the bounding boxes along this direction by a vector of length proportional to the box's dimensions. Scale noise was growing or shrinking bounding boxes by a fixed factor. Spurious boxes of random dimensions and labels were added to the dataset and missing noise was applied by removing random boxes.

### D. Environment

We performed all of the experiments on a server with an AMD EPYC 7313 16-core processor, RTX A5000 graphics processing unit, and 60 GB of memory. The server was running Ubuntu 22.04, MMDetection 2.28.2, and PyTorch 1.12.1 with CUDA 11.3.

### E. Experiments and results

Noise impact. The purpose of the first experiment was to measure the impact of the annotation noise on the quality of models. We applied artificial noise to increasing fractions of incorrect labels of the COCO training and validation datasets. We trained models and evaluated them using mean average precision at IoU = 0.5. The relationship between evaluation results and the fraction of noisy boxes was recorded and presented in Fig. 4. The results show that every type of training dataset noise significantly decreases the quality of trained models. This effect is consistently greater with larger amounts of noisy boxes. Uniform label noise was the most detrimental to the quality of the models, followed by spurious boxes and missing boxes. Location and scale noise (with the magnitude of 25% of box dimensions) were the least influential. CLOD effectiveness. Next, we evaluated the CLOD algorithm using the same artificial label noise. We trained models on training parts of selected datasets. Then, we added noise to 20% of examples from the corresponding validation datasets. CLOD was used to find the disturbed examples in these validation datasets. We calculated the area under the receiver operating characteristic curve (AUROC) against the label quality threshold for different types of artificial noise. We present the final results in Fig. 5. The proposed method is best at detecting spurious bounding boxes but it detects label noise almost as well. It did not, however, succeed in pointing out low amplitude location and scale noise, showing performance similar to a random classifier. However, it is consistent across different datasets and model architectures.

uniform

A glance at the ROC curves (Fig. 6) reveals that CLOD can detect nearly all types of noise well. Considering all but missing examples, the method points out nearly 80% of noisy boxes with a false positive rate under 0.1. For the missing examples, however, it seems that to achieve the same, one needs to accept a 0.3 false positive rate.

We chose the clustering threshold based on earlier experiments that compared results for a range of thresholds. We included the results in Fig. 7. Highest-scoring thresholds were 0.4, 0.5, and 0.6, which makes 0.5 a good default threshold. CLOD vs state-of-the-art. We also compared CLOD to ObjectLab [21]. Artificial noise (see sec. V-C) was added to 25Then, we ran CLOD and ObjectLab to detect the noisy boxes. We evaluated the performance of the methods by calculating AUROC for every combination of noise types and datasets. The results are presented in Tab. III.

CLOD scored, on average, around 30% higher than Ob-jectLab in detecting missing boxes. It also performed well in detecting spurious examples, which is a case that ObjectLab does not consider. ObjectLab however, scored 14% higher when considering mislabeled boxes in the Waymo dataset. In other cases, the two methods achieved similar scores. Dataset variants. The fourth experiment was to show the performance of CLOD in real-world settings. We compared model quality scores between multiple variants of COCO and Waymo datasets while treating the respective original datasets as a baseline. We used human-revised variants of both COCO and Waymo datasets to further assess the importance of data quality.

Creating the other two variants was the main part of this experiment. We wanted to gauge how accepting CLOD suggestions would affect the overall quality of the dataset. The suggestions datasets are the original datasets with the best 20% of CLOD suggestions applied. The selected datasets were created by matching suggested bounding boxes to those from the human-revised variants based on IoU (>= 0.5).

Both training and validation datasets were corrected because both can contain errors. Additionally, correcting the dataset alters the distribution of labels and sizes of bounding boxes. For example, if numerous small boxes were added to the training dataset but not to the validation dataset, the model would not be evaluated fairly.

We found counterparts for the best 20% of suggestions and applied them to the original dataset. The purpose of creating this dataset was to check what effect accepting good humanprovided modifications and rejecting bad ones has on the quality of the datasets. This is under the assumption that CLOD rates annotations perfectly. We provide the summary of the mentioned datasets in Tab. IV. We compared the mean average precision (mAP) of models trained and evaluated using described variants and recorded the values into Tab. V. Results show that the revised Sama-Coco dataset scores very similarly to the original COCO dataset. This is not the case with the revised Waymo, which scored much lower. The corrections suggested by CLOD scored the highest, and selected datasets came out in between. Additionally, we calculated the Manual inspection. The last experiment was to run CLOD on the original datasets and view annotations that were deemed suspicious. Some examples are presented and commented on below. We also took note of the annotation rating time and peak memory usage. We present these results in tab. VII. On average, CLOD processed approximately 4000 annotations per second. It used approximately 4 KiB of memory per annotation on average. Additionally, having analyzed the distribution of quality scores we concluded that, in the COCO dataset, 25144 annotations (2.8% of the dataset, quality cutoff: 3.9%) should be manually reviewed. When it comes to the Waymo dataset, only 878 annotations (0.4% of the dataset) fell below the 3.9% quality threshold. This threshold was picked by determining the point above which there is a significant increase in the number of boxes with quality scores below it.

The first category of suspicious examples found in the COCO dataset represents groups of objects in a single box (Fig. 8. Each object should be annotated separately. As the first image shows, such cases are not limited to groups of people but also objects like umbrellas.

The second category of boxes are those that label images of people as person. There are three examples in Fig. 9. Two of them are photographs and one is a sculpture. These boxes probably should not have been included in the dataset.

Fig. 8: Groups of objects labeled as one object, COCO. The next category is spurious boxes (Fig. 10). These do not contain specified objects or the presence of such objects is ambiguous.

Some instances of objects are blurry. Examples are shown in Fig. 11. Such objects probably should not have been labeled as they might be very challenging to detect.

The last categories of boxes we found in the COCO dataset were incorrectly placed and mislabeled ones (Fig. 12). An interesting example, presented at the bottom of the figure, contains an ambiguous object that an annotator classified as truck.

In the Waymo dataset we found objects which are difficult to identify because of water on the camera lens (Fig. 13), some mislocated boxes (Fig. 14), boxes that do not appear to contain any objects (Fig. 12) and objects difficult to classify (Fig. 16).

## VI. DISCUSSION

All of the experiments show that CLOD is a viable method for finding incorrect labels in object detection datasets. It is the first method that finds and identifies missing, spurious, mislocated, and mislabeled bounding boxes. Thanks to the suggestion feature, in most cases, dataset reviewers only need to decide whether to keep each suggestion or discard it. Such an approach makes the whole process take less time than traditional relabeling. Noise impact. The results of the first experiment have confirmed that a high-quality dataset is crucial to obtain a highquality model. We parameterized the location and scale noise types, where the parameter specifies the magnitude of the noise, i.e., how much the location and scale are changed. During the first experiments, we set these values at 25%, which caused a relatively small impact on model quality. Increasing this amplitude would have angled these curves further downwards. Eliminating a number of noisy examples equal to 5% of the dataset could improve mAP@50 by as much as 0.085, which in some cases equates to 20% improvement. These results reveal the need for fixing erroneous labels in object detection datasets. CLOD effectiveness. The second experiment has shown that the method can detect all types of noise with notable correctness as confirmed by the AUROC scores. When it comes to disturbed location or scale of bounding boxes, low displacements and scale factors were difficult to detect. On the other hand, CLOD detected boxes with location and scale disturbed by 50% of their dimensions as often as those with other types of noise. CLOD vs state-of-the-art. Comparison of CLOD to Object-Lab yields favorable results for our new method. It provides an additional benefit of detecting spurious boxes while also being more effective in detecting missing ones. However, the ObjectLab might be a better choice when focusing on detecting mislabeled boxes in small, uniform datasets with few possible labels. It's also worth mentioning that while CLOD completed the rating of a given dataset in less time than ObjectLab (39.61 s vs. 42.29 s for COCO and 15.44 s vs. 37.68 s for Waymo), it used around twice as much system memory (921.55 MiB s Dataset variants. The similarity or decrease of mAP scores for revised datasets might be caused by annotation practices that make the object detection task more difficult. Depending on the labeling policy, when very small objects are annotated, we may increase the complexity of the dataset for the model. Therefore, improving quality of the dataset, we can also make it more challenging for the model and decrease the original Manual inspection. Suspicious examples found in original datasets show that the proposed CLOD method can be utilized to find real labeling issues. Browsing low-quality bounding boxes revealed that annotation guidelines are inconsistent or not respected by annotators. In the COCO dataset, there were many images where groups of small objects were marked with a single large box. In the Waymo dataset, bounding boxes often contained almost entirely obscured objects. This is probably due to the fact that this dataset's original form is multi-camera video sequences and point clouds. It means that annotators saw more than single frames from the front camera. Nonetheless, one might argue that a subset of an object detection dataset should still be a valid dataset.

Unfortunately, the problem of noisy labels in object detection databases is weakly addressed in the literature. The stateof-the-art datasets could contain a non-negligible amount of erroneous annotations. Therefore, the results obtained using such data can be considerably biased. There were initiatives to fix popular datasets in the past, like in [28] and [23] but only parts of them were manually reviewed and reannotated. Another example could be [29] in which the authors proved that the evaluation of existing face datasets is biased due to different guidelines for the annotators, and reviewing annotations could significantly improve the evaluation protocol of object detectors. Datasets could be automatically searched using our method to find suspicious annotations. Then, only the images selected by CLOD could be manually re-annotated, thus reducing the cost of such a project.

## VII. CONCLUSION

We have introduced the CLOD algorithm that successfully extends the confident learning method to the domain of object detection. In the experimental study, we have shown that it obtains promising results when applied to the task of evaluating annotations in object detection datasets. Finding incorrect annotations with the achieved accuracy means that it is viable to re-annotate all examples marked by the algorithm as suspicious. The performed experiments proved that stateof-the-art object detection databases contain a non-negligible amount of noisy labels that decrease the maximal performance of the existing object detection architectures. It is probable that by removing noisy labels from these datasets, we could improve the quality and evaluation protocol of well-known publicly available object detection datasets. Moreover, the proposed methodology may improve the trustworthiness of the training datasets for object detection algorithms used in safety-critical applications.

The CLOD source code is available under GNU General Public License v3 here: https://github.com/safednn-group/ safednn-clean.

## Figures et tableaux

**Fig. 1:** A proposed use-case of the CLOD algorithm.

**Fig. 2:** Data flow diagram for CLOD.

Algorithm 1: The reduction algorithm. This way, the whole dataset is processed, cluster by cluster, and the final matrices Y ′ and P′ are fed to the CL algorithm. The results are the aggregated s * k scores for each row k of the Y ′ and P′ matrices. We assign the label quality score s * k to each annotation in the C X k set. If there are no annotations in C X k , we return the model-predicted annotations C P k as possible missing annotations with the quality score of s * k . Similarly to both original and multi-label CL algorithms, a rank-and-prune (removing a percentage of images with the lowest annotation confidence scores) may be used to select the annotations that are the most likely to be erroneous. We can also use the results of clustering to guess what type of error we might be dealing with. Considering each cluster separately:1) If there are only model predictions in the cluster, it indicates a possibly missing annotation (false negative), 2) If there are no model predictions in the cluster, it indicates a possibly spurious annotation (false positive), 3) The presence of annotations and predictions with different labels indicates a possibly mislabeled annotation, 4) The presence of annotations with the same labels indicates a possibly mislocated annotation. See Fig.3for examples of each issue.

**Fig. 3:** Examples of spurious (top left), missing (top right), mislocated (bottom left), and mislabeled boxes (bottom right). Green: original boxes, orange: model predictions.

**Fig. 4:** Influence of different types of noise in the training dataset on model quality. Bands represent the stretch of values across different model architectures.

**Fig. 5:** Effectiveness of the CLOD method in detecting different types of artificial noise. IoU clustering threshold: 0.5. Median from 3 experiments.

**Fig. 6:** Fig. 7: Fig. 6: A few examples of CLOD ROC curves.

**Fig. 9:** Images of people labeled as person, COCO.

**Fig. 10:** Spurious boxes, COCO.

**Fig. 11:** Blurry objects, COCO.

**Fig. 12:** Examples of mislocated boxes (first three) and mislabeled boxes (bottom), COCO.

**Fig. 13:** Objects hardly visible due to water on lens, Waymo.

**Fig. 14:** Incorrectly placed boxes, Waymo.

**Fig. 15:** Ambiguous boxes, Waymo.

**Fig. 16:** Objects that might not be vehicles, Waymo.

[figure sans légende identifiée] each cluster C X Otherwise, it is set to 0. It means that if the current cluster

     | Object detection model
    Noisy dataset | Predictions
    Agglomerative clustering
    Box clusters
    Reduction algorithm
    Noisy labels & predicted probabilities
    Ranking
    Label quality scores
    k notations in k-th cluster and C P C P k , where C X k are original an-k are model predictions in k-th cluster, we calculate one row Y ′ k of the new binary label matrix Y ′ and one row P′ | 

**TABLE I:** Datasets.

    Dataset | Images | Instances
    Common Objects in Context 2017 | 123,287 | 886,284
    training | 118,287 | 860,001
    validation | 5,000 | 36,781
    Sama-Coco | 123,287 1,115,464
    training | 118,287 1,067,995
    validation | 5,000 | 47,469
    partial Waymo Open Dataset v1.4.0 | 10,000 | 230,479
    training | 7,980 | 185,470
    validation | 2,020 | 45,009
    revised p. Waymo Open Dataset v1.4.0 | 10,000 | 229,426
    training | 7,980 | 184,830
    validation | 2,020 | 44,596

**TABLE II:** Training parameters

    Parameter | Faster R-CNN | RetinaNet | YOLO
    Epochs | 12 | 12 | 273
    LR | 0.02 | 0.01 | 0.001
    Batch size | 2 / worker | 2 / worker | 8 / worker
     |  |  | random crop,
    Transforms | resize to 1333x800 (COCO only), random flip, normalization | random resize 320x320 or 608x608 (COCO only), random flip, photometric distortion,
     |  |  | normalization
    Optimizer | Stochastic gradient descent

**TABLE III:** AUROC values for different noise types for CLOD and ObjectLab. The best parameters were determined for all methods by a grid search.

    Noise | Dataset | CLOD ObjectLab
    label | COCO | 0.833 | 0.851
    label | Waymo | 0.746 | 0.854
    location | COCO | 0.855 | 0.835
    location | Waymo | 0.845 | 0.851
    scale | COCO | 0.850 | 0.822
    scale | Waymo | 0.825 | 0.828
    spurious COCO | 0.897 | N/A
    spurious Waymo | 0.967 | N/A
    missing | COCO | 0.710 | 0.524
    missing | Waymo | 0.705 | 0.564

**TABLE IV:** Datasets created using CLOD.

    Dataset | Images | Instances
    COCO Suggestions | 123,287 4,085,931
    training | 118,287 3,924,926
    validation | 5,000 | 161,005
    COCO Selected | 123,287 | 996495
    training | 118,287 | 955,077
    validation | 5,000 | 41,418
    Waymo Suggestions | 10,000 | 178,964
    training | 7,980 | 144,713
    validation | 2,020 | 34,251
    Waymo Selected | 10,000 | 229,426
    training | 7,980 | 184,830
    validation | 2,020 | 44,596

**TABLE V:** Faster R-CNN model quality scores, trained using datasets created using CLOD.

    Dataset | mAP | mAP50 | mAP75
    COCO |  |  | 
    Original | 0.316 | 0.501 | 0.342
    Revised | 0.318 | 0.492 | 0.347
    Suggest. | 0.366 | 0.610 | 0.379
    Selected | 0.356 | 0.572 | 0.379
    Waymo |  |  | 
    Original | 0.310 | 0.548 | 0.316
    Revised | 0.237 | 0.415 | 0.242
    Suggest. | 0.452 | 0.774 | 0.471
    Selected | 0.315 | 0.554 | 0.316

**TABLE VI:** Faster R-CNN model quality scores for various object sizes. , mAP M , mAP L for small, medium, and large objects based on the split provided by the authors of the COCO dataset. We present the results in Fig. VI.

    Dataset | mAPS | mAPM | mAPL
    COCO |  |  | 
    Original | 0.181 | 0.344 | 0.400
    Revised | 0.194 | 0.351 | 0.420
    Suggest. | 0.325 | 0.383 | 0.359
    Selected | 0.252 | 0.367 | 0.414
    metrics mAP S |  |  | 

**TABLE VII:** Time and memory usage during label rating.

    Dataset | Predictions Time [s] Memory [GiB]
    COCO | 3941531 | 1027.97 | 16.95
    Sama-Coco | 3888731 | 1059.9 | 17.35
    partial Waymo | 621403 | 61.75 | 1.74
