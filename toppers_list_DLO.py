import pandas as pd

def DLO_list(df, DLO_df,grade):
    if DLO_df.empty:
        return None
    df.columns = df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    DLO_df.columns = DLO_df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    df=df[df['ROLLNO'].isin(DLO_df['ROLLNO'])]
    df.loc[:,grade] = pd.to_numeric(df[grade], errors='coerce')
    sub2_df=df.sort_values(by=grade,ascending=False)
    sub2_df = sub2_df.head(3)
    sub2_df =sub2_df[["ROLLNO","NAME",grade]]
    return sub2_df



