from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from openai import OpenAI

# --- Load environment variables from .env file ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

# --- Initialize OpenAI client ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Initialize Flask app ---
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Workout generation route
@app.route('/generate', methods=['POST'])
def generate_workout():
    try:
        # Safely get form inputs
        name = request.form.get('name', 'User')
        age = request.form.get('age', 'unknown')
        gender = request.form.get('gender', 'not specified')
        goal = request.form.get('goal', 'general fitness')
        experience = request.form.get('experience', 'beginner')
        equipment = request.form.get('equipment', 'none')

        # Prompt for the AI model
        prompt = f"""
        You are a certified professional fitness trainer.
        Create a personalized 7-day workout plan for {name}, a {age}-year-old {gender}.
        Goal: {goal}
        Experience Level: {experience}
        Available Equipment: {equipment}

        Include:
        - Warm-up (before workout)
        - Main workout (sets, reps, rest)
        - Weekly schedule (Day 1 to Day 7)
        - Cooldown
        - Tips for recovery and motivation
        """

        # Generate workout plan with OpenAI
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional fitness coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

        workout_plan = response.choices[0].message.content.strip()

        return render_template('index.html', workout_plan=workout_plan, name=name)

    except Exception as e:
        # Handle any internal errors gracefully
        return render_template('index.html', workout_plan=f"⚠️ Error generating plan: {str(e)}")

# --- Run Flask App ---
if __name__ == "_main_":
    app.run(debug=True)