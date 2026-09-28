---
id: 2023-montgomerie-corcoran-satay-streaming-architecture-toolflow-accelerating
title: "SATAY: A Streaming Architecture Toolflow for Accelerating YOLO Models on FPGA Devices"
year: 2023
backend: grobid
---

## Abstract

{ alexander.montgomerie-corcoran15, petros.toupas21, zhewen.yu18, christos-savvas.bouganis }@imperial.ac.uk

## I. INTRODUCTION

Object detection is a fundamental concept in computer vision, enabling machines to identify and locate objects in images or videos. It has wide-ranging applications, from autonomous driving [1] to surveillance systems [2] and medical imaging [3]. Advancements in object detection, driven by novel model designs, aim to achieve real-time performance. One category of such extremely fast and efficient models is the YOLO family, which achieves state-of-the-art performance in object detection benchmarks [4], [5].

Accelerating YOLO networks on FPGA devices can significantly improve their inference speed, enabling faster execution compared to traditional CPU or GPU implementations, and are well-suited for real-time object detection. Many previous research works [6], [7] focused on the optimisation of the computationally intensive convolutional layers on FPGA fabrics, and offloaded the other operations to CPUs. Such heterogeneous overlay-based designs offer flexibility to deploy various versions of YOLO networks; however, they are severely constrained by the data communication bottlenecks between FPGAs and CPUs. Other works [8]- [10], have explored the deployment of the entire YOLO network onto the FPGA device, by building customised computation units and data flows into their accelerator designs. As such, the impact of data communication bottlenecks is minimised and the overall performance is enhanced. However, the proposed accelerator designs in these works are tailored to specific versions of the YOLO network, and lack the versatility to target more modern object detection models. The lack of easy adaptation hinders the hardware community from keeping up with the latest advancements in the state-ofthe-art versions of the YOLO family.

In this paper, we introduce a toolflow that enables the mapping of diverse models from the YOLO family onto a wide range of FPGA devices. Our toolflow is designed to achieve both high performance and versatility by tackling the following challenges: a) Diverse Operation Libraries: When accelerating YOLO networks on FPGAs, it is crucial to have efficient hardware implementations for both standard operations, such as convolution and max pooling, as well as custom operations specific to YOLO models, such as leaky ReLU, SiLU, and resize.

b) Long Skip Connections: YOLO networks rely on multi-scale feature fusion to detect objects of different sizes. This process involves merging feature maps from different stages of the network, which leads to long skip connections in the computation graph. This requires extensive buffer placement for streaming architectures. c) Large Design Space: Over the generations of YOLO models, there has been a discernible trend towards deeper network architectures, with 47 new layers introduced since YOLOv3. The increased complexity and size of the network architectures has brought increased difficulty in finding optimal hardware configurations.

Our toolflow addresses these challenges by introducing novel streaming hardware components for YOLO-specific operations, applying fine-grain quantization methods to alleviate on-chip memory resource constraints, and implementing a software FIFO to further reduce the on-chip memory usage. Automated design space exploration is performed with these, generating hardware designs which surpass edge-GPU performance, and achieve state-of-the-art performance compared to FPGA accelerator designs.

## II. BACKGROUND & RELATED WORK

### A. Object Detection

Object detection is a fundamental computer vision task that aims to identify and locate objects within images or videos. This task involves detecting the presence of objects in an image and accurately determining their spatial boundaries, while assigning a specific category or label to each detected object.

To achieve accurate object detection, state-of-the-art methods can be broadly classified into two categories:

One-stage Methods: such as YOLO (You Only Look Once) [11], SSD (Single Shot MultiBox Detector) [12], and RetinaNet [13], prioritise fast inference speed. These models efficiently detect objects by directly predicting bounding boxes and class probabilities in a single pass through the network.

Two-stage Methods: including Faster R-CNN (Region Convolutional Neural Network) [14], Mask R-CNN (Mask Region Convolutional Neural Network) [15], and Cascade R-CNN [16], focus on achieving higher detection accuracy. These approaches typically involve a preliminary region proposal step followed by a fine-grained object classification and localisation step. Although two-stage methods are computationally more expensive, they often yield superior detection performance.

