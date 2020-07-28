release: python bin/download_model.py
web: uvicorn sentiment_analyzer.api:app --host=0.0.0.0 --port=${PORT:-5000}


