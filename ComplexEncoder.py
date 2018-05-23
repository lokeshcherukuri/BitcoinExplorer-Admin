import json


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toString'):
            return obj.toString()
        else:
            return json.JSONEncoder.default(self, obj)
