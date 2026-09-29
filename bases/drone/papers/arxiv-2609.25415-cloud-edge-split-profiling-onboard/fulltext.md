---
id: arxiv-2609.25415-cloud-edge-split-profiling-onboard
title: "Cloud, Edge, or Split? Profiling Onboard and Split Vision-Language Model Deployment for Drone AI"
year: 2026
backend: pymupdf
---

Cloud, Edge, or Split? Profiling Onboard and Split

Vision-Language Model Deployment for Drone AI

Zoha Azimi∗, Reza Farahani†, Schahram Dustdar†, Christian Timmerer∗ ∗Christian Doppler Laboratory ATHENA, Department of Information Technology (ITEC), University of Klagenfurt, Austria

†Distributed Systems Group (DSG), TU Wien, Austria

## Abstract

Vision-Language Models (VLMs) enable edge devices like unmanned aerial vehicles (UAVs) to interpret visual observations and reason about complex environments using natural-language instructions. However, their practical deployment remains challenging as onboard inference is constrained by limited computational, memory, and energy resources, whereas cloud-based inference introduces communication latency, bandwidth overhead, and dependence on network connectivity. To address these limitations, split computing offers a promising alternative by partitioning VLM inference between the resourceconstrained UAVs and more capable remote servers. However, the performance trade-offs among fully onboard, cloud-based, and split-computing architectures for lightweight VLMs have not yet been systematically profiled. This paper benchmarks these three deployment paradigms using SmolVLM-256M as a representative lightweight VLM. We quantify their inference latency, computational resource utilization, communication overhead, and energy consumption across varying image resolutions and network conditions. Our results show that no deployment strategy is universally optimal; instead, the preferred strategy depends on the interaction between network conditions and input image resolution.

Index Terms—Vision-Language Models (VLMs), Unmanned Aerial Vehicles (UAVs), Split Computing, Onboard Inference, Edge Computing, Drone AI.

## I. INTRODUCTION

Vision-Language Models (VLMs) integrate visual perception with natural-language reasoning, enabling systems to interpret complex scenes and answer open-ended queries beyond predefined perception tasks. For Unmanned Aerial Vehicles (UAVs), commonly known as drones, this multimodal capability shifts aerial perception from rigid, task-specific pipelines toward flexible, interactive scene understanding [1], [2]. Consequently, VLMs are gaining attraction in autonomous navigation [3], disaster response [4], and infrastructure inspection [5], where semantic reasoning and intuitive human- UAV interaction are critical [6]–[8]. Despite these capabilities, deploying VLMs on UAVs remains challenging because of their limited onboard computing, memory, energy, and communication resources.

**Fig. 1** shows three representative VLM deployment strategies: 1) fully cloud-based inference, 2) fully onboard inference, and 3) split UAV–cloud inference, each involving distinct tradeoffs in onboard resource utilization, communication overhead, inference latency, and energy consumption.

1) Fully cloud-based inference strategy: The UAV transmits captured images to a remote cloud server, where the entire

- What components are observed? - Are there any defects in the components? - What is the condition of the component?

Three Deployment Strategies

Fully Cloud-Based

Inference Fully Onboard

Inference

Split UAV-Cloud

Inference

VLM

Response

VLM

Response

Vision Encoder + Projection Module

Visual Embeddings Response

Text Decoder

**Figure 1:** Overview of three VLM inference deployment strategies

for UAVs: fully cloud-based, fully onboard, and split UAVcloud inference.

VLM inference pipeline is executed [5], [9]. This strategy leverages abundant cloud resources to support the execution of computationally demanding VLMs [10]. However, imageupload delay contributes directly to end-to-end latency, making performance highly dependent on the availability, bandwidth, and stability of the UAV-cloud connection.

