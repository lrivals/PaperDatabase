---
id: arxiv-2402.09780-tinycl-efficient-hardware-architecture-continual
title: "TinyCL: An Efficient Hardware Architecture for Continual Learning on Autonomous Systems"
year: 2024
backend: grobid
---

## Abstract

The Continuous Learning (CL) paradigm consists of continuously evolving the parameters of the Deep Neural Network (DNN) model to progressively learn to perform new tasks without reducing the performance on previous tasks, i.e., avoiding the so-called catastrophic forgetting. However, the DNN parameter update in CL-based autonomous systems is extremely resource-hungry. The existing DNN accelerators cannot be directly employed in CL because they only support the execution of the forward propagation. Only a few prior architectures execute the backpropagation and weight update, but they lack the control and management for CL. Towards this, we design a hardware architecture, TinyCL, to perform CL on resourceconstrained autonomous systems. It consists of a processing unit that executes both forward and backward propagation, and a control unit that manages memory-based CL workload. To minimize the memory accesses, the sliding window of the convolutional layer moves in a snake-like fashion. Moreover, the Multiply-and-Accumulate units can be reconfigured at runtime to execute different operations. As per our knowledge, our proposed TinyCL represents the first hardware accelerator that executes CL on autonomous systems. We synthesize the complete TinyCL architecture in a 65 nm CMOS technology node with the conventional ASIC design flow. It executes 1 epoch of training on a Conv + ReLU + Dense model on the CIFAR10 dataset in 1.76 s, while 1 training epoch of the same model using an Nvidia Tesla P100 GPU takes 103 s, thus achieving a 58× speedup, consuming 86 mW in a 4.74 mm 2 die.

## I. INTRODUCTION

In recent years, Deep Neural Networks (DNNs) have been deployed in several applications, like computer vision, finance, healthcare, and robotics [1]- [4]. A common practice is to train a DNN on the desired task using the training set, and then deploy the trained model on the target for inference [5]. In this way, it is possible to conduct DNN training on large data centers (e.g., using high-end GPUs), and then conduct resource-constrained optimizations (e.g., compression) to deploy DNN inference on autonomous systems [6]- [9]. However, this practice limits the dynamic capabilities of DNNs that cannot adapt to new tasks or a distribution variation of the input data within the same task. In this regard, the Continual Learning (CL) paradigm enables the dynamic change of DNN parameters to evolve and learn new tasks (or new classes) [10]- [12]. The main goal of CL-based algorithms is to avoid Catastrophic Forgetting (CF), i.e., the DNN should maintain the knowledge of how to perform the previous tasks while learning new tasks [13].

### A. Target Research Problem

Since they require the execution of the backpropagation and parameters' update, CL algorithms impose more demanding computation and memory resources than traditional systems that conduct only inference [14]. Hence, it is extremely important to execute CL algorithms in an efficient manner to be able to deploy them onto resource-constrained autonomous systems.

Most of the existing architectures and optimizations for DNNs focus only on optimizing the inference process [15]. Therefore, they cannot execute the backward operations required by CL algorithms. Some architectures [16] that have been proposed to accelerate the training can be adopted to conduct backpropagation computations, but they do not support the execution of CF-avoiding policies.

### B. Novel Contributions

To overcome these limitations, we propose TinyCL, a hardware architecture that can efficiently execute CL operations on autonomous systems. Our architecture reuses the same processing units for computing the forward and backward computations, and a specialized control unit dictates the data flow based on the CL policy. In a nutshell, our contributions are (see Figure 1):

• RTL Design of the complete TinyCL architecture, in which multiple Processing Units execute the computation in parallel and the convolutional sliding window is designed following a snake-like pattern. (Section III) • Synthesis of the TinyCL architecture using the conventional ASIC flow for a 65 nm CMOS technology node. (Section IV) • Compared to its equivalent software-level implementation on an Nvidia Tesla P100 GPU, the TinyCL architecture achieves 35× speedup; compared to other DNN training accelerators in the literature, the TinyCL architecture achieves lower latency, power consumption, and area, thus making it suitable for being adopted on resource-constrained autonomous systems. (Section IV-C)

## II. BACKGROUND AND RELATED WORK

### A. Convolutional Neural Networks

Convolutional Neural Networks (CNNs) are a branch of DNNs used in image recognition tasks. Convolutional and dense layers are the basis blocks of every CNN. In a convolutional layer, a multi-channel input feature V is convoluted with a 4D kernel K to produce a multi-channel output Z (see Equation (1)).

