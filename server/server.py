import logging
from concurrent import futures

import keyboard as kb

import os

import grpc
import chat_app_pb2 as pb2
import chat_app_pb2_grpc as pb2_grpc
class ChatServicer(pb2_grpc.ChatAppServicer):

    def clearConsole(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)

    def receiveMessages(self, request, context) -> pb2.ChatMessage:

        self.clearConsole()

        print(f'Got message request from {request.name}.\nType text to send. Press Ctrl+C to stop.\n')

        while context.is_active():
            try:
                key = kb.getche()
                yield pb2.ChatMessage(msg=key)
            except KeyboardInterrupt:
                context.cancel()
                print('\nClosing the stream. Press again Ctrl+C to shutdown the server.')
                return
            except:
                return

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChatAppServicer_to_server(ChatServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()