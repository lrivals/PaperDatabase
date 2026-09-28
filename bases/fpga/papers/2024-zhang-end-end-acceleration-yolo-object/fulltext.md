---
id: 2024-zhang-end-end-acceleration-yolo-object
title: "End-to-end acceleration of the YOLO object detection framework on FPGA-only devices"
year: 2024
backend: grobid
---

## Abstract

Object detection has been revolutionized by convolutional neural networks (CNNs), but their high computational complexity and heavy data access requirements make implementing these algorithms on edge devices challenging. To address this issue, we propose an efficient object detection accelerator for YOLO series algorithm. Our architecture utilizes multiple dimensions of parallelism to accelerate the convolution computation. We employ line-buffer-based parallel data caches and dedicated data access units to minimize off-chip bandwidth pressure. Additionally, our proposed design not only accelerates the convolutional computation, but also control-intensive post-processing to achieve low detection latency. We evaluate the final design on Xilinx V7-690t FPGA device, achieving a throughput of 525 GOP/s for a batch size of 1 and 914 GOP/s for a batch size equal to 2. Compared with state-of-the-art YOLOv2 and YOLOv3 implementations, our proposed accelerator offers up to 9Â throughput improvement and 5Â shorter latency.

## 1. Introduction

Deep learning-based object detection algorithms have been applied in many fields, such as autonomous driving [1], medical image detection [2], and industrial inspection [3]. However, these algorithms still face some crucial problems, such as the high computational workload and bandwidth requirement of the convolutional neural network (CNN) computation, which restricts the actual application. Although a few object detection accelerators have been proposed, they still face some challenges. In the approach [4,5], two streaming object detection accelerators are designed, which map all the CNN layers within the YOLOv2-Tiny on a field programmable gate array (FPGA). All nine convolution layers are pipelined, which reduces the off-chip data access and improves the throughput. Though low latency and high digital signal processor (DSP) efficiency are achieved, it is challenging to implement very deep CNN algorithms such as YOLOv2 or YOLOv3 on them because the number of layers is restricted by the hardware resource. In the approach [6], an implementation of YOLOv3-Tiny is proposed, which achieves 460GOPS/s on the VC707 development board with a data width of 18-bit. Similarly, the work in the literature [7] introduced fast Fourier transform (FFT) to speed up the convolution operation. However, feature maps and weights are represented by relatively high bit width data types, i.e., 16-bit fixed-point numbers. This causes a higher consumption of computational and memory resources. In contrast, most CNN models can be represented by 8-bit data with negligible loss of accuracy, according to recent quantization research [8]. Lower data bit width can reduce DSP and memory consumption on FPGA, which enables the design to achieve equivalent performance with fewer hardware resources and lower energy consumption.

Furthermore, in most accelerator designs [4][5][6]9], the pre-and post-processing algorithms, such as the softmax layer, intersection-over-union (IOU) calculation, and nonmaximum suppression (NMS), are typically implemented on central processing units (CPUs). However, in certain scenarios with stringent latency requirements, CPU-based implementation schemes can often fail to satisfy the low latency demands, as indicated by studies of [10,11]. For instance, in industrial robotics, detecting targets within a brief latency window is crucial. This imposes strict requirements not just on the CNN computational latency but also on the post-processing latency. Therefore, it becomes necessary to devise an object detection accelerator that incorporates a dedicated hardware unit for postprocessing algorithms.

In this work, an end-to-end YOLO-based object detection hardware accelerator targeting implementation on FPGA fabric-only devices is proposed. The accelerator is designed with a flexible architecture in which each layer of the convolutional neural networks are computed in a sequential way so that it is possible to implement object detection algorithms with different sizes, e.g., YOLOv2 and YOLOv3. However, this structure increases the difficulty of data accessing and caching. To address this challenge, three data access units and an on-chip buffer are designed, where the former utilize the burst transfer to fully take advantage of the off-chip bandwidth, and the latter improves the on-chip data reuse. Moreover, the data access is overlapped with the convolution computation. The proposed accelerator is finally implemented and evaluated on the Xilinx's V7-690t FPGA device showing a throughput improvement of up to 9Â compared to the previous implementations [4,6,9] for YOLOv2 or YOLOv3. Furthermore, the pre-and post-processing of the algorithm are also conducted on the FPGA fabric, which further decreases the detection latency.

In summary, the main contributions of this paper are summarized as follows.

(1)

A novel end-to-end object detection accelerator targeting FPGA-only devices is proposed. The proposed architecture is scalable in multiple computational dimensions, enabling efficient acceleration of complex object detection neural network models, such as YOLOv2 and YOLOv3, on devices with varying resource constraints. In addition, FPGA fabrics are utilized to expedite post-processing operations in the object detection algorithms, thereby minimizing detection latency. Our design offers a unique approach to object detection acceleration, which addresses the challenges of deploying large network models on FPGA-only devices.

(2) An on-chip data caching strategy is proposed, which overlaps the data transfer time with convolutional computation, resulting in improved execution efficiency of the accelerator. The proposed approach utilizes a ping-pong buffer to enhance the data reuse of feature maps and weights. Additionally, weightloading unit and feature loading unit are designed to operate independently. Their state synchronization occurs only when a computation group's workload is complete, reducing the synchronization frequency and minimizing accelerator stall. (3) The proposed accelerator is implemented in parameterized HLS code, allowing for quantitative performance and hardware resource consumption modeling. A design space exploration scheme is developed to facilitate an automatic and fast search of the most appropriate parameter setting for any specific FPGA device.

The rest of the paper is organized as follows. Section 2 gives the background, discussing the structure of the YOLO series algorithms and the quantization method used in this paper. Section 3 presents the accelerator design, including data access unit design, computation unit design, and post-processing unit design. Section 4 details the modeling of the accelerator's performance and resource consumption and provides the optimal design parameters based on these models. The experiment setup is described in Sect. 5, which also discusses the experiment results. Finally, Sect. 6 concludes the work. For ease of reading, the abbreviations and symbols used in this paper are summarized in Table 1.

## 2. Detection algorithm preparation

In this section, the structure of the YOLO series algorithms is briefly introduced. Then, batch normalization (BN) fusion is applied. Finally, the activation and the weights are quantized to 8-bit.

### 2.1. Detection algorithm overview

As shown in Fig. 1, the YOLO series algorithms are composed of preprocessing, CNN computation, and postprocess procedures. In the preprocessing stage, the input is resized to a uniform size and then normalized. The CNN backbone neural network consists of the most computation workload in the inference procedure. Additionally, leaky ReLU and BN follow the convolution layers. The input of the CNN network is divided into D Â D grids, and a total of P vectors are generated by each grid. Each vector corresponds to a predicted bounding box, and it is composed of ð5 þ CÞ numbers where one number corresponds to the probability of containing an object, four numbers are responsible for the size and location of the bounding box, and the rest C numbers correspond to the category information. So, the output of size D Â D Â P Â ð5 þ CÞ is generated after convolution operations.

In the post-processing procedure, coordinates and confidence scores are calculated using the CNN outputs. Postprocessing consists of computation-intensive operations and control-intensive operations. Most of the computational resource is consumed by the sigmoid and exponential operations when decoding the coordinates of the bounding boxes. Then, NMS is carried out to filter out the redundant predictions, which is a control-intensive operation. Finally, the predicted objects are shown to the users.

### 2.2. Network structure optimization

Batch normalization helps to accelerate the training and prevent overfitting [12] when training the neural network. During the inference of the neural network, the BN operation is denoted as

ŷm ¼ c m Â y m À l m ffiffiffiffiffiffiffiffiffiffiffiffiffi ffi r 2 m þ p þ b mð1Þ

