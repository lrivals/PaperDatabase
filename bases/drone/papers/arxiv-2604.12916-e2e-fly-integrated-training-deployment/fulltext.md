---
id: arxiv-2604.12916-e2e-fly-integrated-training-deployment
title: "E2E-Fly: An Integrated Training-to-Deployment System for End-to-End Quadrotor Autonomy"
year: 2026
backend: pymupdf
---

E2E-Fly: An Integrated Training-to-Deployment System for

End-to-End Quadrotor Autonomy

Fangyu Sun†, Fanxing Li†, Linzuo Zhang, Yu Hu, Renbiao Jin, Shuyu Wu, Wenxian Yu*, Danping Zou*

## Abstract

Training and transferring learning-based policies for quadrotors from simulation to reality remains challenging due to inefficient visual rendering, physical modeling inaccuracies, unmodeled sensor discrepancies, and the absence of a unified platform integrating differentiable physics learning into end-toend training. While recent work has demonstrated various endto-end quadrotor control tasks, few systems provide a systematic, zero-shot transfer pipeline, hindering reproducibility and realworld deployment. To bridge this gap, we introduce E2E-Fly, an integrated framework featuring an agile quadrotor platform coupled with a full-stack training, validation, and deployment workflow. The training framework incorporates a high-performance simulator with support for differentiable physics learning and reinforcement learning, alongside structured reward design tailored to common quadrotor tasks. We further introduce a two-stage validation strategy using sim-to-sim transfer and hardware-inthe-loop testing, and deploy policies onto two physical quadrotor platforms via a dedicated low-level control interface and a comprehensive sim-to-real alignment methodology, encompassing system identification, domain randomization, latency compensation, and noise modeling. To the best of our knowledge, this is the first work to systematically unify differentiable physical learning with training, validation, and real-world deployment for quadrotors. Finally, we demonstrate the effectiveness of our framework for training six end-to-end control tasks and deploy them in the real world.

Index Terms—Quadrotor training framework, sim-to-real transfer, differentiable physics learning, reinforcement learning, reward design.

## I. INTRODUCTION

End-to-end learning has gained increasing attention in quadrotor autonomy by directly mapping raw sensor observations to actuator commands through neural networks [1]–[4]. Unlike conventional modular architectures, which decompose the whole task into sequential modules, such as perception, planning, and motor control, end-to-end policies bypass those intermediate computations, thereby reducing system latency and mitigating error propagation across modules. This datadriven paradigm has demonstrated compelling performance in agile flight [3], [4], obstacle avoidance [5], [6], and high-speed trajectory tracking [7], [8], outperforming traditional modelbased controllers in highly dynamic or uncertain environments. Within this paradigm, differentiable physics learning, which leverages analytical gradients of the quadrotor dynamics for efficient policy training, has demonstrated impressive performance in quadrotor tasks such as hovering [9] and high-speed collision avoidance [10], [11]. By providing exact gradients, it substantially improves learning efficiency and final policy

All authors are with the School of Automation and Perception, Shanghai Jiao Tong University, China (e-mail: dpzou@sjtu.edu.cn).(∗) denotes the corresponding author.(†) denotes equal contribution.

quality compared with black-box reinforcement learning (RL) and standard imitation learning approaches.

Despite recent successes, the practical application of endto-end methods to real-world quadrotors is still challenging. Firstly, training an end-to-end control policy involves choosing appropriate simulators and learning algorithms as well as designing effective rewards for the given task. Secondly, quick and safe validation must be particularly required for quadrotor tasks, as crashes can result in severe damage not only for the vehicle but also for the onboard sensors and computers. Finally, accurate sim-to-real alignment is essential for realworld deployment, including system identification, sensory noise modeling, and control latency compensation. All those factors motivate the development of a system that integrates simulation, learning algorithms, and hardware into a cohesive training-to-deployment pipeline. Such a unified system can substantially accelerate the train-to-deployment procedure, improving the efficiency and safety during debugging and evaluating the trained networks.

Many research platforms for quadrotors have been developed, while only a few of them support training-to-deployment effectively. Agilicious [22] is a co-designed hardware and software research platform for aggressive autonomous flight, featuring a high thrust-to-weight ratio (5g acceleration) and a powerful onboard GPU-based computer (Nvidia Jetson TX). Its modular software stack, including a rendering-based simulator and hardware-in-the-loop support, provides flexibility for both traditional perception–planning–control pipelines and learning-based methods. However, its primary focus lies in enabling high-performance flight rather than offering a thorough workflow for end-to-end policy training or systematic sim-to-real transfer. AirGym [24], in contrast, is specifically designed for RL. It integrates an RL training environment with hardware for validation, employing PX4 for low-level control and an RK3588-based onboard computer. It investigates several practical considerations for successful sim-to-real transfer, such as system identification, action smoothing, and domain randomization. Nevertheless, AirGym does not incorporate differentiable physical learning algorithms and lacks guidance on reward design for common quadrotor tasks and evaluation on different learning algorithms.

While these systems are valuable, there remains a need for a unified framework that integrates advanced simulators, stateof-the-art learning algorithms, comprehensive reward design, and training guidelines for common tasks, and detailed protocols for validation and sim-to-real alignment. Such a system would significantly lower the barrier for developing robust end-to-end quadrotor controllers and provide a consistent methodology for both researchers and practitioners.

**TABLE I:** Key characters comparison of state-of-the-art approaches in this area.

Type Hardware Render Sensors Algorithm Validation Deployment Number of Tasks

Flightmare [12] simulator × Unity D,R,S,I RL HIL × × RotorS [13] simulator × OpenGL D,R,I × × × × CrazyS [14] simulator × OpenGL D,R,I × × × × CrazySim [15] simulator × OpenGL D,R,S,I × × × × FlightGoggles [16] simulator × Unity D,R,S,I × HIL × × FastSim [17] simulator × Unity D,R,S,I,L RL HIL × × AirSim [18] simulator × Unreal D,R,S,I × HIL × × PyBulletDrone [19] simulator × OpenGL D,R,S,I RL × × × OmniDrone [20] simulator × Isaac Sim D,R,S,I,L RL × × × VisFly [21] simulator × Habitat-sim D,R,S,I RL,DS × × × Agilicious [22] platform ✓ Unity D,R,S,I × HIL LC × AirGym [23] platform ✓ Isaac Sim D,R,I RL × SI,DR

E2E-Fly platform ✓ Habitat-sim D,R,S,I RL,DS HIL,sim-to-sim SI,LC,DR,NM

I, R, D, S, and L refer to IMU, RGB, depth, segmentation, and LiDAR, respectively. HIL refers to hardware-in-the-loop validation. RL and DS represent reinforcement learning and differentiable simulation. SI, LC, DR, and NM represent system identification, latency compensation, domain randomization, and noise modeling, respectively. ✓indicates support, × indicates no support. E2E-Fly is a system-level quadrotor platform that provides the entire technical stack from training to validation and to deployment, including a customization parallel training environment, two hardware platforms for offboard and onboard validation, a fast renderer based on Habitat-sim, four types of sensors, sim-to-sim, and hardware-in-the-loop interfaces, algorithms covering RL and differentiable simulation, and four sim-to-real alignment techniques.

To this end, we present E2E-Fly, a unified training-todeployment pipeline designed specifically for developing endto-end control policies for a diverse range of quadrotor tasks. E2E-Fly integrates advanced simulators, state-of-the-art learning algorithms, and comprehensive guidelines for reward design, system identification, and sim-to-real alignment. The platform also provides two reference quadrotor designs for real-world evaluation, together with six representative benchmark tasks that illustrate the full workflow of training, validating, and deploying end-to-end policies using algorithms such as PPO [25] and Back-Propagation Through Time (BPTT) [26].

For the training stage, E2E-Fly adopts VisFly [21], a high-performance differentiable simulator capable of rendering multi-modal sensory observations at high frame rates while providing end-to-end differentiability through the quadrotor dynamics. This enables the use of highly efficient gradientbased learning techniques such as BPTT [26], offering substantially improved sample efficiency compared with blackbox RL such as PPO [25]. To further support policy learning across diverse tasks, we provide structured reward-design guidelines rooted in common principles of quadrotor flight, including progress-based shaping, smooth action penalization, attitude or velocity regularization, and collision-avoidance costs. We also include curriculum-learning examples for obstacle avoidance and racing, demonstrating how progressive task shaping improves convergence and robustness.

