---
id: 2025-yu-yolo-gcof-lightweight-low-altitude
title: "YOLO-GCOF: A Lightweight Low-Altitude Drone Detection Model"
year: 2025
backend: grobid
---

## Abstract

The maturity of the drone industry and the open access to low-altitude airspace have resulted in massive use of low-altitude drones. While the use of drones has brought economic efficiency, the illegal use of drones has raised concerns about increased drone trespass in the no-fly zone and countermeasure strategies. These concerns underscore the urgent need for low-altitude drone object detection. Traditional radar detection methods often struggle to detect small drones at low altitudes. To address this issue, we propose a lightweight model named YOLO-GCOF, leveraging an optimized version of the YOLOv8 architecture to enhance accuracy and enable efficient deployment on embedded devices. YOLO-GCOF incorporates the GSConv-Integrated Dynamic Group Convolution Shuffle Transformer (GI-DGCST) module as the feature extraction module, which captures fine-grained details and improves the detection of small-scale features. The integration of multi-level feature information is achieved by incorporating the Coordinate-Scale Attention High-level Screening-Feature Fusion Pyramid Networks (CSA-HSFPN) into the neck layer. The HSFPN architecture enables efficient multi-scale feature fusion, and the CSA module optimizes feature selection across scales, improving the model's ability to detect key features using both scale and coordinate information. The Detect-Olive Group Convolution Head (Detect-OGCH) module, a lightweight parametersharing design, is integrated into the head layer to significantly reduce the model's GFLOPs and parameter count while maintaining detection performance. Lastly, the original Complete Intersection over Union (CIoU) is replaced with the Focaler-SCYLLA IoU (Focaler-SIoU) to improve detection accuracy. The YOLO-GCOF model outperforms the original YOLOv8n, as demonstrated by a 1.1% improvement in mAP@50, alongside reductions in parameter count, computational overhead, and model size by 60%, 49.4%, and 55.1%, respectively. Additionally, the YOLO-GCOF model achieved 91.5% mAP@50 on the DUT-Anti-UAV dataset. These results and successful deployment on Raspberry Pi 4B demonstrate that the YOLO-GCOF is highly effective for lightweight, high-performance low-altitude drone detection.

## I. INTRODUCTION

As the drone industry and its associated supply chains mature, modern drones have become affordable, small scale, highly flexible, and easy to operate. The gradual opening of low-altitude airspace has accelerated drone market growth. Drones are now widely used in aerial photography, fire rescue, light shows, and more. However, this proliferation has exposed sensitive areas, such as research and training bases and military facilities, to the risks of illegal intrusion

The associate editor coordinating the review of this manuscript and approving it for publication was Yongming Li . and aerial reconnaissance, posing a significant threat to public safety and national security. Effective detection of low-altitude drones is a critical component of drone countermeasures and control. Current monitoring techniques, such as radar detection [1], radio spectrum detection [2], and acoustic detection [3], often require expensive equipment and specific environments. Radar detection relies on electromagnetic wave reflections to locate targets, but drones, with their low altitude, slow speed, and small reflective area, pose significant challenges [4]. Additionally, ground clutter at low altitudes further complicates radar detection. Wireless detection identifies drones based on radio signals, but it cannot detect low-altitude drones that do not emit such signals. Acoustic detection relies on the acoustic fingerprint produced by the mechanical components of a low-altitude drone during flight. However, in practice, complex background noise often masks the drone's acoustic signature, making it difficult to reliably and accurately extract the drone's fingerprint. The optoelectronic detection method for low-altitude drones uses machine vision and object detection algorithms for effective detection. Machine vision-based optoelectronic detection offers strong visualization, real-time tracking of agile, small-scale low-altitude drones, fast response times, high positioning accuracy, and low-cost, rapid deployment. This is well-suited for detecting low-altitude drones.

Recent advancements in artificial intelligence have significantly enhanced object detection. Deep learning-based algorithms automatically learn complex features from large datasets, improving detection accuracy, robustness, and performance across diverse environments. In contrast, traditional object detection methods that combine handcrafted features with machine learning classifiers [5] face challenges such as high computational complexity, low efficiency, and limited generalization. These methods also struggle with real-time detection, whereas deep learning improves both speed and accuracy. Deep learning-based algorithms are particularly effective for detecting low-altitude drones due to their small size and agile flight.

