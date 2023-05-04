# Code done by Rushabh

import json
import time
class Cache:

    """This function initializes the cache .
    If file exists, the dictionary is initialized from the file itself or else
    the dictionary is initialized as an empty dictionary
    The maximum length of the dictionary is set to 10."""
    def __init__(self):
        try:
            with open('cache.json','r') as f:
                self.cache_dict = json.load(f)
        except FileNotFoundError:
            self.cache_dict = {}
        self.maxlength = 10


    """This function is used to add the data in the cache.
    If the cache is not full it directly adds the key (The text in search box) and the value(results obtained after 
    search) in the dictionary or else
    it finds the least recently added key value pair and removes it and adds the new key value pair to the dictionary.
    We also write the dictionary to a file on every add for checkpointing purposes.
    """
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

    #This function is used to write the dictionary to the file
    def write_to_file(self,data):
        with open('cache.json','w') as f:
            json.dump(data,f)

    # This function checks weather the dictionary is full or not
    def is_full(self):
        if len(self.cache_dict) == self.maxlength:
            return True
        else:
            return False

    # This function checks if a particular key is present in dictionary or not
    def is_present_in_cache(self,key):
        if key in self.cache_dict:
            return True
        else:
            return False

    # This function returns the value of the searched key.
    def retrieve_from_cache(self,key):
        self.cache_dict[key][-1] = time.time()
        return self.cache_dict[key]
