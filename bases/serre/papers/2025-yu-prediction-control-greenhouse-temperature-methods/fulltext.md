---
id: 2025-yu-prediction-control-greenhouse-temperature-methods
title: "Prediction and control of greenhouse temperature: Methods, applications, and future directions"
year: 2025
backend: grobid
---

## Abstract

Greenhouse cultivation is crucial for global food security and sustainable agricultural development. To maintain efficient greenhouse crop production, temperature management is the core. For a better understanding of the current status, methods, applications, and future directions for greenhouse prediction and control, this paper provides a comprehensive review of different technologies for greenhouse temperature management. The contributions cover three key aspects: (1) The role of different sensing techniques, the Internet of Things, wireless sensor networks, and multimodal data fusion technologies in supporting greenhouse temperature management; (2) Status and advantages of traditional models, artificial intelligent (AI)-based models, and hybrid models for greenhouse temperature prediction; (3) Applicable scenarios and limitations of different control methods, such as fuzzy logic, model predictive control (MPC), reinforcement learning (RL) and intelligent systems for greenhouse temperature control. Comparative analysis demonstrates that deep learning models excel in greenhouse temperature prediction, while fuzzy logic, MPC, and RL exhibit unique strengths in greenhouse temperature control. Despite the potential demonstrated by advanced AI technology in greenhouse temperature management, practical applications continue to encounter challenges such as model robustness, interpretability, and computational efficiency. To fully exploit the potential of AI, future research should focus on developing plant-centric AI models, exploring the application of AI in sustainable energy management of greenhouses, and developing digital twin models to promote the development of AI and greenhouse technology, creating a new paradigm for sustainable, resilient, and intelligent agriculture. This review offers a comprehensive perspective on optimizing greenhouse environment management, which is crucial to address challenges in food security and climate change.

## 1. Introduction

The global population is projected to reach 9.7 billion by 2050, necessitating a substantial increase in agricultural productivity to ensure food security while minimizing the environmental impact of crop production (Molotoks et al., 2021). Greenhouse horticulture has emerged as a promising solution to meet this growing demand, providing a controlled environment for year-round crop cultivation that optimizes resource use efficiency and protects crops from adverse weather conditions, pests, and diseases (Achour et al., 2021;Maraveas et al., 2022). By decoupling crop production from seasonal and geographical constraints, greenhouse cultivation enables the sustainable intensification of food production in regions where open-field cultivation is not feasible or efficient (Gruda et al., 2019;Nemali, 2022;Zhou et al., 2021). Studies have demonstrated that greenhouse can reduce water consumption by up to 50%-90% (Czyzyk et al., 2014) and increase crop yields by 2.17 times compared to open-field cultivation (Mishra et al., 2020), highlighting its potential to address the challenges of water scarcity and land use competition in the face of climate change and population growth.

Temperature control is a critical factor in determining the success of greenhouse crop production, as it directly influences plant physiological processes such as photosynthesis, respiration, transpiration, and nutrient uptake (Boote et al., 2013). While temperature and humidity are closely coupled in greenhouse environments, this study focuses primarily on temperature control due to its significant impact on crop growth, while acknowledging their interdependence.

Maintaining optimal temperature ranges is essential to maximize crop yield and quality while minimizing the risk of physiological disorders and diseases (Bisbis et al., 2018). The relationship between temperature and crop performance is complex and non-linear, with different crops having specific temperature requirements for various stages of growth and physiological processes (Wang et al., 2017). For example, a review by Shamshiri et al. (2018) indicates that the ideal daytime temperature for tomatoes should be maintained between 21-29.5 • C, while the nighttime temperature should be kept within 18.5-21 • C. Maintaining these temperatures promotes photosynthesis, ensures pollen viability, and supports fruit development. Deviations from these temperature ranges may inhibit plant growth, pollen sterility, or decreased fruit quality. Similarly, lettuce plants thrive with a daytime temperature of 22-26 • C and a nighttime temperature of 15-20 • C for optimal head formation and quality (Blanchard and Runkle, 2011;Adeyemi et al., 2018;Kumazaki, 2022). Deviations from these optimal temperature ranges can lead to suboptimal growth, reduced yield, and increased susceptibility to pests and diseases (Velásquez et al., 2018). Therefore, precise temperature control is essential for high-yield and high-quality cultivation in a greenhouse.

Precise temperature control strategies are also crucial for reducing energy consumption and promoting sustainable greenhouse practices (Gruda et al., 2019;Bersani et al., 2021). Heating and cooling systems account for a substantial portion of total energy consumption in greenhouses, ranging from 50%-80% depending on the climate and type of greenhouse (Zhang et al., 2022;Cuce et al., 2016). The energy demand for temperature control is influenced by various factors, such as greenhouse design, insulation properties, ventilation rate, and crop temperature requirements (Ghoulem et al., 2019). Studies have shown that implementing advanced temperature control strategies, such as model predictive control (MPC), can reduce energy consumption by 30% compared to conventional on/off control while maintaining optimal crop growth conditions (Ding et al., 2018b). In addition, integrating renewable energy systems, such as solar thermal collectors and geothermal heat pumps, can further reduce the carbon footprint and operating costs of greenhouse temperature control (Cuce et al., 2016). Table 1 summarizes the significance of greenhouse temperature prediction and control.

The evolution of greenhouse temperature control has been closely intertwined with advancements in technology, particularly in the field of artificial intelligence (AI) (Fig. 1). The journey from traditional manual control to AI-driven smart greenhouses spans several decades, marked by significant technological milestones (Tijerina et al., 2024;Subeesh and Mehta, 2021). Although AI concepts emerged in the 1950s, their practical application in greenhouse management was initially limited due to insufficient sensing and computing capabilities (Araújo et al., 2023;de Oliveira and e Silva, 2023). In the early stages, greenhouse temperature control relied on rule-based methods derived from Importance of greenhouse temperature prediction and control.

### List of Abbreviations

AI

### Aspect Significance Reference

Plant growth -Ensures optimal photosynthesis and respiration -Enhances yield and quality -Reduces physiological disorders and diseases Ali et al. (2021) and Körner et al. (2009) Energy efficiency -Accounts for 65%-85% of greenhouse energy use -Can reduce energy consumption by 30% Zhang et al. (2020) and Ahamed et al. (2019) Environmental impact -Lowers carbon footprint and operating costs -Promotes sustainable practices Balafoutis et al. (2017) resource efficiency -Optimizes water and nutrient usage -Minimizes waste and pollution Czyzyk et al. (2014) and Achour et al. (2020) Crop resilience -Protects against extreme weather and climate change -Improves adaptability to changing conditions Fei et al. (2024) and Gruda et al. (2019) natural conditions and human experience. The introduction of basic automation in the 1950s-1980s marked the beginning of modern greenhouse technology (Nemali, 2022). The 1980s-2000s saw the integration of computer systems and PID (Proportional-Integral-Derivative) controllers, enabling more precise temperature management and marking a critical step towards precision agriculture (Yuen Fong Chan et al., 2007;Precision Agriculture Science and Technology, 2023). The advent of sensor technologies and the Internet of Things (IoT) in the 2000s-2010s facilitated real-time data collection and remote monitoring, with wireless sensor networks (WSN) and cloud computing laying the essential infrastructure for data-driven approaches (Bersani et al., 2022;Al-Fuqaha et al., 2015). It was not until the 2010s, with the rise of big data analytics and machine learning, that AI began to show its full potential in greenhouse management, with early applications of support vector machines (SVM) and artificial neural networks (ANN) for environmental prediction (Araújo et al., 2023). This period saw an increasing focus on predictive modeling and resource optimization. In the 2020s, we are witnessing the emergence of AI-driven smart greenhouses, where AI is the core technology for comprehensive environmental control (Subeesh and Mehta, 2021). The current wave of AI applications in greenhouse temperature control offers unprecedented opportunities to optimize crop production, resource use efficiency, and sustainability (Hoseinzadeh and Garcia, 2024). Advanced AI techniques, including deep learning and RL, revolutionize greenhouse environmental management by enabling data-driven decision-making, adaptive control, and autonomous optimization (Jin et al., 2021;Ajagekar and You, 2022a). This evolution reflects technological progress and a paradigm shift towards more intelligent and sustainable agricultural practices.

The application of AI in greenhouse temperature control presents a significant opportunity to address the challenges of sustainable food production in the face of climate change, population growth, and resource scarcity. By leveraging the power of AI techniques, such as machine learning, deep learning, and advanced control strategies, greenhouse growers can optimize crop yield, quality, and resource use efficiency while reducing energy consumption and environmental impacts (Rizwan et al., 2023). However, despite the promising potential of AI in greenhouse temperature control, several challenges and limitations need to be addressed. Developing accurate and reliable AI models requires high-quality data, which may be difficult or expensive to obtain in practice (Guo et al., 2021;De Melo et al., 2022). The interpretability and transparency of AI models, intense learning models, are often limited, making it challenging for growers and operators to understand and trust the model predictions and control actions (Li et al., 2022b;Vellido, 2020). Moreover, integrating AI-based control systems with existing greenhouse infrastructure and management practices may require significant investments and technical expertise (Guzman et al., 2023;Ajagekar et al., 2023). To address these challenges and realize the full potential of AI in greenhouse temperature control, interdisciplinary research efforts and collaborations are needed in the fields of plant science, engineering, computer science, and social science (Ullah et al., 2022). The development of explainable, adaptive, and scalable AI models that can incorporate domain knowledge and expert feedback, coupled with the advancement of sensing technologies and decision support tools, will be crucial for the successful implementation of AIbased greenhouse management systems in real-world settings (Marvin et al., 2022;Sabrina et al., 2022). By bridging the gap between AI and greenhouse cultivation, we can harness the power of data-driven decision-making and autonomous optimization to create a more sustainable and productive food system for the future (Marvin et al., 2022).

To conduct this review comprehensively, we collected research information from major scientific databases including Web of Science, Scopus, IEEE Xplore, and Google Scholar using combinations of keywords such as 'greenhouse temperature prediction', 'greenhouse climate control', 'artificial intelligence greenhouse', 'deep learning temperature forecasting', and 'smart greenhouse systems.' Boolean operators (AND, OR) were used to connect these terms. Our review primarily focused on peer-reviewed articles published between 2000-2025, with an emphasis on developments from the past decade. Only Englishlanguage peer-reviewed publications were included, while preprints, theses, and non-academic sources were generally excluded unless containing significant empirical data unavailable elsewhere. The selection criteria prioritized studies that reported quantitative performance metrics (e.g., RMSE, MAE, R 2 , energy savings), clearly described methodologies, and presented empirical validation. We organized the literature according to methodological approaches (traditional models, AI-based methods, and hybrid systems) and systematically compared them based on prediction accuracy, computational requirements, implementation complexity, and practical applicability. Special attention was given to studies that demonstrated innovative integration of multiple technologies or addressed significant challenges in greenhouse temperature management.

While several reviews have previously explored aspects of greenhouse climate control (Shamshiri et al., 2018;Marvin et al., 2022), most have focused separately on either traditional models or AI technologies without providing an integrated perspective on sensing, prediction, and control systems. There remains a critical need for a comprehensive review that unites these aspects and charts future directions for sustainable intelligent greenhouse systems, especially given the recent rapid advancements in deep learning and reinforcement learning applications in agriculture. This review is uniquely positioned to serve researchers, engineers, and policymakers by bridging the gap between cuttingedge AI research and practical greenhouse management, addressing urgent challenges in global food security and climate-resilient agriculture through a holistic analysis of sensing technologies, prediction models, and control strategies.