The combination of deep learning models with embedded devices is becoming increasingly common in various fields. Deploying low-altitude drone detection models on embedded devices is particularly beneficial for the longterm operation of scenarios such as drone surveillance, due to the low-latency and low-power advantages of embedded systems. In addition, running deep learning tasks locally on these devices reduces data transfer and cloud computing costs, making large-scale deployment of more comprehensive surveillance feasible. However, deep learning models typically require significant computational resources and memory, which poses a challenge for embedded devices with limited hardware. In addition, overly complex models can degrade real-time performance, while simply reducing the model size often affects detection accuracy.

For this purpose, this paper proposes the YOLO-GCOF model, an enhancement of the YOLOv8 architecture, designed to improve low-altitude drone detection. Key innovations include an optimized target feature extraction module, a refined feature fusion network, a lightweight head network, and an improved Intersection over Union (IoU) loss function. These advancements enable model lightweighting while maintaining real-time detection capabilities and enhancing detection accuracy. The resulting model is well-suited for detecting low-altitude drones in no-fly zones, offering strong technical support for drone surveillance, addressing safety concerns in restricted areas, and improving economic efficiency.

## II. RELATED WORK

The rise of new low-altitude drones, characterized by small reflective areas, high flight flexibility, and low altitudes, has made traditional detection methods ineffective. However, with the advancement of artificial intelligence, deep learning-based object detection has become a prominent research focus. Compared to traditional object detection methods, deep learning-based object detection methods make it possible to efficiently detect this new type of low-altitude drone.

Object detection algorithms based on deep learning can be divided into two categories: two-stage region-based and one-stage regression-based [6]. The former generates candidate regions before classifying targets and refining bounding boxes. Notable algorithms in this category include RCNN, Fast RCNN, Faster RCNN, and Mask RCNN [7], [8], [9], [10]. In contrast, one-stage algorithms, such as SSD and YOLO [11], [12], directly process images through a neural network, generating both classification and location information without the need for candidate region generation. The two-stage object detection algorithm achieves high detection accuracy but is computationally intensive, with a large number of parameters and extended inference times. In contrast, the one-stage object detection algorithm, while slightly less accurate, offers advantages such as reduced computational complexity, fewer parameters, smaller model sizes, and higher detection efficiency, making it more suitable for realtime detection applications.

The YOLO algorithm, as a classical one-stage object detection model, has been iterated over many iterations to form a series of versions. By choosing the right combination of algorithm version and model size, YOLO achieves an optimal balance between detection speed, accuracy, and model complexity, making it widely adopted in various fields. Among the many versions, YOLOv8 stands out as the landmark version in the YOLO family for its real-time performance, high accuracy, and powerful multi-scale detection capabilities.

In the backbone layer, YOLOv8 [13] utilizes the C2f module as the feature extraction module to better aggregate multi-scale information. By stitching the output of different Bottleneck modules with the original feature maps, it improves the representation of features across various scales. The neck layer, based on the Path Aggregation Network [14] structure, aggregates multi-level feature paths, further boosting the model's ability to handle multi-scale information. Additionally, YOLOv8 employs a decoupled head, separating the classification and detection tasks to better model the relationship between object location and category, thereby improving detection performance. The loss function comprises classification loss and regression loss. Low-altitude drones are small in size, which presents challenges similar to those encountered in small target detection tasks: the target in the original image is often too small, with limited distinctive features, making it difficult to extract useful information. Additionally, the complex background and significant variations in target scale from different angles can cause the target to be 'buried' in the background, leading to missed detections. Zhang et al. [15] improved the SSD algorithm by incorporating a multi-scale feature fusion module and an attention mechanism to address the issue of insufficient feature information for small objects. This enhancement led to an average accuracy of 84.07% in detecting low-altitude drones. Wang et al. [16] introduced an enhanced Faster-RCNN algorithm aimed at low-altitude drone detection. This method utilizes the ResNet50 architecture to extract features and applies bilinear interpolation to sample and fuse feature maps. Subsequently, the Region Proposal Network (RPN) is used for binary categorization and bounding box regression. Additionally, the soft-nms algorithm is used to optimize redundant anchor boxes. The final AP values for large and small targets are 89.7% and 82.1%, respectively. Zhao et al. [17] introduced a low-altitude drone detection algorithm based on YOLOv7. This method modifies the original YOLOv7 anchor box and enhances the feature fusion network by adding more network layers, improving the fusion of shallow and deep features to better capture small target features. To improve detection performance across various scales and targets, an additional smaller prediction head is incorporated into the network, achieving a mAP of 75.69%.

