import streamlit as st
import json
import os

# Path to the cleaned questions JSON file
file_path = "cleaned_questions.json"
ratings_file = "ratings.json"

# Load the questions data
def load_questions():
    if not os.path.exists(file_path):
        st.error("Questions file not found.")
        return []
    with open(file_path, 'r') as file:
        return json.load(file)

# Load existing ratings or create an empty file
def load_ratings():
    if os.path.exists(ratings_file):
        with open(ratings_file, 'r') as file:
            return json.load(file)
    return {}

# Save ratings to the JSON file
def save_ratings(ratings):
    with open(ratings_file, 'w') as file:
        json.dump(ratings, file, indent=4)

# Main Streamlit app
def main():
    st.title("Question Rating App")

    # Select user
    user = st.selectbox("Select User", ["Sarah", "Dom"])

    # Load questions and ratings
    questions = load_questions()
    ratings = load_ratings()

    if not questions:
        st.warning("No questions available.")
        return

    # Iterate through questions
    for question in questions:
        question_id = question['_id']['$oid']
        st.header(f"Question: {question['question']}")
        st.subheader(f"Type: {question['question_type']}")
        st.write(f"Explanation: {question.get('explanation', 'No explanation provided.')}")

        if question.get("answer_options"):
            st.write("### Answer Options:")
            for i, option in enumerate(question["answer_options"], start=1):
                st.write(f"{i}. {option}")

        # Initialize user ratings for the question if not already present
        if question_id not in ratings or not isinstance(ratings[question_id], dict):
            ratings[question_id] = {}

        # Get the current user's rating or set to None
        current_rating = ratings[question_id].get(user, None)

        # Display existing rating
        if current_rating is not None:
            st.write(f"Your current rating: {current_rating}")

        # Display rating widget
        rating = st.slider(
            f"Rate this question (ID: {question_id})", 
            min_value=1, 
            max_value=5, 
            value=current_rating if current_rating is not None else 3
        )

        # Add a "Save Rating" button
        if st.button(f"Save Rating for Question ID: {question_id}"):
            ratings[question_id][user] = rating
            save_ratings(ratings)
            st.success("Rating saved successfully!")

    st.write("---")
    st.write("All ratings will be stored and can be accessed for review.")

if __name__ == "__main__":
    main()
