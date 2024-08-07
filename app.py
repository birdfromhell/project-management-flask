from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.secret_key='lloveyou'
    

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        user_obj = User()
        user_obj.id = user[0]
        return user_obj
    return None
    

@app.route('/')
@login_required
def index():
        cur = mysql.connection.cursor()
        cur_client = mysql.connection.cursor()
        cur.execute("""SELECT tb_m_project.*, tb_m_client.client_name, DATE_FORMAT(project_start, "%d %b %Y") AS formatted_start, DATE_FORMAT(project_end, "%d %b %Y") AS formatted_end 
        FROM tb_m_project INNER JOIN tb_m_client ON tb_m_project.client_id = tb_m_client.client_id;""")
        cur_client.execute('SELECT * FROM tb_m_client')
        data = cur.fetchall()
        data_client = cur_client.fetchall()
        cur.close()
        cur_client.close()
        return render_template('index.html', projects=data, clients=data_client)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember') == 'on'
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            user_obj = User()
            user_obj.id = user[0]
            session.permanent = True
            login_user(user_obj,remember=remember)
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        print("Form Data Received:", request.form)
        project_name= request.form ['project_name']
        client = request.form ['client']
        status = request.form ['status']

        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO tb_m_project (project_name, client_id, project_status) VALUES(%s,%s,%s)',
                    (project_name, client, status))
        mysql.connection.commit()
        flash('Project Berhasil Ditambahkan')

    return redirect(url_for('index'))

@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        print("Form Data Received:", request.form)  # Debugging line
        client_name = request.form.get('client_name')
        client_address = request.form.get('client_address')

        if not client_name or not client_address:
            flash('Client name and address are required!', 'error')
            return redirect(url_for('index'))

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tb_m_client (client_name, client_address) VALUES(%s,%s)',
                    (client_name, client_address))
        mysql.connection.commit()
        flash('Client Berhasil Ditambahkan')

    return redirect(url_for('index'))

@app.route('/edit_project/<project_id>', methods=['POST'])
def edit_project(project_id):
    if request.method == 'POST':
        project_name= request.form ['project_name']
        client = request.form ['client']
        project_start = request.form ['project_start']
        project_end = request.form ['project_end']
        status = request.form ['status']
    
    cur=mysql.connection.cursor()
    sql = 'UPDATE tb_m_project SET project_name=%s, client_id=%s, project_start=%s, project_end=%s, project_status=%s WHERE project_id=%s'
    data = (project_name, client, project_start, project_end, status, project_id)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    cur=mysql.connection.cursor()
    cur.execute(f'DELETE from tb_m_project WHERE project_id = {project_id}')
    mysql.connection.commit()
    flash('Project Berhasil Di hapus')
    return redirect(url_for('index'))

@app.route('/change_status/<project_id>')
def change_status(project_id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT project_status FROM tb_m_project WHERE project_id = {project_id}')
    status = cur.fetchone()
    if status[0] == 'DONE':
        status = 'OPEN'
    elif status[0] == 'OPEN':
        status = 'DOING'
        cur.execute(f'UPDATE tb_m_project SET project_status = "{status}", project_start = CURDATE() WHERE project_id = {project_id}')
    else:
        status = 'DONE'
        cur.execute(f'UPDATE tb_m_project SET project_status = "{status}", project_end = CURDATE() WHERE project_id = {project_id}')
    cur.execute(f'UPDATE tb_m_project SET project_status = "{status}" WHERE project_id = {project_id}')
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(port=8080, debug=True)
