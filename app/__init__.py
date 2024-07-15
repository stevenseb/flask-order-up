import os
from flask import Flask
from livereload import Server
from app import routes
from app.assets import compile_assets

app = Flask(__name__)
app.config.update({'SECRET_KEY': os.environ.get('SECRET_KEY')})
app.register_blueprint(routes.bp)

# Compile static assets
compile_assets(app)

if __name__ == "__main__":
    # Create a LiveReload server
    server = Server(app.wsgi_app)
    
    # Watch for changes in the static and templates directories
    server.watch('app/static/js/*.*')
    server.watch('app/static/css/*.*')
    server.watch('app/templates/*.*')

    # Watch for changes in Python files
    server.watch('app/routes.py')
    server.watch('app/__init__.py')
    server.watch('app/assets.py')
    server.watch('app.py')
    
    # Use watchdog to monitor changes in Python files
    import subprocess
    def restart_server():
        subprocess.call(['pkill', '-f', 'flask run'])
        subprocess.call(['flask', 'run'])

    server.watch('app/routes.py', restart_server)
    server.watch('app/__init__.py', restart_server)
    server.watch('app/assets.py', restart_server)
    server.watch('app.py', restart_server)
    
    # Start the server
    server.serve(port=5000, host='127.0.0.1', open_url=True)
