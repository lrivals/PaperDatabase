---
id: 2024-zhang-end-end-acceleration-yolo-object
title: "End-to-end acceleration of the YOLO object detection framework on FPGA-only devices"
year: 2024
backend: pymupdf
---

ORIGINAL ARTICLE

End-to-end acceleration of the YOLO object detection framework on FPGA-only devices

Dezheng Zhang1,2 • Aibin Wang1,2 • Ruchan Mo1,2 • Dong Wang1,2

Received: 23 December 2022 / Accepted: 14 September 2023 / Published online: 13 November 2023  The Author(s), under exclusive licence to Springer-Verlag London Ltd., part of Springer Nature 2023

## Abstract

Object detection has been revolutionized by convolutional neural networks (CNNs), but their high computational complexity and heavy data access requirements make implementing these algorithms on edge devices challenging. To address this issue, we propose an efﬁcient object detection accelerator for YOLO series algorithm. Our architecture utilizes multiple dimensions of parallelism to accelerate the convolution computation. We employ line-buffer-based parallel data caches and dedicated data access units to minimize off-chip bandwidth pressure. Additionally, our proposed design not only accelerates the convolutional computation, but also control-intensive post-processing to achieve low detection latency. We evaluate the ﬁfinal design on Xilinx V7-690t FPGA device, achieving a throughput of 525 GOP/s for a batch size of 1 and 914 GOP/s for a batch size equal to 2. Compared with state-of-the-art YOLOv2 and YOLOv3 implementations, our proposed accelerator offers up to 9 throughput improvement and 5 shorter latency.

Keywords Convolution neural networks (CNN)  Object detection  YOLOv2  Field-programmable gate array (FPGA)  High-level synthesis (HLS)  Accelerator architecture  Post-processing

## 1 Introduction

Deep learning-based object detection algorithms have been applied in many ﬁfields, such as autonomous driving [1], medical image detection [2], and industrial inspection [3]. However, these algorithms still face some crucial problems, such as the high computational workload and bandwidth requirement of the convolutional neural network (CNN) computation, which restricts the actual application. Although a few object detection accelerators have been

proposed, they still face some challenges. In approach [4, 5], two streaming object detection accelerators are designed, which map all the CNN layers within the on ﬁfield programmable gate array (FPGA). All nine convolution layers are pipelined, which reduces off-chip data access improves throughput. Though low latency and high digital signal processor (DSP) efﬁciency are achieved, it is challenging to implement very deep CNN algorithms such as YOLOv2 or YOLOv3 on them because the number of layers is restricted by the hardware resource. In the approach [6], an implementation of YOLOv3-Tiny is proposed, which achieves 460GOPS/s on the VC707 development board with a data width of 18-bit. Similarly, the work in the literature [7] introduced fast Fourier transform (FFT) to speed up the convolution operation. However, feature maps and weights are represented by relatively high bit width data types, i.e., 16-bit ﬁfixed-point numbers. This causes a higher consumption computational memory resources. In contrast, most CNN models can be represented by 8-bit data with negligible loss of accuracy, according to recent quantization research [8]. Lower data bit width can reduce DSP and memory consumption on

& Dong Wang

wangdong@bjtu.edu.cn

Dezheng Zhang dezhengzhang@bjtu.edu.cn

Aibin Wang 21120301@bjtu.edu.cn

Ruchan Mo moruchan@bjtu.edu.cn

Institute of Information Science, Beijing Jiaotong University, Beijing 100044, China

Beijing Key Laboratory of Advanced Information Science and Network Technology, Beijing 100044, China

(0123456789().,-volV)(0123456789(). ,- volV)

FPGA, which enables the design to achieve equivalent performance with fewer hardware resources and lower energy consumption.

Furthermore, in most accelerator designs [4–6, 9], the pre- and post-processing algorithms, such as the softmax layer, intersection-over-union (IOU) calculation, and nonmaximum suppression (NMS), are typically implemented on central processing units (CPUs). However, in certain scenarios with stringent latency requirements, CPU-based implementation schemes can often fail to satisfy the low latency demands, as indicated by studies of [10, 11]. For instance, in industrial robotics, detecting targets within a brief latency window is crucial. This imposes strict requirements not just on the CNN computational latency but also on the post-processing latency. Therefore, it becomes necessary to devise an object detection accelerator that incorporates a dedicated hardware unit for postprocessing algorithms.

In this work, an end-to-end YOLO-based object detection hardware accelerator targeting implementation on FPGA fabric-only devices is proposed. The accelerator is designed with a ﬂflexible architecture in which each layer of the convolutional neural networks are computed in a sequential way so that it is possible to implement object detection algorithms with different sizes, e.g., YOLOv2 and YOLOv3. However, this structure increases the difﬁculty of data accessing and caching. To address this challenge, three data access units and an on-chip buffer are designed, where the former utilize the burst transfer to fully take advantage of the off-chip bandwidth, and the latter improves the on-chip data reuse. Moreover, the data access is overlapped with the convolution computation. The proposed accelerator is ﬁfinally implemented and evaluated on the Xilinx’s V7-690t FPGA device showing a throughput improvement of up to 9 compared to the previous implementations [4, 6, 9] for YOLOv2 or YOLOv3. Furthermore, the pre- and post-processing of the algorithm are also conducted on the FPGA fabric, which further decreases the detection latency.

In summary, the main contributions of this paper are summarized as follows.

(1) A novel end-to-end object detection accelerator targeting FPGA-only devices is proposed. proposed architecture is scalable in multiple computational dimensions, enabling efﬁcient acceleration of complex object detection neural network models, such as YOLOv2 and YOLOv3, on devices with varying resource constraints. In addition, FPGA fabrics are utilized to expedite post-processing operations in the object detection algorithms, thereby minimizing detection latency. Our design offers a unique approach to object detection acceleration,

which addresses the challenges of deploying large network models on FPGA-only devices. (2) An on-chip data caching strategy is proposed, which overlaps the data transfer time with convolutional computation, resulting in improved execution efﬁciency of the accelerator. The proposed approach utilizes a ping-pong buffer to enhance the data reuse of feature maps and weights. Additionally, weightloading unit and feature loading unit are designed to operate independently. Their state synchronization occurs only when a computation group’s workload is complete, reducing the synchronization frequency and minimizing accelerator stall. (3) The proposed accelerator is implemented in parameterized HLS code, allowing for quantitative performance hardware resource consumption modeling. A design space exploration scheme is developed to facilitate an automatic and fast search of the most appropriate parameter setting for any speciﬁc FPGA device.

The rest of the paper is organized as follows. Section 2 gives the background, discussing the structure of the YOLO series algorithms and the quantization method used in this paper. Section 3 presents the accelerator design, including data access unit design, computation unit design, and post-processing unit design. Section 4 details the modeling of the accelerator’s performance and resource consumption and provides the optimal design parameters based on these models. The experiment setup is described in Sect. 5, which also discusses the experiment results. Finally, Sect. 6 concludes the work. For ease of reading, the abbreviations and symbols used in this paper are summarized in Table 1.

## 2 Detection algorithm preparation

In this section, the structure of the YOLO series algorithms is brieﬂy introduced. Then, batch normalization (BN) fusion is applied. Finally, the activation and the weights are quantized to 8-bit.

### 2.1 Detection algorithm overview

As shown in Fig. 1, the YOLO series algorithms are composed of preprocessing, CNN computation, and postprocess procedures. In the preprocessing stage, the input is resized to a uniform size and then normalized. The CNN backbone neural network consists of the most computation workload in the inference procedure. Additionally, leaky ReLU and BN follow the convolution layers. The input of the CNN network is divided into D  D grids, and a total of

P vectors are generated by each grid. Each vector corresponds to a predicted bounding box, and it is composed of ð5 þ CÞ numbers where one number corresponds to the probability of containing an object, four numbers are responsible for the size and location of the bounding box, and the rest C numbers correspond to the category information. So, the output of size D  D  P  ð5 þ CÞ is generated after convolution operations.

