---
id: 2022-malviya-edge-compatible-convolutional-autoencoder-implemented
title: "Edge-Compatible Convolutional Autoencoder Implemented on FPGA for Anomaly Detection in Vibration Condition-Based Monitoring"
year: 2022
backend: grobid
---

## Abstract

Estimating the state of the health of machines using vibration signals analyzed with complex deep-learning models poses memory and processing speed constraints for edge implementation, whereas cloud-based computing poses high latency, high cost of data transmission and storage, and privacy threats. Moreover, in most practical settings, a large amount of data may be available or easily obtainable for machines in healthy/normal operating condition, and not in anomalous conditions. Thus, there exists a need to develop lightweight unsupervised learning based algorithms that can be implemented on an embedded platform for data processing and estimating state of health. In this letter, we present a lightweight convolutional autoencoder (CAE) implemented on a low-cost FPGA platform (PYNQ-Z2, Xilinx Zynq-7020 SoC) to discern anomalies in vibration data sets. We present an extensive performance analysis of various encoding methods to represent 1-D time-series as images and the feasibility analysis of FPGA-implementation of CAE. The optimized model has less than 10 000 trainable parameters and shows the highest accuracy (>88% on CPU, >85% with fixed point arithmetic on FPGA) using scalogram encoding when trained and tested on the Airbus SAS helicopter accelerometer dataset.

## I. INTRODUCTION

Condition-based monitoring (CBM) is a maintenance strategy that utilizes sensor measurements for estimating the state of health of machines and automated early diagnosis of faults that are used to trigger remedial actions. Physics-based models combined with statistical signal processing make it possible to perform damage assessment from time-domain signals in structural health monitoring, for use cases where the impact of damage on sensor performance is adequately described with mathematical models [1]- [3]. With the advent of lowcost sensors, inexpensive computing, and data processing solutions, deep learning is emerging as a valuable tool for CBM, where such mathematical models may be impractical [4], [5]. Performance of deep learning models for CBM heavily depends on features generated from the data [6]. Developing accurate supervised learning models requires a large dataset comprising of measurements collected on machines in healthy (normal) operating condition as well as in the presence of all possible faults that need to be determined with these models. Several data-driven deep learning techniques, both supervised and unsupervised, have been proposed to monitor the health condition of machines, including convolutional neural networks (CNNs) [7]- [9] and variants of autoencoders (AEs) [4], [10], [11]. In most practical settings, a large amount of data may be available for machines in healthy operating condition. AEs leverage unsupervised learning to detect any deviation in sensor outputs based on training performed solely using data collected for healthy condition.

Cloud-based implementations of deep learning models have several downsides, such as high latency, high cost of data transmission, and privacy threats. The pace of the development of edge-computing solutions for CBM has been slow, due to a number of practical challenges. The TinyML community is boosting the integration of machine learning within microcontroller-based edge solutions; however, all frameworks reported focus primarily on neural network implementations for voice and facial recognition [12]. Modern field programmable gate array (FPGA) devices enable key analytics and hardware acceleration with integrated computing and signal processing, and have been used for edge implementation of deep learning algorithms [13]- [15].

In this letter, we present a lightweight convolutional autoencoder (CAE) to detect anomalies in vibration signatures of machines. The model is trained and tested on the publicly available Airbus SAS helicopter accelerometer dataset [16] containing highly complex vibration measurements from real helicopter flight tests (model overview shown in Fig. 1). We compare the CAE model performance for various encodings for data representation. The model thus developed has an order of magnitude lower number of trainable parameters (8755), as compared with other models reported in literature, and resulted in accuracy of 88.8% when tested on a CPU workstation, and 85.02% on a low-cost FPGA board (PYNQ-Z2), comparable with more complex models reported in literature. The hardware acceleration of the model on PYNQ-Z2 is attested by average inference time of 5.9 ms, i.e., a factor of 18.52X speed-up compared with CPU.

## II. ANOMALY DETECTION FRAMEWORK

### A. Dataset Overview

The Airbus SAS helicopter accelerometer dataset [16] comprises of accelerometers placed at different positions and along different directions (longitudinal, vertical, and lateral) on a helicopter to measure vibration signals in all operating conditions. The dataset consists of multiple 1-D time-series of duration 1 min taken from different flights, obtained at sampling rate of 1024 Hz (i.e., 61 440 samples in each series). All data, as provided, are multiplied by a factor so that the absolute values are meaningless, without any other normalization. The training data consists of 1677 such recordings under normal operating condition. The testing dataset is composed of 594 recordings measured on helicopters at various locations and angles that may or may not be identical to those of the training dataset.

