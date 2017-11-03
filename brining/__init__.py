""" brining

    Provides inplace augmentation of python classes with automated
    Python to Json, and Json to Python object mapping via
    either class decorator or inherited mixin class. This also supports
    nested augmented or 'brined' objects

    Optional hinting is also provided via a Python class name hint stored as an
    @class key  in the JSON serialization. This is compatible with
    the style used by the LD-JSON specification.

    Utility function debrine(s) can regenerate new objects from
    a hinted serialization.

    Allows round tripping Python declassifiction/ JSON serialization,
    JSON deserialization / Python classifiction.

    Major limitation vis a vis pickle is that the hint does not guarantee that
    the same class is used for both serialization and deserialization other than
    in name only.

    Example Usage:
    from libs.brining import brined, Brine, debrines

    Decorator:

    @brined()
    class B(object):
        def __init__(self):
            self.x =  1
            self.y =  2
            self.z =  3

    Mixin:

    class B(Brine):
        def __init__(self):
            self.x =  1
            self.y =  2
            self.z =  3

    Wrapper Function:

    brinify(B)


    Examples:

    b=B()
    s = b._dumps()
    print s
    {
      "x": 1,
      "y": 2,
      "z": 3,
      "@class": "B"
    }

    r = '{\n  "x": 4,\n  "y": 5,\n  "z": 6,\n  "@class": "B"\n}'
    b._loads(r)

    b.x
    4
    b.y
    5
    b.z
    6


    Utility Function:

    a = debrines(r,[B])
    a.x
    4

    B._Keys = ['z', 'x']
    print b._dumps()
    {
      "z": 6,
      "x": 4,
      "@class": "B"
    }


    brinify(B,hinted=False)
    print b._dumps()
    print b._dumps()
    {
      "x": 1,
      "y": 2,
      "z": 3
    }

    r = '{\n  "x": 4,\n  "y": 5,\n  "z": 6 }'

    b._loads(r)
    b.x
    4

    getattr(b, '@class')

    AttributeError: 'B' object has no attribute '@class'

    To dump a list or other sequence of brined objects
    brinees = [Brine(),Brine(),Brine()]
    json.dumps(brinees, default=brining.default, indent=2)

    See LICENSE.txt for Licensing details
    Copyright (c) <2013> <Samuel M. Smith>

"""
import sys
import os
import errno
import inspect

#from collections import OrderedDict as odict
from ioflo.aid import odict

import simplejson as json


def brined(keys=None, propertied=False, safed=False, hinted=True, extendable=False):
    """ Explicit decorator to explicitly augment cls with brining
        (JSON serializationdeserialization)

        A brined python object is serialized with json but with annotations that allow
        the object to be deserialized to the same class name. This is called automatic
        declassification/serialization and automatic deserialization/classification.
        This is similar to pickle with the notable exception that there is no way to
        guarantee the class definition is the same.
        So there must be coordination when serializing/declassifying and
        deserializing/classifying to ensure roundtrip preservation of information.
        This is still better than using python dicts with
        manual deserialization/classification
        and manual declassification/serialization.

        Brining a class adds class attributes and methods that  use leading
        underscore to avoid namespace collisions. The class attribute _Brined
        is added to mark the class as brined.

        A brined object will serialize all attributes (not methods)
        not starting with underscore from self.__dict__

        To control the serialization set the decorator parameters:
            keys, properly, safely, hintedly

             keys list, If _Keys is not None then _Keys is a list in order of the
                attributes to serialize.

            propertied, If True then include data descriptor properties

            safed, If True Then test if serialization would raise TypeError and exclude.

            hinted, If True require hint in serialization. THe hint is a key
                "@class" with value .__class__.__name__ in the serialization

            extendable, If True allow unique keys in deserialization to create
                new attributes in object.

        These will set the associated class attributes:
            _Keys, _Propertied, _Safed, _Hinted, _Extendable


    """

    def briner(cls):
        """ Implicit decorator
        """
        if not hasattr(cls, "_Brined"):
            cls._Brined = True
            cls._Keys = keys # custom inclusion and ordering, when None do not use
            cls._Propertied = propertied # When True include data descriptor properties
            cls._Safed = safed # When True test for and exclude non-serializible attributes
            cls._Hinted = hinted
            cls._Extendable = extendable

            cls._dumpable = dumpable
            cls._default = staticmethod(default)
            cls._dumps = dumps
            cls._update = update
            cls._loads = loads
            cls._ocfn = staticmethod(ocfn)
            cls._dump = dump
            cls._load = load
        return cls

    return briner

