---
id: 2023-mou-ink-detection-carbonized-herculaneum-papyri
title: "Ink Detection from Carbonized Herculaneum Papyri using Deep Learning"
year: 2023
backend: pymupdf
---

2023 26th International Conference on Computer and Information Technology (ICCIT) 13-15 December, Cox’s Bazar, Bangladesh

Ink Detection from Carbonized Herculaneum Papyri

using Deep Learning

1st Farzana Sharmin Mou Dept. of Computer Science

University of Birmingham

Birmingham, UK farzanamou773@gmail.com

2find Tanvir Ahmed Dept. of Computer Science and Engineering Dhaka University of Engineering & Technology, Gazipur

Dhaka, Bangladesh tanvirliban@gmail.com

## Abstract

A Roman villa in the town of Herculaneum, next to Pompeii, housed a library with thousands of ancient Greek and Roman scrolls. The eruption of Mount Vesuvius buried this villa approximately 2000 years old ago which has been discovered. The scrolls can no longer be opened without breaking them because they were carbonized by the heat of the volcano. Since Herculaneum ink is carbon-based, it affords no X-ray contrast against the underlying carbon-based papyrus. Some detached papyrus fragments that can be read under infrared light can be used as ground truth data for a machine learning model that could identify otherwise undetectable ink from X-rays. The process of ink detection involves locating the inked portions of the papyrus using data from a 3D X-ray scan of the papyrus surface. The model has been trained by selecting a pixel from the binary label picture and sampling a subvolume from the surface volume at the same coordinates. In order to update the model weights, then backpropagate the known label data. Once trained, the model can be used to predict the appearance of a label picture from diverse input data. Three distinct models, namely U-Net, Attention U-Net, and a Pretrained Autoencoder with Attention U-Net, have been applied. Then, utilizing those three models, ensemble approaches have been employed (average, voting, and weighted average) to choose the optimum outcome. The best dice score of 0.766 has been achieved by the average ensembling technique. This project shows how machine learning can detect ink in 3D scans and decipher carbonized parchment contents.

Index Terms—ink detection, unet, attention mechanism, pretrained autoencoder, ensemble technique, computer vision

## I. INTRODUCTION

Texts let us understand ancient Greeks and Romans. While other sources provide information about the classical period, literature on papyrus scrolls include the concepts that shaped Western civilisation. To understand Greek and Roman literature, we rely on the few ancient works preserved by mediaeval copyists, while most were destroyed during the Middle Ages [1]. With the discovery of the Villa of the Papyri in Herculaneum, this may change.

In 79 AD, Mount Vesuvius destroyed Herculaneum and Pompeii on the Bay of Naples. Julius Caesar’s father-in-law’s huge villa at Herculaneum was buried 20 meters deep in mud and ash. A large collection of papyrus manuscripts has been found [2]. Volcanic heat carbonizes texts. Additionally, they are maintained. Even though most ancient writings degrade and perish in air, the Villa of the Papyri library has stayed

underground for a long time. An Italian farmhand hits a marble sidewalk while drilling a well. Beautiful statues, frescoes, and scrolls were found during excavations. Overcarbonization makes them fragile. The desire to read them would quadruple our ancient literature.

Many scrolls are tragically destroyed during the initial opening. Several scrolls include Greek philosophical writings after an Italian monk methodically unrolled them over decades. Over 600 documents remain unread. Excavations were never completed, and thousands of scrolls may be buried. This ash lump may contain Roman and Greek philosophy, science, literature, mathematics, poetry, and politics, waiting to be uncovered. Using X-ray tomography and computer vision, Dr. Brent Seales’ University of Kentucky team decoded the En- Gedi scroll [3] without opening it. The scroll found in Israel’s Dead Sea region contained Leviticus chapters. This shows how to read a carbonized scroll without opening it. Since then, virtual unwrapping has grown into a successful industry [4]. The Herculaneum Papyri are harder to read because their ink is carbon-based, unlike the En-Gedi scroll’s denser inks, which prevent X-ray contrast.

