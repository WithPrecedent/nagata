"""
dummy_module: fake module for module importation tests
Corey Rayburn Yung <coreyrayburnyung@gmail.com>
Copyright 2020-2022, Corey Rayburn Yung
License: Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0)

ToDo:

"""
import dataclasses


@dataclasses.dataclass
class DummyDataclass(object):
    
    pass
    
class DummyClass(object):
    
    pass
    
def dummy_function() -> None:
    return
