import streamlit as st
import pandas as pd

from classifier.model import  Model, get_model
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
    st.title('Finnish sentiment analysis')
    st.write('Finnish sentiment detection using finetuned BERT.')
    txt = st.text_area('Text to analyze', '''Hyvaaaaaaaaaaaaa''')
    if st.button('Analyze'):
        with st.spinner('Analyzing sentiment ...'):
            st.write('Sentiment:', predict(txt))
    else:
        st.write('Waiting for text to analyze')

    
