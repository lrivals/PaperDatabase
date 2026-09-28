---
id: arxiv-2504.11967-securing-skies-comprehensive-survey-anti
title: "Securing the Skies: A Comprehensive Survey on Anti-UAV Methods, Benchmarking, and Future Directions"
year: 2025
backend: grobid
---

## Abstract

Unmanned Aerial Vehicles (UAVs) are indispensable for infrastructure inspection, surveillance, and related tasks, yet they also introduce critical security challenges. This survey provides a wide-ranging examination of the anti-UAV domain, centering on three core objectives-classification, detection, and tracking-while detailing emerging methodologies such as diffusion-based data synthesis, multi-modal fusion, vision-language modeling, self-supervised learning, and reinforcement learning. We systematically evaluate state-of-the-art solutions across both single-modality and multi-sensor pipelines (spanning RGB, infrared, audio, radar, and RF) and discuss large-scale as well as adversarially oriented benchmarks. Our analysis reveals persistent gaps in real-time performance, stealth detection, and swarm-based scenarios, underscoring pressing needs for robust, adaptive anti-UAV systems. By highlighting open research directions, we aim to foster innovation and guide the development of next-generation defense strategies in an era marked by the extensive use of UAVs.

## 1. Introduction

Unmanned Aerial Vehicles (UAVs) have expanding roles in civilian and military domains, offering benefits for infrastructure inspection, reconnaissance, and surveillance. Yet their rapid proliferation also introduces serious security threats, including unauthorized entry into restricted airspace and covert data gathering. As low-cost, agile drones become more prevalent, the need for robust counter-UAV (anti-UAV) technologies that can detect, track, and neutralize hostile UAVs grows increasingly urgent. RGB [167], 2). Thermal [54]; 3). RGB + Thermal [157]; 4). RGB + Audio + Radar + LiDAR [160].

Scope & Motivation. This survey provides a comprehensive overview of current anti-UAV research, focusing on three key objectives: classification (Section 3), detection (Section 4), and tracking (Section 5). We underscore the importance of leveraging multi-modal data-encompassing RGB, infrared (IR), radar, RF, and audio-to address smallobject detection, erratic flight trajectories, and adversarial tactics. Figure 2 illustrates five primary research thrusts that drive modern anti-UAV innovations: (i) diffusion-based data synthesis and domain adaptation, (ii) vision-language modeling, (iii) self-supervised and unsupervised learning, (iv) multi-modal fusion, and (v) reinforcement learning. Datasets & Benchmarking. The advancement of anti-UAV systems crucially depends on high-quality, large-scale datasets. Section 2 reviews pivotal benchmarks-including DroneRF, Halmstad Drone, and Anti-UAV-detailing their annotation fidelity, sampling rates, and environmental diversity. We also highlight the pressing need for more specialized datasets to cover scenarios such as night-time op-Table 1. Statistical Comparison of Public UAV Datasets. "Seq." = number of sequences, "Frame" = number of frames, "T-Type" = target types, "S-Type" = scenario types. "Modality": RGB, IR, Audio (A), Radar (RA), LiDAR (L), RF. "Task": Classification (C), Detection (D), Tracking (T). "Annotation": class, mask, bbox, centroid, 3D coords (3D coordinates), or trajectory. Emerging Techniques & Future Directions. Section 6 spotlights key emerging paradigms-such as diffusiondriven augmentation, vision-language integration, selfsupervised learning, advanced multi-modal fusion, and reinforcement learning for real-time control-and discusses their tremendous potential to reshape anti-UAV capabilities.

Ultimately, these methods aim to enable adaptable, realtime systems equipped to handle evolving threats through domain adaptation, robust sensor integration, and rapid policy updates. Section 6 concludes with a forward-looking perspective on next-generation anti-UAV solutions, outlining how these emerging methodologies can drive future research and industrial innovation. and USC Drone [92,142] provided core RGB datasets for aerial detection and tracking. Beyond the visual domain, DroneRF [8] captures electromagnetic signatures for RF-based UAV classification, while DroneAudio [2] and Acoustic-UAV [21] focus on acoustic features. More recent efforts extend coverage to multi-modal data: Halmstad Drone [124,125] fuses RGB, IR, and audio, and MMAUD [160] integrates radar and LiDAR. Communitydriven competitions (e.g., the 2nd and 3rd Anti-UAV Workshops [166,168] and the 4th Anti-UAV Challenge [93]) feature adversarial or cluttered scenarios that reflect realworld operational complexity, while UAVSwarm [137] and mDrone [169] emphasize large-scale swarm coordination or low-visibility tracking-both highlighting the need for robust multi-sensor fusion [106].

