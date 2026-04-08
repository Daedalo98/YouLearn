_**applied sciences**_ 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0001-01.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0001-02.png)


## _Article_ 

## **A Feature-Based Structural Measure: An Image Similarity Measure for Face Recognition** 

**Noor Abdalrazak Shnain[1] , Zahir M. Hussain[2,3,] * ID and Song Feng Lu[1] ID** 

- 1 School of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan 430074, China; nooraljanabi@hust.edu.cn (N.A.S.); lusongfeng@hust.edu.cn (S.F.L.) 

- 2 Faculty of Computer Science & Mathematics, University of Kufa, Najaf 54001, Iraq 

- 3 School of Engineering, Edith Cowan University, Perth, WA 6027, Australia 

- Correspondence: zmhussain@ieee.org or zahir.hussain@uokufa.edu.iq or z.hussain@ecu.edu.au; Tel.: +964-781-232-2479 

- Received: 4 July 2017; Accepted: 31 July 2017; Published: 3 August 2017 

**Featured Application: This work integrates image structural features into a new similarity measure suitable for face recognition with the new merit of recognition confidence.** 

> **Abstract:** Facial recognition is one of the most challenging and interesting problems within the field of computer vision and pattern recognition. During the last few years, it has gained special attention due to its importance in relation to current issues such as security, surveillance systems and forensics analysis. Despite this high level of attention to facial recognition, the success is still limited by certain conditions; there is no method which gives reliable results in all situations. In this paper, we propose an efficient similarity index that resolves the shortcomings of the existing measures of feature and structural similarity. This measure, called the Feature-Based Structural Measure (FSM), combines the best features of the well-known SSIM (structural similarity index measure) and FSIM (feature similarity index measure) approaches, striking a balance between performance for similar and dissimilar images of human faces. In addition to the statistical structural properties provided by SSIM, edge detection is incorporated in FSM as a distinctive structural feature. Its performance is tested for a wide range of PSNR (peak signal-to-noise ratio), using ORL (Olivetti Research Laboratory, now AT&T Laboratory Cambridge) and FEI (Faculty of Industrial Engineering, São Bernardo do Campo, São Paulo, Brazil) databases. The proposed measure is tested under conditions of Gaussian noise; simulation results show that the proposed FSM outperforms the well-known SSIM and FSIM approaches in its efficiency of similarity detection and recognition of human faces. 

**Keywords:** face recognition; structural similarity measure; feature similarity measure; edge detection; Gaussian noise 

## **1. Introduction** 

In view of the current issues of terrorism, security in the western world has been heightened, and is becoming an important and challenging task. Surveillance cameras are now common in airports, hospitals, universities, ATMs, banks and anywhere else with a security system. There is an urgent need to find an accurate and reliable automated system which is able to recognize human faces, in order to identify suspicious persons using cameras [1]. Facial recognition has therefore become the focus of current research, and has received significant attention from academics; many techniques and methods for recognizing human faces have been proposed and applied. However, until now there has been no method which offers the required accuracy in all situations. In other words, existing systems still fall far short of the abilities of a human perception system. This challenge is mainly due to factors that affect the features of an image, such as changes in illumination, background, facial expression 

_Appl. Sci._ **2017** , _7_ , 786; doi:10.3390/app7080786 

www.mdpi.com/journal/applsci 

_Appl. Sci._ **2017** , _7_ , 786 

2 of 17 

and head pose. The task of automatic face recognition is therefore a very complex problem; see [2–4] for surveys. 

In general, there are two classes of face recognition methods: structural and statistical approaches. Structural approaches are based on the extraction of the local features of a face, such as the shapes of the eyes, mouth and nose. These methods suffer from the unpredictability in facial appearance and environmental conditions, e.g., head pose, when a profile image is compared with a frontal image [5]. Conversely, in statistical approaches the complete face region is treated as input data; in other words, global features are extracted from the whole image. The region surrounding the face, including the hair, shoulders and background, is considered to be irrelevant data and may adversely affect the recognition results [6]. Statistical approaches for feature extraction which are based on statistical moment have been used for classification and recognition applications due to their invariance properties [7]. 

In most facial recognition applications, the similarity between two images is calculated, i.e., using a reference image and a training database image. Several matching algorithms for face and object recognition systems have been designed based on image similarity measurements, such as the structural similarity measure (SSIM), which won an Emmy award for its prediction of the perceived quality of digital images and videos [8]. 

The main aim of this work is to design an efficient similarity index to resolve the shortcomings of the existing measures in giving high confidence in recognition. The proposed measure combines the best features of the well-known SSIM and FSIM approaches, striking a balance between performance for similar and dissimilar images of human faces. In addition to the statistical structural properties provided by SSIM, edge detection is incorporated as a distinctive structural feature. In addition to confidence, the proposed measure (FSM) gives a reliable similarity between any two images even under noise, in other words, FSM produces maximal similarity when the images are similar, while giving near-zero similarity when the images are dissimilar. These properties gave the proposed measure high ability to recognize face images under noisy conditions, different facial expressions and pose variations. Such properties are highly needed in security applications while checking the identity of a specific face image in a big database. 

## **2. Background** 

During the last few years, many studies, methods and approaches to similarity and recognition of human faces have been presented to achieve high success rates for accuracy, confidence in identification and authentication in security systems. A significant step in image similarity was presented by Wang and Bovik in 2004 [9], when they proposed the SSIM. This measure is based on the statistical similarity between two images. However, SSIM can give ambiguous results for two different poses, and confusing results in certain cases where it indicates a high similarity for two images which are in fact dissimilar [10]. 

In an attempt to develop the similarity measures and using them for face recognition; Hu et al. proposed a similarity measure based on Hausdorff distance for face recognition. This measure can provide similarity and dissimilarity information of two objects to compare them such as faces with different illumination condition and facial expression. The measure has a better performance than the measures based on conventional Hausdorff distance and the eigenface approaches [11]. 

Xu et al. [12] proposed two new operators for face recognition; to find the pixel intensity variation information of overlapping blocks resulted from the original face image. Two factors let the proposed operators work better than the conventional interest operator: the first one is that by taking the relative as the feature of an image block. The second one is that the scheme to partition an image into overlapping allows the proposed operators to give more representation information for the face image. 

In 2011, an improved version of SSIM was proposed by Zhang et al. [13]. This measure was called feature similarity index for image quality assessment (FSIM) in an effort to emphasize its use in recognition; this method depends on the low-level features of images. In this measure, the dimensionless and gradient magnitude are the main features, which play complementary roles in 

_Appl. Sci._ **2017** , _7_ , 786 

3 of 17 

characterizing the image. However, FSIM also produces confusing results in certain cases; for example, it may detect a similarity between dissimilar images or a non-trivial amount of similarity between two different poses. 

Singh et al. [14] presented a new similarity approach and applied it in face recognition; by combining phase information of wavelet moments and use the real and imaginary components of wavelet moments to describe an image and develop a similarity measure which is invariant under image rotation. 

In 2016 Li et al. presented a novel approach for solving the problem of automatic face recognition when the human faces are taken from frontal views with varying illumination and disguise. The approach is based on extracting dynamic subspace of images and obtaining the discriminative parts in each individual to represent the characteristics of discriminative components and give a recognition protocol to classify face images [15]. 

The topic of 3D face recognition is getting attention. In 2008 a novel deformation invariant image for robust 3D face recognition was proposed by Li et al. [16]. This work is divided into three phases; firstly getting the depth and the intensity of an image from the original 3D facial data. Secondly, geodesic level curves are created by constructing radial geodesic distance image from the depth image. Finally, deformation invariant image is created by evenly sampling points from the selected geodesic level curves in the intensity image. In 2017 Marcolin et al. presented 105 new geometrical descriptors for 3D face analysis. These descriptors created by composing primary geometrical descriptors (for instance mean and Gaussian) and the coefficients of the fundamental forms, and by applying trigonometric functions (for instance sine and cosine) and logarithm to them [17]. Another approach for 3D feature extraction via geometrical analysis is presented in [18]. To the best of our knowledge, 3D face recognition methods haven’t addressed 3D image similarity so far. It is the intention of the Authors to handle this topic soon. 

All of these works didn’t address the confidence in recognition. Only the recognition rate has been used as performance measure. Suppose that two measures ( _M_ 1 and _M_ 2) recognized a face image with 100% similarity. This recognition does not mean that the two measures have the same performance. For example, if _M_ 1 produces significant similarities between the test image and another group of _K_ database images, then the suspected faces would be not only the one with maximal similarity, but 1 + _K_ of possible faces. Now if _M_ 2 produces significant similarity with one correct face while giving trivial similarities with the rest of the database, then _M_ 2 is giving the correct answer with more confidence than _M_ 1 which gave several confusing faces in addition to the best match. The proposed measure outperforms existing measures by far in giving less confusion while recognizing the best match for a given face image. 

The remainder of this paper is arranged as follows: Section 3 describes the design of the proposed FSM approach for use in face recognition. Section 4 presents the experimental results, performance analysis and discussion. Section 5 presents the conclusions. 

## **3. Similarity Measures** 

Similarity is the strength of the relationship between two images, while a similarity measure is defined as the distance (based on a specific norm) between various data points. The performance of any similarity measure is heavily dependent on the choice of an appropriate distance function for a given dataset. In this work, an efficient measure is proposed; put simply, it combines the essential elements of both the feature similarity and structural similarity measures. Its performance is analyzed in comparison with both the SSIM and FSIM approaches; the results of the proposed measure were better in all cases, even under conditions of noise. 

## _3.1. Overview of SSIM: A Structural Similarity Measure_ 

Automatic detection of the similarity between images is a significant issue; it plays an essential role in image processing due to its importance in many image processing applications such as enhancement, 

_Appl. Sci._ **2017** , _7_ , 786 

4 of 17 

compression and identity checks. The most important step in the development of image similarity techniques was taken in 2004 by Wang and Bovik [9] when they designed the structural similarity measure (SSIM), which considered image distortion as a combination of three factors: correlation, luminance and contrast. This measure is used extensively in image quality assessment and in many image processing algorithms. The basis of this measure is a set of statistical measurements such as mean, variance and co-variance, used to develop a definition for a distance function that can calculate the structural similarity between a test image and training images. The SSIM measure is expressed by the following equation: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0004-03.png)


where _ρ_ ( _x_ , _y_ ) represents the similarity between two images _x_ and _y_ ; _x_ is the reference image, while _y_ is usually a corrupted version of _x_ ; and _µx_ , _µy_ , _σx_ and _σy_ are the statistical means and variances of images _x_ and _y_ , respectively. The variable _σxy_ is the statistical co-variance between the pixels in images _x_ and _y_ . The constants _c_ 1 and _c_ 2 are given by _c_ 1 = ( _K_ 1 _L_ )[2] and _c_ 2 = ( _K_ 2 _L_ )[2] , where _K_ 1 and _K_ 2 are small constants and _L_ = 255 (maximum pixel value). Researchers have confirmed that the values of these constants have little effect on the performance of SSIM [19]. 

## _3.2. Overview of FSIM: A Feature Similarity Measure_ 

The feature similarity measure (FSIM) is based on the fact that human visual perception recognizes an image according to its low-level features. FSIM is divided into two parts: the first is the phase congruency (PC), which is a dimensionless measure for the significance of a local structure, while the second is the gradient magnitude (GM). PC and GM play complementary roles in image characterization [13]. The FSIM index between two images _f_ 1 and _f_ 2 is defined as follows: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0004-07.png)


where Ω represents the whole spatial domain for image pixels, _PC_ is the phase congruency and _SL_ is a similarity resulting from combined similarity measure for phase congruency _SPC_ (x) and similarity measure for gradient _SG_ (x) given by the formula: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0004-09.png)


where α and _β_ are parameters used to adjust the relative importance of phase congruency (PC) and gradient magnitude (GM) features, here taken as _α_ = _β_ = 1; and 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0004-11.png)


where _T_ 1 is a positive constant, inserted to increase the stability of _SPC_ (such a consideration was also included in SSIM), and 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0004-13.png)


is the gradient similarity, where _G_ = � _Gx_[2] (x) + _Gy_[2] (x) is the gradient magnitude; _Gx_ and _Gy_ are partial derivatives of image _f_ (x). The phase congruency PC is defined as follows: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0004-15.png)


_Appl. Sci._ **2017** , _7_ , 786 

5 of 17 

where ϵ is a small positive constant, and 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0005-03.png)


where _H_ (x) = ∑ _n on_ (x) and _K_ (x) = ∑ _n en_ (x), _on_ (x) = _ξ_ (x) _∗ Mn[e]_[;] _[ e][n]_[(][x][)][=] _[ξ]_[(][x][)] _[ ∗][M] n[o]_[, noting that] _[M] n[e]_ and _Mn[o]_[are even and odd symmetric filters on scale] _[ n]_[, and ‘*’ denotes convolution.][The function] _[ ξ]_[(][x][)] is a 1D signal obtained after arranging pixels in different orientations. The local amplitudes _An_ (x) are 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0005-05.png)


where x is the position on scale _n_ . 

## _3.3. The Proposed Measure (FSM)_ 

As discussed above, there are certain shortcomings in the performance of the feature similarity and structural similarity measures, particularly since they produce confusing results in some cases. Both FSIM and SSIM may detect a non-trivial amount of similarity when two images are dissimilar and can give low recognition confidence. Both measures fail to detect similarity under conditions of significant noise. 

A new similarity index is proposed here to resolve the shortcomings of SSIM and FSM and to give a more reliable measure of similarity, especially for human face images. This new measure is called the Feature-Based Structural Measure (FSM). On the other front, a new measure for confidence in face recognition is proposed. 

FSM combines the best features of the well-known SSIM and FSIM approaches, striking a balance between their performances for similar and dissimilar images. The inclusion of edge detection in FSM presents a distinctive structural feature, in which two binary edge images, _gx_ and _gy_ , are obtained after edge detection of the original images _x_ and _y_ using Canny’s method [20]. The FSM is given by a rational function, as follows: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0005-11.png)


where, _F_ ( _x_ , _y_ ) represents the proposed similarity between two images _x_ and _y_ ; usually, _x_ represents the reference image and _y_ represents a corrupted version of _x_ ; Φ represents the feature similarity measure (FSIM); and _ρ_ represents the structural similarity measure (SSIM). The constants are chosen as _a_ = 5, _b_ = 3 and _c_ = 7, while _e_ = 0.01 is added to balance the quotient and avoid division by zero. The function _R_ ( _x_ , _y_ ) refers to the global 2D correlation between the images, as follows: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0005-13.png)


where _x_ o and _y_ o are the image global means. This function is applied here as _R_ � _gx_ , _gy_ � on the new images obtained from the application of edge detection to the original images _x_ and _y_ . The simulation results show that the proposed FSM technique gives better performance than SSIM and FSIM for facial recognition, even under conditions of noise. This excellent performance is due to the rational combination of different approaches (hence different features) with proper weights in Equation (9). The proper weights can control the good/bad features provided by the combined measures. 

The only limitation for the proposed measure is the complexity of Equation (9) as compared with the complexity of Equations (1) and (2), where it requires more time. This issue can be alleviated by high-performance computing. However, this is a cheap price for correct recognition, especially in security applications. 

_Appl. Sci._ **2017** , _7_ , 786 

6 of 17 

## _3.4. A Measure for Face Recognition Confidence_ 

The quality of recognition varies from one measure to another; hence, a measure is necessary to evaluate its performance. Here, a measure for the quality of recognition is designed based on the confidence provided by the face recognition method. This confidence indicates the nearness of the similarities to a test image given for the recognized face and the second most likely face from the database. 

The similarity between a test image and a database of _N_ face images will produce _N_ similarity numbers, ranging between 0 and 1. These numbers are method-dependent. A cluster of numbers within a small range indicates a reduced confidence. The most important similarities (that should be well apart) are the maximum similarity number (which gives the best match, or recognition result) and the second maximum number, which is associated with confusion. If normalization is applied then the maximum is always 1, while the difference _m_ with the second maximum would vary according to the degree of confusion. The confidence in face recognition at level _k_ of similarity with a specific test image is defined in this work as follows: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0006-05.png)


where _nk_ is the number of persons with _k_ -level of similarity _sk > k_ . 

## _3.5. Discussion_ 

Image similarity measures (for face recognition) didn’t address the issue of confidence in recognition. Only the recognition rate has been used as performance measure. Suppose that two measures ( _M_ 1 and _M_ 2) have recognized a face image (inside a database) with 100% similarity to a reference face image. This recognition does not mean that the two measures have the same performance. For example, if _M_ 1 produces significant similarities between the test image and another group of _K_ (a positive integer of) database images, then the suspected faces would be not only the one with maximal similarity, but a number 1 + _K_ of possible faces. Now if _M_ 2 produces significant similarity with one correct face while giving trivial similarities with the rest of the database images, then _M_ 2 is giving the correct answer with more confidence than _M_ 1 which gave several confusing faces in addition to the best match. We will see that the proposed measure outperforms existing measures by far in giving less confusion while recognizing the best match (in a database) for a given face image. 

## **4. Experimental Results and Performance** 

## _4.1. Image Database_ 

Most automatic face recognition systems are dependent on a comparison between a given face image (a reference image) and images saved in memory. The face images in memory are represented by a training set saved as a database. In this paper, our training sets are: 

1. ORL faces images database: AT&T (American Telephone & Telegraph, Inc; New York City, NY, USA) or ORL database this is a well-known database which is widely used for testing face recognition systems. It consists of 40 individuals; each with 10 different images (poses). These images are taken with different levels of illumination, rotation, facial expression and facial details such as glasses. The size of each image is 92 _×_ 112 pixels, with 256 grey levels per pixel [21]. See Figure 1. 

2. FEI faces images database: FEI database or Brazilian database, it consists of 200 individuals; each with 14 different images (poses). These images are taken at the artificial intelligence laboratory of FEI in Brazil; represented by students and staff at FEI, between 19 and 40 years old with distinct appearance, hairstyle, and adorns. The images in FEI database are colorful and size of each image 

_Appl. Sci._ **2017** , _7_ , 786 

7 of 17 

is 640 _×_ 480 pixels; in our experiment we used 700 images from FEI database for 50 individuals each with 14 poses [22]. See Figure 2. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0007-03.png)


**Figure 1.** Various face poses for a single person from The AT&T (American Telephone & Telegraph) Face Database. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0007-05.png)


**Figure 2.** Various face poses for a single person from The FEI (Brazilian) Face Database. 

## _4.2. Testing_ 

The proposed FSM approach is tested using MATLAB R2015 (from Mathworks Inc., Natick, MA, USA), with a focus on its performance in detecting similarity under noisy conditions. Specifically, the corruption of images under Gaussian noise is considered, due to the fact that this is the main source of noise in many image processing systems. Peak signal-to-noise ratio (PSNR) was used in this test, as follows: 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0007-09.png)


where _L_ is the maximum level of illumination and _pn_ is the power of the Gaussian noise [23]. 

## _4.3. Results and Discussion_ 

The new FSM technique was implemented as per Equation (9), with the well-known measures SSIM as per Equation (1) and FSIM as per Equation (2). These three methods were implemented simultaneously on 1100 images from two datasets; all images of AT&T database and 700 images of FEI database to compare their performance. The distance between the first and second maxima of the similarity curve (peaks) is used for all recognition methods. A greater distance means more confidence in the facial recognition decision. Almost for all cases, the proposed FSM keeps larger difference between the test image and other individuals; better confidence in the recognition process is obtained. Figure 3 shows the poses of the fourth person in the AT&T database, used for testing; Figure 4 shows the poses of the eighth person, also used for testing. Figure 5 shows the poses of the fifth person in FEI database and Figure 6 shows the poses of the fifteenth person in FEI database also used for testing. The reference pose, used as the test image, is indicated. A pose with no significant angle is chosen for the purposes of testing and comparison, although eye-glasses are considered in the first test (see Figure 3), which increases the difficulty of face recognition. 

_Appl. Sci._ **2017** , _7_ , 786 

8 of 17 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0008-02.png)


**Figure 3.** Poses for person No. 4 in AT&T database. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0008-04.png)


**Figure 4.** Poses for person No. 8 in AT&T database. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0008-06.png)


**Figure 5.** Poses for person No. 5 in FEI database. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0008-08.png)


**Figure 6.** Poses for person No. 15 in FEI database. 

_Appl. Sci._ **2017** , _7_ , 786 

9 of 17 

In Figures 7–10, the proposed FSM gives better performance in terms of recognition confidence. In spite of the fact that the other measures SSIM and FSIM correctly decide the proper person with maximum similarity, they give low confidence in their decision because there are many cases of distrust (big similarities with wrong persons) in their decisions (similarities); this is a big challenge when we employ these measures in security recognition tasks. FSM gives more confidence to decide the proper person from a database. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0009-03.png)


**----- Start of picture text -----**<br>
Face Recognition Using Similarity Measures<br>1<br>SSIM<br> Max at p = 4<br>FSM<br>0.8 FSIM<br>0.6<br>0.4<br>0.2<br>0<br>-0.2<br>0 5 10 15 20 25 30 35 40<br> Person index in database<br> Similarity with the test image<br>**----- End of picture text -----**<br>


**Figure 7.** Performance of similarity measures using person No. 4 (pose 10) in the AT&T database. Confidence in recognition for SSIM, FSIM and FSM is 0.5693, 0.2597 and 0.8556 respectively. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0009-05.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0009-06.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0009-07.png)


**----- Start of picture text -----**<br>
Face Recognition Using Similarity Measures<br>1<br>SSIM<br> Max at p = 8<br>FSM<br>0.8 FSIM<br>0.6<br>0.4<br>0.2<br>0<br>-0.2<br>0 5 10 15 20 25 30 35 4 0<br> Person index in database<br>**----- End of picture text -----**<br>


**Figure 8.** Performance of similarity measures using person No. 8 (pose 10) in the AT&T database. Confidence in recognition for SSIM, FSIM and FSM is 0.5773, 0.2803 and 0.8661 respectively. 

_Appl. Sci._ **2017** , _7_ , 786 

10 of 17 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0010-02.png)


**----- Start of picture text -----**<br>
Face Recognition Using Similarity Measures<br>1<br>SSIM<br>0.9  Max at p = 5 FSM<br>FSIM<br>0.8<br>0.7<br>0.6<br>0.5<br>0.4<br>0.3<br>0.2<br>0.1<br>0<br>0 5 10 15 20 25 30 35 40<br> Person index in database<br>of similarity measures using person No. 5 (pose 7) in<br> Similarity with the test image<br> Similarity with the test image<br>**----- End of picture text -----**<br>


**Figure 9.** Performance of similarity measures using person No. 5 (pose 7) in the FEI database. Confidence in recognition for SSIM, FSIM and FSM is 0.2354, 0.2103 and 0.8791 respectively. 

**Figure 10.** Performance of similarity measures using person No. 15 (pose 8) in the FEI database. Confidence in recognition for SSIM, FSIM and FSM is 0.2430, 0.1916 and 0.8697 respectively. 

Figure 11 shows the performance of similarity measures using person No. 15 in FEI database. Pose 8 is the Reference Image, while a different pose (pose 10) is used for testing for all database images (including the target person). FSIM fails, while confidence of SSIM, and FSM is 0.0364, 0.12 respectively. 

_Appl. Sci._ **2017** , _7_ , 786 

11 of 17 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-02.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-03.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-04.png)


**----- Start of picture text -----**<br>
Face Recognition Using Similarity Measures<br>1<br>SSIM<br>FSM<br>0.9 FSIM<br>0.8<br>0.7<br>0.6<br>0.5  Max at p = 15<br>0.4<br>0 5 10 15 20 25 30 35 4 0<br> Person index in database<br>**----- End of picture text -----**<br>


**Figure 11.** Performance ~~of similarity measures using person No. 15 in the FEI datab~~ ase. Pose 8 is the Reference Image, while pose 10 is used for testing for all database images (including the target person). FSIM fails, while confidence in recognition for SSIM, and FSM is 0.0364, 0.12 respectively. 

Figures 12–15 we simulated the confidence measure as per Equation (11) to show the efficiency of the proposed measure (FSM) in giving the highest confidence versus the well-known SSIM and FSIM. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-07.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-08.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-09.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-10.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-11.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-12.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-13.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-14.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-15.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-16.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-17.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-18.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-19.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-20.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-21.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-22.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-23.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-24.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-25.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-26.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-27.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-28.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-29.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-30.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0011-31.png)


**Figure 12.** Recognition confidence for similarity measures SSIM, FSIM and FSM using person No. 4 (pose 10) in the AT&T database. 

_Appl. Sci._ **2017** , _7_ , 786 

12 of 17 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-02.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-03.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-04.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-05.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-06.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-07.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-08.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-09.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-10.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-11.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-12.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-13.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-14.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-15.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-16.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-17.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-18.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-19.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-20.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-21.png)


**Figure 13.** Recognition confidence for similarity measures SSIM, FSIM and FSM using person No. 8 (pose 10) in the AT&T database. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-23.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-24.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-25.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-26.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-27.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-28.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-29.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-30.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-31.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-32.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-33.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-34.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-35.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-36.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-37.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-38.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-39.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-40.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-41.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-42.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-43.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-44.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0012-45.png)


**Figure 14.** Recognition confidence for similarity measures SSIM, FSIM and FSM using person No. 5 (pose 7) in FEI database. 

In Figures 16–19, the proposed measure FSM produces near-one (maximal) similarity for similar images under Gaussian noise, while giving near-zero similarity when the images are dissimilar. The other measures SSIM and FSIM gave non-trivial amounts of similarity when the two images are quite different, which indicates a shortcoming in these measures. 

_Appl. Sci._ **2017** , _7_ , 786 

13 of 17 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-02.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-03.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-04.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-05.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-06.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-07.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-08.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-09.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-10.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-11.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-12.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-13.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-14.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-15.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-16.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-17.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-18.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-19.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-20.png)


**Figure 15.** Recognition confidence for similarity measures SSIM, FSIM and FSM using person No. 15 (pose 7) in FEI database. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-22.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-23.png)


**----- Start of picture text -----**<br>
( a )<br>**----- End of picture text -----**<br>



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-24.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-25.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-26.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-27.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-28.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-29.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-30.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-31.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-32.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-33.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-34.png)


**----- Start of picture text -----**<br>
( b )<br>**----- End of picture text -----**<br>



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-35.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-36.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-37.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-38.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-39.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-40.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0013-41.png)


**Figure 16.** Performance of similarity measures using similar images under Gaussian noise; ( **a** ) The test images; ( **b** ) Performance comparison among (SSIM, FSM and FSIM) under Gaussian noise. 

_Appl. Sci._ **2017** , _7_ , 786 

14 of 17 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0014-02.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0014-03.png)


**----- Start of picture text -----**<br>
( a )<br>( b )<br>**----- End of picture text -----**<br>



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0014-04.png)


**Figure 17.** Performance of similarity measures using similar images under Gaussian noise; ( **a** ) Above: The test images; ( **b** ) Performance comparison among (SSIM, FSM and FSIM) under Gaussian noise. 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0014-06.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0014-07.png)


**----- Start of picture text -----**<br>
( a )<br>( b )<br>**----- End of picture text -----**<br>


**Figure 18.** Performance of similarity measures using dissimilar images under Gaussian noise; ( **a** ) Above: The test images; ( **b** ) Performance of SSIM, FSM and FSIM under Gaussian noise. 

_Appl. Sci._ **2017** , _7_ , 786 

15 of 17 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0015-02.png)



![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0015-03.png)


**----- Start of picture text -----**<br>
( a )<br>( b )<br>**----- End of picture text -----**<br>


**Figure 19.** Performance of similarity measures using dissimilar images under Gaussian noise; ( **a** ) The test images; ( **b** ) Performance comparison among (SSIM, FSM and FSIM) under Gaussian noise. 

Figures 7 and 8 show the results of the similarity test on person No. 4 and person No. 8 in AT&T database. The similarity test between the reference image and other images in database, where for the 10 poses for each individual the maximum similarity between the rest of the poses is considered. 

Figures 9 and 10 show the results of the similarity test on person No. 5 and person No. 15 in FEI database. The similarity test between the reference image and other images in database, where for the 14 poses for each individual the maximum similarity between the rest of the poses is considered. 

The performance of the proposed measure was also tested when the image was corrupted with Gaussian noise. Peak signal-to-noise ratio (PSNR) was utilized in this case, as discussed above for Equation (12); this was then compared with the structural similarity measure (SSIM) and feature similarity measure (FSIM). The results show the effectiveness of FSM in similarity and face recognition. Figures 16 and 17 show the performance of FSM for similar images under Gaussian noise, while Figures 18 and 19 show the performance of FSM for dissimilar images under Gaussian noise. Similar images from AT&T database corrupted with Gaussian noise were tested; these are shown in Figure 16a. The performance of FSM (represented by Equation (9)) as compared to that of SSIM and FSIM is shown in Figure 16b. 

Similar images from FEI database corrupted with Gaussian noise were tested; these are shown in Figure 17a. The performance of FSM (represented by Equation (9)) as compared to that of SSIM and FSIM is shown in Figure 17b. 

The results of comparing another face image are shown in Figure 18a. Another face image was used from AT&T database as the dissimilar image. Figure 18b shows the performance of FSM (represented by Equation (9)) as compared to SSIM and FSIM for conditions of Gaussian noise. 

In [24] it is shown that higher-order correlations can lead to better performance. It is the intention of the authors to extend this work in the near future towards a higher-order correlative measure, analogous to that in Equation (9). 

_Appl. Sci._ **2017** , _7_ , 786 

16 of 17 

The results of comparing another face image are shown in Figure 19a. Another face image was used from FEI database as the dissimilar image. Figure 19b shows the performance of FSM [represented by Equation (9)] as compared to SSIM and FSIM under Gaussian noise. 

## **5. Conclusions** 

An efficient similarity measure known as the feature-based structural measure (FSM) is proposed here, based on a rational functional and combining the well-known algorithms of the structural similarity measure (SSIM) and feature similarity measure (FSIM) with Canny edge-detected versions of two images. This measure enhances the best features of both SSIM and FSIM in addition to the distinctive structural feature provided by Canny’s approach. It is shown here that FSM outperforms the conventional SSIM and FSIM in its ability to detect the similarity (that is, high similarity results) among similar faces, even under significantly noisy conditions; it also avoids the detection of similarity in the case of dissimilar faces, which is a major shortcoming of the existing FSIM and SSIM approaches. A measure for confidence in face recognition has also been proposed as a performance measure for face recognition methods. In facial recognition tasks, FSM gives higher recognition confidence than existing measures. In addition to confidence, the proposed measure (FSM) gives a reliable similarity between any two images even under noise, in other words, FSM produces maximal similarity when the images are similar, while giving near-zero similarity when the images are dissimilar. These properties gave the proposed measure high ability to recognize face images under noisy conditions, different facial expressions and pose variations. Such properties are highly needed in security applications while checking the identity of a specific face image in a big database. In this work, global analysis of facial images has been used, in which the complete facial region is taken as input data and treated simultaneously. Local face analysis has been shown to play an important role in improving face recognition performance. The authors intend to extend their previous work on local analysis to improve the performance of the above measure. In addition, the Authors suggested a call for 3D image similarity, a new topic that they will handle soon. 

**Acknowledgments:** The Authors would like to thank Huazhong University of Science and Technology (China), Edith Cowan University (Australia), and Chinese Scholarship Council for financial support of this project. Many thanks go to the (anonymous) Reviewers of this work for their deep remarks and constructive comments. Without those valuable comments this paper would never be in this readable form. 

**Author Contributions:** All authors extensively discussed the contents of this paper and contributed to its modelling and preparation. Noor Abdalrazak Shnain and Zahir M. Hussain proposed the model, drafted the manuscript, performed experiments, and analyzed results. The revisions of mathematical modelling and simulations were done by Song Feng Lu. 

**Research Ethics:** The authors declare that there are no ethical issues associated with this work. 

## **References** 

1. Parmar, D.N.; Mehta, B.B. Face recognition methods & applications. _arXiv_ **2014** , arXiv:1403.0485. 

2. Zhao, W.; Chellappa, R.; Phillips, P.J.; Rosenfeld, A. Face recognition: A literature survey. _ACM Comput. Surv. (CSUR)_ **2003** , _35_ , 399–458. [CrossRef] 

3. Barrett, W.A. A survey of face recognition algorithms and testing results. In Proceedings of the Conference Record of the Thirty-First Asilomar Conference on Signals, Systems & Computers, Pacific Grove, CA, USA, 2–5 November 1997. 

4. Fromherz, T. _Face Recognition: A Summary of 1995–1997_ ; Technical Report ICSI TR-98-027; International Computer Science Institute: Berkeley, CA, USA, 1998. 

5. Wiskott, L.; Fellous, J.M.; Krüger, N.; Malsburg, C.V.D. Face recognition by elastic bunch graph matching. _IEEE Trans. Pattern Anal. Mach. Intell._ **1997** , _19_ , 775–779. [CrossRef] 

6. Turk, M.A.; Pentland, A.P. Face recognition using eigenfaces. In Proceedings of the CVPR’91 IEEE Computer Society Conference on Computer Vision and Pattern Recognition, Washington, DC, USA, 19–23 June 1991. 

_Appl. Sci._ **2017** , _7_ , 786 

17 of 17 

7. Belkasim, S.O.; Shridhar, M.; Ahmadi, M. Pattern recognition with moment invariants: A comparative study and new results. _Pattern Recognit._ **1991** , _24_ , 1117–1138. [CrossRef] 

8. Taj-Eddin, I.A.; Afifi, M.; Korashy, M.; Hamdy, D.; Nasser, M.; Derbaz, S. A new compression technique for surveillance videos: Evaluation using new dataset. In Proceedings of the Sixth International Conference on Digital Information and Communication Technology and its Applications (DICTAP), Konya, Turkey, 21–23 July 2016. 

9. Wang, Z.; Bovik, A.C.; Sheikh, H.R.; Simoncelli, E.P. Image quality assessment: From error visibility to structural similarity. _IEEE Trans. Image Process._ **2004** , _13_ , 600–612. [CrossRef] [PubMed] 

10. Hashim, A.N.; Hussain, Z.M. Novel imagedependent quality assessment measures. _J. Comput. Sci._ **2014** , _10_ , 1548–1560. [CrossRef] 

11. Hu, Y.; Wang, Z. A similarity measure based on Hausdorff distance for human face recognition. In Proceedings of the 18th International Conference on Pattern Recognition (ICPR 2006), Hong Kong, China, 20–24 August 2006. 

12. Xu, Y.; Yao, L.; Zhang, D.; Yang, J.Y. Improving the interest operator for face recognition. _Exp. Syst. Appl._ **2009** , _36_ , 9719–9728. [CrossRef] 

13. Zhang, L.; Zhang, L.; Mou, X.; Zhang, D. FSIM: A feature similarity index for image quality assessment. _IEEE Trans. Image Process._ **2011** , _20_ , 2378–2386. [CrossRef] [PubMed] 

14. Singh, C.; Sahan, A.M. Face recognition using complex wavelet moments. _Opt. Laser Technol._ **2013** , _47_ , 256–267. [CrossRef] 

15. Li, H.; Suen, C.Y. Robust face recognition based on dynamic rank representation. _Pattern Recognit._ **2016** , _60_ , 13–24. [CrossRef] 

16. Li, L.; Xu, C.; Tang, W.; Zhong, C. 3D face recognition by constructing deformation invariant image. _Pattern Recognit. Lett._ **2008** , _29_ , 1596–1602. [CrossRef] 

17. Marcolin, F.; Vezzetti, E. Novel descriptors for geometrical 3D face analysis. _Multimedia Tools Appl._ **2017** , _76_ , 13805–13834. [CrossRef] 

18. Moos, S.; Marcolin, F.; Tornincasa, S.; Vezzetti, E.; Violante, M.G.; Fracastoro, G.; Speranza, D.; Padula, F. Cleft lip pathology diagnosis and foetal landmark extraction via 3D geometrical analysis. _Int. J. Interact. Des. Manuf. (IJIDeM)_ **2017** , _11_ , 1–18. [CrossRef] 

19. Hassan, A.F.; Hussain, Z.M.; Cai-lin, D. An Information-Theoretic Measure for Face Recognition: Comparison with Structural Similarity. _Int. J. Adv. Res. Artif. Intell._ **2014** , _3_ , 7–13. 

20. Canny, J. A computational approach to edge detection. _IEEE Trans. Pattern Anal. Mach. Intell._ **1986** , _8_ , 679–698. [CrossRef] [PubMed] 

21. AT&T Laboratories Cambridge. The Database of Faces. Available online: http://www.cl.cam.ac.uk/ research/dtg/attarchive/facedatabase.html (accessed on 28 April 2017). 

22. Thomaz, C.E. (Caru). FEI Face Database. Available online: http://fei.edu.br/~cet/facedatabase.html (accessed on 15 May 2017). 

23. Hassan, A.F.; Cai-lin, D.; Hussain, Z.M. An information-theoretic image quality measure: Comparison with statistical similarity. _J. Comput. Sci._ **2014** , _10_ , 2269–2283. [CrossRef] 

24. Lajevardi, S.M.; Hussain, Z.M. Novel higher-order local autocorrelation-like feature extraction methodology for facial expression recognition. _IET Image Process._ **2010** , _4_ , 114–119. [CrossRef] 


![](saved_pdfs/unchecked/SLPXDX3L/images/SLPXDX3L.pdf-0017-20.png)


- © 2017 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (http://creativecommons.org/licenses/by/4.0/). 

