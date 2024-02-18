import sqlite3
import csv
import os

class CreateVectorDB:
    def __init__(self,csvfilename='./data/data.csv',dbfilename='./db/vector.db'):
        self.csvfilename = os.path.join('data',csvfilename)
        self.dbfilename = dbfilename
        
    def __enter__(self):
        # Initialization code
        return self
        
    def createDb(self):
        # Create a connection to the SQLite database
        conn = sqlite3.connect(self.dbfilename)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Read CSV and create a table in SQLite
        with open(self.csvfilename, 'r',encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # Assuming the first row in the CSV contains column headers
            headers = next(csv_reader)
            
            # Delete the table if already exists
            cursor.execute('DROP TABLE IF EXISTS data;')
            
            # Create a table in SQLite using the headers
            cursor.execute(f"CREATE TABLE IF NOT EXISTS data ({', '.join(headers)});")
            
            # Insert data into the table
            for row in csv_reader:
                cursor.execute(f"INSERT INTO data VALUES ({', '.join(['?']*len(row))})", row)

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print(f'Vector DB created! in {self.dbfilename}')
    
    def query(self,query='select * from data;'):
        # Create a connection to the SQLite database
        conn = sqlite3.connect(self.dbfilename)
        
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        results=cursor.fetchall()
        
        conn.commit()
        conn.close()
        
        return results
    
    def __exit__(self,exc_type, exc_value, traceback):
        print("DB Obj is destroyed")