---
id: 2012-nectoux-pronostia-experimental-platform-bearings-accelerated
title: "PRONOSTIA: An Experimental Platform for Bearings Accelerated Degradation Tests"
year: 2012
backend: grobid
---

## Abstract

This paper deals with the presentation of an experimental platform called PRONOSTIA, which enables testing, verifying and validating methods related to bearing health assessment, diagnostic and prognostic. The choice of bearings is justified by the fact that most of failures of rotating machines are related to these components. Therefore, bearings can be considered as critical as their failure significantly decreases availability and security of machines. The main objective of PRONOSTIA is to provide real data related to accelerated degradation of bearings performed under constant and/or variable operating conditions, which are online controlled. The operating conditions are characterized by two sensors: a rotating speed sensor and a force sensor. In PRONOSTIA platform, the bearing's health monitoring is ensured by gathering online two types of signals: temperature and vibration (horizontal and vertical accelerometers). Furthermore, the data are recorded with a specific sampling frequency which allows catching all the frequency spectrum of the bearing during its whole degradation. Finally, the monitoring data provided by the sensors can be used for further processing in order to extract relevant features and continuously assess the health condition of the bearing. During the PHM conference, a "IEEE PHM 2012 Prognostic Challenge" is organized. For this purpose, a web link to the degradation data is provided to the competitors to allow them testing and verifying their prognostic methods. The results of each method can then be evaluated regarding its capability to accurately estimate the remaining useful life of the tested bearings.

## I. INTRODUCTION

To remain competitive, industrial companies must continuously keep their production means in good operating conditions by improving their availability, reliability, security while reducing their maintenance costs. One of possible solutions which allows satisfying the above requirements is the implementation of appropriate maintenance strategies. In this domain the Condition-Based Maintenance (CBM) and Predictive Maintenance (PM) are the most efficient ones [1]- [3], because they allow optimizing the maintenance by anticipating the failure's occurrence. Indeed, contrary to a traditional corrective maintenance, where the interventions are done after the occurrence of the failure, in a CBM (or a PM), the interventions are done according to the observed or estimated health condition of the equipment. Generally, a CBM system is seen as the integration of seven layers [4]: sensors, signal processing, condition monitoring (or fault detection), health assessment (or fault diagnostic), prognostic, decision support and finally presentation layers. Among these activities, failure prognostic is considered as the most recent one, with an increasing research as well as industrial interest. The increasing interest accorded to failure prognostic has led to numerous methods, tools and applications during the last decade. According to the reported literature, failure prognostic methods can be classified into three main approaches: model-based, data-driven and hybrid approaches [1], [4], [5]. Model-based prognostic approach relies on the use of an analytical model (set of algebraic or differential equations) to represent the behavior of the system including its degradation. The advantage of this approach is that it provides precise results. However, its drawback dwells in the fact that real systems are often nonlinear and the degradation mechanisms are generally stochastic and difficult to obtain in the form of analytical models. Data-driven prognostic approach aims at transforming the monitoring and operating data into relevant information and behavior models of the system including its degradation. This approach uses artificial intelligence tools and/or statistical methods to learn the degradation model and to predict the Remaining Useful Life (RUL) of the equipment. The datadriven approach can be used in cases where getting monitoring data and processing them is easier than constructing physical and analytical behavior models. Hybrid prognostic methods combine both model-based and data-driven approaches and thus take benefit and drawback from both of them. In practice, tests and verifications of fault detection and isolation (or fault diagnostic) methods are easy to perform, because the faults can be easily simulated or introduced on the real industrial system. However, this is not the case for prognostic methods where the fault is generally a consequence of a long and slow degradation of one or more components of the system. Thus, to test these methods, it is necessary to create (or initiate) the degradation through accelerated degradation tests of physical components. For this purpose, researchers have made their own experimental platforms, but only a few number of these platforms are opened to external researchers to provide them with real monitoring data [6]. This paper aims at presenting a new experimental platform, called PRONOSTIA, related to bearings' degradation tests. This platform comes to complete the list of existing ones and will be a source of experimental data acquired for constant and/or variable operating conditions, enabling therefore the verification of condition monitoring, fault detection, fault diagnostic and prognostic approaches. In this sens, an IEEE PHM 2012 Prognostic Challenge is organized during the 2012 IEEE PHM conference, which took place in Denver. Thus, in addition to the presentation of PRONOSTIA, this paper gives details on the organized PHM challenge (who and how to participate, the related data, the requested results, etc.). The paper is organized as follows: after the introduction, section 2 gives a brief state of the art on the existing experimental platforms reported in the literature, the PRONOSTIA platform is presented in section 3, the acquired data and some experimental results are given in section 4, the IEEE PHM 2012 Prognostic Challenge is explained in section 5 and finally, section 6 concludes the paper.

