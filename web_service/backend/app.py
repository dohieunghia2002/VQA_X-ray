from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import request

import torch
from transformers import BlipForQuestionAnswering, BlipProcessor, BlipImageProcessor
from PIL import Image
import numpy as np

# Load the model and processor
model_checkpoint_path = 'BLIP.pth'  # Specify the path to your checkpoint
text_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
image_processor = BlipImageProcessor.from_pretrained("Salesforce/blip-vqa-base")

# Create the model and load the checkpoint
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
checkpoint = torch.load(model_checkpoint_path, map_location='cpu')
model.load_state_dict(checkpoint)

def generate_answer(image, question_text):
    global text_processor
    global image_processor
    global model

    # Preprocess the image
    image_encoding = image_processor(image, do_resize=True, size=(128, 128), return_tensors="pt")

    # Tokenize and preprocess the question
    encoding = text_processor(
        None,
        question_text,
        padding="max_length",
        truncation=True,
        max_length=32,
        return_tensors="pt"
    )
    encoding["pixel_values"] = image_encoding["pixel_values"]

    # print("inpt_ids",len(encoding["input_ids"]))
    # print("pxl",len(encoding["pixel_values"]))

    # Forward pass to generate answer
    with torch.no_grad():
        outputs = model.generate(input_ids=encoding['input_ids'], pixel_values=image_encoding['pixel_values'])

    # Decode the predicted answer
    predicted_answer = text_processor.decode(outputs[0], skip_special_tokens=True)

    return predicted_answer


app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/predict', methods=['POST'])
@cross_origin(origins='*')
def predict():
    file = request.files['file']
    image = Image.open(file).convert('RGB')

    question_text = request.form['question']
    answer = generate_answer(image, question_text)

    return jsonify({
        'answer': answer
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9999')