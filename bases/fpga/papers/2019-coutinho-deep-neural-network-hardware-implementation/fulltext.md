---
id: 2019-coutinho-deep-neural-network-hardware-implementation
title: "Deep Neural Network Hardware Implementation Based on Stacked Sparse Autoencoder"
year: 2019
backend: grobid
---

## Abstract

Deep learning techniques have been gaining prominence in the research world in the past years; however, the deep learning algorithms have high computational cost, making them hard to be used to several commercial applications. On the other hand, new alternatives have been studied and some methodologies focusing on accelerating complex algorithms including those based on reconfigurable hardware has been showing significant results. Therefore, the objective of this paper is to propose a neural network hardware implementation to be used in deep learning applications. The implementation was developed on a fieldprogrammable gate array (FPGA) and supports deep neural network (DNN) trained with the stacked sparse autoencoder (SSAE) technique. In order to allow DNNs with several inputs and layers on the FPGA, the systolic array technique was used in the entire architecture. Details regarding the designed implementation were evidenced, as well as the hardware area occupation and the processing time for two different implementations. The results showed that both implementations achieved high throughput enabling deep learning techniques to be applied for problems with large data amounts.

## I. INTRODUCTION

The use of Artificial Intelligence (AI) techniques for solving problems in several areas, such as Deep Learning (DL), also called Deep Neural Networks (DNN), have been gaining a great deal of attention in recent years. The DNNs are able to prove high computational power, concomitantly with the use of several hidden layers. Among the various Deep Learning techniques found in the literature, those ones based on Autoencoders (AEs) are mainly applied to prediction and classification problems [1]- [3].

The methodology of using multiple stacked autoencoders, forming a single DNN has proved to be effective in the training of deep learning networks, as can be seen in [4], [5]. Stacked Sparse Autoencoders (SSAE) have been used in classification problems as can be seen in [5]. In this approach, each hidden layer is composed of an individually trained sparse autoencoder, in an unsupervised way. The output of each hidden layer of each AE is used as input to the next AE, so that the input data characteristics are propagated through the network layer by layer, enabling the output The associate editor coordinating the review of this manuscript and approving it for publication was Fan Zhang. layer to perform the data classification, after a supervised training.

However, deep neural networks have a high computational complexity due to the large number of hidden layers, which makes it difficult or impossible to apply this approach in several commercial applications. This problem is further aggravated by applying this technique in problem with large data amounts. With that in mind, several researches aiming the acceleration of complex algorithms have been conducted, and among them the use of reconfigurable computing have proved to be a great option.

The present paper is organized as follows: This first section presented a general introduction about the work explaining the motivation behind it. Section II discusses some related works and the state of the art. In Section III will be presented a theoretical foundation regarding the deep learning techniques, evidencing the Stacked Sparse Autoencoder. Section IV presents the hardware architecture details for the feedforward phase of two implementation. Section V will present the results of the proposed hardware validation and synthesis results, as well as comparisons with a state-of-theart work. Finally, Section VI will present the final considerations regarding the obtained results.

## II. RELATED WORKS

It is possible to find in the literature a great variety of works containing hardware implementations of artificial intelligence algorithms. As in the works developed in [6]- [9], in which it was possible to achieve high speed gains with the use of Field Programmable Gate Array (FPGA) reconfigurable computing, comparing to implementations using graphics processing units (GPUs) and general purpose processors used in High Performance Computers (HPC).

In [6] a hardware Radial Base Functios (RBF) Artificial Neural Network (ANN) was implemented and trained with the Least Mean Square (LMS) algorithm. The architecture implemented in Register-transfer level (RTL) was analyzed in terms of hardware occupancy rate, bit resolution and processing delay. The synthesis results for two distinct scenarios and several fixed point resolutions suggest the possibility of using the design in more complex practical situations. In the work of [7]- [9] a FPGA parallel implementation of genetic algorithm was proposed. The architecture was also implemented in RTL and performed tests with different parameters. The functions used by the genetic algorithm were stored in Lookup Tables (LUTs), thus eliminating the need for a dedicated circuit to perform each function and, consequently, enabling the reduction of area occupied in the FPGA, making the implementation more flexible. That approach resulted in a throughput increase, since building a complex circuit for these functions would produce longer hardware critical paths.

Some work involving implementations of DL techniques in FPGA motivated the development of this work. In the work of [10] it was proposed the implementation of a Convolutional Neural Network (CNN) in FPGA using fixed point. The circuit was built using the Vivado HLS tool. The hardware implementation, using a FPGA Virtex 7, managed to operate approximately 16.42 times faster than a CNN implemented in Matlab. Another proposal for the implementation of a CNN in FPGA is presented in [11] which also used high-level synthesis (HLS). Experiments showed that the FPGA implementation achieved up to 3× more energy efficiency than a CPU implementation, and a energy efficiency equivalent to the same CPU implementation with 16 threads operating in parallel. In addition, in respect to the implementation in SoC GPU for mobile applications, it was possible to obtain a gain of almost 15× in terms of speed and 16× in terms of energy efficiency. In [12] is proposed an optimized implementation to accelerate the CNNs on FPGA. For this, an analytical design scheme was adopted using the roofline model. However, the hardware implementation was developed using HLS. The CNN implemented had as target a Virtex 7 FPGA, and it obtained a speedup of 17.42× over the Intel Xeon 2.2 GHz Microprocessor.

The work [13] presented the effects of using data representation with limited precision in neural network training. The results showed that using stochastic rounding with a resolution of 16 bits fixed-point, it was possible to obtain a similar performance to the 32 bits in floating point. The work used the systolic matrix strategy to build multiplier arrays, thus contributing to the implementation throughput increase. Aiming the use of reconfigurable computing, [14] proposed a deep learning accelerator unit on FPGA, called DLAU. The proposed architecture was split into three processing units using a pipeline scheme and it can be applied to different network topologies. The hardware was developed using the Xilinx Zynq Zedboard development platform which features an ARM Cortex-A9 processor. Experiments showed that the DLAU achieved a speedup of 36.1× over Intel Core 2 2.3 GHz processors, in addition to achieving low power consumption compared to implementing an NVIDIA Tesla K40c GPU.

The systolic array has been studied for designing deep learning accelerators in recent years, for to reduce the area and power of the large matrix multiply unit [15], as also, to achieve high throughput [16]. The systolic array can provide low global data transfer and high clock frequency which is suitable for large-scale parallel design on FPGAs [16].

In [17] a DNN implementation in FPGA was proposed using VHSIC Hardware Description Language (VHDL) and floating point which enabled the use of a single layer of physical computation to execute the entire network feedforward step. Synthesis were performed for several network architectures and the largest ones supported by each hardware used in the experiments were identified. The Xilinx Virtex-5 XC5VLX-110T FPGA was able to fit the 784 -40 -40 -40 -10 architecture, whereas the Xilinx ZynQ-7000 XC7Z045 FPGA could fit the 784 -126 -126 -126 -10 architecture. However, it was observed that with the 784 -40 -40 -10 and 784 -126 -126 -10 architectures, the best results were obtained in terms of recognition rate and processing time, reaching the maximum performance of 15810 and 15900 manuscript digits frames (from the MNIST database) per second, respectively. In the work of [18] an RTL compiler was proposed to accelerate FPGA Deep Learning algorithms that aimed to achieve similar performance to the implementations in RTL, since implementations that used high-level synthesis could not optimize the FPGA resources consumption.

