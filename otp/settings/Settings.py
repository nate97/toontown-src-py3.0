import collections
import json
import os


class Settings(collections.MutableMapping):
    def __init__(self, filename):
        self.filename = filename

        self.store = {}
        self.read()

    def read(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.store = json.load(f)
        else:
            self.write()

    def write(self):
        with open(self.filename, 'w') as f:
            json.dump(self.store, f)

    def __setitem__(self, key, value):
        self.store[key] = value
        self.write()

    def __delitem__(self, key):
        del self.store[key]
        self.write()

    def __getitem__(self, key):
        return self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
