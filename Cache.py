import json
import time
class Cache:

    def __init__(self):
        try:
            with open('cache.json','r') as f:
                self.cache_dict = json.load(f)
        except FileNotFoundError:
            self.cache_dict = {}
        self.maxlength = 10


    def add_in_cache(self,key,value):
        full = self.is_full()
        if full == False:
            value.append(time.time())
            self.cache_dict[key] = value
            self.write_to_file(self.cache_dict)
        else:
            x = float('inf')
            for key1 in self.cache_dict:
                value_1 = self.cache_dict[key1]
                if value_1[-1] < x:
                    x = value_1[-1]
                    del_key = key1
            del self.cache_dict[del_key]
            value.append(time.time())
            self.cache_dict[key] = value
            self.write_to_file(self.cache_dict)

    def write_to_file(self,data):
        with open('cache.json','w') as f:
            json.dump(data,f)

    def is_full(self):
        if len(self.cache_dict) == self.maxlength:
            return True
        else:
            return False

    def is_present_in_cache(self,key):
        if key in self.cache_dict:
            return True
        else:
            return False

    def retrieve_from_cache(self,key):
        self.cache_dict[key][-1] = time.time()
        return self.cache_dict[key]