Using Verilog, [19] implemented a Convolutional autoencoder (CAE) network in FPGA, which represents a type of CNN. The FPGA implementation was validated by running image compression algorithms. Comparisons with other hardware implementation such as CPU and GPU implementations were carried out. The speed comparison pointed that the FPGA was faster than the CPU and slower than the GPU. However, with regard to performance per watt the FPGA scored significantly higher than both others.

One of the first DNN implementations in FPGA using Stacked Sparse Autoencoders is presented in [5]. DNN was used to perform image classification of the data set called CIFAR-10. The network architecture used two hidden layers, containing 2000 neurons in the first hidden layer and 750 in the second one, in addition to 3072 inputs and 10 neurons in the output layer, called 3072 -2000 -750 -10 architecture. For the implementation, a high-level synthesis OpenCL framework was applied, which might have contributed for the FPGA results being inferior in processing efficiency when compared to the GPU implementation. In [20], the advantages of using fixed point in autoencoder implementations are shown, considering that using a 4 bits resolution in the integer part, it was possible to obtain the same accuracy of using floating point. For the experiments, the 784 -400 -10 network architecture and the MNIST database were used. However, no information was presented regarding the FPGA hardware resources occupancy rate and processing time.

In [21]- [23], proposals for traditional neural networks using autoencoders were presented. In [21] a sparse autoencoder architecture was implemented in VerilogHDL. The tests were carried out with a 196 -100 -196 network architecture using the natural image data set of the Kyoto city in Japan. In [22], it was proposed, in addition to the traditional autoencoders architectures, a structure with two chained autoencoders, the 4 -2 -1 -2 -4 architecture, however, it aimed to rebuild the input in the output, as in the conventional models. In this work, unlike the ones previously mentioned which implemented autoencoders techniques as well, the circuit was implemented in RTL, which allowed it to achieve superior efficiency comparing to the other autoencoder implementations mentioned here. The target FPGA was a Xilinx Virtex-6 xc6vlx240t.

Similar to the work structure showed in [22], in [23], autoencoders were used to implement the 32-16-8-16-32 architecture. However, in this work the Xilinx Vivado HLS tool was used to perform the synthesis from the C language to RTL. A Xilinx Kintex-7 xc7k410tffg900-2 FPGA was used for the experiments. The implementation was able to achieve high throughput (about 200 Mega samples per second (MSPS)) and low latency (about 105 ns). However, it was observed that most of the FPGA hardware resources were occupied, which makes impracticable to design a network architecture larger than the one implemented.

In order to guarantee the FPGA implementation efficiency, through the optimum usage of resources, the implementation proposed in the present work was constructed in RTL, unlike [5]. The RTL implementation was also adopted in [22], however, in that work it was implemented autoencoders structures that were more similar to traditional ones than to DNNs. Thus, the present paper presents a hardware implementation proposal of a Deep Neural Network based on the Stacked Sparse Autoencoder technique. The hardware was developed for the feedforward phase adopting the systolic array technique, which allowed the use of multiple neurons and several layers. Data regarding hardware occupancy rate and processing time will be presented for a Virtex 6 XC6VLX240T-1FF1156 FPGA.

## III. DEEP LEARNING

In the last years, several Deep Learning techniques have become the object of research of many academic works around the world. These techniques can be defined as a modernization of Multilayer Perceptron (MLP) networks, considering that one of the main differences between MLP networks and DNNs is the feasibility of the DNNs to train networks with numerous hidden layers, which is a major problem in conventional MLPs.

The term autoencoder precedes the Deep Learning advent. In its traditional structure, autoencoders were mainly applied to dimensionality reduction and patterns learning problems. In these networks the training occurs so that the output layer provides a reconstruction of the input layer, thus, both layers have the same size. At the same time, only one hidden layer is used and performs the characteristics extraction of the input data. Consequently, the autoencoder architecture is composed of three layers: an input, a hidden and an output. The input and hidden layers form the network encoder while the hidden and output layers make up the decoder [24]. The autoencoders have been used in many unsupervised learning problems where it is possible to represent a P-dimensional input vector (from input layer) in an M -dimensional vector (from output hidden layer), where M < P. In other words, the autoencoders can reduce the dimensionality of the input by extracting the essential information (hidden layer output). With autoencoders, it is also possible to recover the input information using the neurons of the output layer. Basically, the neurons of the hidden layer reduce the input information and the neurons of the output layer recover that information [25].

### A. STACKED SPARSE AUTOENCODER (SSAE)

With the Deep Learning ascent, the autoencoders began to be used in a chained fashion, forming networks with numerous hidden layers, whose training was previously performed in each autoencoder in an unsupervised way. Among the autoencoder types the sparse are known for being heavily applied to classification problems. In the stacked sparse autoencoders, each hidden layer is composed of the hidden layer of an individually trained sparse autoencoder. Each sparse autoencoder receives as input the output of the hidden layer of the previous sparse autoencoder so that the characteristics of the input data are extracted along the network hidden layers, enabling the output layer to perform the classification after the supervised training. In this work, the network training was performed using this methodology. Figure 1 presents the proposed SSAE architecture with an input layer (P data inputs), two hidden layers (M and N inputs) and an output layer (H outputs). This architecture can be represented as a

P -M -N -H SSAE.

This work is focused on implementing the SSAE feedforward phase, in which the equation that defines the output of the i-th neuron from the k-th layer, z k i (n), at the n-th instant, can be expressed as

z k i (n) = U l j=1 w k ij (n) × y l j (n) + wb k i (n) × b (1)

where w k ij (n) is the weight associated with the j-th input of the i-th neuron in the k-th layer at the n-th instant, y l j (n) is the j-th input of the l-th layer, in which l = k -1, at the n-th instant, wb k i (n) is the bias weight of the i-th neuron from the k-th layer at the n-th instant, b is the bias, which has a value of 1, and U l is the number of inputs of the l-th layer, where

U 0 = P, U 1 = M e U 2 = N .

In the hidden layers the sigmoid activation function was used, so the output associated with the i-th neuron from the k-th layer at the n-th instant, v k i (n), can be expressed as

v k i (n) = 1 1 + e -z k i (n)(2)

in which v k i (n) will be the value of the j-th input to be used in the next layer at the n-th instant, y l+1 j (n), that is

y l+1 j (n) = v k i (n)(3)

in which j = i. The softmax activation function was used in the output layer. This function has been adopted in neural classification networks as presented in [5], and can be characterized as

s i (n) = e z K i (n) H h=1 e z K h (n)(4)

in which s i (n) consists of the i-th output of the last layer K with H neurons at the n-th instant. The H value is determined by the number of classes of the problem, since this function indicates the probability that each data belongs to a specific class.

## IV. IMPLEMENTATION DESCRIPTION

In this work, two SSAE proposals were implemented for the feedforward phase using the systolic array technique. The main difference between them is in the way the network's synaptic weights are inserted into the hardware. In the following sections characteristics of each proposal will be present, as well as the details regarding the processing time of each implementation.

### A. PROPOSAL 1

Based on the network structure detailed in Figure 1, the overall architecture of the first implementation proposed in this work is presented in Figure 2. This architecture is able to receive the network weights through weights streams, without the need of using memory resources to store them, unlike most implementations found in the literature [5], [22], [23].

