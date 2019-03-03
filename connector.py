import psycopg2
def connect():
    """ wrapper around psycopg2 """
    db_name = 'tms'
    host = 'tms.c08i2kco4yjx.us-east-1.rds.amazonaws.com'
    port=5432
    user='masteruser'
    password="masterPassword"

    conn_string = f"host={host} dbname={db_name} user={user} password={password}"
    print(f'connecting to {db_name} on port {port}')
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('connected')

if __name__ == '__main__':
    connect()
