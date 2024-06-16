from app import app, db, bot
import view
from models.model import *


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)