## II. STATE OF THE ART ON EXPERIMENTAL PLATFORMS

In order to test and verify the prognostic methods developed and published in the literature, dedicated test beds and platforms have been designed and realized by several laboratories over the world. Most of these experimental systems concern specific physical components, such as bearings, gears, pumps, etc. The following paragraphs summarize the experimental platforms which are yet published. Note that not all of the published test beds provide experiment data for external users, but only some of them [6].

### A. Overview of test beds

The following paragraphs present an overview of experimental platforms reported in the literature and related to critical physical components such as gearboxes, pumps, pinions, etc. The test beds related to bearings will be presented in the subsection II-B. A test bed related to a gearbox and a pinion gear has been used in [7]. In this application, a spiral bevel pinion was seeded with two electrical discharge machine (EDM) notches (heel and toe) on the drive side of one of the pinion gear teeth to artificially accelerate tooth root cracking. Several accelerometers were then placed on the gearbox with a health and usage monitoring system (HUMS) used to generate the vibration features. In the case of machining tools, a milling data set experiments related to milling machine for different speeds, feeds and depth of cut can be found in [6]. In the same way, an experimental platform has been developed by SIMTech of Singapore [8] to provide data during the PHM challenge organized in 2010 by the PHM society. In [9] the authors used an experimental setup related to drilling life tests to verify their method. The tests were conducted on a MAHO 700S machine, which is a computer numerical controlled (CNC) five axis machining center, with movement in three perpendicular axes and a rotary/tilt table. Finally, in [10] a method is proposed to estimate the tool wear of a turning process over a wide range of cutting conditions. The developments were validated thanks to experiments conducted on a conventional lathe TUD-50.

Concerning the pumps, an experimental setup has been used in [11] to evaluate the performance of a developed Hidden Semi-Markov Model method for equipment health prognostic. The experimental setup consisted in a real hydraulic pump. During the experiments, long-term wear test experiments were conducted at a research laboratory facility. Three pumps were then worn by running them using oil containing dust. Finally, data set experiments related to charging and discharging of Li-Ion batteries can be found in [6]. The records concern the impedance as the damage criterion and the data set was provided by the Prognostics Center of Excellence at NASA. The same center proposed preliminary data from thermal overstress accelerated aging for six devices. Note that this overview is obviously not exhaustive, but enables to see that real systems are required to test and verify PHM algorithms. Also, the variety of presented applications reveals that most PHM tools are application-based. Thus, further developments to face this aspect are still required. Among the works of the PHM field, bearings failures analysis benefits from a great interest and this is the point addressed in the following of the paper.

### B. Bearings test beds

Numerous prognostic methods proposed in the literature were tested on the degradation of bearings. Thus, in [12] the authors have used a test bed related to bearings' degradations to test and verify their fault detection and diagnostic method. Similarly, a bearing test bed is proposed in [13] to detect defects on the balls, the inner and outer raceways of bearings. In this application, the defects were induced by means of electrical discharge machine. In the same way, a diagnostic method has been proposed in [14] were three accelerometers were used to measure the vibration on the tested bearings. The difference with the above applications is that in this one a load is applied on the bearing to accelerate its degradation. Also, in [15] a dedicated test bed has been used to perform failure prognostic on bearings. The particularity of the used application is that the bearings' degradations were obtained after several days (around 50 days) and thus the amount of data to process was considerable. An experimental platform was used in [16] to simultaneously degrade four bearings, whereas in [17] a test bed for aerospace industry with special bearings tested without lubrication was used. Finally, experimental data related to bearings can be found in the NASA data repository [6]. These data are provided by the Center for Intelligent Maintenance Systems (IMS). In the particular case of bearings test beds, and compared to those proposed in the literature, the data provided by the PRONOSTIA experimental platform are different in the sense that they correspond to "normally"degraded bearings. This means that the defects were not initially initiated on the bearings and that each degraded bearing contains almost all the types of defects (balls, rings and cage). The acquired experimental data can then be used for fault detection, diagnostic and prognostic. Furthermore, even if the data presented in this paper concern at this time only constant operating conditions for each realized experiment, the current design of PRONOSTIA allows us in the future to provide data related to bearings degraded under variable operating conditions.

