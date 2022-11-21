import requests
from pprint import pprint
import json
from datetime import datetime, timedelta, date, time
import re

'''Не дописанный бот для составления расписания c TrueConf Server на текущие сутки и публикации в Telegram. Root55.ru'''

def look_server(url,CrtCA=False):
	HEAD = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla/5.0 (X11; Ebunta; MacrosoFuck x86_64; rv:105.0) Gecko/20100101 Firefox/105.0'
	}
	VIEW_DATA = requests.get(url = url, headers = HEAD, verify = CrtCA, timeout = 10)
	NUM_PAGES = VIEW_DATA.json()
	for PAGE_COUNT in range(1, int(NUM_PAGES.get('cnt') / 100) + 2):
		ALL_PAGES = requests.get(url = url+'&page_id='+str(PAGE_COUNT)+'&page_size=100', headers = HEAD, verify = CrtCA, timeout = 30)
		ALL_CNT = ALL_PAGES.json()
		FULL_CNT = ALL_CNT.get('conferences')
		return FULL_CNT

def conference_search(look_s):
	LIST_CONF = []
	for CONFERENCE in look_s:
		PLANNED = CONFERENCE.get('schedule').get('type')
		TIME_CONFERENCE = CONFERENCE.get('schedule').get('start_time')
		NEW_DAY = datetime.combine(date.today(), time(00, 00, 00)).timestamp()
		END_DAY = NEW_DAY + timedelta(days=1).total_seconds()
		if PLANNED != -1 and END_DAY > TIME_CONFERENCE > NEW_DAY not in look_s:
			TIME_CNT = datetime.fromtimestamp(CONFERENCE.get("schedule").get("start_time")).strftime('%d.%m.%Y в %H:%M')
			GUEST_LIST = CONFERENCE.get('invitations')
			ORGANIZER_CNT = {CONFERENCE.pop('id'): CONFERENCE for CONFERENCE in GUEST_LIST}[CONFERENCE.get('owner').partition('@')[0]].get('display_name')
			NAME_CNT = CONFERENCE.get("topic")
			ID_CNT = CONFERENCE.get("id")
			USERS_CNT = str(sorted([CONFERENCE['display_name'] for CONFERENCE in GUEST_LIST])).replace("'", "").replace(ORGANIZER_CNT+", " or ORGANIZER_CNT, "")[1:-1]
			INFO_CNT = re.sub(r'\<[^>]*\>', '', CONFERENCE.get('description').replace('<p', '\n<p'))
			LIST_CONF.append(
				{
					'publication': '1',
					'name': NAME_CNT,
					'organizer': ORGANIZER_CNT,
					'time': TIME_CNT,
					'id': ID_CNT,
					'users': USERS_CNT,
					'info': INFO_CNT
				}
			)
	return LIST_CONF

def save_json(save_j):
	try:
		file = open('C:\VKSdays\DAY-'+str(date.today())+'.json', encoding='utf-8')
	except:
		with open('C:\VKSdays\DAY-'+str(date.today())+'.json', 'w', encoding='utf-8') as file:
			json.dump(save_j, file, indent=4, ensure_ascii=False)
		return save_j
	else:
		with open('C:\VKSdays\DAY-'+str(date.today())+'.json', encoding='utf-8') as file:
			stock = json.load(file)
		res = [x for x in stock + save_j if x not in stock]
		news = stock+res
		with open('C:\VKSdays\DAY-'+str(date.today())+'.json', 'w', encoding='utf-8') as file:
			json.dump(news, file, indent=4, ensure_ascii=False)
		return res

def new_print(new_p):
	botTg = 'bot2043679747:AAHy34fyDdind4t34ewGXzRwYXX-afbdgHdQ'             #Токен API бота Telegram
	idTg = '-100177808352'                                                #ID группы или пользователя Telegram
	DAY_NAMES = ['Воскресенье','Понедельник','Вторник','Среду','Четверг','Пятницу','Субботу']
	UNIX_TIME = DAY_NAMES[datetime.today().isoweekday()]
	if len(str(new_p)) >= 3:
		for PUBLIC in new_p:
			NAME_CNT = PUBLIC.get('name')
			ORGANIZER_CNT = PUBLIC.get('organizer')
			TIME_CNT = PUBLIC.get('time')
			ID_CNT = PUBLIC.get('id')
			USERS_CNT = PUBLIC.get('users')
			INFO_CNT = PUBLIC.get('info')
			RASPISANIE = '📆 <b>Расписание на '+UNIX_TIME+'</b>\n\n✏ <b>Название ВКС:</b> <i>'+NAME_CNT+'</i>\n🧘 <b>Организатор:</b> '+ORGANIZER_CNT+'\n⏰ <b>Время начала подключения:</b> '+TIME_CNT+'\n\n🪤 <b>Ссылка для подключения:</b> https://10.10.10.10/c/'+ID_CNT+'\n\n👯<b>Список участников:</b> '+USERS_CNT+'\n\n📚 <b>Дополнительная информация:</b> '+INFO_CNT
			TEXT_TG = [(f'{RASPISANIE}')]
			for calendar in TEXT_TG:
				urlTG = 'https://api.telegram.org/'+botTg+'/sendMessage?chat_id='+idTg+'&parse_mode=html&text={}'.format(calendar)
				requests.get(urlTG)
	else:
		print('Ничего нету!')

def main():
	settings = open('C:\setup.txt').read().split('\n')
	look_s = look_server(url ='https://'+settings[0]+'/api/v3.4/conferences/?access_token='+settings[1], CrtCA=settings[2])
	conference_s = conference_search(look_s)
	save_j = save_json(conference_s)
	new_p = new_print(save_j)

if __name__ == '__main__':
	main()