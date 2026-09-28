---
id: arxiv-2108.11539-tph-yolov5-improved-yolov5-transformer
title: "TPH-YOLOv5: Improved YOLOv5 Based on Transformer Prediction Head for Object Detection on Drone-captured Scenarios"
year: 2021
backend: grobid
---

## Abstract

Object detection on drone-captured scenarios is a recent popular task. As drones always navigate in different altitudes, the object scale varies violently, which burdens the optimization of networks. Moreover, high-speed and low-altitude flight bring in the motion blur on the densely packed objects, which leads to great challenge of object distinction. To solve the two issues mentioned above, we propose TPH-YOLOv5. Based on YOLOv5, we add one more prediction head to detect different-scale objects. Then we replace the original prediction heads with Transformer Prediction Heads (TPH) to explore the prediction potential with self-attention mechanism. We also integrate convolutional block attention model (CBAM) to find attention region on scenarios with dense objects. To achieve more improvement of our proposed TPH-YOLOv5, we provide bags of useful strategies such as data augmentation, multiscale testing, multi-model integration and utilizing extra classifier. Extensive experiments on dataset VisDrone2021 show that TPH-YOLOv5 have good performance with impressive interpretability on drone-captured scenarios. On DET-test-challenge dataset, the AP result of TPH-YOLOv5 are 39.18%, which is better than previous SOTA method (DPNetV3) by 1.81%. On VisDrone Challenge 2021, TPH-YOLOv5 wins 5 th place and achieves well-matched results with 1 st place model (AP 39.43%). Compared to baseline model (YOLOv5), TPH-YOLOv5 improves about 7%, which is encouraging and competitive.

## 1. Introduction

Object detection technology on drone-captured scenarios has been widely used in many practical applications, such as plant protection [18,41], wildlife protection [23,22] and urban surveillance [1,15]. In this paper, we focus on improv- ing the performance of object detection on drone-captured images and providing insight for the above-mentioned numerous applications.

Recent years have witnessed significant progresses in object detection tasks using deep convolutional neural networks [40,37,34,27,58]. Some notable benchmark datasets like MS COCO [30] and PASCALVOC [9] greatly Figure 2. The overview of working pipeline using TPH-YOLOv5. Compared to original version, we mainly improve the head by applying Transformer Prediction Head (TPH). We also add one more head to better detect different scale objects. In addition, we employ bag of tricks like data augmentation, multi-scale testing, model ensemble and self-trained classifier to make TPH-YOLOv5 stronger.

promote the development of object detection application. However, most previous deep convolutional neural networks are designed for natural scene images. Directly applying previous models to tackle object detection task on drone-captured scenarios mainly has three problems, which are intuitively illustrated by some cases in Fig. 1. First, the object scale varies violently because the flight altitude of drones change greatly. Second, drone-captured images contain objects with high density, which brings in occlusion between objects. Third, drone-captured images always contain confusing geographic elements because of covering large area. The above-mentioned three problems make the object detection of drone-captured images very challenging.

In object detection task, YOLO series [37,38,39,2] play an important role in one-stage detectors. In this paper, we propose an improved model, TPH-YOLOv5 based on YOLOv5 [21] to solve the above-mentioned three problems. The overview of the detection pipeline using TPH-YOLOv5 is shown in Fig. 2. We respectively use CSPDark-net53 [52,2] and path aggregation network (PANet [33]) as backbone and neck of TPH-YOLOv5, which follows the original version. In the head part, we first introduce one more head for tiny object detection. Totally, TPH-YOLOv5 contains four detection heads separately used for the detection of tiny, small, medium, large objects. Then, we replace the original prediction heads with Transformer Prediction Heads (TPH) [7,49] to explore the prediction potential. To find the attention region in images with large coverage, we adopt Convolutional Block Attention Module (CBAM [54]) to sequentially generate the attention map along channelwise and spatial-wise dimensions. Compared to YOLOv5, our improved TPH-YOLOv5 can better deal with dronecaptured images.

To further improve the performance of TPH-YOLOv5, we employ bag of tricks (Fig. 2). Specifically, we adopt data augmentation during training, which promote the adaptation for dramatic size changes of objects in images. We also add multi-scale testing (ms-testing) and multi-model ensemble strategies during inference to obtain more convincing detection results. Moreover, through visualizing the failure cases, we find that our proposed architecture has excellent localization ability but poor classification ability, especially on some similar categories like "tricycle" and "awning-tricycle". To solve this problem, we provide a selftrained classifier (ResNet18 [17]) using the image patches cropping from training data as classification training set. With self-trained classifier, our method has 0.8%∼1.0% improvement on AP value.