**Fig. 1:** Original scroll & scroll fragments

Because they wanted to apply virtual unwrapping on the Herculaneum Papyri, Dr. Seales and his team tried a new idea. Detached papyri pieces can be read under infrared light, potentially providing ground truth data for a machine-learning algorithm to recognize ink from X-rays. To get high-resolution X-rays, the team scans two scrolls and several shards using a particle accelerator. They believe machine learning can detect subtle papyrus surface patterns that indicate carbon-based ink at 4-8 m resolution and 16 bits of density data per voxel.

Authorized licensed use limited to: ISAE. Downloaded on November 15,2026 at 20:01:30 UTC from IEEE Xplore. Restrictions apply.

Early in 2023, Dr. Seales’ lab made a significant advancement, their machine learning model successfully recognizes ink from the X-ray scans [5]. By using the scans from 2019, researchers were able to show how the Herculaneum scrolls might be virtually unwrapped, even revealing certain characters that were hidden in papyrus layers. The Herculaneum Papyri puzzle has been broken down into a software issue after 275 years, and machine learning can assist in resolving this issue.

Our research sets out to achieve the following goals in response to ink detection:

1) Preprocess the ”surface volumes” created from 3D X-ray scans. 2) Design and optimize image segmentation models for ink detection. 3) Create an ensemble of different models with superior predictive capabilities. In the subsequent sections of this paper, we provide a comprehensive review of related works in the field of ancient scrolls (Section II) and (section III) describes a detailed explanation of the research methodology. The result analysis of the proposed model is discussed in (Section IV). Finally, the paper is concluded in (Section V).

## II. LITERATURE REVIEW

The use of machine learning models to detect ink on carbonized papyrus scrolls excavated from the Roman villa library in Herculaneum provides valuable insights into ancient texts preserved in their original form for almost two millennia. Contemporary machine learning models like Unet, Deeplabv3, and Manet identify and delineate the inked regions within the flattened surface volume, revealing the textual information in these ancient artifacts. Early results show promising progress, with the validation set’s highest dice score reaching 48.44. This study [6] shows how machine learning can detect ink in 3D scans and decipher carbonized parchment. This paper [7] discusses a hieroglyph dataset for segmentation, including its pros and cons and the impact of hyperparameters on the final results. They use the Detectron2 platform, developed by the Facebook AI Research Group, to segment images using the Mask R-CNN architecture.

In this paper [8], they use Deep Convolutional Siamese- Networks to help papyrologists match new data. Images are annotated with minimal human intervention. On an 800fragment retrieval task, their from-scratch self-supervised approach outperforms knowledge transfer from a large dataset with a top-1 accuracy score of 0.73. The Digital Restoration Initiative (DRI) used a machine learning method in 2019 to reveal a Greek character on a Herculaneum papyrus fragment written in carbon ink. Virtually unwrapping cultural heritage is possible. To improve tomography’s hard-to-detect ink signals, machine and deep learning will evolve. This raises crucial questions. How does the use of AI in editing ‘true-born virtual’ texts (which cannot be opened for verification) change the process? A critical edition of a virtually unwrapped papyrus text must document the machine’s role, as shown in this paper

[9]. The article addresses the Data Science requirements for this new type of text to ensure transparency at its early stages. A humanities-science virtual edition model is needed. They [10] present a modified Fast Fourier Convolution operator for volumetric data and apply it to a segmentation architecture for ink detection on Herculaneum papyri. Deep experimental analysis confirms its suitability.

This Kaggle competition [11] features the Vesuvius Challenge - Ink Detection, which focuses on the sub-problem of detecting ink from 3D X-ray scans of papyrus fragments that became detached from some excavated scrolls. This subcontest is hosted on the Kaggle because it is a more traditional data science and machine learning problem involving the development of a model that can be validated against ground truth data. In this project, the dataset from the Kaggle competition has been used to detect ink using machine learning from Herculaneum papyri.

