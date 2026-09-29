---
id: arxiv-1606.09282-learning-without-forgetting
title: "Learning Without Forgetting"
year: 2018
backend: grobid
---

## Abstract

When building a unified vision system or gradually adding new capabilities to a system, the usual assumption is that training data for all tasks is always available. However, as the number of tasks grows, storing and retraining on such data becomes infeasible. A new problem arises where we add new capabilities to a Convolutional Neural Network (CNN), but the training data for its existing capabilities are unavailable. We propose our Learning without Forgetting method, which uses only new task data to train the network while preserving the original capabilities. Our method performs favorably compared to commonly used feature extraction and fine-tuning adaption techniques and performs similarly to multitask learning that uses original task data we assume unavailable. A more surprising observation is that Learning without Forgetting may be able to replace fine-tuning with similar old and new task datasets for improved new task performance.

## 1. INTRODUCTION

M ANY practical vision applications require learning new visual capabilities while maintaining performance on existing ones. For example, a robot may be delivered to someone's house with a set of default object recognition capabilities, but new site-specific object models need to be added. Or for construction safety, a system can identify whether a worker is wearing a safety vest or hard hat, but a superintendent may wish to add the ability to detect improper footware. Ideally, the new tasks could be learned while sharing parameters from old ones, without suffering from Catastrophic Forgetting [1], [2] (degrading performance on old tasks) or having access to the old training data. Legacy data may be unrecorded, proprietary, or simply too cumbersome to use in training a new task. This problem is similar in spirit to transfer, multitask, and lifelong learning.

We aim at developing a simple but effective strategy on a variety of image classification problems with Convolutional Neural Network (CNN) classifiers. In our setting, a CNN has a set of shared parameters θ s (e.g., five convolutional layers and two fully connected layers for AlexNet [3] architecture), task-specific parameters for previously learned tasks θ o (e.g., the output layer for ImageNet [4] classification and corresponding weights), and randomly initialized taskspecific parameters for new tasks θ n (e.g., scene classifiers). It is useful to think of θ o and θ n as classifiers that operate on features parameterized by θ s . Currently, there are three common approaches (Figures 1,2) to learning θ n while benefiting from previously learned θ s :

Feature Extraction (e.g., [5]): θ s and θ o are unchanged, and the outputs of one or more layers are used as features for the new task in training θ n .

Fine-tuning (e.g., [6]): θ s and θ n are optimized for the new task, while θ o is fixed. A low learning rate is typically used to prevent large drift in θ s . Potentially, the original network could be duplicated and fine-tuned for each new task to create a set of specialized networks.

It is also possible to use a variation of fine-tuning where part of θ s -the convolutional layers -are frozen to prevent overfitting, and only top fully connected layers are finetuned. This can be seen as a compromise between finetuning and feature extraction. In this work we call this method Fine-tuning FC where FC stands for fully connected.

Joint Training (e.g., [7]): All parameters θ s , θ o , θ n are jointly optimized, for example by interleaving samples from each task. This method's performance may be seen as an upper bound of what our proposed method can achieve.

Each of these strategies has a major drawback. Feature extraction typically underperforms on the new task because the shared parameters fail to represent some information that is discriminative for the new task. Fine-tuning degrades performance on previously learned tasks because the shared parameters change without new guidance for the original task-specific prediction parameters. Duplicating and finetuning for each task results in linearly increasing test time as new tasks are added, rather than sharing computation for shared parameters. Fine-tuning FC, as we show in our experiments, still degrades performance on the new task. Joint training becomes increasingly cumbersome in training as more tasks are learned and is not possible if the training data for previously learned tasks is unavailable.

Besides these commonly used approaches, methods [8], [9] have emerged that can continually add new prediction tasks by adapting shared parameters without access to training data for previously learned tasks. (See Section 2) In this paper, we expand on our previous work [10], Learning without Forgetting (LwF). Using only examples for the new task, we optimize both for high accuracy for the new task and for preservation of responses on the existing tasks from the original network. Our method is similar to joint training, except that our method does not need the old task's images and labels. Clearly, if the network is preserved such that θ o produces exactly the same outputs on all relevant images, the old task accuracy will be the Fig. 1. We wish to add new prediction tasks to an existing CNN vision system without requiring access to the training data for existing tasks. This table shows relative advantages of our method compared to commonly used methods.

### Fine

Duplicating Compared to our previous work [10], we conduct more extensive experiments. We compare to additional methods -fine-tune FC, a commonly used baseline, and Less Forgetting Learning, a recently proposed method. We experiment on adjusting the balance between old-new task losses, providing a more thorough and intuitive comparison of related methods (Figure 7). We switch from the obsolete Places2 to a newer Places365-standard dataset. We perform stricter, more careful hyperparameter selection process, which slightly changed our results. We also include more detailed explanation of our method. Finally, we perform an experiment on application to video object tracking in Appendix A.

## 2. RELATED WORK

