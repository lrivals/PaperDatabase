---
id: 2015-helwig-condition-monitoring-complex-hydraulic-system
title: "Condition monitoring of a complex hydraulic system using multivariate statistics"
year: 2015
backend: grobid
---

## Abstract

In this paper, a systematic approach for the automated training of condition monitoring systems for complex hydraulic systems is developed and evaluated. We analyzed different fault scenarios using a test rig that allows simulating a reversible degradation of component's conditions. By analyzing the correlation of features extracted from raw sensor data and the known fault characteristics of experimental obtained data, the most significant features specific to a fault case can be identified. These feature values are transferred to a lowerdimensional discriminant space using linear discriminant analysis (LDA) which allows the classification of fault condition and grade of severity. We successfully implemented and tested the system for a fixed working cycle of the hydraulic system. Furthermore, the classification rate for random load cycles was enhanced by a distribution analysis of feature trends.

## I. INTRODUCTION

Condition monitoring of hydraulic systems has gained increasing importance in industrial, energy, and mobile applications [1,2] as a requirement of condition-based maintenance with several benefits such as reduction of machine downtime and maintenance costs. In general, there are two condition monitoring philosophies: first, the model based approach which requires detailed physical and mathematical knowledge about the system's behavior which is difficult to obtain with sufficient detail for complex systems and, secondly, the statistical approach which is based on analysis of previously observed faults and associated measurement data and requires a sufficient quantity of historical data [3]. The literature contains different approaches for condition monitoring of hydraulic systems using multivariate statistics, e.g. support vector machines, artificial neural networks, decision trees, and semantic-statistical methods. Tchakoua et al. determined vibration analysis (VA) as the most popular and efficient condition monitoring technique for rotating systems such as wind turbines detecting mechanical faults like bearing, shaft, and gearbox defects [4]. However, VA reaches its functional limit for non-rotating systems, e.g. the auxiliary hydraulic system of a gearbox where the analysis of process and performance fluid sensor values is required to identify typical faults like pump problems and oil leakage. Laouti et al. presented a statistical framework for wind turbines based on support vector machines and proposed specific feature vectors to be used for the detection of different actuator and sensor faults which are evaluated with simulated fault training data [5]. An approach for the condition monitoring of a hydraulic power system is proposed by El-Betar et al. [6] analyzing experimentally obtained data with a feedforward artificial neural network detecting internal actuator leakage and valve spool blockage. Furthermore, expert systems for hydraulic systems based on tree hierarchical fault models can be found in literature performing a real-time diagnosis based on threshold analysis of process sensor data [7]. We have previously reported analysis of wind-turbine sensor data using a combination of statistical and semantic data analysis methods for prediction of oil filter replacement and could demonstrate that the training from one system could be transferred to another wind turbine in the same wind park [8]. In this paper, we have used scatter-based supervised learning with automated feature extraction and selection from real process and virtual performance sensor data. This allows the system to adapt to changed conditions such as changes of the hydraulic setup, sensor breakdown or occurrence of a new fault scenario with minimal effort. The final goal of this approach is a method or framework which can easily be adapted to new systems with a minimum of effort for the user.

## II. CONCEPT AND METHODS

In the training phase (Fig. 1), measurement data from several sensors under known fault conditions is required describing the behavior of the machine in presence of a fault. Measurement data are sourced from real sensors installed in hydraulic system (e.g. pressure) as well as virtual sensors which combine different directly measured values using a physical model (e.g. system efficiency or cooling power). Based on this data set, feature extraction is performed by selecting a sensor, a characteristic time interval of the continuously repeated working cycle and by calculating the feature function. This is repeated for all available sensors, All of these features have to be evaluated to determine their significance for detecting a specific fault and its grade of severity. Due to the large quantity of data this evaluation process has to be automated as much as possible and manual evaluation is highly impractical.

Thus, the correlation of features and fault characteristics was automatically analyzed in a batch process using Pearson's correlation coefficient, a method describing the linear correlation of two variables, and Spearman's rank correlation coefficient, which is also suitable for nonlinear dependencies and more robust in the case of outliers [10]. After calculating all fault-feature correlation coefficients, these are sorted according to their absolute value and only the n features with the highest correlation for a specific fault are selected as inputs for calculating a linear discriminant analysis (LDA) [11].

