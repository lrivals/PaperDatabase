---
id: 2025-kwong-tomato-leaf-detection-segmentation-extraction
title: "Tomato Leaf Detection, Segmentation, and Extraction in Real-Time Environment for Accurate Disease Detection"
year: 2025
backend: grobid
---

## Abstract

Agricultural production is a critical sector that directly impacts the economy and social life of any society. The identification of plant disease in a real-time environment is a significant challenge for agriculture production. For accurate plant disease detection, precise detection of plant leaves is a meaningful and challenging task for developing smart agricultural systems. Most researchers train and test models on synthetic images. So, when using that model in a real-time scenario, it does not give a satisfactory result because when a model trained on images of leaves is fed with the image of the plant, then its accuracy is affected. In this research work, we have integrated two models, the Segment Anything Model (SAM) with YOLOv8, to detect the tomato leaf of a tomato plant, mask the leaf, and extract the leaf in a real-time environment. To improve the performance of leaf disease detection in plant leaves in a real-time environment, we need to detect leaves accurately. We developed a system that will detect the leaf, mask the leaf, extract the leaf, and then detect the disease in that specific leaf. For leaf detection, the modified YOLOv8 is used, and for masking and extraction of the leaf images from the tomato plant, the Segment Anything Model (SAM) is used. Then, for that specific leaf, an image is provided to the deep neural network to detect the disease.

## 1. Introduction

In recent years, the integration of computer vision and machine learning techniques in agriculture has revolutionized crop management and disease detection [1]. Amongst the various applications, particularly in tomato plants, the exact segmentation and analysis of plant leaves have gained significant attention because of their importance in early disease detection, nutrient deficiency identification, and overall plant health monitoring [2]. Plant leaf segmentation is an important aspect of computer vision and agricultural technology. It supports various applications, including disease monitoring, growth monitoring, and yield prediction. However, there has been a great improvement in the deep learning domain, due to which the methods and results of leaf segmentation processes have become more efficient and effective [3].

Tomato (Solanum lycopersicum) happens to be one of the most widely cultivated as well as economically important vegetable crops across the globe. However, tomato plants are affected by different diseases and environmental conditions that lower the yield and quality of the crop. Therefore, timely notice and correct assessment of plant health conditions are essential to enable quick response actions for minimization of the loss of the crops [4]. Most

•

Improved backbone and neck architecture for better feature extraction.

•

Improved loss functions and data augmentation methods.

•

Native support, for instance, segmentation tasks.

•

Improved performance on small object detection.

Likewise, the authors in [10] have also proposed the Segment Anything Model (SAM), which has allowed for significant advancement in image segmentation as it has the ability to segment any object in an image based on various types of prompts, including points, boxes, and even text. SAM is envisioned as a promptable segmentation system that can create a mask for every target that can be found on an image, all based on the type of text prompt it receives. The main features of SAM include:

• SAM can segment objects accurately without prior training.

•

SAM has input prompts flexibility such as accepting points, masks, text, or boxes as prompts.

•

SAM is trained on 11 million images and 1.1 billion masks.

•

For interactive applications, SAM can accurately generate masks in real time.

It is worth noting that SAM was not specifically developed for agricultural uses; however, its potential functionality can be proved useful in other tasks, such as leaf segmentation. The authors in [11] showed how SAM can be utilized in crop monitoring by examining the crop features in detail and making attempts to obtain such features for the leaves of the plants. Advanced models for tomato leaf segmentation have immense research potential due to reconciling the intricacies of agriculture image analysis with the advancements in computer vision technologies. Leaf segmentation is very important for the later steps of the analysis, such as in the case of disease detection, growth monitoring, and yield prediction [12]. Individual leaf extraction from complex backgrounds which include other parts of the plant, soil, and agricultural equipment, is considered a complex task. These models have the potential to provide a robust foundation for more specialized agricultural AI applications.

The identification of plant disease in a real-time environment is a major challenge for agriculture production [13]. For the accurate detection of plant disease, accurate detection of plant leaves is very important for the development of smart agriculture systems. A majority of the researchers train and test the models on synthetic images. Therefore, when using that model in a real-time scenario, it does not give a satisfactory result because the model trained with leaf images does not perform well with plant images, and its precision suffers.

For this purpose, we have used YOLOv8 and SAM, two recent deep-learning models. In this work, we have focused on tomato leaf detection, segmentation, and extraction.

The objectives of this study are to understand the capabilities of both YOLOv8 and SAM regarding tomato leaf detection and segmentation. We measure their performance around accuracy, efficiency, and how well they cope with changes in their surroundings. Apart from this, we have investigated the potential of these models in this study to handle the inherent challenges in agricultural imaging, such as varying lighting conditions, natural variability in leaf shapes and sizes, and occlusions. The results of this work are very useful for creating automated tomato plant monitoring systems in the agricultural sector. We aim to expand the boundaries of precision agriculture by utilizing the best features of YOLOv8 and SAM, which will allow farmers and researchers to make data-based crop management and disease control decisions.

