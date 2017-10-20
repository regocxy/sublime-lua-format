import sublime
import sublime_plugin

class Node:
    (
        TYPE_NONE,
        TYPE_OPER,
        TYPE_ENTER,
        TYPE_STR,
        TYPE_WORD,
        TYPE_KEY,
        TYPE_SEP,
        TYPE_NEWLINE,
        TYPE_INDENT,
        TYPE_UNINDENT,
        TYPE_UNINDENT2,
        TYPE_COMMIT,
        TYPE_COND,
        TYPE_OTHER
    ) = range(0, 14)

    def __init__(self, name='', type=TYPE_NONE):
        self.name = name
        self.type = type
        self.parent = None
        self.child = None

    def behind(self, node):
        if self.child:
            self.child.parent = node
        node.child = self.child
        node.parent = self
        self.child = node

    def front(self, node):
        if self.parent:
            self.parent.child = node
        node.parent = self.parent
        node.child = self
        self.parent = node


class Link:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, node):
        if not self.tail:
            self.head = self.tail = node
        else:
            self.tail.behind(node)
            self.tail = node
        self.size += 1

    def remove(self, node):
        pass


class Formater(object):

    CHAR_ENTER = '\n'

    Seps = ['~', '>', '<', '=', '+', '-', '*', '/', '%', ':', ',', ' ', '\t', CHAR_ENTER, '\'', '"', '{', '}', '(', ')', '[', ']']
    Conds = ['~', '>', '<', '=']
    Ops = ['+', '-', '*', '/', '%']
    Indents = ['if', 'for', 'repeat', 'while', 'function', '{']
    Unindents = ['end', 'until', '}']
    Unindents2 = ['else', 'elseif']
    Others = ['print', 'in', 'pairs', 'ipairs', 'then', 'do', 'require', 'local', 'return', 'and', 'or', 'not']

    def __init__(self):
        self.link = Link()
        self.link2 = Link()
        setting = sublime.load_settings('LFormat.sublime-settings')
        self.tab_size = setting.get('tab_size', 4)

    def do_link(self, ctx):
        cache = ''
        for c in ctx:
            if c in Formater.Seps:
                if cache:
                    self.link.append(Node(cache, Node.TYPE_WORD))
                    cache = ''
                self.link.append(Node(c, Node.TYPE_SEP))
            else:
                cache += c
        if cache:
            self.link.append(Node(cache, Node.TYPE_WORD))
        node = self.link.head
        while node:
            if node.name == '[' and node.child and node.child.name == '[':
                cache = '[['
                node = node.child.child
                if node:
                    while node and not (node.name == ']' and node.child.name == ']'):
                        cache += node.name
                        node = node.child
                    cache += ']]'
                    node = node.child
                self.link2.append(Node(cache, Node.TYPE_STR))
            # elif node.name == '[' and node.child.name == '=':
            #     n = 1
            #     while node and node.name == '=':
            #         n += 1
            #         node = node.child
            #     if node.name == '[':
            #         while node and not (node.name == ']' and node.child.name == '='):
            #             cache += node.name
            #             node = node.child
            elif node.name == '\'':
                cache = '\''
                node = node.child
                if node:
                    while node and node.name != '\'':
                        cache += node.name
                        node = node.child
                    cache += '\''
                self.link2.append(Node(cache, Node.TYPE_STR))
            elif node.name == '"':
                cache = '"'
                node = node.child
                if node:
                    while node and node.name != '"':
                        cache += node.name
                        node = node.child
                    cache += '"'
                self.link2.append(Node(cache, Node.TYPE_STR))
            elif node.name == '-' and node.child and node.child.name == '-':
                cache = '--'
                node = node.child.child
                if node:
                    if node.name == '[' and node.child and node.child.name == '[':
                        cache += '[['
                        node = node.child.child
                        if node:
                            while node and not (node.name == ']' and node.child.name == ']'):
                                cache += node.name
                                node = node.child
                            cache += ']]'
                            node = node.child
                        self.link2.append(Node(cache, Node.TYPE_COMMIT))
                    else:
                        while node and node.name != Formater.CHAR_ENTER:
                            cache += node.name
                            node = node.child
                        self.link2.append(Node(cache, Node.TYPE_COMMIT))
                        self.link2.append(Node(Formater.CHAR_ENTER, Node.TYPE_WORD))
            else:
                if node.name != ' ' and node.name != '\t':
                    if node.name in Formater.Indents:
                        self.link2.append(Node(node.name, Node.TYPE_INDENT))
                    elif node.name in Formater.Unindents:
                        self.link2.append(Node(node.name, Node.TYPE_UNINDENT))
                    elif node.name in Formater.Unindents2:
                        self.link2.append(Node(node.name, Node.TYPE_UNINDENT2))
                    elif node.name in Formater.Conds:
                        self.link2.append(Node(node.name, Node.TYPE_COND))
                    elif node.name in Formater.Ops:
                        self.link2.append(Node(node.name, Node.TYPE_OPER))
                    elif node.name in Formater.Others:
                        self.link2.append(Node(node.name, Node.TYPE_OTHER))
                    else:
                        self.link2.append(Node(node.name, Node.TYPE_WORD))
            if node:
                node = node.child

    def do_format(self, ctx):
        self.do_link(ctx)
        indent = 0
        node = self.link2.head
        while node:
            if node.type == Node.TYPE_UNINDENT:
                if indent >= self.tab_size:
                    indent -= self.tab_size
                tbl = [' ', ' '*indent, Formater.CHAR_ENTER, '{']
                if node.parent and node.parent.name not in tbl:
                    node.front(Node(' ', Node.TYPE_WORD))
                tbl = [',', ')', Formater.CHAR_ENTER]
                if node.child and node.child.name not in tbl:
                    node.behind(Node(' ', Node.TYPE_WORD))

            if not node.parent or node.parent.name == Formater.CHAR_ENTER:
                if indent:
                    if node.type == Node.TYPE_UNINDENT2:
                        if indent >= self.tab_size:
                            node.front(Node(' '*(indent - self.tab_size), Node.TYPE_WORD))
                        if node.child and node.child.name != ' ':
                            node.behind(Node(' ', Node.TYPE_WORD))
                    else:
                        node.front(Node(' '*indent, Node.TYPE_WORD))
            if node.type == Node.TYPE_INDENT or \
                (node.name == 'do' and (node.parent and node.parent.name == Formater.CHAR_ENTER or node.parent.name == ' '*indent)):
                indent += self.tab_size
                if node.child and node.child.name != Formater.CHAR_ENTER and node.child.name != ' ':
                    if not ((node.name == 'function' and node.child.name == '(') or node.child.name == '}'):
                        node.behind(Node(' ', Node.TYPE_WORD))
            elif node.name == ',':
                tbl = [' ', Formater.CHAR_ENTER]
                if node.child and node.child.name not in tbl :
                    node.behind(Node(' ', Node.TYPE_WORD))
            elif node.name == ':':
                tbl = [' '*indent, Formater.CHAR_ENTER]
                if node.parent and node.parent.name in tbl:
                    node.front(Node(' '*self.tab_size, Node.TYPE_WORD))
            elif node.type == Node.TYPE_COND:
                if node.parent and node.parent.type != Node.TYPE_COND and node.parent.name != ' ':
                    node.front(Node(' ', Node.TYPE_WORD))
                if node.child and node.child.type != Node.TYPE_COND and node.child.name != ' ':
                    node.behind(Node(' ', Node.TYPE_WORD))
            elif node.type == Node.TYPE_OPER:
                if node.parent and node.parent.name != ' ':
                    node.front(Node(' ', Node.TYPE_WORD))
                if node.child and node.child.name != ' ':
                    if not (node.name == '-' and node.child.name.isdigit()):
                        node.behind(Node(' ', Node.TYPE_WORD))
            elif node.type == Node.TYPE_COMMIT:
                tbl = [Formater.CHAR_ENTER, ' ', ' '*indent]
                if node.parent and node.parent.name not in tbl:
                    node.front(Node(' ', Node.TYPE_WORD))
            elif node.type == Node.TYPE_OTHER:
                tbl = [Formater.CHAR_ENTER, ' ', ' '*indent]
                if node.parent and node.parent.name not in tbl:
                    node.front(Node(' ', Node.TYPE_WORD))
                if node.child and node.child.name not in tbl:
                    tbl = ['print', 'require', 'pairs', 'ipairs']
                    if not (node.name in tbl and node.child.name == '('):
                        node.behind(Node(' ', Node.TYPE_WORD))

            node = node.child
        out = ''
        node = self.link2.head
        while node:
            out += node.name
            node = node.child
        return out

class LFormatCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        formater = Formater()
        self.view.replace(edit, region, formater.do_format(content))

    def is_visible(self):
        f = self.view.file_name()
        if f and (f.endswith('.lua') or f.endswith('.elua')):
            return True
        return False
