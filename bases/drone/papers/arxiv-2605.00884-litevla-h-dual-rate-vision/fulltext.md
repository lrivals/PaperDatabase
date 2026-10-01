---
id: arxiv-2605.00884-litevla-h-dual-rate-vision
title: "LiteVLA-H: Dual-Rate Vision-Language-Action Inference for Onboard Aerial Guidance and Semantic Perception"
year: 2026
backend: pymupdf
---

LiteVLA-H: Dual-Rate Vision-Language-Action Inference for Onboard Aerial

Guidance and Semantic Perception

Justin williams * 1 Kishor Datta Gupta 1 Roy George 1 Mrinmoy Sarkar 2

## Abstract

Vision-language-action (VLA) models have shown strong semantic grounding and task generalization in manipulation, but aerial deployment remains difficult because drones require lowlatency closed-loop guidance under strict onboard compute and communication constraints. We present LiteVLA-H, a compact 256M-parameter VLA system designed for dual-rate operation on an NVIDIA Jetson AGX Orin: a fast outer-loop guidance mode for short action-token outputs and a slower semantic mode for scene understanding, hazard description, and operator-facing narration. The central empirical observation is that, in this compact edge regime, end-to-end latency is dominated by multimodal pre-fill rather than by the marginal cost of decoding a few extra tokens. This motivates a scheduler that issues reactive action tokens at 50.65 ms (19.74 Hz) while still supporting sentence-level semantic outputs at 149.90–164.57 ms (6.08–6.67 Hz) on the same embedded platform. To specialize the model without collapsing its descriptive competence, we use a knowledge-preserving fine-tuning recipe that mixes reactive flight data, aerial semantic data, and generic caption/VQA supervision. Beyond reporting current latency measurements, we position the system against recent state-of-theart architectures, including AnywhereVLA, FutureVLA, and ReMem-VLA, showing that the measured action branch reaches a higher edge inference rate under our deployment conditions while retaining periodic semantic awareness.

## 1. Introduction

Vision-language-action (VLA) models unify visual grounding, natural-language conditioning, and action generation inside a single autoregressive policy. Systems such as RT-2 and OpenVLA show that web-scale visual-linguistic pretraining can improve robotic generalization and semantic competence (Brohan et al., 2023; Kim et al., 2025b). At the same time, a fast-growing literature now studies how to

adapt, compress, and accelerate VLAs for real-world control (Kim et al., 2025a; Jiang et al., 2025; Ma et al., 2025; Jiang et al., 2026; Lu et al., 2026).

Aerial robots make this problem sharper. A drone must react quickly to visual change, but it also benefits from higherlevel semantic understanding for obstacle description, runway awareness, scene summarization, and human supervision. Recent aerial systems such as SINGER, VLA-AN, AerialVLA, AIR-VLA, and AirVLA confirm that languagegrounded aerial autonomy is becoming an active research direction (Adang et al., 2025; Wu et al., 2025; Xu et al., 2026a; Sun et al., 2026; Tucker et al., 2026). However, many current results emphasize navigation success, benchmark creation, or server-class inference rather than the practical scheduling problem faced by a compact onboard model: how should the same edge VLA support both reactive guidance and slower semantic reasoning?

This paper studies that question through LiteVLA-H, a compact aerial VLA deployment built around a 256M-parameter multimodal backbone and an edge-oriented inference stack. Relative to the earlier LiteVLA-Edge baseline (Williams et al., 2026), LiteVLA-H makes three technical changes that are central to a stronger systems framework. First, we explicitly separate outer-loop guidance from the low-level flight controller: the VLA produces short-horizon action tokens at approximately 20 Hz, while the onboard autopilot continues to run inner-loop attitude stabilization at conventional high frequency. Second, we characterize latency as the sum of multimodal pre-fill and token decoding, then show that short-output edge inference is pre-fill dominant. Third, we make the training objective more explicit by introducing a mixed loss over action, aerial semantic, and generic caption/VQA data, with an optional knowledge-preserving regularizer.

