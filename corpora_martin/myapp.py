# импортируем все необходимое
from flask import Flask
from flask import render_template, redirect, url_for, request


app = Flask(__name__)

@app.route('/')
def question_page():
    return render_template('my_opros.html')

@app.route('/my_statistika.html')
def stats():
    return render_template('my_statistika.html')

@app.route('/my_opros.html')
def form():
    return redirect(url_for('question_page'))

@app.route("/sorokin_bio.html")
def sorokin_bio():
    return render_template("sorokin_bio.html")

@app.route("/instr.html")
def instr():
    return render_template("instr.html")


@app.route('/search', methods=['POST'])
def my_form_post():
    import json
    from nltk import word_tokenize
    from string import punctuation

    with open("../processed_data.json", encoding="utf-8") as f:
        text_data = json.loads(f.read())

    # токенизирует а-ля Mystem
    def tokenize(text: str):
        result = []
        tokens = word_tokenize(text)
        for i, token in enumerate(tokens):
            if i == len(tokens) - 1:
                result.append(token)
            elif token in punctuation:
                result.append(token + " ")
            elif tokens[i + 1] in punctuation:
                result.append(token)
            else:
                result.append(token)
                result.append(" ")
        return result

    # выдает промежуток вокруг слова, если задать индекс
    def text_with_window(text: tuple, i: int, j: int, window=10):
        if window <= len(text[j + 1:]):
            end = j + 1 + window
        else:
            end = len(text)
        if i >= window:
            beg = i - window
        else:
            beg = 0
        first = ""
        for token in text[beg:i]:
            first += token[0]
        centre = ""
        for token in text[i:j + 1]:
            centre += token[0]
        last = ""
        for token in text[j + 1:end]:
            last += token[0]
        return (first, centre, last)

    # поиск фразы
    def search(text: str):
        cmpnts = tokenize(text)
        result = []
        for text in text_data:
            for i, token in enumerate(text[1]):
                catch = False
                cmpnt_attr = cmpnts[0].split("+")
                if len(cmpnt_attr) == 2:
                    if cmpnt_attr[0] in token and cmpnt_attr[1] in token:
                        catch = True
                elif cmpnts[0] in token:
                    catch = True

                if catch:
                    if len(cmpnts) == 1:
                        example = (text[0], text_with_window(text[1], i, i))
                        result.append(example)
                    else:
                        text_cmpnts = enumerate(zip(text[1][i + 1:], cmpnts[1:]))
                        for j, (token, cmpnt) in text_cmpnts:
                            found = False
                            cmpnt_attr = cmpnt.split("+")
                            if len(cmpnt_attr) == 2:
                                if cmpnt_attr[0] in token and cmpnt_attr[1] in token:
                                    found = True
                                    example_is = True
                            elif cmpnt in token:
                                found = True
                                example_is = True
                            if not found:
                                example_is = False
                                break
                        if example_is:
                            example = (text[0], text_with_window(text[1], i, i + j + 1))
                            result.append(example)
        return result

    text = request.form['query']
    result = search(text)

    return render_template("/search.html", result=result)



if __name__ == '__main__':
    app.run(debug=True)