To provide a better and more comprehensive understanding of the current status, methods, applications, and future directions for greenhouse prediction and control, this paper offers a detailed review of different sensing, prediction, and control methods for greenhouse temperature management, including a comparative analysis as well as future directions for each aspect. The following chapters are organized as follows: Section 2 provides an overview of sensing technologies in greenhouse temperature management; Section 3 analyzes traditional methods for greenhouse temperature prediction, while Section 4 reviews AI-based methods; and Section 5 covers different approaches for greenhouse temperature control. Future research directions and conclusions are presented in Sections 6 and 7.

## 2. Sensing technology in Greenhouse temperature management

The advent of data-driven technologies, including the IoT, WSNs, and sophisticated data fusion techniques, has revolutionized greenhouse temperature management. These innovations enable precise monitoring, efficient data processing, and intelligent control of environmental conditions, thereby optimizing agricultural productivity. The increasing adoption of IoT and sensor technologies in greenhouse has enabled the collection of vast amounts of real-time data on environmental parameters, crop growth, and resource consumption (Maraveas et al., 2022). These data-driven approaches provide unprecedented opportunities to optimize greenhouse management and decision-making using AI techniques (Elijah et al., 2018). This section delves into critical advancements in data-driven technology for greenhouse temperature management, emphasizing IoT and sensor technology, data acquisition and processing techniques, and multimodal data fusion approaches.

Greenhouse sensors utilize various physical principles to measure environmental parameters: temperature sensors employ resistive, thermocouple, or infrared mechanisms; humidity sensors detect moistureinduced electrical changes; and light sensors convert photonic energy to electrical signals. These sensors target properties directly influencing plant physiology, with integrated sensor systems combining multiple measurement capabilities into unified platforms for comprehensive monitoring of the greenhouse microclimate.

### 2.1. Data acquisition and processing techniques

Data acquisition and processing techniques in greenhouse temperature control integrate sensors, microcontrollers, and communication technologies to ensure optimal environmental conditions for plant growth. Various systems employ diverse sensors to measure temperature, humidity, soil pH, CO 2 concentration, and light intensity, as detailed in Table 2.

These technologies collectively enhance the efficiency, accuracy, and automation of greenhouse temperature control, improving crop management and productivity. By leveraging advanced sensors, microcontrollers, and communication technologies, these systems enable precise data acquisition, real-time monitoring, and intelligent control of environmental conditions.

### 2.2. Multimodal data fusion technology

Multimodal fusion integrates data from diverse sensors to provide comprehensive environmental representation, operating at three levels: data-level (raw sensor readings), feature-level (extracted characteristics), and decision-level (integrated outputs). This approach overcomes individual sensor limitations through weighted averaging, Kalman filtering, Bayesian methods, or deep learning techniques, enabling more accurate environmental assessment despite complex parameter interactions. Multimodal data fusion technology is crucial in refining greenhouse temperature control and fostering optimal crop growth conditions. This technology affords a holistic understanding of the greenhouse environment by merging data from multiple sensors that monitor parameters such as temperature, humidity, CO 2 concentration, and solar radiation. Table 3 outlines various multimodal data fusion techniques and their specific applications in greenhouse temperature management.

The development and application of multimodal data fusion technology in greenhouse systems emphasize its importance in intelligent control systems. It addresses key challenges in data fusion processes and optimizes environmental parameter adjustments for enhanced crop growth and economic benefits.

### 2.3. Impact of multimodal data fusion on temperature prediction and control

The integration of multimodal data fusion has shown vast potential in enhancing temperature prediction and control by utilizing complementary information from various data sources. For instance, the Deep Multimodal Encoder (DME) framework, similar to the neural network models for data fusion mentioned in Table 3, has exhibited outstanding performance in sensor data compression and missing data imputation. This framework achieves a root RMSE of merely 20% compared to traditional methods like K-nearest neighbors and sparse principal component analysis, and it reconstructs temperature modalities from humidity and illuminance data with an RMSE of 7 • C from highly compressed data (Liu et al., 2017). Additionally, the stacked autoencoder approach, which aligns with the adaptive weighted fusion techniques in Table 3, has proven effective in extracting critical features from multimodal sensor data, leading to more than a 45% improvement in RMSE for regression tasks over linear approaches and up to a 10% improvement over shallow neural network methods (Zhang et al., 2015).

The SSAE-LSTM model further enhances prediction performance by mining the inherent correlation features of multimodal data, yielding superior precision, accuracy, recall, and F-score compared to other neural networks (Zhu et al., 2021). Furthermore, the dynamic multimodal fusion (DynMM) approach adapts to the computational demands of different multimodal data, reducing computation costs by 46.5% with negligible accuracy loss in sentiment analysis and achieving a +0.7% mIoU improvement in RGB-D semantic segmentation (Xue and Marculescu, 2023). The nonparametric multivariate empirical mode decomposition (EMD) method also shows promise in process monitoring and control by decomposing signals into intrinsic mode functions, aiding in the construction of control charts for monitoring process dynamics in ultraprecision machining processes (Shen et al., 2019). Collecting data on environmental factors, flower names, and growth status also enables greenhouse managers to manage crop growth more effectively (Lin et al., 2022).

These advancements highlight the efficacy of multimodal data fusion in refining temperature prediction and control. They offer robust and precise models that outperform traditional methods and singlemodality approaches. By utilizing complementary information from various data sources, multimodal data fusion techniques enable more accurate and efficient control of greenhouse environmental conditions, ultimately enhancing crop growth and productivity. However, the heterogeneity and multimodality of the data generated by different sensors and platforms pose significant challenges for data integration, fusion, and analysis (Li et al., 2022a). Advanced data fusion techniques, such as Bayesian networks, Dempster-Shafer theory, and deep learning, can be used to combine data from multiple sources and modalities, such as environmental sensors, imaging sensors, and remote sensing platforms, to provide a more comprehensive and accurate understanding of the greenhouse environment and crop growth dynamics (Meng et al., 2020). Moreover, the application of self-supervised learning and transfer learning techniques can enable the development of scalable and adaptable AI models that can learn from unlabeled data and transfer knowledge across different greenhouse environments and crop types (Moon and Eek Son, 2021;Luo et al., 2024).

## 3. Traditional methods for greenhouse temperature prediction

Developing temperature prediction models requires a deep understanding of the underlying physical and biological processes that dominate greenhouse energy and mass transfer (Hu and You, 2024). This section focuses on conventional approaches to greenhouse temperature prediction, including mechanistic models based on physical principles and early machine learning applications that preceded the advanced AI techniques discussed in Section 4.

Traditional mechanistic models, such as energy balance models and computational fluid dynamics (CFD) models, can provide valuable information on complex heat and mass transfer phenomena in greenhouses, such as convective and radiative heat exchange between the crop canopy, the greenhouse cover, and the surrounding environment (Bournet and Rojano, 2022). These mechanistic models can generate synthetic data for training and validating AI models and incorporate physical constraints and domain knowledge into the learning process (De Melo et al., 2022). While AI-based prediction models can leverage the vast amounts of data generated by IoT sensors and remote sensing platforms to provide accurate and timely forecasts of greenhouse temperature dynamics, taking into account the complex interactions among crops, climate, and management practices (Ayoub Shaikh et al., 2022). These prediction models can optimize temperature control strategies in real-time, anticipating disturbances and adapting to changing environmental conditions (Gholamzadehmir et al., 2020;Ajagekar and You, 2022a). Hybrid models that combine various approaches, such as mechanical models, AI techniques, and their combinations, have shown promising results in improving the accuracy, interpretability, and adaptability of temperature predictions and control strategies while leveraging the strengths of different modeling paradigms to address the challenges associated with data requirements, computational costs, and system complexity (Eredics and Dobrowiecki, 2010;Fan et al., 2019).

This section provides a comprehensive overview of different traditional, AI-based, and hybrid models for greenhouse temperature prediction and control, including their applicable scenarios, limitations, advantages, comparative analysis, and future ditections.

### 3.1. Greenhouse temperature prediction methods

#### 3.1.1. Mechanism modeling

The system dynamics model describes the dynamic behavior of greenhouse temperature using differential equations, such as the one shown in Eq. (1).

𝑑𝑇 𝑖𝑛 𝑑𝑡 = 1 𝐶 𝑔 ( 𝑄 𝑠𝑜𝑙𝑎𝑟 + 𝑄 ℎ𝑒𝑎𝑡𝑖𝑛𝑔 -𝑄 𝑣𝑒𝑛𝑡𝑖𝑙𝑎𝑡𝑖𝑜𝑛 -𝑄 𝑐𝑜𝑣𝑒𝑟 )(1)

where 𝑇 𝑖𝑛 is the indoor air temperature, 𝐶 𝑔 is the heat capacity of the greenhouse, 𝑄 𝑠𝑜𝑙𝑎𝑟 is the solar radiation heat gain, 𝑄 ℎ𝑒𝑎𝑡𝑖𝑛𝑔 is the heat input from the heating system, 𝑄 𝑣𝑒𝑛𝑡𝑖𝑙𝑎𝑡𝑖𝑜𝑛 is the heat loss due to ventilation, and 𝑄 𝑐𝑜𝑣𝑒𝑟 is the heat loss through the greenhouse cover.

The energy balance model focuses on the energy flows and temperature changes in the greenhouse, considering the net energy gain or loss as expressed in Eq. (2).

𝑄 𝑛𝑒𝑡 = 𝑄 𝑠𝑜𝑙𝑎𝑟 + 𝑄 ℎ𝑒𝑎𝑡𝑖𝑛𝑔 -𝑄 𝑣𝑒𝑛𝑡𝑖𝑙𝑎𝑡𝑖𝑜𝑛 -𝑄 𝑐𝑜𝑣𝑒𝑟 -𝑄 𝑒𝑣𝑎𝑝𝑜𝑡𝑟𝑎𝑛𝑠𝑝𝑖𝑟𝑎𝑡𝑖𝑜𝑛 (2)

where 𝑄 𝑛𝑒𝑡 is the net energy gain or loss in the greenhouse, and 𝑄 𝑒𝑣𝑎𝑝𝑜𝑡𝑟𝑎𝑛𝑠𝑝𝑖𝑟𝑎𝑡𝑖𝑜𝑛 is the heat loss due to plant evapotranspiration. Each heat component in the above equations represents specific physical processes in the greenhouse: 𝑄 𝑠𝑜𝑙𝑎𝑟 represents solar radiation heat gain, influenced by cover transmissivity and incident solar radiation; 𝑄 ℎ𝑒𝑎𝑡𝑖𝑛𝑔 denotes heat input from the heating system, dependent on system type and efficiency; 𝑄 𝑣𝑒𝑛𝑡𝑖𝑙𝑎𝑡𝑖𝑜𝑛 accounts for heat exchange through air renewal, affected by ventilation rate and temperature differences; 𝑄 𝑐𝑜𝑣𝑒𝑟 represents heat transfer through the greenhouse covering material, determined by material properties and external conditions; and 𝑄 𝑒𝑣𝑎𝑝𝑜𝑡𝑟𝑎𝑛𝑠𝑝𝑖𝑟𝑎𝑡𝑖𝑜𝑛 captures the energy consumed during plant transpiration and soil evaporation, which varies with crop type and growth stage. These components are typically estimated using empirical correlations, physical models, or sensor-based approaches, with the accuracy depending on greenhouse configuration and environmental conditions.

Table 4 compares the system dynamics model and the energy balance model, two commonly used approaches for greenhouse temperature prediction.

#### 3.1.2. Early machine learning applications

Machine learning algorithms enable greenhouse temperature prediction by extracting patterns from historical data to make future predictions. Different algorithms employ distinct mathematical principles to model the relationship between input variables and temperature, which explains their varying performance in different scenarios.

Various basic machine learning techniques have been applied to greenhouse temperature prediction, representing a transition from purely mechanistic models towards data-driven approaches. These methods, while less complex than the advanced AI techniques discussed in Section 4, provided important foundations for modern greenhouse temperature prediction. Table 5 analyzes and evaluates these early machine learning applications for greenhouse temperature prediction.

