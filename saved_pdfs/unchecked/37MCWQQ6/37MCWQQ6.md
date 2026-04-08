Proceedings of the Second International Conference on Electronics and Sustainable Communication Systems (ICESC-2021) IEEE Xplore Part Number: CFP21V66-ART; ISBN: 978-1-6654-2867-5 

## A comparative study of machine learning and  deep learning algorithms for recognizing facial emotions 

## Amritha Krishnadas 

Department of Electrical and Electronics Engineering Amrita School of Engineering, Coimbatore Amrita Vishwa Vidyapeetham, India amrithakrishnadasak@gmail.com 

## S. Nithin 

Department of Electrical and Electronics Engineering Amrita School of Engineering, Coimbatore Amrita Vishwa Vidyapeetham, India s_nithin@cb.amrita.edu 

_Abstract_ — **This article compares the performance of three algorithms for Facial Emotion Recognition (FER). The algorithms chosen include one machine learning model – Support Vector Machine (SVM) and two deep learning models – Convolutional Neural Network (CNN) and VGG16. All three algorithms were implemented using Python and evaluated on FER2013 dataset. The metrics used for comparison were testing accuracy, training time and the size of the weights file. The best performing algorithm from the study is used to implement FER in real time on a live video stream. The implementation details are presented and results are discussed.** 

_**Keywords—Facial Emotion Recognition, Convolutional Neural Networks, Support Vector Machines, VGG16, Transfer Learning, Haar Cascade classifier**_ 

## I. INTRODUCTION 

Facial expressions are some of the best ways a person communicates with the outside world. It reflects the thoughts, beliefs and the emotions experienced by a person; thereby showcasing their mental state. FER can be defined as the process of detecting and recognizing a person’s emotions with the help of their facial expressions [1] and hence can be employed for non-verbal communication [2]. With the recent advancements in humanoid robots, FER is utilized for multiple applications [3][4]. These include lie detection, understanding certain mental disorders, analyzing customer reactions and many more. 

The process of recognizing facial emotions requires the use of Machine Learning (ML) or Deep Learning (DL) models. The various ML approaches include Support Vector Machine (SVM) [5], Naive Bayes algorithm, decision trees and random forest. The deep learning approaches include Convolutional Neural Network (CNN) [3], Recurrent Neural Networks (RNN), deep Boltzmann machine and Long Short-Term Memory (LSTM). 

An efficient dataset and an understanding of the ML and DL algorithms usage can help in improving the 

accuracy with a reduced training time. B.Balasubramanian et al. [1] discuss on the various ML and DL algorithms used for the FER application. The article also holds a detailed explanation on the FER datasets such as CK+, JAFFE, FER2013, AFEW and EmotioNet and details such as the number of images held in each set, the different expression categories, different illumination and background noises present. The authors concluded that the SVM model outperformed the other ML models for real time FER application and the CNN provided better accuracy than the ML models. The relevance and usage of ML and DL is explained in the analysis done by J. L. Berral-García [6]. The author explained scenarios where the ML and DL models will yield optimal accuracy. It was concluded that the usage of the algorithms depends upon the complexity of the problem considered, starting from Bayesian networks to complicated neural networks. 

Extensive research has taken place to obtain an optimal algorithm with reduced training time and without sacrificing the accuracy. The work done by Ahmed T et.al [3] is a comparative study for facial recognition of 10 different identities. The models chosen for the comparison were VGG16, VGG19 which used pretrained weights and AlexNet and MobileNet which were developed afresh. It was observed that the MobileNet model provided the highest test accuracy. A similar comparison of metrics such as precision, recall and f1score of the LeNet-5, AlexNet, VGG-16, ResNet50 and Inception-V1 model for an image classification application is explained by Parvin F et.al [7]. The InceptionV1 model achieved the highest test accuracy. A similar comparison for the classification of flowers was done by Wu Y et.al using CNN and the DL models employing transfer learning [8]. The authors concluded that the transfer learning model converges better and faster with improved generalization ability and robustness. The work done by Draško Radovanović et.al [9] compares the ML and DL model for early plant disease detection. The algorithms considered were SVM, k-nearest neighbor (k-NN), fully connected CNN and CNN model. A similar comparison was performed by 

978-1-6654-2867-5/21/$31.00 ©2021 IEEE 