### B. The YOLO Model Family

Since its initial release [11] in 2016, several versions of YOLO have been developed, each improving on accuracy and efficiency. The major limitation of the initial YOLO model was its inability to detect small objects. In order to enhance the network's ability to detect objects of various sizes, YOLOv2 [17], v3 [18] and v4 [19] incorporated anchor boxes, feature pyramid networks, and path aggregation networks in their designs respectively.

The basic building components of the network have also witnessed improvements in computational efficiency. From YOLOv4, the plain feedforward convolutions have been replaced by the Cross Stage Partial (CSP) Blocks, which is a variation of the residual block that incorporates crossstage connections for enhanced feature representation [19]. In YOLOv6 and v7, the Reparameterized Block has been incorporated which includes convolutions with different kernel sizes in parallel at training time [20]- [22].

The advancements in the YOLO family have enabled accurate and efficient object detection. However, they have also increased the number of operation types and the complexity of layer interconnection. This presents research opportunities in hardware accelerator designs on FPGA devices, aiming to outperform CPUs and GPUs. In this work, we focus on the YOLOv3, YOLOv5 and YOLOv8 families of architectures, as they represent the most dramatic changes in network architecture as well as accuracy and workload, across the generations of models.

### C. FPGA Object Detection Acceleration

The field of research into object detection acceleration has focused on one-stage methods [23], [24], due to their efficient network architectures. Several studies have explored FPGA-based accelerators for YOLO networks in particular, capitalising on the flexibility and customisation offered by FPGAs. Accelerators for YOLO-v2 were implemented in [6], [25], with notable performance advantages over embedded CPUs and GPUs. Both studies employed weight binarization techniques to reduce computation costs and memory requirements. Additionally, they adopted a sequential computation order, allowing the convolutional layers to share the computation resource effectively. Building upon this sequential computation approach, [8], [9] and [26] further extend this line of work to YOLOv3, v4 and v5 respectively, accommodating the customised operations involved in each version. As network designs became more compact and less redundant in evolving versions, the quantization strategies in these studies also became less aggressive. [8] utilised a combination of 1bit and 8-bit quantization, while both [9] and [26] opted for 16-bit quantization instead.

The aforementioned studies focused on designing accelerators for specific versions of the YOLO family, achieving notable computational efficiency. However, there is a considerable time delay between advancements in machine learning and hardware communities. Currently, there is a lack of published performance results for running the latest YOLOv8 on FPGA devices owing to the challenges discussed in Section I. In this work, we present a toolflow that enables the mapping of various YOLO models (from v3 to v8) onto a wide range of FPGA devices. Our approach differs from related work such as Vitis-AI [7], which builds heterogeneous accelerators across CPUs and FPGAs. Instead, we focus solely on FPGA devices and employ a fully pipelined streaming architecture to maximise performance and efficiency.

## III. HARDWARE ARCHITECTURE

This section outlines the streaming architecture and the hardware building blocks which have been designed and tailored to the YOLO model family.

### A. Streaming Architecture

A streaming architecture [27]- [30] design principle is taken for the FPGA accelerators generated by our toolflow. Streaming architectures follow an elastic circuit [31] design paradigm, where computation nodes communicate in a pure data flow manner, with ready/valid handshake interfacing. In the case of neural network acceleration, these computation nodes correspond to nodes in the machine learning graph. This design style leads to deeply pipelined architectures that make efficient use of on-chip routing bandwidth.

To illustrate the general data flow of a generated design, Figure 2 shows an example block diagram of a YOLOv5 accelerator." It can be seen that each machine learning operation is implemented as a dedicated hardware block within the FPGA fabric. The execution of the hardware begins when the input image is streamed into the hardware from off-chip DDR memory, with an 'NHWC" format. The computational pipeline within the FPGA processes the input image, producing the bounding box predictions at the output, which are returned to off-chip memory. The only other external connections are that of the off-chip buffer, which is discussed in Section IV-C. During execution, all the model's parameters stay on-chip, requiring no off-chip memory accesses.

