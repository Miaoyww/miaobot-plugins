import asyncio
import json
from pathlib import Path
import random
from httpx import *
from nonebot import on_message, logger
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import *

__plugin_meta__ = PluginMetadata(
    name='随机回复',
    description='随机回复一句话~',
    usage='''当你at bot并且回复一些话的时候，它会随机回复你'''
)

from nonebot.rule import to_me

reply = on_message(rule=to_me())

replies = json.load(open(Path(__file__).parent / "reply.json", "r", encoding='utf-8'))


@reply.handle()
async def _(event: MessageEvent):
    text = str(event.message)
    nickname = event.sender.nickname
    user_id = event.sender.user_id
    if not await check_text(text):
        logger.info(f"USER {user_id}|{nickname} 发送了违规文本 {text} 拒绝回复")
        return
    result = await get_reply_result(text)
    if result is not None:
        await asyncio.sleep(random.randint(10, 20) / 10)
        logger.info(f"USER {user_id}|{nickname} 发送了 {text} 其回复是 {result} ")
        await reply.finish(result)


async def get_reply_result(text: str) -> str | None:
    keys = replies.keys()
    for key in keys:
        if text.find(key) != -1:
            return random.choice(replies[key])


async def check_text(text: str) -> bool:
    params = {"token": "DCPsDueVPz8mxfDn", "text": text}
    async with AsyncClient() as client:
        data = (await client.post("https://v2.alapi.cn/api/censor/text", timeout=3, params=params)).json()
        if data["code"] == 200:
            if data["data"]["conclusion_type"] == 2:
                return False
            else:
                return True
