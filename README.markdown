# CS114 Machine Learning Final Project - UIT

This repository contains the final project for the CS114 Machine Learning course at UIT. The project consists of two sub-projects: **Handwritten Digits Classification** and **Scores Prediction Based on Wecode Practical Score**.

## Part 1: Handwritten Digits Classification

- **Dataset**: The dataset for this task was collected by all students in the class and aggregated at: [Kaggle Handwritten TL Dataset](https://www.kaggle.com/datasets/nahrixt/handwritten-tl).
- **Objective**: We will experiment with various models and architectures on the above dataset. The trained models will then be used to predict labels for two larger datasets:
  - **2k Images Dataset**: [Kaggle Handwritten Test 2k](https://www.kaggle.com/datasets/nahrixt/handwritten-test-cs114)
  - **10k Images Dataset**: [Kaggle Handwritten Test 10k](https://www.kaggle.com/datasets/nahrixt/handwritten-test-10k)
- **Directory Structure**: The `hwd_checkpoints` directory stores the experimental results with the following structure:

```
hwd_checkpoints
    ├── dataset1 (named based on input preprocessing for the model)
    │   ├── model1 (model trained on this dataset)
    │   │   ├── handwritten-digits-classifier.ipynb
    │   │   ├── predict_2k_<submit_id>_<score>.txt: prediction results on the 2k dataset
    │   │   ├── predict_10k_<submit_id>_<score>.txt: prediction results on the 10k dataset
    │   │   ├── best_model.pth: saved file of the best model
    │   │   ├── train_log.txt: log file of the training process
    │   ├── model2
    │   ├── ...
    │   ├── modeln
    ├── dataset2
    ├── dataset3
    ├── top.py
```

- **top.py Script**: This script aggregates and compares the results of the experimented models. Usage:
  ```bash
  python top.py --top <X> --set <Y>
  ```
  Where:
  - `X`: An integer specifying the number of top results to display (default is 4).
  - `Y`: A string, either `"2k"`, `"10k"`, or `"all"`, to select the dataset for display (default is `"all"`).

## Part 2: Scores Prediction Based on Wecode Practical Score

[On going]