The variables and constants of the implementation are represented in fixed point and for each j-th entry, y 0 j (n), 1 bit is used in the integer part (without signal) and 12 bits in the decimal part, as the inputs are normalized between 0 and 1. For the synaptic weights of neurons from hidden layers, one and two, expressed as w 1 ij (n) and w 2 ij (n), as well as for the bias weights of all layers, wb k i (n), 5 bits are used in the integer part (one bit for signal) and 12 bits in the decimal part. For the weights from the output layer neurons, w 3 ij (n), 7 bits are used in the integer part (one bit for signal) and 12 bits in the decimal part.

For this proposal implementation, the systolic array technique was used and it acts as an intermediary approach between a completely parallel and fully serial methodology. This technique allows data to be received serially and the processing elements (PEs) perform their operations in parallel [26]. The network implemented in this work used two hidden layers, consisting of the 784-100-50-10 architecture. However, to add more hidden layers to the network it is necessary to replicate the inner block present in Figure 2, which represents the second hidden layer of the network. Another small adjust is necessary in order to set each layer with the amount of desired neurons.

### 1) SSAE LAYERS

The architecture of the k-th hidden layer, called k autoencoder in Figure 2, is presented in Figure 3 and it implements the systolic array technique. Each neuron of the k-th layer is represented by a i-th PE k i and the amount of PEs is defined by the value of V k , where V 1 = M , V 2 = N and V 3 = H . Thus, each i-th PE k i implements the Equation 1. The values computed in each i-th PE k i from the k-th hidden layer pass through an activation function, called here AF k (see Equation 2), and are used as input to the next layer (see Equation 3).

The values computed in the output layer PEs go through the activation function defined in Equation 4 in order to generate the network output. The sel signal corresponds to the multiplexer selector, Mux k , used to select the outputs of each i-th PE k i for the k-th layer input activation function, AF k .

Through the systolic array, the inputs values flow between the PEs so that each PE starts its operations at the instant following the beginning of the operations of its preceding PE, causing these modules to operate in parallel. It is worth mentioning that it is from the second hidden layer, that is, when k > 1, that the bias, b, and the bias weights, wb k i (n), are inserted as input of the k-th layer, as per the structure shown in Figure 2. Only in the first hidden layer, that is, when k = 1, these values are inserted together with the network inputs and the weights of the neurons layer, respectively. An advantage of this first proposal is the insertion of the weights from each layer in a serial way through a single weight stream in the first hidden layer and two weights streams in the other network layers. This would be the least amount of weight streams required for the operation of this implementation, however, this architecture is easily scalable, which allow the weight streams parallelization for each layer. The amount of weight streams per layer may range from one to the amount of neurons in the layer, V 1 , in the first network hidden layer, and from 2 up to 2 × V k , in the others network layers, due to bias weights.

It is worth mentioning that the possibility of receiving the weights by streams allows the use of the same hardware for different problems, since the weights trained for a different problem can be inserted in the network, as well as the inputs of the problem in question, without the need to reconfigure the hardware.

### 2) PROCESSING ELEMENTS (PEs)

The architecture of the first hidden layer PEs differs from the PE architecture of the other layers. In the first hidden layer, the bias, b, and the bias weights, wb 1 i (n), are inserted along with the network inputs and the neurons synaptic weights in the layer, respectively. Thus, the architecture of each i-th PE 1 i from proposal 1 is detailed in Figure 4 and it's formed by a multiplier, an adder and four registers, R. The architecture of each i-th PE k i , for k > 1, from proposal 1, is detailed in Figure 5 and it's formed by two multipliers, two adders and six registers, R. Each i-th PE k i generates an output after Z samples, where for the first hidden layer, Z = P and for the others, the Z variable must be greater than or equal to the number of entries (Z ≥ P) and multiple of the number of neurons of the first hidden layer (mod(Z , M ) = 0).

### 3) ACTIVATION FUNCTIONS (AFs)

The implementation of each k-th activation function, AF k , was designed using Lookup Tables (LUTs) as shown in Figure 6, which allows the approximation of functions through a L-values table. In order to implement the activation function of each hidden layer (Equation 2), ROM memories with 16 bits of depth were used, in which L = 2 16 , storing words of 13 bits. For the implementation of the activation function from the output layer, the softmax, defined by Equation 4, a LUT was used to approximate the exponential function, only then the Equation 4 division was performed. The output layer LUT, AF 3 , was set to a depth of L = 2 16 , storing 57 bits.

An important fact associated with this implementation strategy is the use of a single activation function only, or LUT, per layer. This feature significantly reduces the space occupied in the FPGA (see [6]).

### 4) PROCESSING TIME

In proposal 1, a ring counter in each k-th layer, as shown in Figure 3, is used to enable receipt of the weights in each i-th PE k i from the k-th layer. Since the least amount of weight streams per layer is being used, the operation of the k-th layer's ring counter must be V k times faster than the operation of each PE k i . In order to maintain the implementation timing, V k > V k+1 is considered. Thus, the execution time of each PE circuit is determined by the ring counter run-time of the first hidden layer, t rc . Therefore, the PE time, t PE , can be defined as

t PE = (V 1 × t rc )(5)

where (V 1 × t rc ) ≥ t c and t c is the system critical path time. The proposed architecture has an initial delay that can be expressed as (6) in which Q represents the initial delay of the first layer, and it is a number greater than or equal to the number of neural network inputs (Q ≥ P) and a multiple of the number of neurons from the first hidden layer (mod(Q, M ) = 0). As the first layer is greater than other layers (

d = (Q × K + D) × t PE

V 1 > V 2 > . . . > V K -1 > V K

), the variable Q can be used to estimate the delay for all layers. K is the number of network layers with neurons and, D is the delay in number of samples which is a result of the hidden and output layers activation functions. The neural network throughput, th ff , in frames per second (FPS) or in inputs per second (IPS) can be expressed as

th ff = 1 Q × t PE .(7)

It is important to mention that the throughput achieved is independent from the number of layers of the network, as it only depends on the amount of inputs and neurons used in the first hidden layer. The amount of layers with neurons, K , will only impact in the system initial delay.

Based on Equation 7, the execution time of the proposed SSAE, called here as feedforward time, t ff , after the initial delay of d seconds (Equation 6), can be expressed as

t ff = Q × t PE = 1 th ff (8)

thus, in every t ff , it is possible to obtain the output of all the H neurons from the last layer, that is, the network output for a given input.

### B. PROPOSAL 2

The general architecture of the second proposal is presented in Figure 7 and it is based on the structure shown in Figure 1.

The main differences regarding the first proposal are related to the way in which the synaptic weights are inserted into the network. In this second proposal, the weight values are stored in ROM memories and they are no longer received serially as in the first implementation. The project variables and constants are represented in fixed point, using the bit resolutions presented in Subsection IV-A, for proposal 1.

### 1) SSAE LAYER

The Figure 3 presents the general architecture of the k-th hidden layer, called k autoencoder (Figure 2). In this second proposal, there are no streams for the synaptic weights, since these values are stored in LUTs using ROM memories. This is possible since the network training has been previously finished, thus there is no need to change the weights once the network has already been trained for a specific problem. However, in the need to use the network for a new problem, the hardware must be reconfigured, storing the new weights, obtained after the previous network training for the new problem in the lookup tables.

### 2) PROCESSING ELEMENTS (PEs)

In this proposal, the PEs architecture from the first hidden layer differs from the PE architecture from the other layers.

