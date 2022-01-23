import json
import os
from pathlib import Path


class KeyMatch:
    keys = []
    values = []
    file_name = "Libraries\Files\preferences.json"

    def __init__(self):
        """ This is a parser that works with the internal json file that is preferences.json"""
        file = open(self.file_name).read()
        preferences = json.loads(file)
        for preference in preferences['preferences']:
            for _ in preference['setting']:
                self.keys.extend(preference['setting'])
            for _ in preference['value']:
                self.values.extend(preference['value'])

    def match(self, key):
        if key in self.keys:
            d = self.values[self.keys.index(key)]
            return d

    def load(self, data):
        """this is to save new data into the storage file"""
        self.reload()
        d = json.dumps(data, indent=1)
        with open(self.file_name, 'w') as f:
            f.write(d)

    def load_defaults(self):
        if os.path.exists(str(Path.home()) + "/Download"):
            folder = str(Path.home()) + "/Download"
        else:
            folder = str(Path.home())
        defaults = {'preferences': [
            {'setting': ['internet_validation'],
             'value': [True]},
            {'setting': ['link_validation'],
             'value': [True]},
            {'setting': ['concurrency_limit'],
             'value': [10]},
            {'setting': ['approval'],
             'value': [False]},
            {'setting': ['directory'],
             'value': [folder]},
            {'setting': ['warning'],
             'value': [False]},
            {'setting': ['theme'],
             'value': ["Dark"]},
            {'setting': ['notifications'],
             'value': [True]},
            {'setting': ['warn_settings'],
             'value': [False]},
            {'setting': ['save_down_proc'],
             'value': [True]},
            {'setting': ['beep_finish'],
             'value': [True]},
            {'setting': ['beep_error'],
             'value': [False]}
        ]}
        d = json.dumps(defaults, indent=1)
        with open(self.file_name, 'w') as f:
            f.write(d)

    def reload(self):
        file = open(self.file_name).read()
        preferences = json.loads(file)
        for preference in preferences['preferences']:
            for _ in preference['setting']:
                self.keys.extend(preference['setting'])
            for _ in preference['value']:
                self.values.extend(preference['value'])


class StorageAPI:
    store = None
    holder = None
    file_name = "Libraries\Files\storage.json"
    datum = None
    ids = []
    tags = []
    pids = []

    def __init__(self):
        """This method saves information about all downloads"""
        file = open(self.file_name).read()
        self.datum = json.loads(file)

    def add_data(self, content):
        """Save data into the file"""
        self.datum.append(content)
        d = json.dumps(self.datum, indent=1)
        with open(self.file_name, 'w') as f:
            f.write(d)

    def get_secondary_geography(self, identifier):
        for data in self.datum:
            if data['id'] == identifier:
                geography = data['secondary_location']
                return geography

    def get_timestamp(self, identifier):
        for data in self.datum:
            if data['id'] == identifier:
                stamp = data['timestamp']
                return stamp

    def get_unknown(self, identifier, key):
        for data in self.datum:
            if data['id'] == identifier:
                criteria = data[key]
                return criteria

    def delete_data(self, identifier):
        for data in self.datum:
            if data['id'] == identifier:
                self.datum.pop(self.datum.index(data))
                d = json.dumps(self.datum, indent=1)
                with open(self.file_name, 'w') as f:
                    f.write(d)

    def delete_all_data(self):
        """Delete all the data in the file storage"""
        self.datum.clear()
        d = json.dumps(self.datum, indent=1)
        with open(self.file_name, 'w') as f:
            f.write(d)

    def update_data(self, identifier, tag, pid, url, name, size, media, secondary_location, place, timestamp):
        self.delete_data(identifier)
        new = {'id': identifier,
               'tag': tag,
               'pid': pid,
               'url': url,
               'name': name,
               'size': size,
               'media': media,
               'secondary_location': secondary_location,
               'directory': place,
               'timestamp': timestamp}
        self.add_data(new)

    def update_singular_data(self, identifier, key, value):
        for data in self.datum:
            if data['id'] == identifier:
                data[key] = value
        d = json.dumps(self.datum, indent=1)
        with open(self.file_name, 'w') as f:
            f.write(d)

    def get_all_ids(self):
        for data in self.datum:
            if data['id'] in self.ids:
                pass
            else:
                self.ids.append(data['id'])
        return self.ids

    def get_all_tags(self):
        for data in self.datum:
            if data['tag'] in self.tags:
                pass
            else:
                self.tags.append(data['id'])
        return self.tags

    def get_all_pids(self):
        for data in self.datum:
            if data['pid'] in self.pids:
                pass
            else:
                self.pids.append(data['id'])
        return self.pids
