import asyncio
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP, Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

version = on_command("ver", aliases={"版本", "version"}, permission=SUPERUSER)
update = on_command("upd", aliases={"更新", "update"}, permission=SUPERUSER)


@version.handle()
async def version_handler(matcher: Matcher):
    await matcher.send("function version test passed")


@update.handle()
async def version_handler(matcher: Matcher):
    await matcher.send("function update test passed")
