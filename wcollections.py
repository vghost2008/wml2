import numpy as np
import random

class ExperienceBuffer():
    def __init__(self, buffer_size = 100000):
        self.buffer = []
        self.buffer_size = buffer_size

    def add(self, experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.buffer[0: (len(experience) + len(self.buffer)) - self.buffer_size] = []
        self.buffer.extend(experience)

    def sample(self, size):
        if not isinstance(self.buffer[0],np.ndarray):
            data = random.sample(self.buffer,size)
            data = list(zip(*data))
            return [np.array(list(x)) for x in data]
        else:
            return np.reshape(np.array(random.sample(self.buffer, size)), [size]+list(self.buffer[0].shape))


class CycleBuffer:
    def __init__(self,cap=5):
        self.cap = cap
        self.buffer = []
    def append(self,v):
        self.buffer.append(v)
        l = len(self.buffer)
        if l>self.cap:
            self.buffer = self.buffer[l-self.cap:]

    def __getitem__(self, slice):
        return self.buffer[slice]

    def __len__(self):
        return len(self.buffer)

class AlwaysNullObj(object):
    def __init__(self,*args,**kwargs):
        print(f"Construct a always null object")
        pass

    def __getattr__(self, item):
        return self

    def __setattr__(self, key, value):
        pass

    def __delattr__(self, item):
        pass

    def __call__(self, *args, **kwargs):
        return self

class MDict(dict):
    def __init__(self, *args, **kwargs):
        '''

        Args:
            *args:
            **kwargs:
            example:
            x = MDict(dtype=list)
            x[1].append('a')
            x[2].append('b')
            x[1].append('c')
            print(x)
            output:
            {1: ['a', 'c'], 2: ['b']}
        '''
        self.default_type = None
        self.default_value = None
        if "dtype" in kwargs:
            self.default_type = kwargs.pop("dtype")
        elif "dvalue" in kwargs:
            self.default_value = kwargs.pop("dvalue")
        super().__init__(*args,**kwargs)

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return self.__getitem__(key)

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        if key in self:
            return super().__getitem__(key)
        elif self.default_type is not None:
            super().__setitem__(key,self.default_type())
            return super().__getitem__(key)
        elif self.default_value is not None:
            super().__setitem__(key,self.default_value)
        return super().__getitem__(key)

    def __delattr__(self, key):
        del self[key]
