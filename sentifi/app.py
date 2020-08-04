import streamlit as st
import pandas as pd
from twython import Twython
from classifier.model import  get_model
from PIL import Image
import json
from dateutil.parser import parse
import plotly.express as px
from geopy.geocoders import Nominatim

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
            ('Let me write some text', 'Get some Tweets')
        )

    EMOJIS_MAP = {
            'positive' : ':smile:',
            'neutral' : ':expressionless:',
            'negative' : ':rage:'
        }

    if option != 'Get some Tweets' :
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
        result_type = st.radio(
            'Result type',
            ('Recent', 'Popular')
        )
        fetch_tweets = st.button('Go')

        if fetch_tweets :
            query = {'q': twitter_keywords,
                    'result_type' : result_type,
                    'count':number_tweets,
                    'lang': 'fi',
                    }
            percent_complete = 0
            my_bar = st.progress(percent_complete)
            with st.spinner('Fetching tweets...'): 
                dict_ = { 'date': [], 'text': [], 'location':[], 'sentiment': [], 'confidence' : [], 'latitude':[], 'longitude':[]}
                geolocator = Nominatim(user_agent="sentifi")

                for status in python_tweets.search(**query)['statuses']:
                    percent_complete +=1
                    my_bar.progress(int((percent_complete / number_tweets)*100))
                    dict_['date'].append(parse(status['created_at']))
                    dict_['text'].append(status['text'])
                    dict_['location'].append(status['user']['location'].lower())
                    print('getting coords')
                    location = geolocator.geocode(status['user']['location'].lower())
                    print(location)
                    if location:
                        dict_['latitude'].append(location.latitude)
                        dict_['longitude'].append(location.longitude)
                    else :
                        dict_['latitude'].append(0)
                        dict_['longitude'].append(0)
           

                    results = predict(status['text'])
                    dict_['sentiment'].append(results["sentiment"])
                    dict_['confidence'].append(results["confidence"])
                    
                df = pd.DataFrame(dict_)
            st.markdown("***")
            st.text(f'Sentiment Analysis Summary')
            fig = px.pie(df, names='sentiment', color_discrete_map={'negative':'red', 'positive':'green', 'neutral':'blue'})
            st.write(fig) 
            st.map(df)
            for idx, row in df.iterrows():
                st.markdown("***")        
                st.markdown(row['text'])
                st.markdown(row['date'])
                st.markdown(f'{EMOJIS_MAP[row["sentiment"]]} {row["sentiment"]} with a confidence of {int(row["confidence"]*100)}%')

