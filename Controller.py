from Domain import Sub, Media
from requests import get
from bs4 import BeautifulSoup

class CtrlEx(Exception):
	pass

baseDownLink = 'http://www.addic7ed.com'

class Controller():
	def scrapMedia(self, name):
		found = []
		searchUrl = 'http://www.addic7ed.com/search.php?search=' + str(name) + '&Submit=Search'
		p = get(searchUrl)
		soup = BeautifulSoup(p.text,'html.parser')
		for a in soup.find_all('a', debug=True):
			found.append(Media(a.text, "http://www.addic7ed.com/" + a['href']))

		if (len(found) == 0):
			raise CtrlEx("Movie or TV Show not found!")
		return found

	def scrapSubs(self, link, lang):
		found = []
		p = get(link)
		soup = BeautifulSoup(p.text, 'html.parser')

		for div in soup.find_all('div', id='container95m'):
			ver = div.find('td', class_="NewsTitle")
			if (ver != None):
				good = False
				ver = ver.text.split(',')[0].strip()
				if ver.split(' ')[0] == "Version":
					imp = div.find('img', title="Hearing Impaired")
					if (imp == None):
						imp = "Normal"
					else:
						imp = "Hearing impaired"
					lan = div.find_all('td', class_="language")
					for l in lan:
						if lang in l.text.strip():
							good = True
							link = l.find_next('a', class_="buttonDownload")
							break
					if good:
						found.append(Sub(ver, lang, imp, baseDownLink + link['href']))

		if len(found) == 0:
			raise CtrlEx("There are no subs for the selected language!")
		return found

	def downloadSub(self, name, link):
		headers = {'User-Agent': 'Mozilla/6.0'}
		r=get(link,headers)
		with open(name+".srt", "wb") as archive:
			archive.write(r.content)

def test():
	ctrl = Controller()
	a = ctrl.scrapMedia('sherlock')
	for i in a:
		print(i.name + " " + i.link)
	f = ctrl.scrapSubs('http://www.addic7ed.com/serie/Sherlock_%282010%29/3/99/The_Abominable_Bride', 'English')
	for i in f:
		print(i.getVersion() + " " + i.getLang() + " " + str(i.getImpaired()) + " " + i.getLink())


#test()