Z(i, j, k) = c(K, V, s) i,j,k = l,m,n [V (l, (j -1) • s + m, (k -1) • s + n) • K(i, l, m, n)]

(1) Applying the Stochastic Gradient Descent (SGD), the computation to propagate the gradient across layers is a convolution between the previous kernel K and the gradient G propagated from the previous layer, as shown in Equation ( 2), while the gradient of the kernel is computed through Equation (3).

h(K, G, s) i,j,k = ∂ ∂V i,j,k J(V, K) = l,m s.t.(l-1)•s+m=j n,p s.t.(n-1)•s+p=k q G q,l,n • K q,i,m,p(2)

g(G, V, s) i,j,k,l = ∂ ∂K i,j,k J(V, K) = m,n G i,m,n • V j,(m-1)•s+k,(n-1)•s+l(3)

The Dense layer computes a matrix multiplication between a 1D row matrix I with a 2D weight matrix W (see Equation ( 4)).

y n = m i=0 I i • W i,n(4)

Applying SGD, we can compute the gradient propagation that is a matrix multiplication between the input gradient dY propagated from the previous layer and the transpose of the weight (see Equation ( 5)).

dX i = N n=0 dY n • W T n,i(5)

Then, the gradient of the weights is computed as in Equation (6).

dW i,n = I i • dY n(6)

### B. Continual Learning Algorithms

The goal of CL, also known as incremental learning, lifelong learning, or sequential learning, is to gradually learn from different data streams and extend the acquired knowledge [17]. The data streams can be associated with different tasks that the CL system can perform. Incrementally learning all the tasks is an NP-hard problem [18]. Moreover, the major issue of CL is represented by CF, i.e., the ability of the system to perform previously learned tasks degrades over time when new tasks are added [13]. In the literature, several CL methods have been proposed to mitigate CF. CL algorithms can be categorized as regularization-based methods, memorybased methods, and dynamic approaches.

Regularization-based methods apply constraints in the weight update phase to mitigate CF. Weight regularization methods such as Elastic Weight Consolidation (EWC) [19] impose a quadratic penalty to selectively regularize the parameters based on their importance to perform the previous tasks, calculated through the Fisher information matrix. Function regularization methods like the Learning without Forgetting (LwF) [20] employ knowledge distillation to learn the training samples of the new tasks while preserving the knowledge of the previous tasks.

Memory-based approaches, also known as replay-based methods, retrain or finetune the DNN jointly using samples from previous tasks and samples from new tasks. The Gradient Episodic Memory (GEM) method [21] constrains the parameter update such that the training loss of each individual previous task does not increase. Its variant, called A-GEM [22], ensures that the average training loss for all previous tasks does not increase. The Incremental Classifier and Representation Learning (iCaRL) [23] method stores a subset of training samples for each task and jointly minimizes the training loss for new tasks and the distillation loss for the previously learned tasks. Experience Replay (ER) [24] combines training with samples of the new tasks and old samples that are stored in a replay memory. The Maximally Interfered Retrieval (MIR) method [25] selects the samples from the old tasks that would have the largest impact on the forgetting property. The Gradient-based Sample Selection (GSS) strategy [26] maximizes the gradient diversity of the stored sample subset. Greedy Sampler and Dumb Learner (GDumb) approach [27] greedily stores training samples in the memory buffer to maintain a balanced class distribution. The replay data can also be generated at runtime by using the Deep Generative Replay (DGR) method [28], where a generator creates synthetic samples that contain previous tasks knowledge.

Dynamic approaches dynamically increase the DNN architecture to learn features of new tasks. The Continual Neural Dirichlet Process Mixture (CN-DPM) method [29] retains the knowledge of the previous tasks by building a mixture of experts where a new model is trained for a new task, while the existing models for the previous tasks are not modified. The Progressive Segmented Training (PST) method [30] focuses on a single network and, when training on a new task, it divides the parameters into two groups according to their importance to perform that task. The group of important parameters is frozen to preserve the current knowledge, while the other group is saved and can be updated when learning future tasks.

Our architecture supports memory-based approaches due to the simplicity of their hardware implementation, but it can be easily extended to execute other CL algorithms.

### C. DNN Training Accelerators