Multi-task learning, transfer learning, and related methods have a long history. In brief, our Learning without Forgetting approach could be seen as a combination of Distillation Networks [11] and fine-tuning [6]. Fine-tuning initializes with parameters from an existing network trained on a related data-rich problem and finds a new local minimum by optimizing parameters for a new task with a low learning rate. The idea of Distillation Networks is to learn parameters in a simpler network that produce the same outputs as a more complex ensemble of networks either on the original training set or a large unlabeled set of data. Our approach differs in that we solve for a set of parameters that works well on both old and new tasks using the same data to supervise learning of the new tasks and to provide unsupervised output guidance on the old tasks.

### 2.1. Compared methods

Feature Extraction [5], [12] uses a pre-trained deep CNN to compute features for an image. The extracted features are the activations of one layer (usually the last hidden layer) or multiple layers given the image. Classifiers trained on these features can achieve competitive results, sometimes outperforming human-engineered features [5]. Further studies [13] show how hyper-parameters, e.g. original network structure, should be selected for better performance. Feature extraction does not modify the original network and allows new tasks to benefit from complex features learned from previous tasks. However, these features are not specialized for the new task and can often be improved by fine-tuning.

Fine-tuning [6] modifies the parameters of an existing CNN to train a new task. The output layer is extended with randomly intialized weights for the new task, and a small learning rate is used to tune all parameters from their original values to minimize the loss on the new task. Sometimes, part of the network is frozen (e.g. the convolutional layers) to prevent overfitting. Using appropriate hyper-parameters for training, the resulting model often outperforms feature extraction [6], [13] or learning from a randomly initialized network [14], [15]. Fine-tuning adapts the shared parameters θ s to make them more discriminative for the new task, and the low learning rate is an indirect mechanism to preserve some of the representational structure learned in the original tasks. Our method provides a more direct way to preserve representations that are important for the original task, improving both original and new task performance relative to fine-tuning in most experiments.

Multitask learning (e.g., [7]) aims to improve all tasks simultaneously by combining the common knowledge from all tasks. Each task provides extra training data for the parameters that are shared or constrained, serving as a form of regularization for the other tasks [16]. For neural networks, Caruana [7] gives a detailed study of multi-task learning. Usually the bottom layers of the network are shared, while the top layers are task-specific. Multitask learning requires data from all tasks to be present, while our method requires only data for the new tasks.

Adding new nodes to each network layer is a way to preserve the original network parameters while learning new discriminative features. For example, al. [17] propose Deep Block-Modular Neural Networks for fully-connected neural networks, and Rusu et al. [18] propose Progressive Neural Networks for reinforcement learning. Parameters for the original network are untouched, and newly added nodes are fully connected to the layer beneath them. These methods has the downside of substantially expanding the number of parameters in the network, and can underperform [17] both fine-tuning and feature extraction if insufficient training data is available to learn the new parameters, since they require a substantial number of parameters to be trained from scratch. We experiment with expanding the fully connected layers of original network but find that the expansion does not provide an improvement on our original approach.

### 2.2. Topically relevant methods

Our work also relates to methods that transfer knowledge between networks. Hinton et al. [11] propose Knowledge Distillation, where knowledge is transferred from a large network or a network assembly to a smaller network for efficient deployment. The smaller network is trained using a modified cross-entropy loss (further described in Sec. 3) that encourages both large and small responses of the original and new network to be similar. Romero et al. [19] builds on this work to transfer to a deeper network by applying extra guidance on the middle layer. Chen et al. [20] proposes the Net2Net method that immediately generates a deeper, wider network that is functionally equivalent to an existing one. This technique can quickly initialize networks for faster hyper-parameter exploration. These methods aim to produce a differently structured network that approximates the original network, while we aim to find new parameters for the original network structure (θ s , θ o ) that approximate the original outputs while tuning shared parameters θ s for new tasks. Feature extraction and fine-tuning are special cases of Domain Adaptation (when old and new tasks are the same) or Transfer Learning (different tasks). These are different from multitask learning in that tasks are not simultaneously optimized. Transfer Learning uses knowledge from one task to help another, as surveyed by Pan et al. [21]. The Deep Adaption Network by Long et al. [22] matches the RKHS embedding of the deep representation of both source and target tasks to reduce domain bias. Another similar domain adaptation method is by Tzeng et al. [23], which encourages the shared deep representation to be indistinguishable across domains. This method also uses knowledge distillation, but to help train the new domain instead of preserving the old task. Domain adaptation and transfer learning require that at least unlabeled data is present for both task domains. In contrast, we are interested in the case when training data for the original tasks (i.e. source domains) are not available.

Methods that integrate knowledge over time, e.g. Lifelong Learning [24] and Never Ending Learning [25], are also related. Lifelong learning focuses on flexibly adding new tasks while transferring knowledge between tasks. Never Ending Learning focuses on building diverse knowledge and experience (e.g. by reading the web every day). Though topically related to our work, these methods do not provide a way to preserve performance on existing tasks without the original training data. Ruvolo et al. [26] describe a method to efficiently add new tasks to a multitask system, cotraining all tasks while using only new task data. However, the method assumes that weights for all classifiers and regression models can be linearly decomposed into a set of bases. In contrast with our method, the algorithm applies only to logistic or linear regression on engineered features, and these features cannot be made task-specific, e.g. by finetuning.