Our contributions are listed as follows:

• We add one more prediction head to deal with large scale variance of objects.

• We integrate the Transformer Prediction Heads (TPH) into YOLOv5, which can accurately localize objects in high-density scenes.

• We integrate CBAM into YOLOv5, which can help the network to find region of interest in images that have large region coverage.

• We provide useful bag of tricks and filtering some useless tricks for object detection task on drone-captured scenarios.

• We use self-trained classifier to improve the classification ability on some confusing categories.

• On VisDrone2021 test-challenge dataset, our proposed TPH-YOLOv5 achieve 39.18% (AP), outperforming DPNetV3 (previous SOTA method) by 1.81%. In Vis-Drone2021 DET challenge, TPH-YOLOv5 wins 5 th place and has minor gap comparing with 1 st place models.

## 2. Related Work

### 2.1. Data Augmentation

The effectiveness of data augmentation is to expand the dataset, so that the model has higher robustness to the images obtained from different environments. Photometric distortions and geometric distortions are wildly used by researchers. As for photometric distortion, we adjusted the hue, saturation and value of the images. In dealing with geometric distortion, we add random scaling, cropping, translation, shearing, and rotating. In addition to the abovementioned global pixel augmentation methods, there are some more unique data augmentation methods. Some researchers have proposed methods using multiple images together for data augmentation i.e. MixUp [57], CutMix [56] and Mosaic [2]. MixUp randomly select two samples from the training images to perform random weighted summation, and the labels of the samples also correspond to the weighted summation. Unlike occlusion works that generally use zero-pixel "black cloth" to occlude a image, Cut-Mix uses an area of another image to cover the occluded area. Mosaic is an improved version of the CutMix. Mosaic stitches four images, which greatly enriches the background of the detected object. In addition, batch normalization calculates the activation statistics of 4 different images on each layer.

In TPH-YOLOv5, we use a combination of MixUp, Mosaic and traditional methods in data augmentation.

### 2.2. Multi-Model Ensemble Method in Object Detection

Deep learning neural networks are non-linear methods. They provide greater flexibility and can scale in proportion to the amount of training data. One disadvantage of this flexibility is that they learn through random training algorithms, which means that they are sensitive to the details of the training data, and may find a different set of weights each time they train, resulting in different predictions. This gives the neural network a high variance. A successful way to reduce the variance of neural network models is to train multiple models instead of a single model, and combine the predictions of these models.

There are three different methods to ensemble boxes from different object detection models: Non-maximum suppression (NMS) [36], Soft-NMS [53], weighted boxes fusion (WBF) [43]. In the NMS method, if the overlap, intersection over union (IoU) of the boxes is higher than a certain threshold, they are considered to belong to the same object. For each object, NMS only leaves one bounding box with the highest confidence, and other bounding boxes are deleted. Therefore, the box filtering process depends on the choice of this single IoU threshold, which have a big impact on model performance. Soft-NMS has made a slightly change to NMS, which made Soft-NMS shows a significant improvement over traditional NMS on standard benchmark datasets (such as PASCAL VOC [10] and MS COCO [30]). It sets an attenuation function for the confidence of adjacent bounding boxes based on the IoU value instead of completely setting their confidence scores to zero and delete them. WBF works differently from NMS. Both NMS and Soft-NMS exclude some boxes, while WBF merges all boxes to form the final result. Therefore, it can solve all the inaccurate predictions of the model. We use WBF to ensemble final models, which performs much better than NMS.

### 2.3. Object Detection

CNN-based object detectors can be divided into many types: 1) one-stage detectors: YOLOX [11], FCOS [48], DETR [65], Scaled-YOLOv4 [51], Effi-cientDet [45]. 2) two-stage detectors: VFNet [59], CenterNet2 [62]. 3) anchor-based detectors: Scaled-YOLOv4 [51], YOLOv5 [21]. 4) anchor-free detectors: CenterNet [63], YOLOX [11], RepPoints [55]. Some detectors are specially designed for Drone-captured images like RRNet [4], PENet [46], CenterNet [63] etc. But from the perspective of components, they generally consist of two parts, an CNN-based backbone, used for image feature extraction, and the other part is detection head used to predict the class and bounding box for object. In addition, the object detectors developed in recent years often insert some layers between the backbone and the head, people usually call this part the neck of the detector. Next, we will separately introduce these three structures in detail.

