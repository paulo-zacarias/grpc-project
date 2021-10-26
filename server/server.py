import asyncio
import logging

import grpc
import chat_app_pb2 as pb2
import chat_app_pb2_grpc as pb2_grpc

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []

class ChatServicer(pb2_grpc.ChatAppServicer):
 
    async def receiveMessages(self, request, context: grpc.ServicerContext):
        print(f'Got message request from {request.name}')

        while True:
            text = input('Type text: ')
            if(text == '+exit'):
                return
            yield pb2.ChatMessage(msg=text)

            # message = input(f'Type text: ')
            # yield pb2.ChatMessage(msg=message)

async def serve() -> None:
    server = grpc.aio.server()
    pb2_grpc.add_ChatAppServicer_to_server(ChatServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    # await server.wait_for_termination()

    # https://github.com/grpc/grpc/pull/26622/files
    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(serve())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()