Various hardware architectures implemented in ASIC or FPGA for accelerating DNN training have been proposed in recent years. The work in [31] is composed of heterogeneous processing tiles to efficiently execute different operations with diverse computational characteristics. The DeepTrain architecture [32] deploys heterogeneous programmable data flows to achieve data reuse during different training operations. The Gist architecture [33] utilizes layer-specific encoding schemes to exploit redundancy in DNN training by storing the feature maps computed during the forward pass and reusing them in the backward pass. The SIGMA accelerator [34] supports irregular sparse workload. To efficiently handle sparsity, the Procrustes accelerator [35] employs a dense tensor dimension for performing arithmetic operations that involve sparse tensors. The LNPU architecture [36] implements fine-grained mixed precision to perform training. The HNPU architecture [37] supports low-precision training by dynamically configuring the fixed-point representation. The FlexBlock architecture [38] supports multiple block floatingpoint precisions. The ETA architecture [39] performs training based on the proposed piecewise integer format. The work in [40] trains the DNN through a two-step process that consists of sample collection and policy update for continuous control of the behavior. The above-mentioned architectures allow the execution of standard training in an efficient manner. However, the execution of CL algorithms requires additional abstraction layers to correctly manage the workload.

### D. Optimizations for Continual Learning at the Edge

Recent works have proposed specialized optimization to improve the efficiency of CL algorithms on resourceconstrained devices. Huai et al. [41] designed a method for improving the efficiency during the re-training phase of latency-constrained high-end edge systems. The SparCL framework [42] enables efficient continual learning through weight and gradient sparsity. The SIESTA algorithm [43] proposed to alternate awake cycles with sleep cycles to consolidate the memory. The Miro methodology [44] designs the memory hierarchy to leverage the tradeoff between energy and accuracy.

While these works demonstrated potential to improve the efficiency in some parts of the process, they do not consider the complete system implemented on a specialized accelerator, as we do in this paper.

## III. TINYCL ARCHITECTURE DESIGN

### A. Data quantization

Since high-precision data is not necessary, a 16-bit fixedpoint (4-bit integer + 12-bit fractional data) format is used. Accordingly, the work in [45] suggests that value clipping is useful to increase accuracy in DNNs where batch normalization is not applied.

### B. Top-Level Architecture

Our system is composed of 4 groups of data memory ( GDumb memory, Gradient memory, Kernel memory and Partial Feature memory), a control unit and a processing unit, as depicted in Figure 2.

### C. Processing Unit

Our processing unit, depicted in Figure 3, includes 9 parallel multiply and accumulate (MAC) blocks, each of them executing an 8-operand multiplication and addition in parallel. 3 manager units (gradient, kernel, and feature) are designed to drive the data flow. 3 address managers (gradient, kernel, and feature) compute the addresses needed to the forward, gradient propagation, and kernel derivative.

### Gradient

### D. MAC

Our MAC is composed of 8 multipliers and 8 adders, as shown in Figure 4. The multipliers are configured in a parallel fashion, while the adders can be configured in two ways: multioperand mode or multi-adder mode. • Multi-Adder mode: During kernel gradient calculation, the adders sum the 8 multiplication results with 8 input values to obtain the partial sum outputs. In the weight gradient calculation, as we compute in parallel 8 channels at a time, each time we have to multiply 8 channels of one input feature with one channel of the input gradient. The results of these 8 multiplications will be summed with the previous multiplication done. • Multi-Operand mode: During forward and gradient propagation, we compute 8 input channels at a time. In this case, since the output is the sum of these 8 input channels (3D-convolution), we configure the 7 adders to operate as an adder-tree. To reduce the loss of information, the results of the 16-bit multiplications are kept in full precision and propagated to the 32-bit adders. After the addition, the output is reduced to 16 bit, rounded to nearest.

### E. Memory

A typical DNN accelerator that performs only inference needs to save only its parameters. However, a CL accelerator needs to save other data. • Gradient Memories: To temporarily save the gradients to be used between two computations, a couple of memories must be used. The memories shall be 2 because 1 would not be enough. In a multi-channel convolution operation, the feature we are calculating will overwrite a feature we will need in further calculus.

To increase throughput and decrease stalls, we design the memories with a port width of 128 bits, to read 8 features at a time. To further increase the throughput, the SRAM is organized according to the channel. For example, if we compute convolution with an input feature of 32 × 32 with 8 channels and we output a feature of 32 × 32 of 8 channels, we will have 8 blocks for partial features of 32 × 32 × 16 bits, 64 blocks of 3 × 3 × 16 bits to save the kernels and 16 blocks of 32 × 32 × 16 bits memory for gradient propagation. Moreover, dedicated buffers prefetch data from memory.

### F. Control Unit and Data Flow

Our control unit manages the multi-layer computation, passing the actual matrix input and output sizes to the PU. For each layer, the Control Unit (CU) manages the data flow from memories to MACs for executing 6 different computations:

