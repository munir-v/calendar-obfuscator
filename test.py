import pandas as pd

df = pd.read_csv('/Users/macsprod/Downloads/calendly events-export.csv')

df['Start Date & Time'] = pd.to_datetime(
    df['Start Date & Time'], 
    format='%Y-%m-%d %I:%M %p'
)
df['End Date & Time'] = pd.to_datetime(
    df['End Date & Time'], 
    format='%Y-%m-%d %I:%M %p'
)

df['START DATE'] = df['Start Date & Time'].dt.date
df['START TIME'] = df['Start Date & Time'].dt.time
df['END DATE'] = df['End Date & Time'].dt.date
df['END TIME'] = df['End Date & Time'].dt.time

df['SUBJECT'] = df['Invitee Name'].astype(str) + " and " + df['User Name'].astype(str)

df['DESCRIPTION'] = (
    df['Question 1'].astype(str) 
    + ": " 
    + df['Response 1'].astype(str) 
    + "; " 
    + df['Question 2'].astype(str) 
    + ": " 
    + df['Response 2'].astype(str)
)

df.to_csv('/Users/macsprod/Downloads/output.csv', index=False)