where y m and ŷm denote the input and output of the BN operation, respectively, and the subscript m denotes channel index. The fixed estimation of mean and variance of the mini-batch is denoted as l m and r 2 m , respectively, and the c m and b m are learnable parameters. Moreover, the , generally equally 1:0 Â 10 À5 , is added to the denominator for numerical stability. Batch normalization helps to achieve a stable distribution of activation, but the multiplication and division consume a lot of hardware resource when the network is implemented on the FPGA. Batch normalization can be seen as a linear operation like ŷm ¼

a m Â y m þ g m where a m ¼ c m ffiffiffiffiffiffiffiffiffiffiffiffiffi ffi r 2 m þ p ;ð2Þ

g m ¼ b m À l m c m ffiffiffiffiffiffiffiffiffiffiffiffiffi ffi r 2 m þ p :ð3Þ

Taking BN and convolution calculation into account, the process can be denoted as

ŷm ¼ a m Â ðx Ã W m þ B m Þ þ g m ;ð4Þ

where x, W m and B m denote the input, weight and bias of the convolution computation. The linear operation in Eq. 4 can be further fused into the convolution calculation, i.e.,

ŷm ¼ x Ã ða m Â W m Þ þ ða m Â B m þ g m Þ;ð5Þ

where a m Â W m and a m Â B m þ g m are the updated weight and bias. Furthermore, in the original network, the location and confidence are extracted by the neural network within one layer, for example, the 23rd filter in the YOLOv2 algorithm. A total of 100 images are randomly selected as the input of the network, and their distribution of the location and category information is shown in Fig. 2. It can be seen that the location information is mainly distributed between À2 and 2, while the category information is mainly distributed between À15 and 10. The difference in the numerical distribution makes it difficult to do the model quantization. Therefore, that convolutional layer is divided into two independent convolution layers, where one extracts the location information, and the other is responsible for the category information, and they are quantized separately.

### 2.3. Network quantization

Previous studies have shown that the parameters of neural networks can be represented by 8-bit dynamic fixed-point numbers without introducing obvious accuracy loss [13,14]. Neural network quantization not only relieves the pressure on the memory system, but also improves the efficiency of the DSP. Specifically, compared to a full precision network, the storage and bandwidth requirement of the 8-bit quantized model decreases by four times [15]. In current Intel and Xilinx FPGA devices [4,16], two 8 Â 8 fixed-point multiplication can also be efficiently implemented by consuming only one DSP block. This reduces hardware consumption and enables more operations to be carried out concurrently. In this work, the model and the activation are represented using the 8-bit dynamic fixedpoint number [15]. The value x of a B-bit fixed-point number x BÀ1 x BÀ2 . . .x 0 with the fractional length fl is given by

x ¼ Àx BÀ1 Á 2 BÀ1 þ X BÀ2 i¼0 x i Á 2 i ! Á 2 Àfl :ð6Þ

The fl correlates with the step size or resolution, and the representation range of a dynamic fixed-point number. To cover the large dynamic range of the data in CNN inference, the input, output, weight, and bias of each layer are quantized, respectively [15]. However, the parameter fl is an integer, and it is challenging to be optimized using backpropagation. In this work, we calculate the fl parameter from a continuous step size r using the equation fl ¼ Àblog r 2 c. The parameter r is calculated using the BRECQ quantization method [13].

In the BRECQ scheme, the quantization is performed on the weights, biases, and activations. For each layer in the CNN, the step size r for weights and biases is initialized by exhaustive search to minimize the quantization loss:

r Ã w ¼ arg min r w k ŵinit À wk 2 F ;ð7Þ

where k Á k F denotes the Frobenius norm, w denotes the weights or bias before the quantization, r Ã w denotes the initialized step size, and ŵinit denotes the initial quantized weights or bias which equals to

ŵinit ¼ r w Â clipðbw=r w c; À2 BÀ1 ; 2 BÀ1 À 1Þ:ð8Þ

To reduce the quantization loss, a learnable parameter v is added to the ŵinit to calibrate the least significant bits (LSBs) of the weights or bias. A sigmoid-like function rðÁÞ is then used to ensure that rðvÞ equals to 0 or 1. With this calibration, the final weight ŵ is equal to

ŵ ¼ r Ã w Â clipðbw=r Ã w c þ rðvÞ; À2 BÀ1 ; 2 BÀ1 À 1Þ:ð9Þ

In addition, a small number of randomly selected images are fed into the neural network as inputs. The difference between the convolution result of the quantized weight and the convolution result of the original weight is taken as the loss function. Afterward, back-propagation is used to optimize the learnable parameter v and the step size r w , i.e., v; r w ¼ arg min

v;r w kx Ã w À x Ã ŵk 2 F :ð10Þ

Similar to the weight quantization, the quantized activation x is equals to

x ¼ r x Â clipðbx=r x c; À2 BÀ1 ; 2 BÀ1 À 1Þ;ð11Þ

where the step size r x is also initialized and optimized using the similar method with the weight quantization.

## 3. Accelerator hardware design

The top-level architecture of the proposed accelerator is illustrated in Fig. 3. The proposed hardware accelerator is mainly composed of central processing element (PE) arrays, feature load unit, weight load unit, feature store unit, task scheduler unit, max-pooling unit and pre/postprocessing unit. A MicroBlaze processor is responsible for sending coarse-grained instruction to control the accelerator. The feature load unit and weight load unit are responsible for loading the features and weights from the external double data rate (DDR) synchronous dynamic random-access memory (SDRAM) to the on-chip buffers, which are designed to cache the required data for convolution operations to improve the data reuse and external memory bandwidth efficiency. The PE array is designed to accelerate the neural network computation by utilizing as many on-chip DSP blocks as possible to perform parallel convolution operations. Batch processing is also introduced by instancing multiple PE arrays to further improve the throughput. The convolution results are then written back to the external memory through the feature store unit. Each function unit has its own loop counter, and synchronizations between the functional units are controlled by the Task Scheduler unit. Synchronizations are only performed when all the cached data have been consumed by the PE array. The low synchronization frequency reduces the risk of accelerator stall caused by the high-latency off-chip memory access. Moreover, the preprocessing and postprocessing algorithms are done by the dedicated hardware unit.

### 3.1. PE array design

As shown in Fig. 3, the PE array is organized as N r compute units (CUs). Each CU, consisting of N p PEs, performs of the on-chip data busses and improve the arithmetic intensity of the executed computation. Moreover, this operation pattern could also be utilized to improve the peak performance of the convolution computation by up to 2Â with the same on-chip DSP cost by packing the two multiplication into one DSP block [4].

The detailed architecture of the PE is shown in Fig. 4a. Each PE contains N n DSP48 blocks that perform 2 Â N n 8bit integer multiplications in parallel. The products of these multiplications are summed and accumulated by an adder tree and a 32-bit accumulator, implementing the operations of

P N n i¼1 b i Â a i and P N n i¼1 b i Â d i in parallel.

Since the two 8 Â 8-bit integer multiplications of b i Â a i and b i Â d i share the common multiplier, we can pack these 2 Â N n multiplications into N n DSP48E1 block. The procedure of the packed multiplication and the hardware structure of the packed multiplier are shown in Fig. 4b,c, respectively. Firstly, the 8-bit integer a i is shifted and added with the other 8-bit integer d i by utilizing the pre-adder in the DSP block, and the 25-bit result is then multiplied with the common 8-bit multiplier b i using the 25 Â 18-bit hard multiplier. Finally, a 17-bit calibration number is added to the product by utilizing the 48-bit accumulator to eliminate the error caused by the sign extension operation when b i Â d i is negative [17]. Moreover, the 17-bit calibration number is calculated in advance by a simple logic circuit. In the approach of [18], up to eight products of the multiplications can be accumulated. However, it can only be applied to the DSP48E2 blocks due to the limitation on the width of the multiplier [19]. In contrast, our proposed scheme can be adopted for both DSP48E1 and DSP48E2 architectures. Compared to the approach of [4], our scheme consumes less logic resource since the operation of a i \\16 þ d i is conducted by the pre-adder inside the DSP48E1 block and only a small amount of logic resource is consumed to generate the calibration number. Moreover, the PE array is instanced for N b times to further improve the throughput by introducing batch processing. In total, the PE arrays consume

