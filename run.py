import sys
import os

# Add fallback for missing flask.debughelpers
try:
    import flask.debughelpers
except ImportError:
    # Create a mock module to handle the missing module
    import types
    flask_mock = types.ModuleType('flask.debughelpers')
    flask_mock.attach_enctype_error_multidict = lambda x: x
    flask_mock.FormDataRoutingRedirect = Exception
    sys.modules['flask.debughelpers'] = flask_mock
    print("Created mock for flask.debughelpers")

# Use the new virtual environment if it exists
new_venv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'venv_new', 'Lib', 'site-packages'))
if os.path.exists(new_venv_path) and new_venv_path not in sys.path:
    sys.path.insert(0, new_venv_path)
    print(f"Added {new_venv_path} to sys.path")

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 