## III. THE PRONOSTIA PLATFORM

PRONOSTIA is an experimentation platform (Fig. 1) dedicated to test and validate bearings fault detection, diagnostic and prognostic approaches. The platform has been designed and realized at AS2M 1 department of FEMTO-ST 2 institute. The main objective of PRONOSTIA is to provide real experimental data that characterize the degradation of ball bearings along their whole operational life (until their total failure). This experimental platform allows to conduct bearings' degradations in only few hours, and thus it is possible to get significant number of experiments within a week. PRONOSTIA is composed of three main parts: a rotating part, a degradation generation part (with a radial force applied on the tested bearing) and a measurement part, which are detailed hereafter.

### A. The rotating part

This part includes the asynchronous motor with a gearbox and its two shafts. The first shaft is near to the motor and the second shaft is placed at the ride side of the incremental encoder. The asynchronous motor is the actuator that allows the bearing to rotate through a system of gearing and different couplings. The motor has a power equal to 250 W and transmits the rotating motion through a gearbox, which allows the motor to reach its rated speed of 2830 rpm, so that it can deliver its rated torque while maintaining the speed of the secondary 1 Automatic control and Micro-Mechatronic Systems 2 Franche-Comté Electronics, Mechanics, Thermal Processing, Optics -Science and Technology shaft to a speed less than 2000 rpm. The gearbox is homemade and consists of two pulleys bound by a timing belt, itself held by a turnbuckle. Compliant and rigid shaft couplings are used to create connections for the transmission of the rotating motion produced by the motor to the shaft support bearing. The bearing support shaft (Fig. 2) leads the bearing through its inner race. This one is kept fixed to the shaft with a shoulder on the right hand and a threaded locking ring on the left hand. The shaft which is made of one piece is held by two pillow blocks and their large gearings. Two clampings allow the longitudinal blocking of the shaft between the two pillow blocks. The human machine interface of PRONOSTIA allows the operator to set the speed, to select the direction of the motor's rotation and to display the monitoring parameters such as the motor's instantaneous temperature expressed in percentage of the maximum temperature of use. The whole driving chain of the motor includes the human interface machine and a frequency converter, which are both connected with a Profibus-DP link to an industrial programmable logic controller.

### B. Generation of the radial force

This part has all its components, except the proportional regulator, grouped in a unique and same aluminum plate and is partially isolated from the instrumentation part by a thin layer of polymer. The aluminum plate supports a pneumatic jack (Fig. 3), a vertical axis and its lever arm, a force sensor, a clamping ring of the test bearing, a support test bearing shaft, two pillow blocks and their large oversized bearings. The radial force applied on the test ball bearing constitutes the heart of the global system. In fact, the radial force reduces the bearing's life duration by setting its value up to the bearing's maximum dynamic load which is 4000 N. This load is generated by a force actuator, which consists in a pneumatic jack, where the supply pressure is delivered by a digital electro-pneumatic regulator.

### Proportional regulator

### Pneumatic jack

Fig. 3. The pneumatic jack, the pressure regulator and the radial force generation.

The force issued from the pneumatic jack is indirectly applied on the external ring of the test ball bearing. This force is first amplified by a rotating lever arm, then transmitted to the test bearing through its clamping ring (Fig. 3).

### C. Measurements part

The Bearing's operation conditions are determined by instantaneous measures of the radial force applied on the bearing, the rotation speed of the shaft handling the bearing and of the torque inflicted to the bearing. Each of these three analog measures is acquired at a frequency equal to 100 Hz. The characterization of the bearing's degradation is based on two data types of sensors: vibration and temperature (Fig. 4). The vibration sensors consists of two miniature accelerometers positioned at 90 • to each other; the first is placed on the vertical axis and the second is placed on the horizontal axis. The two accelerometers are placed radially on the external race of the bearing. The temperature sensor is an RTD (Resistance Temperature Detector) platinum PT100 (1/3 DIN class) probe, which is place inside a hole close to the external bearing's ring. The acceleration measures are sampled at 25.6 kHz and the temperature ones are sampled at 10 Hz. The data acquisition system is based on a four slot chassis, which includes three I/O modules. It aggregates the data issued from the whole sensors and transmits them through an USB 2.0 link to the central unit in charge of real time data visualization and storage. Finally, the visualization of the monitoring data is done by a specific application implemented under Labview environment and installed on a dedicated computer (Fig. 5). This application allows the operator to visualize raw signals from different sensors. The acquired data are formatted, time stamped and stored locally in the computer under different files. The data can then be used for offline or online processing in order to continuously assess the health condition of the test bearing (fault detection, diagnostic and prognostic applications). Figure 6 depicts an example of what one can observe on the ball bearing components before and after an experiment.

