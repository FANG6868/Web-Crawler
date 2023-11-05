import os
import jieba
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to read stop words from the 'cn_stopwords' file
def read_stop_words():
    with open('cn_stopwords.txt', 'r', encoding='utf-8') as file:
        stop_words = [line.strip() for line in file]
    return stop_words

# Function to tokenize and preprocess text using Jieba while removing stop words
def tokenize_and_preprocess(text, stop_words):
    # Tokenize the text using Jieba
    words = jieba.cut(text)

    # Remove stop words from the tokenized text
    words = [word for word in words if word not in stop_words]

    return " ".join(words)

# Function to calculate similarity between two files
def calculate_similarity(file1, file2, stop_words):
    if not os.path.isfile(file1) or not os.path.isfile(file2):
        # Skip if either file does not exist
        return None

    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()
        # Create a TF-IDF vectorizer using Jieba tokenizer
        tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: tokenize_and_preprocess(x, stop_words))
        tfidf_matrix = tfidf_vectorizer.fit_transform([content1, content2])
        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity

# List of years from 2001 to 2018
years = list(range(2001, 2019))

# List of quarters
quarters = ['第一季度', '第二季度', '第三季度', '第四季度']

# Read stop words from the 'cn_stopwords' file
stop_words = read_stop_words()

# Initialize an empty list to store the results
results = []

# Iterate through different years and quarters, and compare each report with the report from the previous quarter
for year in years:
    for i, quarter in enumerate(quarters):
        # Construct file names for the current and previous quarters
        current_file = f"{year}_{quarter}.txt"

        # Check if it's not the first quarter and the last quarter
        if year != 2001 or (year == 2001 and i > 0) and year != 2018 or (year == 2018 and i < 3):
            previous_quarter = quarters[i - 1] if i > 0 else quarters[3]
            previous_year = year - 1 if i == 0 else year
            previous_file = f"{previous_year}_{previous_quarter}.txt"

            # Calculate and print similarity
            similarity = calculate_similarity(current_file, previous_file, stop_words)

            # Append the results to the list
            results.append({
                "Current File": current_file,
                "Previous File": previous_file,
                "Similarity": similarity if similarity is not None else "N/A"
            })

# Create a DataFrame from the results list
df = pd.DataFrame(results)

# Save the DataFrame to an Excel file named 'similarity.xlsx'
df.to_excel("similarity.xlsx", index=False)

print("Similarity results saved to 'similarity.xlsx' file.")

