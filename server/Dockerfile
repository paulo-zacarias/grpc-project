FROM python:3.7.12-slim-buster

WORKDIR /server

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/chat_app.proto

EXPOSE 50051

CMD ["server.py"]
ENTRYPOINT [ "python"]