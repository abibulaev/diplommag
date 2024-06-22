from app import app, login_manager, TELEGRAM_AUTH_URL, send_notification, mass_send_notification
from flask import render_template, request, redirect, url_for, jsonify, send_from_directory, abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from models.model import *
from flask_login import login_user, logout_user
from flask_login import current_user, login_required, logout_user
import random
import string
import os


login_manager.login_view = 'login'

user = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("landing.html")

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        if (password == confirm_password) and username and email:
             passw = generate_password_hash(password)
             user = User(username=username, email=email, password_hash=passw)
             db.session.add(user)
             db.session.commit()
             return(redirect(url_for('login')))
    return render_template("registr.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global user
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('redirect_to_telegram'))
    return render_template("log_in.html")

@app.route('/telegram_auth', methods=['GET', 'POST'])
def telegram_auth():
    global user
    data = request.get_json()
    chat_id = data.get('chat_id')
    if user:
        user.chat_id = chat_id
        db.session.add(user)
        db.session.commit()
    return jsonify({"status": "success"}), 200

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
    project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    return render_template('main.html', user = current_user, projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
    project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    if request.method == "POST":
        invite_code = request.form.get('invite_code')
        if invite_code:
            project = Project.query.filter_by(code=invite_code).first()
            project.team.append(current_user)
            db.session.add(project)
            db.session.commit()
            send_notification(project.teamlead.chat_id, f'Пользователь {current_user.username} присоединилися к проекту {project.name}')
            return redirect(url_for('home'))
        else:
            title = request.form.get('project-name')
            description = request.form.get('project-description')
            start_date = request.form.get('project-start-date')
            end_date = request.form.get('project-end-date')
            code = generate_random_code()
            file = request.files['task-file']
            check_code = Project.query.filter_by(code=code).first()
            if not check_code:
                if file:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    project = Project(name=title, description=description, start_date=start_date, end_date=end_date, code=code, file_url=filepath, teamlead_id=current_user.id)
                    db.session.add(project)
                    db.session.commit()
                else:
                    project = Project(name=title, description=description, start_date=start_date, end_date=end_date, code=code, teamlead_id=current_user.id)
                    db.session.add(project)
                    db.session.commit()
                return redirect(url_for('home'))

    return render_template('add_project.html', user = current_user, date = datetime.now().strftime('%Y-%m-%d'), projects=projects)

def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choices(characters, k=length))
    return random_code

@app.route('/project/team', methods=['GET', 'POST'])
@login_required
def team():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
    project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    teamlead = User.query.filter_by(id=project.teamlead_id).first()
    return render_template('team.html', user = current_user, project=project, teamlead=teamlead, projects=projects)

