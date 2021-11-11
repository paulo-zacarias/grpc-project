# Chat-app

This project implements a *one-way* chat application using [grpc](https://grpc.io/), [Python](https://www.python.org/) and [.NET/C#](https://dotnet.microsoft.com/).

## Getting started

This project consists of two containerized (Docker) applications:
* Python: server
* .NET: client
 
**The server** accepts the text typed by the user in the console.
 
**The client** printouts the text from the server to the console as it is being typed.

grpc is used for inter-container communication.

### Prerequisites

To run this application you will need [Docker](https://www.docker.com/).

### Installation

Clone this project if you haven't done it yet :) <br>
Open a terminal in the root folder and build the images and containers:

```
docker-compose up --no-start
```

In the same terminal start the server:
```
docker start -i app-server
```
If the server starts successfully it will show the info message: *Starting server on [::]:50051*

Open another terminal and start the client:
```
docker start -i app-client
```

### Usage

After starting the client, the server's terminal should show the following message: *Got message request from fooBar. Type text to send. Press Ctrl+C to stop.*

At this point you can type in the server's terminal and the text will be displayed in the client's terminal.

## Contact

Paulo Zacarias - [paulo.zacarias@ericsson.com](paulo.zacarias@ericsson.com).