FROM python:3.9

EXPOSE 5007

WORKDIR /manejoIncidentes

COPY . /manejoIncidentes/

RUN pip install pipenv && pipenv install

ENV PYTHONPATH /manejoIncidentes

ENTRYPOINT ["pipenv", "run", "python", "./src/main.py"]