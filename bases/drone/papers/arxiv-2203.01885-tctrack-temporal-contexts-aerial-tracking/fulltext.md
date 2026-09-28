---
id: arxiv-2203.01885-tctrack-temporal-contexts-aerial-tracking
title: "TCTrack: Temporal Contexts for Aerial Tracking"
year: 2022
backend: grobid
---

## Abstract

Temporal contexts among consecutive frames are far from being fully utilized in existing visual trackers. In this work, we present TCTrack 1 , a comprehensive framework to fully exploit temporal contexts for aerial tracking. The temporal contexts are incorporated at two levels: the extraction of features and the refinement of similarity maps. Specifically, for feature extraction, an online temporally adaptive convolution is proposed to enhance the spatial features using temporal information, which is achieved by dynamically calibrating the convolution weights according to the previous frames. For similarity map refinement, we propose an adaptive temporal transformer, which first effectively encodes temporal knowledge in a memory-efficient way, before the temporal knowledge is decoded for accurate adjustment of the similarity map. TCTrack is effective and efficient: evaluation on four aerial tracking benchmarks shows its impressive performance; real-world UAV tests show its high speed of over 27 FPS on NVIDIA Jetson AGX Xavier.

## 1. Introduction

Visual tracking is one of the most fundamental tasks in computer vision. Owing to the superior mobility of unmanned aerial vehicles (UAVs), tracking-based applications are experiencing rapid developments, e.g., motion object analysis [57], geographical survey [61], and visual localization [47]. Nevertheless, aerial tracking still faces two difficulties: 1) aerial conditions inevitably introduce special challenges including motion blur, camera motion, occlusion, etc; 2) the limited power of aerial platforms restricts the computational resource, impeding the deployment of time-consuming state-of-the-art methods [6]. Hence, an ideal tracker for aerial tracking must be robust and efficient.

Most existing trackers adopt the standard tracking-by- detection framework and perform detection for each frame independently. Among these trackers, discriminative correlation filter (DCF)-based methods are widely applied on aerial platforms because of their high efficiency and low resource requirements originated from the operations in the Fourier domain [16,31,38]. However, these trackers struggle when there are fast motions and severe appearance variations. Recently, the Siamese-based network has emerged as a strong framework for accurate and robust tracking [2,4,11,41,42]. Its efficiency is also optimized in [7,21,22] for the real-time deployment of Siamese-based trackers on aerial platforms. However, the strong correlations inherently existing among consecutive frames, i.e., the temporal information, are neglected by these frameworks, which makes it difficult for these approaches to perceive the motion information of the target objects. Therefore, those trackers are more likely to fail when the target undergoes severe appearance change caused by different complex conditions such as large motions and occlusions. This has sparked the recent research into how to make use of temporal information for visual tracking. For DCF-based approaches, the variation in the response maps along the temporal dimension is penalized [33,47], which guides the current response map by previous ones. In Siamese-based networks, which is the focus of this work, temporal information is introduced in most works through dynamic templates, which integrates historical object appearance in the current template through concatenation [72], weighted sum [74], graph network [24], transformer [68], or memory networks [23,73]. Despite their success in introducing temporal information into the visual tracking task, most of the explorations are restricted to only a single stage, i.e., the template feature, in the whole tracking pipeline.

In this work, we present a comprehensive framework for exploiting temporal contexts in Siamese-based networks, which we call TCTrack. As shown in Fig. 1, TCTrack introduces temporal context into the tracking pipeline at two levels, i.e., features and similarity maps. At the feature level, we propose an online temporally adaptive convolution (TAdaConv), where features are extracted with convolution weights dynamically calibrated by the previous frames. Based on this operation, we transform the standard convolutional networks to temporally adaptive ones (TAdaCNN). Since the calibration in the online TAdaConv is based on the global descriptor of the features in the previous frames, TAdaCNN only introduces a negligible frame rate drop but notably improves the tracking performance. At the similarity map level, an adaptive temporal transformer (AT-Trans) is proposed to refine the similarity map according to the temporal information. Specifically, AT-Trans adopts an encoder-decoder structure, where (i) the encoder produces the temporal prior knowledge for the current time step, by integrating the previous prior with the current similarity map, and (ii) the decoder refines the similarity map based on the produced temporal prior knowledge in an adaptive way. Compared to [23,24,68], AT-Trans is memory efficient and thus edge-platform friendly since we keep updating the temporal prior knowledge at each frame. Overall, our approach provides a holistic temporal encoding framework to handle temporal contexts in Siamese-based aerial tracking.

Extensive evaluations of TCTrack show both the effectiveness and the efficiency of the proposed framework. Competitive accuracy and precision are observed on four standard aerial tracking benchmarks in comparison with 51 state-of-the-art trackers, where TCTrack also has a high frame rate of 125.6 FPS on PC. Real-world deployment on NVIDIA Jetson AGX Xavier shows that TCTrack maintains impressive stability and robustness for aerial tracking, running at a frame rate of over 27 FPS.