Before real-world deployment, E2E-Fly offers two validation stages: sim-to-sim and hardware-in-the-loop. For sim-tosim validation, we extend the AirSim [18] simulator with streamlined, Betaflight-compatible interfaces that expose all core control channels while removing redundant operations. For hardware-in-the-loop validation, E2E-Fly is integrated with a motion-capture system so that real-time pose information from the physical quadrotor drives the simulator, which in turn generates virtual sensory input—allowing the end-toend policy to be executed on a real quadrotor in an obstaclefree environment while interacting with virtual obstacles. This

significantly reduces the risk of damaging hardware during early-stage evaluation.

Finally, to support seamless deployment, we design and release two quadrotor hardware platforms tailored for policies trained with E2E-Fly. Building on these platforms, we develop a four-stage sim-to-real alignment methodology encompassing system identification, latency compensation, domain randomization, and sensor-noise modeling, with the supporting betaflight-ctrl package enabling robust communication and low-level control implementation. The complete pipeline is extensively validated on six benchmark tasks across both hardware platforms.

In summary, E2E-Fly is the first system to unify differentiable physical simulation, first-order gradient-based learning, structured validation, and real-world deployment into a cohesive workflow for quadrotor end-to-end control. To better understand our contributions, we compare E2E-Fly with previous systems in Table I. By providing an integrated stack spanning software and hardware, the platform enables both rapid policy development and reliable physical execution, thereby accelerating research iteration cycles and lowering the barrier to applying end-to-end methods in agile quadrotor flight.

## II. RELATED WORK

### A. Simulators and Platforms for Quadrotors

The development of quadrotor simulators and platforms has remarkably accelerated policy training. Existing systems can be broadly categorized into simulators and integrated softwarehardware platforms.

Among simulators, Gazebo [27] provides a versatile 3D simulation foundation with a powerful physics engine, upon which RotorS [13] offers modular pipelines for verifying state estimators and controllers. Specialized tools like CrazyS [14] and CrazySim [15] deliver software-in-the-loop tests for Crazyflie drones. To enhance visual realism, several simulators, including FlightGoggles [16], Flightmare [12], FastSim [17], and AirSim [18], leverage commercial game engines like

Training Deployment Validation

𝒑𝒕 𝒗𝒕 𝒒𝒕 𝝎𝒕

Learning-based policy

Curriculum

Sim-to-sim AirSim

HIL Vis-HIL node

Hardware Onboard and Offboard Platform

Control Bridge

Finite State Machine

System Init

Auto Ascent

Stable Hover

Policy Ctrl

ROS

Betaflight-ctrl package

/bfctrl/odom

/camera/image

Sub

𝐓𝟏

𝐓𝟐

𝐓𝟑

𝐓𝟒

Dynamics

Image

State

Differentiable simulator VisFly

Training

Motion capture, Sensors

Sim-to-real Alignment

Latency Compensation System Identification

Noise Interference Domain Randomization

Input

Algorithm

Reinforcement Learning Differentiable Learning

Deployment

**Fig. 1:** The overview architecture of E2E-Fly. In the training phase, the state-based and vision-based inputs are acquired from VisFly. During this process, the reward function is designed according to the reward function manual, while the accurate dynamics model supports training both via RL and differentiable simulation. The trained policy can be directly transferred to AirSim via an internal interface for cross-platform sim-to-sim test. In the real-world deployment phase, we provide two quadrotor hardware platforms that support real-time hardware-in-the-loop simulation and onboard flight test, respectively. The transfer from policy outputs to low-level control commands is achieved through our open-source betaflight-ctrl package.

Unity and Unreal. PyBulletDrone [19] and OmniDrone [20] prioritize physics computation speed for parallel RL training. VisFly [21], built on Habitat-Sim [28], further supports highspeed rendering, differentiable simulation, and end-to-end policy training. In terms of integrated software-hardware platforms, Agilicious [22] provides an open-source, co-designed quadrotor platform by integrating high-performance computing units with agile flight hardware and offering a modular software stack. AirGym [23] integrates hardware, a simulator, and a deployment chain to validate RL-based sim-to-real transfer on physical systems.

Collectively, these contributions have significantly advanced the field. However, they exhibit three limitations: (1) a focus on either simulation fidelity or hardware integration, but rarely both, (2) insufficient support for differentiable physical learning within a unified workflow, and (3) fragmented or underspecified sim-to-real alignment techniques. Consequently, the community still lacks a fully integrated platform that enables systematic sim-to-real transfer, supports diverse learning paradigms, and facilitates zero-shot policy deployment across various tasks.

### B. Reward Function Design for Quadrotors

The design of the reward function critically governs the performance of learned policies by defining the solution space of the optimization problem. Despite the diversity of quadrotor tasks, effective reward structures often share key insights about stability, agility, and perceptual awareness.

Traditional learning-based approaches often decompose rewards into sparse and dense formulations. Sparse rewards, such as binary success-failure signals, offer straightforward design principles but suffer from low sample efficiency, challenging exploration requirements, and inherent non-differentiability [29], [30]. In contrast, dense rewards provide incremental guidance by penalizing state deviations or incentivizing task progress [31], [32], while maintaining temporal consistency and differentiability. For most quadrotor

control tasks, sparse and dense rewards can be used together. Zhao et al. [33] employ a dense velocity-tracking reward alongside a sparse penalty for hazards and errors to guide the agent in adaptive flight through obstacle-aware environments. Xie et al. [34] use a dense position reward together with a sparse gap-angle constraint to guide the drone through a narrow gap. In autonomous drone racing [31], [32], [35], [36], training typically employs a high-weighted progress reward, a substantial crash penalty, and a sparse success reward to encourage rapid traversal of the gate while avoiding collisions. Some studies also leverage dense–sparse reward combinations to tackle complex dynamic tasks, such as traversing swinging circles [37], [38], flying through dynamic gaps [39], and performing dynamic obstacle avoidance [10].

Despite these isolated achievements, no systematic guideline for reward design exists. Current approaches rely heavily on heuristic tuning and expert knowledge, indicating a clear need for a structured methodology that abstracts common insights across a wide range of quadrotor tasks.

### C. Sim-to-Real Alignment for Quadrotors

Sim-to-real refers to the process of safely and efficiently transferring algorithms developed in simulation to the real world. Eliminating the gaps between simulated and real environments is the main challenge for algorithm deployment. These gaps mainly stem from the dynamic discrepancies, latency, and observation noises that are difficult to calibrate.

In recent years, numerous approaches have been introduced to narrow the sim-to-real gap. Among these, domain randomization [40]–[45] has been empirically shown to be one of the most effective techniques. Randomly varying physical parameters and adding sensor noise during training encourages the deep network to learn robust features that generalize across sim-to-real discrepancies. In parallel, system identification [22], [46], [47] has been developed to compensate for dynamic inaccuracies and latency. These approaches incorporate measured real-world system parameters into the simulation,

effectively reducing dynamics-induced mismatches. To address noise introduced by visual inputs, researchers propose specialized solutions tailored to optical flow [11], RGB image [48], and depth map [49], respectively. Beyond these, Dionigi et al. [50] investigate how the design of the observation space in quadrotor control policies influences sim-to-real transfer, thereby filling a gap in understanding the role of input. Chen et al. [51] identify several points that influence quadrotor policies transfer, including training randomization and appropriate parameter identification. Building upon these insights, we further establish a comprehensive framework for minimizing the sim-to-real gap by combining system identification, latency compensation, domain randomization, and noise modeling into a complete and detailed solution.

## III. SYSTEM OVERVIEW

The architecture of our E2E-Fly is illustrated in Fig. 1. During the training phase, the policy receives image and state observations from VisFly, supported by reward design, accurate and differentiable quadrotor dynamics, and curriculum learning, thereby enabling training through both RL and differentiable physical learning algorithms. In the validation phase, the trained policy can be directly evaluated through the simulator’s internal interfaces, including sim-to-sim transfer and hardware-in-the-loop test. For real-world deployment, sim-to-real alignment is achieved through system identification, latency compensation, domain randomization, and noise modeling. Finally, the policy is deployed onto the hardware platform, where the betaflight-ctrl package converts policy commands into low-level control signals, thereby completing an end-to-end pipeline for policy training, validation, and deployment.