• Convolution -forward computation In each of these computations, data are fetched and loaded into buffers, so that at each clock cycle, the respective features are directly processed by the MACs of the PU. In this way, we are able to maintain a high hardware utilization.

### 1) Forward Computation of the Convolutional Layer

In the forward operation, each multi-channel input feature must be 3D-convoluted with a 4D kernel to create a single pixel in the new feature, as in Equation (1).

To create more channels in the output feature, more 3D kernels are used. Using 9 instances of the MAC, we compute in parallel a 8×3×3 3D convolution. To output a single output feature, groups of 8 × 3 × 3 input features (a 3 × 3 submatrix for each channel) are convolved with a 8 × 3 × 3 matrix of weights (kernels). If the input feature has more input channels, this operation is repeated. However, most of the input features that are part of the convolution of 9 output feature (for each output channel) are used in the next output feature calculations.

When we reach the final feature of a row and move to the next row, we do not restart from column 0. Instead, we start decreasing the column counter, following a snake-like movement (see Figure 5). In this way, 6 features are always reused. Hence, when the computations are at full throttle, for each output feature (i.e., for each cycle), we fetch 3 input features for 8 channels (16-bit each) and write one value. In this way, each cycle, 6 of the 9 input features are saved and 3 new are loaded. These 9×8 values are then sent to the 9 MACs. Each MAC takes 8 channels of a feature and multiplies them for 8 channels of the kernel. These 9 values are then summed together in a 9-operand Dadda adder to generate the output. This process is conducted for the whole set of output features. The addresses to read the input features and the kernels, and to write the new output features are generated by the Forward Address Manager, which uses the dynamic size given by the CU as the bound for the column, row, and channel counters. When the column counter reaches the dynamic size, it will not be zeroed due to snake movement, but its address will be maintained and increased by one row. When the end of the matrix is reached, the channel counter is increased.

### 2) Kernel Gradient Computation

To calculate the gradient of the kernels, a 2D convolution must be executed, as in Equation (3). The input gradient is convoluted with 9 different sub-matrices of the input feature, which are shifted according to the respective position of the gradient kernel. Since the input feature is padded with 2 stripes of zeros on the right and bottom borders, the resulting matrix has sizes increased by 2 in both dimensions. The index of the kernels is also used for indexing which MAC is used to compute the gradient, according to Equation (7).

### Kernel Input

### Feature Map

M AC k,l <= g(G, V, s) i,j,k,l = ∂ ∂K i,j,k,l J(V, K)(7)

Therefore, the features are shared between convolutions (to an even larger extent than for the forward convolution).

### 3) Gradient Propagation

To compute the gradient propagation, the input gradient is convoluted with the 4D kernel. The data flow is the same as for the forward propagation since the input gradient is computed as the input feature in the forward computations.

### 4) Dense Layer Computation

This section illustrates how the dense layer operations are conducted using the same 9 MACs of the PU.

• Forward propagation: It is implemented as a matrix multiplication between the flatted features of the previous layer with a 2D matrix. The weight matrix has a size (m,n) where m is the number of input features and n is the number of output features. Note that in the last dense layer, the output features' value is equal to the number of classes. This number, due to the CL setup, is not static and changes during the operation. The output of the forward algorithm is implemented according to Equation (8), which is described considering to have a 3D matrix with sizes (I, J, K) instead of the conventional flattened values.

y n = m i=0 I i • W i,n = I,J,K i,j,k=0 I i,j,k • W i,j,k,n(8)

In this way, we can reuse the same logic of the forward computation for convolutional layers. In this case, for each clock cycle, 8 pixels of 8 channels of the input feature and 8 weights of 8 channels are read and sent to 8 of the 9 MACs. All 64 results are then summed together and saved into the partial sum register. This is done for the whole set of input features and it is repeated n times, where n is the number of output features. In this way, we can dynamically set the number of iterations required. • Gradient propagation: The gradient propagation dX is equal to the matrix multiplication between input gradient propagation and the transpose of the weights, as described in Equation (5). In this case, the optimization is more complicated. Due to the fact the size of dY is dynamic due to the CL settings and is not necessarily a power of 2, we cannot reach a 100% utilization of the hardware resources. We propose to execute inside a single MAC the computation for each feature of dX, iteratively using the register and the partial sum logic. Using 9 MACs, we can compute 9 pixel in n/8 clock cycles, where n is the number of output features, and the whole computation in (I/9) • (n/8) cycles. An example of how MACs are indexed is shown in Equation (9).

M AC 0,0 <= dX 0 = 7 n=0 dY n • W T n,0(9)

