import os
import requests
from bs4 import BeautifulSoup

primURL = 'http://phdcomics.com/comics.php' 
inicioUrl = 'http://phdcomics.com/'
MAX = 5

def pastas():
	if not(os.path.isdir("phd")):	
		try:
			os.mkdir("phd")
		except Exception, e:
			raise e

def getHtml(primURL):
	html = requests.get(primURL)
	return html.text

def DownloadUrl(url):
	resposta = requests.get(url)
	if resposta.status_code == 200:
		nome = "phd/"+ str(MAX)
		f = open(nome, 'wb')
		f.write(resposta.content)
		f.close()

def sopa(Html):
	global MAX
	global inicioUrl
	soup = BeautifulSoup(Html,"lxml")
	tag = soup.find(id='comic')
	urlDown = tag['src']
	DownloadUrl(urlDown)

	#pega a proxima pagina
	prox = ""
	listaUrls = []
	for a in soup.find_all('a', href=True):
		if 'php?comicid' in a['href']: 
			listaUrls.append( a['href'] )
	prox = listaUrls[2]
	
	return prox

def limpaPasta():
	arq = os.listdir('phd')
	for i in range(len(arq)):
		os.remove('phd/'+arq[i])

def programa():
	pastas()
	limpaPasta()
	global MAX
	global primURL
	nextHtml = "http://www.phdcomics.com/" + sopa(getHtml(primURL))
	while MAX >= 1:
		print(".")
		nextHtml = "http://www.phdcomics.com/comics/" + sopa(getHtml(nextHtml))
		MAX -= 1
	print("tirinhas atualizadas, 1 para mais antiga, 5 para mais recente.")

programa()