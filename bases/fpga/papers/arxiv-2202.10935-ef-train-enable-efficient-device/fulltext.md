---
id: arxiv-2202.10935-ef-train-enable-efficient-device
title: "EF-Train: Enable Efficient On-device CNN Training on FPGA Through Data Reshaping for Online Adaptation or Personalization"
year: 2022
backend: pymupdf
---

EF-Train: Enable Efficient On-device CNN Training on FPGA Through Data Reshaping for Online Adaptation or

YUE TANG, University of Pittsburgh, USA XINYI ZHANG, University of Pittsburgh, USA PEIPEI ZHOU, University of Pittsburgh, USA JINGTONG HU, University of Pittsburgh, USA

Conventionally, DNN models are trained once in the cloud and deployed in edge devices such as cars, robots, or unmanned aerial vehicles (UAVs) for real-time inference. However, there are many cases that require the models to adapt to new environments, domains, or new users. In order to realize such domain adaption or personalization, the models on devices need to be continuously trained on the device. In this work, we design EF-Train, an efficient DNN training accelerator with a unified channel-level parallelism-based convolution kernel that can achieve end-to-end training on resource-limited low-power edge-level FPGAs. It is challenging to implement on-device training on resource-limited FPGAs due to the low efficiency caused by different memory access patterns among forward, backward propagation, and weight update. Therefore, we developed a data reshaping approach with intra-tile continuous memory allocation and weight reuse. An analytical model is established to automatically schedule computation and memory resources to achieve high energy efficiency on edge FPGAs. The experimental results show that our design achieves 46.99 GFLOPS and 6.09 GFLOPS/W in terms of throughput and energy efficiency, respectively.

CCS Concepts: • Hardware →Integrated circuits; Reconfigurable logic and FPGAs; Hardware accelerators.

Additional Key Words and Phrases: on-device training, edge FPGAs, data reshaping

INTRODUCTION Deep Neural Networks (DNNs) have been widely used in edge devices such as cars, robotics [1], and unmanned aerial vehicles (UAVs) [2], to accomplish various tasks, including autonomous driving, object detection, etc. FPGAs are promising platforms with higher computational density, communication bandwidth, and energy efficiency, and can be configured based on different tasks. Nowadays, FPGAs have been widely used in various edge device domains. For example, edge-scale FPGAs are commonly utilized in object detection tasks with high frames per second and low power consumption [3]. The Corazon-AI built on Xilinx Zynq is a perfect fit for various computervision-based applications including video surveillance, advanced driver-assistance systems (ADAS), medical robotics, industrial automation, and augmented reality [4]. Combined with reconfigurability, FPGAs have been adopted in several autonomous platforms such as pony.ai [5] and ZF ProAI [6]. In medical applications, an FPGA-based low-latency multi-layer perception (MLP) processor for real-time cancer detection has been developed, since FPGA-based design can directly interface with sensors, display devices, and reduce data movement delays [7]. Burger et al. applied an FPGA-based embedded device to monitor users’ electrocardiograms (ECGs) in a pervasive internet-of-things (IoT) system [8]. FPGAs have also been well performed in other areas such as agricultural robots [9], UAVs [10], etc.

In traditional FPGA-based edge device applications, DNNs are pre-trained in the cloud before being deployed in FPGAs, which is not efficient for domain adaption. When the environments, tasks,

Authors’ addresses: Yue Tang, University of Pittsburgh, Pittsburgh, USA, yut51@pitt.edu; Xinyi Zhang, University of Pittsburgh, Pittsburgh, USA, xinyizhang@pitt.edu; Peipei Zhou, University of Pittsburgh, Pittsburgh, USA, peipei.zhou@ pitt.edu; Jingtong Hu, University of Pittsburgh, Pittsburgh, USA, jthu@pitt.edu.

or users change, data needs to be collected from the edge FPGAs and transmitted to the cloud. Then, the cloud retrains a new model, transmitting the model back to the edge devices. The whole process is inefficient and time-consuming. Therefore, it is often desirable for edge FPGAs to continuously and locally learn from new data. Such on-device learning can directly improve model accuracy and adapt to new environments. Currently, several algorithms have been proposed to enable edge devices to achieve domain adaption locally. For example, a MobileDA framework [11] has been developed to allow a novel teacher network trained in the server to distill the knowledge for a student network running in the edge device, and the algorithm was employed on an embedded GPU and NVIDIA Jetson TX2. A transductive transfer learning model HDCNN [12] has been proposed to allow adaptation without requiring collecting large volumes of labeled training data in the target domain, and the algorithm was tested on 1080 Ti GPU. To implement these complex and fantastic software-level algorithms on FPGA-based edge devices, an FPGA-based training accelerator is indispensable. However, traditional FPGA-based edge device applications lack such hardware-level designs for training operations, which prevents FPGA-based devices from applying these algorithms directly.

Furthermore, directly training Convolutional Neural Network (CNN) models on local FPGAs can facilitate personalization. For example, in some medical applications such as home monitoring [13], long-term ECG monitoring [14], etc., the distinction of different users’ physical conditions will impact data distribution, so models need to be fine-tuned based on specific users. The system in [8] utilized cloud services to log a user’s condition over time and continuously improve the system’s performance. It would be more effective if models could be directly updated on the FPGA device. Besides, learning at the edge can provide better privacy since users do not need to upload data into the central cloud [15].

However, it has been challenging to implement on-device training on FPGAs. Previous works mainly focused on implementing CNN inference on FPGAs. For example, Zhang et al. [16] exploited various optimization techniques including loop unrolling, loop tiling, and loop transformation on the FPGA accelerator, and proposed a roofline model to quantitatively analyze its computing throughput and required memory bandwidth. Various designs [17, 18] have been proposed to map well-trained neural networks on FPGAs for inference with high throughput and low latency. Compared with CNN inference, it is more complex to efficiently implement CNN training on FPGAs in terms of the following aspects. First, the inference process only includes forward propagation (FP), whereas the training process includes FP, backward propagation (BP), and weight update (WU), which leads to a 3X computation operation count with more types of operations [19]. Second, the large volume of activation data in FP needs to be used in BP and WU, and the loss data generated in BP is also required in WU. Such data dependency across multiple layers makes it difficult for on-board memory management and data reusing in dynamic random access memory (DRAM) in an end-to-end training system [20]. Third, since FP, BP, and WU have different memory access patterns, simply using the memory optimizations of FP in the whole training process leads to low memory access efficiency in BP and WU. Because of the above-mentioned challenges, CNN training on FPGAs has not been comprehensively investigated.

Recently, several FPGA-based architectures have been designed to accelerate training on large scale FPGAs. F-CNN [21] first performed FP and BP on a Maxeler MPC-X dataflow FPGA node but WU on CPU. Designs such as [22, 23] aimed to further reduce the CNN training latency and improve throughput. However, these works mainly focused on cloud-level devices with abundant resources. A straightforward training implementation on edge FPGAs is still challenging.

To tackle the challenges in implementing on-device training on edge-level FPGAs, we propose EF-Train, a new efficient FPGA-based training accelerator with a unified channel-level parallelismbased convolution kernel to handle the computation complexity. The unified kernel means that

it processes convolution operations of FP, BP, and WU in the training phase utilizing the same computation resources on the FPGA chip. The channel-level parallelism means that the kernel allocates these computation resources to process multiple channels of feature maps in parallel. We also propose a data reshaping approach to solve the communication bottleneck in realistic end-to-end training processes. The overview of the design framework is shown in Fig. 1. The data reshaping approach is a compile-time optimization that achieves intra-tile and inter-tile memory access continuity and weight reuse in mini-batch training. The proposed design can be implemented on resource-limited FPGAs without sacrificing precision. Neural networks can be trained on both small batches and large batches. Since training and inference are conducted separately in realistic applications, and FPGAs are configurable to implement different designs on the same hardware platform for different applications, our design can be applied to those well-developed FPGA-based inference devices. In a relatively long life cycle of the inference phase, the original design can guarantee high throughput and low latency. If users or the environments change, the device can be switched to implement our design immediately to learn from local data for online adaptation or personalization rather than transmitting data to the cloud centers and waiting for the cloud centers to transmit the well-trained model back to the device. Our main contributions are as follows.

• We propose EF-Train, an efficient FPGA-based CNN training accelerator with a unified convolution kernel to process FP, BP, and WU with full precision. The accelerator exploits channel-level parallelism to achieve high computation utilization for both small and large batch sizes. Our accelerator supports end-to-end CNN training with convolutional (Conv) layers, fully connected (FC) layers, batch normalization (BN) layers, rectified linear unit (ReLU) layers, and pooling layers (Section 3). • We propose a data reshaping approach to solve the off-chip communication bottleneck. The features and weights are stored in off-chip memory with intra-tile continuous memory allocation to remove discontinuous memory accesses within a tile. We also reduce inter-tile discontinuous memory accesses by scheduling loop orders between tiles. We further exploit weight reuse among multiple images in a mini-batch to improve communication efficiency when the batch size is larger than one (Section 4). • We build a performance and resource model for the proposed accelerator. Based on the model, a computation and memory resources scheduling tool is established to determine design parameters for different FPGA devices and different neural networks (Section 5). • We deploy the training process on PYNQ-Z1 and ZCU102 for various CNNs on both Cifar-10 and ImageNet datasets. Experimental results show that our design can achieve 46.99 GFLOPS and 6.09 GFLOPS/W in terms of throughput and energy efficiency, respectively (Section 6).

BACKGROUND AND MOTIVATIONS

CNN Training

The training process of a five-layer CNN is shown in Fig. 2, including the FP process (red arrows), the BP process (black arrows), and the WU process (yellow arrows). The network includes two Conv layers, one FC layer, one BN layer, one ReLU layer, and one pooling layer which are practical and can make up most neural networks in real-world scenarios.

In the FP process, activation is propagated layer by layer. In a Conv layer such as layer 1, the input activation 𝐴1 conducts multiply-accumulate (MAC) operations with the weights 𝑊1. A BN layer is always followed by a Conv layer. In layer 2, the inputs of the BN layer include the input activation 𝐴2 and learnable parameters 𝛾2 and 𝛽2. The immediate outputs include 𝜆2, ˆ𝐴2, and output activation 𝐴3. 𝐴3 then goes through the ReLU and pooling layers. Finally, the FC layer provides classification results for the input image.

Challenges for On-device Training on Edge-level FPGAs

Computation Complexity: • Involves FP, BP, and WU with more types of operations.

Communication Bottleneck: • On-board memory management difficulties. • Low memory access efficiency in FP, BP, and WU

Section 3

Section 4 Data Reshaping Approach

Section 5

Performance and Resource Model

Computation and Memory Resources Scheduling Tool

Unified Channel-level Parallelism-based Convolution Kernel

## (préambule)

**Fig. 1.** Overview of our design framework.

layer 1 layer 3 layer 4 layer 5

A1 Conv

W1

A2 Relu A4 Pool A5 Conv

W5

A6

f Label

L6 Conv L5

Conv

dW5

Pool L4 Relu L2

Conv

dW1

layer 6

FC

W6

FC

FC

dW6

A7

L7

layer 2

BN A3

L3 BN

γ2 β2

λ2 Â2

**Fig. 2.** CNN training process.

In the BP process, the loss will be calculated and propagated back to the first layer. The loss of the last layer is calculated by the loss function 𝑓. This paper adopts the most commonly used cross-entropy loss function. The stochastic gradient descent (SGD) is applied in CNN training. In a Conv layer, layer 5 for example, the loss 𝐿6 needs to be padded first to ensure the size of the convolution results 𝐿5 is the same as the size of 𝐴5. The tensors for weights 𝑊5 are transposed on dimensions for output channels and input channels. The original kernel tensors need to be flipped. Then, 𝐿5 is calculated by the convolution operation between the transposed weights and 𝐿6. In the maximum pooling layer, layer 4, 𝐴4 is compared with 𝐴5 to determine which element on 𝐿4 should obtain the value from the corresponding position on 𝐿5. If layer 4 is an average pooling layer, the values for each element of each patch in 𝐿5 will be directly accumulated and propagated to 𝐿4. In the ReLU layer, layer 3, an element of 𝐿3 will return zero if the value in the same position of 𝐴3 is less than zero. Otherwise, the value of the corresponding position in 𝐿4 will be propagated back. In the BN layer, layer 2, 𝛾2 and 𝛽2 are updated according to the value of 𝜆2, ˆ𝐴2, and 𝐿3. Then the loss is propagated back to 𝐿2.

The gradients of weights in layer 𝑖is calculated after the loss of layer 𝑖+ 1 is propagated. In layer 5, 𝑑𝑊5 is calculated by conducting MAC operations for 𝐴5 and 𝐿6. The gradients are accumulated inside a batch. In a mini-batch, after the above-mentioned operations are conducted for all images, 𝑊5 will be updated by subtracting 𝑑𝑊5 × 𝑙𝑒𝑎𝑟𝑛𝑖𝑛𝑔𝑟𝑎𝑡𝑒.

Related Works

