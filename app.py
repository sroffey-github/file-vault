from flask import Flask, render_template, request, flash, session, redirect, url_for, send_from_directory
from dotenv import load_dotenv
import controller, uuid, os

load_dotenv()

FILES_PATH = os.getenv('FILES_PATH')

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

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

if __name__ == '__main__':
    controller.init()
    app.run(debug=True)