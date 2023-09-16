from pyvis.network import Network
from parse_files import build_files_dependency_nodes_and_edges
from parse_functions import build_funcs_dependency_nodes_and_edges

def build_dependency_graph(nodes, edges):
    net = Network(height="1250px", width="100%", bgcolor="#03001C", font_color="#FFF2F2", directed=True, layout={"circle": True}
)

    for node in nodes:
        if "." in node:
            net.add_node(n_id=node, title=node, color="#A5D7E8", size=25, label=node)
        else:
            net.add_node(n_id=node, title=node, color="#FFDEB4", size=40, label=node)
    for edge in edges:
        source, target = edge
        if "." in source:
            net.add_edge(source, target, color="#57C5B6", width=3, arrowStrikethrough=0.0005)
        else:
            net.add_edge(source, target, color="#FFDEB4", width=3)
    return net

if __name__ == "__main__":
    src_folder = "src"
    nodes, edges = build_files_dependency_nodes_and_edges(src_folder)
    dependency_graph = build_dependency_graph(nodes, edges)
    dependency_graph.show("file_graph.html", notebook=False)
    nodes, edges = build_funcs_dependency_nodes_and_edges(src_folder)
    dependency_graph = build_dependency_graph(nodes, edges)
    dependency_graph.show("func_graph.html", notebook=False)
