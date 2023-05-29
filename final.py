import openai
import PyPDF2
from summarizer import Summarizer  # Import BertSummarizer.

# 设置API Key
# Setting OpenAI API Key
openai.api_key = 'API KEY'

# 用于读取txt文件的函数
# Function to read txt files
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 用于读取pdf文件的函数
# Function to read pdf files
def read_pdf_file(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    pdf_file.close()
    return text

# 用于读取文件并区分txt和pdf文件的函数
# Read files and distinguish files from txt and pdf
def read_files(files):
    text = ""
    for file in files:
        if file.endswith('.txt'):
            text += read_txt_file(file)
        elif file.endswith('.pdf'):
            text += read_pdf_file(file)
    return text

# 用于获取回答的函数，使用了OpenAI的Davinci模型
# Function to get answer from OpenAI Davinci model
def ask_gpt(question, text):
    model = Summarizer()
    # 究极无敌耗时间的摘要生成
    # Create a summary for all the files
    summarized_text = model(text, ratio=0.007)
    prompt = f"{summarized_text}\n\n{question}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# 列出所有需要读取的文件
# List all files paths
files = ['张一鸣微博创业思考231条精华版.pdf','张一鸣微博2886条.pdf','zhanyiming.txt']
all_text = read_files(files)

# 回答问题，知道用户输入exit
while True:
    question = input("请提问: ")
    if question.lower() == "exit":
        break

    answer = ask_gpt(question, all_text)
    print("回答:", answer)

# Alternative Approach
# Clean data + use gpt-4-32k model + read a single file for a single question, which increase cost in money, add code comlexity, decrease cost in time
# 其他的解决方案
# 清理数据+使用gpt-4-32k模型+对于单个问题选择单个文件，会增加金钱成本，代码复杂度，但是减少每次运行时间