## III. RESEARCH METHODOLOGY

The research technique used to create and assess the precise and effective ink detection model is described in this part. The technique includes model architecture, data collection, and preprocessing of the dataset, the training procedure, and evaluation metrics. Fig. 2 summarises the overall research process.

**Fig. 2:** The flowchart of the Complete Research Process

In this research, three distinct models, i.e. U-Net, Attention U-Net, Pretrained autoencoder with Attention U-Net with three types (average, voting, weighted average) of ensembling techniques have been employed to identify and delineate the inked regions within the flattened surface volume, unraveling the hidden textual information concealed within these ancient artifacts. By experimenting with various layers and optimizing

Authorized licensed use limited to: ISAE. Downloaded on November 15,2026 at 20:01:30 UTC from IEEE Xplore. Restrictions apply.

model architectures, the research aims to achieve accurate and efficient ink detection.

### A. Dataset Explanation

Two datasets have been used to conduct this research. EduceLab Dataset (III-A1) is consisted of the fragments of ancient scroll which is the main dataset of our research and AL-PUB Dataset (III-A2) is used for pretraining autoencoder.

1) EduceLab Dataset: The dataset [5] was published by EduceLab — A Digital Restoration Initiative, University of Kentucky, Stanley and Karen Pigman College of Engineering as part of Vesuvius Challenge - Ink Detection [11] on Kaggle. This dataset consists of 4µm 3D X-Ray scans. The 3D scans are in vertical slices from side to side. (.tif) files are slices from the 3D X-Ray surface volume. Each file contains a greyscale slice in the z-direction. Each fragment contains 65 slices. Combined this image stack gives us width * height * 65 number of voxels per fragment. Two fragments are in the hidden test set, which together are roughly the same size as a single training fragment. The sample slices available to download in the test folders are simply copied from training fragment one. Other than these the dataset contains a binary mask of which pixels contain data, a binary mask of the ink vs no-ink labels and the infrared photo on which the binary mask is based. This dataset is constructed from the ancient scroll using the process of Fig. 3.

**Fig. 3:** From a fragment (a) they obtain a 3D volume (b), from which they segment a mesh (c), around which they sample a surface volume (d). they also take an infrared photo (e) of the fragment, which they align (f) with the surface volume, and then manually turn into a binary label image (g).

In our pursuit of detecting ink on carbonized ancient scrolls, we have implemented a comprehensive data processing pipeline. Image resizing, stacking slices, random location sampling and data augmentation techniques have been applied in this pipeline.

• Image Resizing: Large images share a consistent size (here shared height 4000) while preserving their original aspect ratios.

• Data Loading: These scans are stored as sequences of 2D image slices. The slices are stacked along the last dimension to form a 3D volume representation. To identify regions of interest on the scrolls, binary masks are employed. In addition to masks, label images are

employed to provide additional information about the scrolls.

• Random Location Sampling: To effectively train this machine learning model, random location sampling has been employed to select training and validation data points shown in Fig. 4. Randomization is essential to ensure that the dataset is diverse and unbiased.

• Data Augmentation: Random contrast adjustments has been applied to the training data. Data augmentation introduces diversity into the training dataset, enhancing the model’s performance when exposed to various input data variations.

**Fig. 4:** Sample of random locations with validation zone

The training dataset is constructed by repeatedly sampling random training locations. Subvolumes and corresponding labels, centered around these sampled locations, are extracted. This process is performed in combination with data augmentation techniques. Validation data is selected from areas not utilized in the training process. Test dataset is constructed using the similar process by using test images.

2) AL-PUB Dataset: All images in the AL-PUB Dataset [12] are derivatives of images owned by the University of Oxford & the Egypt Exploration Society. This dataset is used for pretraining autoencoder in this research. Images are loaded

**Fig. 5:** Samples of AL-PUB dataset of 24 Greek Letters