DRAM Access Issues for Current FPGA-based Inference Accelerators: Currently, FPGAs have been widely adopted in edge domains thanks to the well-developed FPGA-based inference accelerators [16, 17]. Among the inference accelerators, many works [16, 24, 25] mainly focused on selecting optimal design parameters to improve the acceleration performance for individual Conv layers. Optimizing techniques such as loop tiling, loop unrolling are adopted by these works. Although the proposed algorithms achieved higher performance efficiency on a given Conv layer, the proposed designs only presented isolated accelerators without completing end-to-end inference where all layers of a neural network are tested continuously. In an end-to-end system, the layers’ intermediate results are usually transferred between on-chip buffer and off-chip DRAM due to the limited on-chip storage size, so the impact of off-chip memory accesses should be considered in realistic scenarios. For most edge-level FPGAs, direct memory access (DMA) is a commonly used effective data swapping way for continuous address data reading. However, in current FPGA-based DNN deployments, when the on-chip memory cannot hold all the features and weights of a Conv layer, data need to be fetched and processed in tiles based on the computation pattern. Such tiling schemes break the continuity of data addresses in DRAM and thus reduce the DMA transmission efficiency. The detailed analysis will be further discussed in Section 4. This discontinuity can degrade the DMA transferring speed from about 8GB/s to around 1GB/s [26]. The optimal algorithms proposed in the above-mentioned accelerators are based on the assumption that data are well pre-allocated between adjacent layers so tiles can be loaded from and stored back to the DRAM continuously. However, in actual end-to-end systems, such allocation overhead is extremely large compared to the acceleration time. Solutions for The DRAM Access Issues in The Inference Phase: Issues related to DRAM memory access have been addressed in recent works. For example, ROMANet [27] proposed a design space exploration (DSE) by searching for the appropriate data partitioning and scheduling for each layer of a network to reduce the number of memory accesses. DRMap [28] proposed a generic DRAM mapping policy and a DSE to reduce the DRAM access latency and energy. These two works were implemented on Tensor Processing Units (TPUs). [29] defined a multi-bank on-chip memory management (MOMM) problem to minimize the DRAM access overhead in the processing of CNNs on a neural processing unit (NPU) with a multi-bank on-chip memory. However, since FPGAs have different hardware architecture with TPUs or NPUs, their optimizing algorithms cannot be directly applied to FPGA-based designs. For example, in the TPU-based designs [27, 28], the architecture of the on-chip accelerator is already fixed, with fixed MAC arrays and fixed on-chip buffers for input features, output features, and weights, respectively. In FPGA-based designs, only the total number of DSPs and on-chip memory sizes are given, and the allocation and connection of MAC arrays and individual buffers are configured by the designer. Therefore, optimizations on FPGA-based designs should not only reduce DRAM access latency or frequency based on the off-chip DRAM access policy but also be comparable to support the on-chip acceleration designs.

A few FPGA-based works reorganized the DRAM layout to relieve the memory access discontinuity and validated the approaches on realistic end-to-end tests. For example, [26] compared three different layout schemes of input features in the inference phase and finally found that the channel-major scheme where the input features are fetched and stored along the input channel direction first could improve access continuity and reduce data duplication. Caffeine [30] combined

both on-chip and off-chip data reorganizations for the convolutional matrix-multiplication representation to maximize the underlying memory bandwidth utilization. FlexCNNe [31] further optimized data layout optimizations on the concatenation layers.

However, all these works [26]-[31] are based on the computation and memory access pattern in the inference phase which only has FP. The training phase involves FP, BP, and WU where their data access pattern for output features, input features, and weights are different. Therefore, the above-mentioned approaches cannot be directly applied in CNN training, and a new optimized design considering FP, BP, and WU together is required. FPGA-based Training Accelerators: As mentioned in Section 1, CNN training on FPGAs has not been comprehensively investigated. The training process is much more complicated than the inference process, so it is sub-optimal to directly adopt the frameworks of inference accelerators for training.

Due to the computation complexity and communication bottleneck, currently, only a few works aim to achieve efficient FPGA-based training. With FPGA clusters, FPDeep explored layer-level parallelism for training a CNN model in a fine-grained pipeline [32], which has superior scalability to a large number of FPGAs. However, such larger clusters are not suitable to be adopted on edgelevel applications. For training on a single FPGA, an automatic compiler for training accelerator on Stratix 10 was developed in the precision of 16-bit fixed-point [22]. DarkFPGA adopted batch-level parallelism using 8-bit integers for training a VGG-like network on the Maxeler MAX5 platform [23]. It achieved high throughput when the batch size is large. A sparse CNN training accelerator was designed on VCU1525. The accelerator was implemented on a pre-trained CNN model with 85% parameters pruned [33]. However, these existing works mainly focused on cloud-level devices with abundant computation and memory resources.

Besides, even with cloud-level resources, reduced precision and pruning approaches have also been utilized to decrease computation intensity and communication bottleneck. Although quantization adopted in prior training accelerators [23, 34] led to remarkable benefits in terms of resource usage and power consumption, these works have not provided any evidence that such quantization techniques can remain high accuracy on a large dataset (e.g. ImageNet) with dense neural networks. Currently, training with full precision is still preferred in most realistic applications, and its high computation and memory overhead should be faced directly. However, none of the above-mentioned state-of-art training accelerators targeted resource-limited edge FPGAs with full precision, which is more challenging to implement end-to-end CNN training but is more practical in real-world scenarios. Therefore, an optimized design is necessary to implement on-device training on resource-limited FPGAs without sacrificing precision. Implementation of BN layers: Apart from the computation-intensive Conv layer, the BN layer is also a key component and is essential for the training process. In inference, a BN layer can be folded into the adjacent CONV layer, since it just performs a simple linear transformation [35]. However, the batch normalization process in the training phase is much more complex. It needs to calculate the expected value and variance of the data in the whole mini-batch, which involves lots of on-chip and off-chip data transmission. Lu et al. [35] optimized the computation flow of BN layers during FP and BP, and implement BN layers in their CNN training accelerator. Unlike [35] which adopts the 8-bit fixed-point in Conv layers and FP16 in BN layers, our work supports BN layers with full precision, which brings more challenges for computation and transmission requirements.

Motivations of The Proposed Design To implement on-device training on resource-limited FPGAs, we need to solve the computation complexity and communication bottleneck illustrated in Fig. 1.

In the training phase, the FP, BP, and WU processes are conducted iteratively and need to be completed on the same accelerator. Edge FPGAs have limited computational resources. Using separate kernels for FP, BP, and WU leads to resource underutilization and low energy efficiency. Therefore, to efficiently process the complex computation for FP, BP, and WU, we need to design a training accelerator that can handle the three processes in a unified convolution kernel and can achieve a high parallelism degree considering the flexibility of DNN architectures. For a Conv layer, there are three levels of parallelism that are adopted in FPGA-based accelerators: batch-level parallelism, feature-map-level parallelism, and channel-level parallelism. Fig. 3 (a) illustrates the process of batch-level parallelism, where 𝑇𝑏nominates the number of output feature maps (OFMs) of images in a mini-batch that are processed in parallel. Fig. 3 (b) shows the process of feature-maplevel parallelism, where 𝑇𝑓×𝑇𝑓features of OFMs are processed in parallel. Fig. 3 (c) shows the process of channel-level parallelism, where 𝑇𝑚nominates the number of output channels of OFMs that are processed in parallel, and 𝑇𝑛nominates the number of input channels of input feature maps (IFMs) that are processed in parallel. The degree of parallelism depends on the amounts of utilized computation units on the hardware. Table 1 shows the comparisons of the three levels of parallelism. Considering a Conv layer with 𝐵images in a mini-batch, it is assumed that the number of input channels is 𝑁, the number of output channels is 𝑀, the size of an OFM is 𝑅×𝐶, and the size of a weights kernel is 𝐾× 𝐾. 𝑇𝑚𝑜𝑝𝑠= 𝐵× 𝑀× 𝑁× 𝑅×𝐶× 𝐾× 𝐾multiply operations are required to process such a layer. For the batch-level parallelism, it takes ⌈𝐵

𝑇𝑏⌉× 𝑀× 𝑁× 𝑅× 𝐶× 𝐾× 𝐾 cycles to complete the Conv layer. Such parallelism can achieve high throughput when the batch size is large, and the size of the feature map and the number of channels have little impact on the performance. For example, in previous works, DarkFPGA [23] built its accelerator with batch-level parallelism and achieved high throughput when the batch size is 128. However, when the batch size is small or even 1 (online learning), most computation units will remain idle. For example, when 𝐵< 𝑇𝑏, completing the Conv layer costs 𝑇𝑚𝑜𝑝𝑠cycles, and 𝑇𝑏−𝐵

𝑇𝑏 of computation resources remain idle. It leads to a low parallelism degree and such under-utilization of resources makes the performance sub-optimal. For the feature-map-level parallelism which has been adopted by works like [22], it takes 𝐵× 𝑀× 𝑁× ⌈𝑅

𝑇𝑓⌉× ⌈𝐶

𝑇𝑓⌉× 𝐾× 𝐾cycles to finish a Conv layer. The batch size and the number of channels have little impact on such parallelism. The parallelism will benefit from layers with large feature map size but has under-utilization for layers with small feature map size. For example, when 𝑅< 𝑇𝑓and 𝐶< 𝑇𝑓, completing the Conv layer costs 𝑇𝑚𝑜𝑝𝑠cycles, and

𝑇𝑓−𝑅

𝑇𝑓 × 𝑇𝑓−𝐶

𝑇𝑓 of computation resources will remain idle. However, in CNN training, the size of a feature map may vary from large size (like 224 × 224 for the input image of the ImageNet) to 1 × 1 for the FC layer. The feature-map-level parallelism will be inefficient to process the layers with a small feature map. For channel-level parallelism, it takes 𝐵× ⌈𝑀

𝑇𝑚⌉× ⌈𝑁

𝑇𝑛⌉× 𝑅× 𝐶× 𝐾× 𝐾cycles to complete the Conv layer. It acquires a high parallelism degree with a large channel number, and the batch size and feature map size have little impact on it. When the channel number is small, for example, when 𝑁< 𝑇𝑛, completing the Conv layer costs 𝐵× ⌈𝑀

𝑇𝑚⌉× 𝑁× 𝑅× 𝐶× 𝐾× 𝐾 cycles, and 𝑇𝑛−𝑁

𝑇𝑛 of computation resources will remain idle. However, for most neural networks, only the first layer has a small input channel number (𝑁= 3). For other layers, the channel size (for example 32, 64, etc.) is usually larger than the maximum degree of parallelism that an edge FPGA can achieve. Therefore, channel-level parallelism is widely adopted by FPGA-based inference accelerators [16, 24]. Generally speaking, the channel-level parallelism can achieve a constantly high degree of parallelism across multiple layers, so it is adopted in the proposed design as shown in Fig. 1. The proposed accelerator with a channel-level parallelism-based convolution kernel to process FP, BP, and WU will be introduced in detail in Section 3.

OFM of Image 1 OFM of Image Tb

Tb

Tf

OFM of An Image IFM of An Image

OFM of An Image

**Fig. 3.** Three levels of parallelism. (a) Batch-level parallelism, (b) Feature-map-level parallelism, (c) Channellevel parallelism.

**Table 1.** Comparisons of the three levels of parallelism

Parallelism Batch-level Parallelism

Feature-map-level

Parallelism

Channel-level

Parallelism

Large Batch Size advantaged little impact little impact Small Batch Size disadvantaged little impact little impact Large Feature Map Size little impact advantaged little impact Small Feature Map Size little impact disadvantaged little impact Large Channel Number little impact little impact advantaged Small Channel Number little impact little impact disadvantaged

Furthermore, the communication bottleneck is also challenging for edge-level FPGAs in endto-end training. As illustrated in Fig. 2, the activation data in FP needs to be used in BP and WU, and the loss data generated in BP is also required in WU. The length and heterogeneity of the data dependency paths in different layers make external memory accesses inevitable [20]. Previous training accelerators attempted to avoid external memory accesses. For example, FPDeep [32] scaled CNN computations to larger clusters so that only on-chip memory is needed for the CONV layers. However, such larger clusters cannot be used on edge devices. [36] implemented LeNet-10 on an FPGA and stored the inputs and outputs of one layer on the chip. Such design can only support small networks, but for many larger networks (e.g. Vgg-16, AlexNet, etc.), the on-chip memory of an edge FPGA is not big enough to hold weights or features in every Conv layer. Therefore, several works [23, 33, 34] applied quantization or pruning to reduce off-chip memory access. However, unlike inference where compressed networks cause little accuracy decrease [37], these training works have not proved that their compression techniques can remain high accuracy on large datasets with dense networks. To guarantee accuracy, it is necessary to implement CNN training with full precision. Our goal is to design a general accelerator supporting end-to-end training with both dense and small networks without sacrificing precision, so it is necessary to appropriately manage external memory access and allocate on-chip buffers. As mentioned in Section 2.2, the tiling schemes involved in on-chip accelerator design break the continuity of data addresses in DRAM and thus reduce the DMA transmission efficiency. Therefore, it is necessary to improve the address continuity of data to improve the efficiency of data swapping considering the complex data patterns in FP, BP, and WU altogether. To solve this communication issue, as shown in Fig. 1, a data reshaping approach is proposed and will be introduced in detail in Section 4.

FPGA-BASED CNN TRAINING ACCELERATOR

In this section, we propose an FPGA-based accelerator exploiting channel-level parallelism to deal with the training process. A unified convolution kernel is designed to process FP, BP, and WU with full precision.

The Architecture of The Training Accelerator

The proposed training accelerator is shown in Fig. 4. We implement our accelerator on an end-toend training system. At first, the CPU transmits labels, initial weights, the activation data of the first layer, layer parameters, initial parameters for BN layers, and the DMA start addresses for each layer to the off-chip DRAM. The layer parameters include computation type (e.g. Conv, ReLU, BN, or pooling) and the shape information. The DMA start addresses are calculated off-line according to the off-chip memory layout based on our data reshaping approach mentioned in Section 4. Our accelerator executes computation-intensive kernels based on data dependencies within a CNN model, while the entropy loss function is computed on the off-chip ARM core.

Weights

Off-chip Memory (DRAM)

Activation data Loss data Labels Indexes

IFM DMA

WEI DMA

OFM DMA OUT DMA

IFM buffer

Weight

buffer Pooling Indexes

OFM buffer

Pooling

Kernel

Conv Kernel

PE PE PE

PE PE PE

PE PE PE

On-Chip Memory and Data Flow IFM

Weights

Tm×Tn

IFM

OFM

Weights Tm×Tn

②

OFM

①

Labels, Initial weights, Activation data of the first layer, Initial

BN parameters, Layer parameters, DMA start addresses CPU

BN Kernel

BN Parameters

Parameters

for BN

**Fig. 4.** Accelerator architecture.