## IV. EXPERIMENTAL RESULTS

### A. Degradation patterns

Depending on various factors, the degradation may be different for distinct bearings. Assuming that no other information is available about the other components than the rotating system and that load and speed are constant, one has to use only the data collected via the sensors located around the bearings. Moreover, nothing is known about the nature and the origin of the degradation (balls, inner or outer races, cage...) therefore data-driven techniques has to be applied. According to the bearing and to the way the degradation evolves, the fault modes can be slightly different for distinct bearings. As a result, the degradation "patterns" may have particular characteristics as illustrated in the following. In this paper, we considered several experiments for which different features (health index) were extracted. The choice of features is typical of bearings diagnostics and prognostics [18]. Figure 7 shows a vibration raw signal taken from PRONOSTIA during a whole experiment.

### B. The ideal degradation

As a first example, consider an experiment where several features (and health index) agree about the degradation and where the patterns depicted are very typical. Figure 8 illustrates the evolution of the power spectrum density (PSD) computed on the horizontal accelerometer sensor. The evolution is mainly monotonic increasing and represents an ideal case where a prediction model can be used with some easy thresholds for RUL estimation. The K-factor computed on the vertical accelerometer signal also depicts a slowly degradation with almost no noise (Fig. 9). K-factor computed on the data of the vertical and horizontal accelerometers.

### C. Sudden degradations

In some cases, the degradation appears suddenly and does not depict a slow monotonic behavior. In this case, finding a prediction model is much more difficult based on those typical health index such as PSD (Fig. 10) or the K-factor (Fig. 11). Therefore, other features have to be imagined.

### D. Theoretical models mismatch

Applying prediction models based on life duration is not relevant. Indeed, the degradation of bearings considered in PRONOSTIA depict very different behaviors leading to very different experiment duration (until the fault). Moreover, the theoretical models based on frequency signatures to detect bearings' faults (such as the inner and outer races and the cage faults) do not work with the data provided by PRONOSTIA. This is because the frequency signatures are difficult to obtain due to the fact that the degradation may concern at a same time all the components of the test bearing. Finally, the existing reliability laws for bearings' life duration, such as the L 10 , do not give same results than those obtained by the experiments (theoretical estimated life durations are different from those given by the experiments).

### E. Level of noise

The level of noise is not controlled and depends on the degradation process. In figures 8 to 11 the level of noise presented different values. There are some cases where this level can be high, possibly explained by the interactions with other parts of the rotating system. Figures 12 and13 depict the crest factor and the PSD for an experiment where the level of noise is particularly high. Figure 14 shows an example of a Wavelet Packet Decomposition (WPD) performed on vibration data provided by an accelerometer. A WPD is a time-frequency technique which permits to adjust the size of the temporal window according to the analyzed frequencies. A WPD has two parameters: a scale parameter a for the frequency and a translation parameter b for the time [19]. By using a WPD, the original vibration signals can be decomposed into several levels and the energy of each level can be calculated.

## V. IEEE PHM 2012 PROGNOSTIC CHALLENGE

### A. Outline of the challenge

The IEEE Reliability Society and Femto-st Institute organize the IEEE PHM 2012 Prognostic Challenge. The challenge is focused on prognostics of the remaining useful life (RUL) of bearings, a critical problem since most of failures of rotating machines are related to these components, strongly affecting availability, security and cost effectiveness of mechanical or power industries.

### B. Aims of the challenge

As for the PHM challenge, 3 different loads were considered:

• First operating conditions: 1800 rpm and 4000 N;