(1000 images from each class) and resized to a dimension of (64, 64) pixels to ensure consistency. Augmentation parameters, including rotation, width shift, height shift, shear, zoom, horizontal flip, and fill mode haven been used. To meet the desired input shape, images are expanded to possess 20 channels. This is achieved by padding with zero channels. The final step of this data preparation journey involves splitting 80% of the data for training and 20% for validation.

Authorized licensed use limited to: ISAE. Downloaded on November 15,2026 at 20:01:30 UTC from IEEE Xplore. Restrictions apply.

### B. Proposed Methodology

Three distinct models, i.e. U-Net, Attention U-Net, Pretrained autoencoder with Attention U-Net with three types (average, voting, weighted average) of ensembling techniques have been employed to identify and delineate the inked regions within the flattened surface volume, unraveling the hidden textual information concealed within these ancient artifacts. By experimenting with various layers and optimizing model architectures, the research aims to achieve accurate and efficient ink detection.

1) U-Net: The U-Net model [13] begins with an input layer configured to accept data of shape (64, 64, 20). The first half of the U-Net is for downsampling, which begins with a convolutional layer with 64 filters (output channels), each having a 3x3 kernel and a stride of 2. This layer reduces the spatial dimensions by half. Batch normalization is applied after the convolutional layer. Residual connections are set aside for later use. Two blocks with separable convolutional layers follow. Each block consists of: Activation (ReLU), separable convolutional layer with the specified number of filters (128 or 256), batch normalization, activation (ReLU), another separable convolutional layer, batch normalization, max-pooling layer with a 3x3 window and a stride of 2, residual connection is added back from the previous block. These operations are repeated for both the 128 and 256 filter blocks, downsampling the spatial dimensions further. The second half of the U-Net is for upsampling. Blocks with convolutional transpose layers (deconvolution) are used to upsample. Each block consists of: Activation (ReLU), convolutional transpose layer with the specified number of filters (256, 128, or 64), batch normalization, activation (ReLU), another convolutional transpose layer, batch normalization, upSampling2D layer, which doubles the spatial dimensions, a residual connection from the corresponding downsampling block is added back to the current block. These operations are repeated for all three filter sizes, gradually increasing the spatial dimensions. The model concludes with an output layer consisting of a single convolutional filter. This filter utilizes a 3x3 kernel and a sigmoid activation function. The purpose of this layer is to generate a per-pixel classification map, particularly useful for binary image segmentation tasks where each pixel is assigned a probability value. The model is compiled with the Adam optimizer, binary cross-entropy loss function (suitable for binary segmentation tasks), and a suite of evaluation metrics including accuracy, precision, recall, and Intersection over Union (IoU).

2) Attention U-Net: The Attention U-Net architecture is designed to address specific challenges and improve the performance of standard UNet models in image segmentation tasks. Attention UNet introduces attention gates that allow the model to selectively focus on relevant features from both the encoder and decoder pathways. Standard UNet models lack mechanisms to adaptively fuse information, potentially leading to the mixing of important and less important features. Attention gates mitigate this issue. The attention mechanism

helps the model develop a better understanding of the spatial relationships within the image.

The attention gate comprises two separate convolutional layers. One operates on the feature map from the encoder of U-Net, and the other on the feature map from the decoder of U-Net. Batch normalization is applied to the outputs of both convolutional layers, ensuring that activations are well-scaled and centered. The outputs of the two convolutional layers are element-wise summed. This step allows the model to compute attention weights based on the compatibility of features from the encoder and decoder. The summed output undergoes ReLU activation, promoting non-linear interactions and emphasizing informative regions. Finally, a sigmoid activation function is applied to the result, producing a weight map. This map determines the degree of importance assigned to each region in the decoder’s feature map. The upsampled feature map is concatenated with the attention-weighted feature map from the encoder. This concatenation combines high-level semantic information from the decoder with low-level spatial details from the encoder.