### B. Data Encoding and Preprocessing

We represent 1-D time-series as images by applying the following popular encodings: spectrogram, scalogram, Markov transition field (MTF), and Gramian angular field (GAF). Spectrogram is a visual representation of the temporal variation in spectrum of frequencies of a signal, computed using the short-time Fourier transform. Scalogram is the absolute value of the continuous wavelet transform of a signal, plotted as a function of time and frequency. MTF is an image representation of transition probabilities, indicating disparity in value between any pair of points in the time-series [17]. GAF helps quantify the linear dependence of a set of vectors, constructed by a dot product of every couple of vectors in polar coordinates [17]. To compute spectrograms, each sequence of length 61 140 is divided into three frames of length 25 000 samples, with overlap. Spectrograms are computed using block size of 1024 and 512 points overlap between blocks and represented as images of size 512 × 48. To compute scalogram, MTF, and GAF, each sequence of length 61 140 is divided into 120 subseries with 512 samples each. Scalograms are computed using Mexican hat wavelet, with a scale size of 64. The resulting output of size 64 × 512 is compressed to size 64 × 64. Similarly, MTF and GAF of size 512 × 512 are compressed to size 64 × 64. The image size is reduced by averaging pixels in each nonoverlapping m × n size patch, with blurring kernel 1 mn . For MTF and GAF, we set m = 8 and n = 8. For scalogram, we set m = 1 and n = 8.

### C. CAE Architecture

The encoded images are further analyzed with a CAE. The CAE compresses the signal to a lower dimension space (core layer) using an encoder and then reconstructs the compressed signal into original shape using a decoder. The hidden layers in the encoder learn patterns in the input data and extract essential information and are, therefore, trained only using healthy data (normal operating condition). When the model encounters an input belonging to anomalous dataset, the decoder produces a signal with a large reconstruction error. The reconstruction error is quantified using cross entropy of the reconstructed signal. The

## III. HARDWARE ACCELERATION

The CAE (given in Table 1) is trained on a CPU workstation (64-bit Intel Core i7-8700 @ 3.2GHz, 16GB RAM), and the trained model is implemented on the PYNQ-Z2 board equipped with opensource PYNQ python framework that enables seamless design of programmable logic circuits by importing them as hardware libraries and programming through their APIs. The CAE is implemented in Vivado high-level synthesis (HLS) compiler in C programming language, and then exported as intellectual property (IP). The IP is integrated with other IP blocks in Vivado to generate the bitstream. Separate bitstreams are implemented for the encoder and decoder that are initialized by python overlays in PYNQ. data buffers to improve throughput and latency. The input image stream is padded with zeros and convolved with the kernel using line buffer and window data structures. Fig. 2 shows this implementation for a kernel of size 3 × 3. The line buffer has size 2 × length of the input and serves as a cache that fills elements into the rightmost column of the window at every new iteration (clock cycle). As such, only one new input pixel has to be read from the I/O port at every clock cycle. The use of line buffer also helps with memory management. At every clock cycle, contents of each line buffer are shifted to the line buffer above it, and a new pixel is read into the vacant buffer. Similarly, data in the uppermost buffer are purged since they are no longer needed. The FPGA only ever holds a fraction of the image data and not the entire image at any particular time. The max pooling and upsampling functions are implemented similarly as convolution, using line buffers and windows. The only difference is the computation and stride with which the value is updated in the window. In max pooling, the maximum value present in the window is passed into the output pixel, while in upsampling, the central value is repeated in all rows and columns of the window. Due to data buffers and stream interconnection between functions, all convolution and pooling/upsampling layers finish execution simultaneously. Next, the data stream is passed as an input to a typical neural network consisting of a single FC layer. Unlike convolution, FC layer performs a sequential execution and, hence, requires all inputs to calculate each output sample, thus requiring as many multipliers as number of input samples.

### A. HLS Implementation

