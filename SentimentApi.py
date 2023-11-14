from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


def analyse_sentiment(sentence):
    tweet=sentence
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)

    # load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    

    # sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores

@app.route("/analyze/<text>")
def analyzeText(text):
    scores = analyse_sentiment(text)
    string_array = [str(num) for num in scores ]
    result_string = ''.join(string_array)
    print()
    print(text, scores[0])
    print()
    if scores[0]:
        return jsonify("sample text")
    else:
        return jsonify("sample text")
    #return result_string

@app.route("/analyze2", methods=['POST'])
def analyzeText2():
    content = request.json
    text = content['text']
    scores = analyse_sentiment(text)
    string_array = [str(num) for num in scores]
    result_string = ''.join(string_array)
    print()
    print(text,scores[0])
    print()
    if scores[0]>0.5:
        return jsonify({"modifiedText": "-"*(len(text)-1)})
    else:
        return jsonify({"modifiedText": text})
    return jsonify({"modifiedText": result_string})



@app.route("/")
def homePage():
    return "home"

@app.route("/echo/<sound>")
def echoing(sound):
    return sound

if __name__ == "__main__":
    app.run(debug=True)