## 2. Related Work

Tracking by detection. After D. S. Bolme et al. firstly proposed the MOSSE filter [5], many researches [16,31,38] have been made to boost the tracking performance. However, since they suffer from poor representative feature expression, they are hard to maintain robustness under com-plex aerial tracking conditions. Recently, Siamese-based trackers have stood out attributing to their SOTA accuracy and attractive efficiency [2,3,9,26,41,42,78]. For meeting the aerial tracking requirement, some works propose efficient tracking methods [7,21,22].

Despite achieving SOTA performance, those trackers above disregard the temporal contexts in the tracking scenarios, thereby blocking the performance improvement. Differently, our tracker can effectively model the historical temporal contexts during the tracking for increasing the discriminability and robustness. Temporal-based tracking methods. Previously, many works are devoted to exploiting the temporal information in tracking scenarios for raising the tracking performance [10,33,43,47]. Recently, many DL-based temporal tracking methods focus on dynamic templates based on transformer integration [68], template memory update [23,27,73], graph network [24], weighted sum [74], and explicit template update [72]. They try to update the template features in an explicit way or implicit way based on the pre-defined parameters. Then, based on the transformed template features, those trackers exploit the discrete temporal information in tracking sequences.

Despite superior tracking performance, they introduce temporal information via only a single level in the whole tracking pipeline, blocking further improvement of tracking performance. To fully exploit the temporal contexts, in this work, we propose a comprehensive framework for exploring the temporal contexts via two levels, i.e., features level and similarity maps level. Temporal modelling in videos. Modelling the temporal dynamics is essential for a genuine understanding of videos. Hence, it is widely explored in both supervised [20,35,48,49,63,70] and self-supervised paradigm [28,29,34,36,39]. Self-supervised approaches learns temporal modelling by solving various pre-text tasks, such as dense future prediction [28,29], jigsaw puzzle solving [36,39], and pseudo motion classification [34], etc. Supervised video recognition explores various connections between different frames, such as 3D convolutions [62], temporal convolution [63], and temporal shift [48], etc. Closely related to our work is the temporally adaptive convolutions [35], which is applied for temporal modeling in videos. In this work, to adapt to the tracking task, we propose an online CNN which can extract spatial features according to temporal contexts for enriching the temporal information comprehensively.

## 3. Temporal Contexts for Aerial Tracking

In this section, the detailed structure of our framework is described as shown in Fig. 2. The proposed framework considers temporal contexts from two new perspectives: (1) online feature extraction where we incorporate temporal context by TAdaCNN (Sec. 3.1); and (2) similarity map refine- ment where we use a novel AT-Trans to encode the temporal knowledge and then refine the similarity map according to the temporal prior knowledge (Sec. 3.2).

### 3.1. Feature extraction with online TAdaConv

As a key component of our framework, an online TAda-Conv is proposed for feature extraction based on [35] to consider temporal contexts whose structures are shown in Fig. 3. Formally, given the input feature to the online TAda-Conv at a certain stage in the network X t in the t-th frame, the output of the online TAdaConv Xt can be obtained as follows:

Xt = W t * X t + b t ,(1)

where the operator * denotes the convolution operation and W t , b t are the temporal weight and bias of our convolution. A standard convolution layer uses learnable parameters for weights and bias, and shares them in the whole tracking sequence. Differently, in our online convolution layer, the parameters are calculated by the learnable parameters (W b and b b ) and calibration factors that are varied for each frame, i.e.,

W t = W b • α w t and b t = b b • α b t .

Different from the original structure in video understanding, online TAdaConv processes one frame at a time. Hence, it only considers the temporal context in the past just like tracking in the real world. Specifically, we keep a temporal context queue X ∈ R L×C of L frame descriptors Xt ∈ R C including that of the current frame:

X = Cat( Xt , Xt-1 , ..., Xt-L+1 ) ,(2)

where Cat represents the concatenation and the frame descriptor is obtained by a global average pooling (GAP) over the feature of the each coming frame, i.e., Xt = GAP(X t ).

For the generation of calibration factors α w t and α b t , we perform two convolutions over the temporal context queue X with a kernel size of L, i.e., α w t = F w ( X) + 1, α b t = F b ( X) + 1, where F i denotes the convolution operation. Besides, the weights of F are initialized to zero so that at the initialization, W t = W b and b t = b b . For t ≤ L -1, where there is not enough previous frames, we fill that with the descriptor of the first frame X1 . Given our backbone ϕ tada that considers the temporal contexts in the feature extraction process, the similarity map R t for the t-th frame can be obtained as:

R t = ϕ tada (Z) ϕ tada (X t ) ,(3)

where Z denotes the template and represents the depthwise correlation [41]. After that, F t can be obtained by a convolution layer, i.e., F t = F(R t ). Remark 1: To the best of our knowledge, our online TAdaCNN is the first to integrate temporal contexts in the feature extraction process in the tracking task.

### 3.2. Similarity Refinement with AT-Trans

