---
id: arxiv-2505.23355-grower-loop-interactive-reinforcement-learning
title: "Grower-in-the-Loop Interactive Reinforcement Learning for Greenhouse Climate Control"
year: 2025
backend: grobid
---

## Abstract

Climate control is crucial for greenhouse production as it directly affects crop growth and resource use. Reinforcement learning (RL) has received increasing attention in this field, but still faces challenges, including limited training efficiency and high reliance on initial learning conditions. Interactive RL, which combines human (grower) input with the RL agent's learning, offers a potential solution to overcome these challenges. However, interactive RL has not yet been applied to greenhouse climate control and may face challenges related to imperfect inputs. Therefore, this paper aims to explore the possibility and performance of applying interactive RL with imperfect inputs into greenhouse climate control, by: (1) developing three representative interactive RL algorithms tailored for greenhouse climate control (reward shaping, policy shaping and control sharing); (2) analyzing how input characteristics are often contradicting, and how the trade-offs between them make grower's inputs difficult to perfect; (3) proposing a neural network-based approach to enhance the robust-

## 1. Introduction

In response to the threat that climate change poses to global food security, greenhouse production has emerged as a vital strategy for mitigating risks and enhancing food production efficiency worldwide [1,2,3]. Within greenhouse systems, climate control plays a critical role, as it directly influences plant growth by regulating key environmental factors such as temperature, humidity, and CO 2 concentration. However, climate control is also one of the most significant sources of energy consumption in greenhouse operations [4]. Looking ahead, greenhouse horticulture faces several pressing challenges, including high energy demands [5], as well as a shortage of skilled labor and experienced managers [6].

Therefore, developing optimal and autonomous climate control systems is essential for improving crop productivity while minimizing energy and resource consumption.

Over the past years, various control methods have been investigated and can be broadly classified into model-based and non-model-based approaches [7].

Model-based methods rely on a presentation (model) of the greenhouse system (climate, crop, and economic). Among them, model predictive control (MPC) is the most common approach due to its ability to handle the complexity of the greenhouse system [8,9]. MPC predicts the future behavior of the system using a model and optimizes its strategy accordingly. In contrast, non-modelbased methods rely on knowledge, experience, or data. This type of method includes expert systems [10], fuzzy logic [11], and genetic algorithms [12]. However, these methods can't guarantee optimality as they don't include dynamic optimization [7].

Recently, reinforcement learning (RL) has attracted growing attention in greenhouse climate control. RL is a learning-based method with a model-free nature and adaptive learning capabilities. These features enable RL to perform effectively in complex, error-prone, and uncertain environments [13] [14], which are characteristic of greenhouse systems. As a data-driven approach, RL can continuously optimize control strategies while adapting to dynamic envi-ronmental conditions. Several studies have already evaluated RL in simulated greenhouse settings [15,16,17], demonstrating its potential for achieving optimal climate control. Despite these promising results, RL applications in greenhouse climate management still face significant challenges. Among the most frequently mentioned limitations are low learning efficiency and limited robustness [17]. Moreover, current RL approaches often exclude growers from the control loop, failing to leverage their domain knowledge and practical experience, which could enhance learning efficiency. This lack of involvement may also lead to growers' reluctance to adopt RL or other artificial intelligence methods in real-world applications, as they have limited control or understanding of the decision-making process.

Interactive RL is a variant of RL that incorporates human input into the training process. In this approach, the RL agent learns through interactions with both the environment and human feedback. Interactive RL has been tested on classic control tasks like Pac-Man [18], MountainCar [19], and CartPole [19], and more complicated environments like robotic arm control [20]. These studies have demonstrated that interactive RL can surpass traditional RL in terms of both training efficiency and overall performance. However, to the best of our knowledge, interactive RL has not yet been explored in the context of greenhouse climate control. In addition, inputs in greenhouse climate control are difficult to perfect and could present a potential challenge for interactive RL.

Given this background, this paper aims to explore the feasibility and performance of applying interactive RL with imperfect inputs to greenhouse climate control. The main contributions are summarized as follows:

• We developed three representative interactive RL algorithms tailored for greenhouse climate control: policy shaping, which uses grower advice on actions; control sharing, and reward shaping, both of which rely on grower's feedback regarding control performance.

• We analyzed how input characteristics are often contradicting, and how the trade-offs between them make grower's inputs difficult to perfect. We also discuss the potential shortcomings of different methods inputs can be provided.

• We proposed a neural network-based approach to enhance the robustness of interactive RL agents under limited input availability by incorporating additional neural networks to aggregate grower's input.

• We conducted a comprehensive evaluation and comparison of the three interactive RL algorithms in a simulated greenhouse environment, considering the potential variability and characteristics of actual grower input.

The remainder of the paper is organized as follows. Section 2 introduces the simulated greenhouse environment, the baseline RL algorithm, and the background of interactive RL. Section 3 presents the characteristics of imperfect inputs and how they are simulated. Section 4 introduces the proposed interactive RL algorithms. The evaluation results are then presented and discussed in Section 5. Finally, Section 6 draws the conclusion as well as provides future work and recommendations.

