#run:
#scrapy runspider WebCrawler/spiders/LUME_spider.py -o output/LUME/lume.js -t json

import scrapy

urlbase = "https://lume.ufrgs.br"
class LUMEpider(scrapy.Spider):
	propriedades = ['nome','visualise','format','size']
	name = "LUME" #id do crawler

	def start_requests(self):
		urls = [
			'https://lume.ufrgs.br/browse?rpp=100&sort_by=2&type=dateissued&offset=177260&etal=-1&order=ASC'
		]
		for url in urls:
			yield scrapy.Request(url = url, callback = self.parse)

	def parse(self,response):
		for href in response.css('.artifact-title'):
			url = href.css('a::attr(href)').extract_first()+'?show=full'
			#print("URI:    "+url)
			yield response.follow(url,self.parseItem)
		proxima = response.css('.next-page-link::attr(href)').extract_first()
		if proxima is not None:
			#print("PROXIMO:    "+urlbase+proxima)
			yield response.follow(urlbase+"/"+proxima)
	def parseItem(self,response):
		
		outFilePath = "output/LUME.html"
		data = {}
		
		data['name'] = response.css(".word-break")[0].css('::attr(title)').extract_first()
		data['visualise'] = urlbase+response.css(".file-link.col-xs-6.col-xs-offset-6.col-sm-2.col-sm-offset-0")[0].css('a::attr(href)').extract_first()
		data['format'] = response.css(".word-break")[2].css('::text').extract_first()
		data['size'] = response.css(".word-break")[1].css('::text').extract_first()
		for linha in response.css(".ds-table-row"):
			campo = linha.css('td')[0].css('::text').extract_first()
			if campo not in self.propriedades:
				self.propriedades.append(campo)
			data[campo] = linha.css('td')[1].css('::text').extract_first()


		#print("\n\n\n\n")
		#print(data)
		#print("\n\n\n\n")
		#self.log('pagina %s salva !!!!!!!!!!!!!!!!!!!!!!!!!' % response.url)
		yield data
		#with open(outFilePath,"wb") as file:
		#	json.dump(data,file)