The structure of this paper is as follows. Sec. IV details the training pipeline, including the simulator, learning-based algorithms, reward design formats for quadrotor tasks, and curriculum learning. Sec. V demonstrates the policy validation framework, covering both sim-to-sim transfer and hardwarein-the-loop simulation. Sec. VI covers real-world deployment, introducing the hardware platform, low-level control bridge, and four concrete alignment techniques for sim-to-real transfer. Sec. VII validates the effectiveness of the proposed system through six comprehensive benchmark experiments. Sec. VIII discusses the comparative advantages and disadvantages of RL and differentiable simulation, along with strategies for combining their strengths.

## IV. TRAINING

This section focuses on the training methodology, detailing the simulator, learning-based policy training, general-purpose reward design for quadrotor tasks, and curriculum learning.

### A. Fast Rendering Simulator: VisFly

VisFly [21] is a versatile quadrotor simulator that enables parallel multi-agent training with synchronized multi-modal perception (RGB, depth, segmentation) and high-frequency state/IMU data. Leveraging Habitat-sim’s rendering engine [28], it achieves up to 6000 FPS at 256×256 depth resolution.

Built on a fully differentiable dynamics model implemented in PyTorch, it supports analytical gradients and GPU-accelerated physics, facilitating differentiable physics algorithms. The framework provides interfaces for RL and differentiable simulation, enabling efficient parallel training for advanced quadrotor tasks. It incorporates four established control interfaces: single-rotor thrust, mass-normalized collective thrust and body rates (CTBR), position and yaw, and linear velocity and yaw. In the subsequent section, we primarily employ the CTBR as the policy output, as it has been proven [52]–[54] to be one of the optimal low-level control commands for a quadrotor’s end-to-end tasks.

The initial version of VisFly is limited to simulation-based training, whereas our enhanced framework integrates sim-tosim and hardware-in-the-loop validation, and a betaflight-ctrl interface. We have further integrated a comprehensive set of sim-to-real alignment techniques into VisFly, including system identification, latency compensation, domain randomization, and noise modeling. These additions support zero-shot policy deployment in minutes via rostopic, providing complete sim-to-real workflows for learning-based policies. The specific implementations of betaflight-ctrl package, sim-to-sim, hardware-in-the-loop simulation, and sim-to-real alignment will be detailed in Sec. VI-B, Sec. V-A, Sec. V-B, and Sec. VI-C.

### B. Policy Training Algorithm

1) Reinforcement Learning: We formulate the quadrotor control task as an infinite-horizon Markov Decision Process (MDP), defined by the tuple (S, A, P, R, γ). The state space S and the action space A are continuous. The state transition function P : S × A →S, describes the system dynamics, determining the next state via st+1 = P(st, at). The reward function R : S × A →R assigns an immediate reward rt = R(st, at) at each time step. The objective function is defined in Eq. 1.

J (θ) = Es0∼ρ0,at∼πθ(·|st)

" ∞ X

t=0

γtR(st, at)

where J (θ) represents the expected discounted return, s0 is sampled from the initial state distribution ρ0, st ∈S, at ∈A, and γ ∈[0, 1) denotes the discount factor. The goal is to learn an optimal policy π∗

θ with parameters θ that maximizes J (θ) from the initial state distribution. The optimization objective is thus defined in Eq. 2.

π∗

θ = argmax

πθ

J (θ)

When the policy is optimized via gradient ascent, the parameters are updated according to Eq. 3.

θt+1 ←θt + α∇θJ (θ)

where α is the learning rate, ∇θJ (θ) represents an estimate of the policy gradient. If the reward function and dynamics model are differentiable, we can compute an accurate gradient via differentiable simulation.

2) Learning via Differentiable Simulation: BPTT [26] leverages first-order gradients within differentiable simulation, enabling precise computation of the gradient as expressed in Eq. 4.

∇θJ (θ) =

N−1 X

t=0

γt ∂R(st, at)

∂θ

!

where N represents the length of the horizon. The analytic first-order gradient can be computed via backward chain propagation, as shown in Eq. 5.

∇θJ (θ) =

N−1 X

t=0

γt

X

i=1

∂R(st, at)

∂st

tY

j=i

 ∂sj

∂sj−1

 ∂si

∂ai

∂ai

∂θ

+

N−1 X

t=0

γt ∂R(st, at)

∂at

∂at

∂θ

For quadrotors, the transition function is governed by the differential dynamics ˙st = P(st, at). In practical implementation, this continuous process is discretized into a time-stepped evolution of the system, expressed as st+1 = st+P(st, at) dt.

Compared with the estimated gradient in Eq. 1, BPTT achieves faster convergence and higher sample efficiency by using analytic gradient, making it particularly well-suited for continuous control tasks in robotics with accurate dynamics and differentiable rewards.

3) Quadrotor Dynamics: We employ a fully differentiable quadrotor dynamics [21] as the state transition function ˙st in Eq. 6.

˙st =





˙pW

˙qt ˙vW

˙ωt



=





vW

qt ·

 0

ωt/2



m

 

RW B

 

f T

t + f D



+ g J−1  

τ T

t + τ D

t −ωt × Jωt







where m and J are mass and diagonal moment of inertia matrix, pW

and vW

are the position and velocity vector in the world frame, unit quaternions qt with ||qt|| = 1 are used to represent orientations, RW B

is the rotation matrix from the body frame to the world frame, ωt represents angular velocity in the body frame. g = [0, 0, −9.81]T denotes the gravity vector. f T

and τ T

denote the collective thrust in the body-z axis and cumulative body torques produced by the rotors, as shown in Eq. 7.

f T

t =

X

i

f i

t, τ T

t =

X

i

(τ i

t + ri × f i

t)

where f i

t and τ i

t are the thrust and torque generated by motor i, and ri is the arm length of the force.

We employ quadratic functions to model the relationship between the thrust and torque generated by a single motor and its rotational speed Ωt, as shown in Eq. 8.

f i

t =





kf0 kf1 · Ωt kf2 · Ω2



, τ i

t =





kτ0 kτ1 · Ωt kτ2 · Ω2





where kf0,kf1, kf2 and kτ0,kτ1, kτ2 represent the parameters for the two quadratic functions, respectively. The motor is

simulated using a first-order system. The dynamic equation for each motor is defined in Eq. 9.

˙Ωt = kmotor (Ωcmd

−Ωt)

where kmotor is the motor time constant, Ωcmd

is the commanded rotor speed. Air drag force f D

and torque τ D

are also modeled for aggressive motion. It is worth noting that our estimation of drag is precise to both the first-order and second-order drag coefficients shown in Eq. 10.

f D

= kD ◦vB

t ◦vB

where vB

represents the velocity in the body frame, kD is the coefficient of second-order drag simulating the friction drag at high speeds. The simulation of the drag component is crucial for our system to achieve stability at low speeds and aggressiveness at high speeds.

### C. Reward Design for Quadrotor Tasks

The efficacy of learning-based controllers is fundamentally governed by the reward function, which shapes the policy’s behavior by defining the optimization landscape that guides its actions. To establish a systematic methodology, this section presents a comprehensive reward design framework encompassing both dense and sparse formulations, with all parameters λi assumed positive unless specified otherwise. It should be noted that the reward functions in this section are denoted directly without unified normalization.

Dense Rewards: Dense rewards provide continuous, differentiable learning signals essential for policy optimization, particularly when leveraging BPTT via differentiable simulation. These formulations enable stable gradient-based learning across the state-action space.

a) Progress: The fundamental objective for a quadrotor in most tasks is to progress toward a desired target. In traditional paradigms, this objective is typically achieved through waypoint tracking or the execution of motion primitives. In learning-based frameworks, the same behavior is formulated as a progress reward, which motivates the policy to move toward the goal. A widely adopted formulation for this reward [32] is given by Eq. 11.

= λ1 · ∥dt−1 −dt∥

This reward promotes swift flight toward the goal by incentivizing a reduction in distance to the target. We usually use a significant positive parameter λ1 to make it a leading term during aggressive tasks. Where dt represents the distance between the drone’s position pt and goal position gt defined in Eq. 12.

dt = ∥pt −gt∥

More directly, the agent is rewarded for reducing the distance to the goal, thereby promoting proximity to the target, as formulated in Eq. 13.

= −λ2 · ∥dt∥

For tasks with stability requirements like hovering and landing, it’s beneficial to decouple rewards for the xy-plane and zaxis displacements. This aligns with control architectures that require independent steering. Accordingly, we design a planar progress reward rprogxy

