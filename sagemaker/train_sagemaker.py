import sagemaker
from sagemaker.tensorflow import TensorFlow
from sagemaker import get_execution_role
import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# this is for the training set up, tells which s3 is getting used and which training model is getting sued

# Get the SageMaker role (you can use the default role or pass in your custom role)

# Get the SageMaker role from .env
role = os.getenv('AWS_SAGEMAKER_ROLE')



# Define the TensorFlow estimator
tf_estimator = TensorFlow(
    entry_point='train.py',   # This is the model training script you'll create next
    role=role,
    instance_count=1,         # Number of instances to run the job
    instance_type='ml.m5.large',  # Instance type for training (can be changed to larger if needed)
    framework_version='2.4',  # TensorFlow version
    py_version='py37',        # Python version
    hyperparameters={'epochs': 5},  # Example of passing hyperparameters
)

# Input data (path to your S3 bucket with the cleaned CSV file)
train_input = 's3://helpy-ai-training-data/cleaned_nlm_data.csv'  # Replace with your S3 path to the CSV

# Launch the training job
tf_estimator.fit({'train': train_input})
 