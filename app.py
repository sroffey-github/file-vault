from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import controller, uuid, os

load_dotenv()

FILES_PATH = os.getenv('FILES_PATH')
TEMP_FILE_PATH = FILES_PATH + 'temp/'
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
        if request.method == 'POST': pass
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
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
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

@app.route('/share', methods=['GET', 'POST'])
def share():
    if session.get('username'):
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            # if file and allowed_file(file.filename): # Uncomment this line to filter file types
            filename = secure_filename(file.filename)
            file.save(os.path.join(TEMP_FILE_PATH, filename))
            link = controller.get_link(file.filename)
            return render_template('share.html', link=f'{request.host_url}share/{link}')
        else:
            return render_template('share.html')
    else:
        return redirect(url_for('index'))

@app.route('/share/<unique_id>')
def shared_file(unique_id):
    filename = controller.check_id(unique_id)
    if filename == False:
        return 'Invalid Id'
    else:
        filename = filename[0]
        if os.path.isfile(TEMP_FILE_PATH + filename):
            try:
                return send_from_directory(directory=TEMP_FILE_PATH, path=filename, as_attachment=True)
            finally:
                controller.delete_share(unique_id, TEMP_FILE_PATH + filename)
        else:
            return 'Invald Id'

controller.init()

if __name__ == '__main__':
    app.run(port=8080, debug=False)