Despite advancements in low-altitude drone detection, current models still struggle to balance detection accuracy and model lightweighting. Monitoring low-altitude drones in complex environments, such as forests, urban areas, and lowlight conditions, further complicates detection. Moreover, deploying these models on embedded devices with limited computational resources presents additional challenges. Therefore, further research is needed to develop effective detection methods that can operate efficiently within the constraints of embedded devices.

## III. METHODS

To lighten the model for cost-effective deployment in embedded devices and to improve the accuracy of low altitude drone detection, a series of targeted optimizations of YOLOv8n are carried out in this study. The resulting optimized model is called YOLO-GCOF and its structure is shown in Fig. 1.

First, we propose a novel improvement to the Dynamic Group Convolution Shuffle Transformer (DGCST) module by integrating a residual network, GSConv, and a sandwich structure, resulting in the GSConv-Integrated DGCST (GI-DGCST) module. This module serves as the feature extraction component of the backbone layer. Compared to the C2f module, the GI-DGCST module reduces both the parameter count and computational complexity, while also enhancing detection accuracy. These optimizations make the model more suitable for deployment on embedded devices with limited resources, improving the detection of lowaltitude drones.

Second, the Coordinate-Scale Attention High-level Screening-Feature Fusion Pyramid Networks (CSA-HSFPN) is incorporated to redesign the neck layer structure, enabling efficient fusion of features at multiple scales. By integrating the innovative CSA module with Coordinate Attention (CA) module and multi-scale feature selection mechanism, the model's ability to emphasize essential feature information across different scales is enhanced. By leveraging both scale and coordinate data, the model strengthens its ability to capture essential features, thus enhancing detection performance.

Third, a lightweight Detect-Olive Group Convolution Head (Detect-OGCH) module is designed to replace the original Detect module, based on the concept of parameter sharing. The module enables efficient feature learning through expansion, holding, and compression over the channels, while maintaining low computational and parametric costs.

Finally, to further enhance model performance while preserving its lightweight characteristics, we replace the original CIoU with Focaler-SCYLLA IoU(Focaler-SIoU), combining the advantages of Focaler-IoU and SIoU. This loss function adjusts the traditional IoU loss by employing linear interval mapping, enabling the model to better concentrate on challenging samples. This is particularly useful for detection tasks involving a high proportion of difficult samples, as it helps to alleviate the challenges associated with detecting such objects.

### A. GI-DGCST MODULE

In YOLOv8, the C2f module extracts multi-scale features through multiple convolutional layers and cross-layer connections. This structure allows interaction between features on different levels thus strengthening its expressiveness. Nevertheless, such a network design will significantly increase model complexity and incur higher computational overhead and time costs. This paper replaces the standard C2f module in the backbone architecture with the proposed GI-DGCST module. The GI-DGCST module significantly reduces the computational cost and the model parameters with improved detection accuracy.

Fig. 2 shows the structure of the GI-DGCST module. Two branches constitute the GI-DGCST module. In the other branch, a standard residual connection Conv of both low and high-level features is used. The proposed design helps the model to have more ability to extract richer feature representations which gain the advantage of preserving the fine features of some small objects. The other branch contains a sandwich structure with two GSConv [18] layers, followed by a DGCST [19] module. The DGCST module is introduced to conduct global feature extraction and the GSConv layers for local and inter-channel information fusion. This combination greatly increases the fluidity of information flow and supports a well-synchronized flow of synergy between feature extraction and information integration. The core idea of the DGCST module is the 3:1 partitioning strategy. The output of the GSConv layer does not go to dynamic group convolution and channel shuffle first, but part of it does, the rest is output directly. Dynamic group convolution can dynamically and adaptively change its grouping method according to input features' distribution so that each group of convolution kernels learns distinguished fine-grained features in a targeted way. In addition to avoiding redundant computations frequently committed in static group convolution, this approach allows the model to flexibly capture fine-grained feature details. The dynamic group convolution module has multiple feature maps fed in by it that can be rearranged and mixed by the channel shuffle module enabling information interaction and fusion among different feature map groups. Dynamic group convolution and channel shuffle together help the model pay more attention to fine-grained features, improving the sensitivity of fine features when detecting small-scale targets. The output of the concatenation operation feeds into the feedforward network GSConvFFN. The feedforward network improves the model to learn deep features via nonlinear transformation and feature interaction between channels, and by residual connections. These operations help the model capture local relationships and contextual information inside feature maps so the representational capacity of the model could be better.

