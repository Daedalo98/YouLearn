2020 IEEE Sixth International Conference on Multimedia Big Data (BigMM) 

# Feature Extraction and Feature Selection for Emotion Recognition using Facial Expression 

## Devashi Choudhary, Jainendra Shukla 

HMI Lab, IIIT-Delhi _{_ devashi18003, jainendra _}_ @iiitd.ac.in 

_**Abstract**_ **—Facial expressions play a significant role in describing the emotions of a person. Due to its applicability to a wide range of applications, such as human-computer interaction, driver status monitoring, etc. Facial Expression Recognition (FER) has received substantial attention among the researchers. According to the earlier studies, a small feature set is used for the extraction of facial features for FER system. To date, a systematic comparison of the facial features does not exist. Therefore, in the current research, we identified 18 different facial features (cardinality of 46,352) by reviewing 25 studies and implemented them on the publicly available ExtendedCohn-Kanade (CK+) dataset. After extracting facial features, we performed Feature Selection (FS) using Joint Mutual Information (JMI), Conditional Mutual Information Maximization (CMIM) and MaxRelevance Min-Redundancy (MRMR) and explain the systematic comparison between them, and for classification, we applied various machine learning techniques. The Bag of Visual Words (BoVW) model approach results in significantly higher classification accuracy over the formal approach. Also, we found that the optimal classification accuracy for FER can be obtained by using only 20% of the total identified features. Grey comatrix and haralick features were explored for the first time for the FER and grey comatrix feature outperformed several most commonly used features Local Binary Pattern (LBP) and Active Appearance Model (AAM). Histogram of Gradients (HOG) turns out to be the most significant feature for FER followed Local Directional Positional Pattern (LDSP) and grey comatrix.** 

## I. INTRODUCTION 

Emotions express intention, thought process, physical effort and cognitive processes of a person. Identification of these expressions of a person is Emotion Recognition (ER), and it can be recognized using verbal and non-verbal communications. According to different studies, various characteristics like body action, head movement, hand gestures, heartbeat, speech, and facial expression, shows the emotional state of a person. Facial expressions play a vital role in social communications as it includes the emotion of happiness, fear, sad, surprise, and anger [1]. Due to its vast application not only in perceptual and cognitive science but also in computer animations, affective computing, and psychology, ER using facial expression has become an interesting research topic over the past decades [2]. 

Feature Extraction (FE) and Feature Selection (FS) is an active research topic in the field of computer vision and machine learning. For Facial Expression Recognition (FER), the main stages are FE and FS along with preprocessing of images, to form a feature vector. FE is a process of transforming the input data into a new set of features which 

provide relevant information and, there are various methods for FE from images like Active Appearance Model (AAM), Local Binary Pattern (LBP), Gabor Filters, Scale Invariant Feature Transform (SIFT), etc [3]. FS is the process of automatically or manually selecting features that contribute most to the prediction variable or output and this can be achieved using various FS methods like Joint Mutual Information (JMI), Conditional Mutual Information Maximization (CMIM), and Minimum-Redundancy Maximum-Relevance (MRMR) as they are based on mutual information and form the generic feature set [4]. But, the limitation with the current research is that the model’s performance is evaluated on the small feature set, there is no systematic comparison among methods applied for FE and FS, and due to the distinct dataset, significant features are not known for FER. Hence, the goal of current research is to fill up this gap, by evaluating the performance of a broad set of facial features for FER. 

The rest of the article is distributed in the following manner: In Section 2, we describe feature set and FS algorithms used for FER along with problem statement. In Section 3, we represent the formal approach and the bag-of-visual-words (BoVW) Model Approach used for FER along with employed public dataset. In Section 4, we present results and they are discussed in Section 5. Finally, in Section 6, we summarize the study along with its limitations and suggesting future work as well. 

## II. RELATED WORK 

For FER, higher-level knowledge is required because they express intention, thinking, cognitive processes, physical effort, or other intra- or interpersonal meanings [5]. Facial Expression can be used to assets the person’s experience in context of robot interaction [6], recreational activities [7], healthcare and social media [8]. FER has received substantial attention among the researchers [2]. The continuous model is, how a facial expression can be seen at various intensities while the categorical model consists of _C_ classifiers, each tuned to a special emotion class. Using this model’s emotions are identified [9]. In the virtual reality environment, the FER process consists of three steps: acquisition, feature extraction, and emotion classification and accuracy and performance need to be achieved to give feedback to a user in real-time [10]. Using the shape of facial feature points and the texture information of specific areas, emotions can be identified [11]. Facial features can be extracted by fusing a different version of LBP, 

978-1-7281-9325-0/20/$31.00 ©2020 IEEE 125 DOI 10.1109/BigMM50055.2020.00027 

which outperforms the traditional FER methods [12]. Salient features i.e. the fusion of Histogram of Oriented Gradients (HOG) and LBP aims to provide more reliable results [13]. Gabor filter is a linear filter having frequency and orientation descriptions similar to the human visual system, can be used as a feature factor [14]. Principal Component Analysis (PCA) along with Singular Value Decomposition (SVD) as a feature vector yields better outcomes [15]. The most widely used feature representation technique is the BoVW model and can be used as the identification of facial emotion [16]. Image annotation is attaching keywords to images, BoVW can be applied for it [17]. In the current research, FER consists of 3 stages: FE, FS, and Classification. 

