# import sqlite3
# 
# class Database:
#     def __init__(self, db_name):
#         self.connection = sqlite3.connect(db_name)
#         self.cursor = self.connection.cursor()
#         self.create_table()
# 
#     def create_table(self):
#         self.cursor.execute('''
#         CREATE TABLE IF NOT EXISTS project_data (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp TEXT,
#             distance1 REAL,
#             distance2 REAL,
#             distance3 REAL,
#             latitude REAL,
#             longitude REAL,
#             date TEXT
#         )
#         ''')
#         self.connection.commit()
# 
#     def add_columns(self):
#         try:
#             self.cursor.execute('''
#             ALTER TABLE project_data
#             ADD COLUMN latitude REAL
#             ''')
# 
#             self.cursor.execute('''
#             ALTER TABLE project_data
#             ADD COLUMN longitude REAL
#             ''')
# 
#             self.cursor.execute('''
#             ALTER TABLE project_data
#             ADD COLUMN date TEXT
#             ''')
# 
#             self.connection.commit()
#             print("Columns added successfully.")
#         except sqlite3.Error as e:
#             print("Error adding columns:", e)
# 
#     def insert_data(self, timestamp, distance1, distance2, distance3, latitude, longitude, date):
#         try:
#             self.cursor.execute("INSERT INTO project_data (timestamp, distance1, distance2, distance3, latitude, longitude, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                                 (timestamp, distance1, distance2, distance3, latitude, longitude, date))
#             self.connection.commit()
#             print("Data inserted successfully.")
#         except sqlite3.Error as e:
#             print("Error inserting data:", e)
# 
#     def fetch_all_data(self):
#         try:
#             self.cursor.execute("SELECT * FROM project_data")
#             rows = self.cursor.fetchall()
#             for row in rows:
#                 print(row)
#         except sqlite3.Error as e:
#             print("Error fetching data:", e)
# 
#     def fetch_all_table_names(self):
#         try:
#             self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#             tables = self.cursor.fetchall()
#             table_names = [table[0] for table in tables]
#             return table_names
#         except sqlite3.Error as e:
#             print("Error fetching table names:", e)
#             return []
# 
#     def close(self):
#         self.connection.close()
# 
# # Usage example to fetch all table names and display data:
# if __name__ == '__main__':
#     db = Database('project_data.db')
#     try:
#         table_names = db.fetch_all_table_names()
#         print("Table names:", table_names)
# 
#         print("\nData in Data table:")
#         db.fetch_all_data()
# 
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         db.close()

import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            distance1 REAL,
            distance2 REAL,
            distance3 REAL,
            latitude REAL,
            longitude REAL,
            date TEXT
        )
        ''')
        self.connection.commit()

    def add_columns(self):
        try:
            self.cursor.execute('''
            ALTER TABLE project_data
            ADD COLUMN latitude REAL
            ''')

            self.cursor.execute('''
            ALTER TABLE project_data
            ADD COLUMN longitude REAL
            ''')

            self.cursor.execute('''
            ALTER TABLE project_data
            ADD COLUMN date TEXT
            ''')

            self.connection.commit()
            print("Columns added successfully.")
        except sqlite3.Error as e:
            print("Error adding columns:", e)

    def insert_data(self, timestamp, distance1, distance2, distance3, latitude, longitude, date):
        try:
            self.cursor.execute("INSERT INTO project_data (timestamp, distance1, distance2, distance3, latitude, longitude, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (timestamp, distance1, distance2, distance3, latitude, longitude, date))
            self.connection.commit()
            self.clear_data_if_necessary()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print("Error inserting data:", e)

    def fetch_all_data(self):
        try:
            self.cursor.execute("SELECT * FROM project_data")
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print("Error fetching data:", e)

    def fetch_all_table_names(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            table_names = [table[0] for table in tables]
            return table_names
        except sqlite3.Error as e:
            print("Error fetching table names:", e)
            return []

    def clear_data_if_necessary(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM project_data")
            row_count = self.cursor.fetchone()[0]
            if row_count > 100:
                self.cursor.execute("DELETE FROM project_data")
                self.connection.commit()
                print(f"Deleted all rows to maintain 100 rows.")
        except sqlite3.Error as e:
            print("Error deleting all rows:", e)

    def close(self):
        self.connection.close()

# Usage example to fetch all table names and display data:
if __name__ == '__main__':
    db = Database('project_data.db')
    try:
        table_names = db.fetch_all_table_names()
        print("Table names:", table_names)

        print("\nData in Data table:")
        db.fetch_all_data()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

