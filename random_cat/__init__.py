from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import Event
import httpx

miao = on_command("cat", aliases={"jrcat", "今日猫猫", "猫猫"}, block=True, priority=5)


@miao.handle()
async def hf(bot: Bot, ev: Event):
    try:
        async with httpx.AsyncClient() as client:
            img = await client.get(url="http://edgecats.net/")
            await bot.send(event=ev, message=MessageSegment.image(img.content))
    except:
        return await bot.send(event=ev, message="悲 猫猫获取失败力!")
