import scrapy

urlbase = "http://objetoseducacionais2.mec.gov.br"
class BIOESpider(scrapy.Spider):
	propriedades = ['download','visualise','format','size']
	name = "BIOE" #id do crawler

	def start_requests(self):
		urls = [
			'http://objetoseducacionais2.mec.gov.br/browse?order=ASC&rpp=100&sort_by=1&page=1&etal=-1&type=title'
		]
		for url in urls:
			yield scrapy.Request(url = url, callback = self.parse)

	def parse(self,response):
		for href in response.css('.ds-table-row'):
			url = href.css('td')[2].css('a::attr(href)').extract_first()+'?show=full'
			#print(url)
			yield response.follow(url,self.parseItem)
		proxima = response.css('.next-page-link::attr(href)').extract_first()
		if proxima is not None:
			print(urlbase+proxima)
			yield response.follow(urlbase+"/"+proxima)
	def parseItem(self,response):
		
		outFilePath = "output/BIOE.html"
		data = {}
		
		data['download'] = urlbase+response.css("#metadata-download a::attr(href)").extract_first()
		data['visualise'] = urlbase+response.css("#file-list-ficha-tecnica tr")[1].css('td')[0].css('a::attr(href)').extract_first()
		data['format'] =response.css("#file-list-ficha-tecnica tr")[1].css('td')[3].css('::text').extract_first()
		data['size'] = response.css("#file-list-ficha-tecnica tr")[1].css('td')[2].css('::text').extract_first()
		for linha in response.css(".ds-table-row-metadados"):
			campo = linha.css('td')[0].css('span::text').extract_first()
			if campo not in self.propriedades:
				self.propriedades.append(campo)
			data[campo] = linha.css('td')[1].css('::text').extract_first()


		#print("\n\n\n\n")
		#print(data)
		#print("\n\n\n\n")
		yield data
		#with open(outFilePath,"wb") as file:
		#	json.dump(data,file)

		self.log('pagina %s salva' % response.url)