Besides considering temporal contexts in the feature extraction process, in this work, we also propose an AT-Trans for refining the similarity map F t according to the temporal contexts. Specifically, our AT-Trans has an encoderdecoder structure, where the encoder aims to integrate tem- poral knowledge and the decoder focuses on similarity refinement. In this section, we first revisit the multi-head attention [64] before describing the details of our AT-Trans.

Multi-head attention. As a fundamental component of the transformer, multi-head attention is formulated as follows:

MultiHead(Q, K, V) = Cat(H 1 att , ..., H N att ) W H n att = Attention(QW n q , KW n k , VW n v ) Attention(Q, K, V) = Softmax(QK T / √ d)V ,(4)

where

√ d is the scaling factor while W ∈ R Ci×Ci , W n q ∈ R Ci×C h , W n k ∈ R Ci×C h

, and W n v ∈ R Ci×C h are learnable weights. In our AT-Trans, we employ multihead attention with 6 heads, i.e., N = 6 and C h =C i /6.

Compared to CNN, Transformer can more effectively encode the global context information [18,64]. Hence, to exploit the global temporal contexts more effectively, we propose a transformer-based temporal integration strategy to successively encode global contexts information. Moreover, most existing temporal-based methods generally store the input features for temporal modeling, inevitably introducing sensitive parameters and unnecessary computation. In this work, for eliminating unnecessary operations and sensitive parameters, we adopt an online update strategy for temporal knowledge. Transformer encoder. The encoder generates temporal prior knowledge by integrating the previous knowledge with current features. Generally, we stack two multi-head attention layers before a temporal information filter is applied. The final temporal prior knowledge for the current step is obtained by further attaching a multi-head attention layer to the filtered information. The structure of the encoder is presented in Fig. 4(a).

Given the previous temporal prior knowledge F m t-1 and the current similarity map F t , there are two ways to in- tegrate their information into the current prior knowledge F m t , with respect to the selection of the query, key, and values. One uses F m t-1 as the query and F t as the value and key, while the other uses them in reverse. In our method, we adopt the former, as this essentially puts more emphasis on the current similarity map. This is plausible as closer temporal information is more valuable than the previous one for representing the characteristics of the current object more accurately. Empirical results in Sec. 4.3 also validate the effectiveness of this choice. Hence, we obtain the output of the stacked multi-head attention layer in t-th frame F 2 t by:

Multi-Head Attention Add & Norm Cat & Conv Multi-Head Attention Add & Norm Multi-Head Attention Q K V Add & Norm

F 1 t = Norm(F t + MultiHead(F m t-1 , F t , F t )) F 2 t = Norm(F 1 t + MultiHead(F 1 t , F 1 t , F 1 t )) ,(5)

where Norm represents the layer normalization. Since aerial tracking may frequently encounter less useful contexts caused by motion blur or occlusion, some unwanted contexts may be included if we pass along the complete temporal information without any filtering. To eliminate the unwanted information, a neat temporal information filter is generated by attaching a feed-forward network FFN to the global descriptor of F 1 t obtained by global average pooling GAP, i.e., α = FFN(GAP(F(F 1 t ))). The filtered information F f t is obtained by:

F f t = F 2 t + F(Cat(F 2 t , F 1 t )) * α ,(6)

where F denotes a convolution layer. With this, the temporal knowledge of t-th frame, F m t can be obtained as follows:

F m t = Norm(F f t + MultiHead(F f t , F f t , F f t )) .(7)

Hence, for each frame, we update the temporal knowledge rather than saving all of them. This makes the memory occupancy of the temporal prior knowledge fixed during the whole tracking process, which makes TCTrack memoryefficient compared to approaches that require saving all the intermediate temporal information. Overall, owing to this strategy as well as the temporal filter and the multi-head attention, our AT-Trans adaptively encodes the temporal prior in a memory-efficient way.

For the first frame in a tracking sequence, since the characteristics of different targets are distinct, using a unified initialization for the initial temporal prior F m 0 would be unreasonable. Observing that the similarity map in the first frame essentially represents the semantic features of the target object in an effective way, we set the initial temporal prior by a convolution over the initial similarity map F 0 , i.e., F m 0 = F init (R 1 ). We also empirically show our initialization is better in Sec. 4.3. Transformer decoder. According to the temporal prior knowledge F m t , the decoder aims to refine the similarity map. To better explore the interrelations between temporal knowledge and current spatial features F t , we adopt two multi-head attention layers with feed-forward before output. Its structure is presented in Fig. 4(b). By generating the attention map, the valid information in the temporal knowledge F m t can be extracted for refining the similarity map F t to obtain the final output F * t :

F 3 t = Norm(F t + MultiHead(F t , F t , F t )) F 4 t = Norm(F 3 t + MultiHead(F 3 t , F m t , F m t )) F * t = Norm(F 4 t + FFN(F 4 t ))

.