1506 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on January 22,2023 at 17:36:28 UTC from IEEE Xplore.  Restrictions apply. 

Proceedings of the Second International Conference on Electronics and Sustainable Communication Systems (ICESC-2021) IEEE Xplore Part Number: CFP21V66-ART; ISBN: 978-1-6654-2867-5 

Wibawa M.S [10] in classifying the white blood cells, typically to lymphocytes and neutrophils. The classification was conducted on secondary data from Kaggle dataset using Multi-Layer Perceptron (MLP), k- NN, SVM and CNN. A comparison of Naïve Bayes, VM, decision trees, LSTM, CNN and Word Embedding for classifying emails as phishing or non-phishing was performed by Sikha Bagui et.al [11]. It was observed that for [9],[10] and [11], the DL models outperformed the ML models considered. 

SVM is a popular ML model where its accuracy depends hugely on the hyperparameters like the gamma, C value and the kernel used [5]. An effect of using 4 different kernels for FER application has been discussed by Adeyanju IA et.al [5]. In addition to this, the comparison between radial basis, linear, quadratic and polynomial function with performance as the comparison metric was discussed. The quadratic kernel yielded maximum accuracy followed by the polynomial one. Since the development and use of the humanoid robots are increasing nowadays, the real time face and emotion recognition are also having increasing importance. Rajesh KM et.al has discussed on real time method for face recognition and facial emotion recognition using SVM [12]. It was found that the more the images to compare, the better was the accuracy of the face recognition. The FER involved steps like face detection, facial feature extraction and emotion detection. The images were trained and tested in real time and the various metrics like the accuracy and training time were analyzed. 

CNN’s are popular ANN models consisting of multiple layers so as to classify the images as required [13]. The classification performed can be binary, multi class or a combination of both. The work proposed by Karunakaran P [14] uses both binary and multi class classification for detecting domain generation algorithm. It was concluded that proposed system generated better accuracy than the CNN or RNN methods. The research proposed by Lasri et.al [15] is a FER system based on CNN that recognizes the emotions of the students based on their facial expressions. This model consisted of four layers where faces were detected, cropped and normalized before feeding to the convolutional layers. The confusion matrix for the model showed better performance for the happy and surprise emotions. Thus, the authors concluded that SVM, CNN and VGG16 models, trained under FER2013 dataset would be suitable for the comparison for FER application. The research by Ochin Sharma et al. showcase the limitations of the DL model [16]. It was concluded that the DL limitations mainly focused on the number of images in the dataset, number of hidden layers and the hyper parameter selection. 

This article focuses on comparing one ML approach – SVM and two DL approaches – CNN and VGG16 [8] for FER application. Both the SVM and the CNN models were implemented afresh and the VGG16 model was 

implemented using transfer learning approach. All the three algorithms were trained using the FER2013 dataset.[17]. The comparison metrics used for the work include the testing accuracy, training time and weights file size. Based on the accuracies and the training time, an optimal efficient algorithm is identified and a real time implementation of FER using the same is also performed. The real time implementation was done with the help of libraries like the OpenCV and various Keras Application Programming Interfaces (APIs). 

Section II provides an insight about the algorithms, results and conclusions drawn from it. Section III presents the process flow and results for the real time implementation and Section IV concludes this article. 

## II. COMPARING ALGORITHM IMPLEMENTATION, RESULTS AND ANALYSIS 

FER involves multiple sub process that helps in obtaining the maximum accuracy [12]. Human face from the input image is initially detected using the Haar Cascade classifier. This step is followed by extracting the required features with the help of multiple convolutional layers present in the architecture.  The final step is to classify them based on their emotions. The general flow diagram for FER is depicted in fig 1. 

## _A. CNN_ 

CNN is a DL, feed forward ANN model [13]. dependency of a neuron to only its adjacent ones from the previous stage, makes a CNN model more reliable when compared to a fully connected one. CNN consists of multiple layers that helps in feature extraction process [18]. The output from the convolutional layers is a feature map that is provided as an input to a pooling layer. The pooling layers helps in reducing the size of the feature map obtained and it is subsequently followed by an activation function which can be sigmoid, hyperbolic tangent (Tanh), SoftMax or rectified linear unit (ReLu) functions. This is followed by the fully connected layers that helps in classification. 


![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0002-11.png)


