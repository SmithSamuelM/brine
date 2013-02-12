brine
=====

Python Object to/from JSON serializer/deserializer

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
JSON deserialization / Python classification.

Major limitation vis a vis pickle is that the hint does not guarantee that 
the same class is used for both serialization and deserialization other than
in name only.

Example Usage:
```python
from brining import brined, Brine, debrines
```

Decorator:

```python
@brined()
class B(object):
    def __init__(self):
        self.x =  1
        self.y =  2
        self.z =  3
```

Mixin:

```python
class B(Brine):
    def __init__(self):
        self.x =  1
        self.y =  2
        self.z =  3
```

Wrapper Function:

```python
brinify(B)
```

Examples:

```python
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
```

Utility Function:

```python
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
```
See LICENSE.txt for Licensing details
Copyright (c) <2013> <Samuel M. Smith>
    