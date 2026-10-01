---
id: arxiv-2607.12801-autonomous-tracking-terminal-guidance-moving
title: "Autonomous Tracking and Terminal Guidance of Moving Targets for Fixed-Wing UAVs"
year: 2026
backend: pymupdf
---

Autonomous Tracking and Terminal Guidance of

Moving Targets for Fixed-Wing UAVs

Wei-Hao Liou and Teng-Hu Cheng

## Abstract

This study introduces a unified control framework for fixed-wing unmanned aerial vehicles (UAVs) fitted with a pan-tilt (PT) camera, intended to perform an end-to-end mission spanning from initial target detection to accurate terminal engagement. The proposed system employs a three-phase strategy: a vision-based target acquisition phase, an NMPC-based tracking phase, and a terminal guidance phase. During tracking, the framework uses an Unscented Kalman Filter (UKF) to fuse YOLO-based visual detections with inertial measurements, enabling robust target state estimation under unknown dynamics. To ensure reliable visual contact, we introduce a constraintaware Nonlinear Model Predictive Control (NMPC) strategy that incorporates Control Barrier Functions (CBFs) to explicitly prevent UAV self-occlusion—a common limitation in fixed-wing tracking. Upon satisfying terminal engagement conditions, the system seamlessly transitions control to a quaternion-based Biased Proportional Navigation Guidance (BPNG) law, enforcing precise impact angle constraints. High-fidelity simulations demonstrate that the framework achieves stable, robust tracking and accurate terminal interception while strictly respecting the vehicle’s dynamic limits and camera field-of-view constraints.

Index Terms—Occlusion Avoidance, NMPC, BPNG, CBF, UKF

## I. INTRODUCTION

### A. Background

Unmanned aerial vehicles (UAVs) are indispensable in modern surveillance [1], mapping [2], search and rescue [3], [4], and military operations [5] due to their high efficiency and cost-effectiveness. Among these, fixed-wing UAVs are preferred for high-speed, long-endurance, and large-area missions. Recent advancements in onboard vision have expanded their operational scope to include real-time target tracking. However, tracking moving targets with fixed-wing platforms is inherently challenging due to coupled roll-yaw dynamics and restricted lateral maneuverability. While pan-tilt (PT) cameras improve sensing flexibility, they introduce complex gimbal dynamics and physical field-of-view (FOV) constraints that must be accounted for in the control design. Furthermore, precision missions often require terminal guidance—such as achieving a specific impact angle—which poses significant difficulty for fixed-wing airframes. Our work addresses these requirements by integrating mid-course NMPC-based tracking with terminal BPNG guidance, ensuring both visual contact and precise engagement geometry.

Department of Mechanical Engineering, National Yang Ming Chiao Tung University, Hsinchu, Taiwan 30010 Email: howard55.en12@nycu.edu.tw and tenghu@nycu.edu.tw

This research was supported by the Ministry of Science and Technology, Taiwan (Grant Number NSTC 114-2223-E-A49 -004 -MY3

**Fig. 1:** Tracking and terminal mission of a fixed-wing UAV equipped with a PT camera.

### B. Related Works

Target tracking has been extensively researched, particularly for rotor-type UAVs that benefit from hovering capabilities [6], [7], [8]. For fixed-wing platforms, tracking is complicated by the lack of hovering, requiring controllers that explicitly model motion constraints [9], [10]. To increase sensing versatility, researchers have integrated visual feedback [11] and gimbal cameras [12], [13]. While these studies make significant progress, they often rely on ideal flight assumptions or neglect practical constraints such as feasible speed/altitude envelopes and self-occlusion.

Nonlinear Model Predictive Control (NMPC) is a standard for handling fixed-wing dynamics and constraints [14], [15], [16], [17], [18]. However, many NMPC formulations assume full prior knowledge of the target state, which is often unavailable in real-world scenarios [18]. For terminal engagement, Proportional Navigation Guidance (PNG) and its biased variants (BPNG) are widely used for their simplicity [19], [20], [21]. While recent studies have improved BPNG performance through optimal control [22], achieving robust terminal guidance often requires extensive gain tuning. Finally, although various estimation techniques—such as particle filters [23] and Unscented Kalman Filters (UKF) [24]—have been proposed to solve the unknown-target-motion problem, an integrated framework that jointly optimizes fixed-wing dynamics, camera PT constraints, and terminal guidance remains a significant open challenge in the literature.

### C. Objective

The objective of this work is to develop an integrated guidance, control, and estimation framework for fixed-wing UAVs that enables robust visual target tracking and precise

terminal guidance under realistic dynamic and sensing constraints. As illustrated in Fig. 1, the mission is divided into three sequential phases: (1) initial path flight, where the UAV transitions from its starting location; (2) tracking control, where the UAV maintains a favorable relative position to the moving target while respecting its dynamic constraints and PT joint limits; and (3) terminal guidance, where the UAV aligns its trajectory to achieve the desired impact while maintaining visual contact with the target. The control objective is to ensure robust tracking and accurate terminal engagement throughout all phases.

### D. Contribution

This study presents an integrated, three-phase autonomous framework for fixed-wing UAVs equipped with a PT camera to achieve robust, long-duration tracking and precise terminal engagement of unknown moving targets. Unlike existing works that often rely on unrealistic assumptions—such as known target dynamics [18], ideal flight conditions [13], or isolated tracking and guidance loops—our framework explicitly couples nonlinear estimation with constraint-aware path planning and terminal guidance laws.

The primary contributions of this research are as follows: 1) Unified Estimation and Tracking Framework: We propose an integrated system that relies solely on visual information to perform real-time estimation and tracking. By incorporating a UKF to fuse YOLO-detected image features with inertial measurements, the system robustly estimates the target’s position and velocity under unknown motion, bridging the gap between perception and control. 2) Constraint-Aware NMPC for Gimbaled Tracking: We propose an NMPC framework that ensures target tracking is preserved while simultaneously adhering to the UAV’s dynamic flight envelope and the physical operating constraints of the PT camera. By employing control barrier functions (CBFs), we formulate an explicit constraint to avoid UAV self-occlusion, ensuring continuous visual contact even during aggressive maneuvers—a critical limitation in SOTA tracking approaches that often ignore airframe-shadowing during turns. 3) Seamless Transition to Optimal Terminal Guidance: Our framework features a novel phase-switching logic that transitions from NMPC-based loitering to a quaternion-based biased proportional navigation guidance (BPNG) law. This transition ensures that once mission conditions are met, the UAV is steered to satisfy strict terminal impact angle constraints (IAC) without requiring manual retuning or complex gain scheduling, providing a significant improvement in engagement reliability over classical PNG-based methods.

