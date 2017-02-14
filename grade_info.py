import json


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def load_json(filename):
    info = {}
    try:
        json_file = open(filename, 'r')
        info = byteify(json.load(json_file))
    except IOError:
        pass

    return info

def save_json(filename, info):
    with open(filename, 'w+') as outfile:
        json.dump(info, outfile, indent=4, sort_keys=True)


class GradeInfo:
    def __init__(self, filename='grade.json'):
        self.gi = load_json(filename)
        self.filename = filename

    def get_last_version_num(self, nid):
        if nid in self.gi:
            return self.gi[nid]['version']
        return -1
    
    def update(self, nid, version, grade):
        if nid not in self.gi:
            self.gi[nid] = {}

        self.gi[nid]['grade'] = grade
        self.gi[nid]['version'] = max(version, 0)

    def dump(self, filename=''):
        if not filename:
            save_json(self.filename, self.gi)
        else:
            save_json(filename, self.gi)

if __name__=='__main__':
    gi = GradeInfo()
    gi.dump()
    print gi.gi
