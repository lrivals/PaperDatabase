---
id: arxiv-1711.00614-multimodal-anomaly-detector-robot-assisted
title: "A Multimodal Anomaly Detector for Robot-Assisted Feeding Using an LSTM-based Variational Autoencoder"
year: 2017
backend: grobid
---

## Abstract

The detection of anomalous executions is valuable for reducing potential hazards in assistive manipulation. Multimodal sensory signals can be helpful for detecting a wide range of anomalies. However, the fusion of high-dimensional and heterogeneous modalities is a challenging problem. We introduce a long short-term memory based variational autoencoder (LSTM-VAE) that fuses signals and reconstructs their expected distribution. We also introduce an LSTM-VAE-based detector using a reconstruction-based anomaly score and a state-based threshold. For evaluations with 1,555 robot-assisted feeding executions including 12 representative types of anomalies, our detector had a higher area under the receiver operating characteristic curve (AUC) of 0.8710 than 5 other baseline detectors from the literature. We also show the multimodal fusion through the LSTM-VAE is effective by comparing our detector with 17 raw sensory signals versus 4 hand-engineered features.

## I. INTRODUCTION

People with disabilities often need physical assistance from caregivers. Robots can provide assistance for activities of daily living such as robot-assisted feeding [1] and shaving [2]. However, its structural complexity, task variability, and sensor uncertainty may result in failure. A lack of detection systems for the failures may also lower the usage of robots due to potential failure cost. The detection of an anomalous task execution (i.e., anomaly) can help to prevent or reduce potential hazards in the assistance by recognizing highly unusual situations and stop in these situations.

In this paper, an anomaly detector is a method to identify when the current execution differs from past successful experiences (i.e., non-anomalous executions). Researchers often use an one-class classifier trained on non-anomalous execution. An ideal detector should detect a variety of anomalies, alert the robot quickly, ignore irrelevant task variation, and handle the stream of sensory signals. Multimodal sensory signals can be helpful to detect various anomalies using its high dimensional information. Researchers often reduce the dimension or select features before applying a classifier. Our previous work used also selected 4 hand-engineered features from 3 modalities for a likelihood-based classifier, HMM-GP, using hidden Markov models (HMM) [3], [4]. However, the compressed or selected representations may be missing information relevant to anomaly detection. Creating useful hand-specified features can also involve significant engineering effort and domain expertise. An alternative solution is reconstruction-based detection, such as an autoencoder (AE) based approach that compresses and reconstructs high dimensional inputs based on nonanomalous executions. When an AE is trained only with non-anomalous data, a high reconstruction error can indicate an anomaly. The idea behind this detection is that an AE cannot reconstruct unforeseen patterns of anomalous data well compared to foreseen non-anomalous data. In addition to the reconstruction error, a variational autoencoder (VAE) can compute the reconstruction log-likelihood of the inputs modeling the underlying probability distribution of data. Both AE and VAE can be combined with time-series modeling approaches such as recurrent neural network (RNN) including long short-term memory (LSTM) network.

In this paper, we introduce a long short-term memory-based variational autoencoder (LSTM-VAE) for multimodal anomaly detection. For encoding, an LSTM-VAE projects multimodal observations and their temporal dependencies at each time step into a latent space using serially connected LSTM and VAE layers. For decoding, it estimates the expected distribution of the multimodal inputs from the latent space representation. We train it under a denoising autoencoding criterion [5] to prevent learning an identity function and improve representation capability. Our LSTM-VAE-based detector detects an anomaly when the log-likelihood of current observation given the expected distribution is lower than a threshold. We also introduce a state-based threshold to increase detection sensitivity and lower the false alarms similar to [3].

We evaluated the LSTM-VAE with robot-assisted feeding data that we collected from 24 able-bodied participants with 1,555 feeding executions. The proposed detector is beneficial in that we could directly use high-dimensional multimodal sensory signals without significant effort for feature engineering. It was able to catch an anomaly online. In particular, it was able to set tight or loose decision boundaries depending on the variations of multimodal signals using the state-based threshold. Our method had higher area under receiver operating characteristic (ROC) curves than other baseline methods from the literature. In our evaluation, the area under the curve (AUC) was 0.044 higher than that of our previous algorithm, HMM-GP given the same data. Our new method also had a 0.064 higher AUC when we used 17-dimensional sensory signals from visual, haptic, kinematic, and auditory modalities instead of 4-dimensional hand-engineered features.

