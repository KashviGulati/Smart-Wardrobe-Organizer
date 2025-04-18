from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3
from outfit_rules import suggest_outfit, suggest_mood_outfit
from weather_api import get_weather
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect('wardrobe.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Route for uploading clothes
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        category = request.form['category']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Save to database
            conn = get_db()
            conn.execute("INSERT INTO wardrobe (filename, category) VALUES (?, ?)", (filename, category))
            conn.commit()
            conn.close()

            return redirect(url_for('home'))  # Redirect to home page after upload

    return render_template('upload.html')

# Route to view all clothes in the wardrobe
@app.route('/view_wardrobe')
def view_wardrobe():
    conn = get_db()
    wardrobe_items = conn.execute('SELECT * FROM wardrobe').fetchall()
    conn.close()
    return render_template('wardrobe.html', wardrobe_items=wardrobe_items)

# Route to delete a clothing item
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db()
    conn.execute('DELETE FROM wardrobe WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_wardrobe'))

# Route for outfit suggestions (weather-based)
@app.route('/suggest_outfit')
def suggest_outfit_page():
    weather = get_weather()  # Function to fetch current weather data (returns a tuple)
    outfit = suggest_outfit(weather)  # Suggest outfit based on the weather
    temp, weather_condition = weather  # Unpack the returned tuple

    return render_template('suggest.html', outfit=outfit, temp=temp, weather_condition=weather_condition)

# Route for mood-based outfit suggestions
@app.route('/suggest_mood', methods=['GET', 'POST'])
def suggest_mood_page():
    if request.method == 'POST':
        mood_text = request.form['mood']
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(mood_text)
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        outfit = suggest_mood_outfit(sentiment)
        return render_template('suggest_mood.html', mood=mood_text, sentiment=sentiment, outfit=outfit)
    return render_template('suggest_mood.html')

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to fetch weather data (for suggestion purposes)
@app.route('/get_weather')
def get_weather_data():
    weather = get_weather()  # Example of using the weather API
    return render_template('weather.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)