## II. PROBLEM FORMULATION

### A. Kinematics of the overall system

The kinematic configuration of the complete system is shown in Fig. 2. The system is composed of a fixed-wing UAV,

**Fig. 2:** Kinematics model

**TABLE I:** Definition of Symbol.

Symbol Description G(·) Inertial (ground) frame B(·) UAV body frame C(·) Camera frame r ∈R3 Position ω ∈R3 Angular Velocity

an onboard PT camera, and the target. Multiple coordinate frames are involved and summarized in Table I.

The inertial frame, denoted as the ground frame G, follows an East–North–Up (ENU) convention. The UAV body frame B is defined using a front–right–down (FRD) convention, and under coordinated flight with negligible sideslip, the UAV motion is primarily aligned with the BX axis. The camera frame C is defined with the CZ axis pointing forward, CX to the right, and CY downward. Consider the UAV’s Euler

**Fig. 3:** Euler angle definition and rotation order [25].

angles: roll ϕ, pitch θ, and yaw ψ, as defined in [25], shown in Fig. 3. The transformation from the inertial frame to the UAV body frame is given by:

BRG = Rx(ϕ)Ry(θ)Rz(ψ)NEDRENU,

NEDRENU is a 3 × 3 transformation matrix that converts coordinates from the ENU frame to the North-East- Down (NED) frame. The matrices Rx, Ry, and Rz denote 3×3 rotation matrices corresponding to rotations about the x, y, and z axes, respectively. Thus, the UAV velocity in inertial frame GVp is defined as:

GVp =

Gvpx Gvpy Gvpz

=

VU cos ψ cos θ

VU sin ψ cos θ

VU sin θ

where VU represents the controlled UAV velocity along its body frame x-axis. In addition, the relative pose from the camera to the target illustrated in Fig. 2 is given by:

rq/c = rq −rp −rc/p,

where rc/p is the relative position from the UAV coordinate to the PT camera, as shown in Fig. 4. Taking time derivative of (3) yields:

˙rq/c = Vq −Vp −ωp × rq/c −ωc × rq/c −ωp × rc/p,

where Vp = [vpx vpy vpz]T is the translational velocity of the UAV, ωp = [ωpx ωpy ωpz]T is the angular velocity of the UAV, ωc = [ωcx ωcy ωcz]T is the camera’s angular velocity and Vq = [vqx vqy vqz] is the target’s translational velocity, which is unknown and will be estimated using UKF method.

B. PT Camera Model

**Fig. 4:** Coordinate systems of a fixed-wing UAV mounted with PT camera.

To further illustrate the tracking task and the target estimation derived from camera feedback, a model of the PT camera motion is introduced in this section. The coordinate relationship between the fixed-wing UAV and the PT camera is depicted in Fig. 4, where M denotes the mount frame, P the pan frame, T the tilt frame, and C the camera frame.

The rotational directions of the PT camera are defined in Fig. 5: a positive pan angle corresponds to clockwise rotation, and a positive tilt angle corresponds to upward rotation. Here, θp and θt denote the pan and tilt angles, respectively.

**Fig. 5:** Definition of the coordinate system of the PT camera.

C. UKF[26]

A UKF is employed to estimate the target’s unknown motion. The UKF utilizes a dynamic model and measurements from the PT camera to determine the target’s state. The nonlinear system for the UKF can be expressed as:

xk+1 = F(xk) + wk

zk = H(xk) + vk,

where xk is the state of the target system at time k, zk is discrete measurement by camera at time k, F(xk) is a dynamics model for prediction statem H(xk) is the measurement model for correcting the predicted state, and wk and vk are process and measurement noises respectively.

The dynamics model x ∈R8 used to predict the target motion is involved with the fixed-wing UAV, PT camera and and the tracking target, and it is defined as:

x =

x1 x2 GrT

q

GV T

q

where x1 and x2 are defined as follow:

x1 x2

 X

Z

Y Z

