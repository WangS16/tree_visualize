"""
    pyToJson
    ~~~

    This python script is used to read python source code from a script or 
    string and generate the following abstract syntax tree(AST) in Json format:
    {
        'code': '',
        'ast':[
            {'type': 'node', 'name': nodename, 'children': [int]}
            {'type': 'attr', 'name': node._fields[i], 'children': [int]}
            {'type': 'attr', 'name': node._fields[i], 'value': [Any]}
            ...
        ]
    }
    or
    {
        'file': '',
        'ast':[
            {'type': 'node', 'name': nodename, 'children': [int]}
            {'type': 'attr', 'name': node._fields[i], 'children': [int]}
            {'type': 'attr', 'name': node._fields[i], 'value': [Any]}
            ...
        ]
    }
    

"""

import ast
import json
from typing import List, Dict

def ast_to_json(tree):
    """
    transform the abstract syntax tree(AST) of python source code to 
    json.

    :Args
        tree: ast.AST
    
    :Returns
        json_tree: List[Dict]
    generate format:
    [
        {'type': 'node', 'name': nodename, 'children': [int]}
        {'type': 'attr', 'name': node._fields[i], 'children': [int]}
        {'type': 'attr', 'name': node._fields[i], 'value': [Any]}
        ...
    ]        
    """
    json_tree = []
    
    def transform_node(node):
        """
        generate format:
        {'type': 'node', 'name': nodename, 'children': [int]}        
        """
        pos = len(json_tree)
        json_next = {}
        json_tree.append(json_next)
        json_next['type'] = 'node'
        json_next['name'] = type(node).__name__
        children = []
        for attr in node._fields:
            children.append(transform_attr(node, attr))
        
        json_next['children'] = children

        return pos 
        

    def transform_attr(node, attr):
        """
        generate format:
        {'type': 'attr', 'name': node._fields[i], 'children': [int]}
        or
        {'type': 'attr', 'name': node._fields[i], 'value': [Any]}
        """
        def item_handler(items):
            if isinstance(items, List):
                for item in items:
                    item_handler(item)
            elif isinstance(items, ast.AST):
                children.append(transform_node(items))
            else:
                value.append(items)

        pos = len(json_tree)
        json_next = {}
        json_tree.append(json_next)
        json_next['type'] = 'attr'
        json_next['name'] = attr
        children = []
        value = []
        attr_value = getattr(node, attr)
        item_handler(attr_value)

        if children:
            json_next['children'] = children
        if value:
            json_next['value'] = value

        return pos

    transform_node(tree)
    return json_tree

def read_file_to_string(filename):
    f = open(filename, 'rt')
    s = f.read()
    f.close()
    return s

def parse_file(filename, mode='exec') -> Dict:
    """
    Parse python source code stored in a file.

    :Args
        filename: the path of python script.
        mode: parameter from ast.parse() or compile(). 

    :Returns:
        a Dict storing the file path and corresponding AST information.
    """
    tree = ast.parse(read_file_to_string(filename), filename, mode=mode)
    json_tree = ast_to_json(tree)
    json_file_tree = {}
    json_file_tree['file'] = filename
    json_file_tree['AST'] = json_tree
    return json_file_tree
    # print(json.dumps(json_tree, separators=(',',''),indent=4))
def parse_source_code(source:str, mode='exec') -> Dict:
    """
    Parse python source code stored in a string.

    :Args
        source: a string for python source code.
        mode: parameter from ast.parse() or compile(). 

    :Returns:
        a Dict storing the source code and corresponding AST information.    
    """
    tree = ast.parse(source, mode=mode)
    json_tree = ast_to_json(tree)
    json_code_tree = {}
    json_code_tree['code'] = source
    json_code_tree['AST'] = json_tree
    return json_code_tree

def parse_file_with_save(filename, save_path, mode='exec', 
                                separators=None, indent=None,
                                file_append=False):
    """
    Parse python source code stored in a file and save as a Json file.

    :Args
        filename: the path of python script.
        save_path: the path of generating json file.
        mode: parameter from ast.parse() or compile().  
        separators: parameter from json.dump().
        indent: parameter form json.dump().        
    """
    json_file_tree = parse_file(filename, mode=mode)
    write_mode = 'a' if file_append else 'w'
    with open(save_path, write_mode) as f:
        json.dump(json_file_tree, f, separators=separators, indent=indent)

def parse_source_code_with_save(source:str, save_path, mode='exec', 
                                separators=None, indent=None,
                                file_append=False):
    """
    Parse python source code stored in a string and save as a Json file.

    :Args
        source: a string for python source code.
        save_path: the path of generating json file.
        mode: parameter from ast.parse() or compile().
        separators: parameter from json.dump().
        indent: parameter form json.dump().    
    """
    json_code_tree = parse_source_code(source, mode=mode)
    write_mode = 'a' if file_append else 'w'
    with open(save_path, write_mode) as f:
        json.dump(json_code_tree, f, separators=separators, indent=indent)

def print_parse_file(filename, mode='exec'):
    """
    Parse python source code stored in a file and print in a beautiful 
    format.

    :Args
        filename: the path of python script.
        mode: parameter from ast.parse() or compile().    
    """
    json_file_tree = parse_file(filename, mode=mode)
    print('file:', json_file_tree['file'])
    json_tree = json_file_tree['AST']
    print('AST: [')
    for i, d in enumerate(json_tree):
        print('%d:\t%s' % (i+1, d))
    print(']')

def print_parse_source_code(source:str, mode='exec'):
    """
    Parse python source code stored in a string and print in a beautiful 
    format.

    :Args
        source: a string for python source code.
        mode: parameter from ast.parse() or compile().
    """
    json_code_tree = parse_source_code(source, mode=mode)
    print('code: \"', json_code_tree['code'], '\"')
    json_tree = json_code_tree['AST']
    print('AST: [')
    for i, d in enumerate(json_tree):
        print('%d:\t%s' % (i+1, d))
    print(']') 



if __name__ == "__main__":
    # -------------------------------------------------------
    # Code to test if the function works correctly
    # -------------------------------------------------------
    testfile = "D:\\Code\\tree_visualize\\src\\test.py"
    savefile = "D:\\Code\\tree_visualize\\data\\json\\test.json"
    parse_file_with_save(testfile, savefile, indent=2, file_append=True)
    print_parse_file(testfile)

    source = """
def func(a, b):
    pass
"""
    source_savefile = "D:\\Code\\tree_visualize\\data\\json\\source.json"
    parse_source_code_with_save(source, source_savefile, indent=2, file_append=True)
    print_parse_source_code(source)