The proposed work comprises six sections. We outline the structure of this paper as follows: In Section 2, the literature review has been discussed in detail; Section 3 presents the materials and methods; in this section, the methodology of the proposed work has been discussed in detail; Section 4 consists of the results which demonstrate the simulation results using YOLOv8 and SAM; Section 5 consists of a discussion on the strengths and limitations of the proposed model along with the comparison of our work with the previous studies; Section 6 presents the conclusion.

## 2. Related Works

Tomato leaf detection and segmentation are very important for accurate tomato leaf disease detection. The integration of cutting-edge technologies such as YOLOv8 and SAM has played an important role in the improvement of these tasks. Current research suggest some effective methods for plant leaf segmentation. This study begins with a review of studies on the usage of YOLOv8 and SAM for different purposes to better comprehend the existing literature on their identification. This section focuses on the contribution of this study using other studies in this field.

In this study, the authors proposed a modified YOLOv8s-Seg network for the segmentation of tomato fruits and leaves in real-time, tackling problems emanating from weather conditions and surface characteristics. The proposed model has a mean average precision (mAP) of 92.2%, which outperforms previous models and offers technical support for tomato health monitoring and intelligent harvesting [14].

The authors integrated a new channel attention model into the advanced YOLOv8 model that makes it possible to add the Efficient Channel Attention mechanisms to improve the feature extraction of the model designed for tomato leaf disease detection. The experiments showed that the modified model outperformed the baseline by approximately 1.8% increase in mAP50, while the parameter size was reduced by 74%, which means a more accurate and less computational cost detection system [15].

This work aims to analyze and evaluate different segmentation models in detecting single and multiple diseases in tomato leaves. The accuracy of model B, which is Hybrid-DSCNN, a model combining U-Net and SegNet, was 98.24%, and it proved to be the fastest model, completing 1004 images in 30 nanoseconds [16].

The primary objective of this work is to come up with a deep neural network to detect tomato leaf diseases based on the YOLOv8 architecture. It uses multi-head self-attention to improve feature learning, which in turn improves detection accuracy and makes the model more robust to environmental changes [17].

The authors in this work used YOLOv8 and RoboFlow to detect tomato leaf disease with nine classes and achieved an average precision of 98.9% mAP. The results provided by the authors in this research have the potential for detecting and classifying tomato leaf disease at early stages [18].

The authors in this work stated the deep learning models for classifying and segmenting tomato leaf diseases, focusing on the importance of accurate segmentation in disease detection. The authors in this work highlight the efficiency of models such as U-Net in segmenting diseased areas, contributing to precision agriculture practices [19].

By incorporating SAM along with post-processed steps of segmentation, the author can achieve a zero-shot segmentation of potato leaves without using any supplementary training data. The approach is not exclusive to tomatoes but provides some insight into the segmentation tasks specific to tomato leaves [20].

In this research, the authors have used different CNN architectures such as VGG, ResNet, and DenseNet for tomato leaf disease detection with 10 classes, including healthy ones. The authors have merged the two datasets. After checking the accuracy of these models, the authors developed their own custom CNN model with 10 layers and compared the accuracy of their model with the other models. Their custom-deployed model has an accuracy of over 99% on both datasets [21].

The authors have conducted research on analyzing tomato leaf for disease detection. The authors have used a hybrid system in which they integrated the machine learning algorithm, Exponential Discriminant Analysis (EDA), with transfer learning techniques such as ResNet50, DenseNet201, EfficientNetB0, and DarkNet53. The authors have used the Taiwan and Plant-Village tomato leaf datasets. The results in this work demonstrate that the authors have achieved the mean accuracies of 98.09% and 98.29% on these datasets, respectively [22].

This research meaningfully improves YOLOv8-Seg models towards real-time instance segmentation of plant diseases using the Tomato Leaf Disease dataset as a test case. The modified models are very effective in the segmentation of the diseased regions, and sequentially, disease control can be carried out promptly [23].

The DS-DETR model presented in [9] integrates improvements to the detection transformer (DETR) to enhance its efficiency in the segmentation of tomato leaves infected with diseases. It also promotes the efficient management of diseases by quickly generating accurate disease damage assessments since it achieves an AP mask of 0.6823, which is above state-of-the-art models [24].

In this work, a YOLOV8s-based model for detecting diseases in wilted tomato leaves is presented, yielding an mAP of 92.5%. The model is expected to perform better than YOLOV5 and Faster R-CNN, showing a capability of real-time disease detection [25].

In response to the limitation of deploying detection algorithms based on deep learning on embedded devices, this paper presents an optimization of the YOLOv8n model. The algorithm has been able to perform reliable and efficient real-time detection of tomato leaf diseases and has a low model size, which can be utilized in embedded systems [26].

