


class Sub():
	def __init__(self, version, language, impaired, link):
		self.version = version
		self.language = language
		self.impaired = impaired
		self.link = link

	def getVersion(self):
		return self.version

	def getLang(self):
		return self.language

	def getImpaired(self):
		return self.impaired

	def getLink(self):
		return self.link

class Media():
	def __init__(self, name, link):
		self.name = name
		self.link = link

	def getName(self):
		return self.name

	def getLink(self):
		return self.link