The architecture of each i-th PE 1 i of proposal 2 is detailed in Figure 9 and consists of a multiplier, an adder, four registers, R, and a LUT used to store the weights of the i-th

PE 1 i , called W 1 i . The architecture of each i-th PE k i , for k > 1 FIGURE 7. General architecture of proposal 2.

from proposal 2, is detailed in Figure 10 and consists of two multipliers, two adders, six registers, R, one LUT used to store the weights of the i-th PE k i , called the W k i , and a constant for the bias weight, wb k i . Each i-th PE k i generates an output after Z samples, as shown in Subsection IV-A2 from the proposal 1. The LUTs of each PE k i and W k i , use a ROM memory with a depth of L = Z , storing words of 17 bits in the hidden layers, and 19 bits in the output layer. In addition, the constants used for the bias weight of each i-th neuron, wb k i , were configured with 5 bits in the integer part (using one for signal) and 12 bits in the decimal part.

### 3) ACTIVATION FUNCTIONS (AFs)

The implementation of each k-th activation function, AF k , from the hidden layers as well as the activation function of the output layer of proposal 2 corresponds to what was already presented for proposal 1 in Subsection IV-A3.

### 4) PROCESSING TIME

In this second proposal, the PE execution time corresponds to the system critical path time, t c , i.e.

t PE = t c .(9)

However, the other equations from subsection IV-A4 can be considered for the processing time calculation from proposal 2, taking into account the Equation 9. The initial delay, d, can be defined by Equation 6. In addition, the throughput, th ff , can be expressed by Equation 7, as well as the execution time of the SSAE, t ff , can be expressed by Equation 8. can be expressed as

## V. RESULTS

### A. HARDWARE OCCUPATION ANALYSIS

n PE = n 1 PE + n k≥2 PE = n 1 PE + K k=2 n k PE = V 1 + K k=2 V k (12)

where n k PE is the number of PEs in the k-th layer and the total of logic cells, n LC , is expressed as The regression analysis is not necessary for the multipliers, and the equations can be expressed as

n LC = n 1 LC + n k≥2 LC = n 1 LC + K k=2 n k LC .(13)

n 1 Mult = n 1 PE ,(14)

n k≥2 Mult = 2n k≥2 PE ,(15)

and

n Mult = n 1 Mult + n k≥2 Mult = n 1 Mult + 2 K k=2 n k Mult (16

)

where the n k Mult is the number of multipliers in the k-th layer. The hardware occupation results concerning proposal 2 are presented in Table 2, and the regression analysis for the first and others layers are illustrated in Figures 11 and12, respectively. The regression analysis equations for logic cells can be expressed as

n 1 LC = 133.8n 1 PE + 34.17(17)

and

n k≥2 LC = 191.7n k≥2 PE + 129.1 .(18)

The multipliers occupation can be described by Equations 14, 15 and 16.

It is essential to observe that in Equations 10, 11, 17 and 18, it was considered that the maximum number of DSP multipliers was sufficient for all PEs (n max Mult ≥ n Mult ); otherwise (n Mult > n max Mult ), the Equations 10 and 11 could be rewritten as

n 1 LC = (212.2 + N LCM )α 1 + 212.2n 1 max Mult (19

)

and

n k≥2 LC = (285.1 + 2N LCM )α k≥2 + 285.1 n k≥2 max Mult 2(20)

where

α 1 = n 1 PE -n 1 max Mult (21

)

FIGURE Linear regression curve for the hardware occupation (logic cells) per PE for proposal 2 in the other layers, n k LC (k ≥ 2).

and

α k≥2 = n k≥2 PE - n k≥2 max Mult 2 (22

)

where the N LCM represents the number of logic cells needed to build a multiplier. The n 1 max Mult and n k≥2 max Mult are the maximum numbers of the DSP multiplier used in first and other layers, respectively.

Following the same idea, Equations 17 and 18 can be rewritten as

n 1 LC = (133.8 + N LCM )α 1 + β 1(23)

and

n k≥2 LC = (191.7 + 2N LCM )α k≥2 + β k≥2 (24

)

where

β 1 = 34.17 + 133.8n k 1max Mult (25

)

and

β k≥2 = 129.1 + 191.7 n k≥2 max Mult 2 . (26

)

Figures 15 and16 show the estimate number of PEs for some commercial FPGAs [27]- [29]. The estimation was based on Equations 10, 11, 19 and 20, for proposal 1, and Equations 17, 18, 23 and 24, for proposal 2. Based on Xilinx datasheet of the Multiplier IP Core [30], [31], the variable N LCM = 200. For all values, it was considered

n 1 PE = γ × n PE 100 (27

)

where γ is the percentage of the total number of PEs, n PE , (or neurons) in the first layer (k = 1). Table 3 shows the values of the maximum number of PEs, n max PE for each proposal. Figures 15 and16 show results for γ = 20% and Table 3 presented results for several values of γ .

The results from Figures 15 and16 and Table 3 show the proposal viability for real problems with several layers and neurons (each PE k i represents the i-th neuron associated with the k-th layer).

### B. TIME PROCESSING ANALYSIS 1) PROPOSAL 1 -TIME PROCESSING ANALYSIS

In the proposal 1 (see Figure 4), the weights are input streams per neural network layer, and this reduces the hardware memory needed to store the weights at the same time it reduces the throughput (see Equations 5 and 7). One way to address this drawback is by creating a parallelization in the weights streams per layer, that is,

t PE = (V 1 × t rc ) G = (n 1 PE × t rc ) G (28

)

where G is the parallelization degree of the weights streams, in other words, for the k-th layer, there are G group of PEs, called GPE, and each GPE has pr = V k /G PEs.

Figure 17 illustrates the parallelization of the weight stream where each g-th GPE k g drives a weight stream. The parallelization degree value is 1

≤ G ≤ n 1 PE and (n 1 PE × t rc ) G ≥ t c (29

)

which can be described as

G = n 1 PE -1 η + 1 = γ × n PE 100 -1 η + 1 (30

)

where 0 ≤ η ≤ 1.

Based on Equations 28 and 30, Equation 7 can be rewritten as

th ff = G Q × n 1 PE × t rc = γ ×n PE 100 -1 η + 1 Q × γ ×n PE 100 × t rc .(31)

The number of operations (adds and multipliers) per PE are 2 and 4 for the first (k = 1) and other (k ≥ 2) layers, respectively. Thus using Equation 28, the performance, for proposal 1, pf , in operations per seconds (OPS) can be expressed as

pf = G 2n 1 PE + 4n k≥2 PE n 1 PE × t rc . (32

)

Using Equations 12, 27, and 30, the Equation 32 can be rewritten as

pf = G (400 -2γ ) γ × t rc = γ ×n PE 100 -1 η+1 (400-2γ ) γ × t rc . (33

)

After several synthesis results (see Table 1), the median values of t rc and t c were about 10 ns and 12.31 ns, respectively. The system critical path time can be increased regarding the number of bits and other operations such as the softmax activation function (see Equation 4) in the last layer, however, as the number of PEs is high, the constraint presented in Equation 29 can be easily satisfied. Figures 18,19 and 20 show the throughput curve, th ff , in IPS, and performance, pf , in Giga OPS (GOPS) to several values of Q, G and η for n PE values presented in Table 3 with γ = 40%.

