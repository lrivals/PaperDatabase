---
id: arxiv-1906.02530-can-you-trust-your-model
title: "Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift"
year: 2019
backend: grobid
---

## Abstract

Modern machine learning methods including deep learning have achieved great success in predictive accuracy for supervised learning tasks, but may still fall short in giving useful estimates of their predictive uncertainty. Quantifying uncertainty is especially critical in real-world settings, which often involve input distributions that are shifted from the training distribution due to a variety of factors including sample bias and non-stationarity. In such settings, well calibrated uncertainty estimates convey information about when a model's output should (or should not) be trusted. Many probabilistic deep learning methods, including Bayesian-and non-Bayesian methods, have been proposed in the literature for quantifying predictive uncertainty, but to our knowledge there has not previously been a rigorous largescale empirical comparison of these methods under dataset shift. We present a largescale benchmark of existing state-of-the-art methods on classification problems and investigate the effect of dataset shift on accuracy and calibration. We find that traditional post-hoc calibration does indeed fall short, as do several other previous methods. However, some methods that marginalize over models give surprisingly strong results across a broad spectrum of tasks.

## 1. Introduction

Recent successes across a variety of domains have led to the widespread deployment of deep neural networks (DNNs) in practice. Consequently, the predictive distributions of these models are increasingly being used to make decisions in important applications ranging from machine-learning aided medical diagnoses from imaging (Esteva et al., 2017) to self-driving cars (Bojarski et al., 2016). Such high-stakes applications require not only point predictions but also accurate quantification of predictive uncertainty, i.e. meaningful confidence values in addition to class predictions. With sufficient independent labeled samples from a target data distribution, one can estimate how well a model's confidence aligns with its accuracy and adjust the predictions accordingly. However, in practice, once a model is deployed the distribution over observed data may shift and eventually be very different from the original training data distribution. Consider, e.g., online services for which the data distribution may change with the time of day, seasonality or popular trends. Indeed, robustness under conditions of distributional shift and out-of-distribution (OOD) inputs is necessary for the safe deployment of machine learning (Amodei et al., 2016). For such settings, calibrated predictive uncertainty is important because it enables accurate assessment of risk, allows practitioners to know how accuracy may degrade, and allows a system to abstain from decisions due to low confidence.

A variety of methods have been developed for quantifying predictive uncertainty in DNNs. Probabilistic neural networks such as mixture density networks (MacKay & Gibbs, 1999) capture the inherent ambiguity in outputs for a given input, also referred to as aleatoric uncertainty (Kendall & Gal, 2017). Bayesian neural networks learn a posterior distribution over parameters that quantifies parameter uncertainty, a type of epistemic uncertainty that can be reduced through the collection of additional data. Popular approximate Bayesian approaches include Laplace approximation (MacKay, 1992), variational inference (Graves, 2011;Blundell et al., 2015), dropout-based variational inference (Gal & Ghahramani, 2016;Kingma et al., 2015), expectation propagation Hernández-Lobato & Adams (2015) and stochastic gradient MCMC (Welling & Teh, 2011). Non-Bayesian methods include training multiple probabilistic neural networks with bootstrap or ensembling (Osband et al., 2016;Lakshminarayanan et al., 2017). Another popular non-Bayesian approach involves re-calibration of probabilities on a held-out validation set through temperature scaling (Platt, 1999), which was shown by Guo et al. (2017) to lead to well-calibrated predictions on the i.i.d. test set.

Using Distributional Shift to Evaluate Predictive Uncertainty While previous work has evaluated the quality of predictive uncertainty on OOD inputs (Lakshminarayanan et al., 2017), there has not to our knowledge been a comprehensive evaluation of uncertainty estimates from different methods under dataset shift. Indeed, we suggest that effective evaluation of predictive uncertainty is most meaningful under conditions of distributional shift. One reason for this is that post-hoc calibration gives good results in independent and identically distributed (i.i.d.) regimes, but can fail under even a mild shift in the input data. And in real world applications, as described above, distributional shift is widely prevalent. Understanding questions of risk, uncertainty, and trust in a model's output becomes increasingly critical as shift from the original training data grows larger.

### Contributions

In the spirit of calls for more rigorous understanding of existing methods (Lipton & Steinhardt, 2018;Sculley et al., 2018;Rahimi & Recht, 2017), this paper provides a benchmark for evaluating uncertainty that focuses not only on the i.i.d. setting but also uncertainty under distributional shift. We present a large-scale evaluation of popular approaches in probabilistic deep learning, focusing on methods that operate well in large-scale settings, and evaluate them on a diverse range of classification benchmarks across image, text, and categorical modalities. We use these experiments to evaluate the following questions:

• How trustworthy are the uncertainty estimates of different methods under dataset shift?

• Does calibration in the i.i.d. setting translate to calibration under dataset shift?

• How do uncertainty and accuracy of different methods co-vary under dataset shift? Are there methods that consistently do well in this regime?

In addition to answering the questions above, our code is made available open-source along with our model predictions such that researchers can easily evaluate their approaches on these benchmarksfoot_0 .

## 2. Background

Notation and Problem Setup Let x ∈ R d represent a set of d-dimensional features and y ∈ {1, . . . , k} denote corresponding labels (targets) for k-class classification. We assume that a training dataset D consists of N i.i.d.samples D = {(x n , y n )} N n=1 . Let p * (x, y) denote the true distribution (unknown, observed only through the samples D), also referred to as the data generating process. We focus on classification problems, in which the true distribution is assumed to be a discrete distribution over k classes, and the observed y ∈ {1, . . . , k} is a sample from the conditional distribution p * (y|x). We use a neural network to model p θ (y|x) and estimate the parameters θ using the training dataset. At test time, we evaluate the model predictions against a test set, sampled from the same distribution as the training dataset. However, here we also evaluate the model against OOD inputs sampled from q(x, y) = p * (x, y). In particular, we consider two kinds of shifts:

• shifted versions of the test inputs where the ground truth label belongs to one of the k classes. We use shifts such as corruptions and perturbations proposed by Hendrycks & Dietterich (2019), and ideally would like the model predictions to become more uncertain with increased shift, assuming shift degrades accuracy. This is also referred to as covariate shift (Sugiyama et al., 2009).

• a completely different OOD dataset, where the ground truth label is not one of the k classes. Here we check if the model exhibits higher predictive uncertainty for those new instances and to this end report diagnostics that rely only on predictions and not ground truth labels.

High-level overview of existing methods A large variety of methods have been developed to either provide higher quality uncertainty estimates or perform OOD detection to inform model confidence. These can roughly be divided into:

1. Methods which deal with p(y|x) only, we discuss these in more detail in Section 3.

2. Methods which model the joint distribution p(y, x), e.g. deep hybrid models (Kingma et al., 2014;Alemi et al., 2018;Nalisnick et al., 2019;Behrmann et al., 2018).

3. Methods with an OOD-detection component in addition to p(y|x) (Bishop, 1994;Lee et al., 2018;Liang et al., 2018), and related work on selective classification (Geifman & El-Yaniv, 2017).

We refer to Shafaei et al. (2018) for a recent summary of these methods. Due to the differences in modeling assumptions, a fair comparison between these different classes of methods is challenging; for instance, some OOD detection methods rely on knowledge of a known OOD set, or train using a none-of-the-above class, and it may not always be meaningful to compare predictions from these methods with those obtained from a Bayesian DNN. We focus on methods described by (1) above, as this allows us to focus on methods which make the same modeling assumptions about data and differ only in how they quantify predictive uncertainty.

## 3. Methods and Metrics

We select a subset of methods from the probabilistic deep learning literature for their prevalence, scalability and practical applicabilityfoot_1 . These include (see also references within):

• (Vanilla) Maximum softmax probability (Hendrycks & Gimpel, 2017) • (Temp Scaling) Post-hoc calibration by temperature scaling using a validation set (Guo et al., 2017) • (Dropout) Monte-Carlo Dropout (Gal & Ghahramani, 2016;Srivastava et al., 2015) with rate p

• (Ensembles) Ensembles of M networks trained independently on the entire dataset using random initialization (Lakshminarayanan et al., 2017) (we set M = 10 in experiments below)

• (SVI) Stochastic Variational Bayesian Inference for deep learning (Blundell et al., 2015;Graves, 2011;Louizos & Welling, 2017, 2016;Wen et al., 2018). We refer to Appendix A.6 for details of our SVI implementation.

• (LL) Approx. Bayesian inference for the parameters of the last layer only (Riquelme et al., 2018) -(LL SVI) Mean field stochastic variational inference on the last layer only -(LL Dropout) Dropout only on the activations before the last layer

In addition to metrics (we use arrows to indicate which direction is better) that do not depend on predictive uncertainty, such as classification accuracy ↑, the following metrics are commonly used:

Negative Log-Likelihood (NLL) ↓ Commonly used to evaluate the quality of model uncertainty on some held out set. Drawbacks: Although a proper scoring rule (Gneiting & Raftery, 2007), it can over-emphasize tail probabilities (Quinonero-Candela et al., 2006).

Brier Score ↓ (Brier, 1950) Proper scoring rule for measuring the accuracy of predicted probabilities.

It is computed as the squared error of a predicted probability vector, p(y|x n , θ), and the one-hot encoded true response, y n . That is,

BS = |Y| -1 y∈Y (p(y|x n , θ) -δ(y -y n )) 2 = |Y| -1 1 -2p(y n |x n , θ) + y∈Y p(y|x n , θ) 2 . (1)

The Brier score has a convenient interpretation as BS = uncertainty -resolution + reliability, where uncertainty is the marginal uncertainty over labels, resolution measures the deviation of individual predictions against the marginal, and reliability measures calibration as the average violation of long-term true label frequencies. We refer to DeGroot & Fienberg (1983) for the decomposition of Brier score into calibration and refinement for classification and to (Bröcker, 2009) for the general decomposition for any proper scoring rule. Drawbacks: Brier score is insensitive to predicted probabilities associated with in/frequent events.

Both the Brier score and the negative log-likelihood are proper scoring rules and therefore the optimum score corresponds to a perfect prediction. In addition to these two metrics, we also evaluate two metrics-expected calibration error and entropy. Neither of these is a proper scoring rule, and thus there exist trivial solutions which yield optimal scores; for example, returning the marginal probability p(y) for every instance will yield perfectly calibrated but uninformative predictions. Each proper scoring rule induces a calibration measure (Bröcker, 2009). However, ECE is not the result of such decomposition and has no corresponding proper scoring rule; we instead include ECE because it is popularly used and intuitive. Each proper scoring rule is also associated with a corresponding entropy function and Shannon entropy is that for log probability (Gneiting & Raftery, 2007).