## _A. Facial Features_ 

There are 3 basic facial features eyes, nose, and mouth. Movement of these facial features defines the expression, which identifies the emotion of a person [18]. These features are extracted using computer vision and image processing methods and we called these as ”Handcrafted Features”. 

For the current research, to determine the entire feature set available for FER and also other features which are not explored earlier have proven effective for this purpose, we conduct an online search on IEEE Xplore and ScienceDirect research databases. The keywords used for the search are Facial Expression, Feature Extraction, Feature Selection, Facial Expression, etc. Based on the headings, abstracts, and introduction of earlier research published in conferences and journals, we manually identify the facial features. Finally, we explore 25 articles and implement 18 distinct facial features. 

- 1) LBP [2] [13] [19] [20] 

- 2) Local Directional Rank Histogram Pattern (LDRHP) [12] 

- 3) Local Binary Pattern Histograms (LBPH) [21] [22] 

- 4) Local Directional Position Pattern (LDSP) [12] [23] [12] 

- 5) HOG [2] [24] [25] [26] [13] 

- 6) Gabor Filters [27] [14] 

- 7) Shape Features [11] [28] [29] [30] 

- 8) Texture Features [11] [28] [29] [30] 

- 9) SVD with PCA [15] [31] 

- 10) Sobel Operator [32] [33] 

- 11) Laplacian Filter [34] 

- 12) Kirsch Operator [35] 

- 13) Canny Edge Detector [36] [37] 

- 14) Gray-Level Co-Occurrence Matrix (GLCM) [38] [39] 

- 15) Hue Moments [40] 

- 16) Color Hist [41] 

- 17) Haralick [42] 

- 18) SIFT [43] [44] 

The whole feature set along with the feature’s description is shown in Table 1. 

(ICA) or linear discriminant analysis (LDA). These methods are not useful for the recognition problem as they are not related to automated pattern recognition [45]. There are two categories for FS methods one is classifier independent i.e. ’filter’ methods and another is classifier dependent ‘wrapper’ and ‘embedded’ methods. [4]. Since classifier dependent yield feature set specific to the class and computationally expensive, while filter methods are class-independent so, they have the potential to yield generic feature subset. [4]. 

FS is the process of automatically or manually selecting features that contribute most to the prediction variable or output. Having irrelevant features in data can reduce the accuracy of the models and make models learn based on these features. If the processing of data needs to be done in real-time then extracting information from high dimensional data is a challenging task because the processing of high dimensional data requires significant computations and space complexity [46]. FS algorithm can be used as an optimization of the conditional likelihood it is based on mutual information (measure of feature relevancy) [4]. 

FS algorithms, JMI, CMIM, and MRMR, provides desirable properties of an information-based selection model [4], and, therefore, we employed these in our research. 

JMI distinguishes among features and eliminates the feature redundancy even after all features have the same mutual information (MI). CMIM provides the class information that is not captured by the features in the selected feature set and gives preference to informational and uncorrelated features. MRMR selects the features which are mutually far away from each other while, still having a ”high” correlation to the variable. 

## _C. Problem Statement_ 

It is not known which features are beneficial for FER and as can be observed from the related work, there is a limited contribution to the comparison of different facial features. Hence, the goal of the current research are as follows: 

- 1) To review facial features for FER. 

- 2) To compare different facial features on the CK+ dataset using three FS methods. 

- 3) To identify significant facial features for FER. 

- 4) To compare the formal approach and the BoVW model approach. 

## III. METHODOLOGY 

To achieve the required goal, we have reported a feature set as shown in Table 1. We then extracted that features on publicly available annotated dataset, the Extended-CohnKanade (CK+) dataset [47], and determine the most notable feature and showed a comparison among the formal approach and the BoVW model. 

## _B. Feature Selection_ 

According to the earlier study for FS algorithms, most of the facial features are not explored or have used feature reduction techniques like PCA, Independent Component Analysis 

126 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 