### Backbone.

The backbone that are often used include VGG [42], ResNet [17], DenseNet [20], Mo-bileNet [19], EfficientNet [44], CSPDarknet53 [52], Swin Transformer [35] etc., rather than networks designed by ourselves. Because these networks have proven that they have strong feature extraction capabilities on classification and other issues. But researchers will also fine-tune the backbone to make it more suitable for specific tasks. Neck. The neck is designed to make better use of the features extracted by the backbone. It reprocesses and rationally uses the feature maps extracted by Backbone at different stages. Usually, a neck consists of several bottom-up paths and several top-down paths. Neck is a key link in the target detection framework. The earliest neck is the use of up and down sampling block. The feature of this method is that there is no feature layer aggregation operation, such as SSD [34], directly follow the head after the multi-level feature map. Commonly used path-aggregation blocks in neck are: FPN [28], PANet [33], NAS-FPN [12], BiFPN [45], ASFF [32], SFAM [61].The commonality of these methods is to repeatedly use various up-and-down sampling, splicing, dot sum or dot product to design aggregation strate- gies. There are also some additional blocks used in neck, like SPP [16], ASPP [5], RFB [31], CBAM [54]. Head. As a classification network, the backbone cannot complete the positioning task, and the head is designed to be responsible for detecting the location and category of the object by the features maps extracted from the backbone. Heads are generally divided into two kinds: one-stage object detector and two-stage object detector. Two-stage detectors have long been the dominant method in the field of object detection, and the most representative one is the R-CNN series [14,13,40]. Compared with the two-stage detector, the one-stage detector predicts the bounding box and the class of objects at the same time. The speed advantage of the one-stage detector is obvious, but the accuracy is lower. For one-stage detectors, the most representative models are YOLO series [37,38,39,2], SSD [34] and Reti-naNet [29].

## 3. TPH-YOLOv5

### 3.1. Overview of YOLOv5

YOLOv5 has four different models including YOLOv5s, YOLOv5m, YOLOv5l and YOLOv5x. Generally, YOLOv5 respectively uses the architecture of CSPDarknet53 with an SPP layer as backbone, PANet as Neck and YOLO detection head [37]. To further optimize the whole architecture, bag of freebies and specials [2] are provided. Since it is the most notable and convenient one-stage detector, we select it as our baseline.

When we train the model using VisDrone2021 dataset [64] with data augmentation strategy (Mosaic and MixUp), we find that the results of YOLOv5x are much better than YOLOv5s, YOLOv5m and YOLOv5l, and the gap of AP value is more than 1.5%. Even though the training computation cost of the YOLOv5x model is more than that of other three models, we still choose to use YOLOv5x to pursue the best detection performance. In addition, according to the features of drone-captured images, we adjust the parameters of commonly used photometric distortions and geometric distortions.

### 3.2. TPH-YOLOv5

The framework of TPH-YOLOv5 is illustrated in Fig. 3. We modify the original YOLOv5 to make it specialize in the VisDrone2021 dataset. Prediction head for tiny objects. We investigate the Vis-Drone2021 dataset and find that it contains many extremely small instances, so we add one more prediction head for tiny objects detection. Combined with the other three prediction heads, our four-head structure can ease the negative influence caused by violent object scale variance. As shown in Fig. 3, the prediction head (head No.1) we add is generated from low-level, high-resolution feature map, which is more sensitive to tiny objects. After adding an additional detection head, although the computation and memory cost increase, the performance of tiny objects detection gets large improvement.

Figure 4. The architecture of transformer encoder, which contains two main blocks, a multi-head attention block and a feed-forward neural network (MLP). LayerNorm and Dropout layers help the network converge better and prevent the network from over fitting. Multi-head attention can help the current node not only pay attention to the current pixels, but also obtain the semantics of the context.

