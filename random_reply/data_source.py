import difflib
import json
import os
from pathlib import Path
import random
from typing import Any

from nonebot import logger
from nonebot.adapters.onebot.v11 import MessageSegment

replies = json.load(open(Path(__file__).parent / "reply.json", "r", encoding='utf-8'))
voice_lst = os.listdir(f"{Path(__file__).parent}/res/dingzhen")


def record(voice_name: str, path: str = None) -> MessageSegment or str:
    """
    说明:
        生成一个 MessageSegment.record 消息
    参数:
        :param voice_name: 音频文件名称，默认在 resource/voice 目录下
        :param path: 音频文件路径，默认在 resource/voice 目录下
    """
    if len(voice_name.split(".")) == 1:
        voice_name += ".mp3"
    file = (Path(__file__) / "res" / path / voice_name)
    if file.exists():
        result = MessageSegment.record(f"file:///{file.absolute()}")
        return result
    else:
        logger.warning(f"语音{file.absolute()}缺失...")
        return None


async def get_reply_result(text: str) -> MessageSegment | None:
    if result := get_special_reply_result(text) is not None:
        return result
    return get_text_reply_result(text)


async def get_special_reply_result(text: str) -> MessageSegment | None:
    if f"{text}.mp3" not in voice_lst:
        return record(random.choice(await get_close_matches(text, voice_lst)), "dingzhen")
    else:
        return record(text, "dingzhen")


async def get_close_matches(arg: str, lst: list) -> list:
    match_list = []
    for cf in range(20):
        match = difflib.get_close_matches(arg, lst, cutoff=1.0 - cf / 20.0, n=20)
        if len(match) > 0:
            match_list.append(match[0])
    return match_list


async def get_text_reply_result(text: str) -> MessageSegment | None:
    keys = replies.keys()
    for key in keys:
        if text.find(key) != -1:
            result = MessageSegment.text(random.choice(replies[key]))
            return result
