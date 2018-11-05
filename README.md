## About
Quickly generate Graphene ObjectType definitions from dictionaries, lists, or JSON strings.

[Graphene](https://graphene-python.org/) is an awesome library that helps you build GraphQL APIs in Python. The goal of this project is to make it that much easier to use Graphene.

___

## Basics
The three main functions in this library are `from_dict`, `from_list`, and `from_json`. Each Returns a lists containing strings that define one or many Graphene ObjectType definitions.

##### Dictionaries

To generate an ObjectType definition from a dictionary use the `from_dict` function. Pass in the name of the class and a dictionary containing your data.
```Python
>>> from objecttype_generator import from_dict
>>> person = {'first_name':'John', 'last_name':'Doe', 'age':32 }
>>> for objecttype in from_dict('PersonType', person):
...     print(objecttype)
...
class PersonType(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    age = graphene.Int()
```
In the example above, only one list item was returned. Keep in mind that the ObjectType definition is just a string. Each key in the person dictionary became a field of the string representing the PersonType class. Also note that the appropriate Graphene Scalar was automatically assigned to each field.

##### Lists
Generating an ObjectType definition from a list is similar. You use the `from_list` function passing in the attribute name, a list containing your data, and an optional class name. By default, the class name is 'Query'.
```Python
>>> from objecttype_generator import from_list
>>> numbers = [1, 2, 3, 4, 5]
>>> for objecttype in from_list('numbers', numbers, 'NumberType'):
...     print(objecttype)
...
class NumberType(graphene.ObjectType):
    numbers = graphene.List(graphene.Int,)


    def resolve_numbers(self, info, *args, **kwargs):
        pass
```
The list passed in should contain Python primitives that relate to [Graphene Scalars](https://docs.graphene-python.org/en/latest/types/scalars/) or a dictionary. However, because schema are assumed to be consistent, the first element of the list will be used to determine the appropriate ObjectType that the List field returns. Also note that in the example above a resolver function was automatically generated for the numbers field. This will happen for all Graphene Lists and Fields.


##### JSON Strings

Maybe you want to map an existing REST API to a GraphQL API. An easy way to get that process started is by making requests to each REST endpoint and using the `from_json` function to parse the response. Here's an example using [IEX's company endpoint](https://iextrading.com/developer/docs/#company).
```Python
>>> from objecttype_generator import from_json
>>> import requests
>>> url = 'https://api.iextrading.com/1.0/stock/aapl/company'
>>> resp = requests.get(url)
>>> for objecttype in from_json('CompanyType', resp.text):
...     print(objecttype)
...
class CompanyType(graphene.ObjectType):
    symbol = graphene.String()
    companyName = graphene.String()
    exchange = graphene.String()
    industry = graphene.String()
    website = graphene.String()
    description = graphene.String()
    CEO = graphene.String()
    issueType = graphene.String()
    sector = graphene.String()
    tags = graphene.List(graphene.String,)


    def resolve_tags(self, info, *args, **kwargs):
        pass

```

##### Writing to Files
Obviously, printing out ObjectType definitions can only get you so far. `to_py_file` is a convenience function provided to write ObjectType definitions to files. `to_py_file` takes two positional arguments: the full path to a .py file and a list of ObjetType definitions. Lets reuse the dictionary example from above.
```Python
>>> import os
>>> from objecttype_generator import from_dict
>>> from objecttype_generator.file_generator import to_py_file
>>> path = os.path.abspath('.')
>>> file = os.path.join(path, 'example.py')
>>> person = {'first_name':'John', 'last_name':'Doe', 'age':32 }
>>> to_py_file(file, from_dict('PersonType', person))
>>>os.listdir(path)
['example.py']
>>> with open(file) as f:
...     print(f.read())
...
import graphene

class PersonType(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    age = graphene.Int()


```
In this example we created example.py in the current directory, and the file contais the ObjetType definition. By default, 'import graphene' will be prepended to the top of the file. If you don't want to include this import, you can pass `include_imports = False` to `to_py_file`. Additional imports can be specified as a list using the `import_list` kwarg.
___

## Additional Information

##### Nested dictionaries
In the event that nested dictionaries are encountered while parsing the data inputs to `from_dict`, `from_list`, or `from_json`, an ObjectType definition will be generated for each. The name of the auto-generated, nested ObjectType will be the name of the field in title case + 'Type'. The following example illustrates the point.
```Python
>>> from objecttype_generator import from_dict
>>> nested = {'base':{'deep':{'even_deeper':'some random string'}}}
>>> for objecttype in from_dict('NestExample', nested):
...     print(objecttype, end='\n\n')
...
class DeepType(graphene.ObjectType):
    even_deeper = graphene.String()

class BaseType(graphene.ObjectType):
    deep = graphene.Field(DeepType,)


    def resolve_deep(self, info, *args, **kwargs):
        pass



class NestExample(graphene.ObjectType):
    base = graphene.Field(BaseType,)


    def resolve_base(self, info, *args, **kwargs):
        pass


```
Inspecting the output shows that 3 classes were created: DeepType, BaseType, and NestedExample. We only specified NestedExample. DeepType and BaseType were generated using the named of the field that they correspond to in title case followed by 'Type'. BaseType represents the first nested dictionary. The only key (deep) of the first nested dictionary matches the only field of BaseType. Similarly, DeepType represents the second nested dictionary. Again note that the second nested dictionary only contains one key (even_deeper), and DeepType's only field matches it exactly.

##### None, Empty Lists, and Empty Dictionaries
In the event that None values, empty lists, or empty dictionaries are encountered while parsing data, a placeholder and warning description will be used. Here's an example of what you can expect to see.
```Python
>>> from objecttype_generator import from_dict
>>> none_example = {"none_field":None, "empty_list":[], "empty_dict":{}}
>>> for objecttype in from_dict('NoneExample', none_example):
...     print(objecttype, end='\n\n')
...
class Empty_DictType(graphene.ObjectType):
    pass


class NoneExample(graphene.ObjectType):
    none_field = graphene.Field(UnknownType,
        description = 'WARNING! Received a None value for field: none_field.',
    )
    empty_list = graphene.List(UnknownType,
        description = 'WARNING! Received an empty list for field: empty_list.',
    )
    empty_dict = graphene.Field(UnknownType,
        description = 'WARNING! Received an empty dictionary for field: empty_dict.',
    )


    def resolve_empty_list(self, info, *args, **kwargs):
        pass

    def resolve_empty_dict(self, info, *args, **kwargs):
        pass


```
Each field above either returns an "UnknownType" or a list of "UnknownTypes". Note that "UnknownType" is never actually defined. Trying to use the auto-generated ObjectType definition as is would surly throw an error. To make it even more clear that something went wrong, a warning was added to the description of each field. If you encounter one of these don't panic, just double check your function inputs or manually assign these fields. You might find it odd that a placeholder ObjectType was not generated for none_field. Additional classes are only created if nested dictionaries are found. Because None was found, its unclear what the value of that field is supposed to be, and as a result, no placeholder ObjectType is generated.

___
This library is still under development.
