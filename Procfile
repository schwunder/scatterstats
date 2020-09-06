web: python -m spacy download en_core_web_md && python -m spacy link en_core_web_md en
web: uvicorn main:app --reload --host=0.0.0.0 --port=${PORT:-5000}