## II. RELATED WORK

Anomaly detection is known as novelty, outlier, or event detections in other domains [6]. In robotics, it has been used to detect the failure of manipulation tasks: bin picking [7], bottle opening [8], etc. Many classic machine learning approaches have also been used: support vector machine (SVM) [9], [10], self-organizing map (SOM) [11], k-nearest neighbors (kNN) [12], etc. To detect anomalies from time-series signals, researchers have also used hidden Markov models [3] or Kalman filters [13].

Researchers have often reduced the dimension of highdimensional inputs using principal component analysis (PCA) before applying probabilistic or distance-based detection [9], [14]. However, the compressed representations of outliers (i.e., anomalous data) may be inliers in latent space. Instead, we use a reconstruction-based method that recovers inputs from its compressed representation so that it can measure reconstruction error with the anomaly score. An AE is a representative reconstruction approach that is a connected network with an encoder and a decoder [15]. It has also been applied for reconstructing time-series data using a sliding timewindow [16]. However, the window method does not represent dependencies between nearby windows and a window may not include an anomaly.

To model time-series data with its temporal dependencies, we use an LSTM network [17], which is a type of recurrent neural network (RNN). An LSTM network can make use of long-term dependencies and avoid the vanishing gradient problem [17]. Researchers have used LSTM networks for prediction in this anomaly detection domains such as the following: radio anomaly detection [18] and EEG signal anomaly detection [19]. Malhorta et al. introduced an LSTMbased anomaly detector (LSTM-AD) that measures the distribution of prediction errors [20]. However, the method may not predict time-series under unpredictable external changes such as manual control and load on a machine [21]. Alternatively, researchers have introduced RNN-and LSTM-based autoencoders for reconstruction-based anomaly detection [22], [23]. In particular, Malhorta et al. introduced an LSTM-based encoder-and-decoder (EncDec-AD) that estimates a reconstruction error [21]. We also use this reconstruction scheme for detection and as a baseline method in this paper.

Another relevant approach is a variational autoencoder (VAE) [24]. Unlike the AE, a VAE models the underlying probability distribution of observations using variational inference (VI). Bayer and Osendorfer used VI to learn the underlying distribution of sequences and introduced stochastic recurrent networks [25]. Soelch et al. used their work to detect robot anomalies using unimodal signals [26]. Our work also uses variational inference, but we do not predict and instead only reconstruct data using an LSTM-based autoencoder for multimodal anomaly detection.

## III. LSTM-BASED VARIATIONAL AUTOENCODING

We review an autoencoder and a variational autoencoder. We then describe our proposed LSTM-based variational autoencoder. We represent a vector of multidimensional inputs by x ∈ R D and the corresponding latent space vector by z ∈ R K , where D and K are the number of input signals and the dimension of the latent space, respectively.

### A. Preliminary: Autoencoder(AE)

An AE is an artificial neural network that consists of sequentially connected encoder and decoder networks. It sets the target of the decoder to be equal to the input of the encoder. The encoder network learns a compressed representation (i.e., bottleneck feature or latent variable) of the input. The decoder network reconstructs the target from the compressed representation. The difference between the input and the reconstructed input is the reconstruction error. During training, the autoencoder minimizes the reconstruction error as an objective function. An AE is often used for data generation as a generative model. An AE's decoder can generate an output given an artificially assigned compressed representation.

### B. Preliminary: Variational Autoencoder(VAE)

A VAE is a variant of an AE rooted in Bayesian inference [24]. A VAE is able to model the underlying distribution of observations p(z) and generate new data by introducing a set of latent random variables z. We can represent the process as p(x) = p(x|z)p(z)dz. However, the integral is intractable due to the continuous domain of z. Instead, we can represent the marginal log-likelihood of an individual point as log p(x) = D KL (q φ (z|x)||p θ (z)) + L vae (φ, θ; x) using notation from [24], where D KL is KullbackLeibler divergence from a prior p θ (z) to the variational approximation q φ (z|x) of p(z|x) and L vae is the variational lower bound of the data x by Jensen's inequality. Note that φ and θ are the parameters of the encoder and the decoder, respectively.