## 2. UAV Datasets & Benchmarking

Complex Scenes & Modalities. Recent datasets target increasingly demanding environments and more granular annotations. For instance, Anti-UAV600 [175] and Anti-UAV410 [54] rely on infrared or thermal imaging to capture nighttime or harsh weather conditions, while Drone- vs-Bird [30] focuses on distinguishing UAVs from visually similar wildlife. Other repositories (e.g., Midgard [135] and Rosner [106]) explore indoor or GPS-denied settings, alongside multi-view or re-identification tasks [11,62]. Simultaneously, annotations have expanded from bounding boxes to 3D coordinates and comprehensive trajectory information [160], aligning with the growing complexity of interception and multi-UAV maneuvers.

Trends & Open Challenges. Despite notable advances in dataset scope, several gaps persist. Collections like MMAUD [160] and Halmstad Drone [125] require precise sensor calibration and synchronization, yet standardized fusion protocols remain limited. While UAVSwarm [137] includes up to 23 drones, testing on larger fleets (50+) remains uncommon, constraining research on scaled cooperative tracking and interception. Moreover, stealth or jamming scenarios-emerging as key topics in anti-UAV forums [93,166,168]-are still sparsely represented in open-source datasets. High-resolution streams (e.g., Det-Fly [170] and AOT [10]) also challenge onboard systems in terms of storage and processing, prompting further research into compression and hardware acceleration [10,11].

## 3. UAV Classification Approaches

Table 2 synthesizes representative UAV classification methods covering radio frequency (RF), audio, radar, vision, and LiDAR modalities. These methods range from simple drone-presence detection [91] to more nuanced classifica- RA CNN + LSTM mDrone [169] Exploits Doppler signals from propellers for real-time detection and 3D tracking at 10 Hz. Achieves ≈9 cm localization error, outperforming five classic radar baselines (e.g., 3D MUSIC) by ≈66% in accuracy.

### Vision-Based

### Seidaliyeva et al. (2020) [114] RGB Background subtraction + MobileNetV2

Drone-vs-Bird [30], BirdDetection [158] Combines Drone-vs-Bird with a bird dataset to enhance UAV-vs-bird discrimination. Reached 0.56 F1 at IoU=0.5 (9 FPS). Performance is improved upon by works using more advanced YOLO variants (e.g., [32]).

### Dadboud et al. (2021) [32] RGB

YOLOv5x (PANet neck, mosaic augment) Det-Fly [170], Dronevs-Bird [30] Combined Drone-vs-Bird + Det-Fly, achieving 0.98 mAP@0.5 with 0.96 recall. Improves upon [114] on Drone-vs-Bird, though different training splits limit exact comparison.

### Sangam et al. (2023) [112] RGB CSPDarkNet-53 + VideoSwin

### FL-Drones

[107], NPS-Drones [72], AOT [10] On FL-Drones: 0.89 precision, 0.85 recall, 0.87 F1, 0.84 AP@0.5. On NPS-Drones: 0.94 precision, 0.92 recall, 0.93 F1, 0.93 AP@0.5. On AOT: 0.85 precision, 0.76 recall, 0.80 F1, 0.82 AP@0.5. Comparable to Rebbapragada et al. [102] under similar setups.

### Tu et al. (2024) [132]

RGB YOLOv8 + FCM + FMM DUT Anti-UAV [167] AP@0.5=0.913, AP@0.5:0.95=0.612, below the best YOLO-based methods on this dataset (e.g., [56]) but highlights a lightweight, efficient design.

### Cheng et al. (2024) [26]

RGB YOLOv5s + LGFFM DUT Anti-UAV [167] mAP@0.5=0.943. Improves the recall rate of 2.96% and the precision of 1.41% compared with YOLOv5s. Slightly outperforms [132] on the same benchmark. Low-complexity approach with 4.4 ms/frame inference.

### Bo et al. (2024) [16] RGB

YOLOv7-tiny + Inception-NeXt + SPPFCSPC-SR + "Get-and-Send" DUT Anti-UAV [167] mAP@0.5=0.932 at 104 FPS. Balances fast inference and high accuracy, though slightly lower mAP@0.5 than [26] and [56].

