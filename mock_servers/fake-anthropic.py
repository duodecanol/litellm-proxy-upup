import asyncio
import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from rich import print
from sse_starlette import EventSourceResponse

print("hello")

app = FastAPI()


@app.post("/messages")
@app.post("/v1/messages")
async def anthropic_completion(request: Request):
    print(request.__dict__)
    body = json.loads(await request.body())
    print("request body".center(88, "="))
    print(body)
    stream = body.get("stream", False)
    model: str = body["model"]
    if not model.startswith("claude-3-5-sonnet-20240620"):
        raise HTTPException(status_code=400, detail="Invalid model")
    code = model.removeprefix("claude-3-5-sonnet-20240620").strip("-")
    print(f"{stream = }")
    print(f"{code = }")
    print(f"{model = }")

    if stream:
        match code:
            case "111":
                return EventSourceResponse(
                    streaming_111(), media_type="text/event-stream"
                )
            case "112":
                return EventSourceResponse(
                    streaming_112(), media_type="text/event-stream"
                )
            case _:
                return EventSourceResponse(streaming(), media_type="text/event-stream")

    match code:
        case "529":
            raise HTTPException(
                status_code=529,
                detail="Overloaded Error!",
                headers={"retry-after": "0"},
            )
        case "500":
            raise HTTPException(
                status_code=500,
                detail="Overloaded Error!",
                headers={"retry-after": "0"},
            )
        case "429":
            raise HTTPException(
                status_code=429,
                detail="Overloaded Error!",
                headers={"retry-after": "0"},
            )
        case _:
            return {
                "content": [
                    # {"text": "","type": "text"}
                ],
                "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
                "model": model,
                "role": "assistant",
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "type": "message",
                "usage": {"input_tokens": 2095, "output_tokens": 503},
            }


error_event = {
    "event": "error",
    "data": {
        "type": "error",
        "error": {
            "type": "overloaded_error",
            "message": "Overloaded",
            "status_code": 529,
        },
    },
}
# error_event = HTTPException(
#     status_code=529, detail="Overloaded Error!", headers={"retry-after": "30"}
# )


async def streaming():
    # https://docs.anthropic.com/en/api/messages-streaming
    stream_events = (
        {
            "event": "message_start",
            "data": {
                "type": "message_start",
                "message": {
                    "id": "msg_1nZdL29xx5MUA1yADyHTEsnR8uuvGzszyY",
                    "type": "message",
                    "role": "assistant",
                    "content": [],
                    "model": "claude-3-5-sonnet-20240620",
                    "stop_reason": None,
                    "stop_sequence": None,
                    "usage": {"input_tokens": 25, "output_tokens": 1},
                },
            },
        },
        {
            "event": "content_block_start",
            "data": {
                "type": "content_block_start",
                "index": 0,
                "content_block": {"type": "text", "text": ""},
            },
        },
        {"event": "ping", "data": {"type": "ping"}},
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "Hello"},
            },
        },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "!"},
            },
        },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "How can"},
            },
        },
        error_event,
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "I help"},
            },
        },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "you??"},
            },
        },
        {
            "event": "content_block_stop",
            "data": {"type": "content_block_stop", "index": 0},
        },
        {
            "event": "message_delta",
            "data": {
                "type": "message_delta",
                "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                "usage": {"output_tokens": 15},
            },
        },
        {"event": "message_stop", "data": {"type": "message_stop"}},
    )
    await asyncio.sleep(3)
    n = 0
    for event in stream_events:
        n += 1
        if n == 6:
            await asyncio.sleep(3)
        else:
            await asyncio.sleep(0.14)
        if isinstance(event, Exception):
            raise event
        yield {"event": event["event"], "data": json.dumps(event["data"])}


async def streaming_111():
    # https://docs.anthropic.com/en/api/messages-streaming
    stream_events = (
        {
            "event": "message_start",
            "data": {
                "type": "message_start",
                "message": {
                    "id": "msg_1nZdL29xx5MUA1yADyHTEsnR8uuvGzszyY",
                    "type": "message",
                    "role": "assistant",
                    "content": [],
                    "model": "claude-3-5-sonnet-20240620",
                    "stop_reason": None,
                    "stop_sequence": None,
                    "usage": {"input_tokens": 25, "output_tokens": 1},
                },
            },
        },
        {
            "event": "content_block_start",
            "data": {
                "type": "content_block_start",
                "index": 0,
                "content_block": {"type": "text", "text": ""},
            },
        },
        {"event": "ping", "data": {"type": "ping"}},
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "Hello"},
            },
        },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "!"},
            },
        },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "How can"},
            },
        },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": None},
            },
        },
        # {
        #     "event": "content_block_delta",
        #     "data": None
        # },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "I help"},
            },
        },
        {
            "event": "content_block_delta",
            "data": {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "you??"},
            },
        },
        {
            "event": "content_block_stop",
            "data": {"type": "content_block_stop", "index": 0},
        },
        {
            "event": "message_delta",
            "data": {
                "type": "message_delta",
                "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                "usage": {"output_tokens": 15},
            },
        },
        {"event": "message_stop", "data": {"type": "message_stop"}},
    )
    await asyncio.sleep(1)
    for event in stream_events:
        await asyncio.sleep(0.14)
        if isinstance(event, Exception):
            raise event
        if event is None:
            yield None
            continue
        yield {"event": event["event"], "data": json.dumps(event["data"])}


async def streaming_112():
    # https://docs.anthropic.com/en/api/messages-streaming
    stream_events = (
        {
            "event": "message_start",
            "data": {"type": "message_start", "message": ""},
            # "data": {"type": "message_start", "message": {"id": "msg_1nZdL29xx5MUA1yADyHTEsnR8uuvGzszyY", "type": "message", "role": "assistant", "content": [], "model": "claude-3-5-sonnet-20240620", "stop_reason": None, "stop_sequence": None, "usage": {"input_tokens": 25, "output_tokens": 1}}}
        },
        {
            #     "event": "content_block_start",
            #     "data": {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}
            # },{
            #     "event": "content_block_stop",
            #     "data": {"type": "content_block_stop", "index": 0}
            # }, {
            #     "event": "message_delta",
            #     "data": {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence":None}, "usage": {"output_tokens": 0}}
            # }, {
            "event": "message_stop",
            "data": {"type": "message_stop"},
        },
    )
    await asyncio.sleep(1)
    for event in stream_events:
        await asyncio.sleep(0.14)
        if isinstance(event, Exception):
            raise event
        if event is None:
            yield None
            continue
        yield {"event": event["event"], "data": json.dumps(event["data"])}


def main() -> None:
    """Entrypoint of the application."""

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9119,
    )


main()