Expected Calibration Error (ECE) ↓ Measures the correspondence between predicted probabilities and empirical accuracy (Naeini et al., 2015). It is computed as the average gap between within bucket accuracy and within bucket predicted probability for S buckets B s = {n ∈ 1 . . There is no ground truth label for fully OOD inputs. Thus we report histograms of confidence and predictive entropy on known and OOD inputs and accuracy versus confidence plots (Lakshminarayanan et al., 2017): Given the prediction p(y = k|x n , θ), we define the predicted label as ŷn = arg max y p(y|x n , θ), and the confidence as p(y = ŷ|x, θ) = max k p(y = k|x n , θ). We filter out test examples corresponding to a particular confidence threshold τ ∈ [0, 1] and compute the accuracy on this set.

## 4. Experiments and Results

We evaluate the behavior of the predictive uncertainty of deep learning models on a variety of datasets across three different modalities: images, text and categorical (online ad) data. For each we follow standard training, validation and testing protocols, but we additionally evaluate results on increasingly shifted data and an OOD dataset. We detail the models and implementations used in Appendix A. Hyperparameters were tuned for all methods using Bayesian optimization (Golovin et al., 2017) (except on ImageNet) as detailed in Appendix A.8.

### 4.1. An illustrative example -MNIST

We first illustrate the problem setup and experiments using the MNIST dataset. We used the LeNet (LeCun et al., 1998) architecture, and, as with all our experiments, we follow standard training, validation, testing and hyperparameter tuning protocols. However, we also compute predictions on increasingly shifted data (in this case increasingly rotated or horizontally translated images) and study show accuracy and Brier score as the data is increasingly shifted. Shaded regions represent standard error over 10 runs. To understand the discrepancy between accuracy and Brier score, we explore the predictive distributions of each method by looking at the confidence of the predictions in 1(c) and 1(d). We also explore the entropy and confidence of each method on entirely OOD data in 1(e) and 1(f). SVI has lower accuracy on the validation and test splits, but it is significantly more robust to dataset shift as evidenced by a lower Brier score, lower overall confidence 1(d) and higher predictive entropy under shift (1(c)) and OOD data (1(e),1(f)).

3 0 ± 4 5 ± 6 0 ± 7 5 ± 9 0 ± 1 0 5 ± 1 2 0 ± 1 3 5 ± 1 5 0 ± 1 6 5 ± 1 8 0 ± Intensity of Shift

the behavior of the predictive distributions of the models. In addition, we predict on a completely OOD dataset, Not-MNIST (Bulatov, 2011), and observe the entropy of the model's predictions. We summarize some of our findings in Figure 1 and discuss below.

What we would like to see: Naturally, we expect the accuracy of a model to degrade as it predicts on increasingly shifted data, and ideally this reduction in accuracy would coincide with increased forecaster entropy. A model that was well-calibrated on the training and validation distributions would ideally remain so on shifted data. If calibration (ECE or Brier reliability) remained as consistent as possible, practitioners and downstream tasks could take into account that a model is becoming increasingly uncertain. On the completely OOD data, one would expect the predictive distributions to be of high entropy. Essentially, we would like the predictions to indicate that a model "knows what it does not know" due to the inputs straying away from the training data distribution.

What we observe: We see in Figures 1(a) and 1(b) that accuracy certainly degrades as a function of shift for all methods tested, and they are difficult to disambiguate on that metric. However, the Brier score paints a clearer picture and we see a significant difference between methods, i.e. prediction quality degrades more significantly for some methods than others. An important observation is that while calibrating on the validation set leads to well-calibrated predictions on the test set, it does not guarantee calibration on shifted data. In fact, nearly all other methods (except vanilla) perform better than the state-of-the-art post-hoc calibration (Temperature scaling) in terms of Brier score under shift. While SVI achieves the worst accuracy on the test set, it actually outperforms all other methods by a much larger margin when exposed to significant shift. In Figures 1(c) and 1(d) we look at the distribution of confidences for each method to understand the discrepancy between metrics. We see in Figure 1(d) that SVI has the lowest confidence in general but in Figure 1(c) we observe that SVI gives the highest accuracy at high confidence (or conversely is much less frequently confidently wrong), which can be important for high-stakes applications. Most methods demonstrate very low entropy (Figure 1(e)) and give high confidence predictions (Figure 1(f)) on data that is entirely OOD, i.e. they are confidently wrong about completely OOD data.

### 4.2. Image Models: CIFAR-10 and ImageNet

We now study the predictive distributions of residual networks (He et al., 2016) trained on two benchmark image datasets, CIFAR-10 ( Krizhevsky, 2009) and ImageNet (Deng et al., 2009), under distributional shift. We use 20-layer and 50-layer ResNets for CIFAR-10 and ImageNet respectively.

For shifted data we use 80 different distortions (16 different types with 5 levels of intensity each, see Appendix B for illustrations) introduced by Hendrycks & Dietterich (2019). To evaluate predictions of CIFAR-10 models on entirely OOD data, we use the SVHN dataset (Netzer et al., 2011).

Figure 2 summarizes the accuracy and ECE for CIFAR-10 (top) and ImageNet (bottom) across all 80 combinations of corruptions and intensities from (Hendrycks & Dietterich, 2019). Figure 3 highest accuracy under distributional shift. Comparing the ECE for different methods, we observe that while the methods achieve comparable low values of ECE for small values of shift, ensembles outperform the other methods for larger values of shift. To test whether this result is due simply to the larger aggregate capacity of the ensemble, we trained models with double the number of filters for the Vanilla and Dropout methods. The higher-capacity models showed no better accuracy or calibration for medium-to high-shift than the corresponding lower-capacity models (see Appendix C).

In Figures S8 andS9 we also explore the effect of the number of samples used in dropout, SVI and last layer methods and size of the ensemble, on CIFAR-10. We found that while increasing ensemble size up to 50 did help, most of the gains of ensembling could be achieved with only 5 models. Interestingly, while temperature scaling achieves low ECE for low values of shift, the ECE increases significantly as the shift increases, which indicates that calibration on the i.i.d. validation dataset does not guarantee calibration under distributional shift. (Note that for ImageNet, we found similar trends considering just the top-5 predicted classes, See Figure S5.) Furthermore, the results show that while temperature scaling helps significantly over the vanilla method, ensembles and dropout tend to be better. In Figure 3, we see that ensembles and dropout are more accurate at higher confidence. However, in 3(c) we see that temperature scaling gives the highest entropy on OOD data. Ensembles consistently have high accuracy but also high entropy on OOD data. We refer to Appendix C for additional results; Figures S4 andS5 report additional metrics on CIFAR-10 and ImageNet, such as Brier score (and its component terms), as well as top-5 error for increasing values of shift.

Overall, ensembles consistently perform best across metrics and dropout consistently performed better than temperature scaling and last layer methods. While the relative ordering of methods is consistent on both CIFAR-10 and ImageNet (ensembles perform best), the ordering is quite different from that on MNIST where SVI performs best. Interestingly, LL-SVI and LL-Dropout perform worse than the vanilla method on shifted datasets as well as SVHN. We also evaluate a variational Gaussian process as a last layer method in Appendix E but it did not outperform LL-SVI and LL-Dropout.

### 4.3. Text Models

Following Hendrycks & Gimpel (2017), we train an LSTM (Hochreiter & Schmidhuber, 1997) on the 20newsgroups dataset (Lang, 1995) and assess the model's robustness under distributional shift and OOD text. We use the even-numbered classes (10 classes out of 20) as in-distribution and the 10 odd-numbered classes as shifted data. We provide additional details in Appendix A.4.

We look at confidence vs accuracy when the test data consists of a mix of in-distribution and either shifted or completely OOD data, in this case the One Billion Word Benchmark (LM1B) (Chelba et al., 2013). Figure 4 (bottom row) shows the results. Ensembles significantly outperform all other methods, and achieve better trade-off between accuracy versus confidence. Surprisingly, LL-Dropout and LL-SVI perform worse than the vanilla method, giving higher confidence incorrect predictions, especially when tested on fully OOD data.

Figure 4 reports histograms of predictive entropy on in-distribution data and compares them to those for the shifted and OOD datasets. This reflects how amenable each method is to abstaining from prediction by applying a threshold on the entropy. As expected, most methods achieve the highest predictive entropy on the completely OOD dataset, followed by the shifted dataset and then the in-distribution test dataset. Only ensembles have consistently higher entropy on the shifted data, which explains why they perform best on the confidence vs accuracy curves in the second row of Figure 4. Compared with the vanilla model, Dropout and LL-SVI have more a distinct separation between in-distribution and shifted or OOD data. While Dropout and LL-Dropout perform similarly on in-distribution, LL-Dropout exhibits less uncertainty than Dropout on shifted and OOD data. Temperature scaling does not appear to increase uncertainty significantly on the shifted data.

### 4.4. Ad-Click Model with Categorical Features

Finally, we evaluate the performance of different methods on the Criteo Display Advertising Challengefoot_2 dataset, a binary classification task consisting of 37M examples with 13 numerical and 26 categorical features per example. We introduce shift by reassigning each categorical feature to a random new token with some fixed probability that controls the intensity of shift. This coarsely simulates a type of shift observed in non-stationary categorical features as category tokens appear and disappear over time, for example due to hash collisions. The model consists of a 3-hidden-layer multi-layer-perceptron (MLP) with hashed and embedded categorical features and achieves a negative log-likelihood of approximately 0.5 (contest winners achieved 0.44). Due to class imbalance (∼ 25% of examples are positive), we report AUC instead of classification accuracy.

Results from these experiments are depicted in Figure 5. (Figure S7

## 5. Takeaways and Recommendations

We presented a large-scale evaluation of different methods for quantifying predictive uncertainty under dataset shift, across different data modalities and architectures. Our take-home messages are the following:

• Along with accuracy, the quality of uncertainty consistently degrades with increasing dataset shift regardless of method.

• Better calibration and accuracy on the i.i.d. test dataset does not usually translate to better calibration under dataset shift (shifted versions as well as completely different OOD data).

• Post-hoc calibration (on i.i.d validation) with temperature scaling leads to well-calibrated uncertainty on the i.i.d. test set and small values of shift, but is significantly outperformed by methods that take epistemic uncertainty into account as the shift increases.

• Last layer Dropout exhibits less uncertainty on shifted and OOD datasets than Dropout.

• SVI is very promising on MNIST/CIFAR but it is difficult to get to work on larger datasets such as ImageNet and other architectures such as LSTMs.

• The relative ordering of methods is mostly consistent (except for MNIST) across our experiments.

The relative ordering of methods on MNIST is not reflective of their ordering on other datasets.

• Deep ensembles seem to perform the best across most metrics and be more robust to dataset shift. We found that relatively small ensemble size (e.g. M = 5) may be sufficient (Appendix D).

• We also compared the set of methods on a real-world challenging genomics problem from Ren et al. (2019). Our observations were consistent with the other experiments in the paper. Deep ensembles performed best, but there remains significant room for improvement, as with the other experiments in the paper. See Section F for details.

We hope that this benchmark is useful to the community and inspires more research on uncertainty under dataset shift, which seems challenging for existing methods. While we focused only on the quality of predictive uncertainty, applications may also need to consider computational and memory costs of the methods; Table S1 in Appendix A.9 discusses these costs, and the best performing methods tend to be more expensive. Reducing the computational and memory costs, while retaining the same performance under dataset shift, would also be a key research challenge. We evaluated both LeNet and a fully-connected neural network (MLP) under shift on MNIST. We observed similar trends across metrics for both models, so we report results only for LeNet in Section 4.1. LeNet and MLP were trained for 20 epochs using the Adam optimizer (Kingma & Ba, 2014) and used ReLU activation functions. For stochastic methods, we averaged 300 sample predictions to yield a predictive distribution, and the ensemble model used 10 instances trained from independent random initializations. The MLP architecture consists of two hidden layers of 200 units each with dropout applied before every dense layer. The LeNet architecture (LeCun et al., 1998) applies two convolutional layers 3x3 kernels of 32 and 64 filters respectively) followed by two fully-connected layers with one hidden layer of 128 activations; dropout was applied before each fully-connected layer. We employed hyperparameter tuning (See Section A.8) to select the training batch size, learning rate, and dropout rate.

### A.2 CIFAR-10

Our CIFAR model used the ResNet-20 V1 architecture with ReLU activations. Model parameters were trained for 200 epochs using the Adam optimizer and employed a learning rate schedule that multiplied an initial learning rate by 0.1, 0.01, 0.001, and 0.0005 at steps 80, 120, 160, and 180 respectively. Training inputs were randomly distorted using horizontal flips and random crops preceded by 4-pixel padding as described in (He et al., 2016). For relevant methods, dropout was applied before each convolutional and dense layer (excluding the raw inputs), and stochastic methods sampled 128 predictions per sample. Hyperparameter tuning was used to select the initial learning rate, training batch size, and the dropout rate.

### A.3 ImageNet 2012

Our ImageNet model used the ResNet-50 V1 architecture with ReLU activations and was trained for 90 epochs using SGD with Nesterov momentum. The learning rate schedule linearly ramps up to a base rate in 5 epochs and scales down by a factor of 10 at each of epochs 30, 60, and 80. As with the CIFAR-10 model, stochastic methods used a sample-size of 128. Training images were distorted with random horizontal flips and random crops.

### A.4 20 Newsgroups

We use a pre-processing strategy similar to the one proposed by Hendrycks & Gimpel (2017) for 20 Newsgroups. We build a vocabulary of size 30,000 words and words are indexed based on the word frequencies. The rare words are encoded as unknown words. We fix the length of each text input by setting a limit of 250 words, and those longer than 250 words are truncated, and those shorter than 250 words are padded with zeros. Text in even-numbered classes are used as in-distribution inputs, and text from the odd-numbered of classes are used shifted OOD inputs. A dataset with the same number of randomly selected text inputs from the LM1B dataset (Chelba et al., 2013) is used as completely different OOD dataset. The classifier is trained and evaluated only using the text from the even-numbered in-distribution classes in the training dataset. The final test results are evaluated based on in-distribution test dataset, shift OOD test dataset, and LM1B dataset.

The vanilla model uses a one-layer LSTM model of size 32 and a dense layer to predict the 10 class probabilities based on word embedding of size 128. A dropout rate of 0.1 is applied to both the LSTM layer and the dense layer for the Dropout model. The LL-SVI model replaces the last dense layer with a Bayesian layer, the ensemble model aggregates 10 vanilla models, and stochastic methods sample 5 predictions per example. The vanilla model accuracy for in-distribution test data is 0.955.

### A.5 Criteo

Each categorical feature x k from the Criteo dataset was encoded by hashing the string token into a fixed number of buckets N k and either encoding the hash-bin as a one-hot vector if N k < 110 or embedding each bucket as a d k dimensional vector otherwise. This dense feature vector, concatenated with 13 numerical features, feeds into a batch-norm layer followed by a 3-hidden-layer MLP. Each model was trained for one epoch using the Adam optimizer with a non-decaying learning rate.

Values of N k and d k were tuned to maximize log-likelihood for a vanilla model, and the resulting architectural parameters were applied to all methods. This tuning yielded hidden-layers of size 2572, 1454, and 1596, and hash-bucket counts and embedding dimensions of sizes listed below: 1373,2148,4847,9781,396,28,3591,2798,14,7403,2511,5598,9501,46,4753,4056,23,3828,5856,12,4226,23,61,3098,494,5087] [3,9,29,11,17,0,14,4,0,12,19,24,29,0,13,25,0,8,29,0,22,0,0,31,0,29] Learning rate, batch size, and dropout rate were further tuned for each method. Stochastic methods used 128 prediction samples per example.