This study attempts to detect the tomato leaf miner pest using the YOLOv8-Seg models. The research clearly emphasizes the ability of the model to detect even those tomato leaves of low density for effective pest management measures. Towards this end, the authors go ahead to modify the YOLOv8-seg model to include the Ghost and BiFPN modules which improves the segmentation of leaves. Five test datasets were used to test the model for leaf segmentation with a score of 86.4%, which is high compared with other methods reported in the literature [27].

An approach was taken in this study where a framework based on Mask R-CNN is used for the detection and segmentation of plant leaf disease. The model had a mAP of 76.94%, which indicates its efficiency in segmenting the diseased area of different kinds of plants, including tomatoes [28].

## 3. Materials and Methods

In this section, a detailed methodology for leaf detection, segmentation, and extraction is discussed by integrating YOLOv8 for object detection and SAM for leaf segmentation. The proposed approach influences the strengths of YOLOv8 for efficient tomato leaf detection and SAM for high-quality segmentation within detected bounding boxes. The detailed methodology of the proposed approach is shown in Figure 1.

AgriEngineering 2025, 7, x FOR PEER REVIEW 5 of 16

## 3. Materials and Methods

In this section, a detailed methodology for leaf detection, segmentation, and extraction is discussed by integrating YOLOv8 for object detection and SAM for leaf segmentation. The proposed approach influences the strengths of YOLOv8 for efficient tomato leaf detection and SAM for high-quality segmentation within detected bounding boxes. The detailed methodology of the proposed approach is shown in Figure 1.

### 3.1. Dataset Preparation

The dataset consists of high-resolution images of tomato plants from the tomato village [29]. The images were obtained using contributions from a wide range of publicly available sources to ensure variability in light conditions, the angle of leaves, and the stage of development of the plants. The images were larger, originally comprising 640 × 640 pixels.

To achieve image consistency for model training and testing, all images were remapped to a single resolution of 640 × 640 pixels. The model used was also augmented by performing simple augmentations such as random rotation, horizontal flip, and changing brightness. After collecting the dataset was annotated using the autodistill process. The dataset comprises 11,493 images. These annotated data are divided into training (70%), validation (20%) and testing (10%) sets. This dataset is further provided to YOLOv8.

### 3.2. YOLOv8 for Leaf Detection

For detecting tomato leaves in tomato plant images, we employed the YOLOv8 model. YOLOv8 was preferred because of its ability to detect objects in real time with high accuracy and low computational cost. The boxes were automatically encased around the tomato leaves themselves by using YOLOv8, which was later refined through SAM. YOLOv8 was employed for detection tasks. The network was initialized using the pretrained weights from the COCO dataset and then adjusted to the tomato leaf dataset. Unlabeled data for YOLOv8 were annotated using the autodistill. With the help of autodistill, we can train small, faster-supervised models with big slower foundation models. Using autodistill we can create labeled data to inference on a custom model running on the edge.

### 3.1. Dataset Preparation

The dataset consists of high-resolution images of tomato plants from the tomato village [29]. The images were obtained using contributions from a wide range of publicly available sources to ensure variability in light conditions, the angle of leaves, and the stage of development of the plants. The images were larger, originally comprising 640 × 640 pixels.

To achieve image consistency for model training and testing, all images were remapped to a single resolution of 640 × 640 pixels. The model used was also augmented by performing simple augmentations such as random rotation, horizontal flip, and changing brightness. After collecting the dataset was annotated using the autodistill process. The dataset comprises 11,493 images. These annotated data are divided into training (70%), validation (20%) and testing (10%) sets. This dataset is further provided to YOLOv8.

### 3.2. YOLOv8 for Leaf Detection

For detecting tomato leaves in tomato plant images, we employed the YOLOv8 model. YOLOv8 was preferred because of its ability to detect objects in real time with high accuracy and low computational cost. The boxes were automatically encased around the tomato leaves themselves by using YOLOv8, which was later refined through SAM. YOLOv8 was employed for detection tasks. The network was initialized using the pre-trained weights from the COCO dataset and then adjusted to the tomato leaf dataset. Unlabeled data for YOLOv8 were annotated using the autodistill. With the help of autodistill, we can train small, faster-supervised models with big slower foundation models. Using autodistill we can create labeled data to inference on a custom model running on the edge. For using the autodistill, the unlabeled data is given to the base model, which uses ontology to mark the dataset labeled that is used to train the targeted model, which outputs a distilled model fine-tuned to perform a specific task. The autodistill process is shown in Figure 2.

AgriEngineering 2025, 7, x FOR PEER REVIEW 6 of 16

For using the autodistill, the unlabeled data is given to the base model, which uses ontology to mark the dataset labeled that is used to train the targeted model, which outputs a distilled model fine-tuned to perform a specific task. The autodistill process is shown in Figure 2. The dataset here includes labeled data, which is the output generated by the base model and that can be used to train the target model, which in our case is the YOLOv8 model.

