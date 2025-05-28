import sqlite3
import re


# Initialize the database and create tables if they don't exist
def initialize_database():
    conn = sqlite3.connect("teaching_assistant.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            quiz_type TEXT,
            num_questions INTEGER,
            education_level TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER,
            question_text TEXT,
            question_type TEXT,
            FOREIGN KEY (quiz_id) REFERENCES Quizzes(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            answer_text TEXT,
            FOREIGN KEY (question_id) REFERENCES Questions(id)
        )
    """)

    conn.commit()
    conn.close()


# Parse quiz response and save it to the database
def parse_quiz_response(response):
    # Extract the questions and answers sections
    questions_part = re.search(r"Questions:(.*?)(?=Answers:|$)", response, re.DOTALL)
    answers_part = re.search(r"Answers:(.*)", response, re.DOTALL)

    if not questions_part or not answers_part:
        return []  # Return an empty list if parsing fails

    questions_part = questions_part.group(1).strip()
    answers_part = answers_part.group(1).strip()

    # Process questions and options
    questions = []
    question_texts = re.findall(r"(\d+\.\s.*?)(?=\n\d+\.|\nAnswers:|$)", questions_part, re.DOTALL)
    for question_text in question_texts:
        # Find options within the question text for MCQs, if available
        options = re.findall(r"([A-D]\)\s.*?)(?=\n|$)", question_text)
        if options:
            question_text += '\n' + '\n'.join(options)
        questions.append({'text': question_text.strip(), 'answer': None})

    # Process answers and handle multiple answer types
    answer_entries = re.findall(r"\d+\.\s(.*?)(?=\n|$)", answers_part)
    for i, answer_text in enumerate(answer_entries):
        if i < len(questions):
            # Determine answer type
            if answer_text.strip() in ["True", "False"]:
                answer_type = "True/False"
            elif re.match(r"^[A-D]\)$", answer_text.strip()):
                answer_type = "MCQ"
            else:
                answer_type = "Short Answer"

            questions[i]['answer'] = answer_text.strip()
            questions[i]['type'] = answer_type

    return questions


def save_quiz_to_db(quiz_data, response_text):
    initialize_database()
    conn = sqlite3.connect("teaching_assistant.db")
    cursor = conn.cursor()

    # Insert quiz metadata
    cursor.execute("""
        INSERT INTO Quizzes (topic, quiz_type, num_questions, education_level)
        VALUES (?, ?, ?, ?)
    """, (quiz_data['topic'], quiz_data['quiz_type'], quiz_data['num_questions'], quiz_data['education_level']))
    quiz_id = cursor.lastrowid

    # Parse the response and save questions and answers
    questions = parse_quiz_response(response_text)
    for question in questions:
        cursor.execute("""
            INSERT INTO Questions (quiz_id, question_text, question_type)
            VALUES (?, ?, ?)
        """, (quiz_id, question['text'], question['type']))
        question_id = cursor.lastrowid

        # Insert answer
        cursor.execute("""
            INSERT INTO Answers (question_id, answer_text)
            VALUES (?, ?)
        """, (question_id, question['answer']))

    conn.commit()
    conn.close()