N k = [

d k =

### A.6 Stochastic Variational Inference Details

For MNIST we used Flipout (Wen et al., 2018), where we replaced each dense layer and convolutional layer with mean-field variational dense and convolutional Flipout layers respectively. Variational inference for deep ResNets (He et al., 2016) is non-trivial, so for CIFAR we replaced a single linear layer per residual branch with a Flipout layer, removed batch normalization, added Selu non-linearities (Klambauer et al., 2017), empirical Bayes for the prior standard deviations as in Wu et al. (2019) and careful tuning of the initialization via Bayesian optimization.

### A.7 Variational Gaussian Process Details

For the experiments where Gaussian Processes were compared, we used Variational Gaussian Processes to fit the model logits as in Hensman et al. (2015). These were then passed through a Categorical distribution and numerically integrated over using Gauss-Hermite quadrature. Each class was treated as a separate Gaussian Process, with 100 inducing points used for each class. The inducing points were initialized with model outputs on random dataset examples for CIFAR, and with Gaussian noise for MNIST. Uniform noise inducing point initialization was also tested but there was negligible difference between the three methods. All zero inducing points initializations numerically failed early on in training. Exponentiated quadratic plus linear kernels were used for all experiments. 250 samples were drawn from the logit distribution during training time to get a better estimate of the ELBO to backpropagate through. 250 logit samples were drawn at test time. 10 -5 * I was added to the diagonal of the covariance matrix to ensure positive definiteness.

We used 100 trials of random hyperparamter settings, selecting the configuration with the best final validation accuracy. The learning rate was tuned in [10 -4 , 1.0] on a log scale; the initial kernel amplitude in [-2.0, 2.0]; the initial kernel length scale in [-2.0, 2.0]; the variational distribution covariance was initialized to s * I where s was tuned in [0.1, 2.0]; 1 -β 1 in Adam was tuned on [10 -2 , 0.15] on a log scale.

The Adam optimizer with a batch size of 512 was used, training for the same number of epochs as other methods. The same learning rate schedule was as other methods for the model and kernel parameters, but the learning rate for the variational parameters also included a 5 epoch warmup in order to help with numerical stability.

### A.8 Hyperparameter Tuning

Hyperparameters were optimized through Bayesian optimization using Google Vizier (Golovin et al., 2017). We maximized the log-likelihood on a validation set that was held out from training (10K examples for MNIST and CIFAR-10, 125K examples for ImageNet). We optimized log-likelihood rather than accuracy since the former is a proper scoring rule.

### A.9 Computational and Memory Complexity of Different methods

In addition to performance, applications may also need to consider computational and memory costs; Table S1 discusses them for each method.

Table S1: Computational and memory costs for evaluated methods. Notation: m represents flops or storage for the full model, d represents flops or storage for the last layer, k denotes replications, z the number of inducing points for Gaussian Processes, n denotes number of evaluated points, and v denotes the validation set size. Serving/training compute is identical except that v = 0 for serving. Implicit in this table is a memory/compute tradeoff for sampling. Sampled weights/masks need not be stored explicitly via PRNG seed reuse; we assume the computational cost of sampling is zero.

Method Compute/n Storage Vanilla m m Temp Scaling m + vm/n m LL-Dropout m + d(k -1) m LL-SVI m + d(k -1) m + d SVI mk 2m Dropout mk m Gaussian Process m + z 3 m + z 2 Ensemble mk mk

### B Shifted Images

We distorted MNIST images using rotations with spline filter interpolation and cyclic translations as depicted in Figure S1.

For the corrupted ImageNet dataset, we used ImageNet-C (Hendrycks & Dietterich, 2019). Figure S2 shows examples of ImageNet-C images at varying corruption intensities. Figure S3 shows ImageNet-C images with the 16 corruptions analyzed in this paper, at intensity 3 (on a scale of 1 to 5). Ensembles and dropout outperform all other methods across corruptions, while LL SVI shows no improvement over the baseline model. Figure S6 shows accuracy and ECE for models with double the number of ResNet filters; the higher-capacity models are not better calibrated than their lowercapacity counterparts, suggesting that the good calibration performance of ensembles is not due simply to higher capacity. Figure S9 shows the effect of ensemble size on CIFAR-10 (top) and ImageNet (bottom). Similar to SVI and Dropout, we see that increasing the number of models in the ensemble improves performance with diminishing returns beyond size 5. As mentioned earlier, the Brier score can be further decomposed into BS = calibration + refinement = reliability + uncertainty -resolution where reliability ↓ measures calibration as the average violation of long-term true label frequencies, and refinement = uncertainty -resolution, where uncertainty is the marginal uncertainty over labels (independent of predictions) and resolution ↑ measures the deviation of individual predictions from the marginal.

### D Effect of the number of samples on the quality of uncertainty

### E Variational Gaussian Process Results

### F OOD detection for genomic sequences

We studied the set of methods for detecting OOD genomic sequence, as a challenging realistic problem for OOD detection proposed by Ren et al. (2019). Classifiers are trained on 10 in-distribution bacteria classes, and tested for OOD detection of 60 OOD bacteria classes. The model architecture is the same as that in Ren et al. (2019): a convolutional neural networks with 1000 filters of length 20, followed by a global max pooling layer, a dense layer of 1000 units, and a last dense layer that outputs class prediction logits. For the dropout method, we add a dropout layer each after the max pooling layer and the dense layer respectively. For the LL-Dropout method, only a dropout layer after the dense layer is added. We use the dropout rate of 0.2. For the LL-SVI method, we replace the last dense layer with a stochastic variational inference dense layer. The classification accuracy for in-distribution is around 0.8 for the various types of classifiers.

Figure S11 shows the confidence vs (a) accuracy and (b) count when the test data consists of a mix of in-distribution and OOD data. Ensembles significantly outperform all other methods, and achieve better trade-off between accuracy versus confidence. Dropout performs better than Temp Scaling, and they both perform better than LL-Dropout, LL-SVI, and the Vanilla method. Note that the accuracy on examples p(y|x) ≥ 0.9 for the best method is still below 65%, suggesting that this realistic genomic sequences dataset is a challenging problem to benchmark future methods.

### G Tables of Metrics

The tables below report quartiles of Brier score, negative log-likelihood, and ECE for each model and dataset where quartiles are computed over all corrupted variants of the dataset.

G

## Figures et tableaux

[figure sans légende identifiée] . N : p(y n |x n , θ) ∈ (ρ s , ρ s+1 ]}. That is, ECE = S s=1 |Bs| N | acc(B s ) -conf(B s )|, where acc(B s ) = |B s | -1 n∈Bs [y n = ŷn ], conf(B s ) = |B s | -1 n∈Bs p(ŷ n |x n , θ), and ŷn = arg max y p(y|x n , θ) is the n-th prediction. When bins {ρ s : s ∈ 1 . . . S} are quantiles of the held-out predicted probabilities, |B s | ≈ |B k | and the estimation error is approximately constant. Drawbacks: Due to binning, ECE does not monotonically increase as predictions approach ground truth. If |B s | = |B k |, the estimation error varies across bins.

