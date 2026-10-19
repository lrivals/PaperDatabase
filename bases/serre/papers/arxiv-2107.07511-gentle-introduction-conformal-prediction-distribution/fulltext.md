---
id: arxiv-2107.07511-gentle-introduction-conformal-prediction-distribution
title: "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification"
year: 2021
backend: grobid
---

## Abstract

Black-box machine learning models are now routinely used in high-risk settings, like medical diagnostics, which demand uncertainty quantification to avoid consequential model failures. Conformal prediction (a.k.a. conformal inference) is a user-friendly paradigm for creating statistically rigorous uncertainty sets/intervals for the predictions of such models. Critically, the sets are valid in a distribution-free sense: they possess explicit, non-asymptotic guarantees even without distributional assumptions or model assumptions. One can use conformal prediction with any pre-trained model, such as a neural network, to produce sets that are guaranteed to contain the ground truth with a user-specified probability, such as 90%. It is easy-to-understand, easy-to-use, and general, applying naturally to problems arising in the fields of computer vision, natural language processing, deep reinforcement learning, and so on.

This hands-on introduction is aimed to provide the reader a working understanding of conformal prediction and related distribution-free uncertainty quantification techniques with one self-contained document. We lead the reader through practical theory for and examples of conformal prediction and describe its extensions to complex machine learning tasks involving structured outputs, distribution shift, time-series, outliers, models that abstain, and more. Throughout, there are many explanatory illustrations, examples, and code samples in Python. With each code sample comes a Jupyter notebook implementing the method on a real-data example; the notebooks can be accessed and easily run by clicking on the following icons:

.

## 1. Conformal Prediction

Conformal prediction [1][2][3] (a.k.a. conformal inference) is a straightforward way to generate prediction sets for any model. We will introduce it with a short, pragmatic image classification example, and follow up in later paragraphs with a general explanation. The high-level outline of conformal prediction is as follows. First, we begin with a fitted predicted model (such as a neural network classifier) which we will call f . Then, we will create prediction sets (a set of possible labels) for this classifier using a small amount of additional calibration data-we will sometimes call this the calibration step.

Formally, suppose we have images as input and they each contain one of K classes. We begin with a classifier that outputs estimated probabilities (softmax scores) for each class: f (x) ∈ [0, 1] K . Then, we reserve a moderate number (e.g., 500) of fresh i.i.d. pairs of images and classes unseen during training, (X 1 , Y 1 ), . . . , (X n , Y n ), for use as calibration data. Using f and the calibration data, we seek to construct a prediction set of possible labels C(X test ) ⊂ {1, . . . , K} that is valid in the following sense:

1 -α ≤ P(Y test ∈ C(X test )) ≤ 1 -α + 1 n + 1 ,(1)

where (X test , Y test ) is a fresh test point from the same distribution, and α ∈ [0, 1] is a user-chosen error rate.

In words, the probability that the prediction set contains the correct label is almost exactly 1 -α; we call this property marginal coverage, since the probability is marginal (averaged) over the randomness in the calibration and test points. See Figure 1 for examples of prediction sets on the Imagenet dataset.

To construct C from f and the calibration data, we will perform a simple calibration step that requires only a few lines of code; see the right panel of Figure 2. We now describe the calibration step in more detail, introducing some terms that will be helpful later on. First, we set the conformal score s i = 1 -f (X i ) Yi to be one minus the softmax output of the true class. The score is high when the softmax output of the true class is low, i.e., when the model is badly wrong. Next comes the critical step: define q to be the (n+1)(1-α) /n empirical quantile of s 1 , ..., s n , where • is the ceiling function (q is essentially the 1 -α quantile, but with a small correction). Finally, for a new test data point (where X test is known but Y test is not), create a prediction set C(X test ) = {y : f (X test ) y ≥ 1 -q} that includes all classes with a high enough softmax output (see Figure 2). Remarkably, this algorithm gives prediction sets that are guaranteed to satisfy (1)

### Remarks

Let us think about the interpretation of C. The function C is set-valued -it takes in an image, and it outputs a set of classes as in Figure 1. The model's softmax outputs help to generate the set. This method constructs a different output set adaptively to each particular input. The sets become larger when the model is uncertain or the image is intrinsically hard. This is a property we want, because the size of the set gives you an indicator of the model's certainty. Furthermore, C(X test ) can be interpreted as a set of plausible classes that the image X test could be assigned to. Finally, C is valid, meaning it satisfies (1). 1 These properties of C translate naturally to other machine learning problems, like regression, as we will see.

With an eye towards generalization, let us review in detail what happened in our classification problem. To begin, we were handed a model that had an inbuilt, but heuristic, notion of uncertainty: softmax outputs. The softmax outputs attempted to measure the conditional probability of each class; in other words, the jth entry of the softmax vector estimated P(Y = j | X = x), the probability of class j conditionally on an input image x. However, we had no guarantee that the softmax outputs were any good; they may have been arbitrarily overfit or otherwise untrustworthy. Therefore, instead of taking the softmax outputs at face value, we used the holdout set to adjust for their deficiencies.

The holdout set contained n ≈ 500 fresh data points that the model never saw during training, which allowed us to get an honest appraisal of its performance. The adjustment involved computing conformal scores, which grow when the model is uncertain, but are not valid prediction intervals on their own. In our case, the conformal score was one minus the softmax output of the true class, but in general, the score can be any function of x and y. We then took q to be roughly the 1 -α quantile of the scores. In this case, the quantile had a simple interpretation-when setting α = 0.1, at least 90% of ground truth softmax outputs are guaranteed to be above the level 1 -q (we prove this rigorously in Appendix D). Taking advantage of this fact, at test-time, we got the softmax outputs of a new image X test and collected all classes with outputs above 1 -q into a prediction set C(X test ). Since the softmax output of the new true class Y test is guaranteed to be above 1 -q with probability at least 90%, we finally got the guarantee in Eq. (1).

### 1.1. Instructions for Conformal Prediction

As we said during the summary, conformal prediction is not specific to softmax outputs or classification problems. In fact, conformal prediction can be seen as a method for taking any heuristic notion of uncertainty from any model and converting it to a rigorous one (see the diagram below). Conformal prediction does not care if the underlying prediction problem is discrete/continuous or classification/regression.

### Heuristic uncertainty (per input)

### Rigorous uncertainty (per input) conformal prediction

We next outline conformal prediction for a general input x and output y (not necessarily discrete).

1. Identify a heuristic notion of uncertainty using the pre-trained model.

2. Define the score function s(x, y) ∈ R. (Larger scores encode worse agreement between x and y.)

3. Compute q as the (n+1) (1-α) n quantile of the calibration scores s 1 = s(X 1 , Y 1 ), ..., s n = s(X n , Y n ).

## 4. Use this quantile to form the prediction sets for new examples:

C(X test ) = {y : s(X test , y) ≤ q} .

(

)2

As before, these sets satisfy the validity property in (1), for any (possibly uninformative) score function and (possibly unknown) distribution of the data. We formally state the coverage guarantee next.

Theorem 1 (Conformal coverage guarantee; Vovk, Gammerman, and Saunders [5]). Suppose (X i , Y i ) i=1,...,n and (X test , Y test ) are i.i.d. and define q as in step 3 above and C(X test ) as in step 4 above. Then the following holds:

P Y test ∈ C(X test ) ≥ 1 -α.

See Appendix D for a proof and a statement that includes the upper bound in (1). We note that the above is only a special case of conformal prediction, called split conformal prediction. This is the most widely-used version of conformal prediction, and it will be our primary focus. To complete the picture, we describe conformal prediction in full generality later in Section 6 and give an overview of the literature in Section 7.

### Choice of score function

Upon first glance, this seems too good to be true, and a skeptical reader might ask the following question:

How is it possible to construct a statistically valid prediction set even if the heuristic notion of uncertainty of the underlying model is arbitrarily bad?

Let's give some intuition to supplement the mathematical understanding from the proof in Appendix D. Roughly, if the scores s i correctly rank the inputs from lowest to highest magnitude of model error, then the resulting sets will be smaller for easy inputs and bigger for hard ones. If the scores are bad, in the sense that they do not approximate this ranking, then the sets will be useless. For example, if the scores are random noise, then the sets will contain a random sample of the label space, where that random sample is large enough to provide valid marginal coverage. This illustrates an important underlying fact about conformal prediction: although the guarantee always holds, the usefulness of the prediction sets is primarily determined by the score function. This should be no surprise-the score function incorporates almost all the information we know about our problem and data, including the underlying model itself. For example, the main difference between applying conformal prediction on classification problems versus regression problems is the choice of score. There are also many possible score functions for a single underlying model, which have different properties. Therefore, constructing the right score function is an important engineering choice. We will next show a few examples of good score functions.

## 2. Examples of Conformal Procedures

In this section we give examples of conformal prediction applied in many settings, with the goal of providing the reader a bank of techniques to practically deploy. Note that we will focus only on one-dimensional Y in this section, and smaller conformal scores will correspond to more model confidence (such scores are called nonconformity scores). Richer settings, such as high-dimensional Y , complicated (or multiple) notions of error, or where different mistakes cost different amounts, often require the language of risk control, outlined in Section A.

### 2.1. Classification with Adaptive Prediction Sets

Let's begin our sequence of examples with an improvement to the classification example in Section 1. The previous method produces prediction sets with the smallest average size [6], but it tends to undercover hard subgroups and overcover easy ones. Here we develop a different method called adaptive prediction sets (APS) that avoids this problem. We will follow [7] and [4].

As motivation for this new procedure, note that if the softmax outputs f (X test ) were a perfect model of Y test |X test , we would greedily include the top-scoring classes until their total mass just exceeded 1 -α.

# Get scores. calib_X.shape[0] == calib_Y.shape[0] == n cal_pi = cal_smx.argsort (1)[:,::-1]; cal_srt = np.take_along_axis(cal_smx,cal_pi,axis=1).cumsum(axis=1) cal_scores = np.take_along_axis(cal_srt,cal_pi.argsort(axis=1),axis=1)[range(n),cal_labels] # Get the score quantile qhat = np.quantile(cal_scores, np.ceil((n+1)*(1-alpha))/n, interpolation='higher') # Deploy (output=list of length n, each element is tensor of classes) val_pi = val_smx.argsort (1)[:,::-1]; val_srt = np.take_along_axis(val_smx,val_pi,axis=1).cumsum(axis=1) prediction_sets = np.take_along_axis(val_srt <= qhat,val_pi.argsort(axis=1),axis=1) Formally, we can describe this oracle algorithm as

{π 1 (x), ..., π k (x)} , where k = sup    k : k j=1 f (X test ) πj (x) < 1 -α    + 1,

and π(x) is the permutation of {1, ..., K} that sorts f (X test ) from most likely to least likely. In practice, however, this procedure fails to provide coverage, since f (X test ) is not perfect; it only provides us a heuristic notion of uncertainty. Therefore, we will use conformal prediction to turn this into a rigorous notion of uncertainty.

To proceed, we define a score function inspired by the oracle algorithm:

s(x, y) = k j=1 f (x) πj (x) , where y = π k (x).

In other words, we greedily include classes in our set until we reach the true label, then we stop. Unlike the score from Section 1, this one utilizes the softmax outputs of all classes, not just the true class. The next step, as in all conformal procedures, is to set q = Quantile(s 1 , ..., s n ; (n+1)(1-α) n ). Having done so, we will form the prediction set {y : s(x, y) ≤ q}, modified slightly to avoid zero-size sets:

C(x) = {π 1 (x), ..., π k (x)} , where k = sup    k : k j=1 f (x) πj (x) < q   + 1.(3)

Figure 3 shows Python code to implement this method. As usual, these uncertainty sets (with tie-breaking) satisfy (1). See [4] for details and significant practical improvements, which we implemented here: .

### 2.2. Conformalized Quantile Regression