• Second operating conditions: 1650 rpm and 4200 N; • Third operating conditions: 1500 rpm and 5000 N. Participants are provided with 6 run-to-failure datasets in order to build their prognostics models, and are asked to estimate accurately the RUL of 11 remaining bearings (see Table I). Monitoring data of the 11 test bearings are truncated so that participants are supposed to predict the remaining life, and thereby perform RUL estimates. Also, no assumption on the type of failure to be occurred is given. The learning set is quite small while the spread of the life duration of all bearings is very wide (from 1h to 7h). Performing good estimates is thereby quite difficult and this makes the challenge more exciting. Note also that, as stated in IV-D, there is a mismatch between the experiments and the theoretical framework (L 10 law, BPFI, BPFE, etc.).

### C. Scoring of the challenge

Participants are scored based on their RUL results that are converted into percent errors of predictions. Let note RU L i and ActRU L i respectively the remaining useful life of the bearing estimated by a participant, and the actual RUL to be predicted (where i states for the test bearings defined in Table I). The percent error on experiment i is defined by:

%Er i = 100 × ActRU L i -RU L i ActRU L i (1)

Underestimates and overestimates will not be considered in the same manner: good performance of estimates relates to early predictions of RUL (i.e. cases where %Er i > 0), with deduction to early removal, and more severe deductions for RUL estimates that exceed actual component RUL (i.e. cases where %Er i < 0). The score of accuracy of a RUL estimates for experiment i is thereby defined as follows:

A i =

exp -ln(0.5). (Eri/5) if Er i ≤ 0 exp +ln(0.5).(Eri/20) if Er i > 0

Figure 15 depicts the evolution of this scoring function. The final score of all RUL estimates will be defined as being the mean of all experiment's score:

Score = 1 11 11 i=1 (A i )(3)

More details on the objective of the challenge, the scoring of results, the application form, and obviously on the provided datasets, can be found on the home page of the challenge: http://www.femto-st.fr/ieee-PHM2012-data-challenge.

## VI. CONCLUSION

A new experimental platform, called PRONOSTIA, is presented in this paper. Its main purpose is to provide experimental data related to bearings' degradations. These data can then be used to test and verify research methods in the following fields: condition monitoring, fault detection, diagnostic and prognostic. The particularity of this platform is that the bearing's degradation can be realized under constant as well as variable operating conditions and the data are acquired throughout the whole duration of each experiment. Three sets of experimental data realized under three different operating conditions are provided to researchers in order to test their methods for the prediction of the remaining useful life of the degraded bearings. These tests are organized in a form of a challenge where the results of the proposed methods are then assessed and compared. Moreover, the experimental data remain stored in the indicated website to allow verifications by researchers working in the PHM field over the world. Finally, it can be noted that in the three sets of experimental data provided for the organized challenge, each set contains a given number of historical data realized in same operating conditions. So, to be close to the real industrial applications, further works concern online variations of operating conditions within the same experiment.

## Figures et tableaux

**Fig. 1.** Overview of PRONOSTIA.

**Fig. 2.** Shaft support bearing.

**Fig. 4.** The accelerometers and temperature sensor.

**Fig. 5.** Data visualization and Human Interface Machine.

**Fig. 6.** Normal and degraded bearing.

**Fig. 7.** A vibration raw signal.

**Fig. 8.** Power spectrum density (PSD) computed on the data of the horizontal accelerometer.

**Fig. 10.** Power spectrum density (PSD) computed on the data of the horizontal accelerometer.

**Fig. 11.** K-factor computed on the data of the vertical and horizontal accelerometers.

**Fig. 12.** Crest factor computed on the data of the horizontal and vertical accelerometers.

**Fig. 13.** Power spectrum density (PSD) computed on the data of the vertical accelerometer.

8 Fig. 14. Fig. 14. Wavelet Packet Decomposition (WPD) performed on the data of the horizontal accelerometer.

**Fig. 15.** Scoring function of a RUL estimates according to its percent error

**TABLE I** DATASETS OF IEEE PHM 2012 PROGNOSTIC CHALLENGE

     | Operating Conditions
    Data sets | Conditions 1 | Conditions 2 | Conditions 3
    Learning set | Bearing1_1 Bearing1_2 | Bearing2_1 Bearing2_2 | Bearing3_1 Bearing3_2
     | Bearing1_3 | Bearing2_3 | Bearing3_3
     | Bearing1_4 | Bearing2_4 | 
    Test set | Bearing1_5 Bearing1_6 | Bearing2_5 Bearing2_6 | 
     | Bearing1_7 | Bearing2_7 |
