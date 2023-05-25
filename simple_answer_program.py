import openai
import PyPDF2

# 设置API Key
# Setting OpenAI API Key
openai.api_key = 'api key'

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
    prompt = f"{text[:2000-len(question)-2]}\n\n{question}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# 列出所有需要读取的文件
# List all files paths
files = ['张一鸣微博2886条.pdf', '张一鸣微博创业思考231条精华版.pdf', 'zhanyiming.txt']
all_text = read_files(files)

# 回答问题，知道用户输入exit
while True:
    question = input("请提问: ")
    if question.lower() == "exit":
        break

    answer = ask_gpt(question, all_text)
    print("回答:", answer)

# 缺点
# 由于OpenAI API存在prompt数量限制，每次只能读取少量文本，在读取的文本数据未进行清洗的情况下有51万余token
# 而每次能上传的token数量只有4097个

# 改进思路
# 1. 对于不同问题，选取不同的文件进行读取
# 2. 删除多余空行，对读取数据进行清洗，通过减少token数量提高prompt质量
# 3. 提前将文本翻译成英文，可以大幅度减少token占用数量