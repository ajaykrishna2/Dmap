from datetime import datetime, timedelta
import os
import sys
import psycopg2
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from g_ads4.send_email import *
from g_ads4.ga_db import *
# from g_ads.gdate import *
import ast
import pandas as pd
from datetime import date
from datetime import datetime
from datetime import timedelta
from pytz import timezone

from email.mime.base import MIMEBase
from email import encoders
import configparser


conn = psycopg2.connect(database="dmap", user='postgres', password='ajay@123', host='127.0.0.1', port='5432')
cur = conn.cursor()



sql1 = '''SELECT * FROM gads.gads_customer''';
cur.execute(sql1)
db_data = cur.fetchall()
print(db_data)
data=[el for e in db_data for el in e]
cid=data[0]

sql2 = '''SELECT * FROM gads.gads_connection''';
cur.execute(sql2)
db_data1 = cur.fetchall()
print(db_data1)
data1=[el for e in db_data1 for el in e]
print(data1[1])
data2=ast.literal_eval(data1[2])
print(data2)

config_dict = {
    "developer_token": data1[1],
    "use_proto_plus": data2,
    "client_id": data1[3],
    "client_secret": data1[4],
    "refresh_token": data1[5],
    "login_customer_id": data1[6]
    }

client = GoogleAdsClient.load_from_dict(config_dict=config_dict,version="v9")


def cumulative_date():
    start_date = date(2022, 1, 1)
    end_date = date(2022, 3, 9)
    delta = timedelta(days=1)
    data = []
    while start_date <= end_date:
        data.append(str(start_date))
        start_date += delta
    return data

def time_date():
    format = "%Y-%m-%d"
    now_utc = datetime.now()
    now_ist = now_utc.astimezone(timezone('Asia/Kolkata'))
    Ist = now_ist.strftime(format)
    yesterday = now_ist - timedelta(days=1)
    yes = yesterday.strftime(format)
    return [yes, Ist]

