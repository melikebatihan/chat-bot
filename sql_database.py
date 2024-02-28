import sqlite3, csv

def connect_and_create_table(db_path='chatbot_data.db'):
 
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    db_cur = conn.cursor()

    #db_cur.execute("DROP TABLE IF EXISTS emails")

    db_cur.execute('''CREATE TABLE IF NOT EXISTS emails (
                   Data TEXT,
                   Language TEXT,
                   Link TEXT, 
                   UNIQUE(Data)
                   )
    ''')
    conn.commit()
    return conn


def insert_data(conn, data):
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO emails (Data, Language, Link) VALUES (?, ?, ?)', data);
    conn.commit()

def write_to_csv(conn):
    cur = conn.cursor()
    csv_file_path = 'emails.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header (optional, but recommended)
        #cursor.execute("PRAGMA table_info(my_table)")
        columns = ["Data", "Language", "Link"]
        csv_writer.writerow(columns)
        
        # Write the rows
        for row in cur.execute("SELECT Data, Language, Link FROM emails"): 
            print(row)
            csv_writer.writerow(row)
        