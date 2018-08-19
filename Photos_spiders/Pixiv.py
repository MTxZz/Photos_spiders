import requests
import re
import json
import os

#模拟登陆,得到session用来下载图片
def login():
	url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'

	headers = {
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	}

	proxies = {
		'https':'socks5://127.0.0.1:1080',
	}

	r = requests.get(url,headers = headers,proxies = proxies)
	txt = r.text

	post_key =  re.search(r'name="post_key" value="(.*)"><input',txt,re.I|re.M).group(1)

	postData = {
	'password':	'2016969619',
	'pixiv_id':	'2026969619@qq.com',
	'post_key':	post_key,
	'ref':	'wwwtop_accounts_index',
	'return_to':	'https://www.pixiv.net',
	'source':	'pc',
	}
	session = requests.Session()
	session.headers = headers
	session.post(url,proxies = proxies,data = postData)
	C= session.cookies
	#print(C)
	#经过测试C中的PHPSESSID替换下面headers中的Cookie无法解析网页，想不通，望高人指点
	#print('初始：　' + PHPSESSID)
	return session

'''
得到ID列表,需要从'https://www.pixiv.net/discovery'中找出tt,

'''
def get_List():
	url1 = 'https://www.pixiv.net/discovery'
	#得到tt需要的headers
	headers1 = {
	'Cookie': 'PHPSESSID=33748554_67ef233ab30e6f85d361520e79cf17cd',
	'Referer':'https://www.pixiv.net/',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
	}
	#得到ID列表需要的headers
	headers = {
	'Cookie':'PHPSESSID=33748554_67ef233ab30e6f85d361520e79cf17cd',
	'Referer': 'https://www.pixiv.net/discovery',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',	
	}
	proxies = {
		'https':'socks5://127.0.0.1:1080',
	}
	#得到tt
	r = requests.get(url1,headers = headers1,proxies = proxies)
	txt = r.text
	tt =  re.search(r'name="tt" value="(.*)">',txt,re.I).group(1)

	url = 'https://www.pixiv.net/rpc/recommender.php?type=illust&sample_illusts=auto&num_recommendations=1000&page=discovery&mode=all&tt=' + tt
	res = requests.get(url,headers = headers,proxies = proxies)
	html = res.text 
	js = json.loads(html)
	List = js['recommendations']
	#print(type(List))
	D = []
	D.append(tt)
	D.append(List)
	return D

#50张图片为一页
def get_img(m = 0,n = 50,c =1):
	filepath = '/root/图片/Pixiv/Pixiv_第' + str(c) + '页' 
	os.makedirs(filepath, exist_ok = True)
	D = get_List()
	tt = D[0]
	List = D[1]
	L = len(List)
	url_part = ''
	if n<L:
		print('第 ' + str(c) + '页下载开始')
		for i in range(m,n):
			url_part = url_part + str(List[i]) + ','
		url_part = url_part.rstrip(',')
		url = 'https://www.pixiv.net/rpc/illust_list.php?illust_ids=' + url_part + '&page=discover&exclude_muted_illusts=1&tt=' + tt

		headers1 = {
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
		'Cookie':'PHPSESSID=33748554_67ef233ab30e6f85d361520e79cf17cd',
		'Referer':'https://www.pixiv.net/discovery',
		}
		proxies = {
			'https':'socks5://127.0.0.1:1080',
		}

		r = requests.get(url,headers = headers1,proxies = proxies)
		html = r.text
		js = json.loads(html)

		j = 0
		for i in js:
			j = j+1
			img = i['url']
			img_title = i['illust_title']
			img_height = i['illust_height']
			img_width  = i['illust_width']
			im = re.compile(r'/c/(\d+)x(\d+)')
			img = im.sub('',img)
			img_Info = [j,img,img_title,img_height,img_width]
			#print(img)
			download(filepath,img_Info)
		print('第 ' + str(c) + ' 页下载完成!')
		return get_img(m = m+50,n = n+50,c =c + 1)
	else:
			return

#为每张图片设置Referer头，麻蛋,真鸡儿恶心
def download(filepath,img_Info):

	session = login()
	j = img_Info[0]
	img = img_Info[1]
	img_title = img_Info[2]
	img_height  = img_Info[3]
	img_width = img_Info[4]

	#im = img.split('/')[len(img.split('/'))-1]
	ID = re.search(r'(\d{8})',img).group(1)
	Referer = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(ID)
	#print(Referer)
	headers = {
	'Referer':Referer,
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
	}
	#print(headers)
	res = session.get(img,headers = headers)
	#print(res.text)
	img_name = str(j) + '_' + img_title + '_ 长：' + img_width + ' - 宽：'+ img_height  + '.jpg'
	f = open(filepath + '/%s' % img_name,'wb')
	for chunk in res.iter_content(chunk_size = 20):
		f.write(chunk)
	print('正在下载为: ',img_name,' 的第 ',j,' 张图片')
	print('图片链接为:  ' + img)

if __name__ == '__main__':
	get_img()

