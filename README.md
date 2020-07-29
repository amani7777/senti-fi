# Finnish Sentiment Analysis using BERT and Transformers using PyTorch
The project contains two ways to perform sentiment analysis, via REST API or via a web app.
First, download the trained model from my Drive by running the follwowing command:

```
python bin/download_model.py
```
then install the necessary requirements:
```
pip install -r requirements.txt
```

## REST API
The classifier is doplyed as an API which is built using FastApi and Uvicorn. to give a try, run ;

```
uvicorn sentiment_analyzer.api:app
```

## Streamlit app
The classifier can be test by interacting with a simple app built using Streamlit:

```
streamlit run sentiment_analyzer/app.py
```


***

Special Thanks to [Venelin Valkov](https://github.com/curiousily) for the amazing BERT tutorials.