Target Model: The target model is the supervised model that will consume the labeled dataset generated by the base model, and that is ready for implementation. For performing the specific task, the target model is fined-tuned, and that is usually small and fast. In our case, the target model is YOLOv8. Distilled Model: A distilled model is the final output of the autodistill process; it is a set of weights fine-tuned for your task that can be deployed to obtain predictions. It is the final outcome of the autodistill. This is a set of fine-tuned weights for the specific task and can be implemented to obtain predictions.

After obtaining the labeled data, it is divided into training (70%), validation (20%), and testing (10%) sets. These sets provided YOLOv8 for training, which is the target model. The resolution of the images was reduced to 640 × 640 pixels for this purpose before feeding to YOLOv8.

The training parameters are as follows:

-Batch Size: 16 -Epochs: 100 -Learning Rate: 0.001 -Optimizer: The Adam optimizer is used to minimize the loss function. Autodistill comprises the following steps: Task: The Task explains what will be predicted by the target model. For each component, such as the base, ontology, and target model of the autodistill pipeline it must match and be compatible with each other. Base Model: A base model is a large foundation and a multimodal, such as GoundedSAM, that can perform many tasks. We create the dataset from the unlabeled data along with the ontology by using the base model. Ontology: An ontology explains the prompted labels, what your dataset will describe, and what your target model will predict. A simple Ontology is CaptionOntology, which prompts a Base Model with text captions and maps them to class names. Other Ontologies may, for instance, use a CLIP vector or example images instead of a text caption. This research work is focused on detecting the tomato leaf, so CaptionOntology was like "leaf" = "tomato leaf". Dataset: The dataset here includes labeled data, which is the output generated by the base model and that can be used to train the target model, which in our case is the YOLOv8 model. Target Model: The target model is the supervised model that will consume the labeled dataset generated by the base model, and that is ready for implementation. For performing the specific task, the target model is fined-tuned, and that is usually small and fast. In our case, the target model is YOLOv8. Distilled Model: A distilled model is the final output of the autodistill process; it is a set of weights fine-tuned for your task that can be deployed to obtain predictions. It is the final outcome of the autodistill. This is a set of fine-tuned weights for the specific task and can be implemented to obtain predictions.

After obtaining the labeled data, it is divided into training (70%), validation (20%), and testing (10%) sets. These sets provided YOLOv8 for training, which is the target model. The resolution of the images was reduced to 640 × 640 pixels for this purpose before feeding to YOLOv8.

The training parameters are as follows:

-Batch Size: 16 -Epochs: 100 -Learning Rate: 0.001 -Optimizer: The Adam optimizer is used to minimize the loss function.

Output: YOLOv8 has given the output of bounding box coordinates representing each leaf identified together with their respective confidence scores. YOLOv8 has trained well enough to recognize distinctive leaves in the tomato plant images, more so in instances where leaves may be overlapping or occluded. SAM received bounding boxes obtained from YOLOv8 as preliminary data for the generation of final segmentation masks.

### 3.3. Segment Anything Model (SAM) for Leaf Segmentation

Segment Anything Model (SAM) is used to segment the tomato leaves within YOLOv8 bounding boxes. The SAM has also been designed as a prompt-based segmentation model, whereby once a bounding box or points are provided as prompts to it, fine segmentation occurs. Our focus was targeted segmentation, so we implemented SAM ViT-H (Vision Transformer with a hierarchical structure) and trained on large-scale datasets amenable to segmentation tasks. We picked up a pre-trained checkpoint ("sam_vit_h_4b8939.pth"), which was tailored to our task. For speed of inference, the model was executed on 2 GPU 12GB NVIDIA GeForce GTX 1080 Ti. For generating high-quality segmentation masks, SAM is used for each detected bounding box from YOLOv8, as shown in Figure 3.

Output: YOLOv8 has given the output of bounding box coordinates representing each leaf identified together with their respective confidence scores. YOLOv8 has trained well enough to recognize distinctive leaves in the tomato plant images, more so in instances where leaves may be overlapping or occluded. SAM received bounding boxes obtained from YOLOv8 as preliminary data for the generation of final segmentation masks.

### 3.3. Segment Anything Model (SAM) for Leaf Segmentation

Segment Anything Model (SAM) is used to segment the tomato leaves within YOLOv8 bounding boxes. The SAM has also been designed as a prompt-based segmentation model, whereby once a bounding box or points are provided as prompts to it, fine segmentation occurs. Our focus was targeted segmentation, so we implemented SAM ViT-H (Vision Transformer with a hierarchical structure) and trained on large-scale datasets amenable to segmentation tasks. We picked up a pre-trained checkpoint ("sam_vit_h_4b8939.pth"), which was tailored to our task. For speed of inference, the model was executed on 2 GPU 12GB NVIDIA GeForce GTX 1080 Ti. For generating highquality segmentation masks, SAM is used for each detected bounding box from YOLOv8, as shown in Figure 3. The segmentation process consists of the following steps as shown:

