df1 = pd.DataFrame(df)
df_mapping = pd.DataFrame({
    'Month': ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'],
})
sort_mapping = df_mapping.reset_index().set_index('Month')
df1['Month_num'] = df1['Month'].map(sort_mapping['index'])
df1.sort_values('Month_num')
print(df1)
# cat_month = CategoricalDtype(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'])
# df1['Month'].astype(cat_month)
# # print(df1)
# df1.sort_values(['Month'])
# print(df1)
# print(df['Month'])