2) Fully onboard inference strategy: The entire VLM pipeline is executed using the UAV’s onboard edge resources [11]–[13], eliminating inference-related communication overhead, preserving data locality, and enabling operation without network connectivity. However, even lightweight VLMs can impose substantial computational, memory, and energy demands on embedded hardware, potentially increasing inference latency and shortening flight endurance.

3) Split UAV-cloud inference strategy: It splits the VLM pipeline between the UAV and a remote server [14], trading onboard resource usage against communication overhead and latency. As illustrated in Fig. 1, the UAV executes the vision encoder locally and transmits the resulting visual embeddings (i.e., latent feature tensors encoding the image content) to the cloud, where the language decoder generates the final response. Compared with fully cloud-based inference, this strategy can reduce communication volume when the embeddings are smaller than the original images. Compared with fully onboard inference, it offloads the language decoder, reducing onboard computation and memory requirements. However, its effectiveness depends jointly on the input resolution, embed-

ding size, onboard encoder performance, and the bandwidth, latency, and stability of the UAV-cloud connection.

Despite prior work on all three strategies, the conditions under which each is preferable for lightweight VLM inference on resource-constrained UAVs remain unclear. Existing studies do not systematically compare their end-to-end latency, onboard resource utilization, communication overhead, and energy consumption under realistic experimental conditions. Moreover, network bandwidth and input image resolution alter the balance between communication and computation, making deployment performance highly context-dependent. To address these gaps, this paper empirically evaluates three lightweight VLM deployment strategies for UAV systems. Using SmolVLM-256 [15] as a representative VLM model, we benchmark fully cloud-based, fully onboard, and split UAV-cloud inference under realistic computing and network conditions. Experiments use an NVIDIA Jetson device as the onboard computing platform, with realistic workloads from a UAV-based power line inspection dataset [16] and the CODE- BRIM bridge-defect dataset [17]. Our results reveal distinct trade-offs in end-to-end inference latency, onboard resource utilization, communication overhead, and energy consumption across network-bandwidth and image-resolution settings. No deployment strategy consistently outperforms the others; the best choice depends jointly on network bandwidth, onboard resource constraints, and input image resolution.

The paper has six sections. Section II describes the VLM inference pipeline and motivates the selected UAV-cloud split point before discussing the related work in Section III. Section IV describes the evaluation methodology and experimental setup. Section V reports and analyzes the empirical results and derives deployment-selection guidelines. Finally, Section VI concludes the paper and outlines future directions.

## II. VLM PIPELINE AND SPLIT INFERENCE

VLMs couple visual perception with natural-language generation by connecting a vision encoder to a language model. Modern lightweight VLMs typically comprise three modules: 1) a vision encoder, 2) a projection module, and 3) an autoregressive language decoder. To clarify this data flow, we annotate each stage with the corresponding tensor shapes produced by SmolVLM-256M [15], [18], which is used throughout our experiments.

1) Vision encoder: SmolVLM-256M employs the Sigmoid Loss for Language-Image Pre-Training (SigLIP) vision transformer [19] as its vision encoder, converting each image into high-level visual features by dividing it into fixed-size patches and modeling their relationships through self-attention. To accommodate its fixed 512 × 512 input resolution, the SmolVLM-256M processor first resizes each source image while preserving its aspect ratio such that its longest edge is 2048 px. The resized dimensions are then adjusted to multiples of 512 px, and the image is partitioned into non-overlapping 512 × 512 tiles. A 512 × 512 thumbnail of the entire image is appended to retain global context. Let r = short/long denote the ratio of the shorter image side to the longer one;

for example, r = 1 for a square image and r = 0.5 for a 2:1 image. The longer edge spans four tiles, while the shorter edge spans ⌈4r⌉tiles. The total number of encoder inputs is then T = 4 ⌈4r⌉+ 1, where the additional input represents the global thumbnail. Under this fixed preprocessing configuration, T depends on the image aspect ratio rather than its original pixel count. For example, a square image produces a 4 × 4 grid and T = 17, whereas a 2:1 image produces a 4 × 2 grid and T = 9. Moreover, all T inputs are processed as a single batch. For each 512 × 512 input, SigLIP generates (512/16)2 = 1024 patch embeddings, each with 768 dimensions. Thus, for one source image, the vision encoder produces an output tensor of shape [T, 1024, 768].

