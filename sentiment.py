import pandas as pd
from snownlp import SnowNLP

# Read the Excel file
df = pd.read_excel('E:\\FangLin\\Taobao\\LDA\\八佰_1.xlsx')

# Define a function to get sentiment
def get_sentiment(text):
    return SnowNLP(text).sentiments

# Convert '评论内容' to strings
df['评论内容'] = df['评论内容'].astype(str)

# Apply the function to the '评论内容' column
df['Sentiment'] = df['评论内容'].apply(get_sentiment)

# Save the dataframe to a new Excel file
df.to_excel('E:\\FangLin\\Taobao\\LDA\\八佰_sentiment.xlsx', index=False)

# Take a look at the dataframe
print(df)