The values will be saved in the partial sum register and summed in the next addition, until the end of the vector. • Weight derivative: The derivative of the weight (dW ) is the matrix multiplication between the input feature I used during the forward computation and the gradient propagation coming from the loss computation dY , as described in Equation ( 6).

Using the matrix notation, since both operands are row matrix, their product produces a matrix. This means that the whole matrix I is multiplied with the same value dY n . This calculus can be executed in our MAC. 64 parallel input features are read (8 pixels for 8 channels, as in forward) and multiplied with one feature of dY . The 64 multiplication results are then added together and accumulated to previous multiplication and addition. This is repeated for each feature of dY .

## IV. EXPERIMENTAL RESULTS

### A. Experimental Setup

The complete TinyCL architecture is described at the RTL level using the SystemVerilog language. We synthesized the architecture in a 65 nm CMOS technology node with the ASIC design flow using the Synopsys Design Compiler tool. The synthesized netlist has been functionally tested through gatelevel simulations, compared to the equivalent software-level implementation on TensorFlow [46] running on an NVIDIA Tesla P100 GPU. The complete flow of our experiments is shown in Figure 6. For comparison purposes, we test our system executing a simple DNN model, composed of 2 convolutional layers with ReLU activation, followed by a Dense layer. This model has been trained with the CIFAR10 dataset [47] for 10 epochs, a learning rate of 1, and a batch size of 1, while the training is composed of 5 tasks of 2 classes per task, following the GDumb approach [27]. The model is used side by side with a memory of 6.144 MB, which can contain 1000 32 × 32 RGB training samples.

### B. Sysnthesis Evaluation of Area, Power, and Latency

The synthesized TinyCL architecture has a clock period of 3.87 ns, consumes 86 mW, and occupies an area of 4.74 mm 2 . Figure 7 analyzes in detail the power and area breakdown for each component. It is evident that the Memory block is responsible for the majority of area (80%) and power (76%) of the complete architecture. Our architecture takes 8,192 clock cycles to compute either the forward convolution, the gradient propagation, or the gradient of the weight when we use 8 filters and the input feature has a shape of 32 × 32 × 8. Instead, the dense layer for a feature of shape 32 × 32 × 8 which outputs an array of size 10 takes 1,280 clock cycles for forward computation, 1,821 clock cycles for the computation of the gradients of the weights, and 1,280 clock cycles for the gradient propagation.

### C. Comparison with Related Works

As a first analysis, we compare our TinyCL architecture with its software-level implementation on a P100 GPU. Following the setup described in Section IV-A, the GPU implementation lasts 103 s, while the TinyCL architecture executes the same workload in 1.76 s, thus reaching a speedup of 58×.

Table I compares latency, power, area, and performance of our proposed TinyCL architecture with related works. Note that since there are no available designs specialized for CL workloads, we compare it with existing designs that execute generic DNN training operations. The results show that the proposed TinyCL architecture is suitable for autonomous systems with limited resources since it achieves lower area and power consumption than prior works.

## V. CONCLUSION

We have presented TinyCL, an efficient hardware architecture for CL algorithms, which executes all the involved operations such as forward propagation, backward propagation, and parameter update. A specialized control unit manages the memory and data flow to support memory-based

## Figures et tableaux

**Fig. 1.** Overview of our novel contributions in this work.

**Fig. 2.** Top-level view of the TinyCL architecture.

**Fig. 3.** Overview of the processing unit architecture.

**Fig. 4.** Overview of the multiply-and-accumulate (MAC) architecture.

**Fig. 5.** Example of forward computation of a channel of a convolutional layer.

**Fig. 6.** Experimental setup and tool flow for conducting the experiments.

**Fig. 7.** (a) Area and (b) power breakdown of our TinyCL architecture.

**TABLE I** COMPARISON BETWEEN TINYCL AND RELATED DNN TRAINING ARCHITECTURES.CL policies and different operations on the same Processing Unit. The TinyCL architecture, synthesized in a 65 nm CMOS technology node, achieves 58× speedup compared to an equivalent software-level implementation executing on an Nvidia Tesla P100 GPU, while achieving lower area and power consumption than related works. Our design and analyses open new avenues for developing efficient CL algorithms on resource-constrained autonomous systems.

    Architecture | Latency (ns) | Power (mW) | Area (mm 2 ) | Performance (TOPS)
    HNPU [37] | 4 | 1162 | 12.96 | 3.07
    LNPU [36] | 5 | 367 | 16 | 0.6
    ISSCC19 [40] | 5 | 196 | 16 | 0.204
    TinyCL (our) | 3.87 | 86 | 4.74 | 0.037
