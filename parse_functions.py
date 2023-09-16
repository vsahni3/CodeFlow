import ast
import os

def build_function_call_graph(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=file_path)
    call_graph = {}
    def traverse(node, current_function):
        if isinstance(node, ast.FunctionDef):
            current_function = node.name
            call_graph[current_function] = set()
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            called_function = node.func.id
            if current_function:
                call_graph[current_function].add(called_function)
        for child_node in ast.iter_child_nodes(node):
            traverse(child_node, current_function)

    traverse(tree, None)
    return call_graph

def build_funcs_dependency_nodes_and_edges(root_dir):
    nodes = set()
    edges = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                call_graph = build_function_call_graph(file_path)
                for key in call_graph.keys():
                    nodes.add(key)
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                for key in call_graph.keys():
                    for value in call_graph[key]:
                        if value in nodes:
                            edges.append((key, value))
    return list(nodes), edges