A VAE optimizes the parameters, φ and θ, by maximizing the lower bound of the log likelihood, L vae ,

L vae = -D KL (q φ (z|x)||p θ (z)) + E q φ (z|x) [log p θ (x|z)].(1)

The first term regularizes the latent variable z by minimizing the KL divergence between the approximated posterior and the prior of the latent variable. The second term is the reconstruction of x by maximizing the log-likelihood log p θ (x|z) with sampling from q φ (z|x). The choice of distribution types are important since a VAE models the approximated posterior distribution q φ (z|x) from a prior p θ (z) and likelihood p θ (x|z). A typical choice for the posterior is a Gaussian distribution, N (µ z , Σ z ), where a standard normal distribution N (0, 1) is used for the prior. For the likelihood, a Bernoulli distribution or multivariate Gaussian distribution is often used for binary or continuous data, respectively.

### C. An LSTM-based Variational Autoencoder (LSTM-VAE)

We introduce a long short-term memory-based variational autoencoder (LSTM-VAE). To use the temporal dependency of time-series data in a VAE, we combine a VAE with LSTMs by replacing the feed-forward network in a VAE to LSTMs similar to conventional temporal AEs such as an RNN Encoder-Decoder [22] or an EncDec-AD [21]. Fig. 2 shows an unrolled structure with LSTM-based encoder-anddecoder modules. Given a multimodal input x t at time t, the encoder approximates the posterior p(z t |x t ) by feeding an LSTM's output into two linear modules to estimate the mean µ zt and co-variance Σ zt of the latent variable. Then, the randomly sampled z from the posterior p(z t |x t ) feeds into the decoder's LSTM. The final outputs are the reconstruction mean µ xt and co-variance Σ xt .

We apply a denoising autoencoding criterion [5] to the LSTM-VAE by introducing corrupted input with Gaussian noise, x = x + , where ∼ N (0, σ noise ). We then replace the lower bound in Eq. ( 1) with a denoising variational lower bound L dvae [27],

L dvae = -D KL (q φ (z t |x t )||p θ (z t )) + E qφ (zt|xt) [log p θ (x t |z t )],(2)

where qφ (z t |x t ) is an approximated posterior distribution given a corruption distribution around x t . Given Gaussian distribution for p(x|x) and q φ (z|x), qφ (z t |x t ) can be represented as a mixture of Gaussians. For computational convenience, we use a single Gaussian, qφ (z|x) ≈ q φ (z|x).

We introduce a progress-based prior p(z t ). Unlike conventional static priors using a normal distribution N (0, 1), we vary the center of a normal distribution as N (µ p , Σ p ), where µ p and Σ p are the center and co-variance of the underlying distribution of multimodal inputs, respectively (see Fig. 3). This kind of varying prior can be helpful to introduce the temporal dependency of time-series data into its underlying distribution since a VAE tries to minimize the difference between the approximated posterior and the prior. Unlike the RNN prior of Solch et al. [26] and the transition prior of Karl et al. [28], we gradually change µ p from p 1 to p T as the progress of a task execution. To simplify the prior, we use an isotropic normal distribution so the co-variance matrix is Σ p = I. We can rewrite the regularization term of L dvae as

D KL (q φ (z t |x t )||p θ (z t )) ≈ D KL (N (µ zt , Σ zt )||N (µ p , 1)). = 1 2 tr(Σ zt ) + (µ p -µ zt ) T (µ p -µ zt ) -D -log |Σ zt | .(3)

To represent the distribution of high-dimensional contin-uous data, we use a multivariate Gaussian with a diagonal co-variance matrix. We can derive the reconstruction term in L dvae as

E qφ (zt|xt) [log p θ (x t |z t )] = - 1 2 (log(|Σ xt |) + (x t -µ xt ) T Σ -1 xt (x t -µ xt ) + D log(2π))(4)

We use an LSTM with tanh for each encoder and decoder. We implemented the LSTM-VAE using stateful LSTM models in the Keras deep learning library [29]. We trained the LSTM-VAE using an Adam optimizer with 3-dimensional latent variables and a 0.001 learning rate. Note that we are not using a sliding window in this work, but a window could be applied.