Crq/c = [Cxq/c Cyq/c Czq/c]T = [X Y Z]T .

Assuming that the target follows a constant-velocity motion, the time derivative of the system state in (4) is given by

˙x =



˙x1 ˙x2

˙ GrTq

˙ GV T q

=



vqxx3 −vqzx1x3 + ζ1 + Ω1 + η1 vqyx3 −vqzx2x3 + ζ2 + Ω2 + η2

˙rq/c + Vc + ωc × rq/c

03×1

,

x3 = 1

Z ζ1 = ωcxx1x2 −ωcy −ωcyx2

1 + ωcxx2 ζ2 = ωcx + ωcxx2

2 −ωcyx1x2 −ωcxx1 Ω1 = ωpxx1(x2 + myx3) −ωpy −ωpyx2

−ωpyx3(mz + mxx1) + ωpz(x2 + myx3)

Ω2 = ωpz + ωpxx3(mz + myx2) + ωpxx2

−ωpyx2(x1 + mxx3) + ωpz(−x1 −mxx3)

η1 = (vpxx1 −vpx)x3 η2 = (vpxx2 −vpy)x3,

and ωc = [ωcx, ωcy, ωcz]T denotes the angular velocity vector associated with the camera’s motion, all the coordinates in (6) are expressed in the camera frame C and rc/p = mx my mz

The measurements used by the UKF consist of the target’s 2D image coordinates and the camera position, expressed as

z =

v rT

c

Target detection in the image is performed using the You Only Look Once (YOLO) algorithm. After training, YOLO outputs a bounding box around the detected target, and the

center of this box is selected as the image feature vector Qt(u, v), as illustrated in Fig. 2.

Based on the pinhole camera model, the normalized image coordinates x1 and x2 are given by

x1 = u −cu

fx

x2 = v −cv

fy

where cu and cv denote the principal point of the image, and fx and fy are the focal lengths along the horizontal and vertical axes, respectively. Based on (7) and (8), the measurement model used for UKF is given by

z =

v rc

=

fxx1 + cu fyx2 + cv

rq −rq/c

which relates the measurement vector to the UKF state estimate.

**Fig. 6:** The relation of camera depth under the assumptions.

In long-range fixed-wing UAV missions, directly determining the reciprocal of x3—that is, the image depth Z in (6)—is challenging. Therefore, depth must be estimated using additional measurements.

One of the depth estimation approaches relies on geometric relationships. Specifically, the geometry used for depth computation is shown in Fig. 6. The depth can be derived from trigonometric relations as

α = cos−1(−eT

3 c3),

d = Z = 1

x3

h cos α,

where e3 ∈R3 denotes the unit vector aligned with the inertial GZ axis, c3 ∈R3 represents the unit vector aligned with the camera CZ axis, and the camera height h is determined from the UAV’s altitude.

## III. CONTROL SYSTEM DESIGN

In this section, several controllers are designed to accomplish the full tracking-to-terminal mission. Preserving visual contact with the target is essential in all mission phases. In Phase 1, the IBVS controller locks onto the target image to generate an initial estimate while the UAV follows a simple flight trajectory. In Phases 2 and 3, it continuously keeps the

target centered in the camera FOV, thereby enabling robust tracking, complying with UAV dynamics and PT motion constraints, and facilitating accurate terminal guidance. This section details the design of each controller and explains its function within the three consecutive mission phases illustrated in Fig. 1.

### A. Phase 1: Controller design of the PT camera System

This section presents the design of the IBVS controller, which operates across all flight phases. The IBVS controller generates the required camera rotation commands to maintain the target at the center of the image, and these commands are then converted by the PT controller so that the PT rotations are controlled in accordance with the IBVS controller output for the camera attitude.

1) IBVS controller: The feature vector s(t) = x1, x2

T

is defined as the control state, where x1 and x2 is same defined as (4). The control objective for IBVS is to maintain the target in the center of the camera image, the desired state can be expressed:

s∗=

0 0T .

The error between the current and desired state can be expressed:

e(t) = s(t) −s∗,

where e(t) : [0, ∞) →R2 and s∗denotes a given constant element, differentiating (9) yields:

˙e(t) = ˙s(t).

By incorporating the system’s dynamic model defined in (5), the system equation can be expressed as:

˙e =

 ˙x1

˙x2

= L1ωc + L2

Vp −Vq

ωp

where ωc = [ωcx, ωcy, ωcz]T denotes the angular velocity vector associated with the camera’s motion, and L1 denotes the Jacobian matrix that relates the angular velocity of the camera frame to the feature vector, defined as

L1 =



x1x2 −(1 + x2

1) x2 1 + x2 −x1x2 −x1

and L2 is an interaction matrix defined in (11).

The resulting closed-loop error dynamics can be expressed as:

˙e = −λe,

where λ ∈R+ is the control gain. By reducing the camera angular velocity ωc to the two PT degrees of freedom, the IBVS controller can be designed from the error dynamics in (10) as

ωcx

ωcy

= −ˆL−1

1 L2

Vp −Vq

ωp

−λˆL−1

1 e,

where ˆL1 is a submatrix of L1 defined as:

ˆL1 =

 x1x2 −(1 + x2

1) 1 + x2 −x1x2

.

L2 =