(Eq. 14), alongside individual axis-wise rewards rprogx

, rprogy

, rprogz

(Eqs. 15-17) for precise independent control.

= −λ3 · ∥dxy

t ∥

rprogx

= −λ4 · ∥dx

t ∥

rprogy

= −λ5 · ∥dy

t ∥

rprogz

= −λ6 · ∥dz

t ∥

b) Smooth Action: A penalty on action changes is imperative for smooth control. This practice, similar to minimizing control derivatives in traditional optimization. With a normalized action u, such a penalty typically takes the form of an action smoothness cost, as exemplified in Eqs. 18 and ract1

= ∥ut∥

ract2

= ∥ut −ut−1∥

where ut represents the policy output, ract1

and ract2

are used to punish the current action and two consecutive actions, respectively. We use Eq. 20 to combine these two rewards to encourage a smooth trajectory.

ract3

= −(λ7 · ract1

+ λ8 · ract2

)

c) Orientation: The quadrotor’s orientation is critical in perception-aware tasks [2], [8], [33], because it directly influences perception quality and mission success. In these scenarios, simply tracking a positional trajectory is inadequate. The orientation must be independently planned to maintain optimal target visibility, ensure feature observability, and satisfy dynamic constraints. This requirement is inherently supported by the differential flatness property [55], [56] of quadrotor dynamics. Consequently, a common method for encouraging orientation alignment is to employ a yaw angle-based error, as defined in Eq. 21.

rori1

= λ9 · exp(−ψe

t )

where the ψe

t is the relative yaw angle between the quadrotor and target. An exponential decay is chosen to ensure high sensitivity to angle variations. Another way is to penalize the quaternion error to align the orientation directly, as shown in Eq. 22.

rori2

= −λ10 ·

qt −qdes

where qdes

is the desired orientation of the next target. In [57], the author uses a perception-aware reward to maximize the visibility of the next goal, as shown in Eq. 23.

rori3

= λ11 · exp(−

u2

t + v2

t + ˙u2

t + ˙v2

t )

)

where (ut, vt) and ( ˙ut, ˙vt) represent the pixel position and velocity of the next target in the image plane of the camera.

In specialized maneuvers, such as traversing a narrow gap, the quadrotor must align its roll angle with the gap. The

corresponding reward that enforces this specific alignment is formulated in Eq. 24.

rori4

(

−min (tan |ϕe

t| , λ12) approaching gap otherwise

where ϕe

t is the relative roll angle between the quadrotor and the gap.

d) Linear Velocity: Maintaining controllable flight in perception-aware and stability-critical tasks necessitates explicit constraints on the quadrotor’s linear velocity. We provide two approaches: the first directly penalizes linear velocity to suppress aggressive motion, as formalized in Equation 25; the second employs reference-guided principles to enforce adherence to a predefined speed profile through reward shaping, implemented via Equations 26 and 27.

rv1

t = −λ13 ∥vt∥

rv2

t = −λ14 · (∥vt∥−vd)

rv3

t = −λ15 · (exp(∥vt∥−vd) + 1)

where the scalar vd denotes the desired speed magnitude. Unlike the linear penalty in Eq. 26, Eq. 27 introduces an exponential term that grows rapidly when the velocity exceeds vd. By introducing a +1 offset, a baseline penalty is maintained even when the target velocity is not exceeded. This asymmetric response effectively suppresses aggressive flight tendencies, proving particularly beneficial for scenarios requiring stable operation.

High-stability tasks, including hovering and landing, require independent regulation of vertical velocity, coordinated with the quadrotor’s height to ensure a safe, controlled approach to the ground. This specific functional dependency is formulated in Eq. 28.

rvz

t = λ16 · 1 + |vh t + vz

t |

where the vz

t is the z-axis velocity of the quadrotor. The desired adaptive landing velocity vh

t is defined in Eq. 29.

vh

t = (α · dz

t ). clamp(vmin, vmax)

where α is the velocity coefficient, dz

t denotes the height of the quadrotor above the ground, vmax and vmin represent the maximum and minimum descent velocity, respectively.

e) Angle Velocity: To suppress high-frequency oscillations and ensure stable attitude control, a penalty on angular velocity is recommended. This formulation is especially pertinent when the policy generates CTBR commands, as it directly regularizes the actuation signal, implemented in Eq. 30.

ranglev

= −λ17 ∥ωt∥

f) Collision Avoidance: Collision avoidance is fundamental to autonomous drone navigation in cluttered or dynamic environments. To this end, the reward structure must incorporate mechanisms that actively discourage proximity to obstacles and other agents. We thus formulate collisionavoidance reward terms that penalize unsafe distances, promoting evasive maneuvers before a possible collision. Among

these, Eq. 31 adopts an inverse-distance formulation, providing a computationally efficient and interpretable means of enforcing safety margins.

ravoid1

= λ18

 dcol

+ b



where dcol

represents the distance to the nearest obstacle, and b is a small positive constant to prevent division by zero. Eq. 32 presents a more refined formulation [10], integrating both distance-based and velocity-dependent terms:

ravoid2

= −∥vc

t∥max

 

1 −(dcol −rq), 0

2

+ λ19 ln(1 + exp(λ20(dcol

−rq)))

where vc

t is the approach velocity toward the nearest obstacle and rq is the quadrotor’s radius. The reward combines a truncated quadratic potential and a soft-plus barrier, scaled by approach velocity. This velocity scaling ensures the penalty is active only during approach, with the penalty increasing as the approach speed increases to promote timely deceleration.

Sparse Reward: To guide the agent toward successful task completion, sparse rewards are provided upon reaching each target, while penalties are imposed for crashes. These eventdriven signals are inherently sparse and non-differentiable, serving as critical terminal feedback for policy optimization.

g) Goal and Crash: The sparse rewards for achieving the goal and for crashes are shown in Eqs. 33 and 34.

rgoal

