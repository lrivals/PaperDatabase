---
id: arxiv-2101.08466-anti-uav-large-multi-modal
title: "Anti-UAV: A Large Multi-Modal Benchmark for UAV Tracking"
year: 2021
backend: grobid
---

## Abstract

Unmanned Aerial Vehicle (UAV) offers lots of applications in both commerce and recreation. Therefore, perception of the status of UAVs is crucially important. In this paper, we consider the task of tracking UAVs, providing rich information such as location and trajectory. To facilitate research on this topic, we introduce a new benchmark, referred to as Anti-UAV, opening up a promising direction for UAV tracking in a long distance with more than 300 video pairs containing over 580k manually annotated bounding boxes. Furthermore, the advancement of addressing research challenges in Anti-UAV can help the design of anti-UAV systems, leading to better surveillance of UAVs. Accordingly, a simple yet effective approach named dual-flow semantic consistency (DFSC) is proposed for UAV tracking. Modulated by the semantic flow across video sequences, the tracker learns more robust class-level semantic information and obtains more discriminative instance-level features. Experiments show the significant performance gain of our proposed approach over state-of-the-art trackers, and the challenging aspects of Anti-UAV. The Anti-UAV benchmark and the code of the proposed approach will be publicly available at https://github.com/ucas-vg/Anti-UAV.

using infrared (IR) images for object tracking [14] [15]. The crucial drawback of infrared images is that it usually has a low resolution, providing inadequate information for trackers. Based on the above analysis, we think it is important to fuse information from visible RGB and IR images for tracking UAVs. Specifically, leveraging multi-modal information is beneficial for learning accurate and robust UAV trackers [16] [17]. For this purpose, a multi-modal dataset is required to study the task of tracking UAV.

To the best knowledge, there is no multi-modal UAV tracking benchmark for UAV. In the community, the tracking datasets mainly contain general objects ( e.g., car and person).

To mitigate this, we introduce a new dataset, Anti-UAV, to facilitate the research on UAV tracking. Anti-UAV contains high-quality and high-definition video sequences of both RGB and IR. Each sequence is annotated with bounding boxes, attributes, and flags indicating whether the target object exists. It is worth noting that RGB and IR video sequences are paired in Anti-UAV. Thus, the proposed dataset supports both singlemodal and multi-modal UAV tracking.

Furthermore, based on the fact that Anti-UAV has only one category, this work proposes a novel training strategy named dual-flow semantic consistency (DFSC), containing class-level semantic modulation (CSM) stage and instance-level semantic modulation (ISM) stage for UAV tracking. On the one hand, all different sequences share one trait: the labeled objects in them are only UAVs, which means the network can utilize the crosssequence features. The tracker in the CSM stage adopts classlevel semantic modulation to retrieve anchors that may contain UAV as far as possible to reduce the intraclass differences. On the other hand, the tracker pays more attention to the finegrained instance-level features to distinguish between the real UAV instance of the current tracking sequence and the similar distractors in the ISM stage. Since the DFSC method only works in training, it will not affect the calculation and time consumption in the inference time.

The main contributions of this work can be summarized as:

• A multi-modal dataset, named Anti-UAV, is constructed. The Anti-UAV dataset consists of 318 RGB-T video pairs with ground-truth in different scenes, where "RGB" and "T" represent visible light and thermal infrared, respectively. It has been released publicly for academic research. • To better evaluate the tracker's performance, an evaluation metric that focuses on judging the state of UAV is given. Experimental evaluation and analysis of more than 40 trackers on Anti-UAV are provided. • A novel training strategy, named dual-flow semantic consistency (DFSC), is proposed specifically for UAV tracking. DFSC guarantees the tracker obtain robust and representative feature after CSM and ISM, finally significantly outperforms the baselines. Served as a large-scale multi-modal benchmark, Anti-UAV drives the future research on the frontiers of tracking UAVs in the wild. With the above innovations and contributions, we have organized the CVPR 2020 Workshop on the 1 st Anti-UAV Challenge. These contributions together significantly benefit the community.

## II. RELATED WORK

In the following, an overview of the various researches on object tracking is given in Fig. 1. The related tasks are grouped into RGB, TIR, and RGB-T based datasets as shown in Tab. I. Then we analyze the similarities and differences between some SOTA trackers and the tracker proposed in this paper.

A. Tracking Dataset RGB Tracking Dataset. There are several datasets for RGB object tracking in Tab. I. In OTB [18] [19] and TC128 [20], each frame of a video sequence is annotated with 11 different properties and vertical borders while 314 video sequences with 14 attributes make up ALOV++ [2]. VOT [21] [22] with 60 video sequences , introduces the rotary bounding box, and studies the object tracking annotation extensively.

More recently, TrackingNet [29] and LaSOT [28] offer large-scale tracking datasets. TrackingNet selects about 30,000 videos to form the training subset from YouTube-BB [43]. As for the evaluation subset, it collects 511 videos whose category distribution is similar to the training subset. LaSOT collects and annotates 14,000 videos manually. GOT-10k [30] covers a broader range of object categories with an one-shot evaluation protocol to avoid bias in evaluating the seen class. TIR Tracking Dataset. Composed of 16 sequences of over 60K frames with high resolution, BU-TIV [33] is intended for various TIR visual tasks including tracking, group motion estimation and counting. LTIR [34] is the first standard TIR object tracking benchmark with 20 sequences, 6 target classes, and an evaluation toolkit. VOT-TIR16 [35], an extension of VOT-TIR15 [34], contains 25 sequences and 8 object classes, making it more challenging than VOT-TIR15. VOT-TIR16 has six challenging subsets used to evaluate specific attributes of the tracker. Lately, LSOTB-TIR [37], a large-scale and highly diverse TIR object tracking benchmark, is constructed with 1400 TIR sequences over 600k frames. RGB-T Tracking Dataset. The OSU-CT dataset [38] contains 6 pairs of RGB-T video sequences with limited size and low diversity. RGBT210 [41], consists of 210 RGB-T video pairs recorded on a mobile platform, which enriches the diversity of the dataset. Li et al. [42] collects a total of 234 video pairs to construct a large RGB-T tracking dataset named RGBT234 including more challenging RGB-T video, baseline algorithms, attributes, and evaluation metrics.

Compared with the above datasets, it is worth noting that the video sequence pairs in Anti-UAV are not aligned, which is more challenging than other RGB-T datasets.

### B. Trackers

