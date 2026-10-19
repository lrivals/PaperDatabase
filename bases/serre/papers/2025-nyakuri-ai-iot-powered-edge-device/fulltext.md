---
id: 2025-nyakuri-ai-iot-powered-edge-device
title: "AI and IoT-powered edge device optimized for crop pest and disease detection"
year: 2025
backend: grobid
---

## Abstract

and disease infestations, especially for cereal crops, leading to enormous yield losses. Consequently, innovative solutions are needed to monitor crop health from early development stages through harvesting. While various technologies, such as the Internet of Things (IoT), machine learning (ML), and artificial intelligence (AI), have been used, portable, cost-effective, and energy-efficient solutions suitable for resource-constrained environments such as edge applications in agriculture are needed. This study presents the development of a portable smart IoT device that integrates a lightweight convolutional neural network (CNN), called Tiny-LiteNet, optimized for edge applications with built-in support of model explainability. The system consists of a high-definition camera for real-time plant image acquisition, a Raspberry-Pi 5 integrated with the Tiny-LiteNet model for edge processing, and a GSM/GPRS module for cloud communication. The experimental results demonstrated that Tiny-LiteNet achieved up to 98.6% accuracy, 98.4% F1-score, 98.2% Recall, 80 ms inference time, while maintaining a compact model size of 1.2 MB with 1.48 million parameters, outperforming traditional CNN architectures such as VGGNet-16, Inception, ResNet50, DenseNet121, MobileNetv2, and EfficientNetB0 in terms of efficiency and suitability for edge computing. Additionally, the low power consumption and user-friendly design of this smart device make it a practical tool for farmers, enabling real-time pest and disease detection, promoting sustainable agriculture, and enhancing food security.

devices are capable of detecting and monitoring early signs of infestations via continuous field data collection and analysis, reducing reliance on manual inspection and optimizing resource utilization 15 . However, many existing IoT solutions depend on cloud computing, which is subjected to latency, bandwidth constraints, and connectivity limitations for smallholder farmers with limited access to reliable internet infrastructure, particularly in rural and remote areas. 16,17 . Therefore, to address these limitations, edge computing has been introduced for processing data locally on IoT devices, reducing reliance on cloud-based solutions while improving real-time responsiveness.

Artificial intelligence (AI), machine learning (ML) and the Internet of Things (IoT) have led to the development of advanced smart solutions in precision agriculture to enable real-time decision-making to control and monitor pest and disease outbreaks 18,19 . Convolutional neural networks (CNNs) have demonstrated exceptional performance in image-based processing, enabling early detection of pest and disease outbreaks and preventing their widespread across large areas 20,21 . Cloud-based satellite and drone imaging systems have further enhanced these capabilities by covering large areas and even exploring hard-to-reach zones 22,23 . Nevertheless, these technologies are expensive, computationally intensive, and necessitate advanced infrastructure development. In addition, most of these technologies rely on cloud computing and require strong internet connectivity, making them unsuitable for farmers in rural and remote areas with limited internet access 24,25 . To overcome these challenges, lightweight AI models integrated with affordable and portable edge devices are needed in precision agriculture to serve smallholder farmers.

To address these challenges, this study introduces a power-efficient portable IoT device integrated with a lightweight CNN model named Tiny-LiteNet, specifically designed for edge computing applications in precision agriculture. The system incorporates a high-definition camera for image acquisition, a Raspberry Pi 5 for ondevice processing, a GSM/GPRS module for communication, and a Tiny-LiteNet model optimized for real-time image processing at the edge, enabling real-time monitoring without reliance on strong internet connectivity. The experimental results indicated that Tiny-LiteNet model achieved an accuracy of 98.6%, a compact model size of 1.2 MB with 1.48 million parameters, outperforming traditional deep learning models such as VGGNet-16, Inception3, ResNet50, DenseNet121, EfficientNetB0, and MobileNetv2 in terms of performance efficiency. The device's low-power consumption, user-friendly design, and low dependency on strong internet connectivity make it a practical tool for smallholder farms, enabling real-time monitoring and sustainable agricultural practices.

