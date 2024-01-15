import requests, PyPDF2, re
from bs4 import BeautifulSoup

def get_pdf_links(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links (a elements) that point to PDF files
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

        return pdf_links
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    

def download_and_read_pdf(pdf_url, output):
    # Send an HTTP GET request to download the PDF file
    response = requests.get(pdf_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the PDF content to a local file
        with open(output, 'wb') as file:
            file.write(response.content)

        # Extract text from the downloaded PDF
        pdf_text = read_pdf(output)

        # Print or process the extracted text as needed
        print(pdf_text)
    else:
        print(f"Failed to download the PDF. Status code: {response.status_code}")

def read_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(file)

        # Extract text from each page
        pdf_text = ""
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()

    return pdf_text


url = "https://docs.chromasens.de/"

# Get PDF links from the webpage
pdf_links = get_pdf_links(url)

if pdf_links:
    # Loop through each PDF link and download text
    for i, pdf_link in enumerate(pdf_links, start=1):
        # Extract the file name from the pdf link
        link = re.search(r"([^/]+)\.pdf$", pdf_link).group(1);
        output_filename = f"{link}.pdf"
        download_and_read_pdf(pdf_link, output_filename)
else:
    print("No PDF links found on the webpage.")






