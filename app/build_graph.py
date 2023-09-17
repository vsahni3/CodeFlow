from pyvis.network import Network
from parse_files import build_files_dependency_nodes_and_edges
from parse_functions import build_funcs_dependency_nodes_and_edges

def build_dependency_graph(nodes, edges):
    net = Network(height="1250px", width="100%", bgcolor="#03001C", font_color="black", directed=True, layout={"circle": True}, select_menu=True, filter_menu=False
)

    for node in nodes:
        if "." in node[0]:
            net.add_node(n_id=node[0], title=node[1], color="#A5D7E8", size=25, label=node[0], shape="circle")
        else:
            net.add_node(n_id=node[0], title=node[1], color="#FFDEB4", size=40, label=node[0], shape="circle")
    for edge in edges:
        source, target = edge
        if "." in source:
            net.add_edge(source, target, color="#57C5B6", width=3, arrowStrikethrough=False)
        else:
            net.add_edge(source, target, color="#FFDEB4", width=3, arrowStrikethrough=False)
    return net

def build_graph(file_to_code_summary_map):
    # for key, value in file_to_code_summary_map.items():
    #     print(key)

    nodes, edges = build_files_dependency_nodes_and_edges(file_to_code_summary_map)
    dependency_graph = build_dependency_graph(nodes, edges)
    dependency_graph.show("file_graph.html", notebook=False)
    nodes, edges = build_funcs_dependency_nodes_and_edges(file_to_code_summary_map)
    dependency_graph = build_dependency_graph(nodes, edges)
    dependency_graph.show("func_graph.html", notebook=False)

file_to_code_summary_map = {
    "main": ("", "FOLDER SUMMARY"),
    "module1": ("", "FOLDER SUMMARY"),
    "module2": ("", "FOLDER SUMMARY"),
    "main/main.py": ("# main.py\nfrom module1.module1 import foo\ndef bar():\n\tbaz()\n\tfoo()\ndef baz():\n\tpass\nbar()", "SUMMARY 1"),
    "module1/module1.py": ("# module1.py\nfrom module2.module2 import foo\ndef bar():\n\tfoo()\ndef baz():\n\tpass", "SUMMARY 2"),
    "module2/module2.py": ("# module2.py\ndef foo():\n\tpass", "SUMMARY 3"),
}