## IV. ANOMALY DETECTION

We now introduce an online anomaly detection framework for multimodal sensory signals with state-based thresholding.

### A. Anomaly Score

Our method detects an anomalous execution when the current anomaly score of an observation x t is higher than a score threshold η,

anomaly, if f s (x t , φ, θ) > η ¬anomaly, otherwise,(5)

where f s (x t , φ, θ) is an anomaly score estimator. We define the score as the negative log-likelihood of an observation with respect to the reconstructed distribution of the observation through an encoding-decoding model,

f s (x t , φ, θ) = -log p(x t ; µ xt , Σ xt ),(6)

where µ xt and Σ xt are the mean and co-variance of the reconstructed distribution, N (µ xt , Σ xt ), from an LSTM-VAE with parameters φ and θ. A high score indicates an input has not been reconstructed well by the the LSTM-VAE. In other words, the input has deviated greatly from the non-anomalous training data.

### B. State-based Thresholding

We introduce a varying threshold that changes over the estimated state of a task execution motivated by the dynamic threshold [3]. Depending on the state of task executions, reconstruction quality may vary. In other words, anomaly scores in non-anomalous task executions can be high in certain states, so varying the anomaly score can reduce false alarms and improve sensitivity. In this paper, the state is the latent space representation of observations. Given a sequence of observations, the encoder of LSTM-VAE is able to compute a state at each time step. By mapping states Z and corresponding anomaly scores S from non-anomalous dataset, our method is able to train an expected anomaly score estimator fs : z → s. We use support vector regression (SVR) to map from a multidimensional input z ∈ Z to a scaler s using a radial basis function (RBF) kernel. To control sensitivity, we add a constant c the expected score and represent the state-based threshold as η = fs (z) + c.

### C. Training and Testing Framework

Algorithm 1 shows the training framework of our LSTM-VAE-based anomaly detector. Given a set of non-anomalous training and validation data, (X train , X val ), the framework aims to output the optimized parameters (φ, θ) of an LSTM-VAE and an expected anomaly score estimator fs . Note that we represent N sequences of multimodal observations as X = {x (1) , x (2) , ..., x (N ) }. N train and N val denote the numbers of training and validation data, respectively. We also represent the encoder and decoder functions as f φ : x t → z t and g θ : z t → (µ xt , Σ xt ), respectively. Then, we denote the function of serially connected encoder and decoder (i.e., autoencoder) by f φ,θ with noise injection.

The framework preprocesses X train and X val by resampling those to have length T and normalizing their individual modalities in the range of [0, 1] with respect to X train . The framework then starts to train the LSTM-VAE with respect to X train maximizing L dvae and stops the training when L dvae does not increase for 4 epochs. Then it extracts a set of latent space representations and corresponding anomaly scores from X val as the training set for fs . Finally, this framework returns the trained SVR object as well as the LSTM-VAE's parameters. Note that we reset the state of the LSTM in the beginning of a sequence of data only.

In testing, the detector aims to detect an anomaly in real time. Algorithm 2 shows the pseudo code for the online detection process. In each loop, the detector takes multimodal input x. The detector scales individual dimension with respect to the scaled X train . It then estimates the latent variable and the parameters of the reconstructed distribution. When the anomaly score of the current input is higher than the threshold η, our system detects that the detector determines the current task execution is anomalous and returns the decision. We control the sensitivity of the detector by adding a constant c to fs .

### Algorithm 1: Training algorithm for an LSTM-VAEbased anomaly detector

input :

X train ∈ R Ntrain×T ×D , X val ∈ R N val ×T ×D output : φ, θ, f η 1 X train , X val = Preprocessing(X train , X val ) ; 2 φ, θ ← train LSTM-VAE with (X train , X val ); 3 Z = ∅, S = ∅ ; 4 for i ← 1 to N val do 5

Reset the state of LSTM-VAE;

6 for j ← 1 to T do 7 z ← f φ (X val (i, j)); 8 µ x , σ x ← f φ,θ (X val (i, j)); 9 s ← f s (x val (i, j), µ x , σ x );

fs ← train an SVR with (Z, S).