In the post-processing procedure, coordinates and conﬁdence scores are calculated using the CNN outputs. Postprocessing consists of computation-intensive operations and control-intensive operations. Most of the computational resource is consumed by the sigmoid and exponential operations when decoding the coordinates of the bounding boxes. Then, NMS is carried out to ﬁfilter out the redundant predictions, which is a control-intensive operation. Finally, the predicted objects are shown to the users.

### 2.2 Network structure optimization

Batch normalization helps to accelerate the training and prevent overﬁfitting [12] when training the neural network. During the inference of the neural network, the BN operation is denoted as

^ ym ¼ cm  ym  lm ﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ r2

m þ  p þ bm

where ym and ^ ym denote the input and output of the BN operation, respectively, and the subscript m denotes channel index. The ﬁfixed estimation of mean and variance of the mini-batch is denoted as lm and r2

m, respectively, and the cm and bm are learnable parameters. Moreover, the , generally equally 1:0  105, is added to the denominator for numerical stability. Batch normalization helps to achieve a stable distribution of activation, but the multiplication and division consume a lot of hardware resource when the network is implemented on the FPGA. Batch normalization can be seen as a linear operation like ^ ym ¼ am  ym þ gm where

am ¼ cm ﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ r2

m þ  p ;

gm ¼ bm  lmcm ﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ r2

m þ  p

Taking BN and convolution calculation into account, the process can be denoted as

^ ym ¼ am  ðx  Wm þ BmÞ þ gm;

where x, Wm and Bm denote the input, weight and bias of the convolution computation. The linear operation in Eq. 4 can be further fused into the convolution calculation, i.e.,

**Table 1** Abbreviations

Symbol Description

B Word length of the ﬁfixed-point number

ﬂ Fractional length of the ﬁfixed-point number

Nr Number of CUs within one PE array

Np Number of PEs within one CU

Nn  2 Number of MACs performed by one PE in parallel

Nb Number of PE arrays

Nm Parallelism along the channel direction of the output 2NRAM Number of the line buffers within one feature buffer

Df The depth of the feature buffer

N Number of channels of the input feature map

R Number of rows of the input feature map

C Number of columns of the input feature map

M Number of channels of the output feature map

R0 Number of rows of the output feature map

C0 Number of columns of the output feature map

K Number of rows of the convolution kernel

K0 Number of columns of the convolution kernel

S Stride of the convolution

Ql Width of the computation group for the l-th layer Gr

Number of computation groups in the row direction

Gc

Number of computation groups in the column direction

Gm

Number of computation groups in the channel direction

Hwin Height of the pre-fetch window

Wwin Width of the pre-fetch window

Tl Theoretical inference latency of the l-th layer

C1 Number of DSPs consumed except PE arrays

C2 Factor measuring the BRAM used by weight buffer C3 Factor measuring the BRAM used by feature buffer

C4 Amount of BRAM consumed except the local buffer

C5 Factor measuring the LUT used by an adder tree

C6 Factor measuring the LUT used by an adder tree

C7 Amount of logic consumption of a 32-bit accumulator

C8 Amount of logic consumed except the PE arrays

**Fig. 1** Architecture of the YOLO network

^ ym ¼ x  ðam  WmÞ þ ðam  Bm þ gmÞ;

where am  Wm and am  Bm þ gm are the updated weight and bias.

Furthermore, in the original network, the location and conﬁdence are extracted by the neural network within one layer, for example, the 23rd ﬁfilter in the YOLOv2 algorithm. A total of 100 images are randomly selected as the input of the network, and their distribution of the location and category information is shown in Fig. 2. It can be seen that the location information is mainly distributed between 2 and 2, while the category information is mainly distributed between 15 and 10. The difference in the numerical distribution makes it difﬁcult to do the model quantization. Therefore, that convolutional layer is divided into two independent convolution layers, where one extracts the location information, and the other is responsible for the category information, and they are quantized separately.

### 2.3 Network quantization

Previous studies have shown that the parameters of neural networks can be represented by 8-bit dynamic ﬁfixed-point numbers without introducing obvious accuracy loss [13, 14]. Neural network quantization not only relieves the pressure on the memory system, but also improves the efﬁciency of the DSP. Speciﬁcally, compared to a full precision network, the storage and bandwidth requirement of the 8-bit quantized model decreases by four times [15]. In current Intel and Xilinx FPGA devices [4, 16], two 8  8 ﬁfixed-point multiplication can also be efﬁciently implemented by consuming only one DSP block. This reduces hardware consumption and enables more operations to be carried out concurrently. In this work, the model and the activation are represented using the 8-bit dynamic ﬁfixedpoint number [15]. The value x of a B-bit ﬁfixed-point

number xB1xB2. . .x0 with the fractional length ﬂis given by

x ¼ xB1  2B1 þ

X B2

i¼0

xi  2i !

 2fl:

The ﬂcorrelates with the step size or resolution, and the representation range of a dynamic ﬁfixed-point number. To cover the large dynamic range of the data in CNN inference, the input, output, weight, and bias of each layer are quantized, respectively [15]. However, the parameter ﬂis an integer, and it is challenging to be optimized using backpropagation. In this work, we calculate the ﬂparameter from continuous step size r using equation fl ¼ blogr

2c. The parameter r is calculated using the BRECQ quantization method [13].

In the BRECQ scheme, the quantization is performed on the weights, biases, and activations. For each layer in the CNN, the step size r for weights and biases is initialized by exhaustive search to minimize the quantization loss:

r

w ¼ arg min

rw

k ^winit  wk2

F;

where k  kF denotes the Frobenius norm, w denotes the weights or bias before the quantization, r

w denotes the initialized step size, and ^winit denotes the initial quantized weights or bias which equals to

^winit ¼ rw  clipðbw=rwc; 2B1; 2B1  1Þ:

To reduce the quantization loss, a learnable parameter v is added to the ^winit to calibrate the least signiﬁcant bits (LSBs) of the weights or bias. A sigmoid-like function rðÞ is then used to ensure that rðvÞ equals to 0 or 1. With this calibration, the ﬁfinal weight ^w is equal to

^w ¼ r

w  clipðbw=r

wc þ rðvÞ; 2B1; 2B1  1Þ:

In addition, a small number of randomly selected images

**Fig. 2** Distribution of the location and category data. a The distribution of the location data. b The distribution of the category data

are fed into the neural network as inputs. The difference between the convolution result of the quantized weight and the convolution result of the original weight is taken as the loss function. Afterward, back-propagation is used to optimize the learnable parameter v and the step size rw, i.e.,

v; rw ¼ arg min

v;rw

kx  w  x  ^wk2

F:

Similar to the weight quantization, the quantized activation

^x is equals to

^x ¼ rx  clipðbx=rxc; 2B1; 2B1  1Þ;

where the step size rx is also initialized and optimized using the similar method with the weight quantization.

## 3 Accelerator hardware design

The top-level architecture of the proposed accelerator is illustrated in Fig. 3. The proposed hardware accelerator is mainly composed of central processing element (PE) arrays, feature load unit, weight load unit, feature store unit, task scheduler unit, max-pooling unit and pre/postprocessing unit. A MicroBlaze processor is responsible for sending coarse-grained instruction to control the accelerator. The feature load unit and weight load unit are

responsible for loading the features and weights from the external double data rate (DDR) synchronous dynamic random-access memory (SDRAM) to the on-chip buffers, which are designed to cache the required data for convolution operations to improve the data reuse and external memory bandwidth efﬁciency. The PE array is designed to accelerate the neural network computation by utilizing as many on-chip DSP blocks as possible to perform parallel convolution operations. Batch processing is also introduced by instancing multiple PE arrays to further improve the throughput. The convolution results are then written back to the external memory through the feature store unit. Each function unit has its own loop counter, and synchronizations between the functional units are controlled by the Task Scheduler unit. Synchronizations are only performed when all the cached data have been consumed by the PE array. The low synchronization frequency reduces the risk of accelerator stall caused by the high-latency off-chip memory access. Moreover, the preprocessing and postprocessing algorithms are done by the dedicated hardware unit.

