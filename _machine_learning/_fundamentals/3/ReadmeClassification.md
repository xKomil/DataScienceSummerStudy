# Classification

# Mnist
- importing the dataset
- splitting the dataset into training and testing sets

# Training a Binary Classifier
Binary classifier is a ml model designed to determine which one of two classes a given input belongs
- starting by only identifying one digit
- using stochastic gradient descent (*Summary*)

# Performance Measures
## Measuring Accuracy Using Cross-Validation
Cross-Validation Accuracy: High accuracy values from cross_val_score suggest that the SGDClassifier performs well on the training data.
Dummy Classifier: Comparing with a dummy classifier helps confirm that the model’s high accuracy is not just due to class imbalance but reflects its actual predictive power.

For example, in your case, since only about 10% of the images are of the digit '5', a classifier that always predicts "not a 5" will still achieve a high accuracy of around 90%. This high accuracy can be deceptive because it doesn't reflect how well the model is performing on the minority class

Stratified k-fold (*Summary*) do what cross-validation does, where each fold maintains class distribution. It trains a cloned classifier on training data and evaluates it on test data, printing the accuracy for each fold. This approach allows for custom cross-validation control and is especially useful when fine-tuning the process.

## Confusion Matrices

To evaluate a classifier, the confusion matrix provides insights into how often the model misclassifies instances of one class as another. Here's how you can use it effectively:
Confusion Matrix:
- It counts the number of times instances of each class are classified as each possible class.
- For instance, if you're interested in how often images of 8s are misclassified as 0s, you'd check the value in row #8, column #0 of the matrix.

Using cross_val_predict():
- Instead of using the test set directly for predictions (which you should reserve for final evaluation), use cross_val_predict() to get predictions through k-fold cross-validation.
- This function returns predictions for each instance in the training set as if it were out-of-sample data, providing a clearer picture of model performance.

Computing the Confusion Matrix:
- Once you have the predictions, use the confusion_matrix() function.
- Pass the true labels (y_train_5) and the predicted labels (y_train_pred) to this function to generate the confusion matrix.

![alt text](image.png)


Precision and Recall are key metrics used to evaluate the performance of a classifier, especially in scenarios with imbalanced classes.

Precision:

​![alt text](image-1.png)
Where:

TP: True Positives - the number of correctly identified positive instances.
FP: False Positives - the number of incorrectly identified positive instances.
Explanation: Precision measures how many of the predicted positive instances are actually positive. A classifier with perfect precision predicts all positive cases correctly but might only make a few positive predictions overall.

Example: A classifier that always predicts negative except for one instance (which is correctly predicted as positive) would have 100% precision (since it made one correct positive prediction out of one attempt). However, this is not practical for real-world applications where you need to detect multiple positive instances.

Recall (Sensitivity or True Positive Rate)
Recall: 

![alt text](image-2.png)​
Where:

TP: True Positives - the number of correctly identified positive instances.
FN: False Negatives - the number of positive instances that were incorrectly identified as negative.
Explanation: Recall measures how many of the actual positive instances were correctly detected by the classifier. It is important when the goal is to identify as many positive cases as possible, even if it means some false positives.

Example: If a classifier identifies 80 out of 100 actual positives correctly but misses 20, its recall would be 80%.

## Precission and Recall

To better evaluate classifiers, precision and recall can be combined into a single metric called the F1 score, which is the harmonic mean of precision and recall. This means the F1 score is high only if both precision and recall are high

![alt text](image-3.png)

The F score favors classifiers with similar precision and recall, which isn't always ideal. Sometimes precision is more important, other times it's recall. For instance, a classifier detecting kid-safe videos should prioritize high precision, even if it means low recall, to ensure only safe videos are kept. Conversely, a classifier identifying shoplifters can have low precision if it maintains high recall, ensuring most shoplifters are caught despite some false alerts. Increasing precision reduces recall and vice versa, known as the precision/recall trade-off.

## The Precision/Recall Trade-off
To understand this trade-off, let’s look at how the SGDClassifier makes its classification decisions. It computes a score for each instance using a decision function. If the score exceeds a threshold, the instance is classified as positive; otherwise, it's classified as negative.

Suppose the threshold is set at a certain point: on one side, there are true positives (correctly identified instances), and on the other, there are false positives (incorrectly identified instances). For example, with the threshold at a certain point, you might have 4 true positives and 1 false positive, resulting in a precision of 80% (4 out of 5) and a recall of 67% (4 out of 6).

Raising the threshold can eliminate false positives (increasing precision to 100%) but may also convert true positives into false negatives, reducing recall to 50%. Lowering the threshold has the opposite effect, increasing recall but reducing precision.

