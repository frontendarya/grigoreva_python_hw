import sys, click

@click.command(help="nl")
@click.option("-b", "--input", "file", type=click.File('r'), default=sys.stdin, help="Input file name")

def nl(file):
    try:
        for i, line in enumerate(file, start=1):
            sys.stdout.write(f"{i}\t{line}")
    except FileNotFoundError:
        sys.stderr.write(f"No such file {file} or directory\n")
        sys.exit(1)

if __name__ == '__main__':
    nl()