Figures 18 and19 show the throughput, th ff , with different values of η = {0,1/8,1/4,1/8} and it is possible to observe that the th ff decreases with Q for η = 0, however it is possible 3 with γ = 40%.

to compensate the reduction increasing η (or G). Figures 20 shows the performance of the proposal 1 for several values of η and, it could achieve more than 1000 GOPS or 1 tera OPS (TOPS) on FPGA 4 with η ≥ 0.3. Table 4 shows the values of the th ff in ×1000 IPS (KIPS), and pf illustrated in Figures 18, 19 and 20.

### 2) PROPOSAL 2 -TIME PROCESSING ANALYSIS

For proposal 2, the throughput, th ff , depends just on the system critical path time, t c , and using the Equations 7 and 9, the throughput, in IPS, can be expressed as 2, the t c achieved a median value of approximately 12 ns. However, the t c value can increase with the number of bits and the other circuit elements such the softmax activation function implementation (see Equation 4). It is interesting to notice that the value of t c is similar for the two proposals since the critical path of PE is similar for both. Similarly of proposal 1, the number of operations (adds and multipliers) per PE for proposal 2 are 2 and 4 for the first (k = 1) and other (k ≥ 2) layers, respectively. Thus using Equation 9, the performance, for proposal 2, pf , in operations per seconds (OPS) can be expressed as

th ff = 1 Q × t c . (34

)

pf = 2n 1 PE + 4n k≥2 PE t c .(35)

Using Equations 12, 27, and

n k≥2 PE = n PE - γ × n PE 100 ,(36)

Equation 35 can be rewritten as

pf = 4n PE -2n 1 PE t c = 4n PE -2 γ ×n PE 100 t c .(37)

Figure 22 shows the performance, pf , using several values of n PE and t c for some FPGAs.

### C. POWER CONSUMPTION ANALYSIS 1) PROPOSAL 1 -POWER CONSUMPTION

Figure 23 shows the surface of regression analysis using the measurement points presented in Table 6. equation obtained from regression analysis (R 2 = 0.9987) can be expressed as

P 1 PE = f PE 505 + 0.0592f PE + 10.65n 1 PE 1 × 10 6(38)

where P 1 PE is the dynamic power consumption in watts (W) of the first layer, and f PE is the frequency of PE in MHz, that is

f PE = 1 × 10 -6 t PE = G × 10 -6 n 1 PE × t rc .(39)

The dynamic power measurement for other layers (k ≥ 2) is presented in Table 7. For this case, the surface of regression analysis (R 2 = 0.9984) can be expressed as

P k≥2 PE = f PE 565.3 + 0.0429f PE + 12.39n k≥2 PE 1 × 10 6 .(40)

where P k≥2 PE is the dynamic power consumption in watts (W) for other layers (k ≥ 2). The Figure 24 shows the curve of regression analysis of dynamic power consumption, P k≥2 PE , per Using Equations 27 and 39, the dynamic power consumption, P 1 PE , for the first layer can be expressed as .

P 1 PE = G 505 + 0.0592G×10 -

Finally, the total of dynamic power consumption, P PE , is expressed as

P d = P 1 PE + P k≥2 PE .(43)

Figures 25 and26 show curves associated with power consumption using Equations 41, 42, and 43. Some curves values are presented in Table 8. All values were calculated with γ = 40%.

### 2) PROPOSAL 2 -POWER CONSUMPTION

Figures 27 and 28 show the surface of regression analysis using the measurement points presented in Tables 9 and10, respectively. The equation obtained from regression analysis (R 2 = 0.9964) for the first layer, P . (49)

Figure 29 shows the total dynamic power consumption per PEs, P d , using Equation 49 and Table 11 presented some values for FPGA1, FPGA2, FPGA3 and FPGA4.

### D. VALIDATION

In order to validate the implementation proposed in this article, a data set of manuscript digits called MNIST [32], containing 60000 images in the training set and 10000 images in the test set was used for the experiments. Each image contains 28 × 28 pixels, totaling 784 inputs for the SSAE. The SSAE implemented in this validation used two hidden layers, consisting of the 784-100-50-10 architecture. The experiments were performed with the 10000 images from the MNIST test set. The network training was previously performed using the 60000 images from the train set in the Matlab/Simulink [33] simulation platform (License number 1080073) with the scaled conjugate gradient (SCG) algorithm and the target FPGA was a Virtex 6 XC6VLX240T-1FF1156 [27]. Figure 30 shows the hardware setup for the experiments. It was used the Virtex-6 FPGA ML605 Evaluation Kit by Xilinx [34]. A video demonstration of the proposal 2 executing the MNIST test set is presented in [35].

### 1) PROPOSAL 1 VALIDATION

For the hardware validation, a comparison was made between the results obtained by the implementation on the Matlab/ Simulink platform and the results obtained by the hardware implementation. Thus, the mean square error (MSE) between the output of the Matlab implementation, s ref i (n), and the output of the hardware implementation was calculated. The MSE calculation for this experiment is defined as

MSE = 1 H × 10000 H i=1 10000 n=1 s ref i (n) -s i (n) 2 .(50)

It was found that the MSE between the implementation results in Matlab, which used floating point (64 bits), and the fixed-point hardware implementation was only 2.1 × 10 -6 , which is a fairly acceptable result, since the weights associated with the hardware implementation used only 12 bits in the decimal part. Among the 10000 images used in the validation, Matlab's hit percentage was 93.4%, while the proposed hardware implementation reached a 93.38% hit. The small percentage error in the classification of the implementation in FPGA comparing to the implementation in Matlab is related to the bit resolution used for the network synaptic weights. However, this result is still quite relevant since it indicates that a higher bit resolution (such as 64 bits, for example) is not required to achieve meaningful results, showing that by using only 12 bits in the decimal part, in a fixed point representation, it is possible to guarantee the reduction in the hardware occupation area, besides promoting the throughput increase [6], [20]. After the validation of the hardware implementation using Matlab, the synthesis was performed in order to obtain the FPGA resources allocation report. The Table 12 details the data related to the hardware area occupation of the circuit implemented in the FPGA. The first column shows the number of multipliers which are used mainly by the PEs of each kth layer. The second column displays the number of registers and the third column shows the amount of logic cells used throughout the circuit.

The data presented in Table 12 show the feasibility of the implementation of proposal 1. It turns out that only 16% of the target FPGA logic cells were occupied, indicating that there is still plenty of room to additional layers and neurons. One of the elements that were most used was the multipliers, around 29%, since each PE from the first layer utilizes one, and the PEs of the other layers consume two due to the bias. Despite this, it is noted that it is still possible to greatly increase the number of layers and neurons of the SSAE. The Table 13 presents information about the processing time of proposal 1, considering the least amount of required weight streams. The first column exposes the ring counter time for the first hidden network layer, t rc . The second column shows the architecture initial delay, d, defined by Equation 6. The third column presents the network feedforward execution time, t ff , expressed by Equation 8, after the initial delay (Equation 6), the fourth column shows the network throughput, th ff , determined by Equation 7, which in this particular experiment consists of the number of images classified per second and the last column shows the dynamic power consumption, P d , for this implementation.

### 2) PROPOSAL 2 VALIDATION

The hardware validation results with Matlab for proposal 1, presented in Section V-D1 for a Virtex FPGA 6 XC6VLX240T-1FF1156, also applies for proposal 2. However, new reports were obtained regarding the hardware resources occupation and the processing time, after the synthesis of the implementation of the second proposal.

