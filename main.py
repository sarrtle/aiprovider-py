"""Main application."""

import asyncio
from chat.chat_api import ChatApi
from chat.chat_builder import ChatBuilder

from models.text_generation.deepinfra.meta_llama import LLAMA3_1_8B_INSTRUCT_TURBO

# from models.tts.deepinfra.kokoro import KOKORO
# from models.tts.deepinfra.canopylabs import ORPHEUS_3B
from models.tts.deepinfra.sesame import SESAME
from tts.tts_api import TTSApi
from utils.common import save_tts_to_file


async def test_chat():
    """Test  chat."""
    chat_api = ChatApi().use_tor().as_browser()

    # use with api key
    # chat_api = ChatApi().with_api_key("YOUR_API_KEY")

    chat = ChatBuilder(model=LLAMA3_1_8B_INSTRUCT_TURBO)

    chat.add_system_message("You are a helpful assistant.")
    chat.add_user_message("Hi, what can you do")

    async for stream_response in chat_api.send_chat_stream(chat=chat):
        print(stream_response.choices[0].delta.content)


async def test_tts():
    """Test tts."""
    tts_api = TTSApi().use_tor().as_browser()

    # use with api key
    # tts_api = TTSApi().with_api_key("YOUR_API_KEY")

    response = await tts_api.send_tts_with_clone_audio(
        "Hmm. But what are you doing here in the first place?",
        SESAME,
        "test-input.ogg",
        "Happy birthday! So, what are your plans for the day? Oh, why don't we celebrate on Watatsumi Island? First, I'll take you out at daybreak to see the sunrise, then we can go diving during the heat of the day. In the evening, we can go for a stroll around Sangonomiya Shrine. If it rains, we'll find somewhere cozy to hide out with a few strategy books, and try to bake a cake together! In any case, no need to plan anything, the grand strategist has everything thought out for you!",
    )

    await save_tts_to_file(response.audio, "test.ogg")


async def main():
    """Application."""
    # await test_chat()
    await test_tts()


if __name__ == "__main__":
    asyncio.run(main())
