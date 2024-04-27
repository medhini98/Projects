**IDENTIFYING ENTITIES IN HEALTHCARE DATA**  
  
**Problem Statement**  
  
Build a custom NER to get a list of different treatments for diseases
from clinical text data. The goal is to extract valuable insights from
unstructured medical text, facilitating easier decision-making in
treatment processes.  
  
**Data Description**  

- The data consists two types of files - sentences file and label file.
  This is split into train and test.

- Sentence file: This consists of sentences extracted from different
  clinical records. Each individual word is in a single line of the
  file.

- Label file: For each word in each line of the sentence file, there is
  a corresponding line in the label file that provides the label of that
  word. The labels are T (treatment), D (disease), O (other).

- There is a one-on-one mapping between the sentence and label files.

- In this ‘train_sent’ dataset, there are a total of 2,599 sentences
  when we form the sentences from the words. Similarly, there are a
  total of 1,056 sentences in the ‘test_sent’ dataset.

- The labels in the label files correspond to each word that is
  available in the ‘train_sent’ and 'test_sent' datasets. So, in the
  ‘train_label’ dataset, there are a total of 2,599 lines of labels when
  we form the lines from the label dataset. Similarly, there are a total
  of 1,056 lines of labels in the ‘test_label’ dataset.  
    
  **Methodology**  
    
  **1. Data Preprocessing**
  Transform such that we recover complete sentences and label sequences.
  Empty lines in the files indicate end of current sentence.  
    
  **2. Exploratory Data Analysis**  
  Use PoS tagging on complete data for concept identification. For this,
  use space to identify NOUNs and PROPNs and their frequency.  
    
  **3. Feature Engineering**  
  Define features to train CRF model. Define as features: PoS tags,
  information of preceding word (PoS tag), and beginning and end words
  of sentence. Apply these features in each sentence of the train and
  the test dataset to get the feature values. This is an input variable
  for the CRF model. Labels form the target variable.  
    
  **4. Model Training**  
  Define the target variable and then build the CRF model to identify
  diseases and their treatments from the data.  
    
  **5. Prediction**  
  Use this model to predict labels in the test set.  
    
  **6. Evaluation**  
  Predict labels for test data and evaluate performance using F1
  score.  
    
  **7. Application**  
  The model can be used to identify diseases and treatments. The output
  is structured into a table, mapping diseases to their corresponding
  treatments as identified by the model. This table can then be used to
  can be used to analyze treatment patterns, understand the correlation
  between diseases and treatments, and identify the most commonly
  prescribed treatments for different conditions. This analysis is
  crucial for healthcare data insights and for improving patient care
  strategies.  
    
  **8. Results**  
  The CRF model achieved an F1 score of 91.34%.  
    
  **Domain/Data Assumptions**  

<!-- -->

- If there is a disease in the sentences, then the treatment mentioned
  in that sentence can be assumed to be the treatment for that disease.

- The same treatment can work for different diseases.
