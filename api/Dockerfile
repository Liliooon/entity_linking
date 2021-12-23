FROM python:3.7-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install torch==1.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install sentencepiece==0.1.96
RUN python -c "from transfomers import pipeline; import settings; p = pipeline('token-classification', model=settings.ner_model_id)"

COPY . .

CMD [ "python", "./main.py" ]