Fig.1 Flow diagram for FER 

978-1-6654-2867-5/21/$31.00 ©2021 IEEE 

1507 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on January 22,2023 at 17:36:28 UTC from IEEE Xplore.  Restrictions apply. 

Proceedings of the Second International Conference on Electronics and Sustainable Communication Systems (ICESC-2021) IEEE Xplore Part Number: CFP21V66-ART; ISBN: 978-1-6654-2867-5 

The CNN model considered for the analysis contains three convolutional layers, followed by a fully connected layer and an output layer. The three convolutional layers contain 128, 256 and 512 filters respectively, each having a filter size of (3x3) and pooling layers of size (2x2). The convolutional layers are followed by the flattening layer and four dense layers containing 512, 256, 128 and 7 units respectively. ReLu is chosen as the activation function due to its reduced computational cost [16]. 

The input image size taken for consideration is 48x48. Fig.2 shows the architecture of the CNN model considered for analysis. 

## _B. SVM_ 

The capability of the SVM algorithm to provide high accuracy in higher dimensional spaces make it one of the best and powerful algorithms for classification, regression and outlier detecting applications [19]. The classification is done with a hyperplane classifying the support vectors either with zero or minimal outliers [20]... 

The SVM model considered for the comparison utilizes the input image of size of 48x48 pixels which are then fed to the classifier. The classifier used in this work makes use of a low gamma value of 0.01 so that even the support vectors from the farthest end are considered for the classification. The kernel chosen for the classifier is polynomial and the input to this ML is provided with minimal pre-processing. The polynomial kernel [4] can be represented as: 


![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0003-06.png)


The number of pre-processing steps required for the SVM model is higher when compared with a CNN model. This increased pre-processing is required due to the absence of certain steps in SVM like- convolution, pooling etc. which are observed in the CNN. Thus, one of the aims of this article is to showcase the reduction in accuracy for a SVM model compared with a CNN model, considering the same level of pre-processing. Hence, the SVM classifier is implemented with minimal pre-processing. 


![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0003-08.png)



![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0003-09.png)


Fig.2 Architecture of the CNN model considered 

978-1-6654-2867-5/21/$31.00 ©2021 IEEE 

1508 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on January 22,2023 at 17:36:28 UTC from IEEE Xplore.  Restrictions apply. 

Proceedings of the Second International Conference on Electronics and Sustainable Communication Systems (ICESC-2021) IEEE Xplore Part Number: CFP21V66-ART; ISBN: 978-1-6654-2867-5 

## _C. VGG16_ 

The architecture is trained on the ImageNet dataset and can be used either as a pre-trained network or can be developed    afresh for the feature extraction process. For the scope of this work, for reducing the training time and computational complexity for the application, transfer learning approach is opted [21]. In this method of training, the pre-trained weights of the ImageNet dataset are used and only the dense layers will be trained. The uniformity of the architecture makes it one of the most reliable algorithms for the image classification process 

The VGG16 architecture consists of a series of convolutional layers and pooling layers. These layers help the model to pre-process the input provided and classify it as required. The VGG16 architecture considered for the analysis in this work contains all the convolutional layer sets present in the general VGG16 model. A variation was added in it by introducing three dense layers of varying units after the final set of convolutional layers. The first dense layer added contains 512 units, second dense layers containing 256 units and the final dense layer with 7 units, resembling the 7 classes present in the FER application considered. Fig.3 depicts the architecture of the VGG16 model used for the analysis. The notation of the layers used are similar to fig 2. 

The parameters such as training time, weights file size and the testing accuracy are analyzed for all the algorithms mentioned above for the FER application. 

## _D. Results_ 

A comparative study was conducted for recognizing the facial emotions using the SVM, classic CNN and VGG16 models. The training was conducted on FER2013 dataset that consists of 28,709 images falling under 7 categories. The model was implemented using Python and the training was performed using Google Colab. The runtime type for training CNN and VGG 16 was Graphical Processing Unit (GPU) and for the SVM model was Tensor Processing Unit (TPU). All the deep learning algorithms were trained for 50 epochs. Few images from the FER2013 dataset under various category is provided in the fig 4. 

The metrics used for evaluating CNN are testing accuracy, training time and the weights file size. The output for these metrics is as shown in table I. 

TABLE I EVALUATION METRICS FOR CNN MODEL 

