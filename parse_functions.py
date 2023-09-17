import ast

def build_function_call_graph(args):
    (code, summary) = args
    tree = ast.parse(code)

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

def build_funcs_dependency_nodes_and_edges(file_to_code_summary_map):
    nodes = set()
    edges = []

    for file in file_to_code_summary_map:
        if file.endswith(".py"):
            call_graph = build_function_call_graph(file_to_code_summary_map[file])
            for key in call_graph.keys():
                nodes.add((key, key))
    for file in file_to_code_summary_map:
        if file.endswith(".py"):
            for key in call_graph.keys():
                for value in call_graph[key]:
                    if (value, value) in nodes:
                        edges.append((key, value))
    return list(nodes), edges