N r Â N p Â N n Â N b DSP48E1 blocks to perform 2 Â N r Â N p Â N n Â N b 8-bit MAC operations in each clock cycle.

The MAC results of size N r Â N m Â N b are generated in parallel, where N m is the number of MAC results generated by each CU, and it equals to 2 Â N p .

Due to the data broadcasting structure and shared controlling logic, implementing a large PE array on FPGA devices can lead to high fan-out problems, which may reduce the fmax of the final design [20]. To avoid this problem, an exclusive loop controller is designed for each CU to reduce the fan-out of the controlling logic, and the data broadcasting is only performed within each CU. This multiple CU architecture has a significant advantage in scalability, which enables the proposed accelerator to be implemented on any type of FPGA device with near linear performance growth as the number of on-chip logic and DSP hardware resources increases.

### 3.2. On-chip memory system design

The memory system of the accelerator is mainly composed of a group of on-chip buffers and external memory access units (namely the feature load, feature store unit, and weight load units). The on-chip buffer caches the serial input read from the external memory, reorders, and sends the data to the N r Â N b CUs for parallel computation. The local data buffers can significantly reduce the data access latency of the PE array and improve the data reuse rate to relieve the pressure on external memory bandwidth. Moreover, a ping-pong buffer architecture is also proposed to overlap the data transfer with CU computation. The external memory access units are responsible for performing the high-throughput external memory access, where the burst memory access transfer is utilized.

As shown in Fig. 5, the feature buffer is constructed by 2N RAM line buffers with one shared input port and N r parallel output ports. The depth and the width of each line buffer equal to D f and N m Â N b bytes, respectively. The feature map data are fetched from external memory and stored in the line buffers in a zig-zag way, in which the address mapping sequence is controlled by the input multiplexer. One major benefit of this data caching scheme is that burst memory transfer can be utilized to maximize the external memory bandwidth since the physical address of the input data is continuous within each line. A total number of 2N RAM buffer lines is designed to form a pingpong structure, which overlaps the data transferring procedure with the convolution computation to improve the efficiency of the accelerator. Detailed pipelining strategy is explained in Sect. 3.4.

A total number of N r Â N m Â N b vector outputs are generated by the PE arrays in parallel in every L CU cycles, which correlates with the convolution calculation mapping that is introduced in Sect. 3.3. However, the result must be written back to the external DDR SDRAM in a serial way. This imbalance raises two design challenges for the Feature Store unit, namely converting parallel data into serial data and maximizing external memory bandwidth utilization. A ping-pong buffer is designed to address the first issue. As shown in Fig. 6, once the parallel outputs are generated by the PE array, the ping-pong buffer starts to cache the result. In each cycle, N m Â N b out of the N r Â N m Â N b outputs results are selected and stored in one of the ping-pong buffer. While converting the parallel convolution results of the current iteration, the converted serial results of previous iteration stored in another ping-pong buffer are being written to the external memory concurrently. Secondly, burst memory transfer is also utilized in the data store procedure to maximize the external memory bandwidth and minimize the latency. A total of N r cycles are needed to store the parallel outputs which is generated every L CU cycles. Therefore, to avoid any stall operations in the Feature Store unit or the PE array, the following condition must be satisfied: L CU [ N r . In deep convolution neural network algorithms, the convolution operations are generally performed on vector data with large sizes, which can normally meet this requirement.

### 3.3. Convolution task mapping

Convolution calculation occupies the major workload in CNN inference computation [21]. As illustrated in Algorithm 1, it performs the inner product of the neural network weight W and the input feature map FI. The input, output feature maps and weights are of the size N Â R Â C, M Â R 0 Â C 0 and M Â N Â K Â K 0 , respectively, and S denotes the stride of the convolution. Both parallelism mapping and data caching should be taken into concern together when mapping the convolution calculation on the proposed accelerator. The former optimization finds the best way that maps the convolution algorithm on the PE array that can maximize the acceleration of the convolution Fig. 5 Feature buffer design. The line buffers cache the serial data from the external memory, and output parallel data streams to the CUs computation by executing as many as parallel operations in each cycle. The latter optimization targets utilizing on-chip buffers to enhance on-chip data reuse rate to improve external memory efficiency.

### Parallelism mapping

From Algorithm 1, it can be observed that there is no computation dependency among each output channel dimension mm and each output row dimension rr, so the calculation for multiple output channels and output rows can be conducted in parallel. As shown in Fig. 7, three degrees of parallelism are exploited in the proposed accelerator, i.e., N m and N r convolution kernels are executed in parallel along the output channel and the input row dimensions, respectively, while N n MAC operations are conducted concurrently within each convolution kernel to further accelerate the computation. For a convolution kernel of size K Â K 0 Â N, the MAC results of size N r Â N m are generated every L CU ¼ K Â K 0 Â dN=N n e cycles. The workload of N m convolution kernels along the output channel direction is carried by one CU, where every two convolution kernels are mapped to a PE since they share the same input feature map, which matches the multiplication packing scheme proposed in Sect. 3.1. During the convolution, as shown in Fig. 3, each CU gets its own input feature map data from the feature buffer, and those data are shared by the PEs within a CU. At the same time, weights are loaded and shared among the N r CUs, and each PE gets 2 Â N n pixels of weights correlating with two convolution kernels. Therefore, a total of N r Â N m Â N n MAC operations are conducted concurrently by one PE array. Moreover, the calculation of N b different inputs are also conducted concurrently to further improve the parallelism and the weights reuse.

Data caching To produce one output feature pixel, the accelerator needs to hold the amount of K Â K 0 Â N pixels of feature map and weight data for parallel computation, respectively. As the convolution kernel slides over the whole input feature map, more feature data have to be fetched repeatedly from external memory [16], while the weight data can be reused. To fit the depth of the on-chip feature buffer, we propose to divide and execute each convolution layer as multiple computation groups, and each group consists of N r Â Q l Â N m times of convolution computation defined in Algorithm 1. As shown in Fig. 7, the depth and the height of each computation group (i.e., N m and N r ) fit the size of the PE array, while the width Q l is determined by the depth of the feature buffer. Consequently, the number of computation groups along the row, column, and channel dimensions can be calculated by

G r l ¼ dR 0 l =N r e; G c l ¼ dC 0 l =Q l e; G m l ¼ dM l =N m e:ð12Þ

The whole range of the input feature data that corresponds to one computation group is defined as a pre-fetch window.

As shown in Fig. 7, the height and width of the pre-fetch window can be calculated by

H win ¼ ðN r À 1Þ Â S þ K; W win ¼ ðQ l À 1Þ Â S þ K 0 :ð13Þ

Consequently, the whole input feature map is divided into G r l Â G c l pre-fetch windows during execution on the accelerator, and the data within a pre-fetch window are shared by G m l convolution groups along the output channel dimension. For instance, computation group 1 and group 2 share the pre-fetch Window A.

Since there is a fixed interval of S lines between the feature maps required by the adjacent convolution tasks, each line buffer in the feature buffer is designed to store at most S lines of feature maps to avoid possible data access collision. So, a total number of N RAM ¼ dH win =Se line buffers are configured in the feature buffer. Given the depth of the line buffer as D f , the width of the pre-fetch window equals to

W win ¼ D f =ðN Â SÞ:ð14Þ

Considering the correlation between the Q l and W win which is shown in Eq. ( 13), the width of the computation group is restricted by

Q l ¼ bðW win À K l Þ=S l c þ 1:ð15Þ

For instance, in Fig. 5, assuming that the size of the convolution kernel is of the size 3 Â 3 Â 1 and S ¼ 2, N r ¼ 4, then the height of the perfetch window equals to

H win ¼ ðN r À 1Þ Â S þ K ¼ ð4 À 1Þ Â 2 þ 3 ¼ 9

, and the number of line buffers is CeilðH win =SÞ ¼ Ceilð9=2Þ ¼ 5.

The execution order of the computation groups has a significant impact on the on-chip data reuse rate and external memory bandwidth utilization. Two scheduling schemes are considered in this work. As shown in Fig. 7, the first task scheduling scheme (Scheme-A) launches the computation groups in the order of Group 1, 2,..., 24, which can maximize the reuse rate of cached feature map data since adjacent groups along output dimension M (e.g., Group 1 and 2) share the same pre-fetched window. The second strategy (Scheme-B) is to execute the computation groups in the order of Group 1, 3, 5,..., 24, which can improve the weight data reuse rate, since these groups share the same weights. The efficiency of these two schemes are determined by multiple factors, such as the size of each group, the neural network structure, and the external memory bandwidth limitation. Therefore, experiments have to be conducted on the target FPGA platform to measure the execution time and bandwidth utilization before making the final decision. In Sect. 4.4, we will provide detailed experiment results and compare the pros and cons of these two scheduling schemes based on the Roofline model. Algorithm 2 summarizes the optimized convolution dataflow. In this dataflow, each group of computation tasks is performed sequentially, and its corresponding data are also cached sequentially. Moreover, a total number of G m l groups share the same input feature map. As shown in the Line 11 and Line 17 of Algorithm 2, a total of N m Â N r Â N n MAC operations are conducted concurrently.

Task scheduler is designed to synchronize the state of each function unit and dynamically schedule the convolutional computation, which reduces the control workload of the processor. As illustrated in Fig. 7, the convolution operation is divided into multiple computation groups, and the execution of each group is dynamically scheduled by the task scheduler unit. Besides managing the execution order of the computation groups, the task scheduler unit also synchronizes the state of each function unit. As shown in Fig. 8, at the beginning of each layer, the feature and weight data are first loaded from the external memory and cached in the on-chip buffers. When finishing loading the required data by the first computation group, (i.e., Time 1), the task scheduler unit sends signals to start the PE array. While the PE array conducting the convolution, the Feature Load unit and Weight Load unit continue loading feature map and weight data for the subsequent groups, i.e., from time 1 to 2. Since the convolution group 2 and group 1 share the same input feature map, computation group 2 can be started upon finishing group 1 and loading the required 8 Task-level pipeline strategy weights data, i.e., the time 2. Additional attention should be paid that, at this time point, the loading of pre-fetch window B does not need to be finished, since window A is still in use.

In the proposed architecture, synchronization is only performed when new input feature map or weight data were required, and each functional unit runs independently for the rest of the time, which reduces the risk of accelerator stall caused by high-latency off-chip memory access. In addition, a larger feature map pre-fetch window will reduce the frequency of synchronization, which helps to improve the efficiency of the accelerator, but will consume more on-chip memory resources. Therefore, the size of the perfetch window has to be selected carefully to balance the performance and hardware cost, and it will be introduced in the design exploration Sect. 4.3.

### 3.5. Post-processing

The detailed processing procedures of the post-processing algorithms in YOLO detector is illustrated in Fig. 9. The YOLO algorithms predict the coordinates of bounding boxes relative to the location of the grid cells, where a sigmoid function constrains the center coordinates of the bounding box to fall in the grid cell [12]. The exponent function extracts the height and width of the bounding box, which ensures the width and height are greater than 0. The confidence scores are extracted from the network's prediction by multiplying the outputs of the softmax function and the probability of containing an object. Then, the confidence scores under the threshold are filtered to reduce the amount of candidate boxes. Once finished the coordinates and confidence scores extraction, the NMS is carried out to further filter the redundant predictions. In the NMS stage, the confidence scores are sorted firstly, and the box corresponding to the largest score is selected as one candidate box for this class. Then the IOU values between this box and all other boxes are calculated and those boxes whose IOU values are above the predefined threshold are discarded. This procedure continues until all boxes are either selected or discarded [10].

The coordinates and confidence scores extraction are computational-intensive tasks consisting of a large amount of sigmoid, exponent and softmax functions. These nonlinear functions require complicated floating point operations. In contrast, the NMS algorithm is generally controlintensive since it contains many indexing, sorting and grouping operations. In most accelerator designs [4][5][6]9], those functions are implemented on general-purpose processors, such as the ARM or x86 CPUs, as software programs. Since these CPUs are mainly hard-core processors with high computing performance, the implemented programs can be executed with very low latency delivering real-time detection results. However on FPGA fabric-only devices, only softcore CPU processors, such as the MicroBlaze [22] and NIOS [23] processors, are available with very limited computational capability. Therefore, the above algorithms in the post-processing stage of YOLO detectors have to be implemented in dedicated hardware circuits to achieve real-time processing speed.

