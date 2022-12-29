import pandas as pd
i = pd.MultiIndex.from_tuples([(0, 0), (0, 1), (1, 0), (1, 1)], names=['level_0', 'level_1'])
df = pd.DataFrame(range(0, 4), index=i, columns=['foo'])
#print (df)

import matplotlib.colors as col
colors = {0: (0.6, 0.8, 0.8, 1), 1: (1, 0.9, 0.4, 1)}

c = {k:col.rgb2hex(v) for k, v in colors.items()}
idx = df.index.get_level_values(0)

css = [{'selector': f'.row{i}.level0','props': [('background-color', c[v])]}
             for i,v in enumerate(idx)]
print (css)

df.style.set_table_styles(css)
print(df)