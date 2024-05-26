# app.py
from flask import Flask, request, jsonify, render_template
import difflib

app = Flask(__name__)

# Predefined questions and answers
qa_dict = {
    "How are you?": "I'm fine, thank you!",
    "What is your name?": "I am a chatbot.",
    "What can you do?": "I can answer simple predefined questions.",
    "What is the capital of France?": "The capital of France is Paris.",
    "Who wrote 'To Kill a Mockingbird'?": "Harper Lee wrote 'To Kill a Mockingbird'.",
    "What is the speed of light?": "The speed of light is approximately 299,792 kilometers per second.",
    "What is the tallest mountain in the world?": "Mount Everest is the tallest mountain in the world.",
    "What is the largest ocean on Earth?": "The Pacific Ocean is the largest ocean on Earth.",
    "What is the smallest country in the world?": "The Vatican City is the smallest country in the world.",
    "Who painted the Mona Lisa?": "Leonardo da Vinci painted the Mona Lisa.",
    "What is the chemical symbol for water?": "The chemical symbol for water is H2O.",
    "Who developed the theory of relativity?": "Albert Einstein developed the theory of relativity.",
    "What is the currency of Japan?": "The currency of Japan is the Yen.",
    "What year did the Titanic sink?": "The Titanic sank in 1912.",
    "What is the capital of Japan?": "The capital of Japan is Tokyo.",
    "Who was the first person to walk on the moon?": "Neil Armstrong was the first person to walk on the moon.",
    "What is the largest planet in our solar system?": "Jupiter is the largest planet in our solar system.",
    "What is the hardest natural substance on Earth?": "Diamond is the hardest natural substance on Earth.",
    "What is the longest river in the world?": "The Nile River is the longest river in the world.",
    "What is the boiling point of water?": "The boiling point of water is 100 degrees Celsius.",
    "What is the most widely spoken language in the world?": "Mandarin Chinese is the most widely spoken language in the world.",
    "Who is the author of the Harry Potter series?": "J.K. Rowling is the author of the Harry Potter series.",
    "What is the largest continent?": "Asia is the largest continent.",
    "What is the most populous country in the world?": "China is the most populous country in the world.",
    "What is the smallest planet in our solar system?": "Mercury is the smallest planet in our solar system.",
    "What is the main ingredient in guacamole?": "The main ingredient in guacamole is avocado.",
    "Who discovered penicillin?": "Alexander Fleming discovered penicillin.",
    "What is the currency of the United Kingdom?": "The currency of the United Kingdom is the Pound Sterling.",
    "What is the capital of Australia?": "The capital of Australia is Canberra.",
    "What is the largest mammal in the world?": "The blue whale is the largest mammal in the world.",
    "What is the primary gas found in the Earth's atmosphere?": "Nitrogen is the primary gas found in the Earth's atmosphere.",
    "Who painted the Sistine Chapel ceiling?": "Michelangelo painted the Sistine Chapel ceiling.",
    "What is the powerhouse of the cell?": "The mitochondrion is the powerhouse of the cell.",
    "What is the capital of Canada?": "The capital of Canada is Ottawa.",
    "What is the fastest land animal?": "The cheetah is the fastest land animal.",
    "Who wrote 'Pride and Prejudice'?": "Jane Austen wrote 'Pride and Prejudice'.",
    "What is the main ingredient in chocolate?": "Cocoa beans are the main ingredient in chocolate.",
    "What is the tallest building in the world?": "The Burj Khalifa is the tallest building in the world.",
    "What is the freezing point of water?": "The freezing point of water is 0 degrees Celsius.",
    "Who was the first President of the United States?": "George Washington was the first President of the United States.",
    "What is the longest bone in the human body?": "The femur is the longest bone in the human body.",
    "What is the capital of Italy?": "The capital of Italy is Rome.",
    "Who wrote 'The Odyssey'?": "Homer wrote 'The Odyssey'.",
    "What is the largest desert in the world?": "The Sahara Desert is the largest desert in the world.",
    "What is the most abundant element in the universe?": "Hydrogen is the most abundant element in the universe.",
    "What is the name of the galaxy we live in?": "We live in the Milky Way galaxy.",
    "Who painted 'Starry Night'?": "Vincent van Gogh painted 'Starry Night'.",
    "What is the main language spoken in Brazil?": "Portuguese is the main language spoken in Brazil.",
    "What is the capital of Russia?": "The capital of Russia is Moscow.",
    "What is the heaviest organ in the human body?": "The liver is the heaviest organ in the human body.",
    "What is the process by which plants make food?": "Photosynthesis is the process by which plants make food.",
    "What is the capital of China?": "The capital of China is Beijing.",
    "What is the most common blood type?": "The most common blood type is O positive.",
    "Who wrote 'Moby-Dick'?": "Herman Melville wrote 'Moby-Dick'.",
    "What is the smallest bone in the human body?": "The stapes is the smallest bone in the human body.",
    "What is the capital of India?": "The capital of India is New Delhi.",
    "Who is known as the 'Father of Computers'?": "Charles Babbage is known as the 'Father of Computers'.",
    "What is the highest waterfall in the world?": "Angel Falls is the highest waterfall in the world.",
    "What is the largest island in the world?": "Greenland is the largest island in the world.",
    "What is the most spoken language in Africa?": "Swahili is the most spoken language in Africa.",
    "Who wrote 'The Great Gatsby'?": "F. Scott Fitzgerald wrote 'The Great Gatsby'.",
    "What is the main ingredient in sushi?": "Rice is the main ingredient in sushi.",
    "What is the capital of Germany?": "The capital of Germany is Berlin.",
    "Who discovered America?": "Christopher Columbus is often credited with discovering America.",
    "What is the largest organ in the human body?": "The skin is the largest organ in the human body.",
    "What is the tallest tree species?": "The coast redwood is the tallest tree species.",
    "What is the main gas in the Earth's atmosphere?": "Nitrogen is the main gas in the Earth's atmosphere.",
    "What is the capital of Spain?": "The capital of Spain is Madrid.",
    "Who wrote '1984'?": "George Orwell wrote '1984'.",
    "What is the hardest substance in the human body?": "Tooth enamel is the hardest substance in the human body.",
    "What is the capital of Egypt?": "The capital of Egypt is Cairo.",
    "Who is known as the 'Queen of Soul'?": "Aretha Franklin is known as the 'Queen of Soul'.",
    "What is the currency of Brazil?": "The currency of Brazil is the Real.",
    "What is the highest mountain in Africa?": "Mount Kilimanjaro is the highest mountain in Africa.",
    "Who wrote 'The Catcher in the Rye'?": "J.D. Salinger wrote 'The Catcher in the Rye'.",
    "What is the capital of Mexico?": "The capital of Mexico is Mexico City.",
    "What is the largest lake in the world?": "The Caspian Sea is the largest lake in the world.",
    "What is the most common gas in the Earth's atmosphere?": "Nitrogen is the most common gas in the Earth's atmosphere.",
    "Who painted 'The Last Supper'?": "Leonardo da Vinci painted 'The Last Supper'.",
    "What is the main ingredient in beer?": "Barley is the main ingredient in beer.",
    "What is the capital of South Korea?": "The capital of South Korea is Seoul.",
    "What is the largest reptile in the world?": "The saltwater crocodile is the largest reptile in the world.",
    "Who wrote 'The Divine Comedy'?": "Dante Alighieri wrote 'The Divine Comedy'.",
    "What is the main ingredient in bread?": "Flour is the main ingredient in bread.",
    "What is the capital of Argentina?": "The capital of Argentina is Buenos Aires.",
    "Who painted 'The Persistence of Memory'?": "Salvador Dalí painted 'The Persistence of Memory'.",
    "What is the smallest country in Asia?": "The Maldives is the smallest country in Asia.",
    "What is the main ingredient in pizza?": "The main ingredient in pizza is dough.",
    "What is the capital of Saudi Arabia?": "The capital of Saudi Arabia is Riyadh.",
    "Who wrote 'War and Peace'?": "Leo Tolstoy wrote 'War and Peace'.",
    "What is the most abundant gas in the Earth's atmosphere?": "Nitrogen is the most abundant gas in the Earth's atmosphere.",
    "What is the capital of Thailand?": "The capital of Thailand is Bangkok.",
    "Who painted 'Guernica'?": "Pablo Picasso painted 'Guernica'."
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    best_match, similarity = find_best_match(user_message)
    if similarity > 0.7:
        response = qa_dict[best_match]
    else:
        response = "Sorry, I don't understand that question."
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