### 2.3. Concurrently developed methods

Concurrent with our previous work [10], two methods have been proposed for continually add and integrate new tasks without using previous tasks' data.

A-LTM [8], developed independently, is nearly identical in method but has very different experiments and conclusions. The main differences of method are in the weight decay regularization used for training and the warm-up step that we use prior to full fine-tuning.

However, we use large datasets to train our initial network (e.g. ImageNet) and then extend to new tasks from smaller datasets (e.g. PASCAL VOC), while A-LTM uses small datasets for the old task and large datasets for the new task. The experiments in A-LTM [8] find much larger loss due to fine-tuning than we do, and the paper concludes that maintaining the data from the original task is necessary to maintain performance. Our experiments, in contrast, show that we can maintain good performance for the old task while performing as well or sometimes better than finetuning for the new task, without access to original task data. We believe the main difference is the choice of old-task new-task pairs and that we observe less of a drop in oldtask performance from fine-tuning due to the choice (and in part to the warm-up step; see Table 2(b)). We believe that our experiments, which start from a well-trained network and add tasks with less training data available, are better motivated from a practical perspective.

Less Forgetting Learning [9] is also a similar method, which preserves the old task performance by discouraging the shared representation to change. This method argues that the task-specific decision boundaries should not change, and keeps the old task's final layer unchanged, while our method discourages the old task output to change, and jointly optimizes both the shared representation and the final layer. We empirically show that our method outperforms Less Forgetting Learning on the new task.

## 3. LEARNING WITHOUT FORGETTING

Given a CNN with shared parameters θ s and task-specific parameters θ o (Fig. 2(a)), our goal is to add task-specific parameters θ n for a new task and to learn parameters that work well on old and new tasks, using images and labels from only the new task (i.e., without using data from existing tasks). Our algorithm is outlined in Fig. 3, and the network structure illustrated in Fig. 2(e).

First, we record responses y o on each new task image from the original network for outputs on the old tasks (defined by θ s and θ o ). Our experiments involve classification, so the responses are the set of label probabilities for each training image. Nodes for each new class are added to the output layer, fully connected to the layer beneath, with randomly initialized weights θ n . The number of new parameters is equal to the number of new classes times the number of nodes in the last shared layer, typically a very small percent of the total number of parameters. In our experiments (Sec. 4.2), we also compare alternate ways of modifying the network for the new task.

Next, we train the network to minimize loss for all tasks and regularization R using stochastic gradient descent. The regularization R corresponds to a simple weight decay of 0.0005. When training, we first freeze θ s and θ o and train θ n to convergence (warm-up step). Then, we jointly train all weights θ s , θ o , and θ n until convergence (joint-optimize step). The warm-up step greatly enhances fine-tuning's oldtask performance, but is not so crucial to either our method or the compared Less Forgetting Learning (see Table 2(b)). We still adopt this technique in Learning without Forgetting (as well as most compared methods) for the slight enhancement and a fair comparison.

For simplicity, we denote the loss functions, outputs, and ground truth for single examples. The total loss is averaged over all images in a batch in training. For new tasks, the loss encourages predictions ŷn to be consistent with the ground truth y n . The tasks in our experiments are multiclass classification, so we use the common [3], [27] multinomial logistic loss:

L new (y n , ŷn ) = -y n • log ŷn (1)

where ŷn is the softmax output of the network and y n is the one-hot ground truth label vector. If there are multiple new tasks, or if the task is multi-label classification where we make true/false predictions for each label, we take the sum of losses across the new tasks and the labels.

For each original task, we want the output probabilities for each image to be close to the recorded output from the original network. We use the Knowledge Distillation loss, which was found by Hinton et al. [11] to work well for encouraging the outputs of one network to approximate the outputs of another. This is a modified cross-entropy loss that increases the weight for smaller probabilities:

L old (y o , ŷo ) = -H(y o , ŷ o ) (2) = - l i=1 y (i) o log ŷ (i) o (3

)

where l is the number of labels and y

(i) o , ŷ (i) o

are the modified versions of recorded and current probabilities y

(i) o , ŷ(i) o : y (i) o = (y (i) o ) 1/T j (y (j) o ) 1/T , ŷ (i) o = (ŷ (i) o ) 1/T j (ŷ (j) o ) 1/T . (4

)

If there are multiple old tasks, or if an old task is multi-label classification, we take the sum of the loss for each old task and label. Hinton et al. [11] suggest that setting T > out set, which aligns with the authors' recommendations.

In experiments, use of knowledge distillation loss leads to a slightly better but very similar performance to other reasonable losses. Therefore, it is important to constrain outputs for original tasks to be similar to the original network, but the similarity measure is not crucial.

λ o is a loss balance weight, set to 1 for most our experiments. Making λ larger will favor the old task performance over the new task's, so we can obtain a old-task-new-task performance line by changing λ o . (Figure 7)