−x3 x1x3 x1(x2 + myx3) −(1 + x2

1 + x3(mz + mxx1)) x2 + myx3 −x3 x2x3 1 + x2 2 + x3(mz + myx2) −x2(x1 + mxx3) −x1 −mxx3

2) PT camera controller: Following the pan-then-tilt rotation order as shown in Fig. 4, the required PT angular velocity (12) of the PT camera can be derived from the camera angular velocity defined in (12) as

ωc =



cos θt −sin θt sin θt cos θt



˙θp

+



˙θt

.

The resulting pan and tilt rates can then be computed from (13) as

˙θt = ωcx ˙θp = ωcy cos θt

.

It is worth noting that a singularity occurs when θt = ±90◦. This issue will be addressed in coordination with other controllers.

### B. Phase 2: NMPC for the tracking phase

During Phase 2, the NMPC is employed to control the UAV’s trajectory while respecting its dynamic constraints and the PT camera’s physical limits. NMPC is a widely used optimal control strategy for nonlinear systems with constraints, making it particularly suitable for UAV tracking missions where the vehicle must follow a moving target while maintaining feasible control inputs. The NMPC system state is defined as

X =

GrT

p ϕ θ ψT ,

where GrT

p denotes the UAV position in the inertial frame, and ϕ, θ, and ψ are same defined as (1). The control input is

U =

VU up uq

T ,

where VU is the forward velocity commanded along the bodyframe BX axis, and up and uq are the angular velocities along BX and BY , respectively, as shown in Fig. 7. By neglected the

**Fig. 7:** Definition of the body-frame angular velocity control inputs.

body-frame yaw rate (i.e., ur ≈0), the relationship between

the body angular velocities and the Euler angle rates is given by [25]  ˙ϕ

˙θ

1 sin ϕ tan θ cos ϕ

 up

uq

.

Incorporating the translational velocity defined in (2), the angular velocity described in (16) and the turning condition governed by the yaw rate as described in [27], the system dynamics are expressed as follows:

˙X =



VU cos ψ cos θ

VU sin ψ cos θ

VU sin θ up + uq sin ϕ tan θ

uq cos ϕ −g

VU

tan ϕ cos θ



where g represents the gravitational constant. Given the system dynamics in (17), the future state Xk+1 can be predicted from the current state Xk and the control input Uk as

Xk+1(Xk, Uk) = Xk + ˙XkTs,

where Ts is the sampling time. Accordingly, for a given current state Xk and a sequence of control inputs U

Uk, Uk+1, . . . , Uk+Nc

, a corresponding sequence of predicted future states X =

Xk+1, Xk+2, . . . , Xk+Np

can be obtained. Here, Np and Nc denote the prediction and control horizons, respectively. In this study, the prediction and control horizons are set as the same, Np = Nc = N.

1) NMPC: An optimal cost function J(X, U) is defined over the predicted state sequence X. To accomplish the tracking objective in Phase 2, the cost function consists of four components,

J(X, U) =

N−1 X

k=0

 

f1(Xk) + f2(Xk) + f3(Xk) + f4(Uk)



where each term addresses a specific tracking requirement. The term f1(Xk) regulates the planar distance between the UAV and the target on the inertial XY -plane,

f1(Xk) =

p

(Gxp,k −Gxq,k)2 + (Gyp,k −Gyq,k)2 −R

w1 ,

Grp,k [Gxp,k Gyp,k Gzp,k]T and Grq,k [Gxq,k Gyq,k Gzq,k]T denote the positions of the UAV and the target expressed in the inertial frame G, respectively. f1 drives the UAV to keep a target separation of R, ensuring both dependable visual tracking and advantageous terminal geometry. The altitude control component is given by

f2(Xk) =

Gzp,k −H

w2 ,

where H is the target flight altitude and w2 is the weight associated with this objective. The term f2 imposes a penalty on any deviation from the specified flight altitude. To limit

aggressive maneuvers and decrease control effort, an attitude smoothness term is introduced as

f3(Xk) =

Qk+1 −Qk

w3 ,

where Qk =

ϕk θk ψk

T and w3 ∈R3×3 is a diagonal weighting matrix. The function f3 penalizes changes in the Euler angles between successive sampling instants. Finally, continuity of the input across successive NMPC horizons is encouraged through

f4 =

u∗

p,−1 u∗

q,−1

−

up,0

uq,0

w4

where u∗

p,−1 and u∗

q,−1 are the optimal body rates applied to the UAV in the previous NMPC solution, and up,0 and uq,0 denote the first input elements of the current control horizon. To compute the optimal control sequence U∗, the NMPC problem is formulated by minimizing the cost function J(X, U), subject to state and input constraints,

U∗= arg min

J(X, U)

s.t. Xlb ≤X ≤Xub,

Ulb ≤U ≤Uub,

where Xlb and Xub represent the lower and upper bounds of the predicted state set X, while Ulb and Uub denote the lower and upper bounds of the control input set U. In this case, they are set to match the physical limits of UAV motion. Thus, the possible UAV attitude, input velocity, and angular rate are defined as follows:

ϕmin ≤ϕk ≤ϕmax

θmin ≤θk ≤θmax VU,min ≤VU,k ≤VU,max

up,min ≤up,k ≤up,max uq,min ≤uq,k ≤uq,max.

**Fig. 8:** Illustration of UAV self-occlusion during a loitering mission: (left) normal unobstructed LOS, and (right) LOS obstruction caused by airframe-shadowing during a banking turn.