Our contributions are as follows:

1. We identify a pre-fill-dominant latency regime for compact edge-deployed VLAs and argue that time-to-firstaction is the correct systems bottleneck for aerial guidance.

## 2. We introduce a dual-rate scheduler that supports

19.74 Hz outer-loop action emission while retaining 6.08–6.67 Hz sentence-level semantic perception on one Jetson AGX Orin.

3. We formulate a knowledge-preserving fine-tuning objective that mixes action, aerial semantic, and general multimodal supervision.

4. We provide ablation and comparative analysis against recent robust frameworks (e.g., AnywhereVLA, FutureVLA, ReMem-VLA), emphasizing where the evidence is strongest: onboard timing, scheduler behavior, and the retention–reactivity tradeoff.

## 2. Related Work

### 2.1. VLAs and Real-Time Inference

RT-2 introduced the standard VLA paradigm by representing robot actions as tokens within a vision-language model (Brohan et al., 2023). OpenVLA released a 7B open-source VLA trained on diverse real-world demonstrations (Kim et al., 2025b). Follow-on work examined how fine-tuning choices affect both control quality and runtime; OpenVLA- OFT reported that decoding strategy, action representation, and objective design materially affect throughput and task success (Kim et al., 2025a).

The most relevant recent trend for this paper is the move from merely asking whether a VLA can control a robot to asking whether it can react within a physical deadline. VLA-Perf frames this as a systems problem spanning model architecture, inference runtime, context length, hardware placement, and communication delay (Jiang et al., 2026). Running VLAs at Real-time Speed shows that aggressive runtime optimization can enable high-rate VLA inference on consumer GPUs (Ma et al., 2025), while FASTER argues that reaction latency depends on time-to-first-action and action execution horizon, not only on average model throughput (Lu et al., 2026). LightVLA addresses a complementary bottleneck by pruning visual tokens to reduce attention cost (Jiang et al., 2025). These works motivate separating first-token action latency from longer semantic decoding latency instead of reporting only a single end-toend number.

Recent architectures have also pushed for specialized operational awareness. FutureVLA decouples visual and motor features to extract predictive joint embeddings for temporal continuity (Xu et al., 2026b), while ReMem-VLA utilizes dual-level recurrent queries to enhance memory in long-horizon tasks (Li et al., 2026). AnywhereVLA combines a compact VLA-style interface with mapping and exploration modules for mobile manipulation (Gubernatorov et al., 2025). Our work is complementary: rather than adding memory or prediction modules, we focus on the

short-output, compact-model, embedded-device regime relevant to aerial robotics and exploit the empirical dominance of pre-fill cost through a dual-rate deployment schedule.

### 2.2. Aerial Language-Grounded Autonomy

Several recent works adapt vision-language policies to UAVs. SINGER learns an onboard generalist visionlanguage navigation policy for drones using only onboard sensing and compute (Adang et al., 2025). VLA-AN presents an efficient onboard aerial VLA with a lightweight action module (Wu et al., 2025). AerialVLA studies minimalist end-to-end UAV navigation with continuous control and landing signals (Xu et al., 2026a), while AIR-VLA introduces a benchmark and dataset for aerial manipulation systems (Sun et al., 2026). The related AirVLA transfer work studies how physics-guided adaptation can move VLA policies toward aerial manipulation (Tucker et al., 2026).

The common lesson from this literature is that aerial VLA systems must be both semantically grounded and timingaware. However, most prior work emphasizes navigation success, benchmark construction, or cross-embodiment transfer. In contrast, LiteVLA-H targets a narrower systems problem: managing one compact multimodal backbone on one edge computer across two timescales of inference, where the fast branch must support outer-loop guidance and the slow branch must preserve semantic awareness.

## 3. Problem Formulation and System Design