10 Add z and s into Z and S, respectively.

## V. EXPERIMENTAL SETUP

### A. Instrumental Setup

Our system uses a PR2 from Willow Garage, a generalpurpose mobile manipulator with two 7-DOF arms with powered grippers and an omni-directional mobile base. For safety and prevention of possible hazards, we used a lowlevel PID controller with low gains and a 50 Hz mid-level model predictive controller from [30] without haptic feedback. We used the following sensors: an RGB-D camera with a microphone (Intel SR300) on the right wrist, a force/torque sensor (ATI Nano25) on the utensil handle, joint encoders, and current sensors. These sensors measure mouth position and sound, force on the utensil, spoon position, and joint torque, respectively.

### B. Data Collection

We used data from 1,555 feeding executions collected from 24 able-bodied participants where we newly collected 1,203 non-anomalous feeding executions for this work. 16 participants were male and 8 were female, and the age range was 19-35. We conducted the studies with approval from the Georgia Tech Institutional Review Board (IRB).

We divided our data into two subsets: a training/testing dataset collected from our previous work [4], and a pretraining dataset. The training/testing dataset consists of data from 352 executions (160 anomalous and 192 non-anomalous) collected from 8 able-bodied participants who used the feeding system with yogurt and a silicone spoon.

The pre-training dataset uses data from 1,203 nonanomalous executions from 16 newly recruited participants who used various foods and utensils. Pre-training with this dataset allowed us to initialize the weights of the LSTM-VAE to find a better fit in fine tuning. Among the dataset, 559 non-anomalous executions were from 9 participants who used 3 types of food and corresponding utensils: cottage cheese and silicone spoon, watermelon chunks and metal fork, and fruit mix and plastic spoon. An experimenter also conducted 428 non-anomalous feeding executions as a self-study with 6 foods (yogurt, rice, fruit mix, watermelon chunks, cereal, and cottage cheese) and 5 utensils (small/large plastic spoons, a silicone spoon, and plastic/metal forks). We also collected additional data from 216 non-anomalous executions from 6 participants who used yogurt and a silicone spoon.

### C. Experimental Procedure

This feeding system allows the user to command three autonomous subtasks: scooping/stabbing, clean spoon, and feeding. The user sends these commands using a web-based graphical user interface. A typical feeding sequence consists of scooping or stabbing followed by feeding. In order to approximate one form of limited mobility that people with disabilities might have, we instructed the participants to not move their upper bodies and to eat food off of the utensil using their lips.

Each participant performed anomalous and non-anomalous feeding executions while the participant, experimenters, or the system produced anomalies. We randomly determined the order of these executions. We defined 12 types of representative anomalies through fault tree analysis [31]: touch by user, aggressive eating, utensil collision by user, sound from user, face occlusion, utensil miss by user, unreachable location, environmental collision, environmental noise, utensil miss by system fault, utensil collision by system fault, and system freeze (see Fig. 5). For anomalies caused by the user, we instructed the participants on their actions through demonstration videos and verbal explanation. The participant had control over the details of the anomaly, such as the exact timing and magnitude of their actions.

### D. Data collection and Pre-processing

For each feeding execution, we collected 17 sensory signals from 5 sensors: sound energy (1), force (3) applied on the end effector, joint torque (7), spoon position (3), and mouth position (3), where the number in parentheses represents the dimension of signals. We zeroed the initial value and resampled each signal to have 20 Hz for the robot's actual anomaly check frequency. We then scale signals in the non-anomalous dataset to have a value between 0 and 1.

Corresponding to this scale, we also scaled signals from the anomalous dataset. Finally, we have a sequence of tuples per execution (i.e., sequence length × 17). For visualization and comparison purposes, we also extracted 4-dimensional hand-engineered features used in our previous work [32]: sound energy, 1st joint torque, accumulated force, and spoonmouth distance. Here, we used sound energy 1 instead of raw 44 100 kHz 16 bit PCM encoding since the under sampling could miss auditory anomalies.

### E. Baseline Methods

To evaluate the performance of the proposed method, we implemented 5-baseline methods,

