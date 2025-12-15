import mysql.connector
import os

def get_db_connection():
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        return mysql.connector.connect(
            host=os.environ.get('MYSQLHOST'),
            user=os.environ.get('MYSQLUSER'),
            password=os.environ.get('MYSQLPASSWORD'),
            database=os.environ.get('MYSQLDATABASE'),
            port=os.environ.get('MYSQLPORT')
        )
    else:

        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='PaDaK123@$$',
            database='NewFinalsdb'
        )

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

if __name__ == "__main__":
    conn = get_db_connection()
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"You are connected to database: {record[0]}")
            
            cursor.execute("SELECT * FROM INDUSTRY LIMIT 5;")
            rows = cursor.fetchall()
            print("\nIndustry Table Data:")
            for row in rows:
                print(row)
                
        except Error as e:
            print(f"Query failed: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            close_connection(conn)