Let It denote the current RGB observation, xt a compact textual context containing mission state and optional operator instructions, and mt ∈{act, sem} a mode variable. LiteVLA-H implements a prompt-conditioned multimodal policy

yt = fθ(It, xt, mt),

where yt is either a short action-token sequence used for outer-loop guidance or a sentence-level semantic description used for supervision and scene awareness.

### 3.1. Design Objective

The design goal is not to replace a high-rate flight controller. Instead, LiteVLA-H should satisfy two coupled timing constraints:

Tact ≤Bact,

Tsem ≤Bsem,

where Bact is the reaction-time budget for action updates and Bsem is the slower budget for semantic reporting. In our deployment, the fast branch targets approximately 20 Hz outer-loop guidance, while the slow branch targets 6–7 Hz semantic updates.

RGB Camera

Prompt + Context

Telemetry

Vision Encoder Prompt / Projector Shared LiteVLA-H Backbone Dual-Rate Scheduler

Action Decode

1–2 tokens Flight Controller

outer-loop in

Inner-loop stabilization

Semantic Decode

sentence output Safety / Logs / UI

50.6 ms/19.7 Hz

149.9–164.5 ms / 6.1–6.7 Hz

Jetson AGX Orin onboard inference Fast guidance loop

Slow semantic loop

**Figure 1.** LiteVLA-H system diagram. One shared multimodal backbone is queried at two timescales: a fast action mode for outer-loop

guidance and a slower semantic mode for scene awareness, logging, and operator support. The conventional flight controller remains responsible for inner-loop stabilization.

### 3.2. Dual-Rate Scheduling

Let ∆a be the action-query period and ∆s the semanticquery period. The scheduler maintains

∆s = K∆a, K ∈N, K > 1,

with optional event-triggered semantic refreshes when a hazard predicate, confidence drop, or mission-state transition is detected.

### 3.3. Latency Decomposition and Pre-fill Dominance

For an output of n tokens, total latency can be decomposed as

L(n) = P(It, xt, mt) +

n X

i=1

Di,

where P(·) is multimodal pre-fill cost and Di is the cost of decoding token i. The measured regime of interest satisfies

P ≫Di for small n,

which means the system is pre-fill dominant. In our current deployment, P ≈48 ms and the marginal cost of each decoded token is approximately 1–2 ms.

### 3.4. Edge Runtime

LiteVLA-H is deployed on an NVIDIA Jetson AGX Orin with a compact runtime configuration and a truncated context window (nctx = 2048). The current implementation uses FP16 execution for a stable tradeoff between memory footprint and numerical fidelity.

## 4. Knowledge-Preserving Fine-Tuning

We model training as a weighted mixture objective

L = λaLact + λsLsem + λgLgen + λkpLkp,

where Lact is the action loss, Lsem is the aerial semantic loss, Lgen is the generic caption/VQA loss, and Lkp is an

**Table 1.** Training recipe and hyperparameter configurations.

Hyperparameter Value

Backbone parameters 256M Sequence length nctx Precision FP16 λa λs λg λkp Reactive action samples 120,000 Aerial semantic samples 45,000 Generic caption/VQA samples 85,000 Training steps / epochs 50,000 / 10 Batch size Learning rate 3e-4

optional knowledge-preserving regularizer. One practical choice is a distillation term against the pre-specialized backbone,

Lkp = KL (pθ0(· | I, x) ∥pθ(· | I, x)) ,

computed on a held-out generic multimodal stream.

## 5. Experimental Setup

### 5.1. Platform and Deployment Configuration

We benchmark LiteVLA-H on an NVIDIA Jetson AGX Orin under a fixed deployment configuration using the same 256M-parameter backbone, FP16 execution, and context window used throughout the paper. The reported timing focuses on the inference path from prepared image–prompt input to emitted tokens. Full vehicle reaction time also includes camera exposure, sensor transport, flight-controller scheduling, actuator dynamics, and airframe response; those effects are outside the core inference benchmark and should be measured separately for a final flight-safety case.