We will next show how to incorporate uncertainty into regression problems with a continuous output, following the algorithm in [8]. We use quantile regression [9] as our base model. As a reminder, the quantile regression algorithm attempts to learn the γ quantile of Y test |X test = x for each possible value of x. We will call the true quantile t γ (x) and the fitted model tγ (x). Since by definition Y test |X test = x lands below t 0.05 (x) with 5% probability and above t 0.95 (x) with 5% probability, we would expect the interval t0.05 (x), t0. 95 (x) to have approximately 90% coverage. However, because the fitted quantiles may be inaccurate, we will conformalize them. Python pseudocode for conformalized quantile regression is in Figure 5.

After training an algorithm to output two such quantiles (this can be done with a standard loss function, see below), t α/2 and t 1-α/2 , we can define the score to be the difference between y and its nearest quantile, s(x, y) = max tα/2 (x) -y, y -t1-α/2 (x) .

After computing the scores on our calibration set and setting q = Quantile(s 1 , ..., s n ; (n+1)(1-α) n ), we can form valid prediction intervals by taking

C(x) = tα/2 (x) -q, t1-α/2 (x) + q .(4)

Intuitively, the set C(x) just grows or shrinks the distance between the quantiles by q to achieve coverage.

q u a n t il e re gre s s io n p rediction s e t Figure 6: A visualization of the conformalized quantile regrssion algorithm in Eq. (4). We adjust the quantiles by the constant q, picked during the calibration step.

As before, C satisfies the coverage property in Eq. (1). However, unlike our previous example in Section 1, C is no longer a set of classes, but instead a continuous interval in R. Quantile regression is not the only way to get such continuous-valued intervals. However, it is often the best way, especially if α is known in advance. The reason is that the intervals generated via quantile regression even without conformal prediction, i.e. [ tα/2 (x), t1-α/2 (x)], have good coverage to begin with. Furthermore, they have asymptotically valid conditional coverage (a concept we will explain in Section 3). These properties propagate through the conformal procedure and lead to prediction sets with good performance.

One attractive feature of quantile regression is that it can easily be added on top of any base model simply by changing the loss function to a quantile loss (informally referred to as a pinball loss),

L γ ( tγ , y) = (y -tγ )γ1 y > tγ + ( tγ -y)(1 -γ)1 y ≤ tγ .

The reader can think of quantile regression as a generalization of L1-norm regression: when γ = 0.5, the loss function reduces to L 0.5 = | tγ (x) -y|/2, which encourages t0.5 (x) to converge to the conditional median. Changing γ just modifies the L1 norm as in the illustration above to target other quantiles. In practice, one can just use a quantile loss instead of MSE at the end of any algorithm, like a neural network, in order to regress to a quantile.

### 2.3. Conformalizing Scalar Uncertainty Estimates

#### 2.3.1. The Estimated Standard Deviation

As an alternative to quantile regression, our next example is a different way of constructing prediction sets for continuous y with a less rich but more common notion of heuristic uncertainty: an estimate of the standard deviation σ(x). For example, one can produce uncertainty scalars by assuming Y test | X test = x follows some parametric distribution-like a Gaussian distribution-and training a model to output the mean and variance of that distribution. To be precise, in this setting we choose to model Y test | X test = x ∼ N (µ(x), σ(x)), and we have models f (x) and σ(x) trained to maximize the likelihood of the data with respect to E [Y test | X test=x ] and Var [Y test | X test = x] respectively. Then, f (x) gets used as the point prediction and σ(x) gets used as the uncertainty. This strategy is so common that it is commoditized: there are inbuilt PyTorch losses, such as GaussianNLLLoss, that enable training a neural network this way. However, we usually know Y test | X test isn't Gaussian, so even if we had infinite data, σ(x) would not necessarily be reliable. We can use conformal prediction to turn this heuristic uncertainty notion into rigorous prediction intervals of the form f (x)± qσ(x).

#### 2.3.2. Other 1-D Uncertainty Estimates

More generally, we assume there is a function u(x) such that larger values encode more uncertainty. This single number can have many interpretations beyond the standard deviation. For example, one instance of an uncertainty scalar simply involves the user creating a model for the magnitude of the residual. In that setting, the user would first fit a model f that predicts y from x. Then, they would fit a second model r (possibly the same neural network), that predicts y -f (x) . If r were perfect, we would expect the set f (x) -r(x), f (x) + r(x) to have perfect coverage. However, our learned model of the error r is often poor in practice.

There are many more such uncertainty scalars than we can discuss in this document in detail, including 1. measuring the variance of f (x) across an ensemble of models, 2. measuring the variance of f (x) when randomly dropping out a fraction of nodes in a neural net, 3. measuring the variance of f (x) to small, random input perturbations, 4. measuring the variance of f (x) over different noise samples input to a generative model, 5. measuring the magnitude of change in f (x) when applying an adversarial perturbation, etc. These cases will all be treated the same way. There will be some point prediction f (x), and some uncertainty scalar u(x) that is large when the model is uncertain and small otherwise (in the residual setting, u(x) := r(x), and in the Gaussian setting, u(x) := σ(x)). We will proceed with this notation for the sake of generality, but the reader should understand that u can be replaced with any function. Now that we have our heuristic notion of uncertainty in hand, we can define a score function, This score function has a natural interpretation: it is a multiplicative correction factor of the uncertainty scalar (i.e., s(x, y)u(x) = y -f (x) ). As before, taking q to be the (1-α)(n+1) n quantile of the calibration scores guarantees us that for a new example,

s(x, y) = y -f (x) u(x) . # model(X)[:,0]=E(Y|X),

P [s(X test , Y test ) ≤ q] ≥ 1 -α =⇒ P Y test -f (X test ) ≤ u(X test )q ≥ 1 -α.

Naturally, we can then form prediction sets using the rule

C(x) = f (x) -u(x)q, f (x) + u(x)q . (5

)

pre dic t i o n s e t Figure 8: A visualization of the uncertainty scalars algorithm in Eq. (5). We produce the set by adding and subtracting qu(x). The constant q is picked during the calibration step.

Let's reflect a bit on the nature of these prediction sets. The prediction sets are valid, as we desired. Due to our construction, they are also symmetric about the prediction, f (x), although symmetry could be relaxed with minor modifications. However, uncertainty scalars do not necessarily scale properly with α. In other words, there is no reason to believe that a quantity like σ would be directly related to quantiles of the label distribution. We tend to prefer quantile regression when possible, since it directly estimates this quantity and thus should be a better heuristic (and in practice it usually is; see [10] for some evaluations). Nonetheless, uncertainty scalars remain in use because they are easy to deploy and have been commoditized in popular machine learning libraries. See Figure 7 for a Python implementation of this method.

### 2.4. Conformalizing Bayes

Our final example of conformal prediction will use a Bayesian model. Bayesian predictors, like Bayesian neural networks, are commonly studied in the field of uncertainty quantification, but rely on many unverifiable and/or incorrect assumptions to provide coverage. Nonetheless, we should incorporate any prior information we have into our prediction sets. We will now show how to create valid prediction sets that are also Bayes optimal among all prediction sets that achieve 1 -α coverage. These prediction sets use the posterior predictive density as a conformal score. The Bayes optimality of this procedure was first proven in [11], and was previously studied in [12,13]. Because our algorithm reduces to picking the labels with high posterior predictive density, the Python code will look exactly the same as in Figure 2. The only difference is interpretation, since the softmax now represents an approximation of a continuous distribution rather than a categorical one.

Let us first describe what a Bayesian would do, given a Bayesian model f (y | x), which estimates the value of the posterior distribution of Y test at label y with input X test = x. If one believed all the necessary assumptions-mainly, a correctly specified model and asymptotically large n-the following would be the optimal prediction set:

S(x) = y : f (y | x) > t , where t is chosen so y∈S(x) f (y | x)dy = 1 -α.

However, because we cannot make assumptions on the model and data, we can only consider f (y | x) to be a heuristic notion of uncertainty.

Following our now-familiar checklist, we can define a conformal score,

s(x, y) = -f (y | x),

which is high when the model is uncertain and otherwise low. After computing q over the calibration data, we can then construct prediction sets:

C(x) = y : f (y | x) > -q . (6

)

prediction set This set is valid because we chose the threshold q via conformal prediction. Furthermore, when certain technical assumptions are satisfied, it has the best Bayes risk among all prediction sets with 1 -α coverage. To be more precise, under the assumptions in [11], C(X test ) has the smallest average size of any conformal procedure with 1 -α coverage, where the average is taken over the data and the parameters. This result should not be a surprise to those familiar with decision theory, as the argument we are making feels similar to that of the Neyman-Pearson lemma. This concludes the final example.

## Discussion

As our examples have shown, conformal prediction is a simple and pragmatic technique with many use cases. It is also easy to implement and computationally trivial. Additionally, the above four examples serve as roadmaps to the user for designing score functions with various notions of optimality, including average size, adaptivity, and Bayes risk. Still more is yet to come-conformal prediction can be applied more broadly than it may first seem at this point. We will outline extensions of conformal prediction to other prediction tasks such as outlier detection, image segmentation, serial time-series prediction, and so on in Section 4. Before addressing these extensions, we will take a deep dive into diagnostics for conformal prediction in the standard setting, including the important topic of conditional coverage.

## 3. Evaluating Conformal Prediction

We have spent the last two sections learning how to form valid prediction sets satisfying rigorous statistical guarantees. Now we will discuss how to evaluate them. Our evaluations will fall into one of two categories.

1. Evaluating adaptivity. It is extremely important to keep in mind that the conformal prediction procedure with the smallest average set size is not necessarily the best. A good conformal prediction procedure will give small sets on easy inputs and large sets on hard inputs in a way that faithfully reflects the model's uncertainty. This adaptivity is not implied by conformal prediction's coverage guarantee, but it is non-negotiable in practical deployments of conformal prediction. We will formalize adaptivity, explore its consequences, and suggest practical algorithms for evaluating it.

2. Correctness checks. Correctness checks help you test whether you've implemented conformal prediction correctly. We will empirically check that the coverage satisfies Theorem 1. Rigorously evaluating whether this property holds requires a careful accounting of the finite-sample variability present with real datasets. We develop explicit formulae for the size of the benign fluctuations-if one observes deviations from 1 -α in coverage that are larger than these formulae dictate, then there is a problem with the implementation.

Many of the evaluations we suggest are computationally intensive, and require running the entire conformal procedure on different splits of data at least 100 times. Naïve implementations of these evaluations can be slow when the score takes a long time to compute. With some simple computational tricks and strategic caching, we can speed this process up by orders of magnitude. Therefore to aid the reader, we intersperse the mathematical descriptions with code to efficiently implement these computations.

### 3.1. Evaluating Adaptivity

Although any conformal procedure yields prediction intervals that satisfy (1), there are many such procedures, and they differ in other important ways. In particular, a key design consideration for conformal prediction is adaptivity: we want the procedure to return larger sets for harder inputs and smaller sets for easier inputs. While most reasonable conformal procedures will satisfy this to some extent, we now discuss precise metrics for adaptivity that allow the user to check a conformal procedure and to compare multiple alternative conformal procedures.

Set size. The first step is to plot histograms of set sizes. This histogram helps us in two ways. Firstly, a large average set size indicates the conformal procedure is not very precise, indicating a possible problem with the score or underlying model. Secondly, the spread of the set sizes shows whether the prediction sets properly adapt to the difficulty of examples. A wider spread is generally desirable, since it means that the procedure is effectively distinguishing between easy and hard inputs.

#

It can be tempting to stop evaluations after plotting the coverage and set size, but certain important questions remain unanswered. A good spread of set sizes is generally better, but it does not necessarily indicate that the sets adapt properly to the difficulty of X. Above seeing that the set sizes have dynamic range, we will need to verify that large sets occur for hard examples. We next formalize this notion and give metrics for evaluating it.

Conditional coverage. Adaptivity is typically formalized by asking for the conditional coverage [14] property:

P [Y test ∈ C(X test ) | X test ] ≥ 1 -α.(7)