GSConv is illustrated in Fig. 3. GSConv initially halves the input channels through a standard convolution operation. The output is then processed through a depthwise convolution and a standard convolution, which are concatenated with the original output. A shuffle operation is applied to produce the final output. By reorganizing features, GSConv effectively captures information at different levels while minimizing redundancy. Additionally, as a lightweight convolution, GSConv offers excellent performance, making it well-suited to our needs.

### B. CSA-HSFPN STRUCTURE

During the downsampling of small target features, deeper feature maps are more prone to losing essential information, whereas shallower, high-resolution feature maps often retain sufficient critical details. Consequently, integrating deep and shallow feature information allows the model to convey rich semantic information, enhancing its ability to capture small target features. This paper implements a multi-scale feature fusion approach based on the HSFPN [20] structure, enabling the model to extract features at different scales more efficiently and comprehensively, as illustrated in Fig. 4.

The HSFPN architecture comprises two main components: the Feature Selection, which selects features from the backbone layer, and the Selective Feature Fusion (SFF) module, which integrates these features. The Feature Selection module filters features across different scales, relying on both the CSA module and the Dimensional Matching (DM) module.

The CSA module, implemented using multi-scale feature selection mechanism and CA [21] mechanism, is illustrated in Fig. 5. The multi-scale selection leverages Conv2d layers with varying dilation rates to localize features at different scales. The Generate Dynamic Weight(GDW) module dynamically adjusts weights, enabling the module to focus on features at the required scales. The CA mechanism averages and pools the input spatially along the horizontal and vertical axes, concatenates these outputs, compresses the channels using convolution, and then encodes the spatial information along vertical and horizontal dimensions. This encoded spatial information is processed through a split operation, followed by Conv2d and Sigmoid layers. Finally, Given the input X, the re-weighting process of the CA mechanism for the spatial information A H and A W obtained from the two branches is shown in (1). The multi-scale feature selection mechanism enhances the model's capacity to recognize features at different scalessmall-scale convolutions capture detailed features, while large-scale convolutions capture contextual information. The CA mechanism strengthens the connection between feature information and spatial coordinates, enabling the model to better perceive and capture features based on spatial location information. In the CSA module, the multi-scale feature selection mechanism supplies multi-resolution feature information, while the CA mechanism dynamically adjusts attention based on coordinate information, emphasizing critical feature information. This design allows the model to balance fine details with contextual cues, enriching the overall feature representation. Before feature fusion, the DM mechanism aligns the dimensions of feature maps from different scales to ensure a consistent number of channels across them.

F out = X × A H × A W (1)

The SFF module's core principle is to integrate filtered primary and advanced features via a selective fusion mechanism, as illustrated in Fig. 6. Starting with the advanced feature input F advanced ∈ R C×H×W and a primary feature F primary ∈ R C×H 1 ×W 1 , the advanced feature is initially expanded using a ConvTranspose operation with a 2-stride and a 3 × 3 convolution core, getting the feature F advanced ∈ R C×2H×2W . To harmonize the dimensions of advanced and primary features, bilinear interpolation is employed to either enlarge or shrink the advanced features, producing F att ∈R C×H 1 ×W 1 . Subsequently, the CA module adjusts the advanced features by applying corresponding attention weights, facilitating the refinement of primary features and ensuring alignment in their dimensions. Finally, the refined primary features are merged with the advanced features, enhancing the overall feature representation. This fusion approach combines the semantic content of advanced features with the detailed information from primary features, ultimately improving the model's effectiveness across multiple scales. Equations ( 2) and (3) outline the feature selection and fusion processes:

F att = BL ConvTranspose(F advanced )

(2)

F out = F primary × CA (F att ) + F att(3)

### C. DETECT-OGCH MODULE

In YOLOv8, the Head's parameters count constitutes nearly half of the entire model, making its optimization essential. To address this, this paper introduces a lightweight, decoupled detection head, Detect-OGCH module, inspired by a shared structure, as shown in Fig. 7. The Head module employs group convolution to form an olive-shaped backbone convolution structure, followed by two convolutions with 1 × 1 kernel size to separate the classification and detection heads. Group convolution avoids fully connecting all input channels, instead processing each group independently. This design not only reduces computational demands and accelerates processing but also regularizes the model, as each convolution kernel operates independently on corresponding inputs, enhancing model generalization. The olive-shaped backbone structure provides an ''expansionpreservation-compression'' effect on the feature map. In the channel expansion phase, important features are emphasized, enriching the module's feature representation capacity. During the channel preservation phase, information is stably transmitted in higher dimensions, minimizing the loss of significant details and reducing interference from irrelevant data. Finally, in the channel compression phase, key features are selectively retained, restoring the feature map's shape.

