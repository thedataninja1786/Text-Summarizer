import string 
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
from flask_ngrok import run_with_ngrok
from flask_ngrok import run_with_ngrok
import datetime
from flask import Flask, render_template , request 

stop_words_en = stopwords.words('english')
stop_words_gr = stopwords.words('greek')
stop_words = stop_words_en + stop_words_gr 
stop_words = set(stop_words)

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('Summarizer_2.html')

@app.route('/summary', methods = ['POST'])
def summary():
  data = request.form['input']

  punctuations = string.punctuation
  frequency_dict = {}

  for sentence in data.split('.'):
    for word in sentence.split():
      if word not in stop_words and word not in punctuations:
        word = word.lower()
        if word not in frequency_dict.keys():
          frequency_dict[word] = 1 
        else:
          frequency_dict[word] += 1 

  max_frequncy = max(frequency_dict.values())

  #Standardize to get the score of each word
  for word in frequency_dict.keys():
    frequency_dict[word] = round(frequency_dict[word] / max_frequncy,3)

  #Returns the score of each sentence
  sentence_score = []
  for sentence in data.split('.'):
    score =  0 
    for word in sentence.split():
      word = word.lower()
      if word in frequency_dict.keys() and word not in "''":
        score += frequency_dict[word]
    sentence_score.append([sentence,score])

  sentence_num = 4 #sentences included in the summary 
  sorted_arr = sorted(sentence_score,key=lambda x: x[1],reverse=True)[:sentence_num] #returns the top n sentences 
  output = [elem for elem in sentence_score if elem in sorted_arr] #returns the element in the original order

  def summarize(summary):
    ds = []
    for i in summary:
      ds.append(i[0])
    ds = ".".join(ds) + "."
    return ds 

  summary = summarize(output)

  return render_template('Summarizer_2.html',data = summary)

if __name__ == '__main__':
  app.run()
