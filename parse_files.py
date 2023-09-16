import os
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

def extract_imports(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read(), filename=file_path)

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

def build_files_dependency_nodes_and_edges(root_dir):
    nodes = set()
    edges = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_name = os.path.relpath(file_path, root_dir)
                folder_name, file_node_name = file_name.split("/")
                nodes.add(folder_name)
                nodes.add(file_node_name)
                edges.append((folder_name, file_node_name))
                imports = extract_imports(file_path)

                for imp in imports:
                    if imp.startswith("."):
                        imp_path = os.path.normpath(os.path.join(root, imp + ".py"))
                        imp_name = os.path.relpath(imp_path, root_dir)
                        edges.append((file_name, imp_name))
                    else:
                        folder_src, file_src = file_name.split("/")
                        folder_dest, file_dest = imp.split("/")
                        edges.append((file_dest, file_src))

    return list(nodes), edges
