from setuptools import setup, find_packages

APP = ['src/main.py']

OPTIONS = {
    'iconfile': 'assets/icon.png',
    'plist': {
        'CFBundleName': 'PomodoroTimer',
        'CFBundleIdentifier': 'com.lrzo01.PomodoroTimer',
        'LSUIElement': True,
    },
    'packages': find_packages(where='src'),  
    'resources': ['assets'], 
    'codesign': False
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
