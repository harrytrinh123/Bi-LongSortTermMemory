import re
import datetime
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras import Model
from predit_helper import predict_on_text

init_model = load_model("model_0.13501.h5")
# init_model.summary()
model = Model(
    inputs=init_model.input,
    outputs=[
        init_model.output,
        init_model.get_layer('attention_weight').output
    ]
)

# print(predict_on_text("trang web của bạn rất hay", model))
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/predict", methods=["POST"])
def predict():
    print(request.json)
    text = request.json["text"]
    probs = predict_on_text(text, model)
    return jsonify({
        "text": text,
        "probabilities": probs
    })

if __name__ == "__main__":
    app.run()