•

Input Image and Bounding Box Setup: The SAM was fed with the original RGB image along with the bounding box from YOLOv8.

•

Image Preprocessing: The image was normalized and resized per the input specification of SAM.

•

Segmentation Output: SAM provided binary masks portraying the segmented leaf areas inside the defined bounding boxes. SAM's features along with YOLOv8, have the ability to work around the complex boundaries and the occlusions, each mask was an accurate representation of the leaf's shape.

The segmented leaves, after the segmentation process, were then extracted from the image for further analysis or to be used in subsequent applications such as disease detection. For every segmented leaf, the following post-processing techniques were implemented:

•

Mask Refinement: The binary masks were refined by erosion and dilation such as morphological techniques to smoothen the object boundaries. The segmentation process consists of the following steps as shown:

• Input Image and Bounding Box Setup: The SAM was fed with the original RGB image along with the bounding box from YOLOv8.

•

Image Preprocessing: The image was normalized and resized per the input specification of SAM.

•

Segmentation Output: SAM provided binary masks portraying the segmented leaf areas inside the defined bounding boxes. SAM's features along with YOLOv8, have the ability to work around the complex boundaries and the occlusions, each mask was an accurate representation of the leaf's shape.

The segmented leaves, after the segmentation process, were then extracted from the image for further analysis or to be used in subsequent applications such as disease detection. For every segmented leaf, the following post-processing techniques were implemented:

•

Mask Refinement: The binary masks were refined by erosion and dilation such as morphological techniques to smoothen the object boundaries.

•

Leaf Extraction: The mask was used to cut out each leaf from the image, while the coordinates of the bounding box were used to define the area of the leaf.

•

Resizing: The size of the cutout leaf areas was resized to 640 × 640 pixels using the bilinear interpolation method so that the samples remained consistent.

The extracted leaves were saved and transferred to a designated folder for further analysis. The extracted leaf masks were exported in a PNG format whereas a corresponding mask was recorded for use in the performance evaluation.

The performance of YOLOv8 is assessed through the computation of precision, recall, and F1 confidence score. The performance of SAM is assessed with standard segmentation metrics, which include the Intersection over Union (IoU), Dice coefficient, and qualitative visual assessments. We also report the computational efficiency of how well YOLOv8 and SAM perform together to segment the tomato leaves. For the tomato leaf detection, the performance evaluation metrics are listed below ( 1)-( 4).

recall = TP TP + FN (1) precision = TP TP + FP (2) F1 -score = (2 * TP) (2 * TP + FN + FP) (3) IoU = (TP) (TP + FN + FP) (4) dice coefficient = (2 * TP) (2 * TP + FP + FN)(5)

where:

• FP: False Positives (incorrectly predicted positive cases)

• TP: True Positives (correctly predicted positive cases)

• FN: False Negatives (incorrectly predicted negative cases)

## 4. Results

This section presents the results of the experiments conducted for leaf detection using YOLOv8 and the SAM for segmentation in the images of tomato plants, focusing on the segmentation of the tomato leaves.

The tomato leaves were detected in the tomato plant images using the YOLOv8 model. The bounding boxes that Yolov8 had created were provided as input to the SAM for precise segmentation. The performance of YOLOv8 + SAM for detection and segmentation of the tomato leaves was assessed based on the following parameters:

• Mean Average Precision (mAP):

The model achieved a mAP of 90.7% with a confidence threshold of 0.5. This is shown in Figure 4a, which indicates the high accuracy of detection of tomato leaves on different tomato plant images.

•

Precision, Recall, and F1 Score: To assess the quality of the segmentation masks, precision, recall, and the F1 score were determined for every image at the pixel level. The Precision curve measures the proportion of correctly predicted positive pixels. The Recall curve measures the proportion of actual positive pixels that were correctly predicted. The F1 Score is the harmonic mean of precision and recall. Precision was 100% shown in Figure 4b, while recall was 98%, as shown in Figure 4c, reflecting the model's capability to detect the tomato leaves and minimize false positives correctly. To evaluate the performance of the YOLOv8 + SAM framework, we divided the dataset into a training set (70%), validation set (20%), and test set (10%), as shown in Table 1.

All segmentation results were compared against the ground truth masks using the evaluation metrics mentioned above.

After detecting the tomato leaves using YOLOv8, the SAM model was used to segment the leaves based on the bounding boxes. SAM's ability to provide fine-grained segmentation of leaf boundaries was critical in improving the precision of the leaf regions, particularly for complex shapes and overlapping leaves. IoU measures the overlap between the predicted segmentation mask and the ground truth mask. We reported IoU scores for individual leaves and calculated the average IoU over the entire test set.

