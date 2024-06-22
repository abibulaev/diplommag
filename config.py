class Configuration:
    #All config
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = '73870e7f-634d-433b-946a-8d20132bafac'

    UPLOAD_FOLDER = './static/files/'
   
    
    #DataBase
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/itplaner'