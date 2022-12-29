from Utility.save_output_to_folder import *
import logging
def park_view(parkview_client_statement):
        try:
            # creating 101599 Comm of LaGrange tab
            Comm_of_LaGrange=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 101599)
            ]
            Comm_of_LaGrange.loc['total'] =Comm_of_LaGrange[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Comm_of_LaGrange, "101599 Comm of LaGrange", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Comm_of_LaGrange")
        try:
            # creating 102999 Whitely tab
            Whitely=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 102999)
            ]
            Whitely.loc['total'] =Whitely[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Whitely, "102999 Whitely", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Whitely")

        try:
            # creating 103599 Wabash tab
            Wabash=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 103599)
            ]
            Wabash.loc['total'] =Wabash[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Wabash, "103599 Wabash", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Wabash")

        try:
            # creating 103999 Huntington tab
            Huntington=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 103999)
            ]
            Huntington.loc['total'] =Huntington[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Huntington, "103999 Huntington", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Huntington")

        try:
            # creating 104999 Parkview tab
            Parkview=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 104999)
            ]
            Parkview.loc['total'] =Parkview[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Parkview, "104999 Parkview", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Parkview")

        try:
            # creating 105599 Dekalb tab
            Dekalb=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 105599)
            ]
            Dekalb.loc['total'] =Dekalb[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Dekalb, "105599 Dekalb", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Dekalb")

        try:
            # creating 105999 Comm Hosp Noble tab
            Comm_Hosp_Noble=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 105999)
            ]
            Comm_Hosp_Noble.loc['total'] =Comm_Hosp_Noble[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Comm_Hosp_Noble, "105999 Comm Hosp Noble", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Comm_Hosp_Noble")

        try:
            # creating 106899 Ortho tab
            Ortho=parkview_client_statement.loc[
            (parkview_client_statement['Acct Location'] == 106899)
            ]
            Ortho.loc['total'] =Ortho[['Over Paid','Pd to Agency','PD to you','Due Agency','Due You']].sum()
            save_statement_to_output_folder.send_statement(Ortho, "106899 Ortho", "Park_View_Statement","Park_View")
        except Exception as e:
            logging.exception("error in splitting data in Ortho")


