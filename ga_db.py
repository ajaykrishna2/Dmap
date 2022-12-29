
import psycopg2

conn = psycopg2.connect(database="dmap", user='postgres', password='ajay@123', host='127.0.0.1', port='5432')
cur = conn.cursor()

def create_schema():
    sql2 = '''CREATE SCHEMA IF NOT EXISTS gads;'''
    print('hi')
    cur.execute(sql2)
def create_table():
    sql1 = '''CREATE TABLE IF NOT EXISTS gads.gads_raw_data(
            Cust_id text,
            id float, 
            campaignname text,
            daily_budget integer,
            impressions integer,
            clicks integer,
            ctr	float,
            avg_cpc	float,
            amount_spent integer,
            date1 date,
            s_date date,
            e_date date,
            CONSTRAINT fk_client FOREIGN KEY(Cust_id) REFERENCES gads.gads_customer(Cust_id)
            );''';

    cur.execute(sql1)
    print('hi')
    # print()
def insert_data(i):
    cur.execute("INSERT INTO gads.gads_raw_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)",i)
    print(i)
    print("data ins")

def save():
    conn.commit()
    conn.close()