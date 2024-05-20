import pytest
from aiogram.filters import StateFilter

from aiogram_tests.handler import MessageHandler
from aiogram_tests.handler import RequestHandler
from aiogram_tests.handler import TelegramEventObserverHandler
from .middleware import TestMiddleware


def test_request_handler_initialization():
    RequestHandler((), ())


def test_request_handler_dp_middlewares():
    r_h = RequestHandler(dp_middlewares=(TestMiddleware(),))
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 1

    r_h = RequestHandler(dp_middlewares=(TestMiddleware(), TestMiddleware()))
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 2

    r_h = RequestHandler(
        dp_middlewares=(TestMiddleware(), TestMiddleware()),
        exclude_observer_methods=["message"],
    )
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 0


def test_telegram_observ_methods_handler_init():
    async def callback(*args, **kwargs):
        pass

    with pytest.raises(ValueError):
        _ = TelegramEventObserverHandler(callback, state_data=[])


EMPTY_MESSAGE = {
    "chat": {
        "id": 0,
        "type": "private"
        },
    "date": 0,
    "message_id": 0,
    "text": ""
}


@pytest.mark.asyncio
async def test_telegram_observ_handler():
    async def callback(*args, **kwargs):
        pass

    t_h = MessageHandler(callback)
    await t_h(EMPTY_MESSAGE)
    handlers_count = len(t_h.dp.message.handlers)
    assert handlers_count == 1

    t_h = MessageHandler(callback, StateFilter(None))
    await t_h(EMPTY_MESSAGE)
    handlers_count = len(t_h.dp.message.handlers)
    assert handlers_count == 1


@pytest.mark.asyncio
async def test_state_telegram_observ_handler():
    async def callback(*args, **kwargs):
        pass

    t_h = MessageHandler(callback, state="state", state_data={"name": "Mike"})
    await t_h(message=EMPTY_MESSAGE)

    context = t_h.dp.fsm.get_context(t_h.bot, 12345678, 12345678)
    state = await context.get_state()
    data = await context.get_data()

    assert state == "state"
    assert data == {"name": "Mike"}