@app.route('/project/epictable', methods=['GET', 'POST'])
@login_required
def epiccard():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
        project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    epics = Epic.query.filter_by(project_id=project_id).all()

    epic_data = []

    for epic in epics:
        total_tasks = len(epic.tasks)
        completed_tasks = len([task for task in epic.tasks if task.status == 'Закрыта'])
        print(completed_tasks)
        progress = round((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
        epic_data.append({
            'epic': epic,
            'progress': progress
        })

    return render_template('epiccard.html', user=current_user, project=project, epics=epic_data, projects=projects)

@app.route('/project/tasktable', methods=['GET', 'POST'])
@login_required
def tasktable():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
    project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    tasks = Task.query.filter((Task.user_id == current_user.id) & (Task.project_id==project_id)).all()

    total_tasks = len(tasks)
    if total_tasks > 0:
        done_tasks = len([task for task in tasks if task.status == 'Закрыта'])
        progress_percentage = round((done_tasks / total_tasks) * 100)
    else:
        progress_percentage = 0

    return render_template('tasktable.html', user = current_user, project=project, tasks=tasks, projects=projects, progress_percentage=progress_percentage)

@app.route('/project/addepic', methods=['GET', 'POST'])
@login_required
def addepic():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
        project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    
    if request.method == 'POST':
        title = request.form.get('goal-name')
        description = request.form.get('goal-description')
        start_date = request.form.get('goal-start-date')
        end_date = request.form.get('goal-end-date')

        epic = Epic(title=title, description=description, start_date=start_date, end_date=end_date, project_id=project_id)
        db.session.add(epic)
        db.session.commit()

        mass_send_notification(project.team, f'Была создана цель {title}')
        
        return redirect(url_for('addepic', project_id=project_id))

    return render_template('addepic.html', user=current_user, project=project, projects=projects)

@app.route('/project/addtask', methods=['GET', 'POST'])
@login_required
def addtask():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
    project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    epics = Epic.query.filter_by(project_id=project_id).all()
    if request.method == 'POST':
        epic_id = request.form.get('project-title')
        user_id = request.form.get('manager-name')
        title = request.form.get('task-title')
        description = request.form.get('task-desc')
        end_date = request.form.get('task-deadline')
        task_priority = request.form.get('task-priority')

        file = request.files['task-file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            task = Task(title=title, description=description, end_date=end_date, priority=task_priority, status='Поставлена', file_url=filepath, user_id=user_id, project_id=project_id)
            epic = Epic.query.filter_by(id=epic_id).first()
            epic.tasks.append(task)
            db.session.add(task, epic)
            db.session.commit()
        else:
            task = Task(title=title, description=description, end_date=end_date, priority=task_priority, status='Поставлена', user_id=user_id, project_id=project_id)
            epic = Epic.query.filter_by(id=epic_id).first()
            epic.tasks.append(task)
            db.session.add(task, epic)
            db.session.commit()

        send_notification(User.query.filter_by(id=user_id).first().chat_id, 
                          f'Была создана новая задача для вас: {title} \nОписание: {description} \nДедлайн: {end_date}')

        return redirect(url_for('addtask', project_id=project_id))
    return render_template('addtask.html', user = current_user, project=project, epics=epics, projects=projects)

@app.route('/project/taskcard', methods=['GET', 'POST'])
@login_required
def taskcard():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
    project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    project_id = request.args.get('project_id')
    task_id = request.args.get('task_id')
    task = Task.query.filter_by(id=task_id).first()
    project = Project.query.filter_by(id=project_id).first()
    comments = Comment.query.filter_by(task_id=task_id).all()
    
    if request.method == 'POST':
        text = request.form.get('comment_text')
        comment = Comment(user_id=current_user.id, text=text, task_id=task_id)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('taskcard', project_id=project_id, task_id=task_id))

    return render_template('taskcard.html', user = current_user, project=project, task=task, projects=projects, comments=comments)

@app.route('/project', methods=['GET', 'POST'])
@login_required
def project():
    projects_as_teamlead = Project.query.filter(Project.teamlead_id == current_user.id).all()
    team_member_query = db.session.query(project_user_association.c.project_id).filter(
    project_user_association.c.user_id == current_user.id)
    projects_as_team_member = Project.query.filter(Project.id.in_(team_member_query)).all()
    projects = list(set(projects_as_teamlead + projects_as_team_member))
    project_id = request.args.get('project_id')
    project = Project.query.filter_by(id=project_id).first()
    return render_template('project.html', user = current_user, project=project, projects=projects)

@app.route('/changestatus')
@login_required
def changestatus():
    project_id = request.args.get('project_id')
    task_id = request.args.get('task_id')
    status = request.args.get('status')
    print(status)
    task = Task.query.filter_by(id=task_id).first()
    
    if status == 'proceed':
        task.status = 'Выполняется'
        task.start_date = datetime.utcnow()  # Фиксация времени начала задачи
        db.session.add(task)
        db.session.commit()

        send_notification(Project.query.filter_by(id=project_id).first().teamlead.chat_id, f"Пользователь {User.query.filter_by(id=task.user_id).first().username} приступил к задаче - {task.title}")

        return redirect(url_for('taskcard', project_id=project_id, task_id=task_id))
    
    if status == 'close':
        task.status = 'Закрыта'
        task.complete_task()  # Фиксация времени завершения задачи
        db.session.add(task)
        db.session.commit()
        send_notification(Project.query.filter_by(id=project_id).first().teamlead.chat_id, f"Пользователь {User.query.filter_by(id=task.user_id).first().username} закрыл задачу - {task.title}")
        
        return redirect(url_for('taskcard', project_id=project_id, task_id=task_id))

@app.route('/redirect_to_telegram')
def redirect_to_telegram():
    return render_template('redirect.html', url=TELEGRAM_AUTH_URL)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory='./', path=filename, as_attachment=True)