Table 14 presents the synthesis data related to the FPGA occupation area from proposal 2. The columns of this table are organized according to what was already presented for Table 12 in the Subsection V-D1 for proposal 1.

The data presented in Table 14 show that the proposal 2 was able to further optimize the use of FPGA hardware resources comparing to proposal 1. This was possible due to the use of LUTs to store the synaptic weights in each i-th PE k i , dispensing with the implementation of some modules used in proposal 1. It can be seen that only 11% of the FPGA logic cells were occupied. The amount of multipliers used remained the same in relation to the previous proposal, around 29%, since there was no change in the way calculations were performed in each PE k i . Thus, the data presented for proposal 2 reaffirm the possibility of significantly increasing the number of layers and neurons of the network, indicating even better results than the previous proposal.

The Table 15 presents information about the circuit processing time for the second proposal. The first column exposes the PE processing time, t PE , and the other columns are organized according to what was presented to the table 13 in the subsection V-D1, referring the proposal 1.

The data presented in Table 15, for proposal 2, are quite expressive. The PE execution time achieved was only 48 ns, the initial delay, 0.1 ms, and the feedforward time achieved 0.03 ms. With this, it was possible to reach a throughput of 26000 classified images per second, which is a value approximately 20× higher than the value obtained in proposal 1, using the least possible amount of weight streams. In this way, it was verified that the use of LUTs to store the network neuron weights resulted in the throughput increase in comparison with the previous proposal. However, when using the maximum weights streams limit per layer, proposal 1 tends to reach the results of proposal 2. Thus, both proposals proved feasibility in massive data problems.

### E. STATE OF THE ART COMPARISON

From the results presented in the previous sections, this section is intended to make a comparison of the results obtained by the implementation of each proposal here presented with the results of works from the state of the art. Table 16 shows a comparison with works presented in [5] and [14]. In those works, it is possible to compare results associated with throughput, th ff , and power consumption, P d , for two different deep neural network size.

The related work presented in [5] proposes an SSAE FPGA implementation and it uses an equivalent FPGA in terms of processing for the validation. As presented in Table 16, the proposal 1 has speedup gains for the values of G ≥ 4, however implementation has an expressive power saving (about 1000×) for several values of G (1 ≤ G ≤ 8). When G increases, the speedup also increases (see Figures 18 and19) and the power saving decreases (see Figures 25 and26). Regarding the proposal 2, the speedup was about 116× over the architecture presented in [5] and the power saving was about 11×. The work presented [5] was implemented with the high-level synthesis OpenCL framework and, this method reduces the customization capacity implying a reduction in performance. In [14], the speedup was more expressive than the work presented in [5], between 31× and 251× for proposal 1 and about 1784× for proposal 2, however the power consumption was lower. It is interesting to observe that the power saving is greater for larger architectures, on the other hand the speedup is lower. The FPGA accelerator proposed in [14], called DLAU, computes just 32 neurons with 32 weights every clock cycle and the implementations here proposed can compute several neurons (or PEs) every clock cycle and which increases the performance when comparing with the DLAU.

Table 17 compares the performance results, pf , in GOPS with works presented in [36], [12], [13] and [37]. The proposals presented in [36] and [12] were implemented with HLS tools. In [36] was proposed an HLS engine called Caffeine and in [12] was proposed an implementations with Xilinx Vivado HLS. In [13] was presented the effects of the data precision in neural network implementations and in [37] was presented an application-specific integrated circuit (ASIC) proposal.

As presented in Table 17, the speedup is higher with respect to cases based on HLS, [36] and [12]. The proposal 1 achieved a speedup about 7.4× and 20.8× over works presented in [36] and [12], respectively and proposal 2 achieved a speedup about 4.11× and 11.5× over the same works. Finally, it is important to note that the implementations here proposed (proposal 1 and 2) presented a speedup even over ASIC implementations, as presented in [37].

## VI. CONCLUSION

This paper presented a hardware implementation proposal of the Stacked Sparse Autoencoder Deep Learning technique. The DNN feedforward phase was implemented using fixed point and design in RTL. Throughout the implementation the systolic array technique was applied, which allowed the use of many neurons in the various network layers, besides allowing the results to be obtained in a short processing time. All the implementation details were presented as well as results related to the syntheses for occupation and processing time of two distinct implementations targeting a FPGA Virtex 6 XC6VLX240T-1FF1156.

The results showed that both implementations could achieve high throughputs. Particularly, the use of LUTs to store the synaptic weights of each neuron in proposal 2 allowed the reduction of the area occupied in the FPGA, besides guaranteeing the increase of the throughput obtained, compared to the lower bound value of the proposal 1 throughput. In spite of that, the throughput value reached by proposal 1 could be increased in line with the increase in the number of weight streams per network layer and may tend to the throughput value obtained by proposal 2. On top of that, the proposal 1 allows, in practical applications, the same hardware to be used for different problems by enabling new weights to be added to the network through weight streams after previous network training. In addition, the comparison with related works also justified the feasibility of the proposed implementations, demonstrating the possibility of reaching high speedups. Finally, the results indicated the suitability of using this Deep Learning technique in massive data problems.

## Figures et tableaux

FIGURE 1. Proposed stacked sparse autoencoder architecture.

FIGURE 2. General architecture of proposal 1.

FIGURE 3. Architecture of the SSAE k-th hidden layer from proposal 1.

FIGURE 4. i -th PE 1 i architecture from proposal 1.

FIGURE 5. i -th PE k i architecture, for k > 1, from proposal 1.

FIGURE 6. k-th activation function, AF k , associated with the hidden layers.

FIGURE 12. Linear regression curve for the hardware occupation (logic cells) per PE for proposal 1 in the other layers, n k LC (k ≥ 2).

FIGURE 17. Architecture of the GPEs in the k-th hidden layer from proposal 1.

FIGURE 18. Throughput, th ff , (in IPS) for several values of Q and η for n PE values presented in Table3with γ = 40%.

FIGURE 19. Throughput, th ff , (in IPS) for several values of and G for n PE values presented in Table3with γ = 40%.

**Figure 21** shows the curves of the th ff for various values of Q and t c . Based on the values presented in Table2, the t c achieved a median value of approximately 12 ns. However, the t c value can increase with the number of bits and the other circuit elements such the softmax activation function implementation (see Equation4). It is interesting to notice that the value of t c is similar for the two proposals since the critical path of PE is similar for both.Similarly of proposal 1, the number of operations (adds and multipliers) per PE for proposal 2 are 2 and 4 for the first (k = 1) and other (k ≥ 2) layers, respectively. Thus using

FIGURE 22.TABLE 5. FIGURE 22. Proposal 2 performance, pf , (in GOPS) to several values of n PE and t c for some FPGAs. with γ = 40%.

FIGURE 25. Total dynamic power consumption, P d , per number of PEs, n PE , for several values of G of proposal 1 (γ = 40%).

FIGURE 26. Total dynamic power consumption, P d , per number of η for some FPGAs of proposal 1 (γ = 40%).

FIGURE 29.TABLE 11. FIGURE 29. Proposal 2 total dynamic power consumption, P d , (in watts) to several values of n PE and t c for some FPGAs with γ = 40%. TABLE 11. Values of the dynamic power consumption, P d , (in watts) shown in Figure 29 (γ = 40%).

