import requests
import re
import os

def get(inp, url_List = [], name_List = [], i = 1):
	url = inp + '?page=' + str(i)
	print(url)
	resp = requests.get(url)
	html = resp.text 
	#print(html)
	if '没有找到任何资源，请调整筛选条件，重新查询！' in html:
		return

	else:

		title = re.compile('svs="(.*?)"  >')
		name = re.search(title,html).group(1)
		print(name)

		Urls = re.compile('src=\'http://s.aigei.com/(.*?)\'',re.DOTALL|re.M)
		Names = re.compile('"trans-title">(.*?)</b>',re.DOTALL)
		url_List = url_List + re.findall(Urls,html)
		name_List = name_List + re.findall(Names, html)

		'''		print(url_List)
		print(name_List)
		print(len(url_List))
		print(len(name_List))'''
		download(url_List, name_List,i)
		return get(inp,url_List,name_List, i =i+1)

def download(url_List, name_List,i):
	filepath = '/root/图片/Aigei/Aigei_第' + str(i) + '页' 
	os.makedirs(filepath, exist_ok = True)
	j = 0
	for u in url_List:
		img_url = 'http://s.aigei.com/' + u
		n = name_List[j]
		r = requests.get(img_url)
		img_name = str(j) + '_' + n 
		f = open(filepath + '/%s' % img_name,'wb')
		for chunk in r.iter_content(chunk_size = 20):
			f.write(chunk)
		print('正在下载为: ' + img_name + ' 的第 ' + str(j+1) + ' 张图片')
		print('图片链接为:  ' + img_url)
		j = j+1



if __name__ == '__main__':
	inp = input('请输入你要爬的素材详情页链接：')

	clean = re.compile('#items')
	inp = clean.sub('',inp)
	print(inp)
	get(inp)