2) To prevent self-occlusion: In addition to (19), an extra motion constraint on the UAV bank angle is imposed to avoid visual self-occlusion, as depicted in Fig. 8, assuming that the tilt angle is constrained to nonpositive values in accordance with the mechanical limits shown in Fig. 5. In the normal case (left side of Fig. 8), the line of sight (LOS) between the onboard sensor and the maritime target remains

unobstructed as long as the PT camera satisfy the joint limits (i.e., −π ≤θp ≤π, −π

2 ≤θt ≤0). In contrast, as the UAV increases its bank angle to sustain circular flight, it enters the occluded scenario (right side), in which the tilted wing crosses and obstructs the LOS vector, despite the fact that the same PT camera motion constraints are still satisfied. Thus, the onset of occlusion is determined by the roll angle ϕ, and the target remains visible and trackable as long as it lies along the positive direction of the UAV body-frame Z-axis, i.e., Bz ≥0, as shown in Fig. 9. The relative position between the UAV and

**Fig. 9** 

the target in the inertial frame G is given by

Grq/p =G rq −Grp =

Gxq/p Gyq/p Gzq/p

By neglecting the UAV pitch angle (a valid assumption in the Phase 2 stage) and using the coordinate transformation given in (1), the relative position in the UAV body frame B can be written as

Brq/p =

Gxq/p sin ψ + Gyq/p cos ψ Gxq/p cos ψ cos ϕ −Gyq/p sin ψ cos ϕ −Gzq/p sin ϕ −Gxq/p cos ψ sin ϕ + Gyq/p sin ψ sin ϕ −Gzq/p cos ϕ

.

Given the preference Bz ≥0 illustrated in Fig. 8, it is desirable for the target to lie above the UAV’s body-frame XY-plane (Bzq/p ≥0). Accordingly, the constraint is formulated as

Bzq/p = −Gxq/p cos ψ sin ϕ+Gyq/p sin ψ sin ϕ−Gzq/p cos ϕ ≥0,

which can be expressed as

tan ϕ

(

≤−Gzq/p/Rp, Rp > 0, ≥−Gzq/p/Rp, Rp < 0,

where Rp = Gxq/p cos ψ −Gyq/p sin ψ.

This constraint guarantees that the target remains within the camera’s field of view while also enforcing that every mechanically reachable target lies above the UAV’s bodyframe XY-plane. To additionally guarantee that the constraints in (20) are fulfilled via the rolling up in the NMPC as defined in (18), control barrier functions (CBFs) are employed to recast these constraints into inequality form, which will be merged into the constraints in (19). We first examine the situation where, according to (20), the target is positioned on the righthand side of the UAV, which is described by

Rp ≥0.

To satisfy the condition stated above, we define a scalar function h(ϕ), and we aim to impose the following inequality constraint:

h(ϕ) = tan−1

−Gzq/p

Rp

!

−ϕ ≥0, Rp ≥0.

Accordingly, the CBF condition is defined as

˙h ≥−βh, Rp ≥0,

where the dynamics ˙ϕ defined in (17) is used, and β > 0 is a design parameter that determines the strictness of the constraint enforcement. By taking the time derivative of the scalar function h(ϕ) defined in (21) and considering the CBF condition given in (22), the following nonlinear inequality constraint on the control input is obtained:

up ≤β



tan−1 −Gzq/p

Rp



−ϕ



+ α −uq sin ϕ tan θ,

for Rp ≥0, where α is the time derivative of the first term defined in (21). Similarly, under the condition that the target is located on the left side of the UAV, the following inequality holds:

up ≥β



tan−1 −Gzq/p

Rp



−ϕ



+ α −uq sin ϕ tan θ,

for Rp ≤0. Based on the target’s relative position, the nonlinear input constraints (23) and (24) are incorporated into the NMPC formulation (19) to guarantee that the UAV remains within the camera’s tilt-angle limits.

### C. Phase 3: Biased proportional navigation for terminal guidance

A BPNG scheme is utilized to impose the impact angle constraint (IAC), guaranteeing that the UAV reaches the target with a specified terminal angle. When Phase 3 begins, control authority is handed over from the NMPC to the BPNG controller, which directs the UAV toward the moving target while shaping the trajectory to fulfill the IAC and preserving visual tracking through the camera system. In this phase, the control input changes from (15) to the UAV’s angular velocity

ωcmd =

up uq ur,T

as depicted in Fig. 7, to steer the UAV so that it is aimed at the target. Therefore, a quaternion-based BPNG controller, developed based on the approach in [22], is adopted for terminal guidance of the controlled UAV. The optimal threedimensional IAC law derived from the quaternion-based BPNG framework in [22] is given by

u∗

IAC = NσΩ× Vp + NfVp

tgo

× ( Vp × Vf

|Vp × Vf|) cos−1( Vp · Vf

|Vp||Vf|),

where Vp denotes the UAV velocity direction vector, which is assumed to be aligned with the body x-axis under coordinated flight with negligible sideslip, Vf is the desired terminal velocity direction corresponding to the prescribed impact angle, and tgo is the estimation time-to-go until impact, defined as

tgo = |rq/p|

|Vp| ,

**Fig. 10:** The relation between terminal angles and terminal velocity vector.

with rq/p representing the relative position vector between the UAV and the target. The guidance gains Nσ and Nf are selected based on the optimal values reported in [22], and are set to Nσ = 6 and Nf = 2 in this study. The relationship between the desired terminal velocity direction Vf and the prescribed impact pitch and yaw angles θf and ψf, as illustrated in Fig. 10, is given by

Vf =

cos θf cos ψf, cos θf sin ψf, −sin θf

T ,

where the impact roll angle does not influence the terminal velocity direction and is therefore neglected. Under the coordinated-flight assumption, the optimal control input obtained from (26) is always perpendicular to the UAV velocity vector. Consequently, when expressed in the UAV body frame, the IAC input can be decomposed solely along the BY and BZ axes as

Bu = Rx(ϕ)Ry(θ)Rz(ψ)u∗

IAC

0 uy uz

The commanded body-rate vector specified in (25) can be determined from the centripetal acceleration experienced during navigation

Bu = ωcmd × BVp =

urVU −uqVU

where BVp =

VU

under the assumption of coordinated flight with negligible sideslip. By setting the resulting acceleration in (27) equal to the commanded acceleration in (28), we obtain:

ωcmd =

−uz

VU uy VU

These are then sent to the flight controller as the ultimate control commands, while up is left uncontrolled because it has no influence on aiming.

**Fig. 11:** Block diagram of the Control architecture.

### D. Control Architecture

The integrated control architecture for Phase 2 and Phase 3 is illustrated in the block diagram in Fig. 11. As the foundational perception layer, the onboard sensor suite provides the UAV’s states, including d, rp, rc, Vp, ωp, ωc. Concurrently, the PT camera captures the target’s image, which is processed by the YOLO algorithm to detect the image-plane target location u, v. These visual and inertial measurements are fused via the UKF to estimate the target’s position rq and velocity Vq.

Based on these estimations, the framework operates in two distinct guidance phases via a Tracking/Terminal phase switch:

1) Phase 2 (Loitering Phase): The NMPC takes rq and Vq, together with the altitude H and radius R, as inputs to compute the UAV control commands VU, up, uq, according to the design in (18). Simultaneously, the IBVS controller regulates the PT rates ˙θp, ˙θt using the target feedback to keep the target centered within the camera’s field of view. 2) Phase 3 (Terminal Engagement Phase): Once the prescribed loitering condition is satisfied, the system switches to Phase 3. The BPNG controller then becomes active, using rq and Vq to generate the commands VU, uq, and ur as specified in (29), thereby guiding the fixed-wing UAV toward the moving target to realize the intended impact configuration.