• RANDOM: A random binary classifier in which we control its sensitivity by weighting a class. • OSVM: A one-class SVM-based detector trained with only non-anomalous executions. We move a sliding window (of size 3 in time like EncDec-AD [21]) one step at a time. We control its sensitivity by adjusting the number of support vectors. • HMM-GP: A likelihood-based classifier using an HMM introduced in [32]. We vary the likelihood threshold with respect to the distribution of hidden states. • AE: A reconstruction-based anomaly detector using a conventional autoencoder with a 3 time step sliding window based on [33]. • EncDec-AD: A reconstruction-based anomaly detector using an LSTM-based autoencoder [21]. We use window size L = 3 as in the paper, but unlike the paper we use a diagonal co-variance matrix when we model the distribution of reconstruction-error vectors. From now on, we will also use the term LSTM-VAE to refer to our LSTM-VAE-based detector. 1 Root mean square (RMS) of 1,024 frames.

## VI. EVALUATION

We first investigated the reconstruction function of the LSTM-VAE. The upper 4 sub graphs in Fig. 6 show the reconstructed distribution of 4 hand-engineered features from non-anomalous and anomalous feeding executions in the robot-assisted feeding task. For Fig. 6a, the observed features (blue curves) and the mean of reconstructed distribution (red curves) show a similar pattern of change over time. On the other hand, in an anomalous execution (see Fig. 6b), the LSTM-VAE resulted in a large deviation between observed and reconstructed accumulated force since the pattern of accumulated force by the collision is not easily observable from non-anomalous executions. Consequently, we can observe the anomaly score (blue curve) gradually increases after the onset of the deviation from the lower sub graph of Fig. 6b. Note that the anomalous execution came from a face-spoon collision caused intentionally by the user.

The anomaly score metric is effective in distinguishing anomalies. Fig. 7 shows the distributions of the anomaly scores over time of a participant's 24 anomalous and 20 nonanomalous feeding executions during leave-one-person-out cross validation. The blue and red shaded regions show the mean and standard deviation of non-anomalous and anomalous executions' anomaly scores, respectively. The score of non-anomalous executions shows a specific pattern of change with a smaller average and variance than that of anomalous executions, making anomalies easily distinguishable from non-anomalous situations.

The lower sub graphs of Fig. 6 also show the state-based threshold is capable of achieving a tighter anomaly decision boundary (red dash lines) than a fixed threshold over time. The expected anomaly scores (red curves) and the actual scores (blue curves) show a similar pattern of change. However, the expected score is lower than the actual score given an anomaly. Brown boxes show the time of anomaly detection where the first detection time matches with the initial increase of accumulated force.

We compared our LSTM-VAE with 5 other baseline methods through a leave-one-person-out cross-validation method. Given the training/testing dataset, we used data I shows our detector outperformed the other 5 baseline methods with higher area under the ROC curve (AUC) when using 4 hand-engineered features. The AUC is 0.044 higher than the next best method, HMM-GP.

We also investigated the performance when using 17 sensory signals with the additional pre-training dataset. Our method resulted in the highest performance of AUC that is 0.064 higher than the next best method, EncDec-AD. It is also higher than the result from hand-engineered features. This indicates an LSTM-VAE is capable of modeling the heterogeneous high-dimensional multimodal signals and detecting anomalies among those signals without significant feature extraction effort. In this evaluation, we pre-trained each method using the pre-training dataset in addition to the dataset from the 7 participants. We then fine-tuned each method with the data from 7 participants. Note that we train an OSVM with the pre-traning dataset only and we did not succeed in training HMM-GP due to underflow errors resulting from the high-dimensional input.

Fig. 8 shows ROC curves from an LSTM-VAE with two thresholding techniques. The red curve shows the result of the proposed state-based thresholding. The yellow curve shows the result of conventional fixed thresholding. The state-based thresholding resulted in higher true positive rates given the same false positive rates. In this evaluation, we used 17 sensory signals with the pre-training dataset.

## VII. CONCLUSION

We introduced an LSTM-VAE-based anomaly detector for multimodal anomaly detection. An LSTM-VAE models the underlying distribution of multi-dimensional signals and reconstructed the signals with expected distribution information. The detector estimated the negative log-likelihood of multimodal input with respect to the distribution as anomaly score. By introducing a denoising autoencoding criterion and state-based thresholding, the detector successfully detected

