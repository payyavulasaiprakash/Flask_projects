import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from PIL import Image
import tensorflow as tf
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MODEL_PATH'] = 'model.h5'

# Configure the app to serve static files
app.static_folder = 'static'

# Load the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Preprocess the data
x_train = x_train / 255.0
x_test = x_test / 255.0

# Reshape the data
x_train = np.reshape(x_train, (-1, 28, 28, 1))
x_test = np.reshape(x_test, (-1, 28, 28, 1))

# Create the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Check if a pre-trained model exists
if os.path.exists(app.config['MODEL_PATH']):
    # Load the pre-trained model
    model = tf.keras.models.load_model(app.config['MODEL_PATH'])
else:
    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

    # Save the trained model
    model.save(app.config['MODEL_PATH'])

model.summary()

def preprocess_image(image_path):
    image = Image.open(image_path).convert('L')
    image = image.resize((28, 28))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=2)
    return image.reshape(1, 28, 28, 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the uploaded image file
        image_file = request.files['image']
        
        # Save the image file
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
        
        # Preprocess the image
        image = preprocess_image(image_path)
        
        # Make a prediction
        prediction = model.predict(image)
        # predicted_digit = prediction.tolist()
        predicted_digit = np.argmax(prediction)
        # Encode the image to base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Remove the saved image file
        os.remove(image_path)
        
        # Return the prediction and image data
        return jsonify({'prediction': str(predicted_digit), 'image_data': image_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True,port=3000)