### Coordinates calculation

The location of a prediction box is represented by the coordinates of two diagonal points, i.e., ðx 1 ; y 1 Þ and ðx 2 ; y 2 Þ. According to the YOLO algorithm [12], the normalized location x 1 can be calculated by

x 1 ¼ ½ðrðt x Þ þ c x Þ À ð0:5 Á p w Á e t w Þ Á scale;ð16Þ

where r denotes the sigmoid function, and t x and t w are coordinates information extracted from the CNN outputs, and c x is the offset from the top left corner of the image, and p w represents the width of the bounding box prior. The architecture of the proposed hardware location decoding unit is shown in Fig. 10. Since t x , t w , c x and p w are all quantized in 8-bit fixed-point format, the sigmoid and exponential functions can be implemented by look-up table with low hardware costs. In the location decoding unit, two look-up tables with 256 entries are utilized to Confidence scores calculation The confidence scores equal to the product of the softmax function and the probability of containing an object. Its architecture is shown in Fig. 11, which can be divided into three stages. In the first stage, the maximum value is extracted from the serial inputs. In the second stage, the subtraction is conducted between the inputs and the maximum value, and their exponentiation and summation operations are calculated. In the last stage, the floating point multiplication and division are carried out. It should be taken into account that during the confidence score calculation, only the multiplication and division in the third stage are carried out using the float data.

Si ¼

e ðx i ÀX max Þ P N j¼1 e ðx j ÀX max Þ ;ð17Þ

NMS unit After the coordinates and confidence scores were calculated, a large number of redundant candidate boxes for the same target are generated, and these candidate boxes may overlap with the neighboring boxes. In order to solve this problem, the NMS is carried out to find the best target bounding box and eliminate the redundant boundary boxes. A hardware-friendly NMS algorithm was proposed by [10], where the sorting of confidence scores was omitted. The design achieved a very low latency at the cost of using 430 on-chip DSP blocks. This hinders the implementation of the hardware NMS on some resource-constrained devices. Inspired by that work, a resource-efficient NMS algorithm is proposed in this work, which is shown in Algorithm 3. For each input bounding box, its IOU between each selected box is calculated. The selected box will be replaced when the IOU is beyond the threshold, and the confidence score is less than that of the input box. The input box is inserted to the selected boxes when the IOU between the input box and each of the selected boxes is less than threshold. The hardware architecture of the NMS unit and the overall post-processing unit is shown in Fig. 12.

The proposed NMS hardware unit is mainly composed by a selected box buffer and an IOU calculation unit. The NMS unit connects with the coordinate and score calculation units using two channels, which forms a deep pipeline structure to reduce the off-chip data access. A threshold unit is designed to filter out the boxes with low confidence score, which relieves the workload of the NMS unit.