The main contributions of this work include: (1) the development of a portable, low-power AI-IoT edge device for real-time pest and disease detection; (2) the design of an efficient lightweight CNN model "Tiny-LiteNet" suitable for deployment on resource-constrained edge devices, and (3) the demonstration of its effectiveness in smallholder farming environments with limited connectivity. This contribution provides a scalable and costeffective solution for improving crop health monitoring and advancing sustainable agriculture in Africa and other developing regions. The rest of the paper is organized as follows: Section "Related works" presents related works, Section "Methodology" describes the methodology, Section "Validation of numerical results" discusses the results, and finally, Section "Results and discussion" concludes the paper. In addition, a complete list of key abbreviations and their descriptions is provided in Table 1.

## Related works

Various studies have been conducted to identify solutions for invasive pests and disastrous diseases affecting crops. This section presents emerging technologies such as AI, ML, and IoT applied in precision agriculture, specifically for controlling crop health conditions.

IoT technology has emerged as a real-time solution for monitoring and controlling agricultural pests and diseases. In 26 , a CROPCARE system was developed for real-time crop disease control by integrating mobile vision based on MobileNetv2 with the IoT and achieved impressive results. The parallel and distributed simulation framework (PDSF) integrated with the IoT was proposed for pest monitoring in 27 . This tool employs a core graphical processing unit (GPU) to manage the number of sensors coupled to it to control and monitor crop pests, achieving 98.65% accuracy. accuracy. Furthermore, the integration of IoT devices with UAV platforms has modernized precision agriculture 28 . A smart pest detection and management method for cotton plants was developed in 29 . In his framework, motion detection sensors were used to detect pests, and an automatic targeted spray was applied via drone. However, most existing IoT solutions rely on cloud computing, which is impractical in rural areas with limited internet connectivity. The introduction of ML algorithms, specifically their subset, namely, DL, has indeed revolutionized agricultural practices by automating labour-intensive tasks, including pest and disease detection 30,31 . ML's prediction capabilities enable it to predict pest and disease outbreaks before they worsen. The work of N. Ullah et al. 32 presented DeepPestNet, a convolutional neural network model for recognizing and classifying 10 species of pest with 98.92% accuracy. Similarly, W. Albattah et al. 33 proposed an improved EfficientNetV2-B4 model by customizing the existing EfficientNet architecture, achieving average precision, recall, and accuracy values of 99.63%, 99.93%, and 99.99%, respectively. Furthermore, the study presented in 34 proposed a DL model based on the Faster R-CNN architecture integrated with a mobile application to recognize and locate pests within images, achieving an impressive accuracy of 99.0%.

Leveraging the power of unmanned aerial vehicles (UAVs), AI, and the IoT has advanced precision agriculture and precise plant health monitoring. The integration of these technologies enables real-time data collection, analysis, prediction, and informed decision-making to improve the accuracy and responsiveness of pest and disease management systems 35 . In the work presented in 36 , crop diseases and pest infestations were detected and monitored by integrating a UAV and DL based on the YOLOv5 model, obtaining remarkable results of up to 96.0% average precision, 93.0% average recall, and 95.0% mean average precision (mAP). Additionally, R. Fu 37 introduced a swarm system of drones equipped with a CNN model based on YOLOv10 to detect and geolocalize invasive pests such as Araujia sericifera and Cortaderia selloana affecting organic orange groves and achieved an F1 score of up to 80%.

Despite this remarkable achievement, most AI, ML, and IoT solutions focus on high-resource settings, leaving a gap in affordable, scalable, and energy-efficient aspects for smallholder farmers in developing regions 38,39 . This study addresses this gap by developing a portable IoT device integrated with a lightweight DL model, specifically designed for edge computing in resource-constrained agricultural environments, suitable for smallholder farmers with limited resources. A comparative summary of recent works that have used emerging technologies such as IoT, UAVs, Blockchain, 5G, and AI/ML techniques for agricultural pest and disease control is provided in Table 2 below.

## Methodology System overview

This study proposes an AI-powered IoT system for the early detection and classification of crop pests and diseases, leveraging edge computing for real-time processing. The system integrates an image acquisition unit, a deep learning-based classification model for on-device processing, and cloud-based analytics for efficient monitoring and decision-making. The workflow consists of five main stages: data collection, preprocessing, model training, deployment on an edge device, and real-time inference. The proposed system aims to provide farmers with timely and accurate information to mitigate agricultural losses.

## IoT layered architecture of the proposed edge device