The average Dice coefficient was 88%, which is a strong indicator of the overlap between the predicted and ground truth masks. This suggests that SAM accurately segmented the leaf regions, particularly around the edges, where precision is essential for identifying healthy and diseased leaves. The overall pixel accuracy of the segmentation process was 80.78%, showing that the model correctly identified the majority of leaf pixels while minimizing false positives for the background or non-leaf regions.

Alongside the quantitative metrics, the segmentation quality was assessed through visual analysis. Figures 5 and6 shows examples of the original image, YOLOv8-detected bounding boxes, and the final segmented masks from SAM. In these images, the bounding boxes produced by YOLOv8 successfully identified the main leaf structures.

SAM further refined the segmentation, providing precise boundaries, even in the presence of overlapping leaves. The segmented masks clearly delineated the tomato The Dice Coefficient (or F1 score for segmentation) was used to evaluate the similarity between the predicted masks and ground truth. Figure 4d shows the F1 confidence curve of 84% at 0.612.

To evaluate the performance of the YOLOv8 + SAM framework, we divided the dataset into a training set (70%), validation set (20%), and test set (10%), as shown in Table 1. All segmentation results were compared against the ground truth masks using the evaluation metrics mentioned above.

After detecting the tomato leaves using YOLOv8, the SAM model was used to segment the leaves based on the bounding boxes. SAM's ability to provide fine-grained segmentation of leaf boundaries was critical in improving the precision of the leaf regions, particularly for complex shapes and overlapping leaves. IoU measures the overlap between the predicted segmentation mask and the ground truth mask. We reported IoU scores for individual leaves and calculated the average IoU over the entire test set.

The average Dice coefficient was 88%, which is a strong indicator of the overlap between the predicted and ground truth masks. This suggests that SAM accurately segmented the leaf regions, particularly around the edges, where precision is essential for identifying healthy and diseased leaves. The overall pixel accuracy of the segmentation process was 80.78%, showing that the model correctly identified the majority of leaf pixels while minimizing false positives for the background or non-leaf regions.

Alongside the quantitative metrics, the segmentation quality was assessed through visual analysis. Figures 5 and6 shows examples of the original image, YOLOv8-detected bounding boxes, and the final segmented masks from SAM. In these images, the bounding boxes produced by YOLOv8 successfully identified the main leaf structures.

AgriEngineering 2025, 7, x FOR PEER REVIEW 10 of 16 leaves from the background, with SAM accurately capturing the leaf edges. The visual inspection confirms that SAM performs well on complex images, handling variations in lighting, occlusions, and leaf orientation. The masked leaves are then extracted and stored and a separate folder for further analysis, such as disease detection, as shown in Figure 7. By integrating SAM with YOLOv8, one of the key improvements reflected was the enhancement of leaf edges. YOLOv8′s bounding boxes and masks provided a rough approximation of the leaf area, but SAM was able to capture the finer details of the leaf shapes, including serrated edges and irregularities. leaves from the background, with SAM accurately capturing the leaf edges. The visual inspection confirms that SAM performs well on complex images, handling variations in lighting, occlusions, and leaf orientation. The masked leaves are then extracted and stored and a separate folder for further analysis, such as disease detection, as shown in Figure 7. By integrating SAM with YOLOv8, one of the key improvements reflected was the enhancement of leaf edges. YOLOv8′s bounding boxes and masks provided a rough approximation of the leaf area, but SAM was able to capture the finer details of the leaf shapes, including serrated edges and irregularities. SAM further refined the segmentation, providing precise boundaries, even in the presence of overlapping leaves. The segmented masks clearly delineated the tomato leaves from the background, with SAM accurately capturing the leaf edges. The visual inspection confirms that SAM performs well on complex images, handling variations in lighting, occlusions, and leaf orientation.