## IV. SIMULATION

To validate the proposed methods developed in this work, real-time simulations were conducted using the Gazebo simulator [28], which is integrated with the Robot Operating System (ROS Noetic, running on Ubuntu 20.04) and the PX4 autopilot firmware (version 1.13.2).

All simulations1 were performed in a three-dimensional setting to assess the performance of the proposed integrated guidance, control, and estimation framework. A fixed-wing UAV equipped with a pan–tilt camera was modeled to carry out the tracking-to-terminal mission, and a separate threedimensional surface vehicle model served as the moving target.

1https://youtu.be/m4xUBHrImvo

The specifications of both the UAV and the surface vehicle used in the simulations are provided in Table II. This setup allowed for a thorough evaluation of the proposed method, confirming its effectiveness and robustness in dynamic, physically consistent environments.

**TABLE II:** Gazebo Model Specifications.

Model Description Value

Fixed-wing UAV

Fuselage length (m) Wingspan (m) 2.4 Wing area (m2) 0.35

Water Vehicle

Width (m) Length (m) Height (m)

PT Camera

Pan range (rad) −π to +π Tilt range (rad) −π/2 to +π/2 Max. panning vel. (rad/s) 2/3π Max. tilting vel. (rad/s) 2/3π

### A. System Setup

The overall simulation implementation, illustrating the data flow and interaction among the UAV-target dynamics, the estimation modules, and the cooperative controllers within the ROS framework, is presented in Fig. 12. The high-

**Fig. 12:** Simulation system architecture.

fidelity environment is simulated using Gazebo paired with the PX4 Autopilot, which outputs the UAV’s inertial states d, rp, rc, Vp, ωp, ωc, while the simulated ship target provides its true trajectory states rq, Vq for verification.

The mission execution follows a three-phase sequential structure:

• Phase 1 (Target Acquisition): The UAV initially operates in Phase 1, where the PT camera searches for and firmly captures the maritime target. The raw camera images are processed by YOLOv5 to extract the imageplane target coordinates (u, v), establishing a reliable visual tracking lock.

• Phase 2 (NMPC-based Loitering): Once target lock is confirmed, the framework transitions to Phase 2. The NMPC controller is configured with a prediction horizon of N = 50 and a sampling time of ∆T = 0.1 s. During this phase, the UAV is commanded to loiter around the

moving target with a desired planar radius of R = 500 m while maintaining a target altitude of 500 m, regulated via the generated commands VU, up, uq. Concurrently, the IBVS controller regulates the PT rates ˙θp, ˙θt to counteract the airframe motions and mitigate potential self-occlusion risks.

