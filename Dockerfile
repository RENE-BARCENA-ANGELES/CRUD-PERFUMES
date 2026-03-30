FROM python:3.13.2-alpine3.21
#RUN addgroup flask && adduser -S -G flask flask
#USER flask
WORKDIR /app/
COPY --chown=flask requirements.txt .
RUN pip install -r requirements.txt
COPY --chown=flask . .
EXPOSE 5000
CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]