As illustrated in Fig. 4, the off-chip memory (DRAM) stores data for activation, loss, weights, labels, indexes for pooling, and parameters for BN. Data are transmitted through the DMA AXIstream bus to on-chip memory for computation. There are 4 DMA stream channels: IFM DMA, OFM DMA, WEI DMA, and OUT DMA. These 4 channels are independent and can work in parallel. On the FPGA chip, a unified Conv kernel is designed to process FP, BP, and WU with the same computation resources, i.e. the digital signal processors (DSPs). The Conv kernel is composed of multiple processing elements (PEs) to implement MAC operations. The adder tree structure is adopted for the proposed kernel since it is flexible to support different computation patterns for FP, BP, and WU. The connection of each multiplier and adder for FP and BP is shown in 1○of Fig. 4, while the connection of each multiplier and adder for WU is shown in 2○of Fig. 4. The Pooling Kernel focuses on the pooling operation. The BN Kernel achieves batch normalization and updates BN parameters during FP and BP. ReLU is always followed by a Conv or BN layer. The accelerator compares the output features with 0 when storing output features back to the DRAM in Conv or BN layers, so ReLU does not need a unique functional unit. Five types of on-chip block RAMs (BRAMs) are used to buffer IFMs, weights or weights gradients, OFMs, pooling indexes, and BN

**Table 2.** Definitions of Symbols

Notation Description

𝑖,𝑗 Index of a Conv layer 𝑁𝑖 Number of the input channels of the 𝑖th Conv layer Number of the output channels of the 𝑖th Conv layer Number of the rows of the OFMs for the 𝑖th Conv layer Number of the columns of the OFMs for the 𝑖th Conv layer 𝐾𝑖 Size of the weights kernel for the 𝑖th Conv layer 𝑆𝑖 Stride for the 𝑖th Conv layer 𝐴𝑖[𝑏,𝑚,𝑟,𝑐] Activation for the 𝑖th Conv layer in FP 𝐿𝑖[𝑏,𝑛,𝑟,𝑐] Loss for the 𝑖th Conv layer in BP 𝑊𝑖[𝑛,𝑚,𝑘𝑟,𝑘𝑐] Weights for the 𝑖th Conv layer 𝑑𝑊𝑖[𝑛,𝑚,𝑘𝑟,𝑘𝑐] Weights gradients for the 𝑖th Conv layer in WU 𝑇𝑚 Number of the output channels in a tile of output features in each Conv layer 𝑇𝑛 Number of the input channels in a tile of input features in each Conv layer 𝑇𝑟𝑖 Number of the rows in a tile of output features in the 𝑖th Conv layer 𝑇𝑐𝑖 Number of the columns in a tile of output features in the 𝑖th Conv layer 𝑀𝑖_𝑜𝑛 Number of the output channels of the weights that stored on-chip in the 𝑖th Conv layer 𝑅𝑗_𝑖𝑛 Number of the rows of the IFMs for the 𝑗th Conv layer 𝐶𝑗_𝑖𝑛 Number of the columns of the IFMs for the 𝑗th Conv layer 𝑇𝑟𝑗_𝑖𝑛 Number of the rows in a tile of input features in the 𝑗th Conv layer 𝑇𝑐𝑗_𝑖𝑛 Number of the columns in a tile of input features in the 𝑗th Conv layer

parameters. We adopt double-buffer designs so that data transmission and computation can be conducted in parallel.

The Forward and Backward Propagation of A Convolutional Layer

Our accelerator adopts channel-level parallelism, loop unrolling, and loop tiling. The symbols are defined in Table 2. In channel-level parallelism,𝑇𝑛and𝑇𝑚are determined by available computation resources (i.e. DSPs) on the FPGA chip and are fixed for all Conv layers. The degree of parallelism is determined by 𝑇𝑛×𝑇𝑚.

Our accelerator achieves SGD in CNN training. The forward and backward propagation processes of a Conv layer processing the 𝑏th image in a mini-batch can be formulated in Eq. (1) and (2), where 𝑊′

𝑖is the transposed and flipped tensor of 𝑊𝑖. As illustrated in 1○of Fig. 4, in FP and BP, the Conv Kernel conducts MAC operations for weights and input features from activation or loss. The IFM buffer stores a tile of activation or loss transmitted via the IFM DMA channel, and the Weight buffer stores weights transmitted via the WEI DMA channel. The OFM buffer stores a tiled of MAC outcomes. Computation results are transmitted to the DRAM via the OUT DMA channel. If a Conv layer is followed by a ReLU layer, for FP, the data in the OFM buffer will be compared with 0 before entering into the OUT DMA channel. For BP, the activation of the previous layer will be transmitted via the OFM DMA channel, and the accelerator decides which value should be

propagated according to Eq. (3).

𝐴𝑖+1[𝑏,𝑚,𝑟,𝑐] =

𝑁𝑖 ∑︁

𝑛=1

𝐾𝑖 ∑︁

𝑘𝑟=1

𝐾𝑖 ∑︁

𝑘𝑐=1

𝐴𝑖[𝑏,𝑛,𝑆𝑖× 𝑟+ 𝑘𝑟,𝑆𝑖× 𝑐+ 𝑘𝑐] ×𝑊𝑖[𝑚,𝑛,𝑘𝑟,𝑘𝑐]

𝐿𝑖[𝑏,𝑛,𝑟,𝑐] =

∑︁

𝑚=1

𝐾𝑖 ∑︁

𝑘𝑟′=1

𝐾𝑖 ∑︁

𝑘𝑐′=1

𝐿𝑖+1[𝑏,𝑚,𝑆𝑖× 𝑟+ 𝑘𝑟′,𝑆𝑖× 𝑐+ 𝑘𝑐′] ×𝑊′

𝑖[𝑛,𝑚,𝑘𝑟′,𝑘𝑐′]

𝐿𝑖[𝑏,𝑚,𝑟,𝑐] =

(

𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐], 𝐴𝑖[𝑏,𝑚,𝑟,𝑐] > 0, 0, 𝑜𝑡ℎ𝑒𝑟𝑠

The Weight Update of A Convolutional Layer The gradients of weights can be calculated in Eq. (4). The generated hardware implementation of the PE architecture processing WU operations in the Conv kernel is shown in 2○of Fig. 4. During the WU, the Conv Kernel conducts MAC operations for the activation data transmitted via the IFM DMA channel and the loss data transmitted via the OFM DMA channel. The gradients are stored in the Weight buffer. Once the Conv Kernel completes the computation for the last image in a mini-batch, the original weights are transmitted via the WEI DMA channel. Then, weights are updated by deducting the product of the gradients and learning rate. New weights are sent back to DRAM via the OUT DMA channel.

𝑑𝑊𝑖[𝑚,𝑛,𝑘𝑟,𝑘𝑐] =

∑︁

𝑏=1

∑︁

𝑟=1

∑︁

𝑐=1

𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐] × 𝐴𝑖[𝑏,𝑛,𝑆𝑖× 𝑟+ 𝑘𝑟,𝑆𝑖× 𝑐+ 𝑘𝑐]

The Forward and Backward Propagation of A Pooling Layer In the FP process of a pooling layer, the activation is transmitted via the IFM DMA channel and stored in the IFM buffer. In the maximum pooling, the Pooling Kernel compares adjacent pixels, transfers the results back to DRAM via the OUT DMA channel, and records the index for the maximal pixel into the Pooling Indexes buffer. The index of a pixel is a 2-bit integer. For average pooling, the kernel just calculates the average value of a patch of features. In the BP process of maximum pooling, the indexes are loaded back via the WEI DMA channel, and loss from the previous layer is loaded via the IFM DMA channel. The Pooling Kernel compares the indexes and stores the propagated value into the IFM buffer. The BP process of the maximum pooling is formulated in Eq. (5). For average pooling, the loss values of a patch are directly accumulated. After a tile of data is processed, the calculated loss is sent back via the OUT DMA channel.

𝐿𝑖[𝑏,𝑚,𝑆𝑖×𝑟+𝑘𝑟,𝑆𝑖×𝑐+𝑘𝑐] =

(

𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐],𝐴𝑖+1[𝑏,𝑚,𝑟,𝑐] = 𝐴𝑖[𝑏,𝑚,𝑆𝑖× 𝑟+ 𝑘𝑟,𝑆𝑖× 𝑐+ 𝑘𝑐], 0,𝑜𝑡ℎ𝑒𝑟𝑠

The Forward Propagation of A BN Layer Our BN kernel is based on the computation flow in [35]. However, unlike the prior work which utilizes half-precision, we adopt full precision which brings more computation and transmission challenges. The BN parameters in Fig. 4 includes learnable parameters 𝛾𝑖[𝑚] and 𝛽𝑖[𝑚] and immediate parameters 𝜆𝑖[𝑚] and ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐], where 𝑚is the index of the channel. The 𝛾𝑖[𝑚] and 𝛽𝑖[𝑚] are used to generate the immediate parameters and the output activation 𝐴𝑖+1[𝑏,𝑚,𝑟,𝑐] during FP. During BP, the immediate parameters and the loss propagated from the next layer 𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐]

are used to update the learn parameters and propagate the loss 𝐿𝑖[𝑏,𝑚,𝑟,𝑐] back. Since the size of 𝛾𝑖[𝑚], 𝛽𝑖[𝑚], and 𝜆𝑖[𝑚] is 𝑀(the number of the output channels), the on-chip BRAMs are large

enough to hold these data in a BN layer. Therefore, we use the BN Parameters buffer to store these parameters as well as the expected value and variance. The ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐] is transmitted to DRAM together with 𝐴𝑖+1[𝑏,𝑚,𝑟,𝑐].

In FP, the BN Kernel first loads 𝛾𝑖[𝑚] and 𝛽𝑖[𝑚] from DRAM to the BN Parameters buffer via the WEI DMA channel. Then it loads 𝐴𝑖[𝑏,𝑚,𝑟,𝑐] via the IFM DMA channel and calculates the expected value 𝐸(𝑋)𝑖[𝑚] and variance 𝑉(𝑋)𝑖[𝑚] according to Eq. (6)-(8). To avoid disarranging the DRAM data layout for adjacent Conv layers, we load data tile by tile using the same data format as that in Conv layers. The expected value and variance are calculated after the entire data of a mini-batch is accessed. Then input activation is loaded from the beginning to calculate the immediate parameters according to Eq. (9) and Eq. (10), where 𝜖is a constant parameter. 𝜆𝑖[𝑚] is stored in the BN Parameters buffer, while ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐] is transmitted to DRAM via the OUT channel in parallel with activation loading. Finally, the output activation is calculated according to Eq. (11). The BN operation completes after the activation, 𝛾𝑖[𝑚], 𝛽𝑖[𝑚], and 𝜆𝑖[𝑚] are stored to DRAM.

𝐸(𝑋)𝑖[𝑚] = 𝐵× 𝑅𝑖× 𝐶𝑖

∑︁

𝑏=1

∑︁

𝑟=1

∑︁

𝑐=1

𝐴𝑖[𝑏,𝑚,𝑟,𝑐]

𝐸(𝑋2)𝑖[𝑚] = 𝐵× 𝑅𝑖× 𝐶𝑖

∑︁

𝑏=1

∑︁

𝑟=1

∑︁

𝑐=1

𝐴2

𝑖[𝑏,𝑚,𝑟,𝑐]

𝑉(𝑋)𝑖[𝑚] = 𝐸(𝑋2)𝑖[𝑚] −(𝐸(𝑋)𝑖[𝑚])2

𝜆𝑖[𝑚] = √︁

𝑉(𝑋)𝑖[𝑚] + 𝜖

ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐] = (𝐴𝑖[𝑏,𝑚,𝑟,𝑐] −𝐸(𝑋)𝑖[𝑚]) × 𝜆𝑖[𝑚]

𝐴𝑖+1[𝑏,𝑚,𝑟,𝑐] = ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐] × 𝛾𝑖[𝑚] + 𝛽𝑖[𝑚]

The Backward Propagation of A BN Layer

In BP, ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐], 𝜆𝑖[𝑚] and 𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐] are used to update the learnable parameters 𝛾𝑖[𝑚] and 𝛽𝑖[𝑚], and 𝐿𝑖[𝑏,𝑚,𝑟,𝑐] is propagated back. 𝜆𝑖[𝑚], 𝛾𝑖[𝑚], and 𝛽𝑖[𝑚] are first uploaded via the WEI channel and stored in the BN Parameters buffer. Then, the BN Kernel loads ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐] and 𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐] via the IFM and OFM channel respectively to calculate the gradients for 𝛾𝑖[𝑚] and 𝛽𝑖[𝑚] according to Eq. (12) and (13). The learnable parameters are updated by deducting the gradients, while 𝐿𝑖[𝑏,𝑚,𝑟,𝑐] is calculated according to Eq. (14).

𝑑𝛾𝑖[𝑚] =

∑︁

𝑏=1

∑︁

𝑟=1

∑︁

𝑐=1

𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐] × ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐]

𝑑𝛽𝑖[𝑚] =

∑︁

𝑏=1

∑︁

𝑟=1

∑︁

𝑐=1

𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐]

𝐿𝑖[𝑏,𝑚,𝑟,𝑐] = 𝛾𝑖[𝑚] × 𝜆𝑖[𝑚] × (𝐿𝑖+1[𝑏,𝑚,𝑟,𝑐] − 𝑑𝛽𝑖[𝑚] 𝐵× 𝑅𝑖× 𝐶𝑖−ˆ𝐴𝑖[𝑏,𝑚,𝑟,𝑐] × 𝑑𝛾𝑖[𝑚] 𝐵× 𝑅𝑖× 𝐶𝑖) (14)

DATA RESHAPING APPROACH In this section, we propose a data reshaping approach to solve the communication bottleneck between the on-chip buffer and off-chip memory in realistic end-to-end training processes. We first analyze the discontinuous memory access for the isolate accelerator with the unified channellevel parallelism-based Conv kernel proposed in Section 3. Then we introduce our data reshaping approach which involves three aspects. We first achieve intra-tile continuous memory allocation by reorganizing the DRAM layouts for input features, output features, and weights. Then, we re-schedule the loop order to achieve inter-tile continuous memory allocation. These two parts are optimized together. Finally, considering the training process involves convolution operations among a mini-batch, we propose and apply a weight reuse strategy based on the proposed data layout.