• Phase 3 (BPNG-based Terminal Engagement): When both the desired loiter radius and altitude metrics are successfully satisfied, the Tracking/Terminal phase switch triggers a transition to Phase 3. The BPNG controller takes over from the NMPC to command the UAV inputs (VU, uq, ur), steering the fixed-wing airframe toward the target to fulfill the specified terminal impact angle constraint.

In this simulation, the maritime target vehicle is modeled to move on a horizontal plane with a constant velocity vector, representing a realistic sea-surface tracking scenario. The initial position of the fixed-wing UAV is set in mid-air at (−1000, 0, 1000) m, whereas the target ship departs from the coordinate origin (0, 0, 0) m along the surface.

Visual measurements are actively captured via the onboard PT camera, whose mechanical gimbals are subject to physical constraints: the pan angle is bounded within [−π, π] rad, the tilt angle is limited within [−π/2, π/2] rad. Target detection within the camera’s captured frames is performed by the YOLOv5 vision module, which computes the image-plane coordinates (u, v) of the target’s geometric center. These noisy pixel measurements, along with the UAV’s inertial states from the onboard sensors, serve as the measurement inputs to the UKF. The UKF dynamically filters the sensor noise to yield smooth, real-time target state estimations (ˆrq, ˆVq), which are subsequently distributed to the NMPC, BPNG, and IBVS control loops to close the tactical feedback.

### B. Trajectory and Estimation in Mission Scenario

The complete three-dimensional flight trajectory of the fixed-wing UAV across all operational phases is analyzed in Fig. 13, sweeping across both the horizontal XY-plane and the vertical XZ-plane.

• Phase 1 (Target Acquisition): Operating initially at a cruising altitude of over 1000 m, the UAV actively searches for the moving target along the black dashed trajectory. Once the target is firmly locked by the PT camera, the system smoothly switches to the tracking loop.

• Phase 2 (Cooperative Loitering): As observed in the XY trajectory, the UAV initiates a curved entry maneuver to establish a precise circular loitering pattern with the prescribed radius R = 500 m centered near the moving target. Concurrently, the XZ profile reveals that the UAV is commanded to descend from its initial altitude to the designated 500 m flight ceiling. Maintaining this specific horizontal offset R serves a critical geometric purpose: it effectively avoids the classical IBVS singularity issue discussed in (14) that occurs during direct overhead flight, while the IBVS actively steers the gimbal to counteract

self-occlusion risks induced by the severe roll angles during this loitering firing.

• Phase 3 (Terminal Engagement): Upon satisfying the loitering entry criteria, the control framework activates the Tracking/Terminal phase switch at approximately X = 1200 m. The BPNG controller takes over the autopilot commands, guiding the UAV to break away from its circular orbit. As depicted in the XZ plane, the UAV performs a highly synchronized dive, rapidly sacrificing its altitude from 500 m down to 0 m to intercept the maritime surface target while strictly aligning its velocity vector with the desired terminal impact angle constraint.

**Fig. 13:** The result tracking trajectory for fixed-wing UAV.

**Fig. 14:** The distance between the target and the UAV in the XY plane.

**Figure 14** depicts the horizontal separation between the UAV and the target throughout the tracking phase. Beginning

from a significant initial offset, the NMPC controller effectively follows the target while preserving the desired standoff distance (e.g., R=500 m). The tracking phase concludes when the UAV attains a predefined transition altitude of 500 m relative to the target—illustrated in the XZ plane in Fig. 13—at which point control authority is handed over to the BPNG controller for terminal guidance. This altitude serves as an arbitrarily chosen transition threshold rather than a tuned parameter and can be modified without requiring changes to the NMPC framework, since the controller independently steers the UAV to the prescribed terminal condition.

**Fig. 15:** Comparison of the estimated target position in the x-direction obtained by the UKF and the ground truth.

**Fig. 16:** Comparison of the estimated target position in the y-direction obtained by the UKF and the ground truth.

**Fig. 17:** Comparison of the estimated target velocity in the x-direction obtained by the UKF and the ground truth.

**Fig. 18:** Comparison of the estimated target velocity in the y-direction obtained by the UKF and the ground truth.

**Fig. 19:** Position estimation error and RMSE in the x-direction.

**Fig. 20:** Position estimation error and RMSE in the y-direction.

**Fig. 21:** Velocity estimation error and RMSE in the xdirection.

**Fig. 22:** Velocity estimation error and RMSE in the ydirection.

The UKF-derived estimates of the target’s position and velocity are depicted in Fig. 15-18, while the associated estimation errors and RMSE are shown in Fig. 19-22. The position errors remain within 8 m, which is small compared to the surface vehicle’s dimensions (see Table II) and therefore does not impair tracking performance. These results demonstrate that the UKF yields accurate and robust state estimates of the target relative to the fixed-wing UAV. After convergence is reached via persistent visual measurements, the estimated velocity aligns closely with the ground truth. In summary, the UKF successfully reconstructs the unknown target trajectory, with its effectiveness contingent on continuous visual feedback during the tracking process.

### C. Visual Tracking Performance

**Fig. 23:** The error between the target and the FOV center.

**Fig. 24:** The percentage error between the detected target and FOV center.

The tracking error metrics and the corresponding imageplane target pixel trajectories are illustrated in Fig. 23 and

**Fig. 24.** The tracking error is quantified as the pixel displacement between the image center origin (640, 360) and the target centroid bounding box detected by the YOLOv5 vision module. Given the camera’s resolution of 1280 × 720 pixels, these figures directly evaluate the transient and steady-state authority of the IBVS loop in commanding the PT rates.