Transformer encoder block. Inspired by the vision transformer [6], we replace some convolutional blocks and CSP bottleneck blocks in original version of YOLOv5 with transformer encoder blocks. The structure is shown in Fig. 4. Compared to original bottleneck block in CSPDark-net53, we believe that transformer encoder block can capture global information and abundant contextual information. Each transformer encoder contains two sub-layers. The first sub-layer is a multi-head attention layer and the second one (MLP) is a fully-connected layer. Residual connections are used between each sub-layer. Transformer encoder blocks increase the ability to capture different local information. It can also explore the feature representation potential with self-attention mechanism [50]. On the Vis-Drone2021 dataset, transformer encoder blocks have better performance on occluded objects with high-density.

Based on YOLOv5, we only apply transformer encoder blocks in the head part to form Transformer Prediction Head (TPH) and the end of backbone. Because the feature maps at the end of the network have low resolution. Applying TPH on low-resolution feature maps can decrease the expensive computation and memory cost. Moreover, when we enlarge the resolution of input images, we optional remove some TPH blocks at early layers to make the training process available.

### Convolutional block attention module (CBAM).

CBAM [54] is a simple but effective attention module. It is a lightweight module that can be integrated into most notable CNN architectures, and it can be trained in an end-to-end manner. Given a feature map, CBAM sequentially infers the attention map along two separate dimensions of channel and spatial, and then multiplies the attention map with the input feature map to perform adaptive feature refinement. The structure of the CBAM module is shown in the Fig. 5. According to the experiment in the paper [54], after integrating CBAM into different models on different classification and detection datasets, the performance of the model get large improved, which proves the effectiveness of this module.

On drone-captured images, large covering region always contains confusing geographical elements. Using CBAM can extract the attention area to help TPH-YOLOv5 resist the confusing information and focus on useful target objects.

Ms-testing and model ensemble. We train five different models in terms of different perspectives for model ensemble. During inference phase, we first perform ms-testing strategy on single model. The implementation details of ms-testing are the following three steps. 1) Scaling the testing image to 1.3 times. 2) Respectively reducing the image to 1 time, 0.83 times, and 0.67 times. 3) Flipping the images horizontally. Finally, we feed the six different-scaling images to TPH-YOLOv5 and use NMS to fuse the testing predictions.

On different models, we perform the same ms-testing operation and fuse the final five predictions by WBF to get the final result. Self-trained classifier. After training the VisDrone2021 dataset with TPH-YOLOv5, we test the test-dev dataset and then analyze the results by visualizing the failure cases and draw a conclusion that TPH-YOLOv5 has excellent localization ability but poor classification ability. We further explore the confusion matrix which is shown in Fig. 6, and observe that the precision of the some hard categories such as tricycle and awning-tricycle are very low. Therefore, we propose an extra self-trained classifier. First, we construct a training set by cropping the ground-truth bounding boxes and resizing each image patches to 64×64. Then we select ResNet18 [17] as classifier network. As shown in experimental results, our method get around 0.8%˜1.0% improvement on AP value with the help of this self-trained classifier.

## 4. Experiments

We use the testset-challenge and testset-dev of the Vis-Drone2021 dataset to evaluate our model, and we report mAP (average of all 10 IoU thresholds, ranging from [0.5: 0.95]) and AP50. VisDrone2021-DET dataset is the same as VisDrone2019-DET dataset and VisDrone2018-DET dataset.

### 4.1. Implementation Details

We implement TPH-YOLOv5 on Pytorch 1.8.1. All of our models use an NVIDIA RTX3090 GPU for training and testing. In the training phase, we use part of pre-trained model from yolov5x, because TPH-YOLOv5 and YOLOv5 share most part of backbone (block 0˜8) and some part of head (block 10˜13 and block 15˜18), there are many weights can be transferred from YOLOv5x to TPH-YOLOv5, by using these weights we can save a lot of training time.

Because the VisDrone2021 training set is a bit small, we only train the model on VisDrone2021 trainset for 65 epochs, and the first 2 epochs are used for warm-up. We use adam optimizer for training, and use 3e-4 as the initial learning rate with the cosine lr schedule. The learning rate of the last epoch decays to 0.12 of the initial learning rate. The size of the input image of our model is very large, the long side of the image is 1536 pixels, which leads to the batch size is only 2. Data analysis. According to our previous engineering experience, it is very important to walk through dataset before training the model, which can often be of great help to the improvement of mAP. We have analyzed bounding boxes in the VisDrone2021 dataset. When the input image size is set to 1536, there are 622 of 342391 labels are less than 3 pixels in size. As shown in Fig. 7, these small objects are hard to recognize. When we use gray squares to cover these small objects and train our model on the processed dataset, the mAP improves by 0.2, better than not.

