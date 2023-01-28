# # For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9

EXPOSE 8081

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# # -------------------------------------------------------------------------#
# # DEV MODE
# # -------------------------------------------------------------------------#

# # TODO: handle this with an environment variable and a flag you savage
# # -------------------------------------------------------------------------#
# # END DEV MODE
# # -------------------------------------------------------------------------#

COPY ./app /code/app

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8081", "--log-level", "debug"]