### 5.2. Evaluation Questions

The experiments are organized around three questions. First, can a compact VLA emit an action token fast enough for onboard outer-loop aerial guidance? Second, can the same model still produce useful semantic descriptions without forcing the action loop to run at the slower semantic rate? Third, does mixed fine-tuning preserve enough general visual-language competence to avoid turning the model into a narrow action classifier?

### 5.3. Metrics

We report five primary metrics. Time-to-first-action (TTFA) is the latency from the start of a model query to the first valid action token. End-to-end semantic latency is the time to produce the complete sentence-level response. Action rate and semantic rate are computed as 1000/T for latency T in milliseconds. Retention score measures whether captioning and VQA-style competence remain after aerial action finetuning.

For the latency analysis, we also report the pre-fill fraction

ρ = P Tact

,

where P is multimodal pre-fill latency and Tact is the measured action latency. A high ρ indicates that optimizing only the number of decoded output tokens will have limited effect on the first-action deadline.

### 5.4. Comparison Protocol

Comparisons to prior VLA systems are used for systemslevel positioning rather than as a perfectly controlled leaderboard. Hardware platforms, task suites, action spaces, and robot embodiments differ across the cited works. Therefore, the key claim of LiteVLA-H is not universal dominance across all robotic settings; it is that, under the reported Jetson AGX Orin deployment, a compact pre-fill-dominant VLA can be scheduled to preserve a high-rate action branch while maintaining a slower semantic branch.

## 6. Results

### 6.1. Measured Edge Latency

**Table 2** reports the current measured latency on Jetson AGX Orin. The main result is the separation between the firstaction deadline and the longer semantic response. The action branch emits a single action token in 50.65 ms, corresponding to 19.74 Hz. In contrast, sentence-level semantic responses require 149.90–164.57 ms, corresponding to 6.08– 6.67 Hz. If semantic generation were forced to run every control frame, the whole system would be capped near the slower semantic rate. The dual-rate design avoids that col-

**Table 2.** Measured inference latency on Jetson AGX Orin.

Task Mode Output Complexity Latency (ms) Rate (Hz)

Reactive guidance Single action token Scene caption Single sentence Guided semantic 2 sentences + action cue Contextual awareness 3 sentences + action cue

**Table 3.** Latency decomposition profiling. Rows are profiling views and are not strictly additive because several subsystem measurements overlap with the pre-fill path.

Component Latency (ms) Notes

Dominant-path measurements Multimodal pre-fill Shared vision-language prompt pass Marginal decoded token Added cost after first response path Post-processing / IPC Zero-copy transfer

Overlapping subsystem profile Vision encoder only Computed via nvprof Projector / prompt pack Linear projection layer First-token decoder path Includes scheduling/cache setup KV-cache update Memory management

lapse by treating action emission as the deadline-critical branch and semantic decoding as a lower-rate background service.

The latency gap is large enough to justify explicit scheduling. The single-sentence caption path is approximately 149.90/50.65 ≈2.96× slower than the action path. The longest contextual-awareness mode is only 14.67 ms slower than the one-sentence caption mode, a 9.8% increase. This pattern supports the pre-fill-dominance hypothesis: once the multimodal prompt has been processed, additional semantic tokens add cost, but the fixed image–language fusion cost remains the dominant systems bottleneck.

### 6.2. Timing Interpretation

Using the measured pre-fill value P = 47.8 ms and action latency Tact = 50.65 ms, the pre-fill fraction is

ρ = 47.8

50.65 ≈0.944.

Thus, about 94.4% of the action-query latency is consumed before useful output-length optimization can matter. This has two practical consequences. First, reducing a one-token action output to a different one-token format will not substantially improve reaction time unless the pre-fill path is also improved. Second, a scheduler that protects the firstaction deadline is more valuable than a scheduler that treats action and semantic outputs as interchangeable requests.

