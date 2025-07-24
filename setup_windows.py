import PyInstaller.__main__
import sys

PyInstaller.__main__.run([
    'kittys_robot_gui.py',
    '--onefile',
    '--windowed',
    '--name=KittySudoku',
    '--icon=NONE',
    '--add-data=.;.',
    '--hidden-import=reportlab',
    '--hidden-import=reportlab.pdfgen',
    '--hidden-import=reportlab.lib',
    '--hidden-import=reportlab.lib.pagesizes',
    '--distpath=./dist_windows',
    '--workpath=./build_windows',
    '--specpath=.',
    '--noconfirm',
    '--clean'
])