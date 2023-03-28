FROM python:3.8.10

RUN pip install Flask==2.2.0 redis requests

ADD ./gene_api.py /gene_api.py

CMD ["python", "gene_api.py"]