The streaming architecture approach taken has many benefits over alternative single-engine accelerators. The designs are able to exploit the inherent parallelism found in YOLO model architectures. Storing the weights on-chip dramatically reduces the off-chip memory bandwidth requirements, a bottleneck commonly seen in most other architecture designs.

### B. Building Blocks

The streaming architectures described in this work are composed of a number of building blocks. The design of such building blocks follows a dataflow approach, with ready/valid interfaces, and are tailored to the set of operations required by the YOLO family, in particular the Resize and HardSwish components. Parallelism can be exploited in all of the building blocks and it is discussed in Section IV-B.

### Weights Weights Accumulation Accumulation

Line buf

### Line buf

Line buf

### Line buf

Fig. 3: Convolution building block.

### a) Convolution:

The hardware implementation of the convolution operation is shown in Figure 3. A sliding window generator comprised of line buffers feeds a matrix-vector multiplication engine, generating partial sums which are then accumulated. The parallelism across inputs as well as within the kernel itself is illustrated. The sliding window generator leads to very efficient usage of on-chip memory, requiring only (K -1) × W × C of words of a feature map to be stored on-chip. The matrix-vector multiplication engine contains an array of K × K DSPs. Parameters for the convolution are stored on-chip in URAM and BRAM, alleviating the memory bandwidth bottleneck common in systolic array architectures.

b) Max Pooling: The max pooling operation utilises a similar architecture to the convolution hardware. A sliding window generator feeds a comparator tree, which discovers the maximum value in the window. This component also benefits from the efficient on-chip memory needed by the sliding window generator. d) Split, Concat and Add: These components constitute the branching and merging operations seen in YOLO models. The split hardware separates channels of the feature map, which appear sequentially in the stream, using a demultiplexer. Conversely, the concat hardware combines the channel dimensions of several feature maps using a stream multiplexer. Both components require buffering for the channel dimension to prevent unnecessary back-pressure. The add hardware performs an element-wise addition of data from two streams.

### e) Leaky ReLU and HardSwish:

The activation functions used in the latest YOLO models are Leaky ReLU and SiLU, both of which are significantly more resource-intensive than ReLU. In particular, the SiLU operation involves computing the sigmoid function, which requires costly floating point hardware. Instead, the HardSwish activation [32] is used (x•RELU 6(x+3)/6), which has a lot more efficient hardware implementation, as seen in Figure 7a. Despite HardSwish being an approximation of the SiLU function, we demonstrate in Section VI that it has a negligible impact on accuracy. The implementation of Leaky ReLU involves a multiplication with a constant, as well as a multiplexer for inputs above zero.

## IV. DESIGN SPACE EXPLORATION

This section outlines the design space exploration performed to discover efficient designs for YOLO accelerators. The design space exploration outlined is a component of a toolflow that automates the mapping of a YOLO model to FPGA bitstream. The stages of the toolflow are outlined below.

1) Parsing: ONNX model is parsed into an Internal Representation (IR). 2) DSE: Design space exploration is performed on the IR. 3) Generation: A bitstream is generated from the IR. This work uses the open-source toolflow SAMO [33] as a skeleton framework, which follows a similar approach to the other toolflows, namely fpgaConvNet [27] and FINN [30]. The design space exploration in this work focuses on resource allocation for both increasing performance and meeting on-chip resource constraints. For reference, a taxonomy of symbols used in this section is given in Table I.

### A. Quantization

Due to the requirement of storing parameters on-chip, quantization techniques are employed to drastically reduce the resources required. During the parsing step, our toolflow accepts ONNX models in the floating point format and simulates the quantization effect using the ONNX runtime. We adopt a layer-wise blocking floating point format, where the weights are quantized as follows:

w = round( w S -Z) (1)