**Figure 1:** Figure1: Results on MNIST: 1(a) and 1(b) show accuracy and Brier score as the data is increasingly shifted. Shaded regions represent standard error over 10 runs. To understand the discrepancy between accuracy and Brier score, we explore the predictive distributions of each method by looking at the confidence of the predictions in 1(c) and 1(d). We also explore the entropy and confidence of each method on entirely OOD data in 1(e) and 1(f). SVI has lower accuracy on the validation and test splits, but it is significantly more robust to dataset shift as evidenced by a lower Brier score, lower overall confidence 1(d) and higher predictive entropy under shift (1(c)) and OOD data (1(e),1(f)).

**Figure 2:** Calibration under distributional shift: a detailed comparison of accuracy and ECE under all types of corruptions on (a) CIFAR-10 and (b) ImageNet. For each method we show the mean on the test set and summarize the results on each intensity of shift with a box plot. Each box shows the quartiles summarizing the results across all (16) types of shift while the error bars indicate the min and max across different shift types. Figures showing additional metrics are provided in Figures S4 (CIFAR-10) and S5 (ImageNet). Tables for numerical comparisons are provided in Appendix G.

**Figure 3:** Results on CIFAR-10 and ImageNet. Left column: 3(a) and 3(d) show accuracy as a function of confidence. Middle column: 3(b) and 3(e) show the number of examples greater than given confidence values for Gaussian blur of intensity 3. Right column: 3(c) and 3(f) show histogram of entropy and confidences from CIFAR-trained models on a completely different dataset (SVHN).

