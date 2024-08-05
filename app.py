import streamlit as st
from quiz_generater import extract_text_from_pdf, preprocess_text, generate_quiz_questions,format_quiz


st.title("PDF to Quiz Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    # Preprocess text
    clean_text = preprocess_text(pdf_text)
    
    # Generate quiz questions
    st.write("Generating quiz questions...")
    raw_quiz_text = generate_quiz_questions(clean_text)
    # print("answer ",raw_quiz_text)
    
    # Format the quiz
    formatted_quiz = format_quiz(raw_quiz_text)
    # print("formatted",formatted_quiz)
    st.write("jsonData",formatted_quiz)
    
    # Display the quiz
    st.write("Quiz Questions:")
    for idx, question in enumerate(formatted_quiz, 1):
        st.subheader(f"{question['question']}")
        for option in question['options']:
            st.write(f"- {option}")
        st.write(f"**Answer:** {question['answer']}")