from my_latex_cute_lib import main
import subprocess


def convert_tex_to_pdf(table, tex_file):
    main.table_to_latex(table, tex_file)
    main.img_to_latex('malone.png', tex_file)
    subprocess.run(['pdflatex', tex_file])


table_input = input('2D-array: ')
filename_input = input('filename: ')

table = eval(table_input)
convert_tex_to_pdf(table, filename_input)

