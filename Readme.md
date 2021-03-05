test server post method 

curl -d '{"base64":"baeldung"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/upload/




curl -d @testreq.json -H 'Content-Type: application/json' http://127.0.0.1:8000/upload/
runserver uvicorn main:app --reload