2) Projection module: It maps the encoder features into the language model’s embedding space while compressing the visual sequence. SmolVLM-256M employs pixel shuffle, which combines each s × s block of neighboring patch embeddings into a single representation by concatenating their feature vectors along the channel dimension. This reduces the number of spatial tokens by a factor of s2 while increasing the channel dimension by the same factor, without discarding feature values. With s = 4, each tile’s 32 × 32 × 768 feature grid is rearranged into an 8 × 8 × 12 288 representation, reducing the sequence length from 1024 to 64. A Multi-Layer Perceptron (MLP) then projects each 12 288-dimensional vector to the decoder’s hidden size of 576, producing an output tensor of shape [T, 64, 576]. Thus, each local tile or global thumbnail contributes 64 visual tokens, resulting in 64T visual tokens that replace the corresponding image placeholder tokens.

3) Autoregressive language decoder: SmolVLM-256M employs SmolLM2-135M [20], a lightweight Large Language Model (LLM) with a hidden dimension of 576, to process the combined visual and text embeddings and generate the response autoregressively. Let Ntext denote the number of non-image tokens. Since each source image contributes 64T visual tokens, the decoder input length is Lin = Ntext + 64T. Inference comprises two phases: (i) prefill, which processes all Lin input tokens in parallel and initializes the key-value (KV) cache, with its computational cost largely determined by the input sequence length; and (ii) decoding, which uses the KV cache to generate one token per step, making its latency dependent on the number of generated tokens.

The tensor shapes above determine the communication payload of the selected split point. In this work, the model is partitioned after the projection module, i.e., the vision encoder and projection module execute onboard the UAV, while the language decoder executes in the cloud. A split directly after the vision encoder would transmit a feature tensor of shape [T, 1024, 768], whereas the selected split transmits the projected visual-token tensor of shape [T, 64, 576]. Assuming identical numerical precision and no additional compression, this reduces the number of transmitted values by 1024×768

64×576 ≈ 21, reducing the communication payload by the same factor.

Forest City 1 Mountain City 2

Sand Warehouse Wasteland Industrial Figure 2: Representative frames from the UAV power line inspection

dataset [16], covering forest, urban, mountain, sand, warehouse, wasteland, and industrial environments.

III. RELATED WORK Research on UAV-based VLM systems spans both application and system-level concerns, from enabling aerial perception and reasoning to executing and distributing inference under onboard resource constraints. Thus, we categorize related work into three areas: 1) VLMs for UAV applications, 2) edge AI profiling, and 3) distributed VLM inference. 1) VLMs for UAV applications: Recent works have integrated VLMs into UAV-based systems to enhance perception, reasoning, and human-UAV interaction. Hu et al. [21] introduced LLVM-Drone, a domain-guided prompt-execution framework coupled with lightweight vision models to improve the reliability of language-driven UAV navigation. It translates natural-language instructions into executable UAV commands and visually validates their outcomes. Lelis and Dutta [22] proposed an autonomous emergency-response framework combining UAVs, VLMs, and LLMs, where VLM-generated scene descriptions support victim detection and high-level decisionmaking. Chen et al. [5] developed a VLM-based human- UAV collaboration framework for bridge inspection that combines CLIP-based vision-language understanding with fewshot learning and prompt adaptation. Farahani et al. [23] proposed EVLM, an intent-driven infrastructure monitoring framework that uses a VLM on keyframes extracted from power line video footage for defect and component detection and description. Although these studies demonstrate the potential of VLMs for UAV autonomy, they focus primarily on application-level capabilities and do not examine the systemlevel trade-offs among VLM inference deployment strategies.

