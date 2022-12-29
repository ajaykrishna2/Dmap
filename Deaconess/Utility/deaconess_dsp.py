from Utility.save_output_to_folder import *
import logging

def deaconess_dsp(dsp_client_statement):
    try:
        # creating MED1OS tab
        MED1OS = dsp_client_statement.loc[
            (dsp_client_statement['Client #'].isin(['130I55', '130MDM', '130R25', '130R55', '130ECA']))
        ]

        save_statement_to_output_folder.send_statement( MED1OS, "MED1 OS", "deaconess_dsp", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1OS" )

    try:
        # creating MED1ACL tab
        MED1ACL=dsp_client_statement.loc[
            (dsp_client_statement['Client #'].isin( ['130E55'] ))
        ]

        save_statement_to_output_folder.send_statement( MED1ACL, "MED1 ACL", "deaconess_dsp", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1ACL" )

    try:
        # creating CBSOS tab
        CBSOS=dsp_client_statement.loc[
            (dsp_client_statement['Client #'].isin(['130E25', '130AWP', '130INS', '130SPP']))
        ]

        save_statement_to_output_folder.send_statement( CBSOS, "CBS OS", "deaconess_dsp", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSOS" )

    try:
        # creating CBSACL tab
        CBSACL=dsp_client_statement.loc[
            (dsp_client_statement['Client #'].isin( ['130ERP', '130WCP'] ))
        ]

        save_statement_to_output_folder.send_statement( CBSACL, "CBS ACL", "deaconess_dsp", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSACL" )