Ms-testing. When training neural network models for computer vision problems, data augmentation is a technique often used to improve performance and reduce generalization errors. When using a model to make predictions, image data augmentation of test dataset can also be applied to allow the model to make predictions on multiple different versions of images. The prediction of the augmented images can be averaged to get better prediction performance.

We scale the test images to three different sizes in mstesting, and then flip them horizontally, so that a total of 6 different images are obtained. After testing six different images and fusing the results, we get the final test result.

### 4.2. Comparisons with the State-of-the-art

On VisDrone2021-DET testset-challenge.

Due to the limited number of submissions in the Vis-Drone2021 competition server, we only obtained the results of 4 models on testset-challenge and the final results of the ensemble of 5 models. We finally got a good score of 39.18 on testset-challenge, which is much higher than VisDrone2020's best score of 37.37. Ranked fifth in the VisDrone 2021 leader board, our score is 0.25 lower than the 39.43 of the first place. If the number of submissions is not used up, we will definitely get better results. Table 1 lists the score of our model, compared with the scores in the previous year's VisDrone competition and the scores of algorithms submitted by the committee. Methods mAP (%) AP50 (%) RetinaNet [29] 11.81 21.37 RefineDet [60] 14.90 28.76 DetNet59 [26] 15.26 29.23 Cascade-RCNN [3] 16.09 31.91 FPN [28] 16.51 32.20 Light-RCNN [25] 16.53 32.78 CornetNet [24] 17.41 34.12 RRNet (2019 2 nd ) [4] 29.13 55.82 DPNet-ensemble (2019 SOTA) [8] 29.62 54.00 SMPNet (2020 2 nd ) [47] 35.98 59.53 DPNetV3 (2020 SOTA) [47] 37.37 Effect of extra prediction head. Adding a detection head for tiny objects makes the number of layers of the original YOLOv5x change from 607 to 719, and GFLOPs from 219.0 to 259.0. This of course increases the amount of calculation, but the mAP improvement is also very high. From Fig. 9 we can see that TPH-YOLOv5 performs well when detecting small objects, so the increasing in calculation is worthwhile. Effect of transformer encoder blocks. After using the transformer encoder block, the total layers of the model decrease from 719 to 705, and GFLOPs from 259.0 to 237. Some detection result on VisDrone2021 testsetchallenge. We have selected some representative images as the display of the test results. Fig. 9 shows the result of large objects, tiny objects, dense objects and the image covering a large area.

## 5. Conclusion

In this paper, we add some cutting-edge techniques i.e. transformer encoder block, CBAM and some experienced tricks to YOLOv5 and form a state-of-the-art detector called TPH-YOLOv5, which is especially good at object detection in drone-captured scenarios. We refresh the record of VisDrone2021 dataset, our experiments showed that TPH-YOLOv5 achieved state-of-the-art performance in VisDrone2021 dataset. We have tried a large number of features, and used some of them to improve the accuracy of object detector. We hope this report can help developers and researchers get a better experience in the analysis and processing of drone-captured scenarios.

## 6. Acknowledgments

This work was supported by National Natural Science Foundation of China (62072021).

## Figures et tableaux

**Figure 1.** Intuitive cases to explain the three main problems in object detection on drone-captured images. The cases in first row, second row and third row respectively shows the size variation, high-density and large coverage of objects on drone-captured images.

**Figure 3.** The architecture of the TPH-YOLOv5. a) CSPDarknet53 backbone with three transformer encoder blocks at the end. b) The Neck use the structure like PANet. c) Four TPHs (transformer prediction heads) use the feature maps from transformer encoder blocks in Neck. In addition, the number of each block is marked with orange numbers on the left side of the block.

**Figure 5.** The overview of CBAM module. Two sequential submodules are used to refine feature map that go through CBAM, residual paths are also used.

**Figure 6.** Confusion matrix was made at IoU threshold of 0.45, confidence threshold of 0.25.

**Figure 7.** Some images were taken too high, resulting in many small objects, which cannot be recognized.

