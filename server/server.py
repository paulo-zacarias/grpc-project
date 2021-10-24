import asyncio
import logging

import grpc
import chat_app_pb2 as pb2
import chat_app_pb2_grpc as pb2_grpc

class ChatServicer(pb2_grpc.ChatAppServicer):
 
    async def receiveMessages(self, request, context):
        print(f'Got message request from {request.name}')
        while True:
            message = input(f'Type text: ')
            yield pb2.ChatMessage(msg=message)

async def serve() -> None:
    server = grpc.aio.server()
    pb2_grpc.add_ChatAppServicer_to_server(ChatServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())