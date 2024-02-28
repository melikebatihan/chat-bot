import requests, re, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import spacy_sentence_preprocess as ssp
import nltk_sentence_preprocess as nsp

class WebScrape:
    def __init__(self, website_link, folder_location=''):
        self.folder = folder_location
        if self.folder and not os.path.exists(folder_location): os.mkdir(folder_location)
        
        self.rootUrl = website_link
        self.url = website_link
        self.sublinks = []
        self.href_links = {}
        self.contents = []

    def write_to_file(self, txtfile, content):        
        #Name the pdf files using the last portion of each link which are unique in this case
        filename = os.path.join(self.folder, txtfile)
        with open(filename, 'wt', encoding="utf-8") as f:
            f.write(content)

    def request_content(self):   
        # Send an HTTP GET request to the URL
        main_page = requests.get(self.url)

        # Check if the request was successful (status code 200)
        if main_page.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(main_page.content, 'html.parser')

            # Find the <div class="content_block_text"> element
            content_block = soup.find_all('div', class_=['content_block_article_head', 'content_block_text'])
        
            for content in content_block:
                main_content_text = content.get_text(separator=" ", strip=True) #(separator='\n', strip=True)
                main_content_text = nsp.preprocess_doc(main_content_text)
            
                # Write the content in a file or save in the contents list
                if self.folder: 
                    file = self.url.split("/")[-1] + ".txt"
                    self.write_to_file(file, main_content_text)
                
                self.contents.append(main_content_text)
                print(self.contents)
            # Find all links (a elements) that point to docs
            subpages = [a.get('href').strip() for a in soup.find_all('a', href=True) if "/docs/" in a.get('href')] 
            #sublinks += [subpage for subpage in subpages if subpage not in sublinks]
            if not subpages: return
        
            for page in subpages:
                absolute_sublink = "" 
                # Append to list if new link contains original link
                if page.startswith(self.rootUrl[6:]):  #"//docs.chromasens.de"): 
                    absolute_sublink = "https:" + page
                    #print("Page with root url: " + page)
                
                # Include all href that do not start with website link but with "/"
                elif (page.startswith("/v1/") or page.startswith("/docs/")) and page not in self.href_links: 
                    self.href_links[page] = None
                    absolute_sublink = self.rootUrl + page #[1:]
                   # print("Page with '/': " + page)
                
                else: continue
            
                if absolute_sublink not in self.sublinks: 
                    self.sublinks.append(absolute_sublink)
                    self.url = absolute_sublink
                    self.request_content()
        else:
            print(f"Failed to retrieve the webpage. Status code: {main_page.status_code} - {main_page.url}")