Relationship to joint training. As mentioned before, the main difference between joint training and our method is the need for the old dataset. Joint training uses the old task's images and labels in training, while Learning without Forgetting no longer uses them, and instead uses the new task images X n and the recorded responses Y o as substitutes. This eliminates the need to require and store the old dataset, brings us the benefit of joint optimization of the shared θ s , and also saves computation since the images X n only has to pass through the shared layers once for both the new task and the old task. However, the distribution of images from these tasks may be very different, and this substitution may potentially decrease performance. Therefore, joint training's performance may be seen as an upper-bound for our method.

Efficiency comparison. The most computationally expensive part of using the neural network is evaluating or backpropagating through the shared parameters θ s , especially the convolutional layers. For training, feature extraction is the fastest because only the new task parameters are tuned. LwF is slightly slower than fine-tuning because it needs to back-propagate through θ o for old tasks but needs to evaluate and back-propagate through θ s only once. Joint training is the slowest, because different images are used for different tasks, and each task requires separate backpropagation through the shared parameters.

All methods take approximately the same amount of time to evaluate a test image. However, duplicating the network and fine-tuning for each task takes m times as long to evaluate, where m is the total number of tasks.

### 3.1. Implementation details

We use MatConvNet [28] to train our networks using stochastic gradient descent with momentum of 0.9 and dropout enabled in the fully connected layers. The data normalization (mean subtraction) of the original task is used for the new task. The resizing follows the implementation of the original network, which is 256 × 256 for AlexNet and 256 pixels in the shortest edge with aspect ratio preserved for VGG. We randomly jitter the training data by taking random fixed-size crops of the resized images with offset on a 5 × 5 grid, randomly mirroring the crop, and adding variance to the RGB values like in AlexNet [3]. This data augmentation is applied to feature extraction too.

When training networks, we follow the standard practices for fine-tuning existing networks. For random initialization of θ n , we use Xavier [29] initialization. We use a learning rate much smaller than when training the original network (0.1 ∼ 0.02 times the original rate). The learning rates are selected to maximize new task performance with a reasonable number of epochs. For each scenario, the same learning rate are shared by all methods except feature extraction, which uses 5× the learning rate due to its small number of parameters.

We choose the number of epochs for both the warmup step and the joint-optimize step based on validation on the held-out set. We look at only the new task performance during validation. Therefore our selected hyperparameter favors the new task more. The compared methods converge at similar speeds, so we used the same number of epochs for each method for fair comparison; however, the convergence speed heavily depend on the original network and the task pair, and we validate for the number of epoch separately for each scenario. We perform stricter validation than in our previous work [10], and the number of epochs is generally longer for each scenario. One exception is ImageNet→Scene where we observe overfitting and have to shorten the training for feature extraction. We lower the learning rate once by 10× at the epoch when the held out accuracy plateaus.

To make a fair comparison, the intermediate network trained using our method (after the warm-up step) is used as a starting point for joint training and Fine Tuning, since this may speed up training convergence. In other words, for each run of our experiment, we first freeze θ s , θ o and train θ n , and use the resulting parameters to initialize our method, joint training and fine-tuning. Feature extraction is trained separately because does not share the same network structure as our method.

For the feature extraction baseline, instead of extracting features at the last hidden layer of the original network (at the top of θ s ), we freeze the shared parameters θ s , disable the dropout layers, and add a two-layer network with 4096 nodes in the hidden layer on top of it. This has the same effect of training a 2-layer network on the extracted features. For joint training, loss for one task's output nodes is applied to only its own training images. The same number of images are subsampled for every task in each epoch to balance their loss, and we interleave batches of different tasks for gradient descent.

## 4. EXPERIMENTS

Our experiments are designed to evaluate whether Learning without Forgetting (LwF) is an effective method to learn a new task while preserving performance on old tasks. We compare to common approaches of feature extraction, finetuning, and fine-tuning FC, and also Less Forgetting Learning (LFL) [9]. These methods leverage an existing network for a new task without requiring training data for the original tasks. Feature extraction maintains the exact performance on the original task. We also compare to joint training (sometimes called multitask learning) as an upper-bound on possible old task performance, since joint training uses images and labels for original and new tasks, while LwF uses only images and labels for the new tasks.

We experiment on a variety of image classification problems with varying degrees of inter-task similarity. For the original ("old") task, we consider the ILSVRC 2012 subset of ImageNet [4] and the Places365-standard [30] dataset. Note that our previous work used Places2, a taster challenge in ILSVRC 2015 [4] and an earlier version of Places365, but the dataset was deprecated after our publication. ImageNet has 1,000 object category classes and more than 1,000,000 training images. Places365 has 365 scene classes and ∼ 1, 600, 000 training images. We use these large datasets also because we assume we start from a well-trained network, which implies a large-scale dataset. For the new tasks, we consider PASCAL VOC 2012 image classification [31] ("VOC"), Caltech-UCSD Birds-200-2011 fine-grained classification [32] ("CUB"), and MIT indoor scene classification [33] ("Scenes"). These datasets have a moderate number of images for training: 5,717 for VOC; 5,994 for CUB; and 5,360 for Scenes. Among these, VOC is very similar to ImageNet, as subcategories of its labels can be found in ImageNet classes. MIT indoor scene dataset is in turn similar to Places365. CUB is dissimilar to both, since it includes only birds and requires capturing the fine details of the image to make a valid prediction. In one experiment, we use MNIST [34] as the new task expecting our method to underperform, since the hand-written characters are completely unrelated to ImageNet classes.

