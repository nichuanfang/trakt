import asyncio
import base64
import json
import os

import dotenv
import requests
from telebot import TeleBot

from core import core
from core.users import User
from libsql import db

dotenv.load_dotenv(override=True)

bot = TeleBot(token=os.environ['GH_BOT_TOKEN'])
# token文件保存路径
core.CONFIG_PATH = os.path.join(os.path.dirname(__file__), '.pytrakt.json')


def auth():
	"""Auth by device code
	"""
	# 1. 查询环境变量中是否存在TRAKT_TOKEN
	# 2. 如果存在，直接使用该token进行登录 TOKEN(需要base64解码)
	# 3, 如果不存在，使用设备激活码进行登录,登录成功后，将token保存到环境变量中(需要tgbot配合激活设备)
	TRAKT_TOKEN = os.getenv('TRAKT_TOKEN')
	if TRAKT_TOKEN != None and TRAKT_TOKEN != '':
		try:
			token = base64.b64decode(TRAKT_TOKEN).decode('utf-8')
			json.dump(json.loads(token), open(core.CONFIG_PATH, 'w+'))
			# 加载token文件
			core.load_config()
			# 获取当前用户
			user = User(os.environ['TRAKT_USER'])
			return user
		except Exception as e:
			print(f'TRAKT_TOKEN无效!: {e} \n\n 尝试认证...')
			response = core.device_auth(client_id=os.environ['TRAKT_CLIENT_ID'],
			                            client_secret=os.environ['TRAKT_CLIENT_SECRET'],
			                            tgbot=bot, store=True)
			if response.status_code == 200:
				# 保存token到github outputs中
				TRAKT_TOKEN = json.load(open(core.CONFIG_PATH, 'r'))
				TRAKT_TOKEN = base64.b64encode(json.dumps(
					TRAKT_TOKEN).encode('utf-8')).decode('utf-8')
				bot.send_message(chat_id=os.environ['GH_BOT_CHAT_ID'], text='TRAKT设备激活成功')
				os.system(f'echo "TRAKT_TOKEN={TRAKT_TOKEN}" >> "$GITHUB_OUTPUT"')
			else:
				raise Exception(f'认证失败! 请检查TRAKT_CLIENT_ID和TRAKT_CLIENT_SECRET是否正确设置:  {response.text}')
	else:
		print(f'TRAKT_TOKEN为空! 尝试重新认证...')
		response = core.device_auth(client_id=os.environ['TRAKT_CLIENT_ID'],
		                            client_secret=os.environ['TRAKT_CLIENT_SECRET'],
		                            tgbot=bot, store=True)
		if response.status_code == 200:
			# 保存token到github outputs中
			TRAKT_TOKEN = json.load(open(core.CONFIG_PATH, 'r'))
			TRAKT_TOKEN = base64.b64encode(json.dumps(
				TRAKT_TOKEN).encode('utf-8')).decode('utf-8')
			bot.send_message(chat_id=os.environ['GH_BOT_CHAT_ID'], text='TRAKT设备激活成功')
			os.system(f'echo "TRAKT_TOKEN={TRAKT_TOKEN}" >> "$GITHUB_OUTPUT"')
			# 获取当前用户
			user = User(os.environ['TRAKT_USER'])
			return user
		else:
			raise Exception(f'认证失败! 请检查TRAKT_CLIENT_ID和TRAKT_CLIENT_SECRET是否正确设置:  {response.text}')


def refresh_movie_cache():
	"""通过请求https://api.jaychou.site/trakt/refresh_cache来更新movie缓存
	"""
	try:
		requests.get('https://api.jaychou.site/trakt/refresh_movie_cache')
		print('更新movie缓存成功!')
	except:
		print('更新movie缓存失败!')


def refresh_show_cache():
	"""通过请求https://api.jaychou.site/trakt/refresh_show_cache来更新movie缓存
	"""
	try:
		requests.get('https://api.jaychou.site/trakt/refresh_show_cache')
		print('更新show缓存成功!')
	except:
		print('更新show缓存失败!')


async def sync_movie(user: User):
	"""
	同步电影记录
	@param user: trakt用户
	"""
	# 已观看的电影
	watched_movies = user.watched_movies
	# 同步电影进度
	refresh_movie_cache_flag = db.update_movies(watched_movies)
	if refresh_movie_cache_flag:
		# 通知api服务更新movie缓存
		refresh_movie_cache()


async def sync_show(user: User):
	"""
	同步剧集记录
	@param user: trakt用户
	"""
	# 已观看的剧集
	watched_shows = user.watched_shows
	# 同步剧集进度
	refresh_show_cache_flag = db.update_shows(watched_shows)
	if refresh_show_cache_flag:
		# 通知api服务更新show缓存
		refresh_show_cache()


async def main():
	# 认证授权
	user = auth()
	try:
		# asyncio.gather虽然不是异步函数 但它执行异步函数 所以需要一个异步的上下文环境 为此需要将代码包装到一个异步的main函数中 再由asyncio.run来作为入口调用执行
		# sync_movie(user)
		await asyncio.gather(sync_show(user))
	finally:
		db.client.close()


if __name__ == '__main__':
	asyncio.run(main())
