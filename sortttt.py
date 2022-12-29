import pandas as pd
df = pd.DataFrame({
    'cloth_id': [1001, 1002, 1003, 1004, 1005, 1006],
    'size': ['S', 'XL', 'M', 'XS', 'L', 'S'],
})
print(df)
df_mapping = pd.DataFrame({
    'size': ['XS', 'S', 'M', 'L', 'XL'],
})
sort_mapping = df_mapping.reset_index().set_index('size')
df['size_num'] = df['size'].map(sort_mapping['index'])
df.sort_values('size_num')
print(df)