We mainly use the AlexNet [3] network structure because it is fast to train and well-studied by the community [6], [13], [15]. We also verify that similar results hold using 16-layer VGGnet [27] on a smaller set of experiments. For both network structures, the final layer (fc8) is treated as task-specific, and the rest are shared (θ s ) unless otherwise specified. The original networks pre-trained on ImageNet and Places365-standard are obtained from public online sources.

We report the center image crop mean average precision for VOC, and center image crop accuracy for all other tasks. We report the accuracy of the validation set of VOC, ImageNet and Places365, and on the test set of CUB and Scenes dataset. Since the test performance of the former three cannot be evaluated frequently, we only provide the performance on their test sets in one experiment. Due to the randomness within CNN training, we run our experiments three times, and report the mean performance.

Our experiments investigate adding a single new task to the network or adding multiple tasks one-by-one. We also examine effect of dataset size and network design. In ablation studies, we examine alternative response-preserving losses, the utility of expanding the network structure, and fine-tuning with a lower learning rate as a method to preserve original task performance. Note that the results have multiple sources of variance, including random initialization and training, pre-determined termination (performance can fluctuate by training 1 or 2 additional epochs), etc.

### 4.1. Main experiments

Single new task scenario. First, we compare the results of learning one new task among different task pairs and different methods. Table 1(a), 1(b) shows the performance of our method, and the relative performance of other methods compared to it using AlexNet. We also visualize the old-new performance comparison on two task pairs in Figure 7. We make the following observations:

On the new task, our method consistently outperforms finetuning, LFL, fine-tuning FC, and feature extraction except for ImageNet→MNIST and Places365→CUB using fine-tuning. The gain over fine-tuning was unexpected and indicates that preserving outputs on the old task is an effective regularizer. (See Section 5 for a brief discussion). This finding motivates replacing fine-tuning with LwF as the standard approach for adapting a network to a new task.

On the old task, our method performs better than fine-tuning but often underperforms feature extraction, fine-tuning FC, and sometimes LFL. By changing shared parameters θ s , fine-tuning significantly degrades performance on the task for which the original network was trained. By jointly adapting θ s and θ o to generate similar outputs to the original network on the old task, the performance loss is greatly reduced.

Considering both tasks, Figure 7 shows that if λ o is adjusted, LwF can perform better than LFL and fine-tuning FC on the new task for the same old task performance on the first task pair, and perform similarly to LFL on the second. Indeed, fine-tuning FC gives a performance between finetuning and feature extraction. LwF provides freedom of changing the shared representation compared to LFL, which may have boosted the new task performance.

Our method performs similarly to joint training with AlexNet. Our method tends to slightly outperform joint training on the new task but underperform on the old task, which we attribute to a different distribution in the two task datasets. Overall, the methods perform similarly, a positive result since our method does not require access to the old task training data and is faster to train. Note that sometimes both tasks' performance degrade with λ o too large or too small. We suspect that making it too large essentially increases the old task learning rate, potentially making it suboptimal, and making it too small lessens the regularization. Dissimilar new tasks degrade old task performance more.

For example, CUB is very dissimilar task from Places365 [13], and adapting the network to CUB leads to a Places365 accuracy loss of 8.4% (3.8% + 4.6%) for fine-tuning, 3.8% for LwF, and 1.5% (3.8% -2.3%) for joint training. In these cases, learning the new task causes considerable drift in the shared parameters, which cannot fully be accounted for by LwF because the distribution of CUB and Places365 images is very different. Even joint training leads to more accuracy loss on the old task because it cannot find a set of shared parameters that works well for both tasks. Our method does not outperform fine-tuning for Places365→CUB and, as expected, ImageNet→MNIST on the new task, since the hand-written characters provide poor indirect supervision for the old task. The old task accuracy drops substantially with fine-tuning and LwF, though more with fine-tuning. Similar observations hold for both VGG and AlexNet structures, except that joint training outperforms consistently for VGG, and LwF performs worse than before on the old task.

(Table 1(c)) This indicates that these results are likely to hold for other network structures as well, though joint training may have a larger benefit on networks with more representational power. Among these results, LFL diverges using stochastic gradient descent, so we tuned down the learning rate (0.5×) and used λ i = 0.2 instead. Multiple new task scenario. Second, we compare different methods when we cumulatively add new tasks to the system, simulating a scenario in which new object or scene categories are gradually added to the prediction vocabulary. We experiment on gradually adding VOC task to AlexNet trained on Places365, and adding Scene task to AlexNet trained on ImageNet. These pairs have moderate difference between original task and new tasks. We split the new task classes into three parts according to their similarity -VOC into transport, animals and objects, and Scenes into large rooms, medium rooms and small rooms. (See supplemental material) The images in Scenes are split into these three subsets. Since VOC is a multilabel dataset, it is not possible to split the images into different categories, so the labels are split for each task and images are shared among all the tasks.