Relying on the encoder-decoder structure of AT-Trans, the temporal contexts are effectively exploited to refine the similarity maps for boosting robustness and accuracy. The comparison of similarity maps in Fig. 5 shows the effectiveness of the similarity map refinement, especially where camera motion, severe motion, and occlusion exist.

### Backbone

### Inference time Parameters

AlexNet [40] 3.4ms 2.47M VGG11 [58] 3.7ms 9.22M ResNet18 [30] 10.1ms 11.2M MobileNet v2 [56] 13.7ms 2.2M EfficientNet [60] 27.4ms 39.4K SqueezeNet1 0 [37] 8.8ms 735.42K ShuffleNet v2 x0.5 [77] 16.6ms 341.8K

Remark 2: To the best of our knowledge, AT-Trans is the first attempt to use temporal contexts for similarity maps.

## 4. Experiments

Our framework is evaluated on four public authoritative benchmarks and tested on real-world aerial tracking conditions. In this section, our method is comprehensively evaluated on four well-known aerial tracking benchmarks, i.e., UAV123 [54]

, UAVTrack112 L[21], UAV123@10fps[54], and DTB70[45]. 51 existing top trackers are included for a thorough comparison, where their results are obtained by running the official codes with their corresponding hyperparameters. For a clearer comparison, we divide them into two groups, (i) light-weight trackers[1,2,6,7,12,14-17,22, 27, 33, 38, 41, 43, 44, 46, 47, 51, 52, 65-67, 75, 76, 80] and (ii) deep trackers[4,8,9,11,13,23,25,26,41,50,53,59,68,69,71,74,78,79].

### 4.1. Implementation Details

We use AlexNet as the backbone of our tracker, as efficiency is essential for aerial tracking. As shown in Table 1, the comparison in inference time of different popular backbones on the NVIDIA Jetson AGX Xavier platform has shown that AlexNet has the lowest latency, while the recent developments in mobile networks [37,56,77] suffer from high memory access cost (MAC). For initialization, we use ImageNet pre-trained model for AlexNet and use the same initialization for online TAdaConv as in [55]. The AT-Trans in our TCTrack is randomly initialized.

We train our tracker with the videos whose length are 4 from VID [55], Lasot [19], and GOT-10K [32]. We train TCTrack for a total of 100 epochs on two NVIDIA TITAN RTX GPUs. For the first 10 epochs, the parameters of the backbone are frozen, following [41]. The rest of the training process employs a learning rate decreasing from 0.005 to 0.0005 in log space. SGD is employed as the optimizer with a momentum of 0.9, where the mini-batch size is 124 pairs. The input sizes of the template and the search area are 127 2 and 287 2 respectively. The proposed online TAdaConv is used in the replacement of the last two convolutional layers. Remark 3: For more detailed information about the evaluation criteria and loss function, please refer to the supple- mentary material.

### 4.2. Comparison with Light-Weight Trackers

In this subsection, TCTrack is compared with 29 existing efficient trackers on the standard aerial tracking benchmarks. For Siamese-based methods, we evaluate them with the same backbone as ours for a fair comparison. UAV123. UAV123 [54] is a large-scale aerial tracking benchmark involving 123 challenging sequences with more than 112K frames. Performance evaluation on UAV123 can verify the tracking performance in most commonly aerial tracking conditions. As shown in Fig. 6, our TCTrack outperforms HiFT and SiamRPN++ in AUC (3%) and (4.3%). DTB70. DTB70 [45] includes 70 severe motion scenarios in various challenging scenes. For evaluating the effectiveness of our method in handling motion, we adopt this benchmark to prove the robustness of TCTrack. Our tracker ranks 1st with an improvement of 5% in AUC against the other best tracker illustrated in Fig. 6. UAV123@10fps. Adopting an image rate of 10 FPS, the motion and variation are more abrupt and severe in UAV123@10fps [54], thereby significantly raising the difficulty of tracking. From the comparison with our other SOTA trackers, we can clearly see that our tracker maintains superior robustness and exceeds the second-best tracker in terms of success and precision rate. Attribute-based performance. In aerial tracking conditions, the severe motion of UAVs will increase the difficulty of tracking. To fully analyze the robustness of our tracker in Prec. AutoTrack [47] 0.405 0.675 C-COT [17] 0.422 0.691 ARCF [33] 0.399 0.640 UDT+ [66] 0.405 0.637 STRCF [43] 0.360 0.609 ECO [12] 0.436 0.684 UDT [66] 0.388 0.620 TADT [46] 0.462 0.712 SRDCF [16] 0.320 0.508 SiameseFC [2] 0.452 0.690 CoKCF [75] 0.283 0.520 DaSiamRPN [80] 0.479 0.729 BACF [38] 0.358 0.593 SiamAPN++ [7] 0.537 0.735 DSiam [27] 0.321 0.512 SiamRPN++ [41] 0.559 0.773 HiFT [6] 0.551 0.734 TCTrack (ours) 0.582 0.786 specific challenges such as fast motion, camera motion, occlusion, deformation, etc, attribute-based comparisons are conducted. The comparison between other SOTA trackers presented in Fig. 7 proves the robustness of our framework in several challenging conditions. Since our tracker can accumulate the consecutive temporal knowledge from 1st frame to the current frame, our tracker can learn the historical location of the object. Therefore, our tracker achieves superior performance in occlusion and fast-motion scenes. Furthermore, benefiting from our content-adaptive temporal knowledge and online TAdaConv, TCTrack can handle the negative influence introduced by the environment.

