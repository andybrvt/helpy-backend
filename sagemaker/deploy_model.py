import sagemaker
from sagemaker.tensorflow import TensorFlowModel
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the model path and role from .env
model_data = os.getenv('MODEL_DATA')
role = os.getenv('AWS_SAGEMAKER_ROLE')


# Create the TensorFlow model from the saved model in S3
model = TensorFlowModel(
    model_data=model_data,
    role=role,
    framework_version='2.4',  # Make sure this matches your TensorFlow version
)

# Deploy the model to a SageMaker endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.large'  # You can adjust based on your needs
)

# Optionally, you can now use the predictor to make real-time predictions
test_input = ["I need help getting out of bed."]
prediction = predictor.predict(test_input)
print(prediction)
