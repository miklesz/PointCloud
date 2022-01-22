from setuptools import setup

#'console_apps': {
#'gui_apps': {

setup(
    name="demo",
    options = {
        'build_apps': {
            'include_patterns': [
                'models/*',
                'music/*',
            ],
            'gui_apps': {
                'demo': 'main.py',
            },
            "icons": {
                # The key needs to match the key used in gui_apps/console_apps.
                # Alternatively, use "*" to set the icon for all apps.
                "demo": ["icon-256.png"],
            },
            'log_filename': 'output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
                'p3assimp',
            ],
        }
    }
)
