FROM python:3.11.5
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./plotly-dash-frontend /code/plotly-dash-frontend
EXPOSE 8050
CMD ["python", "/code/plotly-dash-frontend/index.py"]


CMD ["gunicorn", "index:server", "--bind", "0.0.0.0:8080"]