def get_google_ads_data(customer_id):

    try:
        ga_service = client.get_service("GoogleAdsService")

        # start_date1 = str(input('Enter start date(yyyy-mm-dd): '))
        # start_date11 = datetime.strptime(start_date1, "%Y-%m-%d")
        # start_date12 = start_date11.strftime('%Y-%m-%d')
        # end_date1 = str(input('Enter end date(yyyy-mm-dd): '))
        # end_date11 = datetime.strptime(end_date1, "%Y-%m-%d")
        # end_date12 = end_date11.strftime('%Y-%m-%d')
        create_schema()
        create_table()
        conn.commit()
        # conn.close()list(rows.values())
        # conn.rollback()
        # cur = conn.cursor()
        # sql4 = '''SELECT * FROM gads.gads_raw_data''';
        # cur.execute(sql4)
        # db_data3 = cur.fetchall()
        # print(db_data3)

        format = "%Y-%m-%d"
        now_utc = datetime.now()
        now_ist = now_utc.astimezone(timezone('Asia/Kolkata'))
        Ist = now_ist.strftime(format)
        yesterday = now_ist - timedelta(days=1)
        yes = yesterday.strftime(format)
        start_date = now_ist - timedelta(days=180)
        start=start_date.strftime(format)
        # print(type(yes))
        # print(Ist)
        start_date12 = yes
        end_date12 = yes
        start_date12 = yes
        end_date12 = yes



        query = f"""
                    SELECT campaign.name, metrics.clicks, campaign.id,metrics.impressions,
                     campaign.campaign_budget,  metrics.ctr, metrics.average_cpc,
                     campaign_budget.period,campaign_budget.total_amount_micros,
                     segments.date,segments.month,campaign.end_date, campaign.start_date, campaign.status,
                     campaign.base_campaign, campaign.bidding_strategy, campaign.bidding_strategy_type,
                     campaign.campaign_budget, campaign.experiment_type, campaign.payment_mode, campaign.resource_name, 
                     campaign.serving_status, bidding_strategy.currency_code, bidding_strategy.name, bidding_strategy.type, 
                     campaign_budget.type FROM campaign
                    WHERE  segments.date >= '{start_date12}' AND segments.date <= '{end_date12}' AND campaign_budget.period = 'DAILY'   ORDER BY campaign.id"""
        # Issues a search request using streaming.
        stream = ga_service.search_stream(customer_id=str(customer_id), query=query)
        # start_date111 = date(2022, 1, 1)
        # end_date111 = date(2022, 3, 9)
        # print(start_date111)
        # delta = timedelta(days=1)
        # data6 = []
        # while start_date111 <= end_date111:
        #     data6.append(str(start_date111))
        #     start_date111 += delta
        # return data6
        # print(start_date111)

        for batch in stream:
            for row in batch.results:
                # c_date(row.segments.date, row.campaign.start_date, row.campaign.end_date)
                date1 = datetime.strptime(row.segments.date, '%Y-%m-%d')
                format = "%Y-%m-%d"
                # print(datetime.date1.weekday())
                date2 = date1.strftime(format)
                date3 = datetime.strptime(row.campaign.start_date, '%Y-%m-%d')
                date4 = date3.strftime(format)
                date5 = datetime.strptime(row.campaign.end_date, '%Y-%m-%d')
                date6 = date5.strftime(format)
                # print(type(date1))
                avg_cpc=round((row.metrics.average_cpc) / 1000000,3)
                # df['week_number_of_year'] = df['date_given'].dt.week


                print(

                        f"Campaign with ID {row.campaign.id} and name "
                        f'"{row.campaign.name}" was found.'
                        f"With Clicks :- {row.metrics.clicks} and impressions:- "
                        f'"{row.metrics.impressions}" was found.'
                        f'"{(row.metrics.average_cpc) / 1000000}" with average cpc'
                        f'"{row.metrics.ctr}" and with ctr'
                        f'"{row.segments.date}" and with date'
                        f'"{row.campaign_budget.period}" and with Daily budget '
                        f'"{row.campaign_budget.total_amount_micros}" and Amount Spent'
                        f'"{row.segments.date}" and with date'
                        f'"{row.campaign.start_date}" and with start date'
                        f'"{row.campaign.end_date}" and with end date'
                    )

                rows = {
                    'Client_id':cid,
                    'id': row.campaign.id,
                    'campaignname': row.campaign.name,
                    'daily_budget': row.campaign_budget.period,
                    'impressions': row.metrics.impressions,
                    'clicks': row.metrics.clicks,
                    'CTR': row.metrics.ctr,
                    'avg_cpc': avg_cpc,
                    'amount_spent': row.campaign_budget.total_amount_micros,
                    'date1': date2,
                    'start_date': date4,
                    'end_date': date6
                    # 'Status':row.campaign.status,
                    # 'base_campaign':row.campaign.base_campaign,
                    # 'c_bidding_strategy':row.campaign.bidding_strategy,
                    # 'c_bidding_strategy_type':row.campaign.bidding_strategy_type,
                    # 'campaign_budget':row.campaign.campaign_budget,
                    # 'experiment_type':row.campaign.experiment_type,
                    # 'payment_mode':row.campaign.payment_mode,
                    # 'resource_name':row.campaign.resource_name,
                    # 'serving_status':row.campaign.serving_status,
                    # 'currency_code':row.bidding_strategy.currency_code,
                    # 'b_name':row.bidding_strategy.name,
                }
                # print(list(rows.values()))
                insert_data(list(rows.values()))
                # cur.execute(
                #     "INSERT INTO gads.gads5(Client_id,campaignname,daily_budget,clicks,id,impressions,ctr,avg_cpc,amount_spent,date,start_date,end_date) VALUES (%s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s,)",
                #     (data[0],rows['campaignname'],rows['daily_budget'],rows['clicks'], rows['id'],rows['impressions'],rows['CTR'],
                #      rows['avg_cpc'],rows['amount_spent'],rows['date1'],rows['start_date'],rows['end_date']))

        # print("data inserted to db")
        email()
        save()


    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)


if __name__ == "__main__":
    get_google_ads_data(cid)


