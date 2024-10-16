import tensorflow as tf
import pandas as pd
import boto3
from io import StringIO
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

def load_data_from_s3(bucket_name, file_key):
    """Load CSV data from S3"""
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    return data

def train_model():
    # Load the data from S3
    bucket_name = 'helpy-ai-training-data'
    file_key = 'cleaned_nlm_data.csv'
    data = load_data_from_s3(bucket_name, file_key)

    # Strip spaces from column names
    data.columns = data.columns.str.strip()

    # Split features and labels
    X = data['Request'].values  # Your input text (requests)
    y_task_type = data['task_type'].values  # Convert to NumPy array
    y_emergency = data['Emergency'].values  # Convert to NumPy array

    # Preprocess the text (convert text to numerical data)
    max_tokens = 20000
    output_sequence_length = 100
    vectorize_layer = TextVectorization(max_tokens=max_tokens, output_mode='int', output_sequence_length=output_sequence_length)
    vectorize_layer.adapt(X)
    X_vectorized = vectorize_layer(X)

    # Convert labels to numerical form (if necessary)
    y_task_type = tf.convert_to_tensor(y_task_type)
    y_emergency = tf.convert_to_tensor(y_emergency)

    # Define a multi-output model
    inputs = tf.keras.Input(shape=(None,), dtype="int64")

    embedding = tf.keras.layers.Embedding(input_dim=max_tokens, output_dim=128)(inputs)
    pooling = tf.keras.layers.GlobalAveragePooling1D()(embedding)
    dense_1 = tf.keras.layers.Dense(128, activation='relu')(pooling)
    dense_2 = tf.keras.layers.Dense(64, activation='relu')(dense_1)

    # Two output layers (multi-output)
    task_type_output = tf.keras.layers.Dense(30, activation='softmax', name='task_type_output')(dense_2)
    emergency_output = tf.keras.layers.Dense(5, activation='softmax', name='emergency_output')(dense_2)

    # Create the model with inputs and both outputs
    model = tf.keras.Model(inputs=inputs, outputs=[task_type_output, emergency_output])

    # Compile the model
    model.compile(optimizer='adam', 
                  loss={'task_type_output': 'sparse_categorical_crossentropy', 'emergency_output': 'sparse_categorical_crossentropy'},
                  metrics=['accuracy'])

    # Print model summary
    model.summary()

    # Train the model with both labels
    model.fit(X_vectorized, {'task_type_output': y_task_type, 'emergency_output': y_emergency}, epochs=5)

    # Save the model to the path that SageMaker expects
    model.save('/opt/ml/model')

if __name__ == '__main__':
    train_model()
