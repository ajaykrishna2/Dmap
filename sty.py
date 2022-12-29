import pandas as pd
from IPython.display import display
import numpy as np

df = pd.DataFrame({'text': ['foo foo', 'bar bar'],
                 'number': [1, 2]})

df1 = df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
df2 = df1.set_properties(**{'text-align': 'center'}).hide_index()
display(df2)