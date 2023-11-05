import pdfplumber
import codecs

# Define the range of years and quarters you want to process
years = range(2001, 2019)
quarters = ['第一季度', '第二季度', '第三季度', '第四季度']

# Iterate through years and quarters
for year in years:
    for quarter in quarters:
        # Skip processing for 2018 第四季度
        if year == 2018 and quarter == '第四季度':
            continue

        # Generate the PDF file name based on the year and quarter
        pdf_file_name = f"{year}年{quarter}中国货币政策执行报告.pdf"

        # Use pdfplumber to extract text from the PDF
        with pdfplumber.open(pdf_file_name) as pdf:
            # Create a text file with a name based on the year and quarter
            txt_file_name = f"{year}_{quarter}.txt"
            with codecs.open(txt_file_name, 'a', 'utf-8') as f1:
                for page in pdf.pages:
                    f1.write(page.extract_text())

# This code will iterate through all combinations of years and quarters and extract text from the corresponding PDFs, skipping 2018 第四季度.