The proposed edge device is structured in a layered IoT architecture designed for real-time agricultural pest and disease monitoring 49,50 . Each layer in this architecture from data acquisition to decision-making phase has specific functions, threats associated to it, security measures, and functional components as summarized in the Table 3.

As illustrated in Fig. 1, the system starts by acquiring images of plants from the field and preprocessing them for efficient analysis via the Tiny-LiteNet model. Once the pest or disease is detected, the system activates a notification system by alerting farmers on site and sending a notification message describing the plant health condition. Furthermore, the images of the detected plant health conditions are stored on the device and sent on a cloud platform when the internet is available for further analysis.

Figure 2 illustrates the proposed system architecture of the AI-powered portable edge device that integrates a high-definition camera for real-time crop image acquisition, a Raspberry Pi 5 for on-device processing, and a

## Technology Strengths Limitations

IoT 15,[40][41][42] Real-time monitoring and control, low-cost and energy-efficient sensor deployment, continuous data collection, High efficiency, and sensor network Limited battery life for remote deployment, sensor calibration complexity, limited connectivity in rural areas, and security problems UAV 23,36,43 High resolution aerial imaging, large and inaccessible farmland coverage, and rapid data acquisition susceptibility to weather condition, limited flight period, complex design, and data processing overhead Blockchain [44][45][46] Traceability, security, decentralized data acquisition and decision-making, and reliable supply chain High computational resource demand, complexity for small-scale systems, not yet widely adopted for smallholder farmers 5G

## Hardware components

The key hardware components used for the overall function of the system are as follows:

• Sensing unit: The sensing unit consists of a high-definition camera module used for image acquisition from the field and weather sensors, including humidity, temperature, and rain sensors, used for weather condition monitoring. • Processing U55nit: Data acquired from sensors are processed by Raspberry Pi 5, which is integrated with the CNN model "Tiny-LiteNet model" optimized for pest and disease image classification. • Communication unit: The processed data is communicated via the GSM/GPRS module for cloud connectivity and notification to the farmers. • Power Sour55ce: The system is powered by a solar system optimized for energy efficiency to charge an embedded lithium battery.

## Software and AI Model Development

## Dataset collection and preprocessing

To train the CNN model, we used two datasets from the PlantVillage repository and images acquired from the field, including pest and disease datasets. Both datasets were pre-processed and normalized as detailed in Tables 4 and5.

## Processing technique Details

Image

## Tiny-LiteNet Model development

As illustrated in Fig. 3, a pretrained MobileNetv2 model was used as the teacher model, from which foundational knowledge was acquired. Additionally, a student model consisting of six squeeze-and-excitation (SE) depthwise blocks to enhance feature representation, reduce computational cost, and improve model accuracy combined with a fully connected layer was added to convert the high-level feature maps into class scores for classification tasks. The overall architecture significantly reduces the computational cost of the MobileNetv2 architecture but has a relatively decreased accuracy of 1%, which does not affect the overall performance of pest and disease detection.

## Performance metrics calculation

Various performance metrics were calculated to evaluate the effectiveness of the Tiny-LiteNet model and the integrated IoT system and to determine their suitability for crop pest and disease detection.

## Accuracy (A)

The accuracy is the rate of correctly classified instances for both infected and noninfected plants.

A = (T P + T N) (T P + T N + F P + F N) (1

)

where:

• TP (true positives): The correctly identified instances (pest/disease for our case)

• TN (True Negatives): The correctly identified as no instances (not infected plant for our case)

• FP (false positives): The incorrectly identified instances (pest/disease) for our case)

• FN (False Negatives): incorrectly identified as no instances (not infected plant for our case)

## Recall (R)

The recall is the percentage of instances predicted correctly as positive (infected plants) out of all available positive instances.

## R = (T P ) (T P + F N)

(2)

## Precision (P)

The precision metric represents the rate of correctly predicted positive instances (infected plants) over all the predicted positive instances.

## P = (T P ) (T P + F P )

(3) Fig. 3. Tiny-LiteNet architecture.

## Mean average precision (mAP)

The mean average precision (mAP) represents the weighted mean of precision taken at each threshold of intersection over union (IoU), averaged across all classes.

mAP = ∑ N i=1 (Pi + Pi+1)∆Ri 2N(4)

