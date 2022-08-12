FROM python:3-alpine
WORKDIR /app
ENV FLASK_APP=/app/src/app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH=/app/src:$PYTHONPATH
RUN apk add --no-cache gcc musl-dev linux-headers
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
