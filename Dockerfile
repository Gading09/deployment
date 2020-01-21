FROM python:3.6.5
MAINTAINER Your Name "hedy@alterra.id"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirement.txt
WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

