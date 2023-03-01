FROM python:3.8

ARG work_dir=/var/www
RUN mkdir ${work_dir}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR ${work_dir}

COPY ./requirements.txt ${work_dir}/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev default-libmysqlclient-dev &&\
    pip install --upgrade pip &&\
    pip install -r requirements.txt &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./backend ${work_dir}
RUN groupadd -g 1000 www
RUN useradd -u 1000 -ms /bin/bash -g www www

# Copy existing application directory permissions
COPY --chown=www:www . ${work_dir}

CMD [ "gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--reload" ]