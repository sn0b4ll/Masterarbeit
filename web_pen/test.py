import os
import subprocess

tex_path = os.path.join(os.getcwd(), 'tex')
pdf_file = os.path.join(tex_path, 'Fragen.pdf')
os.chdir(tex_path)
try:
    out = subprocess.check_output(['/usr/local/texlive/2016/bin/x86_64-darwin/pdflatex',  '-synctex=1', '-interaction=nonstopmode', 'Fragen12.tex'], cwd=tex_path)
except subprocess.CalledProcessError as error:
    print(error)
