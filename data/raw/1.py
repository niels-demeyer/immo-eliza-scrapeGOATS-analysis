import pandas as pd
df = pd.read_csv('houses_moreinfo.csv')

data_top = df.head()

column_names = list(df.columns.values)

column_names1 = [col.strip() for col in column_names]

df.columns = column_names1

space_count = df['price'].apply(lambda x: x == ' ').sum()

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df_cleaned = df.dropna(subset=['price'])
indices_to_drop = df_cleaned[df_cleaned['life_annuity'] == 1].index

df_cleaned = df_cleaned.drop(indices_to_drop)

df_cleaned = df_cleaned.drop(
    ['type_sale', 'sale_type', 'has_balcony', 'life_annuity'], axis=1)

df_cleaned.to_csv("houses_cleaned", index=False)
