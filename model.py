import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf

# Load the saved model
model = tf.keras.models.load_model('heart_disease_model.h5')

# Optional: Verify the model by checking its summary
model.summary()
