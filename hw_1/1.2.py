import sys, click

@click.command(help="tail")
@click.argument('files', type=click.File('r'), nargs=-1)

def tail(files):
    if not files:
        lines = sys.stdin.readlines()[-17:]
        click.echo(''.join(lines))

    else:
        for file in files:
            if len(files) > 1:
                sys.stdout.write(f"\n==={file.name}===\n")
            lines = file.readlines()[-10:]
            sys.stdout.write(''.join(lines))

if __name__ == '__main__':
    tail()