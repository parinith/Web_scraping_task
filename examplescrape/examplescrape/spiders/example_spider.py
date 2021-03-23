import scrapy


class ExampleScrapy(scrapy.Spider):
    name = "example"
    page_number = 2
    start_urls = [
    "https://www.houseofindya.com/zyra/cat?depth=1&label=jewelry&page=1"

    ]


    def parse(self, response):
        l = []
        for post in response.css('div.catgNamer'):
            url = post.css('.catgList ul li::attr(data-url)').getall()
            print("url =",len(url))
            c =0
            for i in url:
                if response.urljoin(i):
                    u = response.urljoin(i)
                    d = scrapy.Request(u, callback=self.parse_page2)
                    yield d

            next_page = "https://www.houseofindya.com/zyra/cat?depth=1&label=jewelry&page="+str(self.page_number)
            print(next_page)
            if self.page_number <= 8:
                 self.page_number+=1
                 yield scrapy.Request(next_page, callback=self.parse)

    def remove_html_tags(self,text):
        import re
        clean = re.compile('<.*?>')
        s = re.sub(clean, '', text)
        s = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]","",s)
        return  s

    def parse_page2(self, response):
        name  = response.css(".prodRight h1::text")[0].get()
        price = response.css('.prodRight h4 span::text')[1].get()
        price = int(price.strip())
        description = response.css('.prodecbox p')[1].get()
        description = self.remove_html_tags(description)
        image_urls = response.css(".sliderBox li a img::attr(data-original)").getall()
        dic = {
                'name' : name,
                'price' : price,
                'description' : description,
                'image_urls' : image_urls
        }
        yield dic