Analysis on Discontinuous Memory Access The pseudo-code of a tiled convolution layer is shown in Fig. 5. The pseudo-code in Fig. 5 (a) is applied in FP and BP, following previous FPGA-based inference works [16, 30], while the pseudocode in Fig. 5 (b) is applied in WU, based on the accelerator design proposed in Section 3. As discussed in Section 2, the continuity of data significantly influences the DMA transmission efficiency. In this section, we analyze the data discontinuity when features are placed with the BCHW pattern and the BHWC pattern, where B represents batch, C represents channel, H represents height (row), and W represents width (column).

1. for (row=0; row<R; row+=Tr){ 2. for (col=0; col<C; col+=Tc){ 3. for (to=0; to<M; to+=Tm){ 4. for (ti=0; ti<N; ti+=Tn){

5. for(i=0; i<K; i++){ 6. for(j=0; j<K; j++){ 7. for(trr=0; trr<Tr; trr++){ 8. for(tcc=0; tcc<Tc; tcc++){ 9. for(too=0; too<Tm; too++){ 10. for(tii=0; tii<Tn; tii++){ OFM[too][trr][tcc] += WEI[too][tii][i][j]*IFM[tii][S*trr+i][S*tcc+j] }}}}}}}}}}

Off-chip data transmission

On-chip computation

1. for (to=0; to<M; to+=Tm){ 2. for (ti=0; ti<N; ti+=Tn){ 3. for (row=0; row<R; row+=Tr){ 4. for (col=0; col<C; col+=Tc){

5. for(trr=0; trr<Tr; trr++){ 6. for(tcc=0; tcc<Tc; tcc++){ 7. for(i=0; i<K; i++){ 8. for(j=0; j<K; j++){ 9. for(too=0; too<Tm; too++){ 10. for(tii=0; tii<Tn; tii++){ WEI[too][tii][i][j] += OFM[too][trr][tcc]*IFM[tii][S*trr+i][S*tcc+j] }}}}}}}}}}

Off-chip data transmission

On-chip computation

**Fig. 5.** Pseudo-code of a tiled convolution layer. (a) Pseudo-code for FP and BP, (b) Pseudo-code for WU.

Features are placed in the BCHW pattern: Fig. 6 (a) shows the data layout of 𝑀𝑖×𝑅𝑖×𝐶𝑖output features stored in DRAM for the 𝑖th layer. The output features are placed with the BCHW pattern commonly used in CNN accelerating CPU, and GPU platforms [38, 39]. While OpenVINO [39] is primarily for CPUs, it would also work for CPU, GPU, and FPGA platforms. In this layout, a cube represents an element of the features, and the indexes represent the orders of the elements stored in DRAM. In FPGA-based DNN deployments, data are fetched and processed in tiles. As shown in Fig. 6, the size of a tile is 𝑇𝑚×𝑇𝑟𝑖×𝑇𝑐𝑖for output features.

The output features of layer 𝑖are also the input features for its next layer 𝑗. As shown in Fig. 7 (a), the size of the input features in layer 𝑗is 𝑁𝑗× 𝑅𝑗_𝑖𝑛× 𝐶𝑗_𝑖𝑛. For input features, the size of a tile is 𝑇𝑛×𝑇𝑟𝑗_𝑖𝑛×𝑇𝑐𝑗_𝑖𝑛.

Tci

Z

Burst length=Tci

Burst length=Tci

**Fig. 6.** Data layout of output features before reshaping. (a) Data stored in DRAM, (b) Data transmitted via the OUT DMA channel in FP/BP, (c) Data transmitted via the OFM DMA channel in WU.

Burst length=Tcj_in

Tcj_in

repeat times

110 111 ...

Burst length=Tcj_in

Z

**Fig. 7.** Data layout of input features before reshaping. (a) Data stored in DRAM, (b) Data transmitted via the IFM DMA channel in FP/BP, (c) Data transmitted via the IFM DMA channel in WU.

repeat times

repeat times

Burst length=Tn

(d)

Burst length=Tm

Burst length=Tn

FP:

**Fig. 8.** Data layout of weights before reshaping. (a) Weights stored in DRAM, (b) Weights transmitted via the WEI DMA channel in FP, (c) Weights transmitted via the WEI DMA channel in BP, (d) Weights transmitted via the OUT DMA channel in WU.

In each DMA stream, the AXI-stream bus allows a pipeline data stream when the data addresses are continuous. Burst length represents the number of data with continuous addresses in the data

stream. When a discontinuity happens, the DMA needs to be restarted. Therefore, our goal is to avoid discontinuity, i.e. elongate the burst length for different transmission patterns.

During FP, the Conv Kernel conducts MAC operations with weights and input features, and then it generates output features. The output features are transmitted to the DRAM via the OUT DMA channel, which is shown in Fig. 6 (b). For the next layer, the input features are fetched from DRAM to the FPGA chip via the IFM DMA stream, which is shown in Fig. 7 (b). As illustrated in Fig. 5 (a), in a Conv layer, the OFM buffer is reused to store and accumulate the immediate convolution results between each tile of input features and each tile of weights. The first tile of output features is generated by accumulating the convolution results when the input features tiles move from the first input channel to the last channel. It corresponds to the movement in the X direction in Fig. 7. Then, the next tiles of output features are generated in the X direction in Fig. 6, so the data access pattern of input features (the dashed box in Fig. 7 (b)) repeats ⌈𝑀

𝑇𝑚⌉times. After the output features tiles move from the first output channel to the last output channel, they begin to move in the Z direction, and the input features tiles follow the Z direction as well. From Fig. 6 (b) and Fig. 7 (b), the address of data is discontinuous for both inside and outside of a tile. The burst length of the output features in the 𝑖th layer is 𝑇𝑐𝑖, and the burst length of the input features in the 𝑗th layer is 𝑇𝑐𝑗_𝑖𝑛. The data movement in BP is similar to that in FP.

In WU, the data access pattern inside a tile is the same as that in FP/BP. However, the inter-tile data access pattern is different from that for FP/BP. It is because, in WU, the Conv Kernel conducts MAC operations for input features (the activation data transmitted via the IFM DMA channel) and output features (the loss data transmitted via the OFM DMA channel) to calculate weight gradients. Therefore, as shown in Fig. 5 (b), the WEI buffer is reused to store and accumulate the immediate convolution result between each tile of input features and each tile of output features. The first tile of weight gradients is generated when the input and output features tiles move from the first row and the first column to the last row and the last column. It corresponds to the movement in the Z direction in Fig. 6 and Fig. 7. Then, the next tile of weight gradients is generated along the input channel direction. The tiles of input features move along the X direction, while the pattern of output feature tiles (the dashed box in Fig. 6 (c)) repeats ⌈𝑁

𝑇𝑛⌉times. After the gradients of weights are calculated from the first input channel to the last input channel, the next tiles are generated along the output channel direction. Thus, the pattern of input feature tiles (the dashed box in Fig. 7 (c)) repeats ⌈𝑀

𝑇𝑚⌉times, while the output feature tiles move along the X direction. As shown in Fig. 7 (c), the burst length for input features is 𝑇𝑐𝑗_𝑖𝑛. As shown in Fig. 6 (c), the burst length for output features is 𝑇𝑐𝑖.

In CNN training, the data layout of weights is also more complex compared to the inference process. As illustrated in Fig. 8 (a), 𝑀𝑖× 𝑁𝑖× 𝐾𝑖× 𝐾𝑖weights of layer 𝑖are stored in DRAM. In FP, weights are fetched in the input channel first and then the output channel when the output features are generated along the X direction in Fig. 6. Then, the output features are generated along the Z direction, while the weights access pattern (the dashed box in Fig. 8 (a)) repeats ⌈𝑅

𝑇𝑟⌉× ⌈𝐶

𝑇𝑐⌉ times. WU shares the same intra-tile weights access pattern with FP, but it does not need to repeat during inter-tile data access. The burst lengths for FP and WU are both 𝑇𝑛. In BP, each 𝐾𝑖× 𝐾𝑖

kernel needs to be flipped. Such reallocation can be processed on the FPGA chip. However, since the numbers of input channels and output channels are interchanged, the memory access pattern of a tile is also changed. The weights kernels are transposed between the input channel dimension and the output channel dimension. In Fig. 8, the yellow cubes represent a tile of weights in FP and WU, and the cubes with the red box represent a tile of weights in BP. As illustrated in Fig. 8 (c), in BP, the number of output channels becomes 𝑀𝑖′ = 𝑁𝑖, the number of input channels becomes 𝑁𝑖′ = 𝑀𝑖, and the burst length is 𝑇𝑚.

Features are placed in the BHWC pattern: As can be seen from Fig. 6, Fig. 7, and Fig. 8, the tiled data breaks the data continuity of memory access in FP, BP, and WU for the isolate accelerator. In FPGA-based inference works, the BHWC pattern is also commonly used in end-to-end designs to optimize memory access [26, 30]. Fig. 9 (a) and Fig. 10 (a) show the data layout of features placed in the BHWC pattern following previous inference-based works. According to the loop order in Fig. 5 (a), in FP and BP, tiles move in the channel dimension first and then move in the Z direction. Therefore, it is effective to fetch ⌈𝑁

𝑇𝑛⌉tiles of input features to the on-chip memory and reuse the data after ⌈𝑀

𝑇𝑚⌉tiles of output features are calculated. With such optimizations, the data discontinuity of features is alleviated in FP and BP. As shown in Fig. 9 (b) and Fig. 10 (b), the burst length for output features is 𝑀𝑖×𝑇𝑐𝑖, and the burst length for input features is 𝑁𝑗×𝑇𝑐𝑗_𝑖𝑛. Besides, the FPGA accelerator does not need to repeatedly load the input feature tiles from the DRAM.

However, in WU, the Conv Kernel conducts MAC operations for input features and output features to calculate weight gradients, so input and output feature tiles should move in the Z direction first to calculate the weight gradients of 𝑇𝑚×𝑇𝑛weights kernels and then move in the channel direction, which is illustrated in Fig. 5 (b). Therefore, features cannot be continuously fetched to the on-chip buffer and reused as that in the inference phase unless the on-chip memory is large enough to hold all features of each layer. When the on-chip memory cannot hold all features of a Conv layer in resource-limited FPGAs, the burst length for output features is 𝑇𝑚, and the burst length for input features is 𝑇𝑛. The data layouts are shown in Fig. 9 (c) and Fig. 10 (c).

In CNN inference, weights will not change in the whole process, and they are loaded in the same pattern for different layers. Therefore, in the inference phase, weights can be pre-allocated tile by tile to ensure continuous memory access. The pre-allocated data layout is illustrated in Fig. 11 (a). As shown in Fig. 11 (b) and Fig. 11 (d), the burst length is 𝑀𝑖× 𝑁𝑖in FP and WU. However, as illustrated in Fig. 11 (c), the weight kernels are transposed between the input channel dimension and the output channel dimension, and the tiling scheme in BP breaks the memory access continuity. Since weights are updated after one iteration of FP, BP, and WU, it is impossible to pre-allocate them before each iteration. Therefore, data discontinuity is inevitable in BP. As shown in Fig. 11, the burst length is 𝑇𝑚.

Optimizing Discontinuous Memory Access

To optimize the discontinuous memory access, our data reshaping approach includes the following steps. Firstly, we achieve intra-tile continuous memory allocation for both features and weights by reorganizing the DRAM layouts for output features, input features, and weights which are shown in Fig. 12, Fig. 13, and Fig. 14 respectively. Then we schedule the loop order based on the pseudo-code in Fig. 15 to achieve inter-tile continuous memory allocation. Finally, weights are reused among a mini-batch based on the proposed data layouts. In this section, we reorganize the data layouts and schedule the loop order together to achieve both intra-tile and inter-tile continuous memory address allocation. Intra-Tile Continuous Memory Allocation: Inspired by previous inference works [26, 30], employing channel-last data layout can improve data continuity for the channel-level parallelismbased accelerator. However, as explained in Section 4.1, simply changing the data layout cannot optimize the memory access continuity in FP, BP, and WU together. The memory access patterns in the three processes need to be considered together. In CNN inference, the selection of 𝑇𝑚and 𝑇𝑛is flexible. However, to ensure data continuity of weights kernels in both FP and BP, we fix 𝑇𝑚= 𝑇𝑛 in our training accelerator so that weights can be loaded tile by tile in both FP and BP.

**Fig. 12** (a) shows the data layout of the output features in DRAM after data reshaping. The first 𝑇𝑚channels of OFMs are placed in the row-column-channel pattern. The next 𝑇𝑚channels of

Tci

Z

Burst length=Mi×Tci

Burst length=Tm

**Fig. 9.** Data layout of output features with the BHWC memory allocation and feature reuse. (a) Data stored in DRAM, (b) Data transmitted via the OUT DMA channel in FP/BP, (c) Data transmitted via the OFM DMA channel in WU.

Burst length=Nj×Tcj_in

Tcj_in

11 ... 57 58 59

Burst length=Tn

Z

13 14 15 16

**Fig. 10.** Data layout of input features with the BHWC memory allocation and feature reuse. (a) Data stored in DRAM, (b) Data transmitted via the IFM DMA channel in FP/BP, (c) Data transmitted via the IFM DMA channel in WU.

repeat times

repeat times

(d)

Burst length=Tm

FP:

**Fig. 11.** Data layout of weights placed tile by tile based on inference-based data flow. (a) Weights stored in DRAM, (b) Weights transmitted via the WEI DMA channel in FP, (c) Weights transmitted via the WEI DMA channel in BP, (d) Weights transmitted via the OUT DMA channel in WU.

OFMs are followed with the same pattern. When applying loop tiling, we assign the tiling parameter

𝑇𝑐𝑖= 𝐶𝑖so that data are continuous inside a tile for both FP and WU. From Fig. 12 (b) and (c), the

burst lengths of output features during FP, BP, and WU are larger than the size of a tile.

Burst length=Mi×Ri×Ci

Burst length=Tm×Ri×Ci

Tci=Ci

37 39 41 43 45 47

... 48

**Fig. 12.** Data layout of output features after reshaping. (a) Data stored in DRAM, (b) Data transmitted via the OUT DMA channel in FP/BP, (c) Data transmitted via the OFM DMA channel in WU.

Burst length=Tn×Trj_in×Tcj_in

Burst length=Tn×Trj_in×Tcj_in

Tcj_in=Cj_in

repeat times

... 108

repeat times

