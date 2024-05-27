# app.py
from flask import Flask, request, jsonify, render_template
import difflib
import time
import threading
import datetime

app = Flask(__name__)

# Dummy timetable for a week
timetable = {
    "Monday": [("Math", "08:00 AM"), ("English", "10:00 AM"), ("Physics", "12:03 PM")],
    "Tuesday": [("Biology", "09:00 AM"), ("Chemistry", "11:00 AM"), ("History", "02:00 PM")],
    "Wednesday": [("Math", "08:00 AM"), ("Art", "10:00 AM"), ("PE", "01:00 PM")],
    "Thursday": [("Geography", "09:00 AM"), ("English", "11:00 AM"), ("Physics", "02:00 PM")],
    "Friday": [("Math", "08:00 AM"), ("Chemistry", "10:00 AM"), ("Computer Science", "01:00 PM")],
}

qa_dict = {
    "What classes am I having today?": "Please ask for today's classes.",
    "What's today's date?": "Please ask for today's date.",
    "Do I have physics today?": "Please ask if you have physics today."
}

def find_best_match(user_message):
    best_match = None
    highest_similarity = 0.0

    for question in qa_dict.keys():
        similarity = difflib.SequenceMatcher(None, user_message, question).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = question

    return best_match, highest_similarity

def get_classes_for_today():
    today = datetime.datetime.now().strftime("%A")
    classes_today = timetable.get(today, [])
    return classes_today

def check_for_class():
    while True:
        now = datetime.datetime.now().strftime("%H:%M %p")
        today = datetime.datetime.now().strftime("%A")
        classes_today = timetable.get(today, [])
        for cls, cls_time in classes_today:
            if now == cls_time:
                # Ring alarm
                print(f"ALARM: You have {cls} now!")
                time.sleep(60) 
        time.sleep(60) 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    best_match, similarity = find_best_match(user_message)
    response = "Sorry, I don't understand that question."
    if similarity > 0.7:
        if best_match == "What classes am I having today?":
            classes_today = get_classes_for_today()
            if not classes_today:
                response = "You have no classes today."
            else:
                response = "Your classes today are:\n" + "\n".join([f"{cls[0]} at {cls[1]}" for cls in classes_today])
        elif best_match == "What's today's date?":
            response = f"Today's date is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
        elif best_match == "Do I have physics today?":
            classes_today = get_classes_for_today()
            if any(cls[0] == "Physics" for cls in classes_today):
                response = "Yes, you have physics today."
            else:
                response = "No, you don't have physics today."
        else:
            response = qa_dict[best_match]
    return jsonify({"response": response})

if __name__ == '__main__':
    alarm_thread = threading.Thread(target=check_for_class)
    alarm_thread.daemon = True
    alarm_thread.start()
    app.run(debug=True)