3. Use transformer encoder blocks can not only increase mAP, but also reduce the size of the network. At the same time, it also plays a role in the detection of dense objects and large objects. Effect of model ensemble. We list the mAP of the final results of our five different models in each category and compared them with the fusion model in table 3. In training phrase, we use different input image sizes and change the weight of each category to make each model unique. So that the final ensemble model can get a relatively balanced result. 1) TPH-YOLOv5-1 use the input image size of 1920 and all categories have equal weights. 2) TPH-YOLOv5-2 use the input image size of 1536 and all categories have equal weights. 3) TPH-YOLOv5-3 use the input image size of 1920 and the weight of each category is related to the number of labels, which is shown in Fig. 8. The more labels of a certain category, the lower the weight it is given. 4) TPH-YOLOv5-4 use the input image size of 1536 and the weight of each category is related to the number of labels. 5) TPH-YOLOv5-5 use the backbone of YOLOv5l and use the input image size of 1536.

**Figure 8.** The number of labels of each category.

**Figure 9.** Some visualization results from our TPH-YOLOv5 on testset-challenge, different category use bounding boxes with different color. The performance is good at localization tiny objects, dense objects and objects blurred by motion.

**Table 1.** The comparison of the performance in VisDrone2021 testset-challenge4.3. Ablation StudiesOn VisDrone2021-DET testset-dev. we analyze importance of each proposed component on local testset-dev as we cannot test these on VisDrone2021 competition server, the number of submissions to the competition server is very valuable. The impact of each component is listed in the table 2. [corps du tableau reconstruit par Docling : à vérifier]

    Methods | mAP(%) | AP50(%)
    RetinaNet[29] | 11.81 | 21.37
    RefineDet[60] | 14.90 | 28.76
    DetNet59[26] | 15.26 | 29.23
    Cascade-RCNN[3] | 16.09 | 31.91
    FPN[28] | 16.51 | 32.20
    Light-RCNN[25] | 16.53 | 32.78
    CornetNet[24] | 17.41 | 34.12
    RRNet (2019 2nd )[4] | 29.13 | 55.82
    DPNet-ensemble(2019SOTA)[8] | 29.62 | 54.00
    SMPNet (2020 2nd )[47] | 35.98 | 59.53
    DPNetV3 (2020 SOTA)[47] | 37.37 | 62.05
    TPH-YOLOv5 ensemble | 39.18 | \

**Table 2.** Ablation Study on VisDrone2021 testset-dev. [corps du tableau reconstruit par Docling : à vérifier]

    Methods | mAP (%) | AP50 (%)
    YOLOv5 | 28.88 | 49.33
    YOLOv5+P2 | 31.03(↑2.15) | 51.61(↑2.28)
    YOLOv5+P2+transformer | 32.84(↑1.81) | 53.87(↑2.26)
    TPH-YOLOv5 (previous+CBAM) | 33.63(↑0.79) | 54.77(↑0.90)
    TPH-YOLOv5+ms-testing | 34.90(↑1.27) | 56.40(↑1.63)
    TPH-YOLOv5+ms-testing+Classifier | 35.74(↑0.84) | 57.31(↑0.91)

**Table 3.** Comparison of TPH-YOLOv5 models' performances on VisDrone2021 testset-dev for each category.

    Methods | all | pedestrian people bicycle | car | van | trunk tricycle awning-tricycle | bus | motor
    TPH-YOLOv5-1 | 34.90 | 27.52 | 15.32 | 15.21 | 65.99 44.23 47.56 | 23.96 | 22.11 | 58.85 28.44
    TPH-YOLOv5-2 | 34.29 | 27.97 | 14.88 | 14.17 | 67.63 45.01 44.76 | 25.12 | 20.48 | 55.72 27.74
    TPH-YOLOv5-3 | 34.68 | 22.88 | 16.01 | 19.26 | 48.88 42.98 47.82 | 32.86 | 35.65 | 54.16 28.25
    TPH-YOLOv5-4 | 34.17 | 23.48 | 15.79 | 17.62 | 49.99 42.76 47.13 | 31.66 | 32.21 | 54.19 27.37
    TPH-YOLOv5-5 | 33.04 | 25.98 | 14.90 | 13.10 | 63.05 43.45 42.56 | 25.20 | 21.06 | 53.65 27.10
    TPH-YOLOv5 ensemble 37.32 | 29.00 | 16.75 | 15.69 | 68.94 49.79 45.16 | 27.33 | 24.72 | 61.80 30.90