1 2 ...

DRAM：

**Fig. 13.** Data layout of input features after reshaping. (a) Data stored in DRAM, (b) Data transmitted via the IFM DMA channel in FP/BP, (c) Data transmitted via the IFM DMA channel in WU.

WEI/OUT DMA stream

Burst length=Tm×Tn

DRAM：

FP/WU:

**Fig. 14.** Data layout of weights after reshaping. (a) Weights stored in DRAM, (b) Weights transmitted via the WEI/OUT DMA channel in FP/WU, (c) Weights transmitted via the WEI DMA channel in BP.

The selection of 𝑇𝑚= 𝑇𝑛, 𝑇𝑐𝑖= 𝐶𝑖, and 𝑇𝑐𝑖_𝑖𝑛= 𝐶𝑖_𝑖𝑛also guarantee that features of different layers share similar data layouts and tiling schemes no matter they serve as output features or input features of a Conv layer in FP/BP/WU. Therefore, the intra-tile continuity of input features is also guaranteed. The data layout of the input features in DRAM for the 𝑗th layer is shown in Fig. 13 (a). According to Fig. 13 (b) and (c), the burst length equals the size of a tile.

After selecting 𝑇𝑚= 𝑇𝑛, weights can be placed and fetched tile by tile during FP, BP, and WU. The data layout is illustrated in Fig. 14. Before data reshaping, weights need to be repeatedly

transmitted between the FPGA chip and the DRAM in FP and BP, which is inefficient especially for mini-batch training. Therefore, weight reuse based on our unique data layout is necessary which will be introduced in detail in Section 4.3. After reshaping, the burst length for FP and WU is 𝑀𝑖× 𝑁𝑖, while the burst length for BP is 𝑇𝑚×𝑇𝑛, which are shown in Fig. 14 (b) and (c), respectively. Inter-Tile Loop Order Optimization: The proposed data reshaping approach also achieves intertile data continuity by rescheduling the loop order in Fig. 5. The loop order of 1, 2, and 3 in Fig. 5 (a) does not have data dependency. Based on our data layout, we move loop 3 to the outermost loop so that the output features share similar memory access patterns in FP/BP and WU. The loop order of off-chip data transmission in FP/BP is shown in Fig. 15 (a). As shown in Fig. 12 and Fig. 13, in FP/BP, tiles of input features are fetched in the X direction first to generate the first output features tile. Then the tiles of output features are generated and stored in the Y direction first, so the input features tiles movement follows the Y direction as well. Then the output features tiles are generated and stored in the X direction, and the access pattern of input features repeats ⌈𝑀

𝑇𝑚⌉ times. The burst length of output features in the OUT DMA channel is 𝑀𝑖× 𝑅𝑖× 𝐶𝑖.

The loop order in Fig. 15 (b) is adopted in WU. From Fig. 12 and Fig. 13, tiles of both input features and output features are fetched and stored in the Y direction first to calculate weights gradients for the first tile. Then weights are updated along the input channel dimension, so the input features tiles move in the X direction, while the output features access pattern (the dashed box in Fig. 12 (c)) repeats ⌈𝑁

𝑇𝑛⌉times. After that, weights are updated along the output channel dimension, so the output features tiles move in the X direction, while the input features access pattern (the dashed box in Fig. 13 (c)) repeats ⌈𝑁

𝑇𝑛⌉times. The burst length of output features in the OFM DMA channel is 𝑇𝑚× 𝑅𝑖× 𝐶𝑖. When the IFM buffer and the OFM buffer are large enough to hold the 𝑇𝑛× 𝑅𝑖_𝑖𝑛× 𝐶𝑖_𝑖𝑛input and 𝑇𝑚𝑖× 𝑅𝑖× 𝐶𝑖output features, i.e. 𝑅𝑖≤𝑇𝑟𝑖, the output features do not need to be repeatedly loaded. The loop order can be optimized as shown in Fig. 15 (c).

1. for (to=0; to<M; to+=Tm){ for (row=0; row<R; row+=Tr){ for (ti=0; ti<N; ti+=Tn){ load IFM; if (row==0){ load WEI; } on-chip convolution; } store OFM; } 12. }

1. for (to=0; to<M; to+=Tm){ for(ti=0; ti<N; ti+=Tn){ for(row=0; row<R; row+=Tr){ load OFM; load IFM; on-chip convolution; } store WEI; } 10. }

1. for (to=0; to<M; to+=Tm){ load OFM; for(ti=0; ti<N; ti+=Tn){ load IFM; on-chip convolution; store WEI; } }

**Fig. 15.** Pseudo-code of loop order scheduling between tiles. (a) Loop order for FP and BP, (b) Loop order for WU, (c) Loop order for WU when 𝑅𝑖≤𝑇𝑟𝑖.

Weight Reuse in Mini-batch Training Based on the above-mentioned optimization, we further reduce DRAM data access by reusing weights in mini-batch training. Different from inference, training involves processing a batch of data at once, so data reuse is necessary to decrease the transmission times of weights between on-chip buffer and off-chip memory. On FPGAs, a BRAM bank size is large enough to store multiple tiles of weights. Therefore, we propose a weight reuse strategy based on our data layout. Thanks

to our loop order shown in Fig. 15, we can load weights only when the accelerator processes the output feature tile lying in the first row. As illustrated in Fig. 16, when the accelerator processes a tile of features in the first row of the first image in a batch, 𝑀𝑖_𝑜𝑛× 𝑁𝑖× 𝐾𝑖× 𝐾𝑖weights are loaded and stored in the WEI double buffers, where 𝑀𝑖_𝑜𝑛is the multiple of 𝑇𝑚depending on the on-chip BRAM resources. After the first 𝑀𝑖_𝑜𝑛channels of OFMs in the image are processed, the first 𝑀𝑖_𝑜𝑛channels of OFMs of the next image will be processed, so weights do not need to be uploaded again. The next 𝑀𝑖_𝑜𝑛channels of the first image will be processed after the first 𝑀𝑖_𝑜𝑛channels of all images in the batch are processed. Therefore, weights do not need to be transmitted back and forth. After the above-mentioned steps, the burst length is 𝑀𝑖×𝑁𝑖for FP/WU and 𝑇𝑚× 𝑀𝑖_𝑜𝑛′ for BP, which are illustrated in Fig. 16 (b) and (c) respectively.

WEI/OUT DMA stream

Mi_on

Mi_on'

FP/WU:

Burst length=Tm×Mi_on'

13 ... 16

25 ... 28

**Fig. 16.** Data layout of weights after weight reuse. (a) Weights stored in DRAM, (b) Weights transmitted via the WEI/OUT DMA channel in FP/WU, (c) Weights transmitted via the WEI DMA channel in BP.

In mini-batch training, weight reuse will not affect the burst length of output features in WU and input features. For output features in FP and BP, after the first 𝑀𝑖_𝑜𝑛channels of OFMs of the first image are transmitted to DRAM, the next image of the batch will be processed before other channels of the prior image. Therefore, as shown in Fig. 17, the burst length is 𝑀𝑖_𝑜𝑛× 𝑅𝑖× 𝐶𝑖.

Burst length=Mi_on×Ri×Ci

Image 1 Image 2

Mi_on

**Fig. 17.** Data layout of output features in mini-batch training after weight reuse. (a) Output features of two images in a batch, (b) Output features transmitted the via the OUT DMA channel in FP/BP.

PERFORMANCE AND RESOURCE MODEL

In this section, we establish an analytic model to calculate the latency and resources for our design. Unlike previous works [16, 24] which only focused on the performance of a bare accelerator running on separate Conv layers, our model considers the discontinuity of off-chip memory access in a realistic end-to-end training process. Based on the model, we build a scheduling tool to determine design parameters for given FPGA devices and given network models.

Performance Model

For a [𝑀𝑖, 𝑁𝑖, 𝑅𝑖,𝐶𝑖, 𝐾𝑖, 𝐾𝑖,𝑆𝑖] Conv layer 𝑖, we assume the parameters of a tile is [𝑇𝑚,𝑇𝑛,𝑇𝑟𝑖,𝑇𝑐𝑖]. 𝑇𝑚and 𝑇𝑛are fixed for all layers since they are determined by the number of DSPs, while 𝑇𝑟𝑖

and 𝑇𝑐𝑖are adjustable according to different layer parameters. In our design, 𝑇𝑚= 𝑇𝑛, and 𝑇𝑐𝑖= 𝐶𝑖. The computation latency of a tile of features in FP, BP, and WU can be represented as

𝐶𝑂𝑀𝑃= 𝑇𝑟𝑖×𝑇𝑐𝑖× 𝐾𝑖× 𝐾𝑖clock cycles.

The continuity of memory address significantly impacts the off-chip communication efficiency. To consider the memory access discontinuity, we assume the start time of the DMA stream is 𝑡𝑠𝑡𝑎𝑟𝑡. When discontinuity happens, DMA restarts. We have tested the start time on both the PYNQ-Z1 and the ZCU102 board, and 𝑡𝑠𝑡𝑎𝑟𝑡≈400 cycles under 100MHz clock. We determine the data width parameters 𝑝to model the off-chip/on-chip communication bandwidth. For 32-bit floating-point, if the DMA stream width is 128 bits, 𝑝= 4. Since the burst length of input features equals the size of a tile, discontinuity happens every time a tile of input features are fetched. The latency of loading a tile of input features is formulated as 𝑡𝑖

𝐼𝐹𝑀= 𝑡𝑠𝑡𝑎𝑟𝑡+ ⌈𝑇𝑛

𝑝⌉× ((𝑇𝑟𝑖−1) ×𝑆𝑖+𝐾𝑖) × ((𝑇𝑐𝑖−1) ×𝑆𝑖+𝐾𝑖) clock cycles. The weights loading latency can be represented as 𝑡𝑖

𝑊𝐸𝐼= ⌈𝑇𝑚×𝑇𝑛

⌉× 𝐾𝑖× 𝐾𝑖clock

cycles, and the latency of storing a tile of output features is formulated as 𝑡𝑖

𝑂𝑈𝑇= ⌈𝑇𝑚

𝑝⌉×𝑇𝑟𝑖×𝑇𝑐𝑖

clock cycles. 𝑡𝑠𝑡𝑎𝑟𝑡is added to 𝑡𝑖

𝑊𝐸𝐼and 𝑡𝑖

𝑂𝑈𝑇only when the discontinuity happens, which will be discussed in detail as follows. We define 𝑡𝑖

𝐿𝑂𝐴𝐷= max

𝐼𝐹𝑀,𝑡𝑖

𝑊𝐸𝐼

, 𝑡𝑖

𝑃𝑅𝑂𝐷1 = max

𝐼𝐹𝑀,𝑡𝑖

𝐶𝑂𝑀𝑃

,

𝑃𝑅𝑂𝐷2 = max

𝐿𝑂𝐴𝐷,𝑡𝑖

𝐶𝑂𝑀𝑃

, and 𝑡𝑖

𝑆𝑇𝑂𝑅𝐸= max

𝐶𝑂𝑀𝑃,𝑡𝑖

𝑂𝑈𝑇

. We assume in layer 𝑖, 𝑀𝑖_𝑜𝑛× 𝑇𝑛× 𝐾𝑖× 𝐾𝑖weights are stored on-chip. If the batch size is 𝐵, weights will be loaded only during the iteration when the proposed accelerator processes the first image in the batch. For other iterations, the latency of processing 𝑀𝑖_𝑜𝑛channels of an image in FP can be formulated as follows.

𝐿𝑎𝑡1𝑖= ⌈𝑁𝑖

𝑇𝑛−1⌉× 𝑡𝑖

𝑃𝑅𝑂𝐷1 + 𝑡𝑖

𝐼𝐹𝑀+ 𝑡𝑖

𝐶𝑂𝑀𝑃

𝐿𝑎𝑡2𝑖= ⌈𝑁𝑖

𝑇𝑛−1⌉× 𝑡𝑖

𝑃𝑅𝑂𝐷1 + 𝑡𝑖

𝐼𝐹𝑀+ 𝑡𝑖

𝑆𝑇𝑂𝑅𝐸

𝐿𝑎𝑡3𝑖= (⌈𝑀𝑖_𝑜𝑛

𝑇𝑚⌉× ⌈𝑅𝑖

𝑇𝑟𝑖⌉−1) × 𝐿𝑎𝑡2𝑖+ 𝐿𝑎𝑡1𝑖+ 𝑡𝑖

𝑂𝑈𝑇+ 𝑡𝑖

𝑠𝑡𝑎𝑟𝑡

Weights need to be loaded when our accelerator processes the first image in the mini-batch. In FP, 𝑡𝑠𝑡𝑎𝑟𝑡can be neglected in weight transmission since the burst length equals the size of weights, which means the addresses are continuous during the whole Conv layer. Therefore, the latency of the proposed accelerator processing 𝑀𝑖_𝑜𝑛channels of the first image can be formulated as follows.

𝐿𝑎𝑡𝑏1𝑖= ⌈𝑁𝑖

𝑇𝑛−1⌉× 𝑡𝑖

𝑃𝑅𝑂𝐷2 + 𝑡𝑖

𝐿𝑂𝐴𝐷+ 𝑡𝑖

𝐶𝑂𝑀𝑃

𝐿𝑎𝑡𝑏2𝑖= ⌈𝑁𝑖

𝑇𝑛−1⌉× 𝑡𝑖

𝑃𝑅𝑂𝐷2 + 𝑡𝑖

𝐿𝑂𝐴𝐷+ 𝑡𝑖

𝑆𝑇𝑂𝑅𝐸

𝐿𝑎𝑡𝑏3𝑖= ⌈𝑀𝑖_𝑜𝑛

𝑇𝑚⌉× ⌈𝑅𝑖

𝑇𝑟𝑖−1⌉× 𝐿𝑎𝑡2𝑖+ ⌈𝑀𝑖_𝑜𝑛

𝑇𝑚 −1⌉× 𝐿𝑎𝑡𝑏2𝑖+ 𝐿𝑎𝑡𝑏1𝑖+ 𝑡𝑖

𝑂𝑈𝑇+ 𝑡𝑖

𝑠𝑡𝑎𝑟𝑡