FIGURE 30. Hardware setup for the experiments with the Xilinx Virtex-6 FPGA ML605 evaluation kit.

**TABLE 1.** Hardware occupation (logic cells and multipliers) per PE for proposal 1. [corps du tableau reconstruit par Docling : à vérifier]

    Layer | nPE | nLC | nMult
    First layer (n1 E) | 1 5 10 25 50 | 141 (0.06%) 853 (0.35%) 1664 (0.69%) 4200 (1.74%) 9397 (3.90%) 22162 (9.19%) | 1 (0.13%) 5 (0.65%) 10 (1.30%) 25 (3.26%) 50 (6.51%) 100 (13.02%)
    First layer (n1 E) | 100 |  | 
    Other layers (nP2 k≥2 | 1 | 269 (0.11%) | 2 (0.26%)
    Other layers (nP2 k≥2 | 2 | 599 (0.25%) | 4 (0.52%)
    Other layers (nP2 k≥2 | 5 | 1349 (0.56%) | 10 (1.30%)
    Other layers (nP2 k≥2 | 10 | 2610 (1.08%) | 20 (2.60%)
    Other layers (nP2 k≥2 | 25 | 6511 (2.70%) | 50 (6.51%)
    Other layers (nP2 k≥2 | 50 | 14621 (6.06%) | 100 (13.02%)

**TABLE 2.** Hardware occupation (logic cells and multipliers) per PE for proposal 2. [corps du tableau reconstruit par Docling : à vérifier]

    Layer | nPE | nLC | nMult
    First layer (n1 E) | 1 5 10 25 50 | 141 (0.06%) 746 (0.31%) 1384 (0.57%) 3375 (1.40%) 6682 (2.77%) 13432 (5.57%) | 1 (0.13%) 5 (0.65%) 10 (1.30%) 25 (3.26%) 50 (6.51%)
    First layer (n1 E) | 100 |  | 100 (13.02%)
    Other layers (nk2 k≥2 | 1 | 229 (0.09%) | 2 (0.26%)
    Other layers (nk2 k≥2 | 2 | 570 (0.24%) | 4 (0.52%)
    Other layers (nk2 k≥2 | 5 | 1151 (0.48%) | 10 (1.30%)
    Other layers (nk2 k≥2 | 10 | 2056 (0.85%) | 20 (2.60%)
    Other layers (nk2 k≥2 | 25 | 4860 (2.02%) | 50 (6.51%)
    Other layers (nk2 k≥2 | 50 | 9735 (4.04%) | 100 (13.02%)

**TABLE 3.** The estimate of the maximum number of PEs, n max PE , for some commercial FPGAs. [corps du tableau reconstruit par Docling : à vérifier]

    Label | FPGA.Name | n LC xdu | n max Mult | n xdu PE.γ = 20% | n xdu PE.Proposal 1 γ = 40% | n xdu PE.γ = 60% | n xdu PE.γ = 20% | n xdu PE.Proposal 2 γ = 40% | n xdu PE.γ = 60%
    FPGA1 | Virtex 6 XC6VLX240T | 241152 | 768 | 620 | 680 | 750 | 720 | 800 | 890
    FPGA2 | Virtex 6 XC6VLX760 | 758784 | 864 | 1470 | 1610 | 1780 | 1720 | 1900 | 2120
    FPGA3 | Virtex 7 XC7V2000T | 1954560 | 2160 | 3780 | 4140 | 4510 | 4410 | 4880 | 5450
    FPGA4 | Virtex UltraScale VU440 | 5540850 | 2880 | 9700 | 10000 | 10000 | 10000 | 10000 | 10000

**TABLE 4.** Values of the throughput, th ff , (in KIPS) and performance, pf , (in GOPS) shown in Figures 18, 19 and 20 (γ = 40%). Throughput, th ff , (in IPS) to several values of Q and t c for proposal 2. [corps du tableau reconstruit par Docling : à vérifier]

     | n PE max.η.G | FPGA1 680.1/8.34 | FPGA1 680.1/4.68 | FPGA1 680.1/2.136 | FPGA2 1610.1/8.81 | FPGA2 1610.1/4.161 | FPGA2 1610.1/2.322 | FPGA3 4140.1/8.207 | FPGA3 4140.1/4.414 | FPGA3 4140.1/2.828 | FPGA4 10000.1/8.500 | FPGA4 10000.1/4.1000 | FPGA4 10000.1/2.2000
    Q = 100 | th f f (KIPS) | 125 | 250 | 500 | 125 | 250 | 500 | 125 | 250 | 500 | 125 | 250 | 500
    Q = 1000 | thff f (KIPS) | 12.5 | 25.0 | 50.0 | 12.5 | 25.0 | 50.0 | 12.5 | 25.0 | 50.0 | 12.5 | 25.0 | 50.0
    Q = 10000 | thf f (KIPS) | 1.25 | 2.50 | 5.00 | 1.25 | 2.50 | 5.00 | 1.25 | 2.50 | 5.00 | 1.25 | 2.50 | 5.00
     | pf (GOPS) | 27.2 | 54.4 | 108.8 | 64.8 | 128.8 | 257.6 | 165.6 | 331.2 | 662.4 | 400 | 800 | 1600

**Table 5** Surface of regression analysis of dynamic power consumption, P 1 PE , per number of PEs, n 1 PE , and frequency of PE, f PE , in MHz for the first layer of proposal 1. [corps du tableau reconstruit par Docling : à vérifier]

    tc = 10 ns tc = 5 50 ns | Q th f f (KIPS) thf f (KIPS) | 100 1000 200 | 1000 100 | 10000 10 2 | 100000 1 0.2
     |  |  | 20 |  | 
     |  | FPGA1 | FPGA2 | FPGA3 | FPGA4
     | n PE max | 680 | 1610 | 4140 | 10000
    tc = 10 ns | pf (GOPS) | 217 | 515 | 1324 | 3200
    tc = 50 ns | pf (GOPS) | 43 | 103 | 264 | 640

**TABLE 6.** Measured dynamic power consumption per number of PEs, n 1 PE , and frequency of PE, f PE , in MHz for the first layer of proposal 1. [corps du tableau reconstruit par Docling : à vérifier]

    fPE. | P1 PE.npE = 5 | P1 PE.np E = 10 | P1 PE.np E = 25 | P1 PE.np E = 50
    2MHz | 0.001W | 0.001W | 0.002W | 0.002W
    5MHz | 0.003W | 0.003 W | 0.004W | 0.005 W
    10 MHz | 0.006 W | 0.006 W | 0.008 W | 0.010 W
    15 MHz | 0.008W | 0.009 W | 0.012W | 0.015 W
    20 MHz | 0.011W | 0.012W | 0.016 W | 0.021 W
    40 MHz | 0.022 W | 0.024W | 0.032 W | 0.041 W
    60 MHz | 0.033 W | 0.037W | 0.048W | 0.062 W
    80 MHz | 0.044W | 0.049 W | 0.065 W | 0.082 W
    100 MHz | 0.055 W | 0.061 W | 0.081 W | 0.103 W

**TABLE 7.** Measured dynamic power consumption per number of PEs, n k≥2 PE , and frequency of PE, f PE , in MHz for other layers of proposal 1 (k ≥ 2).

    FIGURE 24. Surface of regression analysis of dynamic power consumption, P k≥2 PE , per number of PEs, n k≥2 PE , and frequency of PE, f PE ,
    in MHz for other layers of proposal 1 (k ≥ 2).
    number of PEs, n k≥2 PE , and frequency of PE, f PE , in MHz for
    other layers of proposal 1 (k ≥ 2).

**TABLE 8.** Some curves values presented in Figures 25 and 26. Surface of regression analysis of the dynamic power consumption, P 1 PE , per number of PEs, n 1 PE , and frequency of PE, f PE , in MHz for the first layer of proposal 2.

    FIGURE 27. Using Equations 27, 36 and 45, the Equations 44 and 46
    can be characterized as | 
     | P 1 PE = | 569.0849 + 24.4342 γ ×n PE 100 t c × 10 12 |  | (47)
    and |  |  | 
    P k≥2 PE = | 639.3527 + 20.7985 n PE -γ ×n PE 100 t c × 10 12 | . | (48)

**TABLE 9.** Measured dynamic power consumption per number of PEs, n 1 PE , and frequency of PE, f PE , in MHz for the first layer of proposal 2.

    FIGURE 28. Surface of regression analysis of the dynamic power consumption, P k≥2 PE , per number of PEs, n k≥2 PE , and frequency of PE, f PE , in MHz for the first layer of proposal 2.

**TABLE 10.** Measured dynamic power consumption per number of PEs, n k≥2 PE , and frequency of PE, f PE , in MHz for other layers of proposal 2 (k ≥ 2).

    Based of Equations 43, 47 and 48, the total dynamic power
    consumption per PEs, P d , for proposal 2 can be expressed as
    P d = | 1208.4376 + 20.7985n PE + 3.6357 γ ×n PE 100 t c × 10 12

**TABLE 12.** Proposal 1 -hardware area occupation. [corps du tableau reconstruit par Docling : à vérifier]

     | Multipliers (nMult) | Logic cells (nCL)
    Synthesis Estimated | 220 (28.65%) | 37796 (15.67%)
    (Equations 10, 11, 13, and 16) | 220 (28.65%) | 38326 (15.89%)

**TABLE 13.** Proposal 1 -processing times and delays (G = 1 and Q = 800). [corps du tableau reconstruit par Docling : à vérifier]

    trc | d | tff | thff | Pd Measurement | Estimated (Eqs. 41, 42, and 43)
    10 ns | 2.4 ms | 0.8 ms | 1.25 KFPS | 0.003 W | 0.0047W

**TABLE 14.** Proposal 2 -hardware area occupation. [corps du tableau reconstruit par Docling : à vérifier]

     | Multipliers (nMult) | Logic cells (nCL)
    Synthesis Estimated | 220 (28.65%) | 24399 (10.12%)
    (Equations 13, 16, 17, and 18) | 220 (28.65%) | 25045 (10.39%)

**TABLE 15.** Proposal 2 -processing times and delays (Q = 800). [corps du tableau reconstruit par Docling : à vérifier]

    tc | d | tff | thff | Pd Measurement | Estimated (Eq. 49)
    45 ns | 0.1 ms | 0.04 ms | 25 KFPS | 0.112W | 0.110W

**TABLE 16.** State of the art comparison associated with throughput, th ff , and power consumption, P d , for two different deep neural network size. [corps du tableau reconstruit par Docling : à vérifier]

    Ref.. | References.Device. | References.Network architecture. | Value.thf f (FPS) 45 | G 1 2 | Proposal 1.thf f (FPS) 12.5 25 | Proposal 1.Q = 4000, trc = 10 ns, and tc = 45 ns Speedup | Proposal 2.thf f (FPS) 5208 | Proposal 2.Speedup ≈116×
    [5] | Intel (Altera) Stratix V | 3072 - 2000 - 750 - 10 | Pd (W) | 4 8 G | 50 100 Pd (W) | ≈ 1.11× ≈ 2.22× Power saving | Pd (W) | Power saving
     |  |  | 16 | 1 2 | 0.0023 0.0045 | ≈ 7081× ≈ 3540× |  | 
     |  |  |  | 4 8 | 0.0090 0.0181 | ≈1770× ≈ 885× | 1.46 | ≈11×
     |  |  | Q = 1000, trc = 10 ns, and tc = 45 ns | Q = 1000, trc = 10 ns, and tc = 45 ns | Q = 1000, trc = 10 ns, and tc = 45 ns | Q = 1000, trc = 10 ns, and tc = 45 ns | Q = 1000, trc = 10 ns, and tc = 45 ns | Q = 1000, trc = 10 ns, and tc = 45 ns
     |  |  | thf f (FPS) | G 1 | thf f (FPS) 390.62 | Speedup ≈31× | thf f (FPS) | Speedup
     |  |  | 12.45 | 2 4 8 | 781.25 1562.5 3125 | ≈ 62× ≈ 125× ≈251× | 22222 | ≈1784×
    [14] | Xilinx XC7Z020 | 784 - 256 - 256 - 10 | Pd (W) | G 1 | Pd (W) 0.0059 | Power saving ≈309× | Pd (W) | Power saving
     |  |  | 1.814 | 2 4 8 | 0.0117 0.0234 0.0468 | ≈ 154× ≈77× ≈38× | 0.29 | ≈ 6×

**TABLE 17.** State of the art comparison associated with performance, pf , in GOPS. [corps du tableau reconstruit par Docling : à vérifier]

    Ref. | References.Device | Value | Proposals.Proposal 1 | Proposals.Proposal 1 | Proposals.Proposal 1 | Proposals.Proposal 2 | Proposals.Proposal 2
    [36] | Xilinx Ultrascale KU060 FPGA |  | npdx max = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | npdx max = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | npdx max = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | npdx max = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | npdx max = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns
    [36] | Xilinx Ultrascale KU060 FPGA | pf (GOPS) 173 | η 0.1 0.2 0.3 0.4 | pf (GOPS) 320 640 960 1280 | Speedup ≈1.8× ≈3.7× ≈5.5× ≈7.4× | pf (GOPS) 711 | Speedup ≈ 4.11×
    [12] | Xilinx Virtex7 485t FPGA |  | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns
    [12] | Xilinx Virtex7 485t FPGA | pf (GOPS) 61.62 | η 0.1 0.2 0.3 0.4 | pf (GOPS) 320 640 960 1280 | Speedup ≈ 5.2× ≈ 10.4× ≈ 15.6× ≈ 20.8× | pf (GOPS) 711 | Speedup ≈11.5×
    [13] | Xilinx Kintex K325T FPGA |  | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns PE | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns PE | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns PE | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns PE | = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns PE
    [13] | Xilinx Kintex K325T FPGA | pf (GOPS) 260 pf (GOPS) | η 0.1 0.2 0.3 0.4 npEx η | pf (GOPS) 320 640 960 1280 = 10000, γ = 40%, trc = 10 ns, and tc = 45 ns | Speedup ≈1.2× ≈2.5× ≈3.7× ≈4.9× | pf (GOPS) 711 | Speedup ≈ 2.7×
    [37] | ASIC | pf (GOPS) 260 pf (GOPS) | 0.2 0.3 | pf (GOPS) 640 960 1280 | Speedup ≈ 1.4× ≈ 2.1× ≈ 2.8× | pf (GOPS) | Speedup
    [13] | Xilinx Kintex K325T FPGA | 452 | 0.4 0.5 | 1600 | ≈ 3.5× | 711 | ≈1.53×
