# for displaying total enrolments by state based on published by
import pandas as pd
df1 = pd.read_csv("/home/ajay/csv/cid.csv" )
df2 = pd.read_csv("/home/ajay/csv/cid1.csv")
df3=df1.groupby(['Published by'])['Total enrolments By State'].sum()
print(df3)





#output
Published by
APEKX                                        2110459
Akshara Foundation                               137
Andaman and Nicobar Islands                    82380
Arunachal Pradesh                             121618
Assam                                         238924
Bihar                                        5514425
CBSE                                         2117773
Chandigarh                                    261224
Chhattisgarh                                 2099223
Dadra and Nagar Haveli and Daman and Diu       44404
Delhi                                        1120621
Diksha Pilot Tests                              5077
EKSTEP                                        300640
EKSTEP, UPS SEVAKHAR KALA                       1510
Goa State                                      50295
Gujarat                                      4582745
Haryana                                      1773758
Himachal Pradesh                              192979
IT_CELL CSE_AP AMARAVATI, APEKX                    3
Jammu And Kashmir                            1722919
Jharkhand State                              3073966
Karnataka                                    3026543
Ladakh                                         83549
MITRA                                        1102800
Madhya Pradesh                              12007089
Manipur                                       223761
Meghalaya                                     406522
Mizoram                                        55830
NCERT                                        3767702
Nagaland                                       83604
Odisha                                       3320410
Pondicherry                                   233276
Punjab                                         48609
Rajasthan                                    7520233
TalentSprint, TalentSprint                       132
Tamilnadu                                     284174
The Teacher App                              3000392
Tripura                                       275207
UNICEF                                             1
Uttarakhand                                    84119
ZPHS PALASAMUDRAM, APEKX                       18136
iGOT                                         3047877
सहज | SAHAJ                                 24915504