### Elsayed et al. (2024) [41]

RGB YOLOv6 + LERFNet + large-kernel LAM DUT Anti-UAV [167] mAP@0.5=0.936, with 0.953 precision. Surpasses [16] in accuracy, albeit at presumably higher resource use than the YOLOv7-tiny approach.

### Huang et al. (2024) [56]

RGB YOLOv8 + ghost conv + EMA + DCNv2

Det-Fly [170], DUT Anti-UAV [167] On DUT Anti-UAV, yields 0.971 mAP@0.5, highest among YOLO-based reports here ( [16,26,41,132]). On Det-Fly, obtains 0.934 mAP@0.5.

### Sun et al. (2024) [122] IR

YOLOv8 w/ triple-input, BiFormer attention, smallobject layer

Abbrev.: UAV = Unmanned Aerial Vehicle, CNN = Convolutional Neural Network, PSD = Power Spectral Density, LSTM = Long Short-Term Memory, DNN = Deep Neural Network, RNN = Recurrent Neural Network, YOLO = You Only Look Once, FMM = Feature Modeling Module, FCM = Feature Capture Module, LGFFM = Local-Global Feature Focusing Module, EMA = Efficient Multi-scale Attention, DCNv2 = Deformable Convolution v2, CSDE = Cross Stage Detail Enhance, CSP-PMSA = Cross Stage Partial, Partial Multi-scale, DERS = Detail Enhanced Rep Shared, MCJT = Multi-Consistency Joint Tracker, RMCM = Robust Motion Constraint Module, FSRM = Flexible Spatial Remapping Module, ATUS = Adaptive Template Update Strategy, MFCC = Mel Frequency Cepstrum Coefficient, RCNN = Region-based CNN, FPN = Feature Pyramid Network, SWIN = Shifted Window Transformer, DETR = Detection Transformer, OEN = Object Enhancement Net, IR = Infrared, LiDAR = L F1 = harmonic mean of precision & recall, mAP@0.5 = mean Average Precision at 0.5 IoU, mAP@0.5:0.95 = mean Average Precision at IoU in [0.5:0.95], AP@0.5 = Average Precision at 0.5 IoU, SOTA = state-of-the-art, RA = Radar.

Hui [58], Anti-UAV [61], Anti-UAV410 [54] On Hui dataset: 0.943 mAP@0.5 at 72 FPS. Generalizes well to Anti-UAV (0.948 mAP@0.5) and Anti-UAV410 (0.927 mAP@0.5). Demonstrates strong IR-based detection across multiple IR benchmarks.

### Wisniewski et al. (2024) [145]

RGB Faster R-CNN MAV-VID [104], Anti-UAV [61], Drone-vs-Bird [30] AP@0.5=0.970 on MAV-VID, AP@0.5=0.498 on Drone-vs-Bird, AP@0.5=0.678 on Anti-UAV.

### Zhou et al. (2024) [173]

RGB YOLOv8 + multi-scale spatial attention + HDC Det-Fly [170] Achieved 0.815 precision, 0.849 recall. Gains of +0.05 precision/+0.06 recall relative to YOLOv8 baseline. Lags behind [56] and [49] in absolute mAP on Det-Fly, but emphasizes robust small-object detection.

### Rebbapragada et al. (2024) [102]

RGB SWIN + DETR + OEN FL-Drones [107], NPS-Drones [72], AOT [10] Matches Sangam et al. [112] in precision/recall/AP@0.5 = 0.89/0.85/0.84 on FL-Drones and 0.94/0.92/0.93 on NPS-Drones with a transformer-based pipeline. On AOT dataset, obtains 0.85 precision, 0.76 recall, AP@0.5=0.82 comparable to [112]. [49] RGB YOLOv8 w/ CSDE, CSP-PMSA, OmniKernel, DERS head Det-Fly [170], MOT-Fly [29] On MOT-Fly, hits mAP@0.5=0.949 with only 1.13M parameters. On Det-Fly, achieves 0.964 mAP@0.5-slightly exceeding [56] at 0.934, though using different training splits. [144]. Other studies address issues of small object size and motion blur, incorporating advanced detectors or domain adaptation [113,134]. While performance in controlled scenarios is high, vision-based methods degrade under extreme illumination, adverse weather, or dense clutter [18,34].

