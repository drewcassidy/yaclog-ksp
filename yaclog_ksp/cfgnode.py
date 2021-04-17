#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

#  Original: https://github.com/taniwha/cfgnode

# <pep8 compliant>

from yaclog_ksp.script import Script


class ConfigNodeError(Exception):
    def __init__(self, fname, line, message):
        Exception.__init__(self, "%s:%d: %s" % (fname, line, message))
        self.message = "%s:%d: %s" % (fname, line, message)
        self.line = line


def cfg_error(self, msg):
    raise ConfigNodeError(self.filename, self.line, msg)


class ConfigNode:
    def __init__(self):
        self.values = []
        self.nodes = []

    @classmethod
    def parse_node(cls, node, script, top=False):
        while script.token_available(True):
            token_start = script.pos
            if script.get_token(True) is None:
                break
            if script.token == "\xef\xbb\xbf":
                continue
            if script.token in (top and ['{', '}', '='] or ['{', '=']):
                cfg_error(script, "unexpected " + script.token)
            if script.token == '}':
                return
            key = script.token
            # print(key,script.line)
            while script.token_available(True):
                script.get_token(True)
                token_end = script.pos
                line = script.line
                if script.token == '=':
                    value = ''
                    if script.token_available(False):
                        script.get_line()
                        value = script.token.strip()
                    node.values.append((key, value, line))
                    break
                elif script.token == '{':
                    new_node = ConfigNode()
                    ConfigNode.parse_node(new_node, script, False)
                    node.nodes.append((key, new_node, line))
                    break
                else:
                    # cfg_error(script, "unexpected " + script.token)
                    key = script.text[token_start:token_end]
        if not top:
            cfg_error(script, "unexpected end of file")

    @classmethod
    def load(cls, textv):
        script = Script("", textv, "{}=", False)
        script.error = cfg_error.__get__(script, Script)
        nodes = []
        while script.token_available(True):
            node = ConfigNode()
            ConfigNode.parse_node(node, script, True)
            nodes.append(node)
        if len(nodes) == 1:
            return nodes[0]
        else:
            return nodes

    @classmethod
    def loadfile(cls, path):
        data = open(path, "rb").read()
        try:
            contents = "".join(map(lambda b: chr(b), data))
        except TypeError:
            contents = data
        return cls.load(contents)

    def get_node(self, key):
        for n in self.nodes:
            if n[0] == key:
                return n[1]
        return None

    def get_node_line(self, key):
        for n in self.nodes:
            if n[0] == key:
                return n[2]
        return None

    def get_nodes(self, key):
        nodes = []
        for n in self.nodes:
            if n[0] == key:
                nodes.append(n[1])
        return nodes

    def get_value(self, key):
        for v in self.values:
            if v[0] == key:
                return v[1].strip()
        return None

    def has_node(self, key):
        for n in self.nodes:
            if n[0] == key:
                return True
        return False

    def has_value(self, key):
        for v in self.values:
            if v[0] == key:
                return True
        return False

    def has_value_line(self, key):
        for v in self.values:
            if v[0] == key:
                return v[2]
        return None

    def get_values(self, key):
        values = []
        for v in self.values:
            if v[0] == key:
                values.append(v[1])
        return values

    def add_node(self, key, node):
        self.nodes.append((key, node))
        return node

    def add_new_node(self, key):
        node = ConfigNode()
        self.nodes.append((key, node))
        return node

    def add_value(self, key, value):
        self.values.append((key, value))

    def set_value(self, key, value):
        for i in range(len(self.values)):
            if self.values[i][0] == key:
                self.values[i] = key, value, 0
                return
        self.add_value(key, value)

    def __str__(self, level=0):
        extra = 0
        if level >= 0:
            extra = 2
        segments = [''] * (len(self.values) + len(self.nodes) + extra)
        index = 0
        if level >= 0:
            segments[index] = "{\n"
            index += 1
        for val in self.values:
            segments[index] = "%s%s = %s\n" % ("    " * (level + 1), val[0], val[1])
            index += 1
        for node in self.nodes:
            ntext = node[1].__str__(level + 1)
            segments[index] = "%s%s %s\n" % ("    " * (level + 1), node[0], ntext)
            index += 1
        if level >= 0:
            segments[index] = "%s}\n" % ("    " * level)
            index += 1
        return "".join(segments)


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        text = open(arg, "rt").read()
        try:
            node = ConfigNode.load(text)
        except ConfigNodeError as e:
            print(arg + e.message)