The latency of our accelerator processing the whole Conv layer in FP is formulated in Eq. (21).

𝐿𝑎𝑡𝑖= ⌈

𝑀𝑖_𝑜𝑛⌉× ((𝐵−1) × 𝐿𝑎𝑡3𝑖+ 𝐿𝑎𝑡𝑏3𝑖).

In BP, the situation is similar to that in FP, except that the addresses of weights are discontinuous after 𝑀𝑖_𝑜𝑛channels. The accelerator loads 𝑀𝑖_𝑜𝑛×𝑇𝑛×𝐾𝑖×𝐾𝑖weights together when processing

the first tile of the first image, so it costs 𝑡𝑖

𝑊𝐸𝐼= ⌈𝑀𝑖_𝑜𝑛×𝑇𝑛

⌉× 𝐾𝑖× 𝐾𝑖+ 𝑡𝑖

𝑠𝑡𝑎𝑟𝑡clock cycles. 𝐿𝑎𝑡1𝑖,

𝐿𝑎𝑡2𝑖, 𝐿𝑎𝑡3𝑖, 𝐿𝑎𝑡2𝑖, 𝐿𝑎𝑡𝑏1𝑖, and 𝐿𝑎𝑡𝑏2𝑖remain unchanged, while 𝐿𝑎𝑡𝑏3𝑖= (⌈𝑀𝑖_𝑜𝑛

𝑇𝑚⌉× ⌈𝑅𝑖

𝑇𝑟𝑖⌉−1) × 𝐿𝑎𝑡2𝑖+ 𝐿𝑎𝑡𝑏1𝑖+ 𝑡𝑖

𝑂𝑈𝑇+ 𝑡𝑖

𝑠𝑡𝑎𝑟𝑡. In WU, loss features are loaded from the off-chip memory to the OFM buffer. Transmitting a tile of loss features costs 𝑡𝑖

𝑂𝐹𝑀= 𝑡𝑖

𝑠𝑡𝑎𝑟𝑡+𝑇𝑟𝑖×𝑇𝑐𝑖× ⌈𝑇𝑚

𝑝⌉clock cycles. Weights are updated after all the gradients of the batch are accumulated, so transmitting the updated weights costs the same time as loading weights, which means 𝑡𝑖

𝑂𝑈𝑇=𝑡𝑖

𝑊𝐸𝐼. Same with FP, 𝑡𝑠𝑡𝑎𝑟𝑡can be neglected when calculating 𝑡𝑖

𝑊𝐸𝐼. We define 𝑡𝑖

𝐿𝑂𝐴𝐷= max

𝐼𝐹𝑀,𝑡𝑖

𝑂𝐹𝑀

, 𝑡𝑖

𝑃𝑅𝑂𝐷1 = max

𝐿𝑂𝐴𝐷,𝑡𝑖

𝐶𝑂𝑀𝑃

, 𝑡𝑖

𝑃𝑅𝑂𝐷2 = max

𝐼𝐹𝑀,𝑡𝑖

𝐶𝑂𝑀𝑃

, and 𝑡𝑖

𝑆𝑇𝑂𝑅𝐸= max

𝐶𝑂𝑀𝑃,𝑡𝑖

𝑂𝑈𝑇

. The latency of WU of the 𝑖th Conv layer is formulated as follows.

𝐿𝑎𝑡1𝑖= ⌈𝑅𝑖

𝑇𝑟𝑖−1⌉× 𝑡𝑖

𝑃𝑅𝑂𝐷1 + 𝑡𝑖

𝐿𝑂𝐴𝐷+ 𝑡𝑖

𝐶𝑂𝑀𝑃

𝐿𝑎𝑡𝑏1𝑖= ⌈𝑅𝑖

𝑇𝑟𝑖−1⌉× 𝑡𝑖

𝑃𝑅𝑂𝐷1 + 𝑡𝑖

𝐿𝑂𝐴𝐷+ 𝑡𝑖

𝑆𝑇𝑂𝑅𝐸

𝐿𝑎𝑡𝑖= (((𝐵−1) × ⌈𝑀𝑖_𝑜𝑛

𝑇𝑚⌉× ⌈𝑁𝑖

𝑇𝑛⌉+1) ×𝐿𝑎𝑡1𝑖+ (⌈𝑀𝑖_𝑜𝑛

𝑇𝑚⌉× ⌈𝑁𝑖

𝑇𝑛⌉−1) ×𝐿𝑎𝑡𝑏1𝑖+𝑡𝑖

𝑂𝑈𝑇) × ⌈

𝑀𝑖_𝑜𝑛⌉

As illustrated in Fig. 15 (c), when 𝑅𝑖≤𝑇𝑟𝑖, the output features do not need to be repeatedly loaded. Under this circumstance, the latency of WU is formulated as follows.

𝐿𝑎𝑡1𝑖= ⌈𝑁𝑖

𝑇𝑛𝑖−1⌉× 𝑡𝑖

𝑃𝑅𝑂𝐷2 + 𝑡𝑖

𝐿𝑂𝐴𝐷+ 𝑡𝑖

𝐶𝑂𝑀𝑃

𝐿𝑎𝑡𝑏1𝑖= ⌈𝑁𝑖

𝑇𝑛𝑖−1⌉× (𝑡𝑖

𝑃𝑅𝑂𝐷2 + 𝑡𝑖

𝑂𝑈𝑇) + 𝑡𝑖

𝐿𝑂𝐴𝐷+ 𝑡𝑖

𝐶𝑂𝑀𝑃+ 𝑡𝑖

𝑂𝑈𝑇

𝐿𝑎𝑡𝑖= ⌈

𝑀𝑖_𝑜𝑛⌉× ⌈𝑀𝑖_𝑜𝑛

𝑇𝑚⌉× ((𝐵−1) × 𝐿𝑎𝑡1𝑖+ 𝐿𝑎𝑡1𝑏𝑖)

Resource Model

For Conv layers, the on-chip resources that need to be considered for Conv layers include DSPs and BRAMs. For DSPs, 𝑇𝑚×𝑇𝑛MAC operations are conducted in parallel. Therefore, the computation constraint is shown in Eq. (28), where 𝑞is the factor depending on data types. On Xilinx FPGAs, each MAC utilizes 5 DSPs for 32-bit floating-point, so 𝑞= 5 in the proposed design. In terms of on-chip memory, we select double buffers to load and store data and conduct Conv operations in parallel. The number of BRAM banks for each IFM buffer and OFM buffer are shown in Eq. (29) and Eq. (30) respectively. The notation BITs is the data bit-width adopted in the design. For the Weight buffer, we place 𝑀𝑖_𝑜𝑛×𝑁𝑖kernels together for weight reuse. These data are scattered in double buffers. The number of BRAM banks for one Weight buffer is shown in Eq. (31). The on-chip memory constraint is shown in Eq. (32).

𝐷𝐶𝑜𝑛𝑣= 𝑞×𝑇𝑚×𝑇𝑛< 𝑡𝑜𝑡𝑎𝑙𝐷𝑆𝑃𝑠𝑛𝑢𝑚𝑏𝑒𝑟

𝐵𝐼𝐹𝑀= max

𝐵𝑖

𝐼𝐹𝑀= max



𝑇𝑛× ⌈((𝑇𝑟𝑖−1) × 𝑆𝑖+ 𝐾𝑖) × ((𝑇𝑐𝑖−1) × 𝑆𝑖+ 𝐾𝑖) × 𝐵𝐼𝑇𝑠

𝑆𝑖𝑧𝑒𝑜𝑓𝑎𝐵𝑅𝐴𝑀𝐵𝑎𝑛𝑘 ⌉



𝐵𝑂𝐹𝑀= max

𝐵𝑖

𝑂𝐹𝑀= max



𝑇𝑚× ⌈ 𝑇𝑟𝑖×𝑇𝑐𝑖× 𝐵𝐼𝑇𝑠 𝑆𝑖𝑧𝑒𝑜𝑓𝑎𝐵𝑅𝐴𝑀𝐵𝑎𝑛𝑘⌉



𝐵𝑊𝐸𝐼= max

𝐵𝑖

𝑊𝐸𝐼= max

(

𝑇𝑚×𝑇𝑛× ⌈

𝐾𝑖× 𝐾𝑖× ⌈𝑁𝑖

2×𝑇𝑛⌉× ⌈𝑀𝑖_𝑜𝑛 𝑇𝑚⌉× 𝐵𝐼𝑇𝑠 𝑆𝑖𝑧𝑒𝑜𝑓𝑎𝐵𝑅𝐴𝑀𝐵𝑎𝑛𝑘 ⌉

)

𝐵𝐶𝑜𝑛𝑣= 2 × (𝐵𝐼𝐹𝑀+ 𝐵𝑂𝐹𝑀+ 𝐵𝑊𝐸𝐼) < 𝑡𝑜𝑡𝑎𝑙𝐵𝑅𝐴𝑀𝑠𝑛𝑢𝑚𝑏𝑒𝑟

It should be noted that in realistic end-to-end system design, the boundary of 𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣 should be slightly smaller than the total DSPs and BRAMs numbers. It is because except for the MAC operations, several operations also take up a small fraction of on-chip resources. For example, some non-Conv layers (e.g. maximum pooling, average pooling, ReLU, etc.), which are inevitable in practical end-to-end training processes need extra DSPs to make comparisons and extra BRAMs to buffer the indexes. Besides, some neural networks have irregular weights kernel shapes for different Conv layers. Adding an extra buffer to fetch a tile of weights from the on-chip Weight buffer to the Conv Kernel can relieve the routing congestion in realistic FPGA implementation. Besides, since FP, BP, WU have different loop orders, extra DSPs are utilized to calculate BRAM addresses under different layer parameters. This address calculation is much more complex than that in inference. Therefore, in practical design, the estimated boundary of the on-chip resources should be set lower than the available resources empirically. The details will be further explained in Section 5.3.

Computation and Memory Resources Scheduling Tool

Based on the above-mentioned model, we build a computation and memory resources scheduling tool for different devices and different networks. Algorithm 1 shows the framework of our scheduling tool. As mentioned in Section 5.2, 𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣are lower than the total DSPs and BRAMs numbers in realistic FPGA implementation. Therefore, it is wise to set a boundary for 𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣that is lower than the available on-chip resources. According to the experimental results in Section 6, assigning 80% of DSPs and 75% BRAMs to the estimated boundary for 𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣should be enough. Then we determine 𝑇𝑚and 𝑇𝑛according to the DSPs number. Then we choose the optimal 𝑇𝑟𝑖, 𝑇𝑐𝑖, and 𝑀𝑖_𝑜𝑛for each layer according to Eq. (15) - (27). Specifically, in steps 3 and 4, we find the lower bound for 𝐵𝐼𝐹𝑀and 𝐵𝑂𝐹𝑀by assuming that the buffers can only hold one row for the largest feature maps. Then, from step 5 to step 12, we try to assign resources for Weight buffers so that they can hold as many weights for each layer as possible. After we determine 𝐵𝑊𝐸𝐼and 𝑀𝑖_𝑜𝑛for each layer, we re-assign IFM and OFM buffers under the constraints shown in Eq. (29), (30), and (32), and find the optimal 𝑇𝑟𝑖and 𝑇𝑐𝑖for each layer. After 𝑇𝑚, 𝑇𝑛, and

[𝑇𝑟𝑖,𝑇𝑐𝑖, 𝑀𝑖_𝑜𝑛]1≤𝑖≤𝑛are determined, we can calculate the DMA start addresses for each layer off-line based on the data reshaping approach in Section 4.

EXPERIMENTS

The proposed work is evaluated on edge-level FPGAs PYNQ-Z1 and ZCU102 with working frequency at 100MHz. The accelerator is designed with Vivado HLS, which generates IP core from C language. The obtained IP cores are connected, synthesized, and implemented in Vivado (v2019.1). The Vivado Project Summary reports resource utilization and power after implementation. Finally, we employ Xilinx SDK to program SoC on PYNQ-Z1 and ZCU102 to achieve end-to-end CNN training.

Effectiveness of The Data Reshaping Approach In this section, we need to validate the effectiveness of the proposed data reshaping approach ([𝑇𝑚,𝑇𝑛] = [16, 16]). We test the Conv layers of the AlexNet on ZCU-102. We select the batch size 𝐵as 4 and the DMA stream width as 128 bits. We adopt the results using the BCHW data layout and the results using the BHWC data layout as baselines ([𝑇𝑚𝐵𝑎𝑠𝑒,𝑇𝑛𝐵𝑎𝑠𝑒] = [32, 8]). The BCHW pattern does not involve any optimization. For the BHWC pattern, 𝑁/𝑇𝑛tiles of input features and 𝑀/𝑇𝑚tiles of the output features are buffered in the on-chip BRAM for data reuse based on the loop order in the inference phase. Weights are pre-allocated tile by tile based on the data flow in inference. The comparisons are shown in Tables 3, 4, and 5.

Algorithm 1 Computation and Memory Resources Scheduling

Input:

CNN layers parameters [𝑀𝑖, 𝑁𝑖, 𝑅𝑖,𝐶𝑖, 𝐾𝑖, 𝐾𝑖,𝑆𝑖]1≤𝑖≤𝑛, batch size 𝐵, data type parameter 𝑞, DMA stream width, total DSPs number, total BRAMs number; Output:

𝑇𝑚, 𝑇𝑛, [𝑇𝑟𝑖,𝑇𝑐𝑖, 𝑀𝑖_𝑜𝑛]1≤𝑖≤𝑛, 𝐵𝐼𝐹𝑀, 𝐵𝑂𝐹𝑀, 𝐵𝑊𝐸𝐼;

1: Estimate the boundary for 𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣; 2: Assign 𝑇𝑚, 𝑇𝑛according to Eq. (28), while 𝑇𝑚= 𝑇𝑛; 3: Find 𝑘= arg max

𝑅𝑖× 𝐶𝑖

;

4: Determine the lower bound for 𝐵𝐼𝐹𝑀and 𝐵𝑂𝐹𝑀, i.e. inf 𝐵𝐼𝐹𝑀= 𝐵𝑘 𝐼𝐹𝑀, inf 𝐵𝑂𝐹𝑀= 𝐵𝑘