Each time a new task is added, the responses of all other tasks Y o are re-computed, to emulate the situation where data for all original tasks are unavailable. Therefore, Y o for older tasks changes each time. For feature extractor and joint training, cumulative training does not apply, so we only report their performance on the final stage where all tasks are added. Figure 4 shows the results on both dataset pairs. Our findings are usually consistent with the single new task experiment: LwF outperforms fine-tuning, feature extraction, LFL, and fine-tuning FC for most newly added tasks. However, LwF performs similarly to joint training only on newly added tasks (except for Scenes part 1), and underperforms joint training on the old task after more tasks are added.

Influence of dataset size. We inspect whether the size of the new task dataset affects our performance relative to other methods. We perform this experiment on adding CUB to ImageNet AlexNet. We subsample the CUB dataset to 30%, 10% and 3% when training the network, and report the result on the entire validation set. Note that for joint training, since each dataset has a different size, the same number of images are subsampled to train both tasks (resampled each epoch), which means a smaller number of ImageNet images being used at one time. Our results are shown in Figure 5. Results show that the same observations hold. Our method outperforms fine-tuning on both tasks. Differences between methods tend to increase with more data used, although the correlation is not definitive.

### 4.2. Design choices and alternatives

Choice of task-specific layers. It is possible to regard more layers as task-specific θ o , θ n (see Figure 6(a)) instead of regarding only the output nodes as task-specific. This may provide advantage for both tasks because later layers tend to be more task specific [13]. However, doing so requires more storage, as most parameters in AlexNet are in the first two fully connected layers. Target: Fig. 6. Illustration for alternative network modification methods. In (a), more fully connected layers are task-specific, rather than shared. In (b), nodes for multiple old tasks (not shown) are connected in the same way. LwF can also be applied to Network Expansion by unfreezing all nodes and matching output responses on the old tasks. expansion", which adds nodes to some layers. This allows for extra new-task-specific information in the earlier layers while still using the original network's information. Figure 6(b) illustrates this method. We add 1024 nodes to each layer of the top 3 layers. The weights from all nodes at previous layer to the new nodes at current layer are initialized the same way Net2Net [20] would expand a layer by copying nodes. Weights from new nodes at previous layer to the original nodes at current layer are initialized to zero. The top layer weights of the new nodes are randomly re-initialized. Then we either freeze the existing weights and fine-tune the new weights on the new task ("network expansion"), or train using Learning without Forgetting as before ("network expansion + LwF"). Note that both methods needs the network to scale quadratically with respect to the number of new tasks.

Table 2(a) shows the comparison with our original method. Network expansion by itself performs better than feature extraction, but not as well as LwF on the new task. Network Expansion + LwF performs similarly to LwF with additional computational cost and complexity.

Effect of lower learning rate of shared parameters. We investigate whether simply lowering the learning rate of the shared parameters θ s would preserve the original task performance. The result is shown in Table 2(a). A reduced learning rate does not prevent fine-tuning from significantly reducing original task performance, and it reduces new task performance. This shows that simply reducing the learning rate of shared layers is insufficient for original task preservation.

L2 soft-constrained weights. Perhaps an obvious alternative to LwF is to keep the network parameters (instead of the response) close to the original. We compare with the baseline that adds 1 2 λ o w -w 0 2 to the loss for fine-tuning, where w and w 0 are flattened vectors of all shared parameters θ s and their original values. We change the coefficient λ o and observe its effect on the performance. λ o is set to 0.15, 0.5, 1.5, 2.5 for Places365→VOC, and 0.005, 0.015, 0.05, 0.15, 0.25 for ImageNet→Scene.

As shown in Figure 7, our method outperforms this baseline, which produces a result between feature extraction (no parameter change) and fine-tuning (free parameter change). We believe that by regularizing the output, our method maintains old task performance better than regularizing individual parameters, since many small parameter changes could cause big changes in the outputs.

Choice of response preserving loss. We compare the use of L 1 , L 2 , cross-entropy loss, and knowledge distillation loss with T = 2 for keeping y o , ŷ o similar. We test on the same task pairs as before. Figure 7 shows our results. Results indicate our knowledge distillation loss slightly outperforms compared losses, although the advantage is not large.

## 5. DISCUSSION

We address the problem of adapting a vision system to a new task while preserving performance on original tasks, without access to training data for the original tasks. We propose the Learning without Forgetting method for convolutional neural networks, which can be seen as a hybrid of knowledge distillation and fine-tuning, learning parameters that are discriminative for the new task while preserving outputs for the original tasks on the training data. We show the effectiveness of our method on a number of classification tasks.

As another use-case example, we investigate using LwF in the application of tracking in Appendix A. We build on MD-Net [35], which views tracking as a template classification task. A classifier transferred from training videos is finetuned online to classify regions as the object or background. We propose to replace the fine-tuning step with Learning without Forgetting. We leave the details and implementation to the appendix. We observe some improvements by applying LwF, but the difference is not statistically significant.

