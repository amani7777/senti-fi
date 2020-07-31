import streamlit as st
import pandas as pd
from twython import Twython
from classifier.model import  get_model
from PIL import Image
import json
from dateutil.parser import parse


model = get_model()

def predict(sentence):
    sentiment, confidence, probabilities = model.predict(sentence)
    return {
        'sentiment':sentiment, 'confidence':probabilities[sentiment], 'probabilities':probabilities
    }



   

if __name__ == "__main__":

    image = Image.open('././static/fin-flag.png')
    st.sidebar.image(image)
    st.sidebar.markdown(":smile: :expressionless: :rage:  ")
    st.sidebar.title('Welcome to Sentifi!')
    st.markdown('## Finnish Sentiment Analysis using FinBERT and Transformers with PyTorch.')

    option = st.sidebar.radio(
            'How would you like to perform sentiment analysis ?',
            ('Let me write some text', 'Tweets')
        )

    EMOJIS_MAP = {
            'positive' : ':smile:',
            'neutral' : ':expressionless:',
            'negative' : ':rage:'
        }

    if option != 'Tweets' :
        txt = st.text_area('Text to analyze', '''Oikein hyvä''')

        if st.button('Analyze'):
            with st.spinner('Analyzing sentiment ...'):
                results = predict(txt)
                st.markdown(f'# {EMOJIS_MAP[results["sentiment"]]} {results["sentiment"]} with a confidence of {int(results["confidence"]*100)}%')
    
    else :
        
        with open("./twitter/twitter_credentials.json", "r") as file:
            creds = json.load(file)

        print(creds)
        python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        twitter_keywords =  st.text_input('Twitter keywords')
        number_tweets =  st.number_input('Number of Tweets')
        fetch_tweets = st.button('Go')
        percent_complete = 0
        my_bar = st.progress(percent_complete)
        if fetch_tweets :
            query = {'q': twitter_keywords,
                    'result_type' : 'recent',
                    'lang': 'fi',
                    }
  

            with st.spinner('Fetching tweets...'): 
                dict_ = { 'date': [], 'text': [], 'sentiment': [], 'confidence' : []}
                for status in python_tweets.search(**query)['statuses']:
                    date = parse(status['created_at'])
                    text = status['text']
                    dict_['date'].append(date)
                    dict_['text'].append(text)
                    results = predict(text)
                    dict_['sentiment'].append(results["sentiment"])
                    dict_['confidence'].append(int(results["confidence"]*100))
                    
                    st.markdown(text)
                    st.markdown(f'{date}')
                    st.markdown(f'{EMOJIS_MAP[results["sentiment"]]} {results["sentiment"]} with a confidence of {int(results["confidence"]*100)}%')
                    st.markdown('***')
                df = pd.DataFrame(dict_)
            st.dataframe(df)    
            st.sidebar.markdown("***")        
            st.sidebar.text(f'Total Tweets: {len(df)}')
            st.sidebar.text(df.sentiment.value_counts().to_dict())