𝑂𝐹𝑀, when 𝑇𝑐𝑘= 𝐶𝑘, 𝑇𝑟𝑘= 1; 5: for 𝑖= 1; 𝑖≤𝑛; 𝑖+ + do 6: Calculate 𝐵𝑖

𝑊𝐸𝐼based on (31) when 𝑀𝑖_𝑜𝑛= 𝑀𝑖, and initialize 𝑙= 1;

7: if 2 × (inf 𝐵𝐼𝐹𝑀+ inf 𝐵𝑂𝐹𝑀+ 𝐵𝑖

𝑊𝐸𝐼) ≥𝑒𝑠𝑡𝑖𝑚𝑎𝑡𝑒𝑑𝐵𝐶𝑜𝑛𝑣𝑏𝑜𝑢𝑛𝑑𝑎𝑟𝑦then 8: l++;

9: Find the minimal 𝑀𝑖_𝑜𝑛satisfying 𝑀𝑖

𝑙 ≤𝑀𝑖_𝑜𝑛, 𝑀𝑖_𝑜𝑛mod 𝑇𝑚= 0, and go to step 7; 10: end if

11: end for 12: Calculate 𝐵𝑊𝐸𝐼and 𝑀𝑖_𝑜𝑛for each layer based on Eq. (31); 13: for 𝑖= 1; 𝑖≤𝑛; 𝑖+ + do 14: Set 𝑇𝑐𝑖= 𝐶𝑖, and select all 𝑇𝑟𝑖

𝑚satisfying Eq. (29), (30), and (32), where 1 ≤𝑇𝑟𝑖

𝑚≤𝑅𝑖; 15: Determine 𝑇𝑟𝑖= arg min

𝑚

𝐿𝑎𝑡𝑖

𝑚based on Eq. (15)- (27);

16: end for 17: Calculate 𝐵𝐼𝐹𝑀and 𝐵𝑂𝐹𝑀based on Eq. (29), (30);

As mentioned in Section 2.3, our goal is to design a general accelerator supporting end-to-end training with both dense and small networks without sacrificing precision, so it is necessary to appropriately manage external memory access and allocate on-chip buffers. When applying loop tiling, the tiling schemes involved in the accelerator design break the continuity of data addresses in DRAM and thus reduce the transmission efficiency between on-chip buffer and off-chip DRAM. Table 3 shows the experimental results of our baseline which is a bare accelerator with the unified channel-level parallelism-based convolution kernel. It does not involve any optimizations related to the off-chip DRAM access policy. As illustrated in Section 4, the burst length before data reshaping is much smaller than the size of a tile. To ensure that the accelerator conducts MAC operations with correct features and weights matrices in realistic end-to-end training, data should be reallocated before being transmitted from DRAM to the on-chip accelerator. Therefore, our baseline includes the on-chip acceleration time and off-chip reallocation time. After applying data reshaping, data can be fetched from DRAM to the accelerator directly without extra reallocation.

For Conv 1, the number of input channels is only 3, 𝑇𝑛𝐵𝑎𝑠𝑒= 8, and 𝑇𝑛= 16. Therefore, 5/8 computation resources remain idle for the baseline, while 13/16 computation resources for our proposed design remain idle. That’s why the acceleration time for the baseline is shorter than the latency in our proposed design. However, features should be reallocated before entering the next layer (for FP) or after being generated from the prior layer (for WU). As shown in Table 3, the reallocation time is much longer than the acceleration time. For Conv 2 to Conv 5, 𝑇𝑟𝑖≥𝑅𝑖and 𝑇𝑐𝑖≥𝐶𝑖, so features do not need to be reallocated between adjacent layers, but weights still need

to be reallocated before entering the Conv layer (for FP and BP) or updated from the Conv layer

**Table 3.** Experimental Results of The Baseline with The BCHW Data Layout

[𝑇𝑟𝑖

𝐵𝑎𝑠𝑒,𝑇𝑐𝑖

𝐵𝑎𝑠𝑒] Acceleration

(cycles)

Reallocation

(cycles)

(cycles)

[11, 11]

[11, 11]

[27, 27] [27, 27] [27, 27]

[13, 13] [13, 13] [13, 13]

[13, 13] [13, 13] [13, 13]

[13, 13] [13, 13] [13, 13]

1,494,958,747 1,562,001,846

**Table 4.** Experimental Results of The Baseline with The BHWC Data Layout and Data Reuse

[𝑇𝑟𝑖

𝐵𝑎𝑠𝑒,𝑇𝑐𝑖

𝐵𝑎𝑠𝑒] Acceleration

(cycles)

Reallocation

(cycles)

(cycles)

[11, 11]

[11, 11]

[27, 27] [27, 27] [27, 27]

[13, 13] [13, 13] [13, 13]

[13, 13] [13, 13] [13, 13]

[13, 13] [13, 13] [13, 13]

(for WU). To sum up, the total acceleration time for the baseline is close to that for our proposed design under the same degree of parallelism (𝑇𝑚𝐵𝑎𝑠𝑒×𝑇𝑛𝐵𝑎𝑠𝑒= 𝑇𝑚×𝑇𝑛) and tile size boundary of features (max

𝑇𝑟𝑖

𝐵𝑎𝑠𝑒× max

𝑇𝑐𝑖

𝐵𝑎𝑠𝑒= max

𝑇𝑟𝑖× max

𝑇𝑐𝑖), but the extra reallocation time in realistic

**Table 5.** Experimental Results Validating Data Reshaping Approach

[𝑇𝑟𝑖,𝑇𝑐𝑖] Without Weight Reuse

(cycles)

After Weight Reuse

(cycles)

[2, 55]

[2, 55]

[27, 27] [27, 27] [27, 27]

[13, 13] [13, 13] [13, 13]

[13, 13] [13, 13] [13, 13]

[13, 13] [13, 13] [13, 13]

end-to-end training is even longer than the acceleration time. Therefore, accelerating without considering the actual data layout in DRAM between adjacent layers is inefficient in realistic end-to-end training.

The baseline in Table 4 uses the BHWC data layout and applies data reuse to alleviate the discontinuous memory access. As illustrated in Figs. 9-11, features and weights are continuous in a long burst length in FP, so data are not reallocated during the Conv layers. Such an approach is efficient in the inference phase. In BP, although the memory access pattern of features is the same as that in FP, the weights transmission patterns are quite different. As shown in Fig. 11 (c), the burst length is much less than the size of a tile, so weights should be reallocated in each Conv layer. The extra reallocation time is much longer than the acceleration time. In WU, the on-chip buffer can hold all the features for Conv 2-Conv 5 layers, so it is practical to load all the features to the FPGA chip without extra reallocation. However, in the Conv 1 layer, the on-chip memory cannot hold all the features. Even though the input features can be pre-allocated before entering into the neural network since they serve as the inputs for the whole process, the output features which are calculated in BP cannot be allocated ahead of time. Therefore, the Conv 1 layer also requires extra reallocation time in WU, which is quite inefficient.

As mentioned in Section 4, we optimize the DRAM access incrementally. We first achieve intra-tile continuous memory allocation by reorganizing the DRAM layouts for input features, output features, and weights. Then we re-schedule the loop order to achieve inter-tile continuous memory allocation. These two parts are combined to improve memory access continuity together when the batch size is 1. Considering the training process involves convolution operations among a mini-batch, we further propose and apply a weight reuse strategy based on the proposed data layout. Table 5 shows the experimental results of the data reshaping approach without weight reuse and after weight reuse. The batch size is also 4, and the latency for FP/BP without and after weight reuse is nearly the same. It is because, in FP and BP, input features and weights are transmitted together. As can be

seen from Section 5, When ⌈𝑇𝑛

𝑝⌉× ((𝑇𝑟𝑖−1) ×𝑆𝑖+𝐾𝑖) × ((𝑇𝑐𝑖−1) ×𝑆𝑖+𝐾𝑖) > ⌈𝑇𝑚×𝑇𝑛

⌉×𝐾𝑖×𝐾𝑖,

𝐼𝐹𝑀> 𝑡𝑖

𝑊𝐸𝐼. Therefore, reusing the weights may not reduce the latency as a whole. However, in WU, the latency with weight reuse is apparently less than that without reuse. It is because the transmission of weights happens during storing the results in WU, which cannot be totally covered by 𝑡𝑖

𝐶𝑂𝑀𝑃(For example, in the last iteration of the loop in line 2 from Fig, 15 (b) and the loop in line 3 from Fig, 15 (c)). As a whole, reusing weights can reduce the latency of the training phase of the whole network. Fig. 18 shows the latency without and with weight reuse when the batch size ranges from 2 to 128. It shows that when the batch size increases, applying the reuse strategy has more apparent advantages than only achieving intra-tile and inter-tile data access continuity.

Without Weight Reuse After Weight Reuse

Latency per batch (s)

**Fig. 18.** Experimental Results of The Data Reshaping Approach without Weight Reuse and after Weight Reuse

Accuracy of The Performance Model

After displaying the effectiveness of the data reshaping approach, we use the AlexNet to validate the accuracy of the performance model. Our scheduling tool first determines optimal tiling parameters which are shown in Table 6. Then the latency is estimated by our model and tested on-board separately. As shown in Table 6, the estimated results are close to the tested results. The results verify the accuracy of the performance model.

CNN Training Performance In this section, we conduct end-to-end evaluations on different neural networks. We first compare our design with the automatic compiler-based FPGA accelerator [22]. It adopted a combination of channel-level parallelism and feature map-level parallelism with the unrolling factors for columns, rows, and output channels. It initially stored weights tile by tile in a transposable format in DRAM and read the entire weights of a Conv layer from DRAM to their on-chip buffer. The baseline implemented a ‘1X’ CNN on the CIFAR-10 dataset with the structure as Conv 1 ([𝑀𝑖, 𝑁𝑖, 𝑅𝑖,𝐶𝑖, 𝐾𝑖,𝑆𝑖] = [16, 3, 32, 32, 3, 1]) - Conv 2 ([16, 16, 32, 32, 3, 1]) - Pooling - Conv 3 ([32, 16, 16, 16, 3, 1]) - Conv 4 ([32, 32, 16, 16, 3, 1]) - Pooling - Conv 5 ([64, 32, 8, 8, 3, 1]) - Conv 6 ([64, 64, 8, 8, 3, 1])- Pooling - FC ([10, 1024, 1, 1, 1, 1]), using 16-bit fixed-point precision. We test the same network on both PYNQ-Z1 and ZCU102 boards. The DMA stream bandwidth is 128 bits for ZCU102 and 32 bits for PYNQ-Z1. Our design focuses on implementing on-device FPGAs without sacrificing precision, so 32-bit floating-point is adopted. Vivado utilization report provides the utilization of BRAMs, DSPs, and the power report provides the total on-chip power. We measure the latency of training the whole batch with the batch size of 128. Then we calculate the latency per image and the throughput.

**Table 6.** Experimental Results Validating The Performance Model

[𝑇𝑟𝑖,𝑇𝑐𝑖, 𝑀𝑖_𝑜𝑛] Our Model (cycles) On-board (cycles) Deviation

[2, 55, 96]

[2, 55, 96]

0.74% 2.75%

[27, 27, 112]

[27, 27, 48] [27, 27, 112]

0.04% 0.28% 0.09%

[13, 13, 112] [13, 13, 112] [13, 13, 112]

1.28% 3.91% 0.90%

[13, 13, 112] [13, 13, 112] [13, 13, 112]

1.69% 2.81% 1.34%

[13, 13, 112] [13, 13, 112] [13, 13, 112]

1.73% 2.55% 1.38% 1.05%

**Table 7** shows the comparison results between the baseline [22] and our design in terms of resource utilization, throughput, energy efficiency, etc. The Stratix 10 GX adopted in the baseline is an advanced FPGA board developed by Intel. It is unfair to compare the throughput directly for different devices. However, energy efficiency is an important metric to judge the performance of edge devices, thus we use energy efficiency as the metric for different designs on different FPGAs. We nominate the throughput and efficiency by multiplying the bit width of the data type. Although using the fixed-point data type is much more DSP-efficient and power-efficient than adopting floating-point under the same bit width, our nominal efficiency still can outperform that of the baseline. The reason is that the baseline has more data transmission latency especially for WU where accessing weight gradients, weights, and storing back the updated values leads to DRAM access latency. 51% percent of the overall latency in one iteration of a batch is consumed in WU [22]. Fig. 19 shows the latency breakdown of our design. The total latency for each training process is calculated by summarizing latency for each Conv layer, and the latency for MAC is the theoretical computation latency calculated by accumulating 𝑡𝑖

𝐶𝑂𝑀𝑃for each Conv layer based on the performance model. Since the ’1X’ CNN is a relatively small network, the number of loops is also small. According to the performance model, although double buffers are adopted, the computation and data transmission is conducted in sequential in the first and last iteration of the loop, while they are in parallel for the middle iterations. Therefore, when the number of loops is small, the proposed design also includes much data transmission latency for FP, BP, WU. However, other optimizations like loop order scheduling and weight reuse in a mini-batch reduce the number of off-chip memory access. Therefore, our computation latency is still much more than 50% percent of the total latency in FP, BP, or WU, which takes up a larger proportion compared with the baseline.

Besides, the baseline stored the entire weights of a Conv layer from DRAM to the on-chip buffer. Their design cannot support denser networks where the on-chip buffer cannot hold the entire weights of each Conv layer. However, our design does not have such restrictions and can support many larger networks.

**Table 7.** Experimental Results on the ’1X’ CNN

Baseline [22]

Stratix 10 GX PYNQ-Z1 1699 (30%) 𝐷𝐶𝑜𝑛𝑣(𝐷𝐶𝑜𝑛𝑣/𝑈𝑠𝑒𝑑𝐷𝑆𝑃𝑠) 10.6 (4.4%) 𝐵𝐶𝑜𝑛𝑣(𝐵𝐶𝑜𝑛𝑣/𝑈𝑠𝑒𝑑𝐵𝑅𝐴𝑀𝑠) 1.85 (11.14X) 6.89 (2.99X) Data Type Fixed 16 FP 32 FP 32 Latency/Image (ms) 163 GOPS Nominal Throughput