w is the original floating-point weights and w is its integer format. The parameters scale S and zero point Z are chosen based on the minimum and maximum of the weights within the same layer, as well as the wordlength w w chosen for quantization.

S = w max -w min 2 L -1(2)

Our quantization process is performed post-training, and directly applied to pre-trained weights without additional finetuning. We further explore the impact of wordlength choice for weights quantization, as depicted in Figure 8. The results indicate that quantization has minimal effect on the accuracy of YOLO models, as long as the wordlength w w is at least 8 bits. In all these experiments, activations are also quantized, with their wordlength w a fixed at 16 bits.

### B. Performance Optimisation

Within streaming architectures, the performance is dictated by the slowest node within the accelerator. The performance can be improved by increasing parallelism within the node, at the cost of increased resources. The resources that are affected by increased parallelism are the look-up table and embedded multiplier resources. As can be seen in Table III, the main constraint on designs is the DSPs, and therefore we focus our resource-constrained optimisation solely on DSP allocation.

### Algorithm 1 DSP Allocation Algorithm

Initialise all parallelism factors to 1

p n = 1 ∀ n ∈ [1..N ];

Iterate until all DSPs are utilised while

N n=1 r DSP (n) < R DSP do n = 1

Start with the first node

L base = L(p)

Calculate baseline latency To assist with the design space exploration, models of performance and resources are developed. The purpose of modelling is to allow for rapid evaluation of a design point and alleviate any need for performing synthesis and place and route in order to obtain performance and resource metrics. This allows for magnitudes greater design points to be evaluated within a reasonable period of time. To begin with, a model for the latency of a node n in the accelerator is given as,

Δ prev = 0 zero performance improvement for m in [1..N ]

l(n, p) = Hn•Wn•Cn•Fn pn•f clk if Convolution Hn•Wn•Cn pn•f clk otherwise

where l(n, p) is the latency model, p n is the parallelism factor, and f clk is the clock frequency of the design. The general principle of the latency model is that each node has a workload to execute, which will take that many number of cycles. By increasing parallelism within the node, this workload can be executed in parallel, reducing the latency by the parallelism factor. The latency for the whole design with N nodes is described as,

L(p) = max n∈[1..N ] l(n, p) + N n=1 d(n) f clk

where d(n) is the pipeline depth in cycles of each node n. This latency model states that the latency is dictated by the slowest node in the accelerator plus the time taken for data to pass through the pipeline.

To evaluate the impact on resources, a model of DSP usage for each type of node is given below.

r DSP (n, p) = ⎧ ⎪ ⎪ ⎪ ⎨ ⎪ ⎪ ⎪ ⎩ K 2 • p n if Convolution 2 • p n if HardSwish p n if Leaky ReLU 0 otherwise

Using the performance and resource models, an optimisation problem can be formulated for maximising the performance of the accelerator design, as shown below,

max p L(p) s.t. N n=1 r DSP (n, p) < R DSP

where R DSP is the available DSP resources of the FPGA. To solve this optimisation, a greedy algorithm was created, and is described in Algorithm 1.

### C. Memory Allocation

The memory allocated on-chip consists of three components: weight parameter storage, feature map caching in the sliding window line buffers, and buffering required for skip connections. A summary of the relative size of these memory components alongside where in the system they are allocated is shown in Table II. The weights storage contributes to the majority of memory required by the streaming architecture system. Due to the deeply pipelined hardware architecture, the weights are required to stay on-chip as their bandwidth requirements are too large to transfer off-chip. This can lead to large on-chip memory requirements, with up to 26MB of memory needed within the FPGA. Therefore there is motivation to reduce the on-chip resources of the next largest memory component, the skip connection buffers.

The deep connections between components of YOLO models require extensive buffering for a single partition streaming architecture. Figure 2 illustrates the variety of skip connections used in YOLO models, and the corresponding FIFOs required. To reduce the on-chip memory resources required by implementing buffers on-chip, we instead move the buffering off-chip by implementing an off-chip software FIFO.