Design space exploration plays an important role in FPGAbased accelerator design, which enables the system to achieve a balance between performance and resource consumption. In this section, the performance and resource consumption models are first built, and comprehensive design space exploration is then carried out to find the optimal parameters for the PE array and the on-chip memory system. Moreover, the performance of the two task scheduling schemes discussed in Sect. 3.3 is also measured and compared by using the Roofline model.

### 4.1. Accelerator performance

According to the Roofline model [24,25], the throughput is constrained by either the bandwidth roof (R bw ) or computational roof (R cp ). The computational roof measures the peak throughput provided by the computation resource in the system. The bandwidth roof measures the throughput that the memory system can support [25]. The overall throughput equals to minðR bw ; R cp Þ. The proposed design has a total of N r Â N b CUs. Each CU performs N m Â N n MAC operations concurrently. Considering a MAC operation as two operations, i.e., addition and multiplication, the computational roof equals to

R cp ¼ 2 Â N n Â N r Â N m Â N b Â Freq:ð18Þ

Once finishing loading a feature pre-fetch window, the feature will be used by G m l computation groups along the output channel dimension. Therefore, the total pixels of feature map data loaded from and written to the external memory for the l-th layer of convolution computation is

H f l ¼ ðG c l Â G r l Â W win Â H win Â N þ C 0 Â R 0 Â MÞ Â N b :ð19Þ

For each computation group, an amount of K Á K 0 Á N Á N m weights is required, so the total amount of weights that needs to be loaded from external memory during one layer of calculation equals to

H w l ¼ G c l Â G r l Â K Â K 0 Â N Â M:ð20Þ

The arithmetic intensity, which is calculated as the ratio of the amount of calculation to the amount of external memory access, is denoted as

I ¼ #OP l H f l þ H w lð21Þ

where the #OP l denotes the number of operations performed in the l-th convolution/FC layer, and it equals

#OP l ¼ 2 Â K Â K 0 Â N Â C 0 Â R 0 Â M Â N b :ð22Þ

Further, the peak throughput supported by the memory system equals to the product of the arithmetic intensity and external memory bandwidth, i.e.,

R bw ¼ I Â BW DDR ;ð23Þ

where BW DDR denotes the bandwidth of the external memory. The theoretical execution latency for the l-th convolution/FC layer equals to the quotient of the number of MAC operations and the throughput, i.e.,

T l ¼ #OP l Á dR 0 =N r e Á N r =R 0 minðR cp ; R bw Þ :ð24Þ

Equation ( 25) measures the latency of performing the deep CNN algorithm, which equals to the sum of latency of all the layers, while the overall throughput equals to the quotient of the total amount of calculation and the T sum .

T sum ¼ X L l¼0 T lð25Þ

### 4.2. Hardware resource consumption

The proposed accelerator can be configured by a group of hardware parameters, including the N n , N r , N m , and N b related to the parallelism and the D f related to the depth of

C dsp ¼ 1 2 Â N n Â N r Â N m Â N b þ C 1 ;ð26Þ

where C 1 denotes the DSP resource consumed by the rest of parts of the accelerator, such as the address generator. The feature buffer and weight buffer consume the most of on-chip RAM resources. The feature buffer is composed by N r þ dðK=SÞe À 1 dual-ports RAMs with the depth of D f Â S Â N. When modeling the consumption of on-chip RAMs, not only the size of the buffer needs to be considered, but also the width of the port. A few more RAM blocks are needed to achieve a large port width, for the onchip memory block has its limitation of maximum port width. In this work, the width of the feature buffer equals to 8 Â N m Â N b bit, and the width of the weight buffer equals to 8 Â N n Â N m bit. The total on-chip memory consumption is estimated by ( 27)

C mem ¼ C 2 Â N n Â N m þ C 3 Â N r Â N m Â D f Â N b þ C 4 ;ð27Þ

where C 2 , C 3 , C 4 denotes the factor the parameters that measure the number of BRAM consumed by the weight buffer, feature buffer, and the rest of the modules.

The PE array takes up most of the logic consumption to generate the adder tree and the accumulator. The logic consumption for each adder tree correlates with the number of additional operations, i.e., N n , and the logic consumption for a 32-bit accumulator can be seen as a constant. Moreover, there are a total of N r Â N m Â N b adder trees and accumulators in the PE array. So, the logic consumption is estimated by

C logic ¼ ðC 5 Â N n þ C 6 þ C 7 Þ Â N r Â N m Â N b þ C 8 ;ð28Þ

where C 5 Â N n þ C 6 and C 7 measure the logic consumed by an adder tree and a 32-bit accumulator, respectively, and C 8 denotes the logic consumed by other functional units.

### 4.3. Design space exploration

The final goal of the design space exploration is to find the highest throughput while keeping the three types of hardware resource consumption within the device limitation. In the design space exploration, the hardware resource consumption is constrained under 70% to prevent timing issues, i.e., maxðThroughputÞ s:t: :

C dsp 0:7 Â DSP lim C mem 0:7 Â MEM lim C logic 0:7 Â LOGIC lim ;ð29Þ

