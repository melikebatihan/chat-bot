import requests, re, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import spacy_sentence_preprocess as ssp
import nltk_sentence_preprocess as nsp

sublinks = []
href_links = {}
website_link = "https://docs.chromasens.de"

def write_to_file(txtfile, content):        
    #Name the pdf files using the last portion of each link which are unique in this case
    filename = os.path.join(folder_location, txtfile)
    with open(filename, 'wt', encoding="utf-8") as f:
        f.write(content)

def request_links(url, root_url): 
    
    # Send an HTTP GET request to the URL
    main_page = requests.get(url)

    # Check if the request was successful (status code 200)
    if main_page.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(main_page.content, 'html.parser')

        # Find the <div class="content_block_text"> element
        content_block = soup.find_all('div', class_=['content_block_article_head', 'content_block_text'])
        
        for content in content_block:
            main_content_text = content.get_text(separator=" ", strip=True) #(separator='\n', strip=True)
            main_content_text = nsp.preprocess_doc(main_content_text)
            file = url.split("/")[-1] + ".txt"
            write_to_file(file, main_content_text)
        
        # Find all links (a elements) that point to docs
        subpages = [a.get('href').strip() for a in soup.find_all('a', href=True) if "/docs/" in a.get('href')] 
        #sublinks += [subpage for subpage in subpages if subpage not in sublinks]
        if not subpages: return
        
        for page in subpages:
            absolute_sublink = "" 
            # Append to list if new link contains original link
            if page.startswith("//docs.chromasens.de"): 
                absolute_sublink = "https:" + page
                print("Page with root url: " + page)
                
            # Include all href that do not start with website link but with "/"
            elif (page.startswith("/v1/") or page.startswith("/docs/")) and page not in href_links: 
                href_links[page] = None
                absolute_sublink = root_url + page #[1:]
                print("Page with '/': " + page)
                
            else: continue
            
            if absolute_sublink not in sublinks: 
                sublinks.append(absolute_sublink)
                request_links(absolute_sublink, root_url)
    else:
        print(f"Failed to retrieve the webpage. Status code: {main_page.status_code} - {main_page.url}")

folder_location = r'C:\Users\melike.batihan\VS_Projects\PythonProjects\VectorDB\contents'
support_emails = "\\diskstation3.chromasens.local\CSTORE3\P_new\Swap_no_backup\Rudi.Zang\Support-Postfach"

if not os.path.exists(folder_location):os.mkdir(folder_location)

request_links(website_link, website_link)

# Convert list of links to dictionary and define keys as the links and the values as "Not-checked"
dict_links = dict.fromkeys(sublinks, "Not-checked")
print("Sublinks:\n", dict_links, "\nHrefs:\n", href_links )