|TABLE I EVALUATION|METRICS FOR CNN MODEL|
|---|---|
|**Comparing Metric**|**Obtained Value**|
|Testing Accuracy (%)|57|
|Training Time (minutes)|37|
|Weights file size (MB)|54.4|



The SVM model with the least   pre-processing is used for the analysis. This is done so as to perform a direct comparison with the CNN model. 


![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0004-11.png)


Fig.3 Architecture of VGG16 model considered 

978-1-6654-2867-5/21/$31.00 ©2021 IEEE 1509 Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on January 22,2023 at 17:36:28 UTC from IEEE Xplore.  Restrictions apply. 

Proceedings of the Second International Conference on Electronics and Sustainable Communication Systems (ICESC-2021) IEEE Xplore Part Number: CFP21V66-ART; ISBN: 978-1-6654-2867-5 


![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0005-01.png)


Fig.4 Various emotions from FER2013 dataset (a). Happy, (b). Neutral, (c). Fear, (d) Disgust, (e). Surprise, (f). Angry and (g). Sad 

The testing accuracy, training time and model size obtained for the SVM model trained is provided in table II. 

TABLE II EVALUATION METRICS FOR SVM MODEL 

|**Comparing Metric**|**Obtained**<br>**Value**|
|---|---|
|Testing Accuracy (%)|34|
|Training Time (minutes)|32|
|Model size (MB)|385|



The various metrics like the testing accuracy, training time and size of the weights file for the VGG16 architecture is as shown in table III. 

TABLE III EVALUATION METRICS FOR VGG16 MODEL 

|**Comparing Metric**|**Obtained**<br>**Value**|
|---|---|
|Testing Accuracy (%)|57.3|
|Training Time (hours)|10 - 12|
|Weights file size (MB)|110.8|



## _E. Analysis_ 

From the results obtained in tables I, II and III, it can be concluded that the testing accuracy is highest for the VGG 16 model which was implemented by transfer learning and is followed by the CNN model. The SVM model provides the least accuracy due the absence of pre-processing performed on them. The training time is also highest for the VGG 16 model followed by the CNN model and SVM. Thus, it was observed that the DL model outperformed the ML model as in [9], [10] and [11]. It is also observed that the CNN approach provides good accuracy and reduced training time 

## III. REAL TIME IMPLEMENTATION OF  FER 

## _A. Real time implementation_ 

The real time implementation used a CNN model that has undergone and completed training in the comparison phase. The implementation was completed using Python libraries like the OpenCV [22][23][24] and various Keras [25] APIs. The json model and weights of the trained model are loaded for the recognition process. The input images are initially converted to grayscale so as to reduce the processing time and complexity. This step is followed by the face detection from the live webcam stream which employs the frontal Haar Cascade [26] classifier. The features required for the emotion recognition is then obtained from the region of interest and is fed to the prediction model. The prediction model predicts the input image based on the trained model and classifies it into the corresponding classes. The process flow of the real time model is provided in fig 5. 

## _B. Results_ 

From the values obtained in tables I, II and III under section II, it was observed that CNN model was best performing algorithm in terms of improved accuracy and a shorter training time and hence it is used for the real time implementation. The output of the real time FER system is depicted in fig 6. 

## _C. Analysis_ 

The real time application was implemented using the live video stream from the webcam. The input image after converting to greyscale were subjected to face detection with the help of face Haar Cascade classifier. 


![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0005-18.png)


Fig. 5 Process flow for real time implementation 

978-1-6654-2867-5/21/$31.00 ©2021 IEEE 1510 Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on January 22,2023 at 17:36:28 UTC from IEEE Xplore.  Restrictions apply. 

Proceedings of the Second International Conference on Electronics and Sustainable Communication Systems (ICESC-2021) IEEE Xplore Part Number: CFP21V66-ART; ISBN: 978-1-6654-2867-5 


![](saved_pdfs/unchecked/37MCWQQ6/images/37MCWQQ6.pdf-0006-01.png)


Fig. 6. Output of real time implementation using trained CNN model: (a).Happy, (b) Neutral, (c) Sad, (d) Surprise, (e) Angry and (f) Fear 

Once the face was detected, the required features for the prediction was taken. With the extracted features, the emotion recognition was performed. The application was responsive and took a response time of about 3.57 sec to predict. 

