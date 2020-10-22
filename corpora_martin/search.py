import json
from nltk import word_tokenize
from string import punctuation

# токенизирует а-ля Mystem
def tokenize(text: str):
    result = []
    tokens = word_tokenize(text)
    for i, token in enumerate(tokens):
        if i == len(tokens)-1:
            result.append(token)
        elif token in punctuation:
            result.append(token+" ")
        elif tokens[i+1] in punctuation:
            result.append(token)
        else:
            result.append(token)
            result.append(" ")
    return result

# выдает промежуток вокруг слова, если задать индекс
def text_with_window(text: tuple, i: int, j: int, window=10):
    result = ""
    if window <= len(text[j+1:]):
        end = j+1+window
        result_end = "..."
    else:
        end = len(text)
        result_end = ""
    if i >= window:
        result+="..."
        beg = i-window
    else:
        beg = 0
    for token in text[beg:i]:
        result+=token[0]
    result+="<b>"
    for token in text[i:j+1]:
        result+=token[0]
    result+="</b>"
    for token in text[j+1:end]:
        result+=token[0]
    result+=result_end
    return result.replace("\n", " ")


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
                    example = (text[0], text_with_window_set(text[1], i, i))
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
                        example = (text[0], text_with_window_set(text[1], i, i + j + 1))
                        result.append(example)
    return result

# записывает результат поиска
def write_search_file(search):
    with open("search_results.json", "w") as f:
        f.write(json.dumps(search, ensure_ascii=False))