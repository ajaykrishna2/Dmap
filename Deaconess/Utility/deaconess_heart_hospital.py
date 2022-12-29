from Utility.save_output_to_folder import *
import logging

def splitting_heart_hospital(hh_client_statement):
    try:
        # creating MED1OS tab
        MED1OS = hh_client_statement.loc[
            (hh_client_statement['Client #'].isin(['131I55', '131MDM', '131R25', '131R55', '131REC', '131ECA']))
        ]

        save_statement_to_output_folder.send_statement( MED1OS, "MED1 OS", "deaconess_heart_hospital", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1OS" )

    try:
        # creating MED1ACL tab
        MED1ACL=hh_client_statement.loc[
            (hh_client_statement['Client #'].isin( ['131E55'] ))
        ]

        save_statement_to_output_folder.send_statement( MED1ACL, "MED1 ACL", "deaconess_heart_hospital", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1ACL" )

    try:
        # creating CBSOS tab
        CBSOS=hh_client_statement.loc[
            (hh_client_statement['Client #'].isin(['131E25', '131AWP', '131INS', '131SPP','131M25']))
        ]

        save_statement_to_output_folder.send_statement( CBSOS, "CBS OS", "deaconess_heart_hospital", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSOS" )

    try:
        # creating CBSACL tab
        CBSACL=hh_client_statement.loc[
            (hh_client_statement['Client #'].isin( ['131ERP', '131WCP'] ))
        ]

        save_statement_to_output_folder.send_statement( CBSACL, "CBS ACL", "deaconess_heart_hospital", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSACL" )