where N denotes the number of threshold increments, Pi represents the precision at the i th IoU threshold, and ∆Ri denotes the increase in recall from the i th to the (i + 1) th IoU threshold. F1 score (F)

F = 2 * (P * R) (P * R) (5)

Algorithm 1 in Fig. 4 illustrates the pseudocode of the proposed AI-powered IoT edge system, indicating the flow of data from image acquisition to pest or disease prediction, confidence evaluation, and text-based explanations generation. The algorithm starts with capturing real-time image stream from camera and processed by the lightweight Tiny-LiteNet model on a Raspberry Pi 5 that classifies images in their respective classes, followed by the retrieval of corresponding interpretive text, enabling real-time, power-efficient, and interpretable decision support for agricultural monitoring in resource-constrained environments.

## Validation of numerical results

To ensure a reliable and generalized model, the proposed Tiny-LiteNet model was adopted to a rigorous evaluation methodology namely folded cross-validation (CV). A class-conscious fivefold cross-validation technique was used across the entire dataset, with 80% training and 20% testing subsets, ensuring equal representation of classes in each fold. Furthermore, the process was repeated five times with different data splits and the average resulting performance metrics include accuracy, recall, F1-score, and Cross Validation Accuracy (5-Fold Cross Validation Accuracy) were recorded

CV A = 1 K K ∑ i=1 Ai (6

)

where:

• a benchmarking process was conducted across various edge devices including Raspberry Pi 5, Raspberry Pi 4, Arduino Nano 33 BLE sense, Raspberry pi pico, and FPGA and measured the inference time, memory footprint, and power consumption under edge computing constraints.

## Results and discussion

This section describes the results of the research after integrating the developed AI model with a physical edge device.

## Results

Figure 5 shows the training and validation performance of the Tiny-LiteNet model over 150 epochs. In Fig. 5a, the model training and validation accuracies increase rapidly in the first 10 epochs and stabilize for the remaining epochs, with a validation accuracy of approximately 98.6%, demonstrating the excellent learning capability of the model. Additionally, as illustrated in Fig. 5b, both training and validation losses decline rapidly in the first 20 epochs, indicating the model effectiveness learning capability.

As shown in Fig. 6a, the model training and validation accuracies increase rapidly in the first 20 epochs and stabilize for the remaining epochs, with a validation accuracy of approximately 99%, indicating excellent learning capability. Similarly, as shown in Fig. 6b, both training and validation losses decrease rapidly in the first 25 epochs, indicating the model effectiveness learning ability.

Figure 7 presents two confusion matrices, each illustrating the performance of the Tiny-LiteNet model in classifying crop pests and diseases. Figure 7a shows the model for classifying corn leaf diseases, whereas Fig. 7b presents the model for classifying crop pests. The model performed exceptionally well, except for some confusion regarding Gray_leaf_spot disease and grasshopper pest.

As shown in Fig. 8a,b, the developed Tiny-LiteNet model effectively predicts and classifies images with high accuracy. This includes images of plant health conditions, such as maize crop pests, diseases, and fruit pests. In addition, the prediction labels indicate a high degree of precision, highlighting the model's robustness across various image processing tasks. Furthermore, after classification, a description is added, summarizing image information and suggesting control measures to facilitate decision-making.

To validate the effectiveness of the developed model, we trained and compared seven traditional CNN models, including VGGNet-16, Inception3, RasNet, DenseNet, EfficientNetB0, and MobileNetv2. As presented in Table 6, the results demonstrated that our model (Tiny-LiteNet) outperforms other models in terms of model size, number of parameters, and inference time, with relative accuracy.

Figure 9 illustrates the accuracy, storage efficiency, and responsiveness trade-offs across eight CNN models, highlighting the effectiveness of Tiny-LiteNet for resource-constrained deployments.

## Comparative benchmarking of the edge devices' performance

To select a suitable edge device with optimal performance to run the Tiny-LileNet model, comprehensive benchmarking was conducted across six edge platforms capable of running lightweight CNN models. The performance evaluation focused on latency, power consumption, memory usage, and deployment feasibility for the Tiny-LiteNet model, as presented in Table 7.

