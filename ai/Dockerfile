# # For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9

# EXPOSE 8083

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /code/ai

COPY ./requirements.txt /code/ai/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/ai/requirements.txt

COPY . .

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8083", "--log-level", "debug"]