Throughout all operational phases, the IBVS controller successfully constrains the moving target well within the camera’s field of view (FOV), preventing target loss. Distinct geometric characteristics can be observed between the horizontal (u) and vertical (v) error axes. The tracking error and high-frequency fluctuations in the vertical v-direction are noticeably larger than those in the horizontal u-direction. Rather than being a artifact of resolution scaling, this asymmetry is primarily attributed to the intense longitudinal coupled dynamics; the dramatic altitude variation and aggressive pitching maneuvers during the loitering transition and the subsequent terminal dive directly excite the gimbal’s tilt axis. Nevertheless, the IBVS loop demonstrates rapid disturbance rejection, consistently pulling the tracking error back toward the steady-state bounds.

Particularly during the Phase 3 terminal engagement, despite the transient spikes triggered by the tracking-to-terminal controller handoff, the target pixel coordinates are kept tightly centered. These pixel measurements are continuously fed into the measurement update step of the UKF, ensuring the estimation loop receives high-rate, reliable tracking lines. These results confirm that the integrated IBVS-gimbal system achieves stable, highly robust visual tracking, providing a critical tactical cornerstone for the closed-loop guidance architecture.

### D. Terminal Impact Angle

In this section, the terminal engagement performance of the UAV managed by the BPNG scheme during Phase 3 is critically analyzed. Upon entering Phase 3 at t ≈146 s, the guidance architecture seamlessly transitions control authority to the BPNG law to intercept the mobile ground target. Fig. 25 illustrates the temporal evolution of the UAV’s velocity heading Euler angles (yaw ψ and pitch θ).

Unlike stationary intercept scenarios, the moving target geometry demands highly dynamic corrections. As depicted in the profiles, the heading angles do not simply converge monotonically; instead, they exhibit substantial tactical adjustments to satisfy the strict terminal constraint vectors. In the longitudinal plane, the pitch angle undergoes a steep diving maneuver, temporarily overshooting to approximately −60◦

near t = 171 s to rapidly deplete altitude, before the BPNG aggressively pulls the aircraft back to precisely settle at the designated impact pitch of θf = −30◦at the final intercept instant.

Simultaneously, the heading yaw angle corrects its loitering orientation—transitioning from the periodic wrapping profiles observed in Phase 2—and aligns tightly with the specified impact yaw of ψf = 30◦. These localized terminal corrections effectively demonstrate the capability of the biased proportional navigation law to decouple and satisfy both the interception requirement and the highly restricted directional impact angles simultaneously under highly dynamic simulation environments.

**Fig. 25:** The Euler angle of the UAV’s velocity direction.

### E. Evaluation of Self-Occlusion

To avoid self-occlusion as discussed in Section III-B2, the geometric condition in (20) constrains the UAV’s roll with respect to the target, ensuring that the PT joint remains within its operational range throughout the target tracking task. These constraints are realized in (23) and (24), which convert the UAV pose restrictions into input-level constraints in the NMPC framework.

The performance of these constraints is assessed using a comparable simulation that isolates Phase 2. Two illustrative cases are examined, representing clockwise (CW) and counterclockwise (CCW) circling, where the Phase 2 NMPC enforces a circular path at a specified stand-off distance from the moving target. The direction of circling is selected based on the target’s initial lateral position with respect to the UAV.

To evaluate the effectiveness of the CBF constraint defined in (23) and (24), two scenarios are examined: operation without the CBF constraint and operation with it. The unconstrained scenario is shown in Fig. 26, where θt becomes positive and the joint limit is surpassed in order to keep tracking the target, which leads to visual occlusion. In contrast, Figs. 27 and 28 present the tilt angle under the proposed CBF constraint, showing that the tilt remains within its normal operating range while keeping the target inside the camera’s FOV. This prevents UAV self-occlusion and confirms that the proposed UAV pose constraints reliably guarantee visual tracking.

**Fig. 26:** Tilt angle during a tracking mission carried out without applying the proposed CBF constraint.

**Fig. 27:** Tilt angle during the clockwise tracking mission subject to the proposed CBF constraint.

**Fig. 28:** Tilt angle during a counterclockwise tracking mission under the proposed CBF-based constraint.

## V. CONCLUSION

This work presented an integrated control framework for fixed-wing UAVs, combining NMPC, IBVS, and BPNG to facilitate a seamless transition from target tracking to terminal engagement. The proposed architecture addresses the critical challenges of long-endurance tracking by fusing YOLObased visual observations with an Unscented Kalman Filter, enabling robust state estimation of moving targets with unknown dynamics. By embedding CBFs within the NMPC, we successfully mitigated the risk of airframe-induced selfocclusion, ensuring continuous visual contact and gimbal stability throughout the loitering phase. Furthermore, the implementation of a quaternion-based BPNG law proved highly

effective in guiding the UAV toward the moving target while satisfying strict impact angle constraints. High-fidelity simulation results validated the robustness of the entire framework, confirming its capability to handle realistic dynamic limits and maintain precise engagement. Future work will focus on improving resilience against temporary target loss through predictive gimbal pointing strategies and enhancing the UKF with adaptive motion models to further optimize performance in complex, dynamic maritime environments.