### Hao et al. (2025)

### Multi-Modal

(5) Multi-Modal Recognition. Integrating multiple sensors (e.g., RF+Audio [46], Radar+LiDAR+Vision [160],

or Audio+Vision [151]) can mitigate single-sensor blind spots. Deng et al. [33] fused fisheye RGB, radar, and Li-DAR data from MMAUD, reaching 81.36% accuracy on a 4-class task, while Xiao et al. [151] combined audio and RGB streams to achieve 99.3% accuracy and sub-meter pose errors. Although multi-modal setups improve robustness, they also require careful calibration, synchronization, and greater computational resources [136,160]. Key Insights & Challenges. Across these approaches [18,34,134,136,170], each modality faces inherent constraints:

(1) RF-based solutions excel at flight-mode or type identification [3,9], but radio congestion and potential adversarial attacks are critical hurdles [40,136]. (2) Audio-based meth-ods achieve high accuracy in controlled settings yet suffer from significant performance drops in high-noise or windy environments [2,14,60]. (3) Radar-based pipelines bypass visual occlusions but incur higher costs and calibration demands [85,136]. (4) Vision-based approaches generally provide fine-grained recognition but degrade with lighting or weather changes [134,143]. ( 5) Multi-modal fusion can mitigate single-sensor weaknesses and reduce false positives [33,46] yet raises complexity in real-time deployment [160]. Additionally, adversarial robustness remains an open problem, particularly where sensors or neural networks may be fooled by spoofing or deceptive signals [64,84]. A continuing research direction involves efficient, low-latency architectures [136,152] that can handle on-board or edgebased processing for rapid UAV detection and classification.

## 4. UAV Detection Approaches

Table 3 summarizes UAV detection pipelines spanning radar, vision, and multi-modal solutions. Each modality addresses distinct obstacles-such as small object size, cluttered environments, and adverse weather-offering unique advantages and trade-offs. Although direct numerical comparisons are challenging due to varying datasets and evaluation protocols, these methods collectively illustrate emerging trends in detection algorithms and system design. We discuss salient insights from the literature below.

(1) Radar-Based Detection. Radar methods detect UAVs by exploiting micro-Doppler signatures, providing resilience under low-visibility or harsh weather conditions [136,169]. For instance, Zhao et al. [169] achieved decimeter-level localization at 10 Hz by combining CNNs with LSTMs, outperforming conventional radar baselines. However, radar sensors can suffer from interference and clutter, particularly in urban areas or heavily congested electromagnetic environments [147].

(2) Vision-Based Detection. Vision-based techniques remain widely adopted, benefiting from readily available cameras and sophisticated CNN-based detectors [128,174].

Early work centered on region-based methods [103] and YOLO architectures [17,139], gradually evolving into more lightweight or attention-oriented variants [26,49,56]. While mosaic augmentation and specialized modules can improve small-object detection [26,32], vision-based approaches remain vulnerable to occlusions, clutter, and extreme distances. Researchers have thus explored thermal and infrared (IR) imaging [89,122] or speed-accuracy trade-offs for real-time embedded scenarios [16,41].