### 3.1 PE array design

As shown in Fig. 3, the PE array is organized as Nr compute units (CUs). Each CU, consisting of Np PEs, performs

**Fig. 3** Architecture of the accelerator

the multiply-accumulate operations (MAC) involved in the convolution neural network algorithm in parallel. The proposed multi-CU architecture is designed to relieve the stress in place and route caused by the high fan-out of the PE array and improve the scalability of the overall design. Those CUs are connected to the input connection and output connection interfaces. Three vector input ports (a~, b~, and d~) and one output port (p~) are designed for each PE, in which two inner product operations are conducted concurrently, i.e., b~ a~ and b~ d~. The two inner products share a common input vector b~, which can reduce the complexity of the on-chip data busses and improve the arithmetic intensity of the executed computation. Moreover, this operation pattern could also be utilized to improve the peak performance of the convolution computation by up to 2 with the same on-chip DSP cost by packing the two multiplication into one DSP block [4].

The detailed architecture of the PE is shown in Fig. 4a. Each PE contains Nn DSP48 blocks that perform 2  Nn 8bit integer multiplications in parallel. The products of these multiplications are summed and accumulated by an adder tree and a 32-bit accumulator, implementing the operations of PNn

i¼1 bi  ai and PNn

i¼1 bi  di in parallel. Since the two 8  8-bit integer multiplications of bi  ai and bi  di share the common multiplier, we can pack these 2  Nn multiplications into Nn DSP48E1 block. The procedure of the packed multiplication and the hardware structure of the packed multiplier are shown in Fig. 4b, c, respectively. Firstly, the 8-bit integer ai is shifted and added with the other 8-bit integer di by utilizing the pre-adder in the DSP block, and the 25-bit result is then multiplied with the common 8-bit multiplier bi using the 25  18-bit hard multiplier. Finally, a 17-bit calibration number is added to

the product by utilizing the 48-bit accumulator to eliminate the error caused by the sign extension operation when bi  di is negative [17]. Moreover, the 17-bit calibration number is calculated in advance by a simple logic circuit. In the approach of [18], up to eight products of the multiplications can be accumulated. However, it can only be applied to the DSP48E2 blocks due to the limitation on the width of the multiplier [19]. In contrast, our proposed scheme can be adopted for both DSP48E1 and DSP48E2 architectures. Compared to the approach of [4], our scheme consumes less logic resource since the operation of ai\\16 þ di is conducted by the pre-adder inside the DSP48E1 block and only a small amount of logic resource is consumed to generate the calibration number. Moreover, the PE array is instanced for Nb times to further improve the throughput by introducing batch processing. In total, the PE arrays consume Nr  Np  Nn  Nb DSP48E1 blocks to perform 2  Nr  Np  Nn  Nb 8-bit MAC operations in each clock cycle. The MAC results of size Nr  Nm  Nb are generated in parallel, where Nm is the number of MAC results generated by each CU, and it equals to 2  Np.

Due to the data broadcasting structure and shared controlling logic, implementing a large PE array on FPGA devices can lead to high fan-out problems, which may reduce the fmax of the ﬁfinal design [20]. To avoid this problem, an exclusive loop controller is designed for each CU to reduce the fan-out of the controlling logic, and the data broadcasting is only performed within each CU. This multiple CU architecture has a signiﬁcant advantage in scalability, which enables the proposed accelerator to be implemented on any type of FPGA device with near linear performance growth as the number of on-chip logic and DSP hardware resources increases.

**Fig. 4** DSP efﬁcient PE design. a The architecture of a PE. b The procedure of the packed multiplication. c Mapping the packed multiplication into a DSP48E1

### 3.2 On-chip memory system design

The memory system of the accelerator is mainly composed of a group of on-chip buffers and external memory access units (namely the feature load, feature store unit, and weight load units). The on-chip buffer caches the serial input read from the external memory, reorders, and sends the data to the Nr  Nb CUs for parallel computation. The local data buffers can signiﬁcantly reduce the data access latency of the PE array and improve the data reuse rate to relieve the pressure on external memory bandwidth. Moreover, a ping-pong buffer architecture is also proposed to overlap the data transfer with CU computation. The external memory access units are responsible for performing the high-throughput external memory access, where the burst memory access transfer is utilized.

As shown in Fig. 5, the feature buffer is constructed by 2NRAM line buffers with one shared input port and Nr parallel output ports. The depth and the width of each line buffer equal to Df and Nm  Nb bytes, respectively. The feature map data are fetched from external memory and stored in the line buffers in a zig-zag way, in which the address mapping sequence is controlled by the input multiplexer. One major beneﬁt of this data caching scheme is that burst memory transfer can be utilized to maximize the external memory bandwidth since the physical address of the input data is continuous within each line. A total number of 2NRAM buffer lines is designed to form a pingpong structure, which overlaps the data transferring procedure with the convolution computation to improve the efﬁciency of the accelerator. Detailed pipelining strategy is explained in Sect. 3.4.

A total number of Nr  Nm  Nb vector outputs are generated by the PE arrays in parallel in every LCU cycles, which correlates with the convolution calculation mapping that is introduced in Sect. 3.3. However, the result must be written back to the external DDR SDRAM in a serial way.