2) Edge AI Profiling: The growing computational demands of foundation models have motivated profiling AI inference on resource-constrained edge platforms [24]. Husom et al. [25] evaluated 28 quantized LLMs on a Raspberry Pi 4, measuring inference latency, energy consumption, and task accuracy across different quantization levels to characterize the tradeoffs among model compression, execution efficiency, and output quality. Extending such analysis to multimodal models, Zhan et al. [26] profiled on-device VLM inference across multiple model architectures, input resolutions, and hardware platforms, including the NVIDIA RTX 3070 and Jetson Orin NX. Their analysis quantified the relationships among inference latency, output generation, and energy consumption. Although these works characterize the device-level behavior of foundation models, they consider isolated edge devices

(a) (b) (c)

**Figure 3:** Representative bridge-defect images [17], covering (a)

crack, (b) spallation with exposed and corroded reinforcement, and (c) efflorescence.

under fixed execution configurations and do not capture the system-level trade-offs central to UAV deployment, where computation placement, wireless communication, and onboard energy constraints jointly determine performance.

3) Distributed VLM Inference: To mitigate the computational demands of VLMs, recent works have distributed inference across edge and cloud resources. Li et al. [14] partitioned visual processing onto edge devices and language generation onto centralized servers, improving throughput over cloud-only inference without additional model compression. Qian et al. [27] introduced a cloud-edge context-transfer framework that uses delayed outputs from a large cloud VLM as historical context for lightweight edge inference. Its context-replacement and visual-focus mechanisms improve responsiveness and consistency in real-time visual grounding. Zhang et al. [28] proposed an edge-cloud framework that restricts onboard processing to regions of interest to improve response accuracy. Although these works demonstrate the benefits of edge-cloud collaboration, they focus on specific distributed designs and primarily compare them with cloudonly inference. They do not quantify the collaboration cost relative to both fully onboard and fully cloud inference, leaving it unclear when split inference is preferable.

## IV. EVALUATION METHODOLOGY AND EXPERIMENTAL

SETUP

This section presents our methodology for profiling three deployment strategies for VLM inference. It defines the deployment configurations and evaluation objectives, details the hardware specifications, datasets, inspection prompts, network conditions, and measurement metrics.

A. VLM model and preprocessing configuration

All experiments use SmolVLM-256M [15], a lightweight VLM with 256 million parameters. We retain its default image-processor settings, size={"longest_edge": 2048} and max_image_size=512, and hold them constant across all deployment configurations, ensuring that observed performance differences arise from deployment placement and experimental conditions rather than changes to model preprocessing.

KDE

2000 3000 4000

(a) Image width.

KDE

(b) Image height.

KDE

(c) Image aspect ratio. Figure 4: Kernel density estimates (KDEs) of the spatial dimensions of the 150 selected CODEBRIM images.

### B. Deployment configurations

We evaluate three VLM deployment configurations spanning fully cloud-based, fully onboard, and split UAV-cloud inference, as shown in Fig. 1:

1) Fully cloud-based inference: The UAV captures the image and transmits the image-query pair to the cloud server, where the entire VLM pipeline executes.

2) Fully onboard inference: The entire VLM pipeline executes on the UAV edge computing platform without inferencerelated cloud communication.

3) Split UAV-cloud inference: The vision encoder and projection module execute onboard the UAV, and the resulting visual tokens are transmitted to the cloud server, where the language decoder generates the response.

### C. Evaluation objectives

To compare the three deployment configurations, our evaluation is structured around the following objectives:

1) Deployment characterization: We quantify the inference latency, CPU and GPU utilization, memory usage, and energy consumption of each deployment configuration.

2) Network sensitivity: We determine how variations in network throughput affect communication latency and relative performance, identifying the conditions under which each deployment configuration is preferred.