UAVTrack112 L. To validate the effectiveness of our framework in long-term tracking performance, we conduct the evaluations on UAVTrack112 L [21], which is the current biggest long-term aerial tracking benchmark including over 60k frames. Table 3. Ablation study of different components of adaptive temporal transformer on UAV123 [54]. TIF denotes the temporal information filter in the AT-Trans (Fig. 4). sive framework that fully exploits temporal contexts, TC-Track achieves superior performance against other trackers in terms of precision (0.786) and success rate (0.582).

### 4.3. Ablation Study

To verify the effectiveness of our framework, comprehensive ablation studies are presented in this subsection. Clarification of symbol. In Table . 3, we denote our proposed transformer architecture without temporal information filter as Transformer. We analyze the influence caused by different models, training methods, initializations, and query selections. Furthermore, for ensuring the correctness of our experiments, all tracker adopts the same process (including training, parameter settings, etc.) except for the studied module. Analysis on AT-Trans. I) Adding the consecutive temporal knowledge without filtering out the invalid information (third line) will confuse the tracker. Therefore, the tracking performance is impeded significantly. By adding our information filter in the tracking-by-detection framework, our module can also raise the performance by adaptively selecting valid contexts (second line). II) As we discussed before, using the unique information of the tracking object in the first frame to initiate the temporal knowledge is more appropriate than random initiation, especially in occlusion conditions (raising about 6%). III) We also analyze the effect caused by the different queries. The results prove that refinement based on the current similarity map is more effective and suitable for raising performance, especially in motion scenarios (improved over 10%).

Compared with Transformer, there is a significant improvement brought by our temporal knowledge encoded by AT-Trans (9.8% in overall AUC and 6.7% in overall precision). Specifically, our tracker yields the best performance with an improvement of about 12.0% and 15.1% in handling the motion scenes. In the occlusion conditions, owing to the consecutive temporal contexts, our tracker can relocate the object via the previous information, thereby boosting the success rate by 11.4%. Studies about the length of temporal sequences in TAda-Conv. As shown in Table . 4, when the image range of TAdaConv is increasing, the performance is raising. To introduce the temporal contexts effectively and efficiently, in this work, we adopt 3 as the length of sequences, i.e., L=3.

### 4.4. Comparison with Deep Trackers

Our approach aims to introduce temporal information to raise the robustness and handle the challenges in aerial tracking. Therefore, to comprehensively illustrate our efficiency and performance against other SOTA trackers with deeper backbones, further comparisons are constructed including over 20 trackers on NVIDIA TITAN RTX. As illustrated in Fig. 8, although adopting the lightweight CNN as our backbone, TCTrack achieves competitive performance compared with the best tracker while running 2.49 times faster than the best tracker (TransT). Attribute to our content-adaptive and memory-efficient structure, our framework with temporal contexts can fill the performance margin caused by deeper backbones while maintaining the promising efficiency in aerial tracking conditions.

## 5. Real-world Tests

In this section, we implement our tracker on UAV to validate its practicability in real-world conditions. Specifically, NVIDIA Jetson AGX Xavier and Pixhawk 2 are adopted as the aerial onboard computer and flight controller. During the real-world UAV tests, RAM usage and GPU VRAM usage are 15.29% and 3%, respectively. Additionally, the utilization of GPU and CPU is 46% and 12.43% on average. The center location error (CLE) is adopted to evaluate the tracking performance (20 is the success threshold).

The special challenges in the real-world tests involve different illumination, scale variation, occlusion, motion blur, and low-resolution scenes. The visualization of our tracking recording of practical UAV is shown in Fig. 9. When facing partial occlusion and low illumination (the first row), our tracker can maintain impressive stability and robustness via exploiting the consecutive temporal knowledge. Meantime, our tracker also achieves satisfying accuracy when facing motion blur and the occluded object (the second row). Additionally, the visualization of the third row strongly presents the powerful ability of our tracker under camera motion conditions. Finally, our tracker remains at a speed of over 27 FPS during the tests without the acceleration of TensorRT 3 . The real-world tests on our practical UAV strongly demonstrate the practicability and feasible deployment ability of our framework. Furthermore, our tracker presents stable and promising tracking performance in complex aerial tracking conditions.

## 6. Conclusion and Discussion

In this work, we propose a comprehensive framework for introducing temporal contexts into aerial tracking which Potential limitations. Hindered by the short-term training method, the potential of our framework in very long-term temporal modeling and long-time occlusion is not fully explored. Moreover, the TensorRT and ONNX versions will be developed in our future works.