(

λ21 arrive the goal otherwise

rcrash

(

−λ22 collision occur otherwise

The experiments in Sec. VII employ the reward design methodology outlined in this section to formulate each taskspecific reward and accomplish the tasks. Table II summarizes the proposed reward function formulations for key foundational tasks considered in this work.

**TABLE II:** The reward design instruction for different types of tasks.

Alg. Task

rprog

+ ract

t + rv

t + ranglev

+ rgoal

+ rcrash

rprog

+ ract

t + rv

t + ranglev

+ rgoal

+ rcrash

rprog

+ ract

t + rori

t + rv

t + ranglev

+ rgoal

+ rcrash

rprog

+ ract

t + rgoal

+ rcrash

Obstacle avoidance rprog

+ rori

t + rv

t + ranglev

+ ravoid

+ rgoal

+ rcrash

rprog

+ ract

t + rori

t + rv

t + ranglev

rprog

+ ract

t + rv

t + ranglev

rprog

+ ract

t + rori

t + rv

t + ranglev

rprog

+ ranglev

+ rv

Obstacle avoidance rprog

+ rori

t + rv

t + ranglev

+ ravoid

The table above provides the reward function designs for all experiments in this paper, with each reward term derived from the reward function manual in the methodology section. This design instruction serves as the standard for the subsequent experimental section.

### D. Curriculum Learning

Based on task complexity, we employ distinct training strategies. For fundamental tasks such as hovering and landing, a direct one-step training paradigm proves effective. In contrast, complex scenarios such as high-speed obstacle avoidance or navigation in densely cluttered environments often cause agents to converge to local optima under one-step training. To address this limitation, we implement a structured curriculum learning strategy that progressively guides the agent through increasingly challenging sub-tasks.

For example, training for high-speed collision-free flight in complex environments begins with simple point-to-point navigation without obstacles. Through sequential curriculum stages, both environmental complexity and flight speed are systematically increased. We demonstrate that with appropriate curriculum design and parameterization, such environmental variations do not hinder the agent’s ability to master individual sub-tasks or the overall objective. Table III summarizes specific curriculum designs for representative complex tasks, illustrating this progressive learning approach.

**TABLE III:** The examples of curriculum designs for complex tasks.

Task Curriculum Design

High speed obstacle avoidance

C1: obstacle-free point navigation C2: sparse obstacle navigation C3: high-speed collision-free flight

Racing with random obstacles

C1: obstacle-free racing C2: sparse obstacle racing C3: dense obstacle racing

C1, C2, and C3 represent curriculum 1, curriculum 2, and curriculum 3, respectively.

## V. VALIDATION

This section presents two complementary strategies for policy validation: cross-simulator (sim-to-sim) transfer and hardware-in-the-loop simulation.

### A. Sim-to-sim: From VisFly to Airsim

Direct transfer of control policies trained in a single simulator to physical quadrotors poses significant risks, particularly for aggressive maneuvers where unavoidable sim-to-real gaps in aerodynamics, system dynamics, latency, and sensor noises can critically compromise performance. To mitigate these challenges, sim-to-sim validation serves as an intermediate step, enabling verification of policy logic consistency, assessment of generalization capability under varied dynamics, and identification of simulator-specific biases before real-world deployment. This progressive verification strategy substantially enhances policy robustness while systematically reducing the sim-to-real gap.

We implement a cross-simulator validation framework that transfers policies trained in VisFly to AirSim before real-world deployment. AirSim [18], an open-source simulator built on Unreal Engine, offers high-fidelity physics and photorealistic sensor simulation. Our framework establishes a direct interface between VisFly and AirSim, enabling policy evaluation under

identical control logic across simulators. We further develop an AirSim-compatible version of the betaflight-ctrl package that maintains all core control interfaces while eliminating redundant remote operations. This integration allows policies to be validated in AirSim without modification, ensuring consistency throughout the sim-to-real pipeline.

### B. Hardware-in-the-loop simulation: VIS-HIL node

Hardware-in-the-loop simulation integrates physical quadrotor hardware into a simulated visual environment, forming a real-time closed-loop system that enables rigorous validation of control and perception algorithms under realistic yet safe conditions. This approach is particularly critical for perception-aware agile flight, where real-world testing not only imposes safety risks but also exposes vulnerable onboard sensors and computing units to potential damage during aggressive maneuvers. To address these challenges, the E2E-Fly framework implements this paradigm by operating a physical quadrotor within a motion-capture system while rendering photorealistic virtual scenes, building upon prior work [16]. Unlike purely synthetic simulations, this approach preserves the authentic dynamics and proprioceptive sensing of the real vehicle, while facilitating testing in arbitrarily complex and visually rich scenarios—all without incurring physical collision risks [22]. Consequently, it significantly accelerates the development cycle for vision-based agile flight systems by mitigating the safety and cost constraints inherent in physical testing.

Simulator Real World

Quadrotor Position and Attitude

Real-time Image Input

Photorealistic Environment : VisFly Images: RGB, Depth, Semantic Segmentation Physical Platform: VIS-H Motion Capture System: Vicon

**Fig. 2:** The hardware-in-the-loop simulation in E2E-Fly. It consists of a real quadrotor flying in a motion capture system combined with a photorealistic simulation of complex 3D environments. Multiple sensors can be simulated with minimal delays while virtually flying in various simulated scenes. Such hardware-in-the-loop simulation offers a modular framework for prototyping robust vision-based algorithms safely, efficiently, and inexpensively.

To implement hardware-in-the-loop verification within E2E- Fly, we developed a dedicated simulation node, VIS-HIL, which synchronizes the real quadrotor with its simulated counterpart. The node subscribes to the quadrotor’s real-time pose via rostopics, aligns it with the corresponding coordinate frame in VisFly, and generates simulated visual observations that match the physical pose. These visual data, published at a configurable frequency (30Hz by default), serve as inputs for policy inference, while the quadrotor’s state and dynamics are measured directly from the motion capture system and IMU. The VIS-HIL node supports multiple visual modalities,

including RGB, depth, and semantic segmentation, enabling flexible evaluation of perception-based control policies under realistic and controlled conditions.

## VI. DEPLOYMENT

In this section, we present a comprehensive methodology for deploying trained policies onto physical quadrotors, encompassing two distinct hardware platforms, a low-level control bridge, and a complete four-stage sim-to-real alignment framework.

### A. Quadrotor Platform

We design two quadrotor platforms, VIS-Real (VIS-R) and VIS-Hardware-in-the-loop (VIS-H), for both onboard and offboard real-world experiments. The structures are based on frame OddityRC, illustrated in Fig. 3.

Intel D435i

3.5 inch Propeller

Wireless Data Transmission

Height:7cm

Betaflight F722 Radax x4

**Fig. 3:** Proposed quadrotor platforms: VIS-R and VIS-H. VIS- R is used for onboard experiments with a Radax X4 and an Intel D435i RGB-D camera. VIS-H supports offboard and hardware-inthe-loop experiments via a wireless data transmitter and a wireless video transmitter.

The VIS-R integrates a Radax X4 onboard computer with an Intel N100 processor, capable of executing real-time inference for lightweight neural networks. It is further equipped with a front-facing Intel RealSense D435i stereo camera for synchronized RGB-D perception. In contrast, the VIS- H adopts an offboard processing architecture, utilizing a wireless data link and an FPV camera to stream images and receive control commands from a ground station in real time. This design enhances operational safety during initial tests of aggressive maneuvers by isolating high-value computing hardware from potential crash damage. Furthermore, the VIS- H’s communication architecture enables its use in hardwarein-the-loop experiments, where it can interface with a highfidelity simulator while leveraging ground-station resources to execute larger-scale models in real time.

To enhance the agility and maximum speed, the masses of VIS-R and VIS-H are 750g and 470g (excluding the battery). The flight controller utilizes the Betaflight-compatible STM32F7-based Mini flight controller, paired with 3000KV motors and 3.5-inch D90s propellers. Comprehensive system identification parameters, including detailed electromechanical specifications, are provided in Sec. VI-C1). The overall cost of the VIS-R and VIS-H systems is approximately 630$ and 280$, respectively.

### B. Low-Level Control Bridge: betaflight-ctrl

The betaflight-ctrl package integrates a finite-state machine (FSM) with four primary operational modes: System Initialization, Autonomous Ascent, and Stabilized Hover, as well as a Policy Control mode for executing policy commands. The FSM first autonomously elevates the drone to a predefined altitude, then stabilizes it in hover. From this state, the quadrotor can either be manually repositioned or switched into Policy Control, in which the drone follows the outputs of the trained policy. To ensure operational safety, the FSM enables rapid fallback to Stabilized Hover via manual input or automatic fallback when deviations or hazards are detected, thereby safeguarding against failures of the learned policy or offboard program.

Meanwhile, the betaflight-ctrl package establishes communication between the onboard computer and the flight controller, enabling real-time publishing and utilization of telemetry data (including attitude, acceleration, battery voltage, remote control signals, and flight modes), thereby facilitating experiment analysis. Moreover, betaflight-ctrl incorporates an adaptive throttle–acceleration mapping, supports diverse command modes (position, velocity–altitude, acceleration, attitude–thrust, CTBR), and provides auxiliary tools for diagnostics and development, including PID analysis, CPU load monitoring, and automated rosbag logging.

### C. Sim-to-real Alignment

1) System Identification: System identification plays a critical role in narrowing the sim-to-real gap, particularly for aggressive flight tasks where model inaccuracy can severely compromise policy effectiveness. Since the design of an endto-end policy fundamentally depends on an accurate system representation, we perform a comprehensive identification process that encompasses not only the precise measurement of physical parameters but also full latency compensation and response alignment between simulation and real-world dynamics. In this section, we detail our system identification methodology and justify the necessity of each alignment step. Given its importance, latency compensation is treated separately in Sec. VI-C2.

Since E2E-Fly employs an accurate dynamics model, we begin system identification by precisely measuring physical parameters. While mass m and arm length ri are directly measured, the moment of inertia J is obtained through a digital prototype that replicates the actual quadrotor’s material composition and weight distribution. The inertia matrix is derived from this computational model, with estimation errors controlled within 10%. The digital prototype used for inertia calculation is shown in Fig. 4.

We then characterize the motor-propeller system using the high-precision LY-5KGF test stand (Fig. 5). With FV2000 motors and 3.5-inch propellers matching the VIS-H and VIS-R configurations, we execute a throttle sweep from 0% to 100% at fixed intervals. Multiple operating points are sampled to fit a quadratic thrust-speed mapping, whose coefficients are directly embedded in the simulation. For dynamic response identification, we record throttle transitions between 5% and

3.5 inch Propeller

Intel D435i

Betaflight F722

4S Battery Radax X4

3000KV motor

