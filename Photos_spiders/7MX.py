#coding=utf-8
import requests
import json
import os
import sys
import re


headers = {
'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':	'gzip, deflate',
'Accept-Language':	'en-US,en;q=0.5',
'Connection':	'keep-alive',
'Host':	'api.7mx.com',
'Upgrade-Insecure-Requests':	1,
'User-Agent':	'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
}
def download(i):
	filepath = '/root/图片/7MX/7MX_第' + str(i + 1) + '页' 
	os.makedirs(filepath, exist_ok = True)
	url = 'http://api.7mx.com/media/category_recommend_list?line=' + str(i) + ',0,0&limit=40'
	r = requests.get(url)
	r.headers = headers
	r.coding = 'utf-8'
	html = r.text
	j = json.loads(html)
	data = j['data']
	control = j['msg']
	if control == '':
		print('第 ' + str(i + 1) + '页下载开始')
		j = 1
		for ID in data:
			img_url = ID['image']
			title = ID['title']
			image_height = ID['image_height']
			image_width  = ID['image_width']
			img_name = str(j) + '_' + title + '_ 长：' + image_width + ' - 宽：'+ image_height  + '.jpg'
			r_name = re.compile('\/',re.M)
			img_name = r_name.sub('-',img_name)
			res = requests.get(img_url)
			res.headers = headers
			f = open(filepath + '/%s' % img_name,'wb')
			for chunk in res.iter_content(chunk_size = 20):
				f.write(chunk)
			print('正在下载为: ',img_name,' 的第 ',j,' 张图片')
			j = j+1
			print('图片链接为:  ' + img_url)
		print('第 ' + str(i + 1) + ' 页下载完成!')


	else:
		print('全部下载完成!')
		sys.exit()
		
	return download(i+1)
if __name__ == '__main__':
	i = 0
	download(i)