Negative impacts. Although TCTrack aims to explore temporal contexts comprehensively for aerial tracking, impressive efficiency and effectiveness make it easy to be deployed on UAVs for unauthorized surveillance.

## Figures et tableaux

**Figure 1.** Overview of our framework namely TCTrack. It exploits temporal information at two levels: (a) the extraction of features by the temporally adaptive convolutional neural networks (TAdaCNN) and (b) the refinement of similarity maps by the adaptive temporal transformer (AT-Trans).

**Figure 2.** Overview of our framework. It mainly consists of three components, i.e., TAdaCNN for online feature extraction shown in Fig. 3, AT-Trans for similarity map refinement shown in Fig. 4, and classification&regression for final prediction. This figure illustrates the workflow of our TCTrack when tracking sequences are t frames. Through temporal contexts before correlation and after, comprehensive temporal knowledge is introduced in our framework. Best view in color.

**Figure 3.** The schema of our online TAdaConv. The temporal calibration factor is generated by the feature sequences (number of its is L). Based on the temporal vectors, the parameters of our online TAdaConv can be adjusted adaptively in every frame.

FFNFigure 4. Figure 4. Structure of the adaptive temporal transformer. The left sub-window illustrates the adaptive temporal encoder to model the temporal knowledge. The right sub-window shows the component of the decoder. Best viewed in color.

**Figure 5.** Comparison between similarity maps before refinement (second column) and after (third column) refinement.

**Figure 6.** Overall performance of all trackers on three well-known aerial tracking benchmarks. Our tracker achieves superior performance against other SOTA trackers. TCTrack-L represents the tracker with AT-Trans while the TCTrack denotes the full version of our framework.

**Figure 7.** Attribute-based evaluation of all trackers on three well-known aerial tracking benchmarks. Our temporal tracker can maintain promising performance under severe motion, occlusion, and deformation. More results are shown in the supplementary material.

**Figure 8.** Comparisons to trackers with deeper backbones on DTB70. Our tracker achieves competitive performance compared with other deeper trackers while possessing superior efficiency.

**Figure 9.** Recording of real-world tests on the embedded platform. The tracking targets are marked with red while the CLE represents the center location error. To avoid unpredictable disclosure of personally identifiable information, images are processed merely. consists of two perspectives, e.g., feature extraction and similarity refinement. Specifically, in this work, AT-Trans and online TAdaCNN are the first attempts for exhaustively exploring temporal contexts. Besides, attributing to our online updating strategy, unnecessary operations and memory loading are avoided. Extensive experiments on four benchmarks and real-world tests on our UAV demonstrate the effectiveness and efficiency of our framework. We hope that our framework can inspire further research in aerial and even general tracking with temporal contexts.

**Table 1.** Comparison of inference time and parameters on NVIDIA Jetson AGX Xavier. Here, we use 287×287×3 as the input image and only evaluate the inference time of the CNN. [corps du tableau reconstruit par Docling : à vérifier]

    Backbone | Inference time | Parameters
    AlexNet [40] | 3.4ms | 2.47M
    VGG11 [58] | 3.7ms | 9.22M
    ResNet18 [30] | 10.1ms | 11.2M
    MobileNet v2 [56] | 13.7ms | 2.2M
    EfficientNet [60] | 27.4ms | 39.4K
    SqueezeNet1 0 [37] | 8.8ms | 735.42K
    ShuffleNet v2 x0.5 [77] | 16.6ms | 341.8K

**Table 2.** Overall performance on UAVTrack112 L. The best three performances are respectively highlighted with red, green, and blue colors. [corps du tableau reconstruit par Docling : à vérifier]

    Trackers | Succ. | Prec. | Trackers | Succ. | Prec.
    AutoTrack[47] | 0.405 | 0.675 | C-COT[17] | 0.422 | 0.691
    ARCF [33] | 0.399 | 0.640 | UDT+[66] | 0.405 | 0.637
    STRCF [43] | 0.360 | 0.609 | ECO[12] | 0.436 | 0.684
    UDT [66] | 0.388 | 0.620 | TADT[46] | 0.462 | 0.712
    SRDCF [16] | 0.320 | 0.508 | SiameseFC[2] | 0.452 | 0.690
    CoKCF [75] | 0.283 | 0.520 | DaSiamRPN[80] | 0.479 | 0.729
    BACF [38] | 0.358 | 0.593 | SiamAPN++[7] | 0.537 | 0.735
    DSiam [27] | 0.321 | 0.512 | SiamRPN++[41] | 0.559 | 0.773
    HiFT [6] | 0.551 | 0.734 | TCTrack(ours) | 0.582 | 0.786

