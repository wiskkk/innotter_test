import asyncio

from fastapi import FastAPI

from pika_client import PikaClient
from router import router


class FooApp(FastAPI):

    def __init__(self, *args, **kwargs):
        print(12)
        super().__init__(*args, **kwargs)
        print(13)
        self.pika_client = PikaClient(self.log_incoming_message)
        print(self.pika_client)
        print('13.1')

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Способ сделать что-то осмысленное с входящим сообщением"""
        print(14)
        print('Здесь мы получили входящее сообщение', message)


print(15)
foo_app = FooApp()
print(16)
foo_app.include_router(router)
print(17)
foo_app.pika_client.process_incoming_message()


@foo_app.on_event('startup')
async def startup():
    print(18)
    loop = asyncio.get_running_loop()
    print(19)
    task = loop.create_task(foo_app.pika_client.consume(loop))
    print(20)
    await task