RGB Based Trackers. Most traditional trackers mainly base on filtering [44][45][46][47][48][49][50]. In the initialization stage, a discriminative filter is trained based on the minimum mean square error of the result according to the first frame sample. Then, the filter finds the target's position through the response map.

Despite some advantages of correlation filter in precision and efficiency, there are still some drawbacks. The performance of most existing trackers relies on an appropriate search area. In addition, the limitations of negative samples will also limit the ability of the filter to distinguish the background.

Moreover, neural networks are introduced to object tracking. The first attempt to apply deep learning to tracking task is made by Wang et al., who also creatively proposes the deep target tracking framework [51]. Since then, the research on the deep tracker has been widely carried out. From the aspect of structure, these methods can be divided into the methods based on pre-training network combined with correlation filter [52][53][54][55][56][57], siamese-based network [9][10][11][12]58], convolutional neural network [47,[59][60][61][62][63], and so on [64][65][66]. TIR Based Trackers. Since the deep learning method has achieved great success in visual tracking, some works begin to introduce convolutional neural network (CNN) to improve the performance of TIR tracker.

MCFT [67] integrates deep features of VGGNet and correlation filter into a TIR tracker. LMSCO [68] makes a combination of appearance features and motion features to construct a TIR target tracking. As a multi-level similarity model, MLSSNet [69] is proposed for robust TIR tracking under a Siamese Network. Based on the particle filter framework for TIR target tracking, a mask sparse representation deep appearance model [70] is proposed to replace the previous random sampling for searching useful candidates. RGB-T Based Trackers. As thermal infrared sensors are increasingly popular, the number of RGB-T tracking datasets increases. Accordingly, more and more works [71] devote their efforts to study target tracking specifically for RGB-T datasets.

Wu et al. [72] use the spliced image patch of RGB and heat source to represent each sample sparsely in the target template space. The authors of [17] combines the minimal operational tracking results for RGB and thermal mode calculations of sparse representation coefficients. A weighted sparse representation regularized graph [41] is proposed to learn a robust object representation. Besides, some methods based on deep learning [73] and correlation filter [74] have been proposed.

### C. Image-based Training Strategy

Intra-image Training Strategy. Reasonable use of all instances on a single image can improve the performance of the tracker. SPM [75] proposes a Series-Parallel Matching framework for stronger discriminative power and robustness. During the Coarse Match stage, it is expected that the target object can be discovered even though it is undergoing tremendous change in representation. GlobalTrack [76] proposes crossquery loss to enhance the discriminative power of tracker. Notebly, this training strategy is efficient because features are shared in the feature extraction part. But it is essential that the training images belong to the object detection dataset. Only when the training set is such a dataset there will be multiple target bounding box labels on a single image. In contrast, DFSC can be applied to the single object tracking dataset, which focuses on the cross sequence images. Different query-search image pairs are used to improve the robustness of the tracker in the CSM stage. Inter-image Training Strategy. Even if the intra-image training strategy has achieved some achievements, some works begin to focus on cross-image instances to break through current limitations. Copying and pasting over parts of an image or the whole image has been successfully utilized as a training strategy in image classification, object detection, and so on. Due to difficult cases such as occlusion in 2D human keypoints dataset, the authors [77] proposes a data augmentation method including artificially creating occlusion and constructing ambiguous image. This method [78] is also validated on 3D human keypoint dataset, which achieves the state-of-the-art performance. In the classification task, Mixup [79] mixes two random samples in proportion. The results of classification are allocated in proportion. While Cutmix [80] is to cut out a part of the region and randomly fills the region with the pixel values of other data in the training set. The classification results are allocated according to a certain proportion. Unlike the methods mentioned above, the method in this paper copy and paste on the feature level. Besides "copying and pasting" strategies, The authors of [81] introduce the existing detection datasets to enrich the positive sample data and hard negative sample data. As UAV is the only tracking category in Anti-UAV, cross-sequence pairs are used to improve the robustness of the tracker in CSM, which does not introduce additional detection datasets. At the same time, it only operates in the current batch and shares the computation at the feature extraction stage.

## III. ANTI-UAV BENCHMARK

### A. Data Collection

For the feasibility of algorithms' performance evaluation on large-scale Anti-UAV, 318 RGB-T video pairs are collected, each containing an RGB video and a thermal video.

We record various videos of several UAV types flying in the air. In order to ensure the diversity of data, UAVs, mainly from DJI and Parrot, are utilized to collect tracking data as shown in Fig. 2. The videos recorded include two lighting conditions (day and night), two light modes (infrared and visible) and diverse backgrounds (buildings, cloud, trees, etc.). Each video is stored in an MP4 file with a frame rate of 25 FPS.

### B. Annotation

To guarantee the annotation quality of the Anti-UAV dataset, a progressive strategy is adopted to accurately annotate the bounding box of UAV from coarse to fine. There are three stages in the process of data annotation. Coarse Annotation. In the first stage, the data is coarsely annotated: (i) We annotate the attributes/scenes of each video, such as the size of UAVs, the condition of occlusions, possible false target, etc.. (ii) Each video is annotated every 25 frames. The annotation rules of this stage are as follows: If the target appears in the current frame, the flag is set as "1" and vice versa; the UAV is labeled with an approximate rectangle. In the annotation files, the keyword "exist" can be "1" (True) or "0" (False), and the keyword "get rect" can be expressed as "[x1, y1, x2, y2]" (the coordinates of the upper left and lower right corner of the bounding box). Fine Annotation. According to the complexity, the videos are ranked in each scene. Then the top 10 are chosen for further annotation. After selection, there are 30 infrared and visible video pairs left. Based on the results of coarse annotation, each video frame is annotated in detail. Inspection and Correction. After the second stage, there are still some annotating errors such as bounding boxes with the Scale Distribution. The target size of UAV fluctuates widely in the whole Anti-UAV dataset. The size of the UAV object can be calculated as s(w, h) = √ w × h. Hence, the scale distribution of UAV is given in the Fig. 3b for better analysis. It shows that the scale distributions of the three sets are relatively similar. To a certain extent, the scale distribution of the test set looks more centralized and sharper. The average values of the target size of three sets are all less than 40 pixels.

### D. Attributes

The overall performance on Anti-UAV can not reflect the detailed difference between trackers. Provided by binary attribute annotations, the evaluation metric helps identify the Fig. 4: Screenshots taken from Anti-UAV. The challenging attributes are helpful to analyze the shortcomings and advantages of trackers from all aspects. It is worth mentioning that there is no alignment between multi-modal data. Seven attributes are provided as shown in Fig. 4. For better presenting the Anti-UAV, statistics are done for the specific situation of each attribute as shown in Fig. 5. According to the statistical results, the following conclusions can be reached:

• The proportion of OV is relatively larger in the test set.

However, it is not high on the whole. • The case that the target among adjacent frames moves more than 60 pixels takes up a large proportion in Anti-UAV, which is one of difficulties in UAV tracking. • If the SV standard of OTB is followed, almost no sequence will be considered as SV. Therefore, [0.66, 1.5] may be more suitable for UAV tracking. • There are more video sequences captured in the day.

• A large proportion of videos have the attribute of TC.

To comprehensively analyze, TC is divided into three categories more finely. According to the performance of SiamRPN++LT [11] on the infrared set, the complexity levels are divided into easy, medium and hard.

### E. Evaluation Metrics

Anti-UAV is annotated with bounding boxes, attributes and existing flags. Moreover, an empty bounding box list denotes a "not exist" flag. Trackers need to obtain the perception of UAV status. In this case, the presence of UAV in the visual range is introduced into the evaluation metric:

SA = t IOUt × δ(vt > 0) + pt × (1 -δ(vt > 0)) T .(1)

Protocol I. Visible or infrared video sequences are used to evaluate UAV trackers' performance, respectively. Researchers can use any training set except for those with UAV objects. It aims to verify the trackers' performance for UAV tracking without the training of the UAV dataset. Moreover, it can demonstrate the generalization of trackers in Protocol I. Protocol II. Researchers can use visible or infrared training video sequences of Anti-UAV to finetune their trackers or train them from scratch. Protocol II aims to provide a unique UAV tracking evaluation of trackers. Because there are several options for researchers to choose from, so it is essential to point out which performance comes from training data settings.

The IoU t is Intersection over Union (IoU) between each tracking bounding box and corresponding ground-truth. The v are the ground-truth visibility flags (the tracker's predicted p are used to measure the state accuracy). The state accuracy SA is averaged over all frames in a sequence. The average state accuracy of all video sequences mSA is the final evaluation result. Precision and success are introduced to measure the performance of trackers, which is the same as [18]. Otherwise, it will bring an unfair performance comparison.

Protocol III. Researchers are encouraged to explore how to make the most of multi-modal data. The final performance is evaluated on both annotations of visible and infrared video sequences. Unlike the standard multi-modal tracking datasets published, the multi-modal data of Anti-UAV are not aligned, which is a new direction to explore using multi-modal data without alignment to track UAVs in the future.

## IV. METHODOLOGY

Motivation. There is only one class of objects in Anti-UAV dataset -UAV. Therefore, even in different video sequences, the foreground information is related to each other. Inspired by this, the network can combine the features from different video sequences during training so that the feature learned can be more robust. Based on this idea, dual-flow semantic consistency (DFSC) training strategy is proposed.

Overview. As shown in Fig. 6, DFSC training strategy is composed of CSM stage and ISM stage. During the CSM stage, the feature map of search image is modulated by ROI features from different video sequences' query images. In this case, the tracker will focus on potential representation of instances in entire UAV category. Then in ISM stage, the selected proposals will be only modulated by the ROI feature of the current video sequence's query image. In the following, the DFSC training strategy is given in detail.

### A. Class-level Semantic Modulation

The class-level semantic modulation stage is to find candidate boxes containing UAV category objects, which can be regarded as a UAV detection problem. The training strategy of the query guided region proposal network (query-guided RPN) as introduced in GlobalTrack is modified. The specific training strategy modulates the search area by using crosssequence query. The general UAV modulation feature obtained in the CSM stage can be defined as t. Specifically, the crosssequence query modulation is defined as follows,

tij = fCSM (zi, xj) = fout((fz(zi) ⊗ fx(xj))),(2)

where z i denotes the ROI features of the query in i-th sequence, x j denotes the feature of the search image of jth sequence extracted from backbone. Specially, f CSM is the modulater to modulate the intra-sequence and cross-sequence using different combinations of z i and x j . t ij retains the size of x j , and it denotes the modulated feature which will be utilized to generate the proposals. f out is utilized to align the feature channel number of t ij and x j , f z and f x respectively act on z i and x j to obtain the projected feature. ⊗ represents convolution operator.

It is worth mentioning that the value range of i and j is between 0 and the current batch size n. When i and j are not equal, the cross sequence's image modulation method will be adopted. When i and j are equal, the image modulation method degenerates to the intra-sequence.

According to the above definition, the classification and regression part of the tracker are trained in the CSM stage.

In training, the loss function is defined as follows,

LCSM (zi, xi, zj, xj) = Lsame + αLcross = i,j∈n,i=j Lrpn( tij) + α i,j∈n,i =j Lrpn( tij). (3

)

Here α is a weight coefficient for adjusting the ratio between L cross and L same . Both L cross and L same are loss functions of RPN. Here "cross" denotes RPN prediction after crosssequence modulation while "same" denotes PRN prediction after intra-sequence modulation. Specifically, the training loss function of RPN can be expressed as follows

Lrpn( tij) = 1 N cls n L cls (sn, s * n ) + β 1 Nreg n Lreg(pn, p * n ).(4)

Here β is a weight utilized to balance the classification and regression losses, s n and s * n respectively represent the estimated classification score and corresponding groundtruth, while p n and p * n are the location of the n-th proposal and the corresponding groundtruth.

### B. Instance-level Semantic Modulation

In the previous stage, proposals similar to UAV class are chosen. While in ISM stage, the emphasis is on instancerelated information. At this point, the tracker aims to distinguish instances from those with similar appearance information or from complex background.

Given the query of the sequence to which the current feature belongs, proposals will be utilized for classification and bounding box refinement. The instance-level semantic modulation between z and x k is performed as:

tk = fISM (z, x k ) = f out ((f z (z) f x (x k ))),(5)

where x k represents the selected k-th proposals and z represents the ROI feature of the query image that in the same sequence which the current feature x k comes from. f ISM is the modulater to modulate instance-special information into selected proposals. f out keeps tk and x k the same size. f z and f x represent the feature projection modules for z and x k , respectively. denotes the Hadamard production.

Then, the GlobalTrack QG-RCNN training is proceeded. The modulated ROI feature tk will be performed classification and regression to get the results of the tracker as follows,

LISM (z, x) = 1 Npnum k Lrcnn( tk ).(6)

Here N pnum denotes the number of the selected proposals from the CSM stage. For every modulated ROI feature tk , the loss function can be formulated as

Lrcnn( tk ) = L cls (s n , s * n ) + βL reg (p n , p * n ),(7)

where s n and s * n represent the predicted confidence score and corresponding groundtruth, respectively. p n and p * n are the location of the n-th proposal and the corresponding groundtruth.

## V. EXPERIMENTS A. Trackers

Deep learning based trackers [9-13, 22, 59, 60, 75, 76, 89, 91-99] and correlation filters based trackers [16, 44-46, 48, 50, 55, 82-88, 90] are used for comparison under Protocol I and briefly described below.

Trackers based on deep learning need to train on large-scale datasets. In recent years, due to the rapid development of deep learning and hardware, object tracking based on deep learning has made great progress. In this section, different kinds of trackers are introduced. Siamese network family occupies a very important position in the field of single object tracking.

### B. Implementation Details

Hyper-parameters. For protocol II, GlobalTrack is the baseline. There are two settings of hyper-parameters for visible and infrared datasets, respectively.

For Anti-UAV visible dataset, the pre-trained model provided by GlobalTrack is utilized as the initial model. There are 12 epochs in total, and the initial learning rate is set to 0.02, which is then set to 0.002 and 0.0002 at the 8th epoch and the 11th epoch, respectively. Concerning Anti-UAV infrared dataset, the initial weights transferred from Faster RCNN are adopted and then trained with 18 epochs. The learning rate is also set to 0.02, and we decay it to 0.002 and 0.0002 at the 12th, 15th epoch, respectively.

In the training phase of CSM and ISM, the classification and regression losses are respectively cross-entropy and smooth l1, while the batch size is set to 2 per GPU.

Training Set. Anti-UAV infrared dataset is used for training infrared UAV tracker. However, in the visible UAV tracker training, the pre-trained GlobalTrack model utilizes a combination of MS COCO [100], LaSOT and GOT-10k. During the TABLE III: The whole attribute-based performances mSA (%) of baseline trackers on Anti-UAV validation set using the evaluation protocol I. The trackers are ranked in the same way as in Tab. IV. A larger number means better performance. The first-, second-and third-place trackers are labeled with red, blue and green colors respectively. Best viewed in color. In Tab. III and Tab. IV, each tracker is used without any modification. The evaluation results in mSA (%) is given. For infrared sequence, SiamRCNN achieves the best state accuracy score of 74.33% on the validation set and 65.41% on the test set. According to the experimental results, the tracker based on long-term tracking is more likely to achieve higher performances. The long-term tracker's underlying assumption is that tracking the target out of view is possible. In this setting, long-term tracking will generally have a larger search area or search in the whole image to enable the tracker to obtain the vanishing target reappearing position.

Nevertheless, the above mentioned long-term tracker is challenging to achieve a real-time requirement. The order of the tracker is from low to high according to the performance on the test set. Trackers based on deep learning generally have a For instance, OV generally does not appear in the short-term tracker setting. The short-term tracking sequence is usually not as long as the sequence in the Anti-UAV dataset. Meanwhile, because the UAV is generally far away from the camera, it is also challenging to track such a small target. Therefore, many trackers do not perform well on video sequences with LR attribute, especially correlation filter tracker, due to the trackers' anchor setting. Tracking sequences with TC attribute make up a large part of Anti-UAV. TC easy , TC med and TC hard is generated by the tracking difficulty of the corresponding infrared sequence. TC hard is the most challenging attribute. When tracking UAVs in the video sequences with TC hard attribute, it is not easy to distinguish the UAV from the buildings without fine-tuning using the Anti-UAV training set.

On most attributes, SiamRCNN and GlobalTrack perform much better than other trackers for their more sophisticated processing designs. These two trackers achieve comparable performance except for FM, LR and LI. The superiority that over 4.00% mSA of the above three attributes makes SiamRCNN a lead. And on OV and SV, GlobalTrack is slightly ahead while it is reverse on TC. As for the validation set, GlobalTrack has a slight lead over the second tracker on OC and LI, while the performances of SiamRCNN on other attributes are all the best. Especially on OV, TC and LR, SiamRCNN performs far better than other trackers. Thus SiamRCNN performs well on each of the seven attributes.

### D. Evaluation under Protocol II

Here, the finetuning of the GlobalTrack model only with Anti-UAV directly is defined as the normal training strategy. Otherwise, finetuning the GlobalTrack model using the DFSC method only with Anti-UAV is called the DFSC training set, especially OC. Compared with the normal training strategy, DFSC gains the mSA by 1.28%, 0.97% and 0.78% on OC, SV and LR, respectively. In other attributes, performance improvement is limited.

Moreover, for the test set, DFSC gets the best mSA score (62.75%) on TC all , which is higher than the normal training strategy by 1.07%. Compared with normal training strategy, DFSC gains the mSA by 0.89%, 1.21% and 0.98% and on TC easy , TC med and TC hard , respectively.

On the test set, the large-scale training strategy achieves the highest performance in most attributes except TC and OV. However, the whole performance is not as good as DFSC on mSA. On the one hand, the large-scale training strategy uses more data than the normal and DFSC method, which is conducive to learning more general features beneficial to tracking UAVs. On the other hand, after training on the Anti-UAV training set, the tracker has a more discrimination ability on TC scenarios and is more stable in common scenarios.

To validate the proposed DFSC method, the successful tracking sequences from test set are visualized, as shown in Fig. 8. As a consequence, a potential training strategy is demonstrated to handle such great challenges.

### E. Ablation Study

This subsection provides the analysis about the behaviors of the supervised task and α in Eq. 3 for the dual-flow semantic modulation (DFSC) training strategy. Supervised Task. As shown at the middle of Tab. VI, compared with other methods, DFSC-cls achieves the best performance on mSA, but has the lowest performance on success and precision on the infrared dataset. Nevertheless, DFSC-cls only gets a small margin over DFSC. Instead, DFSC-reg obtains a lower mSA but the highest precision and success scores. DFSC-cls makes the tracker own a more accurate UAV state discrimination ability, but its localization ability is not improved relatively. It validates the classification supervised task in the DFSC method to force the tracker to focus on the powerful capability of UAV perception. On the contrary, more attention to the regression task makes the tracker perform better on UAV localization.

Compared with the DFSC method, DFSC-all both adopt cross sequence semantic information to modulate features in the CSM and ISM stage. In both evaluations, DFSC performs favorably compared with DFSC-all. Class-level semantic modulation in the later stage will make the tracker confused about the information from different UAVs. As a result, instancelevel semantic modulation is necessary for the tracker to enhance discrimination power. Influence of Ratio. The α means the ratio between L cross and L same in Eq. 3. As illustrated in the bottom of Tab. VI, mSA sharply fluctuates if the ratio α changes from large to small, in which case DFSC becomes similar to normal method.

With the increase of the ratio α, the performance first increases and then decreases. When the performance reaches the maximum, α is about 0.25. And if α becomes smaller or larger than this value, the performance will decline. This phenomenon is because when α becomes too large, the tracker will unnecessarily focus too much on the cross sequence feature information. It hinders the tracker from learning classlevel semantic feature, which reduces the robustness of the tracker. When α becomes smaller, DFSC will degenerate into the normal training strategy. A moderate ratio (α=0.25) can achieve a trade-off between intra-sequence semantics and cross-sequence semantics.

## VI. CONCLUSION

In the community, there is no high-quality Anti-UAV benchmark for capturing real dynamic scenes. In this paper, the first UAV tracking dataset is constructed, named Anti-UAV, which collects over 300 video pairs and annotates more than 580k bounding boxes manually. Along with the dataset, evaluation protocols, metrics, and baseline trackers are introduced for the task of UAV tracking. Furthermore, a novel approach named dual-flow semantic consistency (DFSC) is proposed for UAVs tracking. DFSC enables the tracker to fully leverage the semantic information across different video sequences, such that tracker's robustness and discrimination ability can be further improved. Notably, the proposed DFSC does not introduce any additional inference time. In the future, multi-modal with unaligned data for tracking will be further investigated, which has the potential to boost the accurateness of trackers.

## Figures et tableaux

**Fig. 1:** Overview of tracking datasets. Unlike other RGB-T datasets, Anti-UAV is composed of unaligned video pairs.

**Fig. 2:** Overview of UAVs for capturing multi-modal data.

**Fig. 3:** UAV's position distribution and scale distribution in each part of Anti-UAV.

**Fig. 5:** The quantity of sequences with different attributes.

**Fig. 6:** The pipeline of proposed DFSC training strategy. This figure shows the case when two video sequences (denoted as Seq i and Seq j) in a batch. There are CSM and ISM branches in the whole DFSC training process. To reduce the intraclass differences, cross-sequence UAV features are used as modulation factors to maintain class-level semantic information consistency in the CSM stage. During the ISM stage, the modulation of the query feature of the same sequence further boosts the tracker's discrimination power by reinforcing instance-level semantic consistency. Best viewed in color.

**Fig. 7:** The success plot and precision plot on Anti-UAV under protocol I. For clarity, only the top 20 trackers are shown.

**TABLE I:** A comparison of Anti-UAV with other single object tracking (SOT) datasets in terms of the number of video sequences, bounding boxes, and attributes. Anti-UAV is much larger than most RGB-T tracking datasets. In the meantime, Anti-UAV is specifically for UAV tracking and provides corresponding training set.

     | Dataset | Total Sequences | Bboxes | Train Sequences | Bboxes | Sequences | Test | Bboxes | Attribute
     | OTB2013 [18] | 50 | 29.4k | - | - | 50 |  | 29.4k | 11
     | OTB2015 [19] | 100 | 59k | - | - | 100 |  | 59k | 11
     | VOT2014 [23] | 25 | 10k | - | - | 25 |  | 10k | 5
     | VOT2017 [21] | 60 | 21k | - | - | 60 |  | 21k | 5
     | VOT2019 [22] | 60 | 19.9k | - | - | 60 |  | 19.9k | 5
     | ALOV++ [2] | 314 | 16k | - | - | 314 |  | 16k | 14
    RGB | TC128 [20] NUS PRO[24] | 128 365 | 55k 135k | -- | -- | 128 365 |  | 55k 135k | 11 12
     | OxUxA [25] | 366 | 155k | - | - | 366 |  | 155k | 6
     | UAV123[26] | 123 | 113k | - | - | 123 |  | 113k | 12
     | UAV20L[26] | 20 | 59k | - | - | 20 |  | 59k | 12
     | Nfs [27] | 100 | 38k | - | - | 100 |  | 38k | 9
     | LaSOT [28] | 1.4k | 3.3M | 1.1k | 2.8M | 280 |  | 685k | 14
     | TrackingNet [29] | 31k | 14M | 30k | 14M | 511 |  | 226k | 15
     | GOT-10k [30] | 10k | 1.5M | 9.3k | 1.4M | 420 |  | 56k | 6
     | OSU-T [31] | 10 | 0.2k | - | - | 10 |  | 0.2k | -
     | PDT-ATV [32] | 8 | 4k | - | - | 8 |  | 4k | -
     | BU-TIV [33] | 16 | 60k | - | - | 16 |  | 60k | -
    TIR | ASL-TID [32] TIV [33] | 9 16 | 4.3k 63k | -- | -- | 9 16 |  | 4.3k 63k | --
     | LTIR [34] | 20 | 11.2k | - | - | 20 |  | 11.2k | 5
     | VOT-TIR16 [35] | 25 | 14k | - | - | 25 |  | 14k | 10
     | PTB-TIR [36] | 60 | 30k | - | - | 60 |  | 30k | 9
     | LSOTB-TIR [37] | 1400 | 606k | 1280 | 524k | 120 |  | 82k | 12
     | OSU-CT [38] | 6 | 17k | - | - | 6 |  | 17k | -
     | LITIV [39] | 9 | 6.3k | - | - | 9 |  | 6.3k | -
    RGB-T | GTOT [40] RGBT210 [41] | 50 210 | 15.8k 210k | -- | -- | 50 210 |  | 15.8k 210k | 7 12
     | RGBT234 [42] | 234 | 233.8k | - | - | 234 |  | 233.8k | 12
     | Anti-UAV (Ours) | 318 | 585.9k | 160 | 294.4k | 91 |  | 168.4k | 7

**TABLE II:** Illustration of attribute annotation in Anti-UAV. As shown in the Fig.3a, the positions of the boxes are mostly concentrated in the central area of the picture, and the larger transverse variance means that the horizontal movements of UAV are in the majority. Besides, the range of motion of the target in the test set is more diverse. The test set's fluctuation is larger than that of the training set in the corresponding directions.

[figure sans légende identifiée] 78% precision score and a 41.54% success score on the infrared test set. The best deep tracker with online learning is Super-Dimp with 78.48% precision score and 55.44% success score.

     |  |  |  |  |  | Infrared |  |  |  |  |  |  | Visible
    Tracker | OV | OC | FM | SV | LI | TCeasy | TC med | TC | TC hard | TC all | LR | All | All
    MOSSE [44] | 23.29 | 4.63 | 5.26 | 8.08 | 28.64 | 48.70 | 27.19 |  | 8.17 | 34.45 | 6.20 | 29.40 | 21.06
    DAT [82] | 15.98 | 6.77 | 8.30 | 9.63 | 30.76 | 36.06 | 20.62 |  | 1.49 | 24.64 | 3.00 | 29.43 | 38.27
    CSK [45] | 21.33 | 8.90 | 6.02 | 8.06 | 40.32 | 53.32 | 44.70 |  | 7.51 | 41.14 | 1.96 | 37.67 | 35.89
    Staple-CA [83] | 21.33 | 10.65 | 7.09 | 14.09 | 36.96 | 55.63 | 46.81 |  | 14.54 | 44.43 | 10.48 | 37.51 | 37.23
    MCCTH [16] | 26.51 | 20.61 | 8.65 | 17.80 | 39.75 | 54.28 | 42.12 |  | 8.81 | 41.29 | 10.29 | 38.10 | 39.49
    Staple [46] | 33.92 | 13.82 | 7.54 | 17.64 | 36.20 | 54.80 | 40.54 |  | 13.01 | 42.09 | 9.81 | 37.62 | 38.15
    CN [48] | 24.74 | 10.12 | 6.93 | 14.74 | 40.78 | 58.34 | 46.32 |  | 11.22 | 45.03 | 10.25 | 39.82 | 36.04
    DCF [50] | 21.15 | 6.93 | 6.95 | 13.32 | 37.57 | 53.64 | 42.68 |  | 9.02 | 41.14 | 11.44 | 36.65 | 36.48
    KCF [50] | 22.04 | 8.85 | 7.50 | 14.21 | 37.91 | 53.41 | 42.94 |  | 9.67 | 41.23 | 11.92 | 36.82 | 38.11
    STRCF [84] | 39.25 | 25.34 | 21.56 | 27.04 | 48.48 | 47.92 | 41.02 |  | 4.47 | 36.69 | 18.34 | 41.65 | 44.92
    LDES [85] | 21.76 | 8.91 | 19.78 | 13.55 | 46.63 | 54.01 | 42.90 |  | 5.05 | 40.52 | 8.92 | 41.41 | 48.98
    DSST [86] | 23.66 | 10.46 | 7.05 | 14.03 | 43.25 | 55.31 | 45.76 |  | 13.55 | 43.79 | 9.29 | 40.54 | 37.48
    CSRDCF [87] | 40.46 | 21.13 | 25.45 | 27.84 | 50.87 | 58.66 | 52.17 |  | 14.53 | 47.39 | 24.77 | 47.73 | 41.54
    BACF [88] | 19.51 | 9.00 | 18.21 | 20.53 | 44.72 | 56.47 | 44.43 |  | 7.06 | 42.65 | 21.99 | 43.16 | 43.87
    SiamFC [9] | 42.10 | 27.99 | 30.28 | 22.83 | 53.41 | 66.36 | 45.80 |  | 10.45 | 48.99 | 16.59 | 49.34 | 44.08
    Ocean-Online [89] | 16.21 | 21.02 | 19.65 | 24.11 | 45.77 | 52.66 | 39.21 |  | 6.09 | 39.11 | 20.33 | 41.56 | 46.45
    MKCFup [90] | 44.60 | 20.13 | 8.64 | 22.57 | 40.81 | 56.95 | 43.91 |  | 13.77 | 44.24 | 10.25 | 41.31 | 40.21
    SiamMask [12] | 40.77 | 27.28 | 24.22 | 24.16 | 47.10 | 54.82 | 38.76 |  | 12.50 | 41.54 | 14.62 | 44.34 | 44.26
    SiamDW [91] | 43.93 | 39.66 | 29.40 | 35.14 | 56.84 | 59.89 | 42.31 |  | 8.29 | 44.21 | 27.87 | 49.46 | 44.90
    SiamBAN [92] | 20.02 | 31.73 | 19.03 | 24.84 | 48.75 | 57.63 | 49.44 |  | 6.44 | 44.39 | 13.38 | 43.60 | 39.90
    RT-MDNet [59] | 43.88 | 20.82 | 18.60 | 27.35 | 46.97 | 64.97 | 44.42 |  | 13.15 | 48.50 | 13.52 | 45.99 | 44.93
    SPM-AlexNet [75] | 39.84 | 24.75 | 30.35 | 27.70 | 51.15 | 56.73 | 34.98 |  | 8.20 | 40.68 | 14.41 | 46.71 | 46.51
    ECO-HC [55] | 23.16 | 14.96 | 25.38 | 28.66 | 52.66 | 60.61 | 48.51 |  | 16.63 | 47.96 | 30.29 | 49.26 | 43.67
    Ocean-Offline [89] | 26.63 | 42.86 | 32.09 | 24.75 | 55.05 | 59.61 | 41.66 |  | 20.76 | 46.62 | 18.60 | 48.74 | 45.74
    MDNet [60] | 45.88 | 24.16 | 23.47 | 31.13 | 50.42 | 65.96 | 48.59 |  | 14.84 | 50.43 | 24.85 | 49.49 | 45.17
    SiamRPN++ [11] | 35.32 | 41.11 | 28.17 | 28.39 | 55.85 | 57.95 | 44.55 |  | 6.94 | 43.44 | 19.71 | 48.60 | 46.12
    SiamRPN [10] | 32.07 | 31.37 | 25.73 | 30.56 | 52.57 | 65.60 | 45.24 |  | 10.83 | 48.53 | 21.97 | 48.16 | 46.63
    SPM-Res18 [75] | 39.75 | 30.78 | 32.25 | 29.56 | 54.90 | 59.16 | 42.55 |  | 12.45 | 44.79 | 17.95 | 49.56 | 46.09
    SiamFCOS [22] | 41.97 | 42.43 | 29.01 | 34.66 | 53.09 | 58.24 | 37.02 |  | 10.07 | 42.40 | 21.94 | 47.71 | 44.28
    ECO [55] | 31.87 | 32.03 | 38.43 | 38.47 | 55.77 | 69.24 | 45.90 |  | 21.67 | 53.00 | 34.25 | 54.44 | 46.31
    SiamCAR [93] | 25.05 | 46.12 | 40.84 | 29.96 | 63.19 | 68.27 | 55.99 |  | 17.55 | 54.11 | 21.67 | 56.70 | 46.52
    KYS [94] | 36.07 | 55.52 | 57.64 | 52.68 | 64.70 | 66.30 | 35.35 |  | 32.05 | 51.07 | 48.00 | 60.50 | 59.79
    ATOM [13] | 63.01 | 55.82 | 56.04 | 46.91 | 65.05 | 65.36 | 50.03 |  | 25.73 | 52.86 | 38.53 | 60.87 | 58.79
    Dimp [95] | 41.96 | 59.85 | 59.95 | 55.78 | 66.33 | 70.19 | 51.62 |  | 30.16 | 56.79 | 47.52 | 63.51 | 61.54
    ATOM-MU [96] | 42.73 | 55.51 | 58.74 | 47.16 | 64.83 | 68.58 | 46.61 |  | 26.26 | 53.83 | 39.18 | 61.27 | 60.45
    SiamRPN++LT [11] | 50.02 | 68.16 | 63.39 | 54.06 | 70.25 | 76.71 | 61.76 |  | 19.25 | 60.40 | 42.66 | 65.84 | 67.15
    SPLT [97] | 33.39 | 58.42 | 55.22 | 42.49 | 63.18 | 73.09 | 58.73 |  | 19.30 | 57.73 | 45.46 | 60.73 | 57.32
    PrDimp [98] | 65.22 | 63.89 | 62.85 | 55.59 | 66.95 | 69.47 | 55.79 |  | 29.04 | 57.21 | 51.12 | 64.54 | 62.95
    LTDSE [22] | 64.39 | 50.17 | 59.04 | 48.67 | 62.69 | 67.18 | 55.89 |  | 27.43 | 55.66 | 42.54 | 61.27 | 66.64
    Super-Dimp 1 | 52.35 | 68.07 | 65.30 | 64.80 | 67.93 | 68.87 | 59.85 |  | 34.22 | 59.03 | 61.45 | 65.76 | 63.05
    GlobalTrack [76] | 69.21 | 78.62 | 73.35 | 66.11 | 76.33 | 76.47 | 63.08 |  | 43.45 | 65.90 | 60.26 | 72.00 | 67.28
    SiamRCNN [99] | 73.46 | 78.24 | 73.98 | 67.97 | 76.19 | 78.21 | 69.55 |  | 55.48 | 71.07 | 67.93 | 74.33 | 74.32
    finetune stage, only the Anti-UAV visible dataset is adopted. |  |  |  |  |  |  |  | 
    C. Evaluations under Protocol I |  |  |  |  |  |  |  |  |  |  | 
    Overall Performance. Fig. 7 shows the success plot and |  |  |  |  |  |  |  | 
    the precision plot of one pass evaluation (OPE) on Anti- |  |  |  |  |  |  |  | 
    UAV. SiamRCNN achieves the best precision score of 95.70% |  |  |  |  |  |  |  | 
    and a success score of 71.52% on the infrared validation |  |  |  |  |  |  |  | 
    set. On the infrared test set, SiamRCNN obtains state-of-the- |  |  |  |  |  |  |  | 
    art results with a 63.60% success score; however, Global- |  |  |  |  |  |  |  | 
    Track shows top performance with precision score of 87.13%. |  |  |  |  |  |  |  | 
    Moreover, SiamRCNN achieves more remarkable performance |  |  |  |  |  |  |  | 
    improvement than the infrared tracking sequence on the visible |  |  |  |  |  |  |  | 

**TABLE IV:** The performances mSA (%) of baseline trackers on the Anti-UAV test set using the evaluation protocol I. The trackers are ranked by their state accuracy scores of infrared video on test set. Larger number means better performance.

     |  |  |  |  |  | Infrared |  |  |  |  |  |  | Visible
    Tracker | OV | OC | FM | SV | LI | TCeasy | TC med | TC | TC hard | TC all | LR | All | All
    MOSSE [44] | 8.89 | 24.16 | 6.02 | 4.06 | 3.56 | 15.23 | 10.34 |  | 5.80 | 10.13 | 3.80 | 13.47 | 15.23
    DAT [82] | 8.01 | 21.94 | 5.33 | 13.53 | 3.11 | 40.57 | 13.28 |  | 6.50 | 17.41 | 3.76 | 22.68 | 27.19
    CSK [45] | 11.51 | 26.97 | 9.56 | 12.35 | 2.71 | 46.51 | 15.63 |  | 5.30 | 19.54 | 3.29 | 24.26 | 28.38
    Staple-CA [83] | 15.60 | 41.11 | 13.29 | 9.03 | 3.64 | 46.25 | 18.27 |  | 7.38 | 21.37 | 5.53 | 25.44 | 31.40
    MCCTH [16] | 11.58 | 33.21 | 9.84 | 9.08 | 4.95 | 41.09 | 20.33 |  | 6.61 | 21.02 | 5.13 | 25.85 | 29.96
    Staple [46] | 14.74 | 44.09 | 11.56 | 11.67 | 3.70 | 44.56 | 21.51 |  | 6.82 | 22.44 | 5.26 | 26.50 | 29.71
    CN [48] | 14.41 | 39.75 | 10.66 | 15.18 | 3.54 | 59.75 | 28.02 |  | 7.93 | 29.33 | 4.81 | 31.72 | 28.65
    DCF [50] | 14.85 | 36.89 | 12.28 | 11.55 | 3.18 | 60.32 | 30.26 |  | 8.80 | 30.80 | 4.25 | 32.55 | 38.39
    KCF [50] | 16.14 | 37.56 | 12.60 | 11.66 | 3.55 | 60.23 | 30.80 |  | 9.17 | 31.16 | 4.36 | 32.88 | 39.40
    STRCF [84] | 15.72 | 44.39 | 14.69 | 20.18 | 7.31 | 59.49 | 28.26 |  | 10.89 | 30.23 | 7.84 | 33.77 | 45.19
    LDES [85] | 16.83 | 40.97 | 17.86 | 16.33 | 8.40 | 60.88 | 28.07 |  | 10.46 | 30.33 | 7.54 | 34.46 | 49.13
    DSST [86] | 14.45 | 41.19 | 12.59 | 15.88 | 3.57 | 69.31 | 30.86 |  | 9.37 | 33.27 | 4.85 | 35.18 | 35.67
    CSRDCF [87] | 13.70 | 46.26 | 12.96 | 19.14 | 4.97 | 61.55 | 32.05 |  | 10.22 | 32.37 | 7.26 | 35.29 | 47.10
    BACF [88] | 16.17 | 41.91 | 15.66 | 16.70 | 4.13 | 70.16 | 33.02 |  | 8.53 | 34.28 | 4.91 | 36.78 | 47.52
    SiamFC [9] | 18.59 | 60.83 | 21.46 | 23.58 | 13.55 | 63.82 | 29.00 |  | 11.02 | 31.60 | 10.36 | 36.97 | 45.69
    Ocean-Online [89] | 17.98 | 41.56 | 14.72 | 17.35 | 3.73 | 68.51 | 32.02 |  | 9.27 | 33.63 | 4.45 | 37.22 | 48.11
    MKCFup [90] | 16.44 | 43.35 | 15.60 | 14.15 | 3.48 | 70.74 | 35.55 |  | 8.92 | 35.76 | 4.88 | 37.41 | 39.52
    SiamMask [12] | 29.09 | 53.55 | 18.73 | 22.03 | 8.14 | 59.32 | 30.42 |  | 17.91 | 33.27 | 10.08 | 37.44 | 45.92
    SiamDW [91] | 19.36 | 38.14 | 17.65 | 22.18 | 8.52 | 57.68 | 36.28 |  | 13.73 | 34.60 | 9.44 | 38.01 | 49.86
    SiamBAN [92] | 14.92 | 33.72 | 16.42 | 18.84 | 4.78 | 72.67 | 39.33 |  | 16.90 | 40.33 | 6.15 | 40.86 | 44.71
    RT-MDNet [59] | 19.66 | 50.00 | 20.88 | 21.38 | 12.42 | 65.38 | 37.37 |  | 16.21 | 37.55 | 7.98 | 41.05 | 42.59
    SPM-AlexNet [75] | 28.82 | 54.65 | 22.99 | 21.89 | 10.96 | 72.10 | 35.75 |  | 16.00 | 38.19 | 10.86 | 41.33 | 54.09
    ECO-HC [55] | 20.48 | 50.46 | 20.72 | 24.69 | 6.74 | 77.18 | 41.74 |  | 14.76 | 41.91 | 10.21 | 42.39 | 48.91
    Ocean-Offline [89] | 25.11 | 53.63 | 23.74 | 21.07 | 12.22 | 71.65 | 40.67 |  | 9.26 | 38.58 | 10.74 | 42.51 | 47.45
    MDNet [60] | 28.90 | 73.29 | 24.19 | 20.60 | 12.95 | 65.92 | 42.13 |  | 15.44 | 39.79 | 12.14 | 42.95 | 43.94
    SiamRPN++ [11] | 22.96 | 48.88 | 20.44 | 21.27 | 9.63 | 75.16 | 40.24 |  | 16.46 | 41.21 | 10.76 | 43.01 | 51.69
    SiamRPN [10] | 25.35 | 46.57 | 24.50 | 21.90 | 14.92 | 74.95 | 39.37 |  | 11.54 | 39.32 | 11.18 | 43.39 | 47.96
    SPM-Res18 [75] | 27.02 | 55.47 | 23.73 | 26.13 | 10.85 | 76.39 | 40.14 |  | 14.16 | 40.77 | 12.92 | 44.06 | 50.42
    SiamFCOS [22] | 28.74 | 53.54 | 23.39 | 26.24 | 10.81 | 73.10 | 42.28 |  | 17.89 | 42.16 | 12.40 | 44.37 | 48.54
    ECO [55] | 24.38 | 45.92 | 23.90 | 23.36 | 11.38 | 75.76 | 48.21 |  | 14.72 | 44.76 | 7.97 | 46.51 | 47.31
    SiamCAR [93] | 28.90 | 48.06 | 29.03 | 27.63 | 17.82 | 78.88 | 45.27 |  | 13.01 | 43.52 | 12.52 | 47.82 | 54.79
    KYS [94] | 40.80 | 55.25 | 35.23 | 35.70 | 33.30 | 73.71 | 46.77 |  | 17.58 | 44.42 | 24.61 | 49.32 | 55.85
    ATOM [13] | 40.17 | 53.91 | 36.45 | 34.39 | 36.70 | 73.24 | 54.37 |  | 23.58 | 49.77 | 25.84 | 52.19 | 55.68
    Dimp [95] | 40.87 | 55.29 | 36.57 | 40.03 | 32.42 | 73.53 | 48.82 |  | 29.93 | 48.91 | 25.57 | 52.47 | 58.25
    ATOM-MU [96] | 38.67 | 53.84 | 35.37 | 35.73 | 35.44 | 74.30 | 52.16 |  | 26.81 | 49.84 | 24.85 | 52.61 | 54.02
    SiamRPN++LT [11] | 45.50 | 71.71 | 47.09 | 43.61 | 44.70 | 75.88 | 52.75 |  | 18.66 | 48.15 | 32.35 | 54.34 | 61.17
    SPLT [97] | 49.92 | 51.73 | 51.75 | 41.69 | 54.76 | 72.46 | 50.82 |  | 26.39 | 48.65 | 37.89 | 54.63 | 53.10
    PrDimp [98] | 57.43 | 79.52 | 49.40 | 50.05 | 49.09 | 74.29 | 53.68 |  | 31.43 | 51.90 | 37.42 | 56.50 | 57.02
    LTDSE [22] | 56.25 | 75.55 | 53.65 | 49.89 | 56.72 | 71.19 | 52.04 |  | 37.79 | 52.22 | 48.70 | 56.51 | 64.29
    Super-Dimp 1 | 53.37 | 78.79 | 46.59 | 47.45 | 46.77 | 75.39 | 56.50 |  | 31.99 | 53.69 | 35.58 | 57.72 | 59.49
    GlobalTrack [76] | 68.98 | 79.47 | 63.42 | 57.34 | 67.78 | 74.38 | 60.24 |  | 43.02 | 58.46 | 58.48 | 63.86 | 66.24
    SiamRCNN [99] | 68.17 | 78.49 | 67.66 | 57.23 | 73.92 | 78.78 | 61.89 |  | 42.48 | 60.10 | 64.04 | 65.41 | 70.83
    higher performance. In most cases, UAV tracking under visible |  |  |  |  |  |  |  | 
    video sequence has a better solution. |  |  |  |  |  |  |  |  |  |  | 
    Attribute-based Performance. To analyze different chal- |  |  |  |  |  |  |  | 
    lenges faced by existing trackers, all trackers are evaluated on |  |  |  |  |  |  |  | 
    seven attributes. The results of several challenging attributes |  |  |  |  |  |  |  | 
    are shown in Tab. III and Tab. IV. |  |  |  |  |  |  |  |  |  |  |
