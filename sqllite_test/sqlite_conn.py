import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path):
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
                f_name TEXT,
                l_name TEXT,
                m_name TEXT,
                email TEXT,
                h_number TEXT,
                a_number TEXT,
                s_address TEXT,
                apt TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                b_date TEXT,
                ssn TEXT,
                file_path TEXT
            );
        """)
        self.conn.commit()

    def add_record(self, f_name, l_name, m_name, email, h_number, a_number, s_address, apt, city, state, zip, b_date, ssn, file_path):
        """Add a new record to the onboarding table."""
        sql = '''
        INSERT INTO onboarding (f_name, l_name, m_name, email, h_number, a_number, s_address, apt, city, state, zip, b_date, ssn, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        self.cursor.execute(sql, (f_name, l_name, m_name, email, h_number, a_number, s_address, apt, city, state, zip, b_date, ssn, file_path))
        self.conn.commit()

    def fetch_all_records(self):
        """Fetch all records from the onboarding table."""
        query = "SELECT f_name AS 'First Name', l_name AS 'Last Name', email AS 'Email', city AS 'City', file_path FROM onboarding;"
        df = pd.read_sql_query(query, self.conn)
        return df

    def fetch_record(self, file_path):
        """Fetch all records from the onboarding table."""
        query = "SELECT * FROM onboarding WHERE file_path=?;"
        df = pd.read_sql_query(query, self.conn, params=(file_path,))
        return df
    
    def delete_record_by_session_id(self, file_path):
        """Delete a record from the onboarding table by file path."""
        print(file_path)
        sql = 'DELETE FROM onboarding WHERE file_path = ?'
        self.cursor.execute(sql, (file_path,))
        self.conn.commit()


    def close(self):
        """Close the cursor and the database connection."""
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db = DatabaseManager("real_estate_onboarding.db")
    print(db.fetch_all_records().to_string())
    # print(f"{db.fetch_record('/Users/amitshendge/Documents/project-onboarding-forms/output_files/op/49e0cc0a-9fc8-41ac-9969-1e1c6670b1a5').to_dict()}")
    print(db.fetch_record('').to_dict())
    db.close()