For the selected K = 3 dual-rate configuration, three action periods correspond to 3 × 50.65 = 151.95 ms, which closely matches the observed single-sentence semantic latency of 149.90 ms. This makes the semantic branch naturally compatible with every-third-action-cycle refreshes, provided that semantic jobs are skipped or delayed when-

ever an action deadline is pending. In deployment, this suggests a deadline-first policy: action queries are admitted immediately, while semantic queries are opportunistic and non-blocking.

## 7. Ablation Studies

We evaluate the data mixture, architectural additions from recent literature, and runtime efficiency of the proposed dual-rate scheduler.

### 7.1. Data-Mixture and Knowledge-Preservation

**Table 4** analyzes how generic multimodal rehearsal and knowledge-preserving regularization improve retention without sacrificing action quality.

The data-mixture ablation shows the core retention– reactivity tradeoff. Action-only fine-tuning gives the highest action success in the table, but it reduces retained caption competence to 0.31 CIDEr and aerial semantic F1 to 0.42, indicating severe narrowing of the model. Adding aerial semantic data recovers domain awareness, increasing semantic F1 from 0.42 to 0.81, but still leaves generic caption retention weak. Adding generic caption/VQA rehearsal improves retained captioning from 0.45 to 0.76. The full method reaches 0.82 retained CIDEr while keeping action success within 1.1 percentage points of the action-only variant. This is the desired operating point for LiteVLA-H because the system is designed to act and explain, not merely to emit action labels.

### 7.2. Runtime and Scheduler Analysis vs Recent Frameworks

**Table 5** targets the central systems claim, demonstrating that LiteVLA-H provides higher action rates under the reported deployment configuration than standard single-rate semantic execution and the memory- or prediction-heavy variants considered here.

The runtime ablation highlights why the schedule matters. A single-rate semantic system would run at 6.67 Hz and would therefore underuse the model’s faster first-action capability. The dual-rate configuration preserves the 19.74 Hz action rate while adding semantic updates at 6.67 Hz, with only 0.1 GB additional memory relative to the action-only configuration and a 3.6 W power increase. The ReMem- VLA-style and FutureVLA-style variants improve temporal reasoning capacity, but their additional state, query, or prediction paths raise TTFA in this embedded profile. This does not make memory or prediction unnecessary; rather, it shows that such modules should be activated selectively when the mission requires long-horizon reasoning.

### 7.3. Closed-Loop Evaluation Protocol

Latency alone does not prove flight competence. Table 6 therefore summarizes the closed-loop evaluation protocol and representative results used to compare task success, intervention rate, path deviation, hazard recall, and latency. The hardware rows should be interpreted with care unless all systems are evaluated under the same airframe, payload, controller gains, lighting, obstacle layout, and battery state. The most defensible claim from the current evidence is that LiteVLA-H improves the action-update budget while preserving a semantic channel that can support hazard recall and operator awareness.

## 8. Comparison to Prior Work

**Table 7** positionsLiteVLA-H relative to prior systems, while Table 8 provides quantitative benchmarking against the recent state-of-the-art. The comparison is organized around deployment role rather than only around raw model capability. Large manipulation-oriented VLAs such as RT-2 and OpenVLA demonstrate broad semantic transfer, but they are not designed primarily as compact onboard aerial systems. Memory-augmented and predictive approaches improve temporal reasoning, but they introduce extra computation that may be difficult to justify when the immediate requirement is a first action token within a tight embedded deadline. LiteVLA-H occupies a different point in the design space: compact model, onboard execution, aerial guidance, and explicit dual-rate semantic support.

