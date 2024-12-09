import pandas as pd

def clean_csv(input_file, output_file, skiprows=11):
    df1 = pd.read_csv(input_file, skiprows=skiprows) 
    df1.to_csv(output_file, index=False)
    print(f"Merged file saved to: {output_file}")

def merge_csv(input_file1, input_file2, output_file="merged.csv"):
    df1 = pd.read_csv(input_file1)
    df2 = pd.read_csv(input_file2)
    merged_df = pd.merge(df1, df2, on='PacketCounter', how='inner')
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved to: {output_file}")

clean_csv('rf2.csv', 'rf2_clean.csv')
clean_csv('rf3.csv', 'rf3_clean.csv')

merge_csv('rf2_clean.csv', 'rf3_clean.csv', 'merged.csv')
