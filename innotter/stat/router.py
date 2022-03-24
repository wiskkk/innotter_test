from fastapi import APIRouter
from starlette.requests import Request

from schema import MessageSchema, TestSchema, PageSchema

router = APIRouter(
    tags=['items'],
    responses={404: {"description": "Page not found"}}
)


# @router.post('/send-message')
# async def send_message(payload: MessageSchema, request: Request):
#     print(21)
#     request.app.pika_client.send_message(
#         {"message": payload.message}
#     )
#     print(22)
#     return {"status": "ok"}


@router.post('/test')
async def test(payload: PageSchema, request: Request):
    request.app.pika_client.process_incoming_message(
        {'message': payload}
    )
    return {'status': 'ok'}
