from quiz_generation import generate_quiz
from database_generation import save_quiz_to_db


def main():
    while True:
        # Ask if the user wants to generate another quiz
        another = input("Do you want to generate another quiz? (yes/no): ").strip().lower()
        if another != 'yes':
            print("Exiting the quiz generation.")
            break

        # Gather quiz parameters from user
        topic = input("Enter the topic for the quiz: ")
        quiz_type = input("Enter quiz type (MCQs, True/False, ShortQuestions): ").strip().lower()
        num_questions = int(input("Enter the number of questions: "))
        education_level = input("Enter the education level of the students (e.g., primary, secondary, university): ")

        # Prepare data to pass between functions
        quiz_data = {
            'topic': topic,
            'quiz_type': quiz_type,
            'num_questions': num_questions,
            'education_level': education_level
        }

        # Generate quiz content
        response_text = generate_quiz(quiz_data)

        # Print the generated quiz content
        print("\nGenerated Quiz Content:")
        print(response_text)

        # Save generated quiz to the database
        save_quiz_to_db(quiz_data, response_text)
        print("Quiz generated and saved to the database successfully.\n")


if __name__ == "__main__":
    main()