3) Input resolution sensitivity: We quantify how input image resolution affects transmitted data volume, communication overhead, and the resulting trade-offs among the three deployment configurations.

### D. Edge-Cloud platforms and instrumentation

The edge device, representing the UAV’s onboard computing resources, is an NVIDIA Jetson equipped with an 8-core ARM Cortex-A78AE CPU and an NVIDIA Ampere GPU with 1024 CUDA cores and 32 Tensor Cores. We use a highperformance cloud server running Ubuntu 22.04 LTS, powered by Intel Xeon Gold 5218 processors and accelerated by an NVIDIA RTX A6000 GPU.

On the Jetson, tegrastats [29] samples CPU and GPU utilization, memory usage, and module-level power at 100 ms intervals. Per-request energy is obtained by integrating the measured power over the inference interval. On the cloud server, CPU and DRAM energy are read from RAPL [30]

counters, while GPU energy is calculated by integrating power samples collected through PyNVML [31].

### E. Critical-Infrastructure Inspection Datasets

We use two public datasets for UAV-based power line and bridge inspection tasks. The power-line dataset [16] provides simulated UAV video footage of power lines and transmission towers across forest, urban, mountain, sand, warehouse, wasteland, and industrial environments. We select 70 frames spanning these settings, with representative examples shown in Fig. 2. The concrete defect bridge image (CODEBRIM) dataset [17] contains 1590 high-resolution images depicting concrete defects, including cracks, spallation, exposed and corroded reinforcement, and efflorescence. Representative samples are shown in Fig. 3. Because CODEBRIM provides defect-annotated crops with heterogeneous spatial dimensions, we select 150 samples to evaluate sensitivity to input resolution. Fig. 4 summarizes the width, height, and aspect-ratio distributions of the selected images.

F. VLM inspection prompt workload

To represent common VLM workloads in UAV-based infrastructure inspection, we define 18 natural-language prompts grouped into four semantic categories:

1) Component enumeration: Identification and listing of visible infrastructure elements (e.g., “What components are present?”).

2) Context awareness: Assessment of environmental and operational conditions, including visibility, occlusion, and weather effects (e.g., “Are visibility conditions degraded?”).

3) Defect detection: Identification of structural anomalies and risk factors, e.g., rust, cracks, or broken components (e.g., “Detect rust on metal parts”, “Is any component damaged?”).

4) Localization: Spatial grounding of detected components or defects within the scene (e.g., “Where is the damaged component located?”, “Which segment contains corrosion?”).

Each image is paired with the applicable prompts, and the same image-prompt pairs are used across all deployment configurations to ensure a consistent semantic workload.

### G. Network trace and bandwidth conditions

To quantify the sensitivity of each deployment configuration to network variability, we use a 500 s 4G/LTE HTTP throughput trace [32] to emulate time-varying UAV-cloud

**Table I:** Selected bandwidth intervals and corresponding throughput

statistics (Mbps).

Interval Mean Min Max

Low bandwidth (220 s-250 s) 2.1 10.86 Moderate bandwidth (50 s-80 s) 43.5 26.7 61.50 High bandwidth (380 s-480 s) 34.6 103.03

Throughput (Mbps)

**Figure 5:** Time-varying throughput of the 4G/LTE network trace [32].

connectivity. As shown in Fig. 5, the available throughput varies substantially over time. We select three representative intervals corresponding to low-, moderate-, and highbandwidth conditions, whose mean, minimum, and maximum throughput values are summarized in Table I.

### H. Evaluation Metrics

We compare different strategies using inference latency, communication overhead, resource utilization, and energy consumption. Unless stated otherwise, results are reported as the mean, and the standard deviation is reported across distinct image-prompt pairs.

1) Inference latency: The execution time required to process an image-prompt pair and generate a response, excluding network transfer.

2) Communication overhead: The transmitted payload size and corresponding transfer latency under the bandwidth conditions in Table I.

