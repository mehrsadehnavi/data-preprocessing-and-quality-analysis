# Data Quality Assessment and Preprocessing Pipeline

## Overview
This project focuses on analyzing, cleaning, and preparing raw datasets for data mining and machine learning tasks. It includes data quality evaluation based on ISO 25012 standards, preprocessing techniques, and exploratory data analysis (EDA).

The project also involves integrating multiple datasets to improve data completeness and analytical power.

---

## Objectives
- Evaluate data quality using standard metrics
- Handle missing and inconsistent data
- Detect and remove outliers
- Transform and normalize data
- Perform exploratory data analysis
- Integrate multiple datasets

---

## Dataset Description
The project uses application-related datasets (e.g., app metadata including ratings, installs, categories, etc.).

Two datasets are used:
- Primary dataset (incomplete)
- Secondary dataset (larger and more complete)

---

## Phase 1: Data Understanding

### Statistical Analysis
For numerical features:
- Mean
- Median
- Mode
- Min / Max
- Range
- Outlier detection

### Visualization
- Box plots for detecting outliers

---

## Phase 2: Data Quality Assessment

Data quality evaluated based on ISO 25012 (Intrinsic Data Quality):

- Completeness
- Accuracy
- Consistency
- Validity
- Currentness

### Tasks
- Identify missing values (null analysis)
- Detect inconsistencies and errors
- Analyze:
  - Single-schema issues
  - Multi-schema inconsistencies
  - Instance-level problems

---

## Phase 3: Data Preprocessing

### 1. Missing Value Handling
- Mean / Median / Mode imputation
- Column removal (if necessary)

### 2. Data Transformation
- Normalization / Scaling
- Data type conversion

### 3. Feature Engineering
- Creating new features from existing columns

### 4. Outlier Handling
- Detection using statistical methods and boxplots
- Removal or treatment

### 5. Data Reduction
- Removing irrelevant or redundant features

### 6. Encoding
- Converting numerical to categorical (if needed)

### 7. Text Processing (if applicable)
- Tokenization
- Stopword removal
- Stemming / Lemmatization (NLTK)

### 8. Statistical Analysis
- Comparison of app ratings (e.g., Sports category vs overall average)

### 9. Data Visualization
- Graphical representation of key insights

---

## Phase 4: Dataset Integration

- Merge two datasets
- Match similar columns
- Resolve inconsistencies
- Fill missing values after merging
- Create new combined features

---

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib / Seaborn
- NLTK (for text processing)

---

## Project Structure
├── datasets/
| ├── GooglePlay.csv
├── outputs/
| ├── MergedDataset.csv
| ├── Modified_GooglePlay.csv
├── main.py/

---

## How to Run

1. Install dependencies:
pip install pandas numpy matplotlib seaborn nltk

2. Run the scripts

---

## Key Concepts Demonstrated
- Data cleaning and preprocessing pipelines
- Data quality assessment frameworks
- Feature engineering
- Exploratory data analysis (EDA)
- Dataset integration and transformation

---

## Results
- Improved dataset quality
- Reduced missing values and inconsistencies
- Extracted meaningful statistical insights
- Enhanced dataset readiness for machine learning

---

## Author
Mehrsa Dehnavi
