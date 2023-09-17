import ast
from utils import USER_MODULES

def is_module_used(tree, module_name):
    module_used = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id == module_name:
                module_used = True
                break
    return module_used

def extract_imports(args):
    (code, summary) = args
    tree = ast.parse(code)

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name not in USER_MODULES and is_module_used(tree, n.name):
                    imports.append(n.name.replace(".", "/") + ".py")
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for n in node.names:
                if module not in USER_MODULES and is_module_used(tree, n.name):
                    imports.append(f"{module}".replace(".", "/") + ".py")
    return imports

def build_files_dependency_nodes_and_edges(file_to_code_summary_map):
    nodes = set()
    edges = []

    for file in file_to_code_summary_map:
        if file.endswith(".py"):
            folder_name, file_node_name = file.split("/")
            nodes.add((folder_name, file_to_code_summary_map[folder_name][1]))
            nodes.add((file_node_name, file_to_code_summary_map[file][1]))
            edges.append((folder_name, file_node_name))
            imports = extract_imports(file_to_code_summary_map[file])

            for imp in imports:
                if imp.startswith("."):
                    folder_src, file_src = file.split("/")
                    folder_dest, file_dest = (imp + ".py").split("/")
                    edges.append((file_dest, file_src))
                else:
                    folder_src, file_src = file.split("/")
                    folder_dest, file_dest = imp.split("/")
                    edges.append((file_dest, file_src))

    return list(nodes), edges
