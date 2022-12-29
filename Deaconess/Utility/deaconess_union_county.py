from Utility.save_output_to_folder import *
import logging

def deaconess_union_county(union_client_statement):
    try:
        # creating MED1OS tab
        MED1OS=union_client_statement.loc[
                union_client_statement['Clients Acct #'].astype(str).str.contains("43000",regex=True)&
            (union_client_statement['Client #'].isin( ['127I55', '127MDM', '127R25', '127R55', '127ECA','127REC'] ))
        ]

        save_statement_to_output_folder.send_statement( MED1OS, "MED1 OS", "deaconess_union_county", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1OS" )

    try:
        # creating MED1ACL tab
        MED1ACL=union_client_statement.loc[
                union_client_statement['Clients Acct #'].astype(str).str.contains("43000",regex=True)&
            (union_client_statement['Client #'].isin( ['127E55'] ))
        ]

        save_statement_to_output_folder.send_statement( MED1ACL, "MED1 ACL", "deaconess_union_county", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1ACL" )

    try:
        # creating CBSOS tab
        CBSOS=union_client_statement.loc[
                union_client_statement['Clients Acct #'].astype(str).str.contains("43000",regex=True)&
            (union_client_statement['Client #'].isin( ['127E25', '127AWP', '127INS', '127SPP'] ))
        ]

        save_statement_to_output_folder.send_statement( CBSOS, "CBS OS", "deaconess_union_county", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSOS" )

    try:
        # creating CBSACL tab
        CBSACL=union_client_statement.loc[
                union_client_statement['Clients Acct #'].astype(str).str.contains("43000",regex=True)&
            (union_client_statement['Client #'].isin( ['127ERP', '127WCP'] ))
        ]

        save_statement_to_output_folder.send_statement( CBSACL, "CBS ACL", "deaconess_union_county", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSACL" )
