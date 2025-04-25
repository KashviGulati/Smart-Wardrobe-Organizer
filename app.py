from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
from outfit_rules import suggest_outfit, suggest_mood_outfit
from weather_api import get_weather
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from chatbot import initialize_gemini, get_fashion_advice 

app = Flask(__name__)
app.secret_key = "wardrobe_secret_key"
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect('wardrobe.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        category = request.form['category']
        season = request.form.get('season', 'summer')
        gender = request.form.get('gender', 'unisex')
        occasion = request.form.get('occasion', 'casual')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = get_db()
            conn.execute(
                "INSERT INTO wardrobe (filename, category, season, gender) VALUES (?, ?, ?, ?)", 
                (filename, category, season, gender)
            )
            conn.commit()
            conn.close()

            flash('Clothing item added successfully!', 'success')
            return redirect(url_for('view_wardrobe'))

    return render_template('upload.html')

@app.route('/view_wardrobe')
def view_wardrobe():
    conn = get_db()
    wardrobe_items = conn.execute('SELECT * FROM wardrobe').fetchall()
    conn.close()
    return render_template('wardrobe.html', wardrobe_items=wardrobe_items)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db()
    item = conn.execute('SELECT filename FROM wardrobe WHERE id = ?', (item_id,)).fetchone()
    
    if item:
        conn.execute('DELETE FROM wardrobe WHERE id = ?', (item_id,))
        conn.commit()
        
        try:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], item['filename'])
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file: {e}")
    
    conn.close()
    return redirect(url_for('view_wardrobe'))

@app.route('/suggest_outfit')
def suggest_outfit_page():
    weather = get_weather()
    if weather[0] is None:
        return render_template('suggest.html', error="Could not fetch weather data")
    
    outfit_data = suggest_outfit(weather)
    outfits = outfit_data.get('outfits', [])
    description = outfit_data.get('description', '')
    categories = outfit_data.get('categories', [])
    season = outfit_data.get('season', '')
    
    temp, weather_condition = weather

    if not outfits and categories:
        missing_categories = ", ".join(categories)
        flash(f"No matching {missing_categories} found in your wardrobe for {season} season. Showing recommended outfit instead.", 'info')

    return render_template('suggest.html', 
                          outfits=outfits, 
                          outfit_description=description,
                          temp=temp, 
                          weather_condition=weather_condition,
                          missing_categories=categories if not outfits else None)

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
        
        outfit_data = suggest_mood_outfit(sentiment)
        outfits = outfit_data.get('outfits', [])
        description = outfit_data.get('description', '')
        categories = outfit_data.get('categories', [])
        colors = outfit_data.get('colors', '')
        
        if not outfits and categories:
            missing_categories = ", ".join(categories)
            flash(f"No matching {missing_categories} found in your wardrobe. Showing recommended outfit instead.", 'info')
        
        return render_template('suggest_mood.html', 
                              mood=mood_text, 
                              sentiment=sentiment, 
                              outfits=outfits,
                              outfit_description=description,
                              colors=colors,
                              missing_categories=categories if not outfits else None)
    
    return render_template('suggest_mood.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Add these imports at the top of the file
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
from outfit_rules import suggest_outfit, suggest_mood_outfit
from weather_api import get_weather
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from chatbot import initialize_gemini, get_fashion_advice  

@app.route('/fashion_chat')
def fashion_chat():
    return render_template('fashion_chat.html')

@app.route('/validate_api_key', methods=['POST'])
def validate_api_key():
    data = request.json
    api_key = data.get('api_key')
    
    try:
        # Attempt to initialize Gemini with the provided API key
        result = initialize_gemini(api_key)
        return jsonify({'success': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_fashion_advice', methods=['POST'])
def get_fashion_advice_route():
    data = request.json
    message = data.get('message')
    api_key = data.get('api_key')
    
    if not message or not api_key:
        return jsonify({'response': 'Message or API key is missing.'})
    
    try:
        response = get_fashion_advice(message, api_key)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f"Sorry, I encountered an error: {str(e)}"})

# Rest of the app.py file remains unchanged

def init_db():
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS wardrobe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        category TEXT NOT NULL,
        season TEXT DEFAULT 'summer',
        gender TEXT DEFAULT 'unisex',
        occasion TEXT DEFAULT 'casual'
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)