The software implementation in Listing 1 describes a FIFO which concurrently reads and writes to a block of memory in def fifo(dma_in, dma_out, depth, chunk_size=256): # set the chunk counters chunk_cntr_in, chunk_cntr_out = 0, 0 # allocate 2D array of memory mem = np.array((depth, chunk_size)) # execute until transfer is complete while cntr_in < depth and cntr_out < depth: Listing 1: A simplified implementation of the software FIFO in Python, which can be used with the PYNQ framework.

#

### Algorithm 2 Buffer Allocation for Skip Connections

Initialise all buffers on-chip

t buf n,m = ON ∀ n ∈ [1..N ], m ∈ [1..N ];

Iterate over buffers, sorted by largest first

for n, m in sorted([[1..N ], [1..N ]], d(i, j)) do Check if on-chip memory is over-utilised if N n=1 N m=1 s buf (n, m, t buf ) > S avail then t buf n,m = OFF

Re-assign memory to off-chip else break Allocation Complete a first-in, first-out order. To make the software FIFO hardware friendly, chunks of words rather than individual words are transferred, making more efficient use of the bursting abilities of the DMA. A choice of chunk size greater than the DMA burst size leads to no performance degradation. The choice of implementing buffers off-chip has implications in terms of on-chip memory resources and off-chip memory bandwidth. To navigate this design space, we have created an automated methodology for allocating off-chip memory buffers. To do so, we introduce the optimisation variable t buf n,m ∈ {ON, OFF} which dictates the location for a buffer connecting node n to node m.

The off-chip memory bandwidth for a buffer is given as,

b buf (n, m, t buf ) = 2 • Sn,m•wa L if t buf n,m = OFF 0 otherwise(4)

where

S n,m = H n,m × W n,m × C n,m

is the size of the feature map transmitted through the buffer, w a is the wordlength of the activations, and L is the latency of the accelerator design. The on-chip memory requirements are described as,

s buf (n, m, t buf ) = q(n, m) • w a if t buf n,m = ON 0 otherwise(5)

where q(n, m) is the depth of buffer required between nodes n and m. These depths are obtained from buffer depth analysis during simulation.

The objective of the buffer allocation is to discover a design which fits within on-chip memory constraints, whilst minimising off-chip memory bandwidth consumption. Additionally, the number of off-chip memory buffers should be reduced due to the additional resource overheads of DMAs. This optimisation objective for this is described as,

min t buf N n=1 N m=1 b buf (n, m, t buf ) + λ • N n=1 N m=1 (t buf n,m = OFF) s.t. N n=1 N m=1 s buf (n, m, t buf ) < S avail

where λ is a regularisation hyper-parameter for penalising the number of off-chip memory buffers, and S avail is the remaining available on-chip memory space after weights and sliding windows are allocated. For the streaming architecture designed in this work, the memory bandwidth overheads are insignificant (see Figure 9c). Therefore, the buffer allocation methodology for our architecture focuses on moving the largest buffers off-chip first. This is outlined in Algorithm 2.

## V. ABLATION STUDY

In this section, we evaluate the off-chip FIFO allocation method for supporting YOLO models in streaming architectures. An ablation study was performed on the YOLOv5n model targeting the ZCU104 FPGA board. Initially, all buffers were allocated on-chip. These buffers were then ordered by their depth, and the top five buffers were sequentially moved to off-chip memory using the software FIFO implementation.

The results of the ablation study are presented in Figure 9. Across the figures, it can be observed that the first three results have the greatest impact on on-chip memory resources as well as off-chip memory bandwidth utilisation. This coincides with the buffer allocation chosen by the method described in Algorithm 2, demonstrating the method's effectiveness. The impact on on-chip memory resources by re-allocating buffers can be seen in Figure 9a. Removing the first five buffers reduces the buffer memory by 56%, with an overall reduction of 17% for the whole on-chip memory. For resourceconstrained devices, these savings can enable the mapping of larger networks onto these devices. The impact of this can be seen in greater detail in Figure 9b. The resource savings of buffer allocation can bring a design within resource constraints, by allocating the largest buffer off-chip.

