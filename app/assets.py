import os
from flask_assets import Environment, Bundle

def compile_assets(app):
    assets = Environment(app)
    assets.directory = 'app/static'
    assets.url = '/static'
    
    js = Bundle('js/*.js', filters='jsmin', output='dist/js/main.min.js')
    css = Bundle('css/*.css', filters='cssmin', output='dist/css/main.min.css')
    
    assets.register('js_all', js)
    assets.register('css_all', css)
    
    # Ensure output directories exist
    js_output_dir = os.path.join(assets.directory, 'dist/js')
    css_output_dir = os.path.join(assets.directory, 'dist/css')
    
    os.makedirs(js_output_dir, exist_ok=True)
    os.makedirs(css_output_dir, exist_ok=True)
    
    js.build()
    css.build()
