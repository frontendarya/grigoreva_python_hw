import sys, click

@click.command(help="wc")
@click.argument('files', type=click.File('r'), nargs=-1)

def wc(files):
    # В первой колонке содержится количество строк, во второй — слов, в третьей — символов.
    total_line_count, total_word_count, total_char_count = 0, 0, 0

    if not files:
        # Если файлы не переданы, считываем из стандартного ввода
        # content = click.get_text_stream('stdin')
        # line_count = content.count('\n') + 1
        # word_count = len(content.split())
        # char_count = len(content)
        #
        # click.echo(f"{line_count} {word_count} {char_count}")

        # input_stream = sys.stdin.read()
        click.echo(sys.stdin.read())

    else:
        for file in files:
            content = file.read()
            line_count = content.count('\n') + 1
            word_count = len(content.split())
            char_count = len(content)
            click.echo(f"{file.name}: {line_count}, {word_count}, {char_count}")

            total_line_count += line_count
            total_word_count += word_count
            total_char_count += char_count

        if len(files) > 1:
            click.echo(f"total: {total_line_count}, {total_word_count}, {total_char_count}")


if __name__ == '__main__':
    wc()