import re

ETIQUETA = r'(?P<ETIQUETA><(/?[^>]+)>)'
SPACE = r'(?P<SPACE>\s+)'
TEXTO = r'(?P<TEXTO>[\w\-](-|\w|\s)+)'


patterns = [ETIQUETA, TEXTO, SPACE]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        try:
            m = pat.match(text, index)
            if m:
                if m.lastgroup != 'SPACE':
                    yield (m.lastgroup, m.group())
                index = m.end()
            else:
                raise SyntaxError('Bad char %r' % text[index])
        except SyntaxError as e:
            print(f"Bad character '{text[index]}'")
            index += 1  # Move to the next character
 



if __name__ == '__main__':
    f = open("ejemplo.xml", "r")
    xml_data = f.read()
    f.close()
    for tok in tokenize(xml_data):
        print(tok)

