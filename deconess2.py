import logging

import openpyxl
import pandas as pd

def Deaconess(writer):
    try:
        all_dfs1 = pd.read_excel('/home/ajay/Downloads/April/deaconess_dsp.xlsx', sheet_name=None)
        df1 = pd.concat(all_dfs1, ignore_index=True)
        all_dfs2 = pd.read_excel('/home/ajay/Downloads/April/deaconess_gibson.xlsx', sheet_name=None)
        df2 = pd.concat(all_dfs2, ignore_index=True)
        all_dfs3 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_heart.xlsx', sheet_name=None)
        df3 = pd.concat(all_dfs3, ignore_index=True)
        all_dfs4 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_sys.xlsx', sheet_name=None)
        df4 = pd.concat(all_dfs4, ignore_index=True)
        all_dfs5 = pd.read_excel('/home/ajay/Downloads/April/deaconess_heart_hospital.xlsx', sheet_name=None)
        df5 = pd.concat(all_dfs5, ignore_index=True)
        all_dfs6 = pd.read_excel('/home/ajay/Downloads/April/deaconess_henderson.xlsx', sheet_name=None)
        df6 = pd.concat(all_dfs6, ignore_index=True)
        all_dfs7 = pd.read_excel('/home/ajay/Downloads/April/deaconess_union_county.xlsx', sheet_name=None)
        df7 = pd.concat(all_dfs7, ignore_index=True)
        frames = [df1, df2, df3, df4, df5, df6, df7]
        df8 = pd.concat(frames, ignore_index=True)
        df8.to_excel(writer, index=False, sheet_name='deaconess')

    except Exception as e:
        logging.exception("error")



if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Deaconess2.xlsx', engine='xlsxwriter')
    Deaconess(writer)
    writer.save()