**Table 2** reports the comparison of TC-Track and other SOTA trackers. Thanks to our comprehen-

     | 1 |  |  | Fast camera motion (41) on DTB70 |  |  | TCTrack [0.630] |  | 0.6 |  |  | Background clutter (21) on UAV123@10fps |  |  | TCTrack [0.403] |  | 0.8 |  |  |  | Partial occlusion (73) on UAV123 |  |  |  | TCTrack [0.518] |  | 1 |  |  |  | Deformation (18) on DTB70 | TCTrack [0.647]
     |  |  |  |  |  |  |  |  |  |  | TCTrack-L [0.621] |  |  |  |  |  |  |  |  |  |  |  | TCTrack-L [0.401] |  |  |  |  |  |  |  |  |  |  |  | TCTrack-L [0.510] |  |  |  |  |  |  |  |  | TCTrack-L [0.640]
     | 0.9 |  |  |  |  |  |  |  |  |  | HiFT [0.611] SiamAPN++ [0.601] |  |  |  |  |  |  |  |  |  |  |  | SiamRPN++ [0.383] SiamAPN++ [0.379] |  | 0.7 |  |  |  |  |  |  |  |  |  | HiFT [0.488] SiamRPN++ [0.477] |  | 0.9 |  |  |  |  |  |  | HiFT [0.626] SiamAPN++ [0.616]
     |  |  |  |  |  |  |  |  |  |  | SiamAPN [0.599] |  | 0.5 |  |  |  |  |  |  |  |  |  | TADT [0.373] |  |  |  |  |  |  |  |  |  |  |  | SiamAPN++ [0.477] |  |  |  |  |  |  |  |  | SiamAPN [0.616]
     | 0.8 |  |  |  |  |  |  |  |  |  | SiamRPN++ [0.587] |  |  |  |  |  |  |  |  |  |  |  | ECO [0.371] |  |  |  |  |  |  |  |  |  |  |  | TADT [0.474] |  | 0.8 |  |  |  |  |  |  | SiamRPN++ [0.579]
     |  |  |  |  |  |  |  |  |  |  | CCOT [0.551] DeepSTRCF [0.516] |  |  |  |  |  |  |  |  |  |  |  | DSiam [0.368] HiFT [0.365] |  | 0.6 |  |  |  |  |  |  |  |  |  | SiamAPN [0.470] ECO [0.457] |  |  |  |  |  |  |  |  | DeepSTRCF [0.496] DaSiamRPN [0.493]
     | 0.7 |  |  |  |  |  |  |  |  |  | ECO [0.514] |  |  |  |  |  |  |  |  |  |  |  | MCCT [0.363] |  |  |  |  |  |  |  |  |  |  |  | MCCT [0.454] |  | 0.7 |  |  |  |  |  |  | IBCCF [0.478]
     |  |  |  |  |  |  |  |  |  |  | AutoTrack [0.496] |  | 0.4 |  |  |  |  |  |  |  |  |  | UDT+ [0.362] |  |  |  |  |  |  |  |  |  |  |  | UDT+ [0.447] |  |  |  |  |  |  |  |  | SiameseFC [0.467]
    rate | 0.6 |  |  |  |  |  |  |  |  |  | ARCF [0.496] MCCT [0.494] SiameseFC [0.487] | rate |  |  |  |  |  |  |  |  |  |  | MCPF [0.359] DeepSTRCF [0.353] SiamAPN [0.346] | rate | 0.5 |  |  |  |  |  |  |  |  |  | ECO-HC [0.444] CCOT [0.442] DeepSTRCF [0.431] | rate | 0.6 |  |  |  |  |  |  | MCCT [0.466] AutoTrack [0.452] TADT [0.449]
    Success | 0.4 0.5 |  |  |  |  |  |  |  |  |  | UDT+ [0.476] ECO-HC [0.469] STRCF [0.467] TADT [0.466] DaSiamRPN [0.457] | Success | 0.3 |  |  |  |  |  |  |  |  |  | ECO-HC [0.339] CCOT [0.337] DaSiamRPN [0.329] IBCCF [0.328] CSRDCF [0.320] | Success | 0.3 0.4 |  |  |  |  |  |  |  |  |  | IBCCF [0.422] DaSiamRPN [0.414] SiameseFC [0.412] MCPF [0.409] STRCF [0.402] | Success | 0.5 0.4 |  |  |  |  |  |  | CCOT [0.430] ARCF [0.426] ECO [0.424] MCPF [0.410] UDT [0.407]
     | 0.3 |  |  |  |  |  |  |  |  |  | IBCCF [0.456] CSRDCF [0.454] BACF [0.435] UDT [0.434] |  | 0.2 |  |  |  |  |  |  |  |  |  | STRCF [0.317] AutoTrack [0.315] SiameseFC [0.311] CoKCF [0.309] |  | 0.2 |  |  |  |  |  |  |  |  |  | UDT [0.396] SRDCF [0.395] ARCF [0.394] AutoTrack [0.389] |  | 0.3 |  |  |  |  |  |  | ECO-HC [0.404] CSRDCF [0.396] STRCF [0.390] UDT+ [0.386]
     | 0.2 |  |  |  |  |  |  |  |  |  | MCPF [0.426] |  |  |  |  |  |  |  |  |  |  |  | CF2 [0.302] |  |  |  |  |  |  |  |  |  |  |  | CSRDCF [0.380] |  | 0.2 |  |  |  |  |  |  | CF2 [0.377]
     |  |  |  |  |  |  |  |  |  |  | CF2 [0.417] |  | 0.1 |  |  |  |  |  |  |  |  |  | ARCF [0.291] |  |  |  |  |  |  |  |  |  |  |  | BACF [0.373] |  |  |  |  |  |  |  |  | CoKCF [0.355]
     | 0.1 |  |  |  |  |  |  |  |  |  | SRDCF [0.398] fDSST [0.388] |  |  |  |  |  |  |  |  |  |  |  | BACF [0.275] SRDCF [0.263] |  | 0.1 |  |  |  |  |  |  |  |  |  | CF2 [0.372] CoKCF [0.349] |  | 0.1 |  |  |  |  |  |  | DSiam [0.321] BACF [0.302]
     |  |  |  |  |  |  |  |  |  |  | CoKCF [0.376] |  |  |  |  |  |  |  |  |  |  |  | UDT [0.254] |  |  |  |  |  |  |  |  |  |  |  | KCC [0.345] |  |  |  |  |  |  |  |  | fDSST [0.243]
     | 0 | 0 | 0.1 | 0.2 | 0.3 | 0.4 Overlap threshold 0.5 0.6 | 0.7 | 0.8 | 0.9 | 1 | DSiam [0.340] KCC [0.306] DSST [0.281] Staple [0.254] |  | 0 | 0 | 0.1 | 0.2 | 0.3 | 0.4 Overlap threshold 0.5 0.6 | 0.7 | 0.8 | 0.9 | 1 | KCC [0.237] fDSST [0.209] Staple [0.194] DSST [0.137] |  | 0 | 0 | 0.1 | 0.2 | 0.3 | 0.4 Overlap threshold 0.5 0.6 | 0.7 | 0.8 | 0.9 | 1 | Staple [0.342] fDSST [0.329] DSiam [0.328] DSST [0.306] |  | 0 | 0 | 0.1 | 0.2 | 0.3 | 0.4 Overlap threshold 0.5 0.6 | 0.7 | 0.8 | 0.9 | 1 | KCC [0.234] DSST [0.225] SRDCF [0.208] Staple [0.207]

