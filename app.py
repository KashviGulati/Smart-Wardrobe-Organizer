from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3
from outfit_rules import suggest_outfit  # Import the outfit suggestion function
from weather_api import get_weather  # You should have a weather fetching function

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create database connection function
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
@app.route('/wardrobe')
def wardrobe():
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
    return redirect(url_for('wardrobe'))

# Route for outfit suggestions
@app.route('/suggest_outfit')
def suggest_outfit_page():
    weather = get_weather()  # Function to fetch current weather data (returns a tuple)
    outfit = suggest_outfit(weather)  # Suggest outfit based on the weather
    temp, weather_condition = weather  # Unpack the returned tuple

    return render_template('suggest.html', outfit=outfit, temp=temp, weather_condition=weather_condition)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to fetch weather data (for suggestion purposes)
@app.route('/get_weather')
def get_weather_data():
    weather = get_weather()  # Example of using the weather API
    return render_template('weather.html', weather=weather)

# Change this route to 'view_wardrobe' in app.py
@app.route('/wardrobe')
def view_wardrobe():
    conn = get_db()
    wardrobe_items = conn.execute('SELECT * FROM wardrobe').fetchall()
    conn.close()
    return render_template('wardrobe.html', wardrobe_items=wardrobe_items)

if __name__ == '__main__':
    app.run(debug=True)
