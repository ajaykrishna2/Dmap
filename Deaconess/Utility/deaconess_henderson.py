from Utility.save_output_to_folder import *
import logging

def deaconess_henderson(mh_client_statement):
    try:
        # creating MED1OS tab
        MED1OS = mh_client_statement.loc[
            (mh_client_statement['Client #'].isin(['129I55', '129MDM', '129R25', '129R55', '129ECA','129REC']))
        ]

        save_statement_to_output_folder.send_statement( MED1OS, "MED1 OS", "deaconess_henderson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1OS" )

    try:
        # creating MED1ACL tab
        MED1ACL=mh_client_statement.loc[
            (mh_client_statement['Client #'].isin( ['129E55'] ))
        ]

        save_statement_to_output_folder.send_statement( MED1ACL, "MED1 ACL", "deaconess_henderson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1ACL" )

    try:
        # creating CBSOS tab
        CBSOS=mh_client_statement.loc[
            (mh_client_statement['Client #'].isin(['129E25', '129AWP', '129INS', '129SPP']))
        ]

        save_statement_to_output_folder.send_statement( CBSOS, "CBS OS", "deaconess_henderson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSOS" )

    try:
        # creating CBSACL tab
        CBSACL=mh_client_statement.loc[
            (mh_client_statement['Client #'].isin( ['129ERP', '129WCP'] ))
        ]

        save_statement_to_output_folder.send_statement( CBSACL, "CBS ACL", "deaconess_henderson", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSACL" )
