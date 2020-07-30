import streamlit as st
import pandas as pd

from classifier.model import  get_model
from PIL import Image


model = get_model()

def predict(sentence):
    sentiment, confidence, probabilities = model.predict(sentence)
    return {
        'sentiment':sentiment, 'confidence':probabilities[sentiment], 'probabilities':probabilities
    }



   

if __name__ == "__main__":

    image = Image.open('././static/fin-flag.png')
    st.image(image)
    st.markdown(":smile: :expressionless: :rage:  ")
    st.title('Sentifi : Finnish sentiment analysis app')
    st.write('Finnish Sentiment Analysis using FinBERT and Transformers with PyTorch.')
    txt = st.text_area('Text to analyze', '''Oikein hyvä''')
    EMOJIS_MAP = {
        'positive' : ':smile:',
        'neutral' : ':expressionless:',
        'negative' : ':rage:'

    }
    if st.button('Analyze'):
        with st.spinner('Analyzing sentiment ...'):
            results = predict(txt)
            st.markdown(f'# {EMOJIS_MAP[results["sentiment"]]} {results["sentiment"]} with a confidence of {int(results["confidence"]*100)}%')
    

    