The LDA maximizes the separation between different classes (here: faults and their grades of severity) while minimizing the scatter within a class. This is achieved by maximizing the criterion function

) (w J : w S w w S w w J w T b T = ) ((1)

Here, w describes the projection vector, S b the between-class scatter matrix and S w the within-class scatter matrix that are defined as follows:

= - - = c i T i i i b m m m m N S 1 ) )( ((2)

= = - - = c i N j T i ij i ij w i m x m x S 1 1

) )( ( Here, c is the number of classes, N i the number of observations per class i, i the mean vector of class i, the overall mean and i,j the feature vector j of class i. The resulting LDA coefficient matrix can directly be used to project the feature vector into the low-dimensional discriminant space performing a simple linear combination calculation. Validation of the obtained results is performed with leave-oneout-cross-validation (LOOCV) for cycle-based analysis and random sub-sampling for time window length analysis reducing the computing time. The complete analysis is realized using the respective functions in Matlab R2012. Note that the whole process does not require any user input, so it can be automatically performed for any system.

## III. EXPERIMENTAL SETUP

For the evaluation of the condition monitoring concept we developed a hydraulic test rig that allows a reversible change of the state or condition of various components.

The hydraulic system consists of a primary working (Fig. 2a) and a secondary cooling-filtration circuit (Fig. 2b) which are connected via the oil tank. In the working circuit with main pump MP1 (electrical motor power 3.3 kW), different load levels are cyclically repeated with the proportional pressure relief valve V11. It is possible to test fixed working cycles with pre-defined load levels and also variable working cycles with pseudo-random load variations which are equally distributed within a defined range. The first method represents the typical cyclical operation and repeated load characteristic in an industrial application while random load variations can usually be found in mobile machines.

The test system is equipped with several sensors measuring process values such as pressure (PS1 -PS6), flow (FS1, FS2), temperature (TS1 -TS5), electrical power (EPS1), and vibration (VS1) with standard industrial 20 mA current loop interfaces connected to a data acquisition system. In addition, sensors for particle contamination (CS and MCS [12], COPS [13]) and oil parameter monitoring (COPS) with digital EIA-232 and EIA-485 bus interfaces are integrated. Sampling rates range from 100 Hz (pressure) to 1 Hz (temperature), depending on the dynamics of the underlying physical values.

The sensor data are collected and buffered on a PLC (Beckhoff CX5020) at run time and transferred to a PC via EtherCAT where the data is stored for further analysis. It is possible to configure fault characterization measurements with a specifically developed tool with graphical user interface (LabVIEW) which are subsequently performed by the PLC. Using this tool, different fault states can be defined by fault type, severity, and duration which are then combined on different hierarchical levels to achieve a complex test profile by using, e.g., nested sequences of accumulator, pump and valve fault states combined with different grades of cooler fault (Fig. 3b). Table I shows the components and respective parameters that are configurable to simulate fault scenarios. Through the permutation of fault types and grades the LDA is forced to minimize the cross sensitivity to interfering faults and therefore we expect a robust and selective result that is applicable in practical application. On the other hand, the experimental design has to take into account that a fault does not lead to an immediate system failure but represents a range from first, barely noticeable fault-onsets up to distinct effects on the system depending on the grade of severity of the fault. First, we have studied the LDA results from cycle-based features that are extracted from raw data. The total number of features in the time and frequency domain is 1,323 and 1,197, respectively. The selected time-domain features of the constant working cycle and their correlation coefficients |r| are shown in table II. The cooler features with the highest correlation are median values of cooling efficiency, a virtual sensor calculated from the ratio T of oil at cooler and T of TS3 and ambient temperature, and cooling power, a virtual sensor calculated from heat transport equation of oil at the cooler, with values close to 1. The features for the valve condition are primarily extracted from the values of neighboring pressure sensors at time intervals during switching processes also show fairly high correlation of 0.98 to 0.84. In comparison, feature-fault correlations for pump and accumulator faults are significantly lower. Especially the pump features which are primarily extracted from efficiency and flow values at constant load levels (odd interval numbers) are strongly affected by the interfering oil temperature change leading to low fault correlations values of only 0.42 to as low as 0.26. Suitable features for detecting gas leakage of the hydraulic accumulator are mainly based on flow and pressure values during pressure step intervals (even interval numbers) and show medium correlation levels (0.69 to 0.37). Table III compares the achieved cycle-based classification rates based on fixed or random working cycles, time or frequency domain features and Pearson's or Spearman's correlation coefficient. The fault case cooling degradation is not affected by the random load, which is immediately evident due to the position of the cooler in a separate circuit. However, it is remarkable that the valve monitoring is equally effective for fixed and random cycles, i.e. the fault diagnosis does not depend on the load level at the switching operation. Comparison between the correlation coefficients Pearson's r for linear correlation and Spearman's rank correlation coefficient as criterion for the feature selection from the pool of the computed features shows that their classification results are at approximately the same level. However, Spearman's tends to be more suitable for challenging data sets, i.e. those with low classification rates, which is probably due to its robustness in the face of outliers. Comparing time and frequency domain features, the achieved classification rates are similar for the fixed working cycles but the classification rate achieved with frequency domain features decreases more strongly for the random load working cycles. In general, the random load cycles lead to the selection of load-independent features and subsequent classification is more challenging especially for internal pump leakage and accumulator gas pre-charge pressure. IV), so there is still room for improvement. In order to improve the result, further features of the machine's behavior were extracted from the cycle feature distribution over several working cycles. Again, the features with highest correlation were selected for each window length.

Using batch processing, a variable time window (1 to 60 cycles) was iterated through each feature variation with time.

Due to the large number of test cycles, the worst case ratio of features vs. observations is 1:80, which is still sufficiently low to eliminate over-fitting of data, i.e. interpreting random noise as significant results. In addition, the influence of the number of selected best correlating features for the LDA-based classification was evaluated. The classification rate can be improved by approx. 25 % for the fault scenario pump leakage (20 features, fig. 4) and even by 40 % for the fault scenario accumulator gas leakage (20 features, fig. 5) .

The main drawback, i.e. slower analysis due to the larger time window required for the classification, is not critical for practical application since both fault progressions are also slow due to slow degradation of the pump or low leak rates of the accumulator. In both fault-cases, the higher the number of considered features and the greater the length of cycle windows in the studied range are chosen, the better the resulting classification rate is (figs. 4,5). Fig. 6 shows the resulting LDA projections with increasing cycle window length clearly indicating the improved separation between the different classes for the monitoring of accumulator gas pre-charge pressure corresponding to fig. 5.

## V. CONCLUSION

We developed a flexible and versatile condition monitoring system based on statistical data evaluation and supervised classification based on LDA with automated feature extraction and selection using correlation criteria to the fault scenarios to be diagnosed. The approach is based on existing process sensors, but can also make use of additional sensors and can thus be easily adapted to different systems due to the fully automated signal processing scheme. Currently, a similarly universal method for condition monitoring of hydraulic systems covering the mentioned aspects cannot be found in literature to the best of our knowledge. The approach is based on direct measurement of process values, i.e. pressure, flow rate, vibration, electrical power and temperatures, but also on virtual sensors describing physically relevant values, which cannot be measured directly like system and cooling efficiency. Thus, the selected method combines typical condition monitoring approaches based on physical modelling and statistical data evaluation. The selected approach has proven suitable for the detection of different types of faults that exhibit typical symptoms over a wide time scale from milliseconds up to hours and can be used to estimate the grade of severity of the fault. The method was successfully evaluated with a hydraulic test rig using fixed and pseudorandom working cycles simulating industrial and mobile machinery applications, respectively. Due to the combined simulation and superposition of disturbances from different fault scenarios (e.g. oil temperature) in the LDA training, the fault-grade detection is highly selective and insensitive to interference effects. Furthermore, classification deficiencies especially observed for random working cycles were remedied by the analysis of the feature distribution over a longer time window. The system can be expanded to include more fault conditions and grades by repeating the automated analysis, thus allowing an open approach. In addition, the condition monitoring can be continuously improved by taking online measurements during normal operation and offline condition evaluation of the system, i.e. during regular maintenance, into account.

## Figures et tableaux

**Fig. 1** Concept of training of the condition monitoring system.

**Fig. 2.** Hydraulic system for training data collection: (a) working circuit with main pump MP1 with switchable orifice V9, switchable accumulators A1-A4 with different precharge pressures and variable load V11, (b) cooling and filtration circuit with cooler C1.

**Fig. 3.** (a) Fixed working cycle (measured by PS1) with pre-defined load steps with time intervals 1-13 for feature extraction; when using the variable working cycle the load levels (5,7,9,11,13) are generated randomly within the range 120 to 140 bar, (b) fault condition characterization measurement with superposition of different fault types. Transients between fault conditions are excluded.

**Fig. 6.** LDA projected features of random working cycle and accumulator gas leakage monitoring dependent on cycle window length (time domain features, number of features: 20).

**Fig. 4.** Classification rate of internal pump leakage training data vs. cycle window length and number of features (random sub-sampling with 20 cycles and 20 experiments, time domain features, feature selection by Pearson's correlation coefficient, random load working cycle).

**Fig. 5.** Classification rate of accumulator gas leakage training data vs. cycle window length and number of features (random sub-sampling with 20 cycles and 20 experiments, time domain features, feature selection by Pearson's correlation coefficient, random load working cycle).

**TABLE II.** FAULT SPECIFIC MOST CORRELATED FEATURES (CONSTANT WORKING CYCLE) WITH SENSOR (SNS, FIG. 2), TIME INTERVALS WITHIN CYCLE (INT, FIG. 3A) AND FUNCTIONS (FCT) MEDIAN (ME), VARIANCE (VA), SLOPE (SL), POSITION OF MAXIMUM (PO), SKEWNESS (SK) AND KURTOSIS (KU).

     | Cooler features |  |  | Valve features |  |  | Pump features |  | Accumulator features | 
    Sns | Fct | Int | |r| | Sns | Fct | Int | |r| | Sns | Fct | Int | |r| | Sns | Fct | Int | |r|
    * | Me | 10 | 0.99 | PS1 | Va | 4 | 0.98 | FS1 | Me | 5 | 0.42 | EPS1 | Sk | 12 | 0.69
    * | Me | 12 | 0.99 | PS2 | Me | 4 | 0.96 | *** | Me | 8 | 0.38 | PS2 | Me | 3 | 0.66
    * | Me | 2 | 0.99 | PS2 | Va | 3 | 0.96 | FS1 | Va | 9 | 0.34 | FS1 | Sl | 12 | 0.61
    * | Me | 4 | 0.99 | PS2 | Sk | 3 | 0.95 | *** | Me | 13 | 0.34 | FS1 | Va | 1 | 0.59
    * | Me | 8 | 0.99 | PS2 | Ku | 3 | 0.95 | *** | Me | 9 | 0.34 | FS1 | Ku | 12 | 0.59
    * | Me | 11 | 0.99 | PS1 | Sl | 4 | 0.95 | *** | Me | 1 | 0.34 | *** | Sk | 6 | 0.59
    * | Me | 6 | 0.99 | *** | Me | 4 | 0.93 | *** | Me | 2 | 0.33 | *** | Sk | 12 | 0.58
    * | Me | 1 | 0.99 | FS1 | Sk | 3 | 0.92 | *** | Me | 10 | 0.31 | PS2 | Ku | 6 | 0.58
    * | Me | 9 | 0.99 | PS3 | Sk | 3 | 0.92 | FS1 | Me | 9 | 0.31 | PS1 | Ku | 12 | 0.57
    * | Me | 13 | 0.99 | PS2 | Sk | 4 | 0.92 | PS3 | Me | 11 | 0.31 | FS1 | Va | 6 | 0.56
    * | Me | 3 | 0.99 | PS3 | Ku | 3 | 0.9 | PS3 | Me | 9 | 0.3 | EPS1 | Sk | 6 | 0.55
    * | Me | 5 | 0.99 | PS1 | Me | 4 | 0.89 | PS3 | Me | 8 | 0.3 | FS1 | Sk | 12 | 0.55
    * | Me | 7 | 0.99 | PS3 | Me | 4 | 0.88 | FS1 | Me | 11 | 0.29 | PS3 | Me | 3 | 0.54
    ** | Me | 10 | 0.99 | FS1 | Ku | 3 | 0.87 | FS1 | Me | 10 | 0.29 | PS1 | Ku | 6 | 0.53
    ** | Me | 12 | 0.99 | *** | Va | 3 | 0.85 | *** | Me | 11 | 0.28 | FS1 | Po | 12 | 0.53
    ** | Me | 4 | 0.99 | FS1 | Sl | 4 | 0.85 | FS1 | Me | 8 | 0.28 | PS1 | Va | 2 | 0.51
    ** | Me | 2 | 0.99 | EPS1 | Sl | 4 | 0.85 | FS1 | Me | 1 | 0.26 | PS1 | Sk | 12 | 0.41
    ** | Me | 6 | 0.99 | *** | Ku | 3 | 0.84 | PS3 | Me | 1 | 0.26 | PS1 | Sk | 6 | 0.37
    *Virtual sensor: cooling efficiency with TS3, TS4, Tamb, ** Virtual sensor: cooling power with TS3, TS4, FS2, *** Virtual Sensor: system efficiency with
     |  |  |  |  |  |  | EPS1, FS1 and PS2 |  |  |  |  |  |  | 

**TABLE I** 

    . | HYDRAULIC TEST RIG: COMPONENTS AND THEIR SIMULATED
     |  | FAULT CONDITIONS. | 
    Comp. | Condition | Contr. parameter | Possible Range
    Cooler | Cooling | Fan duty cycle of C1 | 0…100 %
    C1 | power |  | (0.6…2.2 kW)
     | decrease |  | 
    Valve | Switching | Control current of V10 | 0…100 % of
    V10 | charact. |  | nom. current.
     | degradation |  | 
    Pump | Internal | Switchable bypass | 3 x 0.2 mm,
    MP1 | leakage | orifices (V9) | 3 x 0.25 mm
    Acc. | Gas leakage | Accumulators A1-A4 | 90, 100, 110,
    (A1-A4) |  | with different pre- | 115 bar
     |  | charge pressures | 
     |  | IV. RESULTS | 
    Fig. 3a shows the fixed working cycle with a duration of 60
    seconds, which is divided into 13 time intervals for which the
    different features are extracted from the measurement values.
    The variable working cycle also has a duration of 60 seconds
    but is based on pseudo-random load levels during each cycle.

**TABLE III** CLASSIFICATION RATES IN PERCENT (BASED ON LOOCV WITH MAHALANOBIS DISTANCE CLASSIFIER AND 20 FEATURES) OF COMPONENT'S CONDITIONS DEPENDING ON WORKING CYCLE, FEATURE DOMAIN AND CORRELATION COEFFICIENT FOR FEATURE SELECTION. [corps du tableau reconstruit par PyMuPDF : à vérifier]

    Working cycle |  | fixed |  | pseudo-random | 
    Corr.-coefficient |  | r |  | r | 
    Time domain features | Cooler | 100.0 | 100.0 | 100.0 | 100.0
     | Valve | 100.0 | 100.0 | 100.0 | 100.0
     | Pump | 97.9 | 98.0 | 72.3 | 73.6
     | Acc. | 90.4 | 88.8 | 54.2 | 54.0
    Freq. domain features | Cooler | 100.0 | 100.0 | 100.0 | 100.0
     | Valve | 99.3 | 99.6 | 49.4 | 61.3
     | Pump | 97.7 | 96.8 | 49.9 | 50.3
     | Acc. | 72.4 | 78.2 | 50.5 | 53.4

cycle fixed pseudo-random Corr.-coefficient r r Time domain features

     | Cooler | 100.0 | 100.0 | 100.0 | 100.0
     | Valve | 100.0 | 100.0 | 100.0 | 100.0
     | Pump | 97.9 | 98.0 | 72.3 | 73.6
     | Acc. | 90.4 | 88.8 | 54.2 | 54.0
    Freq. | Cooler | 100.0 | 100.0 | 100.0 | 100.0
    domain | Valve | 99.3 | 99.6 | 49.4 | 61.3
    features | Pump | 97.7 | 96.8 | 49.9 | 50.3
     | Acc. | 72.4 | 78.2 | 50.5 | 53.4
    Table III revealed unsatisfactory classification results,
    especially for pump and accumulator monitoring during
    random load working cycles based on LDA combined with
    Mahalonobis distance classification. Alternative state-of-the-
    art classification methods such as artificial neural networks
    (ANN) and support vector machines (SVM) do not improve
    significantly the classification rates for random cycle data
    (Table |  |  |  |  | 

**TABLE IV** CLASSIFICATION RATES IN PERCENT (20 FEATURES) FOR LDA COMPARED TO ALTERNATIVE CLASSIFIERS: ARTIFICIAL NEURAL NETWORKS (ANN, MULTILAYER PERCEPTRON WITH 5 HIDDEN LAYERS) AND SUPPORT VECTOR MACHINES (SVM, USING ONE-VS-ALL WITH LINEAR AND RBF KERNEL), RANDOM WORKING CYCLE MEASUREMENT, TIME DOMAIN AND CORRELATION COEFFICIENT FOR FEATURE SELECTION.

     | LDA | ANN | SVM | SVM
     |  |  | (linear) | (RBF)
    Cooler | 100 | 100 | 100 | 100
    Valve | 100 | 100 | 100 | 95.7
    Pump | 73.6 | 80.0 | 72.4 | 64.2
    Accumulator 54.0 | 50.4 | 51.6 | 65.7
    Mean | 81.9 | 82.6 | 81.0 | 81.4
