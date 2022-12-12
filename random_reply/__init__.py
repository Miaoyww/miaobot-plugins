import asyncio
import json
from pathlib import Path
import random
from httpx import *
from nonebot import on_message, logger, on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import *
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.log import logger
from nonebot.rule import to_me
from data_source import *

__plugin_meta__ = PluginMetadata(
    name='随机回复',
    description='随机回复一句话~',
    usage='''当你at bot并且回复一些话的时候，它会随机回复你'''
)

reply = on_message(rule=to_me(), permission=GROUP)


@reply.handle()
async def _(event: MessageEvent):
    text = str(event.message)
    nickname = event.sender.nickname
    user_id = event.sender.user_id
    '''if not await check_text(text):
        logger.info(f"USER {user_id}|{nickname} 发送了违规文本 {text} 拒绝回复")
        return'''
    result = await get_reply_result(text)
    if result is not None:
        await asyncio.sleep(random.randint(10, 20) / 10)
        logger.info(f"USER {user_id}|{nickname} 发送了 {text} 其回复是 {result} ")
        await reply.finish(result)
    else:
        return