That is, for every value of the input X test , we seek to return prediction sets with 1 -α coverage. This is a stronger property than the marginal coverage property in (1) that conformal prediction is guaranteed to achieve-indeed, in the most general case, conditional coverage is impossible to achieve [14]. In other words, conformal procedures are not guaranteed to satisfy (7), so we must check how close our procedure comes to approximating it.

The difference between marginal and conditional coverage is subtle but of great practical importance, so we will spend some time think about the differences here. Imagine there are two groups of people, group A and group B, with frequencies 90% and 10%. The prediction sets always cover Y among people in group A and never cover Y when the person comes from group B. Then the prediction sets have 90% coverage, but not conditional coverage. Conditional coverage would imply that the prediction sets cover Y at least 90% of the time in both groups. This is necessary, but not sufficient; conditional coverage is a very strong property that states the probability of the prediction set needs to be ≥ 90% for a particular person. In other words, for any subset of the population, the coverage should be ≥ 90%. See Figure 10 conditional coverage (at a level of 90%). In the marginal case, all the errors happen in the same groups and regions in X-space. Conditional coverage disallows this behavior, and errors are evenly distributed.

Feature-stratified coverage metric. As a first metric for conditional coverage, we will formalize the example we gave earlier, where coverage is unequal over some groups. The reader can think of these groups as discrete categories, like race, or as a discretization of continuous features, like age ranges. Formally, suppose we have features X

(val) i,1

that take values in {1, . . . , G} for some G. (Here, i = 1, . . . , n val indexes the example in the validation set, and the first coordinate of each feature is the group.) Let I g ⊂ {1, . . . , n val } be the set of observations such that X (val) i,1 = g for g = 1, . . . , G. Since conditional coverage implies that the procedure has the same coverage for all values of X test , we use the following measure:

FSC metric : min g∈{1,...,G} 1 |I g | i∈Ig 1 Y (val) i ∈ C X (val) i

In words, this is the observed coverage among all instances where the discrete feature takes the value g. If conditional coverage were achieved, this would be 1 -α, and values farther below 1 -α indicate a greater violation of conditional coverage. Note that this metric can also be used with a continuous feature by binning the features into a finite number of categories.

Size-stratified coverage metric. We next consider a more general-purpose metric for how close a conformal procedure comes to satisfying (7), introduced in [4]. First, we discretize the possible cardinalities of C(x), into G bins, B 1 , . . . , B G . For example, in classification we might divide the observations into three groups, depending on whether C(x) has one element, two elements, or more than two elements. Let I g ⊂ {1, . . . , n val } be the set of observations falling in bin g for g = 1, . . . , G. Then we consider the following

SSC metric : min g∈{1,...,G} 1 |I g | i∈Ig 1 Y (val) i ∈ C X (val) i

In words, this is the observed coverage for all units for which the set size |C(x)| falls into bin g. As before, if conditional coverage were achieved, this would be 1 -α, and values farther below 1 -α indicate a greater violation of conditional coverage. Note that this is the same expression as for the FSC metric, except that the definition of I g has changed. Unlike the FSC metric, the user does not have to define an important set of discrete features a-priori-it is a general metric that can apply to any example.

See [15] and [16] for additional metrics of conditional coverage.

### 3.2. The Effect of the Size of the Calibration Set

We first pause to discuss how the size of the calibration set affects conformal prediction. We consider this question for two reasons. First, the user must choose this for a practical deployment. Roughly speaking, our conclusion will that be choosing a calibration set of size n = 1000 is sufficient for most purposes. Second, the size of the calibration set is one source of finite-sample variability that we will need to analyze to correctly check the coverage. We will build on the results here in the next section, where we give a complete description of how to check coverage in practice.

How does the size of the calibration set, n, affect conformal prediction? The coverage guarantee in (1) holds for any n, so we can see that our prediction sets have coverage at least 1 -α even with a very small calibration set. Intuitively, however, it may seem that larger n is better, and leads to more stable procedures. This intuition is correct, and it explains why using a larger calibration set is beneficial in practice. The details are subtle, so we carefully work through them here.

The key idea is that the coverage of conformal prediction conditionally on the calibration set is a random quantity. That is, if we run the conformal prediction algorithm twice, each time sampling a new calibration dataset, then check the coverage on an infinite number of validation points, those two numbers will not be equal. The coverage property in (1) says that coverage will be at least 1 -α on average over the randomness in the calibration set, but with any one fixed calibration set, the coverage on an infinite validation set will be some number that is not exactly 1 -α. Nonetheless, we can choose n large enough to control these fluctuations in coverage by analyzing its distribution.

In particular, the distribution of coverage has an analytic form, first introduced by Vladimir Vovk in [14], namely,

P Y test ∈ C (X test ) {(X i , Y i )} n i=1 ∼ Beta (n + 1 -l, l) , where l = (n + 1)α .

Notice that the conditional expectation above is the coverage with an infinite validation data set, holding the calibration data fixed. A simple proof of this fact is available in [14]. We plot the distribution of coverage for several values of n in Figure 11.

Inspecting Figure 11, we see that choosing n = 1000 calibration points leads to coverage that is typically between .88 and .92, hence our rough guideline of choosing about 1000 calibration points. More formally, we can compute exactly the number of calibration points n needed to achieve a coverage of 1 -α ± with probability 1 -δ. Again, the average coverage is always at least 1 -α; the parameter δ controls the tail probabilities of the coverage conditionally on the calibration data. For any δ, the required calibration set size n can be explicitly computed from a simple expression, and we report on several values in Table 1 for the reader's reference. Code allowing the user to produce results for any choice of n and α accompanies the 1: Calibration set size n( ) required for coverage slack with δ = 0.1 and α = 0.1.

### 3.3. Checking for Correct Coverage

As an obvious diagnostic, the user will want to assess whether the conformal procedure has the correct coverage. This can be accomplished by running the procedure over R trials with new calibration and validation sets, and then calculating the empirical coverage for each,

C j = 1 n val n val i=1 1 Y (val) i,j ∈ C j X (val) i,j

, for j = 1, ..., R,

where n val is the size of the validation set, (X

(val) i,j , Y(val)

i,j ) is the ith validation example in trial j, and C j is calibrated using the calibration data from the jth trial. A histogram of the C j should be centered at roughly 1 -α, as in Figure 11. Likewise, the mean value,

C = 1 R R j=1 C j , should be approximately 1 -α.

With real datasets, we only have n + n val data points total to evaluate our conformal algorithm and therefore cannot draw new data for each of the R rounds. So, we compute the coverage values by randomly splitting the n + n val data points R times into calibration and validation datasets, then running conformal. Notice that rather than splitting the data points themselves many times, we can instead first cache all conformal scores and then compute the coverage values over many random splits, as in the code sample in Figure 12.

If properly implemented, conformal prediction is guaranteed to satisfy the inequality in (1). However, if the reader sees minor fluctuations in the observed coverage, they may not need to worry: the finiteness of n, n val , and R can lead to benign fluctuations in coverage which add some width to the Beta distribution in Figure 11. Appendix C gives exact theory for analyzing the mean and standard deviation of C. From this, we will be able to tell if any deviation from 1 -α indicates a problem with the implementation, or

## 4. Extensions of Conformal Prediction

At this point, we have seen the core of the matter: how to construct prediction sets with coverage in any standard supervised prediction problem. We now broaden our horizons towards prediction tasks with different structure, such as side information, covariate shift, and so on. These more exotic problems arise quite frequently in the real world, so we present practical conformal algorithms to address them.

### 4.1. Group-Balanced Conformal Prediction

In certain settings, we might want prediction intervals that have equal error rates across certain subsets of the data. For example, we may require our medical classifier to have coverage that is correct for all racial and ethnic groups. To formalize this, we suppose that the first feature of our inputs, X i,1 , i = 1, ..., n takes values in some discrete set {1, ..., G} corresponding to categorical groups. We then ask for group-balanced coverage:

P (Y test ∈ C(X test ) | X test,1 = g) ≥ 1 -α,(8)

for all groups g ∈ {1, . . . , G}. In words, this means we have a 1 -α coverage rate for all groups. Notice that the group output could be a post-processing of the original features in the data. For example, we might bin the values of X test into a discrete set.

Recall that a standard application of conformal prediction will not necessarily yield coverage within each group simultaneously-that is, (8) may not be satisfied. We saw an example in Figure 10; the marginal guarantee from normal conformal prediction can still be satisfied even if all errors happen in one group.

In order to achieve group-balanced coverage, we will simply run conformal prediction seperately for each group, as visualized below.

Making this formal, given a conformal score function s, we stratify the scores on the calibration set by group, s

(g) i = s(X j , Y j )

, where X j,1 is the ith occurrence of group g.

Then, within each group, we calculate the conformal quantile

q(g) = Quantile s 1 , ..., s n (g) ; (n (g) + 1)(1 -α) n (g)

, where n (g) is the number of examples of group g.

Finally, we form prediction sets by first picking the relevant quantile,

C(x) = y : s(x, y) ≤ q(x1) .

That is, for a point x that we see falls in group x 1 , we use the threshold q(x1) to form the prediction set, and so on. This choice of C satisfies (8), as was first documented by Vovk in [14].

Proposition 1 (Error control guarantee for group-balanced conformal prediction). Suppose (X 1 , Y 1 ), . . . , (X n , Y n ), (X test , Y test ) are an i.i.d. sample from some distribution. Then the set C defined above satisfies the error control property in (8).

### 4.2. Class-Conditional Conformal Prediction

In classification problems, we might similarly ask for coverage on every ground truth class. For example, if we had a medical classifier assigning inputs to class normal or class cancer, we might ask that the prediction sets are 95% accurate both when the ground truth is class cancer and also when the ground truth is class normal. Formally, we return to the classification setting, where Y = {1, ..., K}. We seek to achieve class-balanced coverage,

P (Y test ∈ C(X test ) | Y test = y) ≥ 1 -α,(9)

for all classes y ∈ {1, . . . , K}.

To achieve class-balanced coverage, we will calibrate within each class separately. The algorithm will be similar to the group-balanced coverage of Section 4.1, but we must modify it because we do not know the correct class at test time. (In contrast, in Section 4.1, we observed the group information X test,1 as an input feature.) See the visualization below.

Turning to the algorithm, given a conformal score function s, stratify the scores on the calibration set by class, s

(k) i = s(X j , Y j )

, where Y j is the ith occurrence of class k.

Then, within each class, we calculate the conformal quantile,

q(k) = Quantile s 1 , ..., s n (k) ; (n (k) + 1)(1 -α) n (k)

, where n (k) is the number of examples of class k.

Finally, we iterate through our classes and include them in the prediction set based on their quantiles:

C(x) = y : s(x, y) ≤ q(y) .

Notice that in the preceding display, we take a provisional value of the response, y, and then use the conformal threshold q(y) to determine if it is included in the prediction set. This choice of C satisfies ( 9), as proven by Vovk in [14]; another version can be found in [6].

Proposition 2 (Error control guarantee for class-balanced conformal prediction). Suppose (X 1 , Y 1 ), . . . , (X n , Y n ), (X test , Y test ) are an i.i.d. sample from some distribution. Then the set C defined above satisfies the error control property in (9).

### 4.3. Conformal Risk Control

So far, we have used conformal prediction to construct prediction sets that bound the miscoverage,

P Y test / ∈ C(X test ) ≤ α.(10)

However, for many machine learning problems, the natural notion of error is not miscoverage. Here we show that conformal prediction can also provide guarantees of the form

E C(X test ), Y test ≤ α,(11)

for any bounded loss function that shrinks as C grows. This is called a conformal risk control guarantee. Note that (11) recovers (10) when using the miscoverage loss, C(X test ), Y test = 1 {Y test / ∈ C(X test )}. However, this algorithm also extends conformal prediction to situations where other loss functions, such as the false negative rate (FNR), are more appropriate.

