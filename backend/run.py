import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    flask_env = os.getenv('FLASK_ENV', 'development')
    if flask_env == 'production':
        app.run(host='0.0.0.0', port=5000) # access from all IPs
    else:
        app.run()
    
    
# flask --app run run --debug