**Figure 4:** Top row: Histograms of the entropy of the predictive distributions for in-distribution (solid lines), shifted (dotted lines), and completely different OOD (dashed lines) text examples. Bottom row: Confidence score vs accuracy and count respectively when evaluated for in-distribution and in-distribution shift text examples (a,b), and in-distribution and OOD text examples (c,d).

Figure S1: Examples of rotated and cyclically translated MNIST digits. Results for accuracy and calibration on rotated/translated MNIST are shown in Figure 1.

Figure S2: Examples of ImageNet images corrupted by Gaussian blur, at intensities of 0 (uncorrupted image) through 5 (maximum corruption included in ImageNet-C).

Figure S3: Examples of 16 corruption types in ImageNet-C images, at corruption intensity 3 (on a scale from 1-5). The same corruptions were applied to CIFAR-10.Figure 2 and Section C show boxplots for each uncertainty method and corruption intensity, spanning all corruption types.

FigureFigure S8: FigureS8shows the effect of the number of sample sizes used by Dropout, SVI (and last-layer variants) on the quality of predictive uncertainty, as measured by the Brier score. Increasing the number of samples has little effect on last-layer variants, whereas increasing the number of samples improves the performance for SVI and Dropout, with diminishing returns beyond size 5.

Figure S10: FigureS10: Uncertainty metrics across shift levels on CIFAR-10, where level 0 is the test set, using a last layer Variational Gaussian Process. See Appendix A.7 for experiment details.

