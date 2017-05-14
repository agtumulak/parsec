# Parsec
A general-purpose parser for formatted data output.

## About
Very frustratingly, some codes do not provide easy access to results in binary 
format. Instead, you have to write yet another plain text parser. Parsec 
tries to solve this problem by generalizing the process of parsing a formatted 
output file. The user just has to create a dictionary defining the structure of 
his/her formatted output. The format dictionary is a nested dictionary of 
regular expressions which define section start tokens. The leaves of this 
tree data structure are function objects which are called when the line is 
processed. Because the logic of parsing is separated from the structure of the 
formatted output, this should make it easier to write formatted text parsers in 
da future.

## Usage
A test script which parses `test/meshtal` is provided in `test/parsemeshta.py`. 
From the root directory of parsec run the test parser as a module

```bash
python -m test.parse_meshtal
```
Note that all that the user has to do to produce this output is create a 
dictionary `_format` in `test/parse_meshtal.py` 

```python
_format = {
        re.compile(r'^(mcnp\s+version)') : version_number,
        re.compile(r' Mesh Tally Number\s+(\d{1,8})') : {
            re.compile(r'^\s+(\w) direction') : extents,
            re.compile(r'^\s+(X\s+Y\s+Z\s+Result\s+Rel Error)') : named,
            },
        re.compile(r'made_up') : 's',
        }
```
, define the leaf node functions, and call

```python
parsec(inputfile, _format)
```
The formatted data

```
 Mesh Tally Number       314
 This is a neutron mesh tally.

 Tally bin boundaries:
    X direction:    -10.71     10.71
    Y direction:    -10.71     10.71
    Z direction:   -183.00    183.00
    Energy bin boundaries: 0.00E+00 1.00E+36

        X         Y         Z     Result     Rel Error
      0.000     0.000     0.000 0.00000E+00 0.00000E+00

 Mesh Tally Number       324
 This is a neutron mesh tally.

 Tally bin boundaries:
    X direction:     53.55     74.97
    Y direction:     32.13     53.55
    Z direction:   -183.00    183.00
    Energy bin boundaries: 0.00E+00 1.00E+36

        X         Y         Z     Result     Rel Error
     64.260    42.840     0.000 0.00000E+00 0.00000E+00
...
```
is converted to an in-memory representation

```
{'314': {'X': {u'max': '10.71', u'min': '-10.71'},
         'X         Y         Z     Result     Rel Error': {u'RelError': '0.00000E+00',
                                                            u'Result': '0.00000E+00',
                                                            u'X': '0.000',
                                                            u'Y': '0.000',
                                                            u'Z': '0.000'},
         'Y': {u'max': '10.71', u'min': '-10.71'},
         'Z': {u'max': '183.00', u'min': '-183.00'}},
 '324': {'X': {u'max': '74.97', u'min': '53.55'},
         'X         Y         Z     Result     Rel Error': {u'RelError': '0.00000E+00',
                                                            u'Result': '0.00000E+00',
                                                            u'X': '64.260',
                                                            u'Y': '42.840',
                                                            u'Z': '0.000'},
         'Y': {u'max': '53.55', u'min': '32.13'},
         'Z': {u'max': '183.00', u'min': '-183.00'}},
...
```