Vivado HLS provides a number of pragma directives to optimize the design, e.g., decrease latency, improve throughput performance, and reduce area and device resource usage of resulting register transfer level code. The following optimization methods were used in this article: Vivado HLS unroll pragma (to increase data access and throughput), Vivado HLS pipeline pragma (concurrent execution of operations), and dataflow pipelining (to overlap operation of functions and loops). Further, we used fixed-point arithmetic to optimize hardware utilization, wherein 23 bits were used to represent each value, of which 2 bits were used for the integer part. Memory management is executed by direct memory access (DMA) block in the FPGA. DMA helps in accessing external memory (RAM) present on the board with AXI-Stream protocol. The ARM Cortex-A9 processor present in the FPGA acts as the main controller of the CAE model. Python overlays provided by PYNQ environment help with accessing IP blocks and initiate all data transfers with DMA. of trainable parameters in the model (see Table 1) are very low (8755), thus qualifying it as a light-weight model suitable for embedded hardware (edge) implementation. Model optimization strategies that we explored include increasing number of layers, addition of fully connected layer, various settings for learning rate, as well as various scales for scalogram computation and metrics for reconstruction error. Optimized hyperparameters for each encoding are given in Table 2. The accuracy is calculated by setting the reconstruction error threshold for determining anomaly as μ + σ , where μ and σ are the mean and standard deviation, respectively, for the reconstruction error for healthy (normal) training samples. Scalograms computed using Mexican hat wavelet with a scale size of 64 yield the highest accuracy (88.8%). The number of floating-point operations (FLOPs) capture the overall complexity of the model. The total number of FLOPs for the encoder and decoder blocks are 1.65e6 and 1.82e6, respectively. The CAE is able to perform better with time-frequency representations of the signals (spectrogram and scalogram) that capture more features of nonstationary vibration signals [21], resulting in higher accuracy than encodings, such as GAF and MTF, that primarily preserve temporal characteristics of the signal. Other performance parameters of the model for scalogram are as follows: precision = 88%, recall = 91%, and F 1 score = 89.07%. Table 3 highlights the key features of this article through comparison with other unsupervised models on this dataset reported in literature.

## IV. RESULTS

### A. Anomaly Detection Results

### B. Hardware Implementation

The model architecture described in Section III is implemented on PYNQ-Z2, and the resource utilization report for encoder and decoder blocks is given in Table 4. The model execution time (per inference) on CPU workstation was observed to be 109.3 ms, while the encoder and decoder blocks require 2.1 and 3.8 ms, respectively, on the FPGA, i.e., 5.9 ms, which corresponds to 18.51× speed-up due to hardware acceleration. Due to fixed-point arithmetic implemented on the FPGA, accuracy for the model implemented on the FPGA was found to be 85.02%, which is lower than the CPU implementation. Increasing the number of fixed-point bits will improve accuracy and could be adopted on FPGAs with the higher number of resources. Other models in the 3 were not implemented on PYNQ-Z2 since the model sizes were prohibitively large for edge implementation. Table 5 gives a comparison of this article with other FPGA-based CNN/AE models presented in literature.

## V. CONCLUSION

We report a lightweight CAE model for vibration CBM, with only 8755 trainable parameters, that is able to distinguish vibration signals recorded for anomalous flights from normal flights in the Airbus SAS helicopter accelerometer dataset. The model is implemented on PYNQ-Z2 FPGA board for hardware acceleration with various architecture optimization strategies as described, resulting in a factor of 18.51× speed-up in inference time as compared with CPU workstation, albeit with reduction in accuracy from 88.8% (CPU) to 85.02% (FPGA) due to fixed-point arithmetic implemented on the latter. Various encoding schemes for representing vibration signals as images were studied, and the highest accuracy was observed when the vibration signals are encoded as scalograms computed using Mexican hat wavelet. In future work, we aim to explore strategies to achieve further reduction in the model size, and the development of tools for functional programming of such embedded algorithm implementations, to reduce the development and deployment time for implementing unsupervised CBM systems.

## Figures et tableaux

**Fig. 1.** Time-series inputs are represented as images through suitable encoding, and processed with a CAE comprising of encoder, fully connected, and decoder blocks. When the model encounters anomalous data, the reconstruction error (cross entropy of reconstructed image and original image) exceeds the range of values produced for healthy data.

[figure sans légende identifiée] Convolution, maxpooling, and upsampling functions are called sequentially within each layer in the model, and data are transferred sequentially from one layer to the next using AXI-Stream with added Authorized licensed use limited to: ISAE. Downloaded on September 26,2026 at 17:14:59 UTC from IEEE Xplore. Restrictions apply.

**Fig. 2.** Illustration of line buffer implementation of convolution.

A total of 1677 × 120 = 201 240 images are available in the training dataset, and are sufficient for training of the model. The total number