As an example, consider multilabel classification. Here, the response Y i ⊆ {1, ..., K} a subset of K classes. Given a trained model f : X → [0, 1] K , we wish to output sets that include a large fraction of the true classes in Y i . To that end, we post-process the model's raw outputs into the set of classes with sufficiently high scores, C λ (x) = {k : f (X) k ≥ 1 -λ}. Note that as the threshold λ grows, we include more classes in C λ (x)-it becomes more conservative in that we are less likely to omit true classes. Conformal risk control can be used to find a threshold value λ that controls the fraction of missed classes. That is, λ can be chosen so that the expected value of

C λ(X test ), Y test = 1 -|Y test ∩ C λ (X test )|/|Y test |

is guaranteed to fall below a user-specified error rate α. For example, setting α = 0.1 ensures that C λ(X test ) contains 90% of the true classes in Y test on average. We will work through a multilabel classification example in detail in Section 5.1.

Formally, we will consider post-processing the predictions of the model f to create a prediction set C λ (•). The prediction set has a parameter λ that encodes its level of conservativeness: larger λ values yield more conservative outputs (e.g., larger prediction sets). To measure the quality of the output of C λ , we consider a loss function (C λ (x), y) ∈ (-∞, B] for some B < ∞. We require the loss function to be non-increasing as a function of λ. The following algorithm picks λ so that risk control as in (11) holds:

λ = inf λ : R(λ) ≤ α - B -α n ,(12)

where

R(λ) = C λ (X 1 ), Y 1 + . . . + C λ (X n ), Y n /n

is the empirical risk on the calibration data. Note that this algorithm simply corresponds to tuning based on the empirical risk at a slightly more conservative level than α. For example, if B = 1, α = 0.1, and we have n = 1000 calibration points, then we select λ to be the value where empirical risk hits level λ = 0.0991 instead of 0.1.

Then the prediction set C λ(X test ) satisfies (11).

Theorem 2 (Conformal Risk Control [17]). Suppose (X 1 , Y 1 ), . . . , (X n , Y n ), (X test , Y test ) are an i.i.d. sample from some distribution. Further, suppose is a monotone function of λ, i.e., one satisfying

C λ1 (x), y ≥ C λ2 (x), y(13)

for all (x, y) and

λ 1 ≤ λ 2 . Then E C λ(X test ), Y test ≤ α,

where λ is picked as in (12).

Theory and worked examples of conformal risk control are presented in [17]. In Sections 5.1 and 5.2 we show a worked example of conformal risk control applied to tumor segmentation. Furthermore, Appendix A describes a more powerful technique called Learn then Test [18] capable of controlling general risks that do not satisfy (13).

### 4.4. Outlier Detection

Conformal prediction can also be adapted to handle unsupervised outlier detection. Here, we have access to a clean dataset X 1 , . . . , X n and wish to detect when test points do not come from the same distribution. As before, we begin with a heuristic model that tries to identify outliers; a larger score means that the model judges the point more likely to be an outlier. We will then use a variant of conformal prediction to calibrate it to have statistical guarantees. In particular, we will guarantee that it does not return too many false positives.

Formally, we will construct a function that labels test points as outliers or inliers, C : X → {outlier, inlier}, such that

P (C(X test ) = outlier) ≤ α,(14)

where the probability is over X test , a fresh sample from the clean-data distribution. The algorithm for achieving ( 14) is similar to the usual conformal algorithm. We start with a conformal score s : X → R (note that since we are in the unsupervised setting, the score only depends on the features). Next, we compute the conformal score on the clean data: s i = s(X i ) for i = 1, . . . , n. Then, we compute the conformal threshold in the usual way: q = quantile s 1 , . . . , s n ;

(n + 1)(1 -α) n .

Lastly, when we encounter a test point, we declare it to be an outlier if the score exceeds q:

C(x) = inlier if s(x) ≤ q outlier if s(x) > q .

This construction guarantees error control, as we record next.

Proposition 3 (Error control guarantee for outlier detection). Suppose X 1 , . . . , X n , X test are an i.i.d. sample from some distribution. Then the set C defined above satisfies the error control property in (14).

As with standard conformal prediction, the score function is very important for the method to perform well-that is, to be effective at flagging outliers. Here, we wish to choose the score function to effectively distinguish the type of outliers that we expect to see in the test data from the clean data. The general problem of training models to distinguish outliers is sometimes called anomaly detection, novelty detection, or one-class classification, and there are good out-of-the box methods for doing this; see [19] for an overview of outlier detection. Conformal outlier detection can also be seen as a hypothesis testing problem; points that are rejected as outliers have a p-value less than alpha for the null hypothesis of exchangeability with the calibration data. This interpretation is closely related to the classical permutation test [20,21]. See [22][23][24] for more on this interpretation and other statistical properties of conformal outlier detection.

### 4.5. Conformal Prediction Under Covariate Shift

All previous conformal methods rely on Theorem 1, which assumes that the incoming test points come from the same distribution as the calibration points. However, past data is not necessarily representative of future data in practice.

One type of distribution shift that conformal prediction can handle is covariate shift. Covariate shift refers to the situation where the distribution of X test changes from P to P test , but the relationship between X test and Y test , i.e. the distribution of Y test |X test , stays fixed. Imagine our calibration features {X i } n i=1 are drawn independently from P but our test feature X test is drawn from P test . Then, there has been a covariate shift, and the data are no longer i.i.d. This problem is common in the real world. For example,

• You are trying to predict diseases from MRI scans. You conformalized on a balanced dataset of 50% infants and 50% adults, but in reality, the frequency is 5% infants and 95% adults. Deploying the model in the real world would invalidate coverage; the infants are over-represented in our sample, so diseases present during infancy will be over-predicted. This was a covariate shift in age.

• You are trying to do instance segmentation, i.e., to segment each object in an image from the background. You collected your calibration images in the morning but seek to deploy your system in the afternoon. The amount of sunlight has changed, and more people are eating lunch. This was a covariate shift in the time of day.

To address the covariate shift from P to P test , one can form valid prediction sets with weighted conformal prediction, first developed in [25].

In weighted conformal prediction, we account for covariate shift by upweighting conformal scores from calibration points that would be more likely under the new distribution. We will be using the likelihood ratio

w(x) = dP test (x) dP(x) ;

usually this is just the ratio of the new PDF to the old PDF at the point x. Now we define our weights,

p w i (x) = w(X i ) n j=1

w(X j ) + w(x)

and p w test (x) = w(x) n j=1 w(X j ) + w(x)

.

Intuitively, the weight p w i (x) is large when X i is likely under the new distribution, and p w test (x) is large when the input x is likely under the new distribution. We can then express our conformal quantile as the 1 -α quantile of a reweighted distribution, q(x) = inf s j :

j i=1 p w i (x)1 {s i ≤ s j } ≥ 1 -α ,

where above for notational convenience we assume that the scores are ordered from smallest to largest a-priori. The choice of quantile is the key step in this algorithm, so we pause to parse it. First of all, notice that the quantile is now a function of an input x, although the dependence is only minor. Choosing

p w i (x) = p w test (x) = 1 n+1

gives the familiar case of conformal prediction-all points are equally weighted, so we end up choosing the (n + 1)(1 -α) th-smallest score as our quantile. When there is covariate shift, we instead re-weight the calibration points with non-equal weights to match the test distribution. If the covariate shift makes easier values of x more likely, it makes our quantile smaller. This happens because the covariate shift puts more weight on small scores-see the diagram below. Of course, the opposite holds the covariate shift upweights difficult values of x: so the covariate-shift-adjusted quantile grows.

### Covariate shift conformal

With this quantile function in hand, we form our prediction set in the standard way, C(x) = {y : s(x, y) ≤ q(x)} .

By accounting for the covariate shift in our choice of q, we were able to make our calibration data look exchangeable with the test point, achieving the following guarantee.

Theorem 3 (Conformal prediction under covariate shift [25]). Suppose (X 1 , Y 1 ), ..., (X n , Y n ) are drawn i.i.d. from P × P Y |X and that (X test , Y test ) is drawn independently from P test × P Y |X . Then the choice of C above satisfies

P (Y test ∈ C(X test )) ≥ 1 -α.

Conformal prediction under various distribution shifts is an active and important area of research with many open challenges. This algorithm addresses a somewhat restricted case-that of a known covariate shift-but is nonetheless quite practical.

### 4.6. Conformal Prediction Under Distribution Drift

Another common form of distribution shift is distribution drift: slowly varying changes in the data distribution. For example, when collecting time-series data, the data distribution may change-furthermore, it may change in a way that is unknown or difficult to estimate. Here, one can imagine using weights that give more weight to recent conformal scores. The following theory provides some justification for such weighted conformal procedures; in particular, they always satisfy marginal coverage, and are exact when the magnitude of the distribution shift is known.

More formally, suppose the calibration data {(X i , Y i )} n i=1 are drawn independently from different distributions {P i } n i=1 and the test point (X test , Y test ) is drawn from P test . Given some weight schedule w 1 , ..., w n , w i ∈ [0, 1], we will consider the calculation of weighted quantiles using the calibration data:

q = inf q : n i=1 wi 1 {s i ≤ q} ≥ 1 -α ,

where the wi are normalized weights, wi = w i w 1 + . . . + w n + 1 .

Then we can construct prediction sets in the usual way,

C(x) = {y : s(x, y) ≤ q} .

We now state a theorem showing that when the distribution is shifting, it is a good idea to apply a discount factor to old samples. In particular, let i = d TV (X i , Y i ), (X test , Y test ) be the TV distance between the ith data point and the test data point. The TV distance is a measure of how much the distribution has shifted-a large i (close to 1) means the ith data point is not representative of the new test point. The result states that if w discounts those points with large shifts, the coverage remains close to 1 -α.

Theorem 4 (Conformal prediction under distribution drift [26]).

Suppose i = d TV (X i , Y i ), (X test , Y test ) .

Then the choice of C above satisfies

P (Y test ∈ C(X test )) ≥ 1 -α -2 n i=1 wi i .

When either factor in the product wi i is small, that means that the ith data point doesn't result in loss of coverage. In other words, if there isn't much distribution shift, we can place a high weight on that data point without much penalty, and vice versa. Setting i = 0 above, we can also see that when there is no distribution shift, there is no loss in coverage regardless of what choice of weights is used-this fact had been observed previously in [25,27].

The i are never known exactly in advance-we only have some heuristic sense of their size. In practice, for time-series problems, it often suffices to pick either a rolling window of size K or a smooth decay using some domain knowledge about the speed of the drift:

w fixed i = 1 {i ≥ n -K} or w decay i = 0.99 n-i+1 .

We give a worked example of this procedure for a distribution shifting over time in Section 5.3.

As a final point on this algorithm, we note that there is some cost to using this or any other weighted conformal procedure. In particular, the weights determine the effective sample size of the distribution:

n eff (w 1 , . . . , w n ) = w 1 + . . . + w n w 2 1 + . . . + w 2 n .

This is quite important in practice, since the variance of the weighted conformal procedure can explode when n eff is small; as in Section 3, the variance of coverage scales as 1/ √ n eff , which can be large if too many of the w i are small. To see more of the theory of weighted conformal prediction under distribution drift, see [26].

## 5. Worked Examples

We now show several worked examples of the techniques described in Section 4. For each example, we provide Jupyter notebooks that allow the results to be conveniently replicated and extended. In the multilabel classification setting, we receive an image and predict which of K objects are in an image. We have a pretrained model f that outputs estimated probabilities for each of the K classes. We wish to report on the possible classes contained in the image, returning most of the true labels. To this end, we will threshold the model's outputs to get the subset of K classes that the model thinks is most likely, C λ (x) = {y : f (x) ≥ λ}, which we call the prediction. We will use conformal risk control (Section 4.3) to pick the threshold value λ certifying a low false negative rate (FNR), i.e., to guarantee the average fraction of ground truth classes that the model missed is less than α. In the tumor segmentation setting, we receive an M × N × 3 image of a tumor and predict an M × N binary mask, where '1' indicates a tumor pixel. We start with a pretrained segmentation model f that outputs an M × N grid of the estimated probabilities that each pixel is a tumor pixel. We will threshold the model's outputs to get our predicted binary mask, C λ (x) = {(i, j) : f (x) (i,j) ≥ λ}, which we call the prediction. We will use conformal risk control (Section 4.3) to pick the threshold value λ certifying a low FNR, i.e., guaranteeing the average fraction of tumor pixels missed is less than α.

