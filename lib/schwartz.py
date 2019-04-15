import spacy
from spacy.lang.en import English

nlp = spacy.blank("en")
tokenizer = English().Defaults.create_tokenizer(nlp)


def is_valid_short_form(string):
    return has_letter(string) and (string[0].isalpha() or string[0].isdigit() or string[0] == '(')


def has_letter(string):
    return any(c.isalpha() for c in string)


def has_capital(string):
    return any(c.isupper() for c in string)


def extract_pairs(sentence):
    acronym = ""
    definition = ""
    pairs = []
    c = -1

    o = sentence.find(" (")  # find open parenthesis

    while True:
        if o > -1:
            o += 1  # skip white space, i.e. " (" -> "("

            c = sentence.find(")", o)  # find closed parenthesis
            if c > -1:
                # find the start of the previous clause based on punctuation
                cutoff = max(sentence.rfind(". ", o), sentence.rfind(", ", o))
                if cutoff == -1:
                    cutoff = -2

                definition = sentence[(cutoff + 2):o]
                acronym = sentence[(o + 1):c]

        if len(acronym) > 0 or len(definition) > 0:
            if len(acronym) > 1 or len(definition) > 1:

                next_c = sentence.find(")", c + 1)
                if acronym.find("(") > -1 and next_c > -1:
                    acronym = sentence[(o + 1):next_c]
                    c = next_c

                # if separator found within parentheses, then trim everything after it
                tmp = acronym.find(", ")
                if tmp > -1:
                    acronym = acronym[0:tmp]

                tmp = acronym.find("; ")
                if tmp > -1:
                    acronym = acronym[0:tmp]

                if len(tokenizer(acronym)) > 2 or len(acronym) > len(definition):
                    # extract the last token before "(" as a candidate for acronym
                    tmp = sentence.rfind(" ", o - 2)
                    str = sentence[(tmp + 1):(o - 1)]

                    # swap acronym & definition
                    definition = acronym
                    acronym = str

                    if not has_capital(acronym):
                        acronym = ""  # delete invalid acronym

                _acronym = acronym.strip()
                _definition = definition.strip()

                if is_valid_short_form(acronym):
                    obj = match_pair(_acronym, _definition)
                    if obj is not None:
                        pairs.append({"acronym": obj["acronym"], "definition": obj["definition"]})

            # prepare to process the rest of the sentence after ")"
            sentence = sentence[(c + 1):]
        elif o > -1:
            sentence = sentence[(o + 1):]

        acronym = ""
        definition = ""

        o = sentence.find(" (")
        if o == -1:
            break

    return pairs


def best_long_form(acronym, definition):
    a = len(acronym) - 1
    d = len(definition) - 1

    for i in range(a, -1, -1):
        c = acronym[i].lower()

        if c.isalpha() or c.isdigit():
            while (d >= 0 and definition[d].lower() != c) or \
                    (i == 0 and d > 0 and (definition[d-1].isalpha() or definition[d-1].isdigit())):
                d -= 1

            if d < 0:
                return None

            d -= 1

    d = definition.find(" ", d) + 1
    return definition[d:]


def match_pair(acronym, definition):
    if len(acronym) < 2:
        return None

    best_long = best_long_form(acronym, definition)
    if best_long is None:
        return None

    tn = tokenizer(best_long)
    t = len(tn)
    c = len(acronym)

    for i in range(c-1, -1, -1):
        char = acronym[i]
        if not (char.isalpha() or char.isdigit()):
            c -= 1

    if (len(best_long) < len(acronym)) or best_long.find(acronym + " ") > -1 or \
            best_long.endswith(acronym) or t > 2*c or t > c+5 or c > 10:
        return None

    return {"acronym": acronym, "definition": best_long}
