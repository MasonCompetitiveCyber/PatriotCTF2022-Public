FROM python
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . . 
EXPOSE 5000

RUN python db.py
CMD ["python", "main.py"]