3) Resource utilization: The CPU and GPU utilization and peak memory usage of the participating compute platforms during inference.

4) Energy consumption: The energy consumed by the participating compute platforms per request, obtained by integrating measured power over the inference interval.

V. EMPIRICAL RESULTS AND ANALYSIS This section analyzes the empirical results according to the objectives defined in Section IV-C. It characterizes the latency, resource, memory, and energy costs of each deployment configuration. It also evaluates sensitivity to network conditions and visual-input characteristics and derives technical guidelines for deployment selection.

### A. Deployment characterization

1) Compute latency: Fig. 6 reports the average inference time of fully cloud-based and fully onboard inference, together with the onboard and cloud stages of split UAV-cloud inference. These measurements exclude network-transfer latency

Fully Onboard

Fully Cloud

Edge

Cloud

Inference-time (s)

0.5

1.5

2.5

**Figure 6:** Average inference time per strategy.

and therefore isolate the execution time of each model stage. Fully onboard inference requires approximately 2.76 s per request while executing the complete pipeline on the cloud reduces this latency to approximately 0.72 s, corresponding to a 3.8× speedup due to the substantially greater computational capacity of the server. Under split inference, the onboard vision encoder and projection module require approximately 1.41 s, while cloud-based language decoding requires approximately 0.68 s. The resulting aggregate compute latency is approximately 2.09 s, which is 24 % lower than fully onboard execution but remains substantially higher than fully cloudbased execution. These results show that offloading only the language decoder reduces the UAV’s computational workload, but the onboard vision pipeline remains the dominant component of split-inference latency.

2) Computational resource utilization and memory footprint: Fig. 7 compares the mean CPU, GPU, and RAM utilization of each deployment strategy. Fully onboard inference utilizes approximately 11 % of the CPU, 55 % of the GPU, and 31 % of system memory. In contrast, fully cloud-based inference uses approximately 2 % of the server CPU, 15 % of its GPU, and 2 % of its memory, reflecting the substantially greater capacity of the cloud platform. Moreover, the onboard stage of split inference shows approximately 69 % mean GPU utilization because its measurement interval contains only the compute-intensive vision encoder and projection module. Its lower RAM utilization of approximately 22 %, however, reflects the removal of the language decoder from the UAV. The higher average GPU utilization of this stage, therefore, does not imply greater total computation; rather, it results from concentrating execution on the vision pipeline.

The GPU-memory measurements in Fig. 8 further demonstrate the effect of model partitioning. Fully onboard execution allocates approximately 572 MB of GPU memory and reaches a peak of approximately 854 MB, while the onboard stage of split inference requires only approximately 236 MB of allocated memory and 472 MB of peak memory. Partitioning after the projection module therefore reduces onboard allocated and peak GPU memory by approximately 59 % and 45 %, respectively. The cloud stage of split inference also has a smaller memory footprint than executing the complete model remotely because it loads only the language decoder and its associated state. These reductions are important for UAV platforms, where GPU memory is shared with other perception, navigation, and control workloads.

Resource Utilization (%)

CPU GPU RAM

Fully Onboard

Fully Cloud

Edge

Cloud

**Figure 7:** Average CPU, GPU, and RAM utilization across the de-

ployment configurations and split-inference stages.

GPU memory (MB)

Allocated memory Peak memory

Fully Onboard

Fully Cloud

Edge

Cloud Figure 8: Average allocated and peak GPU memory across the de-

ployment configurations and split-inference stages.

3) Energy consumption: Fig. 9 reports the compute energy consumed per request at each execution location. Fully onboard inference consumes approximately 26 J from the UAV’s onboard processing. Under split inference, the onboard vision encoder and projection module consume approximately 15 J, reducing the inference-related UAV energy consumption by approximately 42 %. The cloud server consumes substantially more energy per request because it operates a higher-power CPU-GPU platform. Fully cloud-based execution consumes approximately 150 J, while the cloud decoder stage of split inference consumes approximately 130 J. For split inference, the total compute energy is the sum of its onboard and cloud components; however, only the onboard component draws from the UAV battery and directly affects flight endurance. Split inference consequently transfers part of the energy cost from the flight platform to fixed cloud infrastructure.

