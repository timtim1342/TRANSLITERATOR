from functools import wraps
from gridtext import GridTextTranscribed


def write_html_header(func):
    @wraps(func)
    def wrapper():
        header = """ <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-16">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <!-- Bootstrap CSS -->
        <title>Свалка текстов</title>
        <style type="text/css">
        body {
            padding: 40px;
            line-height: 1.5;
        }
        .example {
            padding: 1px; /* Поля */
            white-space: pre;
            }
         p {
            margin-top: 1em; /* Отступ сверху */
            margin-bottom: 1em; /* Отступ снизу */
        }
        button {
        background: #f2f6f8; /* Цвет фона */
        border: 1px solid #7a7b7e; /* Параметры рамки */
        width: 30px; /* Ширина кнопки */
        height: 30px; /* Высота */
        border-radius: 30px;
        }
        </style>
        </head>
        <body>
        <header>
        </header>
        <br>
        <br>
        """
        with open("text_heap_light.html", 'a', encoding="UTF-16") as html:
            html.write(header)

        func()
        bottom = """
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        </body>
        </html>
        """
        with open("text_heap_light.html", 'a', encoding="UTF-16") as html:
            html.write(bottom)

    return wrapper


def put_text_light(tg):
    with open("text_heap_light.html", 'a', encoding="UTF-16") as html:
        html.write("""<nav class="navbar navbar-expand-lg navbar-light bg-light rounded"><div class="collapse navbar-collapse justify-content-md-center" id="navbarsExample10">
      <ul class="navbar-nav"><li class="nav-item active"><a class="nav-link" href="#"><h2><b>"""
                   + tg.filename)
        html.write("""\n</b></h2><span class="sr-only">(current)</span></a></li></ul></div></nav>""")

        for interval_number in range(len(GridTextTranscribed.get_labels(tg.latin_transcription))):  # change to time
            cyrillic_transcription, latin_transcription = GridTextTranscribed.get_labels(tg.cyrillic_transcription),\
                GridTextTranscribed.get_labels(tg.latin_transcription)

            html.write(f'{interval_number}: {cyrillic_transcription[interval_number]}<br>--- {latin_transcription[interval_number]}')
            html.write('<br>')

        html.write(f"\n\n<i><p>{'<br>'.join(GridTextTranscribed.get_labels(tg.translation))} \'</p></i><hr>\n\n")

def counts(unique_words_dictionary):
    with open("text_heap_light.html", 'a', encoding="UTF-16") as html:
        html.write(f'Non-unique words: {unique_words_dictionary.total()}<br>')
        html.write(f'Unique words (no punctuation): {len(unique_words_dictionary)}<br>')
        html.write(f'<br>Top-100: {unique_words_dictionary.most_common(100)}')

def make_heap(some_tg):
    put_text_light(some_tg)