Our work has implications for two uses. First, if we want to expand the set of possible predictions on an existing network, our method performs similarly to joint training but is faster to train and does not require access to the training data for previous tasks. Second, if we care only about the performance for the new task, our method often outperforms the current standard practice of fine-tuning. Fine-tuning approaches use a low learning rate in hopes that the parameters will settle in a "good" local minimum not too far from the original values. Preserving outputs on the old task is a more direct and interpretable way to to retain the important shared structures learned for the previous tasks.

We see several directions for future work. We have demonstrated the effectiveness of LwF for image classification and one experiment on tracking, but would like to further experiment on semantic segmentation, detection, and problems outside of computer vision. Additionally, one could explore variants of the approach, such as maintaining a set of unlabeled images to serve as representative examples for previously learned tasks. Theoretically, it would be interesting to bound the old task performance based on preserving outputs for a sample drawn from a different distribution. More generally, there is a need for approaches that are suitable for online learning across different tasks, especially when classes have heavy tailed distributions. mall, movietheater, museum, poolinside, subway, trainstation, warehouse, winecellar.

• Medium rooms: bakery, bar, bookstore, bowling, buffet, classroom, clothingstore, computerroom, deli, fastfood restaurant, florist, gameroom, gym, jewelleryshop, kindergarden, laboratorywet, laundromat, locker room, meeting room, office, pantry, restaurant, shoeshop, toystore, videostore. • Small rooms: artstudio, bathroom, bedroom, children room, closet, corridor, dentaloffice, dining room, elevator, garage, hairsalon, hospitalroom, kitchen, livingroom, nursery, operating room, prisoncell, restaurant kitchen, stairscase, studiomusic, tv studio, waitingroom This split is also used in [10].

## Figures et tableaux

**Fig. 5.** Influence of subsampling new task training set on compared methods. The x-axis indicates diminishing training set size. Three runs of our experiments with different random θn initialization and dataset subsampling are shown. Scatter points are jittered horizontally for visualization, but line plots are not jittered to facilitate comparison. Differences between LwF and compared methods on both the old task and the new task decrease with less data, but the observations remain the same. LwF outperforms fine-tuning despite the change in training set size.

**Fig. 7.** Visualization of both new and old task performance for compared methods, some with different weights of losses. (a)(b): comparing methods; (c)(d): comparing losses. Larger symbols signifies larger λo, i.e. heavier weight towards response-preserving loss.

[figure sans légende identifiée] : task specific parameters for each old task Xn, Yn: training data and ground truth on the new task Initialize: Yo ← CNN(Xn, θs, θo) // compute output of old tasks for new data θn ←RANDINIT(|θn|) // randomly initialize new parameters Train: Define Ŷo ≡ CNN(Xn, θs, θo) // old task output Define Ŷn ≡ CNN(Xn, θs, θn) // new task output

    θ * s , θ * o , θ * n ← argmin | λoL old (Yo, Ŷo) + Lnew(Yn, Ŷn) + R( θs, θo, θn)
    θs, θo, θn | 
    Fig. 3. Procedure for Learning without Forgetting. | 

**TABLE 1** Performance for the single new task scenario. For all tables, the difference of methods' performance with LwF (our method) is reported to facilitate comparison. Mean Average Precision is reported for VOC and accuracy for all others. On the new task, LwF outperforms baselines in most scenarios, and performs comparably with joint training, which uses old task training data we consider unavailable for the other methods. On the old task, our method greatly outperforms fine-tuning and achieves slightly worse performance than joint training. An exception is the ImageNet-MNIST task where LwF does not perform well on the old task.

     |  | (a) Using AlexNet structure (validation performance for ImageNet/Places365/VOC) |  |  | 
     | ImageNet→VOC | ImageNet→CUB | ImageNet→Scenes | Places365→VOC | Places365→CUB | Places365→Scenes | ImageNet→MNIST
     | old | new | old | new | old | new | old | new | old | new | old | new | old | new
    LwF (ours) | 56.2 | 76.1 | 54.7 | 57.7 | 55.9 | 64.5 | 50.6 | 70.2 | 47.9 | 34.8 | 50.9 | 75.2 | 49.8 | 99.3
    Fine-tuning | -0.9 | -0.3 | -3.8 | -0.7 | -2.0 | -0.8 | -2.2 | 0.1 | -4.6 | 1.0 | -2.1 | -1.7 | -2.8 | 0.0
    LFL | 0.0 | -0.4 | -1.9 | -2.6 | -0.3 | -0.9 | 0.2 | -0.7 | 0.7 | -1.7 | -0.2 | -0.5 | -2.9 | -0.6
    Fine-tune FC | 0.5 | -0.7 | 0.2 | -3.9 | 0.6 | -2.1 | 0.5 | -1.3 | 1.8 | -4.9 | 0.3 | -1.1 | 7.0 | -0.2
    Feat. Extraction | 0.8 | -0.5 | 2.3 | -5.2 | 1.2 | -3.3 | 1.1 | -1.4 | 3.8 | -12.3 | 0.8 | -1.7 | 7.3 | -0.8
    Joint Training | 0.7 | -0.2 | 0.6 | -1.1 | 0.5 | -0.6 | 0.7 | -0.0 | 2.3 | 1.5 | 0.3 | -0.3 | 7.2 | -0.0
     |  | (b) Test set performance |  |  | (c) Using VGGnet structure |  |  | 
     |  |  |  | Places365→VOC |  |  | ImageNet→CUB | ImageNet→Scenes |  | 
     |  |  |  | old | new |  |  | old |  | new | old | new |  | 
     |  | LwF (ours) | 50.6 | 73.7 |  | LwF (ours) | 60.6 |  | 72.5 | 66.8 | 74.9 |  | 
     |  | Fine-tuning | -2.1 | 0.1 | Fine-tuning | -9.9 |  | 0.6 | -4.1 | -0.3 |  | 
     | Feat. Extraction | 1.3 | -2.3 |  | LFL | 0.3 |  | -2.8 | -0.0 | -2.1 |  | 
     |  | Joint Training | 0.9 | -0.1 | Fine-tune FC Feat. Extraction | 3.2 8.2 |  | -6.7 -8.6 | 1.4 1.9 | -2.4 -5.1 |  | 
     |  |  |  |  |  | Joint Training | 8.0 |  | 2.5 | 4.1 | 1.5 |  | 

