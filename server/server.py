import asyncio
import logging
from pynput import keyboard
from queue import Queue

import os

import grpc
import chat_app_pb2 as pb2
import chat_app_pb2_grpc as pb2_grpc

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []

class ChatServicer(pb2_grpc.ChatAppServicer):

    total_messages = ''

    def __init__(self):
        self.command = 'cls' if os.name in ('nt', 'dos') else 'clear'

    async def receiveMessages(self, request, context):

        global shallContinue
        shallContinue = True

        def clearConsole():
            os.system(self.command)
            
        clearConsole()
        self.total_messages = ''
        print(f'Got message request from {request.name}.\nType text to send. Press Esc key to stop.\n')

        queue = Queue()

        def on_press(key):
            if key == keyboard.Key.esc:
                print('exit requested...')
                globals()['shallContinue'] = False
                queue.put('')
            if key == keyboard.Key.space:
                queue.put(' ')
            if key == keyboard.Key.enter:
                queue.put('\n')
            if (type(key) == keyboard.KeyCode):
                k = str(key).replace(f'{chr(39)}', '')
                queue.put(k)


        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while True:

            message = queue.get()
            self.total_messages += message
            clearConsole()
            print(self.total_messages)
            if(not shallContinue):
                print()
                self.shallContinue = True
                listener.stop()
                queue.all_tasks_done
                return
            yield pb2.ChatMessage(msg=message)

async def serve() -> None:
    server = grpc.aio.server()
    pb2_grpc.add_ChatAppServicer_to_server(ChatServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()

    # https://github.com/grpc/grpc/pull/26622/files
    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()