The masked leaves are then extracted and stored and a separate folder for further analysis, such as disease detection, as shown in Figure 7. By integrating SAM with YOLOv8, one of the key improvements reflected was the enhancement of leaf edges. YOLOv8 ′ s bounding boxes and masks provided a rough approximation of the leaf area, but SAM was able to capture the finer details of the leaf shapes, including serrated edges and irregularities. For plant disease detection tasks this is very crucial to precisely segment and identify the small lesions or abnormalities on the leaves. Instead of using YOLOv8 and SAM models alone, the integration of these two exhibited significant enhancements in the tomato leaf segmentation. A notable increase can be seen in the IoU and Dice coefficient by using SAM to refine the YOLOv8-detected regions. Table 1 shows the training, validation, and testing performance of our integrated model in terms of precision, recall score, and mAP@50. During validation, our model has a precision score of 99.7%, a recall score of 99.5%, and an mAP@50 of 89.4%. In comparison, the inference time during validation is 144 milliseconds. The testing accuracy of our model shows a precision score of 100% and a recall score of 98%, whereas the inference time during testing was 142 milliseconds. Further analysis confirmed the effectiveness of SAM in handling complex leaf structures and occlusions. This work shows the effectiveness of YOLOv8 and SAM for accurate tomato leaf detection and extraction. We achieved a precision of 100%, a recall of 98%, and an F1 score of 84%. These findings have several practical implications for agriculture. First, our system can enable the accurate identification and extraction of individual tomato leaves. This system can be integrated with a tomato disease detection model for further disease analysis. This can lead to minimizing crop losses by early disease detection in tomato plants. Sec- For plant disease detection tasks this is very crucial to precisely segment and identify the small lesions or abnormalities on the leaves. Instead of using YOLOv8 and SAM models alone, the integration of these two exhibited significant enhancements in the tomato leaf segmentation. A notable increase can be seen in the IoU and Dice coefficient by using SAM to refine the YOLOv8-detected regions. Table 1 shows the training, validation, and testing performance of our integrated model in terms of precision, recall score, and mAP@50. During validation, our model has a precision score of 99.7%, a recall score of 99.5%, and an mAP@50 of 89.4%. In comparison, the inference time during validation is 144 milliseconds. The testing accuracy of our model shows a precision score of 100% and a recall score of 98%, whereas the inference time during testing was 142 milliseconds. Further analysis confirmed the effectiveness of SAM in handling complex leaf structures and occlusions.

This work shows the effectiveness of YOLOv8 and SAM for accurate tomato leaf detection and extraction. We achieved a precision of 100%, a recall of 98%, and an F1 score of 84%. These findings have several practical implications for agriculture. First, our system can enable the accurate identification and extraction of individual tomato leaves. This system can be integrated with a tomato disease detection model for further disease analysis. This can lead to minimizing crop losses by early disease detection in tomato plants. Second, our findings can contribute to precision agriculture practices by enabling targeted interventions based on individual tomato leaf characteristics. Third, our system can reduce farmer costs by automating leaf counting and measurement. Moreover, it has the potential for real-time applications; it can be integrated into a drone-based monitoring system. We believe that our work can contribute to the development of more efficient and sustainable agricultural practices.

## 5. Discussion

In the given research, the tomato leaves were segmented using the images of tomato plants with the help of the YOLOv8 and the Segment Anything Model (SAM) model. The research aimed to evaluate the accuracy of the segmentation of tomato leaves by both models as it is important for many agricultural techniques which include plant monitoring, disease detection, and farming automation. This discussion also examines both models, their integration as well as the strengths and limitations of models to further precision agriculture objectives.

During experiments, YOLOv8 demonstrated a very good ability to detect tomato leaves even in cases such as many disorganized overlapping leaves where multiple leaves were dispersed and or alongside each other. The bounding boxes generated by YOLOv8 provided an adequate preliminary stage for various segmentation tasks as they included all the individual leaves. Additionally, the high precision and recall of the model, measured by its mAP capacity of the model to perform numerous overlapping tasks, enabled the model to detect objects within complicated environments accurately. However, there are still some performance limitations of YOLOv8 in terms of pixel-level segmentation accuracy which is designed only for target bounding box detection. In more complex cases, such as heavily shadowed leaves or leaves that were in the background, the bounding box was typically considered too broad. The limitations of YOLOv8 necessitated the use of a more refined segmentation approach, such as SAM, for achieving finer pixel-level accuracy. The regions identified by YOLOv8 were provided as input to SAM for producing detailed segmentation masks for each detected leaf. This method allowed for a more precise delineation of leaf boundaries, especially in cases where YOLOv8 ′ s bounding boxes were too coarse. SAM was particularly effective in handling the complex shapes and contours of tomato leaves, which is most important for accurate phenotypic analysis in precision agriculture.

Table 2 shows that our integrated model outperforms other segmentation models in terms of mAP, Precision, and Recall score. The most significant advancement is observed in the mAP, where our model achieves 0.90%, outperforming YOLOv8-SAM, the previous best performer. The precision score of our integrated model is estimated at 100%, meaning that when it identifies a tomato leaf, the chances of actually detecting it are exceptionally high. The average inference time of our integrated model over 100 runs is quite better than previous models which is 142 milliseconds with a GPU usage of 71.19%. This helps to mitigate false positives, which, in most cases, highly depend on the precision of the model's detection, especially in real-time applications. A recall rate of 98% reveals that the model has a high probability of detecting most of the tomato leaves in the provided image. This demonstrates the performance of the model under different conditions, such as the presence of small leaves and light conditions, which is a common feature in real-world Our proposed approach, integrating YOLOv8 and SAM, has shown convincing performance in terms of detecting, masking, and extracting tomato leaves. It is important to note that other models, such as YOLOv5-X [30], YOLOv6-L [31], YOLOv7 [32], and YOLOv8-SAM [33], has its merits, but the proposed combination of YOLOv8 and SAM has shown a comparable level of effectiveness, as indicated in Table 2. The visualization of comparatives analysis with the previous model with respect to performance metrics and average inference time is shown in Figures 8 and9.