|**S.No.**|**Features**|**Sub-Features**|**Description**|
|---|---|---|---|
|1|Local Binary Pattern|LBP|It is local descriptor for representation of texture. This is constructed by<br>comparing each pixel with its surrounding neighborhood of pixels.|
|||Local Directional Rank Histogram<br>Pattern (LDRHP )|For each pixel in a depth image, eight local directional strengths are obtained<br>and ranked. Once the rank of all pixels is obtained, eight histograms are<br>developed for the eight surrounding directions. The histograms are then<br>concatenated to represent features for a depth image of a face.|
|||Local Binary Patterns Histograms<br>(LBPH )|First LBP is computed then histogram is created|
|||Local Directional Position Pattern<br>(LDSP)|It considers the binary values of the position with the directions representing<br>the highest and lowest original strengths. The highest strength indicates the<br>strongest direction on the bright side of a pixel and the lowest one indicates<br>the strongest direction in the dark side of that pixel. Besides, the LDSP pattern<br>of a pixel is of six bits.|
|2|Histogram<br>of<br>Oriented<br>Gradients|HOG|It is global descriptor and it provides information about gradient and magnitude<br>of image. On the basis of that feature vector is formed.|
|3|Filter|Gabor Filter|It is a linear flter used for texture analysis, which means that it analyses whether<br>there are any specifc frequency content in the image in specifc directions in<br>a localized region around the point or region of analysis.|
|||Log Gabor Filter|Extension of Gabor flter by taking log.|
|4|Salient Features|LBP+HOG|Combination of HOG and LBP.|
|5|Shape and Texture Fea-<br>tures|Shape Features|Detects the geometry of face i.e. we use a set of points to annotate face<br>shape(like eyes, nose, etc), so face shape can be represented by the coordinates<br>of these landmarks.|
|||Texture Feature|Texture extraction after the geometry of facial features like eyes, nose, and<br>mouth is detected and a feature vector is formed.|
|6|SVD|Singular Value Decomposition And<br>PCA|It is a robust method for storing large images as smaller, more manageable<br>square ones. This is accomplished by reproducing the original image with each<br>succeeding nonzero singular values.|
|7|Edge Detection|Sobel Filter in X and Y direction|It is a flter that convolves with images horizontally and vertically. It provides<br>information about the edges in an image which can be used as a feature vector.|
|||Laplacian Filter|Laplacian flters are derivative flters used to fnd areas of rapid change (edges)<br>in images. Since derivative flters are very sensitive to noise, it is common to<br>smooth the image (e.g., using a Gaussian flter) before applying the Laplacian|
|||Kirsch Operator|The Kirsch operator or Kirsch compass kernel is a nonlinear edge detector that<br>fnds the maximum edge strength in a few predetermined directions.|
|||Canny Edge Detector|Canny edge detection is a technique to extract useful structural information<br>from different vision objects and dramatically reduce the amount of data to be<br>processed. Detection of edge with low error rate, which means that the detection<br>should accurately catch as many edges shown in the image as possible .|
|8|GLCM|Grey Comatrix|It provides a spatial/ texture relationship between the pixel intensities that is<br>the texture of the image is within a specifc range between the pair of pixels.<br>It returns a matrix which is a grey-level cooccurrence matrix. After the GLCM<br>matrix is created we get texture information of images using graycoprops. The<br>information about contrast, correlation, dissimilarity, energy, etc for a given<br>image is obtained.|
|9|Hue Moments|Hue Moments|It uses the moments as a feature to quantify the shape of the image. The extract<br>hu moments, the moments of the image are computed and the vector is created.<br>The image is converted to the grayscale image as moments.|
|10|Color Hist|Color Hist|It is used to extract Color Histogram features from the image. For a given<br>image, for each channel histogram(bins) is created and it’s value range from<br>0-255). Then the histogram is normalized and a vector is formed.|
|11|Haralick|Haralick|It is global feature extractor(the feature vector which quantifes entire image).<br>It provide information about texture to quantify the image.|
|12|SIFT|Scale Invariant Feature Transforms|It is operator which fnds key points(corners) in images( whether images are<br>scaled or rotated) and form feature descriptor using key points.|



TABLE I 

FEATURES AND ITS DESCRIPTION 

127 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 

## _A. CK+ Dataset_ 

- CK+ is a publicly available dataset and is used for given 

- studies [47]. The details are as follows : 

- 1) Image Data: The dataset contains 593 series from 123 subjects. The image sequence varies from10 to 60 frames and it includes the onset (neutral frame) to peak formation (discrete emotion) of the facial expressions. 

- 2) Emotion Labels: All image data from the 593 series from 123 subjects and the emotion label based on the subject’s pattern of each of the 8 basic emotion categories: anger, contempt, disgust, fear, happy, neutral, sadness and surprise. 

- 3) Action Unit Labels: The facial action unit system (FACS) coding of peak frames is provided. There are 43 action units in total and combination if this action units form discrete basic emotions. 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0004-05.png)


Fig. 1. Images from CK+ database 

## _B. Formal Approach_ 

The suggested approach is trained and tested on the CK+ dataset [47]. For our experiments, we chose the last 6 image sequences from each participant for each category for FER. To make the dataset balanced, we considered 108 images from each category. 

To overcome the computational complexity, the image is resized to 64x64. The formal approach is basically, identifying the facial region from images, extracting handcrafted features followed by classification. Figure 2 shows the block diagram of the proposed approach. 

_1) Face Detection:_ ‘Face Detection’ cares about where the face is positioned in an image. It is a method by which we can extract face regions from a human body. Before face detection image is pre-processed using Gaussian filters to remove noise, decrease processing time, and increase the chances of getting correct matches. Detecting a face is very common and various methods are used for it [48] [49] [50] [51]. Among several methods applied, Adaboost and Recurrent Convolutional Neural Network (RCNN) outperforms. As the time required for face detection using Adaboost is very less as compared to RCNN but due to its high false-positive rate, RCNN is used for face detection. 

_2) Feature Extraction:_ In this section, we review the wide variety of features that are important to the FER system. We distinguish different sets of features and how they are extracted. We collected the feature list described in Table 1 for the FER system based on the study of 25 articles. 

- 1) Regarding LBP feature, Previous research shows, it is an efficient feature descriptor [2] [13] [19] [20] and generally used for extracting the texture of the image [2]. Several sub-features for of LBP have been used for FER such as LBPH [21] [22], LDSP [12] [23] [12], and LDRHP [12]. 

- 2) HOG is a global feature descriptor and it is invariant to geometric transformations [2], as it computes the occurrences of gradient orientation and magnitude. The image is divided into several blocks and, then histograms of each block is concatenated to form shape descriptors [24] [25] [26]. For facial expressions, we have different orientations of eyes, nose, and mouth [13], so HOG is a powerful feature descriptor in our algorithm. 