## IV. CONCLUSION 

The performance comparison of SVM, CNN and VGG16 for the FER application was carried out. It was observed that the SVM model provided the least accuracy due to the minimal pre-processing performed which gets better while using CNN due to the multiple layers of convolution and pooling present in it. The highest accuracy and training time was observed for VGG16 classifier. With respect to the training time and the accuracy obtained, a real time implementation using the CNN approach is also performed. The scope of this work can be further enhanced by increasing the number of algorithms for the comparison and also testing the same approaches on multiple datasets. In addition to this, implementation of algorithms on embedded platforms like the Raspberry Pi, Jetson Nano etc. for real time performance analysis is also planned for the future. 

## _**References**_ 

- [1] B. Balasubramanian, P. Diwan, R. Nadar and A. Bhatia, "Analysis of Facial Emotion Recognition," 2019 3rd International Conference on Trends in Electronics and Informatics (ICOEI), Tirunelveli, India, 2019, pp. 945-949, doi: 10.1109/ICOEI.2019.8862731 

- [2] Janina Künecke, Oliver Wilhelm, Werner Sommer, "Emotion Recognition in Nonverbal Face-to-Face Communication," in Journal of Nonverbal Behavior, Apr 2017. [Online]. Available: https://doi.org/10.1007/s10919-017-0255-2 

- [3] T. Ahmed, P. Das, M. F. Ali and M. -. F. Mahmud, "A Comparative Study on Convolutional Neural Network Based Face Recognition," 2020 11th International Conference on 

Computing, Communication and Networking Technologies (ICCCNT), Kharagpur, India, 2020, pp. 1-5, doi: 10.1109/ICCCNT49239.2020.9225688. 

- [4] S. Albawi, T. A. Mohammed and S. Al-Zawi, "Understanding of a convolutional neural network," 2017 International Conference on Engineering and Technology (ICET), Antalya, Turkey, 2017, pp. 1-6, doi: 10.1109/ICEngTechnol.2017.8308186. 

- [5] I. A. Adeyanju, E. O. Omidiora and O. F. Oyedokun, "Performance evaluation of different support vector machine kernels for face emotion recognition," 2015 SAI Intelligent Systems Conference (IntelliSys), London, UK, 2015, pp. 804806, doi: 10.1109/IntelliSys.2015.7361233 

- [6] L. Berral-García, "When and How to Apply Statistics, Machine Learning and Deep Learning Techniques," 2018 20th International Conference on Transparent Optical Networks (ICTON), 2018, pp. 1-4, doi: 10.1109/ICTON.2018.8473910. 

- [7] F. Parvin and M. A. Mehedi Hasan, "A Comparative Study of Different Types of Convolutional Neural Networks for Breast Cancer Histopathological Image Classification," 2020 IEEE Region 10 Symposium (TENSYMP), Dhaka, Bangladesh, 2020, pp. 945-948, doi: 10.1109/TENSYMP50017.2020.9230787 

- [8] Y. Wu, X. Qin, Y. Pan and C. Yuan, "Convolution Neural Network based Transfer Learning for Classification of Flowers," 2018 IEEE 3rd International Conference on Signal and Image Processing (ICSIP), Shenzhen, China, 2018, pp. 562-566, doi: 10.1109/SIPROCESS.2018.8600536. 

- [9] D. Radovanović and S. Đukanovic, "Image-Based Plant Disease Detection: A Comparison of Deep Learning and Classical Machine Learning Algorithms," 2020 24th International Conference on Information Technology (IT), 2020, pp. 1-4, doi: 10.1109/IT48810.2020.9070664 

- [10] M. S. Wibawa, "A Comparison Study Between Deep Learning and Conventional Machine Learning on White Blood Cells Classification," 2018 International Conference on Orange Technologies (ICOT), 2018, pp. 1-6, doi: 10.1109/ICOT.2018.8705892. 

- [11] S. Bagui, D. Nandi, S. Bagui and R. J. White, "Classifying Phishing Email Using Machine Learning and Deep Learning," 2019 International Conference on Cyber Security and Protection of Digital Services (Cyber Security), 2019, pp. 1-2, doi: 10.1109/CyberSecPODS.2019.8885143. 