[figure sans légende identifiée] SF/MF refer to single-frame (SF) training, i.e., the standard tracking-by-detection training method and our multi-frame (MF) training method. CI/RI refer to convolutional initialization and random initialization for temporal prior knowledge. Query denotes which feature map is used as the query in the adaptive temporal encoder in AT-Trans mentioned in Sec. 3.2. 0.810 8.0%↑ 0.615 12.0%↑ 0.793 11.3%↑ 0.586 15.1%↑ 0.710 7.1%↑ 0.510 11.4%↑ 0.800 6.7%↑ 0.604 9.8%↑

     |  | Camera Motion | Fast motion | Partial Occlusion | Overall
    Model | Train Init. Query | Prec. | Succ. | Prec. | Succ. | Prec. | Succ. | Prec. | Succ.
    Transformer Transformer+TIF SF -F m SF -F m t-1 t-1 Transformer MF CI F m t-1 Transformer+TIF MF RI F m t-1 | 0.750 0.767 2.3%↑ 0.749 2.4%↓ 0.779 3.9%↑ | 0.549 0.578 5.3%↑ 0.525 7.6%↓ 0.592 7.8%↑ | 0.712 0.720 1.1%↑ 0.719 2.4%↓ 0.766 7.6%↑ | 0.509 0.525 3.1%↑ 0.500 7.6%↓ 0.566 11.2%↑ | 0.663 0.667 0.6%↑ 0.639 2.4%↓ 0.670 1.1%↑ | 0.458 0.474 3.5%↑ 0.415 7.6%↓ 0.483 5.5%↑ | 0.750 0.765 2.0%↑ 0.732 2.4%↓ 0.772 2.9%↑ | 0.550 0.573 4.2%↑ 0.508 7.6%↓ 0.586 6.6%↑
    Transformer+TIF MF CI Ft Transformer+TIF MF CI F m t-1 | 0.785 4.7%↑ | 0.587 6.9%↑ | 0.726 2.0%↑ | 0.528 3.7%↑ | 0.676 2.0%↑ | 0.480 4.8%↑ | 0.771 2.8%↑ | 0.580 5.5%↑

**Table 4.** Different sequence lengths for the online TAdaConv on UAV123[54].

    Different Variations | Overall Precision Overall Success
    Transformer | 0.750 | 0.550
    Transformer+TAdaConv (L=1) | 0.749 0.1%↓ | 0.561 2.0%↑
    Transformer+TAdaConv (L=2) | 0.774 3.2%↑ | 0.573 4.2%↑
    Transformer+TAdaConv (L=3) | 0.776 3.5%↑ | 0.580 5.5%↑
