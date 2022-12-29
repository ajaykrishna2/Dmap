import pandas as pd
df = pd.DataFrame({
    'config_dummy1': ["dummytext"] * 10,
    'a_y': ["a"] * 10,
    'config_size_x': ["textstring"] * 10,
    'config_size_y': ["textstring"] * 10,
    'config_dummy2': ["dummytext"] * 10,
    'a_x': ["a"] * 10
})
df.at[5, 'config_size_x'] = "xandydontmatch"
df.at[9, 'config_size_y'] = "xandydontmatch"
df.at[0, 'a_x'] = "xandydontmatch"
df.at[3, 'a_y'] = "xandydontmatch"
print(df.to_string())

def color(x, extra):
    c1 = 'color: #ffffff; background-color: #ba3018'
    # print(x)
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)

    #select only columns ends with _x and _y and sorting
    # cols = sorted(extra.filter(regex='_y$').columns)
    cols = sorted(extra.filter(['a_y']).columns)
    #loop by pairs and assign style by mask
    df1=df1[cols]
    # for colx, coly in zip(cols[::2],cols[1::2]):
    #     #pairs columns
    #     m = extra[colx] != extra[coly]
    #     df1.loc[m, [coly]] = c1
    print(df1.to_string())
    return df1

yonly = list(sorted(set(df.columns) - set(df.filter(['config_dummy1','a_x','config_size_x','config_size_y','config_dummy2']).columns)))
df_tmp = df[yonly]
print(df_tmp)
df_tmp.style.apply(color, axis=None, extra=df).to_excel('/home/ajay/styled.xlsx', engine='openpyxl')