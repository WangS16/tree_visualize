import igraph as ig
import plotly.graph_objects as go 

graph = ig.Graph.Tree(25, 2)
print(graph)

fig = go.Figure()

lay = graph.layout('rt')
vnum = graph.vcount()
position = {k: lay[k] for k in range(vnum)}
Y = [lay[k][1] for k in range(vnum)]
M = max(Y)

es = ig.EdgeSeq(graph)   # sequence of edges
E = [e.tuple for e in graph.es]   # list of edges
L = len(position)
Xn = [position[k][0] for k in range(L)]     # x postion for vertices
Yn = [2*M-position[k][1] for k in range(L)]  # y postion for vertices
Xe = []
Ye = []
for edge in E:
    Xe += [position[edge[0]][0], position[edge[1]][0], None]
    Ye += [2*M-position[edge[0]][1], 2*M-position[edge[1]][1], None]

# plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe, y=Ye, mode='lines',
                        line=dict(color='rgb(210, 210, 210)', width=1),
                        hoverinfo='none'))
fig.add_trace(go.Scatter(x=Xn, y=Yn, mode='markers', name='bla',
                        marker=dict(symbol='x-dot', 
                        size=18, color='#6175c1',
                        line=dict(color='rgb(50,50,50)', width=1)),
                        #text=graph.vs['name'],
                        #hoverinfo='text',
                        opacity=0.8))

fig.show()