### B. Network sensitivity

1) Communication overhead: Each deployment strategy imposes a different communication requirement. Fully onboard inference transmits only the generated text response, whereas fully cloud-based inference uploads the JPEGcompressed source image. Split inference instead uploads

Energy consumption (J)

Fully Onboard

Fully Cloud

Edge

Cloud

**Figure 9:** Average compute energy consumption across the deploy-

ment configurations and split-inference stages.

the INT8-quantized visual tokens produced by the onboard projection module. Table II reports the mean payload size and corresponding transfer latency under the bandwidth conditions defined in Table I. Fully cloud-based inference transmits an average of 821.45 kB, compared with 375.84 kB for split inference and approximately 10 kB for fully onboard inference. For the evaluated workload, transmitting quantized visual tokens, therefore, reduces the uplink payload by approximately 54 % relative to transmitting JPEG images.

This reduction is most consequential under low-bandwidth conditions, where the transfer latency decreases from 3.20 s for fully cloud-based inference to 1.47 s for split inference. Under moderate and high bandwidth, the corresponding latencies are 0.155 s and 0.104 s for fully cloud-based inference and 0.071 s and 0.047 s for split inference. Fully onboard inference remains between 0.001 s and 0.040 s because it communicates only a short text response. These results establish a clear sensitivity hierarchy, where fully onboard inference is nearly insensitive to bandwidth, fully cloud-based inference is the most sensitive because image upload dominates communication, and split inference lies between them. However, the communication advantage of split inference is not universal; it depends on whether the projected visual-token payload is smaller than the compressed source image, as examined in the input-resolution analysis.

2) End-to-End latency: Communication latency alone does not determine the preferred deployment strategy. End-toend latency encompasses onboard computation, UAV-to-cloud transfer, and remote computation. As shown in Table III, fully onboard inference achieves the lowest latency under the low-bandwidth condition at 2.77 s, compared with 3.59 s for split inference and 3.87 s for fully cloud-based inference. Its limited communication requirements thus make it the most dependable option when connectivity is constrained or intermittent. Under moderate and high bandwidth, fully cloudbased inference becomes the fastest configuration, achieving 0.83 s and 0.77 s, respectively. At these bandwidths, its faster server-side execution outweighs the image-upload cost. In addition, split inference achieves 2.19 s and 2.17 s, outperforming fully onboard inference at 2.73 s but remaining slower than fully cloud-based inference because it combines onboard visual processing with uplink and remote-decoding latency. The latency-optimal configuration, thus, shifts from fully onboard inference under constrained bandwidth to fully cloud-based inference when sufficient bandwidth is available. Split inference does not minimize end-to-end latency under the evaluated conditions; instead, its principal benefit is balancing lower onboard memory and energy consumption against lower communication overhead than fully cloud-based inference.

### C. Input resolution sensitivity

**Fig. 10** compares the transmission payloads of JPEGcompressed source images with the BF16 and INT8 representations of the projected visual tokens. Unlike the JPEG size, which generally increases with source image resolution, although the exact value also depends on image content and

**Table II:** Mean transmitted payload and transfer latency under the selected bandwidth conditions.

Dep. Strategy Trans. data Trans. Size (KB) Trans. latency (s) Trans. latency (s) Trans. latency (s) (Low BW) (Moderate BW) (High BW)

Fully Onboard Text 0.04 0.002 0.001 Full Cloud JPEG-compressed image 821.45 3.2 0.155 0.104 Quantized visual embeddings 375.84 1.47 0.071 0.047

