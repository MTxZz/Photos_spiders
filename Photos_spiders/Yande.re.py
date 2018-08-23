import requests
import re
import os
import sys

#def get_img(inp,i=1):      #--递归下载全部，不适用，作罢
def get_img(i,inp):
	url = 'https://yande.re/post?page=' + str(i)
	headers = {
	'Cookie':'vote=1; __utma=5621947.1110434715.1534651010.1534651010.1534654962.2; __utmz=5621947.1534651010.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); forum_post_last_read_at=%222018-08-19T05%3A59%3A05.389%2B02%3A00%22; country=GB; yande.re=aXlneitVbm9rNmpPb1B5UkF0Sm82RVNxdlhJdTRLd1BFVTlQU3BnMkZRLzMrRXpvRGh4eG9XaG5idFhPMDJONGxQTUk0b0wzQWhYZWhFd0VUYWtDQkZDa1pWSExMNW1CRlVSdkZqbjEwMUNoOWdXMVFSZnplRENCQ3BXaDBIRmJnNlZBdkRYUldFYTVJdWF0WUJvb0dBPT0tLTB3TThNL2gxcUJ3RXFMNDNmVjF2eWc9PQ%3D%3D--243eb9616bd0ac621b45ecbf1cd1fc772bd5d4f7; __utmc=5621947; __utmb=5621947.1.10.1534654962; __utmt=1',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	}
	resp = requests.get(url,headers = headers)
	html = resp.text
	#print(html
	I = re.compile(r'id="p(\d+)"')
	ID = re.findall(I,html)
	j = 1
	print('第 ' + str(i) + '页下载开始')
	for d in ID:
		get_img_Info(i,j,d,inp)
		j = j+1
	print('第 ' + str(i) + ' 页下载完成!')
	#return get_img(inp,i = i+1)       #--递归下载全部，不适用，作罢

def get_img_Info(i,j,ID,inp):
	url = 'https://yande.re/post/show/' + str(ID)
	headers = {
	'Referer':'https://yande.re/post',
	'Cookie':'vote=1; __utma=5621947.1110434715.1534651010.1534651010.1534654962.2; __utmz=5621947.1534651010.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); forum_post_last_read_at=%222018-08-19T07%3A25%3A32.479%2B02%3A00%22; country=GB; yande.re=VVJ5M2NIR2RHUHYyQlNQSnpmeEo1SHVNYTAvVHhrd3o3TjdqbmVKUkd4SVg1L0YyMHV4YldRUUhqd1N5RTRMeXBhZnF4L3dFRFF4MVhzVko0OWljZW1ZTzA1eS9yZTlKTzJ4SnA3M2hsaGZpWmo3WFZqYkpVWlZ1aFFNWEJBOXFsTjd1SGlQS3drbEVieXAvd3VrSHhRPT0tLVdvS040ckRuV0dYVWd1YmE1aDlFTFE9PQ%3D%3D--376c66df7181047078f8390db27aac1b1fc9e11b; __utmc=5621947; __utmb=5621947.1.10.1534654962',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	}
	resp = requests.get(url,headers = headers)
	html = resp.text
	image_S = re.compile('src="(.*)(.jpg)"')
	image_title = re.compile('<title>(.*?)</title>',re.DOTALL|re.M)

	#img_S　是适当大小的图，质量适中
	img_S = re.search(image_S,html).group(1) + re.search(image_S,html).group(2)
	img_title = re.search(image_title,html).group(1)

	clean = re.compile('/',re.DOTALL)
	img_title = clean.sub('-',img_title)

	if inp == 'ss':
		width_S = re.compile('width="(\d+)"')
		height_S = re.compile('height="(\d+)"')
		w_S = re.search(width_S,html).group(1)
		h_S = re.search(height_S,html).group(1)

		img_List_1 = [j,img_S,img_title,h_S,w_S,i]
		download(img_List_1)

	else:
		width_L = re.compile('large_width="(\d+)"')
		height_L = re.compile('large_height="(\d+)"')
		w_L = re.search(width_L,html).group(1)
		h_L = re.search(height_L,html).group(1)
		#img_L 是原图，质量超好
		im = img_S.replace('sample ','bikini%20cleavage')
		img = im.replace('sample','image')
		img_L = img.replace('wet','tagme')

		img_List_2 = [j,img_L,img_title,h_L,w_L,i]
		download(img_List_2)


def download(img_Info):
	j = img_Info[0]
	img = img_Info[1]
	img_title = img_Info[2]
	img_height  = img_Info[3]
	img_width = img_Info[4]
	i = img_Info[5]

	filepath = '/root/图片/Yande.re/Yande_第' + str(i) + '页' 
	os.makedirs(filepath, exist_ok = True)
	headers = {
	'Referer':'https://yande.re/',
	'Cookie':'__utma=5621947.1110434715.1534651010.1534651010.1534654962.2; __utmz=5621947.1534651010.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); yande.re=YTJKZ0JIRDBWNi93RVBLck5iV3VkTGhzMURjTjVwamNTc3VVa2x0OXlJS1pKRFVPNlhSMlhZekVrSmgxTEJ6R3lOWU5ReTduWkhMVzRPSjZLVzdiRWNEMytQcEJ0aGVZcTZVazZvTDdUWFVjTDlqMXdwVEdUaU5jYVRCTGc5RXJ4QVlvbTYvWHdmSWRTbXhEQ3pXczVnPT0tLU5mUHI1cnVHYWVYaU4zV08xemNPQmc9PQ%3D%3D--7e8d7be49fad6c358f5123feda5151d565321d77; __utmc=5621947; __utmb=5621947.1.10.1534654962',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
	}
	res = requests.get(img,headers = headers)

	img_name = str(j) + '_' + img_title + '_ 长：' + img_width + ' - 宽：'+ img_height  + '.jpg'
	f = open(filepath + '/%s' % img_name,'wb')
	for chunk in res.iter_content(chunk_size = 200):
		f.write(chunk)
	print('正在下载为: ',img_name,' 的第 ',j,' 张图片')
	print('图片链接为:  ' + img)

#网站图片页数大约2000页,由于图片页数太多，这里我不加入递归下载图片了，各位自己选择要下载的页数，自行替换i吧
if __name__ == '__main__':
	inp = input('下载原图请输入：ll/下载高清图请输入：ss(注：高清图质量已经很不错，原图非常大,强烈不建议下载原图，网站炸了)')
	if inp == 'll':
		print('将为您下载原图')
	elif inp == 'ss':
		print('将为您下载高清图')
	else:
		print('你他妈在逗我,下次记得输入ll/ss')
		sys.exit()
	i = input('你想下载第几页的图片？')
	get_img(i,inp)
