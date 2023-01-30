# # For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9

# EXPOSE 8081

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /code/ui

COPY ./requirements.txt /code/ui/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/ui/requirements.txt

COPY ./app /code/ui/app

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8081", "--log-level", "debug"]