**Fig. 4:** The digital prototype employed for moment of inertia test. The model is constructed by accurately assigning the material and mass properties for each component based on the physical quadrotor. Following this, the inertia tensor is computed within the software environment, enabling the extraction of the three principal moments of inertia directly from its diagonal.

3.5 inch Propeller

LY-5KGF

**Fig. 5:** The LY-5KGF test stand for motor system identification. It‘s capable of test propellers of various sizes and featuring software support for remote monitoring and parameter tuning.

95% to identify a first-order delay model, extracting the motor time constant kmotor. All identified parameters are summarized in Table IV.

2) Latency Compensation: All real-world systems with finite computational and communication resources exhibit nonnegligible delays, which are further compounded by dynamic response lags and filter-induced phase shifts. The analysis and mitigation of such latency is critical for control performance, particularly when executing policy commands under model mismatch, external disturbances, and actuator constraints. Experimental validation reveals that system latency primarily arises from two sources: motor response latency and system communication latency. The former, corresponding to the inherent dynamics of the system, has been identified and modeled in Sec. VI-C1. The latter, if left unmodeled and uncompensated, poses a severe threat to sim-to-real transfer, often inducing high-frequency oscillations or even catastrophic control failure during real-world deployment.

To characterize and compensate for system communication latency, we employ a step-response alignment method. A predefined step signal is applied to the real quadrotor’s angular velocity while vertical thrust is maintained at a normalized gravitational acceleration level (suitable for CTBR

**TABLE IV:** Accurate parameters of our hardware platforms

Value

mass m [kg] 0.47 for VIS-H, 0.75 for VIS-R inertia J [kg·m2] [1.25, 1.28, 2.03]×10−3 for VIS-H, [1.41, 1.53, 2.05]×10−3 for VIS-R maximum thrust per motor f max [N] arm length r [m] motor time constant kmotor [s] thrust map [kf2, kf1, kf0] [N·s2/rad2, N·s/rad, N] [4.04 × 10−7, 2.56 × 10−5, −2.62 × 10−2] motor drag coefficient kD [N·m·s/rad] [0.05, 0.05, 1.15] max motor angular velocity Ωmax [rad/s]

commands). Real-world step responses for each axis are recorded via rosbag, while an identical input is applied in simulation. Alignment is achieved by introducing initial action-frame delays in the simulated environment and tuning the underlying PID parameters to match both the amplitude and phase of the physical system’s response.

Experimental measurements indicate a communication delay of approximately 90ms in telemetry-based offboard operation, reduced to below 30ms with onboard computation. Given a control frequency of 30Hz, this corresponds to 3 and 2 action-frame delays for the VIS-H and VIS-R platforms, respectively. After implementing this compensation, the residual latency discrepancy between simulation and real-world operation becomes negligible, enabling nearly identical closedloop behavior across both domains.

3) Domain Randomization: Many studies attempt to narrow the sim-to-real gap by expanding the diversity of domain randomization and the magnitude of introduced noise, enabling agents to cope with corner cases that may arise in real-world scenarios. However, excessive randomization inevitably increases the training burden and prolongs convergence, whereas insufficient randomization often results in poor transferability, as agents fail to generalize to unseen conditions in the physical environment. Thus, determining an appropriate balance between reducing the sim-to-real gap and maintaining a feasible level of training complexity remains an open challenge for quadrotor learning and the broader robotics community.

Building upon this insight, this work provides a set of empirically validated domain-randomization parameters tailored to various tasks, as summarized in Table V. These parameters primarily encompass the quadrotor’s initial configurations and task-specific environmental factors. To enhance training efficiency, a task-oriented randomization scheme is employed, which improves policy robustness while maintaining a balance between learning speed and generalization capability. Furthermore, leveraging accurate system identification, our framework eliminates the need to randomize the quadrotor’s intrinsic physical parameters, thereby simplifying the configuration of the randomization space and streamlining the overall training process.

4) Noise Modeling: It is well recognized that part of the sim-to-real gap arises from discrepancies in real-world noise characteristics that are difficult to model in simulation. Interestingly, even without introducing state-based noise to the quadrotor inputs in E2E-Fly, policies trained within our framework demonstrate zero-shot transfer to physical platforms. This behavior underscores the importance of accurate system

**TABLE V:** Domain randomization parameters for specific tasks.

Task Type Target Task Randomization Parameters

State-based

p, v p p p, v

Vision-based Racing with obstacles p, pgate, qgate, pob Visual landing p, psize, pshape

p, v, pgate, qgate, pob, psize, pshape denote the initial position and linear velocity of the quadrotor, the initial position and orientation of the gate, the initial position of the obstacle, and the size and shape of the landing platform, respectively.

identification and latency compensation in achieving a precise dynamics model. Nevertheless, such noise-free transferability is primarily effective for state-based quadrotor tasks and remains insufficient for vision-based applications.

For perception-aware tasks such as obstacle avoidance and racing in cluttered environments, E2E-Fly incorporates simulated sensor noise without relying on real-world data. We observe that adding Gaussian noise to the inverse depth map (the reciprocal of depth values) helps narrow the discrepancy between simulated and real-world depth perception. Conceptually, this process can be viewed as directly applying Gaussian domain randomization to the disparity map, thereby improving the robustness of the visual features learned from depth information. To further enhance realism, particularly when emulating sensors such as the Intel D435i stereo RGB- D camera, the Redwood depth noise model [58] can be employed. The detailed configurations of visual and state noise are summarized in Table VI.

**TABLE VI:** The type of noise provided in E2E-Fly [21], [28].

Sensor Type Classes

Vision

Gaussian noise Salt & pepper noise Poisson noise Speckle noise Redwood depth noise

Imu Gaussian white noise Bias Random Walk

## VII. EXPERIMENTS AND RESULTS

### A. Benchmark Settings

1) State-based Tasks [59]:

Hover

Racing in cluttered environment

**Fig. 6:** Examples of benchmark training scenarios constructed in the E2E-Fly. We present the simulation performance across various tasks, demonstrating that all policies trained via differentiable simulation and RL can accomplish their objectives.

**Fig. 7:** Training rewards comparison between PPO and BPTT. It is evident from the figure that BPTT exhibits faster convergence, higher sample efficiency, and achieves a higher reward compared with PPO.

**TABLE VII:** We record the training FPS, the total time steps required to converge, and the overall training time for PPO and BPTT on the four baseline tasks. The FPS is measured with 100 parallel environments.

FPS [its/s] time steps [its] Time [s]

≈20000 ≈20000 ≈20000 ≈15000 5e7 1e8 5e7 1e8 ≈2500 ≈5000 ≈2500 ≈6600 ≈13000 ≈13000 ≈24000 ≈20000 1e7 1e7 2e7 5e7 ≈750 ≈750 ≈800 ≈2500

a) Hovering: Hovering, as the most fundamental task, requires the quadrotor to hover stably at the target point from any initial position. In the hovering task, we use a perceptionfree state sdrone

= [pr

t, vt, qt, ωt] ∈R13 as the observation space, where pr

t, qt, vt and ωt represent the relative position from quadrotor to the target, orientation, linear velocity and angle velocity of the quadrotor at time step t respectively. We define the task error as the Euclidean distance between the agent’s position and the hover target point.

b) Tracking: The tracking task requires the quadrotor to start from a random initial point and follow a specified trajectory at a given speed. This task serves as a baseline that bridges traditional and learning-based methods and is particularly important for some RL-based algorithms. The state-only observation space is defined as sdrone

= [pri

t , vt, qt, ωt] ∈ R10+3i, where pri

∈R3i is a concatenation of the relative positions of next i reference points from the quadrotor. In

this paper, we set i = 10. We define the tracking error as the Euclidean distance between the actual trajectory and the target trajectory.

c) Landing: The landing task requires the quadrotor to start from a random position, gradually descend, and eventually land at the required position on the ground. The observation space is defined by sdrone

= [pr

t, vt, qt, ωt] ∈R13. Task completion is defined by a final position error of less than 5cm vertically and 10cm horizontally from the target landing point.

d) Racing: Autonomous drone racing, as one of the most popular tasks has garnered widespread attention. Racing requires the quadrotor to pass through a series of gates in a given order as fast as possible without losing control. We define the observation space as sdrone

= [pr1

t , pr2

t , vt, qt, ωt] ∈R16. The pr1

t ∈R3 and pr2