The trade-off when allocating buffers off-chip is increased memory bandwidth utilisation, which is highlighted in Fig- ure 9c. Moving five of the buffers off-chip leads to a 35% increase in off-chip memory bandwidth utilisation, resulting in 2.15 Gbps of bandwidth. However, the total off-chip memory bandwidth is insignificant compared to the 135 Gbps of offchip memory bandwidth available. This is one of the major benefits of streaming architectures, which make efficient use of the available on-chip memory and bandwidth.

## VI. EVALUATION

In this section, we evaluate the accelerators auto-generated by SATAY. For hardware synthesis, Vivado 2020.1 is used. Our toolflow currently supports AMD FPGA devices, and we have investigated designs for the U250, ZCU104, VCU110, VCU118 devices in this evaluation.

### A. Comparison with other FPGA designs

Table III shows a comparison between the accelerator designs generated by our toolflow, and designs from prior works, for a selection of YOLO models and FPGA platforms. One key benefit of our toolflow is its versatility, as we are able to produce a range of accelerators for different models of the YOLO families, including the state-of-the-art YOLOv8 models, of which this is the first FPGA implementation within the literature. Furthermore, the generated designs achieve exceptionally high performance density, with the YOLOv8s VCU110 accelerator achieving 8% greater GOP/s/DSP than the next best fixed-point accelerator. The performance and accuracy of the various accelerators are explored in more detail in both Table III and Figure 1. When comparing the designs with the same model, our designs achieve 1.1-3.4× GOP/s/DSP on YOLOv3-tiny compared with [10], [34], [35], and 7.3× GOP/s/DSP on YOLOv5s compared with [26]. Nguyern's design [8] achieved significantly higher efficiency than other related works, due to weight binarization. However, their method has only been tested on YOLOv2. As future work, We will investigate if weight binarization can also be applied to the latest, compact YOLO-v8 model.

Overall, our toolflow can generate all the points on the performance density and accuracy Pareto front, as Figure 1 shows, demonstrating both the efficiency of the streaming architecture and the effectiveness of the design space exploration.

### B. Comparison with CPU and GPU

To further evaluate the efficiency of our toolflow, we compare our generated FPGA designs with embedded CPU (ARM Cortex-A72) and GPU (Jetson TX2) devices in Figure 10. For a fair comparison, we have picked FPGA designs with comparable energy consumption to the CPU and GPU, and we observe our FPGA designs have an average of 79× and 3.6× speed-up than the CPU and the GPU, over a wide range of YOLO models.

A more detailed comparison between our auto-generated FPGA designs and the Jetson TX2 GPU can be found in Figure 11 and Table IV. In Figure 11, while the large U250 device has a much larger energy overhead, the rest of the Fig. 11: Energy per inference used during the execution of YOLOv5n models on varying image sizes (320 × 320, 640 × 640). We compare our generated accelerator designs on different FPGA platforms to a Jetson TX2 GPU device.

FPGA devices have comparable energy per inference to that of the GPU, especially when accelerating the detection for the larger image size (640 × 640). In Table IV, it can be seen that the comparable ZCU104 device has much greater performance compared to the Jetson, despite similar power profiles.

## VII. CONCLUSION

This paper presents SATAY, a Streaming Architecture Toolflow for Accelerating YOLO networks on FPGA devices. By addressing the challenges of deploying state-of-the-art object detection models onto FPGA devices for ultra-low latency applications, SATAY automatically generates high performance accelerators. Resulting accelerator designs outperform existing FPGA accelerators, demonstrating competitive performance and energy efficiency compared to CPUs and GPUs.

## ACKNOWLEDGMENT

For the purpose of open access, the author(s) has applied a Creative Commons Attribution (CC BY) license to any Accepted Manuscript version arising.

## Figures et tableaux

