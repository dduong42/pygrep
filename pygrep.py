from contextlib import contextmanager
import ast
import sys


@contextmanager
def parse_source(path):
    with open(path) as f:
        content = f.read()
        yield SourceCode(content)


def bold(s):
    s = '\033[1m' + str(s) + '\033[0m'
    return s


def grepfunc():
    query = sys.argv[1]
    path = sys.argv[2]
    with parse_source(path) as code:
        nodes = code.find_function(query)
        output = []
        for node in nodes:
            output.append('{}:{}'.format(
                bold(node.lineno),
                code.get_line(node.lineno),
            ))
        output = '\n'.join(output)
        if output:
            print(output)


def grepclass():
    query = sys.argv[1]
    path = sys.argv[2]
    with parse_source(path) as code:
        nodes = code.find_class(query)
        output = []
        for node in nodes:
            output.append('{}:{}'.format(
                bold(node.lineno),
                code.get_line(node.lineno),
            ))
        output = '\n'.join(output)
        if output:
            print(output)


class SourceCode(object):
    def __init__(self, content):
        self.node = ast.parse(content)
        self.lines = content.split('\n')

    def find_function(self, name):
        searcher = FunctionSearcher(name)
        searcher.visit(self.node)
        return searcher.matches

    def find_class(self, name):
        searcher = ClassSearcher(name)
        searcher.visit(self.node)
        return searcher.matches

    def get_line(self, lineno):
        return self.lines[lineno - 1]


class Searcher(ast.NodeVisitor):
    def __init__(self, query):
        self.query = query
        self.matches = []
        super(Searcher, self).__init__()


class FunctionSearcher(Searcher):
    def visit_FunctionDef(self, node):
        if node.name == self.query:
            self.matches.append(node)


class ClassSearcher(Searcher):
    def visit_ClassDef(self, node):
        if node.name == self.query:
            self.matches.append(node)
