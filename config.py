class Configuration:
    #All config
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'asfasfasfas'
    
    #DataBase
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/itplaner'
