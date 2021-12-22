FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk add --update npm

COPY package.json ./
COPY package-lock.json ./
RUN npm install 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]
