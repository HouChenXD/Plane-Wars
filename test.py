import pandas as pd
df = pd.read_table('user.txt',names = ['A'],sep=' ')
print(df.sort_values(by=['A'],ascending=False))
#print(df_news.sort_values(by = '1',ascending = True),'\n')