def brinify(cls, keys=None, propertied=False, safed=False, hinted=True, extendable=False):
    """ Class wrapper to explicitly augment cls with brining (JSON serialization
        deserialization)
    """
    if not hasattr(cls, "_Brined"):
        cls._Brined = True
        cls._Keys = keys # custom inclusion and ordering, when None do not use
        cls._Propertied = propertied # When True include data descriptor properties
        cls._Safed = safed # When True test for and exclude non-serializible attributes
        cls._Hinted = hinted # When True require hinting
        cls._Extendable = extendable # When True allow new attributes from deserialization

        cls._dumpable = dumpable
        cls._default = staticmethod(default)
        cls._dumps = dumps
        cls._update = update
        cls._loads = loads
        cls._ocfn = staticmethod(ocfn)
        cls._dump = dump
        cls._load = load
    return cls


def dumpable(self, deep=False):
    """
        Return nested ordered dict of dumpable attributes including
        brined objects

        if deep is True then recursively operate ._dumpable on Briner instances
            This is useful if want to convert to dumpable full nested Briners
            when using as standalone function not part of dump or dumps
    """
    if self._Keys is None:
        keys = list(self.__dict__.keys()) #include instance attribute keys
        if self._Propertied: # include data descripter propertiesf from class
            props = [key for key in dir(self) if hasattr(self.__class__, key) and
                     inspect.isdatadescriptor(getattr(self.__class__, key))]
            keys.extend(props)
        keys.sort()

    else:
        keys = self._Keys

    dumpable = odict() #use odict so serialization is ordered

    for name in keys:  #build nested OrderedDict of serializible attributes
        if name.startswith('_'): continue #skip private

        try: #get the attr associate with name
            attr = getattr(self, name)
        except AttributeError as ex: #skip if fails getattr
            continue

        if inspect.isroutine(attr): continue  #skip methods

        if deep and hasattr(attr, '_Brined'): # descend into Brined objects
            dumpable[name] = attr._dumpable() #recusively operate on Briner instances
            continue

        if not hasattr(attr, '_Brined') and self._Safed:
            try: #last resort, skip attributes that are not json serializible
                temp = json.dumps(attr)
            except TypeError as ex:
                continue

        dumpable[name] = attr #valid attribute

    if self._Hinted:
        dumpable["@class"] = self.__class__.__name__

    return dumpable

def default(obj):
    """ Method for simplejson default"""
    if not hasattr(obj, '_Brined'):
        raise TypeError("%s is not JSON serializable" % type(obj))

    return obj._dumpable()


def dumps(self, indent=2, **kwa):
    """ Return json serialization as string"""
    if 'default' in kwa: #allow override of default function
        default = kwa['default']
        del kwa['default']
    else:
        default = self._default

    return json.dumps(self._dumpable(),
                      default=default,
                      indent=indent,
                      **kwa)


def update(self, dct):
    """ Update attributes from items in dict dct. If an attribute of self does
        not have matching item in dct then do not change that attribute.
        Returns self

        Update behavior is conditonied by class attributes
        _Keys, _Propertied, _Safed, _Hinted

        If _Keys is None (default None) then include all serializible
            attributes from it, Otherwise only update attributes of self
            with names from _Keys.
        if _Safed (default False) then test existing attributes of self
            for serializiblilty before updating them from it. This is slower.
        If _Propertied (default False) then update attributes of self that
          are data descripter properties.
        If _Hinted (default True) then include class hint on dump and require on load
        If _Extendable (default False) then allow new attributes on update

        Private attributes and functions are always excluded from the update.

    """
    if self._Hinted:
        if dct.get("@class") != self.__class__.__name__:
            raise TypeError("Class hint '%s' does not match class name '%s'."
                            % (dct.get("@class"), self.__class__.__name__))

    if self._Keys == None:
        keys = list(self.__dict__.keys())
    else: #filter on both self._Keys and self.__dict__
        keys = [key for key in self._Keys if key in self.__dict__]
    if self._Propertied:
        props = [key for key in dir(self) if hasattr(self.__class__, key) and
                 inspect.isdatadescriptor(getattr(self.__class__, key)) ]
        if props:
            if self._Keys is None:
                keys.extend(props)
            else:
                keys.extend([key for key in props if key in self._Keys])

    if self._Extendable:
        extends = [key for key in dct if not hasattr(self, key) and key != '@class']
        if extends:
            if self._Keys is None:
                keys.extend(extends)
            else:
                keys.extend([key for key in extends if key in self._Keys])

    for key, value in dct.items():
        if key not in keys:
            continue #skip not preexisting instance attribute
        if key.startswith('_'):
            continue #skip private attribute if not privily

        try:
            attr = getattr(self, key)
        except AttributeError as ex:
            if self._Extendable:
                setattr(self, key, value)  #update attribute
            continue #otherwise skip

        if inspect.isroutine(attr): #skip methods
            continue

        if hasattr(attr, '_Brined'): #recursively load
            attr._update(value)
            continue

        if not hasattr(attr, '_Brined') and self._Safed:
            try: #last resort, skip attributes that are not json serializible
                temp = json.dumps(attr)
            except TypeError as ex:
                continue

        setattr(self, key, value)  #update attribute
    return self


