---
title: Real-Time NLPOps System
weight: 1
---
# E-commerce Real-time Product Classification

- **Main Roles**
    - Analyzed data, researched case studies, and implemented findings.
    - Experimented with **BERT models** and **LLMs** for classification tasks.
    - Designed and tested a **retraining pipeline** in a containerized environment.
    - Monitored and reported issues during the **maintenance phase**.
    - Retrained the classification model to accommodate **category revisions**.
- **Duration**: 13 months 
    - **8 months** for system development
    - **5 months** for maintanance and retraining model
- **Tech Stacks**: 
`PyTorch`, `BERT(RoBERTa)`, `LLM(Solar10.7B)`, `Drift Detection`, `Retraining Pipeline`, `Docker`

## Summary
This project aimed to develop an **automated product classification system** for a Korean e-commerce platform facing challenges such as high product registration volume, category misclassification, seasonal data bias, and evolving category structures. A modified filtering method and LLM-assisted annotation significantly improved training data quality. The system utilized a BERT-based model with a threshold-based review process, allowing low-confidence predictions to be flagged for human annotation via a back-office system, improving efficiency through soft labeling. A retraining pipeline was established, incorporating human-annotated data and managing updates via Docker-based automation. The final model achieved 91% accuracy, with 89% of products expected to be correctly categorized post-migration, while significantly reducing annotation costs, improving maintainability, and enhancing scalability to adapt to evolving e-commerce trends.

<hr>

## Problem Statement

An online e-commerce shopping mall in Korea connects sellers and customers by 
receiving product information from sellers and making it available to customers. 
While the shop primarily sells clothing, it also offers fresh food, furniture, and pet supplies.

The problem lies in the registration process, where most sellers upload products in bulk (or 
through agencies using automated programs), leading to a noticeable tendency for category 
misclassification. According to a sample analysis, approximately <u>35% of all products are miscategorized</u>.

To address this issue, the shop requires an automated system, as it currently has 
<u>over 10 million products on sale</u> and <u>around 60K new products registered daily</u>. However, a major 
challenge is the limited budget for human annotation, making it difficult to create high-quality 
training data. Additionally, since e-commerce trends evolve rapidly, the category system is revised 
every six months. Furthermore, because the ultimate goal of this project is to enhance 
customer experience, a real-time system is essential. The project also involves developing a
back-office platform for additional human annotation and data management.

📌 **Problem**

Resolving the issue of products being placed in inappropriate categories: for both products in the shop and those being registered

📌 **Conditions**
- Limited budget for human annotation, compared to huge amount of data to process
- Categories are revised every 6 months
- Real-time system is required

## Key Findings from Data Analysis

After reviewing the complete product dataset at multiple points in time, the team identified the following key insights:

1. The raw dataset consists of more than **10 million products** and is _highly skewed_ in terms of class distribution.
2. The number of product categories exceeds **2,000**.
3. Some products belong to multiple categories, while others do not fit into any. However, 
the shop's policy allows only one category per product, which can cause confusion for both the model and human annotators.
4. Certain categories exhibit strong seasonality, with the number of products fluctuating significantly—sometimes even dropping to zero.


## Key Approaches & Solutions

### 1. Selecting Features
- Classification using product titles yielded the highest performance.
- When training a baseline model with ViT on product images, the accuracy was extremely low due to data noise. Given the need for low latency and low cost, image data was not used.
- Adding additional features such as product price and registered category did not result in significant performance improvements.

### 2. Filtering Training Data
- Applied a modified filtering method based on the approach from [Amazon paper](/docs/portfolio/with-toc/#reference), leading to a slight performance improvement.
    - The core idea was to remove uncertain product-category pairs from the training data as much as possible, iteratively refining the model's accuracy.
    - However, a downside was the total removal of certain patterned data.
- Used LLM for annotation
    - Trained the LLM on a small set of human-annotated data. Since there were a large number of categories, we used fine-tuned BERT to select the Top-K predictions as annotation choices.
    - The LLM achieved an accuracy of approximately 80%. However, when the generated product-category pairs were added to the training data, the classification model showed a significant performance improvement.

### 3. Systemic Approach
- Used a single BERT model to enable low-cost, fast classification while ensuring maintainability.
- Since the classification model cannot be 100% accurate, a **threshold** was set on the model’s classification scores. Cases that were not automatically classified were reviewed step-by-step based on their scores.
- A back-office system was developed for project managers to facilitate this process.
    - This allowed annotation tasks or review of unclassified data to be <u>prioritized based on the model's confidence scores</u>, with lower-scoring cases checked first.
    - Similar to LLM-based training data filtering, **soft predictions** were provided to significantly accelerate human annotation.
        - Instead of selecting from over 2,000 categories, annotators could choose from the Top-10 predicted categories, greatly improving efficiency.

### 4. Building a Retraining Pipeline
- The most critical part of the retraining pipeline was generating new training data.
    - Human-annotated data from the back-office was added in appropriate proportions to both the training and evaluation sets.
- Since the train & eval datasets and incoming data for the automatic classification system were managed via a production database, the process of retrieving and updating datasets was implemented using Docker containers.
- Continuous Learning was tested, but it resulted in a 6% drop in accuracy, indicating difficulty in maintaining memory from previous models.
    - Instead of pure continual learning, we adopted a strategy where new data was added to the existing training dataset to ensure stable performance.


## Main Technologies

- Implemented an automated [masked filtering method](https://www.amazon.science/publications/robust-product-classification-with-instance-dependent-noise) to refine training data from raw data.
- Trained and deployed BERT([RoBERTa](https://huggingface.co/klue/roberta-base)) for classification tasks.
- Trained and deployed LLM([Solar 10.7B](https://huggingface.co/upstage/SOLAR-10.7B-Instruct-v1.0)) using [H2O LLM Studio](https://h2o.ai/platform/ai-cloud/make/llm-studio/) as the code base.
- Developed a **retraining pipeline** in an **AWS Docker environment**, managing data retrieval from the database and reintegration after processing.

## Maintanance and Retraining

### Maintananace

- Weekly and monthly reports indicated a slight drift in incoming data.
- The model struggled to determine whether a product titled "T-shirt" was short-sleeved or 
long-sleeved (i.e., the title lacked sufficient information for classification).
    - **Status**: The model exhibited high confidence in these misclassifications.
    - **Cause**: Since most of the training data consisted of products available from 
    winter to spring, the majority of "T-shirts" in the dataset were long-sleeved.
    - **Action Plan**: While it is impossible to correctly classify a product
    without sufficient information, incorporating additional data from various seasons 
    can improve the model. This adjustment will be implemented in the retraining process.
- Minor issues related to API and database connections were resolved.

### Retraining

- In the production database, the training and evaluation datasets were updated 
with human-annotated data, while category revisions were handled by another department.
- The model was retrained with the updated data, yielding performance similar to previous results.
- The updated training data was systematically stored in the database for ongoing management, and 
the model was trained and evaluated through an automated pipeline.

## Insights
Throughout this project, I participated in the AI model lifecycle, which played a major role in the system.
Looking back, most of the effort was focused on analyzing data—directly tied to business problems—and 
developing strategies to meet business needs: <u>**reducing costs, increasing efficiency, and ensuring continuous operation.**</u>

<hr>

## Reference
- [Robust Product Classification with Instance-Dependent Noise, ECNLP 2022](https://www.amazon.science/publications/robust-product-classification-with-instance-dependent-noise)