(3) Multi-Modal Fusion. Single-modality approaches often fail under suboptimal conditions-low-visibility (vision), interference (radar), or noise (audio) [2,133]. Consequently, multi-modal fusion has gained traction as a means of leveraging complementary sensor data [12,124]. Svanström et al. [124] showed that augmenting YOLO- Ref Anti-UAV [61] SiamAD with CSAM/CAM + hierarchical discriminator + YOLOv5. 88.4% DP @ 37.1 FPS. Improved long-term IR tracking. based RGB or thermal imaging with audio features increased F1 scores and reduced false alarms. Similarly, Wu et al. [147] fused radar and RGB streams via attention-based spatiotemporal networks to improve occlusion handling. Practical adoption, however, demands meticulous sensor synchronization, balanced hardware costs, robust computational efficiency, and real-time data association [102]. Key Insights & Challenges. From prior work [128,136,174], several recurring themes emerge. 1) Small UAV Detection: Limited pixel coverage and subtle micro-Doppler signatures complicate detection [20,50,81], prompting multi-scale feature extraction, deformable convolutions, and transformer backbones [26,56,128]. Ensuring realtime operation at high accuracy remains challenging [136,139]. 2) Environmental Factors: Ambient noise (audio), lighting (vision), and radio interference (radar) degrade performance [2,117,133,169], highlighting the need for advanced clutter suppression and robust sensor hardware. 3) Generalization vs. Specialization: YOLO-based models offer generalizable frameworks [26,32,49], but specialized domains (e.g., stealth UAVs) may require niche architectures or domain-adaptive strategies [16,147]. 4) Multi-Modal Fusion: Complementary sensors effectively reduce false positives and enhance accuracy [124,147], although issues like sensor alignment, real-time latency, and hardware cost must be resolved [12,102]. 5) Benchmarking & Deployment: Heterogeneous data sources, labeling formats, and test conditions [38,97,174] complicate standard-ized evaluations. Though laboratory demonstrations show promise, real-time performance in crowded outdoor settings remains largely underexplored [42,45]. Overcoming these challenges will be crucial for field-ready anti-UAV systems. [138] integrated YOLOX [47] with Swin Transformer [81] and ByteTrack, achieving 78.2% accuracy on UAVSwarm [137]. Deng et al. [33] combined YOLOv9 [140] and EfficientNet-B7 [127] with LSTM/Kalman filtering for 3D tracking, earning top-ranked pose MSE on MMAUD [160] and winning the UG2+ Challenge [94].

Abbrev.: UAV = Unmanned Aerial Vehicle, CNN = Convolutional Neural Network, RNN = Recurrent Neural Network, SVM = Support Vector Machine, DNN = Deep Neural Network, LSTM = Long Short-Term Memory, GMM = Gaussian Mixture Model, IR = Infrared, TIR = Thermal Infrared, ID = Identification, Radar = RA, LiDAR = L, SOTA = State of the Art, YOLO = You Only Look Once, YOLOX = You Only Look Once Extended, DFSC = Dual-Flow Semantic Consistency, LoFTR = Detector-Free Local Feature Matching with Transformers, SiamRPN++ = Siamese Region Proposal Network++, SiamSTA = Siamese Spatio-Temporal Attention tracker, SiamSRT = Siamese Search Region-free Tracker, SiamDT = Siamese Dual-semantic Tracker, SiamFusion = Siamese Modality-Fusion Tracker, DCF = Discriminative Correlation Filter, CDCF = Change Detection-based Correlation Filter, CFRM = Channel Feature Refinement Module, BYTE = Bounding-box Embedding Tracker with Association, STG-RPN = Spatio-Temporal Guided Region Proposal Network, ID-RCNN = Instance Discrimination Region-based CNN, FPS = Frames Per Second, Acc = Accuracy, F1 = F1 Score, TLD = Tracking-Learning-Detection, DFSC = Dual-Flow Semantic Consistency, ATUS = Adaptive Template Updating Strategy, EECF = Eagle-Eye Correlation Filter, ECA = Efficient Channel Attention, STFTrack = Spatio-Temporal Focused Tracker, CAM = Channel Attention Module, MCJT = Multi-Consistency Joint Tracker, α-IoU = Alpha Intersection over Union, Swin = Shifted Window Transformer, MSE = Mean Squared Error, SPLT = Self-paced Learning Tracker.

Huang et al. (2024) [53] IR SiamSRT + C-C RPN + S-L RCNN + TMB + SCFD Anti-UAV [61] Achieved 71.64 and 80.04 scores on Anti-UAV testing and validation sets. Global Siamese tracker using Swin-T + consistency modules (TMB + SCFD). Avoided template degradation; outperformed multiple SOTA trackers. Huang et al. (2024) UAV410 dataset. Proposed SiamDT with dual semantic reasoning + background suppression. Achieved 68.19 and 71.65 scores on its testing and validation sets. Hybrid (Detection + Siamese) Trackers Cheng et al. (2022)

## 5. Anti-UAV Tracking Approaches

(2) Siamese (Contrastive) Trackers. Siamese trackers excel in learning robust feature similarities and handling fast or evasive UAV motion. Huang et al. [52] claimed firstplace in the 1st and 2nd Anti-UAV Challenges [61,166] with SiamSTA, which incorporates sophisticated spatiotemporal attention and motion estimation. Li et al. [75] augmented SuperDiMP with a dual-branch IR fusion strategy, boosting precision by 4.52% in the 2nd Anti-UAV Challenge. Chen et al. [22] further enhanced SiamSTA with CDCF and a multi-stage re-detection mechanism, excelling against small, fast UAVs. Beyond single-modality, Zhang et al. [165]'s SiamFusion seamlessly integrated RGB and IR streams for a 63.37 score on Anti-UAV, illustrating the tangible value of complementary sensor modalities.