**TABLE 1.** Summary of CAE Architecture hyperparameters of the CAE that influence the performance are the number of layers in encoder and decoder, number and size of filters, optimizer, number of FC layers, number of epochs used in training, and activation function. This model utilized rectified linear unit activation function and Adam optimizer with learning rate 0.01. [corps du tableau reconstruit par Docling : à vérifier]

    Section | Layer (type) | # kernels | Output size | # parameters
    Encoder | Input_1 Conv_1 max_pool_1 Conv_2 max_pool_2 | 16 | 64 × 64 × 1 64 × 64 × 16 32 × 32× 16 32×32× 8 16 × 16 × 8 | 0 160 0 1160 0
    Encoder |  | 8 | 16×16×4 8×8×4 256 10 | 292
    Encoder | Conv_3 max_pool_3 Flatten | 4 |  | 0 0
    Encoder | Dense_1 Dense_2 |  |  | 
    Encoder |  |  |  | 2570 2816 0
    Fully- Connected (FC) | Conv_4 |  |  | 
    Fully- Connected (FC) |  |  | 256 | 
    Fully- Connected (FC) | Reshape |  | 8×8×4 | 
    Decoder |  | 4 | 8×8×4 | 148
    Decoder | up_sampling_1 |  | 16× 16× 8 | 0
    Decoder | Conv_5 | 8 | 16 × 16× 8 | 296
    Decoder | up_sampling_2 |  | 32×32×8 | 0
    Decoder | Conv_6 | 16 | 32× 32× 16 | 1168
    Decoder | up_sampling_3 |  | 64 × 64× 16 | 0
    Decoder | Conv_7 | 16 | 64 × 64 × 1 | 145
    Total number of trainable parameters | Total number of trainable parameters | Total number of trainable parameters | Total number of trainable parameters | 8755

**TABLE 2.** CAE Model Results for Various Image Encodings [corps du tableau reconstruit par Docling : à vérifier]

    Encoding | # kernels | # nodes in FC layer | Accuracy
    Spectrogram | 32,8,4 | 10 | 80.4 %
    Scalogram | 16,8,4 | 10 | 88.8 %
    MTF | 16,8,4 | 10 | 59 %
    GAF | 32,8,4 | 5 | 62 %

**TABLE 3.** Comparison of This Work With Other Models for Anomaly Detection in Airbus SAS Helicopter Accelerometer Dataset [corps du tableau reconstruit par Docling : à vérifier]

    Reference | Architecture | # trainable pa- rameters | Accuracy
    Garcia et al. [17] | CAE (2 Conv + 1 FC) | >10M | 85 %
    Ducoffe et al. [18] | Generative adversarial network (GAN) | Not specified | 88.11 %
    This work | CAE (3 Conv + 1 FC) | 8755 | 88.8 %

**TABLE 4.** Resource Utilization on PYNQ-Z2 [corps du tableau reconstruit par Docling : à vérifier]

    Resource | Available | Encoder | Decoder
    LUT | 53 200 | 40 403 (75.7 %) | 38 169 (71.75 %)
    FF | 106400 | 37094 (34.8 %) | 39 839 (37.44 %)
    BRAM | 140 | 6 (4.29 %) | 10 (7.14 %)
    DSP | 220 | 82 (37.27 %) | 106 (48.18 %)

**TABLE 5.** Comparison of This Work With Other FPGA Implementations of CNN/AE Models Reported in Literature literature given in Table [corps du tableau reconstruit par Docling : à vérifier]

    Reference | Application | Architecture | Input size | FPGA family/board and performance | Resource utilization
    Zhang et al. [13] | CNN resource optimization on FPGA | 5-layer CNN, 3 FC layers | 224×224× 3 | Virtex-7 VX485T; inference time: 21.6ms; power consumption: 18.61 W | BRAM: 1024, LUT: 186 251, FF: 205 704
    Feng et al. [14] | Remaining useful life estimation (CBM) | 3-layer CNN with 2-layer RNN | 24 × 24× 3 | PYNQ-Z2; inference time: 214 ms; power con- sumption: 1.99 W | BRAM: 134, LUT: 36 520, FF: 21 193
    Zhao et al. [15] | Image compression | CAE with 3-layer CNN | 256× 256× 3 | Kintex Ultrascale KCU105; inference time: 15.73 ms; power consumption: 2.76 W | BRAM: 55.5, LUT: 22 441, FF: 27100
    Sun et al. [19] | Object detection using MobileNet | 12-layer CNN (MobileNet) | 3 × 160 × 360 | Ultra96-V2; inference time: 35.7 ms; power consumption: 6.1 W | BRAM: 210, LUT: 51 508, FF: 57 859
    Maraoui et al. [20] | LeNet-5 model-based traffic sign recognition | 2-layer CNN and 2 FC layer | 32 × 32 | PYNQ-Z1; inference time: 30 ms | BRAM: 167, LUT: 33 816, FF: 27 854
    This work | Anomaly detection in vibration CBM | CAE with 3-layer CNN, 1 FC layer | 64 × 64 | PYNQ-Z2; inference time: 5.9 ms; power con- sumption: 1.85 W (encoder), 1.79 W (decoder) | Described in Table 4
