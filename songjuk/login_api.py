from bs4 import BeautifulSoup
import requests

from Songjuk import settings


def get_session_and_m():
	r = requests.get(settings.SONGJUK_URL)

	soup = BeautifulSoup(r.text)
	m_tag = soup.find(name='input', id='m')

	return r.cookies['JSESSIONID'], m_tag['value']


def login(rsa_id, rsa_password, jsession_id):
	payload = {
		'type': 'STUD',
		'userId': rsa_id,
	    'pwd': rsa_password,
	}

	cookies = {
		'JSESSIONID': jsession_id,
	}

	r = requests.post(settings.LOGIN_URL, data=payload, cookies=cookies)

	soup = BeautifulSoup(r.text)

	message_tag = soup.find('div', class_='alert alert-block lnline')
	if message_tag:
		return message_tag.text
	else:
		return True