class Cache:

    def __init__(self):
        self.cache_dict = {}
        self.maxlength = 10
        self.ctr = 0

    def add_in_cache(self,key,value):
        full = self.is_full()
        if full == False:
            value.append(self.ctr)
            self.cache_dict[key] = value
            self.ctr = self.ctr+1
        else:
            x = float('inf')
            for key1 in self.cache_dict:
                value_1 = self.cache_dict[key1]
                if value_1[-1] < x:
                    x = value_1[-1]
                    del_key = key1
            del self.cache_dict[del_key]
            value.append(self.ctr)
            self.cache_dict[key] = value
            self.ctr = self.ctr + 1

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
        return self.cache_dict[key]
        #return self.cache_dict.items()