3) Pretrained Autoencoder with Attention U-Net: In this method, the utilization of a pretrained autoencoder alongside an Attention U-Net for image segmentation is employed. The motivation behind this approach arises from acknowledging the invaluable insights and feature representations that can be obtained through pretraining on a dataset of Greek letters. By merging the autoencoder’s robust feature learning abilities with the context-awareness of the Attention U-Net, the overarching aim is to significantly enhance the accuracy and effectiveness of image segmentation.

4) Ensemble Methods: Ensemble models are often used to improve the overall performance and robustness of a machine learning system by combining the predictions of multiple models. The three types of ensemble techniques (average, voting and weighted average) have been trained on three models of U-Net, Attention U-Net and Pretrained Autoencoder with Attention U-Net, using different architectures in this project. The ensemble helps capture a diverse range of information from these models.

### C. Post-processing

In this section, the image processing techniques applied to binary outputs generated during the project is described. These techniques are crucial for cleaning up and preparing the masks for subsequent analysis and visualization.

1) Connected Component Analysis: Connected component analysis is performed on the thresholded binary image. Components with an area less than this threshold are considered noise and are set to zero in the labeled image. This filtering step helps improve the quality of the segmentation shown in Fig. 6b and 6e.

2) Erosion and Dilation: These operations help remove small gaps and noise between connected components, ensuring a more accurate representation of the segmented regions. A square kernel with a size of 3x3 is used for these operations. The number of iterations can be adjusted based on the desired

Authorized licensed use limited to: ISAE. Downloaded on November 15,2026 at 20:01:30 UTC from IEEE Xplore. Restrictions apply.

**Fig. 6:** Improvement using post-processing

**Fig. 7:** Ground Truth Label Vs Predicted Labels of different models

effect. To ensure that the morphological operations did not introduce new noise or artifacts, another round of connected component analysis and size-based filtering is performed on the eroded image. The result of the image processing pipeline is a binary output that has been cleaned, filtered, and is now suitable for further analysis, visualization, or integration shown in Fig. 6.

### D. Evaluation Metrics

To evaluate the segmentation performance of ink detection models, five evaluation metrics can be used: precision, recall, accuracy, dice coefficient and Jaccard index (IoU). These assessment metrics are calculated using specific formulas [14]:

Precision measures the fraction of true positive pixels among all pixels predicted as positive.

Precision = TP TP + FP (1)

Recall measures the fraction of true positive pixels among all ground truth positive pixels.

Recall = TP TP + FN (2)

The ratio of correctly predicted instances to the total instances in a classification problem. It’s a common metric but can be misleading in imbalanced datasets.

Accuracy = TP + TN TP + TN + FN + FP (3)

Dice coefficient, also known as F1-score, measures the similarity between the predicted and ground truth segments. Dice coefficient values range from 0 to 1, with 1 indicating perfect overlap.

Dice = 2TP 2TP + FP + FN (4)

Similar to Dice coefficient, Jaccard Index, also known as IoU measures the overlap between the predicted segmentation and the ground truth segmentation. It’s calculated as

the intersection of the predicted and ground truth regions divided by their union. IoU values range from 0 to 1, with 1 indicating a perfect match between the predicted and ground truth segments.

IoU = TP TP + FP + FN (5)

where, TP occur when the model predicted the positive class. FP occur when the model anticipated a positive class when it was negative. TN occur when the model predicted the negative class. When the model anticipated a negative class when it was positive, FN occurs.

## IV. RESULT & DISCUSSION

### A. Visual Evaluation

Visual confirmation lets non-experts quickly check created images by comparing them to the ground reality. Images are assessed for approximate accuracy, memory, and noise. The development cycle often starts with model validation to assess performance. Visual inspection allows for the assessment of numerous subjective criteria that compose ”readability,” a measure that does not always match quantitative measures. Figure 7 shows how our methods compare to the ground truth. Visual representation shows that Ensemble methods, especially average and weighted average, are easy to interpret.