## Figures et tableaux

**Fig. 1:** Robot-assisted feeding system. A PR2 robot detects anomalous feeding executions collecting 17 sensory signals from 5 types of sensors.

**Fig. 2:** Illustration of a multimodal anomaly detector with an unrolled LSTM-VAE model. We train the LSTM-VAE using multimodal signals and corresponding progress-based priors. We then train a threshold estimator using the outputs of the LSTM-VAE. For testing, we input sensory signals only. The detector then returns an anomaly when current anomaly score is over an estimated threshold η. Note that Linear* and LSTM layers have tanh and softplus activations, respectively. The red arrows are used for training only.

**Fig. 3:** Illustration of the progress-based prior. The center of the prior linearly changes from p 1 as initial progress to p T as final progress.

Algorithm 2: 2 x ← get current multimodal data; 3 x 4 z Testing algorithm for an LSTM-VAE-based anomaly detector. input : x ∈ R D output : Anomaly or ¬Anomaly 1 while True do ← P reprocessing(x); ← f φ (x); 5 µ x , Σ x ← f φ,θ (x); 6 if f s (x; µ x , Σ x ) > fs (z) + c

**Fig. 4:** Left: Examples of food used in our experiments. Right: The 3D-printed utensil handle and 5 utensils used. Red boxes show yogurt and silicone spoon used for our training/testing dataset.

**Fig. 5:** 12 representative anomalies caused by either the user, the environment, or the system in our experiments.

**Fig. 6:** Visualization of the reconstruction performance and anomaly scores over time using an LSTM-VAE. The upper four sub graphs show observations and reconstructed observations' distribution. The lower sub graphs show current and expected anomaly scores. The dashed curve shows a state-based threshold where the LSTM-VAE determines an anomaly when current anomaly score is over the threshold. Brown lines represent the time of anomaly detection.

**Fig. 7:** Fig.7: An example distributions of anomaly scores from a participant's 20 non-anomalous and 24 anomalous executions over time.

**Fig. 8:** Receiver operating characteristic (ROC) curves to compare the performance of LSTM-VAEs with and without a state-based threshold. from 7 participants for training and tested with the data from the remaining 1 participant. TableIshows our detector outperformed the other 5 baseline methods with higher area under the ROC curve (AUC) when using 4 hand-engineered features. The AUC is 0.044 higher than the next best method, HMM-GP.We also investigated the performance when using 17 sensory signals with the additional pre-training dataset. Our method resulted in the highest performance of AUC that is 0.064 higher than the next best method, EncDec-AD. It is also higher than the result from hand-engineered features. This indicates an LSTM-VAE is capable of modeling the heterogeneous high-dimensional multimodal signals and detecting anomalies among those signals without significant feature extraction effort. In this evaluation, we pre-trained each method using the pre-training dataset in addition to the dataset from the 7 participants. We then fine-tuned each method with the data from 7 participants. Note that we train an OSVM with the pre-traning dataset only and we did not succeed in training HMM-GP due to underflow errors resulting from the high-dimensional input.Fig.8shows ROC curves from an LSTM-VAE with two thresholding techniques. The red curve shows the result of the proposed state-based thresholding. The yellow curve shows the result of conventional fixed thresholding. The state-based thresholding resulted in higher true positive rates given the same false positive rates. In this evaluation, we used 17 sensory signals with the pre-training dataset.

**TABLE I:** Comparison of the LSTM-VAE and 5 baseline methods with two types of inputs. Numbers represent the area under the ROC curve (AUC). anomalies in robot-assisted feeding resulting in higher AUC than other 5 baseline methods in literature. Without significant effort of feature engineering, the detector with 17 raw inputs outperformed a detector trained with 4 hand-engineered features. Finally, we also showed the LSTM-VAE with the state-based decision boundary is beneficial for more sensitive anomaly detection with lower false alarms.

    Input | Random | OSVM | HMM-GP | AE | EncDec-AD | LSTM-VAE
    4 hand-engineered features | 0.5121 | 0.7427 | 0.8121 | 0.8123 | 0.7995 | 0.8564
    17 raw sensory signals | 0.5052 | 0.7376 | N/A | 0.8012 | 0.8075 | 0.8710