(GOPS× precision)

7.90 GOPS/W Nominal Effciency (GOPS× precision/W) 130.88 (1.04X)

2000000 4000000 6000000 8000000 10000000

Latency (ns)

Training Phase

MAC

Others

**Fig. 19.** Latency breakdown of CIFAR-10 ’1X’ CNN for FP, BP and WU when the batch size is 128.

In Table 7, the 𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣are the DSPs and BRAMs numbers for the Conv layer estimated by our resource model. The percentage shows the ratio between the estimated resources and actual resources used in the whole end-to-end training. As mentioned in Section 5.2 and Section 5.3, 𝐷𝐶𝑜𝑛𝑣 and 𝐵𝐶𝑜𝑛𝑣are lower than the DSPs and BRAMs numbers used in the realistic end-to-end training process. For ’1X’ CNN, the extra on-chip resources mainly function for maximum pooling layers. Besides, a few DSPs are utilized to calculate BRAM addresses of features and weights.

To validate the correctness of our design, we also implement the whole training phase of the ’1X’ CNN on ZCU102 and compare the training result with that on GPU. We load the Cifar-10 dataset from the secure digital (SD) card to the DRAM and run 50 epochs. The batch size is also 128, and the learning rate is 0.008. We use the V-100 GPU from AWS to validate the training process. The loss curves are shown in Fig. 20. Since we adopt full precision and have not changed the training algorithm, the training result should be nearly the same as that on GPU. As can be seen in Fig. 20,

the two curves are really close to each other. We also test the trained model on the test dataset. The test accuracy is 65.22% running on GPU and 64.82% running on FPGA.

**Fig. 20.** The loss curves during the training phase.

Most state-of-art works [22, 23] mainly implemented their design on Cifar-10 dataset whose input image is really small (3 × 32 × 32) compared to real-world on-device learning scenarios. To verify that our accelerator with the data reshaping approach can support larger networks with larger feature sizes, we test our design on AlexNet and Vgg-16 for ImageNet whose input image parameters are 3 × 227 × 227 and 3 × 224 × 224 respectively.

Latency

Throughput (GFLOPS)

Latency per batch (s)

Latency

Throughput (GFLOPS)

Latency per batch (s)

Latency

Throughput (GFLOPS)

Latency per batch (s)

**Fig. 21.** Experimental Results Training Different CNNs. (a) Throughput and Latency of AlexNet, (b) Throughput and Latency of Vgg-16 without BN layers, (c) Throughput and Latency of Vgg-16 with BN layers

The data reshaping approach enables our accelerator to support end-to-end training with the following situations: (1) when the feature map size of a layer increases and the on-chip memory

**Table 8.** Experimental Results on AlexNet and Vgg-16

Network Vgg-16 without BN Vgg-16 with BN

𝐷𝐶𝑜𝑛𝑣(𝐷𝐶𝑜𝑛𝑣/𝑈𝑠𝑒𝑑𝐷𝑆𝑃𝑠) 𝐵𝐶𝑜𝑛𝑣(𝐵𝐶𝑜𝑛𝑣/𝑈𝑠𝑒𝑑𝐵𝑅𝐴𝑀𝑠) Throughput (GFLOPS) Efficiency (GFLOPS/W)

is not big enough to hold all the feature maps of the layer, and (2) when the number of channels increases and the weights buffer cannot hold all the weights of a layer. For AlexNet, its convolution kernel size ranges from 11×11 to 1×1 and feature map size ranges from 227×227 to 1×1, which covers the above-mentioned situations. Besides, the stride of the first Conv layer of AlexNet is 4. Implementing Conv layers with different stride sizes are more complex than only verifying the design on CNNs where the stride remains 1. Therefore, AlexNet is ideal to verify that our design can support DNNs with a larger feature map size and larger weight density and can deal with different Conv layers shapes. Fig. 21 (a) shows the throughput and latency of a batch for training the AlexNet model with batch size ranging from 2 to 128. When the batch size is 128, the throughput reaches 34.52 GFLOPS. Because of weight reuse, the weights transmission bottleneck is ameliorated when the batch size increases, so the throughput in larger batch size is slightly higher than that for small batch size. However, unlike batch-level parallelism-based designs [23] where the performance varies a lot under different batch sizes, the performance of our channel-level parallelism-based design is less affected by the batch size. As shown in Fig. 21, the throughput when the batch size is 2 is still above 32 GFLOPS. We also test our design on Vgg-16 which has denser parameters, and the performance is shown in Fig. 21 (b). Due to the DRAM memory size limitation of ZCU102, the maximum batch size is 16. As illustrated in Fig. 21, our design achieves higher throughput on Vgg-16 compared with AlexNet. It is because, for channel-level parallelism, the number of input channels of the first Conv layer is only 3, which is smaller than 𝑇𝑛, so the computation resources are not fully utilized in this layer. This effect is also mentioned in Section 6.1. However, such underutilization only happens in the first Conv layer and is alleviated when the neural network becomes deeper. Hence, in the deeper network, Vgg-16, we achieve higher throughput.

To verify that our design can support the BN layer which is a key component of typical CNN architectures, we also test the proposed design on Vgg-16 with BN layers. The performance is shown in Fig. 21 (c). Apart from the loss and activation, the immediate BN parameters also need to be stored in DRAM. Due to the memory size limitation, the maximum batch size is 8. Unlike computation-intensive Conv layers, BN layers involve lots of data transmission processes. Some complex operations like extracting a root also cost extra computation resources and reduce the timing performance. Therefore, the overall throughput is a little less than that for Vgg-16 without BN layers.

**Table 8** also shows the resource utilization and energy efficiency of the FPGA for these networks. With the same estimated DSPs and BRAMs for Conv layers (𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣), AlexNet requires more BRAMs than Vgg-16. It is because, compared to Vgg-16, AlexNet has a less regular weights

kernel shape (ranging from 11× 11 to 1× 1), so we add an extra buffer to fetch a tile of weights from the on-chip Weight buffer before the Conv Kernel conducting MAC operations. Such optimization can release routing congestion caused by complex BRAM addresses calculation and allocation in FP, BP, and WU processes. Apart from the extra buffer, a small fraction of DSPs and BRAMs function for non-Conv layers. The accelerator also utilizes a few DSPs to calculate BRAM addresses. Therefore, as mentioned in Section 5.3, the estimated boundary of 𝐷𝐶𝑜𝑛𝑣and 𝐵𝐶𝑜𝑛𝑣in realistic end-to-end system design should be slightly smaller than the total DSPs and BRAMs numbers. From our experimental results, assigning 80% of DSPs and 75% BRAMs should be enough.

As for the Vgg-16 with BN layers, extra computation resources are utilized to do complex operations such as division, root extraction, etc. Therefore, Vgg-16 with BN layers costs more DSP resources compared with Vgg-16 without BN layers. Additional BRAMs are also utilized to buffer BN parameters for a batch.

In our end-to-end training validation, we utilize 1508 DSPs for the Vgg-16 model. The theoretical peak performance with 1508 DSPs on the 32-bit floating-point accelerator is 1508

× 2 × 0.1 GHz= 60.3 GFLOPS, while our attainable end-to-end test is 46.99 GFLOPS including pooling and ReLU operations.

Comparison with State-of-art Works Comparisons of the best performance between our design and other state-of-art FPGA-based training accelerators are shown in Table 9. In the table, "N/A" means that the metric is not provided, and "≈" means that the value is obtained by approximate estimation. Since the platforms, the neural networks for training, and the data type are different, it is extremely difficult to fairly compare between different training accelerators. However, our design still shows desirable performance even under such circumstances.

To better illustrate the uniqueness of the proposed design, we also compare our work with the accelerators that also adopted 32-bit floating-point. The comparisons are shown in Table 10 and Table 11. The design in [36] was tested on LeNet-10 which is a really small network with the structure as Conv 1 ([𝑀𝑖, 𝑁𝑖, 𝑅𝑖,𝐶𝑖, 𝐾𝑖,𝑆𝑖] = [32, 3, 32, 32, 3, 1]) - Pooling - Conv 2 ([32, 32, 16, 16, 3, 1]) - Pooling - Conv 3 ([64, 32, 8, 8, 3, 1]) - Pooling - FC ([64, 1024, 1, 1, 1, 1]) - FC ([10, 64, 1, 1, 1, 1]). As explained in Section 6.3, the underutilization of computation resources in the first Conv layer reduces the overall throughput. Therefore, the performance of the proposed design on this small network cannot be as superior as that in deeper networks like Vgg-16. However, our design is a general architecture that can support both small networks and larger networks, while the accelerator in [36] only targeted such small networks. It first achieved feature-map level parallelism in a uniform computation engine, and then unrolled channel-level parallelism factors to improve utilization of computation resources. For the memory access issues, the input and output features of each layer are all stored on the FPGA chip, which restricts the work from extending to support the networks where the on-chip BRAMs are not large enough to hold entire features of a Conv layer. However, larger networks like AlexNet and Vgg are commonly applied in practical applications. Unlike [36], our work not only enables on-device training on larger CNN models but also achieves higher throughput when the network becomes deeper. Besides, the number of operations of LeNet-10 reported in [36] is 74.43 MFLOPs. However, according to 𝑡𝑜𝑡𝑎𝑙𝑛𝑢𝑚𝑏𝑒𝑟𝑜𝑓𝑡𝑟𝑎𝑖𝑛𝑖𝑛𝑔𝑜𝑝𝑒𝑟𝑎𝑡𝑖𝑜𝑛𝑠= 2 × (3 × Í𝑛 𝑖=1 𝑀𝑖× 𝑁𝑖× 𝑅𝑖× 𝐶𝑖× 𝐾𝑖× 𝐾𝑖−𝑀1 × 𝑁1 × 𝑅1 × 𝐶1 × 𝐾1 × 𝐾1), the actual number of operations that we obtain is only 25.17 MFLOPs. In this formula, 2× is due to the FP 32 data type, and 3× is due to the fact that each layer needs to conduct FP, BP, and WU except the 1st layer which only needs to conduct FP and WU.

The FeCaffe [41] introduced a Caffe framework with OpenCL which can integrate FPGA to perform CNN network training. It only provided DSP utilization and throughput which are shown

**Table 9.** Comparison of Different FPGA-based Training Accelerators

Accelerator Chow et al.

2017 [36] DarkFPGA

2020 [23] Seo et al. 2020 [40] FeCaffe 2020 [41]

ZU19EG XCVU9P Stratix 10 MX Stratix 10 Technology 16nm 16nm 14nm 14nm 16nm DSP Util. Freq. (MHz) ≈20 Network LeNet-10 Vgg-like ResNet-20 Vgg-16 Dataset CIFAR-10 CIFAR-10 CIFAR-10 ImageNet ImageNet Data Type FP 32 Fixed 8 FP 16 FP 32 FP 32 GFLOPS

GOPS

≈180 GFLOPS

≈24 GFLOPS

GFLOPS Energy Effi. GFLOPS/W

GOPS/W

≈9 GFLOPS/W

GFLOPS/W Nominal Thro.(GOPS × precision)

≈2880 ≈768

Nominal Effi. (GOPS × precision/W)

≈144

**Table 10.** Experimental Results on LeNet-10 Compared with Chow et al. [36]

Chow et al. [36]

ZU19EG

in Table 11. Compared to the FeCaffe framework, our design utilized fewer computation resources but achieved higher throughput implementing AlexNet.

The work in [40] also adopted both feature-map level parallelism and channel-level parallelism, similar to its preliminary work in [22]. The best nominal energy efficiency reaches 144 (GOPS × precision) which is lower than our best nominal energy efficiency which is 194.88 (GOPS × precision). As for the memory access issues, the accelerator in [40] targeted devices equipped with high bandwidth memory (HBM2). Compared with DMA, the HBM2 is superiorly advanced with 16 pseudo channels providing a high number of I/O data pins. However, HBM2 is a new high-speed memory technology and is only integrated into a few modern FPGAs like Stratix 10 MX. Most FPGA-based edge devices still rely on DMA to communicate between the FPGA chip and off-chip DRAM. Besides, [22] and [40] only tested their designs on the Cifar-10 dataset where the input

**Table 11.** Experimental Results on AlexNet Compared with FeCaffe [41]

FeCaffe [41]

Stratix 10 ≈24 GFLOPS

image size is only 32 × 32 which is really small so that their on-chip BRAMs can easily hold 𝑃entire feature maps, where 𝑃is the unrolling factors in the channel dimension. However, our design can support both small and large feature map sizes.

DarkFPGA [23] placed DRAM data layout in the channel-height-width-batch (CHWB) pattern based on its batch-level parallelism-based design. It achieves higher nominal energy efficiency because the 8-bit fixed points can improve the energy efficiency and DSP efficiency out of proportion. The previous study has shown that if the data precision is no more than 8-bit, two MACs can be calculated on one Xilinx DSP48, reducing the DSP usage by half [42]. However, for 32-bit floatingpoint, 1 MAC operation takes up 5 DSPs in the Xilinx FPGA board. Besides, XCVU9P is an extremely high-end cloud-level FPGA that has superior efficiency than commonly used edge FPGAs. However, as mentioned in Section 2.3, the batch-level parallelism adopted by DarkFPGA only achieved high throughput when the batch size is large. From their experiments, when the batch size is below 16, its throughput is below 100 GOPS which is around 800 GOPS×precision after nominating, while our nominal throughput is stably above 1000 GOPS×precision among different batch sizes. Besides, same with [22, 40], DarkFPGA also implemented their design on Cifar-10 dataset with a relatively small feature map size.

CONCLUSION In this paper, we design EF-train, an efficient DNN training accelerator enabling edge FPGAs to continuously learn on the device, which makes it possible for current FPGA-based edge-level applications to achieve domain adaption and personalization. We propose an FPGA-based CNN training accelerator with a unified convolution kernel to process FP, BP, and WU with full precision and a data reshaping approach to ensure continuous memory access during end-to-end training processes. We implement end-to-end CNN training effectively for low-power edge devices with restricted resources. The experimental results show that our design achieves 46.99 GFLOPS and 6.09 GFLOPS/W in terms of throughput and energy efficiency, respectively.
