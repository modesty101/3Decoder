#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import base64
import urllib
import urllib2
''' Base64 / URL / HEX check function'''
def check(value):
	if value[-1] == '=':
		return base64.decodestring(value)
	elif value[0] == '%':
		return urllib.unquote(value)
	elif value[0] == '0':
		return value[2:].decode('hex')

url = "http://45.32.53.225/CTF/decode_Me/"	# 문제
chk_url = "http://45.32.53.225/CTF/decode_Me/check.php?str=" # 체크
''' 문제를 불러올 때 필요한 쿠키값을 가져온다 '''
req = urllib2.Request(url)
res = urllib2.urlopen(req)
cookie = res.headers.get('Set-Cookie')
''' <pre> 파싱 '''
soup = BeautifulSoup(res.read(), 'lxml')
article = check(soup.findAll('pre')[0].string)  # pre 추출
''' 디코딩한 값을 검사하려면 GET/POST 방식으로 전송해야한다. 
urlopen 전에 쿠키(문제) 값을 추가해준다. '''
chk_req = urllib2.Request(chk_url + article)
chk_req.add_header("Cookie",cookie)
chk_res = urllib2.urlopen(chk_req)

''' 문제 -> 쿠키 추가 '''
req.add_header("Cookie",cookie)

for i in range(48):
	''' /decode_Me/ 31번줄 Cookie 추가해서 호출 '''
	res = urllib2.urlopen(req) # req : 문제
	read = res.read() # 페이지 리소스 읽기

	soup = BeautifulSoup(read, 'lxml')
	article = check(soup.findAll('pre')[0].string)  # pre 추출
	
	print read	# 페이지 소스 출력

	chk_req = urllib2.Request(chk_url + str(article)) # Check 값 전송
	chk_req.add_header("Cookie", cookie) # 쿠키 추가
	chk_res = urllib2.urlopen(chk_req) 
	print chk_res.read() # Good Work!!... printing

res = urllib2.urlopen(req)	# 출력
print res.read()