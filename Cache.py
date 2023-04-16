class Cache:

    def __init__(self):
        self.cache_dict = {}

    def add_in_cache(self,key,value):
        self.cache_dict[key] = value

    def is_present_in_cache(self,key):
        if key in self.cache_dict:
            return True
        else:
            return False

    def retrieve_from_cache(self,key):
        return self.cache_dict[key]
        #return self.cache_dict.items()

