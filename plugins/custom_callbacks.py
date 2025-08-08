from traceback import format_exception
from typing import Any, AsyncGenerator, Literal, Optional

from litellm.exceptions import InternalServerError
from litellm.integrations.custom_logger import CustomLogger
from litellm.proxy.proxy_server import DualCache, UserAPIKeyAuth
from litellm.types.utils import ModelResponseStream, StreamingChoices


# This file includes the custom callbacks for LiteLLM Proxy
# Once defined, these can be passed in proxy_config.yaml
class MyCustomHandler(
    CustomLogger
):  # https://docs.litellm.ai/docs/observability/custom_callback#callback-class
    # Class variables or attributes
    def __init__(self):
        pass

    #### CALL HOOKS - proxy only ####

    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: Literal[
            "completion",
            "text_completion",
            "embeddings",
            "image_generation",
            "moderation",
            "audio_transcription",
        ],
    ):
        pass

    async def async_post_call_failure_hook(
        self,
        request_data: dict,
        original_exception: Exception,
        user_api_key_dict: UserAPIKeyAuth,
        traceback_str: Optional[str] = None,
    ):
        pass

    async def async_post_call_success_hook(
        self,
        data: dict,
        user_api_key_dict: UserAPIKeyAuth,
        response,
    ):
        print("async_post_call_success_hook".center(80, "="))
        print(response)
        # CHECK
        # response.choices[-1].message.content
        chunk = response.choices[0]
        content = chunk.message.content
        if isinstance(content, str):
            check_text_len(content)

        print(data)

        print("=" * 80)
        pass

    async def async_moderation_hook(  # call made in parallel to llm api call
        self,
        data: dict,
        user_api_key_dict: UserAPIKeyAuth,
        call_type: Literal[
            "completion",
            "embeddings",
            "image_generation",
            "moderation",
            "audio_transcription",
        ],
    ):
        print("async_moderation_hook".center(80, "="))
        pass

    async def async_post_call_streaming_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        response: str,
    ):
        # async_post_call_streaming_iterator_hook
        # 의 yield 한번 때마다 호출됨.
        # 모든 stream chunk 마다.
        pass

    async def async_post_call_streaming_iterator_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        response: Any,
        request_data: dict,
    ) -> AsyncGenerator[ModelResponseStream, None]:
        """
        Passes the entire stream to the guardrail

        This is useful for plugins that need to see the entire stream.
        """
        print("async_post_call_streaming_iterator_hook".center(80, "="))
        print(request_data)
        x = None
        full_text = ""
        remnant = []
        try:
            item: ModelResponseStream
            async for item in response:
                if not x:
                    x = item
                chunk = item.choices[0]
                if not isinstance(chunk, StreamingChoices):
                    continue
                delta = chunk.delta
                if delta.tool_calls:
                    print(f"@@@@@ { delta.tool_calls = }")
                content = delta.content
                print(f"@@@@@ { chunk = }")

                # choice iter, multimodal
                if chunk.finish_reason:
                    remnant.append(item)
                    print(f"xxxxxxxxxxxxxxx {x = }")
                    print(f"{remnant = }")
                    print(f"{full_text = }")

                    check_text_len(full_text)

                    print("=" * 80)
                    print(f"{response = }")
                    continue
                if isinstance(content, str):
                    full_text += content
                yield item
        except ValueError as err:
            model: str = request_data["model"]
            provider, _, modelname = model.partition("/")

            raise InternalServerError(
                message=str(err),
                llm_provider=provider,
                model=request_data["model"],
            )
        except Exception as err:
            print("*********************************")
            print(format_exception(err))


# def check_text_len(input: str):
#     len_text = len(input)
#     print(f"{len_text = }")
#     if len_text < 80:
#         raise ValueError(
#             f"Response too short: {input}",
#         )


def check_text_len(input: str):
    len_text = len(input)
    print(f"{len_text = }")
    if len_text == 0:
        raise ValueError(
            f"Response too short: {input}",
        )


proxy_handler_instance = MyCustomHandler()
