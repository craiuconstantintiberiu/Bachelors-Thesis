FROM python:3.10.4-slim-buster
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONPATH .
EXPOSE 5000
CMD python dysplasia_classification/UI.py