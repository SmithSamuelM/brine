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


http://opensource.org/licenses/MIT

The MIT License (MIT)
Copyright (c) <2013> <Samuel M. Smith>

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.