import os
CLASS_NAME = 'X'


string_bank = [
    "wow man whats up",
    "yooooooooooooooooo",
    "hello",
    "hey",
    "hey man",
    "heyy",
    "shut up man",
    "hee",
    "heep",
    "heed"
]


class ParseFortunes:

    def __init__(self, path):
        with open(path) as f:
            text = f.read()

        split = text.split('%')
        self.fortunes = [s.strip() for s in split]


fortune_files = []
fortunes = []
for f in os.listdir("fortune-mod/fortune-mod/datfiles"):
    p = f"fortune-mod/fortune-mod/datfiles/{f}"
    if os.path.isfile(p):
        if '.' in f:
            continue
        fortunes += ParseFortunes(p).fortunes

fortunes = [f for f in fortunes if len(f) < 14]

counter = 0


class Trie:

    def __init__(self, c):
        self.d = {}
        self.w = {}
        self.c = c
        self.sum = 0

    def to_template_thing(self, lines):
        global counter

        subs = [x.to_template_thing(lines) for x in self.d.values()]
        sub_tys = []
        for sub in subs:
            sub_ty = f"_{counter}"
            sub_tys.append(sub_ty)
            lines.append(f"using {sub_ty} = {sub};")
            counter += 1

        subs = ",".join(sub_tys)
        tail = f", {subs}" if subs else ""
        value = self.c | (self.sum << 8)
        return f"X<{value}{tail}>"

    def add(self, s):
        if not s:
            return

        c = ord(s[0])

        if c not in self.d:
            self.d[c] = Trie(c)

        self.d[c].add(s[1:])

    def contains(self, s):
        if not s:
            return True

        c = ord(s[0])
        return c in self.d and self.d[c].contains(s[1:])

    def is_leaf(self) -> bool:
        return len(self.d) == 0

    def populate_counts(self):
        self.sum = int(self.is_leaf())
        for k, v in self.d.items():
            v.populate_counts()
            self.sum += v.sum
            self.w[k] = v.sum

    def go(self, name):
        lines = []
        self.populate_counts()
        a = self.to_template_thing(lines)
        return "\n".join(lines) + f"\nusing {name} = {a};"


template = """
using $$$ = %%%;
"""

greetings = [
    "Hi %s",
    "Hi there %s!",
    "Hey %s!",
    "Hello, %s!",
    "Hey you, %s!",
    "Hello there %s",
    "Heyyyyy %s",
    "Is that you %s?",
    "%s! Hey stranger :)",
    "I hate you, %s.",
    "Howdy %s.",
    "Wagwan %s."
]


with open("greetings.hxx", "w") as greetings_file:
    x = Trie(ord(' '))
    for s in greetings:
        x.add(s)
    greetings_file.write(x.go("greetings"))

with open("fortunes.hxx", "w") as fortunes_file:
    x = Trie(ord(' '))
    for s in fortunes:
        x.add(s)
    x.populate_counts()
    fortunes_file.write(x.go("fortunes"))