def loads(self, s):
    """ Deserialize s into dict  and update attributes of self with
        items from this dict
        Returns self
    """
    dct = json.loads(s, object_pairs_hook=odict)
    return self._update(dct)

def ocfn(filename, openMode = 'r+'):
    """ Atomically open or create file from filename.

        If file already exists, Then open file using openMode
        Else create file using write update mode
        Returns file object
    """
    try:
        newfd = os.open(filename, os.O_EXCL | os.O_CREAT | os.O_RDWR, 436) # 436 == octal 0664
        newfile = os.fdopen(newfd,"w+")
    except OSError as ex:
        if ex.errno == errno.EEXIST:
            newfile = open(filename,openMode)
        else:
            raise
    return newfile

def dump(self, filename = "", indent=2, **kwa):
    """ Json serialize self save to file filename"""
    if not filename:
        raise ParameterError("No filename to Dump to:")

    if 'default' in kwa: #allow override of default function
        default = kwa['default']
        del kwa['default']
    else:
        default = self._default

    with self._ocfn(filename, "w+") as f:
        json.dump(self, f, indent=indent, default=default, **kwa)
        f.flush()
        os.fsync(f.fileno())

def load(self, filename = ""):
    """ Loads json object from filename, returns unjsoned object"""
    if not filename:
        raise ParameterError("Empty filename to load.")

    with self._ocfn(filename) as f:
        dct = json.load(f, object_pairs_hook=odict)
        return self._update(dct)

def debrines(s,
             classes=None,
             propertied=False,
             safed=False,
             hinted=True,
             extendable=False):
    """ returns reconstructed brined object from class hinted JSON serialization s
        classes is a list of class objects to use to reconstruct the python objects.
        Each hint requires a class in classes whose .__name__ matches the hint
    """
    if classes is None:
        classes = []

    def hook(pairs):
        """ Method for simplejson object_pairs_hook
            pairs is ordered list of key value duples
        """
        dct = odict(pairs)
        hint =  dct.get('@class')
        for cls in classes:
            if cls.__name__ == hint:
                return brinify( cls,
                                propertied=propertied,
                                safed=safed,
                                hinted=hinted,
                                extendable=extendable)()._update(dct)

        return dct

    obj = json.loads(s, object_pairs_hook=hook)
    return obj

def debrine(filename = "",
            classes=None,
            propertied=False,
            safed=False,
            hinted=True,
            extendable=False):
    """ returns reconstructed brined object from class hinted JSON serialization
        classes is a list of class objects to use to reconstruct the python objects.
        Each hint requires a class in classes whose .__name__ matches the hint
    """
    if not filename:
        raise ParameterError("Empty filename.")

    if classes is None:
        classes = []

    def hook(pairs):
        """ Method for simplejson object_pairs_hook
            pairs is ordered list of key value duples
        """
        dct = odict(pairs)
        hint =  dct.get('@class')
        for cls in classes:
            if cls.__name__ == hint:
                return brinify( cls,
                                propertied=propertied,
                                safed=safed,
                                hinted=hinted,
                                extendable=extendable)()._update(dct)

        return dct

    with ocfn(filename) as f:
        obj = json.load(f, object_pairs_hook=hook)
        return obj


@brined()
class Brine(object):
    """ Brine

        Inheritable Mixin class that is brined.
    """
    pass

