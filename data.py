import pandas as pd

def clean_csv(in_name, out_name):
    df1 = pd.read_csv(in_name, skiprows=11) 
    df1.to_csv(out_name, index=False)

def merge_csv(in_name1, in_name2, out_name="merged.csv"):
    df1 = pd.read_csv(in_name1)
    df2 = pd.read_csv(in_name2)
    merged_df = pd.merge(df1, df2, on='PacketCounter', how='inner')
    merged_df.to_csv(out_name, index=False)

clean_csv('rf2.csv', 'rf2_clean.csv')
clean_csv('rf3.csv', 'rf3_clean.csv')

csv_file1 = 'rf2_clean.csv'
csv_file2 = 'rf3_clean.csv'

# Output file
output_file = 'merged.csv'

# Read the CSV files
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)

# Join the two DataFrames on the 'PacketCounter' column
merged_df = pd.merge(df1, df2, on='PacketCounter', how='inner')  # Use 'how' as 'inner' for matching rows only

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(output_file, index=False)

print(f"Merged file saved to: {output_file}")