Figure S11: Confidence score vs accuracy and count respectively when evaluated for in-distribution and OOD genomic sequences.

[figure sans légende identifiée] Results on Criteo: The first two plots show degrading AUCs and Brier scores with increasing shift while the latter two depict the distribution of prediction confidences and their corresponding accuracies at 75% randomization of categorical features. SVI is excluded as it performed too poorly. score at shift-randomization values above 60%. SVI proved challenging to train, and the resulting model uniformly performed poorly; LL-SVI fared better but generally did not improve upon the vanilla model. Strikingly, temperature scaling has a worse Brier score than Vanilla indicating that post-hoc calibration on the validation set actually harms calibration under dataset shift.

     | 0.80 |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.46 |  |  |  |  |  |  |  |  |  |  | 50000 |  |  |  |  |  | 1.00 |  |  |  |  | 
    AUC | Train 0.55 0.60 0.65 0.70 0.75 | Valid | Test | 5% | 15% | 25% | 35% | 45% | 55% | 65% | 75% | 85% | 95% | Brier Score | Train 0.32 0.34 0.36 0.38 0.40 0.42 0.44 | Valid | Test | 5% | 15% Vanilla 25% Dropout LL-Dropout 35% LL-SVI Temp Scaling Ensemble | 45% | 55% | 65% | 75% | 85% | 95% | 0.4 0 10000 20000 30000 40000 ¸¿ Number of examples p(yjx) | 0.5 | 0.6 Vanilla Dropout LL-Dropout 0.7 ¿ LL-SVI Temp Scaling Ensemble | 0.8 | 0.9 | 1.0 | 0.4 0.70 ¸¿ 0.75 0.80 0.85 0.90 0.95 Accuracy on examples p(yjx) | 0.5 | 0.6 Vanilla Dropout LL-Dropout 0.7 ¿ LL-SVI Temp Scaling Ensemble | 0.8 | 0.9 | 1.0
    Figure 5: |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 

[figure sans légende identifiée] Comprehensive comparison of metrics on Criteo models. The Brier decomposition reveals that the majority of its degradation is due to worsening reliability, and this component alone appears to largely explain the ranking of methods in total Brier score. Ensemble notably degrades most rapidly in resolution but persists with better reliability compared other methods for most of the data-corruption range; on ECE it remains roughly in the middle among explored methods. Dropout (and to a lesser extend LL-Dropout) perform best on ECE and experience slower degradation in both resolution and reliability leading it to surpass ensembles at the severe range of data corruption. Total Brier score and AUC results are discussed in detail in Section 4.4.

     |  |  |  |  |  |  |  | 0.80 |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.46 |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Vanilla |  |  |  |  |  | 
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.44 |  |  |  |  | Dropout |  |  |  |  |  | 
     |  |  |  |  |  |  |  | 0.75 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | LL-Dropout |  |  |  |  | 
     |  |  |  | 1.0 |  |  | AUC | 0.65 0.70 |  |  |  |  |  |  |  |  |  |  |  |  | Brier Score | 0.38 0.40 0.42 |  |  |  |  | LL-SVI Temp Scaling Ensemble |  |  |  |  | 
     |  |  |  | 0.9 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.36 |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  |  | 0.60 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 0.8 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.34 |  |  |  |  |  |  |  |  |  |  |  | 
     | 0.270 |  | Accuracy | 0.5 0.6 0.7 |  |  |  | Train 0.55 Vanilla Valid Test | 5% | Method 15% 25% | 35% | 45% LL Dropout 55% 65% 0.09 | 75% | 85% | 95% |  | Train 0.32 | Valid | Test | 5% | 15% | 25% | 35% | 45% 0.20 | 55% | 65% | 75% | 85% | 95%
    Brier Resolution | 0.265 0.240 0.245 0.250 0.255 0.260 |  |  | 0.2 0.4 0.3 0.6 0.7 |  |  |  | Test Temp Scaling Ensemble Vanilla Dropout Dropout Vanilla Method LL-Dropout LL-SVI Temp Scaling Ensemble | 1 | SVI LL SVI 0.08 0.03 LL Dropout 0.04 0.05 0.06 0.07 Brier Reliability |  | 2 | Shift intensity | 3 |  |  | ECE | 0.05 0.15 0.10 | 4 |  |  |  | 5
     |  |  |  | 0.5 |  |  |  |  | Temp Scaling |  |  | SVI |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     | Train 0.235 | Valid | 0.3 0.4 5% ECE Test | 15% | 25% | 35% | Ensemble Dropout 45% 55% 65% | 75% | 85% | 95% | LL SVI Train 0.02 | Valid | Test | 5% | 15% | 25% | 35% | 45% | 55% | 65% | 75% | 85% | 95% |  | Train 0.00 | Valid | Test | 5% | 15% | 25% | 35% | 45% | 55% | 65% | 75% | 85% | 95%
    0.2 Figure S7: |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 0.1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 0.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  |  | Test |  |  |  |  | 1 |  |  |  |  |  | 2 |  |  |  |  |  |  | 3 |  |  |  |  | 4 |  |  |  | 5
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Shift intensity |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.2 |  |  |  |  | Vanilla |  | Method |  | LL Dropout |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  | Brier Score | 0.6 0.8 1.0 |  |  |  |  | Temp Scaling Dropout Ensemble |  |  | SVI LL SVI |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 0.4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 0.2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 0.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  |  | Test |  |  |  |  | 1 |  |  |  |  |  | 2 |  |  |  |  |  |  | 3 |  |  |  |  | 4 |  |  |  | 5
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Shift intensity |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.6 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  |  |  |  |  | Method |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.5 |  |  |  |  | Vanilla |  |  |  |  |  | LL Dropout |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  | Brier Reliability | 1.2 1.3 1.4 |  |  |  |  | Temp Scaling Dropout Ensemble |  |  | SVI LL SVI |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  |  | Test |  |  |  |  | 1 |  |  |  |  |  | 2 |  |  |  |  |  |  | 3 |  |  |  |  | 4 |  |  |  | 5
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Shift intensity |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.8 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.7 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  | Brier Resolution | 1.2 1.3 1.4 1.5 1.6 |  |  |  |  | Method Temp Scaling Vanilla |  | LL Dropout SVI |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.1 |  |  |  |  | Dropout Ensemble |  |  |  |  | LL SVI |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  | 1.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  |  | Test |  |  |  |  | 1 |  |  |  |  |  | 2 |  |  |  |  |  |  | 3 |  |  |  |  | 4 |  |  |  | 5
     |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Shift intensity |  |  |  |  |  |  |  |  | 
    Figure S4: Boxplots facilitating comparison of methods for each shift level showing detailed compar-
    isons of various metrics under all types of corruptions on CIFAR-10. Each box shows the quartiles
    summarizing the results across all types of shift while the error bars indicate the min and max across
    different shift types. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 

