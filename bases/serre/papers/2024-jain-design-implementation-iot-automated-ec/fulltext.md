---
id: 2024-jain-design-implementation-iot-automated-ec
title: "Design and Implementation of an IoT-based automated EC and pH Control System in an NFT-based Hydroponic Farm"
year: 2024
backend: grobid
---

## Abstract

In hydroponics, the growth of plants is primarily dependent on the precise configuration of the nutrient solution supplied to them. Continuous monitoring and control of the nutrients in the hydroponic tank is essential to maintain optimal growth requirements at all times. Manual monitoring and control of the system is inefficient, as it requires human intervention and can lead to errors and variations in the nutrients supplied. This study presents a system to automatically track pH, current nutrient, and water level in the tank and supply the exact amount of pH solution, nutrient solution, and water whenever needed. The proposed system, when integrated with IoT technology, can help achieve better control over the farm and higher productivity with a reduced amount of manual labor.

## INTRODUCTION

Hydroponics is a farming technique that is based on the cultivation of hydroculture plants [1]. In this technique, plants are grown in a water medium, without soil, and all the required mineral nutrients are supplied through the water. Various factors affect plant growth and crop quality in a hydroponic setup, such as pH levels, concentration, and Electrical Conductivity (EC) of the nutrient solution. The pH is an indicator of the acid or alkaline levels of the solution. Each nutrient in the feeding solution responds differently to changes in the pH level of the solution, and thus plant productivity is directly dependent on pH regulation. The concentration of the nutrient-rich solution depends on two factors: the concentration of the solution, expressed as Total Dissolved Solids (TDS) and the conductivity value of the solution stated as EC [2]. TDS represents the combined amount of all organic and inorganic substances present in a liquid, and the EC is the amount of salts present in the liquid. This dissolved salt in the form of cations and anions makes the nutrient solution electrically conductive [2]. The more nutrients present in the water, the higher the concentration, leading to a higher EC and vice versa. Every plant has an ideal EC that is crucial for its growth, and the inability to maintain the EC in the vital optimal range in the nutrient solution adversely affects its growth [3]. Therefore, maintaining the optimal nutrient density in the solution is a critical aspect and is possible by keeping the EC at the ideal level depending on the type of plant being cultivated.

This study presents an algorithm for the automated monitoring and control of the nutrient dosing system for a hydroponic farm by maintaining nutrient solution parameters (pH and EC) throughout the plant growth life cycle with minimal human intervention [4][5]. Similar studies have already been carried out in the field of automated EC and pH control. In [2], fuzzy logic was used to keep EC in the desired range of 1.0-1.5 mS/cm in a hydroponic system based on the nutrient film technique. This method takes the ideal EC value, the current EC value, and the water level as inputs and provides the time duration for which the water or nutrient valves should be turned on. The algorithm was supported by an Android application to remotely control and monitor the hydroponic plants. In [6], a smart irrigation and nutrient supply system was designed by implementing a fuzzy logic controller to maintain the flow of water and acid and basic solutions in the soil to balance its pH and moisture levels. A mobile application was designed to store and display system data. This system was tested on a chili farm and the results showed that plant growth improved compared to an uncontrolled growth medium. In [7], fuzzy logic control was used to design a hydroponic system built on NFT. The image processing of the HSV histogram was applied to predict the ideal EC for the growth cycle of plants. The system was tested in a pakchoy mustard plant and the results showed that it was capable of predicting nutrient levels in agreement with the age of the plant with a fault rate of 8.9%. In [8], a nutrition feeding system was proposed using an Arduino UNO R3 board. This system used the GP2Y0A21 proximity sensors to detect the water level of the feeding tank and a TDS sensor to detect EC levels. The system was successfully tested on a prototype scale to keep the water levels in the tank at the optimal level and feed nutrients when the concentration fell below 800 ppm.

As there is no single solution to automate both EC and pH in a hydroponic farm, this study developed a combined algorithm to continuously maintain the EC and pH levels in an NFT hydroponic farm. In addition, most studies did not consider the effect various kinds of water, such as natural, distilled, or fresh water, on the TDS and EC ratio while automating them in the nutrient solution. This study aimed to evaluate the correlation of TDS and EC for different types of water to simultaneously maintain and monitor them at all times. Furthermore, the prevailing automation algorithms do not consider the total volume of the tank and the current volume of the nutrient solution when deciding to add more water, nutrient solution, or pH solution to manipulate EC and pH. The proposed algorithm uses the size of the nutrient tank as user input from the app, and the current volume of the solution is constantly monitored using an ultrasonic sensor to ensure its effectiveness for farms with variable nutrient tank sizes. II. SYSTEM DESIGN Figure 1 presents the design of the proposed IoT-based hydroponic system with automated EC and pH control. The system contains a NodeMCU microcontroller that executes the proposed algorithm for automated maintenance and control of EC and pH values. NodeMCU receives current data from the ultrasonic, TDS, and pH sensors connected to the hydroponic system and decides, based on the values received, whether any manipulation is necessary for the water level, nutrient density, or pH value of the water in the irrigation tank [9]. For instance, if the optimal pH level of the farm is set between 6 and 7 and at any given time the pH sensor reads the water pH level at 10, then the microcontroller decides that the pH-lowering solution needs to be added to the irrigation tank to bring it to the ideal range. System design.

