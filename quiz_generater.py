from PyPDF2 import PdfReader
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI
import re
import os

# Set the Google API key
google_api_key=os.getenv("GOOGLE_API_KEY")
os.environ['GOOGLE_API_KEY']=google_api_key


# extract text from pdf
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    text=""
    for page_num in range(number_of_pages):
        page_text=reader.pages[page_num]
        text+=page_text.extract_text()   
    return text    

# preprocess text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text  

llm = GoogleGenerativeAI(model="models/text-bison-001")


def generate_quiz_questions(input_text):
    prompt = prompt = """You are a quiz generator. Given the text below,  create a multiple-choice question with four options (A, B, C, D) and identify the correct answer. Each question should be followed by four possible answers, where one of them is marked as correct.

**Text:** {input_text}

**Instructions:**
1. Read the provided text carefully.
2. Formulate a question that is relevant to the text.
3. Provide four answer options for the question.
4. Clearly identify which option is correct by indicating it as the correct answer.

**Example Output:**

**Question:** What is Python known for according to the text?
(A) Complex syntax
(B) Low-level programming
(C) **Readability and simplicity**
(D) None of the above

---

Please generate five question with four options and indicate the correct answer based on the provided text."""
   
    response = llm.invoke(prompt)
    return response

def create_quiz_from_pdf(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    clean_text = preprocess_text(raw_text)
    quiz_questions = generate_quiz_questions(clean_text)
    return quiz_questions


def format_quiz(raw_quiz_text):
    # Split the input text into lines
    lines = raw_quiz_text.strip().split('\n')
    formatted_quiz = []
    current_question = {}
    
    for line in lines:
        # Identify question lines
        if line.startswith("**Question"):
            # Save the previous question if it exists
            if current_question:
                if "question" in current_question and current_question["options"]:
                    formatted_quiz.append(current_question)
                current_question = {}
            # Start a new question
            current_question["question"] = line.strip().replace("**", "")
            current_question["options"] = []
        # Identify options
        elif line.startswith("(A)") or line.startswith("(B)") or line.startswith("(C)") or line.startswith("(D)"):
            option = line.strip()
            if "**" in option:
                # Remove the asterisks from the correct answer and mark it
                option = option.replace("**", "")
                current_question["answer"] = option
            # Add the option to the list of options
            current_question["options"].append(option)
        # Identify correct answer
        elif line.startswith("Correct answer:"):
            correct_answer = line.strip().split(":")[1].strip()
            current_question["answer"] = correct_answer
    
    # Append the last question if it exists
    if current_question and "question" in current_question and current_question["options"]:
        formatted_quiz.append(current_question)
    
    return formatted_quiz





