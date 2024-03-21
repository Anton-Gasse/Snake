FROM python:3.10

Workdir /snake

copy ./backend/requirements.txt .

#RUN pip3 install -r requirements.txt

RUN pip3 install flask && \
  pip3 install flask-cors && \
  pip3 install cryptography && \
  pip install torch && \
  pip3 install stable-baselines3 && \
  pip3 install gunicorn

copy . .

Expose 443

#CMD python3 -m gunicorn --certfile=backend/ssl_keys/server.pem --keyfile=backend/ssl_keys/key.pem -b 0.0.0.0:443 backend.app:app
CMD python3 ./backend/app.py