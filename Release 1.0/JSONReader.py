import json


class JSONReader:

    @classmethod
    def stringFromFile(cls, path):
        with open(path, 'r', encoding="utf-8") as file_String:
            return file_String.read().replace('\n', '\n')

    @classmethod
    def readJSON(cls, string): return json.loads(string)