- 3) Gabor filter has representation similar to the human visual system [27]. The log gabor filter is an extension of the gabor filter as it allows more knowledge to be captured in the high-frequency ranges [14]. The image is convolved with a to form a feature vector. 

- 4) Shape features are edges to eyes, nose, lips, etc while texture features information of texture related to edges of shape features [11] [28]. The feature vector is formed in the same manner as described in [29] [30]. 

- 5) SVD along with PCA is a method for storing larger size images into smaller [15], it also reduces the computational complexity and the SV part of SVD is considered as a feature vector [31]. 

- 6) Edges in the image give important information. There exist various methods for identifying edges in images like sobel operator [32] [33], laplacian filters [34], kirsch operator [35] and canny edge detector [36] [37] . Detection of edge using canny edge detector yields a low error rate, which means many edges are captured in the image [33]. 

- 7) Grey comatrix gives knowledge about the texture of an image [38]. It returns feature vector consists of contrast, energy, correlation, etc for a given image [39]. Best to our knowledge, it is not explored before and used for the time for FER. 

- 8) Hue Moments uses the moments as a feature to quantify the shape of the image [40]. 

- 9) Color hist uses the pixel intensity overall three-channel red, blue, and green and model histogram of each channel [41]. 

- 10) Haralick features measure the pixel texture pattern within the local area. It encodes the variations in pixel intensities and the uniformity of the image [42]. 

- 11) SIFT is generally used for getting key points in images [43]. Key points give relevant information about the orientation of an image [44]. In the current research, we have extracted 128 key points from the image to create a feature vector. 

Finally, we create a feature vector using the fusion of aboveextracted features. 

_3) Feature Selection:_ As explained in section 2.2, among the various FS methods we applied JMI, CMIM, and MRMR 

128 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0005-00.png)


**----- Start of picture text -----**<br>
Feature Extraction<br>Histogram of<br>Input Data Gradients(HOG)<br>Local Binary MLP Classification<br>Pattern(LBP)� Feature Selection<br>Pre-processing for Edge Detection Learning with<br>each image Joint Mutual# = 5 to 200 Training Data activation relu &<br>Singular Value Information learning rate Yes<br>Decomposition(SVD) alpha Accuracy<br>Face Detection Shape &TextureGabor and Log-Gabor Filters MaximizationConditional�Information#=5 to 25 % of totalMutualfeatures Data No Optimal AccuracyOptimal Yes FrequencyFeature's+<br>Features parameter<br>Haralick Features Minimum Validation Data No<br>Redundancy Validation<br>Grey Comatrix Maximum<br>Hue Moments Relevance Testing Data<br>Colour Hist<br>Scale Invariant<br>Feature Transforms<br>Classification<br>**----- End of picture text -----**<br>


Fig. 2. Block diagram of supervised classification system using Formal Approach 

for identifying important facial features because they provide useful properties of a knowledge-based selection model. We employed more than one FS method because the results achieved from multiple methods are more robust [52]. The classifier performance is evaluated by identifying top _n_ features provided by the FS algorithm. To select the optimal value of _n_ , we varied _n_ from 5 to 25% of total features(total number of features are 46,352). 

_4) Classification:_ Since our goal is to analyze the emotion of a person using handcrafted features, we use the annotated emotions of the CK+ dataset [47]. We have considered 8 basic emotions anger, contempt, disgust, fear, happy, neutral, sadness, and surprise. We have labeled the emotions as anger is in category 0, contempt is in category 1 and so on. Since the dataset contains a sequence of frames, for each category we have considered 108 samples to make the balanced distribution of the dataset. 

After FE and FS, a feature vector is formed which is divided into the ratio of 75: 15: 10 as training, validation, and testing set respectively. We estimated each of the FS methods individually listed in section 2.3 and achieved classification accuracy using various machine learning classifiers like Random Forest, XG Boost and Multi-Layer Perceptron [53]. We implemented Multi-Layer Perceptron (MLP) since it provides the best classification accuracy among all classifiers during the FER process. We used random search and 5-fold crossvalidation method for parameter tuning of MLP Classifier. 

## _C. BoVW Model Approach_ 

It is an extension of a bag of words model algorithm which is used for text classification and it is widely used for image classification and object categorization [54]. BoVW can also be used for the classification of low-resolution images [55]. The key idea of this method is to describe image into local patches i.e. ”interesting region” [56]. The proposed methodology of FER system is illustrated in figure 3. In the proposed 

approach, after face detection as described in section 3.2.1, we divide the image into two patches, one patch describing the behavior of eyes and another patch gives information related to nose and movement of lips. The feature extraction and feature selection are done on these local patches the same as described in sections 3.2.2 and 3.2.3. 

Each extracted features from local patches are put into a bag, we call it a “bag of visual words”. Each of the extracted features is quantized into one of the visual words, and each image is represented by a histogram of this visual word [57]. A clustering algorithm is used for this purpose, generally, the K-means algorithm is used. Clustering is a grouping of similar objects into one group. 

Now, images are presented only by the frequency of visual words, which avoids complex calculations during matching of image local features. The succeeding step is to achieve visual words to build a visual vocabulary from data and to represent images into vectors, which are then used to extract the properties of each category [58]. Now the classification needs to be done in the same manner as described in section 3.2.4. 

## IV. RESULTS 

We aim to provide insights on the following questions: 

- 1) Performance of different FS algorithms and what is an optimal number of features? 

- 2) Which features are most significantly used for FER? 

- 3) Comparison of performance of the applied approaches for achieving the highest classification accuracy? 

## _A. Optimal Number of Features_ 

Figure 4, 5, 6 shows the accuracies for FER, using the three FS methods JMI, CMIM, and MRMR. We have taken 5 to 25% of total features and achieved accuracy using MLP classifier with fine parameter tuning. The optimal accuracy is the highest accuracy achieved at an average of 20 % of the total number 

129 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0006-00.png)


**----- Start of picture text -----**<br>
Feature Extraction<br>Input Data<br>Histogram of<br>Gradients(HOG)<br>Pre-processing foreach image Pattern(LBP)�Local Binary Feature Selection MLP Classification<br>Face Detection Decomposition(SVD)Edge DetectionSingular Value Joint MutualInformation# = 5 to 200 Training Data activation relu &Learning withlearning rate Yes<br>Patches Gabor and Log-Gabor Filters Conditional�Information#=5 to 25 % of totalMutualfeatures Bag ofVisual Data alphaNo AccuracyOptimal Yes Feature'sAccuracy+<br>Shape &Texture Maximization Words Optimal Frequency<br>Features parameter<br>Clustering<br>Haralick Features RedundancyMinimum Reduce Validation No<br>Grey Comatrix Maximum the size Validation Data<br>Hue Moments Relevance of Bag<br>Colour Hist Testing Data<br>Scale Invariant<br>Feature Transforms<br>Classification<br>**----- End of picture text -----**<br>


Fig. 3. Block diagram of supervised classification system using BoVW Model 

of features. To determine the significant difference (i.e. best algorithm) between applied FS algorithms [46], the average values of accuracy and the optimal number of features were compared, but, there is no evidence that one of the algorithms outperforms the others. 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0006-03.png)


**----- Start of picture text -----**<br>
88 Formal Approach<br>BoVW Model<br>86<br>84<br>82<br>80<br>78<br>76<br>74<br>0 5 10 15 20 25 30<br>% of total features<br>Accuracy<br>**----- End of picture text -----**<br>


Fig. 4. Classification Accuracy using JMI 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0006-05.png)


**----- Start of picture text -----**<br>
86 Formal Approach<br>BoVW Model<br>84<br>82<br>80<br>78<br>76<br>74<br>72<br>0 5 10 15 20 25 30<br>% of total features<br>Accuracy<br>**----- End of picture text -----**<br>


Fig. 5. Classification Accuracy using CMIM 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0006-07.png)


**----- Start of picture text -----**<br>
86 Formal Approach<br>BoVW Model<br>84<br>82<br>80<br>78<br>76<br>74<br>72<br>0 5 10 15 20 25 30<br>% of total features<br>Accuracy<br>**----- End of picture text -----**<br>


Fig. 6. Classification Accuracy using MRMR 

## _B. Significant Features_ 

To know the most commonly used features by the different FS methods, we followed an approach similar to the one described in [59] [46]. It computes the relative frequency of each of the features, which is achieved via the following process: 

- 1) Given selected features, for an optimal number of features across all FS methods, we first build a histogram of feature occurrence. 

- 2) Now, normalization of each histogram bin is done by dividing the occurrence of each feature by feature’s cardinality. 

- 3) Finally, we obtained a weighted relative frequency (shown in figure 4) and average weighted relative frequency (shown in figure 5) of each feature across each FS method, by multiplying achieved classification accuracy. 

The relative frequency is varied from 0 to 1. Significant features scores are higher than non-significant features. From figure 7 and figure 8, it can be concluded that HOG is the most significant feature. LDSP is the second most significant feature 

130 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 

among all. The grey co-matrix is explored for the first time in the current research and it is the best performing feature along with HOG and LDSP. 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0007-01.png)


**----- Start of picture text -----**<br>
0.7 JMI<br>0.6 CMIM<br>0.5 MRMR<br>0.4<br>0.3<br>0.2<br>0.1<br>0<br>Features<br>Weighted Relative Frequency<br>**----- End of picture text -----**<br>


Fig. 7. Comparison of Weighted relative frequency for FER using FS methods 


![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0007-03.png)



![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0007-04.png)



![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0007-05.png)



![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0007-06.png)


**----- Start of picture text -----**<br>
0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>Weighted Relative Occurrence 0<br>**----- End of picture text -----**<br>



![](saved_pdfs/unchecked/RCCCPVCP/images/RCCCPVCP.pdf-0007-07.png)


**----- Start of picture text -----**<br>
Features<br>**----- End of picture text -----**<br>


Fig. 8. Weighted relative frequency of each facial feature type for FER 

## _C. Comparison between Applied Approaches_ 

For the current studies, we proposed two approaches formal approach as shown in Figure 2 and the BoVW Model approach as shown in figure 3. According to the results, BoVW approach gives significant results as compared to the formal approach in terms of accuracy for all FS methods applied, as shown in figure 4,5,6. As in BoVW representation, we divide the image into two patches and then features are extracted from these local patches to form the visual vocabulary which tends to improve both the classification accuracy and computational efficiency, while in the formal approach we are considering the entire image as a local patch. 

## V. DISCUSSION 

We observe there is no notable difference in the performance of the three FS methods, all of them produced a high average classification accuracy. The results achieved indicate that on an average 20% of total identified features are required to yield the highest accuracy. This is a notable finding and has not been listed by an earlier study. The optimal number of features 

achieved in the current research implies that the computational complexity is reduced by using various FS methods. 

Regarding the significance of specific features, among all features, HOG is the most significant one for FER. We also showed that the commonly used features like SIFT, canny, SVD does not perform well in this regard. Whereas the grey co-matrix feature has not been explored previously, and as a unique feature it generates a high performance for FER. Furthermore, also the most significant feature related to various versions of LBP that is LDSP, which outperformed all other feature. One of the biggest difficulties for current research is real-time FER and it goes beyond the scope of this study. 

## VI. CONCLUSION 

In the current research, we reviewed 25 articles and implemented 18 different facial features for FER. We examined the significance of different facial features using three FS methods and applying machine learning methods on the publicly available CK+ dataset. We noted that all FS methods showed the use of approximately 20% of identified total features as an optimal number of features for FER. The results reported accuracy of 84.53% using a formal approach and accuracy of 85.9% using the BOVW Model approach at 20% of total identified features. Grey Co-matrix feature along with the LDSP feature outperformed the generally used HOG feature. Our research represents a significant set of features and also gives a new feature set that has been not used in earlier research, such as the grey co-matrix feature. 

One limitation of the current study is that we only focused on the classification of basic emotions like happy, sad, fear, etc. We can use a dimensional model of emotion such as using valence and arousal for emotion recognition [60]. Another limitation is that we used only one dataset i.e. CK+. It is possible to use join multiple datasets so that a general model for FER could be trained. 

## VII. ACKNOWLEDGEMENT 

This research is partly supported through Infosys Centre of Artificial Intelligence and TCS – Centre for Design and New Media. 

## REFERENCES 

- [1] I. M. Revina and W. S. Emmanuel, “A survey on human face expression recognition techniques,” _Journal of King Saud University-Computer and Information Sciences_ , 2018. 

- [2] B. Ko, “A brief review of facial emotion recognition based on visual information,” _sensors_ , vol. 18, no. 2, p. 401, 2018. 

- [3] L. Wang, R.-F. Li, K. Wang, and J. Chen, “Feature representation for facial expression recognition based on facs and lbp,” _International Journal of Automation and Computing_ , vol. 11, no. 5, pp. 459–468, 2014. 

- [4] G. Brown, A. Pocock, M.-J. Zhao, and M. Luj´an, “Conditional likelihood maximisation: a unifying framework for information theoretic feature selection,” _Journal of machine learning research_ , vol. 13, no. Jan, pp. 27–66, 2012. 

- [5] Y. Tian, T. Kanade, and J. F. Cohn, “Facial expression recognition,” in _Handbook of face recognition_ , pp. 487–519, Springer, 2011. 

- [6] M. Swangnetr and D. B. Kaber, “Emotional state classification in patient–robot interaction using wavelet analysis and statistics-based feature selection,” _IEEE Transactions on Human-Machine Systems_ , vol. 43, no. 1, pp. 63–75, 2012. 

131 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 

- [7] A. Drachen, L. E. Nacke, G. Yannakakis, and A. L. Pedersen, “Correlation between heart rate, electrodermal activity and player experience in first-person shooter games,” in _Proceedings of the 5th ACM SIGGRAPH Symposium on Video Games_ , pp. 49–54, ACM, 2010. 

- [8] A. Kirte, A. Mandal, O. Birajdar, and M. V. Kulloli, “A review paper on facial expression recognition,” 

- [9] A. Martinez and S. Du, “A model of the perception of facial expressions of emotion by humans: Research overview and perspectives,” _Journal of Machine Learning Research_ , vol. 13, no. May, pp. 1589–1608, 2012. 

- [10] D. Yang, A. Alsadoon, P. Prasad, A. Singh, and A. Elchouemi, “An emotion recognition model based on facial recognition in virtual learning environment,” _Procedia Computer Science_ , vol. 125, pp. 2–10, 2018. 

- [11] W. Zheng and C. Liu, “Facial expression recognition based on texture and shape,” in _2016 25th Wireless and Optical Communication Conference (WOCC)_ , pp. 1–5, IEEE, 2016. 

- [12] M. Z. Uddin, W. Khaksar, and J. Torresen, “Facial expression recognition using salient features and convolutional neural network,” _IEEE Access_ , vol. 5, pp. 26146–26161, 2017. 

- [13] Y. Liu, Y. Li, X. Ma, and R. Song, “Facial expression recognition with fusion features extracted from salient facial areas,” _Sensors_ , vol. 17, no. 4, p. 712, 2017. 

- [14] K. R. Kulkarni and S. B. Bagal, “Facial expression recognition,” in _2015 Annual IEEE India Conference (INDICON)_ , pp. 1–5, IEEE, 2015. 

- [15] M. Kaur, R. Vashisht, and N. Neeru, “Recognition of facial expressions with principal component analysis and singular value decomposition,” _International Journal of Computer Applications_ , vol. 9, no. 12, pp. 36– 40, 2010. 

- [16] M. S. Ratliff and E. Patterson, “Emotion recognition using facial expressions with active appearance models,” in _Proc. of HRI_ , Citeseer, 2008. 

- [17] C.-F. Tsai, “Bag-of-words representation in image annotation: A review,” _ISRN Artificial Intelligence_ , vol. 2012, 2012. 

- [18] N. D. Haig, “Exploring recognition with interchanged facial features,” _Perception_ , vol. 15, no. 3, pp. 235–247, 1986. 

- [19] B. Tejinkar and S. Patil, “Local binary pattern based facial expression recognition using support vector machine,” _the International Journal of Engineering and Science_ , vol. 7, no. 8, pp. 43–49, 2018. 

- [20] C. Shan, S. Gong, and P. W. McOwan, “Robust facial expression recognition using local binary patterns,” in _IEEE International Conference on Image Processing 2005_ , vol. 2, pp. II–370, IEEE, 2005. 

- [21] C. Xu, Y. Zheng, and Z. Wang, “Eye states detection by boosting local binary pattern histogram features,” in _2008 15th IEEE International Conference on Image Processing_ , pp. 1480–1483, IEEE, 2008. 

- [22] X. Zhang, M. H. Mahoor, and S. M. Mavadati, “Facial expression recognition using l-norm mkl multiclass-svm,” _Machine Vision and Applications_ , vol. 26, no. 4, pp. 467–483, 2015. 

- [23] T. Jabid, M. H. Kabir, and O. Chae, “Local directional pattern (ldp)–a robust image descriptor for object recognition,” in _2010 7th IEEE International Conference on Advanced Video and Signal Based Surveillance_ , pp. 482–487, IEEE, 2010. 

- [24] M. Dahmane and J. Meunier, “Emotion recognition using dynamic gridbased hog features,” in _Face and Gesture 2011_ , pp. 884–888, IEEE, 2011. 

- [25] O. D´eniz, G. Bueno, J. Salido, and F. De la Torre, “Face recognition using histograms of oriented gradients,” _Pattern Recognition Letters_ , vol. 32, no. 12, pp. 1598–1603, 2011. 

- [26] P. Lemaire, M. Ardabilian, L. Chen, and M. Daoudi, “Fully automatic 3d facial expression recognition using differential mean curvature maps and histograms of oriented gradients,” in _2013 10th IEEE International Conference and Workshops on Automatic Face and Gesture Recognition (FG)_ , pp. 1–7, IEEE, 2013. 

- [27] N. Rose, “Facial expression classification using gabor and log-gabor filters,” in _7th International Conference on Automatic Face and Gesture Recognition (FGR06)_ , pp. 346–350, IEEE, 2006. 

- [28] F. Tang and B. Deng, “Facial expression recognition using aam and local facial features,” in _Third International Conference on Natural Computation (ICNC 2007)_ , vol. 2, pp. 632–635, IEEE, 2007. 

- [29] I. Kotsia, S. Zafeiriou, and I. Pitas, “Texture and shape information fusion for facial expression and facial action unit recognition,” _Pattern Recognition_ , vol. 41, no. 3, pp. 833–851, 2008. 

- [30] X. Xie and K.-M. Lam, “Facial expression recognition based on shape and texture,” _Pattern Recognition_ , vol. 42, no. 5, pp. 1003–1011, 2009. 

- [31] A. P. Gosavi and S. Khot, “Facial expression recognition using principal component analysis with singular value decomposition,” _International_ 

_Journal of Advance Research in Computer Science and Management Studies_ , vol. 1, no. 6, 2013. 

- [32] W. Gao, X. Zhang, L. Yang, and H. Liu, “An improved sobel edge detection,” in _2010 3rd International Conference on Computer Science and Information Technology_ , vol. 5, pp. 67–71, IEEE, 2010. 

- [33] E. Nadernejad, S. Sharifzadeh, and H. Hassanpour, “Edge detection techniques: Evaluations and comparisons,” _Applied Mathematical Sciences_ , vol. 2, no. 31, pp. 1507–1520, 2008. 

- [34] S.-C. Tai and S.-M. Yang, “A fast method for image noise estimation using laplacian operator and adaptive edge detection,” in _2008 3rd International Symposium on Communications, Control and Signal Processing_ , pp. 1077–1081, IEEE, 2008. 

- [35] H. Kekre and S. Gharge, “Image segmentation using extended edge operator for mammographic images,” _International journal on computer science and Engineering_ , vol. 2, no. 4, pp. 1086–1091, 2010. 

- [36] X. Chen and W. Cheng, “Facial expression recognition based on edge detection,” _International Journal of Computer Science and Engineering Survey_ , vol. 6, no. 2, p. 1, 2015. 

- [37] P. Zhao-Yi, Z. Yan-Hui, and Z. Yu, “Real-time facial expression recognition based on adaptive canny operator edge detection,” in _2010 Second International Conference on MultiMedia and Information Technology_ , vol. 2, pp. 154–157, IEEE, 2010. 

- [38] C. Madhura and D. Dheeraj, “Feature extraction for image retrieval using color spaces and glcm,” _International Journal of Innovative Technology and Exploring Engineering (IJITEE)_ , vol. 3, no. 2, pp. 159–162, 2013. 

- [39] P. Mohanaiah, P. Sathyanarayana, and L. GuruKumar, “Image texture feature extraction using glcm approach,” _International journal of scientific and research publications_ , vol. 3, no. 5, p. 1, 2013. 

- [40] P.-T. Yap, R. Paramesran, and S.-H. Ong, “Image analysis by krawtchouk moments,” _IEEE Transactions on image processing_ , vol. 12, no. 11, pp. 1367–1377, 2003. 

