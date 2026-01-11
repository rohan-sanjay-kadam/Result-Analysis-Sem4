import pandas as pd
def list_all(df):
    df.columns = df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)

    df['EXAMTOTAL'] = (
        df['EXAMTOTAL']
        .astype(str)
        .str.findall(r'\d+(?:\.\d+)?')  # find ALL numbers
        .str[-1]                        # take the LAST one
    )
    df['EXAMTOTAL'] = pd.to_numeric(df['EXAMTOTAL'], errors='coerce')
    sorted_df = (
        df.sort_values(by='EXAMTOTAL', ascending=False)
          .head(3)[['ROLLNO', 'NAME', 'EXAMTOTAL']]
    )
    return sorted_df


def sub1_list(df):
    df.columns = df.columns.str.strip().str.upper()
    df['EXAM3'] = pd.to_numeric(df['EXAM3'], errors='coerce')
    sub1_df=df.sort_values(by="EXAM3",ascending=False)
    sub1_df = sub1_df.head(3)
    sub1_df =sub1_df[["ROLLNO","NAME","EXAM3"]]
    return sub1_df

def sub2_list(df):
    df.columns = df.columns.str.strip().str.upper()
    df['EXAM6'] = pd.to_numeric(df['EXAM6'], errors='coerce')
    sub2_df=df.sort_values(by="EXAM6",ascending=False)
    sub2_df = sub2_df.head(3)
    sub2_df =sub2_df[["ROLLNO","NAME","EXAM6"]]
    return sub2_df

def sub3_list(df):
    df.columns = df.columns.str.strip().str.upper()
    df['EXAM9'] = pd.to_numeric(df['EXAM9'], errors='coerce')
    sub3_df=df.sort_values(by="EXAM9",ascending=False)
    sub3_df = sub3_df.head(3)
    sub3_df =sub3_df[["ROLLNO","NAME","EXAM9"]]
    return sub3_df

def sub4_list(df):
    df.columns = df.columns.str.strip().str.upper()
    df['EXAM12'] = pd.to_numeric(df['EXAM12'], errors='coerce')
    sub4_df=df.sort_values(by="EXAM12",ascending=False)
    sub4_df = sub4_df.head(3)
    sub4_df =sub4_df[["ROLLNO","NAME","EXAM12"]]
    return sub4_df

def sub5_list(df):
    df.columns = df.columns.str.strip().str.upper()
    df['EXAM15'] = pd.to_numeric(df['EXAM15'], errors='coerce')
    sub5_df=df.sort_values(by="EXAM15",ascending=False)
    sub5_df = sub5_df.head(3)
    sub5_df =sub5_df[["ROLLNO","NAME","EXAM15"]]
    return sub5_df

