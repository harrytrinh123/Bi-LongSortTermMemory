import json

from gensim.utils import simple_preprocess
from underthesea import word_tokenize
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Model

word2id = None
label2id = {
    "tiêu cực": 0,
    "trung tính": 1,
    "tích cực": 2
}
id2label = {v: k for k, v in label2id.items()}
stopwords = None
max_words = None


def create_stopwords(path):
    original_stopwords = ["tiki"]
    with open(path, encoding="utf-8") as words:
        return [w[:len(w) - 1] for w in words] + original_stopwords


def load_stopword():
    global stopwords
    if stopwords is None:
        stopwords = create_stopwords('vietnamese-stopwords-dash.txt')


def load_word_index():
    global word2id, max_words
    if word2id is None and max_words is None:
        with open("dictionary.json", encoding="utf-8") as file:
            payload = json.loads(file.read())
            word2id = payload["dictionary"]
            max_words = int(payload["max_word"])


def word_processing(sentence):
    # Lazy load stopword
    load_stopword()

    sentence = " ".join(simple_preprocess(sentence))
    sentence = [word for word in word_tokenize(
        sentence.lower(), format="text").split() if word not in stopwords]

    # remove coutinues duplicated
    sentence = [v for i, v in enumerate(
        sentence) if i == 0 or v != sentence[i-1]]

    positions = []
    filter_word = ("không", "chẳng", "chả", "đếch", "chưa", "kém",
                   "khỏi", "không_thể", "tạm", "khó", "dễ", "nên")
    # Find không, chẳng in line
    for index, word in enumerate(sentence):
        if word in filter_word:
            positions.append(index)
    for i in positions:
        if i != len(sentence) - 1:
            sentence = sentence[:i] + \
                ['_'.join(sentence[i:i+2])] + [""] + sentence[i+2:]

    return [word for word in sentence if word != ""]


def predict_on_text(text, model: Model):
    # Lazy load word_index
    load_word_index()

    # Word Processing
    tokenized_text = word_processing(text)

    # Encode samples
    encoded_text = [[word2id.get(word.lower(), 0) for word in tokenized_text]]

    # Padding
    encoded_text = pad_sequences(encoded_text, maxlen=max_words)

    # Make predictions
    label_probs, attentions = model.predict(encoded_text)
    label_probs = {id2label[_id]: float(prob) for (
        label, _id), prob in zip(label2id.items(), label_probs[0])}

    return label_probs