**Fig.4.** Performance of each task when gradually adding new tasks to a pre-trained network. Different tasks are shown in different sub-graphs. The x-axis labels indicate the new task added to the network each time. Error bars shows ±2 standard deviations for 3 runs with different θn random initializations. Markers are jittered horizontally for visualization, but line plots are not jittered to facilitate comparison. For all tasks, our method degrades slower over time than fine-tuning and outperforms feature extraction in most scenarios. For Places2→VOC, our method performs comparably to joint training.

     |  |  |  |  |  |  | fine-tuning
     |  |  |  |  |  |  | joint training
     |  |  |  |  |  |  | feat. extraction
     |  |  |  |  |  |  | LwF (ours)
     |  |  |  |  |  |  | LFL
     |  |  |  |  |  |  | fine-tune FC
    0.6 |  |  | 0.58 |  |  |  | fine-tuning
     |  |  |  |  |  |  | joint training
     |  |  |  |  |  |  | feat. extraction
    0.5 |  |  | 0.56 |  |  |  | LwF (ours) LFL
    0.4 |  |  |  |  |  |  | fine-tune FC
     |  |  | 0.54 |  |  |  | 
    0.3 |  |  |  |  |  |  | 
    0.2 |  |  | 0.52 |  |  |  | 
    0.1 |  |  | 0.5 |  |  |  | 
    3% | 10% | 30% | 100% | 3% | 10% | 30% | 100%
    (a) CUB accuracy (new) | (b) ImageNet accuracy (old)

**Table 2** (a) shows the comparison on three task pairs. Our results do not indicate any advantage to having additional task-specific layers.

    Network expansion. We explore another way of modify-
    ing the network structure, which we refer to as "network

**TABLE 2** Performance of our method versus various alternative design choices. In most cases, these alternative choices do not provide consistent advantage or disadvantage compared to our method.(a) Changing the number of task-specific layers, using network expansion, or attempting to lower θs's learning rate when fine-tuning. Performing LwF and fine-tuning with and without warmup. The warmup step is not crucial for LwF, but is essential for fine-tuning's old task performance.

     | ImageNet→CUB | ImageNet→Scenes | Places365→VOC
     | old | new | old | new | old | new
    LwF at output layer (ours) | 54.7 | 57.7 | 55.9 | 64.5 | 50.6 | 70.2
    last hidden layer | 54.7 | 56.2 | 55.7 | 65.0 | 50.7 | 70.6
    2 find last hidden (Fig. 6(a)) | 54.6 | 57.1 | 55.8 | 64.2 | 50.8 | 70.5
    network expansion | 57.0 | 54.0 | 57.0 | 62.5 | 51.7 | 67.1
    network expansion + LwF | 54.4 | 57.0 | 55.7 | 63.9 | 50.7 | 70.4
    fine-tuning (10% θs learning rate) | 52.2 | 54.9 | 54.8 | 62.7 | 49.3 | 69.5
    (b) ImageNet→CUB | ImageNet→Scenes | Places365→VOC
     | old | new | old | new | old | new
    LwF | 54.7 | 57.7 | 55.9 | 64.5 | 50.6 | 70.2
    fine-tuning | 50.9 | 57.0 | 53.9 | 63.8 | 48.4 | 70.3
    LFL | 52.8 | 55.1 | 55.5 | 63.6 | 50.8 | 69.5
    LwF (no warm-up) | 53.5 | 59.9 | 55.2 | 64.9 | 50.4 | 70.0
    fine-tuning (no warm-up) | 42.5 | 59.8 | 49.8 | 63.9 | 42.3 | 70.0
    LFL (no warm-up) | 52.5 | 55.3 | 55.4 | 63.0 | 50.6 | 69.1
