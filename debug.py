
"""A proxy class to debug object usage.

This shouldn't really live in toolbox, can't think of a better place though.
"""

class Debug(object):
    """Wrap a class or instance in this for which you want to trace.
    
    Add class names to ignore if you don't want trace those ones.
    """

    def __init__(self, obj, ignore=[]):
        self.__obj = obj
        self.__ignore = list(ignore)

    def __call__(self, *a, **kw):
        v = self.__obj(*a, **kw)
        if self.__can_proxy(v):
            return Debug(v)
        else:
            return v

    def __can_proxy(self, v):
        return not isinstance(v, (int, long, dict, list, str, unicode))

    def __getattr__(self, name):
        return self.__get(name)

    def __get(self, name):
        cls = self.__obj.__class__.__name__
        if cls not in self.__ignore:
            print "******* %s.%s()" % (cls, name)
        v = getattr(self.__obj, name)
        if self.__can_proxy(v):
            return Debug(v)
        else:
            return v

    def __slice__(self, *a, **kw):
        return self.__get('__slice__')(*a, **kw)

    def __getitem__(self, *a, **kw):
        print (a, kw)
        return self.__get('__getitem__')(*a, **kw)

    def __str__(self, *a, **kw):
        return self.__get('__str__')(*a, **kw)

    def __repr__(self, *a, **kw):
        return self.__get('__repr__')(*a, **kw)

    def __unicode__(self, *a, **kw):
        return self.__get('__unicode__')(*a, **kw)
