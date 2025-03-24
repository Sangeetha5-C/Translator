
from flask import Flask, render_template, request
import sqlite3
from deep_translator import GoogleTranslator
app = Flask(__name__)
# Function to translate Tamil to English
def translate_tamil_to_english(tamil_text):
    return GoogleTranslator(source='auto', target='english').translate(tamil_text)
# Function to translate English to Tamil
def translate_english_to_tamil(english_text):
    return GoogleTranslator(source='auto', target='tamil').translate(english_text)
# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            translated_text TEXT NOT NULL,
            translation_mode TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
# Route for the homepage
@app.route("/", methods=["GET", "POST"])
def home():
    tamil_sentence = ""
    translation = ""
    translation_mode = "tamil_to_english"
    if request.method == "POST":
        tamil_sentence = request.form.get("tamil_text", "").strip()
        translation_mode = request.form.get("translation_mode", "tamil_to_english")
        if tamil_sentence:
            # Perform translation
            if translation_mode == "tamil_to_english":
                translation = translate_tamil_to_english(tamil_sentence)
            elif translation_mode == "english_to_tamil":
                translation = translate_english_to_tamil(tamil_sentence)
            # Save translation to the database
            conn = sqlite3.connect('translations.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO translations (input_text, translated_text, translation_mode)
                VALUES (?, ?, ?)
            ''', (tamil_sentence, translation, translation_mode))
            conn.commit()
            conn.close()
        else:
            translation = "Please enter a valid sentence"
    return render_template('trans.html', translation=translation, tamil_sentence=tamil_sentence, translation_mode=translation_mode)
# Route to display stored translations
@app.route("/view-data", methods=["GET"])
def view_data():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM translations;")
    rows = cursor.fetchall()
    conn.close()
    return render_template('view_data.html', rows=rows)
if __name__ == "__main__":
    # Initialize the database when the app starts
    init_db()
    app.run(debug=True)