The performance analysis results demonstrate that while popular platforms such as Raspberry pi Pico, Arduino Nano 33 BLE sense, and ESP32-CAM are not capable of running the Tiny-LiteNet model, Raspberry Pi 5 uniquely balances high accuracy (98.6%), low latency (16 ms), and reasonable cost ($80), making it the most suitable platform for deploying Tiny-LiteNet in resource-constrained agricultural environments. Additionally, compared with Raspberry pi 5, Raspberry pi 4 has high latency, whereas FPGA, despite its efficiency, has a complex HDL design and high cost, making it a less practical alternative.

As illustrated in Fig. 10, the proposed portable edge device for crop pest and disease detection was implemented and enclosed in a white cover. Subfigure (a) depicts the front view, highlighting the integrated screen for user interaction and results visualization. Subfigure (b) shows the back side, indicating the camera lens for image acquisition and accessible ports along the upper edge side for programming, power, switching, and LED status indication. While subfigure (c) provides an internal view, illustrating the device's component layout and connectivity."

## Discussion

The results demonstrate that the integration of the Tiny-LiteNet model with a Raspberry Pi 5 offers a high performing, lightweight, and efficient solution for detecting and classifying cereal crop pests and diseases. In addition, the proposed system offers an explainability option for farmers, describing the class of a pest or diseases, its effects on plants as well as the control strategies to mitigate risks. The model exhibits exceptional performance accuracy of 98.6%, 98.4% F1-score, and 98.2% recall which are comparable to or exceeding many state-of-the-art deep learning models, including VGG-16, Inception3, ResNet50, DenseNet121, EfficientNetB0, and MobileNetv2 trained on the same dataset. However, what distinguishes Tiny-LiteNet is its compact design (0.72 MB), which ensures fast inference speed, low computational overhead, and compatibility with edge computing platforms, all while maintaining robust predictive capabilities. The incorporation of six squeeze-and-excitation (SE) blocks improves feature extraction and enhances classification performance across diverse pest and disease images. This design choice improves the model's ability to distinguish subtle differences in pest and disease image features across varied backgrounds, lighting conditions, and growth stages, thus increasing its generalization performance. Furthermore, real-time data communication via GSM/GPRS enables remote monitoring and sends notifications to farmers, indicating pest and disease conditions. The system's edge computing capability, portability, and low power consumption make it suitable for smallholder farmers with limited resources.

To evaluate the performance of the proposed system in comparison with recent studies on similar tasks, Table 8 provides a comprehensive analysis of state-of-the-art CNN-based and hybrid deep learning models used for similar tasks in agriculture.

While models such as ResNet50, MobileNetV3 Large, and CNN + ViT achieve higher or comparable accuracies, their large model sizes (often > 100 MB) and high processing demands limit their practicality for edge deployment. In contrast, Tiny-LiteNet combines high performance with minimal resource requirements, positioning it as a more suitable choice for real-time, field-deployable applications. This comparison highlights that Tiny-LiteNet offers a viable solution across accuracy, generalization, model size, and deployment flexibility. Furthermore, the proposed system's ability to run effectively on edge devices like Raspberry Pi 5, integrated with its explainable AI support and fast response time, makes it exclusively suitable for resource-constrained agricultural environments.

## Conclusion

This study presents the design and implementation of a lightweight and power efficient AI-powered IoT edge system optimized for real-time crop pest and disease detection in resource-constrained agricultural environments. The developed system integrates a new lightweight convolutional neural network architecture, namely, "Tiny-LiteNet", optimized for edge deployment with built-in support of model explainability. The experimental evaluation shows that the proposed model achieves a high accuracy of 98.6% accuracy, 98.4% F1-score, 98.2% Recall, 80 ms inference time, a compact model size of 1.2 MB with 1.48 million parameters, outperforming several state-of-the-art CNN models, including VGGNet-16, Inception3, ResNet50, DenseNet121, EfficientNetB0, and MobileNetv2. Additionally, the developed lightweight IoT-Edge device processes data locally without relying on internet connectivity, while maintaining low power consumption and portability, making it suitable for resource-constrained deployment. The system is currently limited on rule-based and relies on preprogrammed expert knowledge for textual output rather than being dynamically generated by a language model, due to the memory and computational restrictions of edge devices. Future work will focus on enhancing the model's ability to generate automatic textual descriptions of plant health conditions by incorporating a large language model (LLM). We also aim to further reduce the system's power consumption for extended field deployment using battery-powered configurations.