0.1 0.2 0.3 0.4 0.5 0.6 0.6 0.8 1.2 1.4 1.6 Megapixels Megapixels Megapixels

Transmission Size (KB)

50K

10K

15K

20K

JPEG-compressed image BF16 visual embedding INT8-quantized visual embedding

**Figure 10:** Transmission payload vs. source-image resolution for JPEG-compressed images and BF16 and INT8 projected visual tokens.

**Table III:** Mean end-to-end latency (s) under the selected bandwidth

conditions.

Dep. Strategy Low BW Moderate BW High BW

Fully Onboard 2.77 2.73 2.73 Fully Cloud 3.87 0.83 0.77 3.59 2.19 2.17

compressibility, the visual-token payload takes a finite set of discrete values determined by the number of enoder inputs. Specifically, with r = short/long ∈(0, 1] the short edge spans ⌈4r⌉∈1, 2, 3, 4 tiles, resulting in encoder-input counts T ∈ 5, 9, 13, 17, as described in Section II. For a projected tensor of shape [T, 64, 576], the corresponding payloads are SBF16 = 64T × 576 × 2 = 73.7T kB and SINT8 = 64T × 576 = 36.9T kB. Thus, BF16 produces four possible payload levels of approximately 370, 660, 960, 1250 kB, while INT8 reduces each of these values by half. For low-resolution inputs (below 0.2 megapixel), a compressed JPEG image can be smaller than either visual-token representation, limiting the communication benefit of split inference. As resolution increases, however, the JPEG payload grows substantially, exceeding 20 MB for the largest images in the evaluated dataset, while the projected visual-token payload remains bounded by 1.2 MB (BF16) and 0.6 MB (INT8) at T = 17, regardless of resolution. Split inference, thus, becomes increasingly communication-efficient for high-resolution inputs. Nevertheless, images with similar pixel counts can produce different visual-token payloads when their aspect ratios result in different tile counts.

### D. Deployment selection guidelines

The preferred VLM inference deployment strategy is determined by the end-to-end critical path, not by compute or communication latency alone. Fully cloud-based inference is latency-optimal when its server-side speedup exceeds the image-upload delay; fully onboard inference is preferable

when limited or unstable bandwidth makes communication dominant. Split inference does not minimize latency under the evaluated conditions, but it substantially reduces onboard memory and energy requirements while transmitting less data than fully cloud-based inference. This tradeoff is input-dependent: JPEG payload size varies with image resolution and compressibility, whereas the visual-token payload depends on aspect-ratio-driven tile count and numerical precision. Therefore, fully onboard inference suits connectivity-constrained operation, fully cloud-based inference suits latency-sensitive operation with sufficient bandwidth, and split inference suits UAVs constrained primarily by memory and battery capacity.

## VI. CONCLUSION AND FUTURE WORK

Efficient deployment of VLM inference on resourceconstrained UAVs requires jointly balancing computation, communication, and energy rather than adopting a fixed deployment strategy. This paper established this through empirical profiling of fully onboard, fully cloud-based, and split UAV-cloud inference using SmolVLM-256M. The results show that fully onboard inference is preferable under constrained connectivity, fully cloud-based inference minimizes latency when sufficient bandwidth is available, and split inference reduces UAV-side memory and energy demands at the cost of additional communication and distributed execution. The appropriate strategy, therefore, depends jointly on network throughput, onboard resources, and visual-input characteristics. Future work will incorporate accuracy into these tradeoffs and develop an adaptive runtime orchestrator that dynamically selects the deployment strategy according to network conditions, resource availability, input characteristics, and application requirements.

ACKNOWLEDGMENT

This work was supported by the Austrian FFG EdgeAI- Drone project, the EU ENFIELD project, the Austrian Federal Ministry for Digital and Economic Affairs, the National Foundation for Research, Technology and Development, and the Christian Doppler Research Association. Christian Doppler Laboratory ATHENA: https://athena.itec.aau.at/.