## 2. Introduction of Greenhouse Environment and RL

This section begins by introducing the simulated greenhouse environment employed in this paper. It then describes the baseline RL algorithm used, followed by an overview of the interactive RL framework.

### 2.1. Greenhouse Environment

This paper investigates a simulated lettuce greenhouse environment under winter weather conditions, as illustrated in Figure 1, using the system dynamic model from [21]. Details of the model are presented in the Appendix. The model is discretized using the Runge-Kutta fourth-order method with a step size of 15 minutes. Modification to the model input is made as follows: inputs (heating and CO 2 injection rate) are converted into setpoints using proportional-integral (PI) control. These two inputs are converted since providing setpoints as input is more intuitive for growers. However, the ventilation rate is not converted, as it passively influences all climate variables. Table 1 summarizes the state and action space of the greenhouse environment.

The action space of the environment is discrete, with three dimensions: adjusting temperature setpoints, adjusting CO 2 setpoints, and adjusting ventilation rate. This results in a total of 27 possible actions. The control interval of the environment is one hour, while the actuator settings (heating and CO 2 injection rate) are updated every 15 minutes using PI control. The reward function (object function to be maximized) is the profit of the greenhouse minus a penalty, formulated as follows:

reward = p lettuce • ∆ dryweight -(p CO2 • u CO2 + p heat • u heat ) -penalty, (1)

where p lettuce is the price of lettuce (16 Hfl/kg), ∆ dryweight is the change in lettuce dry weight (kg/m 2 ), p CO2 is the price of CO 2 supply (0.42 Hfl/kg), u CO2 is the usage of CO 2 supply (kg/m 2 ), p heat is the price of heating (6.35×10 -9 Hfl/J), u heat is the usage of heating (J/m 2 ), penalty is the cost if constraint violated (5.24×10 -3 Hfl/m 2 ). Note that the price of lettuce, heating, and CO 2 are obtained from [16]. The penalty is applied when indoor climate constraints [21] (shown in Table 2) are violated. The weather data used in the environment and episode length are further detailed in Section 5.1.

### 2.2. Baseline RL Algorithm

This paper considers the Proximal Policy Optimization (PPO) [22] implemented in Stable-Baselines3 [23] as the baseline RL algorithm. PPO is selected because its policy is in the form of a probability distribution, which facilitates influencing the action selection of the RL agent.

PPO uses the actor-critic architecture shown in Figure 2, where the critic estimates the value function of the state, while the actor represents the policy of the RL agent in the form of a probability distribution. During training, the critic estimates a baseline value for the actor's current policy. Policies that perform better than the current policy are encouraged, while those that perform worse are discouraged.

Define the temporal difference (TD) at time t as δ t with

δ t = r t + γv π (s t+1 ) -v π (s t ),(2)

where r t is the reward at time t, v π (s t ) is the value of s t under policy π, γ is the discount factor.

The level of encouragement or discouragement is based on the generalized advantage estimation (GAE) A t , which estimates how much better or worse a policy is compared to the baseline estimation. A t is computed by

A t = δ t + (γλ)δ t+1 + • • • + (γλ) T -t+1 δ T -1 = -v π (s t ) + r t + (γλ)r t+1 + • • • + (γλ) T -t v π (s T ),(3)

where GAE trace parameter λ combines multi-step δ t to balance the trade-off between bias and variance.

### 2.3. Interactive RL Backgrounds

In baseline RL, human involvement is typically limited to the design of the reward function. In contrast, interactive RL allows for a greater degree of human participation throughout the learning process. Interactive RL algorithms have been successfully applied across a variety of control tasks, ranging from simple environments (Pacman, Gridworld) [18,19] to more complex, realistic scenarios (robot arm control) [20]. These studies have demonstrated that interactive RL can surpass baseline RL in both learning efficiency and overall performance.

In interactive RL, human inputs can be integrated into the learning process through three approaches [13,24]: reward shaping, policy shaping, and guided exploration. A more detailed overview of these three approaches is presented in Table 3 and elaborated upon below.

Reward Shaping. This approach involves modifying the reward function of the RL agent to incorporate additional sources of information. A seminal contribution to this line of work is the TAMER framework proposed by [27], which has

### Approach Type of Input Adoption Stage Example

Reward shaping Feedback Reward function [25] Policy shaping Action advice Action selection [18], [26] Guided exploration Feedback / Action advice Action selection [25] been widely adopted in interactive RL. In TAMER, the agent learns a feedback function F (s, a) that estimates human-provided feedback, rather than directly learning the Q-function. Building on this foundation, the authors later introduced the DQN-TAMER framework [25], which integrates both human feedback and environment-generated rewards. In their study, they evaluated eight different methods for combining these two sources of information. Among these, reward shaping emerged as an intuitive and effective strategy, and can be formally expressed as follows:

r ′ (s, a) = r(s, a) + β • F (s, a),(4)

