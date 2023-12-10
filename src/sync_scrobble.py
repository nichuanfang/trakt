import os
import json
import base64
from core import core
from trakt import movies, tv, sync, errors
from trakt.users import User
from telebot import TeleBot
from libsql import db

bot = TeleBot(token=os.environ['GH_BOT_TOKEN'])
# token文件保存路径
core.CONFIG_PATH = os.path.join(os.path.dirname(__file__), '.pytrakt.json')


def auth():
    """Auth by device code
    """
    # 1. 查询环境变量中是否存在TRAKT_TOKEN
    # 2. 如果存在，直接使用该token进行登录 TOKEN(需要base64解码)
    # 3, 如果不存在，使用设备激活码进行登录,登录成功后，将token保存到环境变量中(需要tgbot配合激活设备)
    if os.environ.get('TRAKT_TOKEN'):
        try:
            token = base64.b64decode(os.environ['TRAKT_TOKEN']).decode('utf-8')
            json.dump(json.loads(token), open(core.CONFIG_PATH, 'w+'))
            # 加载token文件
            core.load_config()
            print('登录成功!')
            return
        except:
            print('TRAKT_TOKEN解码失败!尝试重新登录...')
    core.device_auth(client_id=os.environ['TRAKT_CLIENT_ID'],
                     client_secret=os.environ['TRAKT_CLIENT_SECRET'], tgbot=bot, store=True)
    # 保存token到github outputs中
    TRAKT_TOKEN = json.load(open(core.CONFIG_PATH, 'r'))
    TRAKT_TOKEN = base64.b64encode(json.dumps(
        TRAKT_TOKEN).encode('utf-8')).decode('utf-8')
    bot.send_message(chat_id=os.environ['TG_CHAT_ID'], text='TRAKT设备激活成功')
    os.system(f'echo "TRAKT_TOKEN={TRAKT_TOKEN}" >> "$GITHUB_OUTPUT"')


if __name__ == '__main__':
    # 认证授权
    auth()
    # 获取当前用户
    try:
        user = User(os.environ['TRAKT_USER'])
    except:
        core.device_auth(client_id=os.environ['TRAKT_CLIENT_ID'],
                         client_secret=os.environ['TRAKT_CLIENT_SECRET'], tgbot=bot, store=True)
        # 保存token到github outputs中
        TRAKT_TOKEN = json.load(open(core.CONFIG_PATH, 'r'))
        TRAKT_TOKEN = base64.b64encode(json.dumps(
            TRAKT_TOKEN).encode('utf-8')).decode('utf-8')
        bot.send_message(chat_id=os.environ['TG_CHAT_ID'], text='TRAKT设备激活成功')
        os.system(f'echo "TRAKT_TOKEN={TRAKT_TOKEN}" >> "$GITHUB_OUTPUT"')
    # 已观看的电影
    watched_movies = user.watched_movies
    # 同步电影进度
    db.update_movies(watched_movies)
    # 已观看的剧集
    watched_shows = user.watched_shows
    # 同步剧集进度
    db.update_shows(watched_shows)
