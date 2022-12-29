import os
import sys
import psycopg2
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from g_ads.gads_process.send_email import *
from g_ads.gads_process.db_connection import *


from datetime import datetime
from datetime import timedelta
from pytz import timezone

class GADS():
    @classmethod
    def get_google_ads_data(cls,customer_id):

        try:
            data1 = db().db_creds()
            datan = dict((key, val) for k in data1 for key, val in k.items())
            cust = datan['cust_id']
            del datan['cid']
            del datan['cust_id']
            client = GoogleAdsClient.load_from_dict(config_dict=datan, version="v9")
            ga_service = client.get_service("GoogleAdsService")
            types = client.get_type('CampaignStatusEnum')
            types_2 = client.get_type('CampaignServingStatusEnum')

            format = "%Y-%m-%d"
            now_utc = datetime.now()
            now_ist = now_utc.astimezone(timezone('Asia/Kolkata'))
            yesterday = now_ist - timedelta(days=1)
            yes = yesterday.strftime(format)
            start_date12 = yes
            end_date12 = yes
            query = f"""SELECT campaign.name, metrics.clicks, campaign.id,metrics.impressions,
                    campaign.campaign_budget,  metrics.ctr,metrics.conversions, metrics.average_cpc,
                    campaign_budget.period,campaign_budget.total_amount_micros,
                    segments.date,campaign.end_date, campaign.start_date, campaign.status,
                    campaign.campaign_budget, campaign.serving_status FROM campaign
                    WHERE  segments.date >= '{start_date12}' AND segments.date <= '{end_date12}'
                    AND campaign_budget.period = 'DAILY' ORDER BY campaign.id"""

            stream = ga_service.search_stream(customer_id=str(customer_id), query=query)

            data = []
            for batch in stream:
                for row in batch.results:
                    date1 = datetime.strptime(row.segments.date, '%Y-%m-%d')
                    format = "%Y-%m-%d"
                    date2 = date1.strftime(format)
                    date3 = datetime.strptime(row.campaign.start_date, '%Y-%m-%d')
                    date4 = date3.strftime(format)
                    date5 = datetime.strptime(row.campaign.end_date, '%Y-%m-%d')
                    date6 = date5.strftime(format)
                    avg_cpc = round((row.metrics.average_cpc) / 1000000, 3)
                    ctr = round(row.metrics.ctr, 3)
                    status = (types.CampaignStatus.Name(row.campaign.status)).strip("")
                    serving_status = (types_2.CampaignServingStatus.Name(row.campaign.serving_status)).strip("")

                    rows = {
                        'Cust_id': cust,
                        'id': row.campaign.id,
                        'campaignname': row.campaign.name,
                        'daily_budget': row.campaign_budget.period,
                        'impressions': row.metrics.impressions,
                        'clicks': row.metrics.clicks,
                        'CTR': ctr,
                        'avg_cpc': avg_cpc,
                        'amount_spent': row.campaign_budget.total_amount_micros,
                        'campaign_date': date2,
                        'start_date': date4,
                        'end_date': date6,
                        'conversions': row.metrics.conversions,
                        'campaign_status': status,
                        'campaign_serving_status': serving_status

                    }
                    data.append(rows)
                    db().insert_data(list(rows.values()))

            email(data)
            db().save1()


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






