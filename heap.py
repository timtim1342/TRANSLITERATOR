from praatio import textgrid
from functools import wraps
import os

"""
В поле глосс не должно быть пустых мест.
Границы крайних форм должны совпадать с границами предложений.
"""

LEXEMES = 0


class ParseTextGrid:
    def __init__(self, filename):
        self.filename = filename

    def file_open(self):
        return textgrid.openTextgrid(self.filename, includeEmptyIntervals=True)

    def translation(self):
        tg = self.file_open()
        translation_tier = tg.tierDict["2"]
        translation_list = [list(word) for word in translation_tier.entryList]
        return translation_list

    def Ctranscription(self):
        tg = self.file_open()
        transcription_tier = tg.tierDict["1"]
        transcription_list = [list(word) for word in transcription_tier.entryList]
        return transcription_list

    def transcription(self):
        tg = self.file_open()
        Ctranscription_tier = tg.tierDict["5"]
        Ctranscription_list = [list(word) for word in Ctranscription_tier.entryList]
        return Ctranscription_list

class MakeGlossLine(ParseTextGrid):

    def make_line(self):
        lines = []
        translation = self.translation()
        transcription = self.transcription()
        Ctranscription = self.Ctranscription()
        for i in range(len(transcription)):
            transc_line = transcription[i][2]
            Ctransc_line = Ctranscription[i][2]
            try:
                trans_line = translation[i][2]
            except IndexError:
                trans_line = 'IndexError: Translation and transcription tiers have different length'

            lines.append((transc_line, Ctransc_line, trans_line))

        return lines

"""
Starting html construction
"""


def write_html_header(func):
    @wraps(func)
    def wrapper():
        header = """ <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <!-- Bootstrap CSS -->
        <title>Свалка тукитинских текстов</title>
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
        with open("text_heap.html", 'a', encoding="UTF-8") as html:
            html.write(header)

        html.close()
        func()
        bottom = """
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        </body>
        </html>
        """
        with open("text_heap.html", 'a', encoding="UTF-8") as html:
            html.write(bottom)
        html.close()
    return wrapper


@write_html_header
def put_texts():
    for filename in os.listdir('latin_textgrids'):
        with open("text_heap.html", 'a', encoding="UTF-8") as html:
            html.write("""<nav class="navbar navbar-expand-lg navbar-light bg-light rounded"><div class="collapse navbar-collapse justify-content-md-center" id="navbarsExample10">
      <ul class="navbar-nav"><li class="nav-item active"><a class="nav-link" href="#"><h2><b>"""
                       + filename.split('.')[0])
            html.write("""\n</b></h2><span class="sr-only">(current)</span></a></li></ul></div></nav>""")
            html.close()
        print(filename)
        parser = MakeGlossLine(os.path.join('latin_textgrids', filename))

        for el in parser.make_line():
            with open("text_heap.html", 'a', encoding="UTF-8") as html:
                html.write(el[0] + '\n' + '<br>')
                html.write(el[1] + '\n')
                #html.write("\n\n<i><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\' " + el[0] + " \'</p></i><hr>\n\n")
                #html.write("\n\n<i><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\' " + el[1] + " \'</p></i><hr>\n\n")
                if el[2] is not None:
                    html.write("\n\n<i><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\' " + el[2] + " \'</p></i><hr>\n\n")
            html.close()
        with open("text_heap.html", 'a', encoding="UTF-8") as html:
            html.write("""<br><br><br>""")
            html.close()


def main():
    try:
        os.remove("text_heap.html")
    except Exception:
        pass

    put_texts()
    print("\nКолчество лексем в копрусе: " + str(LEXEMES))


if __name__ == "__main__":
    main()