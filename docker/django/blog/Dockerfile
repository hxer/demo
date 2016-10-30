FROM ubuntu
MAINTAINER janes

RUN apt-get update \
    && apt-get install -y \
        python-dev \
        python-pip \
    && apt-get build-dep -y \
        python-imaging  # for PIL

RUN pip install Pillow
RUN pip install django==1.8.7

COPY ./code/ /root/blog/

EXPOSE 8000

WORKDIR /root/blog/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
