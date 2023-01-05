from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import controller, uuid, os

load_dotenv()

FILES_PATH = os.getenv('FILES_PATH')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
app.config['UPLOAD_FOLDER'] = FILES_PATH

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('username'):
        if request.method == 'POST':
            usern = request.form['usern']
            passwd = request.form['passwd']
            login = controller.authenticate(usern, passwd)
            if login:
                session['username'] = usern
                return render_template('index.html', files=controller.get_files())
            else:
                flash('Invalid Username or Password')
                return render_template('index.html')
        else:
            return render_template('index.html')
    else:
        if request.method == 'POST':
            pass
        else:
            return render_template('index.html', files=controller.get_files())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    if os.path.isfile(FILES_PATH + filename):
        return send_from_directory(directory=FILES_PATH, path=filename, as_attachment=True)
    else:
        return redirect(url_for('index', files=controller.get_files()))

@app.route('/delete/<filename>')
def delete(filename):
    if os.path.isfile(FILES_PATH + filename):
        os.remove(FILES_PATH + filename)
        return redirect(url_for('index', files=controller.get_files()))
    else:
        return redirect(url_for('index', files=controller.get_files()))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if session.get('username'):
        if request.method == 'POST':
            print('handling...')
            if 'file' not in request.files:
                print('No file part')
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                print('No selected file')
                flash('No selected file')
                return redirect(request.url)
            # if file and allowed_file(file.filename): # Uncomment this line to filter file types
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index', files=controller.get_files()))
        else:
            return render_template('upload.html')
    else:
        return redirect(url_for('index'))

controller.init()

if __name__ == '__main__':
    app.run(port=8080, debug=True)