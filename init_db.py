import sqlite3

def init_db():
    try:
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
            
        cursor.executescript(schema_sql)
        
        conn.commit()
        print("Database initialized successfully (hospital.db)!")
        conn.close()
        
    except Exception as e:
        print(f"Error initializing DB: {e}")

if __name__ == '__main__':
    init_db()
