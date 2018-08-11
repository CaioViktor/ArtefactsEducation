#run:
#scrapy runspider WebCrawler/spiders/CAPES_spider.py -o output/CAPES/capes.js -t json
#Fonte completa do material: dc.identifier
import scrapy

urlbase = "https://educapes.capes.gov.br"
class CAPESpider(scrapy.Spider):
	propriedades = []
	name = "CAPES" #id do crawler

	def start_requests(self):
		urls = [
			'https://educapes.capes.gov.br/simple-search?query=&sort_by=dc.date.available_dt&order=asc&rpp=100&etal=0&start=107400'
		]
		for url in urls:
			print(url)
			yield scrapy.Request(url = url, callback = self.parse)

	def parse(self,response):
		for href in response.css('.artifact-description'):
			url = href.css('div')[0].css("a::attr(href)").extract_first()+'?mode=full'
			#print("URI:    "+url)
			yield response.follow(url,self.parseItem)
		if len(response.css("ul.pagination.pagination-sm.pull-right li")) > 1:
			proxima = response.css("ul.pagination.pagination-sm.pull-right li")[len(response.css("ul.pagination.pagination-sm.pull-right li")) - 1].css("a::attr(href)").extract_first()
			if proxima is not None:
				#print("!!!!!!!!!!!!!!!!!!!PROXIMO:    "+urlbase+proxima)
				yield response.follow(urlbase+"/"+proxima)
	def parseItem(self,response):
		
		outFilePath = "output/CAPES.html"
		data = {}
		for linha in response.css("tr"):
			campo = ""	
			valor = ""
			for idx,val in enumerate(linha.css('td')):
				if idx == 0:
					campo = val.css('::text').extract_first()
				elif idx == 1:
					valor = val.css('::text').extract_first()
			
			if campo not in self.propriedades:
				self.propriedades.append(campo)
			if campo != "":
				data[campo] = valor


		#print("\n\n\n\n")
		#print(data)
		#print("\n\n\n\n")
		#self.log('pagina %s salva !!!!!!!!!!!!!!!!!!!!!!!!!' % response.url)
		yield data
		#with open(outFilePath,"wb") as file:
		#	json.dump(data,file)