The automation system calculates the time duration for which the pump attached to the pH-down solution needs to be turned on, and the same signal will be sent to the relay module to switch on pump 4 for the stipulated period. During this period, the pH-lowering solution from the respective tank will be added to the main irrigation tank of the hydroponic NFT system, thus automatically controlling the pH of the water [10]. In the same way, this system can maintain the nutrient concentration of the irrigation tank by adding more nutrient solution if EC levels fall below the ideal range or by adding more water if EC exceeds the ideal range. The algorithms for deciding and calculating the pump-on duration are discussed in the following section [9,[11][12].

## III. AUTOMATION ALGORITHM ON NFT

Maintaining and automatically controlling the nutrient dosing system in an NFT hydroponic farm with minimum human intervention requires automation of two important parameters of the nutrient solution, namely the nutrient density and the pH level of the nutrient solution. Figure 2 shows a diagram of the parameters elaborated below.

### A. Nutrient Density

The density of the nutrients in the water flowing through the NFT system depends on EC and TDS. A higher EC value represents a higher concentration of dissolved nutrients in the water. These two parameters are correlated, and the association is expressed by [13]

: * (1)

where X is the concentration of charged atoms in water and is therefore dependent on the salinity (EC) of the water. This study uses fresh water with EC in the range of 300 to 350 μS/cm for irrigation in the NFT hydroponic farm. Accordingly, the value of X is assumed to be 0.550.

To maintain nutrient density in the ideal range, the system adds more nutrients when TDS falls below the lower bound and adds more water if TDS exceeds the upper bound of the optimal range. The automated TDS control system needs two parameters from the NFT system: the current TDS of the nutrient water in the irrigation tank and the current volume of the irrigation tank. The first parameter is obtained through the TDS sensor attached to the system and the second parameter is obtained by the following equation:

* !" #$ %&' (2)

where V Current is the current level of nutrient water in the irrigation tank, V Tank is the total volume of the tank, H Tank is the height of the irrigation tank and ULT Sensor is the input reading obtained from the ultrasonic sensor attached to the irrigation tank. If the current TDS is less than the lower limit of the optimal range required for plant growth, (3) is applied to calculate the amount of concentrated nutrient solution to be added to the irrigation tank to balance the TDS levels. If the current TDS is greater than the upper limit of the optimal range, then ( 4) is used to calculate the volume of water to be added to the irrigation tank.

( = ! ) ! *(3)

* = ! *(4)

where V Nutrient is the volume of concentrated nutrient solution to be added to the tank, V Water is the volume of water to be added to the tank, TT is the target TDS to be achieved, which is the average of the ideal TDS range, CT is the current TDS obtained from the TDS sensor, NT is the TDS of the concentrated nutrient solution, and V Current is the water level obtained from (2). After obtaining the volume of either nutrients or water to be added, the last step in the EC maintenance algorithm is to send a signal to the relay to turn on pump 1 in case of water and pump 2 in case of nutrients should be added. The duration in which pump 2 remains open to add nutrients to the irrigation tank is calculated using (5), and the duration for pump 1 to open to add water to the irrigation tank is calculated using (6).

### B. pH Level

Two types of pH solutions were used to maintain the pH level in the required range: an acidic solution of pH 3 and a basic solution of pH 9.5. To automate the process of maintaining pH, the system needs the recommended doses of the acidic and basic solutions as input from the user. The concentrated solutions are then diluted by a factor of 10 and stored in separate tanks to maintain the pH of the nutrient tank. The system regularly takes readings from the pH sensor installed in the nutrient water and compares the input value with the ideal range required. When the sensor reading is less than the ideal range, the basic (pH-up) solution is added to the nutrient water, and when the reading is greater than the upper bound of the optimal range, the acidic (pH-down) solution is added to the tank. The amount of acidic or basic solution to be added is calculated using (7). Next, based on the dose, the system calculates the pump-on duration to add the calculated dose to the nutrient tank using (8).

where R rec is the recommended dose of the pH-up and pHdown solutions in 1 liter of water recommended by the manufacturer and given as an input to the system by the user, R V is the calculated dose of pH-up and pH-down solutions according to the current volume (V Current ) of the nutrient tank (recommended doses are diluted by the ration of 10 to 1), Duration pH is the duration of time in seconds for which the pump connected to the respective pH solution should be turned on and FL pH is the flow rate of the pumps connected to the pH solutions.

IV. EXPERIMENTAL ANALYSIS The above automated EC and pH control and maintenance design was implemented through the experimental setup shown in Figure 1 on a small-scale indoor hydroponic NFT system consisting of an irrigation tank for nutrient supply, water for NFT in tank 1 with pump 1 connected to it, concentrated nutrient solution in tank 2 with pump 2 connected to it, and pHup and pH-down solutions in tanks 3 and 4 with pumps 3 and 4 connected to them, respectively. The automation algorithm was implemented in the system and Tables II and III show the experimental results of EC and pH, respectively, taken at random times throughout the day. The results show that the proposed algorithm was able to detect current TDS and pH values and take the required action when the parameters were not in the optimal range. For example, if the pH of the needed irrigation tank is 5.93, which is less than the minimum pH as given by the user, the algorithm turns on the pump connected to the basic solution needs. The relay connected to the required pump was turned on for 11.45 s, which was calculated based on the current pH and the volume of the tank, resulting in a pH value of 6.12 which is in the optimal range. V. RESULT ANALYSIS AND DISCUSSION An efficient automation algorithm is instrumental for a successful hydroponic farm, as manually maintaining farm parameters is a tedious task that can result in errors that can negatively affect crop production. Automation of the EC, TDS, and pH levels of the farm ensures that the NFT system always passes an adequate amount of nutrients to the plant, eliminating human errors. This study proposed an automation algorithm that considers the various types of water used to make nutrient solutions, maintains the EC and pH levels simultaneously without the need for human intervention, and considers the total size of the nutrient tank that allows its implementation farms of different sizes. The algorithm was then applied to a small-scale NFT hydroponic farm on a test-case basis for 10 days, and all farm parameters for nutrient control were examined through the installed sensors. The ideal TDS and pH ranges were taken from the user through a mobile app. In the case study to test the algorithm, the ideal TDS range was set to 750-850 ppm and the ideal pH range was 6.0-6.5 by the user.

The system was able to maintain the resulting TDS level (TT) at an average of 801.4 ppm and the resulting pH level (T pH ) at an average of 6.26 for the duration of the case study, both within the required range. Furthermore, the proposed system can be implemented in other types of precision agriculture, such as aquaponics or aeroponics, with minimal changes.

## VI. CONCLUSION

The EC and pH values of a hydroponic system must be in the ideal range to ensure optimal nutrient absorption and plant growth. Maintaining these parameters in the ideal range at all times requires continuous sensing and precision, as the longer the parameters deviate from the range, the lower the nutrient absorption in plants. Manually sensing and adjusting values needs regular human intervention. An automation algorithm that is capable of sensing parameters at regular intervals and automatically acting to keep them in the ideal range is important for hydroponic farms to produce good-quality crops. The proposed system detects TDS and pH levels through sensors, chooses the action that should be taken if the parameters are not in the required range, calculates the duration for which the action will take place, and finally implements it to bring the parameters in the ideal range. Compared to manual monitoring and control, the proposed automation system is more reliable as it significantly reduces the chances of human error and the need for persistent human support.

## Figures et tableaux

**Fig. 1.** System design.

**Fig. 2.** Design of automated EC and pH control.

where Duration W is the amount of time (s) the pump 1 connected to the water will open, Duration N is the amount of time (s) pump 2, connected to the nutrient solution, will open, V Nutrient and V Water are the volumes obtained from (3) or (4) and FL is the flow rate of the pump in ml/s.

**TABLE I.** CORRELATION OF EC AND TDS IN WATER OF DIFFERENT SALINITY[6]

    Water Type | EC (Measured at 25 °C) | Ratio TDS/EC (X value)
    Natural Water | 500 -3,000 µS/cm | 0.55 -0.75
    Distilled Water | 1 -10 µS/cm | 0.5
    Fresh Water | 300 -800 µS/cm | 0.55

**TABLE II** 

     | . | EXPERIMENTAL RESULTS OF EC CONTROL
    INPUTS: Ideal TDS range =750-850 ppm, TT = 800 ppm, HTank = 50 cm,
     | VTank = 50 l, FLN = 0.6 l/min, NT = 2000 ppm | 
    Vcurrent (l) | Current TDS (CT) | Action needed | Pump ON time (DurationN) | Resulting TDS (TT)
    45.0 | 745 | Nutrient pump ON | 206.25 s | 792
    43.2 | 853 | Water pump ON | 286.2 s | 801
    46.7 | 774 | No action needed | N/A | N/A
    44.5 | 851 | Water pump ON | 283.7 s | 798
    45.3 | 824 | No action needed | N/A | N/A
    43.8 | 748 | Nutrient pump ON | 189.8 s | 796
    47.4 | 797 | No action needed | N/A | N/A
    47 | 856 | Water pump ON | 329 s | 832
    49.2 | 743 | Nutrient pump ON | 233.7 s | 784
    42.6 | 853 | Water pump ON | 282.2 s | 821
    www.etasr. |  |  |  | 

com Jain & Kaur: Design and Implementation of an IoT-based automated EC and pH Control System in …