where the environment-generated reward r(s, a) is reshaped by adding a weighted estimated feedback F (s, a).

Policy shaping and guided exploration. These two approach both influence the action selection process of the RL agent, but differ in the manner in which this influence is exerted. Policy shaping [18] reshapes the agent's policy by incorporating:

P (s, a) =          1 -β, a = π agent (s, a) β, a = π agent (s, a) • π input (s, a) a ′ ∈A π agent (s, a ′ ) • π input (s, a ′ ) ,(5)

where P (s, a) is the final probability of selecting action a at state s, π agent (s, a)

is the probability of selecting action a at state s under the agent's policy, and

π input (s, a)

is the probability of selecting action a at state s under the input's policy.

Equation ( 5) defines a mixed policy: with probability 1 -β, the agent relies on the agent's policy, and with probability β, it samples from a mixed distribution that combines both the agent's and input's policy. Since this requires that the policy π agent (s) be expressed as probabilities of each action, it is typically applied to policy-based algorithms with stochastic policies (PPO, A2C, etc.).

Guided exploration. In contrast, guided exploration overrides the action selected by the RL agent to guide its exploration [24], instead of modifying the policy.

This makes it applicable to both value-based algorithms and policy-based algorithms.

## 3. Grower's Input

Although interactive RL has the potential to outperform baseline RL, it relies on high-quality input to do so [28]. This section begins by outlining the types of input used in interactive RL and the characteristics these inputs must possess. It then examines how, in the context of greenhouse climate control, these desirable characteristics often conflict with one another, creating tradeoffs that make it challenging for growers to provide optimal input. Finally, the section details the method employed in this study to simulate imperfect inputs.

### 3.1. Human Input in Interactive RL

In interactive RL, human inputs can be categorized into three types: binary critique feedback, scalar-valued feedback, and action advice [24]. Both binary and scalar-valued feedback relate to the action selected by the agent. Binary feedback simply labels the action as "good" or "bad", whereas scalar-valued feedback provides a quantitative evaluation of the action. In contrast, action advice specifies either the optimal action or the probability distribution over all possible actions. Beyond the form of information, the scope of input also differs:

feedback pertains only to the selected action, while action advice provides information about the entire action space. In interactive RL, the quality of input Table 4: Characteristics of human input [28].

### Characteristic Description

Accuracy How appropriate inputs are to the current situation.

is crucial for successive learning [28]. The quality of input can be assessed by seven characteristics [28], summarized in Table 4.

### 3.2. Characteristics of Grower's Input

In greenhouse climate control, grower's inputs are difficult to perfect due to the trade-offs between these four key characteristics: availability, cognitive bias, latency, and knowledge level. These characteristics are discussed in detail below.

Availability. It refers to the accessibility and willingness of human experts to provide input. While RL agents are often trained in simulated greenhouse environments to reduce time and costs, this setup demands a large volume of input within a short period. Given the repetitive and time-consuming nature of providing inputs, growers may find the task tedious and exhausting, which diminishes their willingness to participate. As a result, querying growers at every step of the training process is impractical, leading to low input availability.

To address this issue, two main strategies are commonly used: applying predefined simple rules or leveraging pre-extracted grower knowledge, such as expert systems. However, both approaches have drawbacks. They may introduce cognitive bias and often lack the depth and nuance of real expert input, thereby reducing the overall knowledge level of the guidance provided.

Cognitive bias. This refers to the misalignment between the RL agent's objective of maximizing final profit and the grower's actual decision-making priorities.

Aligning input with the agent's goal requires complex decision-making under uncertainty, similar to dynamic optimization, which reduces input availability due to the need for frequent grower involvement. To improve availability, preextracted grower knowledge (e.g., expert rules) is often used, but this introduces greater cognitive bias. Growers may prioritize crop physiology over profit due to the long production cycles and economic uncertainties in greenhouse operations.

This risk-averse approach aims to ensure high yield and quality, indirectly supporting profitability. Even when grower input targets profit, it often lacks the adaptability of dynamic optimization, limiting its effectiveness under uncertain and changing conditions [7].

Latency. Input with minimal cognitive bias can also lead to increased latency, which refers to delays in providing input. Latency is particularly problematic for action advice, as it must be delivered during the agent's action selection process. In greenhouse production, long growing cycles mean that the final profit, often the target of optimization, is only known at the end of the cycle, resulting in inherently high latency.

### 3.3. Simulation of Growers' Imperfect Inputs

In this paper, three types of simulated inputs are designed, as detailed in Table 5. Both precise action advice and constraint advice are forms of action advice that provide probabilities for each action, but they differ in knowledge level. Feedback with a low knowledge level is excluded, as using feedback to enforce constraints (ranges) is a common practice in RL.

All three types of simulated inputs are based on pre-extracted knowledge and inherently contain cognitive bias. They are categorized into two knowledge levels: low and high. Inputs with a low knowledge level specify suitable ranges (constraints) for climate variables, as detailed in Table 6. In contrast, inputs with a high knowledge level provide optimal climate variable values aiming at maximizing current crop growth. These optimal values are pre-calculated and approximated using interpolation to facilitate faster input generation.

