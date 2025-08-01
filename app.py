import google.generativeai as genai
from flask import Flask, render_template, request

app = Flask(__name__)

# Set your Google Gemini API key
api_key = 'AIzaSyCGwLLZ1UwFd0viHzjh-38ct-ddSlbpjmQ'  # Replace with your actual Google Gemini API key
genai.configure(api_key=api_key)

@app.route('/')
def index():
    # Render the form for user inputs
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    # Handle form data and generate recommendations
    goal = request.form.get('fitness_goals')
    gender = request.form.get('gender')
    training_method = request.form.get('training_method')
    workout_type = request.form.get('workout_type')
    strength_level = request.form.get('strength_level')
    use_advanced_ai = request.form.get('use_advanced_ai')

    # Generate the recommendation based on form data using Google Gemini API
    recommendations = generate_recommendations(goal, gender, training_method, workout_type, strength_level, use_advanced_ai)
    recommendations = convert_bold(recommendations)
    # Render the recommendations on a new page
    return render_template('recommendations.html', 
                           goal=goal, 
                           gender=gender, 
                           strength_level=strength_level, 
                           recommendations=recommendations)

def generate_recommendations(goal, gender, training_method, workout_type, strength_level, use_advanced_ai):
    # Build the prompt that will be sent to the Google Gemini API
    prompt = f"""
    Generate a personalized workout and meal plan for a {strength_level} {gender} aiming to {goal}. 
    Training Method: {training_method}.
    Workout Type: {workout_type}.
    Use advanced AI: {use_advanced_ai}.
    Include workout frequency, details, and a sample meal plan.
    """

    # Request the recommendation from Google Gemini (Generative AI)
    try:
        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        generated_text = response.text.strip()
        return generated_text
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def convert_bold(text):
    """Convert text with asterisks around words to HTML <strong> tags."""
    while '*' in text:
        # Find the first '*' character
        start_idx = text.find('*')
        # Find the next '*' character after the first one
        end_idx = text.find('*', start_idx + 1)
        
        if start_idx != -1 and end_idx != -1:
            # Wrap the text between '*' in <strong> tags
            bold_text = text[start_idx + 1:end_idx]
            # Replace the asterisks and the text with <strong>...</strong> tags
            text = text[:start_idx] + '<strong>' + bold_text + '</strong>' + text[end_idx + 1:]
        else:
            break  # Exit the loop if no valid pairs of asterisks are found

    return text

if __name__ == '__main__':
    app.run(debug=True)