## Measurement

Zhang et al. 51 Gookyi et al. 52 Jawadul et al. 53 Wang et al. 54 Zeng et al. 55 Amin et al 40

## Figures et tableaux

[figure sans légende identifiée] GSM/GPRS module for cloud communication. In addition, it integrates Tiny-LiteNet, a lightweight CNN model based on MobileNetV2, optimized for edge deployment, specifically for crop pest and disease detection.

**Fig. 1.** The flowchart of the system.

**Fig. 2.** Overall system architecture.

**Fig. 4.** Pseudocode of the AI-powered IoT edge system with Tiny-LiteNet and text-based explainability.

**Fig. 5.** Plots (a) and (b) illustrate the model's performance accuracies and losses, respectively, across the pest dataset over 150 epochs.

**Fig. 7.** Confusion matrices for crop disease (a) and (b) crop pests.

**Fig. 6.** Plots (a) and (b) illustrate the model's performance accuracies and losses, respectively, across the disease dataset over 150 epochs.

**Fig. 8.** Prediction results for (a) crop pest and (b) crop disease classification tasks with descriptions.

**Fig. 10.** The physical implementation of the IoT device where the figure in (a) illustrates the front side and the figure in (b) shows the back side of the device, whereas the figure in (c) presents the internal parts.

**Table 1.** Nomenclature.

    Abbreviations Full form | Description
    IoT | Internet of Things | Network of interconnected devices
    UAV | Unmanned Aerial Vehicle | Aerial drone technology
    AI | Artificial Intelligence | Simulates human intelligence in machines
    ML | Machine Learning | Data-driven prediction
    CNN | Convolutional Neural Network Deep learning model for image tasks
    Tiny-LiteNet | Lightweight (Custom Model) | CNN model for pests
    GSM | Global System for Mobile | Mobile communication standard
    GPRS | General Packet Radio Service | Mobile internet data service
    IPM | Integrated Pest Management | Traditional pest control strategy
    LLM | Large Language Model | Advanced AI for language tasks
    RPi | Raspberry Pi | Compact, affordable single-board computer

**Table 2.** Summary

**Table 3.** Architectural IoT layers with functions, security threats, and countermeasures of the proposed system.

**Table 5.** Image preprocessing and dataset augmentation details. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Dataset | No. of images | No. of classes | Source
    Crop pest | 12,400 | 5 | Plant village, field image collection
    Crop disease | 10,700 | 4 | Plant village, field image collection

of images No. of classes Source

    Crop pest | 12,400 | 5 | Plant village, field image collection
    Crop disease 10,700 | 4 | Plant village, field image collection

**Table 4.** Dataset description. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Processing technique | Details
    Image resizing | 224 × 224 pixels
    Width and height shifts | Up to 0–30%
    Shear | Up to 30%
    Zoom | Up to 30%
    Brightness adjustments | [0.8, 1.2]
    Horizontal flips | Applied randomly
    Fill mode | Nearest
    Dataset splitting | 70% training, 15% validation, 15% testing

**Table 7.** Comparative benchmarking of edge devices for Tiny-LiteNet deployment.

    Model name | Accuracy (%) F1- |  |  |  |  | 
     |  |  | Power |  | Inference |  | 
     |  |  | requirement |  | time |  | Cost
    Device |  | Processor | (W) | RAM | (ms) | Memory usage | (USD) Tiny-LiteNet Compatibility
    Raspberry pi 5 (RPi 5) BCM2712 (A76, 2.4 GHz) 4.7 | 8 GB | 16 ± 2 | 570 MB | 80 | Fully compatible ☑
    Raspberry pi 4 (RPi 4) BCM2711 (A72, 1.5 GHz) 4.5 | 4 GB | 32 ± 4 | 472 MB | 60 | 2 × Slower that RPi 5 ⚠
    FPGA |  | Custom HDL (Artix-7) | 3 | Depends on BRAM | 4 ± 1.2 | HDL-dependent 150 | Verry Complex/Requires HLS redesign ⚠
    Raspberry pi pico | RP2040 (M0 + , 133 MHz) 3.7 | 256 KB | N/A | N/A | 20 | Cannot support CNN model ⨉
    Arduino Nano 33 BLE sense | Cortex-M4F (64 MHz) | 3.3 | 200 KB | N/A | N/A | 50 | Cannot handle Tiny-LiteNet model ⨉
    ESP32-CAM | Xtensa LX6 (160 MHz) | 3.3 | 500 KB | N/A | N/A | 5 | Cannot handle Tiny-LiteNet model ⨉