### D. FOCALER-SIOU

employs CIoU Loss as the bounding box regression loss function. Building on DIoU [22] loss, CIoU loss introduces a penalty term for aspect ratio mismatches between the bounding box and Ground Truth (GT) box, aiming to minimize aspect ratio discrepancies. However, for objects at varying scales, the aspect ratio differences in bounding boxes can be significant, leading to instability in the model optimization process. Additionally, CIoU loss lacks adaptability across different detectors and detection tasks, overlooks sample balance, and may restrict the model's convergence rate when sample similarity is low.

SIoU [23] loss introduces an innovative calculation method that considers the angle formed by the ground truth and predicted bounding boxes. The redesigned loss structure ensures improved stability of the predicted box, accelerates convergence, and enhances alignment with the actual box. SIoU loss consists of four terms: Angle Loss, Distance loss, Shape loss, and IoU loss. The formulation of this loss function is provided in (4).

L SIoU = 1 -IoU + + 2(4)

represents the Angle Loss, and Equation ( 5) provides its definition.

= 1 -2sin 2 arcsin (x) - 1 -e -γρ t (7)

ρ x = b gt cx -b cx C w 2 (8) ρ x = b gt cx -b cx C w 2 (9) γ = 2 - (10

)

where C w and C h represent the width and height of the smallest rectangular boundary that encloses both the predicted box and the ground truth box, respectively. represents the Shape Loss, and Equation ( 11) provides its definition. θ represents the degree of concern for shape loss, and its value ranges from 2 to 6.

= 1 -e -|w-w gt | max ( w,w gt ) θ + 1 -e -|h-h gt | max ( h,h gt ) θ (11

)

Imbalance in the distribution of difficult and easy samples is a common issue in various detection tasks. One of the core ideas of Focaler-IoU is to address this imbalance by focusing on the distribution of these samples. To dynamically prioritize different regression samples for various detection tasks, Focaler-IoU [24] reformulates the IoU Loss through a linear interval mapping approach. The modified IoU Loss is expressed in (12).

IoU focaler =    0, IoU < d IoU -d u-d , d ≪ IoU ≪ u 1, IoU > u (12)

Here, [d, u] ∈ [0, 1], where adjusting the values of d and u allows the loss function to prioritize different regression samples. Equation ( 13) defines the Focaler-IoU Loss.

L Focaler-IoU = 1 -IoU focaler (13) By applying the Focaler-IoU Loss to the SIoU Loss, we obtain the Focaler-SIoU Loss, which is defined by Equation. (14).

L Focaler-SIoU = L SIoU + IoU -IoU focaler (14)

cx , b cy ) and (b gt cx , b gt cy ) represent the center coordinates of the predicted box and the GT box, respectively. represents the Distance Loss, and Equation (7) provides its definition. = t = x,y

In the task of detecting low-altitude drones, the distribution of difficult samples is dominant. By allowing the loss function to focus more on these challenging samples, the model can learn to extract features from them more efficiently, thereby improving detection accuracy.

## IV. EXPERIMENTS A. EXPERIMENTAL SETUP

The experimental environment for this study was set up using the hardware included a NVIDIA A10 GPU with 24 GB 1.

### B. DATA PREPARATION

This paper uses two publicly available datasets: the TIB-Net-drone dataset and the Amateur Unmanned Air Vehicle Detection (AUAVD) dataset. The TIB-Net-drone dataset consists of small-scale target samples, while the AUAVD dataset includes large-, medium-, and small-scale target samples, with small-scale targets being the majority. The dataset used in this study is composed of the entire TIB-Net-drone dataset, along with a subset of images filtered from the AUAVD dataset, resulting in a total of 5,010 images. These two datasets collectively form the A&T dataset. As shown in Fig. 8, the dataset includes samples with simple backgrounds, such as open wastelands and parking lots, as well as samples with more complex backgrounds, such as forests and urban residential areas under cloudy skies. The constructed dataset categories include a drone category. The distribution of low-altitude drone shape is shown in Fig. 9, with most being small to medium-sized objects. To train the detection model for low-altitude drones, the dataset is split into three subsets: training, testing, and validation sets, with a distribution ratio of 7:2:1.