This imbalance raises two design challenges for the Feature Store unit, namely converting parallel data into serial data and maximizing external memory bandwidth utilization. A ping-pong buffer is designed to address the ﬁfirst issue. As shown in Fig. 6, once the parallel outputs are generated by the PE array, the ping-pong buffer starts to cache the result. In each cycle, Nm  Nb out of the Nr  Nm  Nb outputs results are selected and stored in one of the ping-pong buffer. While converting the parallel convolution results of the current iteration, the converted serial results of previous iteration stored in another ping-pong buffer are being written to the external memory concurrently. Secondly, burst memory transfer is also utilized in the data store procedure to maximize the external memory bandwidth and minimize the latency. A total of Nr cycles are needed to store the parallel outputs which is generated every LCU cycles. Therefore, to avoid any stall operations in the Feature Store unit or the PE array, the following condition must be satisﬁed: LCU [ Nr. In deep convolution neural network algorithms, the convolution operations are generally performed on vector data with large sizes, which can normally meet this requirement.

### 3.3 Convolution task mapping

Convolution calculation occupies the major workload in CNN inference computation [21]. As illustrated in Algorithm 1, it performs the inner product of the neural network weight W and the input feature map FI. The input, output feature maps and weights are of the size N  R  C, M  R0  C0 and M  N  K  K0 , respectively, and S denotes the stride of the convolution. Both parallelism mapping and data caching should be taken into concern together when mapping the convolution calculation on the proposed accelerator. The former optimization ﬁfinds the best way that maps the convolution algorithm on the PE array that can maximize acceleration convolution

**Fig. 5** Feature buffer design. The line buffers cache the serial data from the external memory, and output parallel data streams to the CUs

computation by executing as many as parallel operations in each cycle. The latter optimization targets utilizing on-chip buffers to enhance on-chip data reuse rate to improve external memory efﬁciency.

Parallelism mapping From Algorithm 1, it can be observed that there is no computation dependency among each output channel dimension mm and each output row dimension rr, so the calculation for multiple output

channels and output rows can be conducted in parallel. As shown in Fig. 7, three degrees of parallelism are exploited in the proposed accelerator, i.e., Nm and Nr convolution kernels are executed in parallel along the output channel

**Fig. 6** Output buffer design. Every LCU clocks, a total of Nr  Nm  Nb outputs are generated. The output buffer caches them and writes them back to the external memory sequentially

**Fig. 7** Mapping the convolution computation into one PE array

and the input row dimensions, respectively, while Nn MAC operations are conducted concurrently within each convolution kernel to further accelerate the computation. For a convolution kernel of size K  K0  N, the MAC results of size Nr  Nm are generated every LCU ¼ K  K0  dN=Nne cycles. The workload of Nm convolution kernels along the output channel direction is carried by one CU, where every two convolution kernels are mapped to a PE since they share the same input feature map, which matches the multiplication packing scheme proposed in Sect. 3.1. During the convolution, as shown in Fig. 3, each CU gets its own input feature map data from the feature buffer, and those data are shared by the PEs within a CU. At the same time, weights are loaded and shared among the Nr CUs, and each PE gets 2  Nn pixels of weights correlating with two convolution kernels. Therefore, a total of Nr  Nm  Nn MAC operations are conducted concurrently by one PE array. Moreover, the calculation of Nb different inputs are also conducted concurrently to further improve the parallelism and the weights reuse.

Data caching To produce one output feature pixel, the accelerator needs to hold the amount of K  K0  N pixels of feature map and weight data for parallel computation, respectively. As the convolution kernel slides over the whole input feature map, more feature data have to be fetched repeatedly from external memory [16], while the weight data can be reused. To ﬁt the depth of the on-chip feature buffer, we propose to divide and execute each convolution layer as multiple computation groups, and each group consists of Nr  Ql  Nm times of convolution computation deﬁned in Algorithm 1. As shown in Fig. 7, the depth and the height of each computation group (i.e., Nm and Nr) ﬁt the size of the PE array, while the width Ql is determined by the depth of the feature buffer. Consequently, the number of computation groups along the row, column, and channel dimensions can be calculated by

Gr

l ¼ dR0

l=Nre;

Gc

l ¼ dC0

l=Qle;

Gm

l ¼ dMl=Nme:

The whole range of the input feature data that corresponds to one computation group is deﬁned as a pre-fetch window. As shown in Fig. 7, the height and width of the pre-fetch window can be calculated by

Hwin ¼ ðNr  1Þ  S þ K;

Wwin ¼ ðQl  1Þ  S þ K0:

Consequently, the whole input feature map is divided into Gr

l  Gc

pre-fetch windows during execution on the accelerator, and the data within a pre-fetch window are

shared by Gm

l convolution groups along the output channel dimension. For instance, computation group 1 and group 2 share the pre-fetch Window A.

Since there is a ﬁfixed interval of S lines between the feature maps required by the adjacent convolution tasks, each line buffer in the feature buffer is designed to store at most S lines of feature maps to avoid possible data access collision. So, a total number of NRAM ¼ dHwin=Se line buffers are conﬁgured in the feature buffer. Given the depth of the line buffer as Df , the width of the pre-fetch window equals to

Wwin ¼ Df =ðN  SÞ:

Considering the correlation between the Ql and Wwin which is shown in Eq. (13), the width of the computation group is restricted by

Ql ¼ bðWwin  KlÞ=Slc þ 1:

For instance, in Fig. 5, assuming that the size of the convolution kernel is of the size 3  3  1 and S ¼ 2, Nr ¼ 4, then height perfetch window equals Hwin ¼ ðNr  1Þ  S þ K ¼ ð4  1Þ  2 þ 3 ¼ 9, and the number of line buffers is CeilðHwin=SÞ ¼ Ceilð9=2Þ ¼ 5.

The execution order of the computation groups has a signiﬁcant impact on the on-chip data reuse rate and external memory bandwidth utilization. Two scheduling schemes are considered in this work. As shown in Fig. 7, the ﬁfirst task scheduling scheme (Scheme-A) launches the computation groups in the order of Group 1, 2,..., 24, which can maximize the reuse rate of cached feature map data since adjacent groups along output dimension M (e.g., Group 1 and 2) share the same pre-fetched window. The second strategy (Scheme-B) is to execute the computation groups in the order of Group 1, 3, 5,..., 24, which can improve the weight data reuse rate, since these groups share the same weights. The efﬁciency of these two schemes are determined by multiple factors, such as the size of each group, the neural network structure, and the external memory bandwidth limitation. Therefore, experiments have to be conducted on the target FPGA platform to measure the execution time and bandwidth utilization before making the ﬁfinal decision. In Sect. 4.4, we will provide detailed experiment results and compare the pros and cons of these two scheduling schemes based on the Rooﬂine model. Algorithm 2 summarizes the optimized convolution dataﬂow. In this dataﬂow, each group of computation tasks is performed sequentially, and its corresponding data are also cached sequentially. Moreover, a total number of Gm

l groups share the same input feature map. As shown in the Line 11 and Line 17 of Algorithm 2, a total of Nm  Nr  Nn MAC operations are conducted concurrently.

### 3.4 Task scheduler design

Task scheduler is designed to synchronize the state of each function unit and dynamically schedule the convolutional computation, which reduces the control workload of the processor. As illustrated in Fig. 7, the convolution operation is divided into multiple computation groups, and the execution of each group is dynamically scheduled by the task scheduler unit. Besides managing the execution order of the computation groups, the task scheduler unit also

synchronizes the state of each function unit. As shown in Fig. 8, at the beginning of each layer, the feature and weight data are ﬁfirst loaded from the external memory and cached in the on-chip buffers. When ﬁnishing loading the required data by the ﬁfirst computation group, (i.e., Time 1), the task scheduler unit sends signals to start the PE array. While the PE array conducting the convolution, the Feature Load unit and Weight Load unit continue loading feature map and weight data for the subsequent groups, i.e., from time 1 to 2. Since the convolution group 2 and group 1 share the same input feature map, computation group 2 can be started upon ﬁnishing group 1 and loading the required

Window A

Group 1

Feature Load unit

Weight Load unit

Window B

Group 2 Group 3

Group 1

Group 6

Feature Store unit

PE array

Group 1 Group 2 Group 23 Group 24 Group 4

Group 4 Group 5

Group 3

Window C

Group 2 Group 3 Group 4 Group 23 Group 24

c n y S c n y S Sync Sync Sync Sync Finish Start

Time

**Fig. 8** Task-level pipeline strategy

weights data, i.e., the time 2. Additional attention should be paid that, at this time point, the loading of pre-fetch window B does not need to be ﬁfinished, since window A is still in use.

In the proposed architecture, synchronization is only performed when new input feature map or weight data were required, and each functional unit runs independently for the rest of the time, which reduces the risk of accelerator stall caused by high-latency off-chip memory access. In addition, a larger feature map pre-fetch window will reduce the frequency of synchronization, which helps to improve the efﬁciency of the accelerator, but will consume more on-chip memory resources. Therefore, the size of the perfetch window has to be selected carefully to balance the performance and hardware cost, and it will be introduced in the design exploration Sect. 4.3.

### 3.5 Post-processing

The detailed processing procedures of the post-processing algorithms in YOLO detector is illustrated in Fig. 9. The YOLO algorithms predict the coordinates of bounding boxes relative to the location of the grid cells, where a sigmoid function constrains the center coordinates of the bounding box to fall in the grid cell [12]. The exponent function extracts the height and width of the bounding box, which ensures the width and height are greater than 0. The conﬁdence scores are extracted from the network’s prediction by multiplying the outputs of the softmax function and the probability of containing an object. Then, the conﬁdence scores under the threshold are ﬁfiltered to reduce the amount of candidate boxes. Once ﬁfinished the coordinates and conﬁdence scores extraction, the NMS is carried out to further ﬁfilter the redundant predictions. In the NMS stage, the conﬁdence scores are sorted ﬁfirstly, and the box corresponding to the largest score is selected as one candidate box for this class. Then the IOU values between this

box and all other boxes are calculated and those boxes whose IOU values are above the predeﬁned threshold are discarded. This procedure continues until all boxes are either selected or discarded [10].

The coordinates and conﬁdence scores extraction are computational-intensive tasks consisting of a large amount of sigmoid, exponent and softmax functions. These nonlinear functions require complicated ﬂfloating point operations. In contrast, the NMS algorithm is generally controlintensive since it contains many indexing, sorting and grouping operations. In most accelerator designs [4–6, 9], those functions are implemented on general-purpose processors, such as the ARM or x86 CPUs, as software programs. Since these CPUs are mainly hard-core processors with high computing performance, the implemented programs can be executed with very low latency delivering real-time detection results. However on FPGA fabric-only devices, only softcore CPU processors, such as the MicroBlaze [22] and NIOS [23] processors, are available with very limited computational capability. Therefore, the above algorithms in the post-processing stage of YOLO detectors have to be implemented in dedicated hardware circuits to achieve real-time processing speed.

Coordinates calculation The location of a prediction box is represented by the coordinates of two diagonal points, i.e., ðx1; y1Þ and ðx2; y2Þ. According to the YOLO algorithm [12], the normalized location x1 can be calculated by

x1 ¼ ½ðrðtxÞ þ cxÞ  ð0:5  pw  etwÞ  scale;

where r denotes the sigmoid function, and tx and tw are coordinates information extracted from the CNN outputs, and cx is the offset from the top left corner of the image, and pw represents the width of the bounding box prior. The architecture of the proposed hardware location decoding unit is shown in Fig. 10. Since tx, tw, cx and pw are all quantized in 8-bit ﬁfixed-point format, the sigmoid and exponential functions can be implemented by look-up table with low hardware costs. In the location decoding unit, two look-up tables with 256 entries are utilized to

**Fig. 9** Work ﬂow of the post-processing Fig. 10 Location decoding unit

generate the outputs of the sigmoid and exponential functions. Moreover, the intermediate data and subsequent operations are quantized to further reduce the hardware resource consumption and calculation latency. The output coordinates are quantized to four 16-bit ﬁfixed-point numbers, since the resolution of the input picture equals to 416  416, and the accuracy of the 16-bit numbers is enough. The whole procedure of the coordinate calculation is fully pipelined and controlled by the ﬁfinite-state machine (FSM) to improve the hardware efﬁciency.

Conﬁdence scores calculation The conﬁdence scores equal to the product of the softmax function and the probability of containing an object. Its architecture is shown in Fig. 11, which can be divided into three stages. In the ﬁfirst stage, the maximum value is extracted from the serial inputs. In the second stage, the subtraction is conducted between the inputs and the maximum value, and their exponentiation and summation operations are calculated. In the last stage, the ﬂfloating point multiplication and division are carried out. It should be taken into account that during the conﬁdence score calculation, only the multiplication and division in the third stage are carried out using the ﬂfloat data.

Si ¼ eðxiXmaxÞ PN

j¼1 eðxjXmaxÞ ;

NMS unit After the coordinates and conﬁdence scores were calculated, a large number of redundant candidate boxes for the same target are generated, and these candidate boxes may overlap with the neighboring boxes. In order to

solve this problem, the NMS is carried out to ﬁnd the best target bounding box and eliminate the redundant boundary boxes. A hardware-friendly NMS algorithm was proposed by [10], where the sorting of conﬁdence scores was omitted. The design achieved a very low latency at the cost of using 430 on-chip DSP blocks. This hinders the implementation of the hardware NMS on some resource-constrained devices. Inspired by that work, a resource-efﬁcient NMS algorithm is proposed in this work, which is shown in Algorithm 3. For each input bounding box, its IOU between each selected box is calculated. The selected box will be replaced when the IOU is beyond the threshold, and the conﬁdence score is less than that of the input box. The input box is inserted to the selected boxes when the IOU between the input box and each of the selected boxes is less than threshold. The hardware architecture of the NMS unit and the overall post-processing unit is shown in Fig. 12. The proposed NMS hardware unit is mainly composed by a selected box buffer and an IOU calculation unit. The NMS unit connects with the coordinate and score calculation units using two channels, which forms a deep pipeline structure to reduce the off-chip data access. A threshold unit is designed to ﬁfilter out the boxes with low conﬁdence score, which relieves the workload of the NMS unit.

## 4 Performance modeling and design space exploration

Design space exploration plays an important role in FPGAbased accelerator design, which enables the system to achieve a balance between performance and resource consumption. In this section, the performance and resource consumption models are ﬁfirst built, and comprehensive design space exploration is then carried out to ﬁnd the optimal parameters for the PE array and the on-chip memory system. Moreover, the performance of the two task scheduling schemes discussed in Sect. 3.3 is also measured and compared by using the Rooﬂine model.

### 4.1 Accelerator performance

According to the Rooﬂine model [24, 25], the throughput is constrained by either the bandwidth roof (Rbw) or computational roof (Rcp). The computational roof measures the peak throughput provided by the computation resource in the system. The bandwidth roof measures the throughput that the memory system can support [25]. The overall throughput equals to minðRbw; RcpÞ. The proposed design has a total of Nr  Nb CUs. Each CU performs Nm  Nn MAC operations concurrently. Considering a MAC operation as two operations, i.e., addition and multiplication, the computational roof equals to

Rcp ¼ 2  Nn  Nr  Nm  Nb  Freq:

Once ﬁnishing loading a feature pre-fetch window, the feature will be used by Gm

l computation groups along the output channel dimension. Therefore, the total pixels of feature map data loaded from and written to the external memory for the l-th layer of convolution computation is

Hf

l ¼ ðGc

l  Gr

l  Wwin  Hwin  N þ C0  R0  MÞ  Nb:

For each computation group, an amount of K  K0  N  Nm weights is required, so the total amount of weights that needs to be loaded from external memory during one layer of calculation equals to

Hw

l ¼ Gc

l  Gr

l  K  K0  N  M:

The arithmetic intensity, which is calculated as the ratio of the amount of calculation to the amount of external memory access, is denoted as

I ¼ #OPl Hf

l þ Hw

where the #OPl denotes the number of operations performed in the l-th convolution/FC layer, and it equals

#OPl ¼ 2  K  K0  N  C0  R0  M  Nb:

Further, the peak throughput supported by the memory system equals to the product of the arithmetic intensity and external memory bandwidth, i.e.,

Rbw ¼ I  BWDDR;

where BWDDR denotes the bandwidth of the external memory. The theoretical execution latency for the l-th convolution/FC layer equals to the quotient of the number of MAC operations and the throughput, i.e.,

Tl ¼ #OPl  dR0=Nre  Nr=R0

minðRcp; RbwÞ

Equation (25) measures the latency of performing the deep CNN algorithm, which equals to the sum of latency of all the layers, while the overall throughput equals to the quotient of the total amount of calculation and the Tsum.

Tsum ¼

X

l¼0

Tl

### 4.2 Hardware resource consumption

The proposed accelerator can be conﬁgured by a group of hardware parameters, including the Nn, Nr, Nm, and Nb related to the parallelism and the Df related to the depth of

**Fig. 11** Softmax unit

**Fig. 12** Hardware architecture of the post-process unit

the feature buffer. Hardware resource consumption is positively correlated with these parameters. In order to quantitatively guide the accelerator design, the logic, memory, and DSP consumption models correlated with these parameters are deﬁned. The PE array accounts for the most of DSP consumption which performs Nn  Nr  Nm  Nb multiplications in every clock cycle concurrently.

Two 8-bit multiplications are done by one DSP block, so the DSP consumption is modeled by

Cdsp ¼ 1

2  Nn  Nr  Nm  Nb þ C1;

where C1 denotes the DSP resource consumed by the rest of parts of the accelerator, such as the address generator.

**Fig. 13** Selection of Df and Nr. a The correlation between external memory access and Df . b The external memory access and speed gain for different Nr

**Fig. 14** Resource consumption estimation. The target device is Xilinx V7-690T and the other parameters are Nr ¼ 13 Df ¼ 8192. a Logic resource. b Block RAMs. c DSP blocks. d Inference latency

The feature buffer and weight buffer consume the most of on-chip RAM resources. The feature buffer is composed by Nr þ dðK=SÞe  1 dual-ports RAMs with the depth of Df  S  N. When modeling the consumption of on-chip RAMs, not only the size of the buffer needs to be considered, but also the width of the port. A few more RAM blocks are needed to achieve a large port width, for the onchip memory block has its limitation of maximum port width. In this work, the width of the feature buffer equals to 8  Nm  Nb bit, and the width of the weight buffer equals to 8  Nn  Nm bit. The total on-chip memory consumption is estimated by (27)

Cmem ¼ C2  Nn  Nm þ C3  Nr  Nm  Df  Nb þ C4;

where C2, C3, C4 denotes the factor the parameters that measure the number of BRAM consumed by the weight buffer, feature buffer, and the rest of the modules.

The PE array takes up most of the logic consumption to generate the adder tree and the accumulator. The logic consumption for each adder tree correlates with the number of additional operations, i.e., Nn, and the logic consumption for a 32-bit accumulator can be seen as a constant. Moreover, there are a total of Nr  Nm  Nb adder trees and accumulators in the PE array. So, the logic consumption is estimated by

Clogic ¼ ðC5  Nn þ C6 þ C7Þ  Nr  Nm  Nb þ C8;

where C5  Nn þ C6 and C7 measure the logic consumed by an adder tree and a 32-bit accumulator, respectively, and C8 denotes the logic consumed by other functional units.

### 4.3 Design space exploration

The ﬁfinal goal of the design space exploration is to ﬁnd the highest throughput while keeping the three types of hardware resource consumption within the device limitation. In the design space exploration, the hardware resource consumption is constrained under 70% to prevent timing issues, i.e.,

maxðThroughputÞ

s:t: : Cdsp  0:7  DSPlim

Cmem  0:7  MEMlim

Clogic  0:7  LOGIClim;

where DSPlim, MEMlim and LOGIClim denotes the available DSP, on-chip memory and logic resource, respectively. According (24), both computation roof

**Fig. 15** Rooﬂine models for the two schemes, where the estimated throughput correlates with the batch size from 1 to 8 is shown. a Scheme-A. b Scheme-B

**Fig. 16** Compilation time for different hardware parameter setting (Nr ¼ 13; Nb ¼ 1)

bandwidth roof should be considered during the exploration of the peak performance. Moreover, the power consumption of the system and the frequency of external memory access are usually positively correlated with each other. Therefore, the external memory access needs to be limited to a relatively low level to reduce the system power consumption and the external memory bandwidth pressure. According to (19) and (20), the feature and weight access are correlated with the number and size of the convolution group which depend on Nr and Df . As shown in Fig. 13a, the external memory access drop sharply with the increase in Df , when Df is less than 8192. However, the decline of external memory access tends to slow down when Df is greater than 8192, and the on-chip memory consumption correlates with Df . Taking the on-chip memory consumption and the external memory access into consideration, the Df is set to 8192. Similarly, as shown in Fig. 13b, the decline of external memory access slows down when Nr is greater than 13. Moreover, the speed-up gain reaches a saturation value when Nr [ 13, which is caused by the low PE array utilization when conducting the last few layers of convolution, where the size of the feature map in dimension R0 is relatively small. According to the external memory access and the speed-up gain, Nr is set to 13 to achieve the most efﬁcient speed-up gain and low external memory access.

Subsequently, a few rounds of compilation are conducted to gather the resource consumption information correlated with different settings of parameters Nn, Nm and Nb, including the logic, on-chip memory, and DSP consumption. The inference latency and the resource consumption are shown in Fig. 14, and the parameters that achieve minimum latency under the device resource limitation are expected. Furthermore, routing or timing failures may be caused by high resource occupancy, so in this

design, we constrain the consumption under 70% of the total hardware resource. In the ﬁfinal implementation, Nn ¼ 8, Nm ¼ 16, Nr ¼ 13 and Nb ¼ 2 are selected, and the achieved highest frequency is 160 MHz.

### 4.4 Comparison of task scheduling methods

As discussed in Sect. 3.4, the scheduling Scheme-A maximizes the reuse of feature map, while the Scheme-B maximizes the reuse of weights. In this section, these two schemes are evaluated by using the Rooﬂine model. The performance of Scheme-A has already been modeled in Sect. 4.1, so this section only focuses on modeling the performance of Scheme-B. In Scheme-B, the input feature map data are not shared among different groups, and a total number of Hwin  Wwin  N input pixels are needed to be loaded from external memory before conducting one group of the convolutional task. Therefore, for the l-th convolution layer, the total amount of feature map data loaded from and written to the external memory in Scheme-B equals to

hf

l ¼ ðGc

l  Gr

l  Gm

l  Wwin  Hwin  N þ C0  R0  MÞ  Nb:

For the weights, every Gc

l  Gr

l groups share the same data, so the amount of weights to be loaded for the l-th layer is

hw

l ¼ K  K0  N  M:

Then, theoretical throughput can be calculated by using Eqs. (30), (31) and the performance models deﬁned in Sect. 4.1. The ﬁfinal obtained Rooﬂine models for both Scheme-A and Scheme-B are shown in Fig. 15, where the overall throughput when implementing YOLOv2 algorithm with different batch sizes are proposed. Special attention should be paid to when modeling the computational roof, and a total of 30% hardware resource is reserved. As shown in Fig. 15a, the arithmetic intensity increases linearly with the increase in batch size from 1 to 4, which is caused by the increase in off-chip bandwidth utilization. The increase in the arithmetic intensity slows down when the batch size is greater than 4, for the full utilization of off-chip bandwidth. As shown in Fig. 15b, the throughput is bandwidthbounded. From the above comparison, it is clear that Scheme-A is superior to Scheme-B, and is thus adopted in the ﬁfinal implementation.

**Fig. 17** Work ﬂow of the accelerator design

## 5 System implementation and performance evaluation

### 5.1 Experimental setup

To evaluate the proposed accelerator, we utilized the KC705 and VC709 development boards, covering FPGAs with varying capacities. The KC705 board contains a lowend Xilinx XC7K325T FPGA with 203k LUTs, 840 DSPs,

and 16Mbit BRAM. One DDR3 memory with a capacity of 1GB is connected to the FPGA device on the board with a transfer bandwidth of 64@1600MTs. The VC709 development board contains a Xilinx XC7VX690T FPGA with 433k LUTs, 3600 DSPs, and 52.9Mbit BRAM. Two DDR3 memories, each with a capacity of 4GB and a transfer bandwidth of 64@1600MTs, are connected to the FPGA device on the board. To compile the HLS and generate RTL, we utilized Vitis HLS 2021.2, and the bitstream was

**Fig. 18** Theoretical and actual execution time of each layer of the YOLOv2 algorithm on the VOC data set (Nn ¼ 8; Nm ¼ 16; Nr ¼ 13; Nb ¼ 1, Frequency = 180 MHz)

**Fig. 19** Theoretical and actual execution time of each layer of the YOLOv3 algorithm on the VOC data set (Nn ¼ 8; Nm ¼ 16; Nr ¼ 13)

generated using Vivado 2021.2. The program for the host processor was compiled using Vitis 2021.2. The neural networks were trained using the MMDetection 2.14 framework [26] on the PASCAL VOC 2007 and VOC 2012 datasets [27]. We quantized the neural network using the scheme of BRECQ [13], optimizing the bit width of activations and network parameters to 8-bit. The platform used for the model quantization was composed of an Intel i7-6700k CPU, four 2080Ti GPUs, and 64 GB RAM. Approximately, 2.5 and 4 h were consumed in quantizing YOLOv2 and YOLOv3, respectively. The HLS compiling

**Fig. 20** Breakdown hardware resource of the accelerator with Nn ¼ 8, Nm ¼ 8, Nr ¼ 13, and Nb ¼ 1. a LUT consumption, b BRAM consumption, c DSP consumption

**Table 2** Performance and resource consumption of the post-processing unit

LUTs DSP BRAM (18k)

Latency (845 boxes)

Coordinates decode

Score calculation

NMS unit

Misc unit

Total 0.38 ms

**Table 3** Comparison with state-of-the-art YOLOv2 and YOLOv2-Tiny implementations on FPGA

ISCAS2021 [4] NCAA2022 [9]

Benchmark model YOLOv2 YOLOv2 YOLOv2 YOLOv2

Dataset KITTI VOC VOC VOC VOC VOC VOC

MAP Quantization (bits)

FPGA device XC7Z045 ZU7EV XC7K325T XC7K325T XC7VX690T XC7VX690T XC7VX690T

LUTs (K) 84/218 91.17/230 134.9/203 134.9/203 153.4/433 153.4/433 212.4/433

DSP Blocks 610/900 387/1728 687/840 687/840 897/3600 897/3600 1737/3600

Block RAM 18K 512/1090 461/624 551/890 551/890 627/2940 627/2940 799/2940

Frequency (MHz)

Batch size

On-chip power (W)

Total power (W)

Efﬁciency (GOPs/W) –/45.5 20.9/–

and hardware generating platform comprised an AMD R9- 5950x CPU and 64 GB RAM. The time consumption for generating hardware varies with hardware parameters is shown in Fig. 16, where the compilation time increases with the increase in hardware parameters Nn and Nm. The compilation time also reﬂects the difﬁculty of hardware generation, which is often related to the factors such as parallelism and fan-out.

ensure fair comparison with previous works [6, 7, 9], the LUT, BRAM, and DSP utilization information reported by Vivado is utilized to evaluate the resource consumption of the accelerator. Both FPGA’s power consumption and the power of the development board were measured. The FPGA’s power consumption was reported by the power analyzer of Vivado, as in previous work [9]. The power consumption of the entire board was measured using the power meter plugged into the development platform, as in previous work [7]. The actual execution time of each layer was measured by using a software timer provided by the MicroBlaze MCU.

The design parameters for the two FPGA devices change accordingly based on their capacities. As per the model described in Sect. 4, the 325T FPGA device was evaluated using selected parameters, namely Nn ¼ 8, Nm ¼ 12, Nr ¼ 13, and Nb ¼ 1, which quantiﬁes the accelerators’ performance on resource-constrained devices. To assess the accelerator’s performance on a device with larger capacity, performance tests were conducted using Nn ¼ 8, Nm ¼ 16, Nr ¼ 13, Nb ¼ 1, and Nn ¼ 8, Nm ¼ 16, Nr ¼ 13, and Nb ¼ 2.

Overall, the workﬂow of the accelerator design is shown in Fig. 17, which is mainly composed of the model preparation and hardware preparation. Once ﬁnishing training the CNN model, the parameters of BN are merged into the weights and bias, then quantization is conducted using the BRECQ method. For the hardware preparation, the optimal hardware parameters for the target FPGA device are generated using the performance and resource model. Then, the HLS compilation is conducted using the aforementioned hardware parameters. Finally, the IP cores are connected, and the hardware is generated using Vivado.

### 5.2 Performance evaluation of the hardware accelerator

The baseline YOLOv2 and YOLOv3 algorithms have been implemented on our proposed hardware accelerator. The theoretical execution time of each layer was used to measure the efﬁciency of the accelerator, and it is calculated by

t0

l ¼ #OPl 2  Nn  Nm  Nr  Nb  Freq ;

where the denominator represents the maximum throughput that the PE array can provide. The execution efﬁciency of the accelerator was calculated by El ¼ t0

l=tl, where tl denotes the measured execution time of the l-th layer. For the YOLOv2 network, the theoretical execution time and actual execution time were also compared in Fig. 18. It can be observed that the actual execution time for most of the layers was close to the theoretical time except for six layers, i.e., the 1st, 4th, 7th, 21st, 23rd, and 24th layer. Two

**Table 4** Comparison with state-of-the-art YOLOv3-related implementations on FPGA

VLSI2022 [28] ISCAS2020 [6]

Benchmark model YOLOv3 YOLOv3 YOLOv3

Dataset ILSVRC2015 VOC VOC VOC VOC VOC

MAP

Quantization (bits)

FPGA device XCZU7EV XC7VX485T XC7K325T XC7K325T XC7VX690T XC7VX690T XC7VX690T

LUTs (K) 123/230 48.5/303 136.5/203 136.5/203 154.6/433 154.6/433 213.2/433

DSP blocks 146/1728 2304/2800 687/840 687/840 897/3600 897/3600 1737/3600

Block RAM 18K 326/624 141/2060 553/890 553/890 631/2940 631/2940 801/2940

Frequency (MHz)

Batch size

On-chip power(W)

Total power (W)

Efﬁciency (GOPs/W) 105.4/– 95.6/–

problems led to the low efﬁciency of the ﬁfirst layer. Firstly, the ﬁfirst layer only has three input channels, resulting in inadequate utilization of the parallelism in the Nn direction. Secondly, according to the performance model, the calculation latency equals to LCU ¼ K  K0  dN=Nne ¼ 3  3  d3=8e ¼ 9; which is smaller than Nr. Consequently, Nr vectors each with a size of 1  1  Nm are produced every LCU clocks. However, it takes Nr clocks to write these vectors back to the DDR memory. Moreover, in contrast to convolutions with large ﬁfilter sizes, 1  1 convolutions have relatively low reuse of the input feature, resulting in a low arithmetic intensity. According to the Rooﬂine model, their performances are restricted by the memory bandwidth limitations. However, the execution time of these layers was very short, so the negative impact on the overall performance was negligible. The actual throughput of the proposed detection system equals to the ratio of the operation amount to the total measured time consumption, i.e.,

TPS ¼

PL

l¼1 #OPl PL

l¼1 tl

In this work, the achieved highest throughput of the accelerator was 914 GOP/s, which is achieved on the XC690T with the Nn ¼ 8, Nm ¼ 16, Nr ¼ 13, and Nb ¼ 2 and the frequency equals to 160 MHz. The power consumption of the FPGA device was 12.5 W, which was estimated using the Vivado development tool, and the power consumption of the whole board was 24.1 W. The performance of implementing YOLOv3 on the accelerator is shown in Fig. 19. The computation efﬁciency of ten layers are lower than 60%, and the reason for the low efﬁciency is the same as that of YOLOv2. Moreover, the execution time of these layers was also short, so the overall efﬁciency is relative high.

The resource consumption of each part of the accelerator is depicted in Fig. 20. Figure 20a indicates that the memory controller and AXI interconnect consume roughly 25% of the LUT resources, which poses challenges for FPGA’s routing and timing optimization. Nevertheless, the model presented in Sect. 4.2 can still accurately predict LUT consumption because we have observed that the resource consumption of memory controller remains constant. Additionally, over 60% of the BRAM consumption in the accelerator is attributed to LocalBuffer. As shown in Fig. 20c, more than 90% of the DSP resources are utilized to implement the PE array. The resource consumption of the LUTs, BRAM, and DSPs are presented by small dots in Fig. 14, and it is apparent that they conform to the model presented in Sect. 4.2.

When implementing YOLOv2 algorithm, a total of 13  13  5 ¼ 845 candidate boxes were processed sequentially by the post-processing unit. As shown in Fig. 18, its time consumption equals to 0.38 ms, which is relatively low compared to the CNN computation. Moreover, the latency is proportional to the number of candidate boxes. The breakdown hardware consumption of the post-processing unit is shown in Table 2, which is composed by the three aforementioned units and one misc unit. The misc unit is mainly composed by channels and global memory ports. Compared to the approach of [10], the hardware resource consumption of our design is relatively low, which enables implementing the accelerator in some resource-constrained devices.

### 5.3 Comparison with state-of-the-art

The performance of several state-of-the-art hardware accelerators based on FPGA for object detection tasks is

**Table 5** Performance evaluation between alternatives

Work ACCESS 2021 [33] ACCESS 2021 [33] DSD2022 [31] TCAD2020 [7]

Device Intel NCS Jetson nano Intel GX1150 ZC706 Xilinx 325T

Architecture ASIC ARM?GPU FPGA ARM?FPGA FPGA

Network YOLO-Tiny

Resolution

Workload (GOP)

Precision FP16 FP32 FP32 INT16 INT8

Frequency

Power

Latency (ms)

Efﬁciency (GOP/W) –/183.6 –/25.25 –/–

compared in Tables 3 and 4 depending on the networks used. To ensure fairness in the comparison, the performance results are measured and reported using a batch size of 1.

**Table 3** presents a comparison between two reference accelerators that implement YOLOv2-related models and our proposed design. The design presented in [4] deployed the entire YOLOv2-Tiny neural network onto a single FPGA device, minimizing the need for external memory access. Furthermore, the computation of all convolution layers was organized as a deep pipeline and workload balance was employed to achieve a low inference latency of 27.78 ms with the input size of 1280  384. However, a limitation of this design is that the accelerator architecture is ﬁfixed and cannot be reprogrammed by software to implement larger detection models, such as standard YOLOv2 or YOLOv3. In contrast, the architecture proposed in this work is highly ﬂflexible and capable of executing convolution computations with arbitrary input and ﬁfilter sizes. For instance, our design can implement the standard YOLOv2 model on the XC7325T device, which has even fewer logic and DSP resources than the device used in [4]. For the detection latency, our YOLOv2-Tiny implemented on XC325T achieved an end-to-end latency of 14.49ms with the input size of 416  416. In [9], a cross-layer dataﬂow strategy was introduced to optimize the frequency of external memory data access. However, this design implemented separated hardware units for the 1  1 and 3  3 convolution layers, leading to signiﬁcant imbalance in hardware resource utilization. Consequently, the highest throughput achievable by the accelerator when executing the YOLOv2 model was limited to only 100.3 GOP/s. In contrast, the programmable convolution unit in our design can fully utilize as many as possible on-chip hardware resources to accelerate all the convolution layers in the neural network model, resulting a 5 throughput at the cost of 2:2 of on-chip DSP resources consumption.

In Table 4, our results are compared with those of two other FPGA accelerators that implement YOLOv3-related models. The design in [28] utilized the similarities between continuous inputs in video, and skipped the convolution operation of similar data between continuous inputs. Winograd algorithm was also used to optimize the 3  3 convolution in the YOLOv3-Tiny to further improve the throughput. Experimental results show that their accelerator achieved a throughput of 348 GOP/s on ZCU104 evaluation board. This work brings new highlights to the processing of continuous video input. However, a relative large batch size is required by that work to utilize the similarity between the input, which results in a large inference latency of 107.81 ms, and this is not suitable for implementing this accelerator on low latency scene. Compared with that work, our accelerator achieved an end-

to-end latency of 15.2 ms on XC325T FPGA, which reduces 7 of latency. The design in [6] consumed 2304 DSPs of the XC7VX485T FPGA device and achieved a performance of 460.8 GOP/s. However, preprocessing, activation functions, pooling, and other miscellaneous operations were conducted by a low-performance Micro- Blaze softcore. The sequential process of those functions likely affected the overall latency, but no information was reported about their overhead. Moreover, the model was represented by 16-bit ﬁfixed-point data, which consumed many DSP resources to perform the MAC operations and led to heavy bandwidth pressure on the off-chip bandwidth. In contrast, our design accelerated the entire detection procedure and achieved an end-to-end latency of only 15.2 ms on XC325T FPGA. Our accelerator achieved 87% of the throughput of the previous work, while using only 29:8% of the DSP resources. This was achieved by quantizing the model to 8-bit, which resulted in an mAP of 76:7% on the VOC data set. To further evaluate the efﬁciency of our proposed design against accelerators implemented on different hardware platforms, we compare four technology alternatives—including ASIC, ARM?GPU, ARM?FPGA, and FPGAonly based object detection accelerators in Table 5. For ASIC-based designs, we select Intel NCS 2 [29], which achieves the lowest power consumption with a detection latency of 55 ms for YOLOv3-Tiny algorithm. The disadvantage of the ASIC design is that its function cannot upgrade to adapt for new detection algorithms, such YOLOv5, YOLOx, and new quantization schemes, such 4bit/2-bit CNN models. For GPU-based designs, we select the Jetson nano development board [30], which can deliver a detection latency of 40 ms for YOLOv3-Tiny with 32-bit computation precision. Compared with that, our design on Xilinx 325T FPGA shows an advantage of 2x shorter latency with only 20% more power consumption. For FPGA-only design, we select the design implemented on a Intel GX1150 FPGA [31]. For YOLOv3-Tiny algorithm, the end-to-end latency is 27.5ms. Due to the 32-bit ﬂfloating point data used for both the CNN computation and postprocessing algorithms, this design consumes more hardware resource and result in inferior detection latency. For ARM?FPGA implementation, we compare the design presented in [7], which employed the fast Fourier transformation (FFT) algorithm to reduce the number of multiplications required convolution computation. However, to maintain the same computation precision, the input operands for the complex multiplications utilized in the FFT were quantized into 16-bit width, resulting in roughly 2 external memory bandwidth compared to an 8bit quantized convolution approach. Consequently, its performance was limited by the external memory bandwidth and its highest achievable throughput was only

201:1=401 ¼ 50:1% that of our proposed accelerator when implemented on a device with similar resource, i.e., XC485T FPGA. Moreover, it only accelerated the CNN computation, while the post-processing was conducted on the CPU. However, the previous works [11, 32] show that the post-processing is crucial for the total latency of the detection.

We also evaluate the power efﬁciency of the accelerators with different technologies. It can be found that the ASIC-based accelerator Intel NCS2 achieved the highest power efﬁciency, because the hardware architecture of the ASIC-based accelerator has been carefully optimized. Compared to our implementation on 325T FPGA, the work in ISCAS2021 [4] achieved higher power efﬁciency. This is because the streaming accelerator has a low DDR access frequency, which reduces the power consumption of the DDR access.

Despite the improvements achieved by our proposed design, there are still some limitations that constrain further performance enhancement. For instance, when the batch size is equal to one, the throughput of the accelerator applied to the XC690T device is only 1.25 times greater than that of the XC325T device, while DSP utilization is only 25%. This limitation can be attributed to two main factors. First, as the degree of parallelism increases, more hardware resources are required. This results in an increase in difﬁcult in FPGA’s place and routing and a subsequent reduction in the operating frequency of the accelerator. For example, the parameters of the accelerator on the 690T were increased from Nm ¼ 12 to Nm ¼ 16, the operating frequency decreased from 200MHz to 180 MHz. Secondly, as shown in Figs. 18 and 19, performance is limited by the bandwidth of external memory when performing 1  1 convolution. As such, further improvement in throughput can only be achieved by increasing the batch size to enhance computational intensity.

## 6 Conclusion

This paper presents an efﬁcient FPGA accelerator design for YOLO series detection algorithms. The design utilizes multiple dimensions of parallelism to accelerate the convolution layers of the network model, and employs multiport parallel line-buffer-like on-chip data cache to minimize the external memory bandwidth utilization, resulting in improved detection performance when compared to state-of-the-art FPGA accelerators. Moreover, the postprocessing algorithms of the YOLO models are implemented by dedicated hardware circuits in the proposed accelerator, which signiﬁcantly reduced the end-to-end detection latency when compared to GPU and CPU-based implementation approaches. The combination of algorithm

and hardware optimization enabled the accelerator to achieve a 4 of throughput when implementing the same YOLOv2 algorithm on a low-end 325T FPGA and achieves a throughput of 859 GOPs/s when implementing YOLOv3 on Xilinx 690T FPGA.

In future work, we plan to utilize more advanced schemes to quantize the convolution with even lower bit width, such as 4-bit or 2-bit quantization, to further reduce the hardware resource cost and the bandwidth utilization. We also plan to implement other object detectors, such as faster-RCNN and FPN, to further evaluate the efﬁciency of proposed design two-stage-based detection algorithms.

Acknowledgements This work was supported by Beijing Natural Science Foundation under Grant No. 4202063, National Key Research and Development Program of China under Grant No. 2019YFB2204200.

Availability of data and materials All data generated or analyzed during this study are included in this published article.

Declarations

Conflict of interest The authors declare that they have no conflict of interest.