- [12] K. M. Rajesh and M. Naveenkumar, "A robust method for face recognition and face emotion detection system using support vector machines," 2016 International Conference on Electrical, Electronics, Communication, Computer and Optimization Techniques (ICEECCOT), Mysuru, India, 2016, pp. 1-5, doi: 10.1109/ICEECCOT.2016.7955175. 

- [13] R. Ravi, S. V. Yadhukrishna and R. prithviraj, "A Face Expression Recognition Using CNN & LBP," 2020 Fourth International Conference on Computing Methodologies and Communication (ICCMC), 2020, pp. 684-689, doi: 10.1109/ICCMC48092.2020.ICCMC-000127. 

- [14] Karunakaran.P, "Deep Learning Approach to DGA Classification for Effective Cyber Security", Journal of Ubiquitous Computing and Communication Technologies, vol.02, no.04, pp. 203-213, Jan. 2021, doi: 10.36548/jucct.2020.4.003 

- [15] I. Lasri, A. R. Solh and M. E. Belkacemi, "Facial Emotion Recognition of Students using Convolutional Neural Network," 2019 Third International Conference on Intelligent Computing in Data Sciences (ICDS), Marrakech, Morocco, 2019, pp. 1-6, doi: 10.1109/ICDS47004.2019.8942386. 

- [16] O. Sharma, "Deep Challenges Associated with Deep Learning," 2019 International Conference on Machine Learning, Big Data, Cloud and Parallel Computing (COMITCon), 2019, pp. 72-75, doi: 

978-1-6654-2867-5/21/$31.00 ©2021 IEEE 

1511 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on January 22,2023 at 17:36:28 UTC from IEEE Xplore.  Restrictions apply. 

Proceedings of the Second International Conference on Electronics and Sustainable Communication Systems (ICESC-2021) IEEE Xplore Part Number: CFP21V66-ART; ISBN: 978-1-6654-2867-5 

10.1109/COMITCon.2019.8862453 

- [17] I. J. Goodfellow, D. Erhan, P. L. Carrier, A. Courville, M. Mirza, B. Hamner, W. Cukierski, Y. Tang, D. Thaler, D.-H. Lee et al., “Challenges in representation learning: A report on three machine learning contests,” in International Conference on Neural Information Processing. Springer, 2013, pp. 117– 124. 

- [18] Saj T K, Sachin. (2020). Facial Emotion Recognition Using Shallow CNN. 10.13140/RG.2.2.32695.88483 

- [19] “Advantages and   Disadvantages of     SVM”, medium.com, https://dhirajkumarblog.medium.com/top-4-advantages-anddisadvantages-of-support-vector-machine-or-svma3c06a2b107, (accessed 10 Jan). 

- [20] A. Baskar and Dr. Gireesh K. T., “Facial Expression Classification Using Machine Learning Approach: A Review”, in Advances in Intelligent Systems and Computing, 2018, vol. 542, pp. 337-345. 

- [21] N. Damodaran, Sowmya V., Govind, D., and Dr. Soman K. P., “Scene Classification using transfer Learning”, in Studies in Computational Intelligence, vol. 804, Springer Verlag, 2019, pp. 363- 399, Springer, Cham. 

- [22] Saxena, Suchitra & Palaniswamy, Suja & Tripathi, Shikha. (2016). Real-time emotion recognition from facial images using Raspberry Pi II. 666-670. 10.1109/SPIN.2016.7566780 

- [23] “Opencv”, opencv.org, https://opencv.org/ (accessed 19 Feb). 

- [24] K. Padmavathi and S. Nithin, "Comparison of Image processing techniques for detecting human presence in an image," 2019 3rd International Conference on Trends in Electronics and Informatics (ICOEI), 2019, pp. 383-388, doi: 10.1109/ICOEI.2019.8862692 

- [25] “Keras.”, keras.io, . https://keras.io/ (accessed 1 Oct) 

- [26] P. Viola and M. Jones, “Rapid object detection using a boosted cascade of simple features,” in Proceedings of the 2001 IEEE Computer Society Conference on Computer Vision and Pattern Recognition. CVPR 2001, Kauai, HI, USA, 2001, vol. 1, p. I- 511- I‑ 518. 

978-1-6654-2867-5/21/$31.00 ©2021 IEEE 

1512 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on January 22,2023 at 17:36:28 UTC from IEEE Xplore.  Restrictions apply. 

