from nonebot import on_command
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    GROUP,
    PRIVATE_FRIEND,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)

from .config import Config
from .data_source import get_setu

setu_matcher = on_command(
    "setu",
    aliases={"来点涩图", "来点色图", "涩涩", "色色"},
    permission=PRIVATE_FRIEND | GROUP,
)


@setu_matcher.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text()
    r18 = True if (isinstance(event, PrivateMessageEvent) and True if args.split(" ")[0] == "r18" else False) else False
    tags = args.split(" ")[r18::]
    await get_setu(setu_matcher, event, r18, tags)
    logger.debug(f"{args} | {tags} | {r18}")
