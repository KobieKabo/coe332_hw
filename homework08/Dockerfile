FROM python:3.8.10

RUN pip install Flask==2.2.0 redis requests
RUN pip install matplotlib==3.7.1

ADD ./gene_api.py /gene_api.py

CMD ["python3", "/gene_api.py"]