where DSP lim , MEM lim and LOGIC lim denotes the available DSP, on-chip memory and logic resource, respectively. According to (24), both the computation roof and bandwidth roof should be considered during the exploration of the peak performance. Moreover, the power consumption of the system and the frequency of external memory access are usually positively correlated with each other. Therefore, the external memory access needs to be limited to a relatively low level to reduce the system power consumption and the external memory bandwidth pressure. According to (19) and ( 20), the feature and weight access are correlated with the number and size of the convolution group which depend on N r and D f . As shown in Fig. 13a, the external memory access drop sharply with the increase in D f , when D f is less than 8192. However, the decline of external memory access tends to slow down when D f is greater than 8192, and the on-chip memory consumption correlates with D f . Taking the on-chip memory consumption and the external memory access into consideration, the D f is set to 8192. Similarly, as shown in Fig. 13b, the decline of external memory access slows down when N r is greater than 13. Moreover, the speed-up gain reaches a saturation value when N r [ 13, which is caused by the low PE array utilization when conducting the last few layers of convolution, where the size of the feature map in dimension R 0 is relatively small. According to the external memory access and the speed-up gain, N r is set to 13 to achieve the most efficient speed-up gain and low external memory access.

Subsequently, a few rounds of compilation are conducted to gather the resource consumption information correlated with different settings of parameters N n , N m and N b , including the logic, on-chip memory, and DSP consumption. The inference latency and the resource consumption are shown in Fig. 14, and the parameters that achieve minimum latency under the device resource limitation are expected. Furthermore, routing or timing failures may be caused by high resource occupancy, so in this design, we constrain the consumption under 70% of the total hardware resource. In the final implementation, N n ¼ 8, N m ¼ 16, N r ¼ 13 and N b ¼ 2 are selected, and the achieved highest frequency is 160 MHz.

### 4.4. Comparison of task scheduling methods

As discussed in Sect. 3.4, the scheduling Scheme-A maximizes the reuse of feature map, while the Scheme-B maximizes the reuse of weights. In this section, these two schemes are evaluated by using the Roofline model. The performance of Scheme-A has already been modeled in Sect. 4.1, so this section only focuses on modeling the performance of Scheme-B. In Scheme-B, the input feature map data are not shared among different groups, and a total number of H win Â W win Â N input pixels are needed to be loaded from external memory before conducting one group of the convolutional task. Therefore, for the l-th convolution layer, the total amount of feature map data loaded from and written to the external memory in Scheme-B equals to

h f l ¼ ðG c l Â G r l Â G m l Â W win Â H win Â N þ C 0 Â R 0 Â MÞ Â N b :ð30Þ

For the weights, every G c l Â G r l groups share the same data, so the amount of weights to be loaded for the l-th layer is

h w l ¼ K Â K 0 Â N Â M:ð31Þ

Then, theoretical throughput can be calculated by using Eqs. ( 30), (31) and the performance models defined in Sect. 4.1. The final obtained Roofline models for both Scheme-A and Scheme-B are shown in Fig. 15, where the overall throughput when implementing YOLOv2 algorithm with different batch sizes are proposed. Special attention should be paid to when modeling the computational roof, and a total of 30% hardware resource is reserved. As shown in Fig. 15a, the arithmetic intensity increases linearly with the increase in batch size from 1 to 4, which is caused by the increase in off-chip bandwidth utilization. The increase in the arithmetic intensity slows down when the batch size is greater than 4, for the full utilization of off-chip bandwidth. As shown in Fig. 15b, the throughput is bandwidthbounded. From the above comparison, it is clear that Scheme-A is superior to Scheme-B, and is thus adopted in the final implementation. 5 System implementation and performance evaluation

### 5.1. Experimental setup

To evaluate the proposed accelerator, we utilized the KC705 and VC709 development boards, covering FPGAs with varying capacities. The KC705 board contains a lowend Xilinx XC7K325T FPGA with 203k LUTs, 840 DSPs, and 16Mbit BRAM. One DDR3 memory with a capacity of 1GB is connected to the FPGA device on the board with a transfer bandwidth of 64 @ 1600MTs. The VC709 development board contains a Xilinx XC7VX690T FPGA with 433k LUTs, 3600 DSPs, and 52.9Mbit BRAM. Two DDR3 memories, each with a capacity of 4GB and a transfer bandwidth of 64 @ 1600MTs, are connected to the FPGA device on the board. To compile the HLS and generate RTL, we utilized Vitis HLS 2021.2, and the bitstream was generated using Vivado 2021.2. The program for the host processor was compiled using Vitis 2021.2. The neural networks were trained using the MMDetection 2.14 framework [26] on the PASCAL VOC 2007 and VOC 2012 datasets [27]. We quantized the neural network using the scheme of BRECQ [13], optimizing the bit width of activations and network parameters to 8-bit. The platform used for the model quantization was composed of an Intel i7-6700k CPU, four 2080Ti GPUs, and 64 GB RAM. Approximately, 2.5 and 4 h were consumed in quantizing YOLOv2 and YOLOv3, respectively. The HLS compiling and hardware generating platform comprised an AMD R9-5950x CPU and 64 GB RAM. The time consumption for generating hardware varies with hardware parameters is shown in Fig. 16, where the compilation time increases with the increase in hardware parameters N n and N m . The compilation time also reflects the difficulty of hardware generation, which is often related to the factors such as parallelism and fan-out.

To ensure a fair comparison with previous works [6,7,9], the LUT, BRAM, and DSP utilization information reported by Vivado is utilized to evaluate the resource consumption of the accelerator. Both FPGA's power consumption and the power of the development board were measured. The FPGA's power consumption was reported by the power analyzer of Vivado, as in previous work [9]. The power consumption of the entire board was measured using the power meter plugged into the development platform, as in previous work [7]. The actual execution time of each layer was measured by using a software timer provided by the MicroBlaze MCU.

The design parameters for the two FPGA devices change accordingly based on their capacities. As per the model described in Sect. 4, the 325T FPGA device was evaluated using selected parameters, namely N n ¼ 8, N m ¼ 12, N r ¼ 13, and N b ¼ 1, which quantifies the accelerators' performance on resource-constrained devices. To assess the accelerator's performance on a device with larger capacity, performance tests were conducted using

N n ¼ 8, N m ¼ 16, N r ¼ 13, N b ¼ 1, and N n ¼ 8, N m ¼ 16, N r ¼ 13, and N b ¼ 2.

Overall, the workflow of the accelerator design is shown in Fig. 17, which is mainly composed of the model preparation and hardware preparation. Once finishing training the CNN model, the parameters of BN are merged into the weights and bias, then quantization is conducted using the BRECQ method. For the hardware preparation, the optimal hardware parameters for the target FPGA device are generated using the performance and resource model. Then, the HLS compilation is conducted using the aforementioned hardware parameters. Finally, the IP cores are connected, and the hardware is generated using Vivado.

### 5.2. Performance evaluation of the hardware accelerator

The baseline YOLOv2 and YOLOv3 algorithms have been implemented on our proposed hardware accelerator. The theoretical execution time of each layer was used to measure the efficiency of the accelerator, and it is calculated by

t 0 l ¼ #OP l 2 Â N n Â N m Â N r Â N b Â Freq ;ð32Þ

where the denominator represents the maximum throughput that the PE array can provide. The execution efficiency of the accelerator was calculated by E l ¼ t 0 l =t l , where t l denotes the measured execution time of the l-th layer. For the YOLOv2 network, the theoretical execution time and actual execution time were also compared in Fig. 18. It can be observed that the actual execution time for most of the layers was close to the theoretical time except for six layers, i.e., the 1st, 4th, 7th, 21st, 23rd, and 24th layer. Two problems led to the low efficiency of the first layer. Firstly, the first layer only has three input channels, resulting in inadequate utilization of the parallelism in the N n direction. Secondly, according to the performance model, the calculation latency equals to L CU ¼ K Â K 0 Â dN=N n e ¼ 3 Â 3 Â d3=8e ¼ 9; which is smaller than N r . Consequently, N r vectors each with a size of 1 Â 1 Â N m are produced every L CU clocks. However, it takes N r clocks to write these vectors back to the DDR memory. Moreover, in contrast to convolutions with large filter sizes, 1 Â 1 convolutions have relatively low reuse of the input feature, resulting in a low arithmetic intensity. According to the Roofline model, their performances are restricted by the memory bandwidth limitations. However, the execution time of these layers was very short, so the negative impact on the overall performance was negligible. The actual throughput of the proposed detection system equals to the ratio of the operation amount to the total measured time consumption, i.e.,

TPS ¼ P L l¼1 #OP l P L l¼1 t l :ð33Þ

In this work, the achieved highest throughput of the accelerator was 914 GOP/s, which is achieved on the XC690T with the N n ¼ 8, N m ¼ 16, N r ¼ 13, and N b ¼ 2 and the frequency equals to 160 MHz. The power consumption of the FPGA device was 12.5 W, which was estimated using the Vivado development tool, and the power consumption of the whole board was 24.1 W. The performance of implementing YOLOv3 on the accelerator is shown in Fig. 19. The computation efficiency of ten layers are lower than 60%, and the reason for the low efficiency is the same as that of YOLOv2. Moreover, the execution time of these layers was also short, so the overall efficiency is relative high.

The resource consumption of each part of the accelerator is depicted in Fig. 20. Figure 20a indicates that the memory controller and AXI interconnect consume roughly 25% of the LUT resources, which poses challenges for FPGA's routing and timing optimization. Nevertheless, the model presented in Sect. 4.2 can still accurately predict LUT consumption because we have observed that the resource consumption of memory controller remains constant. Additionally, over 60% of the BRAM consumption in the accelerator is attributed to LocalBuffer. As shown in Fig. 20c, more than 90% of the DSP resources are utilized to implement the PE array. The resource consumption of the LUTs, BRAM, and DSPs are presented by small dots in Fig. 14, and it is apparent that they conform to the model presented in Sect. 4.2.

When implementing YOLOv2 algorithm, a total of 13 Â 13 Â 5 ¼ 845 candidate boxes were processed sequentially by the post-processing unit. As shown in Fig. 18, its time consumption equals to 0.38 ms, which is relatively low compared to the CNN computation. Moreover, the latency is proportional to the number of candidate boxes. The breakdown hardware consumption of the post-processing unit is shown in Table 2, which is composed by the three aforementioned units and one misc unit. The misc unit is mainly composed by channels and global memory ports. Compared to the approach of [10], the hardware resource consumption of our design is relatively low, which enables implementing the accelerator in some resource-constrained devices.

### 5.3. Comparison with state-of-the-art

The performance of several state-of-the-art hardware accelerators based on FPGA for object detection tasks is 3 and4 depending on the networks used. To ensure fairness in the comparison, the performance results are measured and reported using a batch size of 1. Table 3 presents a comparison between two reference accelerators that implement YOLOv2-related models and our proposed design. The design presented in [4] deployed the entire YOLOv2-Tiny neural network onto a single FPGA device, minimizing the need for external memory access. Furthermore, the computation of all convolution layers was organized as a deep pipeline and workload balance was employed to achieve a low inference latency of 27.78 ms with the input size of 1280 Â 384. However, a limitation of this design is that the accelerator architecture is fixed and cannot be reprogrammed by software to implement larger detection models, such as standard YOLOv2 or YOLOv3. In contrast, the architecture proposed in this work is highly flexible and capable of executing convolution computations with arbitrary input and filter sizes. For instance, our design can implement the standard YOLOv2 model on the XC7325T device, which has even fewer logic and DSP resources than the device used in [4]. For the detection latency, our YOLOv2-Tiny implemented on XC325T achieved an end-to-end latency of 14.49ms with the input size of 416 Â 416. In [9], a cross-layer dataflow strategy was introduced to optimize the frequency of external memory data access. However, this design implemented separated hardware units for the 1 Â 1 and 3 Â 3 convolution layers, leading to significant imbalance in hardware resource utilization. Consequently, the highest throughput achievable by the accelerator when executing the YOLOv2 model was limited to only 100.3 GOP/s. In contrast, the programmable convolution unit in our design can fully utilize as many as possible on-chip hardware resources to accelerate all the convolution layers in the neural network model, resulting a 5Â throughput at the cost of 2:2Â of on-chip DSP resources consumption.

In Table 4, our results are compared with those of two other FPGA accelerators that implement YOLOv3-related models. The design in [28] utilized the similarities between continuous inputs in video, and skipped the convolution operation of similar data between continuous inputs. Winograd algorithm was also used to optimize the 3 Â 3 convolution in the YOLOv3-Tiny to further improve the throughput. Experimental results show that their accelerator achieved a throughput of 348 GOP/s on ZCU104 evaluation board. This work brings new highlights to the processing of continuous video input. However, a relative large batch size is required by that work to utilize the similarity between the input, which results in a large inference latency of 107.81 ms, and this is not suitable for implementing this accelerator on low latency scene. Compared with that work, our accelerator achieved an end-to-end latency of 15.2 ms on XC325T FPGA, which reduces 7Â of latency. The design in [6] consumed 2304 DSPs of the XC7VX485T FPGA device and achieved a performance of 460.8 GOP/s. However, preprocessing, activation functions, pooling, and other miscellaneous operations were conducted by a low-performance Micro-Blaze softcore. The sequential process of those functions likely affected the overall latency, but no information was reported about their overhead. Moreover, the model was represented by 16-bit fixed-point data, which consumed many DSP resources to perform the MAC operations and led to heavy bandwidth pressure on the off-chip bandwidth. In contrast, our design accelerated the entire detection procedure and achieved an end-to-end latency of only 15.2 ms on XC325T FPGA. Our accelerator achieved 87% of the throughput of the previous work, while using only 29:8% of the DSP resources. This was achieved by quantizing the model to 8-bit, which resulted in an mAP of 76:7% on the VOC data set.

To further evaluate the efficiency of our proposed design against accelerators implemented on different hardware platforms, we compare four technology alternatives-including ASIC, ARM?GPU, ARM?FPGA, and FPGAonly based object detection accelerators in Table 5. For ASIC-based designs, we select Intel NCS 2 [29], which achieves the lowest power consumption with a detection latency of 55 ms for YOLOv3-Tiny algorithm. The disadvantage of the ASIC design is that its function cannot upgrade to adapt for new detection algorithms, such YOLOv5, YOLOx, and new quantization schemes, such 4bit/2-bit CNN models. For GPU-based designs, we select the Jetson nano development board [30], which can deliver a detection latency of 40 ms for YOLOv3-Tiny with 32-bit computation precision. Compared with that, our design on Xilinx 325T FPGA shows an advantage of 2x shorter latency with only 20% more power consumption. For FPGA-only design, we select the design implemented on a Intel GX1150 FPGA [31]. For YOLOv3-Tiny algorithm, the end-to-end latency is 27.5ms. Due to the 32-bit floating point data used for both the CNN computation and postprocessing algorithms, this design consumes more hardware resource and result in inferior detection latency. For ARM?FPGA implementation, we compare the design presented in [7], which employed the fast Fourier transformation (FFT) algorithm to reduce the number of multiplications required for convolution computation. However, to maintain the same computation precision, the input operands for the complex multiplications utilized in the FFT were quantized into 16-bit width, resulting in roughly 2Â external memory bandwidth compared to an 8bit quantized convolution approach. Consequently, its performance was limited by the external memory bandwidth and its highest achievable throughput was only 201:1=401 ¼ 50:1% that of our proposed accelerator when implemented on a device with similar resource, i.e., XC485T FPGA. Moreover, it only accelerated the CNN computation, while the post-processing was conducted on the CPU. However, the previous works [11,32] show that the post-processing is crucial for the total latency of the detection.

We also evaluate the power efficiency of the accelerators with different technologies. It can be found that the ASIC-based accelerator Intel NCS2 achieved the highest power efficiency, because the hardware architecture of the ASIC-based accelerator has been carefully optimized. Compared to our implementation on 325T FPGA, the work in ISCAS2021 [4] achieved higher power efficiency. This is because the streaming accelerator has a low DDR access frequency, which reduces the power consumption of the DDR access.

Despite the improvements achieved by our proposed design, there are still some limitations that constrain further performance enhancement. For instance, when the batch size is equal to one, the throughput of the accelerator applied to the XC690T device is only 1.25 times greater than that of the XC325T device, while DSP utilization is only 25%. This limitation can be attributed to two main factors. First, as the degree of parallelism increases, more hardware resources are required. This results in an increase in difficult in FPGA's place and routing and a subsequent reduction in the operating frequency of the accelerator. For example, the parameters of the accelerator on the 690T were increased from Nm ¼ 12 to Nm ¼ 16, the operating frequency decreased from 200MHz to 180 MHz. Secondly, as shown in Figs. 18 and19, performance is limited by the bandwidth of external memory when performing 1 Â 1 convolution. As such, further improvement in throughput can only be achieved by increasing the batch size to enhance computational intensity.

## 6. Conclusion

This paper presents an efficient FPGA accelerator design for YOLO series detection algorithms. The design utilizes multiple dimensions of parallelism to accelerate the convolution layers of the network model, and employs multiport parallel line-buffer-like on-chip data cache to minimize the external memory bandwidth utilization, resulting in improved detection performance when compared to state-of-the-art FPGA accelerators. Moreover, the postprocessing algorithms of the YOLO models are implemented by dedicated hardware circuits in the proposed accelerator, which significantly reduced the end-to-end detection latency when compared to GPU and CPU-based implementation approaches. The combination of algorithm and hardware optimization enabled the accelerator to achieve a 4Â of throughput when implementing the same YOLOv2 algorithm on a low-end 325T FPGA and achieves a throughput of 859 GOPs/s when implementing YOLOv3 on Xilinx 690T FPGA.

In future work, we plan to utilize more advanced schemes to quantize the convolution with even lower bit width, such as 4-bit or 2-bit quantization, to further reduce the hardware resource cost and the bandwidth utilization. We also plan to implement other object detectors, such as faster-RCNN and FPN, to further evaluate the efficiency of the proposed design for two-stage-based detection algorithms.

## Figures et tableaux

lllFig. 1 Fig. 1 Architecture of the YOLO network

**Fig. 2** Distribution of the location and category data. a The distribution of the location data. b The distribution of the category data

**Fig. 3** Architecture of the accelerator

**Fig. 4** DSP efficient PE design. a The architecture of a PE. b The procedure of the packed multiplication. c Mapping the packed multiplication into a DSP48E1

**Fig. 6** Output buffer design. Every L CU clocks, a total of N r Â N m Â N b outputs are generated. The output buffer caches them and writes them back to the external memory sequentially

**Fig. 9** Work flow of the post-processing Fig. 10 Location decoding unit

**Fig. 11** Fig. 12 Fig. 11 Softmax unit

**Fig. 13** Selection of D f and N r . a The correlation between external memory access and D f . b The external memory access and speed gain for different N r

**Fig. 14** Resource consumption estimation. The target device is Xilinx V7-690T and the other parameters are N r ¼ 13 D f ¼ 8192. a Logic resource. b Block RAMs. c DSP blocks. d Inference latency

**Fig. 15** Roofline models for the two schemes, where the estimated throughput correlates with the batch size from 1 to 8 is shown. a Scheme-A. b Scheme-B

**Fig. 17** Work flow of the accelerator design

18Fig. 19 Fig. 19 Theoretical and actual execution time of each layer of the YOLOv3 algorithm on the VOC data set (N n ¼ 8; N m ¼ 16; N r ¼ 13)

**Fig. 20** Breakdown hardware resource of the accelerator with N n ¼ 8, N m ¼ 8, N r ¼ 13, and N b ¼ 1. a LUT consumption, b BRAM consumption, c DSP consumption

**Table 1** Abbreviations

    Symbol | Description
    B | Word length of the fixed-point number
    fl | Fractional length of the fixed-point number
    N r | Number of CUs within one PE array
    N p | Number of PEs within one CU
    N n Â 2 | Number of MACs performed by one PE in parallel
    N b | Number of PE arrays

**Table 2** Performance and resource consumption of the post-processing unit

     | LUTs | DSP | BRAM | Latency
     |  |  | (18k) | (845 boxes)
    Coordinates decode | 3173 | 16 | 5 | -
    Score calculation | 1343 | 0 | 2 | -
    NMS unit | 1773 | 3 | 2 | -
    Misc unit | 2604 | 0 | 11.5 | -
    Total | 8893 | 19 | 20.5 | 0.38 ms

**Table 3** Comparison with state-of-the-art YOLOv2 and YOLOv2-Tiny implementations on FPGA

     | ISCAS2021 [4] NCAA2022 [9] Ours | Ours | Ours | Ours | Ours
    Benchmark model | YOLOv2-Tiny | YOLOv2 | YOLOv2-Tiny YOLOv2 | YOLOv2-Tiny YOLOv2 | YOLOv2
    Dataset | KITTI | VOC | VOC | VOC | VOC | VOC | VOC
    MAP | 77.1 | 75 | 53.5 | 76.7 | 53.5 | 76.7 | 76.7
    Quantization (bits) | 8 | 8 | 8 | 8 | 8 | 8 | 8
    FPGA device | XC7Z045 | ZU7EV | XC7K325T | XC7K325T XC7VX690T | XC7VX690T XC7VX690T
    Technology (nm) | 28 | 16 | 28 | 28 | 28 | 28 | 28
    LUTs (K) | 84/218 | 91.17/230 | 134.9/203 | 134.9/203 | 153.4/433 | 153.4/433 | 212.4/433
    DSP Blocks | 610/900 | 387/1728 | 687/840 | 687/840 | 897/3600 | 897/3600 | 1737/3600
    Block RAM 18K | 512/1090 | 461/624 | 551/890 | 551/890 | 627/2940 | 627/2940 | 799/2940
    Frequency (MHz) | 200 | 200 | 200 | 200 | 180 | 180 | 160
    Batch size | 1 | 1 | 1 | 1 | 1 | 1 | 2
    Throughput (GOP/S) | 464.5 | 100.3 | 406 | 418 | 492 | 525 | 914
    On-chip power (W) | - | 4.8 | 7.8 | 7.8 | 8.3 | 8.3 | 12.5
    Total power (W) | 10.2 | - | 12.3 | 12.3 | 19.8 | 19.8 | 24.1
    Efficiency (GOPs/W) -/45.5 | 20.9/- | 52.1/33.0 | 53.6/33.9 | 58.8/24.8 | 62.7/26.5 | 72.7/37.9

**Table 4** Comparison with state-of-the-art YOLOv3-related implementations on FPGA

     | VLSI2022 [28] ISCAS2020 [6] Ours | Ours | Ours | Ours | Ours
    Benchmark model | YOLOv3-Tiny | YOLOv3-Tiny | YOLOv3-Tiny YOLOv3 | YOLOv3-Tiny YOLOv3 | YOLOv3
    Dataset | ILSVRC2015 | - | VOC | VOC | VOC | VOC | VOC
    MAP | 73.1 | - | 58.1 | 75.4 | 58.1 | 75.4 | 75.4
    Quantization (bits) | 8 | 18 | 8 | 8 | 8 | 8 | 8
    FPGA device | XCZU7EV | XC7VX485T | XC7K325T | XC7K325T XC7VX690T | XC7VX690T XC7VX690T
    Technology (nm) | 16 | 28 | 28 | 28 | 28 | 28 | 28
    LUTs (K) | 123/230 | 48.5/303 | 136.5/203 | 136.5/203 | 154.6/433 | 154.6/433 | 213.2/433
    DSP blocks | 146/1728 | 2304/2800 | 687/840 | 687/840 | 897/3600 | 897/3600 | 1737/3600
    Block RAM 18K | 326/624 | 141/2060 | 553/890 | 553/890 | 631/2940 | 631/2940 | 801/2940
    Frequency (MHz) | 200 | 200 | 200 | 200 | 180 | 180 | 160
    Batch size | 8 | 1 | 1 | 1 | 1 | 1 | 2
    Throughput (GOP/S) | 348.0 | 460 | 401 | 409 | 491 | 501 | 859
    On-chip power(W) | 3.3 | 4.8 | 7.8 | 7.8 | 8.42 | 8.42 | 12.61
    Total power (W) | - | - | 12.3 | 12.3 | 19.8 | 19.8 | 24.5
    Efficiency (GOPs/W) 105.4/- | 95.6/- | 51.4/32.6 | 52.4/33.2 | 58.0/24.7 | 59.5/25.3 | 68.1/35.0

**Table 5** Performance evaluation between alternatives

    Work | ACCESS 2021 [33] | ACCESS 2021 [33] | DSD2022 [31] | TCAD2020 [7] | Ours
    Device | Intel NCS | Jetson nano | Intel GX1150 | ZC706 | Xilinx 325T
    Architecture | ASIC | ARM?GPU | FPGA | ARM?FPGA | FPGA
    Network | YOLOv3-Tiny | YOLOv3-Tiny | YOLOv3-Tiny | YOLO-Tiny | YOLOv3-Tiny
    Resolution | 448 | 448 | - | - | 416
    Workload (GOP) | 10.1 | 10.1 | 5.56 | - | 5.7
    Precision | FP16 | FP32 | FP32 | INT16 | INT8
    Frequency | 700 | 1300 | 200 | 166 | 200
    Power | 1 | 10 | - | 9.4 | 7.8/12.3
    Technology (nm) | - | - | 20 | 28 | 28
    Latency (ms) | 55 | 40 | 27.5 | - | 15.2
    Throughput (GOP/s) | 183.6 | 252.5 | 202 | 201 | 401
    Efficiency (GOP/W) | -/183.6 | -/25.25 | -/- | 21.4 | 52.2/33.0