### 5.1. Multilabel Classification

### 5.2. Tumor Segmentation

More formally, our calibration set {(X i , Y i )} n i=1 contains exchangeable images X i and sets of tumor pixels Y i ⊆ {1, . . . , M } × {1, . . . , N }. As in the previous example, we let the loss be the false negative proportion, FNR . Then, picking λ as in 12 yields the bound on the FNR in 5.1. Figure 14 gives results and code on a dataset of gut polyps. On the left is a plot of coverage over time; 'weighted' denotes the procedure in Section 5.3 while 'unweighted' denotes the procedure that simply computes the conformal quantile on all conformal scores seen so far. Note that we compute coverage using a sliding window of 500 points, which explains some of the variability in the coverage. Running the notebook with a trailing average of 5000 points reveals that the unweighted version systematically undercovers before the change-point as well. On the right is a plot showing the intervals resulting from the weighted procedure.

### 5.3. Weather Prediction with Time-Series Distribution Shift

In this example we seek to predict the temperature of different locations on Earth given covariates such as the latitude, longitude, altitude, atmospheric pressure, and so on. We will make these predictions serially in time. Dependencies between adjacent data points induced by local and global weather changes violate the standard exchangeability assumption, so we will need to apply the method from Section 4.6.

In this setting, we have a time series (X t , Y t ) T t=1 , where the X t are tabular covariates and the Y t ∈ R are temperatures in degrees Celsius. Note that these data points are not exchangeable or i.i.d.; adjacent data points will be correlated. We start with a pretrained model f taking features and predicting temperature and an uncertainty model û takes features and outputs a scalar notion of uncertainty. Following Section 2.3, we compute the conformal scores

s t = Y t -f (X t ) û(X t ) .

Since we observe the data points sequentially, we also observe the scores sequentially, and we will need to pick a different conformal quantile for each incoming data point. More formally, consider the task of predicting the temperature at time t ≤ T . We use the weighted conformal technique in Section 5.3 with the fixed K-sized window w t = 1 {t ≥ t -K} for all t < t. This yields the quantiles qt = inf q : 1 min(K, t -1) + 1

t-1 t =1 s t 1 {t ≥ t -K} ≥ 1 -α .

With these adjusted quantiles in hand, we form prediction sets at each time step in the usual way,

C(X t ) = f (X t ) -qt û(X t ) , f (X t ) + qt û(X t ) .

We run this procedure on the Yandex Weather Prediction dataset. This dataset is part of the Shifts Project [29], which also provides an ensemble of 10 pretrained CatBoost [30] models for making the temperature predictions. We take the average prediction of these models as our base model f . Each of the models has its own internal variance; we take the average of these variances as our uncertainty scalar û. The dataset includes an in-distribution split of fresh data from the same time frame that the base model was trained and an out-of-distribution split consisting of time windows the model has never seen. We concatenate these datasets in time, leading to a large change point in the score distribution. Results in Figure 15 show that the weighted method works better than a naive unweighted conformal baseline, achieving the desired coverage in steady-state and recovering quickly from the change point. There is no hope of measuring the TV distance between adjacent data points in order to apply Theorem 4, so we cannot get a formal coverage bound. Nonetheless, the procedure is useful with this simple fixed window of weights, which we chose with only a heuristic understanding of the distribution drift speed. It is worth noting that conformal prediction for time-series applications is a particularly active area of research currently, and the method we have presented is not clearly the best. See [31][32][33] and [34] for two differing perspectives.

### 5.4. Toxic Online Comment Identification via Outlier Detection

True Negative:

ХОТЕЛОСЬ БЫ УЗНАТЬ ,КАК В ЭТОМ ГОДУ БУДУ ТПРОИЗВОДИТЬ СПУСК ВОДЫ И БУДУТ ЛИ ЗАТОПЛЕНИЯ I would like to know how water will be drained this year and whether there will be flooding.

### True Positive:

CALLATE BOT DE M****A SIN VIDA SOCIAL SHUT UP, BOT OF S**T WITHOUT A SOCIAL LIFE False Positive: Bah, sono completamente d accordo con te, e questa dovrebbe essere un enciclopedia libera???? veramente ridicolo! Bah, I completely agree with you, and this is supposed to be a free encyclopedia ????

False Negative:

votre petit discours provocateur à souhait n a pas plus d effet sur moi qu un pet de lapin sur une toile cirée your provocative little speech has no more effect on me than a rabbit fart on an oilcloth We provide a type-1 error guarantee on a model that flags toxic online comments, such as threats, obscenity, insults, and identity-based hate. Suppose we are given n non-toxic text samples X 1 , ..., X n and asked whether a new text sample X test is toxic. We also have a pre-trained toxicity prediction model f (x) ∈ [0, 1], where values closer to 1 indicate a higher level of toxicity. The goal is to flag as many toxic comments as possible while not flagging more than α proportion of non-toxic comments.

The outlier detection procedure in Section 4.4 applies immediately. First, we run the model on each calibration point, yielding conformal scores s i = f (X i ). Taking the toxicity threshold q to be the (n + 1)(1 -α) -smallest of the s i , we construct the function

C(x) = inlier f (x) ≤ q outlier f (x) > q.

This gives the guarantee in Proposition 3-no more than α fraction of future nontoxic text will be classified as toxic.

Figure 16 shows results of this procedure using the Unitary Detoxify BERT-based model [35,36] on the Jigsaw Multilingual Toxic Comment Classification dataset from the WILDS benchmark [37]. It is composed of comments from the talk channels of Wikipedia pages. With a type-1 error of α = 10%, the system correctly flags 70% of all toxic comments.

### 5.5. Selective Classification

In many situations, we only want to show a model's predictions when it is confident. For example, we may only want to make medical diagnoses when the model will be 95% accurate, and otherwise to say "I don't know." We next demonstrate a system that strategically abstains in order to achieve a higher accuracy than the base model in the problem of image classification.

More formally, given image-class pairs {(X i , Y i )} n i=1 and an image classifier f , we seek to ensure

P Y test = Y (X test ) P (X test ) ≥ λ ≥ 1 -α,(15)

where Y (x) = arg max y f (x) y , P (X test ) = max y f (x) y , and λ is a threshold chosen using the calibration data. This is called a selective accuracy guarantee, because the accuracy is only computed over a subset of high-confidence predictions. This quantity cannot be controlled with techniques we've seen so far, since we are not guaranteed that model accuracy is monotone in the cutoff λ. Nonetheless, it can be handled with Learn then Test-a framework for controlling arbitrary risks (see Appendix A). We show only the special case of controlling selective classification accuracy here.

We pick the threshold using based on the empirical estimate of selective accuracy on the calibration set,

R(λ) = 1 n(λ) n i=1 1 Y i = Y (X i ) and P (X i ) ≥ λ , where n(λ) = n i=1 1 P (X i ) ≥ λ .

Since this function is not monotone in λ, we will choose λ differently than in Section 4.3. In particular, we will scan across values of λ looking at a conservative upper bound for the true risk (i.e., the top end of a confidence interval for the selective misclassification rate). Realizing that R(λ) is a Binomial random variable with n(λ) trials, we upper-bound the misclassification error as

R + (λ) = sup r : BinomCDF( R(λ); n(λ), r) ≥ δ

for some user-specified failure rate δ ∈ [0, 1]. Then, scan the upper bound until the last time the bound exceeds α, λ = inf λ : R + (λ ) ≤ α for all λ ≥ λ .

Deploying the threshold λ will satisfy (15) with high probability.

Proposition 4. Assume the {(X i , Y i )} n i=1 and (X test , Y test ) are i.i.d. and λ is chosen as above. Then (15) is satisfied with probability 1 -δ.

See results on Imagenet at level α = 0.1 in Figure 17. For a deeper dive into this procedure and techniques for controlling other non-monotone risks, see Appendix A.

## 6. Full conformal prediction

Up to this point, we have only considered split conformal prediction, otherwise known as inductive conformal prediction. This version of conformal prediction is computationally attractive, since it only requires fitting the model one time, but it sacrifices statistical efficiency because it requires splitting the data into training and calibration datasets. Next, we consider full conformal prediction, or transductive conformal prediction, which avoids data splitting at the cost of many more model fits. Historically, full conformal prediction was developed first, and then split conformal prediction was later recognized as an important special case. Next, we describe full conformal prediction. This discussion is motivated from three points of view. First, full conformal prediction is an elegant, historically important idea in our field. Second, the exposition will reveal a complimentary interpretation of conformal prediction as a hypothesis test. Lastly, full conformal prediction is a useful algorithm when statistical efficiency is of paramount importance.

### 6.1. Full Conformal Prediction

This topic requires expanded notation. Let (X 1 , Y 1 ), . . . , (X n+1 , Y n+1 ) be n + 1 exchangeable data points. As before, the user sees (X 1 , Y 1 ), . . . , (X n , Y n ) and X n+1 , and wishes to make a prediction set that contains Y n+1 . But unlike split conformal prediction, we allow the model to train on all the data points, so there is no separate calibration dataset.

The core idea of full conformal prediction is as follows. We know that the true label, Y n+1 , lives somewhere in Y -so if we loop over all possible y ∈ Y, then we will eventually hit the data point (X n+1 , Y n+1 ), which is exchangeable with the first n data points. Full conformal prediction is so-named because it directly computes this loop. For each y ∈ Y, we fit a new model f y to the augmented dataset (X 1 , Y 1 ), . . . , (X n+1 , y). Importantly, the model fitting for f must be invariant to permutations of the data. Then, we compute a score function s y i = s(X i , Y i , f y ) for i = 1,. . . ,n and s y n+1 = s(X n+1 , y, f y ). This score function is exactly the same as those from Section 2, except that the model f y is now given as an argument because it is no longer fixed. Then, we calculate the conformal quantile, qy = Quantile s y 1 , . . . , s y n ;

(n + 1)(1 -α) n .

Then, we collect all values of y that are sufficiently consistent with the previous data (X 1 , Y 1 ), . . . , (X n , Y n ) are collected into a confidence set for the unknown value of Y n+1 :

C(X test ) = {y : s y n+1 ≤ qy }. (16

)

This prediction set has the same validity guarantee as before:

Theorem 5 (Full conformal coverage guarantee [1]). Suppose (X 1 , Y 1 ), ..., (X n+1 , Y n+1 ) are drawn i.i.d. from P, and that f is a symmetric algorithm. Then the choice of C above satisfies

P (Y n+1 ∈ C(X n+1 )) ≥ 1 -α.

More generally, the above holds for exchangeable random variables (X 1 , Y 1 ), ..., (X n+1 , Y n+1 ); the proof of Theorem 5 critically relies on the fact that the score s . We defer the proof to [1], and note that upper bound in (1) also holds when the score function is continuous.

What about computation? In principle, to compute (16), we must iterate over all y ∈ Y, which leads to a substantial computational burden. (When Y is continuous, we would typically first discretize the space and then check each element in a finite set.) For example, if |Y | = K, then computing ( 16) requires (n + 1) • K model fits. For some specific score functions, the set in (16) can actually be computed exactly even for continuous Y , and we refer the reader to [1] and [38] for a summary of such cases and [39,40] for recent developments. Still, full conformal prediction is generally computationally costly.

Lastly, we give a statistical interpretation for the prediction set in ( 16). The condition s y n+1 ≤ qy is equivalent to the acceptance condition of a certain permutation test. To see this, consider a level α permutation test for the exchangeability of s y 1 , . . . , s y n and the test score s y n+1 , rejecting when the score function is large. The values of y such that the test does not reject are exactly those in (16). In words, the confidence set is all values of y such that the hypothetical data point is consistent with the other data, as judged by this permutation test. We again refer the reader to [1] for more on this viewpoint on conformal prediction.

### 6.2. Cross-Conformal Prediction, CV+, and Jackknife+

