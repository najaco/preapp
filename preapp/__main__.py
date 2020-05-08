from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from preapp.nodes import RootNode

if __name__ == "__main__":
    RootNode().process()