Figure 3 illustrates examples of the three input types, focusing solely on temperature. In constraint advice, actions that keep the temperature within the specified range are assigned equal probabilities of selection. Precise action advice sets the temperature as close as possible to the optimal setpoint. Feedback is provided after the outcome of the action (S t+1 ) is observed, evaluating whether the resulting temperature is closer to the optimal value compared to the potential effects of alternative actions.

## 4. Interactive RL for Greenhouse Climate Control

This section begins by explaining how the three types of inputs described in Section 3.3 are integrated into PPO. It then introduces a neural network-based approach to enhance the robustness of interactive RL agents when input availability is limited. Finally, it describes the proposed interactive RL algorithm.

### 4.1. Incorporating Grower's Inputs

In this work, reward shaping and control sharing are employed to incorporate grower feedback, while policy shaping is used to implement the two types of action advices. As introduced in Section 2.3, both guided exploration and policy shaping influence action selection. Since PPO is a policy-based algorithm with a stochastic policy, these two approaches are quite similar and are expected to yield comparable performance. Nonetheless, control sharing, a form of guided exploration, is still being evaluated in this work because it allows direct influence on action selection through feedback. Moreover, although using reward shaping to incorporate feedback is intuitive because feedback resembles the human-designed reward function, prior studies suggest that it has limitations since it modifies the reward signal and only affects the policy indirectly [25],

whereas control sharing may leverage feedback more effectively.

The used reward shaping and control sharing are adapted from the DQN-TAMER framework [27,25]. Reward shaping modifies the reward according to (4), while control sharing influences action selection by overriding the RL agent's policy as below:

P (a) =      1 -β, a = π agent (s, a) β, a = arg max a (F (s, a)) .(6)

Both two approaches employ a weighting factor (likelihood) β to regulate the degree of input involvement. Additionally, an auxiliary neural network (the F function) is introduced to estimate feedback in both methods. The F function takes state variables as input and outputs estimated feedback values for each possible action.

Policy shaping [26] is chosen to incorporate both types of action advices. It influences action selection according to (5). Additionally, a new neural network, π grower , is introduced to estimate the action advice, similar to the F function used in the DQN-TAMER framework.

### 4.2. Addressing Limited Availability

In all three algorithms, an additional network (F function or π grower ) is used to estimate the input. This network not only facilitates the control sharing method but also enhances the algorithm's tolerance to limited input availability and high latency. This capability is especially important when inputs must be obtained by querying growers at every step or when providing input demands significant time and effort.

With the additional network (F function or π grower ), the goal of providing inputs to the agent's training is similar to active learning: maximize the learning efficiency of input estimation with minimal input given. As in active learning, two sampling approaches exist: pool-based and stream-based. This paper only focuses on the pool-based approach for two reasons: First, the pool-based approach has better sample efficiency [29], which suits the needs of limited input while not reach update interval do 6:

Interact with the environment using the estimated input

7:

end while

8:

Select n steps to provide inputs

9:

Add provided input to D input 10:

Update the PPO agent 11:

Update the F function (π grower ) and π error (if exists) using D input for N iterations 12: end while availability better. Second, the stream-based approach requires immediate decisions (one chance per step), increasing complexity and potentially the burden of the grower if the final decision is given by the grower.

As in active learning, it is essential to efficiently select which steps to provide input. Within pool-based approach, two selection strategies are compared in this paper: a random strategy and a selective strategy. The random strategy samples input steps randomly, while the selective strategy is inspired by SafeDAgger [30].

In the selective strategy, a new neural network, π error , is introduced to estimate the discrepancy between the simulated input and the model's estimated input.

Inputs are provided only at steps with high predicted discrepancy. Mean squared error is used to quantify the discrepancy for feedback, while Kullback-Leibler (KL) divergence is applied for action advice.

### 4.3. Interactive RL Implementation

The implemented interactive RL algorithms are detailed in Algorithm 1.

Modifications to the baseline PPO framework for incorporating grower inputs and addressing limited input availability are emphasized in bold. In addition to the introduction of auxiliary neural networks, a new buffer, D input , is implemented to store data for updating these networks. Furthermore, three new hyperparameters are defined: the weight factor β, the number of inputs n, and the number of update iterations N . The weight factor β regulates the influence of grower input, as described in ( 4), ( 5), and ( 6). The parameter n constrains the number of inputs provided during each update interval. The number of update iterations N specifies the number of times the auxiliary networks are updated within each interval.

## 5. Results and Discussion

This section presents a comprehensive evaluation and comparison of the three interactive RL algorithms using simulated imperfect inputs. It begins by describing the experimental setup and training hyperparameters. Subsequently, it evaluates and discusses the performance of the three interactive RL algorithms, the effect of input weight (likelihood), and the influence of input availability.

### 5.1. Experiment Settings