Publicly available dataset DUT-Anti-UAV includes a variety of drone types and diverse scene information, such as skies, dark clouds, jungles, high-rise buildings, residential areas, farmland, and playgrounds. Additionally, the dataset encompasses a range of lighting conditions and weather conditions.

### C. EVALUTION METRICS

To comprehensively evaluate the model's performance, F1-score, mAP, the number of parameters (Params), and Giga Floating-point Operations per second (GFLOPs) are used as evaluation metrics. GFLOPs assess the model's computational complexity, and Params is used to evaluate its size. Generally, to facilitate deployment on lower-performance devices, the model should have fewer parameters and lower computational requirements. The model size is the size of the weights file after training is completed, evaluated in MB.

Equation (17) shows the formula for the F1-score. The greater the value of this metric, the better the model's performance will be. The F1-score combines Precision and Recall, effectively balancing both metrics. Equation (18)shows the average precision formula for the N categories.

Precision = TP TP + FP (15

)

Recall = TP TP + FN (16

)

F1 = 2 × Precision × Recall Precision + Recall (17) mAP = 1 N N i=1 1 0 Precision (Recall) d (Recall)(18)

of memory and an Intel Xeon Platinum 8369B CPU. The deep learning framework for this study based on Pytorch 2.3.1, with Cuda version 12.1, and Python version 3.10. The hyperparameters configuration for training experiments are shown in Table

### D. EXPERIMENTAL RESULTS

### 1) IMPACT OF VARIOUS MODULES WITH DYNAMIC TECHNOLOGIES ON NETWORK PERFORMANCE

The use of dynamic techniques is effective, as it enables the module to dynamically adjust the model's parameters based on the characteristics of the inputs, improving detection accuracy while maintaining a lightweight model. To validate the performance of the GI-DGCST module, comparative experiments are conducted with other modules that utilize dynamic techniques. Table 2 presents the test results based on the dataset employed in this study. As shown in the table, the GI-DGCST module not only significantly reduces computational complexity and parameter count, but also improves the model's detection accuracy compared to other modules that use dynamic techniques. Although its GFLOPs exceed those of the original DGCST module by 0.2G, it achieves a 1.5% increase in both mAP@50 and mAP@50-95, making the trade-off justifiable. The introduction of GI-DGCST enhances model accuracy with a lower computational overhead, partly because GSConv can efficiently capture features at different levels, and partly due to the sandwich structure design, which facilitates synergy between feature extraction and information flow. This enables the DGCST module to better capture global context and improve sensitivity to fine-grained features, thereby enhancing the model's feature extraction capabilities.

### 2) IMPACT OF DIFFERENT ATTENTION MODULES IN THE HSFPN ARCHITECTURE ON NETWORK PERFORMANCE

To verify the performance of the CSA module, Module 1: Channel Attention, Module 2: Coordinate Attention, and Module 3: Content Anchor Attention are integrated into the HSFPN structure, and the model is trained on the dataset used in this paper. Table 3 presents the test results for each attention module in the HSFPN structure, with Module 4: ours.

As shown in the table, the CSA module provides the greatest improvement in detection accuracy compared to the other attention modules. The combination of the multi-scale feature selection mechanism and the coordinate attention mechanism enables the model to comprehensively consider both detailed features and contextual information. This improves the model's focus on critical features and delivers rich semantic information for feature fusion.

### 3) THE EFFECT OF THE NUMBER OF GROUPS IN DETECT-OGCH ON MODEL PERFORMANCE

The core in Detect-OGCH module consists of GConv layer, and the number of groups directly impacts its performance.

If the number of groups is set too large, each group will have too few channels, which may hinder the module from capturing global features, thereby negatively impacting model performance. On the other hand, if the number of groups is set too small, it increases the Params and GFLOPs, leading to unnecessary overhead. This may also impair the module's ability to extract features and learn complex patterns, thereby reducing its overall performance.

### 4) COMPARISON OF DIFFERENT LOSS FUNCTIONS

In target detection tasks, the choice of IoU loss function is crucial to model performance, as it directly impacts the prediction accuracy of the model on the target bounding boxes. Different IoU loss functions evaluate the overlap between predicted and ground truth boxes using varying calculations, which in turn affects gradient updates during training and the final detection performance.

### 5) ABLATION EXPERIMENT

