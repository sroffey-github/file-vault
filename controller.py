from dotenv import load_dotenv
import hashlib, sqlite3, os

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH')
FILES_PATH = os.getenv('FILES_PATH')

def init():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    c.close()
    conn.close()

def authenticate(usern, passwd):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    passwd = hashlib.sha256(passwd.encode()).hexdigest()
    c.execute('SELECT username FROM Users WHERE username = ? AND password = ?', (usern, passwd))
    results = c.fetchall()
    if results:
        return True
    else:
        return False

def human_size(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])

def get_files():
    file_list = []

    filenames = os.listdir(FILES_PATH)
    for f in filenames:
        size = human_size(os.path.getsize(FILES_PATH + f))
        ctime = os.path.getctime(FILES_PATH + f)
        file_list.append([ctime, f, size])

    return file_list