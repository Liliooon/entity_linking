FROM python:3-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install torch==1.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
