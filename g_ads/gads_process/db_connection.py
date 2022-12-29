import os
import psycopg2
import logging
import configparser
configuration_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuration_path)
HOST = config['postgresql']['HOST']
PORT = config['postgresql']['PORT']
DATABASE = config['postgresql']['DB']
USER = config['postgresql']['USER']
PASSWORD = config['postgresql']['PASSWORD']
conn = psycopg2.connect(user=USER,
                              password=PASSWORD,
                              host=HOST,
                              port=PORT,
                              database=DATABASE)

cur = conn.cursor()




class db():


    @classmethod
    def db_creds(cls):
        try:
            sql2 = '''SELECT * FROM dmap_entsm.gads_connection''';
            cur.execute(sql2)
            db_data1 = cur.fetchall()
            data1 = [el for e in db_data1 for el in e]
            data2 = []
            config_dict ={"cust_id":data1[0],
            "cid": data1[1],
            "developer_token": data1[2],
            "use_proto_plus": data1[3],
            "client_id": data1[4],
            "client_secret": data1[5],
            "refresh_token": data1[6],
            "login_customer_id": data1[7]
            }
            data2.append(config_dict)
            return data2
        except Exception as e:
            logging.exception(e)


    @classmethod
    def insert_data(cls,i):
        try:
            cur.execute("INSERT INTO dmap_entsm.gads_rawdata(cust_id ,campaign_id ,campaign_name,daily_budget,impressions ,clicks ,ctr ,avg_cpc ,amount_spent ,campaign_date ,start_date ,end_date ,conversions ,campaign_status,campaign_serving_status ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)",i)
        except Exception as e:
            logging.exception(e)


    @classmethod
    def save1(cls):
        try:
            conn.commit()
            conn.close()
        except Exception as e:
            logging.exception(e)
