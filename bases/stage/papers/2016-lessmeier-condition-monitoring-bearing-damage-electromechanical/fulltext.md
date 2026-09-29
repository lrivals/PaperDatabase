---
id: 2016-lessmeier-condition-monitoring-bearing-damage-electromechanical
title: "Condition Monitoring of Bearing Damage in Electromechanical Drive Systems by Using Motor Current Signals of Electric Motors: A Benchmark Data Set for Data-Driven Classification"
year: 2016
backend: grobid
---

## Abstract

This paper presents a benchmark data set for condition monitoring of rolling bearings in combination with an extensive description of the corresponding bearing damage, the data set generation by experiments and results of datadriven classifications used as a diagnostic method. The diagnostic method uses the motor current signal of an electromechanical drive system for bearing diagnostic. The advantage of this approach in general is that no additional sensors are required, as current measurements can be performed in existing frequency inverters. This will help to reduce the cost of future condition monitoring systems. A particular novelty of the present approach is the monitoring of damage in external bearings which are installed in the drive system but outside the electric motor. Nevertheless, the motor current signal is used as input for the detection of the damage. Moreover, a wide distribution of bearing damage is considered for the benchmark data set. The results of the classifications show that the motor current signal can be used to identify and classify bearing damage within the drive system. However, the classification accuracy is still low compared to classifications based on vibration signals. Further, dependency on properties of those bearing damage that were used for the generation of training data are observed, because training with data of artificially generated and real bearing damages lead to different accuracies. Altogether a verified and systematically generated data set is presented and published online for further research.

## 1. INTRODUCTION