**Fig. 1:** Comparison between the accuracy and performance of FPGA accelerator designs generated by our SATAY toolflow and prior works, for the COCO dataset. Our toolflow demonstrates state-of-the-art performance for YOLO model inference, defining the Pareto frontier.

1 DDRFig. 2: Fig. 2: An example of the YOLOv5 accelerator generated by our toolflow. Black arrows show on-chip data flow, while blue arrows show off-chip data flow. Dashed black lines show the skip connections that are diverted to off-chip (Section IV-C).

**Fig. 4:** Max pooling building block.

**Fig. 5:** Fig. 6: Fig. 5: Resize building block.c) Resize:The resize hardware uses a sliding window generator to cache a window of words from the current and previous rows of the feature map. The words are then selected and duplicated by a MUX with data-dependent control logic. This novel hardware performs the resizing operation on the fly, requiring minimal buffering.

**Fig. 7:** Activation building blocks.

**Fig. 8:** Fig.8: Quantization results on YOLOv3, YOLOv5, and YOLOv8 and all of their variants. The x-axis shows the exploration of different weight wordlengths. The activation's wordlength is fixed at 16 bits throughout these experiments. Models are evaluated on the COCO-val2017 dataset.

**Fig. 9:** Fig.9: Ablation study on moving the top 5 largest buffers to off-chip memory, within a generated design for a 640x640 YOLOv5n model. The impact on on-chip memory resource usage, off-chip memory bandwidth utilisation, and LUTRAM usage is shown. In Figure9b, the red line depicts the maximum LUTRAM usage for the ZCU104 FPGA platform.

**Fig. 10:** Comparison of the different versions of YOLO models (v3, v5, v8) across three different devices (ARM Cortex-A72, Jetson TX2, VCU118 (SATAY)). The input image size used for v3 models is 416×416 and for the v5, v8 models is 640×640. The results were obtained on the COCO-128 dataset.

**TABLE I:** Taxonomy of symbols used during DSE.

    Symbol | Description
    H, W | Spatial dimensions of feature map
    C | Channel dimension of feature map
    F | Filter dimension in convolution
    K | Kernel size of convolution and pooling
    ww, wa | Wordlength of weights and activations
    pn ∈ p | Parallelism of node n
    t buf n,m ∈ t | 

[figure sans légende identifiée] do Increase the parallelism of node m p = {p 1 , ..., p m-1 , p m + 1, p m+1 , ..., p N }

    Performance improvement of increasing p m
    Δ m = L base -L( p) | 
    Check if improvement greater than previous best
    if Δ m < Δ prev then | 
    n = m | Update best candidate node
    Δ prev = Δ | 

**TABLE II:** Summary of typical memory types and utilisation.

    Memory Type | Utilisation | On-Chip
    Weights | 50% -89% Yes
    Feature Maps (Sliding Window) | 4% -20% | Yes
    Feature Maps (Skip Connections) | 7% -30% | Partial

**TABLE IV** 

    : Accuracy, performance, energy and power results
    on YOLOv5n over different FPGA platforms, as well as a
    Jetson TX2 GPU device. |  |  | 
     | U250 | ZCU104 VCU110 VCU118 | Jetson TX2
     |  | YOLOv5n (320 × 320) | 
    mAP50 (%) |  |  | 21.2 |  | 22
    Latency (ms) | 3.72 | 9.83 | 4.92 | 2.21 | 10.73
    Power (W) | 115.94 | 14.82 | 23.88 | 63.27 | 6.59
    Energy (mJ) | 431.05 | 142.6 | 117.5 | 139.81 | 70.71
     |  | YOLOv5n (640 × 640) | 
    mAP50 (%) |  |  | 26.7 |  | 27.7
    Latency (ms) | 5.22 | 21.41 | 11.73 | 4.64 | 32.28
    Power (W) | 105.51 | 14.5 | 22.75 | 60.27 | 8.58
    Energy (mJ) | 550.86 | 317.33 | 266.88 | 279.8 | 276.96
