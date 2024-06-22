from app import db
from datetime import datetime
from flask_login import UserMixin

project_user_association = db.Table('project_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    chat_id =  db.Column(db.String(50))
    password_hash = db.Column(db.String(255), nullable=False)
    projects = db.relationship('Project', secondary=project_user_association, back_populates='team')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    code = db.Column(db.String(6))
    file_url = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    teamlead_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teamlead = db.relationship('User', foreign_keys=[teamlead_id])
    team = db.relationship('User', secondary=project_user_association, back_populates='projects')
    epic_id = db.Column(db.Integer, db.ForeignKey('epic.id'))

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Project {}>'.format(self.name)
    
epic_tasks = db.Table('epic_tasks',
    db.Column('epic_id', db.Integer, db.ForeignKey('epic.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

class Epic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    tasks = db.relationship('Task', secondary=epic_tasks, backref=db.backref('epics', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Epic, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Epic {}>'.format(self.title)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=True)  # Время начала задачи
    end_date = db.Column(db.Date, nullable=True)
    completed_date = db.Column(db.DateTime, nullable=True)  # Время завершения задачи
    priority = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50))
    file_url = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Task {}>'.format(self.title)

    def complete_task(self):
        self.status = 'Закрыта'
        self.completed_date = datetime.utcnow()

    def time_spent(self):
        if self.start_date and self.completed_date:
            return self.completed_date - self.start_date
        return None

    def time_spent(self):
        if self.start_date and self.completed_date:
            return self.completed_date - self.start_date
        return None
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Comment {}>'.format(self.title)