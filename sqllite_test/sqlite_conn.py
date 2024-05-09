import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path='/root/project/real_estate_onboarding.db'):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()


    def perform_query(self, query):
        """Create the onboarding table if it does not exist."""
        self.cursor.execute(query)
        self.conn.commit()

    def create_table(self):
        """Create the onboarding table if it does not exist."""
        self.perform_query("""
            CREATE TABLE IF NOT EXISTS onboarding (
                name TEXT,
                email TEXT,
                contact_number TEXT,
                address TEXT,
                ssn TEXT,
                file_path TEXT
            );
        """)
        self.conn.commit()

    def add_record(self, name, email, contact_number, address, ssn, file_path):
        """Add a new record to the onboarding table."""
        sql = '''
        INSERT INTO onboarding (name, email, contact_number, address, ssn, file_path)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        self.cursor.execute(sql, (name, email, contact_number, address, ssn, file_path))
        self.conn.commit()

    def fetch_all_records(self):
        """Fetch all records from the onboarding table."""
        query = "SELECT * FROM onboarding;"
        df = pd.read_sql_query(query, self.conn)
        return df

    def close(self):
        """Close the cursor and the database connection."""
        self.cursor.close()
        self.conn.close()