AgriEngineering 2025, 7, x FOR PEER REVIEW 13 of 16

This demonstrates the performance of the model under different conditions, such as the presence of small leaves and light conditions, which is a common feature in real-world problems. Our proposed approach, integrating YOLOv8 and SAM, has shown convincing performance in terms of detecting, masking, and extracting tomato leaves. It is important to note that other models, such as YOLOv5-X [30], YOLOv6-L [31], YOLOv7 [32], and YOLOv8-SAM [33], has its merits, but the proposed combination of YOLOv8 and SAM has shown a comparable level of effectiveness, as indicated in Table 2. The visualization of comparatives analysis with the previous model with respect to performance metrics and average inference time is shown in Figures 8 and9. This demonstrates the performance of the model under different conditions, such as the presence of small leaves and light conditions, which is a common feature in real-world problems. Our proposed approach, integrating YOLOv8 and SAM, has shown convincing performance in terms of detecting, masking, and extracting tomato leaves. It is important to note that other models, such as YOLOv5-X [30], YOLOv6-L [31], YOLOv7 [32], and YOLOv8-SAM [33], has its merits, but the proposed combination of YOLOv8 and SAM has shown a comparable level of effectiveness, as indicated in Table 2. The visualization of comparatives analysis with the previous model with respect to performance metrics and average inference time is shown in Figures 8 and9.

## Figures et tableaux

**Figure 1.** Methodology for Tomato Leaf Detection, Segmentation, and Masks Extraction.

**Figure 1.** Methodology for Tomato Leaf Detection, Segmentation, and Masks Extraction.

**Figure 2.** Autodistill Process for auto-labeling unlabeled data.

**Figure 2.** Autodistill Process for auto-labeling unlabeled data.

**Figure 3.** Segment Anything Model for Tomato Leaf Segmentation.

**Figure 3.** Segment Anything Model for Tomato Leaf Segmentation.

**Figure 4.** Performance Metrics of YOLOv8 (a) Precision-Recall Curve (b) Precision-Confidence Curve (c) Recall-Confidence Curve (d) F1-Confidence Curve.

**Figure 4.** Performance Metrics of YOLOv8 (a) Precision-Recall Curve (b) Precision-Confidence Curve (c) Recall-Confidence Curve (d) F1-Confidence Curve.

**Figure 5.** Leaf Detection within Bounding Boxes.

**Figure 6.** Leaf Masking Using SAM.

**Figure 5.** Leaf Detection within Bounding Boxes.

**Figure 5.** Leaf Detection within Bounding Boxes.

**Figure 6.** Leaf Masking Using SAM.Figure 6. Leaf Masking Using SAM.

**Figure 6.** Leaf Masking Using SAM.Figure 6. Leaf Masking Using SAM.

**Figure 7.** Leaf Masks Extraction to a separate folder.

**Figure 7.** Leaf Masks Extraction to a separate folder.

**Figure 8.** Figure 8. Figure 8. Comparison chart with previous models based on precision, recall, and accuracy.

**Figure 8.** Figure 9. Figure 8. Comparison chart with previous models based on precision, recall, and accuracy.

**Table 1.** Training, validation, and testing results of our model for tomato leaf class on the tomato village dataset.

    Mode | Images | Instances | Precision | Recall | mAP@50 | Inference Time (ms)
    Training | 8045 | 42,866 | 99.7% | 99.5% | 89.4% | 144
    Validation | 2298 | 9894 | 100% | 96.8% | 93.7% | 140
    Testing | 1150 | 4086 | 100% | 98% | 90% | 142

**Table 1.** Training, validation, and testing results of our model for tomato leaf class on the tomato village dataset.

    Mode | Images | Instances Precision | Recall | mAP@50 | Inference Time (ms)
    Training | 8045 | 42,866 | 99.7% | 99.5% | 89.4% | 144
    Validation | 2298 | 9894 | 100% | 96.8% | 93.7% | 140
    Testing | 1150 | 4086 | 100% | 98% | 90% | 142

**Table 2.** Comparison of our integrated model with different detection algorithm models.

    Model | Resolution | Precision | Recall | mAP | Average Inference Time (ms)
    YOLOv5-X | 608 × 608 | 88% | 85% | 80% | 415
    YOLOv6-L | 640 × 640 | 89% | 81% | 91% | 400
    YOLOv7 | 640 × 640 | 87% | 83% | 91% | 278
    YOLOv8-SAM | 960 × 960 | 92% | 83% | 89% | 198
    Our |  |  |  |  | 
    integrated | 640 × 640 | 100% | 98% | 90% | 142
    model |  |  |  |  |
