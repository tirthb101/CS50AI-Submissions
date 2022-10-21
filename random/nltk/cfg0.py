from lib2to3.pgen2 import grammar
import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP

    NP -> N | D N
    VP -> V | V NP

    D -> "the" | "a"
    N -> "she" | "city" | "car"
    V -> "saw" | "walked"

""")

parser = nltk.ChartParser(grammar)


try:
    data = input("").split(" ")
    for tree in parser.parse(data):
        tree.pretty_print()
        tree.draw()
except:
    pass