## The ROC Curve
The receiver operating characteristic (ROC) curve is a common tool for binary classifiers. Unlike the precision/recall curve, the ROC curve plots the true positive rate (recall) against the false positive rate (FPR). The FPR is the ratio of negative instances incorrectly classified as positive and is equal to 1 minus the true negative rate (TNR), also known as specificity. Therefore, the ROC curve plots sensitivity (recall) versus 1 minus specificity

You can plot the FPR against the TPR using Matplotlib. The following code produces the plot in Figure 3-7. To find the point that corresponds to 90% precision, we need to find the index of the desired threshold. Since thresholds are listed in decreasing order, we use <= instead of >= on the first line.

One way to compare classifiers is by measuring the *area under the curve (AUC)*. A perfect classifier has a ROC AUC of 1, while a random classifier has a ROC AUC of 0.5. Scikit-Learn provides a function to estimate the ROC AUC.

TIP: Since the ROC curve is similar to the precision/recall (PR) curve, you may wonder which one to use. Generally, prefer the PR curve when the positive class is rare or when false positives are more concerning than false negatives. Otherwise, use the ROC curve. For example, a high ROC AUC score might suggest a good classifier, but this could be due to a low number of positives. In contrast, the PR curve can highlight that the classifier needs improvement by showing how close it is to the top-right corner.

These are estimated probabilities, not actual ones. For instance, images classified as positive with an estimated probability of 50%-60% are actually positive about 94% of the time, indicating the model's probabilities are too low. Models can also be overconfident. The sklearn.calibration package provides tools to calibrate these probabilities to better match actual probabilities. See the extra material section in this chapter’s notebook for more details.

## Multiclass classification

Binary classifiers distinguish between two classes, while multiclass classifiers can handle more than two classes. Some Scikit-Learn classifiers (e.g., LogisticRegression, RandomForestClassifier) natively support multiclass classification, while others are strictly binary (e.g., SGDClassifier, SVC). To perform multiclass classification with binary classifiers, two strategies are common:

One-versus-the-rest (OvR): Train a binary classifier for each class, and classify based on which classifier gives the highest score.
One-versus-one (OvO): Train a binary classifier for every pair of classes. This approach requires more classifiers but is more efficient for algorithms that scale poorly with large datasets.
Scikit-Learn automatically applies OvR or OvO depending on the algorithm used.

![alt text](image-4.png)
# Summary
## [stochastic gradient descent](https://www.geeksforgeeks.org/ml-stochastic-gradient-descent-sgd/)

Stochastic Gradient Descent (SGD) is an optimization algorithm used in training machine learning models, especially in deep learning and linear regression. It is a variant of the Gradient Descent algorithm and is particularly useful for large datasets and online learning scenarios.

Gradient Descent:
Gradient Descent is an optimization technique used to minimize a loss function by iteratively moving towards the minimum value.
It involves computing the gradient (partial derivatives) of the loss function with respect to the model parameters and updating the parameters in the opposite direction of the gradient.

Stochastic Gradient Descent:
Unlike traditional Gradient Descent, which uses the entire dataset to compute the gradient at each step, SGD uses only one sample (or a small batch of samples) at each iteration.
This makes SGD faster and more suitable for large datasets because it can start making progress right away and does not require loading the entire dataset into memory.

## [StratifiedKFold](https://www.geeksforgeeks.org/stratified-k-fold-cross-validation/)
StratifiedKFold is an enhancement to the standard k-fold cross-validation method. It ensures that each fold of the dataset used for training and testing preserves the percentage of samples for each class label, maintaining the class distribution across all folds. This is particularly useful for imbalanced datasets, where some classes are much more frequent than others.

## [Decision Function](https://www.geeksforgeeks.org/ml-decision-function/)
Decision function is a method present in classifier{ SVC, Logistic Regression } class of sklearn machine learning framework. This method basically returns a Numpy array, In which each element represents whether a predicted sample for x_test by the classifier lies to the right or left side of the Hyperplane and also how far from the HyperPlane. It also tells us that how confidently each value predicted for x_test by the classifier is Positive ( large-magnitude Positive value ) or Negative ( large-magnitude Negative value)

## [AUC](https://www.statystyczny.pl/auc-area-under-curve-czyli-co-kryje-sie-pod-krzywa/)

The Area Under the Curve (AUC) is a metric used to evaluate the performance of a binary classifier by measuring the area under its ROC curve. It ranges from 0.5 for a random classifier to 1 for a perfect classifier.

# 205