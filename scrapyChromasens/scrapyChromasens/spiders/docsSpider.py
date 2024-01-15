import scrapy, os, requests

class DocsChromasens(scrapy.Spider):
    name = 'chromasens'
    start_urls = ["https://docs.chromasens.de/"]
    
    # Constructor or initializer method
    def __init__(self):
        self.folder_location = r'C:\Users\melike.batihan\VS_Projects\PythonProjects\VectorDB\pdfs'
        self.checked_urls = []

    def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            post_link = response.urljoin(link)
            
            if post_link.lower().endswith(".pdf"): yield self.save_pdf(post_link)
            
            elif post_link not in self.checked_urls and "docs.chromasens" in post_link:    
                self.checked_urls.append(post_link)
                yield scrapy.Request(post_link, callback=self.parse)
            
    def save_pdf(self, url):        
        if not os.path.exists(self.folder_location):os.mkdir(self.folder_location)
        #Name the pdf files using the last portion of each link which are unique in this case
        filename = os.path.join(self.folder_location, url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(requests.get(url).content)