Split conformal prediction requires only one model fitting step, but sacrifices statistical efficiency. On the other hand, full conformal prediction requires a very large number of model fitting steps, but has high statistical efficiency. These are not the only two achievable points on the spectrum-there are techniques that fall in between, trading off statistical efficiency and computational efficiency differently. In particular, cross-conformal prediction [41] and CV+/Jackknife+ [42] both use a small number of model fits, but still use all data for both model fitting and calibration. We refer the reader to those works for a precise description of the algorithms and corresponding statistical guarantees.

## 7. Historical Notes on Conformal Prediction

We hope the reader has enjoyed reading the technical content in our gentle introduction. As a dénouement, we now pay homage to the history of conformal prediction. Specifically, we will trace the history of techniques related to conformal prediction that are distribution-free, i.e., (1) agnostic to the model, (2) agnostic to the data distribution, and (3) valid in finite samples. There are other lines of work in statistics with equal claim to the term "distribution-free" especially when it is interpreted asymptotically, such as permutation tests [43], quantile regression [9], rank tests [44][45][46], and even the bootstrap [47,48]-the following is not a history of those topics. Rather, we focus on the progenitors and progeny of conformal prediction.

### Origins

The story of conformal prediction begins sixty-three kilometers north of the seventh-largest city in Ukraine, in the mining town of Chervonohrad in the Oblast of Lviv, where Vladimir Vovk spent his childhood. Vladimir's parents were both medical professionals, of Ukrainian descent, although the Lviv region changed hands many times over the years. During his early education, Vovk recalls having very few exams, with grades mostly based on oral answers. He did well in school and eventually took first place in the Mathematics Olympiad in Ukraine; he also got a Gold Medal, meaning he was one of the top graduating secondary school students. Perhaps because he was precocious, his math teacher would occupy him in class by giving him copies of a magazine formerly edited by Isaak Kikoin and Andrey Kolmogorov, Kvant, where he learned about physics, mathematics, and engineering-see Figure 18. Vladimir originally attended the Moscow Second Medical Institute (now called the Russian National Research Medical University) studying Biological Cybernetics, but eventually became disillusioned with the program, which had too much of a medical emphasis and imposed requirements to take classes like anatomy and physiology (there were "too many bones with strange Latin names"). Therefore, he sat the entrance exams a second time and restarted school at the Mekh-Mat (faculty of mechanics and mathematics) in Moscow State University. In his third year there, he became the student of Andrey Kolmogorov. This was when the seeds of conformal prediction were first laid. Today, Vladimir Vovk is widely recognized for being the co-inventor of conformal prediction, along with collaborators Alexander Gammerman, Vladimir Vapnik, and others, whose contributions we will soon discuss. First, we will relay some of the historical roots of conformal prediction, along with some oral history related by Vovk that may be forgotten if never written. Work on collectives began at the turn of the 20th century, with Gustav Fechner's Kollectivmasslehre [49], and was developed significantly by von Mises [50], Abraham Wald [51], Alonzo Church [52], and so on. A long debate ensued among these statisticians as to whether von Mises' axioms formed a valid foundation for probability, with Jean Ville being a notable opponent [53]. Although the theory of von Mises' collectives is somewhat defunct, the mathematical ideas generated during this time continue to have a broad impact on statistics, as we will see. More careful historical reviews of the original debate on collectives exist elsewhere [52,[54][55][56]. We focus on its connection to the development of conformal prediction.

### Vladimir Vovk

Kolmogorov's interest in Bernoulli sequences continued into the 1970s and 1980s, when Vovk was his student. Vovk recalls that, on the way to the train station, Kolmogorov told him (not in these exact words), "Look around you; you do not only see infinite sequences. There are finite sequences."

Feeling that the finite case was practically important, Kolmogorov extended the idea of collectives via Bernoulli sequences.

Definition 1 (Bernoulli sequence, informal). A deterministic binary sequence of length n with k 1s is Bernoulli if it is a "random" element of the set of all n k sequences of the same length and with the same number of 1s. "Random" is defined as having a Kolmogorov complexity close to the maximum, log n k .

As is typical in the study of random sequences, the underlying object itself is not a sequence of random variables. Rather, Kolmogorov quantified the "typicality" of a sequence via Kolmogorov complexity: he asked how long a program we would need to write in order to distinguish it from other sequences in the same space [57][58][59]. Vovk's first work on random sequences modified Kolmogorov's [60] definition to better reflect the randomness in an event like a coin toss. Vovk discusses the history of Bernoulli sequences, including the important work done by Martin-Löf and Levin, in the Appendix of [61]. Learning the theory of Bernoulli sequences brought Vovk closer to understanding finite-sample exchangeability and its role in prediction problems.

We will make a last note about the contributions of the early probabilists before moving to the modern day. The concept of a nonconformity score came from the idea of (local) randomness deficiency. Consider the sequence 00000000000000000000000000000000000000000000000000000000000000000001.

With a computer, we could write a very short program to identify the '1' in the sequence, since it is atypical -it has a large randomness deficiency. But to identify any particular '0' in the sequence, we must specify its location, because it is so typical -it has a small randomness deficiency. A heuristic understanding suffices here, and we defer the formal definition of randomness deficiency to [62], avoiding the notation of Turing machines and Kolmogorov complexity. When randomness deficiency is large, a point is atypical, just like the scores we discussed in Section 2. These ideas, along with the existing statistical literature on tolerance intervals [63][64][65][66] and works related to de Finetti's theorems on exchangeability [67][68][69][70][71][72] formed the seedcorn for conformal prediction: the rough notion of collectives eventually became exchangeability, and the idea of randomness deficiency eventually became nonconformity. Furthermore, the early literature on tolerance intervals was quite close mathematically to conformal prediction-indeed, the fact that order statistics of a uniform distribution are Beta distributed was known at the time, and this was used to form prediction regions in high probability, much like [14]; more on this connection is available in Edgar Dobriban's lecture notes [73].

### Enter Conformal Prediction

The framework we now call conformal prediction was hatched by Vladimir Vovk, Alexander Gammerman, Craig Saunders, and Vladimir Vapnik in the years 1996-1999, first using e-values [74] and then with pvalues [5,75]. For decades, Vovk and collaborators developed the theory and applications of conformal prediction. Key moments include:

• the 2002 proof that in online conformal prediction, the probability of error is independent across time-steps [76];

• the 2002 development, along with Harris Papadopoulos and Kostas Proedrou, of split-conformal predictors [2];

• Glenn Shafer coins the term "conformal predictor" on December 1, 2003 while writing Algorithmic Learning in a Random World with Vovk [1].

• the 2003 development of Venn Predictors [77] (Vovk says this idea came to him on a bus in Germany during the Dagstuhl seminar "Kolmogorov Complexity & Applications");

• the 2012 founding of the Symposium on Conformal and Probabilistic Prediction and its Applications (COPA), hosted in Greece by Harris Papadopoulos and colleagues;

• the 2012 creation of cross-conformal predictors [41] and Venn-Abers predictors [78];

• The 2017 invention of conformal predictive distributions [79].

Algorithmic Learning in a Random World [1], by Vovk, Gammerman, and Glenn Shafer, contains further perspective on the history described above in the bibliography of Chapter 2 and the main text of Chapter 10. Also, the book's website links to several dozen technical reports on conformal prediction and related topics. We now help the reader understand some of these key developments.

Conformal prediction was recently popularized in the United States by the pioneering work of Jing Lei, Larry Wasserman, and colleagues [3,[80][81][82][83]. Vovk himself remembers Wasserman's involvement as a landmark moment in the history of the field. In particular, their general framework for distribution-free predictive inference in regression [83] has been a seminal work. They have also, in the special cases of kernel density estimation and kernel regression, created efficient approximations to full conformal prediction [3,84]. Jing Lei also created a fast and exact conformalization of the Lasso and elastic net procedures [85]. Another equally important contribution of theirs was to introduce conformal prediction to thousands of researchers, including the authors of this paper, and also Rina Barber, Emmanuel Candès, Aaditya Ramdas, Ryan Tibshirani who themselves have made recent fundamental contributions. Some of these we have already touched upon in Section 2, such as adaptive prediction sets, conformalized quantile regression, covariate-shift conformal, and the idea of conformal prediction as indexing nested sets [86]. This group also did fundamental work circumscribing the conditions under which distribution-free conditional guarantees can exist [87], building on previous works by Vovk, Lei, and Wasserman that showed for an arbitrary continuous distribution, conditional coverage is impossible [3,14,83]. More fine-grained analysis of this fact has also recently been done in [88], showing that vanishing-width intervals are achievable if and only if the effective support size of the distribution of X test is smaller than the square of the sample size.

### Current Trends

We now discuss recent work in conformal prediction and distribution-free uncertainty quantification more generally, providing pointers to topics we did not discuss in earlier sections. Many of the papers we cite here would be great starting points for novel research on distribution-free methods.

Many recent papers have focused on designing conformal procedures to have good practical performance according to specific desiderata like small set sizes [6], coverage that is approximately balanced across regions of feature space [4,7,15,27,87,89], and errors balanced across classes [6,23,90,91]. This usually involves adjusting the conformal score; we gave many examples of such adjustments in Section 2. Good conformal scores can also be trained with data to optimize more complicated desiderata [92].

Many statistical extensions to conformal prediction have also emerged. Such extensions include the ideas of risk control [4,18] and covariate shift [25] that we previously discussed. One important and continual area of work is distribution shift, where our test point has a different distribution from our calibration data. For example, [93] builds a conformal procedure robust to shifts of known f -divergence in the score function, and adaptive conformal prediction [31] forms prediction sets in a data stream where the distribution varies over time in an unknown fashion by constantly re-estimating the conformal quantile. A weighted version of conformal prediction pioneered by [26] provides tools for addressing non-exchangeable data, most notably slowly changing time-series. This same work develops techniques for applying full conformal prediction to asymmetric algorithms. Beyond distribution shift, recent statistical extensions also address topics such as creating reliable conformal prediction intervals for counterfactuals and individual treatment effects [94][95][96], covariate-dependent lower bounds on survival times [97], prediction sets that preserve the privacy of the calibration data [98], handling dependent data [99][100][101], and achieving 'multivalid' coverage that is conditionally valid with respect to several possibly overlapping groups [102,103].

Furthermore, prediction sets are not the only important form of distribution-free uncertainty quantification. One alternative form is a conformal predictive distribution, which outputs a probability distribution over the response space Y in a regression problem [79]. Recent work also addresses the issue of calibrating a scalar notion of uncertainty to have probabilistic meaning via histogram binning [104,105]-this is like a rigorous version of Platt scaling or isotonic regression. The tools from conformal prediction can also be used to identify times when the distribution of data has changed by examining the score function's behavior on new data points. For example, [24] performs outlier detection using conformal prediction, [61,106] detect change points in time-series data, [107] tests for covariate shift between two datasets, and [108] tracks the risk of a predictor on a data-stream to identify when harmful changes in its distribution (one that increases the risk) occur.

Developing better estimators of uncertainty improves the practical effectiveness of conformal prediction. The literature on this topic is too wide to even begin discussing; instead, we point to quantile regression as an example of a fruitful line of work that mingled especially nicely with conformal prediction in Section 2.2. Quantile regression was first proposed in [9] and extended to the locally polynomial case in [109]. Under sufficient regularity, quantile regression converges uniformly to the true quantile function [109][110][111][112][113]. Practical and accessible references for quantile regression have been written by Koenker and collaborators [114,115].

Active work continues today to analyze the statistical properties of quantile regression and its variants under different conditions, for example in additive models [116] or to improve conditional coverage when the size of the intervals may correlate with miscoverage events [16]. The Handbook of Quantile Regression [115] includes more detail on such topics, and a memoir of quantile regression for the interested reader. Since quantile regression provides intervals with near-conditional coverage asymptotically, the conformalized version inherits this good behavior as well.

Along with such statistical advances has come a recent wave of practical applications of conformal prediction. Conformal prediction in large-scale deep learning was studied in [4], focusing on image classification.

One compelling use-case of conformal prediction is speeding up and decreasing the computational cost of the test-time evaluation of complex models [117,118]. The same researchers pooled information across multiple tasks in a meta-learning setup to form tight prediction sets for few-shot prediction [119]. There is also an earlier line of work, appearing slightly after that of Lei and Wasserman, applying conformal prediction to decision trees [120][121][122]. Closer to end-users, we are aware of several real applications of conformal prediction. The Washington Post estimated the number of outstanding Democratic and Republican votes in the 2020 United States presidential election using conformal prediction [123]. Early clinical experiments in hospitals underscore the utility of conformal prediction in that setting as well, although real deployments are still to come [124,125]. Fairness and reliability of algorithmic risk forecasts in the criminal justice system improves (on controlled datasets) when applying conformal prediction [125][126][127]. Conformal prediction was recently applied to create safe robotic planning algorithms that avoid bumping into objects [128,129]. Recently a scikit-learn compatible open-source library, MAPIE, has been developed for constructing conformal prediction intervals. There remains a mountain of future work in these applications of conformal prediction and many others.

Today, the field of distribution-free uncertainty quantification remains small, but grows rapidly year-onyear. The promulgation of machine learning deployments has caused a reckoning that point predictions are not enough and shown that we still need rigorous statistical inference for reliable decision-making. Many researchers around the world have keyed into this fact and have created new algorithms and software using distribution-free ideas like conformal prediction. These developments are numerous and high-quality, so most reviews are out-of-date. To keep track of what gets released, the reader may want to see the Awesome Conformal Prediction repository [130], which provides a frequently-updated list of resources in this area.

We will end our Gentle Introduction with a personal note to the reader-you can be part of this story too. The infant field of distribution-free uncertainty quantification has ample room for significant technical contributions. Furthermore, the concepts are practical and approachable; they can easily be understood and implemented in code. Thus, we encourage the reader to try their hand at distribution-free uncertainty quantification; there is a lot more to be done!

### A Distribution-Free Control of General Risks

For many prediction tasks, the relevant notion of reliability is not coverage. Indeed, many applications have problem-specific performance metrics-from false-discovery rate to fairness-that directly encode the soundness of a prediction. In Section 4.3, we saw how to control the expectation of monotone loss functions using conformal risk control. Here, we generalize further to control any risk and multiple risks in a distribution-free way without retraining the model. As an example, in instance segmentation, we are given an image and asked to identify all objects in the image, segment them, and classify them. All three of these sub-tasks have their own risks: recall, intersection-over-union (IOU), and coverage respectively. These risks can be automatically controlled using distribution-free statistics, as we preview in Figure 19.

We first re-introduce the theory of risk control below, then give a list of illustrative examples. As in conformal risk control, we start with a pretrained model f . The model also has a parameter λ, which we are free to choose. We use f (x) and λ to form our prediction, T λ (x), which may be a set or some other object. For example, when performing regression, λ could threshold the estimated probability density, as below.

We then define a notion of risk R(λ). The risk function measures the quality of T λ according to the user. The goal of risk control is to use our calibration set to pick a parameter λ so that the risk is small with high probability. In formal terms, for a user-defined risk tolerance α and error rate δ, we seek to ensure

P R λ < α ≥ 1 -δ,(17)

where the probability is taken over the calibration data used to pick λ. Note that this guarantee is highprobability, unlike that in Section 4.3, which is in expectation. We will soon introduce a distribution-free technique called Learn then Test (LTT) for finding λ that satisfy (17). Below we include two example applications of risk control which would be impossible with conformal prediction and conformal risk control.

• Multi-label Classification with FDR Control: In this setting, X test is an image and Y test is a subset of K classes contained in the image. Our model f gives us the probability each of the K classes is contained in the image. We will include a class in our estimate of y if fk > λ -i.e., the parameter λ thresholds the estimated probabilities. We seek to find the λs that guarantees our predicted set of labels is sufficiently reliable as measured by the false-discovery rate (FDR) risk R( λ).

• Simultaneous Guarantees on OOD Detection and Coverage: For each input X test with true class Y test , we want to decide if it is out-of-distribution. If so, we will flag it as such. Otherwise, we want to output a prediction set that contains the true class with 90% probability. In this case, we have two models: OOD(x), which tells us how OOD the input is, and f (x), which gives the estimated probability that the input comes from each of K classes. In this case, λ has two coordinates, and we also have two risks. The first coordinate λ 1 tells us where to threshold OOD(x) such that the fraction of false alarms R 1 is controlled. The second coordinate λ 2 tells us how many classes to include in the prediction set to control the miscoverage R 2 among points identified as in-distribution. We will find λs that control both R 1 ( λ) and R 2 ( λ) jointly.

We will describe each of these examples in detail in Section B. Many more worked examples, including the object detection example in Figure 19, are available in the cited literature on risk control [18,131]. First, however, we will introduce the general method of risk control via Learn then Test.

### A.1 Instructions for Learn then Test

First, we will describe the formal setting of risk control. We introduce notation and the risk-control property in Definition 2. Then, we describe the calibration algorithm.

### Formal notation for error control

Let (X i , Y i ) i=1,...,n be an independent and identically distributed (i.i.d.) set of variables, where the features X i take values in X and the responses Y i take values in Y. The researcher starts with a pre-trained predictive model f . We show how to subsequently create predictors from f that control a risk, regardless of the quality of the initial model fit or the distribution of the data.

Next, let T λ : X → Y be a function with parameter λ that maps a feature to a prediction (Y can be any space, including the space of responses Y or prediction sets 2 Y ). This function T λ would typically be constructed from the predictive model, f , as in our earlier regression example. We further assume λ takes values in a (possibly multidimensional) discrete set Λ. If Λ is not naturally discrete, we usually discretize it finely. For example, Λ could be the set {0, 0.001, 0.002, ..., 0.999, 1}.

We then allow the user to choose a risk for the predictor T λ . This risk can be any function of T λ , but often we take the risk function to be the expected value of a loss function,

R(T λ ) = E   L T λ (X test ), Y test Loss function   .(18)

The loss function is a deterministic function that is high when T λ (X test ) does badly at predicting Y test . The risk then averages this loss over the distribution of (X test , Y test ). For example, taking

R miscoverage T λ ) = E 1 {Y test / ∈ T λ (X test )} = P (Y test / ∈ T λ (X test ))

gives us the familiar case of controlling miscoverage.

To aid the reader, we point out some facts about (18) that may not be obvious. The input T λ to the risk is a function; this makes the risk a functional (a function of a function). When we plug T λ into the risk, we take an expectation of the loss over the randomness in a single test point. At the end of the process, for a deterministic λ, we get a deterministic scalar R(T λ ). Henceforth, for ease of notation, we abbreviate this number as R(λ) := R(T λ ).

Our goal is control the risk in the following sense: Definition 2 (Risk control). Let λ be a random variable taking values in Λ (i.e., the output of an algorithm run on the calibration data). We say that T λ is a (α, δ)-risk-controlling prediction (RCP) if, with probability at least 1 -δ, we have R λ ≤ α.

In Definition 2, we plug in a random parameter λ which is chosen based on our calibration data; therefore, R( λ) is random even though the risk is a deterministic function. The high-probability portion of Definition 2 therefore says that λ can only violate risk control if we choose a bad calibration set; this happens with probability at most δ. The distribution of the risk over many resamplings of the calibration data should therefore look as below. Recalling Definition 2, our goal is to find a set function whose risk is less than some user-specified threshold α. To do this, we search across the collection of functions {T λ } λ∈Λ and estimate their risk on the calibration data (X 1 , Y 1 ), . . . , (X n , Y n ). The output of the procedure will be a set of λ values which are all guaranteed to control the risk, Λ ⊆ Λ. The Learn then Test procedure is outlined below.

1. For each λ ∈ Λ, associate the null hypothesis H λ : R(λ) > α. Notice that rejecting the H λ means you selected λ as a point where the risk is controlled. Here we denote each null with a blue dot; the yellow dot is highlighted, so we can keep track of it as we explain the procedure. 3. Return Λ = A {p λ } λ∈Λ , where A is an algorithm that controls the familywise-error rate (FWER).

For example, the Bonferroni correction yields Λ = λ : p λ < δ |Λ| . We define the FWER and preview ways to design good FWER-controlling procedures in Section A.1.2. The nulls with red crosses through them below have been rejected by the procedure; i.e., they all control the risk with high probability. 0.0 0.5 1.0

By following the above procedure, we get the statistical guarantee in Theorem A.1.

Theorem A.1. The Λ returned by the Learn then Test procedure satisfies

P sup λ∈ Λ {R( λ)} ≤ α ≥ 1 -δ.

Thus, selecting any λ ∈ Λ, T λ is an (α, δ)-RCP.

The LTT procedure decomposes risk control into two subproblems: computing p-values and combining them with multiple testing. We will now take a closer look at each of these subproblems.

### A.1.1 Crash Course on Generating p-values

What is a p-value, and why is it related to risk control? In Step 1 of the LTT procedure, we associated a null hypothesis H λ to every λ ∈ Λ. When the null hypothesis at λ holds, the risk is not controlled for that value of the parameter. In this reframing, our task is to automatically identify points λ where the null hypothesis does not hold-i.e., to reject the null hypotheses for some subset of λ such that R(λ) ≤ α. The process of accepting or rejecting a null hypothesis is called hypothesis testing.

Rejecting the null hypothesis H λ → the risk is controlled at λ.

Accepting the null hypothesis H λ → the risk is not controlled at λ.

In order to reject a null hypothesis, we need to have empirical evidence that at λ, the risk is controlled. We use our calibration data to summarize this information in the form of a p-value p λ . A p-value must satisfy the following condition, which we sometimes refer to as validity or super-uniformity, ∀t ∈ [0, 1], P H λ (p λ ≤ t) ≤ t,

super-uniform p-valueOne of the key ingredients in Learn then Test is a p-value with distribution-free validity: it is valid under without assumptions on the data distribution. For example, when working with risk functions that take values in [0, 1]-like coverage, IOU, FDR, and so on-the easiest choice of p-value is based on Hoeffding's inequality:p Hoeffding λ = e -2n α-R(λ) 2 + .More powerful p-values based on tighter concentration bounds are included in[18]. In particular, many of the practical examples in that reference use a stronger p-value called the Hoeffding-Bentkus (HB) p-value,p HB λ = min exp{-nh 1 ( R(λ) ∧ α, α)}, eP Bin(n, α) ≤ n R(λ) ,where h 1 (a, b) = a log a b + (1 -a) log 1 -a 1 -b .

where P H λ refers to the probability under the null hypothesis. Parsing the super-uniformity condition carefully tells us that when p λ is low, there is evidence against the null hypothesis H λ . In other words, for a particular λ, we can reject H λ if p λ < 5% and expect to be wrong no more than 5% of the time. This process is called testing the hypothesis at level δ, where in the previous sentence, δ = 5%. Note that any valid p-value will work-it is fine for the reader to keep p Hoeffding λ in mind for the rest of this manuscript, with the understanding that more powerful choices are available.

### A.1.2 Crash Course on Familywise-Error Rate Algorithms

If we only had one hypothesis H λ , we could simply test it at level δ. However, we have one hypothesis for each λ ∈ Λ, where |Λ| is often very large (in the millions or more). This causes a problem: the more hypotheses we test, the higher chance we incorrectly reject at least one hypothesis. We can formally reason about this with the familywise-error rate (FWER).

Definition 3 (familywise-error rate). The familywise-error rate of a procedure returning Λ is the probability of making at least one false rejection, i.e., FWER Λ = P ∃ λ ∈ Λ : R( λ) > α .

As a simple example to show how naively thresholding the p-values at level δ fails to control FWER, consider the case where all the hypotheses are null, and we have uniform p-values independently tested at level δ. The FWER then approaches 1; see below. This simple toy analysis exposes a deeper problem: without an intelligent strategy for combining the information from many p-values together, we can end up making false rejections with high probability. Our challenge is to intelligently combine the p-values to avoid this issue of multiplicity (without assuming the p-values are independent). This fundamental statistical challenge has led to a decades-long and continually rich area of research called multiple hypothesis testing. In particular, a genre of algorithms called FWER-controlling algorithms seek to select the largest set of Λ that guarantees FWER( Λ) ≤ δ. The simplest FWER-controlling algorithm is the Bonferroni correction,

Λ Bonferroni = λ ∈ Λ : p λ ≤ δ |Λ| .

Under the hood, the Bonferroni correction simply tests each hypothesis at level δ/|Λ|, so the probability there exists a failed test is no more than δ by a union bound. It should not be surprising that there exist improvements on Bonferroni correction. First, we will discuss one important improvement in the case of a monotone loss function: fixed-sequence testing. As the name suggests, in fixed-sequence testing, we construct a sequence of hypotheses {H λj } N j=1 where N = |Λ|, before looking at our calibration data. Usually, we just sort our hypotheses from most-to least-promising based on information we knew a-priori. For example, if large values of λ are more likely to control the risk, {λ j } N j=1 just sorts Λ from greatest to least. Then, we test the hypotheses sequentially in some fixed order at level δ, including them in Λ as we go, and stopping when we make our first acceptance: Λ FST = {λ j , j ≤ T }, where T = max t ∈ {1, ..., N } : p λ t ≤ δ, for all t ≤ t . This sequential procedure, despite testing all hypotheses it encounters at level δ, still controls the FWER. For monotone and near-monotone risks, such as the false-discovery rate, it works quite well.

It is also possible to extend the basic idea of fixed-sequence testing to non-monotone functions, creating powerful and flexible FWER-controlling procedures using an idea called sequential graphical testing [132]. Good graphical FWER-controlling procedures can be designed to have high power for particular problems, or alternatively, automatically discovered using data. This topic is given a detailed treatment in [18], and we omit it here for simplicity.

We have described a general-purpose pipeline for distribution-free risk control. It is described in PyTorch code in Figure 20. Once the user sets up the problem (i.e., picks Λ, T λ , and R), the LTT pipeline we described above automatically produces Λ. We now go through three worked examples which teach the reader how to choose Λ, T and R in practical circumstances.

### B Examples of Distribution-Free Risk Control

In this section, we will walk through several examples of distribution-free risk control applied to practical machine learning problems. The goal is again to arm the reader with an arsenal of pragmatic prototypes of distribution-free risk control that work on real problems.

1. Flag out-of-distribution (OOD) inputs without too many false flags.

2. If an input is deemed in-distribution (In-D), output a prediction set that contains the true class with high probability.

Part of the purpose of this example is to teach the reader how to deal with multiple risk functions (one of which is a conditional risk) and a multi-dimensional parameter λ.

Our setup requires two different models. The first, OOD(x), outputs a scalar that should be larger when the input is OOD. The second, f (x) y , estimates the probability that input x is of class y; for example, f (x) could represent the softmax outputs of a neural net. Similarly, the construction of T λ (x) has two substeps, each of which uses a different model. In our first substep, when OOD(x) becomes sufficiently large, exceeding λ 1 , we flag the example as OOD by outputting ∅. Otherwise, we essentially use the APS method from Section 2.1 to form prediction sets. We precisely describe this procedure below:

T λ (x) =

∅ OOD(x) > λ 1 {π 1 (x), ..., π K (x)} else, where K = inf{k : k j=1 f (x) πj (x) > λ 2 } and π(x) sorts f (x) from greatest to least. We usually take Λ = {0, 1/N, 2/N, ..., 1} 2 , i.e., we discretize the box [0, 1] × [0, 1] into N 2 smaller boxes, with N ≈ 1000. The intuition of T λ (x) is very simple. If the example is sufficiently atypical, we give up. Otherwise, we create a prediction set using a procedure similar to (but not identical to) conformal prediction. The first risk function R 1 is the probability of a false flag, and the second risk function R 2 is the coverage conditionally on being deemed in-distribution. The user must define risk-tolerances for each, so α is a twovector, where α 1 determines the desired fraction of false flags and α 2 determines the desired miscoverage rate. Setting α = (0.05, 0.1) will guarantee that we falsely throw out no more than 5% of in-distribution data points, and also that among the data points we claim are in-distribution, we will output a prediction set containing the correct class with 90% probability. In order to control both risks, we now need to associate a composite null hypothesis to each λ ∈ Λ. Namely, we choose

H λ : H(1)

λ or H

λ ,

where H λ is the union of two intermediate null hypotheses, H

λ : R 1 (λ) > α 1 and H

ve never seen anything like this before!" "I'm 90% certain this is a squirrel or a chipmunk."Along the same lines, we control two risk functions simultaneously,R 1 (λ) = P (T λ (X test ) = ∅) and R 2 (λ) = P Y test / ∈ T λ (X test ) T λ (X test ) = ∅ .

λ : R 2 (λ) > α 2 .

We summarize our setup in the below table.

## Figures et tableaux

**Figure 1:** Prediction set examples on Imagenet. We show three progressively more difficult examples of the class fox squirrel and the prediction sets (i.e., C(X test )) generated by conformal prediction.

**Figure 2:** Illustration of conformal prediction with matching Python code.

**Figure 3:** Python code for adaptive prediction sets.

**Figure 4:** A visualization of the adaptive prediction sets algorithm in Eq. (3). Classes are included from most to least likely until their cumulative softmax output exceeds the quantile.

**Figure 5:** Python code for conformalized quantile regression.

**Figure 7:** Python code for conformalized uncertainty scalars.

**Figure 9:** A visualization of the conformalized Bayes algorithm in Eq. (6). The prediction set is a superlevel set of the posterior predictive density.

**Figure 10:** Figure10: Prediction sets with various notions of coverage: no coverage, marginal coverage, or conditional coverage (at a level of 90%). In the marginal case, all the errors happen in the same groups and regions in X-space. Conditional coverage disallows this behavior, and errors are evenly distributed.

**Figure 13:** Examples of false negative rate control in multilabel classification on the MS COCO dataset with α = 0.1. False negatives are red, false positives are blue, and true positives are black.

[figure sans légende identifiée] More formally, our calibration set {(X i , Y i )} n i=1 contains exchangeable images X i and sets of classes Y i ⊆ {1, ..., K}. With the notation of Section 4.3, we set our loss function to be FNR (C λ (x), y) = 1-|C λ (x)∩y|/|y|. Then, picking λ as in 12 yields a bound on the false negative rate, E FNR C λ(X test ), Y test ≤ α.

**Figure 13** Figure13gives results and code for FNR control on the Microsoft Common Objects in Context dataset[28].

**Figure 14:** Examples of false negative rate control in tumor segmentation with α = 0.1. False negatives are red, false positives are blue, and true positives are black.

**Figure 15:** Figure15: Conformal prediction for time-series temperature estimation with α = 0.1. On the left is a plot of coverage over time; 'weighted' denotes the procedure in Section 5.3 while 'unweighted' denotes the procedure that simply computes the conformal quantile on all conformal scores seen so far. Note that we compute coverage using a sliding window of 500 points, which explains some of the variability in the coverage. Running the notebook with a trailing average of 5000 points reveals that the unweighted version systematically undercovers before the change-point as well. On the right is a plot showing the intervals resulting from the weighted procedure.

**Figure 16:** Examples of toxic online comment identification with type-1 error control at level α = 0.1 on the Jigsaw Multilingual Toxic Comment Classification dataset.

**Figure 17:** Results using selective classification on Imagenet with α = 0.1.

Yn+1 n+1 is exchangeable with s Yn+1 1 ,

**Figure 18:** Pages from the 1976 edition of Kvant magazine.

**Figure 19:** Object detection with simultaneous distribution-free guarantees on the expected intersection-over-union, recall, and coverage rate.

2. For each null hypothesis, compute a p-value using a concentration inequality. For example, Hoeffding'sinequality yields p λ = e -2n(α-R(λ)) 2 + , where R(λ) = 1 n n i=1 L(T λ (X i ), Y i ).We remind the reader what a p-value is, why it is relevant to risk control, and point to references with stronger p-values in A.1.1.

# Implementation of LTT. Assume access to X, Y where n=X.shape[0]=Y.shape[0] lambdas = torch.linspace(0,1,N) # Commonly choose N=1000 losses = torch.zeros((n,N)) # Compute the loss function next for (i,j) in [(i,j) for i in range(n) for j in range(N)]: prediction_set = T(X[i],lambdas[j]) # T ( ) is problem depemdent losses[i,j] = get_loss(prediction_set,Y[i]) # Loss is problem dependent risk = losses.mean(dim=0) pvals = torch.exp(-2*n*(torch.relu(alpha-risk)**2)) # Or any p-value lambda_hat = lambdas[pvals<delta/lambdas.shape[0]] # Or any FWER-controlling algorithm

**Figure 20:** PyTorch code for running Learn then Test.

[figure sans légende identifiée] If we take Λ = {λ : p λ < δ}, then FWER( Λ) = 1 -(1 -δ) |Λ| .

**Figure 22:** Examples of multi-label classification with FDR control on the MS-COCO dataset. Black classes are true positives, blue classes are spurious, and red classes are missed. The FDR is controlled at level α = 0.1, δ = 0.1.

λ 1 λ 2 λ 3 λ 4 λ 5 λ 6 λ 7 λ 8 λ 9 λ 10 Figure 21: Figure 21: An example of fixed-sequence testing with δ = 0.05. Each blue circle represents a null, and each row a step of the procedure. The nulls with a red cross have been rejected at that step.

[figure sans légende identifiée] , no matter what (possibly incorrect) model is used or what the (unknown) distribution of the data is.

    true class (1) compute scores softmax output # on holdout data | (2) get quantile (3) construct prediction set softmax output | # 1: get conformal scores. n = calib_Y.shape[0] cal_smx = model(calib_X).softmax(dim=1).numpy() cal_scores = 1-cal_smx[np.arange(n),cal_labels] # 2: get adjusted quantile q_level = np.ceil((n+1)*(1-alpha))/n
    class | scores, | class

[figure sans légende identifiée] for a visualization of the difference between conditional and marginal coverage.

    group | no coverage Group 1 Group 2 | Group 1 marginal Group 2 | Group 1 conditional Group 2 correctly covered example incorrectly covered example
    by |  |  |  | 
    errors | 5% coverage | 14% coverage | 100% coverage 80% coverage | 90% coverage 90% coverage
    regression |  |  |  | 

table.

     | Distribution of coverage (infinite validation set) | 
     |  |  |  |  |  |  | n=100 n=1000 n=10000 1
    0.82 | 0.84 | 0.86 | 0.88 | 0.90 | 0.92 | 0.94 | 0.96 | 0.98
     |  | 0.1 0.05 0.01 0.005 | 0.001 |  | 
     | n( ) 22 102 2491 9812 244390 | 
    Table |  |  |  |  |  |  |  | 

**Figure12:** Python code for computing coverage with efficient score caching. Notice that from the expression for conformal sets in (2), a validation point is covered if and only if s(X, Y ) ≤ q, which is how the third to last line is succinctly computing the coverage.if it is benign. Code for checking the coverage at all different values of n, n val , and R is available in the accompanying Jupyter notebook of Figure12.

    try: # try loading the scores first
    scores = np.load('scores.npy')
    except:
    # X and Y have n + n_val rows each
    scores = get_scores(X,Y)
    np.save(scores, 'scores.npy')
    # calculate the coverage R times and store in list
    coverages = np.zeros((R,))
    for r in range(R):
    np.random.shuffle(scores) # shuffle
    calib_scores, val_scores = (scores[:n],scores[n:]) # split
    qhat = np.quantile(calib_scores, np.ceil((n+1)*(1-alpha)/n), method='higher') # calibrate
    coverages[r] = (val_scores <= qhat).astype(float).mean() # see caption
    average_coverage = coverages.mean() # should be close to 1-alpha
    plt.hist(coverages) # should be roughly centered at 1-alpha