[figure sans légende identifiée] .1 CIFAR-10

    G.2 ImageNet |  |  |  |  |  | 
    Method | Vanilla Temp. Scaling Ensembles Dropout LL-Dropout LL-SVI
    Brier Score (25th) | 0.553 | 0.551 | 0.503 | 0.577 | 0.550 | 0.590
    Brier Score (50th) | 0.733 | 0.726 | 0.667 | 0.754 | 0.723 | 0.766
    Brier Score (75th) | 0.914 | 0.899 | 0.835 | 0.922 | 0.896 | 0.938
    NLL (25th) | 1.859 | 1.848 | 1.621 | 1.957 | 1.830 | 2.218
    NLL (50th) | 2.912 | 2.837 | 2.446 | 3.046 | 2.858 | 3.504
    NLL (75th) | 4.305 | 4.186 | 3.661 | 4.567 | 4.208 | 5.199
    ECE (25th) | 0.057 | 0.031 | 0.022 | 0.017 | 0.034 | 0.065
    ECE (50th) | 0.102 | 0.072 | 0.032 | 0.043 | 0.071 | 0.106
    ECE (75th) | 0.164 | 0.129 | 0.053 | 0.109 | 0.123 | 0.148
    G.3 Criteo |  |  |  |  |  | 
    Method | Vanilla Temp. Scaling Ensembles Dropout LL-Dropout | SVI LL-SVI
    Brier Score (25th) | 0.353 | 0.355 | 0.336 | 0.350 | 0.353 0.512 | 0.361
    Brier Score (50th) | 0.385 | 0.391 | 0.366 | 0.373 | 0.379 0.512 | 0.396
    Brier Score (75th) | 0.409 | 0.416 | 0.395 | 0.393 | 0.403 0.512 | 0.421
    NLL (25th) | 0.581 | 0.594 | 0.508 | 0.532 | 0.542 7.479 | 0.554
    NLL (50th) | 0.788 | 0.829 | 0.552 | 0.577 | 0.600 7.479 | 0.633
    NLL (75th) | 0.986 | 1.047 | 0.608 | 0.624 | 0.664 7.479 | 0.711
    ECE (25th) | 0.041 | 0.055 | 0.044 | 0.043 | 0.052 0.254 | 0.066
    ECE (50th) | 0.097 | 0.113 | 0.100 | 0.085 | 0.100 0.254 | 0.127
    ECE (75th) | 0.135 | 0.149 | 0.141 | 0.116 | 0.136 0.254 | 0.162
    Method | Vanilla Temp. Scaling Ensembles Dropout LL-Dropout | SVI LL-SVI
    Brier Score (25th) | 0.243 | 0.227 | 0.165 | 0.215 | 0.259 0.250 | 0.246
    Brier Score (50th) | 0.425 | 0.392 | 0.299 | 0.349 | 0.416 0.363 | 0.431
    Brier Score (75th) | 0.747 | 0.670 | 0.572 | 0.633 | 0.728 0.604 | 0.732
    NLL (25th) | 2.356 | 1.685 | 1.543 | 1.684 | 2.275 1.628 | 2.352
    NLL (50th) | 1.120 | 0.871 | 0.653 | 0.771 | 1.086 0.823 | 1.158
    NLL (75th) | 0.578 | 0.473 | 0.342 | 0.446 | 0.626 0.533 | 0.591
    ECE (25th) | 0.057 | 0.022 | 0.031 | 0.021 | 0.069 0.029 | 0.058
    ECE (50th) | 0.127 | 0.049 | 0.037 | 0.034 | 0.136 0.064 | 0.135
    ECE (75th) | 0.288 | 0.180 | 0.110 | 0.174 | 0.292 0.187 | 0.275