(3) Hybrid (Detection + Siamese) Trackers. Hybrid methods combine detection pipelines with Siamese matching, capitalizing on each paradigm's respective strengths. Cheng et al. [25] introduced SiamAD, a synthesis of YOLOv5, multi-hybrid attention modules, and SiamRPN++, achieving 88.4% detection precision at 37.1 FPS on the Anti-UAV dataset [61]. Yu et al. [159] integrated Transformers, YOLOv5, LoFTR, GMM, and OSTrack for second place in the 3rd Anti-UAV Challenge [168], affirming the practical effectiveness of multi-stage IR-based tracking. Key Insights & Challenges. Although real-time Siamese trackers [115] and detection-based pipelines [43] can sustain high frame rates, they often struggle under clutter, occlusion, or swarm conditions, thereby motivating more adaptive architectures [23,154]. Stealth maneuvers and jamming further complicate UAV tracking, emphasizing the necessity for robust domain adaptation and dynamic cue prioritization [35]. While RGBT sensor fusion [71,129] mitigates individual sensor shortcomings, incorporating Li-DAR or radar [33] inevitably increases calibration overhead and computational load. Existing benchmarks rarely capture large-scale swarms, diverse weather conditions, or severe occlusions, consequently restricting methodical progress [149]. Transformer-based solutions [23,31,150] address complex motion patterns and partial occlusion but can lag in real-time performance, necessitating specialized hardware optimizations for on-board or edge devices.

Extending multi-object trackers (e.g., ByteTrack [163]) to larger UAV swarms remains challenging due to association uncertainty and domain-specific constraints. Ultimately, next-generation trackers will demand faster inference, improved sensor fusion, and broader datasets to achieve reliable anti-UAV performance in real-world conditions.

## 6. Emerging Techniques & Future Directions

Recent UAV research has embraced advanced machine learning paradigms to boost performance, scalability, and autonomy. Figure 2 categorizes these innovations into five key themes: (i) diffusion models for data synthesis and domain adaptation, (ii) vision-language models for semantic understanding, (iii) self-/unsupervised learning, (iv) multimodal fusion and sensor integration, and (v) reinforcement learning for autonomous control. We outline critical developments and future opportunities below. Diffusion Models for Data Synthesis & Domain Adaptation. Diffusion models [51,120] generate high-fidelity UAV imagery to address data scarcity and enhance domain diversity, including text-conditioned approaches [101,109]. Recent advances in faster sampling [99,110] support near real-time augmentation, while diffusion-based domain adaptation [13,98,164] alization [88], further strengthening multi-UAV detection [66], tracking [69,141], and recognition [118], as well as security [4]. Moving forward, large-scale self-supervised pre-training that rapidly adapts to domain shifts in real time may enable ongoing responses to evolving UAV behaviors and stealth tactics.

Multi-Modal Fusion & Sensor Integration. Combining sensors (e.g., RGB, IR, radar, and audio) significantly boosts UAV detection and tracking robustness [86,96,111,175]. Classical fusion [79,96] is now augmented by deep embedding methods [7,155], allowing adaptive sensor weighting under real-time constraints. However, maintaining precise synchronization [147] and carefully balancing power or bandwidth remain essential considerations for robust, large-scale deployments.

Reinforcement Learning & Autonomous Control. Reinforcement Learning (RL) has proven effective for adaptive UAV decision-making in dynamic environments, building on foundational breakthroughs [87,116]. Modern UAVcentric RL research tackles interception [15,177], detection [6], tracking [146], and high-speed racing [65], frequently integrating generative or multi-modal inputs for rapid policy updates. Future directions may emphasize hierarchical or multi-agent RL for large-scale swarm control, balancing cooperative behavior with adversarial countermeasures and mission-specific constraints.

## 7. Conclusion

