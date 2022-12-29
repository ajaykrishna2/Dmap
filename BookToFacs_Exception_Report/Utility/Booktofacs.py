import numpy as np
import pandas as pd
class book_to_facs_exception:
    def payrpt(self,payrpt):
        # Removing left preceeding zeros
        payrpt['Acct#'] = payrpt['Acct#'].str.lstrip('0')
        payrpt = payrpt.rename({"PRN":"payrpt_PRN"},axis=1)
        payrpt_sum = payrpt[['Client#', 'payrpt_PRN']].groupby(['Client#']).sum()
        payrpt_PRN_sum = payrpt_sum.reset_index()
        return payrpt_PRN_sum

    def NON_STV(self,NON_STV):
        NON_STV['Acct#'] = NON_STV['Acct#'].str.lstrip('0')
        NON_STV = NON_STV.rename({"PRN": "NON_STV_PRN"}, axis=1)
        NON_STV_sum = NON_STV[['Client#', 'NON_STV_PRN']].groupby(['Client#']).sum()
        NON_STV_PRN_sum = NON_STV_sum.reset_index()
        return NON_STV_PRN_sum

    def STV(self, STV):
        STV['Acct#'] = STV['Acct#'].str.lstrip('0')
        STV = STV.rename({"PRN": "STV_PRN"}, axis=1)
        STV_sum = STV[['Client#', 'STV_PRN']].groupby(['Client#']).sum()
        STV_PRN_sum = STV_sum.reset_index()
        return STV_PRN_sum

    def COMMUNITY(self, COMMUNITY):
        COMMUNITY['Acct#'] = COMMUNITY['Acct#'].str.lstrip('0')
        COMMUNITY = COMMUNITY.rename({"PRN": "COMMUNITY_PRN"}, axis=1)
        COMMUNITY_sum = COMMUNITY[['Client#', 'COMMUNITY_PRN']].groupby(['Client#']).sum()
        COMMUNITY_PRN_sum = COMMUNITY_sum.reset_index()
        return COMMUNITY_PRN_sum

    def MED1(self, MED1):
        MED1['Acct#'] = MED1['Acct#'].str.lstrip('0')
        MED1 = MED1.rename({"PRN": "MED1_PRN"}, axis=1)
        MED1_sum = MED1[['Client#', 'MED1_PRN']].groupby(['Client#']).sum()
        MED1_PRN_sum = MED1_sum.reset_index()
        return MED1_PRN_sum

    def RCR(self, RCR):
        RCR['Acct#']=RCR['Acct#'].astype(str)
        RCR['Acct#'] = RCR['Acct#'].str.lstrip('0')
        RCR = RCR.rename({"PRN": "RCR_PRN"}, axis=1)
        RCR_sum = RCR[['Client#', 'RCR_PRN']].groupby(['Client#']).sum()
        RCR_PRN_sum = RCR_sum.reset_index()
        return RCR_PRN_sum

    def Amount_validation(self,payrpt,NON_STV,STV,COMMUNITY,MED1,RCR,save_file):
        payrpt_clientid = self.payrpt(payrpt)
        NON_STV_clientid = self.NON_STV(NON_STV)
        STV_clientid = self.STV(STV)
        COMMUNITY_clientid = self.COMMUNITY(COMMUNITY)
        MED1_clientid = self.MED1(MED1)
        RCR_clientid = self.RCR(RCR)
        data_frames = [NON_STV_clientid, STV_clientid, COMMUNITY_clientid, MED1_clientid]
        result = pd.concat(data_frames)
        concated_df = pd.merge(result,RCR_clientid,on="Client#", how='outer')
        # Creating empty dataframe with column names
        df = pd.DataFrame(columns=['Client#','NON_STV_PRN','STV_PRN','COMMUNITY_PRN','MED1_PRN','RCR_PRN'])
        splitted_df = df.append(concated_df)
        # Filling zeros if the cells are blank, to perform math operations
        splitted_df.fillna(value=0, inplace=True)
        splitted_df['Total_PRN'] = splitted_df['NON_STV_PRN']+splitted_df['STV_PRN']+splitted_df['COMMUNITY_PRN']+\
        splitted_df['MED1_PRN']+splitted_df['RCR_PRN']
        merged_df = pd.merge(splitted_df, payrpt_clientid, on="Client#", how='outer')
        merged_df['Total_PRN'] = round(merged_df['Total_PRN'],2)
        merged_df['payrpt_PRN'] = round(merged_df['payrpt_PRN'], 2)
        comparison_column = np.where(merged_df["Total_PRN"] == merged_df["payrpt_PRN"], True, False)
        merged_df['PRN-Validation'] = comparison_column
        save_file.send_statement(merged_df,"Amount_Validation","Book_to_Facs","output/Exec_Book_to_Facs")

    def Exception_report(self,payrpt,NON_STV,STV,COMMUNITY,MED1,RCR,save_file):
        # Splitted tabs processing
        data_frames = [NON_STV,STV,COMMUNITY,MED1,RCR]
        concated_df = pd.concat(data_frames,axis=0)
        concated_df['year'] = pd.DatetimeIndex(concated_df['Date']).year
        concated_df['month'] = pd.DatetimeIndex(concated_df['Date']).month
        concated_df['day'] = pd.DatetimeIndex(concated_df['Date']).day
        concated_df['flag_book_to_facs'] = concated_df["Acct#"].map(str) + concated_df["year"].map(str) +\
        concated_df['month'].map(str) +concated_df["day"].map(str) + concated_df['PRN'].map(str)
        concated_df['flag_id'] = concated_df["Acct#"].map(str)+concated_df["year"].map(str) +\
        concated_df['month'].map(str)+concated_df["day"].map(str)+concated_df['Pmt Type'].map(str)+concated_df['COR Type'].map(str)
        splitted_df = concated_df[['Client#', 'Client Name', 'Acct#', 'Total', 'Pmt Type', 'COR Type', 'PRN',\
        'Int', 'Atty', 'Misc','CC','PJI', 'Total Pay', 'O/P Amt','flag_book_to_facs','flag_id']]
        splitted_df = splitted_df.rename({"Client#": "Client#_BookToFacs","Client Name":"Client Name_BookToFacs",\
        "Acct#":"Acct#_BookToFacs","Total":"Total_BookToFacs","Pmt Type":"Pmt Type_BookToFacs","COR Type":"COR Type_BookToFacs",\
        "PRN":"PRN_BookToFacs","Int":"Int_BookToFacs","Atty":"Atty_BookToFacs","Misc":"Misc_BookToFacs","CC":"CC_BookToFacs",\
        "PJI":"PJI_BookToFacs","Total Pay":"Total Pay_BookToFacs","O/P Amt":"O/P Amt_BookToFacs"}, axis=1)
        # Payrpt input processing
        payrpt['year'] = pd.DatetimeIndex(payrpt['Date']).year
        payrpt['month'] = pd.DatetimeIndex(payrpt['Date']).month
        payrpt['day'] = pd.DatetimeIndex(payrpt['Date']).day
        payrpt['flag_payrpt'] = payrpt["Acct#"].map(str) + payrpt["year"].map(str) + payrpt['month'].map(str) +\
                                payrpt["day"].map(str) + payrpt['PRN'].map(str)
        payrpt['flag_id'] = payrpt["Acct#"].map(str) + payrpt["year"].map(str) + payrpt['month'].map(str) +\
                            payrpt["day"].map(str) + payrpt['Pmt Type'].map(str)+payrpt['COR Type'].map(str)
        #Merging payrpt and splitted tabs 
        merged_df = pd.merge(splitted_df,payrpt[['Client#', 'Client Name', 'Acct#', 'Total', 'Pmt Type', 'COR Type','PRN', 'Int',\
                    'Atty', 'Misc', 'CC','PJI', 'Total Pay', 'O/P Amt','flag_payrpt','flag_id']],on='flag_id',how='outer')
        # Finding out the Missing_Acct#_BookToFacs
        exception = merged_df[~merged_df['flag_book_to_facs'].isin(merged_df['flag_payrpt'].values)]
        exception=exception[['Client#', 'Client Name', 'Acct#', 'Total', 'Pmt Type', 'COR Type', 'PRN', 'Int', 'Atty',\
                  'Misc', 'CC','PJI', 'Total Pay', 'O/P Amt']]
        save_file.send_statement(exception,"Missing_Acct#_BookToFacs","Book_to_Facs","output/Exec_Book_to_Facs")

