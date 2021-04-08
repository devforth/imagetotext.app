
Deployed application: [imagetotext.app/](https://imagetotext.app/)

Text extraction is based on hint: [How to extract text from image in Python](https://hinty.io/vserhiyev/how-to-extract-text-from-image-in-python/) If you have any questions, please ask in comments under hint.
# How to self-host it

This repo holds a `Dockerfile` with all needed (Correct version of Python and all dependencies which are managed via Pipenv).

Example of instantiation, e.g. Docker Compose:

```

services:
  imagetotext:
    network_mode: host
    build: <path_to_this_repo>
    command: /bin/bash -c "cd /code/ && pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8314 --workers 6"
    restart: always

```

Then you can use `http://<ip_of_server>:8314` or use any proxy server to route requests to port 8314, e.g. Nginx:



```
# imagetotext.app
server {
    server_name imagetotext.app;
    listen 80;
    
    listen 443 ssl;
    ssl_certificate /etc/ssl/cert/$CERT_NAME.crt;
    ssl_certificate_key /etc/ssl/cert/$CERT_NAME.key;

    charset utf-8;
    client_max_body_size 75M;

    location / {
        proxy_set_header Authorization "";
        proxy_connect_timeout 400s;
        proxy_read_timeout 400s;
        proxy_set_header X-Forwarded-For $$proxy_add_x_forwarded_for;
        proxy_set_header Host $$http_host;
        proxy_redirect off;
        
        proxy_buffers 128 8k; 
        proxy_buffer_size 16k;

        proxy_pass http://127.0.0.1:8314;

        add_header Last-Modified $$date_gmt;
        etag off;
    }
}
```




# Run dev autorelaod server locally

Tested on Ubuntu 20.04 (Native and [WSL 2](https://hinty.io/ivictbor/simple-way-to-docker-on-windows-10-home-with-wsl-2/)):

1\. Install deps


```
apt install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
```

>  ⚠ Do this before `pipenv sync`


Tesseract should have version `4.1.1+`.

2\. Then enter a repo dir and do:

```
pipenv sync
```

3\. Run app:

```
pipenv run uvicorn main:app --reload
```

# Testing and troubleshooting

👷‍♂️ To fix any exception produced by python code use [fixexception.com](http://fixexception.com/) – works very well 💪

```
curl -d '{"base64":"baeldung"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/upload/
```

Or paste same JSON in `testreq.json` file and run:

```
curl -d @testreq.json -H 'Content-Type: application/json' http://127.0.0.1:8000/upload/
```

To test only tesseract on your computer:

```
tesseract `absolute path to any image with text (/home/ykorolikhin/Pictures/test_text.png)` stdout 
```