This survey examined the evolving anti-UAV landscape, focusing on detection, tracking, and recognition. We highlighted recent progress in sensor fusion, deep learning, and multi-modal systems, emphasizing the urgency of robust, real-time solutions under adverse conditions. Analysis of representative datasets revealed gaps in adversarial robustness and scalable swarm tracking. Key insights underscore cross-modal integration, resilience to adversarial tactics, and the promise of self-supervised and reinforcement learning. Moving forward, generative modeling, semantic understanding, and adaptive multi-modal frameworks are poised to drive the next wave of anti-UAV innovations.

## Figures et tableaux

**Figure 1.** Datasets capturing UAV with diverse modalities: 1).RGB[167], 2). Thermal[54]; 3). RGB + Thermal[157]; 4). RGB + Audio + Radar + LiDAR[160].

**Figure 2.** Taxonomy for emerging methods and technologies in UAV research.

**Table 1** 

**Table 3.** Representative UAV Detection Approaches by Modality. Disclaimer: All entries summarize our own interpretation of each paper's methodology and reported outcomes. Since authors use distinct datasets, labels, and metrics, no direct numerical comparison is valid.

**Table 4.** Representative UAV Tracking Approaches. Disclaimer: All entries summarize our own interpretation of each paper's methodology and reported outcomes. Since authors use distinct datasets, labels, and metrics, no direct numerical comparison is valid.

[figure sans légende identifiée] SiamSTA with CDCF and 3-stage redetection. Achieved top precision in 2nd Anti-UAV Challenge. Achieved 68.26 and 76.11 scores on Anti-UAV test and validation sets. Robust on fast/small UAVs.

    . (Yr.) | Mod. | Method | Dataset | Key Observations (Our Reading)
    Detection-Based Trackers |  |  |  | 
    Jiang et al. (2023) [61] | RGB, IR | GlobalTrack + DFSC | Anti-UAV [61] | Released 318-sequence RGB-T UAV tracking benchmark. Achieved the best state accuracy score of 74.33% on the validation set and 65.41% on the test set
    Wu et al. (2024) [148] | RGB | DCF + dual-fovea + contrast + opponent-color (EECF) | Anti-UAV [61], USC-Drone [24] | Real-time EECF tracker (86 FPS) via dual-fovea design. Achieved the state accuracy score of 66.42% on Anti-UAV, 70.45% on USC-Drone.
    Wang et al. (2024) [138] | RGB | YOLOX + Swin-T + α-IoU + BYTE | UAVSwarm [137] | Detection-driven approach with α-IoU + ByteTrack. Achieved 78.2% tracking accuracy on UAVSwarm test split.
    Deng et al.(2024) [33] | RGB, RA, L | YOLOv9 + EfficientNet-B7 + LSTM | MMAUD [160] | Intergrated YOLOv9 + EfficientNet-B7 + LSTM/Kalman for classification and tracking. Achieved 2.21 Pose MSE Loss on 3D tracking of MMAUD and ranked 1st in UG2+ Challenge.
    Siamese (Contrastive) Trackers |  |  | 
    Huang et al. (2021) [52] | IR | SiamSTA | 1st / 2nd Anti-UAV Challenges [61] [166] | Achieved 74.46 and 67.30 scores on 1st / 2nd Anti-UAV test-dev sets, ranking 1st. Extended SiamSTA with spatio-temporal attention + motion estimation.
    Li et al. (2022) [75] | IR | SuperDiMP (ResNet50) | 2nd Anti-UAV Chal-lenge [166] | Used SuperDiMP with dual-branch IR fusion. Achieved +5.84% SR and +4.52% PR over baseline. Focused on contrast inversion robustness.
    Chen et al. (2022) [22] | IR | SiamSTA + CDCF | 1st Anti-UAV Chal-lenge [61] | 
    Zhang et al. (2023) [165] | RGB, IR | SiamFusion | Anti-UAV [61] | 
    Xie et al. (2023) [153] | IR | FPN-based Siamese + STG-RPN + ID-RCNN (STF-Track) | Anti-UAV [61] | STFTrack using STG-RPN and ID-RCNN. Achieved 91.2% precision, 66.6% success @ 12.4 FPS. Addressed distractors and thermal crossover.
    Zhang et al. (2024) [162] | IR | OSTrack + MCJT (RMCM + FSRM + ATUS ) | 1st / 2nd / 3rd Anti-UAV Challenges [61] [166] [168] | 