To evaluate the impact of each improved module on the low-altitude drone detection model, ablation experiments are conducted using YOLOv8n as the baseline. The results of these experiments are presented in Table 6. Exp 1 replaces the C2f module in YOLOv8's backbone with GI-DGCST, resulting in a reduction of 0.4M Params and 0.9G GFLOPs, while improving F1, mAP@50, and mAP@50-95 by 0.1%, 0.4%, and 0.1%, respectively. This suggests that the GI-DGCST module, compared to the C2f module, allows for easier extraction of low-altitude drone target features with a lower computational cost. Exp 2 introduces CSA-HSFPN into the model, reducing the model's Params and GFLOPs by 1.1M and 1.2G, respectively, while improving mAP@50 and mAP@50-95 by 0.6% and 0.7%. This demonstrates that reconstructing the neck network structure using the HSFPN framework, combined with the introduction of the CSA module, enhances the fusion and extraction of features at different scales. Exp 3 replaces the original Detect module with Detect-OGCH module, leading to a reduction of 0.5M Params and 2.0G GFLOPs. Although F1 decreases slightly by 0.2%, mAP@50 and mAP@ 50-95 improve by 0.2% and 0.9%, respectively. This indicates that the Detect-OGCH module allows the model to maintain strong performance with a significant reduction in GFLOPs. Exp 4 replaces the original CIoU with Focaler-SIoU, improving mAP@50 by 0.2%. This implies that modifying the loss function to emphasize the imbalance between challenging and simple samples can enhance the model's performance.

Exp 3 incorporates GI-DGCST module and CSA-HSFPN into the model, leading to a reduction of 1.5M in Params and 2.0G in GFLOPs, while achieving improvements in F1, mAP@50, and mAP@50-95 over the baseline model. This indicates that GI-DGCST and CSA-HSFPN can complement each other in different parts of the model, and their introduction is effective. Exp 5 adds the Detect-OGCH module to Exp 3, and its performance improves compared to the baseline model in both cases. Although mAP@50 decreases by 0.1% compared to Exp 3, its GFLOPs decrease by 2G, which we consider worthwhile. Exp 7, which introduces all the modules, reduces Params and GFLOPs by 1.8M and 4G compared to the baseline model, and improves F1, mAP@50, and mAP@50-95 by 1%, 1.1%, and 0.7%, respectively. the last two figures show that the detection accuracy of the improved model is higher than that of the baseline model in complex backgrounds. To more intuitively observe the difference in how the models focus on target features before and after improvement, heat maps are generated using Lay-erCAM [25] for visual presentation. As shown in Fig. 11, the improved model is able to focus more effectively on the target area in simple backgrounds without redundancy, and it significantly reduces the interference of background noise in complex backgrounds, leading to more accurate drone detection. These two visual comparisons confirm that the improvements made to the model are effective.

### 6) DETECTION PERFORMANCE ANALYSIS OF THE MODEL BEFORE AND AFTER ENHANCEMENT

### 7) MODELS COMPARISON

To better evaluate the performance of the improved models, this study compares YOLOv5n, YOLOv7-t, YOLOv8n, YOLOv9-t, YOLOv10n, and YOLO11n. The detection results of each model on the A&T dataset are presented in Table 7. Based on this table, YOLOv8-GCOF achieves the second highest F1-score. Although YOLOv7-t has a higher F1-score than YOLOv8-GCOF, it comes at the cost of higher computational complexity. YOLO-GCOF outperforms other models, achieving top scores of 92.6% for mAP@50 and 59.5% for mAP@50-95. Table 8 compares YOLO-GCOF with other models in terms of Params, GFLOPs, and model size. YOLO-GCOF achieves the best results, with 1.2M Params, 4.1G FLOPs, and a model size of 2.68MB. Thus, YOLO-GCOF excels in both detection accuracy and lightweight design. Additionally, the performance of the YOLO-GCOF model was further evaluated on the DUT-Anti-UAV dataset, with the results presented in Table 9. As shown in the table, YOLO11n achieved the highest F1-score, while YOLO-GCOF ranked second with an F1-score of 89.4%. In terms of mAP@50, the key metric, YOLO-GCOF ranked first with a score of 91.5%, while YOLOv8-GCOF placed third with a mAP@50-95 of 61.2%.

### 8) EMBEDDED EXPERIMENT

The Raspberry Pi 4B, developed by the Raspberry Pi Foundation (UK), is a microcomputer motherboard based on the ARM architecture. It is equipped with a Broadcom BCM2711 quad-core, 64-bit ARM Cortex-A72 processor (clocked at up to 1.5 GHz), 8GB of LPDDR4 SDRAM, and a Broadcom VideoCore VI GPU, providing sufficient computing power for deep learning applications. With appropriate configuration and optimization, efficient deep learning inference and deployment can be achieved despite the device's limited performance. The Raspberry Pi 4B is shown in Fig. 12.