score (%) Recall/ sensitivity (%) Size (MB) Parameter (million) 5-Fold Cross Validation Accuracy Inference Time (ms)

    VGGNet-16 | 98.7 | 97.2 | 97.2 | 129.1 | 81 | 98.4% | 74
    Inception3 | 98.8 | 98.4 | 98.6 | 93 | 85.2 | 98.6% | 59
    RasNet50 | 98.5 | 98.0 | 98.0 | 96 | 24 | 98% | 61
    DenseNet121 98.9 | 98.8 | 98.8 | 84 | 27 | 98.8% | 45
    EfficientNetB0 98.3 | 97.8 | 98 | 9 | 4.2 | 98.1% | 23
    MobileNetv2 | 98.7 | 98.1 | 98.0 | 7 | 3.5 | 98.5 | 21
    Tiny-LiteNet | 98.6 | 98.4 | 98.2 | 1.2 | 1.48 | 98.5% | 16

**Table 6.** Comparison of the Tiny-LiteNet model with traditional models. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Model name | Accuracy (%) | F1-score (%) | Recall/ sensitivity (%) | Size (MB) | Parameter (million) | 5-Fold Cross Validation Accuracy | Inference Time (ms)
    VGGNet-16 | 98.7 | 97.2 | 97.2 | 129.1 | 81 | 98.4% | 74
    Inception3 | 98.8 | 98.4 | 98.6 | 93 | 85.2 | 98.6% | 59
    RasNet50 | 98.5 | 98.0 | 98.0 | 96 | 24 | 98% | 61
    DenseNet121 | 98.9 | 98.8 | 98.8 | 84 | 27 | 98.8% | 45
    EfficientNetB0 | 98.3 | 97.8 | 98 | 9 | 4.2 | 98.1% | 23
    MobileNetv2 | 98.7 | 98.1 | 98.0 | 7 | 3.5 | 98.5 | 21
    Tiny-LiteNet | 98.6 | 98.4 | 98.2 | 1.2 | 1.48 | 98.5% | 16

Proposed model

    Model | MobileNetv2 | Custom-CNN | MobileNetv3 Large BerryNet-Lite CNN + ViT | ResNet50 | Tiny-LiteNet
    Accuracy | 98.14% | 94.60% | 99.66% | 99.45% | 98.17% | 99.8% | 98.6%
    Recall | 97% | 93% | 99.42% | 97.96% | 91.98% | 99.92% | 98.2%
    F1-Score | 97.1% | 93% | 99.42% | 96.90% | - | 99.91% | 98.4%
    Model Size | 8.97 MB | 0.72 MB | > 16 MB | - | > 100 MB | > 100 MB | 0.72 MB
    Suitability for Edge application YES | YES | YES | YES | YES | YES | YES
    Edge Computing | YES | YES | YES | NO | YES | NO | YES
    Explainability | NO | NO | YES | YES | NO | NO | YES

**Table 8.** Pest and disease detection comparison of the proposed system with the recent studies. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Measurement | Zhang et al.51 | Gookyi et al.52 | Jawadul et al.53 | Wang et al.54 | Zeng et al.55 | Amin et al40 | Proposed model
    Model | MobileNetv2 | Custom-CNN | MobileNetv3 Large | BerryNet-Lite | CNN + ViT | ResNet50 | Tiny-LiteNet
    Accuracy | 98.14% | 94.60% | 99.66% | 99.45% | 98.17% | 99.8% | 98.6%
    Recall | 97% | 93% | 99.42% | 97.96% | 91.98% | 99.92% | 98.2%
    F1-Score | 97.1% | 93% | 99.42% | 96.90% | - | 99.91% | 98.4%
    Model Size | 8.97 MB | 0.72 MB | > 16 MB | - | > 100 MB | > 100 MB | 0.72 MB
    Suitability for Edge application | YES | YES | YES | YES | YES | YES | YES
    Edge Computing | YES | YES | YES | NO | YES | NO | YES
    Explainability | NO | NO | YES | YES | NO | NO | YES