Hourly weather data from Den Haag [31] is used to provide outdoor weather for the lettuce greenhouse environment. This dataset includes hourly global radiation, temperature, and humidity. As CO 2 levels are not included, they are assumed to be constant at 400 ppm, since the global average CO 2 is around 400 ppm [32].

For training, each episode spans 14 days (336 steps). The full lettuce growth cycle (56 days) is not used for training due to its long episode, as overly long episodes would cause rollout rewards to reflect outdated training trajectories, and the rollout reward is used as part of the result. However, using an episode length too short might cause challenges for the RL agent to optimize the longterm goal. Through tuning, 14 days were selected for this project. The initial dry weight is randomly sampled between 3.5 g and 300 g. By doing so, all potential dry weights were included in the shortened episode. Start dates are randomly selected between November and February from the years 2011 to 2020 to reflect typical winter conditions.

For testing, each episode covers a complete 56-day growth cycle, beginning with an initial dry weight of 3.5 g. Weather data from 2021 to 2024 is used. For each year, two test trajectories are selected: one from January 1st to February 25th, and another from December 1st to January 25th of the following year. In total, seven trajectories are used for evaluation.

### 5.2. RL Agent Training

The hyperparameters used to train the PPO agent are summarized in Table 7 and Table 8. The value of these hyperparameters is determined by tuning. The parameters listed in Table 7 are applied consistently across all RL agents, while those in Table 8 are specific to the interactive RL algorithms. Among these, the input weight (likelihood) β and the number of inputs n are varied to evaluate their impact on the agent's performance. In all experiments, the input weight (likelihood) β is linearly decreased from its initial value to zero over the first 400,000 steps and remains at zero thereafter. The entropy coefficient, which promotes exploration behavior [33], is also adjusted in interactive RL settings. It is reduced in control sharing and in policy shaping with precise action advice, as both approaches inherently encourage exploration. To mitigate result variance, each configuration (algorithm, input weight, etc.) is trained using 15 seeds (100, 200, . . . , 1500).

### 5.3. Performance of Interactive RL

Table 9 shows the average cumulative reward of interactive RL algorithms in the test environment. In all experiments, the availability of inputs is full, and the input weights (likelihood) β are chosen to be the ones that work best in the test. Additionally, baseline PPO using only simulated feedback as the reward function is also trained and tested, with its test reward reduced to only 0.71 Hfl/m 2 . This is expected and indicates that the simulated inputs are far from perfect. The policy shaping using precise action advice performs best in this environment, with 8.4% improvement. Policy shaping using constraints and control sharing also increase rewards. However, reward shaping reduces the reward, indicating that it is more sensitive to the quality of input. Policy shaping with precise advice and control sharing each achieves about 10% reductions in energy and CO 2 usage. Policy shaping with constraint advice only reduces its energy usage by less than 10%, while its CO 2 usage is only slightly reduced compared with baseline PPO. In contrast, reward shaping lowers both energy and CO 2 usage but also reduces the harvested weight, resulting in a 9.4% decrease in profit relative to baseline PPO.

Figure 5 shows the average setpoints and indoor climate variables for each hour of the day. All interactive RL algorithms, except for reward shaping, show a similar pattern. They maintain lower temperature setpoints and consequently lower indoor temperatures than the baseline PPO. Notably, indoor temperatures and CO 2 setpoints are generally higher than the corresponding indoor values, and high indoor CO 2 and indoor values are observed at night. This is due to several factors: First, the greenhouse environment has no actuator that can actively reduce temperature or CO 2 level. Second, in the later stage of the growing cycle, the plant's respiration can produce a large amount of CO 2 . Third, since there are no violation constraints on high CO 2 level or temperature at night and relative humidity remains within constraints, the agent is not motivated to use ventilation to lower these variables.

In contrast, reward shaping shows a different pattern. It maintains low temperature setpoints and CO 2 setpoints at night. This is because it receives positive feedback for doing so, without extra cost. During the day, it also maintains low temperature setpoints and CO 2 setpoints, due to the conflict between the reward and the feedback.

The comparison of interactive RL algorithms suggests that even imperfect inputs can improve the RL agent's performance, except for reward shaping. In contrast, reward shaping follows the feedback's underlying policy and fails to improve the performance of the RL agent. Reward shaping faces the conflict between the reward and the feedback. Manipulating reward functions with imperfect feedback may misguide the learning process [19,25]. Therefore, making it more sensitive to imperfect inputs than other algorithms.

Policy shaping and control sharing improve performance even when using imperfect input. This is probably because PPO uses GAE to improve its policy.

As shown in (3), GAE is a type of advantage function that calculates how much better or worse taking an action is compared to v π (s). Both policy shaping and control sharing incorporate inputs by influencing the action selection of the RL agent. Since using feedback as the reward function reduces cumulative rollout rewards, v π (s) can be underestimated when incorporating imperfect inputs, leading to higher GAE estimates, which can accelerate learning. Also, an underestimated v π (s) improves exploration [34], which can help the RL agent explore a better policy.

### 5.4. Impact of Input Weight (Likelihood)