### B. Quantitative Evaluation

Section III-D describes the evaluation matrices used here for quantitative evaluation. After calculating the evaluation matrices on all methods, following Table I has been formed based on precision, recall, accuracy, dice coefficient and IoU.

### C. Result Analysis

Precision, recall, dice and IoU are important metrics for image segmentation because they provide insights into the model’s ability to accurately find out the object of interest (foreground) from the background. While accuracy is a common metric, it is not the most informative in imbalanced

Authorized licensed use limited to: ISAE. Downloaded on November 15,2026 at 20:01:30 UTC from IEEE Xplore. Restrictions apply.

datasets, where one class significantly outweighs the other like these fragments have more background than foreground.

**TABLE I:** Evaluation metrics of different methods

Method Name Precision Recall Accuracy Dice IoU U-Net 0.763 0.537 0.927 0.630 0.460 Attention U-Net 0.723 0.640 0.930 0.679 0.514 Pretrained Attention U-Net

0.751 0.595 0.931 0.664 0.497

Ensemble (Avg.) 0.831 0.710 0.950 0.766 0.620 Ensemble(Voting) 0.889 0.568 0.942 0.693 0.531 Ensemble (Weighted Avg.)

0.877 0.654 0.950 0.749 0.599

From Table I the result analysis is:

• U-Net: U-Net performs well in terms of precision (0.763) and accuracy (0.927), indicating that it provides mostly accurate positive predictions. However, its recall (0.537) is relatively lower, which suggests that it misses some true positive instances. The Dice coefficient (0.630) and IoU (0.460) also show reasonable segmentation performance.

• Attention U-Net: Attention U-Net has a higher recall (0.640) compared to U-Net, meaning it captures more of the actual positive instances. However, its precision (0.723) is slightly lower. The Dice coefficient (0.679) and IoU (0.514) are also improved compared to U-Net.

• Pretrained Autoencoder with Attention U-Net: This method strikes a balance between precision (0.751) and recall (0.595). It offers a good trade-off between accurately identifying positive instances and not missing too many. The Dice coefficient (0.664) and IoU (0.497) are also reasonable.

• Ensemble (Avg.): The ensemble method that averages predictions from multiple models performs exceptionally well in terms of precision (0.831), recall (0.710), Dice coefficient (0.766), and IoU (0.620). It achieves the highest accuracy (0.950) among all methods, indicating robust performance.

• Ensemble (Voting): Another ensemble approach, using a majority voting scheme, achieves high precision (0.889) but relatively low recall (0.568). This may indicate that the voting ensemble is cautious about false positives but may miss some true positive pixels.

• Ensemble (Weighted Avg.): The weighted averaging ensemble method balances precision (0.877) and recall (0.654) well, along with strong performance in Dice coefficient (0.749) and IoU (0.599). Its accuracy (0.950) matches that of the averaging ensemble. Overall, from the analysis, we can see that ensemble methods drastically improve, specifically the average and weighted average ensemble.

V. CONCLUSION We have provided techniques for identifying the carbon ink found inside scrolls from Herculaneum. We validate the method using several metrics and visual evaluation, demonstrating the accuracy of our generated images, using scroll

pieces with known ground truth. This strategy, in our opinion, offers the only viable way to use deep learning and modern image technology to interpret the intact Herculaneum scrolls. Research shows that the Ensemble technique improves outcomes compared to other approaches. Undoubtedly, there is a significant discrepancy between the findings of this study and the ultimate goal of deciphering the complete Herculaneum scrolls. Given the many pipeline improvements, there is optimism that we can collectively solve this discrepancy. Our empirical findings suggest that small pipeline improvements can improve text readability. These gradual improvements are expected to help restore the whole Herculaneum papyri and exceed existing quality and precision. This research showcases the utilization of machine learning techniques for the purpose of identifying ink presence in 3D images, with the ultimate objective of deciphering the contents of carbonized parchment.