t ∈R3 correspond to the relative position of the drone to the next two gates’ centers. The task is successful

when the agent traverses all gates in the correct order, thereby completing one full lap.

2) Vision-based Tasks: a) Visual Landing: The visual landing task requires the quadrotor to land using vision input rather than the target’s position. The observation space include the semantic segmentation and basic state defined by ssemantic

∈R64×64 and sdrone

= [pt, vt, qt, ωt] ∈R13. It is worth noting that this task does not require any target information or depth, which relies solely on the segmentation. During the training phase, we use the landing platform measuring 50cm × 50cm × 20cm with a random shape (circle, square, triangle). The task completion is the same as the state-based landing task.

b) Racing in Cluttered Environment: Another visionbased task involves racing with random obstacles, which requires perceiving external obstacles from visual input. Therefore, the observation space includes both depth map and basic state defined by sdepth

∈R64×64 and sdrone



p1

t, p2

t, vt, vd, qt, ωt



. Task completion is defined as flying one full lap without collisions.

Specifically, our end-to-end policy is trained to map observations directly to CTBR commands. The action is defined by at = [Tt, ωx

t , ωy

t , ωz

t ] ∈R4, where Tt and ωx

t , ωy

t , ωz

response the collective thrust and bodyrate respectively. We clamp the action to [−1, 1] during training and use the ReLU activation function at the policy network’s last layer to keep the policy outputs within a fixed range.

For the reward functions, we follow the provided instruction in Sec. IV-C. In Sec. VII-D, we compare how different reward formulations affect the performance of the same task.

### B. Policy Training

To verify that our system can perform robust and efficient zero-shot transfer across various algorithms, we employ BPTT [59] and PPO [25] as the representatives of differentiable simulation and RL for policy training. The parameters for both algorithms are shown in Table VIII. All experiments are run on a 32-core 13th Gen Intel(R) Core(TM) i9-13900K processor and an RTX-4090 GPU.

**TABLE VIII:** Parameters for policy training.

Value

optimizer Adam learning rate 1e-3 decay to 1e-5 discount factor horizon length replay buffer size batch size number of parallel environments

optimizer Adam learning rate 1e-4 decay to 1e-5 discount factor clip range GAE-λ batch size number of parallel environments

### C. Learning via Reinforcement Learning and Differentiable Simulation

This paper presents the first comprehensive, task-by-task experimental comparison between RL and differentiable simulation. Four classical state-based tasks, hovering, landing, tracking, and racing, are used as benchmarks. To ensure fairness, both PPO and BPTT share identical reward functions, observation spaces, network architectures, training parameters, and policy outputs. The observation definitions and reward structures are summarized in Table IX, while the reward curves and training efficiency metrics are presented in Fig. 7 and Table VII.

Across all tasks, Fig. 7 shows that BPTT achieves substantially faster convergence and consistently reaches higher reward values than PPO. As detailed in Table VII, the difference in FPS between the two methods is minimal, indicating comparable per-step computational cost. However, BPTT requires significantly fewer environment steps to converge, resulting in markedly shorter overall training times. On average, BPTT converges in approximately 1,200 seconds, representing less than 30% of PPO’s training time of roughly 4,150 seconds. This superior efficiency can be attributed to the availability of precise analytical gradients in differentiable simulation. With an accurate quadrotor dynamics model, BPTT directly obtains the gradient of the policy objective with respect to the parameters, enabling rapid and stable optimization. As a result, only a small number of iterations are needed to reach high-performing policies, demonstrating the high sample efficiency of the differentiable simulation. In contrast, PPO relies on stochastic gradient estimates derived from extensive sampling, which leads to slower convergence despite eventually producing policies capable of accomplishing each task. The simulation results of the trained policies are illustrated in Fig. 6, confirming the effectiveness of both methods and highlighting the significantly higher training efficiency of BPTT.

### D. Learning under Different Reward Functions

To demonstrate that the reward-design guidelines proposed in Sec. IV-C can effectively accomplish different tasks and to validate the contribution of each reward component, we compare task performance under various reward configurations. Four state-based tasks are selected as benchmarks, and both BPTT and PPO are employed to evaluate performance under the specified reward combinations. Specifically, for each task, we design multiple reward functions to independently examine (1) the effectiveness of the proposed reward design instruction for the given task, and (2) the influence of including or excluding each reward component introduced in Sec. IV-C on the overall task performance. The task evaluation curves for PPO and BPTT are shown in Fig. 8 and Fig. 9, respectively. The evaluation metrics include success rates for landing and racing, as well as position error for hovering and tracking.

As shown in Fig. 8 and Fig. 9, the rewards designed following our proposed instruction effectively guide both PPO and BPTT to accomplish various state-based tasks. The fundamental reward components, including progress, action

**TABLE IX:** The observation space and reward function of state-based tasks.

Task Observation Example Parameters

(pt, qt, vt, at) ∈R13

+ rori2

+ rv1

t + ranglev1

(D) λ2 = 0.01, λ10 = 0.0001, λ13 = 0.002, λ17 = 0.002 (pt, qt, vt, at) ∈R13

+ rvz

t + ranglev1

(D) λ3 = 0.04, λ16 = 0.1, λ17 = 0.001 (pi=1−10

, qt, vt, at) ∈R40

+ rori2

+ rv1

t + ranglev1

(D) λ2 = 0.02, λ10 = 0.001, λ13 = 0.002, λ17 = 0.002 (p1

t , p2

t , qt, vt, at) ∈R16

+ rori2

+ rv1

t + ranglev1

(D) λ1 = 0.9, λ10 = 0.001, λ13 = 0.002, λ17 = 0.002

The table above provides the reward function designs for state-based tasks in this paper, with each reward term derived from the reward function manual in the methodology section. Here, D denotes fully differentiable rewards.p, q, v, and a represent the relative position between the body center and the target, the orientation expressed in quaternions, the linear velocity, and the angular velocity, respectively.

Position Error (m)

Hovering Error

Success Rate

Landing Success Rate

Position Error (m)

Tracking Error

Success Rate

Racing Success Rate

rfull w/o rv w/o rprog w/o ract w/o ranglev w/o rsparse

**Fig. 8:** Success rate and task error under different reward settings training via PPO. The figure presents the ablation study evaluating the effects of the individual reward components trained with PPO. The rfull represents the configuration using all reward components listed in Table II, while w/o rv,w/o rprog,w/o ract,w/o ranglev,w/o rsparse denote the cases without linear-velocity reward, progress reward, actionsmoothness reward, angular-velocity reward, and sparse reward, respectively. For the racing task, only the rfull, w/o rprog, w/o rsparse, w/o ranglev reward curves are included.

Position Error (m)

Hovering Error

Success Rate

Landing Success Rate

Position Error (m)

Tracking Error

Success Rate

Racing Success Rate

rfull w/o rv w/o rprog w/o ranglev

**Fig. 9:** Success rate and task error under different reward settings training via BPTT. The figure presents the ablation study evaluating the effects of the individual reward components trained with BPTT. The rfull represents the configuration using all reward components listed in Table II, while w/o rv,w/o rprog,w/o ranglev denote the cases without linear-velocity reward, progress reward, action-smoothness reward, angular-velocity reward, and sparse reward, respectively. For the racing task, only the rfull and w/o rprog reward curves are included.

smoothness, linear velocity, and angular velocity, are essential for both BPTT and PPO in stability-oriented tasks such as hovering, landing, and tracking. The absence of any component degrades task performance. These elements work together to maintain drone stability while completing tasks, preventing loss of control at high speeds or under large attitude angles. For the landing task, distinct progress rewards for the xy-plane and the z-axis are introduced to accommodate their respective velocity constraints. In racing, where precise attitude control and stabilization demands are relaxed, a heavily weighted progress reward plays a dominant role in accomplishing the task.

Furthermore, terminal rewards provide critical guidance for RL algorithms such as PPO. The sparse rewards issued upon task completion, along with collision penalties, enable the agent to recognize the influence of specific behaviors on longterm cumulative returns, thereby steering policy optimization toward successful task completion and crash avoidance. Overall, the experimental results further validate that our general-purpose reward-design methodology reduces tuning effort and remains effective across different tasks and algo-

rithms. By systematically selecting and combining appropriate reward components according to specific task requirements, our framework streamlines the training process and ensures efficient policy convergence.

### E. Learning with Visual Input

