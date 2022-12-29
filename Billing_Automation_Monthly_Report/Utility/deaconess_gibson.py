from Utility.save_output_to_folder import *
import logging

def deaconess_gibson(ggh_client_statement):
    try:
        # creating MED1OS tab
        MED1OS = ggh_client_statement.loc[
            (ggh_client_statement['Client #'].isin(['128I55', '128MDM', '128R25', '128R55', '128ECA','128REC']))
        ]

        save_statement_to_output_folder.send_statement( MED1OS, "MED1 OS", "deaconess_gibson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1OS" )

    try:
        # creating MED1ACL tab
        MED1ACL=ggh_client_statement.loc[
            (ggh_client_statement['Client #'].isin( ['128E55'] ))
        ]

        save_statement_to_output_folder.send_statement( MED1ACL, "MED1 ACL", "deaconess_gibson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1ACL" )

    try:
        # creating CBSOS tab
        CBSOS=ggh_client_statement.loc[
            (ggh_client_statement['Client #'].isin(['128E25', '128AWP', '128INS', '128SPP']))
        ]

        save_statement_to_output_folder.send_statement( CBSOS, "CBS OS", "deaconess_gibson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSOS" )

    try:
        # creating CBSACL tab
        CBSACL=ggh_client_statement.loc[
            (ggh_client_statement['Client #'].isin( ['128ERP', '128WCP'] ))
        ]

        save_statement_to_output_folder.send_statement( CBSACL, "CBS ACL", "deaconess_gibson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSACL" )