**Table 4** 

    reviews prominent UAV tracking methods spanning
    detection-based, Siamese-based, and hybrid trackers, em-
    ploying RGB, IR, and multi-modal inputs. Although direct
    numerical comparisons are hampered by dataset and metric
    variations, these approaches collectively represent the state
    of the art in UAV tracking.
    (1) Detection-Based Trackers. Detection-based pipelines
    usually prioritize real-time performance and utilize efficient
    object detectors. For example, Wu et al. [148] proposed
    EECF, a dual-fovea correlation filter tracker operating at
    86 FPS with a state accuracy score of 66.42% on Anti-
    UAV [61] and 70.45% on USC-Drone [24]. Wang et al.

[figure sans légende identifiée] Tracking Lai et al. (2020) [69]; Sio et al. (2020) [118]; Wang et al. (2021) [141]; Cao et al. (2021) [19]

     |  |  | Diffusion Model | Sohl-Dickstein et al. (2015) [119]; Ho et al. (2020) [51]; Song and Ermon (2021) [120]
     |  | Foundational Theories | Data Synthesis | Lu et al. (2023) [83]
     |  |  | Domain Adaptation | Pan and Yang (2010) [95]; Torralba and Efros (2011) [130]; Tsai et al. (2018) [131]
     | Diffusion Models for Data | Text-Conditioned Synthesis | Ramesh et al. (2022) [101]; Saharia et al. (2022) [109]
     | Synthesis and Domain Adaptation |  | 
     |  | High-Resolution Synthesis | Rombach et al. (2022) [105]
     |  | Efficient Synthesis Generation | Salimans and Ho (2022) [110]; Qiao et al. (2025) [99]
     |  | Unsupervised Domain Adaptation | Peng et al. (2024) [98]; Benigmim et al. (2023) [13]; Zhang et al. (2025) [164]
     |  | Pre-training | Su et al. (2019) [121]; Radford et al. (2021) [100]; Zhong et al. (2022) [171]; Li et al. (2022) [74]; Alayrac et al. (2022) [5]; Li et al. (2023) [73]; Huang et al. (2023) [57]
     | Vision-Language Models | Open-Vocabulary Detection | Kamath et al. (2021) [63]; Zareian et al. (2021) [161]; Gu et al. (2022) [48]; Zhou et al. (2022) [172]
     | and Semantic Context |  | 
    Emerging Methods and Technologies | Self-Supervised and Unsupervised Learning | UAV Pioneers Domain Adaptation UAV Pioneers | Detection Semantic Segmentation Tracking Kim et al. (2019) [67]; Kim et al. (2019) [68]; Ye et al. (2022) [156] Liu et al. (2024) [80]; Li et al. (2024) [77] Huang et al. (2025) [55] Feng et al. (2024) [44] Security Alanazi (2024) [4] Swarm Mou et al. (2024) [88] Detection Kim et al. (2023) [66]
     |  |  | Recognition | Lu et al. (2024) [82];
     |  | Multi-Sensor Foundations | 
     | Multi-Modal Fusion and |  | 
     | Sensor Integration |  | 
     |  |  | Detection | AlKhonaini et al. (2024) [6]
     |  |  | Tracking | Wisniewski et al. (2024) [146]
     |  |  | Drone Racing | Kaufmann et al. (2023) [65]
     |  |  |  | narrows the gap between synthetic
     |  |  | and real-world data. Future research may focus on on-the-
     |  |  | fly adaptation from live sensor streams, enabling continuous
     |  |  | refinement under dynamic UAV operating conditions.
     |  |  | Vision-Language Models & Semantic Context. Vision-
     |  |  | language (VL) methods integrate textual cues with visual
     |  |  | features to facilitate open-vocabulary UAV detection and
     |  |  | classification [36, 37, 70, 100, 161, 171]. UAV-specific
     |  |  | adaptations [55, 77, 80] incorporate textual descriptions on
     |  |  | flight profiles, mission goals, or payload attributes, thereby
     |  |  | significantly enriching threat assessment. By leveraging
     |  |  | semantic narratives [27] (e.g., infiltration routes, suspect
     |  |  | cargo), future VL-based systems can swiftly adapt to novel
     |  |  | UAV categories and enhance situational awareness.
     |  |  | Self-Supervised & Unsupervised Learning. Self-and
     |  |  | unsupervised approaches alleviate dependence on labeled
     |  |  | aerial data across varying altitudes, sensors, and weather
     |  |  | [67, 68, 156]. Recent work addresses swarm-wide gener-