To assess the effectiveness of our framework on visionbased tasks, we evaluate two representative benchmarks: landing with semantic segmentation and obstacle-aware racing using depth maps. To demonstrate compatibility with diverse learning paradigms, we train the landing task using BPTT and the racing task using PPO. The reward curves and success rates are presented in Fig. 12, and the corresponding simulation results are shown in Fig. 10 and Fig. 11.

As illustrated in Fig. 12, our system enables efficient learning across both tasks and supports different algorithms without task-specific modifications. In the obstacle-aware racing scenario, PPO combined with a curriculum learning strategy successfully generalizes to unseen environments and achieves a 100% success rate across three racetracks of different shapes,

**Fig. 10:** Simulation result of vision-based landing. Subfigures (a), (b), and (c) depict the performance of the identical policy while landing on triangular, circular, and square landing pads, respectively. The corresponding segmentation maps from the downward-facing camera are displayed on the right side of each subfigure.

（a） （b） （c）

**Fig. 11:** Simulation result of racing with obstacles. Subfigures (a), (b), and (c) present simulation results obtained in S-shaped, 3D circle, and J-shaped race tracks, respectively, with maximum velocities achieving over 10 m/s.

**TABLE X:** The observation space and reward function of vision-based tasks.

Visual landing Racing with obstacles

Observation (pt, qt, vt, at) ∈R13 & segmentation ∈R64×64 (p1

t , p2

t , qt, vt, vd, at) ∈R17 & depth ∈R64×64

+ rori2

+ rvz

t + ranglev1

(D)

+ ract3

+ rori1

+ ravoid1

+ rgoal

+ rcrash

(PD)

λ3 = 0.04, λ10 = 0.003, λ16 = 0.1, λ17 = 0.001 λ1 = 0.9, λ7 = 0.025, λ8 = 0.002, λ9 = 0.04, λ18 = 0.01, λ21 = 5, λ22 = 4

The table above provides the reward function designs for vision-based tasks in this paper, with each reward term derived from the reward function manual in the methodology section. Here, D denotes fully differentiable rewards, while PD denotes partially differentiable rewards. p, q, v, and a represent the relative position between the body center and the target, the orientation expressed in quaternions, the linear velocity, and the angular velocity, respectively.

Racing with Obstacles

Success Rate

Racing with Obstacles

0.2M 0.4M 0.6M 0.8M

Visual Landing

0.2M 0.4M 0.6M 0.8M

Success Rate

Visual Landing

**Fig. 12:** Reward and success rate curves of visual tasks. From left to right, the figure depicts the reward and success rate curves for racing with obstacles and visual landing.

as shown in Fig. 11. For the vision-based landing task, BPTT achieves end-to-end single-step training using only the semantic segmentation map, without any additional prior knowledge of the landing target. The trained policy exhibits strong generalization across diverse initial positions and landing platforms with varying appearances, as illustrated in Fig. 10. Notably, BPTT requires only 1×106 time steps to complete the landing task, highlighting the substantial sample efficiency enabled by analytical gradient back-propagation. Together, these two vision-based tasks demonstrate the effectiveness of our system in learning robust policies from visual observations.

### F. Zero-shot sim-to-real transfer

To validate the effectiveness of the proposed sim-to-real alignment methodology, we begin by analyzing the step response alignment, as illustrated in Fig. 13. This step is essential because discrepancies in system dynamics or delay characteristics directly translate into inconsistent behavior. Subsequently, we demonstrate the performance of a fully aligned policy in both simulation and the real world (Fig. 14). All real-world flight experiments are conducted on the VIS- R platform, while the aggressive task, racing with random obstacles, is additionally validated through hardware-in-the-

Time (s)

−0.50

−0.25

rad/s

X-axis Angular Velocity

Time (s)

−0.50

−0.25

rad/s

Y-axis Angular Velocity

Time (s)

−0.4

−0.2

rad/s

Z-axis Angular Velocity

Time (s)

N

Z-axis Thrust

cmd real sim

**Fig. 13:** The step-response alignment. We align the step-response of angular velocity and the mass-normalized thrust along the z-axis.

Time (s)

rad/s

X-axis Angular Velocity

Time (s)

rad/s

Y-axis Angular Velocity

Time (s)

rad/s

Z-axis Angular Velocity

Time (s)

N

Z-axis Thrust

cmd real sim

**Fig. 14:** Policy response after step-response alignment. The corresponding policy deployment without requiring additional alignment, yielding a response that closely matches the simulation.

Racing in Cluttered Environments

**Fig. 15:** Zero-shot transfer from simulation to real world via our E2E-Fly system. Real-world performance demonstrates that the policy trained with our system can achieve zero-shot transfer from simulation to the real world.

loop simulation on the VIS-H platform. Finally, to verify whether our system enables zero-shot policy transfer, we evaluate each policy in simulated and real-world experiments, with corresponding results presented in Fig. 6 and Fig. 15, respectively.

As shown in Fig. 13 and Fig. 14, the combination of system identification, latency compensation, domain randomization, and noise modeling produces a close match between simulated and real-world response curves. This alignment enables reliable zero-shot deployment without any task-specific system parameters fine-tuning. Practically, this means that once a policy has converged in simulation, it can be executed directly on the physical platform while preserving its functional characteristics. This capability underscores the critical importance

of comprehensive sim-to-real alignment in quadrotor research. The task-level comparisons in Fig. 6 and Fig. 15 further confirm that the learned policies exhibit nearly equivalent performance across simulated and real environments, demonstrating the robustness and effectiveness of the proposed simto-real alignment pipeline.

## VIII. DISCUSSION

### A. Difficulty for Differentiable Simulation to Design Reward

Despite its theoretical advantages, BPTT in differentiable simulation faces significant challenges when applied to complex, long-horizon tasks. A primary limitation lies in the difficulty of designing effective and smoothly differentiable reward functions. Inappropriate reward landscapes can cause

gradient instability during back-propagation through extended temporal sequences, leading to vanishing or exploding gradients that hinder stable policy optimization. Furthermore, as gradient optimization inherently performs a local search, it is prone to convergence toward suboptimal behaviors driven by local reward gradients rather than global task objectives. For example, in a landing task, an excessively steep differentiable penalty on deviation from the target may bias the drone toward a slow, conservative descent, while obscuring the path to a more agile, time-optimal solution.

### B. Combining the Advantages of Differentiable Simulation and RL

RL does not require knowledge of the precise environment model. Instead, the agent learns policies from reward signals through interaction with the environment. Even with specific dynamic differences between simulation and the real world, techniques such as domain randomization can improve the policy’s robustness. Thanks to its strong exploratory capabilities, RL may discover unconventional yet efficient behavioral patterns. However, it suffers from low sample efficiency and unstable training.

Differentiable simulation, on the other hand, leverages precise differentiable dynamics to optimize policies via gradient back-propagation directly. It boasts extremely high sample efficiency. Nevertheless, BPTT has drawbacks: it not only requires constructing a fully differentiable gradient chain but also makes reward function gradients highly sensitive, posing significant challenges for learning from sparse rewards.

Therefore, RL is well-suited for complex problems with unknown models that require exploration, while differentiable simulation is ideal for tasks with precise, differentiable models that demand efficient, accurate control. However, the two are not mutually exclusive but highly complementary. We believe the future trend is to combine their strengths: using RL’s exploratory power to learn high-level goals and employing differentiable simulation for precise local motion and control optimization at the lower level.

## IX. CONCLUSION

In conclusion, we present E2E-Fly, a unified framework that bridges the sim-to-real gap for quadrotors via an integrated pipeline composed of policy training, validation, and realworld deployment. By synergistically combining differentiable physical learning in a high-speed rendering environment and supporting it with structured reward design and curriculum learning, our system enables efficient policy optimization for diverse state-based and vision-based tasks. The framework ensures robust policy transfer through a comprehensive validation strategy involving sim-to-sim evaluation and hardware-inthe-loop test, and a systematic sim-to-real alignment methodology that includes system identification, latency compensation, domain randomization, and noise modeling. Extensive experiments across six challenging tasks confirm that our approach achieves reliable zero-shot transfer, deploying trained policies directly to physical quadrotors with high performance, thereby offering a complete and reproducible platform for

end-to-end learning in agile autonomous flight. Our work establishes a complete pipeline and an efficient sim-to-real deployment framework for learning-based end-to-end algorithms in quadrotors, laying a solid platform foundation for future research.
