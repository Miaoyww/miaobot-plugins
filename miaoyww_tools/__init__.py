from pathlib import Path
from nonebot import logger
from nonebot.internal.matcher import Matcher
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
import os
import shutil
import requests
import zipfile
import threading

update = on_command("upd", aliases={"更新", "update"}, permission=SUPERUSER)


def del_files(path_file):
    file_list = os.listdir(path_file)
    for item in file_list:
        f_path = os.path.join(path_file, item)
        if os.path.isdir(f_path):
            del_files(f_path)
            os.rmdir(f_path)
        else:
            os.remove(f_path)


def remove_file(old_path, new_path):
    file_list = os.listdir(old_path)
    for file in file_list:
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        shutil.move(src, dst)


@update.handle()
async def update_handler(matcher: Matcher):
    plugins_path = Path(__file__).parent.parent.parent
    plugins_temp_path = f"{plugins_path}\\plugins_temp"
    if os.path.exists(plugins_temp_path):
        del_files(plugins_temp_path)
    logger.info("开始获取插件压缩包")
    if os.path.exists(plugins_temp_path + ".zip"):
        os.remove(plugins_temp_path + ".zip")
    with open(plugins_temp_path + ".zip", "wb") as w:
        resp = requests.get("https://github.com/Miaoyww/miaobot-plugins/archive/refs/heads/main.zip").content
        w.write(resp)
    logger.info("获取成功")
    logger.info("开始解压压缩包")
    file = zipfile.ZipFile(plugins_temp_path + ".zip", )
    file.extractall(plugins_path)
    file.close()
    logger.info("Update Done")

    def callback():
        os.remove(plugins_temp_path + ".zip")
        del_files(f"{plugins_path}\\plugins")
        remove_file(f"{plugins_path}\\miaobot-plugins-main", f"{plugins_path}\\plugins")
        del_files(f"{plugins_path}\\miaobot-plugins-main")

    threading.Thread(callback()).start()
