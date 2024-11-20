FROM python:3.10.15-bookworm
LABEL authors="itzikreuven"



ADD /users .
ADD ../utils /utils/

# Install any necessary dependencies
RUN apt-get update && \
    apt-get install -y zip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

CMD ["python", "users.py"]