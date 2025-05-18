from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import os
import io
import xlsxwriter

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'html'}

app = Flask(__name__, 
    static_folder='static',
    template_folder='templates'
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Create required directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_usernames(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        usernames_with_dates = []
        for user_div in soup.find_all('div', class_='pam'):
            a_tag = user_div.find('a', target='_blank')
            date_div = a_tag.find_next('div') if a_tag else None
            if a_tag:
                username = a_tag.text.strip()
                date = date_div.text.strip() if date_div else 'Unknown date'
                usernames_with_dates.append({'username': username, 'date': date})
        return usernames_with_dates
    except Exception as e:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'followers' not in request.files or 'following' not in request.files:
            flash('Please upload both followers and following files', 'error')
            return redirect(url_for('index'))

        followers_file = request.files['followers']
        following_file = request.files['following']

        if followers_file.filename == '' or following_file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))

        if not (followers_file and allowed_file(followers_file.filename) and 
                following_file and allowed_file(following_file.filename)):
            flash('Invalid file type. Please upload HTML files only', 'error')
            return redirect(url_for('index'))

        followers_filename = secure_filename(followers_file.filename)
        following_filename = secure_filename(following_file.filename)

        followers_path = os.path.join(app.config['UPLOAD_FOLDER'], followers_filename)
        following_path = os.path.join(app.config['UPLOAD_FOLDER'], following_filename)

        followers_file.save(followers_path)
        following_file.save(following_path)

        # Process the uploaded files and generate the results
        followers = extract_usernames(followers_path)
        following = extract_usernames(following_path)

        if not followers or not following:
            flash('Could not extract usernames from the files. Please check if the files are valid.', 'error')
            return redirect(url_for('index'))

        # Convert to sets for comparison
        followers_set = {item['username'] for item in followers}
        following_set = {item['username'] for item in following}

        # Find fans and snakes with their dates
        fans = [item for item in followers if item['username'] not in following_set]
        snakes = [item for item in following if item['username'] not in followers_set]
        mutuals = [item for item in followers if item['username'] in following_set]

        # Clean up uploaded files
        os.remove(followers_path)
        os.remove(following_path)

        return render_template('result.html', fans=fans, snakes=snakes, mutuals=mutuals)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/export_excel', methods=['POST'])
def export_excel():
    data = request.json
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    for sheet_name in ['Fans', 'Snakes', 'Mutuals']:
        worksheet = workbook.add_worksheet(sheet_name)
        worksheet.write_row(0, 0, ['Username', 'Follow Date'])
        for idx, item in enumerate(data.get(sheet_name.lower(), []), 1):
            worksheet.write_row(idx, 0, [item['username'], item['date']])
    workbook.close()
    output.seek(0)
    return send_file(output, download_name='instagram_analysis.xlsx', as_attachment=True)

@app.errorhandler(405)
def method_not_allowed(e):
    flash('Invalid request method. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
