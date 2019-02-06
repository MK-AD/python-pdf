FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# install pip modules (own filesystem layer)
COPY src/app/requirements.txt /src/app/requirements.txt
RUN pip install -r /src/app/requirements.txt

# copy our app
COPY src /src

# some info for the callers
EXPOSE 80
WORKDIR "/src/app"

# run our service
CMD ["python","/src/app/main.py"]