The quantitative table should be read together with the rolebased table. OpenVLA-OFT reports very strong manipulation performance, but its 7B scale and task domain differ from a compact aerial deployment. AnywhereVLA is the closest edge-oriented comparison, but it emphasizes mobile manipulation with mapping and exploration rather than fast aerial outer-loop guidance. FutureVLA and ReMem-VLA are valuable references because they show how prediction and memory can improve long-horizon behavior; however, their strengths address a different bottleneck than the one measured here. The measured contribution of LiteVLA-H is the ability to preserve a fast action path while keeping the semantic path available at a lower rate.

## 9. Discussion

The inclusion of modular, predictive, and memory-aware baselines highlights the main tradeoff in VLA design: more context usually improves reasoning, but it also increases the amount of computation performed before the robot can react. For aerial robots, this tradeoff is sharper than in many tabletop manipulation settings because visual change can be rapid and the platform cannot safely wait for a long sentence before updating its trajectory. LiteVLA-H handles

**Table 4.** Ablation of training mixture and knowledge-preserving regularization.

Variant Action Success (%) Retained Caption (CIDEr) Aerial Semantic (F1) TTFA (ms) E2E Semantic Latency (ms) Comments

Action-only fine-tuning Severe catastrophic forgetting Action + aerial semantic Strong domain awareness Action + aerial semantic + generic Recovered general capability LiteVLA-H (Full Method) Balanced retention

**Table 5.** Ablation of runtime precision, scheduling strategy, and comparative overhead.

Variant Precision Schedule TTFA (ms) Action Rate (Hz) Semantic Rate (Hz) Memory (GB) Power (W)

Single-rate action-only FP16 Every frame – Single-rate semantic-only FP16 Every frame – Dual-rate periodic (Ours) FP16 K = 3 ReMem-VLA Style Queries (Li et al., 2026) FP16 Every frame – FutureVLA Decoupled (Xu et al., 2026b) FP16 Every frame –

this by separating what must be fast from what can be slower. The VLA is not asked to replace the inner-loop stabilizer; instead, it provides short-horizon outer-loop guidance while a conventional flight controller handles attitude stabilization.

### 9.1. Why Pre-fill Dominance Matters

The latency profile changes how optimization should be prioritized. In a decode-dominant regime, shortening responses, changing the tokenizer, or reducing the number of generated tokens would directly improve speed. In the measured LiteVLA-H regime, the action branch is dominated by image–prompt pre-fill. Therefore, the most promising optimizations are reducing visual token count, caching reusable prompt structure, simplifying projector computation, overlapping image preprocessing with previous control execution, and avoiding unnecessary semantic requests. This also explains why the system can afford periodic semantic outputs: semantic decoding is slower, but it does not need to occur at every action update.

### 9.2. Control and Safety Implications

A key design decision is to keep LiteVLA-H at the outerloop level. The action tokens should be interpreted as velocity, heading, waypoint, or mode-level guidance commands, not direct motor commands. This separation reduces the safety burden on the VLA because timing jitter or a malformed token can be filtered by the downstream controller, command validator, and emergency-stop logic. In practice, a deployment should reject stale action tokens, clamp commands to a vehicle-specific envelope, and fall back to hover, braking, return-to-home, or classical obstacle avoidance when model confidence drops or semantic hazard predicates fire.

### 9.3. Semantic Awareness as a Low-Rate Service

The semantic branch is still important even though it is slower. It can describe obstacles, identify runway or landingzone cues, summarize scene changes for logs, and expose

model reasoning to a human operator. The results suggest that this type of awareness can be refreshed at approximately 6–7 Hz without forcing the action loop to operate at that rate. The semantic output should therefore be treated as a supervisory signal rather than a hard real-time control signal. This distinction keeps the system responsive while preserving the interpretability benefits of a multimodal language model.

### 9.4. Implications for Future Architectures

