import os
import json
import igraph as ig 
import plotly.graph_objects as go 


def readJsonAndReturnAST(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        json_file_tree = json.load(f)
        json_tree = json_file_tree['AST']
        return json_tree

def decoupling_leaf(json_tree):
    leaf = []
    leaf_pos = len(json_tree)
    for i in range(len(json_tree)):
        if 'value' in json_tree[i].keys():
            json_tree[i]['children'] = []
            for j in json_tree[i]['value']:
                dic = {'type': 'leaf', 'name':j}
                leaf.append(dic)
                json_tree[i]['children'].append(leaf_pos)
                leaf_pos += 1
    json_tree += leaf
    return json_tree

def gen_ast_graph(json_tree):
    g = ig.Graph()

    # plot_vertices
    g.add_vertices(len(json_tree))
    vertices_type = []
    vertices_name = []

    for i in range(len(json_tree)):
        vertices_type.append(json_tree[i]['type'])
        vertices_name.append(json_tree[i]['name'])

    g.vs['type'] = vertices_type
    g.vs['name'] = vertices_name

    # plot_edges
    # i: source vertice
    next_vertices = len(json_tree)
    for i, dic in enumerate(json_tree):
        if 'children' in dic.keys() and dic['children']:
            # j: target vertice
            for j in dic['children']:
                g.add_edges([(i, j)])
    
    ig.summary(g)
    return g

def graph_tree_visualize(graph):
    # get postion of vertices and edges
    lay = graph.layout('rt', root=0)
    vnum = graph.vcount()
    position = {k: lay[k] for k in range(vnum)}
    Y = [lay[k][1] for k in range(vnum)]
    M = max(Y)

    es = ig.EdgeSeq(graph)   # sequence of edges
    E = [e.tuple for e in graph.es]   # list of edges
    Xn = [2*position[k][0] for k in range(vnum)]     # x postion for vertices
    # Xn2 = [i*2 for i in Xn]
    Yn = [2*M-position[k][1] for k in range(vnum)]  # y postion for vertices
    # Yn2 = [i*2 for i in Yn]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [2*position[edge[0]][0], 2*position[edge[1]][0], None]
        Ye += [2*M-position[edge[0]][1], 2*M-position[edge[1]][1], None]
    # Xe2 = [i*2 for i in Xe if i]
    # Ye2 = [i*2 for i in Ye if i]

    # plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe, y=Ye, mode='lines',
                            line=dict(color='rgb(128, 128, 128)', 
                            shape='hv', width=1),
                            hoverinfo='none'
                            ))
    fig.add_trace(go.Scatter(x=Xn, y=Yn, mode='markers', name='bla',
                            marker=dict(symbol='line-ew', # vertices have no shape
                            size=30, color='rgb(200, 200, 200)',
                            line=dict(color='rgb(248,248,248)',
                                    width=1)),
                            text=graph.vs['type'],
                            hoverinfo='text',
                            opacity=1
                            ))
    
    axis = dict(showline=False, zeroline=False,
                showgrid=False, showticklabels=False,)
    annotations = []
    for k in range(vnum):
        annotations.append(dict(
            text = graph.vs['name'][k],
            x = Xn[k], y = Yn[k],
            xref='x1', yref='y1',
            font=dict(color='rgb(63, 159, 111)',
                    size=10),
            showarrow=False
        ))
    fig.update_layout(title='AST Tree with Reingold-Tilford Layout',
                        annotations=annotations,
                        xaxis=axis,
                        yaxis=axis,
                        hovermode='closest',
                        plot_bgcolor='rgb(248, 248, 248)',
                        boxgap=1,
                        boxmode='group'
                        )
    
    return fig



# read ast information stored in json file
ast_json_path = 'data/json/source.json'
json_tree = readJsonAndReturnAST(ast_json_path)
json_tree_with_leaf = decoupling_leaf(json_tree)
print(json_tree_with_leaf)
# print(type(json_tree))

# generate graph from json tree information
g = gen_ast_graph(json_tree_with_leaf)
# print(g)
# print(g.vcount())
fig = graph_tree_visualize(g)
fig.show()