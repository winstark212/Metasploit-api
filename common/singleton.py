__author__ = "toantv"

def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance
