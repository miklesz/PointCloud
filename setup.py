from setuptools import setup

#'console_apps': {
#'gui_apps': {

# Set up output logging, important for GUI apps!
# 'log_filename': '$USER_APPDATA/Asteroids/output.log',
# 'log_append': False,

# 'log_filename': 'output.log',
# 'log_append': False,

setup(
    name="Kramsta",
    options = {
        'build_apps': {
            'include_patterns': [
                'models/**',
                'music/*',
                'icons/*',
                # 'particles/*'
            ],
            # 'console_apps': {
            #     'Kramsta': 'main.py',
            'gui_apps': {
                'Kramsta': 'main.py',
            },
            "icons": {
                # The key needs to match the key used in gui_apps/console_apps.
                # Alternatively, use "*" to set the icon for all apps.
                "Kramsta": ["icons/icon-256.png", "icons/icon-32.png", "icons/icon-16.png", "icons/icon-8.png"],
            },

            # Set up output logging, important for GUI apps!
            # 'log_filename': 'output.log',
            'log_filename': 'kramsta.txt',
            'log_append': False,

            'plugins': [
                'pandagl',
                'p3openal_audio',
                'p3assimp',
            ],
            'platforms': ['manylinux2010_x86_64', 'macosx_10_9_x86_64', 'win_amd64'],
            # 'platforms': ['macosx_10_9_x86_64', 'win_amd64'],
            # 'platforms': ['macosx_10_9_x86_64'],
        }
    }
)
