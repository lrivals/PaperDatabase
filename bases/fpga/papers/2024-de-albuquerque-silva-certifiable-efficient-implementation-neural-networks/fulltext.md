---
id: 2024-de-albuquerque-silva-certifiable-efficient-implementation-neural-networks
title: "Certifiable and efficient implementation of neural networks on embedded safety-critical real-time systems"
year: 2024
backend: grobid
---

## Abstract

Délivré par l'ISAE-SUPAERO Implantation certifiable et efficace de réseaux de neurones sur des systèmes embarqués temps-réel critiques Thèse présentée et soutenue, le 16 juillet 2024 par Iryna DE ALBUQUERQUE SILVA École doctorale MITT -Mathématiques, informatique, télécommunications

## Résumé français

Contexte. Le monde de l'aéronautique envisage l'utilisation d'algorithmes d'apprentissage automatique, et en particulier de réseaux de neurones, pour faciliter et améliorer des tâches telles que la navigation, la maintenance prédictive et le contrôle du trafic aérien. Toutefois, leur utilisation dans des systèmes critiques soulèfive de nombreuses questions de sécurité et de conformité aux exigences de certification. Ces dernières visent à garantir la correction de la conception jusqu'à l'implantation de la fonction attendue. Récemment de nouvelles directives, telles que le standard ARP6983 [152], sont en cours d'écriture pour compléter files textes réglementaires existant afin de permettre l'introduction d'algorithmes d'apprentissage automatique dans des systèmes avioniques. Ces directives complètent notamment la DO-178C [67], le standard de référence pour le développement de logiciels. Cette thèse étudie l'implantation en temps réel et en toute sécurité de réseaux de neurones feed-forward sur des systèmes avioniques embarqués. En particulier, nous nous concentrons sur le modèle de réseau neuronal entrainé et vérifié hors ligne, appelé modèle d'inférence. L'objectif est de définir une approche de développement logiciel de modèfiles d'inférence en conformité avec exigences de l'avionique.

Approche. Nous avons défini un certain nombre d'objectifs nécessaires pour garantir l'implantation sûre et correcte d'un modèle d'inférence. Ces objectifs sont un sous-ensemble de ceux listés dans files normes de certification, mais ont été identifiés comme difficiles à atteindre pour le processus traditionnel de développement de logiciels d'apprentissage automatique et sont cohérents avec files directives en cours d'élaboration, à savoir files feuilles de route de l'EASA et la norme ARP6983. Plus précisément, files objectifs sélectionnés dans la thèse sont (i) la description précise et non ambigüe de la fonctionnalité du modèle d'inférence, (ii) la préservation de la sémantique et la traçabilité de la description du modèle d'inférence jusqu'à l'exécutable final, (iii) la prédictibilité temporelle de l'implantation, et (iv) une utilisation efficace des ressources disponibles.

## Contributions.

Pour implanter correctement un modèle d'inférence, il est important de définir formellement sa sémantique. Cela correspond à la première contribution de la thèse et nous avons formalisé chaque couche du modèle d'inférence sous forme de fonctions mathématiques. Ensuite, nous avons développé ACETONE, de l'anglais "Avionics C code generator for Neural Networks". ACETONE est un framework qui, à partir de la description d'un modèle d'inférence, génère automatiquement un code C sémantiquement équivalent et prédictible. Nous avons évalué le framework sur un ensemble réaliste de cas d'utilisation pour valider l'approche en regard des objectifs de certification choisis. En outre, nous avons comparé l'approche à des outils de l'état de l'art. Une fois le framework défini et disponible sur GitHub, nous avons choisi un axe d'amélioration et d'optimisation de code pour accélérer files temps de calcul. Plus précisément nous nous sommes concentrés sur files convolutions. L'idée est de reprendre files travaux classiques qui transforment une convolution en une multiplication matricielle. Cependant, files routines d'algèbre linéaire disponibles sur étagère fine sont pas compatibles avec files exigences de l'avionique. C'est la raison pour laquelle, nous avons proposé notre propre implantation prédictive, traçable et efficace d'un algorithme de multiplication matrice-matrice (GEMM) par blocs. Nous avons montré comment configurer un tel algorithme pour une cible donnée tout en proposant une méthode formelle de calcul du nombre d'accès à la mémoire et du nombre de cache misses, ce qui ouvre la voie à une analyse statique du WCET.

A.1 Cycle de développement en W pour files systèmes basés sur l'apprentissage automatique.

Adapté de [5]

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . A.2 Approche adoptée pour l'implantation du modèle d'inférence tenant compte de la certification.173 A.3 Le flux de travail pour une implantation sémantiquement correcte du modèle d'inférence. A.4 Illustration de la fonction associée à la couche Dense. . . . . . . . . . . . . . . . . . . . . A.5 Le flux de travail pour la génération de code C à partir d'une description de modèle d'inférence dans ACETONE. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . A.6 Architecture logicielle d'ACETONE. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . A.7 Exemple de matrices d'entrée pour un algorithme de convolution basé sur GEMM, en considérant un pas de un et sans rajout de zéros (zero-padding). La matrice A correspond au tenseur des noyaux de convolution commodément aplati et la matrice B correspond à la matrice de patchs, créée en copiant et en arrangeant files éléments du tenseur d'entrée original. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . Chapter 1

## Introduction

This PhD project was funded by the Artificial and Natural Intelligence Toulouse Institute (ANITI), as part of the chair on the Certification of Machine Leaning-based systems, in collaboration with ONERA and Airbus. The objective of this thesis was to investigate methodologies and strategies pertaining to the implementation of machine learning algorithms, in particular neural networks, on avionics systems, which are safety-critical real-time systems subject to certification processes.

### 1.1. Context

This doctoral study was motivated by the considerable research interest that the machine learning (ML) domain has gained in recent years. In traditional programming, humans write explicit instructions for a program to follow. However, in machine learning, instead of programming rules explicitly, algorithms are trained on large datasets to learn patterns and relationships within the data. These algorithms then use this learnt knowledge to make predictions when presented with new, unknown data. Examples of tasks where ML succeeds include detecting a runway in an image for aircraft landing [190], supporting predictive maintenance [28], helping air traffic control [193] or yet understanding spoken commands [135].

In the context of this thesis, we are interested in neural networks (NN), which constitute a class of machine learning algorithms. Neural networks are mathematical models consisting of interconnected units, also named artificial neurons, organized in layers, wherein each layer implements a mathematical function. The lifecycle of neural network models can be distinguished into two phases: the learning and the inference phases. During the learning phase, the NN learns the function that it aims to approximate via a recursive tuning of its parameters. In the inference phase, it applies the learnt parameters to process the input data and produce an output. Within this work, our focus lies on the inference phase. More precisely, we concentrate on the implementation of the trained and verified neural network model, output of the learning phase, called inference model.

#### 1.1.1. Certification of avionics systems

Despite its success in many domains, the use of machine learning in safety-critical products, such as avionics systems, raises several questions regarding safety risks. A system is said to be safety-critical when a failure within it may result in catastrophic effects on safety, including the loss of both the system and human lives. For instance, regulatory texts define that for critical systems the acceptable probability of a catastrophic failure is less than 10 ´9 per flight hour.

Thus, avionics systems are subject to certification procedures aiming to ensure compliance with safety standards throughout their complete development cycle, from requirements capture through validation and verification of the intended function. Within the existing documents, we can name the ED-79B/ARP4754B [70] and the ED-135/ARP4761A [71] documents, which present guidelines for the Figure 1.1: W-shaped development cycle for ML-based systems. Adapted from [5].

development and safety assessments at the system level. At the level of components of the system, the ED-80/DO-254 [66] and ED-12C/DO-178C [67] standards offer, respectively, guidance for the secure development of hardware and software items.

#### 1.1.2. Guidelines for ML-based applications in avionics systems

Thus, to allow for the use of ML-based applications in safety-critical systems, stakeholders have started working on addressing the question of its safe and standardized use. The initial scope of these initiatives is restricted to neural networks as well. The common understanding is that the safety-aware development process remains unchanged, except when a system or sub-system integrates ML-based components, in which case adapted guidelines are required. The European Aviation Safety Agency (EASA) has produced roadmaps [1,4] and concept papers [2,5] aiming to guide the research and define a time frame for regulatory deliverables. In particular, the EASA concept papers proposed a new W-shaped development cycle for ML-based applications, depicted in Figure 1.1.

From Figure 1.1, we differentiate the first V cycle, dedicated to the learning phase of the neural network: it contains guidelines ranging from the pre-training data management to the learning process verification, which is concentrated in evaluating the generalization capacity and robustness of the resulting trained models. Conversely, the second V cycle is dedicated to the inference phase: it encompasses orientations concerning the inference model implementation, the verification that the inference model preserves the trained model's properties and its integration within the ML system. The scope of this thesis, the inference model implementation, is highlighted in red.

Therefore, in accordance with EASA's initiatives, an EU-US joint working group (EUROCAE WG-114/SAE G-34) is currently drafting the guidelines, named ED-324/ARP6983 standard [152], to be used in the development of safety-related products implementing ML, allowing their approval in aeronautics. In the context of the inference model implementation, the ARP6983 guideline is expected to interface with the established DO-178C standard, which pertains to the development of software components in avionics systems.

The aforementioned learning and inference phases of neural networks are performed in programming environments named machine learning frameworks. However, most of state-of-the-art machine learning frameworks were not designed for and thus do not entirely comply with certification requirements. Hence the interest of proposing an adapted approach for the inference model implementation.

### 1.2. Approach

In order to study the safe implementation of a trained neural network into an inference model within embedded avionics systems, we adopted the following approach, summarized in Figure 1 First, we restricted our scope to feed-forward deep neural networks. In these variants each intermediate layer of the neural network takes as input the output of the previous layer, allowing no cycles in its structure. Moreover, as mentioned, our focus lies on the inference model. We thus consider that the neural network has been offline trained and verified, and is not expected to evolve during the inference phase. These assumptions align with the understanding of an initial reasonable objective present in the EASA concept papers. However, as long as it is performed offline, we are agnostic to the employed learning paradigm. The latter can be of type supervised, unsupervised or based on reinforcement learning.

Second, we defined a number of quantifiable objectives necessary to guarantee the safe and correct implementation of the inference model. These objectives clearly do not represent all the requirements present in normative standards, but were recognized as complex to obtain for the traditional ML software workflow and are in accordance with the guidelines under construction, i.e. the EASA roadmaps and the ARP6983 standard. The derived certification objectives concerning the inference model implementation range from its description to the final executable inference function. They require:

(i) a precise description of its functionality (Objective 1);

(ii) the preservation of its semantics (Objective 2);

(iii) the traceability of requirements from its description to the final executable (Objective 3);

(iv) its timing predictability (Objective 4); (v) its efficient resource usage (Objective 5). The work scope was also further narrowed to traditional avionics platforms, i.e. hardware architectures that are fully covered by existing safety standards. We thus examine a single-core bare-metal implementation in a commercial off-the-shelf (COTS) processor using the C language.

Third, in order to address the inference model implementation problematic considering the derived objectives and assumptions, we developed the ACETONE framework, which stands for "Avionics C code generator for Neural Networks". It designates a tool that, from the inference model description, automatically generates a semantically equivalent and predictable C code. To have a reference for code generation, we initially provided a formal definition of the semantics of each layer composing the inference model as mathematical functions. ACETONE is designed for straightforward experimenting and the generated code facilitates assessment of the previously mentioned certification objectives. We were able to evaluate the framework on a realistic set of inference models and compare our approach against two state-of-the-art inference tools, designed with nearly the same objectives as ACETONE.

Fourth, after validating the methodology for implementing the inference model against the fixed certification objectives, we began working on improving the code generated by ACETONE. The primary focus concerned the implementation of resource-expensive functions, in particular of the Convolutional layer. We focused on a Convolutional layer optimization that interprets the convolution operator as a matrix-matrix multiplication. However, state-of-the-art implementations of linear algebra routines rely on libraries that were not developed in a manner aware of the requirements of certification, hindering in particular the WCET analysis task. To overcome this limitation while still using principles presented in Basic Linear Algebra Subprograms (BLAS) libraries, we proceeded to develop our own GEMM routines to perform a GEMM-based convolution algorithm.

We initially developed a vanilla GEMM implementation, so called because it does not make use of any hardware-specific tuning techniques to improve memory transfers or computation rate. Subsequently, in an effort to align with established BLAS libraries, we decided to delve deeper on this axis of research and proposed an architecture-aware GEMM implementation. The latter performs a blocked GEMM algorithm, i.e. the multiplication of matrices that have been partitioned into blocks, or submatrices. By choosing the sizes of the blocks in function of the hardware architecture, it is possible to foster their convenient placement at the different levels of the memory hierarchy, improving spatial and temporal locality of the matrices during computation. Consistently prioritizing certification objectives, we focused on a traceable yet efficient implementation of a state-of-the-art blocked GEMM algorithm [79].

Nevertheless, to the best of our knowledge, no existing static analysis method is capable of detecting and leveraging precisely the memory access patterns that GEMM routines implement. Hence, to enforce time-predictability, we performed a study on the algorithm behaviour and proposed adapting the blocking parameters accordingly. In particular, we targeted time-predictability in an ARM Cortex-A15, a COTS processor with single-instruction multiple-data (SIMD) extensions. For each part of the blocked GEMM algorithm, we then derived the formulae that (i) determine the total number of memory accesses and (ii) define an upper bound on the number of L1 data cache misses. We focused on these two numbers as they can be exploited in static WCET estimation techniques such as IPET to tighten the WCET bound.

### 1.3. Organization of the manuscript

The manuscript is organized as follows: first, we introduce essential concepts to aid in understanding its content. Chapter 2 initially presents the necessary background on feed-forward deep neural networks, highlighting the difference between the learning and inference phases. In its second half, this chapter outlines background knowledge on the certification process to which avionics systems are subject and presents the identified challenges for the use of machine learning-based applications in such systems. Chapter 3 discusses the state of the art of frameworks used both for the learning and inference phases of machine learning applications.

In a second part, we present our contributions towards a certifiable and efficient implementation of the inference model. Chapter 4 covers the formalization, in the form of mathematical functions, of the semantics of the inference model. Chapter 5 delves into ACETONE, our proposed framework for automatically generating a semantically equivalent and predictable C code from the inference model description. We first introduce the software architecture of ACETONE, detailing each composing part, namely the front-end, the back-end and its internal representation. Afterwards, we describe the adopted methodology used to evaluate ACETONE and compare it with state-of-the-art frameworks.

Chapter 6 is dedicated to the discussion of certifiable optimizations on the 2D Convolutional layer implementation. We initially present the motivation behind focusing on optimizing this particular layer, then introduce the state of the art in existing methods and discuss their applicability to our context. The remainder of the chapter focuses on general matrix-matrix multiplication (GEMM) routines, which are at the core of the GEMM-based convolution algorithm. We detail both the vanilla and the architecture-aware GEMM implementations. Lastly, we present our analysis on the time-predictability of the architectureaware GEMM routine.

### 1.4. List of publications

## Background: ML-based applications within avionics systems

This chapter initially presents the necessary background on feed-forward deep neural networks to support the discussion of the following chapters. Section 2.1 introduces preliminary concepts on this class of neural networks as well as highlights the difference between the learning and inference phases in the lifecycle of a feed-forward deep neural network model. In a second phase, this chapter introduces background knowledge on the certification process to which avionics systems are subject and presents the identified challenges for the use of machine learning-based applications in such systems. Section 2.2 first presents the existing regulation set with the established certification standards. Section 2.2.1 then introduces ongoing initiatives to evolve the current directives in order to cover ML-based applications, with a focus on the concerns for the implementation of the inference model. Section 2.2.2 details the recommendations for the development of the software components present in avionics systems. Afterwards, Section 2.3 presents the derived certification objectives for a safe implementation of the inference model. Finally, Section 2.4 discusses the identified challenges, particular to ML software or not, to answer the selected certification objectives.

### 2.1. Feed-forward deep neural networks

The field of artificial intelligence (AI) has gained much research attention in the past years. The power of AI resides in the capacity of solving highly complex problems [78]. Within artificial intelligence, machine learning (ML) is an important domain. It describes the study and development of statistical algorithms that are able to efficiently generalize on unknown input data after the extraction of patterns from a similar, and representative, data set. Examples of tasks where ML succeeds are detecting a runway in an image for aircraft landing [190], supporting predictive maintenance [28], helping air traffic control [193] or yet understanding spoken commands [135].

Neural networks are a class of machine learning algorithms. A neural network implements a mathematical function F N that aims at approximating a continuous real-valued function h ˚ [88,155]. The term network comes from the fact that F N is actually composed of many different mathematical functions. Each function composing F N is associated to a layer. A layer can be classified into input, output and intermediate, or hidden, layer. The number of layers in a neural network defines its depth. Deep neural networks are then neural networks with multiple hidden layers.

The neural notation is linked to the notion that each layer itself is a collection of units, wherein a unit is roughly inspired by a biological neuron. Thus, each unit implements a mathematical function as well. The hidden layers can implement linear or non-linear functions. The existence of non-linearity in F N is an essential hypothesis in the theorem that claims that neural networks are universal approximators [88].

There are two types of deep neural networks: feed-forward neural networks and recurrent neural networks. Recurrent neural networks feature layers that take as input some of their output (or the output of a successor layer), thus creating cycles. In feed-forward variants it is not true. A common representation of a feed-forward deep neural network (FDNN) is in the form of a directed acyclic graph (DAG) defining how its layers are connected together. Then we associate a mathematical function F N to this directed graph, describing the mathematical rules of the neural network.

In the remainder of this manuscript, unless otherwise stated, neural networks (NN) or simply networks refer to feed-forward deep neural networks. A formal definition for feed-forward deep neural networks, as well as the formal semantics of the different neural network layers considered in this work are provided in Chapter 4.

#### 2.1.1. Lifecycle of neural networks

In this section we detail what is the lifecycle of neural network models, which consists essentially of two parts: the learning and the inference phases.

The learning phase comprises the preparation of the data set, which depends on the choice of the learning approach, the design of the neural network, its training from collected data and the verification of the resulting model, which is called trained model. In this work we only consider offline learning, meaning that, after being trained, the neural network model does not change at runtime and is a deterministic function. We briefly describe each stage of the learning phase hereafter.

In preparation to the learning phase one must compose and treat the data on which the neural network will learn. It is divided into distinct sets named training, validation and testing data sets. The training data is the set from which the neural network learns the representative features needed for generalizing afterwards. The validation set is used to fine-tune the parameters of the model and assess its capacity to perform the desired task during the learning phase. Lastly, the testing data set is composed of typical input data on which the model is expected to infer once trained.

The learning approach used in the learning phase can be categorized as (i) supervised learning, where the network is trained from a labeled training data set, meaning that each input is labeled with the desired output, (ii) unsupervised learning, where the network is trained from an unlabeled training data set and has to define its own rules to describe a given input and (iii) reinforcement learning, which consists on a trial and error strategy to maximize a cumulative reward and finally learn what is the best action for a given situation. We precise that, as long as it is performed offline, we are indifferent to the employed learning paradigm.

The design of the neural network model includes the choice of the type of mathematical function performed by each layer, the setting of their non-trainable parameters, as well as the overall number of layers. The non-trainable parameters in a model, also called hyperparameters, are those that are not the objective of the optimization in the training process, but can possibly be adjusted during the learning phase. They include, besides the layers' parameters, other constants that guide the training process. Moreover, the design of the model is highly dependent on the type of application targeted. For example, neural networks that contain convolutional functions are efficient to process images while architectures such as multi-layer perceptrons perform well in classification tasks, as will be detailed in Section 4. 6.

Afterwards, for the training stage, a training algorithm is chosen. A training algorithm is a specific optimization algorithm used to update the trainable parameters of a neural network model during the training process. Its primary goal is to minimize a predefined loss function by adjusting the model's trainable parameters based on the gradients of the loss function with respect to those parameters. Examples of training algorithms are stochastic gradient descent (SDG), adaptive moment estimation (Adam) and root mean square propagation (RMS Prop).

Subsequently, the verification stage ensures that all the functional and non-functional requirements defining the performance of the model are met. The requirements for a neural network are specifications that describe the fundamental capabilities and behaviours the network must exhibit to meet its intended purpose. Examples of verifications are the model's generalization capacity, the accuracy of its outputs and the consistency in terms of used resources. Other proofs concern its robustness against abnormal input data and conditions, its stability in the presence of small perturbations in the input data and the capacity to fully test all of its composing functions.

Once validated against functional and non-functional requirements, the trained network can be executed to perform the previously learned task, in what is called the inference phase. Finally, the inference phase consists in the forward, non-iterative, pass of input data trough the neural network. Prior to the inference phase, the trained and verified neural network model first has to be implemented into what is called an inference model.

## Definition 1 (Inference model). The inference model is the implementation of the trained and verified neural network model.

The inference model can then be deployed to a target hardware. The question of how to correctly produce an accurate inference model for a given trained model and a given target hardware, in accordance with safety requirements, is the subject of this thesis.

### 2.2. Certification of avionics systems

The European Aviation Safety Agency (EASA) in Europe and the Federal Aviation Administration (FAA) in the United States define the requirements for aeronautics and space regulation in their respective states. Regarding the airworthiness requirements for airplanes in the transportation category, personal safety is the main concern. Within the scope of this thesis, we are interested in the set of rules concerning the aircraft equipments and systems, present in the Certification Specification (CS) of the EASA and Federal Aviation Regulations (FAR) of the FAA texts, and refereed to CS/FAR 25.1309.

The CS/FAR 25.1309 classifies failure conditions depending on their effects on safety, which is assessed by the impacts on the occupants and the workload of the pilots. The classification then distinguishes catastrophic, hazardous, major, minor, and with no safety effect failures. For example, a catastrophic failure condition is characterized by the loss of the aircraft and its occupants, while a minor failure condition would result in easy crew actions and some inconvenience for occupants. The document also clarifies the probability terms of extremely improbable, extremely remote, remote, or probable. Finally, CHAPTER 2. BACKGROUND: ML WITHIN AVIONICS SYSTEMS the CS/FAR 25.1309 requires a fail-safe system design, which consists in two key principles: (i) no single failure must result in a catastrophic failure condition and (ii) each catastrophic failure condition is extremely improbable.

The acceptable probability of a catastrophic failure occurrence was defined with the following reasoning. Considering the accident rate in commercial aviation over a 10-year period (from 1970 to 1980), it was observed that the rate of catastrophic accidents was slightly below 10 ´6 per flight hour. Approximately 10% of these catastrophic accidents were found to be attributable to system failures, hence a proportion of roughly 10 ´7 accidents per flight hour. Assuming a hypothetical scenario in which a large commercial aircraft could encounter 100 hazards resulting in a catastrophic effect, it was deducted that for critical systems the acceptable probability of catastrophic failure is less than 10 ´9 per flight hour.

In order to translate these high-level rules into objectives and activities that can be understood, and for which evidence can be provided, the CS/FAR 25.1309 also introduces the notion of acceptable means of compliance (AMC). As recognized means for showing compliance with the airworthiness requirements and support certification, we find the standards, written by working groups bringing together aircraft manufacturers, system manufacturers and authorities. Among the existing standards, at the system level, we can cite the ED-79B/ARP4754B [70] and the ED-135/ARP4761A [71] documents.

In general, errors made during the design and development of systems have traditionally been detected and corrected by exhaustive tests conducted on the system and its components, by direct inspection, and by other direct verification methods capable of completely characterising the performance of the system. However, for complex systems, exhaustive testing may either be impossible, because all of the system states cannot be determined, or impractical, because of the number of tests that must be accomplished. For these types of systems, compliance may be shown by the use of development assurance.

The ARP4754B standard then proposes recommended practices for the complete aircraft development cycle, from systems requirements through systems verification. It is used together with the ARP4761A document, which presents guidelines for performing safety assessments of aircraft systems. The aircraft system is composed of multiple components, also named items, each with well-defined interfaces and requirements. The ED-80/DO-254 [66] and ED-12C/DO-178C [67] standards offer then, respectively, guidance for the secure development of hardware and software items.

In addition, the ARP4754B standard defines the notion of development assurance level (DAL), which determines the degree of stringency that should be applied by the development assurance process depending on the consequences that a failure in the system may generate. There are in total five assurance levels with a decreasing number of objectives to be respected: DAL-A corresponds to failures resulting in catastrophic scenarios, DAL-B is for system malfunction causing hazardous situations, DAL-C and DAL-D are for failing with, respectively, major and minor safety consequences, and finally DAL-E covers systems failures with no safety effect associated.

Figure 2.2 depicts the regulation set containing the different guidelines for the development of civil aircraft and systems with an emphasis on safety aspects. In the next section we discuss how this regulation framework is being adapted to cover machine learning-based applications.

#### 2.2.1. Guidelines for ML-based applications in avionics systems

Given the proven capacity of machine learning applications in diverse contexts, industrials, academics and regulatory bodies have started working in addressing the question of its safe, standardized use in safetycritical systems. In February 2020, the EASA published its first Artificial Intelligence Roadmap [1], a document whose objective was to identify the impact of the use of ML in aviation, regarding not only the benefits but also the safety and ethical risks associated. This document was also intended to serve as a basis for discussion with the Agency's stakeholders as well as define the time frame for the regulatory deliverables, in order to be as aligned as possible with the different industrial roadmaps concerning the exploitation of ML solutions. Thus, in April 2021, the EASA released a concept paper with the first usable guidance for Level 1 machine learning applications in aeronautics [2], which covers tasks related to human assistance and augmentation. A new concept paper was released in February 2023 [5]. Its intention was to update concepts and guidance for Level 1 applications and define directions for Level 2 utilization, which comprises tasks where human and AI-based system cooperate and collaborate towards a goal. The EASA roadmap was then updated with the publication of a new issue in May 2023 [4], also responsible for revising the agenda on AI regulation. Concerning the deployment of AI solutions, first approvals of Level 1 applications are said to be expected for as soon as 2025. Guidance on Level 3, which covers advanced automation and autonomous AI, is anticipated to be available for consultation in 2025. Finally, a consolidation phase is programmed, which foresees the finalisation of guidances for the different application levels by 2028.

Since July 2019, a EU-US joint working group, named EUROCAE WG-114/SAE G-34, has been established in order to work on formulating technical standards for certifying aeronautical systems integrating components based on machine learning. In 2021 the group produced a statement of concerns, AIR6988 [154], specifying the adaptations needed in current certification standards and methods to cope with the integration of machine learning. Currently, the group is drafting the guidelines (ED-324/ARP6983 [152]) to be applied in the development cycle of safety-related products implementing AI, allowing their approval in aeronautics. In addition, a standard about AI use cases is also in progress, aiming to document possible technologies, software and hardware architectures, validation approaches, and safety concerns for each use case (AIR6994 [153]).

Figure 2.3 depicts how the existing standards and the work in progress concerning the use of artificial intelligence are expected to interface in the development phase of airborne systems. It indicates that the liaison from the system development process to the software and electronic hardware development process remains unchanged, except when a system or subsystem integrates ML-based components. In which case, it must also follow the ARP6983 guidelines in combination with the established standards.

As evidenced by the various outlined initiatives, the integration of artificial intelligence in safetycritical systems constitutes a research domain in exponential growth and continual evolution. Hereafter we emphasize the approach presented in the EASA concept papers, which is in consonance with the studies of the EUROCAE WG-114/SAE G-34 working group. The first guidelines restrict AI applications to machine learning algorithms, such as neural networks and decision trees. Moreover, only the offline learning paradigm is addressed for now. These constraints are consistent with our hypotheses.

#### 2.2.1.1. AI-based system

Firstly, the EASA AI roadmap document defines the notion of an AI-based system, which is a system composed of several classic subsystems, and at least one of them is an AI-based subsystem. In its turn, an AI-based subsystem embeds at least one ML constituent. An ML constituent is a layer introduced between the system and item levels to group all software and hardware items that are necessary to the ML functionality. Thus, the ML constituent includes traditional software and hardware items, with at least one specialised software or hardware item containing elements of ML inference model(s), in which case it is named an ML item.

An ML item can contain only part or the entirety of one or several ML inference model(s). Put simply, this signifies that there is not necessarily a one-to-one relationship between the ML model(s) resulting from the training phase, and the software and hardware items that implement them.

Example 1 (AI-based system -ACAS-Xu subsystem). An example of an AI-based system is proposed in [45] and depicted in Figure 2.4: it is a version of the airborne anti-collision system ACAS-Xu wherein the look-up tables (LUT) describing the avoidance decisions are replaced by surrogate neural networks. A detailed description of the ACAS-Xu surrogate neural networks will be presented in Section 4.6.1.

The controller contains, besides the neural networks themselves, auxiliary functions for input normalisation, for the selection of the correct neural network according to the time separating the two aircraft (t sep ) and the previous advisory (u prev ), and for post-processing, to compute the advisory manoeuvrer.

The proposed system is completed by a safety net and a check module, both traditional (non-ML) components. The safety net is used to cover regions of the input space where the surrogate neural networks do not approximate well the LUT and the check module serves to switch between the ML controller and the safety net.

The ML constituent contains: (i) the inference models, which were all allocated in one software item, classified as an ML item, (ii) the auxiliary traditional functions, hosted in a traditional software item and, (iii) the safety net and check module, allocated in traditional software items as well. The whole is integrated in a hardware item and constitutes the AI-based system. One could also envisage to decompose one inference model into multiple software items, where each item performs a specific algorithm or mathematical operation and summed up they constitute the complete ML inference model. The inference model could also be dispatched into different hardware items, such as CPU, GPU or matrix-multiplication accelerators units, integrating a system-on-chip (SoC) target hardware.

Example 2 (LeNet-5 inference model distributed into multiple hardware items). In [76], the authors present an example repartition of the LeNet-5 inference model into multiple hardware items. For a detailed description of the LeNet-5 model structure, the reader can refer to Section 4. 6.2. In this study the authors use an UltraScale+ [189] platform, composed of several ARM cores, a GPU and an FPGA. In the example, depicted in Figure 2.5, the convolutional layers are executed on the FPGA and the remaining layers on an ARM core. The idea is to offload the input tensors of each convolutional layer on the FPGA and then retrieve their outputs to continue processing in the ARM cores. Other possibilities of distribution for the inference model are found in the aforementioned paper. Assumption 1 (One-to-one relationship between inference model and SW/HW item.). Within the scope of this thesis, we consider that an inference model is completely hosted in one software item and one hardware item.

#### 2.2.1.2. Trustworthy AI building blocks

Moreover, the EASA AI roadmap delineated four fundamental building blocks deemed crucial for establishing a framework for reliable AI and facilitating the preparedness for the use of, for now, machine learning in aviation. Figure 2.6 depicts the identified components towards AI trustworthiness. The first building block is the AI trustworthiness analysis. This block establishes a connection with the EU Ethical Guidelines devised by the EU Commission. Consequently, it functions as a gateway to the remaining three technical building blocks. The trustworthiness analysis initiates with the characterization of the AI application, encompassing an ethics-based assessment, along with integral safety and security assessments.

The second building block is the AI assurance, designed to address the AI-specific guidance relevant to AI-based systems and encompassing two primary areas. It first defines the notion of learning assurance, as a recognition that the existing development assurance methods are insufficient for covering the unique learning processes inherent to ML. Secondly, explainability focuses on the ability to give human users understandable, reliable, and pertinent information, including the appropriate level of detail on how an ML application generates (or has generated) its outcomes. This building block also covers the continuous monitoring of the AI-based system's safety and the support for incident or accident investigation.

The third building block is the human factors for AI, presenting essential guidance to address the specific human factors requirements associated with the integration of AI. Again, it covers the explainability of the AI application results, but this block also introduces the concept of human-AI teaming, emphasizing the need for effective cooperation or collaboration between human end users and AI-based systems to achieve defined goals.

The fourth building block concerns AI safety risk mitigation and acknowledges the fact that it may not always be possible to fully disclose the AI black box as needed. Consequently, addressing the residual risk associated with this limitation becomes essential to manage the inherent uncertainty of AI.

#### 2.2.1.3. Learning assurance process -AI assurance

In the context of this work we are mostly interested in the learning assurance process, which is part of the aforementioned AI assurance building block. The learning assurance concept aims to offer assurance regarding the intended functionality of the AI-based system.

To elucidate the envisioned learning assurance procedures, EASA concept papers proposed a new W-shaped development cycle for ML items, depicted in Figure 2 The learning assurance process adopts the ideas from the lifecycle of neural networks presented in Section 2.1.1. The first V cycle is dedicated to the learning phase of the neural network: it contains guidelines ranging from the pre-training data management to the learning process verification, which is concentrated in evaluating the generalization capacity and robustness of the resulting trained models. The second V cycle is dedicated to the inference phase: it encompasses orientations concerning the inference model implementation, the verification that the inference model preserves the trained model's properties and its integration within the ML constituent.

Finally, as the focus of this thesis is the safe inference model implementation, we highlight the points evoked in the learning assurance process concerning this stage. In particular, the EASA guidelines provide a preliminary list with the following topics to be addressed:

(i) Requirements capture: the ML constituent requirements referring to the implementation process must be captured, including safety, functional and non-functional requirements. It may encompass demands originating from the learning phase, such as the model expected accuracy, as well as requirements concerning the adaptation to the deployment environment resources.

(ii) Trained model transformation: any post-training model transformation must be identified and validated for its impact on the model behaviour. The environment (i.e. software tools and hardware) necessary to perform the model transformation must also be detected.

(iii) Inference model development: once the trained model transformations are validated, development assurance processes to implement the inference model into software or hardware items must be prepared. In this instance, established certification standards (e.g. DO-178C for software and DO-254 for hardware) should be able to cover the defined objectives.

In summary, efforts are being made to standardize the use of AI in the avionics domain. The new ARP6983 standard is supposed to be placed in between and interface with the existing standards at systems (ARP4754B) and items (DO-178C and DO-254) levels. Extensive research exists on how to train and verify AI-based systems, which are outside of the scope of this thesis. On the other hand, considerations on implementing the inference model lead back to the use of the DO-178C for traditional software items. Hence, in the next section we elaborate more on what is expected in the DO-178C standard concerning the development of software items for avionics systems.

#### 2.2.2. Guidance for software development in avionics systems

For compliance with the DO-178C, a software item must be verified against both functional and nonfunctional requirements.

Functional requirements in a software item are associated to the correctness of a produced output given an input and an underlying computation environment. The validation process of these requirements demands evidence to demonstrate that the function performed by the code has been verified adequately with respect to the system's high and low-level requirements. It must be true both when operating with normal range inputs and conditions, but also in the presence of abnormal conditions and faults, which corresponds to assessing robustness. In addition, aviation regulations specify that avionics software must exclusively incorporate intended aircraft functionality. Thus, requirements traceability, and the validation of traceability links, is an important mechanism to ensure that only the intended functionality is implemented.

A traditional way, outlined in the DO-178C, of verifying functional correctness is requirements-based functional testing, either manually or automated with specialized tools. However, if one wants to rely on automated testing, the tool must also be qualified, as stated in the ED-215/DO-330 [68] complementary standard. In its most recent version, the standard also recognized, through the ED-216/DO-333 [69] supplementary document, the use of formal methods, such as model-checking and abstract interpretation, as a valid means of verifying avionics software functional correctness.

Non-functional requirements, in contrast, reflect quality goals that the software item should meet. In safety-critical software, an important non-functional requirement is timing predictability, i.e. the capacity to determine tight bounds on its execution times [149]. Nonetheless in the particular case of embedded avionics software, we can also cite as a requirement an efficient management of the available resources, comprising memory usage, computational power and energy consumption. Besides, software maintainability is also crucial, so its design must follow a modular structure to guarantee supportability, facilitate possible adjustments and allow reusability.

In the DO-178C, the verification of non-functional requirements commonly involves a blend of testing, reviewing, and analysis. Testing includes verification of the expected behaviour in normal and atypical conditions. Reviewing offers a qualitative evaluation of correctness and analysis provides reproducible evidence of correctness. In particular, the DO-178C explicitly states the need of a timing analysis to derive safe guarantees for the worst-case execution time (WCET) of each software component and prove its timing predictability. However, no restriction is imposed on the type of WCET analysis technique used, as long as it provides strong certification arguments. We elaborate more on timing predictability in Section 2.4.3.

Definition 2 (Worst-case execution time (WCET)). The WCET of a software item is an upper bound on its execution time when running on a specific hardware item.

### 2.3. Derived certification objectives for implementing the inference model

Regarding the presented constraints underlying safety-critical systems, we identified a number of quantifiable objectives necessary to guarantee the safe and correct implementation of a trained neural network into an inference model. These objectives clearly do not represent all of those requested by the normative standards, but were recognized as complex to obtain for machine learning software in its current state and are in accordance with the guidelines under construction -EASA roadmaps and ARP6983. Objective 1 (Precise description of the inference model). Prior to the inference phase, the inference model must be described with a formal, unambiguous and human-readable specification.

At the end of the learning phase, once the trained model is validated against its requirements, such as robustness, stability and generalization capability, it is converted in the inference model. The description of the inference model should encompass all, and only, the elements needed for its accurate implementation, omitting any metadata intrinsic to the learning phase.

Thus, a complete description must include the inference model semantics, i.e. the characterization of the directed acyclic graph structure and the formal semantics of the operations performed by each node of the graph, as well as the data of the learnt parameters.

## Objective 2 (Semantics preservation of the inference model). For any input, the output of the code running on the target hardware should be identical (given perfect real numbers representation) to the one obtained in the training environment.

Once the inference model semantics is defined, i.e. the structure of the directed acyclic graph, the mathematical functions performed by the trained model and the learnt parameters are formally and unambiguously described, the software developer must guarantee that it is preserved until the executable file. Post-training model transformations are allowed during the implementation of the inference model, as long as they do not affect the inference model semantics.

Objective 3 (Requirements traceability). One must ensure traceability between the high-level requirements of the machine learning constituent, the inference model source code and the associated executable file.

This objective ensures that the requirements pertaining to the machine learning constituent are faithfully implemented in the inference model and ported on the target hardware.

Objective 4 (Timing predictability of software item). The software developer must compute the WCET (Worst-Case Execution Time) of every software item composing the avionics system, including any machine learning item, for the corresponding hardware item.

As mentioned, this objective is clearly requested in the DO-178C as a means to guarantee that the avionics systems are timing predictable. Having guarantees on the (theoretical) maximum execution times of the software items is important as it allows for a better dimensioning of the systems. The reason why we select this objective in particular among all the requirements listed in the standard is because given the novelty around the machine learning software there was uncertainty about the feasibility of computing worst-case execution time bounds for it.

Objective 5 (Efficient resource usage). The software developer has to provide evidence that the resource usage of the software item has been considered and analysed, notably in terms of memory usage and timing requirements.

This objective is also listed in the DO-178C for any software present in avionics systems, which is logical considering the embedded resource-constrained environment. We note that besides the worst-case execution time guarantees, consideration must be given to average execution time as well.

### 2.4. Identified challenges to answer the certification objectives

The techniques and methodology applied when implementing software items in safety-critical systems can drastically affect the certification process overall. Implementation decisions must seek to enable, or simply facilitate, the verification of both functional and non-functional requirements. Hereafter we present considerations regarding the implementation of the inference model with respect to the previously introduced certification objectives.

#### 2.4.1. Machine learning framework

The different phases of a neural network lifecycle are performed in programming environments called machine learning frameworks. There is a consequent number of machine learning frameworks in the literature. There exist ML frameworks specialized in the learning phase, such as TensorFlow [6] and PyTorch [143]. In contrast, other ML frameworks are focused on the inference phase, providing optimized executables for a specific deployment target. Examples of inference ML frameworks include TensorRT [137], KaNN [100] or ONNX Runtime [59]. Further details about the existing ML frameworks and their particularities are given in Chapter 3, while in this section we discuss the difficulties in obtaining a precise and unambiguous description of the inference model as required by Objective 1.

Although a neural network model essentially implements known mathematical functions, they happen to be interpreted differently according to the ML framework used, as very little formalism is present in the evolving machine learning domain. Many studies examined the great disparity in the design choices of popular ML frameworks, both in the learning and in the inference phases. In the work of [127], [156] and also [83] the authors performed experimental benchmarking of some ML frameworks and showed that each framework has its own default configurations settings, which are little, or not at all, documented. The impact of framework-dependent parameters in the learning phase is, for example, very different models accuracies when using the same training data set and training algorithm. While on the inference phase it greatly affects the inference time and the usage of hardware resources, notably memory resources.

The authors of [128] and [141] went deeper on studying the differences in the way the various frameworks present the inference model after the learning phase and pointed out a few investigation leads. The first observation was the use of different mathematical operators and default parameters to implement the, in principle, same layer's function. They also noted the adoption of distinct conventions to store the data of the learnt parameters and the data of the multi-dimensional arrays exchanged between the layers. Lastly, according to their optimization choices, the different frameworks may modify the structure of the directed acyclic graph accordingly, by merging or splitting layers nodes. In Chapter 5 we elaborate more about these design choices.

Moreover, it is not uncommon that each ML framework uses its own format to store the description of the inference model to be implemented [141]. Summed with the aforementioned disparities in the representation of the trained neural network, it burdens the task of exporting the inference model from a training ML framework and reusing it with a distinct inference ML framework, characterizing a lack of interoperability among the existing ML frameworks. These observations accentuate the importance of a description of the inference model in a formal, unambiguous and human-readable format, to guarantee that its intended functionality is met after implementation.

#### 2.4.2. Transformations in the inference model

Regarding Objective 2 we must track any transformations done in the inference model. In this context, we can reference modifications required to adapt the trained model to the environment of the inference phase. Such transformations may aim to optimize the trained model in order to reduce its complexity focusing on an embedded system and an optimal use of its resources, notably computation power and memory resources. It could include merging subsequent layers in the directed acyclic graph, such as dense and activation layers, or yet implementing the convolutional layer with customized algorithms (e.g. GEMM-based convolution). Both of these authorized optimizations, i.e. that do not alter the semantics of the inference model, are detailed respectively in Chapters 4 and 6.

#### 2.4.3. Timing predictability

To clarify Objective 4, we present some concepts on timing predictability. As defined in [149], the timing predictability of a system is a measure for the feasibility of determining tight bounds on the execution times of its programs. In this context, a program is equivalent to a software item in the avionics nomenclature.

Assumption 2 (Timing behaviour of a program in isolation). We analyse a program running alone in a single-core processor, without interruptions or preemptions. Hereafter, our program of interest is the inference function.

A real-time program exhibits variability in its execution times notably in function of the values of the input variables, named input state, and the initial values of the hardware state variables, called hardware state. Figure 2.9 illustrates some pertinent properties of a real-time program. The comprehensive set of execution times is represented by the darker upper curve, wherein the shortest execution time is called the best-case execution time (BCET) and the longest execution time is designated as the worst-case execution time (WCET). The lower curve shows a subset of measured execution times, with its minimum and maximum values corresponding to the minimum and maximum observed execution times, respectively. The typically large state space, i.e the set of all configurations of the system given the input and hardware state, makes it often impractical to thoroughly explore all potential executions. It can be thus very difficult to precisely ascertain the exact worst and best-case execution times. The process of describing the execution times of each program when running on a given hardware platform is called timing analysis and we are particularly interested in the worst-case execution time (WCET) analysis. Three main methodologies exist for analysing the worst-case execution time and are detailed hereafter: static techniques, measurement-based techniques and hybrid techniques. The primary criteria for assessing a method for WCET analysis are safety, which refers to whether the produced value is indeed an overestimation of the actual value, and precision, indicating how close the estimates are to the exact values [185].

#### 2.4.3.1. Static analysis

Static WCET analysis techniques aim at deriving bounds for the worst-case execution time of a given program on a target platform without actually executing the program, relying rather on abstraction. This approach essentially combines an analysis of the code for the program, together with some information about input data and an abstract model of the hardware. A typical static analysis of a program's WCET involves three primary steps [184,185] and is depicted in (i) Control-flow analysis, which seeks to identify all feasible paths of the program. In this phase, information about the program's control flow are obtained from the binary executable, from which the control-flow graph (CFG) is reconstructed. A set of flow-facts about the transitions of the CFG can also be derived, either from analysis performed on source or binary code, or yet from manual annotation provided by the program developer, such as values for loop bounds. This first step identifies basic blocks, which are sequences of instructions, for which the instruction flow has only a single entry point and a single exit point.

(ii) Processor-behaviour analysis, which serves to determine an estimate for the program's execution time on the feasible paths. This stage employs static analysis techniques, including abstract interpretation, to analyse specific hardware features such as pipelines [115], data and instruction cache memories [73,130], and branch predictors [41] and thereby determine bounds on the execution times.

(iii) WCET computation, which consists in combining the bounds of the execution times of the basic blocks to find the longest path through the program, which is then used to derive an upper bound on its WCET. This step usually employs the Implicit Path Enumeration Technique (IPET) [124] to define the problem of finding the longest path as an integer linear program (ILP).

In static analysis, hardware and software properties that cannot be precisely determined must be conservatively approximated. This approach may introduce some pessimism and the proposed WCET bound usually overestimates the exact WCET and underestimates the BCET, as observed in Figure 2.9. Thus, provided that the abstract hardware model is an accurate characterisation of the timing behaviour of the real hardware platform and the data flow is well defined, static analysis derives safe upper bounds on the WCET of a program.

Because of its safety guarantees this method is the preferred one for use in safety-critical real-time systems [185] and there is a number of tools that implement the principles of static analysis. Examples are commercial products, such as aiT [72] by AbsInt, and academic initiatives, such as OTAWA [21], Heptane [85], Chronos [123] and SWEET [126].

#### 2.4.3.2. Measurement-based analysis

Measurement-based timing analyses consist in executing the program on top of the actual hardware platform and collecting the measured execution times to afterwards derive WCET estimates. Within measurement-based methodologies there are two main techniques used to obtain WCET estimates from the collected measured times, they either: (i) apply a safety margin to the maximum observed execution time or (ii) use statistical techniques, such as extreme value theory (EVT) [53], to model the distribution of the highest observed execution times and notably detect extreme deviations from the median in the probability distribution. This analytical approach is known as probabilistic WCET (pWCET) estimates [31,48].

The main advantage of measurement-based approaches is providing less pessimistic estimates, since they are based on actual program executions and can capture the system's dynamic behaviour. However, during testing the user must manage to capture the worst-case scenario. It includes notably preparing a test input state which ideally contains the input leading to the WCET and also combining various unfavourable hardware states. Moreover, one must consider the effects of an intrusive instrumentation, which happens for example when extra code is added or the hardware timing is modified in the measurements collection process. As consequence, since measurement-based approaches might not cover the absolute worst-case scenario, they can be considered not sufficient for safety-critical real-time systems.

#### 2.4.3.3. Hybrid analysis

Finally, hybrid timing analysis techniques combine concepts from both static and measurement-based methods to estimate the worst-case execution time [25]. This strategy replaces the hardware abstraction phase with timing measurements taken during testing but keep certain elements of the static analysis process, such as the control flow graph analysis, to provide WCET estimates for unobserved execution paths. Examples of hybrid solutions for WCET estimation are Rapitime [163] by Rapita and Timeweaver [103] by AbsInt.

These techniques have the potential to yield more precise WCET estimates when compared to static analysis and may increase the trustworthiness with respect to measurement-based approaches since some analysis is added into the computation of the WCET estimate. Nonetheless, the efficacy of this approach relies on finding a suitable equilibrium between the previously two categories and usually requires a good understanding of how the program under analysis interacts with hardware features. Assumption 3 (Use of static analysis for WCET estimation). In this work, we adopt static WCET analysis to obtain upper bounds for the worst-case execution time of the inference model. Indeed, the mathematical foundations of static analysis offer a robust foundation for certification arguments. To accomplish this, we use the tool OTAWA, which is described in detail in Chapter 5.

We precise that there is no extra difficulty in obtaining WCET bounds for the execution time of an inference model, considering it is in principle a predictable program, with loop bounds that do not depend on input data. Thus, the same challenges present for traditional software items apply. In the following sections we elaborate more about them.

#### 2.4.4. Programming language

A crucial decision influencing the development of safety-critical software is the selection of the programming language. Indeed, the inclusion or exclusion of specific language features can significantly ease or complicate the certification process. It can notably affect Objectives 3 and 4.

Real-time systems must employ a limited programming approach to support a deterministic execution, ensuring that the timing behaviour of the system is predictable and consistent. Moreover, programming abstractions and functionalities known to ease the software design and implementation may hinder the timing predictability of the produced program. These include dynamic data structures, such as pointers to data and functions that cannot be statically resolved, or more generally, dynamic memory allocation [185]. Indeed, dynamic memory allocation adds uncertainty about the nature of memory accesses and burdens the prediction about the needed execution time. These observations are notably true for a static WCET analysis.

Thus, hard real-time embedded systems are traditionally implemented using low-level programming languages, such as Ada [7] or C [97]. Ada has demonstrated its suitability as a foundation for safetycritical subsets, as exemplified by SPARK [8]. SPARK is a formally defined programming language that strengthens the specification capabilities of Ada by the addition of contracts for data dependencies, information flows, state abstraction and, data and behaviour refinement, in a form that is suitable for static verification. Additionally, Ada compiler implementations have been tailored to meet the requirements of the safety-critical systems, with various compile-time checks to detect problems before run-time.

The C language is theoretically less secure than Ada, with the presence of undefined behaviours, errorprone particular syntax and type checking flaws [97]. Nevertheless, an advantage of C as a language is its considerable maturity, resulting in extensive analysis and practical testing. As a result, its problems are well-documented and understood. Additionally, a great number of commercial and academic tools is available to support the language, helping the verification of this code. Furthermore, to observe safety compliance one can rely on the MISRA-C [133] recommendations, which is a set of software development guidelines for the C programming language. These guidelines provide a widely accepted model for best practices aiming to mitigate C language vulnerabilities and faulty characteristics. The DO-178C does not determine its adoption but relying on the MISRA-C coding rules should facilitate the certification process.

Assumption 4 (Adoption of C language as the programming language for the inference model). In this work, we use the C language because of its maturity and existing support. We eliminate the use of dynamic memory allocation or any dynamic structure capable of introducing dynamic behaviour.

#### 2.4.5. Compiler

The compiler used to transform source code in binary code and also the compiler options employed can directly impact Objectives 4 and 3. A compiler may apply different optimizations and modifications to the program, such as loop unrolling, instruction scheduling, dead code elimination, and function inlining, to cite a few. These optimizations have as main objective to improve the average execution time of the program.

As explained in Section 2.4.3, static WCET analysis techniques operate upon the code of a program as part of the process to obtain WCET estimations and compilers optimizations may drastically change the flow information of the program, requiring, for example, changing the annotated loop bounds [46]. Furthermore, if the final binary representation significantly deviates from the original source code, establishing a mapping between the two instances may become exceedingly challenging, both if done manually or with the use of specialized tools, thereby complicating traceability. In addition, the DO-178C states that for highly critical (e.g. DAL-A) software, it is also necessary to verify any additional code that is introduced by the compiler.

To facilitate the certification task one can rely on formally verified compilers [113] or depend on generic widely-used compilers, but carefully using compiler optimizations.

Assumption 5 (Use of GCC compiler without optimizations to obtain the inference model binary). Within the scope of this thesis, we use the GCC compiler because of its popularity and support for various hardware architectures. Moreover, we adopt the conservative approach of using no compiler optimizations (-O0 flag).

#### 2.4.6. Hardware platform

The architectural features of the hardware platform also greatly impacts the capacity of achieving certification compliance, especially Objective 4.

General purpose single-core commercial off-the-shelf (COTS) processors, and specialized architectures such as field programmable gate arrays (FPGA) and application-specific integrated circuits (ASIC) are covered by the existing guidance for hardware items (DO-254) [114], with some additional guidance given in the AMC 20-152A [64] document. With the wide availability of multiple core (multi-core) processors, their reduced space, weight and power (SWaP) properties [107], they started being considered for use in the avionics context. A position paper named CAST-32A [9] was introduced in 2014 and complemented by the later in 2022. The goal was to identify topics that could impact the safety and then provide objectives to guide the production of avionics software systems executing on multi-core processors.

However, the intricate nature of multi-core architectures renders the certification process considerably more challenging and one of the main difficulties is performing static WCET timing analysis of programs running on different cores but sharing hardware resources, such as interconnect buses and memory caches. Indeed, precise information about the functional and timing behaviour of the processor hardware is required to accurately evaluate the timing effects of contention arising from accessing shared resources, which may be very hard in COTS multi-core processors [10].

More recently, graphics processing units (GPU) devices have captured the interest both from academia and industry. These are specialized processors built with a large number of small cores that can perform parallel processing simultaneously. Originally designed to accelerate the rendering of images and videos in computer games, GPUs have evolved to become powerful processors capable of handling a wide range of computational tasks beyond graphics and are used in various domains such as scientific research, highperformance computing and naturally, artificial intelligence.

Recent works have started investigating the use of GPUs in safety-critical domains, such as avionics [24], space [110,187] and automotive [11]. Nevertheless, the challenges to provide real-time guarantees observed in multi-cores are also present in GPUs. They are due to the partial understanding of GPUs temporal behaviour, powered by the complexity of the micro-architectures, the presence of particular execution models resulting in great execution variability [138] and temporal interference due to complex shared resources strategies [30]. Moreover, their closed proprietary designs [142,191] impair the development of hardware abstract models and techniques for static WCET timing analysis [108]. Finally, GPUs devices have their own programming languages and frameworks for parallel computing, which are not-compliant with safety standards [11,173].

At the time of writing this document, no official standard or guidelines exist concerning the use of GPUs in avionics systems.

Another existing data processing approach are vector extensions, which are integrated in modern COTS processors. Vector extensions are functional units implementing SIMD (single-instruction multipledata) instructions, which process in parallel and independently distinct data elements arranged into vectors. Vector instructions have the same structure as a scalar instruction, i.e. a mnemonic, source register(s), and a destination register. The particularity is that vector registers can accommodate multiple values of different sizes and types. Thus unlike scalar instructions that operate on one element at a time, vector instructions exploit data-level parallelism.

In the work of [147], the authors studied the viability of using vector extensions in safety-critical realtime systems with respect to the certification challenges. They concluded that it is the data processing paradigm that will likely be more rapidly adopted in the development process of high-integrity systems, as they introduce a degree of parallelism, providing performance enhancement (in terms of execution time), without many of the challenges present in multi-core processors and GPUs. They cite notably the absence of race condition questions and the advantage that their operation can be fully mastered and timed. Furthermore, vector extensions can be considered as a mature technology as they have been present in various processor generations by all major vendors.

In Chapter 6 we present and discuss our work on improving the execution time of the inference task using vector extensions.

Assumption 6 (Single-core bare-metal implementation of the inference model in a COTS processor). Within the scope of this thesis, we chose to deploy the inference model in a multi-core COTS processor, which is further detailed in Chapter 5. We, however, rely on a single-core bare-metal implementation to better isolate the challenges that are particular to the inference model.

### 2.5. Conclusion

In this background chapter we highlighted the essential concepts about feed-forward deep neural networks that are necessary for the discussions of the next chapters. We presented the lifecycle of a neural network and introduced the definition of the inference model.

Subsequently, we presented the certification constraints inherent to the development of avionics systems. We gave an overview of the existing initiatives aiming to provide safety guarantees concerning the implementation of artificial intelligence in aeronautical safety-related products and we then focused on the requirements related to software items.

Afterwards, we introduced the certification objectives fixed in this thesis concerning the implementation of the inference model. Finally, we discussed what are the practical encountered challenges to answer the defined certification objectives with respect to machine learning software.

In the following chapter, we present the state of the art on frameworks and tools for designing and implementing neural networks in embedded systems. We then discuss their compliance with our requirements concerning avionics systems.

## Chapter 3

## Background: Machine learning frameworks

This background chapter presents the state of the art of the programming environments, or frameworks, used both for the learning and inference phases of machine learning applications. This bibliography is a necessary step before any choice concerning a certifiable implementation of the inference model. Section 3.1 introduces the most commonly used ML frameworks for the learning phase of neural networks and their main characteristics. Section 3.2 presents the existing frameworks to implement and deploy the inference model, with a focus on resource-constrained embedded systems. We also analyse whether these solutions are suitable for use in safety-critical real-time systems, in particular in aeronautical products. We then focus on two frameworks that propose a static runtime in C language for the inference model implementation, which is in accordance with our assumptions, and are later used for benchmarking our work.

### 3.1. Machine learning frameworks for the learning phase

The learning phase of neural networks is not in the scope of this thesis, but since we want to implement an inference model that has been trained on a machine learning framework, it is imperative to understand how these work. As briefly mentioned in Section 2.4, various frameworks dedicated to the learning phase of neural networks exist. These are intended to facilitate the developer's work of designing, training and verifying neural network models. Consequently, they often do not extensively describe all the inner operations that are performed.

To achieve the objective of providing a certifiable implementation of an inference model, we want to be agnostic and independent of the learning environment. It is thus essential to know exactly what is needed to reconstruct the inference model in the deployment environment. Moreover, we must be able to extract all, and only, the necessary information from the representation format used by the learning framework to export the trained model. Hence, the crucial aspect lies in understanding the inference model semantics as well as its representation format, in order to guarantee a correct and certifiable implementation.

Hereafter we present three of the most commonly utilized ML frameworks for the learning phase and their particularities. We note that our objective is not to determine if a ML learning framework is better than another, as this decision depends on the user preferences and on the requirements associated to development and deployment phases.

In the next subsections we adhere to the following template to present frameworks used in the learning phase: (i) main purpose and specificities, (ii) programming language, (iii) learning hardware targets, (iv) community, (v) auxiliary tools and (vi) export format.

#### 3.1.1. TensorFlow

TensorFlow [6] is an open-source machine learning framework developed by Google. It offers flexibility in building various machine learning models, including neural networks, for tasks such as classification, regression and clustering. Moreover, it supports both high-level and low-level application programming interfaces (APIs), for either easy model designing and training or for maximum customization of the learning process. TensorFlow has APIs available in several programming languages, such as Python, JavaScript, C++ and Java, both for constructing and executing a TensorFlow model. The hardware targets supported by TensorFlow learning routines include CPUs and GPUs. TensorFlow has a very structured approach, inherited from its original declarative programming style, which is beneficial for industrial environments where models must be scalable and highly optimized. However, its most recent version also supports dynamic computation graphs, allowing for more flexibility and easier debugging, thus making it also accessible for research purposes. Built-in visualization tools like TensorBoard facilitate the model graph visualization, the learning progress monitoring, and the analysis of learning performance metrics. TensorFlow has a vast ecosystem of libraries and tools built on top of it, including TensorFlow Lite for deploying models on resource-constrained devices, further detailed in Section 3.2.2.1. Lastly, TensorFlow benefits from a large and active community of developers and researchers who contribute to its development, provide support, and share resources such as tutorials, code samples, and pre-trained models.

TensorFlow trained models can be exported from the framework in the format of Protocol Buffers, or Protobuf [57], files. Protobuf is a format used to serialize structured data. Data represented as series of key-value pairs is serialized into a binary format, designed to be compact, fast to parse and compatible across various object-oriented programming languages. Thus, the trained model saved in a Protobuf file stores a serialized description of the computations done by the model, with a set of named signatures, each identifying a function with multi-dimensional inputs and outputs. It also contains the values of the trainable parameters. The main limitations of relying on Protobuf to our usage is the need to have a dedicated decoder API to extract the fields from the binary serialized data into multi-dimensional arrays with their correct context. Moreover, the output format does not include any direct link to the semantics of the neural networks layers' operations: the person responsible for implementation must read the documentation that is often incomplete.

#### 3.1.2. PyTorch

PyTorch [143] is an open-source machine learning framework developed primarily by Meta. Similar to TensorFlow, PyTorch provides a platform for designing, training, and deploying machine learning models for diverse ML tasks. It supports high-level APIs for multi-dimensional arrays computation with routines for specialized processors (e.g. GPU), but also low-level APIs highly integrated with classic Python libraries for numerical and scientific computing, such as NumPy and SciPy. In addition to the classic Python API, PyTorch also has a C++ API that can be used both in the learning and inference phases of machine learning models. PyTorch supports learning in both CPU and GPU hardware targets. PyTorch is highly popular in the research community due to its ease of use, Python-styled philosophy, and support for imperative programming, which makes debugging and experimentation straightforward. Although it also integrates acceleration libraries such as Intel MKL, NVIDIA cuDNN and NCCL to improve training speed, rendering it suitable for industrial applications. PyTorch also provides modules allowing to log various data such as scalar values, images, histograms, and model graphs to TensorBoard. Like TensorFlow, PyTorch features a broad ecosystem of tools for processing image, text and audio data. In addition, it develops PyTorch Mobile, a tool for the deployment of ML models on embedded processors, currently in its beta version. Finally, PyTorch has a strong community support and its official website provides an extensive documentation.

Neural networks trained within PyTorch can be saved in the format of serialized dictionary objects, using either a .pt or .pth file extension. One can either save the entire model with its parameters, structure, and all necessary information to retrieve it for inference, or only save a dictionary mapping the trainable parameters to their respective layers. Both of these options use pickle [174], which is a Python module implementing binary protocols for serializing Python objects. However, PyTorch binary representation can only be exploited within the framework and no built-in API is available to decode it into a humanreadable format. Like, TensorFlow, the output format for PyTorch models does not contain the semantics of the supported neural network layers.

#### 3.1.3. Keras

Keras [38] is not a machine learning framework per se, but a high-level multi-framework API. Originally built on top of TensorFlow, its latest version (Keras 3.0) can also be used to develop models compatible with PyTorch and JAX [27] back-ends. Keras' proposal is to offer a modular approach, with an intuitive interface for designing and training neural networks. Its high-level API abstracts away much of the complexity of machine learning techniques, making it accessible to beginners and experienced practitioners alike. However, it also supports custom layers, loss functions and metrics, enabling users to experiment with new training procedures or state-of-the-art model architectures. Moreover, within Keras it is possible to dynamically select the back-end used to train and perform inference without having to change the code. This technique facilitates the evaluation of performance metrics, such as the highest achievable efficiency, and also favours the distribution of models that have been pre-trained within the framework. Like TensorFlow and PyTorch, Keras has an active community and disposes of abundant resources and tutorials. Keras is widely employed in research due to its ease of use, while its adaptability regarding the choice of back-ends also makes Keras valued in industry. Keras relies on a H5-based [169] file format to represent the output of the learning phase. A H5 file, short for HDF5 (Hierarchical Data Format Version 5), is a format to serialize structured data in binary form. It is yet another format different from the ones used by TensorFlow and PyTorch. Keras 2.0 relied, by default, on a single H5 file to store the structure of the trained model, the set of trainable parameters and also other training-related information such as the optimizer, losses and evaluation metrics. But the user could also export the structure of the trained model to a JSON-based, human-readable, format trough a built-in method. The generated JSON file would not include the set of trainable parameters though. Keras 3.0 now outputs the trained model in an unified format, .keras extension, which is actually a ZIP archive. It contains a different JSON-based configuration file with records of the model and layers, a H5-based state file with directory keys for layers and their trainable parameters, and a metadata file in JSON.

Because of its user-friendly interface and many available resources we adopted Keras for the learning phase of the neural networks we experimented with, presented in Chapter 4.6. Hence, the results of the inference pass performed within Keras are considered the ground truth, or reference, outcomes that we aim to replicate within ACETONE, as will be detailed in Chapter 5.

#### 3.1.4. Common format for representing trained models

As each ML framework uses its own format to store the description of the inference model to be implemented, there are portability and interoperability issues to be addressed [141]. In addition to this, we must note the fact that the frameworks documentations are diffuse and incomplete. Based on these observations, a few works have arisen to try to tackle these problems. Hereafter we enumerate three examples.

The first format is named NNet [162]. It is a simple text-based format to define feed-forward, fullyconnected (i.e. containing only dense layers), ReLU-activated neural networks. The .nnet file format was originally created in 2016 to describe the ACAS-Xu trained models (see Section 4.6.1) in a humanreadable text document. The project was then later incorporated into the Reluplex [105] repository, a SMT solver for verifying deep neural networks, and is now used to define benchmark networks. The NNet text file has a well defined template containing information about the network architecture, the required normalization of inputs, and the model trainable parameters of each layer. This format is very understandable and agnostic from learning framework, and although it does not contain the semantics of networks layers they can be easily retrieved as it only expresses dense and ReLU layers. However, for our use case the main disadvantage is precisely the fact that NNet only supports a very particular type of neural networks.

The second work is NNEF [170] (Neural Network Exchange Format), a project led by Khronos Group, a consortium for the definition of open standards. The NNEF format encapsulates a complete description of the structure, as well as the operations and trainable parameters of a trained neural network. Its main objective is to have a format independent of both the learning framework and the inference environment on which it will be executed. An NNEF description is composed of two parts: (i) the directed acyclic graph defining the computations to be performed described in a human-readable text file; (ii) the model trainable parameters provided in multiple raw data files. The fact that the directed acyclic graph description is textual is important for the traceability between the specification and the inference model implementation. Moreover, the NNEF specification also provides a direct link between operations (e.g. layers) appearing in the description file and their associated mathematical functions. However, the authors of [76] showed that the NNEF specification still misses a clear formalization of the execution model, that is, a definition of the formal behaviour behind a series of NNEF instructions. The authors then proposed an extension to describe the execution model using the Petri net formalism. Nevertheless, as of the writing of this thesis, the NNEF project seems, unfortunately, no longer maintained.

Lastly, we must also cite ONNX [20], which stands for Open Neural Network Exchange. ONNX is an open-source standard for representing trained machine learning models. It serves as a common intermediate representation, based on an extensible Protobuf schema, that enables interoperability between different machine learning frameworks. With ONNX, it is possible to train a model using one framework (e.g. TensorFlow or PyTorch) and then export it to the ONNX format. Once in ONNX format, the model can be imported into and executed by other frameworks that support ONNX, such as TensorFlow, PyTorch, ONNX Runtime [59] and MATLAB Deep Learning Toolbox [171]. It is the exchange format that offers a greater number of APIs for importing to and exporting from training frameworks In summary, ONNX allows models to be easily transferred across different environments without the need for extensive model conversion or retraining. Moreover, ONNX documentation defines the semantics of the neural network layers supported. However, the main challenge concerning the ONNX format is that it is a binary representation and requires a dynamic interpreter to be exploited. In 2023, a group of researchers interested in the use of ML within safety-critical systems, including ONERA, have convened to develop an embeddable and certifiable profile for the ONNX format, aiming to contribute to the ONNX project as a working group. A working group in the ONNX project is a temporary group formed to address issues that go beyond the general interests of the project's community and governance [139]. At present, the group is engaged in defining the needs for the ML model description format according to the ARP6983 (see Section 2.2.1), deciding on the format specifications and planning their contribution in the form of deliverables to the community. It is a valuable initiative that could complement our work in the future.

### 3.2. Machine learning frameworks for the inference phase

After the design and training of the neural network with the machine learning training framework, the next phase is the implementation of the inference model from the output format description. This study of the state of the art is important for assessing the compatibility of existing inference frameworks with certification requirements. As a reminder, the certification objectives derived in Chapter 2 are: (i) Objective 1: a precise description of the inference model in a human-readable format;

(ii) Objective 2: the preservation of the inference model semantics; (iii) Objective 3: the traceability between high-level requirements and final inference model executable; (iv) Objective 4: WCET bounds computation.

Moreover, we also presented Assumption 3 (static WCET analysis), Assumption 4 (use of C language) and Assumption 6 (single-core implementation).

Again, there exist many machine learning frameworks dedicated to the inference phase. These frameworks exhibit diverse configurations and functionalities, but they primarily focus on optimizing the inference model to improve the average execution time. The majority of inference engines follow a common compiler structure: (i) the front-end converts a trained model into an intermediate representation (IR) and (ii) the back-end then generates a machine-code of the inference model optimized for a given target.

The trained models consumed by inference engines are usually the serialized representation output from the learning frameworks aforementioned (e.g. Protobuf, H5, ONNX). Most toolchains use a two-level IR: the high-level IR is a graph-level representation of the inference model and the low-level IR describes the implementation details of the mathematical functions [159].

The high-level IR is typically used for target-independent optimizations, such as layer's fusion. Once the optimizations applied, high-level layers nodes are lowered to basic linear algebra operations nodes. The low-level IR is used by the back-end to optimize the individual layers by applying for example memory-related optimizations, such as instruction scheduling, static memory allocation and code copy elimination. The inference model is then integrated into a runtime, i.e. the collection of functions that performs the inference task by managing the inputs, instantiating and executing the inference model and recovering the outputs.

We note the difficulty of making this analysis of the state of the art, as we do not find the same level of documentation or a consistent nomenclature across the various existing inference frameworks. Nevertheless, for the following discussion we chose to categorize inference frameworks into two main groups: proprietary and open-source solutions. Some of these frameworks employ an interpreter approach, relying on dynamic interpretation or just-in-time compilation to achieve efficient inference execution. Other employ a code generation approach, either exposing the inference model implementation in a source code, written in widely-used languages like C or C++, which is later compiled to suit the application requirements, or directly generating a binary file. Then we decompose each group into frameworks that fail to align with avionics requirements and frameworks that, in principle, adhere to them. Hereafter we present different approaches and analyse their suitability or lack thereof for the avionics domain.

#### 3.2.1. Proprietary inference engines

Proprietary solutions, often developed by leading technology and specialized companies, offer comprehensive tools and support for inference tasks. These proprietary frameworks may provide advanced features and optimizations tailored to improve the average execution time on specific hardware platforms. However, the internal features are often black-box.

#### 3.2.1.1. Proprietary inference engines not compatible with certification requirements

OpenVINO [93] is a toolkit for optimizing and deploying inference models on Intel hardware, including CPUs, GPUs, FPGAs, and VPUs (Vision Processing Units) [134]. More recently, a non-official support for inference on ARM CPU was released in the form of a community-level add-on [60]. The workflow of OpenVINO starts with the import of a trained model from TensorFlow, PyTorch, ONNX or Pad-dlePaddle [131]. The trained model is converted to a high-level IR (an ov.Model format), where a few customizations take place such as input reshaping, quantization or preprocessing steps before compiling the model. Then the model is compiled to run on a specific target (ov.CompiledModel format), allowing hardware specific optimizations to be made and enabling inference. Finally, inference can be run relying on OpenVINO Runtime, which is a set of C++ libraries with C and Python bindings. Even if it is specialized for Intel hardware, the source codes of OpenVINO compiler and runtime are open-source. However, relying on C++ source codes with dynamic memory allocation makes it difficult to achieve Objective 4.

Vitis AI [104] is an environment for inference acceleration on AMD adaptable platforms. The trained model can be in one of the formats obtained from TensorFlow, PyTorch or ONNX. The environment requires a host CPU (x86 or ARM) and a hardware accelerator that is composed of programmable logic (e.g. FPGA). The trained model is first converted to an intermediate representation (.xmodel format) where the main optimizations performed to reduce its complexity are pruning and quantization. The model is then compiled on the host to generate a microcode for the programmable logic fabric core of the target board. Finally the application to perform inference, which must be written either in C++ or Python, is compiled with the Vitis AI Runtime to run on the accelerator. The Vitis AI compiler or runtime are not open-source, which complicates accomplishing Objectives 2, 3 and 4. Furthermore, the toolchain is dedicated to AMD platforms.

TensorRT [137] is an inference optimizer and runtime engine designed to accelerate inference on NVIDIA GPUs. The framework accepts TensorFlow, PyTorch and ONNX trained models. First the trained model is converted to a TensorRT model format (IR), enabling inference optimizations with techniques such as quantization, layer and tensor fusion. Then TensorRT engine builder generates an optimized compiled model from the converted model. Lastly, inference is performed using NVIDIA's Runtime, based on the CUDA parallel programming model, and relies on cuBLAS library. The TensorRT compiler or runtime are also not open-source, which is unfavourable for Objectives 2, 3 and 4. Moreover, it is not compatible with Assumptions 4 and 6.

#### 3.2.1.2. Proprietary inference engines theoretically compatible with certification requirements

In the realm of proprietary solutions, we can also cite a few approaches that have been developed or seem to be readily adaptable for safety-critical applications with certification requirements. Kalray Neural Network (KaNN) [52,100] is a machine learning inference compiler targeting the Kalray MPPA3 [101] platform. This tool accepts trained models from TensorFlow and ONNX. The front-end first generates an optimized computation graph, by fusing layers and adapting arithmetic representations for example. Then the code generator process defines a collection of OpenCL binary kernels, where each kernel interprets the contents of a static data block with a static schedule. The KaNN compiler is not freely available, making Objectives 2 and 3 difficult to attain. The static scheduling is an asset for safetycritical real-time applications (Objective 4), but the use of OpenCL language is not in accordance with Assumption 4. Moreover, KaNN only targets the Kalray platforms.

MATLAB Coder with Deep Learning Toolbox [171] implements the inference model in a C or C++ code, either generic or optimized for Intel and ARM processors. This toolchain takes as input ONNX and TensorFlow models and requires a first conversion to a MATLAB neural network object. However, no information is available about the used intermediate representations or about the possible performed optimizations. For a generic C or C++ inference code, the runtime does not depend on any third-party libraries, which is in accordance with our requirements. But for Intel and ARM specialized code the runtime relies respectively on the MKL-DNN and ARM Compute libraries. The generated inference code can be mapped to the inference model description, to achieve Objectives 2 and 3, but that requires a significant effort of reverse engineering. Moreover, MATLAB requires a paid license.

Ansys Neural Networks Package [15] is a toolchain to generate C code compatible with DO-178C requirements for an inference model. This package relies on SCADE (Safety Critical Application Development Environment) [14,40], which is both a language and a toolset specifically developed to describe and implement safety-critical applications, relying on the theory of synchronous languages for real-time applications. The generated C code is generic and does not target a specific hardware. The toolchain includes a Keras importer that generates a SCADE model from a neural network model trained within Keras. Then a SCADE library of common neural network layers and activation functions is used by the importer. Lastly, the SCADE suite generates a certifiable C code that can be deployed without relying on any particular runtime. This toolchain was not available in the beginning of this thesis. It is indeed a promising approach, but we decided to directly generate a C source code, without relying on a intermediate SCADE representation. Furthermore, we were not able to access their solution and could not evaluate the C implementation of the inference model to verify if it answers Objectives 2 and 3.

VkCoreVX [44] is CoreAVI's feature set for implementing and deploying neural networks in safetycritical environments. VkCoreVX SC is the backbone of CoreAVI's artificial intelligence and computer vision platform. It is built on top of CoreAVI's Vulkan SC implementation. Vulkan SC [82] (for safetycritical) is a specification aiming to give application developers detailed control of GPU acceleration, in order to meet safety certification standards, such as DO-178C and ISO 26262. The workflow accepts models trained within TensorFlow, PyTorch or Caffe. Trained models are translated into NNEF [170], where optimizations may take place but are not openly documented. The model is finally converted in Vulkan SC and deployed using a compatible and proprietary runtime. This framework promises to answer certification requirements such as Objectives 2, 3 and 4. However, it is a paid solution and focuses on GPU hardware that support Vulkan, thus not in accordance with Assumptions 4 and 6.

#### 3.2.2. Open-source inference engines

Open-source frameworks aim to provide an accessible manner for converting trained models from their high-level representations into compiled executables suitable for deployment on target platforms. Nonproprietary frameworks intent to accommodate a wide range of hardware configurations, offering optimizations tailored to multiple hardware architectures. However, they may often yield performance levels lower than those achievable with vendor-specific libraries.

#### 3.2.2.1. Open-source inference engines without source code generation

TensorFlow Lite [6] is TensorFlow's inference framework for running machine learning models on embedded systems, such as ARM CPUs, Android and iOS devices. TensorFlow Lite requires a special compressed format known as Flat Buffers [165], identified by the .tflite file extension. A TensorFlow Lite model can be saved with or without metadata, i.e. additional information such as required pre or post processing and supported data types. If the trained model contains no metadata, one must rely on TensorFlow Lite Interpreter API as runtime engine. Alternatively, TensorFlow also provides TensorFlow Lite Micro [47] (TFLM), designed for the specific constraints of microcontroller development. Likewise, TFLM expects a .tflite format. TFLM encodes more aggressive optimizations when compared to standard TensorFlow Lite, such as quantization to 8-bit integers and only supports a limited set of TensorFlow operators. The runtime relies on a C++ library, but TFLM is an interpreter-based inference engine. Although the execution code is static, the interpreter handles the model structure at run time, defining which operators to execute and where to obtain the model parameters from. The authors of TFLM claim that choosing this approach instead of a native code generation is preferable for the sake of portability. Relying on the C++ language and on an interpreter approach is not in accordance with our requirements (Assumptions 3 and 4). Moreover, a post-training quantization may complicate the evaluation of Objective 2.

Apache Tensor Virtual Machine (TVM) [34] is a compiler framework whose low-level IR is based on LLVM [58], an open-source compiler structure. Thus, TVM is available for any hardware that has LLVM support. It accepts as input trained models from diverse learning frameworks (e.g. Keras, PyTorch, TensorFlow, PaddlePaddle, Core ML [17]). TVM includes AutoTVM [35] in its workflow, a component to automate search-based optimization of the high-level IR. We highlight here microTVM [43], which is an extension to TVM's compiler targeting microcontrollers. The workflow is nearly the same as of base TVM, with specific changes needed in the runtime to get rid of operating-systems abstractions and support standalone model inference. First, the compiler generates the model mathematical operators implementations in low-level IR, together with the description of the model structure encoded in JSON format and simplified model parameters. For integration, the C Runtime Library is used, alongside an executor. The executor can be of type Ahead of Time (AOT) compilation or Graph parser. The AOT executor pre-compiles the inference model into a runnable function, giving no access to C source code. On the other hand, the Graph executor has to rebuild the computation graph in memory, load the parameters, and then call the operator implementations in the correct order by parsing the graph. A limitation of the Graph executor approach is the amount of memory required to parse the JSON file, contributing to the dynamic memory usage of microTVM. The authors of microTVM present the idea of an Ahead-of-Time Runtime as future work, which would generate C code to call the generated operator implementations directly, rather than relying on a graph parsing approach. An Ahead-of-Time Runtime would be in accordance with our assumptions. But for now, relying on an IR for the mathematical operators and having no access to source code complicates the evaluation of Objectives 2 and 3.

Glow [151] is a machine learning compiler and inference engine for hardware accelerators, accepting as input models from ONNX, Caffe, TensorFlow Lite. Glow supports different back-ends, such as CPU, OpenCL-supported hardware and Habana [94]. The compilation process starts with optimizations on the high-level IR of the model's computation graph, then the graph nodes (layers functions) are lowered to simpler linear algebra operations, where both target-independent and target-specific extra optimizations occur. The most developed back-end in Glow is the CPU back-end, a Just-in-Time compiler, where the lowered graph nodes are converted into LLVM-IR instructions and an optimized machine-level code is generated. The CPU back-end then addresses any CPU target that LLVM can support. Glow also supports Ahead of Time compiled executable bundles. A bundle in this context is a self-contained object file containing all the necessary code to run an inference model. The user can cross-compile a bundle from the CPU back-end of Glow for any target architecture supported by LLVM. Although very efficient, the main disadvantage of the Glow approach is that mapping the original inference model description to the machine-level code becomes challenging (Objectives 2 and 3).

Aidge [32], formerly N2D2 [26], is a framework for deep neural networks simulation, training and deployment. The platform integrates solutions for database construction, data pre-processing, neural network building, benchmarking and code generation for various hardware targets. Supported targets export include CPU, DSP and GPU with OpenMP, OpenCL, CUDA and cuDNN programming models as well as custom hardware IP code generation with high-level synthesis for FPGA. The Aidge toolchain requires a description of the inference model in a textual custom representation, named INI. This file includes information about any data processing, model layers instantiation and trained parameters. Alternatively, a simplified ONNX file can be embedded into the initialization file. The main post-training optimizations include quantization and pruning of the inference model. The reference export mode in Aidge is a C++ code generator which adopts an embedded-oriented approach: standalone C++ compliant project, relying on templates for the layers functions implementations and static memory allocation. The generation of plain C code, with no dynamic memory allocation or floating-point processing, was available in N2D2 but seems to be no longer maintained in Aidge. An ongoing project named DEEPGREEN [3], in which ONERA participates, aims to validate Aidge as a sovereign and safe platform for embedded AI.

MLIR (Multi-Level Intermediate Representation Overview) [116] is a LLVM intermediate representation which was developed with the idea to use the same IR for all compiler optimizations (hence the "Multi-Level"). It contains particular features that target machine learning applications, in particular it is possible to represent the computations of directed acyclic graph in MLIR. MLIR can be instantiated into dialects that allow putting the focus on particular aspects of the code, to specify constraints or apply specific optimizations. An example of MLIR dialect that is particularly relevant to safety-critical embedded applications is described in [146]: it enables the semantics of synchronous reactive applications inside an MLIR description. It is a very promising solution, however, to guarantee Objectives 2 and 3 we chose to adhere to the industrial workflow and thus generate C code.

#### 3.2.2.2. Open-source inference engines with source code generation

We now focus on two open-source frameworks that generate a C source code for the inference model and are characterized by a fully static runtime, featuring predictable scheduling and memory allocation. Consequently, these frameworks are better suited to answer the certification requirements presented in Chapter 2.4 and are further compared with ACETONE in Chapter 5.

#### 3.2.2.2.1. Keras2C

Keras2c [42] is a framework to generate C code from inference models serialized in the H5 Keras format. The Keras2c C back-end consists of a library of functions, relying only on the C standard library, to express a wide range of neural network layers and operators. The authors of Keras2c explain that the objective was to make the generated C code amenable for use in real-time applications, not targeting optimizations for execution time improvement. This is a hardware-agnostic inference framework as it can be used by any platform supporting C code. First, the Keras2c front-end (a Python script) iterates through the H5 file to identify the type of layers present in the model and extract the associated trainable and non-trainable parameters necessary to perform inference. Keras2c is based around the layer API of Keras, which treats each layer of a neural network as an independent function. Thus the layers' C functions are declared in Keras2c back-end library and are generic. Then the C code equivalent to the inference pass, generated by Keras2c compiler, consists in instantiating the layers' C functions in the correct sequence with their associated parameters. By default, all layers parameters are declared as local variables initialized in the source C file as well, thus being allocated on the stack section in memory. For larger models, Keras2c proposes to store the trainable parameters (weights and biases) in an external comma-separated ASCII file (.csv), to be read at run time, and use dynamic memory allocation to manage these variables. The different memory sections are detailed in Chapter 5.

Listing 1 depicts the beginning of the inference C code generated by Keras2c for the ACAS-Xu decr128 model, that is further detailed in Section 4.6.1. The inference function is the C function named acas_decr128. We observe the initialization of the parameters of the first Dense layer: the output array with 128 float elements (dense_output_array), the array with weights parameters containing 640 float elements (dense_kernel_array) and the array with biases parameters containing 128 float elements (dense_bias_array).

For each C array, a k2c_tensor object is created. Listing 2 depicts the tensor object, which is a C struct used to represent the notion of multi-dimensional arrays, by expressing the different dimensions and their sizes. More details on multi-dimensional arrays in neural networks are provided in Chapter 4. Listing 2: Definition of tensor type in Keras2c back-end.

The same sequence of instructions is performed to initialize the parameters of the remaining layers in the core of the C function. Listing 3 depicts the calls to the C functions corresponding to the dense layers of the ACAS-Xu decr128 model. We observe that the C function implementing a dense layer (k2c_dense) is generic and reused throughout the inference function, being instantiated at each call with the layer's specific parameters. Afterwards, Keras2c implements initialize and terminate functions used to, respectively, allocate and deallocate memory, in the case of dynamic memory allocation within large inference models. Keras2c implements a considerable number of Keras layers, including dense, convolutional, pooling, recurrent and embedding layers. It also supports complex inference model types, containing layers with multiple input and output, such as the one depicted in Example 5. To support inference models that do not originally have a single-path, Keras2c uses a version of Kahn's topological sorting algorithm [99] to flatten the model's directed acyclic graph into a linear schedule.

#### 3.2.2.2.2. microTVM with static C runtime

The work of [160] consists of a patch to TVM [34], and more precisely microTVM. It is an unofficial extension to the aforementioned tools that generates a completely static C code from an inference model, originally targeting the deployment of neural networks in microcontrollers. This solution applies the principles of the project of an Ahead of Time Runtime for microTVM, mentioned in Section 3.2.2.1. The workflow starts with the import of a TensorFlow Lite format file (.tflite) by the Static microTVM front-end. In effect, since Static microTVM is built on top of microTVM, it can theoretically accept trained models from all the formats supported by TVM, but the authors of the project only implemented a frontend for TFLite models. Afterwards, the microTVM back-end is invoked. It generates files for the serialized model parameters, the model structure encoded in JSON and the layers' functions implementation.

The Static microTVM compiler then generates a C project for the inference model. The inference function is implemented in a C source code directly containing the calls to the layer's functions. This approach eliminates the need of parsing the JSON file at run time, as is done in microTVM, and allows for a complete static memory allocation. The static memory allocation, however, is not done automatically. The user must inspect the layers' functions in C file generated by the microTVM back-end, look for the allocated workspace for each function and retrieve the maximum needed workspace before calling the Static microTVM compiler. The model trainable parameters are also written in the inference C source code, in the form of byte arrays.

Listing 4 depicts the first part of the C code for inference generated by Static microTVM for the same ACAS-Xu decr128 model. We observe the initialization of the first dense layer's parameters, which are all stored in uint8_t data type, also named byte arrays. We note the layer's input array (g_storage_0 [20]) with 5 float elements of 4 bytes each, the array of layer's weights parameters (g_storage_1[2560]) with 640 float elements of 4 bytes each, the array of layer's biases parameters (g_storage_1[512]) with 128 float elements of 4 bytes each and the layer's output array(g_storage_3[512]). It is a different approach but we retrieve the correspondence with the initialization of the first layer's parameters in Keras2c. Listing 5 shows the continuation of the static C runtime code for inference. We observe that each dense layer corresponds to a different C function. Indeed, the layers' functions have a template per type of layer but the implementation is tailored for each occurrence of a given type in the model. The customized layers' functions contain for example hard-coded loop bounds. The templates for layers' functions are available in the microTVM back-end, which provides the tailored versions when invoked. Afterwards, in the TVMWrapRun function, the initialized parameters are associated to each layer.

Listing 6 details the final part of Static microTVM C code for inference. It contains the initialization of the inference function, with the linking of the model inputs and outputs to the preallocated arrays, as well as the allocation and deallocation of memory needed for the model workspace.

### 3.3. Conclusion

In this chapter we presented machine learning frameworks, which are programming environments for the design and deployment of neural networks. We first introduced ML frameworks specialized in the learning phase of neural networks, highlighting key points to observe when relying on these tools, notably with respect to the output format for the inference model description.

Afterwards, we presented a few solutions for the deployment of inference models. We discussed inference engines, both proprietary and open-source, targeting inference execution in hardware architectures that could be used in the context of avionics systems. For each discussed solution we explained why, ultimately, it does not suit our needs. Finally, we focused on two tools, Keras2c and Static microTVM, capable of generating a static C code for the inference model. These tools are, in principle, in accordance with the hypotheses of this thesis and are further used for benchmark with our proposed framework: ACETONE.

In the following chapter we present the mathematical formalization of the inference model semantics and neural networks layers studied in this work, which is a crucial step for their correct implementation in ACETONE afterwards.

## Part II

## Contributions

Chapter 4

## Formalization of the inference model semantics

The outcome of the bibliographic study of the previous chapters is twofold. First, in Chapter 2, we explained that the development process of software applications in avionics systems is subject to certification and must follow safety standards throughout the design, validation and verification development cycle. We exposed the existing challenges and presented the current regulatory initiatives aiming to allow the use of machine learning software in these safety-critical real-time systems. In particular, we derived certification objectives and defined a certain number of assumptions concerning the implementation of offline trained feed-forward neural networks.

Second, in Chapter 3, we revealed that the existing machine learning frameworks do not entirely comply with certification requirements. Regarding ML frameworks utilized in the learning phase, the primary issue is the absence of a complete description of the inference model encompassing its semantics (Objective 1). Concerning ML frameworks employed in the inference phase, the main challenges are the inability to guarantee the semantics preservation (Objective 2) and traceability (Objective 3) between the inference model description and the final executable, as well as the presence of elements that impair predictability, such as dynamic scheduling and memory allocation (Objective 4).

This chapter presents our first contribution towards a certifiable implementation of the inference model: the formalization of the semantics of the operations performed within neural networks. Section 4.1 provides a formal definition of feed-forward deep neural networks as directed acyclic graphs. Section 4.2 explains our approach to formalize the inference model semantics and emphasizes the importance of such work. Section 4.3 presents the concept of tensors, or multi-dimensional arrays, manipulated within neural networks. Section 4.4 provides the semantics of the neural networks' layers considered in the context of this thesis. Section 4.5 discusses transformations that may be applied to the inference model prior to its implementation, as they do not alter its semantics. Section 4.6 presents the state of the art of neural network models targeted in this thesis. Finally, Section 4.7 introduces our adopted format for an unambiguous description of the inference model.

### 4.1. Formal definition of feed-forward deep neural networks

As briefly mentioned in Chapter 2, a common representation of a feed-forward deep neural network (FDNN) is in the form of a directed acyclic graph (DAG) defining how its layers are connected together. To this directed graph it is then possible to associate a mathematical function F N , describing the mathematical rules of the neural network. Hereafter we provide a formal definition for FDNN.

## Definition 3 (Feed-forward Deep Neural Network).

A feed-forward deep neural network N " pV, Eq is a directed acyclic graph, wherein:

## CHAPTER 4. FORMALIZATION OF THE INFERENCE MODEL SEMANTICS

• V is the finite set of vertices of the graph, which represent its layers l P V ;

• E Ď V ˆV is the set of edges of the graph, representing the data flow within the neural network.

In order to construct the possible flows of data within the feed-forward deep neural network, it is necessary to define what are the predecessors and successors of a vertex, or layer. Definition 4 (Direct predecessors of a layer). The direct predecessors of a layer l are defined as the layers of the set P replq " tl 1 P V | pl 1 , lq P Eu. Definition 5 (Direct successors of a layer). The direct successors of a layer l are defined as the layers of the set Succplq " tl 1 P V | pl, l 1 q P Eu. Definition 6 (Indirect transitive closure of a layer). The indirect transitive closure of a layer l is the set of all its predecessors layers noted Pre ˚plq " Ť k n"1 Pre n plq, wherein:

Pre n plq " # Preplq, if n " 1 Ť l 1 PPre n´1 plq pPrepl 1 q Y tl 1 uq, otherwise

An input layer l only consumes input data, i.e. P replq " H. Similarly, a final layer l only produces output data, i.e. Succplq " H. We represent V I Ď V as the set of input layers and

V O Ď V as the set of output layers. Note that V I X V O " H. The remaining layers, l R V I Y V O , are the hidden layers.

Finally, as a straight consequence of directed acyclic graphs properties, we note that in a feed-forward neural network l R Pre ˚plq.

Example 3 (Feed-forward Deep Neural Network). Figure 4.1 illustrates a feed-forward neural network as described in Definition 3. In this example V I " tl 1 , l 2 u and V O " tl 9 , l 10 , l 11 u. According to Definition 4, the direct predecessors of layer l 7 are P repl 7 q " tl 2 , l 5 u. Likewise, as stated in Definition 5, its direct descendant are Succpl 7 q " tl 8 u. Following Definition 6, all the predecessors layers of l 6 , for example, are the layers of the set P re ˚pl 6 q " tl 3 , l 4 , l 5 , l 1 u. We observe that there are no cycles, or feedback connections in the graph. Definition 7 (Local function associated to a layer). Let N " pV, Eq be a feed-forward deep neural network and l be a layer of the neural network. We denote the local function associated to the layer l as:

f l : R m l Ñ R p l (4.1)

where R m l " R a 1 ˆRa 2 ˆ. . . ˆRan is the Cartesian product of the domains of the n inputs of f l , with n P N `.

Similarly, R p l " R b 1 ˆRb 2 ˆ. . . ˆRb k is the Cartesian product of the domains of the k outputs of f l , with k P N `.

For readability reasons, we may use R m l or the notation R a 1 ˆa2 ˆ...ˆan to represent R a 1 ˆRa 2 ˆ. . .ˆR an , the input dimension of the layer l. Likewise, R p l " R b 1 ˆb2 ˆ...ˆb k represents R b 1 ˆRb 2 ˆ. . . ˆRb k , the output dimension of the layer l.

Definition 8 (Function associated to a FDNN). Let N " pV, Eq be a feed-forward deep neural network and V O Ď V be the set of output layers. Let us denote the function associated to a set of layers such that:

@U Ď V, F U " # pF l 1 , . . . , F ln q, if U " tl 1 , ..., l n u F H , if U " H. (4.2)

wherein:

@l P V, F l " f l pF P replq q (4.3)

We note F N " F V O the function associated to a feed-forward deep neural network.

Example 4 (Single-path feed-forward deep neural network). It corresponds to the particular case of a feed-forward deep neural network, wherein:

• V " tl 1 , . . . , l n u; • @i ě 2, Prepl i q " tl i´1 u. Therefore, V I " tl 1 u, V O " tl n u.

According to Definition 8 the function associated to N is the composition function:

F N : R m l 1 Ñ R p ln x Þ Ñ f ln ˝fl n´1 ˝. . . ˝fl 1 pxq (4.4)

wherein m l 1 in the input dimension of f l 1 and p ln is the output dimension of f ln . More generally, the input dimension of l i is the output dimension of l i´1 , i.e. m l i " p l i´1 . An illustration of an single-path feed-forward deep neural network is shown in Figure 4.2, wherein we observe that Prepl i q " tl i´1 u and Pre ˚pl n q " tl n´1 , . . . , l 1 u.

x l 1 l 2 . . . l n-1 l n y

F N : R m l 1 ˆRm l 2 Ñ R p l 9 ˆRp l 10 ˆRp l 11 F N " pF l 9 , F l 10 , F l 11 q wherein, F l 9 " f l 9 pF l 6 , F l 8 q F l 8 " f l 8 pF l 6 , F l 7 q F l 3 " f l 3 pF l 1 q F l 1 " f l 1 px 1 q F l 10 " f l 10 pF l 8 q F l 6 " f l 6 pF l 3 , F l 4 , F l 5 q F l 4 " f l 4 pF l 1 q F l 2 " f l 2 px 2 q F l 11 " f l 11 pF l 8 q F l 7 " f l 7 pF l 2 q F l 5 " f l 5 pF l 1 q

and m l 1 , m l 2 are the input dimensions of, respectively, f l 1 , f l 2 and p l 9 , p l 10 , p l 11 are the output dimensions of, respectively, f l 9 , f l 10 , f l 11 .

### 4.2. Inference model semantics

We have thus defined neural networks as directed acyclic graphs, wherein each node represents a layer. Furthermore, in Section 2.3, we explained what is the semantics of the inference model: (i) the characterization of the directed acyclic graph structure, and (ii) the formal semantics of the operations performed by each node of the graph. To achieve that, as evoked in Definition 7, we decided to formalize the semantics of neural networks' layers as mathematical functions. For each layer we thus establish a mathematical function, with defined input and output domains, characterized by a clear and unambiguous formula delineating the computation of an output value given any input value within the specified domains.

Indeed, having a defined formal semantics is a crucial step to correctly implement the inference model. The mathematical formulae provide a reference to generate a C code for the inference model that is semantically equivalent to the implementation of the learning environment. Figure 4.3 summarizes the intended workflow. Note, however, that the formal semantics express mathematical equations in the domain of real numbers, while in the algorithmic implementation, we adhere to floating-point arithmetic. Further discussion on this topic is provided in Section 5.3.1.

## Inference model complete description

Inference model formal semantics Inference model implementation (C language)

### 4.3. Tensors

In mathematics, a tensor is defined as a multilinear map and serves as a mathematical construct to denote multilinear relationships among sets of algebraic objects. Tensors are used to describe geometric quantities that have magnitude and direction and may vary in different directions. They are represented by arrays of numbers that change in a specific way under changes of coordinate systems. Within the domain of machine learning, the term is nowadays often employed as a convention for structuring and representing multi-dimensional arrays of numerical data, as are the input and output of neural network layers' mathematical functions (see Definition 7). The borrowing of this term finds its origins in the first decade of the twenty-first century, when multilinear tensor methods emerged in computer vision, computer graphics, and machine learning [178]. Indeed, multilinear algebra provides a transparent framework for analysing complex data structures and disentangling causal factors based on statistical properties [177]. Then use cases extend to image and video processing, where tensor methods effectively elucidate spatial or temporal redundancies [179]. In 2015, the authors of [136] proposed integrating tensor methods into neural networks, by organizing weights into data tensors to analyse and reduce the neural network parameters.

## Definition 9 (Tensor).

A tensor is a multi-dimensional array, defined as:

T P R n 1 ˆn2 ˆ...ˆn k wherein pn 1 , . . . , n k q P N `represent the k dimensions of the array.

The data in the multi-dimensional array are known as the components of the tensor, which are denoted by indices giving their position in the array. The total number of indices k required to identify each component uniquely is equal to the dimension of the array, hence the nomenclature of k-dimensional array.

Definition 10 (Component of a tensor). Let T be a tensor of dimension k, the notation T i 1 ,...,i k , @pi 1 , . . . , i k q P 1, n 1 ˆ. . . ˆ 1, n k designates a specific component of the tensor.

Subsequently we provide definitions for 1-dimensional (1D), 2-dimensional (2D) and 3-dimensional (3D) tensors.

## Definition 11 (1D Tensor).

A 1D tensor is defined as T P R n l , wherein n l P N `represents the length of the tensor. Component T i represents the i th element of the tensor. A 1D tensor is also named a vector.

Example 6 (Illustration of a 1D tensor). Let us consider a 1D tensor as defined in Definition 11. Figure 4.4 depicts such 1-dimensional array. In this example T has length n l " 7. The highlighted component corresponds to element T 4 " 6. Definition 12 (2D Tensor). A 2D tensor is defined as T P R n h ˆnw , wherein n h , n w P N `represent respectively the height and the width dimensions of the tensor. Component T i 1 ,i 2 is located at position i 1 along the height dimension and at position i 2 along the width dimension. A 2D tensor is also named a matrix.

Example 7 (Illustration of a 2D tensor). Let us consider a 2D tensor as defined in Definition 12. Figure 4.5 depicts such multi-dimensional array. In this example T has height n h " 5 and width n w " 7.

The highlighted component corresponds to element T 3,6 " 8.

## Definition 13 (3D Tensor).

A 3D tensor is defined as T P R n h ˆnwˆnc , wherein n h , n w , n c P N `represent respectively the height, the width and the channel dimensions of the array. Component T i 1 ,i 2 ,i 3 is located at position i 1 along the height dimension, at position i 2 along the width dimension and at position i 3 along the channel dimension.

Example 8 (Illustration of a 3D tensor). Let us consider a 3D tensor as defined in Definition 13. Figure 4.6 depicts such multi-dimensional array. In this example T has height n h " 4, width n w " 5 and a number of channels n c " 3. The highlighted component corresponds to element T 4,4,1 " 10.

### 4.4. Neural networks' layers associated functions

Hereafter we present the formal semantics, i.e. the mathematical functions performed within neural networks' layers, that were studied in the context of this thesis. Our work consisted in gathering, extending and formalizing existing literature, notably the evolving documentation of machine learning frameworks (e.g. the documentations of TensorFlow [167], PyTorch [148], ONNX [140] and NNEF [170]).

#### 4.4.1. Activation layers

An activation layer is a specific type of layer that performs an activation function. In the context of neural networks, an activation function is a mathematical function that determines the output of an unit, or neuron, based on its input. Non-linear activation functions allow neural networks to learn complex patterns and relationships in the data. Indeed, by applying a non-linear activation function, it can be demonstrated that a neural network with one hidden layer is an universal function approximator [88]. Definition 14 (Activation layer associated function). Let f : R Ñ R and I be a k-dimensional input tensor. The activation layer associated function is defined as:

A f : R n 1 ˆ...ˆn k Ñ R n 1 ˆ...ˆn k I Þ Ñ O (4.5)

wherein O is the k-dimensional output tensor obtained by applying function f element-wise to tensor I.

## We thus have for each component of tensor O:

O i 1 ,...,i k " f pI i 1 ,..

.,i k q

There are a number of functions f commonly applied within an activation layer in neural networks. Hereafter we present these used in the context of this thesis. 4.6 and depicted in Figure 4.7. 4.9 and depicted in Figure 4.10.

## Definition 15 (ReLU function). The rectified linear unit (ReLU) function is defined in Equation

ReLU : R Ñ R x Þ Ñ maxp0, xq (4.6) -2 -1 1 2 1 2 x f (x)

Sigmoid : R Ñ R x Þ Ñ 1 1 `e´x (4.7) -4 -2 2 4 0.5 1 x f (x)

T anH : R Ñ R x Þ Ñ e x ´e´x e x `e´x (4.8) -3 -2 -1 1 2 3 -1 1 x f (x)

Identity : R Ñ R x Þ Ñ x (4.9) -2 -1 1 2 -2 -1 1 2 x f (x)

#### 4.4.2. Pre-processing layers

Definition 19 (2D Zero-padding layer associated function). Let I be a 3D input tensor and p " pp t ,p b ,p l ,p r q be a 4-tuple of non-negative integers, representing the zero-padding to be applied to the height and width dimensions (2D) of I. Therefore, p t and p b denote the number of zeros applied to, respectively, the top and the bottom of the height dimension. While p l and p r indicate the number of zeros applied to, respectively, the left and the right of the width dimension. The 2D Zero-padding layer associated function is defined as:

P p : R n h ˆnwˆnc Ñ R o h ˆowˆoc I Þ Ñ O (4.10)

wherein O represents the 3D output tensor, o h " n h `pt `pb , o w " n w `pl `pr and o c " n c represent respectively the output height, width and channels dimensions. Each component of tensor O is then defined as:

O i 1 ,i 2 ,i 3 " # 0, if i 1 ď p t or i 1 ě n h `pt or i 2 ď p l or i 2 ě n w `pl I i 1 ´pt,i2´pl,i3 , otherwise.

Flatten : R n h ˆnwˆnc Ñ R n h ¨nw¨nc I Þ Ñ O (4.12)

wherein O is the 1D tensor of size n l " n h ¨nw ¨nc , whose components are defined as:

O i 1 " I Q i 1 nw ¨nc U , Q i 1 mod pnw ¨ncq nc U , i 1 mod nc (4.13)

Alternatively, it is possible to represent components of tensor I in terms of components of tensor O:

I i 1 ,i 2 ,i 3 " O pi 1 ´1q¨pnw¨ncq`pi 2 ´1q¨nc`pi 3 ´1q`1 (4.14)

Example 9 (Flatten layer associated function). Figure 4.11 depicts the flatten layer associated function applied to a 3D tensor whose dimensions are ordered as n h ˆnw ˆnc . We note for example that component

O 13 corresponds to component I 2,2,1 .

The flattening operation definition may initially appear counterintuitive; however, it aligns with the standard approach employed in machine learning frameworks to store multi-dimensional arrays in linear memory. In this example, we represent a 3D tensor organized as n h ˆnw ˆnc , which is a memory layout convention named channels-last. Further discussion on other possible memory layout conventions is presented in Chapter 5.

3,1,3

w n h n c 1,1,1 2,1,1 3,1,1 1,2,1 2,2,1 3,2,1 1,3,1 2,3,1 3,3,1 1,1,2 2,1,2 3,1,2 1,2,2 2,2,2 3,2,2 1,3,2 2,3,2 3,3,2 1,1,3 2,1,3 3,1,3 1,2,3 2,2,3 3,2,3 1,3,3 2,3,3 3,3,3 n h • n w • n c3,1,2 3,1,1 2,1,3 2,1,2 2,1,1 1,1,3 1,1,2 1,1,1 3,2,3 3,2,2 3,2,1 2,2,3 2,2,2 2,2,1 1,2,3 1,2,2 1,2,1 3,3,3 3,3,2 3,3,1 2,3,3 2,3,2 2,3,1 1,3,3 1,3,2 1,3,1 n

Tensor I

Tensor O

#### 4.4.3. Core layers

Definition 21 (Biases layer associated function). Let I be a k-dimensional input tensor. Let B be a kdimensional tensor with biases, or offsets, to be applied to tensor I. The biases layer associated function is defined as:

B B : R n 1 ˆ...ˆn k Ñ R n 1 ˆ...ˆn k I Þ Ñ O (4.15)

wherein O corresponds to the k-dimensional output tensor. Each component of tensor O is defined as:

O i 1 ,...,i k " I i 1 ,...,i k `Bi 1 ,...,i k

Definition 22 (Dense layer associated function). Let I be a 1D input tensor of size n i . Let W be a 2D tensor with dimensions of size pn o , n i q, representing the weights of the layer and B be a 1D tensor of size n o , representing the biases of the layer. The dense layer associated function is a linear transformation defined as:

Dense W,B : R n i Ñ R no I Þ Ñ O (4.16)

wherein O corresponds to the 1D output tensor. Each component of tensor O is defined as:

O i 1 " n i ÿ k"1 W i 1 ,k .I k `Bi 1 (4.17)

Example 10 (Dense layer associated function). Figure 4.12 depicts the dense layer associated function.

We observe the input tensor I, with size n i " 2. We also note the weights tensor W, with dimensions of size n o " 3 and n i " 2 and the biases tensor B, with size n o " 3. The output tensor O with size n o " 3 is the result of the dense layer associated function applied to tensor I.

1 2 1 1 1 -1 0 -2 1 0 0 -1 1 3 × + = Tensor W Tensor I Tensor B Tensor O Figure 4

.12: Illustration of the dense layer associated function.

#### 4.4.4. Pooling layers

Definition 23 (2D Pooling layer associated function). Let I be a 3D input tensor, k " pk h , k w q be a 2-tuple of non-negative integers representing the pooling window, s " ps h , s w q be a 2-tuple of non-negative integers representing the stride with which the pooling window is applied to the height and width dimensions of I and f : R k h ˆkw Ñ R be the pooling function. The 2D Pooling layer associated function is defined as:

Pool s,k,f : R n h ˆnwˆnc Ñ R o h ˆowˆoc I Þ Ñ O (4.18)

wherein O represents the 3D output tensor and o h , o w and o c correspond respectively the output height, width and channels dimensions, which are defined as:

o h " Z n h ´kh s h `1^, o w " Z n w ´kw s w `1^, o c " n c (4.19)

Each component of tensor O is then defined as:

O i 1 ,i 2 ,i 3 " f m P r1,k h s n P r1,kws pI s h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,i 3 q (4.20)

Definition 24 (2D Max-pooling layer associated function). The 2D Max-pooling layer is a type of pooling layer wherein the pooling function f : R k h ˆkw Ñ R is the max function. Each component of tensor O is then defined as:

O i 1 ,i 2 ,i 3 " max m P r1,k h s n P r1,kws pI s h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,i 3 q (4.21)

Example 11 (2D Max-pooling layer associated function). Figure 4.13 depicts the max-pooling operation applied to an input tensor I with dimensions n h " n w " 8 and n c " 1. The pooling window equals k h " k w " 2 and the stride is s h " s w " 2. Thus, the output tensor O has dimensions n h " n w " 4 and n c " 1.

The blue region indicates a first application of the max-pooling function, wherein the maximum of the blue-highlighted elements in I is selected and corresponds to component O 1,1,1 . Likewise, the red region corresponds to the 10 th application of the max-pooling function to tensor I, resulting in component O 3,2,1 .

In our example n c " o c " 1 for easier comprehension. As the 2D Max-pooling function is applied to the 2-dimension, the same logic would be repeated to the remaining channels if n c " o c ‰ 1.

O i 1 ,i 2 ,i 3 " 1 k h ¨kw k h ÿ m"1 kw ÿ n"1 pI s h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,i 3 q (4.22)

Example 12 (2D Average-pooling layer associated function). We note now that component O 1,1,1 corresponds to the average value computed over elements I 1:2,1:2,1 . Similarly, component O 3,2,1 corresponds to the average-pooling function applied to elements I 5:6,3:4,1 .

#### 4.4.5. Convolutional layers

Definition 26 (2D Convolutional layer associated function). Let I be a 3D input tensor. Let K be a vector of n k 3D tensors rK 1 , K 2 , . . ., K n k s, representing the kernels of the convolution, with n k P N `. Each kernel tensor is defined as K j P R f h ˆfwˆfc , wherein f h , f w and f c represent respectively the height, the width and the channel dimensions of the kernel. Hence, K P R f h ˆfwˆfcˆnk is a 4-dimensional tensor. Let s " ps h , s w q be a 2-tuple of non-negative integers, representing the stride with which the convolution kernels are applied to the height and width dimensions of I.

The 2D Convolutional layer associated function is defined as:

C K,s : R n h ˆnwˆnc Ñ R o h ˆowˆoc I Þ Ñ O (4.23)

wherein O represents the 3D output tensor and o h , o w and o c correspond respectively the output height, width and channels dimensions, which are defined as:

o h " Z n h ´fh s h `1^( 4.24) o w " Z n w ´fw s w `1^( 4.25) o c " n k (4.26)

Each component of tensor O is then defined as:

O i 1 ,i 2 ,i 3 " f h ÿ m"1 fw ÿ n"1 fc ÿ l"1 pK i 3 q m,n,l ¨Is h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,l(4.27)

Note that f c must be equal to n c . Furthermore, observe that the 2D convolution operation presented above is actually named 2D cross-correlation in signal processing literature [78]. The difference between the two is that in the standard 2D convolution operation the kernel is flipped, while in the 2D cross-correlation operation it is not. To adhere to the machine learning notation, when referring to 2D convolution we specifically denote the operation in which the kernel is not flipped. 4.15 we observe that each channel of the output tensor O corresponds to the convolution of one convolutional kernel with the input tensor I, which is evidenced by the matching colors. For example, the convolutional kernel K 1 , depicted in red, convolved with the input tensor generates all the elements of the first channel of tensor O, i.e. the components

O i 1 ,i 2 ,1 , @pi 1 , i 2 q P 1, o h ˆ 1, o w . Likewise, component O 5,5,2 , highlighted in green, is computed as: O 5,5,2 " 3 ÿ m"1 3 ÿ n"1 3 ÿ l"1 pK 2 q m,n,l ¨I5´1`m,5´1`n,l f w f h f c n w n h n c n k Tensor I o w o h o c

Tensor O

Tensor K = [K 1 , K 2 , K 3 , K 4 ]

#### 4.4.6. Normalization layers

Definition 27 (Batch-normalization layer associated function). Let I be a 3D input tensor. Let γ, β, µ and σ 2 be 1D tensors of size n c . Wherein γ represents the scale factor, β represents the offset factor, and µ and σ 2 represent respectively the mean and the variance, both computed over a batch during learning phase. Let ϵ be a real constant needed for numerical stability. The batch-normalization layer associated function is defined as:

BN γ,β,µ,σ 2 ,ϵ : R n h ˆnwˆnc Ñ R n h ˆnwˆnc I Þ Ñ O (4.28)

wherein O represents the 3D output tensor. Each component of tensor O is then defined as:

O i 1 ,i 2 ,i 3 " γ i 3 b σ 2 i 3 `ϵ ¨Ii 1 ,i 2 ,i 3 `¨β i 3 ´µi 3 b σ 2 i 3 `ϵ ‚ (4.29)

One may also use the following simplified notation, wherein each component of tensor O is defined as:

O i 1 ,i 2 ,i 3 " α i 3 ¨Ii 1 ,i 2 ,i 3 `Bi 3 (4.30)

with α i 3 "

γ i 3 b σ 2 i 3 `ϵ and B i 3 " β i 3 ´µi 3 b σ 2 i 3 `ϵ .

#### 4.4.7. Merge layers

Definition 28 (Concatenation layer associated function). Let I be a 3D tensor with dimensions of size pn h I , n w I , n c I q. Let J be a 3D tensor with dimensions of size pn h J , n w J , n c J q. Let dim c be an integer P 1, 3 representing the dimension in which the concatenation is performed. The concatenation layer associated function is defined as:

Concat dimc : R n h I ˆnw I ˆnc I ˆRn h J ˆnw J ˆnc J Ñ R o h ˆowˆoc I, J Þ Ñ O (4.31)

wherein O represents the 3D output tensor, whose dimensions are computed as:

o h " # n h I `nh J , if dim c = 1 n h I " n h J , else o w " # n w I `nw J , if dim c = 2 n w I " n w J , else o c " # n c I `nc J , if dim c = 3 n c I " n c J , else (4.32)

Each component of tensor O is then defined in function of dim c : 3,1,3

• if dim c = 1: O i 1 ,i 2 ,i 3 " # I i 1 ,i 2 ,i 3 , if i 1 ď n h I J i 1 ´nh I ,i 2 ,i 3 , if i 1 ą n h I (4.33) • if dim c = 2: O i 1 ,i 2 ,i 3 " # I i 1 ,i 2 ,i 3 , if i 2 ď n w I J i 1 ,i 2 ´nw I ,i 3 , if i 2 ą n w I (4.34) • if dim c = 3: O i 1 ,i 2 ,i 3 " # I i 1 ,i 2 ,i 3 , if i 3 ď n c I J i 1 ,i 2 ,i 3 ´nc I , if i 3 ą n c I (4.

n w I n h I n c I Tensor I 4,1,3,1,2 3,1,1 2,1,3 2,1,2 2,1,1 1,1,3 1,1,2 1,1,1 3,2,3 3,2,2 3,2,1 2,2,3 2,2,2 2,2,1 1,2,3 1,2,2 1,2,1 3,3,3 3,3,2 3,3,1 2,3,3 2,3,2 2,3,1 1,3,3 1,3,2 1,3,1

n w J n h J n c J Tensor J 7,1,3 4,1,2 4,1,1 3,1,3 3,1,2 3,1,1 2,1,3 2,1,2 2,1,1 1,1,3 1,1,2 1,1,1 4,2,3 4,2,2 4,2,1 3,2,3 3,2,2 3,2,1 2,2,3 2,2,2 2,2,1 1,2,3 1,2,2 1,2,1 4,3,3 4,3,2 4,3,1 3,3,3 3,3,2 3,3,1 2,3,3 2,3,2 2,3,1 1,3,3 1,3,2 1,3,1

w o h o c3 7,1,2 7,1,1 6,1,3 6,1,2 6,1,1 5,1,3 5,1,2 5,1,1 4,1,3 4,1,2 4,1,1 3,1,3 3,1,2 3,1,1 2,1,3 2,1,2 2,1,1 1,1,3 1,1,2 1,1,1 7,2,3 7,2,2 7,2,1 6,2,3 6,2,2 6,2,1 5,2,3 5,2,2 5,2,1 4,2,3 4,2,2 4,2,1 3,2,3 3,2,2 3,2,1 2,2,3 2,2,2 2,2,1 1,2,3 1,2,2 1,2,1 7,3,3 7,3,2 7,3,1 6,3,3 6,3,2 6,3,1 5,3,3 5,3,2 5,3,1 4,3,3 4,3,2 4,3,1 3,3,3 3,3,2 3,3,1 2,3,3 2,3,2 2,3,1 1,3,3 1,3,2 1,3,1 o

Tensor O

### 4.5. Semantics-preserving inference model transformations

Once the semantics of each layer is formally defined, it is acceptable to transform the inference model as long as its semantics is preserved. 4.36, we find p t `pb " 3. We then note the set of pairs that satisfy the condition of having o h " n h after the 2D convolutional layer as:

tpp t , p b q | p t `pb " 3u " tp3, 0q, p2, 1q, p1, 2q, p0, 3qu

The same reasoning is applied to the width dimension, where we also find possible pairs satisfying p l `pr " 3. It leads to a total of 16 combinations of zero-padding that fulfill the requirement of the output spatial dimension of the convolutional layer having the same size as the input spatial dimension.

For instance, TensorFlow and PyTorch apply different strategies to zero-pad the 3D array when zeropadding is an option of the 2D Convolutional layer and the user must choose between "same" padding and "valid" padding. "Same" padding indicates that the output must have the same size as the input, while "valid" means that no zero-padding should be applied.

Figure 4.17 depicts this difference when using the "same" option. We observe that TensorFlow starts padding the multi-dimensional array from the bottom right. For our example wherein p t `pb " 3 and p l `pr " 3, TensorFlow chooses to use the pairs pp t " 1, p b " 2q and pp l " 1, p r " 2q. On the other hand, PyTorch begins the zero-padding from the top left, employing the pairs pp t " 2, p b " 1q and pp l " 2, p r " 1q.

In the ML frameworks, this issue can be avoided, however, by using a specific layer for zero-padding beforehand, wherein the p t and p b (resp. p r and p l ) parameters are explicitly set. As a conclusion, we note that in order to avoid any ambiguity concerning the desired semantics of an operation one should not rely on default configurations. Proof. Let us consider a 3D input tensor I with dimensions of size pn h , n w , n c q. Let us assume that the ReLU activation function is applied before the 2D Max-pooling function. In this case we have:

O i 1 ,i 2 ,i 3 " MaxPool s,k pmaxp0, I i 1 ,i 2 ,i 3 qq (4.39)

As it is an element-wise operation, the ReLU function is performed n h ¨nw ¨nc times. On the contrary, if the ReLU activation function is applied after the 2D Max-pooling function, we have:

O i 1 ,i 2 ,i 3 " ReLU p max m P r1,k h s n P r1,kws pI s h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,i 3 qq (4.40)

Which means that the ReLU function is performed on the down-sampled tensor, being thus executed o h ¨ow ¨oc times (see Equation 4. 19). Note that maxpmaxpx i q, 0q " maxpmaxpx i , 0qq, hence the semantics is preserved.

During inference a batch-normalization layer has its parameters fixed and acts as a constant normalizer for the input tensor, it is thus possible to merge this layer with the previous convolutional layer.

## Property 4 (Merging a batch-normalization layer with a 2D convolutional layer). Applying a batchnormalization layer after a 2D Convolutional layer is semantically equivalent to performing a single 2D convolution function with modified kernels and biases. Merging both layers reduces the number of operations to be performed, which reduces average execution time, and saves memory bandwidth required for storing intermediate tensors.

Proof. Let us consider a 3D input tensor I with dimensions of size pn h , n w , n c q. Let us suppose that we have a 2D convolutional layer C p,K,s,B,f followed by a batch-normalization layer BN α,B . The output tensor is obtained as O " BN α,B pC p,K,s,B,f pIqq. Each of the components of tensor O are then computed as:

O i 1 ,i 2 ,i 3 " α i 3 ¨˜f h ÿ m"1 fw ÿ n"1 fc ÿ l"1 pK i 3 q m,n,l ¨Is h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,l `Bi 1 ,i 2 ,i 3 ¸`B i 3 " f h ÿ m"1 fw ÿ n"1 fc ÿ l"1 α i 3 ¨pK i 3 q m,n,l ¨Is h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,l `αi 3 ¨Bi 1 ,i 2 ,i 3 `Bi 3 (4.41)

This is the equation of a 2D convolutional layer C 1 p,α.K,s,α.B`B .

### 4.6. State-of-the-art neural network models

In this section we present examples of neural network models of the literature. The presented models are divided according to their domain of application: one model for multi-dimension data classification, five models for image classification, one model for audio classification and one for time series prediction. Seven of them are single-path feed-forward neural networks (as in Example 4) and one has a more complex structure. These models were used to test and validate our approach for the implementation and deployment of trained models, as will be detailed in Chapter 5.

#### 4.6.1. ACAS-Xu surrogate models

We consider the approximation of the ACAS-Xu system, which stands for Airborne Collision Avoidance System for Unmanned aircraft, using neural networks. The ACAS-Xu system takes input variables, i.e. information from sensors measurements, and computes maneuver advisories, represented by scores. See Figure 4.18. The advisories indicate for example if the current situation is clear-of-conflict (CoC) in which case the ownship -aircraft equipped with the system -can continue its pathway or whether it should turn weakly to the left (WL), weakly to the right (WR), strongly to the left (SL) or strongly to the right (SR) to avoid collision with the intruder.

The input state of the ACAS-Xu system is composed of seven dimensions: ρ is the distance between the two aircraft, θ is the angle to the intruder relative to the ownship heading direction, ψ is the heading angle of intruder relative to the ownship, v int and v own are, respectively, the speed of the intruder and the ownship, t sep is the time until loss of vertical separation between the two aircrafts and u prev is the previous advisory. The original design relies on a set of offline computed lookup tables (LUT) to make the avoidance decisions. Then, some works [45,105] proposed to replace these LUT with surrogate neural networks in order to reduce the memory footprint and thus to improve the execution time. The surrogate neural networks were obtained by discretizing t sep and u prev and producing a network for each discretized combination. Thus the function associated to each model is of the form F N : R 5 Ñ R 5 .

The examined ACAS-Xu neural networks have hidden layers of type Dense separated by an activation layer of type ReLU. Neural networks containing only Dense layers, interleaved with activations functions, are classified as multi-layer perceptrons [86]. We consider regular structures, proposed in [105], which have the same number of units per layer, as well as decreasing structures, proposed in [45], with a number of units that decreases as we advance in the depth of the neural network. We examine the following models:

• ACAS-Xu reg50 : seven Dense hidden layers with 50 units per layer;

• ACAS-Xu reg100 : seven Dense hidden layers with 100 units per layer;

• ACAS-Xu reg200 : seven Dense hidden layers with 200 units per layer;

• ACAS-Xu decr128 : five Dense hidden layers with respectively p128, 128, 64, 32, 16q units per layer;

• ACAS-Xu decr256 : six Dense hidden layers with respectively p256, 256, 128, 64, 32, 16q units per layer.

Figure 4.19 illustrates the ACAS-Xu reg50 model, with a representation that highlights the input and output dimensions of the layers associated functions. We observe, for example, that f dense1 has input dimension R m l 1 " R 5 and output dimension R p l 1 " R 50 . To provide an indication of the size of these neural networks, we note that the ACAS-Xu reg50 model has 15, 855 trainable parameters and an inference pass performs 31, 355 floating-point operations (FLOPs). The ACAS-Xu decr256 model in its turn contains 111,173 trainable parameters and the inference phase executes 221,589 FLOPs. We note that the floating-point operations include additions and multiplications performed in floating-point arithmetic.

¨ρ θ ψ v int v own ‹ ‹ ‹ ‹ ‹ ‹ ‚ f dense1 f relu1 . . . f relu7 f dense8 ¨CoC SR SL W R W L ‹ ‹ ‹ ‹ ‹ ‹ ‚

#### 4.6.2. LeNet-5

The LeNet-5 model [119] is a feed-forward convolutional neural network developed for handwritten digits images recognition, trained on the MNIST data set [120]. It is one of the earliest models of this type and is known for promoting the development of machine learning with the introduction of back-propagation as a gradient computing technique in training algorithm. Although simple, this model contains the main basic type of hidden layers: 2D Convolutional, 2D Pooling and Dense layers. The layers that implement an activation function after the 2D Convolutional and Dense hidden layers are of type Hyperbolic Tangent. Finally, the output layer is followed by a post-processing of type Softmax.

Figure 4.20 illustrates the structure of the LeNet-5 model. In this example we note f conv1 with input dimension R m l 1 " R 28ˆ28ˆ1 and output dimension R p l 1 " R 24ˆ24ˆ6 . Note that the functions of 2D Convolutional, 2D Pooling and Dense layers have a subscript in their name. This indicates that although the mathematical function performed by a layer of a given type is the same, each layer has different parameters. In the case of Hyperbolic Tangent layers, the output is only dependent on the argument of the functions, or the input data.

This model has 44,426 trainable parameters to store and an inference pass executes 572,504 FLOPs.

x f conv1 f tanh f pool1 f conv2 f tanh f pool2 f f lat f dense1 f tanh f dense2 f tanh f dense3 y 28ˆ28ˆ1 24ˆ24ˆ6 24ˆ24ˆ6 12ˆ12ˆ6 8ˆ8ˆ16 8ˆ8ˆ16 4ˆ4ˆ6120

#### 4.6.3. CifarNet

The considered CifarNet model was introduced in [89] and was for a long time the state-of-the-art model used to solve the object classification problem on the CIFAR-10 data set [111], which consists of RGB images with dimension 32 ˆ32 containing objects of ten different classes. CifarNet is composed of three 2D Convolutional, two 2D Pooling, two Dense and five ReLU layers. Figure 4.21 depicts the structure of this model. The main differences between this model and LeNet-5 are that it has a three-dimensional input and the 2D Convolutional layers functions are preceded of 2D Zero-padding layers, to reshape the input, which adds some complexity in terms of computation. With this configuration the number of trainable parameters increases to 122,570 alongside 9,18 million FLOPs performed during inference.

x f conv1 f relu f pool1 f conv2 f relu f pool2 f conv3 f relu f f lat f dense1 f relu f dense2 f relu y 32ˆ32ˆ3 30ˆ30ˆ32 30ˆ30ˆ32 15ˆ15ˆ3213ˆ13ˆ64

#### 4.6.4. AlexNet

The AlexNet architecture was first defined in [112] and is considered as one of the most influential works in the computer vision domain. Indeed, it achieved a considerably improved performance over other methods in the ImageNet Large Scale Visual Recognition Challenge (ILSVRC) of 2012. The ImageNet data set [55] is composed of 256ˆ256 RGB images categorized under 1,000 different object classes. AlexNet introduces a very deep neural network model with layers containing many units. Its training only became feasible with the advent of general purpose graphics processing units (GPU).

The model has five 2D Convolutional layers, four 2D Pooling layers, three Dense layers and the nonlinearity is assured by seven ReLU layers. In total, it has approximately 61 million tunable parameters and an inference pass performs 1.64 billion FLOPs.

x f conv1 f relu f pool1 f conv2 f relu f pool2 f conv3 f relu f conv4 f relu f conv5 f relu f pool3 f pool4 f f lat f dense1 f relu f dense2 f relu f dense3 y 256ˆ256ˆ3 55ˆ55ˆ64 55ˆ55ˆ64 27ˆ27ˆ64 27ˆ27ˆ192 27ˆ27ˆ192 13ˆ13ˆ192 13ˆ13ˆ384 13ˆ13ˆ384

#### 4.6.5. VGG-16

VGG-16 is a convolutional neural network model first proposed by [158] Compared to AlexNet, the authors showed that treating smaller parts of the image at each application of the convolutional function attains the same final result and has the advantage of having less parameters to train per convolutional layer. It implies reducing the size of the convolutional filters and multiplying the number of convolutional layers. One major drawback that derives from the augmented depth of VGG-16 is the high number of parameters, adding up to 138.36 million parameters and requiring 31 billion FLOPs to perform an inference.

x f conv1 f relu f conv2 f relu f pool1 f conv3 f relu f conv4 f relu f pool2 f conv5 f relu f conv6 f relu f conv7 f relu f pool3 f conv8 f relu f conv9 f relu f conv10 f relu f pool4 f conv11 f relu f conv12 f relu f conv13 f relu f pool5 f f lat f dense1 f relu f dense2 f relu f dense3 y 224ˆ224ˆ3 224ˆ224ˆ64 224ˆ224ˆ64 224ˆ224ˆ64 224ˆ224ˆ64 112ˆ112ˆ64 112ˆ112ˆ128 112ˆ112ˆ128 112ˆ112ˆ128 112ˆ112ˆ128 56ˆ56ˆ128 56ˆ56ˆ256 56ˆ56ˆ256 56ˆ56ˆ256 56ˆ56ˆ256 56ˆ56ˆ128 56ˆ56ˆ128 28ˆ28ˆ256 28ˆ28ˆ512 28ˆ28ˆ512 28ˆ28ˆ512 28ˆ28ˆ512 28ˆ28ˆ512 28ˆ28ˆ512 14ˆ14ˆ512 14ˆ14ˆ512 14ˆ14ˆ512 14ˆ14ˆ512 14ˆ14ˆ512 14ˆ14ˆ512 14ˆ14ˆ512 7ˆ7ˆ512

#### 4.6.6. SqueezeNet

SqueezeNet [91] is a deep feed-forward neural network originally released in 2016 for image detection as well. The authors identified a limitation in the existing neural networks used for computer vision, whose development mostly focused on improving accuracy at the cost of deployment feasibility. SqueezeNet was then proposed as an architecture that achieves the accuracy level of AlexNet (Section 4.6.4) on the ImageNet data set using fifty times fewer parameters. To do so, the authors introduced three main strategies for the design of the neural network: (i) replace some of the convolution filters of size 3 ˆ3 with smaller ones of size 1 ˆ1, (ii) reduce the number of convolution filters in each convolution layer and (iii) apply a smaller spatial gap within the application of the convolution filters, to control the reduction in the size of the images along the depth of the model.

Practically, the authors propose a structure named fire module. The fire module consists of one 2D Convolutional layer containing small filters, which output is fed to two distinct 2D Convolutional layers. After each convolutional layer, an activation layer of type ReLU is present. Finally, a layer of type Concatenation concatenates the output of the two layers ReLU. Figure 4.24 details the fire module, f f ire , wherein the presented input and output dimensions correspond to the first module of this type present in the SqueezeNet graph.

x f conv1 f relu1 f conv2 f conv3 f relu2 f relu3 f concat y 55ˆ55ˆ64 55ˆ55ˆ16 55ˆ55ˆ16 55ˆ55ˆ16 55ˆ55ˆ64 55ˆ55ˆ64 55ˆ55ˆ64 55ˆ55ˆ64 55ˆ55ˆ128

f conv1 f relu1 f pool1 f f ire1 f f ire2 f f ire3 f pool2 f f ire4 f f ire5 f f ire6 f f ire7 f pool3 f f ire8 f conv10 f relu f pool4 y 224ˆ224ˆ3 111ˆ111ˆ64 111ˆ111ˆ64 55ˆ55ˆ64 55ˆ55ˆ128 55ˆ55ˆ128 55ˆ55ˆ256 27ˆ27ˆ256 27ˆ27ˆ256 27ˆ27ˆ384 27ˆ27ˆ384 27ˆ27ˆ512 13ˆ13ˆ512 13ˆ13ˆ512 13ˆ13ˆ1000 13ˆ13ˆ1000 1ˆ1ˆ1000

#### 4.6.7. AudioNet

To diversify the set of studied neural network models, we built a basic audio recognition model based on a tutorial made available by TensorFlow [166]. This neural network was trained on a speech commands dataset [181], which contains short audio clips with eight simple commands, such as yes or stop. The original dataset represented in the time domain is converted to spectrograms, which are 2-dimensional arrays. Although real-world speech recognition systems are usually based on recurrent neural networks and have more complex structures, this model gives an insight on some other applications of feed-forward networks.

The AudioNet structure has two 2D Convolutional layers, one 2D Pooling layer, two Dense layers and three ReLU layers. Figure 4.26 depicts the model. The AudioNet model has 1.6 million trainable parameters and performs 32.7 million FLOPs for one inference.

x f conv1 f relu f conv2 f relu f pool1 f f lat f dense1 f relu f dense2 y 32ˆ32ˆ1 30ˆ30ˆ32 30ˆ30ˆ32 28ˆ28ˆ64 28ˆ28ˆ64 4ˆ4ˆ64 12544 128 128 8

#### 4.6.8. Time series prediction model

Time series prediction is another example where neural networks succeed. For this model, we employed the structure named 2D-CNNpred presented in [90]. Its objective is to solve a binary classification problem applied to financial time series for stock market prediction. This neural network uses multiple technical market indicators with different time steps, in the form of 2-dimensional arrays, to predict the probability of an increase in the price of a given market for the next day.

The model contains three 2D Convolutional layers each followed by a ReLU activation layer, two 2D Pooling layers and one Dense layer complemented by the Sigmoid activation layer. Figure 4.27 presents the design of this prediction model. The time series prediction model has 1,169 trainable parameters and an inference pass consists of 112,729 FLOPs.

x f conv1 f relu f conv2 f relu f pool1 f conv3 f relu f pool2 f f lat f dense1 f sigmoid y 60ˆ82ˆ1 60ˆ1ˆ8 60ˆ1ˆ8 58ˆ1ˆ8 58ˆ1ˆ8 29ˆ1ˆ8 27ˆ1ˆ8 27ˆ1ˆ8 13ˆ1ˆ8 104 1 1

x

### 4.7. Format for the inference model description

With the formal definition of the inference model semantics established and a clear understanding of the required information for its implementation, we can now work on a suitable format for storing the inference model description.

As stated in Section 2.3, Objective 1, the existence of an unambiguous and human-readable specification is imperative for enabling a certifiable implementation of the inference model. Nonetheless, in Section 3.1 we explained that the existing machine learning frameworks, by default, export the trained models in a serialized format (e.g. Protobuf, PyTorch format, H5). Moreover, the output descriptions usually contain some training-related data, which becomes unnecessary information once the model has been verified and the focus is on implementing it for the inference phase. Finally, as mentioned, we require a format description that is agnostic to the learning framework used.

To address this question, we initially decided to employ a JSON-based file as the format to store the description of the inference model to be implemented. JSON, for JavaScript Object Notation [144], is a data interchange format used to transmit structured data. In the JSON syntax, data is organized as a dictionary of key and values pairs, separated by commas. Although originated from JavaScript, the JSON format can be used independently from this language and finds supports for easy generation and processing in other programming languages. The main advantages of a JSON format for our use case are its lightweight nature, text-based representation and language-independent compatibility. It is therefore highly suitable for an unambiguous description of the inference model structure and parameters. Besides, it favours traceability to the implementation requirements and facilitates debugging.

To create the JSON-based file for our use we adapted the Keras built-in method that exports part of the trained model in a JSON-based format. As mentioned in Section 3.1.3, the model_to_json Keras method exports the structure of the trained model, i.e. information on the type of each layer, its hyperparameters, whether the layer is trainable or not and the data type encoding. The Keras generated file does not include, however, the actual values of the trainable parameters. Other training-related data can also be found, such as the initialization algorithm used to set the initial values of the trainable parameters.

Listing 7 shows the first 2D Convolutional layer of the LeNet-5 model (Example 4.6.2) in the JSONbased file generated by Keras. We observe in Line 2 the definition of the model type as Sequential, or single-path (see Example 4). The ellipsis in Lines 6 and 52 indicate that the "Layer" key contains more elements (i.e. all the layers of the model), omitted in this listing for conciseness. We find the description of parameters introduced in Definition 26: shape of input batch (or input tensor), numbers of filters (or kernels), kernels size and stride. We also observe that the information about a 2D Zeropadding and posterior activation Hyperbolic Tangent layer are introduced within the 2D Convolutional layer description, as evoked in Property 2. Finally, we retrieve the data layout (or data format) of this layer as well as reserved fields for information on weights and biases initializers, regularizers and constraints.

Note in Line 11 that Keras introduces the notion of batch input tensor. The first dimension of this batch input tensor corresponds to the batch, or the number of input data samples that are processed together during a single iteration of the training or inference algorithm. Since Listing 7 concerns the inference model description, this value is set to "null". It means that the value of the batch employed for inference is not specified, as the user can set it according to their preferences.

Listing 8 depicts the same first 2D Convolutional layer of the LeNet-5 model in the modified JSONbased file adapted for our use. The main modifications concern:

(i) the incorporation of the values of trainable parameters, i.e. weights and biases;

(ii) the addition of the sizes of dimensions of the input and output tensors;

(iii) the inclusion of the size of the flattened output tensor, which is useful afterwards for coding;

(iv) the modification of the 2D Zero-padding description so it precisely defines p t , p b , p l and p r ; (v) the exclusion of training-related information. Note that the first dimension of input and output tensors corresponds to the batch size, denoted in Lines 20 and 21 respectively. In the modified format we explicitly set the batch size to one as in our study we treat one inference forward pass at a time (Assumptions 2 and 6).

Our primary objective was to avoid ambiguity in the description of the elements needed to reconstruct and implement the inference model. Embedding the values of weights and biases in the JSON-based file may appear to diverge from the format's purpose of being a lightweight solution. However, this approach facilitates debugging and allows for a self-contained inference model description. Since our work is primarily a proof-of-concept, it stands as a valid argument.

Finally, it is noteworthy that the JSON-based proposed format may not be complete enough to represent the totality of existing inference models of the literature, but it is sufficient to describe the feed-forward neural networks considered in our study.

### 4.8. Conclusion

In this chapter we presented the semantics of the inference model. We started by introducing the notion of tensors, which are treated as multi-dimensional arrays in the machine learning literature. We then presented the formalization of the semantics of each considered layer in the form of mathematical functions, together with illustrative numerical examples.

Afterwards, we presented examples of model transformations that are authorized in the inference model before the implementation phase, as they preserve its semantics. We also introduced different neural network models of the state of the art.

Finally, we presented our adopted format for the inference model description. It is a JSON-based file that relies on the semantics presented in this chapter to provide an unambiguous and human-readable specification, allowing for a certifiable implementation of the inference model.

Henceforth, we focus on the implementation of the inference model and we will introduce ACETONE, our developed framework for C code generation from the inference model description. In the following chapter we present the software architecture of ACETONE. Its front-end comprises the import of the presented inference model description file while its back-end consists of the implementation of the neural networks' functions detailed in this chapter in the C language. { "class_name": "Sequential", "config": { "name": "sequential", "layers": [ ...{ "class_name": "Conv2D", "config": { "name": "conv2d", "trainable": true, "batch_input_shape": [ null, 28,

"dtype": "float32", "filters": 6, "kernel_size": [

5,

5

],

"strides": [

1, 1 ],

"padding": "valid", "data_format": "channels_last", "dilation_rate": [ { "class_name": "Sequential", "config": { "name": "sequential", "layers": [ ...{ "class_name": "Conv2D", "config": { "name": "conv2d", "trainable": true, "dtype": "float32", "nb_kernels": 6, "kernel_size": [5,5],

"strides": [1,1], "padding": [0,0,0,0], "data_format": "channels_last", "dilation_rate": [1,1], "groups": 1, "activation": "tanh", "use_bias": true, "input_shape":

## Chapter 5

## Development and evaluation of the ACETONE framework

In Chapter 4, we established the formal semantics of the inference model in the form of mathematical functions. We also defined a possible format for the unambiguous and textual description of the inference model, in the form of a JSON-based file. Having fixed these two prerequisites, we can now proceed with our objective of implementing the inference model.

This chapter presents our second contribution towards a certifiable implementation of the inference model: the development of ACETONE. The acronym stands for "Avionics C code generator for Neural Networks" and it designates our proposed framework for generating a semantically equivalent and predictable C code from the inference model description. The ACETONE framework has been presented and published in the proceedings of the Euromicro Conference on Real-Time Systems in 2022 [157].

Section 5.1 presents an outline of the philosophy of our approach. Section 5.2 introduces the software architecture of ACETONE, detailing each composing part, namely the front-end, the back-end and its internal representation. Afterwards, in Section 5.3, we describe the adopted methodology used to evaluate ACETONE. We first introduce the criteria for evaluation, then discuss and compare the obtained results with the aforementioned frameworks of the state of the art, Keras2c and Static microTVM. Finally, in Section 5.4, we present a few enhancements that have been integrated to the baseline version of ACETONE to improve its applicability.

### 5.1. Overview of the approach

ACETONE is a framework that automatically generates a C language implementation based on the inference model description. The generated C code is designed to preserve the semantics of the trained model, i.e. replicate the same behaviour observed in the learning environment. To guarantee the semantics preservation we adhere to the mathematical formalism presented in the previous chapter and provide a C back-end with the implementation of the layers' semantics. The resulting C code is also structured to be predictable. In order to do so, we eliminate the use of programming abstractions that may hinder the timing predictability, notably dynamic memory allocation. The schedule, here the sequence of instructions, is also statically resolved. As we propose a solution for the deployment of the inference model in resource constrained system, we were also interested in designing the inference code regarding its memory usage without however performing very fine optimizations in a first place. To that end, we studied and determined the desired memory layout of the binary corresponding to generated C code. In addition, as we were unsure about the best code generation strategy for our requirements, we initially proposed three different C code versions.

ACETONE is entirely written in the Python programming language. We decided to rely on Python mainly for its simplicity and high-level abstractions, allowing quick prototyping and iteration, as well as for its vast ecosystem of packages. Moreover, as explained, it is the programming environment adopted in the front-end of most of machine learning frameworks, which facilitates sharing concepts. Note that ACETONE functions primarily as a tool for easily and quickly generating C code from a specification and our current intention is not to certify it. Thus, only the code produced by it is subject to evaluation according to the objectives defined in Section 2.3. Figure 5.1 depicts the workflow for the C implementation of the inference model within ACETONE. The framework comprises a front-end responsible for importing the inference model description file, which is, by default, the previously introduced JSON-based file. The front-end reads the model structure, extracts the parameters, and creates the corresponding Python objects that serve as the intermediaterepresentation (IR) of the framework. This IR then interfaces with the framework back-end. The ACETONE back-end is dedicated to implementing the inference function in C, proposing three different code generation strategies. Finally, the ACETONE aggregator, as defined within our context, corresponds to a library of auxiliary methods that integrates all the components and creates the C project corresponding to the inference model.

### 5.2. Software architecture of ACETONE

As noted, ACETONE is written in Python. The aforementioned constituents of the framework are in practice Python classes. We have thus formalized the software architecture of ACETONE in the form of an UML class diagram, depicted in Figure 5.2.

Concerning the ACETONE back-end, we conducted a design space exploration (DSE) and proposed three different versions for it, named V1 back-end, V2 back-end and V3 back-end. As mentioned, the different versions correspond to distinct code generation strategies, as we conducted an empirical study about the prospectives of different strategies. Each version will be elaborated upon in Section 5.2.3.

## ACETONE

#### 5.2.1. ACETONE front-end

The first step of the code generation workflow is the import of the inference model description file by the ACETONE front-end. The most important component of the front-end is the load_model method.

The load_model method takes as input the inference model description file. This method parses the description file to discern the structure of the inference model, i.e. which layers are present and in what order, as well as to extract both trainable and non-trainable parameters. It then transforms the inference model in the intermediate-representation (IR) used in ACETONE. Each layer of the neural network is treated as an independent element. Therefore, whenever the presence of a given type of layer is identified in the model during parsing, the load_model method calls a create_layer method to construct the corresponding Layer object. The Layer objects are ACETONE's IR. The model's graph structure is coded directly within the Layer objects, with pointers to the preceding and succeeding layers. Each type of layer has its own associated create_layer method, that takes as input the particular parameters of the layer. The Layer Python class, which defines all supported layers, is detailed in the following subsection. Afterwards, the load_model method returns the Net object, which is a list containing the Layer objects in the correct order, defining the model's graph structure.

Listing 9 depicts part of the load_model method. We observe the create_layer method associated to the Dense layer. Note from the listing (Line 20) that the activation layer that follows this Dense layer is initialized as a parameter of the latter. Indeed, activation layers are often integrated into other non-activation layers because their associated functions are typically applied element-wise to a tensor (see Definition 14). Thus, merging an activation layer with its preceding layer reduces implementation complexity and computational overhead at run time. In the front-end we also find the load_test_dataset method. This method loads a user-provided file with test input tensors and returns a Python array. Alternatively, if no dataset file is provided, the front-end contains the create_test_dataset method. This method generates random test tensors, also Python arrays, which do not have a conceptual meaning but allow to verify the proper functioning of the code generator.

__init__(self, model_file, test_dataset_file = None, nb_tests = None, **kwargs):... def load_model(self): file = open(self.model_file, 'r') model = json.load(file) net = [] l_temp = create_input_obj(idx = 0, output_size = model['config']['layers'][0]['config']['size']) net.append(l_temp) for idx, layer in list((model['config']['layers']), 1): if layer['class_name'] == 'Dense': current_layer = create_dense_obj( idx = idx, output_size = layer['config']['output_size'], input_shape = layer['config']['input_shape'], output_shape = layer['config']['output_shape'], weights = layer['weights'], biases = layer['biases'], actv = self.create_actv_obj(layer['config']['activation'])) elif layer['class_name'] == others: ... l_temp.succ_layers.append(current_layer) current_layer.pred_layers.append(l_temp) l_temp = current_layer net.append(current_layer) return net Listing 9: Core of the ACETONE front-end load_model method.

Finally, the front-end implements the forward_pass method, which interprets the inference model coded in ACETONE's IR. Simply put, this method performs the inference forward pass in the Python environment. In that regard, it takes as input the Net object and the input testing arrays. The Python output of the forward_pass method is used solely for assessing any significant differences between the Python and C implementations of our understanding and formalization of the inference model semantics. We note that the actual reference for evaluating the code generated by ACETONE is the native implementation of the Keras framework, as will be detailed in Section 5.3.

#### 5.2.2. ACETONE IR -Layer class

We have created an abstract Python class named Layer to regroup all the different types of layers supported by ACETONE, i.e. those listed in Chapter 4. As mentioned, the Layer objects are the intermediate representation within the framework, and do the linking between the ACETONE front-end and back-end. The Layer abstract class defines the data attributes that are common to every layer. The common attributes include:

(i) the layer's index (idx), that represents the position of a given layer in the Net object;

(ii) the layer's type (layer_type), that allows to differentiate between the distinct layers;

(iii) the layer's preceding layer(s) (pred_layers), that lists the direct predecessors of the layer;

(iv) the layer's succeeding layer(s) (succ_layers), that lists the direct successors of the layer;

(v) the back-end version to be used (version), that determines the design of the C code generated.

The Layer abstract class also declares two abstract methods. The first method, forward_pass_layer, implements the semantics of the layer in the Python language. The forward_pass_layer methods of each layer, called in the order defined by the layers' indices, constitute the aforementioned forward_pass method of the ACETONE front-end.

The second method, gen_inf_code_layer, implements the layer semantics in the C language and then passes it to the global gen_inf_code_global method, that is defined in the ACETONE back-end and is actually responsible for generating the C source file. The gen_inf_code_layer method is a sort of template engine. Inside this method, the C code to be generated is defined as a template, which is essentially a Python string. There exist different templates according to the code generation strategy adopted by the back-end, as detailed in next section.

Note from Figure 5.3 that we do not have a class to represent the Flatten layer. Indeed, in neural networks this layer is mainly used to manage the difference in dimensions of output and input tensors of successive layers. In the studied use cases it is essentially present between a 2D Convolutional layer and a Dense layer (see Section 4.6). However, since computer memory is inherently linear, i.e. a onedimensional structure, we decided to represent the multi-dimensional tensors defined in Chapter 4 directly as one-dimensional arrays in the C code. It means that every layer deals with 1D arrays and the flattening function is done implicitly. Thus, a dedicated Flatten layer is not needed. Further explanation about flattening options is provided in Section 5.2.5.

Observe that there is no dedicated class for the 2D zero-padding layer either. Indeed, this layer implements a simple mode of padding wherein only constants (zeros) are added to the input tensor. Moreover, we ensure that the inference model description contains the precise parameters to implement it without ambiguity. Thus, during the implementation phase, we seamlessly integrate padding into the 2D Convolutional layer by modifying the edges of the input tensor when iterating over it.

#### 5.2.3. ACETONE back-end

The ACETONE back-end then takes as input the list of Layer objects to compose the inference function code accordingly. As previously stated, the back-end is deployed into three different versions, which are classes that inherit from the principal class. Thus, the gen_inf_code_global is an abstract method that varies in function of the version adopted. See Figure 5.2.

The objective of the design space exploration was to understand what would be the most suited code generation approach for a given inference model and target hardware. For each version, we first present what is produced by the gen_inf_code_layer method, at layer level, and which files are generated by the gen_inf_code_global method. In the following sections we examine the different codes generated for the LeNet-5 model (Example 4.6.2) and in particular its fifth layer, which is of type Dense.

#### 5.2.3.1. Back-end -version 1

The V1 back-end generates a generic implementation of the inference function. A layer is implemented in the C language as a struct data type, whose fields encode its parameters (e.g. type, output size or trainable parameters). The Layer struct is a super type containing all the necessary attributes for the types of layers considered in our work. Thus, every layer has the same definition and their particular parameters are defined as constants in the inference.h header file. The whole neural network is then treated as an array, an indexed linear sequence, of these structures.

Listing 10 depicts the inference.h generated file for the LeNet-5 model. From Lines 3 to 10, we note the declaration of part of the layers' hyperparameters, i.e. non-trainable parameters. We also observe, from Lines 11 to 23, the definition of the Layer struct data type. In Line 24 we note the definition of the data type Net, which is an array of layers. In this version, the gen_inf_code_layer method of each Layer object also produces a generic implementation of the layer semantics. As mentioned, this implementation corresponds to a template that is defined in the Python function. Listing 11 depicts the implementation produced by the gen_inf_code_layer method of the Dense Layer class. We note the presence of weights (Line 6) and biases (Line 7) tensors, as specified in Definition 22. In Line 8 of this listing we also observe the application of the activation associated function to each component of the output tensor of the layer. Listing 12 depicts the first part of global_vars.c file generated by the gen_inf_code_global method for the LeNet-5 model. We retrieve, as float data types, the trainable parameters of the layers that are concerned, essentially Dense and 2D Convolutional layers. In Line 7 we find the weights_Dense_05[30720] variable, an array with 30, 720 floating-point elements corresponding to the weights of the layer of type Dense, that is the fifth hidden layer (05) of this model. Listing 13 illustrates the second part of global_vars.c file. We find now the initialization of the data type Net. In our example Net contains eight elements of type struct, one for each layer of the model. We note that the layer_type is a function pointer, pointing to the functions declared in the layers.c file. The initialization of the remaining parameters for the first layers is omitted for conciseness. In layer number 5, of type Dense, we observe that the weights (Line 19) and biases (Line 20) fields point to the arrays declared above in the same file. The actv_function (Line 21) field is also a function pointer. Lastly, the unused fields are explicitly set to 0x0. Afterwards, the inference function itself is defined in the inference.c file. Listing 14 depicts the inference function within the V1 back-end. It is a generic function in the sense that it is identical for any feed-forward neural network. The inference function is responsible for calling the layers' functions and copying the output of the current layer to the input of the next layer. It consists of two nested for-loops: the first ranges over the number of layers and the second ranges over number of output elements in the current layer. We observe in Line 8 the calls to the C functions of the different types of layers. Finally, from Lines 9 to 12, the output of each layer is transmitted to the next layer. The static keyword in Line 4 forces these variables to be stored in the BSS segment, as further detailed in Section 5.2.4. This logic of having generic definitions both for the layers and inference functions leads to a helpful simplicity in terms of execution and code size. However, using function pointers to generic layer declarations leads to an absence of context about which precise layer is being executed at a time during inference. Consequently, it causes a certain pessimism during WCET analysis. Further discussion on how this approach impacts the WCET analysis is given in Section 5.3.

int (*layer_type)(int, float*, float*); // Function pointer int layer_output_size; int pad_right; int pad_left; int pad_bottom; int pad_top; int stride_h; int stride_w; int pool_size_h; int pool_size_w; int kernel_size_h; int kernel_size_w; int nb_filters; int input_height; int input_width; int input_channels; int output_height; int output_width; float *weights; float *biases; float (*actv_function)(float); // Function pointer }; struct Layer Net[nb_layers]; int inference(float *output_tensor, float *input_tensor); #endif Listing 10: Example of an inference.h file within the V1 back-end for the LeNet-5 model (Example 4.6.2).

struct layer Net[nb_layers] = { [0] = { .layer_type = Input_layer, ...}, [1] = { .layer_type = Conv2D, ...}, [2] = { .layer_type = AveragePooling2D, ...}, [3] = { .layer_type = Conv2D, ...}, [4] = { .layer_type = AveragePooling2D, ...}, [5] = { .layer_type = Dense, .layer_output_size = l5_output_size, .pad_right = 0x0, .pad_left = 0x0, .pad_bottom = 0x0, .pad_top = 0x0, .stride_h = 0x0, .stride_w = 0x0, .pool_size_h = 0x0, .pool_size_w = 0x0, .kernel_size_h = 0x0, .kernel_size_h = 0x0, .dilation_rate = 0x0, .nb_filters = 0x0, .input_height = 0x0, .input_width = 0x0, .input_channels = 0x0, .output_height = 0x0, .output_width = 0x0, = { .layer_type = Dense, ...}, [7] = { .layer_type = Dense, ...}, [8] = { .layer_type = Softmax, ...}}; Listing 13: Example of the second part of the global_vars.c file generated within the V1 back-end for the LeNet-5 model (Example 4.6.2).

#### 5.2.3.2. Back-end -Version 2

In the V2 back-end, the inference function is tailored for a given inference model. This constitutes the main difference compared to the V1 back-end. In this version, the gen_inf_code_layer method of each Layer object produces a customized implementation of the layer semantics. In practice, for each layer present in the inference model, its hyperparameters are replaced within the template included in the Python method, thus the generated C code contains these hyperparameters hard-coded.

Listing 15 depicts the implementation produced by the gen_inf_code_layer method of the Dense Layer class, in this case tailored for the Dense_05 layer of the LeNet-5 model. We retrieve in this listing the layer's hyperparameters hard-coded in the body of the function: the number 120 in Line 2 corresponds to layer_output_size and the number 256 in Line 4 corresponds to the previous layer_output_size (see Listing 11 for comparison). The layer's trainable parameters (weights_Dense_05 and biases_Dense_05) are still defined in a different C file. Finally, in Line 7 we find the code of the activation layer associated function, a Hyperb_Tan, directly integrated in the Dense layer's function body.

Note that the code represented in Listing 15 is not a C function by itself. Indeed, it will be integrated in the inference.c file, as detailed subsequently.

The gen_inf_code_global method of the V2 back-end generates the following C files: (i) global_vars.c: containing the layers' trainable parameters; (ii) inference.h: presenting the declaration of the inference function; (iii) inference.c: presenting the tailored implementation of the inference function. Since the layers' functions have a tailored implementation, with hard-coded hyperparameters, the notion of a generic Layer struct no longer exists. Thus, the generated global_vars.c of the V2 back-end only contains the trainable parameters initialization. It is then equivalent to Listing 13, seen previously. The inference.h contains the trainable parameters declaration with the extern keyword, as well as the declaration of the inference function.

int inference(float output_tensor[Net[nb_layers-1].layer_size], float input_tensor[Net[0].layer_size]) { static float output_previous[l_size_max], output_current[l_size_max]; Net[0].layer_type(0, input_tensor, output_previous); // Type of layer with index 0 = Input layer for (int i = 1; i < nb_layers; ++i){ Net[i].layer_type(i, output_previous, output_current); for (int j = 0; j < Net[i].layer_size; ++j){ if (i < nb_layers-1) output_previous[j] = output_current[j]; else output_tensor[j] = output_current[j]; } return 0; } Listing 14: Example of an inference.c file within the back-end V1 back-end.

Finally, as mentioned, the generated inference.c file is completely customized for a given inference model. The inference function is entirely inlined and contains all the layers implementations directly written to the C function body, removing any function calls. Listing 16 depicts the tailored inference.c file for the LeNet-5 model. We note that the code of a given type of layer is repeated as many times as this type of layer is identified in the inference model. We also observe in Lines 28 and 29, a sequence of instructions responsible for passing the results of a layer computation to the next layer.

The direct expected effect of this code generation approach is the improvement in execution time performance with respect to the V1 back-end, since the overheads due to functions calls and struct parsing are eliminated. However, it comes at the cost of using more instruction space, as we duplicate code, producing larger source files, which can be prohibitive in an embedded environment. Nonetheless, since we are able to provide the correct context in which layers are executed, it is also expected to reduce the WCET overestimation.

#### 5.2.3.3. Back-end -Version 3

In the V3 back-end the inference function is also customized for a given inference model. However, we adopt a different approach from the previous versions and use a philosophy of full in-lining (with loop unrolling) that can be seen à la SCADE [40].

In this version, the gen_inf_code_layer method of each Layer object yields a tailored implementation of the layer semantics. Internally, the Python method uses the existing template to directly unroll the loops of the function and outputs the expanded code. Consequently, like in the V2 back-end, we do not have the notion of a generic Layer struct.

Listing 17 presents the beginning of the code produced by the gen_inf_code_layer method of the Dense Layer class. It contains only part of the instructions of the Dense_05 layer of the LeNet-5 model. Note the total absence of for-loops. Differently from the V2 back-end, the trainable parameters, weights_Dense_05[i] and biases_Dense_05[i], are also written in the body of the function and not stored in an external file. It implies that a global_vars.c file no longer exists.

The gen_inf_code_global method of the V3 back-end generates the following C files: (i) inference.h: presenting the declaration of the inference function;

i = 0; i < 120; ++i){ dotproduct = 0; for (int j = 0; j < 256; ++j) dotproduct += output_pre[j] * weights_Dense_05[(i + 120*j)]; dotproduct += biases_Dense_05[i]; output_cur[i] = (exp(dotproduct)-exp(-dotproduct))/(exp(dotproduct)+exp(-dotproduct)); // Hyperb_Tan } Listing 15: Implementation of the Dense_05 layer of LeNet-5 produced by the gen_inf_code_layer method of the Dense Layer class in V2 back-end (part of inference.c file).

(ii) inference.c: presenting the implementation of the tailored unrolled inference function.

As for the V2 back-end, the inference.c file contains the inference function wherein the implementation of each layer of the model is completely adapted for it, including its loops unfolded and trainable parameters disclosed. We do not depict this code in a listing because it becomes quickly unreadable, but Within the V3 back-end we notably eliminate the computational overhead due to the branching on the termination condition of loops. We also get rid of the latency of reading data from memory, since everything needed for the layers operations is self contained in a C source file. Additionally, we remove incertitude about the execution path, which is advantageous for the WCET analysis. However, it worsens the drawback already identified in the V2 back-end: the instruction space becomes huge and for large inference models, this approach is not sustainable.

#### 5.2.4. Memory layout strategy

The memory layout of a C binary is segmented into discrete blocks with specific roles. We mainly focus on the stack, data, BSS and text segments. Note that since we abolish dynamic memory allocation, we do not use the heap segment. Figure 5.4 depicts the discussed memory sections.

The stack segment supports the passing of data and control between functions, as well as allocates the local variables of a function. The stack is grown or reduced on a function call or return, respectively.

We try to restrict stack usage due to its limited space and also because it is preferable that objects addresses are resolved at compilation time, both for worst and average execution times. Indeed, as the base address of the stack may be unknown before run time, it adds uncertainty to the WCET estimation and increases the pessimism of the WCET analysis.

In the V1 back-end implementation, the stack segment essentially contains the input and output tensors of the inference function and the calls to the layer's functions (present in the inference.c file). In contrast, in the V2 back-end and V3 back-end implementations, the stack no longer has to handle the calls to the layer's functions.

The data segment contains the initialized global and static C variables and its size does not change at run time. Uninitialized global and static C variables, along with any global or static variables that are initialized to zero, are present in the BSS segment. At run time, uninitialized variables are assigned an initial value of zero in memory.

Local function variables defined with the static attribute are not managed by the stack. Instead, the compiler reserves space in data or BSS segments for each definition and generates a distinct local linker symbol in the symbol table. In our implementations, the intermediate tensors exchanged between layers (i.e. output_previous and output_current) are stored in the BSS segment. In the same segment, we also find the local variables used to store intermediate results within the layers functions computations (e.g. dotproduct, sum, max).

Finally, in the text segment we find the machine code of the compiled program as well as read-only data. In our work, we defined the inference model constant parameters, in particular weights and biases tensors, with the const attribute. Doing so allows us to statically allocate all the required memory at compile time and then use the text segment. Storing the model trainable parameters as read-only data also prevents mistaken access during run time.

#### 5.2.5. Memory layout of tensors

As previously noted, the multidimensional tensors defined in Section 4.3 are directly represented as onedimensional arrays in the C code, which allows storing them in a linear memory address space. The data layout of 3D tensors can follow six combinations, but two formats are of particular interest for the operations performed within neural networks. We name them channels-first or channels-last layout.

dotproduct += output_previous[0] * -0.142333168; dotproduct += output_previous[1] * 0.072229677; dotproduct += output_previous[2] * -8.256957637; ... dotproduct += output_previous[253] * 0.028684311; dotproduct += output_previous[254] * 0.125187222; dotproduct += output_previous[255] * 0.047727926; dotproduct += 0.001061838; // biases_Dense_05[0] output_cur[0] = (exp(dotproduct)-exp(-dotproduct))/(exp(dotproduct)+exp(-dotproduct)); Listing 17: Implementation of the Dense_05 layer of LeNet-5 produced by the gen_inf_code_layer method of the Dense Layer class in V3 back-end (part of inference.c file).

In the channels-first convention, the elements along the width dimension are stored consecutively in memory. The elements along the height dimension have a stride of n w . Finally, the elements along the channel dimension are stored with a stride of n h ¨nw . The opposite is done when the data layout follows the channels-last convention: the corresponding elements of different channels are stored consecutively in memory. Within a channel, the elements along the width dimension have a stride of n c . Lastly, the elements along the height dimension have a stride of pn w ¨nc q.

Figure 5.5a illustrates the data layout with the channels-first format and Figure 5.5b shows the data layout with the channels-last format. In both examples, we have n c " n h " n w " 3. Note that the flattening operation definition (see Definition 20) does not change whether we adopt the channels-first or channels-last convention: the different lies on the way the elements are arranged within the 3D tensor.

This data layout nomenclature may appear counter-intuitive since in the channels-first convention, the channel dimension is the last to be unfolded with regards to the other dimensions of the tensor, and conversely. However, it is due to a historical terminology adopted by machine learning frameworks that has sort of a visual meaning, more end-user oriented, and is not linked to the real implementation. Indeed, the channels-first format is usually noted as n c ˆnh ˆnw , for channels-height-weight, while the channels-last convention is referred to as n h ˆnw ˆnc , for height-width-channels.

The most suitable memory layout between channels-first and channels-last depends on the operations performed within the layer but also on the values of its parameters. For instance, the 2D Pooling layer associated function (see Definition 23) is carried out on elements within a window of one channel at a time, before advancing through the remaining channels of the tensor. Thus, it is intuitive to see that this operation takes advantage of the spatial locality of the channels-first data layout.

Table 5.1 presents the number of processor cycles taken to execute a 2D Pooling layer on an ARM Cortex-A15 processor (see Section 5.3.3) with the channels-first convention, as well as the percentage of increase when using the channels-last format. The chosen pooling configurations are only a fraction of all those that are possible, but are representative enough of the type of tensors found in the literature (see the examples of Section 4.6). We observe that the channels-first layout outperforms its counterpart in almost every input configuration tested, except for the configuration in third column of Table 5.1, wherein I " p27 ˆ27 ˆ192q. We explain this by the fact that in this case, the tensor dimensions are rather small so the entire tensor fits in the cache. It follows that the data layout convention under these circumstances does not greatly influence the execution time. In the case of 2D Convolutional layers, as detailed in Definition 26, each convolutional kernel requires a set of elements from every channel of the input tensor. Hence, it is not straightforward to determine which memory layout will outperform the other when applying a direct convolution algorithm. However, in Chapter 6 we present an implementation of the 2D Convolutional layer that consists in mapping the 3D input tensor to a 2D tensor, unfolding the convolution operation into a matrix-matrix multiplication. In this case, where height and width dimensions are combined, the channels-first data layout is more appropriate [122].

3,3,1 2,3,1 1,3,1 3,2,1 2,2,1 1,2,1 3,1,1 2,1,1 1,1,1 3,3,2 2,3,2 1,3,2 3,2,2 2,2,2 1,2,2 3,1,2 2,1,2 1,1,2 3,3,3 2,3,3 1,3,3 3,2,3 2,2,3 1,2,3 3,1,3 2,1,3 1,1,3 n w n h n c 1,1,1 2,1,1 3,1,1 1,2,1 2,2,1 3,2,1 1,3,1 2,3,1 3,3,1 1,1,2 2,1,2 3,1,2 1,2,2 2,2,2 3,2,2 1,3,2 2,3,2 3,3,2 1,1,3 2,1,3 3,1,3 1,2,3 2,2,3 3,2,3 1,3,3 2,3,3 3,3,3 (a) Channels-first data layout. 1,1,3 1,1,2 1,1,1 0,1,3 0,1,2 0,1,1 1,1,3 1,1,2 1,1,1 1,2,3 1,2,2 1,2,1 0,2,3 0,2,2 0,2,1 1,2,3 1,2,2 1,2,1 1,3,3 1,3,2 1,3,1 0,3,3 0,3,2 0,3,1 1,3,3 1,3,2 1,3,1 n w n h n c 1,1,1 2,1,1 3,1,1 1,2,1 2,2,1 3,2,1 1,3,1 2,3,1 3,3,1 1,1,2 2,1,2 3,1,2 1,2,2 2,2,2 3,2,2 1,3,2 2,3,2 3,3,2 1,1,3 2,1,3 3,1,3 1,2,

## Number of cycles

## Data layout

## Input tensor p24 ˆ24 ˆ6q

k h " k w " 2 s h " s w " 2 p224 ˆ224 ˆ64q k h " k w " 2 s h " s w " 2 p27 ˆ27 ˆ192q k h " k w " 3 s h " s w " 2 p224 ˆ224 ˆ224q k h " k w " 2 s h " s w "

Assumption 7 (Channels-first as the data layout in ACETONE). In all the back-end versions of ACETONE, we implemented the channels-first data layout.

### 5.3. Comparative evaluation of ACETONE

In order to test in practice the advantages and limitations of ACETONE, as well as its behaviour compared to other frameworks in the literature, we defined the following comparative evaluation methodology.

Firstly, we selected a set of representative benchmarks from the machine learning state of the art and that are coherent with the type of neural networks targeted in this study, i.e. feed-forward networks composed of the particular layer types introduced in Section 4.4. Specifically, we relied on the inference models presented in Section 4.6. The objective was to carry out a large test campaign by varying several parameters (e.g. number and type of layers, data type of parameters).

We then defined a certain number of evaluation criteria based on the certification objectives derived in Section 2.3. We will therefore assess:

(i) the semantics preservation (Objective 2);

(ii) the worst-case execution time (Objective 4); (iii) the average execution time (Objective 5);

(iv) the memory layout of executables (Objective 5). We note that not all criteria require the same assessment strategy: computing the WCET, for example, needs to be done once whereas the average execution time measurements need to be repeated several times. Finally, we chose two open-source inference frameworks, also capable of generating a static C code from an inference model, to compare with ACETONE's approach. We elected Keras2c and Static microTVM, previously presented in Section 3.2.2.2.

#### 5.3.1. Semantics preservation assessment

#### 5.3.1.1. Criterion definition

The first evaluation criterion concerns the semantics preservation as stated in Objective 2. We aim to confirm the capacity of our approach to reproduce on the target the result of the inference pass observed in the training framework. As explained, we formally defined the semantics of neural networks in Chapter 4 and then coded them in C language, through ACETONE. Now we want to verify that training and deployment outputs are close enough, i.e. verify that we correctly understood and implemented the inference model semantics as defined in machine learning frameworks. For the purpose of this evaluation, we consider a k-dimensional tensor in its flattened form, i.e. a 1D tensor (see Definition 11).

Criterion 1 (Semantics preservation). Let T " pT 1 , T 2 , . . . , T n q be the output tensor produced by the inference pass in the training framework for a given input tensor I. Let T " p T1 , T2 , . . . , Tn q be the output tensor provided by the C code execution for the same input tensor I.

We define the absolute error as:

∥ T ´T ∥ 8 " max 0ďiďn }p T ´T q i } (5.1)

When comparing the outputs of Python (training framework) and C (deployment framework) programs, we expect differences related to floating-point arithmetic operations, including rounding, truncation and accumulation errors. Furthermore, we must also consider that computations are potentially done in different orders in the two implementations. The gap observed when comparing both results should however lay in a sufficiently narrow range, which depends on the type of application the inference model is used for. In this thesis we do not provide numerical values for the accepted range, as it will be the responsibility of the system designer to decide on an acceptable bound with rationale and convince the certification authorities of its pertinence.

We thus define that the norm described in Criterion 1 asserts a maximum bound on the error observed when comparing both implementations for a given input tensor and it is requested to be minimal. For this requirement we must, however, acknowledge that the numerical floating-point precision in decimal digits according to the IEEE-754 standard [92] is of approximately 10 ´7 in single-precision and 10 ´16 in double-precision.

#### 5.3.1.2. Experimental results

We use Criterion 1 to compute the maximal observed error over 1, 000 test input tensors when the generated codes were executed on a x86 target. We experimented with a consequent number of inputs to understand to what extent the observed errors were related to the input tensors numerical values.

For the results evaluation we clarify that for ACETONE and for Keras2c, the reference training framework was Keras, and for Static microTVM it was TensorFlow Lite. Also, the three back-end versions (V1, V2, V3) provided in ACETONE encode the same semantics and we could verify that they produce the exact same outputs, so no need to make them all appear. Finally, we could not analyse the semantics preservation of AlexNet and VGG-16 models with Keras2c nor Static microTVM. Indeed, these frameworks were not able to handle such models with a great number of parameters: Keras2c required relying on dynamic memory allocation and Static microTVM was not able generate a C code for them.

The results for the semantics preservation assessment using single-precision floating-point data are shown hereafter. Table 5.2 depicts the results obtained for the ACAS-Xu fully-connected models and Table 5.3 illustrates the measured differences observed for the convolutional inference models. We note that all the frameworks produce very similar results with maximum errors of the order of 10 ´6 for all the benchmarks tested in single-precision FP.

## Maximum error

## Framework

## Model

## ACAS-Xu reg50

ACAS-Xu reg100

## ACAS-Xu reg200

ACAS With ACETONE, we were also able to conduct experiments to verify the semantics preservation using double-precision floating-point data. We could not do the same with Keras2c and Static microTVM as they do not offer the support for double-precision FP operations. From Table 5.4 we can observe that the errors detected are accordingly smaller, now of the order of 10 ´15 .

As explained above, no numerical value is fixed concerning the maximum tolerated error to assure the semantics preservation of an inference model deployment. However, we observe that only one significant digit is lost in both cases given the numerical floating-point precision stated in the IEEE-754 standard [92]. The observed errors can be considered acceptable seeing the number of calculations performed in the inference function and we conclude that the semantics preservation is met by all methods.

#### 5.3.2. Worst-case execution time assessment

#### 5.3.2.1. Criterion definition

The second evaluation criterion concerns the timing predictability of a software item as defined in Objective 4. Moreover, as referenced in Assumption 3, we wish to rely on static WCET analysis to assert the timing predictability of a program on a given target.

## Criterion 2 (Worst-case execution time). Estimation of the worst-case execution time of an inference model program trough static analysis with the OTAWA tool.

We select OTAWA [21] because the tool is open-source, presently maintained, and it features an ample set of techniques in terms of analysis. Moreover, it is developed at the TRACES team at the IRIT laboratory of the University of Toulouse, a group we work closely with. OTAWA supports the ARM instruction set but does not contain the micro-architecture model of the ARM Cortex-A15 processor, which is the target used to deploy the studied inference models, as will be detailed in Section 5.3.3. In order to assess timing predictability, we thus compile each C code for a lpc2138 ARM-based target. Since we are not able to perform evaluations with the same target, we do not correlate results for WCET and average measured execution times. Such a comparison would not allow us to determine how much of the discrepancy between WCET bounds and measured execution time results comes from the code itself or from the accuracy of the analyser.

Our objective is not to ascertain the accuracy of the bounds provided by OTAWA or to compare them with those obtained by a commercial analyser. Instead, we want, firstly, to ensure that the code generated by ACETONE is statically analysable. A second objective is to compare the different variants of the generated code with the code produced by state-of-the-art frameworks, by means of a single analysis tool that provides a common basis for comparison.

#### 5.3.2.2. Experimental results

To estimate the WCET, according to Criterion 2, OTAWA requires user annotations with flow-facts information. These constitute additional information about the control flow of the program. They are used to tighten the WCET estimates by limiting the set of paths to explore in the control-flow analysis. Examples of provided flow-facts are loops bounds and targets' addresses for indirect function calls (e.g. function pointers). Listing 18 depicts an example of the flow-facts file that must be completed and provided to OTAWA for the compiled inference project generated by the V1 back-end of ACETONE for the inference model ACAS-Xu decr128. The gray-highlighted code segments were originally question marks introduced by OTAWA and correspond to user provided flow-facts information. The commentary in Line 3, for example, indicates that there is an indirect call inside the function inference, in line 5 of the inference.c source file. Inspecting the source code, we see that it corresponds to the call to the Input_layer function (see Listing 14). Thus, the user can refer to the assembly file and complete the flow-facts file with the address to the Input_layer function, which in this instance corresponds to address 0x8244. The requested address in Line 4 asks for more information about the indirect function call in Line 8 of the inference.c file. In this model we only have Dense layers, so it is the address of the Dense function, which can also be found in the assembly file.

In Line 6 of Listing 18, OTAWA requires information about the loop bounds in the main.c file. It corresponds to a loop that calls the inference function as many times as there are test input tensors. As we are interested in the WCET of one inference run, we indicate that the inference function is called at least once and at most once (min 1 max 1). Likewise, in Line 8 we must provide the bounds for the loop in Line 7 of inference.c: it corresponds to the number of layers in this model, which is equal to 6. Finally, the loop indicated in Line 9 is the one that iterates over the number of units in each layer, in the case of the ACAS-Xu decr128 it ranges from 5 to 128 (see Example 4.6.1). It is precisely in this point that the WCET analysis is penalized in the code generated by ACETONE V1 back-end. As we cannot make the difference between the different instances of the Dense function, OTAWA is obligated to consider that 128 is the upper bound for all the five Dense layers of the ACAS-Xu decr128 model. Listing 18: Flow-facts required by OTAWA to analyse the code for the ACAS-Xu decr128 model provided by the ACETONE V1 back-end.

Listing 19 shows the flow-facts file for the same ACAS-Xu decr128 model, generated by the V2 backend of ACETONE. We note that there are no longer indirect function calls, as explained in Section 5.2.3.2 and depicted in Listing 16. We thus only need to provide loop bounds corresponding to the Dense layer function, which has two-nested loops, as depicted in Listing 15. Moreover, it is possible to supply the precise bounds for each instance of this layer.

Obtaining flow-facts information for the code generated by ACETONE was straightforward and making this process automatic is part of future perspectives. For Keras2c and Static microTVM, we had to slightly modify the generated code to make sure to analyse only the inference code (as we did for our code), and to leave the initialization functions out of the WCET computation. OTAWA was not able to provide WCET bounds for the code generated by the ACETONE V3 back-end, nor for AlexNet and VGG-16 inference models. Indeed, the binaries of these programs are too large and the tool runs out of memory during the analysis.

Table 5.5 depicts the obtained results for the worst-case execution time estimation with OTAWA for the codes generated by ACETONE V1 back-end, V2 back-end, Keras2c and Static microTVM. Analysing this table, we observe that the design choices applied in the C code have a significant impact on the WCET bounds that can be derived by OTAWA. This is not simply a matter of performance optimizations, but also of the ability to provide precise flow-facts information to the analyser. Listing 19: Flow-facts required by OTAWA to analyse the code for the ACAS-Xu decr128 model provided by the ACETONE V2 back-end. function, we are unable to provide contextual information about the layers function calls. OTAWA thus assumes that each call to a layer function is a call to the most expensive layer of this type. We note that when all the layers of the model have the same numbers of units, such as the ACAS-Xu regular structures (reg50, reg100 and reg200 ), this impact is reduced. When it is not the case, such as for the ACAS-Xu decr128 and decr256 models, the WCET estimation pessimism is more pronounced. Hence, we conclude that the numerical results of the WCET analysis of ACETONE V1 back-end and Keras2c codes are excessively pessimistic and inaccurate.

## WCET [cycles]

In ACETONE V2 back-end the inference function is inlined and the different layers are implemented as sequences of independent loops. Therefore, we are able to provide OTAWA with precise information about loop bounds, as depicted in Listing 19. In Static microTVM, as showed in Listing 5 of Section 3.2.2.2.2, each layer of the model is implemented in a tailored independent function, that is called in the correct order in the main inference function. Consequently, OTAWA is also able to benefit from contextual information about the layers' calls with this approach.

#### 5.3.3. Average execution time assessment

#### 5.3.3.1. Criterion definition

The third evaluation criterion concerns the requirement for an efficient resource usage as defined in Objective 5. Indeed, performance, in terms of average execution time, is not the main priority in safety-critical systems. However, it deserves to be addressed as we are working in a resource-constrained environment. To this end, for ACETONE, Keras2c and microTVM, we aim to understand how the usage of hardware resources is reflected in the time the program takes to execute.

## Criterion 3 (Average execution time). Average of the observed times of 50 executions of the inference model program, using the same input tensor, on an ARM Cortex-A15 processor.

As evoked in Assumption 6, within the scope of this thesis we chose to deploy the studied inference models in a multi-core COTS processor. We, however, rely on a single-core bare-metal implementation to better isolate the challenges that are particular to the machine learning item and not hardware-related. This clarifies why we compute the average solely based on 50 iterations: the inference function is a predictable algorithm being executed on a bare-metal configuration, thus variations in execution times are very limited.

In particular, we conducted execution time experiments on the COTS Texas Instruments Keystone II SoC [168]. This SoC integrates an ARM Cortex-A15 processor quad-core cluster, implementing the ARMv7-A architecture. ARM processors are widely employed in many domains, including resourceconstrained environments, and are thus the chosen target for our application.

In order to measure quantitative results for the performed experiments, we used the performance monitor unit (PMU) [18] present in the ARM Cortex-A15 core. The PMU architecture uses specific codes to identify a certain number of events, then associates an event to a counter so that only one event is monitored at a time. The advantage of using PMU counters directly is that they are natively implemented and thus do not require any external monitoring feature. It guarantees accuracy and minimizes the impact of the measurements collection process on the analysed values. The studied core has six configurable event counters plus a specific cycle counter.

Our measurement methodology consisted in (i) selecting the event counter to use and assign an event to track; (ii) resetting the existing counter value; (iii) reading the selected counter register; (iv) executing the code portion under analysis and (v) reading the final value in the selected counter register.

#### 5.3.3.2. Experimental results

Addressing Criterion 3, we measured inference times on an ARM Cortex-A15 core. For all experiments, caches were activated and we put data (data and BSS) and code (text) sections in the DDR. Another alternative would be to place all or some of those segments in the SRAM, which is faster but has limited space (6MB against 2GB). We chose to place all the sections in DDR in order to evaluate the performance of the generated inference code itself, avoiding the complexity associated with the transfer of data between DDR and SRAM. For compilation we relied on the GCC compiler and C codes were compiled without any optimization level (-O0 flag), as of Assumption 5. We used the compilation flag mfloat-abi=hard in order to use the NEON floating-point unit of the processor.

We could not run the AlexNet and VGG-16 inference models on our ARM Cortex-A15 target due to memory limitations. Besides, the code generated by ACETONE V3 back-end also could not be tested for the same reasons. Table 5.6 shows the results for the measured average execution times for each framework and inference model. From Table 5.6 we observe that, as expected, the impact of the different frameworks' design choices are directly translated in the measured average execution times. We note that among the back-end versions proposed by ACETONE, it is the code generated by the V2 back-end that produces the shortest average execution times. As explained, when compared to the V1 back-end, this version reduces the overhead of calling the different layers' functions since they are already inlined in the inference function source code. The hyperparameters of the model are also hard-coded, which reduces much of parsing complexity during run time.

## Average execution time [cycles]

Moreover, we note that the strategy of full inlining and unrolling the inference function adopted in V3 back-end is beneficial for small models, as noted for the ACAS-Xu reg50 and reg100 models. However, this approach quickly reaches its limits as the size of the model augments, as observed starting from ACAS-Xu decr128 model and pronounced by the inability to execute the convolutional models. Observe, nonetheless, that the V2 back-end is consistently better than the V3 back-end even for small models. We could attribute it to a better usage of the instruction cache in the V2, which exploits temporal locality within the loops.

We note that the V2 back-end has even better measured average execution times than Keras2c and Static microTVM for fully-connected networks (i.e. the ACAS-Xu models), and is only slightly slower that Static microTVM for convolutional models. Indeed, Static microTVM employs finer optimizations in the generated code, relying on microTVM back-end. They include, for example, layout optimizations (variations of those presented in Section 5.2.5), operators fusion and constant folding. These optimizations seem to have a greater influence on convolutional neural networks than on simpler fully-connected models. We investigated it further and a deeper discussion on strategies to optimize convolutional models is provided in Chapter 6.

Finally, we observe that Keras2c has the largest measured average execution times for all the benchmarks. We attribute that mainly to the framework's strategy of declaring the layers' trainable parameters in the inference source code. In this manner, these parameters are allocated in the stack segment in memory (see Section 5.2.4) and there is an overhead due to the need of copying these parameters from the text to the stack sections.

#### 5.3.4. Memory layout assessment

#### 5.3.4.1. Criterion definition

The fourth evaluation criterion is also related to the request for an efficient resource usage as defined in Objective 5. With this purpose, we aim to ascertain whether ACETONE's approach appropriately utilizes the available memory resources and compare it with the choices of Keras2c and Static microTVM.

## Criterion 4 (Memory layout of executable). Description of the organization of the inference model executable's contents in the different memory segments.

The objective of having a detailed description of the executable's memory layout is to compare the size of the compiled code in general and especially evaluate the stack usage. It is noteworthy that minimizing both binary size and stack usage is particularly interesting.

#### 5.3.4.2. Experimental results

Following Criterion 4, we analysed the binary's memory layout of the generated codes when compiled to an ARM Cortex-A15 core. For the sake of simplicity, we only present the results obtained for the ACAS-Xu reg50 model, as the same trend is observed for all the inference model programs.

Table 5.7 illustrates the differences in the memory usage strategy among the different frameworks. Following the discussion of Section 5.2.4 for the different back-ends of ACETONE, we observe that the stack usage in the V1 back-end is bigger compared to the others versions. It is due to the function calls from the inference function, even if in this model there are only calls to two functions: Dense and ReLU functions. Concerning the data segment, it contains essentially the model's trainable parameters.

In the V1 back-end however it includes also the struct of layers declaration.

With respect to the BSS segment, all versions provide the same value: it corresponds essentially to the intermediate tensors inside the inference function (output_previous and output_current), together with other auxiliary variables in the main function. We also observe that the unrolled-loops strategy adopted in the V3 back-end greatly increases the text section and the overall binary sizes, making it notably bigger compared to the other solutions.

We note that because Keras2c allocates all the trainable parameters inside the inference function code, its binary stack size is higher than for the other frameworks. Moreover, the trainable parameters shall also be present in the text segment, together with Keras2c back-end, which is a static C library with the layers' functions (see Section 3.2.2.2.1).

Static microTVM also stores the model parameters as constants, which results in a memory distribution very similar to ACETONE. The former however writes the layers' trainable parameters as byte arrays, which is not favourable for traceability requirements and uses the same memory size (data section) as arrays of floats (see Section 3.2.2.2.2).

Our stack usage measurement performed on the target during run time is coherent with the stack usage estimation given by GCC.

#### 5.3.5. Discussion of comparative evaluation results

In this section, we presented a comparative analysis of the code generation approach of the three back-end versions of ACETONE, alongside two frameworks from the state of the art, with respect to the predefined criteria: the semantics preservation, the worst-case execution time, the average execution time and the memory layout of executables. Through careful evaluation, we aimed to discern their main differences and identify potential axes for enhancement within our framework.

Upon thorough comparison, we observed that all three versions of our software were found to satisfactorily address Criterion 1. Concerning Criterion 2, OTAWA was able to produce tighter WCET bounds for the V2 back-end when compared to V1 back-end, while it could not analyse the binary of the V3 back-end because of memory limitations. In addition, the V2 back-end demonstrated a slight superiority in both Criterion 3 and Criterion 4. We can thus conclude that, among the code generation approaches proposed in ACETONE, the V2 back-end offers a good compromise between generality and customization of the inference function.

Furthermore, our experimental findings underlined ACETONE's competitive capability relative to the state of the art. Through testing and validation, we have demonstrated our capacity to not only match but also occasionally exceed Keras2c and Static microTVM results in terms of the initially defined criteria. These outcomes reaffirm the pertinence of our work towards a solution for a certifiable implementation of the inference model. We highlight, however, ACETONE's predominant identified limitation: the performance, computed in terms of measure average execution time, of convolutional neural networks.

### 5.4. Extending the applicability of ACETONE

We proved that ACETONE is capable of answering the initially defined certification-oriented requirements for the implementation of the inference model. Nevertheless, as previously indicated, a few axes of improvement within the framework were identified, including its performance, usability, and scalability. Indeed, the methods and experimental results presented in this chapter constitute the original working prototype of ACETONE. They form the basis of an approach that can be easily extended due to its modular philosophy.

In the context of this thesis, we followed one improvement track, centring our efforts on improving the implementation of 2D Convolutional layers. Further details regarding this work is provided in Chapter 6. However, additional research in progress at ONERA focuses on improving ACETONE's usability and applicability for our research partners by adding new features to the framework. This version under active development is also freely available onlinefoot_1 . We briefly outline these works herein.

## Inference model importers

The first improvement constitutes the addition of other model importers in the ACETONE front-end, which allows exploiting different description formats other than our customized JSON-based file. At the moment ACETONE contains working importers for both ONNX and NNet formats.

The inclusion of an ONNX importer is primarily motivated by the initiative for the development of a safety-critical profile for this format, mentioned in Section 3.1.4. The ONNX importer integrated in ACETONE relies on the ONNX-provided Python module. The ONNX importer extracts from the ONNX model the information needed to create the Layer Python objects in ACETONE. On the other hand, the incorporation of a NNet importer relies on the fact that because of its clarity this format remains the most used to represent the fully-connected models of the ACAS-Xu avionics study case.

## Inference model structures with skip connections

In the scope of this thesis we focused on single-path neural networks (Example 4). As previously explained, in these configurations each layer receives input only from the previous layer. However, it is alternatively possible that the output of one layer is fed not only to the next layer but also to a layer beyond the next one. This creates shortcuts or skip connections that allow information to bypass one or more layers. Inference models like ResNet and DenseNet, which include skip connections in their structure, outperform singlepath models like VGG-16 and AlexNet and have a smaller number of parameters, being more adapted to resource-constrained environments.

Adding the support for such inference models was straightforward. As delineated in Section 5.2.2, each Layer object contains attributes to store the list of its direct predecessors and successors. For single-path models, these attributes only point towards one element, as each layer only has one predecessor and one successor. Thus to support inference model structures with skip connections it was necessary to first adapt the model's parsing method and then add a topological sorting algorithm, to order the different nodes, or layers, of the model.

Adapting the parsing method was necessary to guarantee that all the Layer objects expressed all the dependencies concerning the previous and next layers. Afterwards, a topological sorting algorithm was needed to treat the dependencies and generate the C code with a possible execution schedule. The topological sorting algorithm chosen is named depth-first search. The depth-first search algorithm scans the graph in depth in an initially arbitrary order. It then treats each node of the graph, followed by its successors. The algorithm ends when it encounters any node that has been visited previously since the beginning of the sorting process, or when the current node does not have outgoing edges.

## Chapter 6

## Certifiable optimization of the 2D Convolutional layer

In Chapter 5, we demonstrated that, in terms of measured average execution time, the implementation of inference models generated by ACETONE was very competitive with the solutions provided by state-ofthe-art frameworks. In particular, the ACETONE V2 back-end was able to outperform the other studied tools in several use cases. However, concerning the convolutional models treated, i.e. models that contain at least one 2D Convolutional layer, it was not invariably true. We have previously discussed semanticspreserving transformations, aiming to improve resources usage, at model level. Thus, we now focus on optimizations at layer level.

This chapter presents our third contribution towards a certifiable and efficient implementation of the inference model: optimizations on the 2D Convolutional layer implementation. The content of this chapter constitutes an extension of the paper published at the Special Issue on Predictable Machine Learning of the Real-Time Systems Journal [51] and the one published in the proceedings of the 30th IEEE Embedded Technology and Applications Symposium (RTAS 2024) [49]. Section 6.1 highlights the motivation behind focusing on this particular layer. Section 6.2 presents the state of the art in 2D Convolutional layer optimizations and discusses their applicability to our context. The remaining sections focus on general matrix-matrix multiplication (GEMM) routines, which are at the core of the GEMM-based convolution algorithm. Firstly, Section 6.3 outlines a vanilla GEMM implementation as well as its integration into ACETONE. Afterwards, Section 6.4 introduces an architecture-aware GEMM implementation, that is available in the form of a library. Lastly, Section 6.5 provides an analysis of the time-predictability of the architecture-aware GEMM routine.

### 6.1. Motivation

2D Convolutional layers typically dominate the computational workload within the scope of feed-forward deep neural networks we consider. It is a result of the large number of floating-point operations (FLOPs) involved in the convolution operation, making this layer computationally intensive. Other types of layers present in the studied inference models, such as Dense (or fully-connected) layers, also involve tensor multiplications and may occasionally have a greater number of trainable parameters; however, they still exhibit reduced computational intensity relative to 2D Convolutional layers.

## Example 16 (Comparison of the number of floating-point operations in 2D Convolutional and Dense layers). The number of floating-point operations performed within a 2D Convolutional layer is computed as follows:

2 ¨fh ¨fw ¨nc ¨oh ¨ow ¨oc (6.

f h " 5; f w " 5; n c " 1; o h " 24; o w " 24; o c " 3

Replacing the above values in Equation 6.1 leads to a total of 172, 800 FLOPs within this 2D Convolutional layer.

The chosen Dense layer is the fifth layer of the model and it contains 30, 720 trainable weights. The input tensor has length n i " 256 and the output tensor has length n o " 256, resulting in 30, 720 FLOPs according to Equation 6.2.

We observe that although the 2D Convolutional layer comprises approximately 0.49% of the number of trainable weights of the Dense layer, it performs approximately 5.6 times more FLOPs than the latter. As a result, Convolutional layers are said to be computationally intensive, while Dense layers are more memory intensive.

Despite their computational intensity, 2D Convolutional layers are essential for tasks like image recognition, object detection, and image segmentation, as they are efficient for capturing spatial hierarchies and patterns in data. Consequently, optimizations on 2D Convolutional layers are crucial for deploying convolutional models in environments with constraints on computational resources and timing requirements, such as avionics systems (Objective 5). In the remainder of this work, unless otherwise stated, a Convolutional layer refers to the 2D Convolutional layer.

### 6.2. State of the art in 2D Convolutional layers optimizations

Several techniques exist with the aim of mitigating the computational intensity of Convolutional layers. We categorize the studied Convolutional layer optimization strategies into two distinct groups that will be discussed hereafter: (i) optimizations through layer's parameters compression, and (ii) optimizations at implementation level. Moreover, recall that our focus is on a single-core bare-metal implementation on COTS processors, excluding specialized hardware such as GPUs or TPUs (Hypothesis 6). Consequently, thread-level parallelization techniques are deemed beyond the scope of this study.

#### 6.2.1. Optimizations through layer's parameters compression

Techniques such as quantization, pruning, and low-rank approximation are post-training optimizations. They aim at reducing the memory bandwidth necessary to store trainable parameters and the number of computations in Convolutional layers, without significantly impacting the trained model's generalization capacity or the accuracy of its outputs.

We delineate these approaches herein due to their popularity in the context of Convolutional layers optimizations. Nonetheless, within a certification context, we ascertain that they cannot be applied to an inference model, i.e. a neural network that has already undergone training and validation. Indeed, optimizations through layer's parameters compression fail to preserve the semantics of the inference model, as will be evidenced in subsequent discussions. Hence, they are considered out of the scope of this thesis.

We highlight, however, that ACETONE's methodology readily lends itself to accommodating compressed inference models: once the semantics of compressed models is defined, generating an equivalent C code is straightforward. Then, the same evaluation process described in Section 5.3 can be performed with adapted use cases, in order to verify that the implementation preserves the inference model semantics, is predictable and efficiently leverages hardware resources.

#### 6.2.1.1. Quantization

In the machine learning domain, quantization refers to the process of reducing the precision of the inference model tensors' numerical values [77]. The objective is to transition from higher precision representations, such as single (32-bit) and double (64-bit) precision floating-point numbers, to lower precision representations, such as 8-bit integers numbers. And as a result, improve memory bandwidth and reduce computational complexity.

Quantization techniques leverage the spatial redundancy of information inherent to standard convolutional filters [56] and the consequent robustness to significant discretization of this layer's tensors. Within the Convolutional layer, quantization can be applied to the trainable parameters and to the input and output tensors. Additionally, quantizations methods can be static or dynamic. In static quantization, the number of bits for representing the tensors is chosen prior to deployment and remains constant throughout inference, i.e. values are quantized to the fixed precision representation without adjustment based on the input data. Conversely, in dynamic quantization, the precision of tensors is adjusted dynamically during inference based on the range of values encountered. Relatedly, the work of [98] introduced a technique named quantization-aware training, where the model is trained with the awareness that its parameters are to be quantized during inference. This method allows the training process to adapt to the reduced precision representations and maintain the model's accuracy even after quantization.

The support for quantized models can be easily integrated into ACETONE. In particular, both inference with integer-only quantization and inference with simulated quantization can be added [77]. In the first case, minimal changes would be required in the ACETONE framework to support performing all the operations in low-precision arithmetic. In the latter case, additional steps would be required to first "dequantize" the model parameters, then perform computations in floating-point arithmetic, and finally "requantize" the output tensors. Neither of these strategies severely alter ACETONE's workflow.

#### 6.2.1.2. Pruning

The pruning technique consists in removing from a neural network layer(s), by setting them to zero, trainable parameters that are considered redundant. This process is said to convert a dense neural network into a sparse neural network. Indeed, in order to simplify the training process, networks are typically designed with an excess of trainable parameters [164]. Thus, network pruning is used to reduce the needed memory bandwidth, the number of operations and also over-fitting. However, aggressive pruning often necessitates fine-tuning, i.e. retraining, of the remaining weights to preserve the model's original accuracy.

Initially introduced in 1989, the concept comes from a method known as optimal brain damage [121]. This approach involved calculating the influence of each weight on the training loss, commonly referred to as weight saliency. Subsequently, weights with low saliency were eliminated, and the remaining ones underwent fine-tuning. However, employing weight saliency as metric proved to be complex for large neural networks like AlexNet and VGG-16. Thus, the authors of [84] proposed a pruning solution that relied solely on the magnitudes of the weights: all weights below a threshold were set to zero and the network was retrained to learn the final weights for the remaining sparse connections. But magnitudebased pruning often requires custom hardware design to fully leverage its capabilities, as they can offer tailored solutions to store the sparse tensors in a compressed format.

Hence, other studies have explored the use of a technique named structured pruning, to avoid the need for custom hardware [16,182]. It consists in pruning groups of weights, instead of individual weights. The group of weights can refer to pairs of neighbouring weights, an entire row, column or channel of a convolutional filter, or the entire filter itself. The authors of [194] showed that the remaining tensors after structured pruning could better align with data-parallel processing, such as single-input multiple-data (SIMD) extensions. SIMD are present in many COTS processors, including the ARM Cortex-A15 used in this thesis (see Section 6.4).

#### 6.2.1.3. Low-rank approximation

Tensor decompositions provide a natural extension of the low-rank matrix decomposition to multidimensional arrays. This method decomposes the 4D tensor representing the kernels of the convolution (see Definition 26) into a combination of smaller, 1D or 2D tensors. Subsequently, low-rank approximation can be applied to represent the convolutional kernels using fewer parameters. The objective is thus to reduce memory requirements and speed up the inference pass. However, it comes at the cost of accuracy loss, which can be remedied through further fine-tuning.

The canonical polyadic decomposition (CP-decomposition) [109] is the most direct method to decompose tensors in case of many dimensions. It is solvable via diverse techniques such as a greedy algorithm [56] or a non-linear least-square method [118]. The authors of [118] showed notable 4.5ˆspeed-up on the average execution time of the second Convolutional layer of AlexNet on CPU, at the cost of approximately 1% accuracy loss, using CP-decomposition with low-rank approximation. However, the work of [54] reported an instability issue of low-rank CP decomposition when the tensor dimension surpasses two. To address this challenge, the authors of [106] employed Tucker decomposition [109] as an alternative method and managed to perform tensor approximation in all the Convolutional layers of models such as AlexNet and VGG-16, resulting in up to 3ˆspeed-up on inference time.

#### 6.2.2. Optimizations at implementation level

We now study techniques that are orthogonal to the previous presented methods reliant on parameters compression. These optimizations do not alter the semantics of the inference model beforehand. Instead, these approaches aim to mitigate computational complexity at the level of the Convolutional layer implementation. In the following sections, for each algorithm, we elucidate its main objective, explain how it works, and delineate its advantages and disadvantages.

#### 6.2.2.1. Direct convolution algorithm

Prior to presenting alternative implementation solutions, let us detail the Convolutional layer implementation adopted in the base version of ACETONE introduced in Chapter 5. The initially chosen implementation is based on the named direct convolution algorithm. It is essentially the algorithmic translation of the 2D convolution operation, previously defined in Equation 4.27, and reiterated herein:

O i 1 ,i 2 ,i 3 " f h ÿ m"1 fw ÿ n"1 fc ÿ l"1 pK i 3 q m,n,l ¨Is h ¨pi 1 ´1q`m,sw¨pi 2 ´1q`n,l(6.3)

wherein I and O represent respectively the input and output tensors, and K corresponds to the convolutional kernels tensor. Algorithm 1 illustrates the pseudo-code corresponding to the implementation of Equation 4.27, used in the base version of ACETONE. We note that the direct convolution algorithm consists simply in sixnested loops around a multiply-accumulate operation. This nested-loop approach is straightforward to understand and to implement. However, it has a poor memory access pattern due to the need of fetching from memory the same "window" of the input tensor, each time a new convolutional kernel is applied.

#### 6.2.2.2. FFT-based convolution algorithm

The Fast Fourier Transform (FFT)-based convolution algorithm consists in performing the convolution operation in the frequency domain. The objective of the the FFT-based convolution is to reduce the number of floating-point operations that are performed during convolution computation. This approach is based on the Convolution Theorem establishing that circular convolutions in the time domain are equivalent to point-wise products in the Fourier domain. The basic outline of the FFT-based convolution comprises: (i) applying FFT to both the convolutional kernels tensor and the input tensor, (ii) performing the element-wise multiplication between the two transformed tensors and, (iii) applying inverse FFT to the resulting tensor of the multiplication.

The FFT-based convolution was investigated in [132,176] both for training and inference of convolutional models. The results showed that this method was able to outperform state-of-the-art implementations of the direct convolution algorithm in terms of average execution time. The algorithm was also implemented by [36] in the industrial framework cuDNN. Likewise, the authors of [125] used this approach for improving inference time in embedded systems and demonstrated that they could improve run time without significantly affecting the model's accuracy.

However, the Convolution Theorem is applicable when convolutional kernels and input tensors are of equal dimensions. Thus, considering that the input tensor is typically larger than the convolutional kernels, it becomes necessary to expand the latter to match the size of the input tensor by applying padding. This technique then may incur a non-trivial increase in memory bandwidth, specially as most recent neural networks models use very small kernels such as 3 ˆ3 and 1 ˆ1 (see , SqueezeNet [4.6.6]). Moreover, FFT-based convolution inherently performs circular convolution, which assumes that the input signals are periodic. When dealing with 3D tensors, like images, this means that features near the 2D boundaries of the tensor can affect features on the opposite side, leading to anomalies known as boundary effects. To mitigate boundary effects, padding is often applied to the input tensor before performing the FFT-based convolution.

In conclusion, the authors of [145] and [195] showed that the FFT-based convolution becomes more advantageous than alternative implementations from a certain convolutional kernels size. The input tensor is also required to be sufficiently large, in order to amortize the cost of performing the FFT operation. Furthermore, additional memory is required to store the intermediate tensors in the Fourier domain. Finally, this method does not completely preserves the inference model semantics as it reduces its accuracy [180]. Therefore, FFT-based convolution was not the implementation adopted in our work.

#### 6.2.2.3. Winograd-based convolution algorithm

The work of [117] introduced a Winograd-based approach for performing fast convolutions. The Winogradbased convolution is based on the Winograd's minimal filtering algorithm [186], who demonstrated that a convolution between an input of length n and a kernel of length f can be computed with a theoretical minimum of only n `f ´1 general multiplications. Thus, the objective also is to reduce the number of floating-point operations that are performed during convolution computation. Like the FFT-based method, Winograd-based convolutions use a sequence of three linear transformations. The first two transformations adapt the convolutional kernels an the input tensor to the Winograd domain where convolution can be executed using element-wise multiplication, and the third transformation brings the result back to the input domain.

In [117] the authors illustrated the capacity of Winograd-based convolution to execute less floatingpoint operations than the FFT-based method, which was particularly evident with smaller convolutional kernels such as 3 ˆ3, and showed that it can be around twice as fast as direct convolution. For instance, we showed that most of convolutional models use small convolutional kernels. Moreover, we explained that each window of the input tensor is multiplied with multiple convolutional kernels, and each convolutional kernel is applied to numerous windows of the input tensor (see Example 13), which allows for the amortization of transformations costs across multiple applications. The Winograd-based convolution is also amenable to parallelization. Indeed, the authors of [61] proposed a high-performance realisation of this algorithm using vector intrinsics and OpenMP.

However, the linear transformations involved in the Winograd-based convolution can pose challenges for floating-point accuracy [22]. Typically, larger transform sizes lead to a reduction in the number of necessary operations. But the numerical imprecision of Winograd convolutions rises exponentially with increasing transform sizes [197]. Thus, achieving a satisfactory level of numerical accuracy necessitates breaking convolutions with large inputs into a series of smaller ones, in which case, each smaller segment incurs an overhead of additional general multiplications.

In summary, the Winograd-based convolution presents notable computational benefits for specific configurations of Convolutional layers. However, it exhibits limitations such as the preprocessing overhead for the transformations required, the increased memory usage to store the transformations' intermediate results and the numerical instability introduced, which does not guarantee the model's semantics preservation. Hence, this algorithm was not the privileged approach in our work.

#### 6.2.2.4. GEMM-based convolution algorithm

The GEMM-based convolution algorithm was first introduced by [33] and consists in translating the convolution operation as a compute-intensive and cache friendly general matrix-matrix (GEMM) multiplication. The primary objective of casting the convolution operators into the matrices is to arrange the tensors' elements in memory in the order they will be required for computation. Such an interpretation of the convolution algorithm allows relying on the principles of Basic Linear Algebra Subprograms (BLAS) [62] libraries, which are modules containing low-level routines to perform common linear algebra operations. BLAS libraries benefit from years of research in linear algebra computation [79], providing highly optimized routines for different algorithms such as dot products, vector norms, matrix-vector and matrix-matrix multiplications.

The idea is thus to compute the convolution algorithm as a matrix-matrix multiplication of the form C Ð A ¨B, wherein matrix A is of shape m ˆk, matrix B is of shape k ˆn and the resulting matrix C is of shape m ˆn. All the matrices are real-valued. Matrix C is then obtained by multiplying element-wise the entries of the rows of A and the columns of B. Hence, the original inputs of the Convolutional layer need to be adapted.

First, the input tensor is transformed into an augmented Toeplitz-like matrix [81]. This matrix is constructed by conveniently storing in columns the set of elements, also named patches, of the input tensor that will be multiplied by each convolutional kernel, at the each iteration of the convolution operation. The patch-building algorithm is named im2col in [33], as in image to columns, because in most of the 2D Convolutional layers applications the input tensor is an image (a 3D tensor). The resulting tensor of patches is stored in matrix B.

The im2col algorithm is illustrated in Figure 6.1. In this illustration we have a convolution operation with a stride of one (s h " s w " 1). Each column (patch) of B contains f h ¨fw elements from each channel of the input tensor, totalizing f h ¨fw ¨fc entries. The height and width dimensions of the output tensor (see Equation 4.24) determine the number of columns in the patch matrix, i.e. o h ¨ow . Matrix B is then of shape f h ¨fw ¨fc ˆoh ¨ow .

Second, the convolutional kernels tensor is virtually represented as a 2D tensor (a matrix), with dimensions n k ˆfh ¨fw ¨fc . This matrix containing the convolutional kernels is stored in A. We note that no copying or rearranging is needed in this case, hence the term "virtually" . In Figure 6.1 we observe that each line of matrix A, illustrated with a different color, corresponds to a different convolutional kernel. The different nuances of a same color represent the multiple channels of the original convolutional kernels tensor. Finally, the output tensor, stored in matrix C, does not need to be modified. In this case, each line of C represents a different channel dimension. Remember that o c " n k and f c " h c . We thus find the correspondence with Equation 6.1

Property 5. The GEMM-based convolution preserves the semantics of the direct convolution algorithm.

Indeed, the GEMM-based algorithm performs the exact same arithmetic operations as in the direct convolution algorithm presented in Algorithm 1. The only distinction is that the Convolutional layer input tensors are organized differently in memory.

The authors of [33] showed that using GEMM-based convolution in models for image recognition attained inference time improvement of up to 3ˆon the CPU and 4.11ˆon the GPU. In the work of [36], the authors relied on the im2col principles, but instead divided the matrix of patches in smaller matrices created gradually. They ensured that the smaller matrices could match the matrix sizes required by the underlying GEMM implementation and showed a speed-up in inference time of up to 30% compared to the original im2col algorithm.

Nevertheless, an important drawback of GEMM-based convolution is the required pre-processing, i.e. the patch-building algorithm. Indeed, reshaping and duplicating elements of the input tensor before each Convolutional layer is a costly job that incurs a non-trivial time penalty during inference. Besides that, lowering the 3D input tensor into a matrix of patches requires extra memory compared to the direct convolution algorithm. Indeed, each element of the input tensor is replicated up to f h ¨fw times, which requires in total up to Opf h ¨fw ¨fc ¨nh ¨nw q additional memory. Considering this, the authors of [37] and [12,13] proposed a design space of patch-building algorithms to translate convolution to GEMM, focusing on the memory consumption problem. We elaborate more on these topics in the Section 6.3.

In conclusion, the GEMM-based convolution algorithm emerges as a compelling choice for implementing Convolutional layers in our context. Its simplicity makes it easy to understand and implement. Moreover, previous studies have showed its potential to significantly enhance the average execution time of Convolutional layers, aligning with our goal of optimizing efficiency in convolutional models. Furthermore, it adheres to the certification objective of guaranteeing the preservation of the inference model semantics. Finally, this approach can leverage the robust foundation of matrix multiplication state of the art.

Numerous BLAS implementations of matrix-matrix multiplication (GEMM) routines are available in the literature. Examples of CPU-based open-source libraries include OpenBLAS [188], ATLAS [102] and BLIS [175]. Other solutions are proprietary, such as Intel oneAPI Math Kernel Library (oneMKL) [95] and Arm Performance Libraries [96]. These libraries essentially make use of matrix blocking techniques and most of them propose hardware-specific implementations, in order to optimize computations as much as possible.

However, BLAS libraries were not developed in a manner aware of the requirements of certification, hindering in particular the WCET analysis task. Indeed, they notably employ dynamic memory allocation and rely on many compiler optimizations. Hence, it poses a challenge to use them without modifications in an avionics context. To overcome this limitation while still using principles presented in BLAS libraries, we proceeded to develop our own GEMM routines to perform a GEMM-based convolution algorithm.

Initially, we developed a vanilla GEMM implementation, that is at present fully integrated into the code generation workflow of ACETONE. Subsequently, in an effort to align with established BLAS libraries, we proposed an architecture-aware GEMM implementation, which is now available in the form of a library. This solution offers versatility, as it can be employed either as a standalone library or seamlessly integrated into the ACETONE toolchain. The following sections provide detailed explanations of these two implementations.

### 6.3. Implementation of a vanilla GEMM routine

Our first implementation consists of the straightforward floating-point deployment of the matrix-matrix multiplication algorithm. Indeed, we refer to a vanilla implementation as this version does not make use of any hardware-specific tuning techniques to improve memory transfers or computation rate.

The GEMM routine as defined in the BLAS packages is of the form C Ð αA ¨B `βC, wherein matrix A is of shape m ˆk, matrix B is of shape k ˆn and the resulting matrix C is of shape m ˆn. The α and β terms are constant scalars. Without loss of generality, we consider in this section the special case of the matrix-matrix multiplication where α " 1 and β " 0.

In accordance with Definition 12 concerning 2D tensors, the individual entries of the preceding matrices can be exposed as:

A " ¨A1,1 A 1,2 ¨¨¨A 1,k A 2,1 A 2,2 ¨¨¨A 2,k . . . . . . . . . . . . A m,1 A m,2 ¨¨¨A m,k ‹ ‹ ‹ ‚ , B " ¨B1,1 B 1,2 ¨¨¨B 1,n B 2,1 B 2,2 ¨¨¨B 2,n . . . . . . . . . . . . B k,1 B k,2 ¨¨¨B k,n ‹ ‹ ‹ ‚ , and C " ¨C1,1 C 1,2 ¨¨¨C 1,n C 2,1 C 2,2 ¨¨¨C 2,n . . . . . . . . . . . . C m,1 C m,2 ¨¨¨C m,n ‹ ‹ ‹ ‚

The computation C Ð A ¨B, which evaluates the product A ¨B, is defined as:

C i,j " k ÿ p"1 A i,p ¨Bp,j(6.6)

wherein C i,j represents the dot product obtained by multiplying the i th row of matrix A with the j th column of matrix B. Algorithm 2 illustrates the pseudo-code corresponding to the direct translation of Equation 6.6.

## Algorithm 2: Vanilla GEMM algorithm

Parameters: m, n, k

Input: Matrix A, Matrix B Output: Matrix C for i " 1 to m step 1 do for j " 1 to n step 1 do Ci,j " 0 for p " 1 to k step 1 do Ci,j `" Ai,p ¨Bp,j

As long as the different scalar products of Equation 6.6 are performed exactly once, different orders in which the elements of C are updated result in a mathematically equivalent output. In consequence, the three loops of Algorithm 2 can be reorganized in any order while still producing the correct result. In reality, due to computation being conducted in floating-point arithmetic, round-off errors may accumulate with slight variations depending on the loop order. Nevertheless, such differences are not considered within the scope of our study.

3,1 2,1 1,1 3,2 2,2 1,2 3,3 2,3 1,3 n m 1,1 2,1 3,1 1,2 2,2 3,2 1,3 2,3 3,3

(a) Row-major data layout.

#### 6.3.1. Variants for the vanilla GEMM routine

As specified in BLAS, the GEMM routine allows any, or all, of the three matrices to be transposed. From an implementation perspective, the transposition of a matrix can be regarded as a transition between different data layout conventions. Similarly to 3D tensors, matrices (2D tensors) can be flattened using distinct conventions for their storage within a linear memory address space (see Section 5.2.5). In the case of matrices, the literature emphasizes the row-major and column-major data formats.

## Definition 30 (Row-major data layout). The row-major data layout means that elements within a row of the matrix are stored sequentially in memory. The memory stride between consecutive rows in this data format is equal to the number of columns of the matrix.

Definition 31 (Column-major data layout). The column-major data layout means that elements within a column of the matrix are stored sequentially in memory. In this data format, the memory stride between consecutive columns is equivalent to the number of rows of the matrix.

Example 18 (Row-major and column-major data layouts). Let us consider matrix C P R mˆn , wherein m represents its number of rows and n denotes its number of columns. Figure 6.2 depicts the flattened version of matrix C in the row-major and column-major data formats. In Figure 6.2a, each row of C is represented by a different color. We note that the elements within a row succeed one another and the memory stride between consecutive rows in this case is equal to n. Conversely, in Figure 6.2b, each column of C is depicted in a distinct color. In the column-major data layout, we observe that the elements within a column are sequentially arranged and the memory stride between consecutive columns is equivalent to m. Therefore, we opted to employ a similar approach to BLAS, by working with both transposed and non-transposed matrices, to investigate the different memory access patterns. In our work we follow the same convention as the C programming language, wherein the default memory layout is row-major [161]. Thus, when a matrix is described as non-transposed, it indicates that it is stored in row-major format. We developed the following four variants of the vanilla GEMM routine, wherein C is always non-transposed:

(i) GEMM_NN: matrices A and B are both non-transposed (A ¨B);

(ii) GEMM_NT: matrix A is non-transposed and matrix B is transposed (A ¨B⊺ ); (iii) GEMM_TN: matrix A is transposed and matrix B is non-transposed (A ⊺ ¨B);

I=28ˆ28ˆ1 K=5ˆ5ˆ1ˆ6 I=12ˆ12ˆ6 K=5ˆ5ˆ6ˆ16 I=27ˆ27ˆ64 K=2ˆ2ˆ64ˆ192 I=224ˆ224ˆ3 K=3ˆ3ˆ3ˆ64 10 6

#### 6.3.2. Average execution time assessment of the vanilla GEMM routine

Afterwards we tested the four GEMM routines variants with a certain number of convolution configurations. The objective was to analyse how GEMM-based convolutions, employing the different GEMM routines, compare to each other and to the initial direct convolution algorithm. We thus selected the first and second Convolutional layers of LeNet-5, the second of AlexNet and the first of VGG-16 models. Figure 6.3 shows the measured average execution times on an ARM Cortex-A15 core, expressed in number of processor cycles. Note that the results for GEMM-based algorithms take into account the patch-building algorithm. As explained, for matrix B we execute either the im2col or the im2row routines. Matrix A corresponds to the convolutional kernels, which are known before run time. Thus, regardless of whether the matrix is transposed or not, we consider it is prepared beforehand. From Figure 6.3 we can observe that the GEMM-based convolutions, which exploit a better memory access pattern, always outperform the direct algorithm.

However, convolution parameters, e.g. size of input tensor, number of convolutional kernels or filtering stride, which influence the structure of the matrices, impact the performance of the different GEMM-based algorithms. Inspecting Figure 6.3 we conclude that no routine consistently achieves the best results across all the Convolutional layers tested. We observe nevertheless that the GEMM_NN and GEMM_NT routines are always among the best. Thus, in order to obtain clearer insights, we chose to explore these variants in the remainder of the section.

#### 6.3.3. Optimization on the construction of the matrix of patches

In this section, we do not focus on enhancing the vanilla GEMM routine itself; rather, our attention is directed to improving the GEMM-based convolution algorithm that employs the previously presented vanilla GEMM routine.

Indeed, having to create an augmented matrix from the input tensor before each Convolutional layer represents a resource-intensive task that imposes a significant time overhead during inference. To address this, we developed a variant of the GEMM-based convolution algorithm that performs the patch-building algorithm offline. This strategy shares the same principle as the idea presented in [63].

Certainly, we do not have the precise values for the elements comprising the matrix of patches, because they are the input of the layer and are only discovered at run time. However, we do know where to find them within the input tensor. That is, we know the addresses of the variables constituting the matrix of Figure 6.4: Indirect GEMM-based convolution. A matrix of pointers only containing the addresses of input elements is created before run time and is used instead of the matrix of patches. patches relative to the input tensor array, whatever the actual input is. So, we can prepare the skeleton of the matrix of patches beforehand in, for example, the ACETONE code generator.

In practice, we say that the code generated for the GEMM-based convolution algorithm contains a matrix of pointers to the elements of the input tensor composing the patches. In opposition to explicitly creating the augmented matrix of patches with the actual floating-point values. Figure 6.4 illustrates how the matrix of pointers works. We name this algorithm indirect GEMM-based convolution, in opposition to the standard GEMM-based convolution discussed before.

In Figure 6.5 we examine how two algorithms using the indirect GEMM-based convolution version, namely indirect GEMM_NN and indirect GEMM_NT, compare to their equivalent in the standard version and to the direct convolution algorithm, in terms of average execution time. We observe a reduction in the number of cycles measured, whose intensity depends on the convolution configuration. We explain this by the fact that the patch-building algorithm is done before run time.

#### 6.3.4. Integration of the vanilla GEMM routine into ACETONE

We integrated the templates for the the vanilla GEMM routines into ACETONE, enabling the execution of GEMM-based convolutions. Figure 6.6 presents how the different encodings of the convolution operation are managed in the software architecture. In practice, we added new Layer classes that inherit from the Conv2D class and implement their own method. The Conv2D class is now an abstract class. Conv2D_direct corresponds to the original coding implemented in ACETONE (Algorithm 1), while Conv2D_std_gemm and Conv2D_indirect_gemm are the extensions proposed in this chapter. Inside the GEMM-based classes we also find different templates for the variations GEMM_NN, GEMM_NT, GEMM_TN and GEMM_TT. Thus, at model initialization for code generation within ACETONE, the user must choose the algorithm to be used in the Convolutional layer. In order to test the practical advantages and limitations of GEMM-based convolutions, we applied the same evaluation methodology described in Section 5.3, i.e. (i) we selected feed-forward neural networks from the state of the art; (ii) we assessed the semantics preservation, the worst-case execution time, the average execution time and the memory layout of executables; (iii) we compared our results with Keras2c and microTVM.

Since we are mostly interested in evaluating the effect of the new proposed routines on the measured average execution time of Convolutional layers, we will only test convolutional models. Furthermore, remember that the code generation strategy adopted in the V2 back-end was slightly superior to the other ACETONE versions in the evaluated criteria. Thus, in the following sections, when discussing the code generated by ACETONE we refer to the code generated by the V2 back-end, i.e. featuring an inlined and tailored inference function (see Section 5.2.3.2).

Finally, we note that the current available version of Keras2c implements the convolution operation using the direct algorithm, without any implementation optimization such as GEMM-based convolutions. Likewise, the kernel sources generated by microTVM for bare-metal targets do not use BLAS libraries automatically, but some other optimizations are done mainly at graph-level, such as data layout optimizations, operators fusion and constant folding. When calling TVM with external (BLAS) libraries, Static microTVM is unable to generate an entirely static code, particularly in the functions of Convolutional layers.

#### 6.3.4.1. Semantics preservation assessment

To assess the semantics preservation we rely on Criterion 1. The GEMM-based convolutions presented in this chapter do not modify the semantics of the direct convolution algorithm, as stated in Property 5. Thus, the results for the semantics preservation evaluation presented in Section 5.3.1 are still valid. Table 6.1 summarizes the bounds of errors in semantics preservation, both for single and double-precision floating-point arithmetic, observed in the codes generated by ACETONE, Keras2c and Static microTVM. We note that only one significant digit is lost in both single and double precisions, given the numerical floating-point precision stated in the IEEE-754 standard [92].

## Maximum error

## Output tensor range

FP32 (all) FP64 (ACETONE only) s ´1, 1r » 10 ´6 » 10 ´15

Table 6.1: Results for the semantics preservation both in FP32 and FP64 precision.

#### 6.3.4.2. Worst-case execution time assessment

To estimate the WCET we continue to employ OTAWA, according to Criterion 2. In Table 6.2 we present the WCET estimation for the codes generated by ACETONE employing the direct convolution and the GEMM-based convolution algorithms, both in the standard and the indirect forms. We also present the bounds produced for Keras2c and Static microTVM, from Section 5.3.2, for comparison. Examining Table 6.2, we note that the design decisions implemented within the C code notably influence the WCET bounds calculated by OTAWA. Once more, it is closely associated with the ability to provide accurate flow-facts data to the analyser.

The GEMM-based convolutions presented in this chapter aimed to improve the measured average execution times of ACETONE generated programs in priority, essentially by making a better use of the cache. We can however note in Table 6.2 that the WCET bounds produced by OTAWA were also reduced with GEMM-based convolutions, compared to the version using the direct convolution algorithm. This behaviour is consistent as the average execution times indeed decreased (see Section 6.3.4.3) and leads us to believe that OTAWA was able to recognize in its analysis the improved cache usage. We note that now ACETONE, using the indirect GEMM_NT algorithm, obtains the tighter bounds in most of use cases, with exception to the TimeSeries inference model.

## WCET [cycles]

#### 6.3.4.3. Measured execution time assessment

To measure the execution times we utilized an ARM Cortex-A15 core of the Texas Instruments Keystone II SoC, as defined in Criterion 3. In this section we added extra statistics, in addition to the average execution time, in order to refine our evaluation. Again, for all experiments, caches were activated. Data (data and BSS) and code (text) sections were placed in the DDR. For compilation, we relied on the GCC compiler and C codes were compiled without any optimization level (-O0 flag). Table 6.3 shows the results for the average, minimum, maximum and standard deviation values for the measured execution times obtained for each framework for the different inference models.

## Measured execution time [cycles]

Framework We can observe a great improvement in the measured average execution time when employing GEMMbased convolution algorithms within ACETONE. Furthermore, convolution with the indirect GEMM_NT strategy is the one that performs best. Indeed, besides eliminating the patch-building overhead, it has an optimal memory access pattern, since input tensor (matrix A) and convolutional kernels tensor (matrix B) are accessed in the order they are laid out in memory. Also, the optimizations on operators performed by Static microTVM have a greater influence on smaller models, like LeNet-5 and TimeSeries but they are outperformed by GEMM-based convolution on bigger models. Finally, Keras2c has the worst measured average execution time of all benchmarks: besides using a naive convolution algorithm, we attribute that to the strategy of allocating the trainable parameters on the stack segment.

The additional statistics on the measured execution times presented in Table 5.6 confirm that there is little variation between successive tests. The small standard deviation values indicate that the measured execution times are close to the average of the 50 iterations. Indeed, since we use the same test input tensor for consecutive measurements, the exact same operations are performed every time and small differences in execution times may be related to the initial state of the target processor. As future work, it could be worth investigating why indirect GEMM_NT also presents smaller standard deviation values.

#### 6.3.4.4. Memory layout assessment

To study the memory layout of executables following Criterion 4, we compiled the generated codes to an ARM Cortex-A15 core of the Texas Instruments Keystone II SoC. For the sake of conciseness, we only present the results obtained for the LeNet-5 model as the same trend is observed in all models. Table 6.4 illustrates the differences in the memory usage strategy among the three evaluated frameworks and the distinct convolution algorithms used in ACETONE. Table 6.4: Memory layout of the executable generated for LeNet-5.

## Size of memory segments [bytes]

Framework

From Table 6.4 we note the increase of memory usage when employing GEMM-based convolutions in opposition to the direct convolution algorithm. In the case of the standard GEMM algorithm, the extra space needed for the matrix of patches is allocated in the BSS segment, since it is only initialized at run time by the patch-building algorithm. Contrarily, for the indirect GEMM variant, the buffer of pointers to the patches matrix is present in the initialized data segment (data).

Keras2c aside, we conclude that ACETONE's implementation of the direct convolution algorithm has the best memory footprint, but the poorest measured execution times and highest WCET bounds. Indeed, the different strategies for the convolution operation implemented in ACETONE allow a trade-off between optimizing for either average execution time or code size.

### 6.4. Implementation of an architecture-aware GEMM routine

In Section 6.3.3 we studied an offline patch-building algorithm to improve the GEMM-based convolution. Henceforth, we focus on optimizing the GEMM routine itself. We thus investigate an architecture-aware GEMM routine, which denotes an implementation that is tailored to the target processor architecture. To achieve this, we adhere to the principles of BLAS libraries while ensuring alignment with the software development protocols of safety-critical systems.

In Section 6.4.1 we first explain the functioning of a state-of-the-art architecture-aware GEMM algorithm. Then, in Section 6.4.2, we present the needed concepts to actually map the GEMM algorithm to the hardware architecture. In Section 6.4.3, we introduce implementations of the GEMM algorithm adapted to our context. From Sections 6.4.4 to 6.4.5, we evaluate the proposed implementations of the architecture-aware GEMM routine in terms of measured average and worst-case execution time. Finally, in Section 6.4.7, we present the current state of the art of GEMM-based routines implementations.

As explained, in BLAS libraries, the GEMM routine computes C Ð αA ¨B `βC wherein C, A and B are matrices of dimensions m ˆn, m ˆk and k ˆn respectively, and α and β are scaling factors. Without loss of generality, in this section we consider α " 1 and β " 1, which leads to C Ð A ¨B `C. The rationale behind setting β " 1 will be elucidated in subsequent discussions.

Central to understanding how matrix-matrix multiplication is actually optimized in BLAS is to comprehend the concept of blocked matrix multiplication, i.e. the multiplication of matrices that have been partitioned into submatrices. In terms of scalar elements of the matrices, the computation C Ð A ¨B `C, which adds the result of the matrix-matrix multiplication A ¨B to a matrix C, is defined as:

C i,j " k ÿ p"1 A i,p ¨Bp,j `Ci,j(6.7)

Upon partitioning the three matrices into submatrices, we have the following:

A " ¨A1,1 A 1,2 ¨¨¨A 1,K A 2,1 A 2,2 ¨¨¨A 2,K . . . . . . . . . . . . A M,1 A M,2 ¨¨¨A M,K ‹ ‹ ‹ ‚ , B " ¨B1,1 B 1,2 ¨¨¨B 1,N B 2,1 B 2,2 ¨¨¨B 2,N . . . . . . . . . . . . B K,1 B K,2 ¨¨¨B K,N ‹ ‹ ‹ ‚ , and C " ¨C1,1 C 1,2 ¨¨¨C 1,N C 2,1 C 2,2 ¨¨¨C 2,N . . . . . . . . . . . . C M,1 C M,2 ¨¨¨C M,N ‹ ‹ ‹ ‚

wherein submatrix C i,j has dimensions m i ˆnj . Likewise, submatrix A i,p is of shape m i ˆkp and submatrix B p,j has dimensions k p ˆnj . In particular, ř M i"1 m i " m, ř N j n j " n, and ř K p k p " k. Note that the partitioning into submatrices is not done arbitrarily: the blocks of matrices A and B need to be conformal. Two matrices A and B are said to be partitioned conformally for the product A ¨B when the sizes of the blocks are such that all products and sums of the submatrices involved in the matrix multiplication are defined. Stated differently, the number of columns in each block of A must equal the number of rows in the corresponding block of B.

Provided the partitioning is conformal, matrix multiplication involving submatrices follows the same principles as matrix multiplication with scalar entries, with the distinction that the order of individual multiplications with the submatrices does not necessarily commute. The computation C Ð A ¨B `C performed block-wise is thus defined as:

C i,j " K ÿ p"1 A i,p ¨Bp,j `Ci,j(6.8)

Indeed, while the overall algorithmic structure of C Ð A ¨B and C Ð A ¨B `C is similar, the implementation details differ. In the latter case, we explicitly state that any existing values in C have to be preserved. This assumption is important as in the blocked matrix multiplication algorithm the same block of C can be updated in separate steps, as it will be elucidated in next section.

Example 19 (Blocked matrix multiplication). Let us consider matrices A P R mˆk and B P R kˆn , object of a conformal partitioning, such that:

A " ¨1 0 0 0 0 0 1 0 0 0 2 ´1 4 2 1 3 1 ´1 7 5 ‹ ‹ ‚ " ˆA1,1 A 1,2 A 2,1 A 2,2 ˙, B " ¨4 ´2 5 6 7 3 ´1 0 1 6 ‹ ‹ ‹ ‹ ‚ " ˆB1,1 B 2,1

˙

The product A ¨B can thus be computed block-wise as follows:

A ¨B " ˆA1,1 A 1,2 A 2,1 A 2,2 ˙¨ˆB 1,1 B 2,1 ˙" ˆA1,1 ¨B1,1 `A1,2 ¨B2,1 A 2,1 ¨B1,1 `A2,2 ¨B2,1 ˙" ¨4 ´2 5 6 30 8 8 27 ‹ ‹ ‚

The key insight behind the idea of using submatrices lies in the behaviour of cache-based architectures, which are prevalent in current computing paradigms. These architectures excel in executing floatingpoint operations at a rapid pace, while fetching data from memory occurs at a comparatively slower rate. This constraint posed by memory bandwidth can be thus mitigated by transferring submatrices into the processor cache(s), and pipeling the floating-point operations. However, while it is possible to explicitly load data into registers, the transfer of data into caches is primarily facilitated by a careful ordering of the computations. This is because the hardware manages cache replacement, adhering to a predefined cache replacement policy.

In summary, the core optimization principle of the GEMM routine in BLAS consists in: (i) performing a blocked matrix multiplication by dividing A, B, and C into submatrices, or blocks, such that (ii) these blocks fit in the different levels of cache, in order to improve spatial and temporal locality, (iii) enforced by a strategically planned pipelining of computations.

#### 6.4.1. Background: description of the architecture-aware GEMM algorithm

An optimized GEMM algorithm is described in [79] and is the base of the implementation of many popular BLAS libraries, including OpenBLAS [188] and BLIS [175]. The algorithm is parametrized by five parameters to be tuned by the designer depending on the hardware. More precisely, three blocking parameters n c , k c , and m c are chosen according to cache memory features, and the m r and n r parameters are chosen in view of the processor registers. Given these parameters, the algorithm essentially consists of six-nested loops around an outer product that is highly optimized to update each time a small block of C residing in registers.

In this section, unless otherwise stated, we consider that matrices A, B and C have a row-major layout, i.e. we study the GEMM_NN configuration. In order to consider transposed matrices (i.e. GEMM_NT, GEMM_TN or GEMM_TT variants), it would be necessary to specify additional parameters to take into account different strides between consecutive rows and columns of the matrices.

Introduction of terminology. We first introduce the notion of panels. A panel is a submatrix wherein at least one of the dimensions is maintained with respect to the original matrix. A column panel denotes a submatrix that contains all rows but only a subset of consecutive columns from the original matrix. Conversely, a row panel is a submatrix comprising all columns but only a subset of consecutive rows from the original matrix. A block represents a rectangular submatrix within a larger matrix including only a subset of both rows and columns.

In the GEMM algorithm, to further favour cache locality, blocks of A and B are copied and rearranged in copy blocks. In this manner, their elements are contiguous in memory and can be efficiently accessed. This copy is called packing routine in the literature. Within a matrix block we have the notion of a micro-panel. Micro-panels are small row or column panels tailored for the processor registers. Finally, a micro-tile is the name given to a small submatrix also designed to fit in the processor registers. Table 6.5 summarizes the terminology introduced in this paragraph. The matrix partitioning discussed here above is depicted in Figure 6.7. We note that a block C c is computed using the whole row panel with blocks A c and the column panel with blocks B c . The dashed lines represent micro-tiles delineated in the block C c as well as micro-panels present in blocks A c and B c . Algorithm 3 presents the pseudo-code of the architecture-aware GEMM algorithm, which is detailed hereafter. The six nested-loops are enumerated from L1 (outer loop) to L6 (inner loop). We also note the existence of expressions (E1, E2 and E3) that correspond to the actual routines for the packing of B c , packing of A c and macro-kernel. Figure 6.8 depicts the functioning of Algorithm 3.

Blocking for caches. The partitioning of A, B and C into submatrices targeting cache levels is performed by the three outermost loops. Loop L1 traverses matrices C and B along the n dimension (i.e. the columns) and partitions them in column panels of shapes m ˆnc and k ˆnc respectively. The second loop L2 operates on the k dimension and divides matrix A into column panels of shape m ˆkc , as well as divides a column panel of shape k ˆnc of B into blocks B c of shape k c ˆnc . At this moment, block B c is packed into a copy block Bc . Then, loop L3 further partitions a column panel of shape m ˆkc of A into blocks A c of shape m c ˆkc . Similarly to B c , block A c is packed into a copy block Ãc . Finally, the current column panel of C is also divided into blocks C c of shape m c ˆnc . The packing routines performed within the B c and A c blocks are detailed subsequentially.

The attentive reader may observe that the partitioning of A represented in Figure 6.7, i.e. showing a row panel, is not exactly the one described in Algorithm 3. Indeed, Figure 6.7 presents the mathematical operation. Note that in the algorithm description we first iterate over m (L3), then traverse k (L2). Thus, in reality, A is first partitioned into a column panel and then into blocks. See Figure 6.8 for an illustration of the actual order of partitioning of A. The reasoning behind this particular loop ordering will become evident as we elaborate on which matrix blocks are optimized for each cache level in Section 6.4.2.

Algorithm 3: Blocked GEMM algorithm [79] Parameters:

n c , m c , k c , m r , n r Input: Matrix A of shape (m, k), Matrix B of shape (k, n) Input/Output: Matrix C of shape (m, n) (L1) for j c " 0 to n ´1 step n c do (L2) for p c " 0 to k ´1 step k c do E1 Bc " Bpp c : p c `kc ´1, j c : j c `nc ´1q; // Packing Bc (L3) for i c " 0 to m ´1 step m c do E2 Ãc " Api c : i c `mc ´1, p c : p c `kc ´1q; // Packing Ac (L4)

for j r " 0 to n c ´1 step n r do // Macro-kernel

(L5) for i r " 0 to m c ´1 step m r do (L6)

for p r " 0 to k c ´1 step 1 do // Micro-kernel E3 C c pi r : i r `mr ´1, j r : j r `nr ´1q `" Ãc pi r : i r `mr ´1, p r q¨B c pp r , j r : j r `nr ´1q; Macro-kernel. The macro-kernel (loops L4 to L6) computes the block C c of shape m c ˆnc as the result of the accumulation of the previous values of C c and the multiplication of Ãc and Bc . Note that the complete computation of one block C c requires calling the macro-kernel several times, as it results from the multiplication of all (packed) blocks A c of the green row panel of Figure 6.7 by the blocks B c composing the blue column panel. However, also observe that since we loop through m (L3) before k (L2), between two consecutive calls to the macro-kernel routine a different C c block is updated. We also switch to another Ãc block, while using the same Bc block. See Figure 6.8 for an illustration.

Within a macro-kernel, loop L4 partitions a copy block Bc into micro-panels named B r of shape k c ˆnr and loop L5 partitions a copy block Ãc into micro-panels named A r of shape m r ˆkc . A block C c is divided into micro-tiles C r of shape m r ˆnr . Figure 6.9 illustrates the functioning of the macro-kernel algorithm used to update a block C c . A micro-tile C r is computed using the panel A r of its row and the panel B r of its column. In the figure, the indices in the micro-tiles indicate the order in which they are computed. To update C rp0q , micro-panels A rp0q and B rp0q are used. Again, observe that we first iterate over m c (L5), then traverse n c (L4). Hence, the next treated micro-tile is C rp1q , using micro-panels A rp1q and again B rp0q . Micro-tile C rp9q , for example, is updated by micro-panels A rp1q and B rp2q . Note that C c , and therefore C r , are blocks taken directly from the original matrix C, for which no packing routines are performed, thus their elements are not guaranteed to be contiguous in memory. Micro-kernel. The micro-kernel (loop L6) is the last level of decomposition, as it updates a microtile C r , via a sequence of k c outer products (a vector-scalar multiplication). As stated, a micro-tile C r is updated using the entirety of a micro-panel A r (m r ˆkc ) and the entirety of a micro-panel B r (k c ˆnr ). At each iteration, the micro-kernel algorithm computes the product of one column of a micro-panel A r , i.e. a vector of shape m r ˆ1, and one row of a micro-panel B r , i.e. a vector of shape 1 ˆnr . The lengths of these column and row vectors (m r and n r ) are chosen to take advantage of the vector registers of the architecture, as will be further detailed. Figure 6.10 illustrates the operation that is performed inside the micro-kernel, with an example where m r " n r " 4. We note that each column of C r is computed as the result of the product between one column of A r and one element of the row of B r .

Packing routines of A and B. The motivation for packing (copying and rearranging) A c and B c to create copy blocks Ãc and Bc is to favour cache spatial and temporal locality and thus improve access rate. First, to favour spatial locality, the elements are organized in the order they are needed. Concretely, micro-panels A r of A c are copied and stored in Ãc in column-major order, with a stride between consecutive columns of m r . As a reminder, a column-major layout means that elements within a column are stored sequentially in memory and each column is read one after the other. Similarly, each micro-panel B r of Bc is arranged in row-major order, with a stride between consecutive rows of n r . Likewise, a row-major layout means that elements within a row of B r are stored sequentially. We also note that within a copy block each micro-panel is stored after another.

The packing routines are also said to favour temporal locality because they provoke data from A c and B c to be preloaded into certain levels of the memory hierarchy, right before calling the micro-kernel. For example, A c is packed in L3, after B c has been packed in L2, thus its elements are expected to reside in a higher level in the memory hierarchy, i.e. closer to registers, in comparison with elements of B c . Figure 6.10 shows the memory layout of copy blocks and the benefit of such disposition for the microkernel. The arrows within the micro-panels represent the order in which the elements are laid out in memory and accessed in the micro-kernel routine.

#### 6.4.2. Background: mapping of the GEMM algorithm to the hardware architecture

As previously explained, in this thesis we conducted execution time experiments on the COTS Texas Instruments Keystone II SoC [168]. This SoC integrates an ARM Cortex-A15 processor quad-core cluster, implementing the ARMv7-A architecture.

The studied ARM Cortex-A15 has a two-level cache hierarchy. In the Keystone II SoC, each core has a private Level 1 data cache (L1D), and a Level 1 instruction cache (L1I) of size 32KB (size L1 ) each. Both L1 caches have an associativity degree (w L1 ) of 2, a cache line size (c L1 ) of 64B, a number of sets (s L1 ) of 256, and implement a Least Recently Used (LRU) cache replacement policy. The Level 2 cache (L2) of 4MB (size L2 ) is shared among the four cores. It has a 16-way set-associative cache structure (w L2 ), with a fixed cache line size of 64B (c L2 ), 4, 096 cache sets (s L2 ), and a random replacement policy.

Ãc k c m c A r m r n c B r n r k c 1 1 C r Bc

#### 6.4.2.1. SIMD instructions

The ARM Cortex-A15 core is also equipped with vector extensions. As briefly mentioned in Chapter 2, vector extensions are functional units designed to execute SIMD (single-instruction multiple-data) instructions, enabling parallel processing of distinct data elements organized into vectors. Vector instructions exhibit a structure akin to scalar instructions, comprising a mnemonic, source register(s), and a destination register. The difference resides in the capability of vector registers to store multiple values of varying sizes and types. Thus unlike scalar instructions that operate on one element at a time, vector instructions exploit data-level parallelism. Figure 6.11 depicts an SIMD operation. In the remainder of this work, we consider the NEON instructions [19], which is the SIMD extension to the ARMv7-A instruction set, implemented in our target. The NEON unit of the ARM Cortex-A15 core has 32 registers of 64-bit each, named D0-D31, wherein D stands for double-word. These registers can also be seen as 16 registers of 128-bit each, called Q0-Q15, in which Q denotes quad-word. Each of the quad-word registers then maps to a pair of double-word registers.

Using the notation of [129], we note N VEC as the number of elements (floating-point numbers) of size s data that a vector register can hold, which is a dimensionless quantity. Additionally, each vector instruction has a throughput of N INST , expressed in cycles ´1, and a latency of L INST , expressed in cycles. In practice, the blocking parameters n c , k c , m c , m r and n r of the architecture-aware GEMM routine are adjusted by the designer taking into account the latency of the vector units, the number and size of vector registers, as well as the size and associativity degree of the cache levels. With an analysis of the data usage pattern of the routine described in Algorithm 3, one can identify which submatrices are reused at each loop level as well as their reuse factor. This reasoning allows then defining which data should be kept in each cache level at the different stages of the algorithm, to enable fast access and reduce cache conflicts. In summary, the objective is that a micro-panel B r , of shape k c ˆnr , resides in the L1 cache, so it can be rapidly accessed by

#### 6.4.2.2. Choice of blocking parameters

Q mc mr

U

successive calls to the micro-kernel, as it is reused (see Figure 6.9).

Similarly, it is convenient that the copy block Ãc , of shape m c ˆkc , stays in the L2 cache, since its micro-panels are needed for the entirety of the macro-kernel function. Finally, the copy block Bc , of shape k c ˆnc , is suitable to reside in the L3 cache, if one is present in the architecture. The complete argumentation is detailed in the work of [129].

In cutting-edge BLAS implementations like OpenBLAS and BLIS, the blocking parameters are usually manually tuned by experts for each supported target. One can also perform empirical searches to find the best matrix block shapes for a given hardware and matrices configurations, as was done in [29]. Although pertinent, this method is very time-consuming. Alternatively, the authors of [129] developed an analytical approach based on the modeling of the target architecture to tune the parameters of the GEMM kernels with a focus on single-threaded implementation. Finally, some works investigate the use of an auto-tuning framework to search for the optimal parameters, such as [183], [35] and [196]. In the work of [172] the authors enhance the auto-tuning approach by relying on a structured search space that embeds expert knowledge about the target and imposes divisibility constraints on tile sizes and unroll factors to exclude non-feasible cases. This strategy should be studied in future work. We believe that their study can be complemented by ours with the addition of predictability constraints in the selection of blocking parameters, as will be further discussed in Section 6.5.

In this thesis, in order to choose the blocking parameters leading to a high-performance GEMM implementation, we decided to rely on the analytical reasoning extensively discussed in the work of [129]. They propose formulae to determine the blocking parameters according to the target architecture characteristics. Recall that performance in this context is quantified in terms of average execution time.

Subsequently, the notation for architecture parameters presented in this section is employed:

s data , N VEC , N INST , s L1 , c L1 , w L2 , s L2 , c L2 .

First, considering a single-precision floating-point implementation, we determine s data " 4B. For our target, with s data " 4B, we find N VEC " 4. Likewise, in the ARM Cortex-A15 core, we identify N VMLA " 0.5 for the throughput of the VMLA instruction and L VMLA " 8 for its latency. Thus, the formulae of [129] provide the following blocking parameters values:

m r " R ? N VEC ¨LVMLA ¨NVMLA N VEC V ¨NVEC " 4 (6.9) n r " R N VEC ¨LVMLA ¨NVMLA m r V "4 (6.10)

k c " s L1 ¨cL1 2 ¨mr ¨sdata " 512(6.11)

m c " pw L2 ´2q ¨sL2 ¨cL2 k c ¨sdata " 1,792(6.12)

Since the ARM Cortex-A15 does not have an L3 cache, this methodology claims that the value of n c is not crucial. The only advice is to choose a number big enough to avoid redundant partitioning of matrices B and C, and that is a power of two, for cache lines alignment reasons. We thus adopted:

n c " 4,096(6.13)

#### 6.4.3. Implementation details

In this section, we discuss our methodology to attain an efficient yet predictable and traceable implementation of the GEMM algorithm presented in Section 6.4.1. For that, the blocking parameters defined in Equations 6.9 to 6.13 are employed. We note that the different parts of the GEMM algorithm, namely packing B c , packing A c , macro-kernel, and micro-kernel, are implemented as separate functions. It allows us to provide a library with modular code, enables reusability, and facilitates the study of the software behaviour.

#### 6.4.3.1. Optimizations in source code

We first proceeded to implement Algorithm 3 as is, without any optimizations. This initial implementation is named (1) Base implementation. However, it is pertinent to recall that we could not employ any compiler optimizations. Indeed, as explained in Section 2.4, the compiler used and also the compiler options employed can negatively impact the predictability (Objective 4) and traceability (Objective 3) requirements. Thus, to guarantee that the designed source code and the final binary have the same behaviour, one can rely on formally verified compilers [113] or depend on generic widely-used compilers, but without using any of their optimizations. As defined in Assumption 5, we relied on the GCC compiler using the -O0 flag, mainly because of its popularity and support for various architectures, including our target.

Nevertheless, when no optimizations are allowed, the compiler produces binaries with very inefficient register allocation, resulting in many redundant store and load operations to and from the stack. Such behaviour is detrimental to traceability, as an instruction in source code is mapped to various instructions in binary. But it also penalizes efficiency, as the extra memory accesses significantly increase execution time. To remedy this, we proceeded to carefully place all the intermediate variables directly in registers and, whenever possible, inline functions to limit stack usage. This approach improved the code while using at most 10 general-purpose registers simultaneously, which is less than the number of generalpurpose registers available in the ARMv7-A architecture. We named this second implementation as (2) Register-optimized implementation.

It can be asserted that the -O0 compiler configuration consistently produced binaries with suboptimal register allocation in our prior experiments, and we did not investigate it any further back then. Indeed, the significance of this compiler behaviour is accentuated within this particular routine, notably for the presence of multiple nested functions.

#### 6.4.3.2. Optimizations towards a vectorized micro-kernel

As previously mentioned, the micro-kernel of the GEMM algorithm is designed to utilize the hardware vector registers. However, it is worth noting that the (1) Base and (2) Register-optimized implementations do not leverage this technology. In this section we thus present vectorized implementations of the microkernel function using the NEON unit. Algorithm 4 exposes the pseudo-code of the micro-kernel for m r " n r " 4, in single-precision floating-point (s data = 4B). It means that every NEON Q register (128-bit) contains 4 floating-point elements.

Algorithm 4: Vectorized micro-kernel algorithm Q0, Q1, Q2, Q3 " V LOADpCrq // Load Cr into quad-registers // Update Cr for p r " 0 to k c ´1 step 1 do // Load m r (resp. n r ) elements of micro-panel A r (resp. B r ) Q4 " V LOADpA r p0, p r qq Q5 " V LOADpB r pp r , 0qq // Vector-scalar multiplications

Q0 " V M LApQ4, Q5r0s, Q0q Q1 " V M LApQ4, Q5r1s, Q1q Q2 " V M LApQ4, Q5r2s, Q2q Q3 " V M LApQ4, Q5r3s, Q3q

Cr " V ST OREpQ0, Q1, Q2, Q3q // Store quad-registers values to Cr

The NEON instructions can be accessed through special functions called NEON intrinsics. NEON intrinsic functions and data types provide access to low-level NEON functionality at C (or C++) source code level. These allow the creation of C variables that directly map to NEON registers, allowing NEON vectors to be passed as function arguments or return values. Then, in the compilation toolchain, the function calls are replaced by the appropriate NEON instruction(s). The use of intrinsics, in theory, can offer a good balance between abstraction and control, as it allows working with vector units but registers' allocation is still assigned to the compiler. We thus proceeded to code the micro-kernel using NEON intrinsics. We named this third implementation as (3) Micro-kernel vectorized with intrinsics implementation. However, although the behaviour of intrinsics functions is documented, in our setting where the use of compiler optimizations is limited, the generated binary includes many redundant instructions and a great amount of register spills. Figure 6.13 illustrates this issue. The leftmost listing presents the NEON vld1q_lane_f32 intrinsic function, used in the micro-kernel to load a scalar from memory and write the result to one lane of a SIMD register. In the middle we have the expected (documented) translation of this intrinsic function in assembly. The rightmost listing shows how it is actually translated in the assembly code when no optimization is applied (-O0 flag). For this specific function, we observe 8 extra instructions, but for other intrinsic functions such as the vectorized multiply-accumulate (VLMA), there can be up to 18 additional instructions. For the totality of a micro-kernel code, 397 extra instructions are identified in the binary when using NEON intrinsics.

## Expected

To circumvent the aforementioned issues, we proceeded to manually implement the GEMM microkernel using an inline assembly block. We named this fourth implementation as (4) Micro-kernel vectorized with assembly implementation. By manually coding the micro-kernel it is possible to completely control the selection of vector instructions and the register allocation task in this small yet performance-critical function. As depicted in Algorithm 4, the micro-kernel function can have its instructions separated into three main subroutines, which consist of: (i) loading the micro-tile C r into registers, (ii) updating the value of C r in the registers via outer products, and (iii) storing the register values into the micro-tile. These subroutines can then be coded in distinct assembly blocks in order to facilitate verification of correctness. Indeed, if a different instruction set is used, the micro-kernel routine must be adapted. However, automatizing the generation of the micro-kernel vector instructions is possible, as all the parameters required are defined in the design phase.

#### 6.4.4. Measured execution time assessment of the architecture-aware GEMM routine

Herein, we compare measured execution times obtained for the different aforementioned implementations of the architecture-aware GEMM algorithm. We evaluate the blocked GEMM algorithm on square matrices but also on irregular-shaped configurations. The irregular-shaped matrices considered here correspond to the matrix representation of the Convolutional layers studied in Section 6.3.2. Table 6.6 presents the measured execution times of the different GEMM implementations when running on an ARM Cortex-A15 core with no compiler optimizations. For each experiment, the reported measures contain the average, the minimum and the maximum observed times of 50 executions. The (1) Base implementation is the one without any optimizations, and the (2) Register-optimized contains manually forced register allocation and function inlining techniques, as discussed in Section 6.4.3.1. The last two implementations extend the (2) Register-optimized version by using the NEON unit in the microkernel: (3) Micro-kernel vectorized with intrinsics uses the intrinsics functions whereas (4) Micro-kernel vectorized with assembly is the vectorized assembly-coded version. The percentages represent the reduction in the average measured execution times of each optimized implementation with respect to the (1) Base implementation.

int micro_kernel (int kc, float *A, float *B, float *C, int ldC){ register float* _C asm ('r4') = C; register float32x4_t c_0 asm ('q0'); ... c_0 = vld1q_lane_f32(_C, c_0,

We observe a great reduction in overheads (compared to the Base implementation) after the first optimization of the source code, with average execution times reduced by 92.00% in the best case. The measured execution times are increased compared to the Register-optimized version when using NEON intrinsics to vectorize the micro-kernel, contrary to what one could initially expect. As explained, this behaviour is due to the very inefficient register allocation performed by the compiler. Finally, when the micro-kernel is also manually optimized with the introduction of assembly blocks, we obtain average execution times that are comparable to a first level of compiler optimization (-O1 flag). We remark that the amount of improvement brought by the different optimizations is not constant but highly dependent on the configuration of the matrices. In addition, we observe a minimal timing variability in our bare-metal implementation, as evidenced by the reported minimum and maximum observed execution times.

#### 6.4.5. Measured execution time assessment of different convolution algorithms

We now proceed to compare the average execution times of the different convolution algorithms discussed in this chapter, i.e. the direct convolution algorithm and the GEMM-based convolutions, both with vanilla GEMM and architecture-aware GEMM routines. In relation to the vanilla GEMM algorithm, we select the implementation of the standard GEMM_NN variant. Concerning the architecture-aware GEMM algorithm, we consider the (4) Micro-kernel vectorized with assembly implementation. Consistent with the preceding setups for measured execution time assessment, we run tests on an ARM Cortex-A15 core and codes are compiled with the -O0 flag. Similarly, we present the average of the observed execution times of 50 iterations. For the experiments, we adhere to the Convolutional layers configurations previously delineated in the preceding sections (See Figure 6.3 and Table 6.6). We thus consider the following Convolutional layers: the first and second of LeNet-5, the second of AlexNet, the first and the tenth of VGG-16 models. Table 6.7 presents the measured execution times obtained for the different convolution algorithms. The percentages represent the reduction in the average measured execution times of the GEMM-based convolution algorithms with respect to the direct convolution algorithm. Analysis of the results presented in Table 6.7 reveals a significant reduction in average execution times across all tested configurations when employing GEMM-based convolutions. We precise that for the GEMM-based convolutions we take into account the number of cycles used for the patch-building algorithm. We note from Table 6.7 that the use of a vanilla GEMM routine inherently results in a minimum reduction of 22% in execution times. However, upon the implementation an architecture-aware GEMM routine with the strategic use of vector registers, we observe even more substantial enhancements, with reductions in execution times of around 90%. In conclusion, we show that the average execution time of Convolutional layers can be improved with implementations that, in principle, guarantee traceability and predictability.

## Conv

#### 6.4.6. Worst-case execution time assessment of different convolution algorithms

Thus far in this section we have extensively discussed about different implementations of a tailored routine to enhance the average execution time of Convolutional layers. However, as the broader context of our work pertains to avionics software implementation, it is important to determine worst-case execution time bounds for this algorithm as well. Therefore, we used OTAWA to compute via static analysis the WCET bounds for the architecture-aware GEMM routine and compare them with the direct convolution and the vanilla GEMM-based algorithms. We precise, however, that we selected the (2) Register-optimized architecture-aware GEMM implementation (no vectorized micro-kernel), as vector instructions are not present in the lpc2138 ARM-based target used in OTAWA. For experiments, we used the same Convolutional layer configurations as in Table 6.7. Table 6.8 presents the WCET bounds obtained for the different convolution algorithms. The percentages represent the difference in the WCET bounds of the GEMM-based convolution algorithms, with respect to the direct convolution algorithm. Looking at Table 6.8, we observe that OTAWA produces tighter bounds for the vanilla GEMM-based algorithm, in comparison with the direct convolution algorithm. This behaviour is similar to what we have previously noted in Table 6.2 when analysing complete convolutional models. At that juncture, the conclusion drawn was that OTAWA was possibly able to recognize in its analysis the improved cache usage. Nonetheless, when examining the results for the architecture-aware GEMM-based algorithm, we note that the WCET bounds produced are worsened, both with respect to direct and vanilla GEMMbased convolution algorithms. Indeed, this behaviour is contradictory to what was observed for measured execution times. We can thus conclude that OTAWA is not able of detecting and leveraging precisely the memory access patterns that the architecture-aware GEMM routine implements. Consequently, it will be necessary for us to address this issue.

## Conv

#### 6.4.7. State of the art of GEMM-based routines implementations

With the necessary background information now at our disposal, we can present the current state of the art of GEMM-based routines implementations. Since our focus is on embedded targets with vector extensions we highlight works that studied optimized implementations of GEMM-based algorithms on ARM cores.

Vanilla GEMM routine. The authors of [147] propose an implementation of a non-blocked GEMM algorithm in ARM processors with vector extensions, targeting safety-critical real-time systems. They explicitly employ vector instructions (via NEON intrinsics), in opposition to compiler-generated vectorization, and show great gains in average execution times compared to the non-vectorized versions of the algorithm. However, they also observe that when the matrices are too big to fit in the L1 data cache, the potential of vector registers is not fully exploited. The authors claim that their approach is timepredictable, but it is not detailed in the paper how predictability is ensured. Our work can be considered an extension of theirs, as we follow their guidelines on SIMD usage in safety-critical real-time systems and go further on exploiting the hardware architecture for performance and predictability.

Architecture-aware GEMM routine. The authors of LIBXSMM [87] propose optimized implementations of the blocked GEMM algorithm for small matrices based on just-in-time compilation to only build the required micro-kernel variant at run time. This idea is very powerful but not suitable for our application domain as we must privilege a static approach. In contrast, BLASFEO [74] consists of a static library designed to optimize small and irregularly-shaped matrix multiplications. The authors adopt the OpenBLAS GEMM algorithm principles but propose modifications such as converting the layout of matrices to improve cache locality and conditional use of packing routines, as they may be too expensive in small workloads. LibShalom [192] extends the library approach of [74] to perform packing in parallel to computations and also proposes an instruction scheduling optimization targeting ARM v8 multi-core processors. However, these works only target average execution time improvement and rely notably on intensive compiler optimizations. In addition, LibShalom uses OpenMP for parallel execution. We thus consider that their ideas about conditional packing and customized matrices layouts can be adapted to our work scope as future work.

Direct convolution using architecture-aware GEMM ideas. Recent works have proposed a loop-blocking strategy to optimize the original direct convolution algorithm. As explained, a 2D direct convolution algorithm is a 6-dimensional nested loop, thus an architecture-aware loop-tiling strategy such as the one used for GEMM can be derived. The work of [195] introduces a strategy for mapping the loops to the underlying hardware architecture. The authors also propose specialized data layouts for the input and convolutional kernels tensors, so that data is accessed in a more cache-friendly way. However, the proposed data layouts are different from those typically used in neural networks (i.e. HWC and CHW formats) and this strategy requires modifying the tensors format before and after each Convolutional layer. In [23] the authors adapted the blocking strategy presented in [195] to allow for preserving the conventional HWC data layout used in convolution layers and also presented a variant capable of exploiting GEMM routines, which will be explained subsequently. A noted drawback in both works is that the proposed solutions that genuinely have zero memory overheads do not easily accommodate stride, dilation, and padding parameters. Both works target average execution time on ARM v8 cores. In future work, we aim to explore this approach for direct convolution and add a predictability perspective to their approach.

### 6.5. Study on the time-predictability of an architecture-aware GEMM routine

The GEMM algorithm described in Algorithm 3 is intrinsically predictable: there is no conditional branching and all the blocking parameters are known at compile time. However, to the best of our knowledge, no existing static WCET analysis method (not only OTAWA), is capable of detecting and leveraging precisely the memory access patterns that GEMM routines implement. Hence, we studied the blocked GEMM algorithm and provided a set of rules for choosing the blocking parameters in a manner to make it easier to analyse from a temporal perspective. We note that in the remainder of this chapter, unless otherwise stated, a GEMM algorithm refers to the architectureaware GEMM algorithm discussed in Section 6.4.

#### 6.5.1. Philosophy of the approach

We performed an analytical study of the original GEMM algorithm and proposed modifying the blocking parameters to enforce predictability. Within each part of the algorithm, we then derived the formulae that (i) determine the total number of memory accesses and (ii) define an upper bound on the number of data cache misses.

Indeed, static WCET methods require, among other things, to determine if instructions lead to a miss or a hit in the cache hierarchy. If approaches exist for the instruction cache, the analysis is harder for data caches. In the latter case, it is necessary for each memory instruction to determine which range of addresses it can access, then to determine the possible access patterns, and finally to combine these information to determine a conservative bound on the number of misses caused by the memory instruction. Each of these steps is complex and usually degrades the precision of the analysis [130]. We thus focused on delimiting memory accesses and cache misses as these values can be exploited in static WCET estimation techniques, such as IPET, to tighten the WCET bound.

More precisely, looking at Algorithm 3, we assert that memory accesses are caused only by the packing and the macro-kernel routines. Indeed, the for-loop associated variables are stored in registers and thus do not generate memory accesses. We thus focus on the core of the routines, which are represented in Algorithm 3 by expression E1, which manages the packing of B c , expression E2, which manages the packing of A c , and expression E3, which manages the tile C c . In particular, we analyse the (4) Microkernel vectorized with assembly implementation, wherein all intermediate variables are placed in registers. Hence, stack accesses are only performed at the beginning and at the end of the calls to the functions that implement these routines. We identified their exact number in the assembly code and counted them separately. Our objective was to reason about the data cache behaviour and to be able to obtain formulae that (i) for the packing routines, guarantee that the number of cache misses is the theoretical minimum and (ii) for the macro-kernel routine, only slightly overestimate the actual number of cache misses.

We summarize the notations used to reason about the time-predictability of the GEMM routine in Table 6.9. Subsequently, we start by presenting general results on matrix placement in caches and then focus on each of the aforementioned expressions: packing of B c , packing of A c and macro-kernel.

X Li = c Li s data

Number of elements per cache line of L i cache Table 6.9: Notation used on the predictability analysis of GEMM algorithm.

#### 6.5.2. Reminder on cache placement and replacement policies

Cache placement policies determine the placement of memory blocks within a CPU cache. These policies enforce constraints on where a block of memory can reside within the cache, mapping it to specific cache lines or sets of cache lines. Three primary policies exist for placing a memory block in the cache, namely: (i) direct-mapped, (ii) fully associative, and (iii) set-associative. We focus on set-associative caches, which is the most used cache organization nowadays [80]. It is also the structure of the caches of the studied ARM Cortex-A15 core. In a set-associative cache, a memory block is first mapped to an unique set within the cache, then it can placed within any cache line of that set. An n-way set-associative cache, for example, provides n available cache lines for storing a memory block.

The address received by the cache is segmented into bits for offset, index and tag. Offset bits correspond to the cache line size. The cache line size represents the amount of data, in bytes, transferred between the main memory and cache when executing a data read or write instruction. Afterwards, index bits determine the targetted cache set. Finally, tag bits correspond to remaining bits of the address, i.e. , the total number of bits constituting the physical memory address, excluding the offset and index bits. The cache uses the tag to establish whether or not the incoming main memory address is present within its storage. For the following discussions, we name cache block the memory block corresponding to a cache line size. Moreover, the start of a cache block is called a cache block boundary.

Example 20 (Placing a cache block in a 2-way set-associative cache). Figure 6.14 illustrates a 2-way set-associative cache, very similar to the L1 data cache of the ARM Cortex-A15 core used in our study. In this example, since c L1 " 64B, there are log 2 p64q " 6 offset bits. We also have that s L1 " wherein y denotes the cache set index and x denotes the main memory line index. We note that there are 2 cache lines per cache set available for a given main memory line. In the scenario where all cache lines within the set are currently occupied, the incoming data replaces the block identified according to the implemented replacement policy.

-- There exist a certain number of cache replacement policies; herein, we cite four widely used ones: (i) Random, (ii) First In First Out (FIFO), (iii) Least Recently Used (LRU), (iv) Pseudo-LRU (PLRU). In the random replacement policy the cache randomly selects a cache block to evict when a new block needs to be loaded. This policy is simple and cheap to implement; however, it is very difficult to predict its behaviour. As mentioned, the L2 cache of the ARM Cortex-A15 core has a random replacement policy.

Conversely, the FIFO policy evicts the cache block that has been present the longest in the set. This policy operates a queue and uses a replacement counter per set, identifying the cache block for imminent replacement. The counter is incremented upon insertion of an element into a set, and remains unaffected by a cache hit. In terms of predictability, [150] showed that given a queue of length k, wherein k is the associativity of the cache, one needs at most 3k ´1 accesses for any initial cache state to reach a completely known cache state.

In its turn, the LRU policy replaces the cache block that has not been accessed for the longest time. It also maintains a queue of length k. When a cache miss happens, the searched block is inserted at the beginning of the queue. Then the least recently used block, located at the end of the queue, is evicted from the cache. Also, upon a cache hit, the used block is relocated to the front of the queue. Predicting the contents of LRU caches is considered straightforward [150].

Lastly, the PLRU policy is an approximation of LRU that aims to reduce the computational overhead. Instead of tracking the exact access history of each cache block, it uses a data structure, usually a tree or a bit array, to keep track of which cache blocks are more or less likely to be the least recently used. The logic simplification employed by the PLRU policy comes at the cost of losing the guarantee of consistently replacing the least recently used element, which reduces predictability. In summary, the authors of [150] showed that, in terms of predictability, LRU outperforms both PLRU and FIFO. Proof. Let us consider the following function that associates cache block indices to their corresponding set in the cache:

#### 6.5.3. Mapping a matrix to a data cache

f : tk ¨n | k P v0, s Li ´1wu Ñ v0, s Li ´1w x Þ Ñ x mod s Li

For each cache block to be mapped to a different cache set, function f must be bijective. If we represent v0, s Li ´1w as the cyclic group Z{s Li Z equipped with the classical `operator, then f bijective is equivalent to saying that n is a generator of pZ{s Li Z, `q. Now, the generators of pZ{s Li Z, `q are the integers that are coprime with s Li . As a consequence, f is bijective iff n is coprime with s Li . Since the number of cache sets is usually implemented as a power of two, it is sufficient that n be odd to ensure the property. Finally, the property holds for any set that is isomorphic to the set tk ¨n | k P v0, s Li ´1wu, in particular if we apply a translation by a constant integer b.

Let X Li be the number of elements a cache line can store. A data cache has s Li sets, each with w Li ways. Thus, using only one way per cache set it is possible to store at most s Li ¨XLi elements. We consider a matrix M of shape u ˆv, stored in row-major order, aligned in memory to the start of a cache block, such that v is a multiple of X Li . Then the number of cache blocks occupied by a row of matrix M is N b " v X Li . We now consider a slice of M composed of X Li adjacent columns on s Li consecutive rows, also aligned in memory to a cache block boundary. We study how to store such a slice using exactly one way of each data cache set.

## Corollary 1.

If N b is an odd integer, any slice of shape s Li ˆXLi of matrix M , whose first row is aligned to the start of a cache block, has each of its s Li cache blocks mapped to a different cache set.

Proof. First, we suppose that the first row of the first slice of shape s Li ˆXLi of matrix M is mapped to the cache block of index c P N. Since v is a multiple of X Li , each row of M (and thus of the slice of shape s Li ˆXLi ) starts at the beginning of a cache block. In particular, the second row of the first slice of shape s Li ˆXLi of M is mapped to the cache block of index c `Nb . The third row is mapped to the cache block of index c `2 ¨Nb . Finally, the k-th row is mapped to block c `pk ´1q ¨Nb .

From Theorem 1 we have that if N b is an odd integer, the s Li consecutive rows of the first slice of shape s Li ˆXLi of matrix M are mapped to different cache sets. In fact, the property holds for any slice of shape s Li ˆXLi aligned in memory to the start of a cache block, and thus separated from the first slice of shape s Li ˆXLi by an integer offset multiple of X Li . We introduce a running numerical example to facilitate the discussion of the following sections on the time-predictability of the GEMM algorithm with respect to the data cache. Example 21 (Running example for time-predictability analysis). We consider square matrices A, B and C wherein m " n " k " 528. We analyse an L1D cache like the one of our target, with the following characteristics: an LRU replacement policy, associativity degree of 2, size of 32KB, a cache line size (c L1 ) of 64B, and with a number of sets (s L1 ) of 256. Moreover, we consider single-precision floating-point data, where s data is 4B. Thus, the number of elements per cache line in this example is X L1 " c L1 s data " 16.

+

#### 6.5.4. L1D cache behavior in packing Bc

As explained in Section 6.4.1, the packing algorithm reads elements from B c and writes them in a copy block Bc . Both operations are done alternately, i.e. a reading instruction is followed by a writing instruction. Thus, to optimally use the data cache, the objective is to share it between the two operations. We do not wish that writing operations evict cache blocks loaded for the reading and that still may be needed. The contrary is also true: we do not want cache blocks loaded for the writing to be replaced before all their elements are stored. Practically, to prevent this kind of conflict, we dedicate half of the cache for lines used to read from B c and half of the cache for lines to write to Bc . As our processor comes with a 2-way set associative L1D cache, for each cache set, one cache way is dedicated to B c and the other is used for Bc . Note that the idea can be generalized to any even (ą 1) or odd associativity degree cache. Figure 6.16 illustrates this philosophy. The process of writing Bc is done linearly to contiguous addresses. The corresponding cache blocks are thus allocated to cache sets with contiguous indices. Hence, to adhere to efficiently use only half of the cache for the writing, we must have k c " s L1 . In contrast, the process of reading from matrix B c is done by groups of n r contiguous elements before treating the next matrix row, which is n elements away. In total, k c matrix rows are accessed before returning to the first row of B c , which has already been charged in the cache. Thus, for the reading, we find k c ď s L1 . In order to avoid conflicts and under-utilization of the cache sets, we wish to guarantee that each cache block with elements of B c needed at a time is loaded to a different cache set. We thus choose to set k c " s L1 .

However, since the elements read from B c to form one micro-panel are not contiguous in memory, the question of the mapping between matrix rows and cache sets arises. To guarantee that these blocks are mapped to distinct cache sets, it is sufficient, according to Corollary 1, that the number of cache blocks composing a row of B be an odd integer. This can be ensured by padding each row of B by one cache block if necessary. The complete reasoning is illustrated in Figure 6. 16. For Example 21, n X L1 " 33, i.e. a row of B occupies an odd number of cache blocks. Thus, no padding is required, and k c is chosen so that k c " s L1 " 256.

#### 6.5.4.1. Number of memory accesses

A block B c of shape k c ˆnc is partitioned in R n c n r

V micro-panels. We define:

‚ n p " Z n c n r ^: number of complete micro-panels in B c (N.1)

‚ n f " n c mod n r : width of the potential incomplete last micro-panel (N.2)

The n p full micro-panels of shape k c ˆnr are read and then stored in the order they are accessed in the micro-kernel function, i.e. in the row-major order. For the incomplete micro-panel, n f elements are read and then padded with zeros during writing, to attain a width of n r and completely use the vector register's size.

To pack full micro-panels into Bc , there are 2 ¨np ¨kc ¨nr memory accesses. That is, the same number of accesses for read and for write. To pack the last incomplete micro-panel, we find 2¨n f ¨kc `pn r ´nf q¨k c memory accesses. The total number of memory accesses involved in packing B c is: 2 ¨np ¨kc ¨nr `2 ¨nf ¨kc `pn r ´nf q ¨kc (6.15)

For Example 21, we have n r " 4 and n c " 528, i.e. the minimum between n and the n c tailored for the target (see Section 6.4.2). It follows that n p " 132 and n f " 0. Matrix B is then partitioned into 3 blocks B c of shape k c ˆnc : the first two are of shape 256 ˆ528 and the third has shape 16 ˆ528. Thus, the total number of memory accesses for packing the B c blocks into Bc blocks is 557, 568.

In particular, the block could also be mapped to set #10. The reading and writing of the next three elements of the first micro-panel (Br1s...Br3s) cause no extra cache misses, as the corresponding block is already in the cache.

The next element to be read after Br3s is Br528s. It belongs to another cache block that is loaded in set #p10 `33q mod 256 " 43. Note that 33 is the offset between successive cache indices because Q n X L1 U " 33. The writing of element Br528s however is done to the cache block present in set #3. When element Br2112s, i.e. the first element of the fifth row of the first micro-panel, is written in Bc , a new cache block is loaded in set #4. The same reasoning applies until reaching the 256th matrix row. When the copies of the second micro-panel start, with element Br4s, its reading causes no extra misses, while its writing loads a new cache block in set #p3 `256{4q mod 256 " 67.

Finally, as

Q nc X L1 U "33

#### 6.5.5. L1D cache behavior in packing Ac

The process of packing A c to create the copy block Ãc is similar to the one of packing B c : reading and writing happen alternately as well. We can thus also partition the cache between the two operations.

The difference is that now, to construct the micro-panels of shape m r ˆkc , we read one element from m r consecutive rows of A c before returning to the first of these m r rows to read another element. This process is repeated k c times (see Figure 6.10). It follows that, for reading from A c , only m r cache blocks are needed at a time. As explained, m r represents a quantity to be stored in vector registers, which is significantly smaller than s L1 . Hence, to ensure that the corresponding m r cache blocks are mapped to distinct cache sets, once again following Corollary 1, it is sufficient that each row of A c be composed of an odd number of cache blocks. As with B, this can be enforced by padding each row of A with one cache block if necessary.

Finally, the m r ¨kc elements of a micro-panel are written to contiguous memory addresses in Ãc . Thus, once a cache block gets loaded, it is filled by stores before the next one is loaded, at which point the block is no longer needed.

#### 6.5.5.1. Number of memory accesses

We define m p (resp. m f ) in the same way as n p (resp. n f ) for block A c . In order to pack full micropanels present in A c , the algorithm does 2 ¨mp ¨kc ¨mr memory accesses. To pack a potential incomplete micro-panel of A c , 2¨m f ¨kc `pm r ´mf q¨k c memory accesses are performed. In total, to create a copy block Ãc , there are a number of memory accesses equivalent to: 2¨m p ¨kc ¨mr `2¨m f ¨kc `pm r ´mf q¨k c (6.19) Applying the reasoning to Example 21, we have m c " 528, m r " 4, m p " 132 and m f " 0. A is then also partitioned into three A c blocks. Thus, the total number of memory accesses during the packing of blocks A c is 557, 568.

#### 6.5.5.2. Upper bound on the number of cache misses

To reason about the packing of A c , we add the following assumptions:

‚ A and Ãc are aligned to a cache block boundary, (A.5)

‚ k X L1 is an odd integer, (A.6) ‚ k c is a multiple of X L1 , (A.7)

We also introduce the following relevant notations: To read one micro-panel of shape m r ˆkc of A c , knowing Notation N.4, we find:

‚ R k c X L1 V :

m r ¨R k c X L1 V misses (6.20)

Thus, to read the whole A c block, there are: Ar4s is the 17th element to be copied. Reading element Ar4s causes no extra cache misses as this block was already loaded (set #5), but its writing requires a new cache block, which is mapped to set #2. Copying element Ar16s, for example, requires a new cache block both for reading and for writing, mapped respectively to sets #6 and #p1 `16{4q mod 256 " 5. Hence, packing the different A c blocks into Ãc blocks results in 34, 848 L1D cache misses.

R m c m r V ¨mr ¨R k c X L1 V misses. (6

number of cache blocks used by k c elements (micro-panels A r in A c (and Ãc ) (N.6)

#### 6.5.6. L1D cache behavior in macro-kernel

In the macro-kernel function, the copy blocks Ãc and Bc are partitioned in micro-panels used to update a different micro-tile C r in each call to the micro-kernel function (see Algorithm 3). Between successive calls to the micro-kernel, a new micro-tile C r , as well as a new micro-panel A r , are brought into registers. The GEMM algorithm was designed to favour each micro-panel B r to stay in the L1D cache for Q mc mr U executions of the micro-kernel function before being replaced. However, not knowing exactly where the elements of these matrices are mapped in memory, it is not possible to guarantee that the expected behaviour occurs. See Figure 6.9, introduced in Section 6.4.1, that illustrates the macro-kernel algorithm.

## Example 22. The sequence of operations performed in the macro-kernel applied to the example of Fig

- ure 6.9 is: R-C rp0q ; pR-A rp0q ∥R-B rp0q q; W -C rp0q ; R-C rp1q ; pR-A rp1q ∥R-B rp0q q; W -C rp1q ; R-C rp2q ; pR-A rp2q ∥R-B rp0q q; W -C rp2q ; ...

Where R stands for reading and W for writing. The ∥ symbol highlights that A r and B r are read alternately, by groups of m r (respectively n r ) elements, as shown in Algorithm 4.

#### 6.5.6.1. Number of memory accesses

Hereby we outline the following clarifying notation:

‚ R m c m r V ¨R n c n r V : number of micro-tiles C r present in a block C c (N.7)

The micro-kernel routine is then executed

R m c m r V ¨R n c n r

V times, i.e. the number of existing micro-tiles.

In the micro-kernel, a micro-panel A r is accessed k c times to load m r consecutive elements into registers each time. Since in our case m r has the same size as one vector register (4 FP32 elements), with one memory access it is possible to fill the register. Thus, there are k c memory accesses to read A r in the micro-kernel.

The same is also true for a micro-panel B r , with k c memory accesses to read it in the micro-kernel. The micro-tile C r , in contrast, is accessed m r ¨nr times for reading because the elements required in the registers for C r are not contiguous in memory, as they come from multiple rows (see Figure 6.9). Hence, reads cannot be grouped. The same applies for the m r ¨nr writes. Thus, in total, given Notation N.

U

(see Notation N.5). Thus, a micro-panel A r cannot share cache sets with more than two micro-panels B r , and conversely. See Figure 6.18 (page 153) for illustration.

#### 6.5.6.2. Upper bound on the number of cache misses -general case

In the following steps, we study the cache behaviour in the macro-kernel algorithm for the expected lifetime of a micro-panel B r , i.e. for Q mc mr

U

successive calls to the micro-kernel. . We had assumed that its first element, Bc r0s is mapped to cache set #3. Element Bc r1023s is then mapped to cache set #66. Thus, for reading micro-panel B rp0q there are 64 cache misses.

## ii) B r becomes the least recently used because of A r and is evicted by C r

Let us consider the sequence of operations presented in Example 22 (page 150), from R-C rp0q to R-C rp1q . Following Properties 6 and 9, the worst case of conflicts between cache blocks of micro-panels A r and B r happens when, for example, the mapping of micro-panel A rp0q starts exactly one cache block above the micro-panel B rp0q , as depicted in Figure 6. 18. In this case, after the sequence pR-A rp0q ∥R-B rp0q q, all the cache blocks of B rp0q become the least recently used of their respective sets, except for the last one. Then, if C rp0q and C rp1q are both mapped to cache sets where B rp0q is old, the actions of W -C rp0q and R-C rp1q cause the eviction of blocks of B rp0q .

From Property 8 we know that C rp0q and C rp1q are not mapped to the same cache sets, thus each of the micro-tiles can contribute to a maximum of m r misses in B rp0q . Following Property 9 only A rp0q and A rp1q conflict with blocks of B rp0q . Thus only C rp0q and C rp1q can evict blocks of B rp0q , as they are loaded and stored in the same time frame as A rp0q and A rp1q .

According to Property 9, this scenario can happen at most once each time the Remember we assumed that Bc starts in set #3 and Ãc in set #1. Thus, when Cr528s, which belongs to a cache block that is also mapped to set #33, is written, the cache block containing Bc r492s... Bc r495s is evicted.

of Ãc fill one cache way of all cache sets. In the worst case we thus have: ¨mr misses.(6.27) Considering Example 21, we have that after the pR-A rp0q ∥R-B rp0q q sequence, elements Bc r492s... Bc r495s and Ãc r512s... Ãc r515s are present in set #33, with the elements of B rp0q being the least recently used.

iii) B r becomes the least recently used because of C r and is evicted by A r We now consider a sequence of operations comprising three micro-kernel executions, such as the one starting with R-C rp0q and ending with W -C rp2q in Example 22.

We suppose that cache blocks of B rp0q are mapped to the same cache sets as cache blocks of C rp1q and of A rp1q . In this case, when the cache blocks of B rp0q become the least recently used after R-C rp1q , they are evicted by the operations of R-A rp1q . Following the algorithm, when they become old again after W -C rp1q , they cannot be evicted by R-A rp2q , because by construction the cache sets that are occupied by the blocks of A rp1q and A rp2q are distinct (Property 6). See Figure 6.19 for an illustration.

Thus, reading and writing to a given micro-tile C r cannot contribute to evicting B r twice. Again, we must multiply the cache blocks occupied by B r by the number of times one cache way of each cache set is filled with the Q mc mr U micro-tiles C r . We thus have:

» - - - Q mc mr U ¨mr s L1 fi ffi ffi ffi ¨R k c ¨nr X L1 V misses. (6.28)

Let us exemplify this scenario with Example 21. After the pR-A rp0q ∥R-B rp0q q sequence, B rp0q has the most recent blocks in sets #65 and #66. Then writing Cr1056s, of C rp0q , in set #66 makes B rp0q old in this set. In the next sequence, A rp1q is read. When element Ãc r1040s is read and its block loaded in set #66, the reads of B rp0q have not yet reached the block mapped to set #66, so the B rp0q block that was loaded in this set gets evicted.

#### 6.5.6.2.4. Upper bound on cache misses due to writing Cr

We now look at the first four operations of Example 22, i.e. R-C rp0q , R-A rp0q , R-B rp0q and W -C rp0q . As the cache blocks within any given micro-panel do not conflict (Property 7), the problematic case is when cache blocks of A rp0q and of B rp0q are mapped to the same cache sets as cache blocks previously loaded for C rp0q . In this case, R-A rp0q makes elements of C rp0q to be the least recently used, and R-B rp0q can evict them. U consecutive calls to the micro-kernel, Figure 6.20 illustrates a potential mapping of successive micro-tiles C r to cache sets. Each micro-tile occupies m r (potentially scattered) cache blocks (Property 8) and s L1 mr micro-tiles are needed to fill one way of each cache set (for space reasons, not all sets are present in the figure). The figure also depicts a possible mapping of a micro-panel B r and of micro-panels A r . Since our studied L1D cache only has two physical ways, conflicts can arise. However, we also observe that only the cache blocks of micro-tiles C r that are mapped to the same sets as B r can be evicted, i.e. a maximum of For Example 21, this conflictual case corresponds to writing element Cr528s of C rp0q to cache set #33, since after the pR-A rp0q ∥R-B rp0q q sequence, both A rp0q and B rp0q have a cache block in this set.

We must multiply the resulting cache misses by the number of times that the

U

, i.e. the number of existing micro-panels B r . We thus have a total of cache misses in the macro-kernel corresponding to:

R n c n r V ¨ˆR m c m r V ¨mr `R m c m r V ¨R m r ¨kc X L1 V `R k c ¨nr X L1 V `» - - - Q mc mr U ¨Q mr¨kc X L1 U s L1 fi ffi ffi ffi ¨2 ¨mr `» - - - Q mc mr U ¨mr s L1 fi ffi ffi ffi ¨R k c ¨nr X L1 V `» - - - Q mc mr U ¨mr s L1 fi ffi ffi ffi ¨R k c ¨nr X L1 V ‚ (6.30)

Illustrating the presented reasoning with Example 21, we find an upper bound of 2, 703, 897 L1D cache misses in the macro-kernel executions.

Throughout our experiments, we have identified a special case of matrices configurations that slightly modifies the reasoning for cache misses in the macro-kernel. We describe this particular case hereafter.

#### 6.5.6.3. Upper bound on the number of cache misses -particular case

Assume that Ãc , B r and a slice of C c of height m c and width X L1 aligned in memory to the start of a cache block, individually do not occupy more than one cache way by set. In this scenario, cache blocks previously loaded for a given micro-tile C r may be still available when updating the next micro-tile that shares the same cache blocks. It could correspond to, for example, the cache blocks composing C rp0q and C rp4q in Figure 6.9. Additionally, it is likely that Ãc , or a part of it, also stays in the cache for the totality of the macro-kernel. With respect to the general case presented previously, we must revise the misses due to reading C r and A r , as well as writing C r , while the misses due to reading B r do not change.

#### 6.5.6.3.1. Upper bound on cache misses due to C c

Each cache block contains elements belonging to X L1 nr different micro-tiles. Thus on average, each micropanel B r will cause pm c ¨nr X L1 q misses due to the initial reading of micro-tiles (in total: one per row per cache block). In addition, as illustrated in Figure 6.20 and explained in Section 6.5.6.2.4, cache misses due to evictions in C c are bounded by the number of cache blocks occupied by a micro-panel B r . We thus multiply this bound by the number of micro-tiles C r present in a cache block minus one, since these misses can only occur after the first load of these blocks, which are accounted for in the formula for the initial charging of C c . As there are Q nc nr U micro-panels B r in the macro-kernel, we have: however still use n " 736, the subtlety is that the stride in memory between successive matrix rows is now of 752 elements. In matrix configuration (iii), we padded matrix A because k X L1 is not an odd integer. However, we remark from the L1D refills for packing A c in the column of Low et al. that, for this particular matrix, there are no extra misses, even though the rows of A occupy an even number of cache blocks. As explained, for packing A c this condition is not as crucial as for the other functions as only m r cache blocks are used at a time to read A c , which reduces the occurrence of two of these blocks being mapped to the same cache set. Depending on the application, the potential padding of matrices A and B can be performed beforehand or using DMA copies. Otherwise, the padding routine must be included when assessing the measured execution time.

R n c n r V ¨pm c ¨nr X L1 `R k c ¨8 X L1 V ¨p X L1 n r ´1qq misses. (6

For the evaluation of cache misses in the macro-kernel, the first three configurations use the general formulae of Section 6.5.6.2. Contrarily, in the fourth configuration the last macro-kernel corresponds to the particular case presented in Section 6.5.6.3. We observe that in most matrix configurations our formulae overestimate the number of misses in the macro-kernel by approximately 5%, which is reasonable given the complexity of the analysis. For matrix configuration (i), the overestimation is more significant. In this case, the dimensions of the submatrices of the last macro-kernel are slightly bigger than in Section 6.5.6.3, but the remainder is not large enough to fill the cache. This leads to a larger overhead, as our formulae assume full usage of the cache. Table 6.11 shows the average (and variability between minimum and maximum) measured execution times of the GEMM algorithm when using our parameters. It also depicts the difference, in percentage, with respect to the execution times obtained using the parameters of Low et al., presented in the last column of Table 6.6. We observe that the cost of predictability in the measured average execution times does not exceed 4.22% in our experiments.

Lastly, we note that the L2 cache of our target has a random replacement policy, so our formulae cannot be extended for it. However, in our experiments, it was large enough not to interfere.

#### 6.5.8. Discussion on the generalizability of the time-predictability analysis

The formulae for memory accesses and cache misses presented in the previous subsections are tailored for the state-of-art GEMM algorithm of [79] and for an ARM v7-A core of the Keystone II SoC. Our discussions do not focus on whether this algorithm is the most efficient in terms of average execution time, but reason on how to make it time-predictable. To analyze a different GEMM algorithm (e.g. different matrix partitioning to favour that A c , instead of B c , stays in the L1D cache [192]), the formulae must be adapted. Nevertheless, the reasoning to obtain them is described in detail and can be easily extended.

It is also noteworthy that Theorem 1, regarding the maximization of data sets usage when performing strided matrix accesses, is general.

Regarding the hardware model, our main assumptions concern the associativity degree (ą 1) and the replacement policy (LRU) of the L1D cache, as well as the absence of prefetching mechanisms. Thus, if the assumptions hold, the formulae remain valid and can simply be tuned to a different target, as they are parameterized by key hardware characteristics (e.g. vector units latency, cache sizes). When considering a distinct instruction set architecture (ISA), such as a RISC-V, only the micro-kernel function (see Algorithm 4) must be adapted, requiring minimal changes to the library.

### 6.6. Conclusion

In this chapter we discussed certifiable implementations of the 2D Convolutional layer with the primary objective of reducing its average execution time. First, we presented the state of the art in Convolutional layers optimizations. We reviewed optimizations through the layer's parameters compression, which are deemed out of the scope of this work, if only performed in the inference model. Then, we evaluated optimizations at the level of the Convolutional layer implementation and showed that most of them do not preserves the semantics of the inference model. Finally, we highlighted the GEMM-based convolution algorithm, an improved implementation that preserves the semantics of the direct convolution algorithm.

Afterwards, we explored the implementation of a vanilla GEMM routine. We introduced four variants of the vanilla GEMM algorithm and also discussed an indirect GEMM-based convolution, which employs a pre-computed matrix of patches. We showed that coding the Convolutional layer with a vanilla GEMM routine reduced the average inference time of convolutional models, at the cost of increasing memory bandwidth. We were also able to compute the WCET of vanilla GEMM routines using OTAWA.

Subsequently, we addressed the implementation of an architecture-aware GEMM routine. We proposed a predictable and traceable yet efficient implementation of a state-of-art blocked GEMM algorithm. Compared to a non-optimized implementation, the average execution time was reduced by up to 99%, without relying on compiler optimizations. However, we verified that the WCET produced by OTAWA did not reflect any code optimization.

Lastly, we presented a study on the time-predictability of the architecture-aware GEMM routine with respect to the L1 data cache. We demonstrated that, within each part of the algorithm, we were able to provide the correct number of memory accesses. Moreover, the number of L1D cache misses was only overestimated by around 5% in all but one of the tested matrix configurations. Lastly, our results indicated that tuning the parameters for predictability only increased average execution times in less than 5% in the studied use cases.

## Part III

## Conclusion & Perspectives

Chapter 7

## Conclusion & Perspectives

The work carried out in this thesis allowed a first investigation on the methods to implement offline trained feed-forward deep neural networks within embedded safety-critical real-time platforms. In accordance with established standards concerning the development of avionics systems and in progress guidelines addressing machine learning applications within these systems, we delimited a work scope. We were then able to provide a working framework, ACETONE, that successfully addresses this thesis' initial questions. Concurrently, we identified certain constraints inherent in our study, discerning promising perspectives for future exploration.

### 7.1. ML-based applications within avionics systems

In this work we focused on the certifiable and efficient implementation of feed-forward deep neural networks within avionics systems. The lifecycle of this kind of neural network models consists of two parts: the learning and the inference phases. The learning phase comprises the preparation of the data set, which depends on the choice of the learning approach, the design of the neural network, its training from collected data and the verification of the resulting model, which is called trained model. Once the learning phase completed, the inference phase consists in the forward, non-iterative, pass of input data trough the neural network. The inference model is then the implementation of the trained and verified neural network model. The question of how to correctly produce an accurate inference model for a given trained model and a given target hardware, in accordance with safety requirements, is the subject of this thesis.

Indeed, avionics systems are subject to certification procedures and must follow safety standards throughout their design, validation, and verification development cycle. Consequently, given the proven capacity of machine learning applications in diverse contexts, industrials, academics and regulatory bodies have started working in addressing the question of its safe, standardized use in safety-critical systems, such as avionics systems. Examples of initiatives include EASA roadmaps [1,4] and concept papers [2,5], as well as guidelines produced by the EUROCAE WG-114/SAE G-34 working group [152][153][154].

In accordance with the guidelines under construction concerning ML in safety-critical systems and focusing on certification requirements related to software items in avionics systems (DO-178C [67]), we identified a number of quantifiable objectives necessary to guarantee the safe and correct implementation of the inference model, namely:

(i) a precise description of its functionality (Objective 1);

(ii) the preservation of its semantics (Objective 2); (iii) the traceability of requirements (Objective 3); (iv) its timing predictability (Objective 4); (v) its efficient resource usage (Objective 5).

### 7.2. State-of-the-art machine learning frameworks

We have discussed state-of-the-art machine learning frameworks, which are programming environments for the design and deployment of neural networks. We first introduced ML frameworks specialized in the learning phase of neural networks, The learning phase of neural networks is not in the scope of this thesis, but since we aimed to implement an inference model that has been trained on a machine learning framework, it was imperative to understand how these work. Hence, we highlighted key points to observe when relying on these tools, notably with respect to the output format for the inference model description. Afterwards, we presented ML frameworks used in the deployment of inference models. We discussed inference engines, both proprietary and open-source, targeting inference execution in hardware architectures that could be used in the context of avionics systems. For each discussed solution we explained why, ultimately, it does not suit our needs. We then focused on two tools, Keras2c and microTVM, capable of generating a static C code for the inference model. These tools were, in principle, in accordance with the hypotheses of this thesis and were further used for benchmark with our proposed framework, ACETONE.

### 7.3. Contributions

#### 7.3.1. Formalization of the inference model semantics

Our first contribution towards a certifiable implementation of the inference model was the formalization of the semantics of the operations performed within neural networks. Initially, we formally defined feedforward deep neural networks as directed acyclic graphs. We then presented the formalization of the semantics, in the form of mathematical functions, of the neural networks' layers considered in the context of this thesis.

We were then able to present examples of model transformations that are authorized in the inference model before the implementation phase, as they preserve its semantics. We also introduced different neural network models of the state of the art, pertaining to the feed-forward class and containing a particular subset of layers types. Afterwards, we discussed our adopted format for the inference model description. The chosen format is a JSON-based file that relies on the defined semantics to provide an unambiguous and human-readable specification, allowing for a certifiable implementation of the inference model.

#### 7.3.2. Development and evaluation of the ACETONE framework

Once the semantics of the inference model are formally defined and having described a possible format for its unambiguous and textual description, we could proceed to implement the machine learning function. Our second contribution towards a certifiable implementation of the inference model was the development of ACETONE. The acronym stands for "Avionics C code generator for Neural Networks" and it designates our proposed framework for generating a semantically equivalent and predictable C code from the inference model description.

ACETONE is a tool for quickly experimenting, with a modular approach and open-source distribution. The framework is entirely written in Python and its software architecture consists of three main elements. The front-end is responsible for importing the inference model description file, which is, by default, the previously introduced JSON-based file. The front-end reads the model structure, extracts the parameters, and creates the corresponding Layer (Python) objects that serve as the intermediate-representation (IR) of the framework. The IR then interfaces with the framework back-end. The ACETONE back-end is dedicated to implementing the inference function in C. We then discussed the three different code generation strategies proposed by ACETONE, result of a design space exploration, to understand what would be the most suited code generation approach for a given inference model and target hardware.

We have also defined a comparative methodology to evaluate our approach. First, we proposed four assessment criteria, namely, the semantics preservation, the worst-case execution time, the average execution time and the memory layout of executables. We then provided quantitative results to evaluate these criteria for the code generated by each of the studied frameworks, i.e. ACETONE, Keras2c and microTVM, for the inference models considered. We concluded that ACETONE, notably the V2 backend, was overall competitive when compared to state-of-the-art frameworks with respect to the defined criteria. However, at the end of the evaluation phase, we identified in ACETONE a limitation concerning the performance, computed in terms of measured average execution time, of convolutional neural networks.

The ACETONE framework has been presented and published in the proceedings of the 34th Euromicro Conference on Real-Time Systems in 2022 [157]. An artifact with minimal working examples was made available at the same occasion [50].

#### 7.3.3. Certifiable optimization of the 2D Convolutional layer

Based on the observations concerning the measured average execution time of convolutional models within ACETONE, we focused on the implementation of the 2D Convolutional layer, in opposition to studying optimizations at model level. Hence, our third contribution towards a certifiable and efficient implementation of the inference model was optimizing the 2D Convolutional layer implementation.

After a study of the state of the art, we chose to explore the GEMM-based convolution algorithm. It consists of an improved implementation of the Convolutional layer, relying on a GEMM (General Matrix-Matrix Multiplication) routine, that preserves the semantics of the direct convolution algorithm originally implemented in ACETONE. One of the main reasons of leaning towards GEMM-based convolutions was to rely on the principles of BLAS libraries, but these tools were not developed in a manner aware of the requirements of certification, hindering in particular the WCET analysis task. To overcome this limitation, we proceeded to develop our own GEMM routines.

Initially, we developed a vanilla GEMM implementation, a version that does not make use of any hardware-specific tuning techniques to improve memory transfers or computation rate. We introduced four variants of the vanilla GEMM algorithm and also discussed an indirect GEMM-based convolution, which employs a pre-computed matrix of patches. We showed that coding the Convolutional layer with a vanilla GEMM routine reduced the average inference time of convolutional models, at the cost of increasing memory bandwidth. We were also able to compute the WCET of vanilla GEMM routines using OTAWA. The vanilla GEMM implementation is at present fully integrated into the code generation workflow of ACETONE. This work was the subject of the paper published at the Special Issue on Predictable Machine Learning of the Real-Time Systems Journal [157] Subsequently, in an effort to align with established BLAS libraries, we addressed an architectureaware GEMM implementation, which is currently available in the form of a library. We proposed a predictable and traceable yet efficient implementation of a state-of-art blocked GEMM algorithm on a COTS processor with single-instruction multiple-data (SIMD) extensions. Compared to a non-optimized implementation, the measured average execution time was reduced by up to 99%, without relying on compiler optimizations. However, we verified that the WCET produced by OTAWA did not reflect any code optimization. This observation instigated our efforts on a study of the time-predictability of the analysed blocked GEMM algorithm.

Time-predictability was evaluated with respect to the L1 data cache. We then provided a set of rules for choosing the algorithm blocking parameters and predict with precision its number of memory accesses and cache misses. We focused on these two numbers as they can be exploited in static WCET estimation techniques such as IPET in order to tighten the produced WCET bounds. As result, we demonstrated that, within each part of the algorithm, we were able to provide the correct number of memory accesses. Moreover, the number of L1D cache misses was only overestimated by around 5% in all but one of the tested matrix configurations. Our results also indicated that tuning the parameters for predictability only increased measured average execution times in less than 5% in the studied use cases.

Both the avionics-compliant implementation of the blocked GEMM algorithm and the study on its time-predictability were the object of a paper accepted at the 30th IEEE Embedded Technology and Applications Symposium (RTAS 2024) [49].

### 7.4. Perspectives

As a result of the research conducted in this thesis, several perspectives emerge. We highlight notably the extension of our framework ACETONE as well as the deepening of architecture-aware implementations of the inference model. Other activities are also being carried in order to make the software architecture more robust and the framework simpler to use, with a distribution in the form of a Python package.

#### 7.4.1. Extending the capabilities of ACETONE

Furthermore, as mentioned in Chapter 6, other perspectives arise concerning trained models undergone optimizations for parameters compression. These optimizations are particular relevant for environments with limited memory or computational resources, such as avionics. We highlighted that ACETONE can be easily adapted to generate inference C code for compressed models, with the condition that the compression is done before the inference model is established. Concerning quantized models, the framework must be incremented to support operations in low-precision arithmetic, which would probably require refining the semantics preservation assessment as well. With respect to sparse (pruned) inference models, it would be advantageous to adapt the layers' implementations to take advantage of the model's sparsity and only perform computations on the non-zero elements. Adjusting the layers' functions would be particular pertinent for computational expensive layers such as Convolutional, but also Dense layers. In addition, a sparsity-aware representation of the model's parameters could be studied.

Subsequently, as noted in Chapter 6, we studied a certifiable optimized implementation of the Convolutional layer relying on GEMM-based convolutions, however the final blocked GEMM routine is for the moment available as an independent library. A first step would then to integrate the complete solution for optimized GEMM-based convolutions into ACETONE's code generation workflow. The tailored routines could then be automatically generated upon provision of the processor's caches and vector characteristics, as they are parametrized by these hardware intrinsics. Within this thesis we developed an optimized implementation for an ARM v7-A core of the Keystone II SoC. However, to consider a similar processor but with a distinct ISA, only minimal changes would be required to the library. In particular, the assembly vectorized micro-kernel must be modified to support the different instructions. Furthermore, the BLAS studied principles could also be extended for the implementation of Dense layers, which contain a matrix-vector algorithm.

#### 7.4.2. Architecture-aware implementation of the inference model

We showed that optimizing the GEMM routine for a given target hardware highly improves the average inference time. We were also able to perform an analytical study on the time-predictability of this complex routine based on the target hardware characteristics. Both endeavours pave the way for similar research concerning a tailored implementation of the entire inference model. It can be conceivable, for example, to have distinct inference model implementations for each different type of hardware under consideration. Afterwards, a comparative evaluation can be conducted to ascertain what is the most suitable implementation for a given inference model.

In this thesis we restricted our scope to multi-core COTS processors and in particular only studied a single-core implementation. The natural continuation is to investigate parallelism at the level of the different cores. In this regard it is possible to split the different layers of the model into distinct hardware items, or yet parallelise the computations within a layer, similar to the approach proposed in [76]. Another strategy can be to execute one instance of the inference model per core, and allocate the input batch across the various instances.

Another extension could be to propose a specialized implementation per layer configuration. For instance, it was observed in Chapter 6.3 that for the Convolutional layer, different variations of a same algorithm may perform better than others according to the parameters of the layer. It is also the conclusion motivating auto-tuning methods that search for optimal implementation parameters mentioned in Chapter 6.4.

Finally, the work carried within this thesis can be extended to explore open hardware initiatives. Exploring this axis would be highly beneficial for time-predictability considerations. Indeed, mastering the hardware design and components, would allow for a finer analysis regarding the execution behaviour of the complete inference model. In particular, it would be possible to extend the analysis presented in Chapter 6.5 and take into account more elements of the memory hierarchy, such as Level 2 and Level 3 caches, and translation lookaside buffers (TLB), as well as different cache replacement policies.

Part IV Appendices sécurité. Un système est dit critique (pour la sécurité) lorsqu'une défaillance interne peut avoir des effets catastrophiques sur la sécurité, y compris la perte du système et de vies humaines. Par exemple, files textes réglementaires définissent que, pour files systèmes files plus critiques, la probabilité acceptable d'une défaillance catastrophique doit être inférieure à 10 ´9 par heure de vol.

Ainsi, files systèmes avioniques sont soumis à des procédures de certification visant à garantir la conformité aux normes de sécurité tout au long de leur cycle de développement, depuis la définition des besoins jusqu'à la validation et la vérification de la fonction attendue. Parmi files documents existants, nous pouvons citer files normes ED-79B/ARP4754B [70] et ED-135/ARP4761A [71], qui présentent des lignes directrices pour le développement et l'évaluation de la sécurité au niveau du système. Au niveau des composants du système, files documents ED-80/DO-254 [66] et ED-12C/DO-178C [67] offrent, respectivement, des orientations pour le développement sécurisé d'éléments matériels et logiciels. Ainsi, conformément aux initiatives de l'AESA, un groupe de travail conjoint UE-États-Unis (EU-ROCAE WG-114/SAE G-34) rédige actuellement la directive, nommée norme ED-324/ARP6983 [152], à utiliser dans l'élaboration de produits liés à la sécurité mettant en oeuvre l'apprentissage automatique, permettant leur approbation dans l'aéronautique. Dans le contexte de l'implantation du modèle d'inférence, la directive ARP6983 devrait s'interfacer avec la norme DO-178C établie, qui concerne le développement de composants logiciels dans files systèmes avioniques.

Par conséquent, pour permettre l'utilisation d'applications basées sur l'apprentissage automatique dans files systèmes critiques, files acteurs du domaine aéronautique ont commencé à travailler sur la question de son utilisation sûre et standardisée. Le champ d'application initial de ces initiatives est également limité aux réseaux neuronaux entraînés hors-ligne et supervisés. Il a été convenu que le processus de développement axé sur la sûreté de fonctionnement reste inchangé, sauf lorsqu'un système ou un sous-système intègre des composants basés sur l'apprentissage automatique, auquel cas des directives adaptées sont nécessaires. L'Agence de l'Union européenne pour la sécurité aérienne (AESA) a établi des feuilles de route[1,4] et des documents de réflexion[2,5] visant à orienter la recherche et à définir un calendrier pour files livrables réglementaires. En particulier, files documents de réflexion de l'AESA ont proposé un nouveau cycle de développement en forme de W pour files applications basées sur l'apprentissage automatique, représenté dans la Figure A.1.

## A.1.2 Directives pour files applications basées sur l'apprentissage automatique dans files systèmes avioniques

## A.2 Approche

## A.2.1 Définition des objectifs de certification pour l'implantation du modèle d'inférence

Tout d'abord, nous avons limité notre champ d'application aux réseaux neuronaux profonds à action directe. Dans ces variantes, chaque couche intermédiaire du réseau neuronal prend en entrée la sortie de la couche précédente, ce qui fine permet aucun cycle dans sa structure. En outre, comme mentionné, nous nous concentrons sur le modèle d'inférence. Nous considérons donc que le réseau neuronal a été entraîné et vérifié et qu'il n'est pas censé évoluer pendant la phase d'inférence. Ces hypothèses sont conformes à la définition d'un objectif initial raisonnable dans files documents de réflexion de l'AESA. Cependant, tant qu'il est réalisé hors-ligne, nous sommes indifférents au paradigme d'apprentissage employé. Ce dernier peut être de type supervisé, non supervisé ou basé sur l'apprentissage par renforcement.

Deuxièmement, nous avons défini un certain nombre d'objectifs quantifiables nécessaires pour garantir l'implantation sûre et correcte du modèle d'inférence. Ces objectifs fine représentent pas toutes files exigences présentes dans files normes de certification, mais ils ont été reconnus comme étant complexes à obtenir pour le flux de travail traditionnel des logiciels d'apprentissage automatique et sont conformes aux directives en cours d'élaboration, c'est-à-dire files feuilles de route de l'AESA et la norme ARP6983. Les objectifs de certification dérivés concernant l'implantation du modèle d'inférence vont de sa description à la fonction d'inférence exécutable. Ces objectives requièrent :

(i) une description précise de sa fonctionnalité (Objectif 1) ;

(ii) la préservation de sa sémantique (Objectif 2) ; (iii) la traçabilité des exigences depuis leur description jusqu'à l'exécutable final (Objectif 3) ; (iv) la prédictibilité temporelle de l'implantation (Objectif 4) ;

## A.2.3 Formalisation de la sémantique du modèle d'inférence

Comme indiqué dans la Section A.2.1, l'un des objectifs dérivés pour une implantation certifiable du modèle d'inférence concerne la préservation de sa sémantique. Le Chapitre 4 présente donc notre première contribution à cet objectif : la formalisation de la sémantique des opérations effectuées dans files réseaux neuronaux. Ce travail est une extension de l'article présenté à ECRTS 2022 [157]. Dans un premier temps, la Section 4.1 fournit une définition formelle des réseaux neuronaux profonds à action directe en tant que graphes acycliques dirigés. La Section 4.2 explique ensuite notre approche de la formalisation de la sémantique du modèle d'inférence et souligne l'importance de ce travail. Ensuite, la Section 4.3 présente le concept de tenseurs, ou tableaux multidimensionnels, manipulés dans files réseaux neuronaux. Enfin, la Section 4.4 fournit la sémantique, sous forme de fonctions mathématiques, des couches des réseaux neuronaux considérées dans le contexte de cette thèse.

Après la présentation de la sémantique de chaque couche, la Section 4.5 traite des transformations qui peuvent être appliquées au modèle d'inférence avant son implantation, car elles fine modifient pas sa sémantique. La Section 4.6 s'appuie sur files sections précédentes et présente la sémantique des modèfiles de réseaux neuronaux de l'état de l'art ciblés dans cette thèse, c'est-à-dire ceux du type à action directe et contenant un sous-ensemble particulier de types de couches. Enfin, la Section 4.7 introduit le format que nous avons adopté pour la description du modèle d'inférence. Le format choisi est un fichier basé sur JSON qui s'appuie sur la sémantique définie pour fournir une spécification non ambiguë et lisible par l'être humain, permettant une implantation certifiable du modèle d'inférence.

## A.2.3.1 Sémantique du modèle d'inférence

Comme indiqué, dans ce travail, files réseaux neuronaux sont définis comme des graphes acycliques dirigés, dans lesquels chaque noeud représente une couche. En outre, dans la Section 2.3, nous avons expliqué ce qui constitue la sémantique du modèle d'inférence : (i) la caractérisation de la structure du graphe acyclique dirigé, et (ii) la sémantique formelle des opérations effectuées par chaque noeud du graphe. Pour y parvenir, comme l'évoque la Définition 7, nous avons décidé de formaliser la sémantique des couches des réseaux neuronaux en tant que fonctions mathématiques. Pour chaque couche, nous établissons donc une fonction mathématique, avec des domaines d'entrée et de sortie définis, caractérisée par une formule claire et non ambiguë délimitant le calcul d'une valeur de sortie pour toute valeur d'entrée dans files domaines spécifiés.

En effet, la définition d'une sémantique formelle est une étape cruciale pour l'implantation correcte du modèle d'inférence. Les formules mathématiques fournissent une référence pour générer un code C pour le modèle d'inférence qui est sémantiquement équivalent à l'implantation de l'environnement d'apprentissage. La

## A.2.3.2 Fonctions associées aux couches des réseaux neuronaux

Fournir la sémantique formelle des couches d'intérêt a consisté à rassembler, étendre et formaliser la littérature existante, notamment la documentation évolutive des frameworks d'apprentissage automatique (e.g. files documentations de TensorFlow [167], PyTorch [148], ONNX [140] et NNEF [170]). Pour illustrer le contenu de la Section 4.4, nous présentons ici la sémantique formelle de la couche Dense.

## A.2.4.1 Aperc ¸u de l'approche d'ACETONE

Le code C généré par ACETONE est conçu pour préserver la sémantique du modèle entraîné, c'est-à-dire reproduire le même comportement que celui observé dans l'environnement d'apprentissage. Pour garantir la préservation de la sémantique, nous adhérons au formalisme mathématique présenté dans le Chapitre 4 et fournissons un back-end C avec l'implantation de la sémantique des couches. Le code C résultant est également structuré de manière à être prédictible. Pour ce faire, nous éliminons l'utilisation d'abstractions de programmation susceptibles d'entraver la prédictibilité temporelle, notamment l'allocation dynamique de la mémoire. La séquence des instructions est également résolue de manière statique. Comme nous proposons une solution pour le déploiement du modèle d'inférence dans un système à ressources limitées, nous nous sommes également intéressés à la conception du code d'inférence en ce qui concerne son utilisation de la mémoire sans toutefois effectuer des optimisations très fines en premier lieu. À cette fin, nous avons étudié et déterminé l'agencement souhaité de la mémoire du binaire correspondant au code C généré. En outre, comme nous voulions explorer la meilleure stratégie de génération de code pour nos besoins, nous avons initialement proposé trois versions de code C différentes.

ACETONE est entièrement écrit dans le langage de programmation Python. Nous avons décidé de nous appuyer sur Python principalement pour sa simplicité et ses abstractions de haut niveau, permettant un prototypage et une itération rapides, ainsi que pour son vaste écosystème de paquets. De plus, il s'agit de l'environnement de programmation adopté dans l'interface de la plupart des frameworks d'apprentissage automatique, ce qui facilite le partage des concepts. Notez que ACETONE fonctionne principalement comme un outil permettant de générer facilement et rapidement du code C à partir d'une spécification et notre intention actuelle n'est pas de le certifier. Ainsi, seul le code produit par cet outil est soumis à une évaluation selon files objectifs définis dans la Section 2. Tout d'abord, nous avons sélectionné un ensemble de benchmarks représentatifs de l'état de l'art en apprentissage automatique et qui sont cohérents avec le type de réseaux neuronaux ciblés dans cette étude, à savoir files réseaux à action directe composés des types de couches particuliers introduits dans la Section 4.4. Plus précisément, nous nous sommes appuyés sur files modèfiles d'inférence présentés dans la Section 4.6. L'objectif était de mener une vaste campagne de tests en faisant varier plusieurs paramètres (nombre et type de couches, type de données des paramètres).

Nous avons ensuite défini un certain nombre de critères d'évaluation basés sur files objectifs de certification dérivés dans la Section 2. En outre, nos résultats expérimentaux ont souligné la capacité concurrentielle d'ACETONE par rapport à l'état de l'art. Grâce aux tests et à la validation, nous avons démontré notre capacité non seulement à égaler, mais aussi à dépasser occasionnellement files résultats de Keras2c et Static microTVM en termes de critères initialement définis. Ces résultats réaffirment la pertinence de notre travail en vue d'une solution pour une implantation certifiable du modèle d'inférence. Nous soulignons toutefois la principale limite identifiée dans ACETONE: la performance, calculée en termes de temps d'exécution moyen mesuré, des réseaux neuronaux convolutifs.

## A.2.5 Optimisation certifiable de la couche Convolutionnelle 2D

Dans le Chapitre 5, nous avons démontré qu'en termes de temps d'exécution moyen, l'implantation des modèfiles d'inférence générés par ACETONE était très compétitive par rapport aux solutions fournies par files frameworks de l'état de l'art. En particulier, ACETONE back-end V2 a été en mesure de surpasser files autres outils étudiés en ce qui concerne ce critère dans plusieurs cas d'utilisation. Cependant, en ce qui concerne files modèfiles convolutifs traités, c'est-à-dire files modèfiles qui contiennent au moins une couche Convolutionnelle 2D, cela n'a pas été invariablement vrai. Nous avons précédemment discuté des transformations préservant la sémantique, visant à améliorer l'utilisation des ressources, au niveau du modèle. Nous nous concentrons dans un deuxième temps sur files optimisations au niveau des couches. Ainsi, le Chapitre 6 présente notre troisième contribution vers une implantation certifiable et efficace du modèle d'inférence : files optimisations sur l'implantation de la couche Convolutionnelle 2D. Dans la suite de ce résumé, sauf indication contraire, une couche Convolutionnelle fait référence à la couche Convolutionnelle 2D présentée dans la Définition 26.

Dans la Section 6.1, nous commençons par motiver l'attention portée à cette couche particulière. En effet, files couches Convolutionnelles dominent généralement la charge de travail de calcul dans le cadre des réseaux de neurones profonds à action directe que nous considérons. Cela est le résultat du grand nombre d'opérations en virgule flottante (ou FLOPs, de l'anglais floating-point operations) impliquées dans l'opération de convolution, ce qui rend cette couche très intensive en termes de calcul. D'autres types de couches présentes dans files modèfiles d'inférence étudiés, comme files couches Denses, impliquent également des multiplications de tenseurs et peuvent occasionnellement avoir un plus grand nombre de paramètres entraînables ; cependant, elles présentent toujours une intensité de calcul réduite par rapport aux couches Convolutionnelles. Dans l'exemple 16, nous avons étudié une couche Convolutionnelle et une couche Dense du modèle d'inférence LeNet-5 (Exemple 4.6.2) et avons observé que, bien que la couche Convolutionnelle comprenne environ 0, 49% du nombre de poids entraînables de la couche Dense, elle effectue environ 5.6 fois plus de FLOPs que cette dernière. Cette observation corrobore l'affirmation selon laquelle files couches Convolutionnelles sont intensives en termes de calcul, tandis que files couches Denses sont plus intensives en termes de mémoire.

Ensuite, la Section 6.2 présente l'état de l'art des optimisations de la Convolutionnelle 2D et discute de leur applicabilité dans notre contexte. Les sections restantes se concentrent sur files routines de multiplication matricielle générale (GEMM), qui sont au coeur de l'algorithme de convolution basé sur GEMM. Tout d'abord, la Section 6.3 décrit une implantation de GEMM vanille (i.e. de référence et naïfive) ainsi que son intégration dans ACETONE. Ensuite, la Section 6.4 présente une implantation de GEMM dépendant de l'architecture, qui est disponible sous la forme d'une bibliothèque. Enfin, la Section 6.5 fournit une analyse de la prédictibilité temporelle de la routine GEMM dépendant de l'architecture.

## A.2.5.1 Etat de l'art en matière d'optimisation des couches Convolutionnelles 2D

Plusieurs techniques existent dans le but d'atténuer l'intensité de calcul des couches Convolutionnelles. Nous classons files stratégies d'optimisation des couches Convolutionnelles étudiées en deux groupes dis-résultante C est de forme mˆn. Toutes files matrices sont à valeurs réelles. La matrice C est alors obtenue en multipliant élément par élément files entrées des lignes de A et des colonnes de B. Pour exécuter cet algorithme files entrées originales de la couche Convolutionnelle doivent donc être adaptées.

Tout d'abord, le tenseur d'entrée est transformé en une matrice augmentée de type Toeplitz [81]. Cette matrice est construite en stockant commodément en colonnes l'ensemble des éléments, également appelés patchs, du tenseur d'entrée qui seront multipliés par chaque noyau convolutif, à chaque itération de l'opération de convolution. L'algorithme de construction de patchs est appelé im2col dans [33], comme dans image en colonnes, car dans la plupart des applications de couches Convolutionnelles 2D, le tenseur d'entrée est une image (un tenseur tridimensionnel). Le tenseur de patchs qui en résulte est stocké dans la matrice B.

L'algorithme im2col est illustré dans la Figure A.7. Dans cette illustration, nous avons une opération de convolution avec un pas (stride) de un (s h " s w " 1). Chaque colonne (patch) de B contient f h ¨fw éléments de chaque canal du tenseur d'entrée, totalisant f h ¨fw ¨fc entrées. Les dimensions en hauteur et en largeur du tenseur de sortie (voir l'Equation 4.24) déterminent le nombre de colonnes de la matrice de patchs, c'est-à-dire o h ¨ow . La matrice B est alors de la forme f h ¨fw ¨fc ˆoh ¨ow . Nous avons également montré dans l'Exemple 17 que l'algorithme de convolution basé sur GEMM préserve la sémantique de l'algorithme de convolution directe, car files deux algorithmes effectuent exactement files mêmes opérations arithmétiques. La seule différence est que dans files deux algorithmes, files tenseurs d'entrée de la couche Convolutionnelle sont organisés différemment en mémoire.

De nombreuses implantations BLAS des routines GEMM sont disponibles dans la littérature. Parmi files exemples de bibliothèques open-source pour files CPU, on peut citer OpenBLAS [188], ATLAS [102] et BLIS [175]. D'autres solutions sont propriétaires, comme Intel oneAPI Math Kernel Library (oneMKL) [95] et Arm Performance Libraries [96]. Ces bibliothèques utilisent essentiellement des techniques de blocage de matrice et la plupart d'entre elles proposent des implantations spécifiques au matériel, afin d'optimiser files calculs autant que possible. Cependant, files bibliothèques BLAS n'ont pas été développées en tenant compte des exigences de la certification, ce qui entrave en particulier la tâche d'analyse du temps d'exécution au pire cas. En effet, elles utilisent notamment l'allocation dynamique de la mémoire et s'appuient sur de nombreuses optimisations du compilateur. Il est donc difficile de files utiliser sans modifications dans un contexte avionique.

Pour surmonter cette limitation tout en utilisant files principes présentés dans files bibliothèques BLAS, nous avons développé nos propres routines GEMM pour exécuter un algorithme de convolution basé sur GEMM. Initialement, nous avons développé une implantation GEMM vanille, qui est actuellement entièrement intégrée dans le flux de génération de code de ACETONE. Par la suite, dans un effort d'alignement avec files bibliothèques BLAS établies, nous avons proposé une implantation GEMM dépendant de l'architecture, qui est maintenant disponible sous la forme d'une bibliothèque. Cette solution est polyvalente, car elle peut être utilisée comme bibliothèque autonome ou intégrée de manière transparente dans la chaîfine d'outils ACETONE.

## A.2.5.1.3 Implantation d'une routine GEMM vanille

Notre première implantation consiste en un déploiement simple en virgule flottante de l'algorithme de multiplication matrice-matrice. En effet, nous parlons d'une implantation vanille car cette version n'utilise aucune technique de réglage spécifique au matériel pour améliorer files transferts de mémoire ou le taux de calcul. La routine GEMM telle que définie dans files paquets BLAS est de la forme C Ð αA ¨B `βC, où la matrice A est de la forme m ˆk, la matrice B est de la forme k ˆn et la matrice résultante C est de la forme m ˆn. Les termes α et β sont des scalaires constants. Sans perte de généralité, nous considérons pour la routine GEMM vanille le cas spécial de la multiplication matrice-matrice où α " 1 et β " 0.

## Variantes pour la routine GEMM vanille

Comme spécifié dans BLAS, la routine GEMM permet de transposer l'une ou l'autre des trois matrices, ou la totalité d'entre elles. Du point de vue de l'implantation, la transposition d'une matrice peut être considérée comme une transition entre différentes conventions de présentation des données. De la même manière que pour files tenseurs 3D, files matrices (tenseurs 2D) peuvent être aplaties en utilisant des conventions distinctes pour leur stockage dans un espace mémoire linéaire (voir la Section{refsubsec:memlayout-tensors). Dans le cas des matrices, la littérature met l'accent sur files formats de données row-major et column-major, qui sont détaillés dans la section 6.3.1. Nous avons ensuite proposé quatre variantes de l'algorithme GEMM vanille, en explorant différentes dispositions de la mémoire pour files matrices A, B et C.

Ensuite, nous avons testé files quatre variantes des routines GEMM avec un certain nombre de configurations de convolution. L'objectif était d'analyser comment files convolutions basées sur GEMM, utilisant files différentes routines GEMM, se comparent entre elles et par rapport à l'algorithme de convolution directe initial. Nous avons donc sélectionné files première et deuxième couches Convolutionnelles de LeNet-5 [119], la deuxième d'AlexNet [112] et la première des modèfiles VGG-16 [158]. Nous avons pu observer que files convolutions basées sur GEMM, qui exploitent un meilleur accès à la mémoire, surpassent toujours l'algorithme direct. Cependant, files paramètres de convolution, e.g. taille du tenseur d'entrée, nombre de noyaux de convolution ou pas de filtrage, qui influencent la structure des matrices, impactent files performances des différents algorithmes basés sur GEMM. Nous avons conclu qu'aucune routine n'obtient systématiquement files meilleurs résultats pour toutes files couches Convolutionnelles testées. Veuillez vous référer à la Figure 6.3 pour l'intégralité des résultats.

Optimisation de la construction de la matrice de patchs Avant de nous concentrer sur l'amélioration de la routine GEMM vanille elle-même, nous avons porté notre attention sur l'optimisation de l'algorithme de convolution basé sur GEMM qui utilise la routine GEMM vanille précédemment présentée. En effet, la création d'une matrice augmentée à partir du tenseur d'entrée avant chaque couche Convolutionnelle représente une tâche gourmande en ressources, imposant un délai significatif pendant l'inférence. Pour y remédier, nous avons développé une variante de l'algorithme de convolution basé sur GEMM qui exécute l'algorithme de construction des patchs hors-ligne. Cette stratégie repose sur le même principe que l'idée présentée dans [63].

Certes, nous fine connaissons pas files valeurs exactes des éléments constituant la matrice de patchs, car ils dépendent des entrées de la couche et fine sont découverts qu'à l'exécution. Cependant, nous savons où files trouver dans le tenseur d'entrée. En effet, nous connaissons files adresses des variables constituant la matrice de patchs par rapport au tableau du tenseur d'entrée, quelle que soit l'entrée réelle. Ainsi, nous pouvons préparer à l'avance le squelette de la matrice de patchs, par exemple dans le générateur de code ACETONE.

En pratique, nous disons que le code généré pour l'algorithme de convolution basé sur GEMM contient une matrice de pointeurs vers files éléments du tenseur d'entrée constituant files patchs. Contrairement à la création explicite de la matrice augmentée de patchs avec files valeurs réelles en virgule flottante. La Figure 6.4 illustre le fonctionnement de la matrice de pointeurs. Nous appelons cet algorithme convolution indirecte basée sur GEMM, par opposition à la convolution standard basée sur GEMM discutée précédemment.

Dans la Figure 6.5, nous avons pu examiner comment deux algorithmes utilisant la version indirecte de la convolution basée sur GEMM, à savoir indirect GEMM_NN et indirect GEMM_NT, se comparent à leurs équivalents dans la version standard et à l'algorithme de convolution directe, en termes de temps d'exécution moyen. Nous observons une réduction du nombre de cycles mesurés, dont l'intensité dépend de la configuration de la convolution. Nous expliquons cela par le fait que l'algorithme de construction des patchs est effectué avant l'exécution.

## Intégration de la routine GEMM vanille dans ACETONE

Enfin, nous avons intégré files templates des routines GEMM vanille dans ACETONE, permettant ainsi l'exécution de convolutions basées sur GEMM. Afin de tester files avantages pratiques et files limitations des convolutions basées sur GEMM, nous avons appliqué la même méthodologie d'évaluation décrite dans la Section 5.3. Nous avons montré que coder la couche Convolutionnelle avec une routine GEMM vanille réduisait le temps moyen d'inférence des modèfiles convolutionnels (voir Table 6.3), au prix d'une augmentation de la bande passante mémoire (voir Table 6.4). Nous avons également pu calculer le temps d'exécution au pire cas des routines GEMM vanille en utilisant OTAWA et nous avons constaté, dans la Table 6.2, que files bornes du temps d'exécution au pire cas étaient également réduites avec files convolutions basées sur GEMM, par rapport à la version utilisant l'algorithme de convolution directe. Ce comportement est cohérent puisque files temps d'exécution moyens ont effectivement diminué, et cela nous

## Figures et tableaux

**Figure 1.** 2: Figure 1.2: Adopted approach for the certification-aware implementation of the inference model.

**Figure 2.** 1 illustrates the general lifecycle of neural networks, applied to a neural network model used for a classification task. The upper part of the figure depicts the supervised learning process and the bottom part shows the forward pass of the inference phase performed in a new, unseen input.

**Figure 2.** 1: Figure 2.1: Lifecycle of a classification neural network.

" Guidelines and methods for conducting the safety assessment process on civil airborne systems and equipment" ED-79B/ARP4754B "Certification considerations for highly-integrated or complex aircraft systems" System level Airworthiness Regulation Requirements Certification Specifications (EASA) / Federal Airworthiness Requirements (FAR) Recommended practices for system development and safety assessment ED-80/DO-254 "Design assurance guidance for airborne electronic hardware" ED-12C/DO-178C "Software considerations in airborne systems and equipment"

**Figure 2.** 2: Figure 2.2: Airworthiness regulation requirements and recognized means of compliance.

**Figure 2.** 4: Figure 2.4: ACAS-Xu system architecture overview. Adapted from [45].

**Figure 2.** 5: Figure 2.5: LeNet-5 distributed into multiple hardware items. Retrieved from [76].

**Figure 2.** 6: Figure 2.6: Building blocks of the EASA AI roadmap trustworthiness. Excerpt from [5].

[figure sans légende identifiée] .7.

**Figure 2.** 7: W-shaped learning assurance process. The dotted line makes the distinction between the use of traditional development assurance processes, in the upper part, and the adapted development process applied to AI approaches, in the bottom part. Excerpt from [5].

**Figure 2.** Figure 2. 8: Figure 2.8 details our approach of the "model implementation" block of Figure 2.7 and the associated objectives are described hereafter:

**Figure 2.** 9: Figure 2.9: Distribution of execution times of a program (or task) on a processor. Excerpt from [185].

**Figure 2** Figure 2. 10: Figure 2.10: Generic workflow of the static WCET analysis of a program.

**Figure 3** Figure 3. 1: Figure 3.1: Workflow for converting Keras model to C code with Keras2c. Adapted from [42].

Listing 3: Calls to the generic k2c dense function in the C code of the ACAS-Xu decr128 inference model (Example 4.6.1) generated by Keras2c.

**Figure 3.** Figure 3. 2: Figure 3.2: Workflow for converting an inference model to C code with Static microTVM. Adapted from [160].

Listing 4: Initialization of the first layer parameters in the C code of the ACAS-Xu decr128 inference model (Example 4.6.1) generated by Static microTVM. // Call to layers' functions int32_t tvmgen_default_fused_nn_contrib_dense_pack_add_nn_relu(void *, void*); int32_t tvmgen_default_fused_nn_contrib_dense_pack_add_nn_relu_1(void *, void*); int32_t tvmgen_default_fused_nn_contrib_dense_pack_add_nn_relu_2(void *, void*); int32_t tvmgen_default_fused_nn_contrib_dense_pack_add_nn_relu_3(void *, void*); int32_t tvmgen_default_fused_nn_contrib_dense_pack_add_nn_relu_4(void *, void*); int32_t tvmgen_default_fused_nn_contrib_dense_pack_add(void *, void*); // Initialize inference run void TVMWrap_Run() { TVMValue args[4]; int32_t arg_type_ids[4]; DLTensor dlargs[4]; for (int i = 0; i < 4; i++) { args[i].v_handle = &dlargs[i]; } dlargs[0].data = (void*)&g_storage_0[0]; dlargs[1].data = (void*)&g_storage_1[0]; dlargs[2].data = (void*)&g_storage_2[0]; dlargs[3].data = (void*)&g_storage_3[0]; if (tvmgen_default_fused_nn_contrib_dense_pack_add_nn_relu(args, arg_type_ids) != 0) { TVMPlatformAbort(kTvmErrorPlatformCheckFailure); } ...} Listing 5: Calls to the specific dense layers functions of the ACAS-Xu decr128 inference model (Example 4.6.1) in the C code generated by Static microTVM.

Listing 6: Initialization of memory allocation functions in the C code of the ACAS-Xu decr128 inference model (Example 4.6.1) generated by Static microTVM.

2 Figure 4. 1: Figure 4.1: An example of feed-forward deep neural network represented as a directed acyclic graph.

**Figure 4.** 2:Example 5 ( Figure 4.2: An example of an single-path feed-forward deep neural network.

**Figure 4.** 3: Figure 4.3: The workflow for a semantically correct implementation of the inference model.

**Figure 4.** 4: Figure 4.4: An example of a 1D tensor with dimension n l .

**Figure 4.** 5:Figure 4. 6: Figure 4.5: An example of a 2D tensor with dimensions pn h , n w q.

**Figure 4.** 7: Figure 4.7: ReLU function

**Figure 4.** 8: Figure 4.8: Sigmoid function

**Figure 4.** 9: Figure 4.9: Hyperbolic tangent function

**Figure 4.** 10: Identity function

(4. 11 ) 20 ( Definition Flatten layer associated function). Let I be a 3D input tensor. The flatten layer associated function transforms I in a 1D output tensor O. The flatten layer associated function is defined as:

**Figure 4.** 11: Figure 4.11: Illustration of the flattening function applied to a 3D tensor with dimensions n h ˆnw ˆnc .

**Figure 4.** 13: Figure 4.13: Example of application of the 2D Max-pooling layer associated function.

**Figure 4.** 14 shows the average-pooling operation applied to the same tensor I of Example 11. Likewise, the size of the pooling window and the stride employed do not change: k h " k w " 2 and s h " s w " 2.

**Figure 4.** 14: Figure 4.14: Example of application of the 2D Average-pooling layer associated function.

**Figure 4.** 15: Figure 4.15: Illustration of the 2D convolution operation.

35 ) 14 ( Example Concatenation layer associated function).

**Figure 4.** 16 depicts the concatenation layer associated function. In this example tensor I has dimensions of size n h I " 3, n w I " 3 and n c I " 3 and tensor J has dimensions of size n h J " 4, n w J " 3 and n c J " 3. Concatenation is performed along the first dimension (dim c " 1). As a consequence, tensor O, result of the concatenation, has dimensions of size o h " 7, o w " 3 and o c " 3.

**Figure 4.** 16: Figure 4.16: Illustration of the concatenation of tensors I and J along the first dimension (n h ).

[figure sans légende identifiée] TensorFlow padding strategy: from the right bottom of the multi-dimensional array.

[figure sans légende identifiée] PyTorch padding strategy: from the left top of the multi-dimensional array.

**Figure 4.** 17: Figure 4.17: Illustration of the two different padding strategies of TensorFlow and PyTorch.

**Figure 4.** 18: Ownship, intruder and sensor measurements of the ACAS-Xu system. From [39].

**Figure 4.** 19: ACAS-Xu reg50 model.

**Figure 4.** 20: LeNet-5 model.

**Figure 4.** 21: Figure 4.21: CifarNet model.

**Figure 4.** 22: Figure 4.22: AlexNet model.

**Figure 4.** 23: VGG-16 model.

**Figure 4.** 24: Figure 4.24: Structure of the fire module, f f ire1 , introduced in SqueezeNet.

**Figure 4.** 25: Figure 4.25: SqueezeNet model.

**Figure 4.** 26: Figure 4.26: AudioNet model.

**Figure 4.** 27: Figure 4.27: Time series model.

Listing 7: Description of the first 2D Convolutional layer of LeNet-5 model (4.6.2) in the JSON-based file generated by Keras' model to json method.

Listing 8: Description of the first 2D Convolutional layer of LeNet-5 model (4.6.2) in the JSON-based file adapted for usage in ACETONE.

**Figure 5.** 1: Figure 5.1: The workflow for C code generation from an inference model description within ACETONE.

**Figure 5.** 2: Figure 5.2: Software architecture of ACETONE.

**Figure 5.** Figure 5. 3: Figure 5.3: Software architecture of the Layer abstract class and derived layers classes.

int Dense(int layer_idx, float *input, float *output) { float dotproduct; for (int i = 0; i < Net[layer_idx].layer_size; ++i){ dotproduct = 0; for (int j = 0; j < Net[layer_idx-1].layer_size; ++j) dotproduct += input[j] * (Net[layer_idx].weights[(j*Net[layer_idx].layer_size+i)]); dotproduct += Net[layer_idx].biases[i]; output[i] = Net[layer_idx].actv_function(dotproduct); // Function pointer } return 0; } Listing 11: Implementation of the Dense layer produced by the gen_inf_code_layer method of the Dense Layer class in V1 back-end (part of layers.c file). The gen_inf_code_global method of the V1 back-end generates the following C files: (i) layers.h: regrouping the functions' declarations of each type of layer present in the model; (ii) layers.c: regrouping the generic implementations of each type of layer present in the model; (iii) global_vars.c: containing the array of Layer structures, as well as the layers' trainable parameters; (iv) inference.h: presenting the generic declaration of the inference function; (v) inference.c: presenting the generic implementation of the inference function.

# include "inference.h" #include "layers.h" const float weights_Conv2D_01[150] = {-0.020271836, -0.29244548, 0.08360002, ...}; const float biases_Conv2D_01[6] = {-0.16464536, -0.026044395, -0.09863532, ...}; const float weights_Conv2D_03[2400] = {-0.04673595, 0.06358988, 0.19858478, ...}; const float biases_Conv2D_03[16] = {-0.025278127, 0.0104684625, 0.104660794, ...}; const float weights_Dense_05[30720] = {-0.14233316, 0.07173901, -0.08474024, ...}; const float biases_Dense_05[120] = {0.0010618381, -0.12174861, 0.14331335, ...}; const float weights_Dense_06[10080] = {0.18415198, 0.032971565, 0.00037049406, ...}; const float biases_Dense_06[84] = {-0.111380026, -0.0815005, 0.054556172, ...}; const float weights_Dense_07[840] = {0.17784193, -0.394412, -0.3273609, ...}; const float biases_Dense_07[10] = {-0.06807846, 0.103152454, 0.07741842, ...}; ... Listing 12: Example of the first part of the global_vars.c file generated within the V1 back-end for the LeNet-5 model (Example 4.6.2).

}Listing 16: int inference(float output_tensor[10], float input_tensor[784]) { static float output_previous[3456], output_current[3456]; // 3456 = maximum layer size in this network static float dotproduct, sum, max; static int count; // Input_layer_0 for (int i = 0; i < 784; ++i) output_previous[i] = input_tensor[i]; // Conv2D_01 layer implementation for (int f = 0; f < 6; ++f){ for (int i = 0; i < 24; ++i){ for (int j = 0; j < 24; ++j){ sum = 0; for (int c = 0; c < 1; ++c){ for (int m = 0; m < 5; ++m){ for (int n = 0; n < 5; ++n){ int ii = i*1 + m*1 -0; int jj = j*1 + n*1 -0; if (ii >= 0 && ii < 28 && jj >= 0 && jj < 28) sum += output_previous[(ii*28+jj)*1+c] * weights_Conv2D_01[((m*5+n)*1+c)*6+f]; } } } sum += biases_Conv2D_01[f]; output_current[(i*24 + j)*6 + f] = (exp(sum)-exp(-sum))/(exp(sum)+exp(-sum)); result to next layer --block present after each intermediate layer for (int k = 0; k < 3456; ++k) // Maximum 'layer size' of the model is here output_previous[k] = output_current[k]; for (int k = 0; k < 10; ++k) output_tensor[k] = output_current[k]; // Output of inference function return 0; Example of the inference.c file for LeNet-5 model within the back-end V2 back-end. it follows the same principle of the code depicted in Listing 16, i.e. an inference function without function calls.

**Figure 5.** 4:Definition 29 ( Figure 5.4: Memory layout of a C program.

[figure sans légende identifiée] Channels-last data layout.

**Figure 5.** 5: Figure 5.5: Illustration of two different data layout of 3D tensors.

**Figure 6.** 1: Figure 6.1: Example of input matrices for a GEMM-based convolution algorithm, considering a stride of one and no zero-padding. Matrix A corresponds to the convolutional kernels tensor conventionally flattened and matrix B corresponds to the matrix of patches, created by copying and arranging elements of the original input tensor.

[figure sans légende identifiée] Column-major data layout.

**Figure 6.** 2: Figure 6.2: Illustration of two different data layout of 2D tensors.

**Figure 6.** 3: Figure 6.3: Comparison between average execution time of GEMM-based and direct convolution algorithms.

**Figure 6.** 5: Figure 6.5: Comparison between average execution time of standard GEMM-based, direct and indirect GEMM-based convolution algorithms.

**Figure 6.** 6: Figure 6.6: Software architecture of the Conv2D abstract class and derived convolutional layers classes.

**Figure 6.** 7: Figure 6.7: Partitioning of matrices A, B and C into submatrices to perform a blocked GEMM routine.

**Figure 6.** 8:+=Figure 6. 9: Figure 6.8: Actual implemented order of partitioning of matrices A, B and C in Algorithm 3.

**Figure 6.** 10: Figure 6.10: Result of the packing routines to create copy blocks Ãc and Bc .

**Figure 6.** 11: Figure 6.11: Comparison of an add scalar and vector instructions.

**Figure 6.** 12: Figure 6.12: Data movement in Algorithm 3. Adapted from[129].

**Figure 6.** 13: Figure 6.13: Inefficient assembly translation of the vld1q_lane_f32 NEON intrinsic function generated by the GCC compiler with -O0 flag.

**Figure 6.** 14: Figure 6.14: Example of placement of a memory block in a 2-way set-associative cache.

Theorem 1. Let b, n P N. If n is odd, then the cache blocks of indices b, b `n, b `2 ¨n, . . . , b `ps Li ´1q ¨n are all mapped to different cache sets.

**Figure 6.** 15: Figure 6.15: Mapping matrix M to a data cache.

**Figure 6.** 15 provides an illustration for the discussion of Corollary 1. We introduce a running numerical example to facilitate the discussion of the following sections on the time-predictability of the GEMM algorithm with respect to the data cache.

**Figure 6.** 16: Figure 6.16: Mapping rows of matrix B (B c ) and Bc to cache blocks. The rows of a block B c read during packing are not mapped into contiguous cache sets. In contrast, the different micro-panels B r of Bc are stored in sequence.

[figure sans légende identifiée] , packing the three B c blocks results in 34, 848 L1D cache misses.

**Figure 6.** 17: Figure 6.17: Illustration of the packing B c routine for Example 21.

**Figure 6.** 18: Figure 6.18: Potential mapping of micro-tiles C r , micro-panels B r and A r in cache sets. B r becomes the least recently used because of A r and is evicted by C r .

**Figure 6.** 19: Figure 6.19: Potential mapping of micro-tiles C r , micro-panels B r and A r in cache sets. B r becomes the least recently used because of C r and is evicted by A r .

**Figure 6.** 20: Figure 6.20: Potential mapping of micro-tiles C r , micro-panels B r and A r in cache sets. C r is evicted because both A r and B r were mapped to the same cache sets.

[figure sans légende identifiée] C r load a block in one cache way of each set once, which leads to an upper bound of: obtain the upper bound on the total number of cache misses in the macro-kernel one must sum up all the previous equations for the misses due to reading C r , A r , B r and writing C r , and multiply the sum byQ nc nr

Figure A. 1: Figure A.1: Cycle de développement en W pour files systèmes basés sur l'apprentissage automatique. Adapté de [5].

Figure A. 2: Figure A.2: Approche adoptée pour l'implantation du modèle d'inférence tenant compte de la certification.

Figure A. 3: Figure A.3: Le flux de travail pour une implantation sémantiquement correcte du modèle d'inférence.

Figure A. 4:A. 2. 4 Figure A.4: Illustration de la fonction associée à la couche Dense.

Figure A. 5:Figure A. 6: Figure A.5: Le flux de travail pour la génération de code C à partir d'une description de modèle d'inférence dans ACETONE. Comme indiqué, ACETONE est écrit en Python. Les constituants du framework mentionnés ci-dessus sont en pratique des classes Python. Nous avons donc formalisé l'architecture logicielle d'ACETONE sous la forme d'un diagramme de classes UML, représenté dans la Figure A.6. En ce qui concerne le back-end d'ACETONE, nous avons mené une exploration de l'espace de conception (DSE) et proposé trois versions différentes, appelées back-end V1 , back-end V2 et back-end V3. Comme nous l'avons mentionné, files différentes versions correspondent à des stratégies de génération de code distinctes, car nous avons mené une étude empirique sur files perspectives des différentes stratégies. L'architecture logicielle

Figure A. 7: Figure A.7: Exemple de matrices d'entrée pour un algorithme de convolution basé sur GEMM, en considérant un pas de un et sans rajout de zéros (zero-padding). La matrice A correspond au tenseur des noyaux de convolution commodément aplati et la matrice B correspond à la matrice de patchs, créée en copiant et en arrangeant files éléments du tenseur d'entrée original.

Journals • [51] Iryna De Albuquerque Silva, Thomas Carle, Adrien Gauffriau and Claire Pagetti. Extending a predictable machine learning framework with efficient GEMM-based convolution routines. In Real-Time Syst. 59, 3, 408-437, August 2023. DOI: https://doi.org/10.1007/s11241-023-09407-z Iryna De Albuquerque Silva, Thomas Carle, Adrien Gauffriau and Claire Pagetti. ACETONE: Predictable Programming Framework for ML Applications in Safety-Critical Systems. In Proceedings of the 24th Euromicro Conference on Real-Time Systems (ECRTS 2022), Jun 2022. DOI: https://doi.org/10.4230/DARTS.8.1.6 • [49] Iryna De Albuquerque Silva, Thomas Carle, Adrien Gauffriau, Victor Jegu and Claire Pagetti. A predictable SIMD library for GEMM routines. In Proceedings of the 30th IEEE Real-Time and Embedded Technology and Applications Symposium (RTAS 2024), May 2024.

    Chapter 2
    International conferences
    • [157] Part I
    Background

[figure sans légende identifiée] Listing 1: Initialization of the first layer parameters in the C code of the ACAS-Xu decr128 inference model (Example 4.6.1) generated by Keras2c.

    # include <math.h>
    # include <string.h>
    # include "k2c_include.h"
    # include "k2c_tensor_include.h"
    void acas_decr128(k2c_tensor* input_1_input, k2c_tensor* dense_5_output) {
    // Initialization of the first layer parameters
    float dense_output_array[128] = {0};
    k2c_tensor dense_output = {&dense_output_array[0],1,128,{128, 1, 1, 1, 1}};
    float dense_kernel_array[640] = {+1.37222648e-01,-1.17803089e-01...};
    k2c_tensor dense_kernel = {&dense_kernel_array[0],2,640,{ 5,128, 1, 1, 1}};
    float dense_bias_array[128] = {+6.82496652e-03,+1.25179347e-03...};
    k2c_tensor dense_bias = {&dense_bias_array[0],1,128,{128, 1, 1, 1, 1}};
    ...}

[figure sans légende identifiée] ArgInfo inArgInfo[] = {{&g_storage_0[0],20}, }; // Input array of first layer static const ArgInfo outArgInfo[] = {{&g_storage_15[0],20}, }; // Output array of last layer void *TVMWrap_GetInputPtr(int index){

    ...
    // Initialize wrapper for inference function
    void TVMWrap_Init(){
    StackMemoryManager_Init(&g_workspace, g_workspace_buf, WORKSPACE_SIZE);
    }
    static const return inArgInfo[index].buffer;
    }
    size_t TVMWrap_GetInputSize(int index){
    return inArgInfo[index].size;
    }
    void *TVMWrap_GetOutputPtr(int index){
    return outArgInfo[index].buffer;
    }
    size_t TVMWrap_GetOutputSize(int index){
    return outArgInfo[index].size;
    }
    void

[figure sans légende identifiée] Example 13 (2D Convolutional layer associated function). Figure4.15 depicts the 2D Convolutional layer associated function applied to a 3D input tensor. In this example we have the input tensor I with dimensions of size n h " 7, n w " 7 and n c " 3. Tensor K has n k " 4 convolutional kernels. Each convolutional kernel K j has dimensions of size f h " 3, f w " 3 and f c " 3. Moreover, each kernel is applied with equal vertical and horizontal unitary strides: s h " s w " 1. Therefore, the output tensor O has dimensions of size o h "

    X 7´1 1 | `1\ " 5, o w " | X 7´3 1 | `1\ " 5 and o c " 4.
    From Figure |  |  | 

[figure sans légende identifiée] Note that the 2D zero-padding must also satisfy p t `pb ´fh " ´1 and p l `pr ´fw " ´1.

    n h "t | n h `pt `pb ´fh s h | `1u | (4.36)
    n w "t | n w `pl `pr ´fw s w | `1u | (4.37)
    Example 15 (Well-balanced 2D Convolutional layers). The 2D zero-padding layer is a pre-processing
    usually applied before 2D Convolutional layers, but it is occasionally encountered preceding 2D Pooling

[figure sans légende identifiée] Note that in extended 2D Convolutional layers, the biases tensor B usually has a constant value for a given channel dimension, i.e. B i 1x ,i 2y ,i 3 " B i 1m ,i 2n ,i 3 wherein i 1x ‰ i 1m and i 2y ‰ i 2n .Property 3 (2D Max-pooling layer and ReLU activation layer). Applying a ReLU activation layer before a 2D Max-pooling layer is semantically equivalent to applying a ReLU activation layer after 2D Maxpooling layer. However, having the ReLU activation layer after the 2D Max-pooling layer reduces the number of operations to be performed if either the vertical or the horizontal pooling stride are superior to one, i.e. s h ą 1 or s w ą 1.

    Property 2 (Extended 2D Convolutional layers). In machine learning frameworks, 2D Convolutional lay-
    ers usually integrate additional parameters than those listed in Definition 26. Indeed, a 2D Convolutional
    layer is often defined together with a 2D zero-padding layer (Definition 19), an activation layer (Def-
    inition 14) and a biases layer (Definition 21). We thus denote the extended 2D Convolutional layers
    by: | 
    C extd p,K,s,B,f " A f ˝BB ˝CK,s ˝Pp | (4.38)

[figure sans légende identifiée] in 2014. It is used for image recognition and similarly to AlexNet was presented in an ImageNet challenge, achieving 92.7% top-5 test accuracy on this dataset. The top-5 accuracy measures if any of the five highest probabilities provided by the prediction model matches the ground-truth label. This model is also classified as a very deep model, with sixteen layers containing trainable parameters: both of 2D Convolutional and Dense types. In addition, it has five 2D Pooling layers, and fifteen ReLU activation layers, as shown in Figure 4.23.

[figure sans légende identifiée] It produces for example the main C function and a Makefile. The C project contains everything needed to perform inference, including a test dataset, which may be either user-provided or randomly generated. All of ACETONE's content presented in next sections is open-source and available at ONERA's github page under a tag named 2022-ECRTS 1 .

    Inference model description (JSON-based file) | ACETONE front-end | Inference model structure + parameters (Python objects) | ACETONE back-end | Inference function implementation (C source code) | ACETONE aggregator | Inference model implementation (C project)
     |  | ACETONE |  |  |  | 
     |  | IR |  |  |  | 

**Table 5.** 

**Table 5.** 

    -Xu | ACAS-Xu
    decr128 | decr256

**Table 5.** 3: Results for the semantics preservation assessment of convolutional models in FP32 precision.

**Table 5.** 4: Results for the semantics preservation assessment in FP64 precision.

    Maximum error

**Table 5.** 

    Framework | Model ACAS-Xu reg50 | ACAS-Xu reg100 | ACAS-Xu reg200 | ACAS-Xu decr128 | ACAS-Xu decr256 | LeNet-5 | CifarNet | AudioNet | TimeSeries
    ACETONE (V1) | 8 025 404 21 288 195 84 655 395 26 092 073 121 206 406 6 881 827 044 121 680 131 609 54 600 562 334 | 165 902 238
    ACETONE (V2) | 5 617 830 13 971 737 55 122 437 6 128 253 24 461 227 | 121 832 112 | 617 483 465 2 138 965 680 | 8 170 861
    Keras2c |  | 5 033 535 19 692 951 79 383 490 36 838 054 112 237 358 1 160 385 934 33 913 150 451 3 260 034 878 46 645 295 230
    Static microTVM | 4 008 298 15 711 232 58 832 502 6 765 413 27 015 092 | 113 449 651 | 997 882 377 2 178 743 225 | 4 299 639

**Table 5.** 

Size of memory segments [bytes]

    Framework | stack | data | bss | text | total
    ACETONE (V1) | 240 | 3 472 | 712 | 176 124 | 180 548
    ACETONE (V2) | 148 | 2 784 | 712 | 177 820 | 181 464
    ACETONE (V3) | 72 | 2 784 | 712 | 953 732 | 957 300
    Keras2c | 129 280 | 2 816 | 312 | 423 352 | 555 760
    Static microTVM | 210 | 2 784 | 824 | 180 620 | 184 438

**Table 5.** 7: Memory layout of the executable generated for ACAS-Xu reg50.

[figure sans légende identifiée] 1) wherein, f h , f w and n c correspond, respectively, to the convolutional filter height, width and channel dimensions. And o h , o w and o c represent, respectively, the output tensor height, width and channel dimensions. In contrast, for a Dense layer the number of floating-point operations is computed as follows: wherein n i corresponds to the length of the input tensor and n o represents the length of the output tensor. Let us consider one 2D Convolutional and one Dense layer of the LeNet-5 (Example 4.6.2) inference model. The selected 2D Convolutional layer corresponds to the first one of this type in the model. It has 150 trainable weights and the following configuration:

    2 ¨ni ¨no | (6.2)

Algorithm 1: Direct convolution algorithmParameters: n k , f h , fw, fc, s h , sw Input: Input tensor I, Kernels tensor K Output: Output tensor O for i3 " 1 to n Oi 1 ,i 2 ,i 3 `" K m,n,l,i 3 ¨Is h ¨pi 1 ´1q`m,sw ¨pi 2 ´1q`n,l

**Table 6.** 

    Framework | Model | LeNet-5 | CifarNet | AudioNet | TimeSeries
    ACETONE direct convolution | 121 832 112 | 617 483 465 | 2 138 965 680 | 8 170 861
    ACETONE standard GEMM_NN | 110 725 811 | 403 192 446 | 1 403 775 479 | 6 703 008
    ACETONE standard GEMM_NT | 109 745 297 | 299 646 957 | 1 023 605 044 | 5 693 944
    ACETONE indirect GEMM_NN | 108 054 355 | 393 630 348 | 1 377 599 430 | 5 404 820
    ACETONE indirect GEMM_NT | 104 701 978 | 289 307 084 | 1 007 460 909 | 4 381 980
    Static microTVM |  | 113 449 651 | 997 882 377 | 2 178 743 225 | 4 299 639
    Keras2c |  | 1 160 385 934 | 33 913 150 451 | 3 260 034 878 | 46 645 295 230

**Table 6.** 3: Average, minimum, maximum, and standard deviation values for measured execution times (50 executions) on an ARM Cortex-A15 with -O0 flag.

    Model |  | LeNet-5 | CifarNet | AudioNet | TimeSeries
     | avg | 12 703 056 | 242 876 559 | 594 530 189 | 1 904
    ACETONE direct convolution | min max | 12 702 928 12 704 161 | 242 875 774 242 877 227 | 594 033 534 595 796 878 | 1 904 1 918
     | std dev | 182 | 199 | 144 771 | 1
     | avg | 10 413 463 | 107 685 957 | 373 666 343 | 2 359
    ACETONE standard GEMM_NN | min max | 10 413 175 10 413 595 | 107 673 640 107 948 273 | 373 431 005 374 130 784 | 2 358 2 380
     | std dev | 61 | 26 621 | 80 670 | 2
     | avg | 7 846 088 | 86 432 662 | 293 342 053 | 1 623
    ACETONE standard GEMM_NT | min max | 7 845 879 7 847 155 | 86 429 874 86 623 575 | 293 028 691 293 806 837 | 1 623 1 636
     | std dev | 213 | 19 188 | 62 906 | 1
     | avg | 10 170 036 | 101 310 891 | 339 604 963 | 1 883
    ACETONE indirect GEMM_NN | min max | 10 169 742 10 189 748 | 101 302 717 101 622 125 | 339 429 572 340 121 039 | 1 883 1 888
     | std dev | 2 027 | 31 354 | 84 270 | 
     | avg | 7 693 964 | 77 525 969 | 268 068 119 | 1 153
    ACETONE indirect GEMM_NT | min max | 7 693 575 7 694 248 | 77 524 834 77 530 350 | 267 927 035 268 654 573 | 1 153 1 154
     | std dev | 73 | 663 | 95 841 | 
     | avg | 10 178 445 | 193 599 362 | 744 591 139 | 1 267
    Static microTVM | min max | 10 178 413 10 179 534 | 193 563 415 193 833 073 | 741 476 588 748 143 911 | 1 266 1 267
     | std dev | 135 | 42 230 | 2 671 191 | 
     | avg | 25 767 758 | 642 390 830 | 1 542 805 783 | 5 360
    Keras2c | min max | 25 767 366 25 768 707 | 642 345 451 643 387 595 | 1 525 852 550 1 545 161 133 | 5 360 5 378
     | std dev | 216 | 144 170 | 1 925 150 | 1

**Table 6.** Column panel Submatrix comprising all rows but only a subset of consecutive columns from the original matrix Row panel Submatrix comprising all columns but only a subset of consecutive rows from the original matrix Block Submatrix comprising only a subset of consecutive rows and columns from the original matrix 5: Notation used on the study of blocked GEMM algorithm.

    Notation | Description | 
    Copy block | A matrix block that has been rearranged for linear access
    Micro-panel | Small panels present in a copy block, tailored for registers
    Micro-tile | Small block of C c , tailored for registers
    A c | Block of matrix A of shape m c ˆkc | 
    B c | Block of matrix B of shape k c ˆnc | 
    C c | Block of matrix C of shape m c ˆnc | 
    Ãc | Block A c after packing, of shape m c ˆkc
    Bc | Block B c after packing, of shape k c ˆnc
    A r | Micro-panel, included in Ãc | 
    B r | Micro-panel, included in Bc | 
    C r | Micro-tile, included in C c | 
     | micro-tile | micro-panel | micro-panel
     | block | block | block
     |  | row-panel | column-panel

**Table 6.** 6: Measured execution times, in cycles, on an ARM Cortex-A15 with -O0 flag. Difference w.r.t. Base is given in parentheses.

**Table 6.** 7: Measured average execution times, in cycles, on an ARM Cortex-A15 with -O0 flag.

**Table 6.** 8: WCET bounds produced by OTAWA for the different convolution algorithms and various Convolutional layer configurations.

[figure sans légende identifiée] It implies log 2 p256q " 8 index bits. Finally, there are log 2

    32KB 64B¨2 " 256. ´mem size ¨wL1 size L1 | size L1 c L1 ¨wL1 " ¯" 17 tag bits. A
    cache block, initially present in a main memory line, is mapped to a cache set according to the expression:
    y " x mod s Li | (6.14)

[figure sans légende identifiée] Ar0s from A c , a new cache block is loaded to, let us assume, set #5. Writing Ar0s to Ãc loads a cache block to, again hypothetically, set #1. Since k X L1 " 33, for the reading of element Ar528s, a cache block is loaded to set #p5 `33q mod 256 " 38, and this element is written to the cache block present in set #1. Elements Ar1056s and Ar1584s are read from sets #p5 `66q mod 256 " 71 and #p5 `99q mod 256 " 104, respectively. Both are written to set #1.

    Illustrating this logic with Example 21, we have that the first micro-panel of A c contains elements:
     | Ar0s, Ar528s, Ar1056s, Ar1584s;
     | Ar1s, Ar529s, Ar1057s, Ar1585s;
     | ...; |  |  | 
     | Ar255s, Ar783s, Ar1311s, Ar1839s
    While reading element |  |  |  |  | 
     |  |  |  |  |  | .21)
    To write one micro-panel in Ãc , | Q | mr¨kc X L1 | U |  | cache blocks are needed (Notation N.5). We thus have, for
    one micro-panel, a bound of: |  |  |  |  | 
     |  |  |  | R | m r ¨kc X L1 | V | misses. | (6.22)
    Consequently, to write the whole Ãc block (Notation N.6), we find:
     |  | R | m c m r | V | ¨R m r ¨kc X L1 | V | misses.

[figure sans légende identifiée] " 256 and once with k c " 16. Hence, the total of memory accesses in the macro-kernel function in this example is 20, 072, 448.To reason about the L1D misses in the macro-kernel, we add the following assumption: This property derives from Corollary 1 and potential padding of C to achieve Assumption A.2. Because in our study m r " n r , micro-panels A r and B r occupy the same number of cache blocks, i.e.

     |  |  |  |  |  |  |  | 7,
    there are: |  |  |  | R | m c m r | V | ¨R n c n r | V | ¨p2 ¨kc `2 ¨mr ¨nr q | (6.23)
    memory accesses in the macro-kernel function.
    In Example 21, we have | R | m c m r | V | ¨R n c n r | V | " 17, 424. The macro-kernel is also called three times: twice
    with k c ‚ C is aligned to a cache block boundary. | (A.8)
    Besides, let us recall some properties of the submatrices involved in the macro-kernel:
    Property 9. Q mr¨kc |  |  |  |  |  |  | 
    X L1 |  |  |  |  |  |  | 

6.5.6.2.1 Upper bound on cache misses due to reading Cr Cr0s is mapped to cache set #0, we know that element Cr528s is mapped to cache set #p0 `33q mod 256 " 33. Likewise, element Cr1056s is mapped to cache set #p0 `66q mod 256 " 66 and element Cr1584s is mapped to cache set #p0 `99q mod 256 " 99. Reading C rp0q , incurs 4 cache misses. Hence, to read the

    6.5.6.2. |  |  |  | 
     |  |  |  |  | Q | mc mr | U | micro-tiles are updated,
    leading to: |  |  |  | 
     |  |  | R | m c m r | V | ¨mr misses. | (6.24)
    Let us consider the first micro-tile in Figure 6.9, i.e. C rp0q . In the case of Example 21, this micro-tile
    is composed of the elements: |  |  | 
    Cr0s...Cr3s; Cr528s...Cr531s; Cr1056s...Cr1059s; Cr1584s...Cr1587s
    Assuming that element Q | mc mr | U | micro-tiles, there are 132 ¨4 " 528 cache misses.

2 Upper bound on cache misses due to reading Ar Applying the reasoning to Example 21, let us consider the first micro-panel, A rp0q . It contains 1, 024 elements. Its first element corresponds to Ãc r0s, which we assume is mapped to cache set #1. Since the elements within a micro-panel are placed in contiguous addresses in memory (Property 7), Ãc r16s is mapped to cache set #2, while Ãc r1023s is loaded to cache set #64. Reading micro-panel A rp0q causes 64 cache misses, and reading the

    A micro-panel A r occupies | Q | mr¨kc X L1 | U | cache blocks. For any given micro-panel B r , | Q | mc mr | U | micro-panels A r
    are read, leading to: |  |  |  |  |  |  |  | 
     |  |  |  |  |  |  | R | m c m r | V | ¨R m r ¨kc X L1 | V | misses. | (6.25)
     |  | Q | mc mr | U | needed micro-panels then generates 8, 448 cache misses.
    6.5.6.2. |  |  |  |  |  |  |  | 

3 Upper bound on cache misses due to reading Br With respect to the cache misses due to reading B r in the macro-kernel, we differentiate three cases. The first case corresponds to the misses caused by the initial reading of B r . Then, we consider extra misses due to reading B r again because it was unintentionally evicted, either by C r or by A r .

    i) Initial reading of B r |  | 
    A micro-panel B r occupies | Q | kc¨nr X L1 | U | cache blocks. As we focus on the lifetime of a micro-panel B r , for its
    initial loading in the cache we find: | 
     |  |  |  | R | k c ¨nr X L1 | V | misses. | (6.26)

[figure sans légende identifiée] .31)

    Matrix configuration |  | Memory accesses |  | L1D refill | 
    m | n | k |  | Ours | Low et al. | Ours | Low et al. | Theoretical
    (i) 272 | 272 | 272 | Packing B | 148 032 | 148 000 (-0.02%) | 9 253 | 10 612 (12.81%) | 9 254 (0.01%)
     |  |  | Packing A | 148 032 | 148 000 (-0.02%) | 9 252 | 9 251 (-0.01%) | 9 254 (0.02%)
     |  |  | Macro-kernel | 2 811 414 | 2 663 435 (-5.26%) | 333 950 | 347 307 (3.85%) | 384 886 (13.23%)
     |  |  | Total | 3 107 478 | 2 959 435 (-4.76%) | 352 455 | 367 170 (4.01%) | 403 394 (12.63%)
    (ii) 528 | 528 | 528 | Packing B | 557 664 | 557 632 (-0.01%) | 34 856 | 78 145 (55.40%) | 34 857 (0.00%)
     |  |  | Packing A | 557 664 | 557 632 (-0.01%) | 34 854 | 34 852 (-0.01%) | 34 857 (0.01%)
     |  |  | Macro-kernel 20 072 481 19 514 902 (-2.78%) | 2 552 600 2 509 309 (-1.73%) 2 703 897 (5.60%)
     |  |  | Total | 21 187 809 20 630 166 (-2.63%) | 2 622 310 2 622 306 (0.00%) 2 773 611 (5.46%)
    (iii) 256 | 784 | 2,016 ˚Packing B | 3 161 344 | 3 161 216 (0.00%) | 197 591 | 341 213 (42.09%) | 197 592 (0.00%)
     |  |  | Packing A | 1 032 448 | 1 032 320 (-0.01%) | 64 528 | 64 520 (-0.01%) | 64 536 (0.01%)
     |  |  | Macro-kernel 53 788 760 52 183 084 (-2.99%) | 6 894 927 6 766 186 (-1.90%) 7 217 528 (4.47%)
     |  |  | Total | 57 982 552 56 376 620 (-2.77%) | 7 157 046 7 171 919 (0.21%) 7 479 656 (4.31%)
    (iv) 192 | 736 ˚528 | Packing B | 777 312 | 777 248 (-0.01%) | 48 584 | 121 948 (60.16%) | 48 585 (0.00%)
     |  |  | Packing A | 202 848 | 202 784 (-0.03%) | 12 677 | 12 675 (-0.02%) | 12 681 (0.03%)
     |  |  | Macro-kernel 10 174 497 | 9 891 862 (-2.78%) | 1 248 905 1 258 791 (0.79%) 1 322 057 (5.53%)
    ˚Padding applied. |  | Total | 11 154 657 10 871 894 (-2.53%) | 1 310 166 1 393 414 (5.97%) 1 383 323 (5.29%)

**Table 6.** 10: Measures for the number of memory access and L1D refill of the GEMM routine.

**Table 6.** 11: Measured execution cycles, on an ARM Cortex-A15 with -O0 flag. Difference w.r.t. Low et al. is given in parentheses.

[figure sans légende identifiée] Throughout the manuscript, we have identified numerous potential enhancements for incorporation into ACETONE. In Chapter 5 we already discussed ongoing research activities at ONERA aimed at adding support for:(i) more formal inference model description formats, such as ONNX in view of the avionics profile under development; (ii) more complex inference model structures, i.e. with skip connections; (iii) more advanced types of layers, such as Broadcast, Resize and General padding.

[figure sans légende identifiée] Definition 32 (Fonction associée à la couche Dense). Soit I un tenseur d'entrée 1D de taille n i . Soit W un tenseur 2D de taille pn o , n i q, représentant files poids de la couche et B un tenseur 1D de taille n o , représentant files biais de la couche. La fonction associée à la couche Dense est une transformation linéaire définie comme suit :Dense W,B : Rn i Ñ R no W i 1 ,k .I k `Bi 1 (A.2) Example 23 (Fonction associée à la couche Dense). La Figure A.4 représente la fonction associée à la couche Dense. Nous observons le tenseur d'entrée I, de taille n i " 2. Nous notons également le tenseur des poids W, dont files dimensions sont de taille n o " 3 et n i " 2 et le tenseur des biais B, de taille n o " 3. Le tenseur de sortie O de taille n o " 3 est le résultat de la fonction associée à la couche Dense appliquée au tenseur I.

    I Þ Ñ O | (A.1)
    où O correspond au tenseur de sortie 1D. Chaque composante du tenseur O est définie comme suit :
    n i | 
    ÿ | 
    O i 1 " | 
    k"1 | 

3 Discussion des résultats de l'évaluation comparative 3. Nous avons donc évalué : (i) Critère 1: la préservation de la sémantique (Objectif 2); (ii) Critère 2: le temps d'exécution au pire cas (Objectif 4); (iii) Critère 3: le temps d'exécution moyen (Objectif 5); (iv) Critère 4: l'agencement de la mémoire des exécutables (Objectif 5). Dans la Section 5.3, nous détaillons chaque critère et expliquons comment ils sont évalués. En particulier, en ce qui concerne le Critère 2, nous souhaitons nous appuyer sur l'analyse statique pour dériver des limites supérieures pour le temps d'exécution au pire cas d'un modèle d'inférence. Pour ce faire, nous utilisons l'outil OTAWA [21]. Nous avons choisi OTAWA parce que l'outil est open-source et actuellement maintenu, et qu'il propose un large éventail de techniques en termes d'analyse. En ce qui concerne le Critère 3, nous avons mesuré files temps d'inférence sur un coeur ARM Cortex-A15, du SoC Keystone II de Texas Instruments [168].Après une comparaison approfondie, nous avons observé que files trois versions d'ACETONE répondent de manière satisfaisante au Critère 1. En ce qui concerne le Critère 2, OTAWA a été en mesure de produire des bornes de temps d'exécution au pire cas plus serrées pour back-end V2 par rapport à back-end V1 , alors qu'il n'a pas pu analyser le binaire de back-end V3 en raison des limitations de la mémoire. En outre, back-end V2 a démontré une légère supériorité à la fois dans le Critère 3 et le Critère 4. Nous avons donc conclu que, parmi files approches de génération de code proposées dans ACETONE, le back-end V2 offre un bon compromis entre la généralité et la personnalisation de la fonction d'inférence.

    A.2.4.
