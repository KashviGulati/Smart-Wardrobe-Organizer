import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Config
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['DATABASE'] = 'wardrobe.db'

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create DB if it doesn't exist
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wardrobe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    category TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['image']
        category = request.form['category']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Save to DB
            conn = sqlite3.connect(app.config['DATABASE'])
            c = conn.cursor()
            c.execute("INSERT INTO wardrobe (filename, category) VALUES (?, ?)", (filename, category))
            conn.commit()
            conn.close()

            return redirect(url_for('home'))

    return render_template('upload.html')
@app.route('/wardrobe')
def view_wardrobe():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT * FROM wardrobe")
    items = c.fetchall()  # Fetch all items from wardrobe table
    conn.close()
    
    # Pass items to the template for rendering
    return render_template('wardrobe.html', items=items)



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