Radial Basis Function (RBF) networks use radial basis functions, such as the Gaussian function shown in Eq. ( 3), where 𝜙(‖𝑥 -𝑐‖) is the activation function, 𝑥 is the input vector, 𝑐 is the center of the radial basis function, and 𝛽 is a parameter controlling the function's width.

𝜙(‖𝑥

-𝑐‖) = exp(-𝛽‖𝑥 -𝑐‖ 2 )(3)

Bolandnazar et al. ( 2023) applied RBF and SVM models (as described by Eq. ( 4)) for greenhouse temperature prediction and achieved an RMSE of 1.32 • C for RBF, demonstrating the potential of machine learning methods for accurate temperature forecasting.

𝑓 (𝑥) = 𝑁 ∑ 𝑖=1 𝛼 𝑖 𝐾(𝑥 𝑖 , 𝑥) + 𝑏 (4)

The SVM model also outperformed the MLP and LR models. Hosseini Monjezi et al. ( 2023) employed RBF networks and reported an RMSE of 0.82 • C, further confirming the reliability of this approach. Other notable machine learning methods for greenhouse temperature prediction include PSO-SVR, which improves prediction accuracy compared to traditional models (Fan et al., 2021), and SVR, which is robust to outliers and provides high forecast accuracy (Lu et al., 2023). CB-ELM combines the fast training speed of Extreme Learning Machine (ELM) with convex optimization to improve prediction accuracy, outperforming traditional methods like BPNN and SVM (Zou et al., 2017). ELM is computationally efficient and suitable for resourceconstrained devices (Paniagua-Tineo et al., 2011). LSSVM optimizes model parameters and is more accurate than SVM and BPNN (Yu et al., 2016).

Overall, traditional temperature control methods and model prediction approaches have laid the foundation for greenhouse climate Computers and Electronics in Agriculture 237 (2025) 110603 management but have limitations regarding accuracy, efficiency, and adaptability to complex environments. It is worth noting that fuzzy logic systems represent one of the earliest AI-based approaches successfully applied to greenhouse temperature control. These models excel at handling the nonlinear interactions and uncertainties inherent in greenhouse environments. Machine learning techniques, such as SVM, RBF, PSO-SVR, SVR, CB-ELM, ELM, and LSSVM, have shown promising results in improving greenhouse temperature prediction accuracy and adaptability. However, further research is needed to develop advanced and intelligent temperature control methods that can overcome the limitations of traditional approaches and optimize crop yield, quality, and resource use efficiency in the face of new challenges in greenhouse cultivation.

## 4. AI-based methods for Greenhouse temperature prediction

AI techniques have emerged as powerful tools for modeling and predicting complex, nonlinear systems, such as greenhouse microclimate (Iddio et al., 2020;Moon et al., 2018). This section provides an overview of the application of AI techniques in greenhouse temperature prediction, focusing on three main categories of models: ANNs, DL models, and Hybrid models. We discuss the strengths and limitations of each approach, present representative examples from the literature, and provide a comparative analysis of their performance and suitability for different greenhouse scenarios.

It is worth noting that machine learning is a subset of AI, and deep learning is a specialized branch of machine learning. In this paper, we discuss simpler machine learning methods in the traditional methods section (Section 3), while focusing here on more advanced AI techniques for greenhouse temperature prediction.

### 4.1. Artificial neural networks

ANN is a class of machine learning models inspired by the structure and function of biological neural networks (Escamilla-García et al., 2020). ANNs have been widely applied in greenhouse temperature prediction due to their ability to model complex nonlinear relationships between environmental variables and indoor temperature (Castañeda-Miranda and Castaño, 2017; Kim et al., 2018).

#### 4.1.1. ANN architecture and training

The basic architecture of an ANN consists of an input layer, one or more hidden layers, and an output layer, with each layer composed of interconnected processing units called neurons. The mathematical formulation of a single neuron can be expressed as:

𝑦 = 𝑓 ( 𝑛 ∑ 𝑖=1 𝑤 𝑖 𝑥 𝑖 + 𝑏 ) (5

)

where 𝑦 is the output of the neuron, 𝑓 is the activation function, 𝑤 𝑖 are the weights, 𝑥 𝑖 are the inputs, 𝑏 is the bias term, and 𝑛 is the number of inputs.

The training of an ANN involves adjusting the weights and biases to minimize a loss function, which measures the difference between the predicted and actual outputs. The backpropagation algorithm is commonly used for training ANNs, which can be mathematically expressed as:

𝜕𝐸 𝜕𝑤 𝑗𝑖 = 𝛿 𝑗 𝑥 𝑖 (6

)