We successfully deployed the trained low-altitude drone detection model on the Raspberry Pi 4B and conducted detection tests. Fig. 13 compares the original YOLOv8n with YOLO-GCOF, both deployed on the Raspberry Pi 4B, for low-altitude drone detection. The results show that the improved YOLO-GCOF model achieves higher confidence levels and improved localization accuracy.

## V. CONCLUSION

To address the low performance in detecting low-altitude drones, this study presents an optimized YOLOv8-based lightweight detection model. First, we replace the C2f module in the YOLOv8 backbone with the GI-DGCST module, which integrates residual connectivity, a sandwich structure, DGCST module, and GSConv layer. This design mitigates the loss of small-scale features during downsampling, while the sandwich structure enhances feature extraction and information integration. Next, we reconstruct the neck structure with HSFPN to improve feature fusion across scales and propose the CSA module to incorporate both scale and coordinate information, boosting the model's discriminative ability. We also design Detect-OGCH module to replace the original detection head module, reducing GFLOPs while maintaining performance. Finally, the CIoU loss function is replaced with Focaler-SIoU, which is better suited for datasets with many challenging samples, improving bounding box regression. Experimental results show that, compared to YOLOv8n, the proposed model reduces Params, GFLOPs, and model size by 60%, 49.4%, and 55.1%, respectively, while improving mAP@50 by 1.1%. These reductions, along with high detection accuracy, make the model well-suited for deployment on performance-limited devices. Additionally, the YOLO-GCOF model achieves a detection accuracy of 91.5% on the DUT-Anti-UAV dataset, outperforming other models and demonstrating its superior performance.

This study acknowledges the challenges of low-altitude drone detection, especially in complex real-world environments, where models may mistakenly classify non-drone objects, such as birds or balloons, as drones. In the next phase, we plan to expand the model's capabilities by adding more object categories, further optimizing its performance and enhancing its applicability in real-world scenarios.

## Figures et tableaux

[figure sans légende identifiée] The classification loss uses VariFocal Loss, which addresses category imbalance and directs the model's focus to key samples that improve detection. The regression loss includes Complete IoU (CIoU) loss and Distribution Focal Loss (DFL), with CIoU optimizing box positioning and DFL refining bounding box predictions by introducing distributed modeling, thereby enhancing detection accuracy.

FIGURE 1. YOLO-GCOF network architecture.

FIGURE 2. GI-DGCST structure diagram.

FIGURE 3. GSConv.

FIGURE 4. Framework of HSFPN.

FIGURE 5. CSA module.

FIGURE 6. Selective feature fusion mechanism.

FIGURE 7. Detect-OGCH module.

FIGURE 8. Samples of selected low-altitude drones from the A&T dataset.

FIGURE 9. Low-altitude drone shape distribution diagram.

**Fig. 10** shows the test results before and after model improvement. As shown in the first figure, the improved model reduces false detections. The second figure demonstrates that the improved model reduces missed detections, while

FIGURE 10. Detection results of YOLOv8(a) and Detection results ofYOLO-GCOF(b).

FIGURE 11. LayerCAM rendering of model validation datasets before and afterimprovement. (a) Origin images, (b) YOLOv8, and (c)YOLOV8-GCOF.

FIGURE 13. YOLOv8 (a) and YOLO-GCOF (b) Detection results on the Raspberry Pi4B.

**TABLE 1.** Configuration of experimental training.

**TABLE 2.** Comparison results of modules using different dynamic technologies.

**TABLE 3.** Comparison results of different attention modules.

**Table 4** shows the test results of Detect-OGCH module with various group configurations on the dataset used in this study, where x denotes the number of channels in the input to Detect-OGCH module, and the table values indicate the group count in the three convolution layers of the Detect-OGCH backbone module. As shown in the table, it is evident that properly configuring the number of groups is crucial for maximizing the performance of Detect-OGCH module.

**TABLE 4.** Experimental results of different group configurations.

**Table 5** 

    presents the test

**TABLE 5.** Comparison results of different IoU loss functions.

**TABLE 6.** Results of ablation experiment.

**TABLE 7.** Comparison results of detection performance of different models on the A&T dataset.

**TABLE 8.** Comparison results of different detection models.

**TABLE 9.** Comparison results of different models on the DUT-Anti-UAV dataset.
