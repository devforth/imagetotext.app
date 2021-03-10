
Demo: ![https://imagetotext.app/](https://imagetotext.app/)

# test backend

```
curl -d '{"base64":"baeldung"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/upload/
```

Or paste json in `testreq.json` file

```
curl -d @testreq.json -H 'Content-Type: application/json' http://127.0.0.1:8000/upload/
pipenv run uvicorn main:app --reload
apt-get install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
```