𝛿 𝑗 = { 𝑓 ′ (𝑛𝑒𝑡 𝑗 )(𝑡 𝑗 -𝑦 𝑗 )

for output layer neurons 𝑓 ′ (𝑛𝑒𝑡 𝑗 ) ∑ 𝑘∈downstream(𝑗) 𝛿 𝑘 𝑤 𝑘𝑗 for hidden layer neurons (7) where 𝐸 is the loss function, 𝑤 𝑗𝑖 is the weight connecting neuron 𝑖 to neuron 𝑗, 𝛿 𝑗 is the local gradient for neuron 𝑗, 𝑛𝑒𝑡 𝑗 is the weighted sum of inputs for neuron 𝑗, 𝑡 𝑗 is the target output for neuron 𝑗, and 𝑦 𝑗 is the actual output of neuron 𝑗.

#### 4.1.2. ANN models for greenhouse temperature prediction

ANNs have been widely applied to model complex nonlinear relationships and achieve high prediction accuracy in greenhouse temperature prediction. Various ANN architectures, such as BP, feedforward neural networks (FFNN), wavelet neural networks (WNN), multilayer perceptrons (MLP), and deep neural networks (DNN), have been employed to forecast greenhouse temperature with different time horizons ranging from one hour to one day ahead. The most common input variables for ANN models include temperature, humidity, solar radiation, and wind speed, key factors influencing greenhouse microclimate. For instance, Codeluppi et al. (2021) developed a BP network that utilized temperature, humidity, solar radiation, and wind speed as inputs to predict greenhouse temperature one day ahead, achieving an R 2 value of 0.94. Similarly, Jung et al. (2020a) However, simple ANN models have some limitations, such as the lack of an explicit mechanism for handling temporal dependencies in time series data, which can limit their performance in capturing longterm patterns and trends (Escamilla-García et al., 2020). To address this issue, researchers have explored the use of time-series ANN models, such as the one proposed by Dariouchy et al. (2009), which achieved an R 2 value of 0.987 when predicting greenhouse temperature one day ahead. Several researchers have also investigated the application of hybrid ANN models for greenhouse temperature prediction. Bolandnazar et al. ( 2023) compared the performance of MLR and RBF networks in predicting greenhouse temperature using temperature, humidity, wind speed, and solar radiation concentration as inputs, reporting an R 2 value of 0.931 for the RBF model. Taki et al. (2016) combined MLP and basic back-propagation algorithm to predict greenhouse temperature one day in advance, achieving an RMSE of 0.23 • C. The performance of ANN models for greenhouse temperature prediction has been evaluated using various metrics, such as RMSE, MAE, MAPE, and R 2 . These results demonstrate the ability of ANN models to accurately predict greenhouse temperature and capture the complex nonlinear relationships between input variables and temperature dynamics.

To put it briefly, ANN models have shown great potential for accurately predicting greenhouse temperature. Various architectures and input variables are employed to model the complex nonlinear relationships governing greenhouse microclimate. Despite their limitations in handling temporal dependencies, ANNs remain a powerful tool for greenhouse temperature prediction and have laid the foundation for developing more advanced deep-learning approaches.

### 4.2. Deep learning models

Deep learning models, such as Convolutional Neural Network (CNN), Recurrent Neural Network (RNN), and Transformers, have demonstrated outstanding performance in various domains, including time series forecasting and spatial-temporal data processing. These models can learn hierarchical representations of input data and extract relevant features automatically, making them well-suited for greenhouse temperature prediction tasks (Moon et al., 2019;Torres et al., 2021).

#### 4.2.1. Convolutional neural networks

CNNs are designed to process grid-like data, such as images and spatial-temporal data, by applying convolutional layers that learn local patterns and features (Krizhevsky et al., 2017). The mathematical formulation of a convolutional layer can be expressed as: where 𝑠(𝑖, 𝑗) is the output of the convolutional layer at position (𝑖, 𝑗), 𝑥 is the input, 𝑤 is the filter kernel, and * denotes the convolution operation.

𝑠(𝑖, 𝑗) = (𝑥 * 𝑤)(𝑖, 𝑗) = ∑ 𝑚 ∑ 𝑛 𝑥(𝑖 -𝑚, 𝑗 -𝑛)𝑤(𝑚, 𝑛) (8)

#### 4.2.2. Recurrent neural networks

RNNs are designed to handle sequential data by maintaining an internal memory state that allows information to persist across time steps. The mathematical formulation of a simple RNN can be expressed as:

ℎ 𝑡 = 𝑓 (𝑊 ℎℎ ℎ 𝑡-1 + 𝑊 𝑥ℎ 𝑥 𝑡 + 𝑏 ℎ )(9)

𝑦 𝑡 = 𝑊 ℎ𝑦 ℎ 𝑡 + 𝑏 𝑦 (10) where ℎ 𝑡 is the hidden state at time step 𝑡, 𝑥 𝑡 is the input at time step 𝑡, 𝑦 𝑡 is the output at time step 𝑡, 𝑓 is the activation function, 𝑊 are the weight matrices, and 𝑏 are the bias vectors. LSTM (Long Short-Term Memory) networks and GRUs (Gated Recurrent Unit) are popular variants of RNNs specifically designed to handle long-term dependencies in sequential data. The mathematical formulation of an LSTM cell can be expressed as:

𝑓 𝑡 = 𝜎(𝑊 𝑓 ⋅ [ℎ 𝑡-1 , 𝑥 𝑡 ] + 𝑏 𝑓 ) (11

)

𝑖 𝑡 = 𝜎(𝑊 𝑖 ⋅ [ℎ 𝑡-1 , 𝑥 𝑡 ] + 𝑏 𝑖 ) (12) C𝑡 = tanh(𝑊 𝐶 ⋅ [ℎ𝑡 -1, 𝑥 𝑡 ] + 𝑏 𝐶 ) (13

)

𝐶 𝑡 = 𝑓 𝑡 * 𝐶 𝑡-1 + 𝑖 𝑡 * C𝑡 (14) 𝑜 𝑡 = 𝜎(𝑊 𝑜 ⋅ [ℎ𝑡 -1, 𝑥 𝑡 ] + 𝑏 𝑜 ) (15) ℎ 𝑡 = 𝑜 𝑡 * tanh(𝐶 𝑡 )(16)

where 𝑓 𝑡 , 𝑖 𝑡 , and 𝑜 𝑡 are the forget, input, and output gates, respectively, 𝐶 𝑡 is the cell state, C𝑡 is the candidate cell state, ℎ 𝑡 is the hidden state, 𝑥 𝑡 is the input at time step 𝑡, 𝑊 are the weight matrices, 𝑏 are the bias vectors, and * denotes the element-wise multiplication.

#### 4.2.3. Transformers

Transformers are a recent advancement in deep learning that has shown state-of-the-art performance in various natural language processing tasks. The key component of Transformers is the self-attention mechanism, which allows the model to attend to different parts of the input sequence when making predictions. The mathematical formulation of the scaled dot-product attention can be expressed as:

Attention(𝑄, 𝐾, 𝑉 ) = softmax ( 𝑄𝐾 ⊤ √ 𝑑 𝑘 ) 𝑉 (17

)

Long Short-Term Memory, GRU = Gated Recurrent Unit, CNN = Convolutional Neural Network, MLP = Multi-Layer Perceptron, RL = Reinforcement Learning, BiLSTM = Bidirectional LSTM, BEDA = Bidirectional self-attentive encoder-decoder framework, T = Temperature, H = Humidity, C = CO 2 , R = Radiation, i = Indoor, o = Outdoor, a = Air, SR = Solar Radiation, WS = Wind Speed, WD = Wind Direction, RF = Rainfall, RH = Relative Humidity, AP = Air Pressure, CC = Cloud Cover, DP = Dew Point, ST = Soil Temperature, LT = Leaf Temperature, dpH = Drainage pH, LI = Light Intensity, TR = Total Radiation, NR = Net Radiation, SVWC = Soil Volumetric Water Content, SS = Shading Screen, CFS = Circulation Fan Status, HVO = Heating Valve Opening, CIR = CO 2 Injection Rate, TS = Thermal Screen, SWO = Side Window Opening, SP = Sprinkler, HT = Heater, VW = Ventilation Window, Time Units: h = hours, min = minutes.

where 𝑄, 𝐾, and 𝑉 are the query, key, and value matrices, respectively, and 𝑑 𝑘 is the dimension of the key vectors. Table 6 compares the key features and performance of the representative deep learning models for greenhouse temperature prediction. As shown in Table 6, deep learning models can achieve high prediction accuracy for greenhouse temperature, with MAE values as low as 0.17 • C and R 2 values greater than 0.936. The choice of the most appropriate deep learning model depends on the specific characteristics of the data, the desired accuracy, and the computational resources available. Models with greater depth (i.e., more layers) generally have a higher capacity to learn complex patterns and relationships in the data. Still, they may also require more computational resources and training time.

Fig. 2 illustrates the typical architecture and data flow in a deep learning model for greenhouse temperature prediction, showcasing the integration of multiple environmental variables as inputs, the hierarchical learning of features through various layers, and the generation of temperature predictions as outputs.

### 4.3. Hybrid models

Hybrid models combine traditional mathematical models, such as system dynamics or energy balance models, with AI models to leverage the strengths of both approaches and improve the accuracy and robustness of greenhouse temperature prediction and control (Ding et al., 2018a;Zhou et al., 2023). These models incorporate physical principles, domain knowledge, and data-driven learning to provide interpretable and adaptable solutions to maintain optimal greenhouse environments.

The choice of the hybrid architecture depends on the specific characteristics of the mechanical and AI models, as well as the available data and computational resources. For instance, Linker and Seginer 7 presents an overview of the critical features and mathematical expressions of different hybrid model architectures employed in greenhouse temperature control.

#### 4.3.1. Theoretical foundations

Hybrid models combine the benefits of inductive and deductive reasoning in modeling complex greenhouse systems. Mechanistic models rely on deductive reasoning, starting from general physical principles and deriving specific predictions based on the system parameters and boundary conditions. AI models, on the other hand, rely on inductive reasoning, learning patterns, and relationships from observed data without explicit prior knowledge of the system dynamics.

Incorporating physical constraints and domain knowledge in hybrid models helps to regularize the learning process, reducing the risk of overfitting and ensuring that the learned relationships are consistent with the underlying physical processes. At the same time, the AI components of hybrid models can capture complex non-linear relationships and adapt to changing conditions, improving the accuracy and robustness of the predictions.

The mathematical formulation of a generic hybrid model for greenhouse temperature control can be expressed as:

𝑇 𝑝𝑟𝑒𝑑 = 𝑓 ℎ𝑦𝑏𝑟𝑖𝑑 (𝑇 𝑚𝑒𝑐ℎ , 𝑇 𝐴𝐼 , 𝑋, 𝜃) (18)

where 𝑇 𝑝𝑟𝑒𝑑 is the predicted temperature, 𝑇 𝑚𝑒𝑐ℎ is the output of the mechanistic model, 𝑇 𝐴𝐼 is the output of the AI model, 𝑋 represents the input variables, and 𝜃 denotes the learnable parameters of the hybrid model. The function 𝑓 ℎ𝑦𝑏𝑟𝑖𝑑 represents the specific hybrid architecture employed, such as serial, parallel, hierarchical, or iterative, as shown in Table 7.

#### 4.3.2. Representative hybrid models

Table 8 summarizes representative hybrid models' key features and performance for greenhouse temperature prediction and control. For example, Montoya et al. (2016) developed a parallel hybrid model, the Model Predictive Hybrid Controller, which utilized weather variables to generate optimal control signals for maintaining desired nocturnal greenhouse temperatures. The parallel architecture allowed for the combination of strengths from both mechanical and AI models, resulting in balanced performance. Exploring the relationship between temperature, light, CO 2 , and the photosynthetic rate is critical to optimizing greenhouse climate for efficient crop production (Körner

#### 4.3.3. Advantages and challenges

Hybrid models offer complementary benefits over singular approaches by combining mechanistic knowledge with data-driven techniques. Their key advantage lies in utilizing established physical principles through energy balance equations and heat transfer models, ensuring predictions remain physically valid while reducing overfitting risks. This integration improves model interpretability, a critical feature for greenhouse operators who must understand control decisions, while maintaining accuracy for complex nonlinear relationships. The mechanical components provide physical meaning while AI elements adapt to environmental complexities. The integration of domain knowledge significantly reduces data requirements compared to pure AI methods, as demonstrated by Zhou et al. (2023) and Moon and Eek Son (2021), enabling more reliable extrapolation beyond training boundaries, essential when facing unexpected climate patterns.

Despite these advantages, hybrid approaches face integration challenges requiring interdisciplinary expertise in both mechanical systems and AI. Parallel architectures struggle with optimal weight determination between model components, where imbalanced weightings can trigger control instabilities during environmental transitions. Additionally, hierarchical and iterative designs face computational intensity issues that may exceed practical limits in resource-constrained greenhouse operations. These trade-offs necessitate careful consideration when implementing hybrid modeling for commercial greenhouse temperature management.

### 4.4. Comparative analysis and future directions

The choice of the most suitable AI technique for greenhouse temperature prediction depends on various factors, such as the system's complexity, data availability and quality, the desired prediction horizon, and the computational resources available. Table 9 provides a comparative analysis of the strengths and limitations of the three main categories of AI models discussed in this section.

As shown in Table 9, each category of AI model has its strengths and limitations, and the selection of the most appropriate approach should be based on carefully considering the specific requirements and constraints of the greenhouse temperature prediction task at hand. Deep learning models generally achieve the highest prediction accuracy, with typical RMSE values ranging from 0.3 to 1.3 • C and R 2 values between 0.96 and 0.99. Hybrid models balance prediction accuracy and interpretability, with typical RMSE values between 0.2 and 0.8 • C and R 2 values ranging from 0.97 to 0.99. Future research directions in the application of AI for greenhouse temperature prediction include:

Integration of multiple data sources, such as remote sensing, weather forecasts, and plant growth models, to improve the accuracy and robustness of temperature predictions. Development of adaptive and self-learning AI models that can automatically adjust their structure and parameters in response to changing environmental conditions and data patterns. Incorporation of uncertainty quantification and probabilistic modeling techniques to provide more informative and reliable temperature predictions, along with confidence intervals and risk assessments. Exploration of transfer learning and domain adaptation techniques to leverage knowledge and models learned from one greenhouse system to another, reducing the need for extensive data collection and model retraining. Integration of AI-based temperature prediction models with greenhouse climate control systems and decision support tools to enable more efficient and sustainable greenhouse management practices.

## 5. Applications of different methods for Greenhouse temperature control

Different traditional and AI-based techniques have gained significant attentions on greenhouse temperature control from both research and application perspective. For instance, the typical control methods, fuzzy logic systems, MPC, RL, and intelligent control systems have notably handled the complexities and uncertainties associated with greenhouse environments. Fuzzy logic systems excel in managing complex and interrelated climatic parameters. At the same time, MPC provides precise control with energy efficiency, and RL offers adaptive and robust solutions by leveraging historical and real-time data. This chapter provides a comprehensive overview of the recent progress on applying these different techniques to greenhouse temperature control, focusing on their key findings, challenges, and opportunities. A comparative analysis of these methods is presented, highlighting their strengths and suitable environments for application. The section also discusses future research directions, emphasizing the potential for integrating these approaches to develop more efficient, sustainable, and autonomous greenhouse climate control systems.

### 5.1. Traditional control methods

Greenhouse temperature control is critical to ensuring optimal plant growth and development. Traditional methods for greenhouse temperature control encompass manual, mechanical, and hybrid control strategies. Manual control offers flexibility and immediate intervention but is labor-intensive and prone to human error, resulting in inconsistent temperature management (Azaza et al., 2016;Devi Thangavel et al., 2023). Mechanical control systems provide automation and constant temperature maintenance but have high costs and limited adaptability, leading to temperature fluctuations and energy waste (Huang, 2023). Temperature fluctuations in a greenhouse with mechanical temperature control reached up to 20 • C, negatively affecting crop growth and development (He et al., 2025;Yu et al., 2025).

Hybrid control (in the context of traditional control methods, distinct from the hybrid models discussed in Section 4.3) combines the benefits of manual and mechanical control, allowing for automated operation with manual overrides, but it requires a complex setup and a high initial investment. The advantages and disadvantages of each approach are summarized in Table 10.

Overall, traditional temperature control methods and model prediction approaches have laid the foundation for greenhouse climate management but have limitations regarding accuracy, efficiency, and adaptability to complex environments. Machine learning techniques, such as SVM, RBF, PSO-SVR, SVR, CB-ELM, ELM, and LSSVM, have shown promising results in improving greenhouse temperature prediction accuracy and adaptability. However, further research is needed to develop advanced and intelligent temperature control methods that can overcome the limitations of traditional approaches and optimize crop yield, quality, and resource use efficiency in the face of new challenges in greenhouse cultivation.

### 5.2. Fuzzy logic systems

Fuzzy logic control is a sophisticated approach for managing the complex and interrelated climatic parameters in greenhouse environments, maximizing the adaptability and precision of fuzzy systems (Abioye et al., 2020;Shihabudheen and Pillai, 2018). Fuzzy logic-based controllers can handle nonlinear interactions between temperature, humidity, and soil moisture, which are crucial for optimal plant growth (Jaiswal and Ballal, 2020;Alpay and Erdem, 2018).

Advanced implementations, such as the integration of fuzzy logic with SVM and adaptive neuro-fuzzy inference systems (ANFIS), enhance the decision-making process by adapting to changing conditions and improving control accuracy (Shihabudheen and Pillai, 2018). The output of an ANFIS can be expressed as:

𝑦 = 𝑁 ∑ 𝑖=1 𝑤 𝑖 𝑓 𝑖 (𝑥) = 𝑁 ∑ 𝑖=1 𝑤 𝑖 (𝑝 𝑖 𝑥 + 𝑞 𝑖 ) (19

)

where 𝑁 is the number of fuzzy rules, 𝑤 𝑖 is the normalized firing strength of the 𝑖th rule, and 𝑝 𝑖 and 𝑞 𝑖 are the consequent parameters. Fuzzy logic has demonstrated significant improvements in optimizing microclimate, enhancing energy efficiency, and reducing resource consumption in greenhouse temperature control (Zhang et al., 2020). Table 11 summarizes fuzzy logic's key findings and applications in greenhouse temperature control.

### 5.3. Model predictive control

MPC is an advanced control strategy proven highly effective in greenhouse temperature control applications. MPC uses a dynamic model of the greenhouse to predict its future behavior and optimize control actions accordingly. The core principle of MPC is to solve an optimization problem at each sampling instant, considering the system's current state, the desired reference trajectory, and the constraints on the input and output variables. By continuously updating the control actions based on the latest measurements and predictions, MPC can adapt to changing conditions and disturbances while maintaining optimal performance (Piñón et al., 2005;Chen et al., 2018). Table 12 presents a comprehensive summary of recent applications of MPC frameworks in greenhouse temperature control. These studies have consistently demonstrated MPC's superiority in control precision, energy efficiency, and robustness compared to traditional control methods. For instance, Bersani et al. (2021) developed an MPC framework for a high-efficiency greenhouse using an energy and mass balances model. The proposed approach achieved a remarkable 30% energy saving compared to relay control while maintaining optimal temperature conditions for crop growth. Ajagekar et al. (2023) proposed an AI-based control framework that combines deep RL techniques to generate insights into greenhouse operation combined with robust optimization to produce energy-efficient controls by hedging against associated uncertainties, which demonstrates a significant reduction in energy consumption of 57% over traditional control techniques. The optimization problem in MPC can be formulated as follows:

min 𝐮 𝑁-1 ∑ 𝑘=0 [ ( 𝐱 𝑘 -𝐱 𝑟𝑒𝑓 ) ⊤ 𝐐 ( 𝐱 𝑘 -𝐱 𝑟𝑒𝑓 ) + 𝐮 ⊤ 𝑘 𝐑𝐮 𝑘 + 𝛥𝐮 ⊤ 𝑘 𝐒𝛥𝐮 𝑘 ] (20

)

Computers and Electronics in Agriculture 237 (2025) 110603

### Low computation cost, high spatial resolution

External disturbances and corrections subject to:

𝐱 𝑘+1 = 𝐟(𝐱 𝑘 , 𝐮 𝑘 , 𝐝 𝑘 )(21)

𝐲 𝑘 = 𝐠(𝐱 𝑘 , 𝐮 𝑘 ) (22) 𝐱 𝑘 ∈  (23) 𝐮 𝑘 ∈  (24) 𝛥𝐮 𝑘 ∈ 𝛥 (25) 𝐲 𝑘 ∈ (26)

where 𝐱 𝑘 ∈ R 𝑛 𝑥 is the state vector at time step 𝑘, 𝐮 𝑘 ∈ R 𝑛 𝑢 is the control input vector, 𝐝 𝑘 ∈ R 𝑛 𝑑 is the disturbance vector, 𝐲 𝑘 ∈ R 𝑛 𝑦 is the output vector, 𝐱 𝑟𝑒𝑓 ∈ R 𝑛 𝑥 is the reference state trajectory, 𝐐 ∈ R 𝑛 𝑥 ×𝑛 𝑥 , 𝐑 ∈ R 𝑛 𝑢 ×𝑛 𝑢 , and 𝐒 ∈ R 𝑛 𝑢 ×𝑛 𝑢 are positive definite weighting matrices,

𝛥𝐮 𝑘 = 𝐮 𝑘 -𝐮 𝑘-1 is the input increment, 𝐟 ∶ R 𝑛 𝑥 × R 𝑛 𝑢 × R 𝑛 𝑑 → R 𝑛 𝑥 represents the nonlinear greenhouse dynamics, 𝐠 ∶ R 𝑛 𝑥 × R 𝑛 𝑢 → R 𝑛 𝑦 is the output function, and  ⊆ R 𝑛 𝑥 ,  ⊆ R 𝑛 𝑢 , 𝛥 ⊆ R 𝑛 𝑢 , and  ⊆ R 𝑛 𝑦

denote the state, input, input increment, and output constraint sets, respectively.

The MPC optimization problem seeks to find the optimal sequence

of control inputs 𝐮 = [ 𝐮 ⊤ 0 , … , 𝐮 ⊤ 𝑁-1

] ⊤ that minimizes the weighted sum of the tracking error, control effort, and input increments over a prediction horizon of 𝑁 steps, subject to the greenhouse dynamics, output function, and state, input, and output constraints. Including the input increment term 𝛥𝐮 𝑘 in the cost function and constraints ensures smooth control actions and prevents excessive actuator wear.

Computers and Electronics in Agriculture 237 (2025) 110603 Fig. 3. Schematic representation of an MPC framework for greenhouse temperature control, illustrating the key components and their interactions. The MPC controller uses a dynamic greenhouse model to predict future system behavior and optimize the control actions based on the current state, reference trajectory, and constraints. The optimal control inputs are applied to the greenhouse through the actuators, while the sensor measurements are used to update the state estimate and adapt the model parameters online.

Despite the promising results, implementing MPC in real-world greenhouses presents several challenges. These include handling statedependent nonlinear constraints (Piñón et al., 2005), performing online minimax optimization to guarantee robustness against uncertainties (Chen et al., 2018), and seamlessly integrating MPC with existing control systems and hardware (Achour et al., 2020). Moreover, the complexity of the optimization problem and the requirement for accurate greenhouse models can limit the scalability and practicality of MPC in large-scale and highly dynamic greenhouse environments.

Fig. 3 presents a schematic representation of an MPC framework for greenhouse temperature control, highlighting the interconnections between the key components, such as the greenhouse model, optimization algorithm, state estimator, and actuators. Developing computationally efficient optimization algorithms, adaptive greenhouse models, and robust state estimation techniques is crucial for successfully implementing MPC in practical greenhouse control systems.

### 5.4. Reinforcement learning

RL has emerged as a promising approach for optimizing greenhouse temperature control strategies without relying on accurate mathematical models of the system. RL algorithms learn optimal control policies through interaction with the environment, receiving rewards or penalties for their actions, and adapting their behavior to maximize the cumulative reward over time. By exploring the state-action space and exploiting the acquired knowledge, RL agents can autonomously discover effective control strategies that balance multiple objectives, such as energy efficiency, crop yield, and climate regulation.

Table 13 provides a comprehensive overview of recent applications of RL in greenhouse temperature control. These studies have employed a variety of RL algorithms, ranging from classical methods like Q-learning to state-of-the-art deep RL techniques, such as deep Qnetworks (DQN) and proximal policy optimization (PPO). The choice of the RL algorithm depends on factors such as the complexity of the greenhouse environment, the dimensionality of the state and action spaces, and the availability of data and computational resources.

For instance, Wang et al. (2020) developed a deep RL approach based on Q-learning for optimizing temperature control in a cucumber greenhouse simulator. The proposed method achieved improved cumulative fruit weight and reduced costs compared to traditional control strategies. The Q-learning algorithm updates the Q-values according to the following equation:

𝑄(𝑠 𝑡 , 𝑎 𝑡 ) ← 𝑄(𝑠 𝑡 , 𝑎 𝑡 ) + 𝛼 [ 𝑟 𝑡 + 𝛾 max 𝑎 𝑄(𝑠 𝑡+1 , 𝑎) -𝑄(𝑠 𝑡 , 𝑎 𝑡 ) ](27)

where 𝑄(𝑠 𝑡 , 𝑎 𝑡 ) is the Q-value of taking action 𝑎 𝑡 in state 𝑠 𝑡 , 𝛼 ∈ (0, 1] is the learning rate, 𝑟 𝑡 is the reward at time step 𝑡, 𝛾 ∈ [0, 1) is the discount factor, and max 𝑎 𝑄(𝑠 𝑡+1 , 𝑎) represents the maximum Q-value of the next state 𝑠 𝑡+1 over all possible actions. The Q-learning algorithm iteratively updates the Q-values based on the observed state transitions and rewards, gradually converging to the optimal Q-function 𝑄 * (𝑠, 𝑎) that satisfies the Bellman optimality equation:

𝑄 * (𝑠, 𝑎) = E 𝑠 ′ ∼𝑃 (⋅|𝑠,𝑎) [ 𝑟(𝑠, 𝑎) + 𝛾 max 𝑎 ′ 𝑄 * (𝑠 ′ , 𝑎 ′ ) ](28)

where 𝑃 (𝑠 ′ |𝑠, 𝑎) is the state transition probability distribution, and 𝑟(𝑠, 𝑎) is the reward function.

However, applying RL in real-world greenhouse control systems poses several challenges. These include handling continuous and highdimensional state and action spaces (Ajagekar and You, 2022b), ensuring safe and efficient exploration of the environment (Chen et al.,Fig. 4. RL framework for greenhouse temperature control, illustrating the interaction between the RL agent and the greenhouse environment. The agent observes the state of the greenhouse, selects an action based on its policy, and receives a reward signal from the environment. The agent's goal is to learn an optimal policy that maximizes the cumulative reward over time while adapting to the changing conditions and disturbances in the greenhouse. (Morcego et al., 2023). Fig. 4 illustrates a typical RL framework for greenhouse temperature control, emphasizing the closed-loop interaction between the RL agent Architecture of an intelligent control system for greenhouse temperature control, showcasing the integration of various components and technologies. The system combines data acquisition from sensor networks, data preprocessing and analysis, machine learning and adaptation, and decision-making and optimization modules to provide a comprehensive and autonomous control framework. The intelligent control system interacts with the greenhouse environment through actuators and interfaces while learning from the system's behavior and performance to continuously improve its control strategies. and the greenhouse environment. Developing sample-efficient RL algorithms, safe exploration strategies, and transfer learning techniques is essential for the practical application of RL in greenhouse control systems. Furthermore, integrating domain knowledge and expert guidance into the RL framework can significantly accelerate the learning process and improve the interpretability and reliability of the learned control policies.

### 5.5. Intelligent control systems

Integrating AI-based temperature prediction models with advanced control strategies, such as MPC, RL, and adaptive control, can enable the development of intelligent and autonomous greenhouse management systems (Zhou and Liu, 2024). MPC is a model-based control strategy that uses a dynamic greenhouse model to predict future system behavior and optimize control actions over a receding horizon (Morcego et al., 2023). By incorporating AI-based temperature prediction models into the MPC framework, the control system can anticipate disturbances, such as weather changes and crop growth, and adapt the control actions accordingly (Halhoul Merabet et al., 2021;Mahmood et al., 2023). RL is a data-driven control strategy that learns the optimal control policy through trial-and-error, using a reward signal to guide the learning process (Recht, 2019). By combining RL with AIbased temperature prediction models, the control system can learn to optimize the temperature control actions in real-time, adapting to the specific crop requirements and environmental conditions (Hu and You, 2024).

Intelligent control systems represent a holistic approach to greenhouse climate management, integrating various AI techniques, such as machine learning, fuzzy logic and optimization algorithms, to create comprehensive and autonomous control frameworks. These systems aim to optimize greenhouse operations, enhance crop growth, and reduce resource consumption by leveraging data from sensor networks, adapting to changing environmental conditions, and learning from past experiences. The main advantage of intelligent control systems lies in their ability to handle the complexities, uncertainties, and multiobjective nature of greenhouse control problems while providing a high level of flexibility, scalability, and user-friendliness.

Table 14 summarizes recent applications of intelligent control systems in greenhouse temperature control, highlighting the diversity of system architectures, technologies, and application scenarios. These studies have consistently demonstrated the potential of AI-based control systems to improve productivity, energy efficiency, and crop quality in different regions and climates. For instance, Zhao et al. ( 2019) developed an IoT-based intelligent greenhouse control system using a long range Radio (LORA) wireless network and sensors for multiple environmental parameters. The system improved operation efficiency and enhanced crop quality in cash crop planting bases in China. The following general architecture can represent the intelligent control system:

𝐮 𝑡 =  ( 𝐱 𝑡 , 𝐲 𝑡 , 𝐝 𝑡 , 𝜽 𝑡 ) (29

)

where

𝐮 𝑡 ∈ R 𝑛 𝑢 is the control input vector at time 𝑡,  ∶ R 𝑛 𝑥 × R 𝑛 𝑦 × R 𝑛 𝑑 × R 𝑛 𝜃 → R 𝑛 𝑢

is the intelligent control algorithm, 𝐱 𝑡 ∈ R 𝑛 𝑥 is the state vector, 𝐲 𝑡 ∈ R 𝑛 𝑦 is the output vector, 𝐝 𝑡 ∈ R 𝑛 𝑑 represents the disturbance vector, and 𝜽 𝑡 ∈ R 𝑛 𝜃 denotes the control parameter vector.

The intelligent control algorithm  can be composed of multiple interacting modules, such as:

1. Data acquisition and preprocessing module:

𝐳 𝑡 =  ( 𝐱 𝑡 , 𝐲 𝑡 , 𝐝 𝑡 ) (30

)

where 𝐳 𝑡 ∈ R 𝑛 𝑧 is the preprocessed data vector, and

 ∶ R 𝑛 𝑥 × R 𝑛 𝑦 × R 𝑛 𝑑 → R 𝑛 𝑧 is the preprocessing function.

2. Learning and adaptation module:

𝜽 𝑡 =  ( 𝐳 𝑡 , 𝐮 𝑡-1 , 𝜽 𝑡-1 )(31)

where  ∶ R 𝑛 𝑧 ×R 𝑛 𝑢 ×R 𝑛 𝜃 → R 𝑛 𝜃 is the learning and adaptation function.

3. Decision-making and optimization module: where  ∶ R 𝑛 𝑧 × R 𝑛 𝜃 → R 𝑛 𝑢 is the decision-making and optimization function.

𝐮 𝑡 =  ( 𝐳 𝑡 , 𝜽 𝑡 )(32)

Integrating these modules enables the intelligent control system to process the collected data, learn from the system's behavior and performance, adapt to changing conditions, and make optimal control decisions in real-time. However, implementing intelligent control systems in real-world greenhouses requires addressing several challenges, such as system complexity, data integration, and cost-effectiveness (Subahi and Bouazza, 2020). Moreover, ensuring these systems' reliability, scalability, and adaptability under varying conditions and user requirements is crucial for their successful deployment.

Fig. 5 presents a generic architecture of an intelligent control system for greenhouse temperature control, emphasizing the seamless integration of various components and technologies. Developing modular, scalable, and adaptable system architectures and using opensource platforms, standardized protocols, and user-friendly interfaces can significantly facilitate implementing and adopting intelligent control systems in diverse greenhouse settings. Furthermore, incorporating advanced AI techniques, such as transfer learning, RL, and explainable AI, can enhance these systems' performance, robustness, and interpretability while reducing the data requirements and computational costs.

### 5.6. Comparative analysis and future directions

Table 15 presents a comparative analysis of fuzzy logic, MPC, and RL in the decision-making about greenhouse temperature control.

Integrating these methods can harness their strengths, resulting in more efficient and autonomous temperature control systems. Future research should focus on: (1) developing robust MPC models for nonlinear greenhouse environments; (2) addressing sample efficiency and safety in RL through model-based approaches; (3) comparing RL with traditional methods to guide hybrid control strategies; and (4) integrating MPC and RL to improve control performance and efficiency.

## 6. Future research directions

Data-driven technologies have revolutionized greenhouse temperature management through precise monitoring, efficient data processing, and intelligent environmental control. The integration of IoT, advanced sensing, and multimodal data fusion has improved control systems' efficiency while creating optimal conditions for plant growth. To fully realize AI's potential in this field, we need to explore new approaches that address fundamental challenges in greenhouse climate control. Drawing from plant systems biology, energy informatics, and Earth system science, we propose three cutting-edge research directions:

### 6.1. Developing plant-centric AI models for precision temperature control

Current AI models for greenhouse temperature control primarily focus on optimizing the physical environment for crop growth without fully considering the complex physiological and genetic mechanisms that regulate plant responses to temperature. To achieve a quantum leap in the efficiency and effectiveness of temperature control, future research should aim to develop plant-centric AI models that integrate multi-omics data, such as genomics, transcriptomics, proteomics, and metabolomics, to unravel the molecular pathways and regulatory networks underlying plant temperature adaptation (Hu and You, 2024;Sears et al., 2024). By leveraging the power of systems biology and machine learning, these models can identify the critical genetic and metabolic markers that predict plant performance under different temperature regimes and design precision temperature control strategies that optimize the expression of desirable traits, such as heat tolerance, yield potential, and nutritional quality. Furthermore, integrating AI with cutting-edge biotechnologies, such as CRISPR-based gene editing and synthetic biology, can enable the rapid development and deployment of climate-resilient crop varieties tailored to the specific temperature profiles of different greenhouses. This plant-centric approach to AI-driven temperature control can revolutionize greenhouse cultivation by unlocking the untapped genetic potential of crops and enabling the production of more nutritious, resilient, and sustainable food.

### 6.2. Exploring the potential of AI for sustainable energy management in Greenhouses

Energy consumption is a significant challenge in greenhouse operations, particularly heating and cooling systems. To reduce the carbon footprint and operating costs of greenhouses, future research should explore the potential of AI for sustainable energy management. This can involve the development of intelligent control algorithms that optimize the use of renewable energy sources, such as solar, geothermal, and biomass, based on real-time weather conditions, crop requirements, and energy prices. Furthermore, integrating AI with advanced energy storage technologies, such as phase change materials (PCMs) and thermal energy storage (TES) systems, can enable the efficient and flexible management of energy supply and demand in greenhouses. By leveraging AI's predictive and adaptive capabilities, we can develop intelligent energy management systems that minimize greenhouse temperature control's environmental impact and economic cost while ensuring optimal crop growth conditions.

### 6.3. Developing AI-empowered digital twins for Greenhouse-Earth system integration

Greenhouses are not isolated systems but are deeply interconnected with the broader Earth system, including the atmosphere, hydrosphere, and biosphere. To fully understand and optimize the role of greenhouses in global sustainable development, future research should aim to develop AI-empowered digital twins that can simulate the complex interactions between greenhouses and the Earth system at multiple spatial and temporal scales (Slob et al., 2023;Wang et al., 2023). These digital twins should integrate high-resolution Earth observation data, process-based crop and climate models, and advanced AI techniques, such as deep learning, RL, and multi-agent systems, to create virtual replicas of greenhouse-Earth system dynamics (Zhou et al., 2023;Zhou and Liu, 2024). By assimilating real-time data from satellites, drones, and IoT sensors, these digital twins can provide actionable insights into the environmental impacts and trade-offs of different greenhouse management practices, such as water use, fertilizer application, and energy consumption. Moreover, by coupling these digital twins with decision support tools and policy simulators, we can explore the potential of greenhouses to contribute to global sustainability goals, such as climate change mitigation, biodiversity conservation, and food security (Zhang et al., 2022). This holistic and integrated approach to greenhouse-Earth system modeling can help policymakers, investors, and the public make informed decisions about the future of greenhouse cultivation and its role in creating a more resilient and sustainable world.

By embracing these transformative research directions, we can unleash the full potential of AI to revolutionize greenhouse temperature control and create a new paradigm for sustainable, resilient, and intelligent agriculture. This will require a bold vision, a multidisciplinary approach, and a collaborative spirit among researchers, innovators, and stakeholders across the public and private sectors. Developing advanced sensing technologies, such as wireless sensor networks, imaging sensors, and remote sensing platforms, can provide more accurate and comprehensive data on greenhouse environmental parameters and crop growth dynamics (Benyezza et al., 2023). The application of physics-guided machine learning techniques, such as ordinary neural differential equations and physics-informed neural networks, can incorporate mechanistic knowledge into the learning process, improving the precision and interpretability of AI models (Hu and You, 2024). Exploring explainable AI techniques, such as attention mechanisms and rule extraction, has become increasingly critical to enhance transparency and trustworthiness of AI-based control systems, enabling growers to understand automated decisions and satisfying regulatory requirements (Fan et al., 2019;Ahmed et al., 2025).

Moreover, developing user-friendly interfaces and decision support tools can enable growers and operators to interact with AI-based control systems and provide expert feedback and guidance (Munoz et al., 2022). Integrating economic and social considerations into optimization objectives and constraints can ensure that AI-based control strategies are technically feasible, economically viable, and socially acceptable (Adesanya et al., 2024). Finally, the establishment of publicprivate partnerships and technology transfer programs can facilitate the dissemination and adoption of AI-based greenhouse management systems, particularly in developing countries and resource-limited settings (Forkuor et al., 2022;Maraveas et al., 2022). By working together to push the frontiers of AI and greenhouse science, we can build a more productive, equitable, and sustainable food system that can feed the world while protecting the planet for future generations.

## 7. Conclusion

Greenhouse cultivation ensures global food security and promotes sustainable agricultural development. Temperature management is a central element of greenhouse crop production. This paper systematically reviews the research progress of AI technology in greenhouse temperature prediction and control, with a focus on the comparative analysis of the strengths and limitations of various AI methods (Fig. 6).

The main conclusions are as follows:

(1) Deep learning models (such as CNN, RNN, and Transformer) demonstrate high performance in greenhouse temperature prediction, with typical RMSE values ranging from 0.3 to 1.3℃, and R 2 values ranging from 0.96 to 0.99. Compared to traditional methods, deep learning models can automatically extract abstract features from vast, multimodal sensor data to construct precise nonlinear dynamic temperature models.

(2) Fuzzy logic systems effectively manage complex, nonlinear, and multivariable coupled greenhouse environments regarding greenhouse temperature control decisions. MPC can achieve precise regulation and energy efficiency optimization, while RL continuously learns from historical data and real-time feedback to provide adaptive and robust control strategies. As analyzed in Section 5.5, these methods are complementary, fuzzy logic offers interpretability, MPC provides optimization precision, and RL enables adaptability, and can be selected or integrated according to specific application needs and constraints.

(3) The Internet of Things, wireless sensor networks, and multimodal data fusion technologies are vital supports for intelligent greenhouse management. Advances in sensor technology have enabled precise monitoring of greenhouse environments and multi-scale, multidimensional data acquisition. Multimodal data fusion methods (deep multimodal encoders and multi-cluster techniques) can integrate heterogeneous sensor data to provide comprehensive and reliable greenhouse state information, offering high-quality input for AI prediction and control models.

Despite the significant potential of AI in greenhouse temperature management, practical applications still face many challenges, such as model robustness, interpretability, and computational efficiency. Future research should focus on developing plant-centered AI models, exploring AI for sustainable energy management in greenhouses, and developing AI-enabled greenhouse-earth system digital twin models, as elaborated in Section 6.

This paper reviews the latest advances in AI for greenhouse temperature prediction and control, analyzing the strengths, limitations, and applications of methods such as neural networks, deep learning, fuzzy logic, MPC, and RL. It also examines how data-driven technologies support intelligent greenhouse management and analyzes key challenges in applying AI to real greenhouse systems, providing insights for future research.

### CRediT authorship contribution statement

### Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Figures et tableaux

**Fig. 1.** Evolution of greenhouse temperature prediction and control technologies. The figure illustrates the progression from traditional to AI-driven methods, highlighting key developments in AI and their application to greenhouse management over different periods.

[figure sans légende identifiée] Computers and Electronics in Agriculture 237 (2025) 110603

**Fig. 2.** Illustration of the architecture and data flow in a deep learning model for greenhouse temperature prediction.

[figure sans légende identifiée] Computers and Electronics inAgriculture 237 (2025) 110603

**Fig.5.** Architecture of an intelligent control system for greenhouse temperature control, showcasing the integration of various components and technologies. The system combines data acquisition from sensor networks, data preprocessing and analysis, machine learning and adaptation, and decision-making and optimization modules to provide a comprehensive and autonomous control framework. The intelligent control system interacts with the greenhouse environment through actuators and interfaces while learning from the system's behavior and performance to continuously improve its control strategies.

**Fig. 6.** Comprehensive framework for AI application in greenhouse temperature prediction and control (P&C). The figure illustrates the transition from traditional methods to integrated AI solutions, highlighting key components such as AI prediction and control methods, data-driven technologies, and their interactions. It also outlines the limitations of traditional approaches, challenges in AI implementation, and future directions for research and development in this field.

Jingxin Yu: Writing -original draft, Validation, Methodology. Congcong Sun: Writing -review & editing, Visualization, Supervision, Formal analysis. Jinpeng Zhao: Writing -original draft, Visualization, Software, Methodology, Data curation. Lushun Ma: Writing -review & editing, Visualization, Software, Methodology. Wengang Zheng: Writing -review & editing, Supervision, Investigation, Funding acquisition. Qiuju Xie: Writing -review & editing, Supervision, Project administration, Methodology, Formal analysis. Xiaoming Wei: Resources, Conceptualization.

**Table 1** 

     | Artificial Intelligence | IoT | Internet of Things
    ANFIS | Adaptive Neuro-Fuzzy Inference System | LSTM | Long Short-Term Memory
    ANN | Artificial Neural Network | MAE | Mean Absolute Error
    BP | Back Propagation | MAPE | Mean Absolute Percentage Error
    CNN | Convolutional Neural Network | MLP | Multi-Layer Perceptron
    DL | Deep Learning | MPC | Model Predictive Control
    DNN | Deep Neural Network | MSE | Mean Squared Error
    DQN | Deep Q-Network | PCM | Phase Change Material
    EMD | Empirical Mode Decomposition | PID | Proportional-Integral-Derivative
    FFNN | Feed Forward Neural Network | PPO | Proximal Policy Optimization
    GRU | Gated Recurrent Unit | RBF | Radial Basis Function
    RMSE | Root Mean Square Error | RNN | Recurrent Neural Network
    RL | Reinforcement Learning | SVM | Support Vector Machine
    SVR | Support Vector Regression | TES | Thermal Energy Storage
    WNN | Wavelet Neural Network | WSN | Wireless Sensor Network

**Table 2** Data acquisition and Processing Systems for greenhouse temperature control.

    System | Key components | Functionality | Benefits | Reference
    Arduino-based | Arduino, DHT22, | Real-time monitoring | Accurate, low cost | Anisha et al. (2021)
     | BH1750 sensors |  |  | 
    WSN-based | WSN, cloud server, | Data transfer, local | Enhanced control | Ouni and Saleem
     | Bluetooth | inspection |  | (2022)
    IoT-based | IoT, temp/humidity | Automatic data | Real-time analysis | Bersani et al. (2022)
     | sensors | collection |  | 
    Microcontroller | MSP430F149, CC2530 | Data processing and | Comprehensive | Chen Pengzhan and
     |  | display | monitoring | Liu Baifen (2010)
    Autonomous robot | Sensors, mapping | Environmental data | 3D mapping | Atefi et al. (2019)
     | capabilities | collection |  | 
    Arduino control | Arduino Uno, | Real-time display, | Efficient control | Jafar et al. (2014)
     | Atmega328 | automatic cooling |  | 
    FPGA-based | FPGA chip, GPRS | Data processing and | Real-time monitoring | Benyezza et al.
     | module | display |  | (2023)
    Cloud-based | Cloud platform, mobile | Remote communication | Smart systems, big data | Munoz et al. (2022)
     | client |  |  | 

**Table 3** Multimodal data fusion techniques in greenhouse temperature management.

    Technique | Key features | Applications | Benefits | Reference
    Moving least square | Optimal sensor placement | Reduced measurement | Precise data collection | Qiao et al. (2022)
     |  | errors |  | 
    Adaptive weighted | Enhanced data precision and | Real-time monitoring, | Accurate, reliable data | Wang et al. (2018)
    fusion | reliability | remote control |  | 
    Time and spatial fusion | Management of slow-changing | Reduced data transmission | Energy conservation | Wei et al. (2017)
     | parameters |  |  | 
    Minimum distance | Improved objectivity and | Optimal crop growth | Precise control | Hang et al. (2017) and Cai
    clustering | accuracy | conditions |  | et al. (2024)
    Two-level data fusion | Integration of key parameters | Stabilized environment | Enhanced crop growth | Bai et al. (2019)
    Improved Kalman filter | Enhanced reliability and | Accurate real-time | Robust data collection | Ullah et al. (2020)
     | anti-interference | monitoring |  | 
    Multi-cluster techniques | Reduced uncertainty and error | Optimized parameter | Boosted economic | Ono (2023)
     |  | adjustments | benefits | 
    Multi-sensor fusion | Intelligent control systems | Data fusion challenges | Improved performance | Majumder and Pratihar (2018)
    Neural network models | Growth and price forecasting | Maximized profitability | Optimized control | Alhnaity et al. (2020)
     |  |  | strategies | 

**Table 4** Comparison of traditional model prediction methods.

    Model type | System dynamics model | Energy balance model
    Mathematical principle | Describes the dynamic behavior of | Focuses on the energy flows and temperature
     | greenhouse temperature using | changes in the greenhouse
     | differential equations | 
    Inputs | Greenhouse geometry and orientation, | Thermal properties of greenhouse components,
     | solar radiation intensity, heating system | solar radiation intensity, heating system
     | capacity and schedule, ventilation rate, | capacity and schedule, ventilation rate, cover
     | cover material properties | material properties, plant evapotranspiration
     |  | rate
    Outputs | Indoor air temperature | Net energy gain or loss in the greenhouse
    Prediction accuracy (RMSE) | 1.2 • C-2.5 • C | 1.5 • C-1.8 • C
    Computational efficiency | Faster (e.g., 1 min per simulation run) | Slower (e.g., 5 min per simulation run)
    Advantages | Simpler model structure, fewer input | More comprehensive energy analysis and
     | parameters required, faster computation | higher prediction accuracy account for plant
     |  | transpiration
    Disadvantages | Lower prediction accuracy in complex | Requires extensive data inputs, computationally
     | environments, neglects some energy | demanding, challenging to implement in
     | transfer processes | real-time control
    Application | Huang et al. (2021) | Badji et al. (2023)

**Table 5** Analysis and evaluation of different Greenhouse Temperature Prediction Methods.

    Method | Advantages/ Disadvantages | Typical case | Prediction performance
    RBF | Good for small | Bolandnazar et al. | 
     | datasets/Sensitive to | (2023) | 
     | parameters |  | 

[figure sans légende identifiée] employed a DNN model with the same input variables to forecast greenhouse temperature 24 h in advance. Other studies have focused on shorter prediction horizons, such as one hour ahead. Dai et al. (2022) proposed a Wavelet Neural Network (WNN) model that used temperature, humidity, and solar radiation as inputs to predict greenhouse temperature one hour in advance. Kim et al. (2018) developed a BP network to forecast greenhouse temperature one hour ahead, obtaining an RMSE of 1.72 • C.

**Table 6** Computers and Electronics in Agriculture 237 (2025) 110603 Comparison of deep learning models for greenhouse temperature prediction.

    Reference | Model | Input variables | Performance | Time horizon | Model depth
    Moon and Eek Son | BiLSTM | T, H, C, R | R 2 : 0.78 (Sweet Pepper), 0.81 | Using 24 h data to predict | 3 layers
    (2021) |  |  | (Tomato) | next 24 h | 
    Eraliev and Lee | LSTM | T, H, C | Best performance at shorter | 1-week data, intervals: 1-15 | Not specified
    (2023) |  |  | intervals | min | 
    Jung et al. (2022) | LSTM | oT, oH, C, R, WS, SS, CFS, | RMSE: 0.00317 and 0.00356 | 30 min | 3 layers
     |  | HVO, CIR, TS, ST, SWO, WD, | kg m -2 s -1 |  | 
     |  | iT, C, iT, LT, SVWC |  |  | 
    Oh et al. (2022) | GRU | oT, WS, SR, H, iT, RF, WD | RMSE = 0.5857, | 25 min | 3 layers
     |  |  | R 2 =0.9848 • C |  | 
    Belhaj Salah and | ElmanNN | iT, oT, iH, oH, WS, SR, SP, | Good control performance | 12 h | 4 layers
    Fourati (2021) |  | HT, VW |  |  | 
    Clemente et al. | Global | SR, RH, aT, DP, CC | Improved predictive | 12 h | 8 layers
    (2023) | Transformer |  | performance |  | 
    Han et al. (2023) | LSTM, BI-LSTM, | H, C, ST, SR, dpH | R 2 : 0.953 (LSTM), 0.946 | 30 min | 3 layers
     | GRU |  | (BI-LSTM), 0.950 (GRU) |  | 
    Jin et al. (2021) | BEDA | T, H, C, LI, TR, NR, AP, WD, | R 2 : 0.749 (T), 0.848 (H), | Using 12 h data to predict | Not specified
     | (CNN-based) | WS, RF | 0.8711 (C) | next 12 h | 
    Codeluppi et al. |  |  |  |  | 

**Table 7** Hybrid model architectures for greenhouse temperature prediction.

    Category | Math. | Advant. | Disadv. | Applications | Complexity | Data Req.
     | formulation |  |  |  |  | 
     |  | Residual learning | Dependence on initial | Known dynamics | Med-High | High
     |  | Trend capture | model | Climate modeling |  | 
     |  | High accuracy | Integration complexity |  |  | 
    Parallel | 𝑇 𝑝𝑟𝑒𝑑 = 𝛼 ⋅ 𝑇 𝑚𝑒𝑐ℎ + | Combined strengths | Weight balancing | Weather prediction | Medium | Medium
     | (1 -𝛼) ⋅ 𝑇 𝐴𝐼 | Adaptive weighting | Model disagreement | Real-time control |  | 
     |  | Balanced performance |  |  |  | 
    Hierarchical | 𝑇 𝑝𝑟𝑒𝑑 = | Structured processing | Design complexity | Multi-scale models | High | High
     | 𝑓 𝑙𝑎𝑦𝑒𝑟 (𝑇 𝑙𝑎𝑦𝑒𝑟-1 , 𝑋) | Task-specific models | Computational intensity | Yield prediction |  | 
     |  | Improved |  |  |  | 
     |  | interpretability |  |  |  | 
    Iterative | 𝑇 (𝑛+1) 𝑝𝑟𝑒𝑑 = | Incremental | Computational expense | Long-term forecasting | High | High
     | 𝑇 𝑚𝑜𝑑𝑒𝑙 (𝑇 (𝑛) 𝑝𝑟𝑒𝑑 , 𝑋) | Multiple iterations improvement | Overfitting risk | Optimization problems |  | 
     |  | Evolving dynamics |  |  |  | 
    (2004) employed a serial hybrid model combining a physical model |  |  | 
    with an RBF neural network to ensure reliable temperature predic- |  |  | 
    tions across different operating domains. The model utilized seasonal |  |  | 
    weather data as input variables and demonstrated effectiveness over |  |  | 
    yearly time horizons. Shi et al. (2024) proposed a hybrid model that |  |  | 
    combines CNN and LSTM to predict air temperature, relative humidity, |  |  | 
    and photosynthetically active radiation in a greenhouse. Their model |  |  | 
    achieved high accuracy, with average errors of 0.540 • C, 0.936%, and |  |  | 
    1.586 W/m 2 for temperature, humidity, and solar radiation, respec- |  |  | 
    tively. |  |  |  |  |  | 
    Table |  |  |  |  |  | 

**Table 8** Representative hybrid models for greenhouse temperature prediction and control.

    Model type | Hybrid architecture | Effectiveness | Input variables | Time horizon | Reference
    Serial | Physical model + RBF | Reliable across operating | Seasonal weather data | Yearly | Linker and Seginer
     |  | domains |  |  | (2004)
    Serial | MLD + Time-series | Effective control | External air temp., | Short-term | Guoqi et al. (2015)
     |  |  | humidity, solar radiation, |  | 
     |  |  | wind speed |  | 
    Parallel | Transformer-BiLSTM | High accuracy (MSE: | 18 environmental | 5 min | Yu et al. (2025)
     |  | 0.06 • C, R 2 > 0.998) | parameters |  | 
    Parallel | Attention CNN-LSTM | High accuracy (MAE: | Temperature, humidity, | Not specified | Huang et al. (2024)
     |  | 0.17 • C, R 2 > 0.936) | CO 2 |  | 
    Parallel | RNN-LSTM | High R 2 values | Temperature, humidity, | 5-30 min | Jung et al. (2020b)
     |  | (Temperature: 0.96, | CO 2 |  | 
     |  | Humidity: 0.80, CO 2 : 0.81) |  |  | 
    Parallel | Model predictive hybrid | Optimal control signals | Weather variables | Nocturnal | Montoya et al. (2016)
     | controller |  |  |  | 
    Parallel | Time-series + LightGBM | Reduced MSE, improved R 2 | Time-series features, | Short-term | Cao et al. (2023)
     |  |  | environmental parameters |  | 
    Parallel | IBP + Genetic Algorithm | High accuracy, low RMSE | External air temp., | Short-term | He et al. (2007)
     |  |  | humidity, wind speed, |  | 
     |  |  | solar radiation |  | 
    Iterative | RBF + offline/online | Effective off-line and | External air temp., solar | Short-term | Ferreira et al. (2002)
     | learning | on-line learning | radiation, internal |  | 
     |  |  | humidity |  | 
    Iterative | ARX + ARMAX | High accuracy, retuning | External air temp., | Yearly | Frausto et al. (2003)
     |  | required | humidity, solar radiation |  | 
    Hierarchical | Hybrid automata + | Economic optimization | External air temp., | Variable | Rodríguez et al. (2008)
     | ARMAX |  | humidity, solar radiation |  | 
    Hierarchical | Mixed logical dynamical | Effective control | Internal temp., operational | Variable | Jiao et al. (2017)
     | system + Propositional |  | constraints |  | 
     | calculus |  |  |  | 

**Table 9** Comparative analysis of AI models for greenhouse temperature prediction.

    Model | Strengths | Limitations | Data | Computational | Application scenarios
     |  |  | requirements | needs | 
    ANN | Captures nonlinear relationships | Limited temporal dependency | Moderate | Moderate | General predictions
     | Simple structure | handling |  |  | with moderate accuracy
     |  | Requires large datasets |  |  | 
    DL | Learns hierarchical features | High computational cost | High | High | Large-scale data with
     | Captures spatial-temporal patterns | Complex and lengthy training |  |  | high precision demands
    Hybrid | Integrates domain knowledge | Complex to implement | Low to | Moderate to | Physically-based
     | High interpretability | Sensitive to data quality | Moderate | High | modeling scenarios

**Table 10** Comparison of traditional temperature control methods.

    Method | Technology |  | Advantages |  | Disadvantages | Scenarios
    Manual control | Thermometers, |  | Low cost, flexible, | Labor-intensive, skill-dependent, | Small-scale greenhouses,
     | hygrometers, visual |  | immediate intervention | inconsistent, human error | low-budget operations
     | observation |  |  |  | 
    Mechanical control | Thermostats, RTDs, |  | Automated, constant | High cost, limited adaptability, | large-scale greenhouses,
     | thermocouples, automatic | temperature, integration | maintenance required, energy wastage, | stable environmental
     | fans/vents |  | with systems, reduced | system failures | conditions
     |  |  | error |  | 
    Hybrid control | Manual/Mechanical |  | Automated with overrides, | Complex setup, high investment, | Medium to large
     | combo, smart thermostats, | flexible, reliable, |  | balancing inputs, manual reliance in | greenhouses, dynamic
     | sensors with overrides |  | energy-efficient |  | emergencies | environments
    Table 11 |  |  |  | 
    Applications of fuzzy logic in greenhouse temperature control. |  | 
    Application | Key findings |  |  | Reference
    Multi-source power systems | Efficient management of renewable energy sources | Riahi et al. (2021)
     |  | and battery storage systems | 
    Hydroponic systems | Improved plant growth with larger leaves and fruit | Sabrina et al. (2022) and
     |  | sizes |  |  |  | Khafajeh et al. (2023)
    Wireless data monitoring | Real-time data access and control, enhancing | Azaza et al. (2016)
     |  | responsiveness and efficiency | 
    Table 12 |  |  |  |  | 
    Applications of MPC frameworks in greenhouse temperature control. |  | 
    Literature | Prediction model | Control method | Control variables |  | Main results | Challenges
    Piñón et al. | MPC + Feedback | Constrained MPC | Temperature |  | Effective control under | Nonlinear constraints
    (2005) | Linearization |  |  |  |  | disturbances
    Chen et al. | Nonlinear physical | PSO-based robust | Temperature |  | High precision and robustness | Online minimax
    (2018) | model | MPC |  |  |  | optimization
    Achour et al. | Mathematical Model | Supervisory MPC | Temperature, CO 2 , |  | Optimized climatic variables | System integration
    (2020) |  |  |  | Humidity, Lighting | 
    Bersani et al. | Energy and mass | Multiobjective MPC | Temperature, Energy | 30% energy saving | Implementing GCHP and
    (2021) | balances |  |  |  |  | solar radiation
    Gong et al. | Climate and Crop | PSO-MPC |  | Heating, Lighting, |  | Increased yield, minimized | Optimizing parameters
    (2023) | Yield Models |  |  | Ventilation |  | energy costs
    Hamidane | State Space Model | Constrained Discrete | Temperature |  | Accurate control, reference | Complex optimization
    et al. (2024) |  | MPC |  |  |  | tracking
    Ito and Hara | Recursive Least | Adaptive MPC + | Temperature |  | 20%-35% error reduction | Multi-point measurement
    (2017) | Squares | Genetic Algorithm |  |  | complexity
    Mahmood | Multilayer Perceptron | MPC |  | Temperature |  | 7.70% energy saving in | Tuning model for new
    et al. (2021) | Model |  |  |  |  | winter, 16.57% in summer | data sets
    Wang and | Adaptive Model | Adaptive MPC | Temperature |  | Stable control, adaptive | Time-varying dynamics
    Wang (2020) |  |  |  |  |  | adjustments
    Fan et al. | Improved SVR | MPC |  | Temperature |  | Improved prediction accuracy | Hyper-parameter
    (2021) |  |  |  |  |  | optimization
    Ajagekar | Deep Reinforcement | AI-based MPC | Temperature |  | 57% energy reduction over | Training and validating
    et al. (2023) | Learning Model |  |  |  |  | traditional control | the model
    Li et al. | CFD Simulations and | Hierarchical |  | Temperature, Humidity,
    (2023) | Energy Balance | Optimization MPC | CO 2 | 

**Table 13** Applications of reinforcement learning in greenhouse temperature control.

    Literature | Algorithm | Simulation | State variables | Action variables | Main Results | Challenges
     |  | environment |  |  |  | 
    Wang et al. | Q-learning | Cucumber | CO 2 , Temperature | Fruit weight, | Improved yield, | Reward structure,
    (2020) |  | simulator |  | Cost | reduced costs | single control
     |  |  |  |  |  | variable
    Ajagekar and | Q-learning | Semi-closed | State-action value | Continuous | Higher returns, 61% | Continuous action
    You (2022a) |  | greenhouse |  | action | energy savings | handling
    Chen et al. | SAM network | Venlo | Temperature, | Skylight, Fan | Reduced energy | Safe exploration,
    (2023) |  | greenhouse | Humidity |  | consumption | optimization
    Hemming et al. | Ensemble models | Autonomous | Temperature, | Planting policy | Effective, robust | Sample efficiency,
    (2019) |  | greenhouse | Humidity, Light, |  | planting policy | safety
     |  |  | CO 2 |  |  | 
    Chen and You | DDRMPC | Semi-closed | Temperature, | Heating, | 14-66.9% energy | Model complexity,
    (2022) |  | greenhouse | humidity, CO 2 | ventilation | savings | safety
    2023), and addressing the sample complexity and computational re- | considering temperature, humidity, and CO 2 simultaneously is a com-
    quirements of training RL agents. Moreover, the transfer of RL policies | plex challenge that requires advanced RL techniques
    learned in simulation to natural greenhouse environments may be |  |  | 
    hindered by modeling uncertainties, sensor noise, and hardware limita- |  |  | 
    tions. Additionally, multi-variable control of greenhouse microclimate |  |  | 

**Table 14** Applications of intelligent control systems in greenhouse temperature control.

    Literature | System architecture | Technologies | Application scenario | Main Results | Challenges
    Joudi and | Innovative greenhouse | Dynamic thermal | Winter temperature | Achieved 16 • C winter | Model validation,
    Farhan (2015) | with roof solar air | model, solar air heaters | enhancement | temp difference | system scaling
     | heaters |  |  |  | 
    Zhao et al. | IoT, LORA network | Multi-parameter | Cash crop planting | Improved efficiency, | Network reliability,
    (2019) |  | sensors, |  | crop quality | complexity
     |  | automatic/manual |  |  | 
     |  | control |  |  | 
    Nicolosi et al. | Neural network, fuzzy | Forecasting, fan-coil | Microclimatic | Better climate control, | System tuning,
    (2017) | control | adjustment | control | plant growth | computational needs
    Lee et al. (2024) | Host-slave computer | Multi-environment | Real-time control of | Optimal crop growth | Initial cost, complexity
     |  | sensors | temp, humidity, CO 2 |  | 
    Chen Pengzhan | Distributed control, | ARM processor, | General greenhouse | Stable performance, | System complexity,
    and Liu Baifen | CAN bus | temp/humidity sensors | control | economical | setup
    (2010) |  |  |  |  | 
    Castañeda- | IoT, ANN, fuzzy control | Anti-frost irrigation, | Frost control | Accurate prediction, | System integration
    Miranda and |  | neural network |  | effective frost control | complexity
    Castaño-Meneses |  |  |  |  | 
    (2020) |  |  |  |  | 
    Jafar et al. | Arduino UNO, wireless | Real-time processing, | Smart greenhouse | Improved productivity, | Data acquisition
    (2014) | communication | sensor network | management | monitoring | complexity, cost
    Subahi and | IoT, Petri Nets model | Scalable, | Extreme climate | Improved productivity, | Massive IoT data
    Bouazza (2020) |  | energy-efficient design | control | efficiency | handling, complexity
    Maulana et al. | Model predictive | Smart sensor block, | Single-span | Increased reliability, | Adaptability, cost
    (2023) | controller | LabVIEW | greenhouses | user-friendly | 
    Alpay and | Android interface, | Fuzzy logic, remote | Smart greenhouse | Accurate control, | Data integration, cost
    Erdem (2018) | wireless network | monitoring | climate control | reduced energy/water | 
     |  |  |  | use | 
    Huang (2023) | PLC, MCGS software | Sensors, PID control | Modern agriculture | Optimized growth, high | System integration, cost
     |  |  |  | yield | 
    Mahfuz et al. | Microcontroller, | Sensor integration, SMS | Smart farming | Effective monitoring, | Reliability, data
    (2020) | wireless communication | alerts |  | remote control | handling

**Table 15** Comparative analysis of fuzzy logic, MPC, and RL in greenhouse temperature control.

    Approach | Strengths | Suitable environments
    Fuzzy logic | Handling nonlinear interactions and | Complex and nonlinear system dynamics
     | interdependencies | 
    MPC | Precise control with energy efficiency | Predictive control for optimal conditions
     |  | and energy minimization
    RL | Adaptive and robust solutions leveraging | Dynamic environments requiring learning
     | historical and real-time data | and adaptation