According to statistics, 40-70% of electro-mechanic drive systems and motor failures are caused by rolling bearing damages, which can lead to high costs in applications because of downtimes (Bonnett & Yung, 2008;Djeddi, Granjon, & Leprettre, 2007). Thus, high-risk applications or those with high maintenance costs are continuously monitored. Detection of bearing damage is typically monitored by vibration analysis using acceleration sensors. These additional acceleration sensors are widely utilized, especially in large applications such as wind power turbines or cement mills. In industrial applications which use a great number of inexpensive small electric motors with an approximate power consumption of around 1 kW or less, the cost for additional sensors is financially not feasible. For this reason, several research projects focus on detecting bearing damage by using existing signals such as motor currents, which can be measured by the already existing frequency inverters. Researchers prefer data-driven classification methods that are based on machine learning algorithms to detect damage states by using the motor current signals (MCS). These methods are often examined in case studies of special applications and damages such as broken rotor bars or bearing damages. The condition monitoring (CM) methods based on MCS are still being investigated and not yet prevalent in industrial applications as they continue to have restrictions. (Bellini, Filippetti, Tassoni, & Capolino, 2008;Herold, Piantsop Mbo'o, & Hameyer, 2013;Paschke et al., 2013;Picot et al., 2014;Stack, Habetler, & Harley, 2003) For MCS-based methods, it has to be distinguished between bearing damage in the motor itself (internal bearings) and bearings in the remaining drive train (external bearings).

Damage of the internal motor bearings or other faults in the motor itself, as for example broken rotor bars or rotor eccentricity, directly influence the airgap of the motor and induce vibrations at characteristic frequencies in the motor current. Detection of damage in external bearings is more complex as the damage signature has to be transmitted indirectly through torque variations along the drive train. Therefore, it is damped and superimposed with disturbances from the powered process, leading to noisy and hard detectable signals. (Blödt, Granjon, Raison, & Rostaing, 2008;Herold et al., 2013;Schoen, Habetler, Kamran, & Bartfield, 1995). Schön et al. (1995) discuss both situations, damage in internal and external bearings, and derive formulas for the theoretically expected frequencies and sidebands in each situation. However, these frequencies can only be detected reliably in special cases because they are influenced by operating conditions, machine design, external noise etc. and have usually only been investigated for large scale damages. (Bellini et al., 2008;Mbo'o, Herold, & Hameyer, 2004). Hence, additional investigations are required.

It is assumed that good results for diagnostics can be achieved with data-driven classification methods using machine learning (ML) (Bellini et al., 2008;Kankar, Sharma, & Harsha, 2011;Paschke et al., 2013). The low availability of training and testing data with the MCS of external bearing for ML procedures limits further research, so that there is insufficient knowledge about the capability of industrial usage. To overcome this limitation, research has to address the systematic generation of training data with mechanical bearing damage. (Nectoux et al., 2012;Stack et al., 2003;Zarei & Poshtan, 2009) This results in two subjects of activity, which should be considered in more detail for the generation of training data: a systematic generation of the bearing damages themselves and their systematic specification.

In the industry, a wide variety of bearing damages occur. Especially the development of fatigue damages or damages caused by solid particles is randomly influenced; in addition, the appearance of damages can change over time. In the literature, six main damage modes and more than 20 different damage symptoms in bearings are treated. (ISO 15243, 2010;Bartz, 1985;Schaeffler Technologies AG & Co. KG, 2015) Recent research studies on CM address only some of these damages. Furthermore, many of the available research papers focus only on artificial bearing damages because these are easy to generate. (Pacas, Villwock, & Dietrich, 2009) Publications show that in most cases only single point damages are used for research, which inhibits the development of reliable CM systems based on MCS. (Bellini et al., 2008;Stack et al., 2003). Thus, it is no surprise that some authors report a high discrepancy between the proposed methods in science and their application in industry. Stack assumes that one reason for this discrepancy is the use of the simple artificial defects in the form of single point damages in research. For a more detailed consideration, bearing damage is nowadays separated into single point and distributed damage. (Nandi, Toliyat, & Li, 2005;Stack et al., 2003;Tandon & Choudhury, 1999) Single point damages are characterized by their small extend at a localized position, for example a crack or a small pit. When the rolling elements run across these defects, shock pulses stimulate vibrations at the characteristic bearing frequencies (Randall, 2011). Distributed damages, also called generalized roughness (Stack et al., 2003) or extended faults (Randall, 2011), induce broadband vibrations which are often not easy to separate from the noise of the signal. In general, these damages are caused by wear, corrosion or plastic deformation, but also by extensive pitting (fatigue) damages (Nandi et al., 2005). The authors of the present paper also observed the combination of different damage types in one bearing, which leads to superimposed signals for CM.

While the bearing damage signature of vibrations is well known, there is little experience with the MCS of external bearing damage and the correlation of the artificial damages used in research with real damages in the industry (Bellini et al., 2008). Especially for MCS-based condition monitoring, the authors of this paper think a more detailed description of damage is required as the separation into single point and distributed damage is not sufficient. Moreover, a precise description of specific test damages and test bearing specifications for experimental examinations are needed. Therefore, a systematic methodology is necessary to characterize the appearance of damage for CM, as existing methodologies are not very specific. Given the need for further research the present paper focuses on the systematic generation of training data for ML classification algorithms based on MCS.

To create a systematic data set, first a method for the systematic description of the rolling bearing damage is described (section 2). Afterwards, the generation of artificial and real bearing damages to be used for training data generation in the experiments (section 3) and the experimental set-up itself (section 4) are explained. Section 5 gives details on the database and their availability for further research.

To validate the data set and as a proof of concept for the general method, the paper points out some damage detection results as well. In section 6 the established method of envelope analysis is used to prove the proper data acquisition and to allow an initial evaluation of the bearing damages. Section 7 shows that machine learning classification algorithms are able to identify the damaged bearings in industrial drive trains using MSC, but require sophisticated training data, as classification accuracies differ depending on the training data sets. Therefore, the dependency of the classification results on different damage types and manifestations of damage is examined.

## 2. CATEGORIZATION OF BEARING DAMAGE

For systematic approaches of the examination of bearing damages, a comprehensive methodology for categorizing bearings and their specific damages is needed. The proper description and categorization of bearing damages and their cause is not an easy task as bearing damages occur as an interaction of different causes and conditions. Moreover, the patterns of damages may vary widely and often occur in combinations. Bearing damages can have different development states and not all of them lead to a sudden failure.

ISO 15243 gives a methodology for the classification of bearing damage and failures. The damages are categorized into six main damage modes and their sub-modes. The six main damage modes are: fatigue, wear, corrosion, electrical erosion, plastic deformation, and fracture and cracking.

This existing methodology of categorization is helpful to describe damages and to figure out their causes. Nevertheless, it only considers the damage modes in general and does not describe the detailed physiognomy of the damage.

The authors do not know of any extensive and established method to describe the physiognomy of bearing damages in detail. Therefore, a method for general categorization and detailed specification was developed. It focuses on the detailed description of the damage as well as on the corresponding bearing and its application. Description criteria were gathered using brainstorming methods and sorting them into a hierarchic structure of categories. The categories and criteria are shown in Table 1.

The criteria were grouped into four main categories, the first three giving information about the bearing and the fourth providing detailed information about the damage. According to these criteria, a detailed profile (or fact sheet) can be created for any damaged bearing.

The criteria of the first group "general info" name the bearing type and the standardized code according to the standards of each bearing series.

The criteria in the second group "manufacturer specific information" give information about the internal geometry and parameters of the bearing as these are not standardized. Consequently, these parameters differ from manufacturer to manufacturer. Especially for CM, these parameters may be important when model based approaches are used and, for example, the geometry is needed to calculate the characteristic frequencies. Criteria in the third category "application specific information" list the specific information of the individual bearing in the form of distinct identification codes and information concerning the place of operation and the corresponding operating conditions. This information is especially valuable to help figure out the damage causes in industry applications. Further on in this paper the four-digit code for each specific bearing is used for identification. It consists of two letters and two numbers, e.g. KA01, KB23.

The damage itself in the fourth group is described by its type and subtype according to ISO 15243 (2010), its As this paper focuses on CM of bearing damages, some of the most important criteria concerning the description of bearing damages for CM are explained in detail. For a better understanding, an example is given in the last column of Table 1.

Damage combination: This criterion characterizes the occurrence of combined or repetitive damage based on the damage symptoms. This is important for real damages which are not plain single point damages. It is described by the following three options:

 Single damage: One single component of the rolling bearing is affected by a single damage, for example a single pitting on the inner ring.

 Repetitive damage: Identical damage symptoms are repeated at several places on the same bearing component, for example several, non-continuous pittings on the inner ring raceway.

 Multiple damage: Different damage symptoms occur in the bearing or identical damage symptoms occur on different bearing components. This option can include repetitive damages. Arrangement of the repetitive and multiple damages: This criterion characterizes the arrangement of the damage symptoms on each component (e.g., the inner ring) for the repetitive and multiple damages (see above). This criterion is described by the following options:

 Regular: The damage symptoms recur in a regular pattern on the component.

 Random: Random distribution of the local damage symptoms.

 No repetition: The damage occurs only once and this criterion does not apply. Geometrical size: The geometrical size of the damage is described by the length, width, and depth of the damage, according to the directions quoted in VDI 3832 (2013) and depicted in Figure 1. Extent of damage: The extent of the damage describes the size of the damage in normalized levels, which are independent of the bearing size. The levels are based on the length of the damage, as this is a determining factor for the signal output in CM and the intensity of the damage from the point of view of a machine operator. For this the percentage of length relative to pitch circumference is calculated and then assigned to five levels according to Table 2.

Table 2. Damage levels to determine the extent of damage.

### Damage level

### Assigned percentage values

Limits for bearing 6203

1 0-2 % ≤ 2 mm 2 2-5 % >2 mm 3 5-15 % >4.5 mm 4 15-35 % >13.5 mm 5 >35% >31.5 mm

damage in industrial applications. Two groups of damages in ball bearings were used in the experiments: artificial and real damages. Both types of damage exist at the inner and outer ring of the ball bearing 6203. For this paper bearings of the manufacturers FAG, MTK and IBU/IBB are used. All these bearings have eight rolling elements and the geometrical sizes are nearly identical, so that the characteristic kinematic frequencies do not vary more than 1-2%.

Characteristic of damage: The characteristic of damage assigns the damages into the already mentioned groups of single point and distributed damages. For a clear and easy division between these groups the dividing value is set to the diameter of the rolling elements, to which the damage length is compared. This guarantees that for the single point defects only one rolling element has contact to the damage in all cases and the extent of the damage is small in comparison to the bearing size.

It should be noted that the appearance of the damages can have a simultaneous influence on several of the critera. Therefore the criteria are not independent. The dependency is tolerated in order to gain a detailed description of damages, due to the facts, that the damage diversity is high and the real phenomena intermix.

Altogether, this method of categorizing gives a very detailed description of the regarded bearings and their damages. The difficulty is to collect all the information and parameters, as some of them are not obvious and hard to obtain. The method was developed using a wide approach and can thus be used to investigate the damage causes or other bearing damage related issues as well.

## 3. GENERATION OF BEARING DAMAGE

A main focus of this research paper is to generate systematic data of measurement signals for condition monitoring with a broad variety of bearing damage. As an intermediate step, the bearing damages had to be generated, requiring a special damage preparation for the bearings.

To keep the amount of experiments manageable, research was limited to ball bearings of type 6203. The types of damage were processed and selected respecting the technical possibilities of their manufacturing and their The artificial damages were introduced manually using machining tools (see 3.1). For the generation of the real bearing damages an apparatus for accelerated lifetime tests was used (see 3.2).

### 3.1. Artificial Damage

The use of artificial damages to develop CM methods is very common, as reported in several research papers. Often rather extensive bearing damages such as holes in the outer race of the bearing are used. (Blödt et al., 2008;Nandi et al., 2005;Zarei & Poshtan, 2009) Some researchers use only outer ring damages, even though inner ring damages are more likely to occur because of the higher Hertzian stress. Furthermore, inner ring damage is not as easy to detect as outer ring damage because in most situations, the signal is disguised by a modulation because of the rotation of the inner ring. (Obaid, Habetler, & Stack, 2003;Pacas et al., 2009) Most commonly used methods for artificial damage preparation are:

 Trenches generated by electrical discharge machining (EDM). (Niknam, Thomas, Hines, & Sawhney, 2013), (Villwock, 2007;Yang, Mathew, & Ma, 2005;Zoubek, Villwock, & Pacas, 2008), (Niknam et al., 2013;Patil, Mathew, Rajendrakumar, & Desai, 2010)  Drilling holes into the rings: The bore diameter, the orientation, and the position depend on the bearing type and size. (Amirat, Choqueuse, & Benbouzid, 2013;Blödt et al., 2008;Djeddi et al., 2007;Silva & Cardoso, 2005;Zarei & Poshtan, 2009) The artificial damages used in this paper were caused by three different methods: 1. electric discharge machining (trench of 0.25 mm length in rolling direction and depth of 1-2 mm), 2. drilling (diameter: 0.9 mm, 2 mm, 3 mm), and 3. manual electric engraving (damage length from 1-4 mm). Table 3 shows three examples of damages caused by each of the three methods. The first two methods are very precise and easy to reproduce. Therefore, these artificial damages are appropriate for comparing research results with other studies. A lack of correlation to real bearing damage is assumed though, because a very abrupt and sharp transition between the damage and the undamaged raceway areas is apparent. To examine this correlation, the third type of artificial damage caused by a manual electric engraver is prepared, which has an irregular surface structure and lower depth, thus resembling real pitting damage. For the present research paper, ball bearings with real damages were obtained from an accelerated life time test.

The accelerated life time test rig consists of a bearing housing and an electric motor, which powers a shaft with four test bearings of type 6203 in the housing (Figure 2). The test bearings rotate under a radial load which is applied by a spring-screw mechanism. The applied radial force is higher than in usual bearing applications to accelerate the appearance of fatigue damages, but still low enough to not exceed the static load capacity of the bearing. Moreover, low viscosity oil was used, which leads to improper lubrication conditions and favors the appearance of damages.

Figure 2. Apparatus for accelerated life time test.

Several damaged bearings were obtained by the lifetime test and categorized according to the developed criteria (see section 2). 33 damages were recognized in 18 bearings out of a test amount of 108 bearings used in the lifetime test.

Around 70 % of the occurred damages were fatigue damages, which arise in the form of pittings. The rest of the bearings, except for one fracture, were damaged by plastic deformation, i.e. in the form of indentations caused by debris. Pitting damages occurred both on the inner and outer ring of the bearings. Indentations were found at the outer ring only. Damage at the rolling elements was not observed. The extent of the damage was categorized by the length of the damaged surface in rolling direction into the levels 1 to 3 (compare Table 2 andTable 5). Multiple damages were characterized according to the damage with the highest extent. the inner ring. For the experiments, representative samples with different properties were selected (see Table 5).

## 4. EXPERIMENTAL SET-UP

To generate the experimental data for the development of CM methods of damaged bearings by using motor current signals, a specific test rig was designed and operated at the Chair of Design and Drive Technology, Paderborn University. The test rig is a modular system to ensure flexible use of different defects in an electrical driven mechanical drive train. Defects in mechanical components, as they occur in gearboxes or electrical machines, are experimentally reproduced to generate failure data using the test rig. For the generation of the measurement data, the current signals of the electric motor are recorded.

Additionally, the vibration signal of the housing of the test bearings are measured as reference.

### 4.1. Test Rig

The test rig consists of several modules: an electric motor (1), a torque-measurement shaft (2), a rolling bearing test module (3), a flywheel (4) and a load motor (5), see (Lessmeier, Piantsop Mbo'o, Coenen, Zimmer, & Hameyer, 2012) Figure 5 shows the schema of the measurement procedure and the recorded measurands. The motor phase currents are measured by a current transducer of the type LEM CKSR 15-NP with an accuracy of 0.8 % of I PN = 15 A. The MCS are then filtered by a 25 kHz low-pass filter and converted from an analogue to a digital signal with a sampling rate of 64 kHz. The current transducers are used instead of the internal ammeters of the inverter because of their easy signal access as the currents can be measured externally between motor and inverter. At this scientific level of development, a high sampling rate and accuracy are additional advantages of this setup. Nevertheless, the used transducers are similar to the ones commonly used in industry applications, so that few difficulties are expected transferring the research outcomes to industrial CM systems.

The acceleration of the bearing housing is measured at the adapter at the top end of the rolling bearing module using a piezoelectric accelerometer (Model No. 336C04, PCB Piezotronics, Inc.) and a charge amplifier (Type 5015A, Kistler Group) with a low-pass filter at 30 kHz. The signal is digitalized and saved synchronously to the MCS with a sampling rate of 64 kHz.

The flywheel and the load machine simulate inertia and load of the driven equipment, respectively. The load motor is a PMSM with a nominal torque of 6 Nm (power of 1.7 kW).

To record the operating conditions the following additional parameters are measured synchronously to the motor currents and vibration signal but with lower sampling rates: the radial force on the bearings (Compression and Tension Force Sensor Type K11, Lorenz, 10 kN), the load torque at the torque-measuring shaft, the rotational speed (Torque Transducer Model 305, Magtrol, 2 Nm) and the oil temperature in the bearing module.

### 4.2. Experiments

The test rig was operated under different operating conditions to analyze the influence of operation parameters The rotational speed of the drive system, the radial force onto the test bearing and the load torque in the drive train are the main operation parameters. To ensure comparability of the experiments, fixed levels were defined for each parameter (Table 6). All three parameters were kept constant for the time of each measurement. At the basic setup (Set no. 0) of the operation parameters, the test rig runs at n = 1,500 rpm with a load torque of M = 0.7 Nm and a radial force on the bearing of F = 1,000 N. Three additional settings are used by reducing the parameters one by one to n = 900 rpm, M = 0.1 Nm and F = 400 N (set No. 1-3), respectively. For each of the settings, 20 measurements of 4 seconds each were recorded. Another parameter is the temperature, which was kept roughly at 45-50 °C during all experiments.

the robustness of the CM methods at different operating conditions.

In total, experiments with 32 different bearings were performed: 12 bearings with artificial damages and 14 bearings with damages from accelerated lifetime tests (see Table 4 andTable 5). Moreover, experiments with 6 healthy bearings and a different time of operation were performed as reference states as shown in Table 7.

## 5. DATABASE

Nowadays, a huge amount of data is collected in industry and science for different purposes; some of it is made public in repositories or on websites. The examination of the data with established methods will be addressed in the next chapter, so that the provided data set and the corresponding documentation fulfill the requirements. Therefore, it is assumed that the data is beneficial to further research.

To enable and encourage collaboration in the field of bearing condition monitoring and to allow researchers to use the generated data as benchmark data sets for further research, the data is published online. The data is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 5 Noncommercial academic use of the data is explicitly allowed, but a citation of the origin is required and expected. 6 For commercial use, please contact the author. The download page is available at the KAt-DataCenter website of the Chair of Design and Drive Technology, Paderborn University, Germany: http://mb.uni-paderborn.de/kat/datacenter

The data consists of measurements from 32 different bearing experiments. The bearings belong to three main groups:

 Undamaged (healthy) bearings ( 6x), see Table 6.

 Artificially damaged bearings (12x), see Table 4.

 Bearings with real damages caused by accelerated lifetime tests, (14x) see Table 5. The specifications of the bearings are listed in the tables above.

In summary, the main characteristic of the data set are:  Synchronously measured motor currents and vibration signals with high resolution and sampling rate of 26 damaged bearing states and 6 undamaged (healthy) states for reference.

 Supportive measurement of speed, torque, radial load, and temperature.

 Four different operating conditions (Table 6).

 20 measurements of 4 seconds each for each setting, saved as a matlab file with a name consisting of the code of the operating condition and the four-digit bearing code (e.g. N15_M07_F10_KA01_1.mat).

 Systematic description of the bearing damage by uniform fact sheets (according to the categorization in section 2 -Categorization of Bearing Damage).

## 6. ENVELOPE ANALYSIS FOR VIBRATION SIGNALS

First of all, the bearing damage diagnostic is performed with the envelope analysis based on the vibration, as this is a well-known and established procedure. The objective of this examination is to verify the data and check the execution of experiments for mistakes and errors. Moreover, the detection of the damages provides a first estimate of the attitude of signals and corresponding damages to the authors.

It can be demonstrated that the results of the envelope analysis correspond to the description in literature. The bearing damages cause typical characteristic kinematic frequencies that can be observed in the signals. These frequencies can be calculated for localized damages when the position of the damage (e.g. outer or inner ring) and the geometrical parameters of the bearing are known. (Randall, 2011) Two single point damages, one at the inner ring (KA04) and one at the outer ring (KI18) are considered exemplarily. The envelope spectra in Figure 6 clearly shows the ballpass frequency of the outer raceway (f o ) and their harmonics. The envelope spectra of the damage at the inner raceway in Figure 7 shows the fundamental rotation frequency of the shaft and its harmonics (f n ), the ballpass frequency of the inner race (f i ), and its sidebands as well as its corresponding harmonics.

Figure 6. Envelope spectra of vibration signal for bearing damage at the outer ring.

Figure 7. Envelope spectra of vibration signal for bearing damage at the inner ring.

## 7. CLASSIFICATION ALGORITHM AND RESULTS

The most common analysis for bearing damages involving MCS is to convert the time domain signals into the frequency domain and check for the bearing characteristic

data set: N15_M07_F10_KI18_1 fi f -2f i n 3fn 4fn f +3f i n f +4f i n 2f -3f i n fn f -3f i n f -f i n 5fn 2f -2f i n 2f -f i n fi 2f +f i n f +f i n f +2f i n 2fn f =25Hz; n f =123,3Hz i f -4f i n

frequencies (Blödt et al., 2008). However, in most cases the raw signals are masked by external noise, what makes this method very difficult to apply. Figure 8 shows exemplary plots of the power spectral density of a healthy bearing, a bearing with outer ring damage, and a bearing with inner ring damage. From Figure 8, only the electrical supply frequency (𝑓 𝑒 ) and its harmonics are easily observable. This is mainly due to the masking of bearing characteristic frequencies by external noise and also the presence of distributed damages which are difficult to detect using characteristic frequency approaches (Yang, Merrild, Runge, Pedersen, & Hakon Børsting, 2009).

However, by extracting features from the raw MCS, it is possible to observe the clustering of various damage classes of the bearing through a feature plot as seen in Figure 9. This shows that machine learning (ML) algorithms can be trained to identify various damages on the bearings from extracted features.

Figure 10 shows the workflow of the application of machine learning for the classification of various bearing damages.

The machine learning algorithm learns to map the input features to the corresponding target which consists of a class label representing the type of damage. A classification model is obtained which can be used to predict the type of damage for a given set of input features. In this work, the bearings were categorized in three classes as either healthy, having inner ring damage, or having outer ring damage. Seven state of the art algorithms and an ensemble of the algorithms using majority voting were implemented. These algorithms include: classification and regression trees (CART), random forests (RF), Boosted Trees (BT), neural networks (NN), support vector machines with parameters optimally tuned using particle swarm optimization (SVM-PSO), extreme learning machine (ELM), and k-nearest neighbors (kNN).

### 7.1. Feature Extraction and Selection

Feature extraction involves deriving time-, frequency,-and time-frequency-domain features from the raw signals.

Signals acquired from machinery components such as faulty bearings are normally considered non-stationary, meaning that frequency components of the signal vary over time.

Therefore, the extraction of time-frequency features is necessary. In this work, wavelet packet decomposition (WPD) is employed for the extraction of the time-frequency features. The raw signal is decomposed up to 3 levels. The detailed coefficients and approximate coefficients of level 1 to 3 are obtained and from which the wavelet energy is computed. Fast Fourier Transform (FFT) and power spectral density (PSD) are used to extract the frequency domain features. A total of 23 features are extracted from each signal. A list of the extracted features can be found in (Kimotho & Sextro, 2014). Since not all features are suitable for fault classification, it is necessary to select features that contain most information on the health status of a component to avoid over-fitting and to improve accuracy. Suitable features for fault or health state classification should provide a good separation between different classes.

In this study, a feature selection method based on maximum separation distance between different health states was employed.

Given a feature set of 𝑗 = 1, 2, . . . 𝑄 features in 𝑐 = 1, 2, . . . 𝑁 𝑐 classes or health states, the feature selection is performed as follows:

1. Normalize the features between 0 and 1.

2. Compute the mean (𝑚 𝑗𝑐 ) of each feature 𝑗 within class 𝑐 as follows

𝑚 𝑗𝑐 = 1 𝑛 ∑ 𝑥 𝑖𝑗𝑐 𝑛 𝑖=1

, where 𝑥 is the feature and 𝑛 is the number of samples.

3. Compute the mean of the squared Euclidean distance (𝑑 𝑗 ) between each feature data point 𝑖 and the mean of the same feature in each class

𝑑 𝑗 = 1 𝑛𝑁 𝑐 2 ∑ ∑ ∑ (𝑥 𝑖𝑗𝑘 -𝑚 𝑗𝑐 ) 2 𝑛 𝑖=1 𝑁 𝑐 𝑐=1 𝑁 𝑐 𝑘=1 .

4. Normalize the separation distance with the maximum feature separation distance to produce a performance evaluation criteria

𝑑 ̅ 𝑗 = 𝑑 𝑗 max (𝑑)

.

5. Select the distance with a performance greater than a predetermined threshold. The threshold can be defined by evaluating the classification accuracy for each combined set of features.

In the current study, a selection criterion of 𝑑 ̅ 𝑗 ≥ 0.7 was found to yield the best results. In this case, 9 out of 23 features are selected from each of the two MCS per sample and 15 features from the vibration signals.

### 7.2. Training with Data from Bearings with

Artificially Induced Damages At first, the algorithms were trained with features extracted from measurements with artificially induced bearing damages (see Table 8). The objective was to use a combination of healthy bearings and artificial damaged bearings to identify bearings with real damages and classify them as either healthy, inner ring damage or outer ring damage (3-class approach). In the testing part, features extracted from data with real damages (Table 8) were used as the input to the classification model. The output was the class label.

Table 9 shows the classification accuracy of the machine learning algorithms used with features extracted from MCS and vibration signals under operating conditions in setting 0 (see Table 6), which was found to produce better performance. Features from vibration signals result in a better classification accuracy than those from MCS. However, the overall performance of other algorithms remains relatively the same regardless of the sensor data used.

Figure 13 is the confusion matrix of the ensemble predictions using features from MCS. There are no false positives or negatives.

However, the highest misclassification rate is recorded with the outer ring damage (class 2), as is the case with the ML methods trained with data of bearings with artificially induced damages. A closer look at the results indicates that the misclassified samples belong to the data sets KA04 and KA22 which have damages of level 1 (see Table 5).

### 7.4. Training with Data of Bearings with Multiple Damages

Further tests were carried out by including data sets from bearings with multiple damages at both raceways, at inner and outer ring (KB23, KB24 and KB27). According to the dominant damage type KB23 and KB24 were assigned to the inner ring damage (class 3), while KB27 was assigned to the outer ring damage (class 2).

Training and testing was done in a 5-fold cross validation manner based on the KAxx and KIxx data sets as described in section 7.3. In addition, KB23 and KB24 were used interchangeably for training and testing in a way that when one was used for training, the other was used for testing. KB27 was only used for testing since it is the only data set where the outer ring damage is dominant. Table 13 shows the average performance of the algorithms for this case. For the neural networks, parameters such as the number of hidden layers and neurons were not tuned and this explains the poor performance.

### 7.5. Summary of Classification Results

The following conclusions can be drawn from the results above:

 Classifications based on vibration signals achieve higher classification accuracy than MCS-based classifications in all cases.

 Training with artificial damage (7.2) and testing with real damages achieve quite low accuracies.

 Training and testing with real damages (7.3) from accelerated lifetime test yield a lot better results.

 Conclusion: For a realistic application of classification methods in CM systems the use of training data with artificial damages is apparently not sufficient.

 Training and testing with an additional focus on multiple damages (7.4) yield even lower accuracies, as an example for different damage behavior according to the categorization of possible industrial damages. The discrepancy in the classification results of some of the machine learning algorithms could be attributed to overfitting. Therefore, further investigations should be done to improve their generalization, for instance through selection of suitable kernel functions or optimal parameter tuning.

Conclusion for application: real industry applications with different electromechanical systems will lead to lower rates, therefore the development and selection of robust algorithms is important. Data sets of the benchmark data will support researchers in developing these algorithms.

## 8. CONCLUSION

Application of data-driven classification algorithms for vibration-based diagnosis of damages in rolling element bearings has been researched widely and appears to be a mature approach. From the present results, it is evident that MCS also have a great potential for fault diagnosis of external rolling element bearings in electromechanical drive systems. The advantage of this approach in general is that no additional sensors are required, consequently reducing the cost of the condition monitoring system.

The particular novelties of the present research include the consideration of damage in external bearings (positioned outside the electric motor) and using the MCS as input for the detection of the damage. Moreover, a wide variety of bearing damage is considered. This paper presents important steps in the development of condition monitoring methods for electromechanical drive systems. The main features of this study can be summarized as:

 Development of a systematic categorization method to describe specific bearing damages in detail.

 Generation of artificial and realistic bearing damages.

 Synchronous acquisition of vibration and motor current signals with a modular experimental setup to gather data sets for the development and testing of classification algorithms.

 Verification of measurement data by using the established method of envelope analysis based on the vibration signals. It proves the proper data acquisition and compares it with the state of the art approaches proposed in literature.

 Application of ML classification algorithms show that they are able to identify the damaged bearings using MCS, but require sophisticated training data. The results show that the MCS can be used together with machine learning algorithms to identify and classify bearing damages within the external drive systems. However, the classification accuracy of the machine learning algorithms with the MCS is still low in comparison to vibration signal approaches. Especially the use of signals from artificially induced damages to identify real damages in the drive systems needs to be further investigated as the damage recognition rate is quite low. Moreover, significant differences are observed using different groups of real damage (single and repetitive damages in comparison to multiple damages).

Therefore, more research should be conducted on improving bearing damage detection from MCS in order to have low cost and accurate condition monitoring system for electromechanical drive systems. To promote further research, the experimental raw data is published alongside with this publication as a benchmark to develop and test data-driven classifiers or other condition monitoring methods. More detailed examinations concerning the behavior of different damages as e.g. with different damage levels can be carried out with the provided data and the associated damage description. As only a few aspects of the classification behavior could be examined in this publication, the examination of CM methods should be intensified using the data sets.

Moreover, some open questions remain, which could be examined using future data sets. Industrial application requires the detection of damages under variable operating conditions. In addition, other mechanical faults in the drive train and other bearing damages should be investigated since this work covers only two main modes of damages out of a possible six. Finally, the implementation into industry applications and related issues have to be discussed and tested.

## Figures et tableaux

**Figure 1.** Parameters for describing the geometry of bearing damages.

**Figure 3** Figure3shows two examples of bearing damages generated in the accelerated lifetime test.

**Figure 3.** Indentation at the raceway of the outer ring (left); small pitting at the raceway of the inner ring (right).Bearing KB27 (left) shows indentations from debris particles at the outer ring. As the damage is repeated along the raceway only some of them are shown. Bearing KI14 (right) has a very small pitting at an early stage (level 1) at

**Figure 4.** The ball bearings with different types of damage are mounted in the bearing test module to generate the experimental data.The rolling bearing module provides the possibility of using a test bearing under a constant radial load, which can be continuously adjusted up to 10 kN before each experiment. An adapter gives the possibility to measure the vibration of the inner housing, which holds the test bearing in the main direction of the load. The precise design of the bearing module and additional features, such as the possibility to simulate tilting faults or the use of roller bearings, are described byLessmeier, Enge-Rosenblatt, Bayer, & Zimmer, 2014.

**Figure 4.** Modular test rig. The motor (1) is a 425 W Permanent Magnet Synchronous Motor (PMSM) with a nominal torque of T = 1.35 Nm, a nominal speed of n = 3,000 rpm, a nominal current of I = 2.3 A and a pole pair number p = 4 (Type SD4CDu8S-009, Hanning Elektro-Werke GmbH & Co. KG). It is operated by a frequency inverter (KEB Combivert 07F5E 1D-2B0A) with a switching frequency of 16 kHz. This standard industrial inverter is used to provide conditions similar to motors used in the industry because the current signals show significant noise due to the pulse-width

**Figure 5.** Schema of measurement procedure.

**Figure 10.** Figure10. Application of machine learning (ML) for fault diagnosis.

**Figure 8.** Frequency spectrum from MCS for (a) healthy bearing, (b) outer ring damage and (c) inner ring damage.

**Figure 9.** Clustering of bearing health states for (a) features from MCS and (b) vibration signals.

**Table 1.** Categorization of bearing damage. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Category and sub-category |  | Criterion | Example
    General info (bearing) |  | Bearing Type | ball bearing
     |  | Bearing designation (dimension series, bore code) | 6203
     |  | Suffix | n/a
    Manufacturer specific information about bearing | Geometry | Diameter of inner raceway | 24.0 mm
     |  | Diameter of outer raceway | 33.1 mm
     |  | Pitch circle diameter | 28.55 mm
     |  | Number of rolling elements | 8 pc.
     |  | Rolling element diameter | 6.75 mm
     |  | Length of rolling element | 6.75 mm
     |  | Nominal pressure angle | 0° N
     | Parameters | Static load rating | 4750 N
     |  | Dynamic load rating | 9500 N
     |  | Speed limit | 12000 rpm
     |  | Manufacturer | FAG
    Application specific information | Identification | Bearing code (used for datasets) | KB24
     |  | Sample number | 12-01
     | Place of operation | Installation site | 01
     |  | Installation type (system type) | KAt - lifetime test rig
     |  | Operator | KAt
     | Operation conditions | Number of load cycles | 2769500
     |  | Lifetime | 15:01 h:min
     |  | Load | 3800 N
     |  | Dynamic equivalent load | 3800 N
     |  | Rotational speed | 2900 rpm
     |  | Load direction | 0 °
     |  | Comment | n/a
    Damage | Type of Damage | Mode | fatigue
     |  | Sub-mode | n/a
     |  | Symptom | pitting
     | Damage location | Component | outer ring
     |  | Position of damage | raceway
     |  | Damage combination | multiple
     |  | Arrangement of the repetitive and multiple damages | no repetition
     | Geometry | Length | 9.4 mm
     |  | Extent of damage | 3
     |  | Width | total raceway
     |  | Depth | n/a
     |  | Characteristic of damage | distributed
     | Damage occurrence | Damage method | acc. lifetime test
     |  | Cause of damage (category) | operating conditions
     |  | Cause of damage (detailed) | load, lubricant

and sub-category Criterion Example General info (bearing)

    location, geometry, and occurrence. If there is more than a |  |  | 
    single damage to one bearing, the criteria of the last group |  |  | 
    are repeated to get a detailed and full description of all |  |  | 
    occurring damages. |  |  | 
     |  | Bearing Type | ball bearing
     |  | Bearing designation | 
     |  | (dimension series, bore | 6203
     |  | code) | 
     |  | Suffix | n/a
     |  | Diameter of inner raceway | 24.0 mm
     |  | Diameter of outer raceway | 33.1 mm
     |  | Pitch circle diameter | 28.55 mm
    Manufacturer specific information about bearing | Geometry | Number of rolling elements Rolling element diameter Length of rolling element Nominal pressure angle Static load rating | 8 pc. 6.75 mm 6.75 mm 0° N 4750 N
     | Parameters | Dynamic load rating | 9500 N
     |  | Speed limit | 12000 rpm
     |  | Manufacturer | FAG
     | Identification | Bearing code (used for datasets) | KB24
     |  | Sample number | 12-01
     |  | Installation site | 01
     | Place of | Installation type (system | KAt -lifetime
     | operation | type) | test rig
    Application |  | Operator | KAt
    specific |  | Number of load cycles | 2769500
    information |  | Lifetime | 15:01 h:min
     |  | Load | 3800 N
     | Operation conditions | Dynamic equivalent load Rotational speed | 3800 N 2900 rpm
     |  | Load direction | 0 °
     |  | Comment | n/a
     | Type of Damage | Mode Sub-mode Symptom | fatigue n/a pitting
     |  | Component | outer ring
     |  | Position of damage | raceway
     | Damage | Damage combination | multiple
     | location | Arrangement of the | 
     |  | repetitive and multiple | no repetition
     |  | damages | 
    Damage |  | Length | 9.4 mm
     |  | Extent of damage | 3
     | Geometry | Width | total raceway
     |  | Depth | n/a
     |  | Characteristic of damage | distributed
     | Damage occurrence | Damage method Cause of damage (category) | acc. lifetime test operating conditions
     |  | Cause of damage (detailed) | load, lubricant

**Table 3.** Artificial bearing damage.Details about the size and a categorization of the available test bearings according to the developed criteria (see section 2) are listed in Table4. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Bearing Code | Component | Extent of Damage (level) | Damage Method
    KA01 | OR | 1 | EDM
    KA03 | OR | 2 | electric engraver
    KA05 | OR | 1 | electric engraver
    KA06 | OR | 2 | electric engraver
    KA07 | OR | 1 | drilling
    KA08 | OR | 2 | drilling
    KA09 | OR | 2 | drilling
    KI01 | IR | 1 | EDM
    KI03 | IR | 1 | electric engraver
    KI05 | IR | 1 | electric engraver
    KI07 | IR | 2 | electric engraver
    KI08 | IR | 2 | electric engraver
    OR: outer ring; IR: inner ring; |  |  | 

**Table 4.** Test bearings with artificial damage.

    Bearing | Code | Component | Extent of | Damage | (level) | Damage | Method
    KA01 OR |  | 1 |  | EDM
    KA03 OR |  | 2 |  | electric engraver
    KA05 OR |  | 1 |  | electric engraver
    KA06 OR |  | 2 |  | electric engraver
    KA07 OR |  | 1 |  | drilling
    KA08 OR |  | 2 |  | drilling
    KA09 OR |  | 2 |  | drilling
    KI01 IR |  | 1 |  | EDM
    KI03 IR |  | 1 |  | electric engraver
    KI05 IR |  | 1 |  | electric engraver
    KI07 IR |  | 2 |  | electric engraver
    KI08 IR |  | 2 |  | electric engraver
     |  | OR: outer ring; IR: inner ring;
    It has to be mentioned that all the artificial damages are
    single point damages without a repetition or combination
    with other damages (compare section 2 -Categorization of
    Bearing Damage) |  |  |  |  | 
    3.2 |  |  |  |  |  |  | 

. Generating Real Bearing Damage Samples by Accelerated Lifetime Tests Therefore, often only a small number of damage states are available. Moreover, there are many different bearing types, sizes and machine types, and the operating conditions may change irregularly as they depend on the application. Therefore, measurements are expected to be influenced by various factors. This is helpful at later development stages to increase the robustness, but distracting for the development of the basic methods. To reduce the external influences, scientific test rigs are used, which enable the generation of realistic bearing damages by accelerated lifetime tests. Furthermore, damages for the needed bearing types and geometries can be systematically generated at reproducible conditions. The main disadvantage is that this consumes a lot of time and resources.(Nectoux et al., 2012;Qiu, Lee, Lin, & Yu, 2006)

    There are two options to test and develop CM methods with
    measurement data of real bearing damages: to measure
    bearing damages in real or in scientific test rigs.

**Table 5.** Test bearings with real damages caused by accelerated lifetime test.

    Bearing code | Damage (main mode and symptom) | Bearing element | Combination | Arrangement | Extent of damage | Characteristic of damage
    KA04 | fatigue: pitting | OR | S | no repetition | 1 | single point
    KA15 | Plastic deform.: Indentations | OR | S | no repetition | 1 | single point
    KA16 | fatigue: pitting | OR | R | random | 2 | single point
    KA22 | fatigue: pitting | OR | S | no repetition | 1 | single point
    KA30 | Plastic deform.: Indentations | OR | R | random | 1 | distributed
    KB23 | fatigue: pitting | IR (+OR) | M | random | 2 | single point
    KB24 | fatigue: pitting | IR (+OR) | M | no repetition | 3 | distributed
    KB27 | Plastic deform.: Indentations | OR + IR | M | random | 1 | distributed
    KI04 | fatigue: pitting | IR | M | no repetition | 1 | single point
    KI14 | fatigue: pitting | IR | M | no repetition | 1 | single point
    KI16 | fatigue: pitting | IR | S | no repetition | 3 | single point
    KI17 | fatigue: pitting | IR | R | random | 1 | single point
    KI18 | fatigue: pitting | IR | S | no repetition | 2 | single point
    KI21 | fatigue: pitting | IR | S | no repetition | 1 | single point
    OR: outer ring; IR: inner ring; |  |  |  | 

[figure sans légende identifiée] Lee, H. Qiu, G. Yu, J. Lin, and Rexnord Technical Services, NSF I/UCR Center for Intelligent Maintenance Systems, Milwaukee, WI, USA: http://ti.arc.nasa.gov/tech/dash/pcoe/prognostic-data-repository/

     | bearing diagnostics employing ML-algorithms.
     | Some diagnostic data sets for bearing damages are publicly
     | available; the most popular and comprehensive ones are
     | listed below: |  |  |  | 
     |  CWRU: Bearing Data Center/ Seeded Fault Test Data | 1
     |  FEMTO Bearing Data Set | 2
     |  MFPT Fault Data Sets | 3 | 
     |  Bearing Data Set IMS | 4 | 
     | These data sets focus on different aspects. Some use
     | artificial damages (CWRU, MFPT), others use real damages
     | (FEMTO, IMS). CWRU and FEMTO use different
     | operating conditions by varying load and speed; others use
     | only different load situations (MFPT) or just one condition
     | (IMS). The FEMTO data set provides run-to-failure data
     | with measurements over a long period, but does not give
     | any information about the properties of the damages.
     | Altogether, the data sets mentioned use the classical
     | vibration signals for bearing diagnostics. To the best
     | knowledge of the authors of the present paper, no publicly
     | available data set providing data for diagnostics of external
     | bearing damages based on MCS is known.
     | Therefore, the focus was to systematically create a high
     | quality data set which takes into account several operating
     | conditions and a wide distribution of artificial as well as
     | realistic bearing damages. |  |  | 
    But obtaining the appropriate data in the needed quality and quantity for specialized research often is still challenging, especially, if a wide range of different types of damages or the yet rarely used MCS are the target of interest. This also applies to training data for | Smith and Randall demand some properties for benchmark data sets which are based on their experience with different diagnostic methods used on a vibration-based CM data set for bearings. They list three requirements (Smith & Randall, 2015), which can be applied accordingly to MCS data sets:
     |  Systematic and comprehensive documentation.
     |  High sampling rates (>40 kHz).
     |  Data verification with established methods before
     | publication of the data. | 
     | The first two issues are already addressed in this paper by
     | the characterization of damage and the extensive
     | documentation of the experiments, including a high
     | sampling rate for the two main signals (64 kHz).
     | 1 Case Western Reserve University (CWRU), Cleveland, Ohio, USA
     | http://csegroups.case.edu/bearingdatacenter/home
     | 2 FEMTO-ST Institute, Besançon, France; http://www.femto-
     | st.fr/en/Research-departments/AS2M/Research-groups/PHM/IEEE-PHM-
     | 2012-Data-challenge.php |  |  | 
     | 3 Mechanical Failures Prevention Group (MFPT) Society (a Division of the
     | Vibration | Institute), |  | Oak | Brook, | IL, | USA,
     | http://www.mfpt.org/FaultData/FaultData.htm
     | 4 J. |  |  |  | 

**Table 6.** Operating parameters.

    Rotational | Load | Radial | Name of
    No. | speed | Torque | force | Setting
     | [rpm] | [Nm] | [N]
    0 | 1500 | 0.7 | 1000 | N15_M07_F10
    1 |  | 900 | 0.7 | 1000 | N09_M07_F10
    2 | 1500 | 0.1 | 1000 | N15_M01_F10
    3 | 1500 | 0.7 | 400 | N15_M07_F04
    Table 7. Operating parameter of healthy (undamaged)
     |  | bearings during run-in period.
    Bearing Code | Run-in Period [h] | Radial Load [N] | Speed [min -1 ]
    K001 |  | >50 | 1000-3000 1500-2000
    K002 |  | 19 | 3000 | 2900
    K003 |  | 1 |  | 3000 | 3000
    K004 |  | 5 |  | 3000 | 3000
    K005 |  | 10 | 3000 | 3000
    K006 |  | 16 | 3000 | 2900

**Table 8.** List of data sets used for training and testing the machine learning algorithms.

    Class |  | Training Testing
    1 | Healthy | K002 | K001
     |  |  | KA22
     |  | KA01 | KA04
    2 | OR Damage | KA05 | KA15
     |  | KA07 | KA30
     |  |  | KA16
     |  |  | KI14
     |  | KI01 | KI21
    3 | IR Damage | KI05 | KI17
     |  | KI07 | KI18
     |  |  | KI16

**Table 9.** Performance of various algorithms trained with features of bearings with artificially induced damages and tested with features of bearings with real damages.Using features extracted from MCS, the support vector machine approach with parameters optimally tuned by using particle swarm optimization (SVM-PSO) shows the best performance of all algorithms with 60.9% classification accuracy. Figure11depicts the confusion matrix for SVM-PSO. On the confusion matrix, the rows correspond to the predicted class and the columns to the true class. The diagonal cells represent the correctly predicted class, while the off-diagonal cells show misclassifications. The left column displays the false positives (healthy samples classified as damaged) and the upper row the false negatives (samples with damages classified as healthy). The bottom row indicate the accuracy and misclassification rate for each true class while the right column shows the accuracy and misclassification rate of each predicted class. The cell in the bottom right gives the overall accuracy. Bearings with inner ring damages (class 3) record the highest misclassification rate, with the majority of the cases being classified as having outer ring damages (class 2).

    Algorithm Classification Accuracy [%]
     | MCS Vibration Signals
    CART | 26.8 | 65.9
    RF | 45.0 | 64.1
    BT | 38.6 | 62.3
    NN | 45.5 | 65.5
    SVM-PSO | 60.9 | 65.5
    ELM | 45.5 | 65.9
    kNN | 45.5 | 63.2
    Ensemble | 45.9 | 75.0

Training with Data of Bearings with Real Damages The data sets in Table10of healthy bearings and those with real damages were used for training and testing in a 5-fold cross-validation manner. For each combination, three data sets from each class were used for training and the other two for testing, resulting in 10 combinations. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Healthy (Class 1) | Outer ring damage (Class 2) | Inner ring damage (Class 3)
    K001 | KA04 | KI04
    K002 | KA15 | KI14
    K003 | KA16 | KI16
    K004 | KA22 | KI18
    K005 | KA30 | KI21

**Table 10.** Categorization of data sets for healthy bearings and bearings with real damages.

    Healthy | Outer ring damage | Inner ring damage
    (Class 1) | (Class 2) | (Class 3)
    K001 | KA04 | KI04
    K002 | KA15 | KI14
    K003 | KA16 | KI16
    K004 | KA22 | KI18
    K005 | KA30 | KI21
    Similarly, features from both MCS and vibration signals
    were used separately. The mean classification accuracy for
    the 10 combinations was computed and is presented in

**Table 11.** Random Forest and the ensemble algorithm have the highest classification rates of 93.3% using the MCS data while CART, RF, and ensemble have the highest classification rate of 98.5% using the vibration data.

**Table 11.** Performance of various algorithms trained and tested with features of bearings with real damages.

    Algorithm Classification Accuracy [%]
     |  | MCS Vibration Signals
    CART |  | 66.7 |  | 98.3
    RF |  | 83.3 |  | 98.3
    BT |  | 81.7 |  | 83.3
    NN |  | 65.8 |  | 44.2
    SVM-PSO | 56.7 |  | 75.8
    ELM |  | 69.2 |  | 60.8
    kNN |  | 68.3 |  | 62.5
    Ensemble | 93.3 |  | 98.3
    Figure 14 is the confusion matrix of the ensemble of
    algorithms using features from vibration signals. A few
    misclassification instances are observed in samples with
    outer ring (KA04) and inner ring (KI21) damages also with
    damages of level 1. |  |  |  | 
     |  |  | MCS | 
     | 1 | 400 33.3% | 0 0.0% | 0 0.0% | 100% 0.0%
    Class Predicted | 2 3 | 0 0.0% 0 0.0% | 320 26.7% 80 6.7% | 0 0.0% 400 33.3% | 100% 0.0% 83.3% 16.7%
     |  | 100% | 80.0% | 100% | 93.3%
     |  | 0.0% | 20.0% | 0.0% | 6.7%
     |  | 1 | 2 | 3 | 
     |  |  | Target Class | 
    Figure 13. Confusion matrix for ensemble of
    algorithms trained and tested with MCS features
    of bearings with real damages.
     |  |  | Vibration Signals | 
     | 1 | 400 33.3% | 0 0.0% | 0 0.0% | 100% 0.0%
    Class Predicted | 2 3 | 0 0.0% 0 0.0% | 390 32.5% 10 0.8% | 10 0.8% 390 32.5% | 97.5% 2.5% 97.5% 2.5%
     |  | 100% | 97.5% | 97.5% | 98.3%
     |  | 0.0% | 2.5% | 2.5% | 1.7%
     |  | 1 | 2 | 3 | 
     |  |  | Target Class | 
    Figure 14. Confusion matrix for ensemble of
    algorithms trained and tested with vibration features
    of bearings with real damages.

**Table 13.** Performance of various algorithms trained and tested with features of bearings with real damages.

    Algorithm | Classification Accuracy [%] MCS Vibration Signals
    CART | 86.3 | 91.3
    RF | 68.1 | 91.3
    BT | 63.7 | 79.4
    NN | 66.3 | 33.2
    SVM-PSO | 80.6 | 70.8
    ELM | 81.9 | 71.9
    kNN | 61.3 | 70.0
    Ensemble | 86.3 | 91.3
    Figures 15 and 16 are the confusion matrices for the
    ensemble of algorithms with the inclusion of the data sets of
    bearings with multiple damages. The inclusion of these data
    sets reduces classification accuracy, with the highest
    misclassification rate falling within the KB27 and with most
    of the samples being classified as having inner ring
    damages. |  |
