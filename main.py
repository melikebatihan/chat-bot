from numpy import insert
import WebScrape as ws
import VectorEmbeddings as ve
import EmailFiltering as ef
import sql_database as db

# Scrape the website
web_link = "https://docs.chromasens.de"
website_content_folder = r'c:\users\melike.batihan\vs_projects\pythonprojects\vectordb\contents'
scraper = ws.webscrape(web_link, website_content_folder)
scraper.request_content()

# Preprocess emails and add them into the database
email_folder = 'P:\Swap_no_backup\Rudi.Zang\Support-Postfach\Success'
email_contents = ef.filter_emails(email_folder)

conn = db.connect_and_create_table()

for content in email_contents:
    embedding = ve.encode_text(content[0])
    db.insert_data(conn, (content[0], content[1], content[2]))

db.write_to_csv(conn)
conn.close()