- [41] J. Van De Weijer and C. Schmid, “Coloring local feature extraction,” in _European conference on computer vision_ , pp. 334–348, Springer, 2006. 

- [42] A. Agarwal, R. Singh, and M. Vatsa, “Face anti-spoofing using haralick features,” in _2016 IEEE 8th International Conference on Biometrics Theory, Applications and Systems (BTAS)_ , pp. 1–6, IEEE, 2016. 

- [43] A. Albiol, D. Monzo, A. Martin, J. Sastre, and A. Albiol, “Face recognition using hog–ebgm,” _Pattern Recognition Letters_ , vol. 29, no. 10, pp. 1537–1543, 2008. 

- [44] S. Berretti, A. Del Bimbo, P. Pala, B. B. Amor, and M. Daoudi, “A set of selected sift features for 3d facial expression recognition,” in _2010 20th International Conference on Pattern Recognition_ , pp. 4125–4128, IEEE, 2010. 

- [45] S. Prasad and L. M. Bruce, “Limitations of principal components analysis for hyperspectral target recognition,” _IEEE Geoscience and Remote Sensing Letters_ , vol. 5, no. 4, pp. 625–629, 2008. 

- [46] J. Shukla, M. Barreda-Angeles, J. Oliver, G. Nandi, and D. Puig, “Feature extraction and selection for emotion recognition from electrodermal activity,” _IEEE Transactions on Affective Computing_ , 2019. 

- [47] P. Lucey, J. F. Cohn, T. Kanade, J. Saragih, Z. Ambadar, and I. Matthews, “The extended cohn-kanade dataset (ck+): A complete dataset for action unit and emotion-specified expression,” in _2010 IEEE Computer Society Conference on Computer Vision and Pattern Recognition-Workshops_ , pp. 94–101, IEEE, 2010. 

- [48] S. Kolkur, D. Kalbande, P. Shimpi, C. Bapat, and J. Jatakia, “Human skin detection using rgb, hsv and ycbcr color models,” _arXiv preprint arXiv:1708.02694_ , 2017. 

- [49] P. Viola, M. Jones, _et al._ , “Rapid object detection using a boosted cascade of simple features,” _CVPR (1)_ , vol. 1, no. 511-518, p. 3, 2001. 

- [50] S. Thakur, S. Paul, A. Mondal, S. Das, and A. Abraham, “Face detection using skin tone segmentation,” in _2011 World Congress on Information and Communication Technologies_ , pp. 53–60, IEEE, 2011. 

- [51] X. Sun, P. Wu, and S. C. Hoi, “Face detection using deep learning: An improved faster rcnn approach,” _Neurocomputing_ , vol. 299, pp. 42–50, 2018. 

- [52] C. Lazar, J. Taminau, S. Meganck, D. Steenhoff, A. Coletta, C. Molter, V. de Schaetzen, R. Duque, H. Bersini, and A. Nowe, “A survey on filter techniques for feature selection in gene expression microarray analysis,” _IEEE/ACM Transactions on Computational Biology and Bioinformatics (TCBB)_ , vol. 9, no. 4, pp. 1106–1119, 2012. 

- [53] Z. G. C¸ am, S. C¸ imen, and T. Yıldırım, “Learning parameter optimization of multi-layer perceptron using artificial bee colony, genetic algorithm and particle swarm optimization,” in _2015 IEEE 13th International_ 

132 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 

_Symposium on Applied Machine Intelligence and Informatics (SAMI)_ , pp. 329–332, IEEE, 2015. 

- [54] X.-C. Li, C.-h. Zhao, and Y. Cang, “Face recognition using the improved bag of words model,” in _2013 Third International Conference on Instrumentation, Measurement, Computer, Communication and Control_ , pp. 772–775, IEEE, 2013. 

- [55] R. T. Ionescu, M. Popescu, and C. Grozea, “Local learning to improve bag of visual words model for facial expression recognition,” in _Workshop on challenges in representation learning, ICML_ , 2013. 

- [56] J. Hao and X. Jie, “Improved bags-of-words algorithm for scene recognition,” in _2010 2nd International Conference on Signal Processing Systems_ , vol. 2, pp. V2–279, IEEE, 2010. 

- [57] Y. Zhang, R. Jin, and Z.-H. Zhou, “Understanding bag-of-words model: a statistical framework,” _International Journal of Machine Learning and Cybernetics_ , vol. 1, no. 1-4, pp. 43–52, 2010. 

- [58] X.-w. Lou, D.-c. Huang, L.-m. Fan, and A.-j. Xu, “An image classification algorithm based on bag of visual words and multi-kernel learning,” _Journal of Multimedia_ , vol. 9, no. 2, p. 269, 2014. 

- [59] R. Jenke, A. Peer, and M. Buss, “Feature extraction and selection for emotion recognition from eeg,” _IEEE Transactions on Affective Computing_ , vol. 5, no. 3, pp. 327–339, 2014. 

- [60] J. Posner, J. A. Russell, and B. S. Peterson, “The circumplex model of affect: An integrative approach to affective neuroscience, cognitive development, and psychopathology,” _Development and psychopathology_ , vol. 17, no. 3, pp. 715–734, 2005. 

133 

Authorized licensed use limited to: Universita degli Studi di Bologna. Downloaded on August 21,2023 at 15:35:18 UTC from IEEE Xplore.  Restrictions apply. 

