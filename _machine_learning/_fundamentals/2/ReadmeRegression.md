# Step by step project as Data scientist
## Steps
- Look at the big picture 
- Get the data
- Explore and visualize the data to gain insights
- Prepare the data for machine learning algorithms
- Select a model and train it
- Fine-tune your model
- Present your solution
- Maintain your system

# Look at the big picture
- What is the problem you are trying to solve?
- What is the business goal?
- Select a performance measure
- Check the assumptions


A *pipeline* in machine learning refers to a sequence of data processing steps, where the output of one component is the input for the next. This structured flow ensures the systematic handling of data transformations, model training, and evaluation.

### Business goal / problem
In this example, the goal is to predict the median housing price in any district based on various metrics.
It's typical supervised learning task, because we can train the model with labeled examples (we have expected median housing price). 
It's a regression task, moreover its a multiple regression problem cause we use multiple features to make a preduction. 
It's a univariate regression since we trying to predict one value for each district. If it were to predict multiple value it would be a multivare regression. 

### Performance measure
[Ocena modeli][https://home.agh.edu.pl/~pszwed/wiki/lib/exe/fetch.php?media=med:med-w03.pdf]
*RMSE* - standardowy błąd regresji/estymaty
*MAE* - średni błąd regresji/estymaty

# Get the data

Download the data and then take a look at the data structure
atribute = column
Create a histogram look for capped data, look for values they are expressed

## **Create a test set**
Split the data into training and test sets

*Data snooping* bias occurs when a dataset is used more than once for model selection, training, or evaluation, leading to overly optimistic performance estimates and potentially misleading results. This bias arises from the leakage of information between the training and evaluation phases, which can inflate the apparent performance of a model.

Creating a test set involves setting aside a portion (typically 20%) of the dataset. While simply picking instances randomly works, it can lead to different test sets on each run, potentially exposing the entire dataset over time. To maintain consistency, you can save the test set after the first run or set a random seed to ensure the same shuffled indices. However, these methods fail if the dataset is updated. A more robust solution is using each instance's unique identifier to determine inclusion in the test set, ensuring stability even with refreshed datasets. This approach keeps the test set consistent across runs and updates.

Possible ways to split data: 

from zlib import crc32
def is_id_in_test_set(identifier, test_ratio):
return crc32(np.int64(identifier)) < test_ratio * 2**32
def split_data_with_id_hash(data, test_ratio, id_column):
ids = data[id_column]
in_test_set = ids.apply(lambda id_: is_id_in_test_set(id_, test_ratio))
return data.loc[~in_test_set], data.loc[in_test_set]

lub:

housing_with_id = housing.reset_index() # adds an `index` column
train_set, test_set = split_data_with_id_hash(housing_with_id, 0.2, "index")

lub:

housing_with_id["id"] = housing["longitude"] * 1000 + housing["latitude"]
train_set, test_set = split_data_with_id_hash(housing_with_id, 0.2, "id")

lub:

from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

Random sampling is generally fine for large datasets, but for smaller datasets, it can introduce significant sampling bias. To ensure a representative sample, stratified sampling is used, where the population is divided into homogeneous subgroups (strata), and instances are sampled from each stratum to match the population proportions. For example, in a survey, 51.1% females and 48.9% males should be included to reflect the US population accurately. If the median income is important for predicting housing prices, you need to create income categories, ensuring each stratum has enough instances to avoid bias.

# Explore and visualize the data

- Visualize geographical data
- Look for correlations
- Experiment with attribute combinations

Skewed-right distributions might require transformation logarithm or square root
Before preparing data for machine learning, consider creating new attribute combinations, such as rooms per household, bedrooms to rooms ratio, and population per household. These new attributes can provide more meaningful insights

# Prepare the Data for ML algorithm

Prepare your data for machine learning algorithms by writing functions for data transformation instead of doing it manually. This approach lets you easily reproduce transformations on any dataset, build a reusable library of functions, apply them in live systems, and experiment with different transformation combinations to find the best one.

- Data cleaning

Most machine learning algorithms can’t handle missing features, so you need to address them. For example, with missing values in the total_bedrooms attribute, you have three options:

Remove the affected districts.
Eliminate the attribute entirely.
Impute missing values by setting them to a specific value (e.g., zero, mean, median) its called *imputation*

- Handling Text and Categorical Attributes

One issue with representing categorical values numerically is that ML algorithms may assume that two nearby values are more similar than two distant values. This can be problematic for categories like ocean_proximity, where, for example, categories 0 and 4 are more similar than categories 0 and 1.
To address this, you can use one-hot encoding: create a binary attribute for each category. For instance, one attribute will be 1 for "<1H OCEAN" and 0 otherwise, another for "INLAND," and so on. This ensures that only one attribute is "hot" (1) at a time, while the others are "cold" (0).
Scikit-Learn's OneHotEncoder class can be used to convert categorical values into one-hot vectors.

A sparse matrix is ideal for matrices with mostly zeros, as it stores only nonzero values and their positions, saving memory and speeding up computations. When you one-hot encode a categorical attribute with many categories, the resulting matrix will be large and sparse, containing mostly zeros with a single 1 per row. Using a sparse matrix in this scenario is efficient.
You can work with a sparse matrix similarly to a 2D array. To convert it to a dense NumPy array, use the toarray() method.

- Feature Scalling and Transformation

Feature scaling is crucial in machine learning as algorithms often perform poorly when numerical attributes have different scales. For example, in housing data, the number of rooms ranges from about 6 to 39,320, while median incomes range from 0 to 15. Without scaling, models might ignore median income and focus more on the number of rooms.
To scale features, use one of these common methods:
- Min-Max Scaling: Rescales data to a fixed range, usually [0, 1].
- Standardization: Centers data around the mean with a unit variance

Standarization is less afected by outliners

If the target distribution has a heavy tail, you might replace the target with its logarithm. Consequently, the regression model will predict the log of the median house value, and you’ll need to compute the exponential of the model’s prediction to get the median house value.

A simpler option for transforming target values is to use a TransformedTargetRegressor. This approach involves constructing the regressor with the regression model and the label transformer, then fitting it on the training set with the original unscaled labels. It will automatically scale the labels, train the regression model on the scaled labels, and use the transformer to inverse-transform predictions.

# Custom Transformers

It’s often beneficial to transform features with heavy-tailed distributions by replacing them with their logarithm, assuming the feature is positive and the tail is on the right.

Although Scikit-Learn offers many useful transformers, you may need to create your own for custom transformations, cleanup tasks, or combining specific attributes.

FunctionTransformer is great for simple transformations, but for a trainable transformer that learns parameters in fit() and uses them in transform(), you need to create a custom class. This class should have fit(), transform(), and optionally fit_transform() methods. You can simplify this by inheriting from TransformerMixin for fit_transform() and from BaseEstimator for get_params() and set_params() methods, which help with hyperparameter tuning

Input Validation: Use functions from sklearn.utils.validation to validate inputs
fit() Arguments: Scikit-Learn requires the fit() method to have two arguments, X and y, even if y is not used
n_features_in_: All Scikit-Learn estimators set n_features_in_ in the fit() method to ensure consistency in transform() or predict()
Returning self: The fit() method must return self
Complete Implementation: Estimators should set feature_names_in_ when using a DataFrame and provide get_feature_names_out() and inverse_transform() methods if the transformation can be reversed

# Transformation Pipelines

Scikit-Learn's Pipeline class helps manage sequences of data transformations. For example, a pipeline for numerical attributes can first impute missing values and then scale the features.

The Pipeline constructor takes a list of name/estimator pairs (tuples) defining the sequence of steps. Names must be unique and not contain double underscores (__). The steps should be transformers (having fit_transform()), except the last one, which can be any estimator type (transformer, predictor, etc.).

It's time to create a single pipeline to perform all the necessary transformations. Here’s what the pipeline will do and why:
Impute Missing Values:
- Numerical Features: Replace missing values with the median to handle gaps, as most ML algorithms do not handle missing values well.
- Categorical Features: Replace missing values with the most frequent category.
One-Hot Encoding:
- Categorical Features: Convert categorical features into numerical format, since most ML algorithms only accept numerical inputs.
Compute Ratio Features:
- Additional Features: Compute ratios like bedrooms_ratio, rooms_per_house, and people_per_house to potentially find better correlations with the target variable.
Cluster Similarity Features:
- Geographical Features: Add cluster similarity features, which might be more informative than using latitude and longitude directly.
Log Transformation:
- Long-Tailed Features: Replace features with long-tailed distributions with their logarithm to create roughly uniform or Gaussian distributions.
Standardization:
- All Numerical Features: Scale all numerical features to ensure they have roughly the same scale, as most ML algorithms perform better under this condition.

# Select and Train Model

When a model underfits the training data, it indicates that the features may not provide enough information for accurate predictions or that the model isn't powerful enough. To address underfitting, you can choose a more powerful model, improve the features, or reduce model constraints. Since this model isn't regularized, reducing constraints isn't an option. You could add more features, but trying a more complex model first is a good approach.

You decide to try a DecisionTreeRegressor, a powerful model capable of finding complex nonlinear relationships in the data.

## Better Evaluation Using Cross-Validation

To evaluate the decision tree model, you can use train_test_split() to create a training and validation set, then train and evaluate the model. However, a better alternative is Scikit-Learn’s k-fold cross-validation. This method splits the training set into 10 non-overlapping folds, trains the model on 9 folds, and evaluates it on the remaining fold, repeating this process 10 times. The result is an array of evaluation scores

The decision tree model doesn't perform as well as initially thought, almost as poorly as the linear regression model. Cross-validation provides not only an estimate of the model's performance but also its precision (standard deviation). The decision tree has an RMSE of about 66,868 with a standard deviation of about 2,061. Linear regression has a mean RMSE of 69,858 and a standard deviation of 4,182. This minimal difference indicates severe overfitting, as shown by low training error and high validation error.

Next, try the RandomForestRegressor. Random forests train many decision trees on random subsets of features and average their predictions, boosting performance through this ensemble method.

Random forests perform much better with an RMSE of around 17,474 on the training set, indicating significant overfitting. To address this, you can simplify or regularize the model, or obtain more training data. Before focusing more on random forests, try various other models (e.g., support vector machines with different kernels, or a neural network) without extensive hyperparameter tuning. The objective is to shortlist a few promising models (two to five) for further exploration

# Fine-Tune your Model

## Grid Search

One option would be to fiddle with the hyperparameters manually, until you find a great combination of hyperparameter values. This would be verytedious work, and you may not have time to explore many combinations.
Instead of manually tuning hyperparameters, you can use Scikit-Learn's GridSearchCV class to automate this process. Simply specify the hyperparameters and their possible values, and GridSearchCV will use cross-validation to evaluate all combinations

## Randomized search

When dealing with a large hyperparameter search space, RandomizedSearchCV is often more efficient than GridSearchCV. Instead of testing all possible combinations, it evaluates a fixed number of random combinations. This has several advantages:

Greater Exploration: For continuous or high-dimensional discrete hyperparameters, random search can explore a wide range of values, while grid search is limited to the predefined list.
Efficiency with Irrelevant Hyperparameters: If a hyperparameter has little effect, grid search still tests all its values, increasing training time. Random search, however, can bypass this inefficiency.
Flexibility in Search Scope: With many hyperparameters, grid search may become impractical due to the exponential growth in combinations. Random search can run for a set number of iterations regardless of the number of hyperparameters.

## Ensemble Methods
Another way to improve your model is to combine the best-performing models into an ensemble. This group of models often outperforms any individual model, as the ensemble can mitigate different types of errors made by each model. For instance, you could train and fine-tune a k-nearest neighbors model and then create an ensemble model that predicts the mean of the random forest prediction and the k-nearest neighbors prediction.

## Analyzing the Best Models and Their Errors

Inspecting the best models can provide valuable insights into your problem. For example, the RandomForestRegressor can indicate the relative importance of each attribute for making accurate predictions. With this information, you might try dropping some less useful features. For instance, if only one ocean_proximity category is significant, you could drop the others.

Additionally, analyze the specific errors your model makes to understand why they occur and how to fix them. This might involve adding new features, removing uninformative ones, or cleaning up outliers.

It's also crucial to ensure your model works well across all categories of districts, such as rural vs. urban, rich vs. poor, and so on. Creating subsets of your validation set for each category takes effort but is essential. If your model performs poorly on a specific category, you might need to address this issue before deployment or avoid using the model for predictions in that category to prevent potential harm.

## Evaluate on Test Set

After refining your models, evaluate the final model on the test set by making predictions and assessing them. To check if the improvement is significant, compute a 95% confidence interval for the generalization error.

Note that hyperparameter tuning might cause the model to perform slightly worse on new data than on the validation set. Avoid adjusting hyperparameters solely to improve test set performance, as this might not generalize well.

In the prelaunch phase, present your findings clearly, document your work, and create visualizations that highlight key insights. Even if the model's performance is only slightly better than expert estimates, it could still be valuable if it allows experts to focus on other tasks.

# Launch, Monitor, and Maintain Your System
Deployment:
Polish Your Solution: Refine your code, write documentation, and create tests.
Save and Transfer Model: Use joblib to save your trained model and transfer it to the production environment.
Load and Use Model: Import necessary classes, load the model, and use it for predictions. For web applications, integrate the model via REST API or direct model calls.

Options for Deployment:
Web Service: Deploy as a web service for easy version upgrades and scaling.
Cloud Deployment: Use services like Google’s Vertex AI to handle scaling and load balancing.

Monitoring:
Performance Tracking: Regularly monitor model performance and set up alerts for significant drops.
Assess Model Drift: Check if performance degradation is due to outdated data or other issues.
Human Analysis: For certain applications, use human raters to review model predictions and provide feedback.

Automation:
Data Collection: Automate data collection and labeling.
Training Scripts: Create scripts to train and fine-tune the model regularly.
Model Evaluation: Automate evaluation and deployment of new models based on performance metrics.

Input Data Quality:
Monitor the quality of input data to catch issues early, such as missing features or unexpected data distribution changes.

Backup and Rollback:
Maintain backups of models and datasets. Ensure you can quickly roll back to previous versions if necessary.

Infrastructure:
Machine learning projects require significant infrastructure. Once established, future deployments will be quicker and more efficient.

# Summary
Pipeline: A structured sequence of data processing steps.
Supervised Learning: Training with labeled examples.
Regression Task: Predicting continuous values.
Multiple Regression: Using multiple features for prediction.
Univariate Regression: Predicting a single value for each instance.
Multivariate regression: Predicting multiple outcome variables based on multiple predictor variables.

TIP: For more advanced imputation methods, you can use the sklearn.impute package:
KNNImputer: Replaces missing values with the mean of the k-nearest neighbors' values, using distances based on all available features.
IterativeImputer: Uses a regression model to predict missing values based on other features, iteratively refining the model and imputed values.

Scikit-Learn Design Principles:
- Consistency: Scikit-Learn features a simple and consistent interface across its objects.
- Estimators: Any object that estimates parameters from a dataset is an estimator (e.g., SimpleImputer). Estimation is done via the fit() method, with hyperparameters set as instance variables.
- Transformers: Some estimators can also transform data (e.g., SimpleImputer). Transformation is done using the transform() method, and the fit_transform() method combines fit() and transform(), often with improved performance.
- Predictors: Estimators that make predictions (e.g., LinearRegression) use the predict() method and can assess prediction quality with score().
- Inspection: Hyperparameters are accessible via public instance variables (e.g., imputer.strategy), and learned parameters via public instance variables with an underscore suffix (e.g., imputer.statistics_).
- Nonproliferation of Classes: Datasets are handled as NumPy arrays or SciPy sparse matrices, and hyperparameters are standard Python types.
- Composition: Reuses existing components, such as creating a Pipeline from a sequence of transformers and a final estimator.
- Sensible Defaults: Provides reasonable default values for most parameters, facilitating quick baseline setups.


TIP: For categorical attributes with many categories (e.g., country code, profession), one-hot encoding can create a large number of features, potentially slowing down training and degrading performance. Instead, consider:
- Using Numerical Features: Replace the categorical feature with related numerical features (e.g., replace ocean_proximity with distance to the ocean or country code with population and GDP).
- Using Alternative Encoders: Utilize encoders from the category_encoders package on (GitHub)[https://github.com/scikit-learn-contrib/category_encoders].
- Using Embeddings: In neural networks, replace each category with a learnable, low-dimensional vector (embedding). This is a form of representation learning

WARNING: Fit scalers only to the training data using fit() or fit_transform(). After fitting, use the scaler to transform() the validation set, test set, and new data. If new data contains outliers, they might be scaled outside the range. To prevent this, set the clip hyperparameter to True.