The comparison with FutureVLA and ReMem-VLA suggests that prediction and memory should not be viewed as replacements for scheduling. They are complementary tools. A future aerial system could activate memory modules only during long-horizon search, relocalization, or occlusion events, while using the lightweight action branch during nominal flight. Similarly, visual-token pruning methods such as LightVLA could reduce the pre-fill bottleneck directly, and VLA-Perf-style modeling could help select the best model–runtime–hardware configuration before flight testing.

### 9.5. Limitations

This study has several limitations. First, the strongest evidence is the onboard inference timing; broader closed-loop flight evaluation is still needed to establish task-level robustness across wind, lighting, motion blur, altitude, payload, and obstacle variation. Second, the comparisons to prior work are not fully controlled because the cited systems differ in embodiment, hardware, benchmark, and action representation. Third, semantic retention is evaluated through proxy metrics and should be validated with human-rated hazard descriptions, failure-case analysis, and out-of-distribution aerial scenes. Fourth, the current action-token interface is best suited for outer-loop guidance; it does not remove the need for classical stabilization, safety monitors, and certified control software.

**Table 6.** Closed-loop evaluation protocol and representative results for simulation and hardware environments.

Benchmark Policy Task Success (%) Intervention Rate Path Deviation Hazard Recall Mean Latency (ms)

Simulated runway navigation Classical baseline 1.2 m – Simulated runway navigation LiteVLA-Edge 0.8 m – Simulated runway navigation ReMem-VLA (Li et al., 2026) 0.7 m Simulated runway navigation LiteVLA-H 0.5 m 50.65 / 149.90

Hardware obstacle course AnywhereVLA (Gubernatorov et al., 2025) 1.1 m Hardware obstacle course FutureVLA (Xu et al., 2026b) 0.9 m Hardware obstacle course LiteVLA-H 0.6 m 50.65 / 149.90

**Table 7.** Positioning ofLiteVLA-H relative to representative prior work.

Method Domain Compact Model Onboard Focus Aerial Semantic Output Closed-Loop Primary Emphasis

RT-2 (Brohan et al., 2023) Manipulation no no no yes yes Generalist VLA with web knowledge transfer OpenVLA (Kim et al., 2025b) Manipulation no no no yes yes Open-source generalist VLA AnywhereVLA (Gubernatorov et al., 2025) Mobile Nav. yes yes no yes yes Modular VLA mapping and exploration pipeline FutureVLA (Xu et al., 2026b) General no no no yes yes Joint Visuomotor prediction & temporal decoupling ReMem-VLA (Li et al., 2026) General no no no yes yes Dual-level recurrent memory queries LiteVLA-H Guidance + semantics yes yes yes yes Partial Dual-rate scheduling under pre-filldominant latency

**Table 8.** Quantitative comparison against state-of-the-art baselines.

Method Params Latency (ms) Rate (Hz) Success (%) Status

OpenVLA-OFT 7B Reproduced AnywhereVLA (Gubernatorov et al., 2025) 450M Reported FutureVLA (Xu et al., 2026b) 7B Reported ReMem-VLA (Li et al., 2026) 7B Reported LiteVLA-Edge 256M Prior baseline LiteVLA-H (action) 256M Measured LiteVLA-H (semantic) 256M – Measured

## 10. Conclusion

We presented LiteVLA-H, a compact dual-rate VLA system for onboard aerial guidance and semantic perception. The central empirical finding is that compact edge-deployed VLA inference is pre-fill dominant: most of the first-action latency is spent before the model decodes useful output tokens. This motivates a deployment strategy in which one model serves two timescales: approximately 20 Hz reactive outer-loop guidance and approximately 6–7 Hz semantic scene interpretation. The broader lesson is that onboard VLA design should report and optimize time-to-first-action separately from sentence-level response latency. Under the measured Jetson AGX Orin configuration, LiteVLA- H shows that a compact model can preserve fast action updates while retaining a useful semantic channel for aerial awareness.

Acknowledgment

This research is supported by the NASA NSPIRES Grant and the Graduate Student Government Association of Clark Atlanta University.
