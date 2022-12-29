from Utility.save_output_to_folder import *
import logging

def deaconess_health_sys(dhs_client_statement):
    try:
        # creating MED1OS tab
        MED1OS = dhs_client_statement.loc[~dhs_client_statement['Clients Acct #'].astype(str).str.contains("40000|41000|40001",
                regex=True)
            & (dhs_client_statement['Client #'].isin(['132I55', '132MDM', '132R25', '132R55', '132REC', '132ECA','132IFM']))
        ]

        save_statement_to_output_folder.send_statement( MED1OS, "MED1 OS", "deaconess_health_sys", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1OS" )

    try:
        # creating MED1ACL tab
        MED1ACL= dhs_client_statement.loc[~dhs_client_statement['Clients Acct #'].astype(str).str.contains("40000|41000|40001",
                regex=True)
            & (dhs_client_statement['Client #'].isin( ['132E55'] ))
        ]

        save_statement_to_output_folder.send_statement( MED1ACL, "MED1 ACL", "deaconess_health_sys", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in MED1ACL" )

    try:
        # creating CBSOS tab
        CBSOS= dhs_client_statement.loc[~dhs_client_statement['Clients Acct #'].astype(str).str.contains("40000|41000|40001",
                regex=True)
            & (dhs_client_statement['Client #'].isin(['132E25', '132AWP', '132INS', '132SPP','132MDC']))
            ]

        save_statement_to_output_folder.send_statement( CBSOS, "CBS OS", "deaconess_health_sys", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSOS" )

    try:
        # creating CBSACL tab
        CBSACL= dhs_client_statement.loc[~dhs_client_statement['Clients Acct #'].astype(str).str.contains("40000|41000|40001",
                regex=True)
           & (dhs_client_statement['Client #'].isin( ['1032','3032', '132ERP', '132WCP','132M25', '132IFU'] ))
        ]

        save_statement_to_output_folder.send_statement( CBSACL, "CBS ACL", "deaconess_health_sys", "Deaconess")
    except Exception as e:
        logging.exception( "error in splitting data in CBSACL" )