The input weight (likelihood) significantly influences the performance of interactive RL algorithms. This section focuses on examining its impact in the context of policy shaping with precise action advice, as the effect of likelihood on the other algorithms exhibits similar trends. This result shows that proper input weight (likelihood) is crucial for interactive RL algorithms. Using a proper range of likelihood improves performance. However, a too high likelihood does not improve the performance (accelerates learning), especially in the early stage of training. This is probably also due to PPO using GAE as well.

Figure 7 shows how the likelihood β influences the performance. In the early stage of training, the RL agent struggles to find a policy better than the input. As the likelihood increases, the RL agent takes good actions (input) more frequently, and the critic overestimates v π (s). As shown in Figure 6 A, increasing likelihood leads to higher rollout rewards in the early stages of training. This suggests that the RL agent selects actions with high rewards more frequently, and v π (s) can be overestimated. As v π (s) is overestimated, GAE estimates decrease, and the policy learns more slowly. Therefore, a too high β accelerates the increase of rollout rewards but does not translate to high test rewards. On the other hand, when β is low, although v π (s) is slightly overestimated and the policy learns slightly slower, good actions (input) still have a bigger chance of being selected. Therefore, the policy may learn slightly slower to slightly faster (depending on the likelihood β).

In the later stage of training, the RL agent has already learned a policy better than the input. In this case, incorporating inputs leads to an underestimation of v π (s), which makes the policy learns faster. With a low β, the agent can still explore and exploit the environment based on its own policy to find a better policy. However, with a high β, the agent has a smaller chance of selecting actions based on its exploration. Therefore, good actions might be missed, and the policy learns more slowly. A reduction in the number of inputs leads to a significant increase in the loss of the F function. Additionally, the selective strategy does not reduce the loss compared to the random strategy, except when 256 inputs are used per update interval. Figure 9 presents the changes in the loss of π grower (policy shaping).

### 5.5. Impact of Input Availability

At the initial time step, the loss is 2.23 and then decreases rapidly. Across all three cases, the selective strategy either does not increase the loss (for 1024 and These results indicate that the impact of limited input availability differs between the two types of inputs. For feedback under control sharing, neither the selective nor the random strategy is effective in maintaining a low loss for the F function. In contrast, for action advice, the selective strategy consistently outperforms the random strategy in reducing the loss of π grower . This distinction suggests that action advice is less sensitive to limited input availability than feedback. The effectiveness of the selective strategy in the context of action advice further implies that selecting inputs based on estimated discrepancy yields more informative updates, thereby enhancing the learning efficiency of π grower .

512 inputs) or only slightly increases it (for 256 inputs) during the early stages of training. Moreover, the selective strategy consistently results in a lower loss of π grower compared to the random strategy across all input levels. It is also noteworthy that the loss increases during the later stages of training in the cases with 512 and 256 inputs per update interval, regardless of the strategy employed.

Additionally, the increase in loss observed during the later stages of training in Figure 9 C suggests that π grower may be overfitting, which could hinder its generalization to unseen data. Future work may address this issue by incorporating regularization techniques or applying early stopping to improve generalization performance.

## 6. Conclusion

Interactive RL combines human (grower) input with the RL agent's learning to improve the overall performance of the RL agent. This method uses a neural network to estimate inputs and convert providing inputs to a process similar to pool-based active learning. The test results indicate that action advice is more robust to limited availability than feedback, particularly when using the discrepancy-based selection strategy.

Despite the contributions, this work has certain limitations that can be addressed in future research. Only PPO is selected as the baseline RL algorithm.

As discussed, GAE used in PPO might be the reason why policy shaping and control sharing are robust to imperfect inputs and sensitive to the level of input incorporation. However, this may not be true for other RL algorithms.

The performance of RL algorithms without using the advantage function may not be improved, which is not explored in this work. Additionally, in the DQN-TAMER framework [19], a too-high level of input incorporation also led to worse performance, but a higher level of input incorporation is tolerated.

Future work should explore interactive RL in continuous action spaces and its integration with other RL algorithms. Additionally, it is important to understand grower's control strategy and decision-making process. For example, inverse RL can be used to understand grower's underlying intention and goal.

This not only helps with providing better inputs, but can also improve reward design for RL agents. It also enables growers to gain a clearer understanding of their intentions and strategies, helping them to prioritize decisions more effectively.

## APPENDIX

The lettuce greenhouse model is described by the following equations: • x 4 (t), %,

dx 1 (t) dt = p 1,1 ϕ phot,c(t)

The model parameters p i,j are defined and presented in Table 11.

## Figures et tableaux

**Figure 1:** Schematic diagram of the lettuce greenhouse environment [21].

**Figure 2:** Actor-critic architecture [22].

**Figure 3:** Examples of simulated grower giving input.

Algorithm 1 2: 3: 4: The proposed interactive RL algorithm 1: Initialize PPO agent Initialize F function (π grower ), π error (for the selective strategy), and buffer D input Set hyperparameters: β, n, and N while not reach total timesteps do 5:

**Figure 4** further compares the performance of interactive RL algorithms to baseline PPO. Except for reward shaping, all interactive RL algorithms maintain a similar harvested lettuce weight while reducing energy and CO 2 usage.

**Figure 4:** Performance of interactive RL algorithms relative to baseline (Vanilla) PPO.

**Figure 5:** Average setpoints and indoor climate variables over a day.

**Figure 6:** Impact of the likelihood for policy shaping with precise advice. A: rollout reward, B: test reward.

**Figure 6** illustrates the evolution of rollout and test rewards during training.The rollout reward refers to the cumulative reward obtained by the RL agent during training and reflects the quality of the agent's actions within the training environment. As expected, a higher input likelihood accelerates the increase in rollout rewards during the early stages of training. However, this early improvement does not correspond to higher test rewards; instead, it results in lower test performance. Moreover, an excessively high initial likelihood (e.g., β = 0.5) leads to slightly reduced rollout rewards in the later stages of training, likely due to the way PPO leverages the advantage function to update its policy. In contrast, using a moderately low initial likelihood (β in the range of 0.05 to 0.2) yields improvements in both rollout and test rewards.

**Figure 7:** Impact of the likelihood for policy shaping with precise advice.

Figures 8 and 9 Figures8 and 9show the changes in the average test loss of F function (π grower ). Each update interval consists of 2048 steps. When 1024 inputs are provided, this corresponds to input being available for only half of the steps within each interval. The test data is generated by allowing both a well-trained and a poorly trained RL agent to interact with the test environment. Simulated inputs corresponding to these interactions are then collected to form the test dataset. Including both well-trained and poorly trained agents ensures a more balanced and representative test set. In both figures, the time steps are limited to 400,000 instead of 500,000, as estimated inputs are not utilized during the final 100,000 steps, and the F function (π grower ) is no longer updated during this period.

**Figure 8** depicts the changes in the loss of the F function (control sharing).

**Figure 8:** Changes in the average loss of F function (control sharing).

**Figure 9:** Changes in the average loss of πgrower (policy shaping).

**Table 1:** State and action space of the greenhouse environment.

     | State space |  |  | Action space
    Name |  | Name |  | Dimension | Action
    Outdoor temperature °C | Temperature setpoint °C | Temperature setpoint -2 °C, 0, +2 °C
    Outdoor humidity | % | Ventilation rate | mm/s Ventilation rate | -0.5 mm/s, 0, +0.5 mm/s
    Outdoor CO2 | ppm CO2 setpoint | ppm | CO2 setpoint | -200 ppm, 0, +200 ppm
    Indoor temperature | °C | Hour of the day |  | 
    Indoor humidity | % | Radiation | W/m 2 | 
    Indoor CO2 | ppm Lettuce weight | kg/m 2 | 

**Table 2:** Constraints for indoor climate.

    Indoor climate variable Lower constraint Upper constraint
    Temperature (°C) | 6.5 | 40
    CO2 level (ppm) | 0 | 1500
    Relative humidity (%) | 0 | 90

**Table 3:** The three approaches of interactive RL.

**Table 5:** Three types of grower's simulated inputs.

    Characteristics Feedback | Precise action | Constraint advice
     |  | advice | 
    Input form | Binary (bad action: | Probabilities for | Probabilities for
     | -1, good action: 1) | action | action
    Cognitive bias | Maximize current | Maximize current | Maximize current
     | crop growth | crop growth | crop growth
    Knowledge level | High (consider the | High (consider the | Low (consider the
     | optimal values of | optimal values of | suitable range of
     | climate variables) | climate variables) | climate variables)

**Table 6:** Ranges of climate conditions for constraint advice.

    Indoor climate variable Daytime range Nighttime range
    CO2 setpoint (ppm) | 400 -1500 | 300 -600
    Temperature setpoint (°C) 10 -25 | 6 -10

**Table 7:** Hyperparameters for all RL agents.

    Hyperparameters | Values | Hyperparameters | Values
    Learning rate | 1×10 -4 | Actor and critic size | 512×4
    Step numbers per update | 2048 | Gamma (discount factor) | 0.97
    Batch size | 256 | Total training steps | 500,000

**Table 8:** Hyperparameters used in interactive RL agents.

    Hyperparameters | Values
    Sizes of π grower and π error networks 256×3
    Number of inputs n | 2048/1024/512/256/128
    Initial input weight (likelihood) β | 0.5/0.2/0.1/0.05
    Number of iterations N | 500
    Entropy coefficient | 1×10 -2 (no inputs, reward shaping, policy
     | shaping(constraint)) / 1×10 -3 (policy
     | shaping(precise), control sharing)
    Learning rate for π grower network | 1×10 -4 (policy shaping(precise)) / 1×10 -3
     | (reward shaping, control sharing)
    Learning rate for π error network | 1×10 -3

**Table 9:** Average cumulative reward on the test environment.

     | baseline PPO PPO with | Policy shaping | Policy shaping | Control sharing | Reward shaping
     |  | feedback only | (precise) β=0.2 | (constraint) β=0.1 | β=0.05 | β=0.2
    Cumulative | 1.91 | 0.71 | 2.07 | 1.97 | 2.04 | 1.73
    reward(Hfl/m 2 ) |  |  |  |  |  | 
    Relative change | 0 | -62.8% | +8.4% | +3.1% | +6.8% | -9.4%
    to baseline |  |  |  |  |  | 
    PPO |  |  |  |  |  | 

[figure sans légende identifiée] -p 1,2 x 1 (t)2 x3(t)/10-5/2 , -ϕ phot,c (t) + p 2,2 x 1 (t)2 x3(t)/10-5/2 + u 1 (t)10 -6 -ϕ vent,c (t) , (t)-(p 3,2 u 2 (t)10 -3 + p 3,3 )(x 3 (t) -d 3 (t)) + p 3,4 d 1 (t) , -exp(-p 1,3 x 1 (t)))[p 1,4 d 1 (t)(-p 1,5 x 3 (t) 2 + p 1,6 x 3 (t) -p 1,7 ) × (x 2 (t) -p 1,8 )]/φ(t), φ(t) = p 1,4 d 1 (t) + -p 1,5 x 3 (t) 2 + p 1,6 x 3 (t) -p 1,7 x 2 (t) -p 1,8 , ϕ vent,c (t) = u 2 (t)10 -3 + p 2,3 x 2 (t) -d 2 (t) , ϕ vent,h (t) = u 2 (t)10 -3 + p 2,3 x 4 (t) -d 4 (t) , ϕ transp,h (t) = p 4,2 (1 -exp(-p 1,3 x 1 (t))) CO2 (τ ) -y 2 (τ )) dτ, u 3 (t) = p 5,3 (u temp (t) -y 3 (t)) + p 5,4 t t-1 hour (u temp (τ ) -y 3 (τ )) dτ,where the meaning of variables is shown in Table10. Furthermore, ϕ phot,c (t), ϕ vent,c (t), ϕ transp,h (t) and ϕ vent,h (t) are the gross canopy photosynthesis rate, mass exchange of CO 2 through the vents, canopy transpiration and mass exchange of H 2 O through the vents, respectively. The measurement equation is defined asy 1 (t) = 10 3 • x 1 (t) g • m -2 ,y 2 (t) = 10 6 • p 2,4 (x 3 (t) + p 2,5 ) p 2,6 p 2,7 • x 2 (t), ppm, y 3 (t) = x 3 (t), °C, y 4 (t) = 10 2 • p 2,4 x 3 (t) + p 2,5

     |  |  |  |  | t
    u 1 (t) = p 5,1 (u CO2 (t) -y 2 (t)) + p 5,2 p4,8x3(t) (u 11 • exp t-1 hour x3(t)+p4,9
    dx 2 (t) dt | = | 1 p 2,1 |  | 
    dx 3 (t) dt u 3 dx 4 (t) = 1 p 3,1 dt 1 = p 4,1 |  | 
     |  | × | p 4,3 p 4,4 (x 3 (t) + p 4,5 ) | exp | p 4,6 x 3 (t) x 3 (t) + p 4,7 | -x 4 (t) ,

**Table 10:** Meaning of the lettuce greenhouse model parameters. CO 2 injection (mg/m 2 /s) y 1 (t) dry-weight (kg/m 2 ) u 2 (t) ventilation (mm/s) y 2 (t) indoor CO 2 (ppm) u 3 (t) heating (W/m 2 ) y 3 (t) indoor temperature ( • C) u CO 2 (t) CO 2 setpoint (ppm) y 4 (t) indoor humidity (%) u temp (t) temperature setpoint ( • C)

**Table 11:** Model parameter values[21].

    parameter | value | parameter | value | parameter value parameter value | parameter | value
    p1,1 | 0.544 | p2,1 | 4.1 | p3,1 | 3•10 4 | p4,1 | 4.1 | p5,1 | 0.05
    p1,2 | 2.65 •10 -7 | p2,2 | 4.87 •10 -7 | p3,2 | 1290 | p4,2 | 0.0036 | p5,2 | 3 •10 -6
    p1,3 | 53 | p2,3 | 7.5 •10 -6 | p3,3 | 6.1 | p4,3 | 9348 | p5,3 | 55
    p1,4 | 3.55 •10 -9 | p2,4 | 8.31 | p3,4 | 0.2 | p4,4 | 8314 | p5,4 | 2.5 •10 -2
    p1,5 | 5.11 •10 -6 | p2,5 | 273.15 |  |  | p4,5 | 273.15 |  | 
    p1,6 | 2.3 •10 -4 | p2,6 | 101325 |  |  | p4,6 | 17.4 |  | 
    p1,7 | 6.29 •10 -4 | p2,7 | 0.044 |  |  | p4,7 | 239 |  | 
    p1,8 | 5.2 •10 -5 |  |  |  |  | p4,8 | 17.269 |  | 
     |  |  |  |  |  | p4,9 | 238.3 |  |
