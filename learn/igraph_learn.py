import logging
import igraph as ig 
print(ig.__version__)

# 创建一个无向图，并且手动添加节点和边
# g = ig.Graph()
# g.add_vertices(3)
# g.add_edges([(0, 1), (1, 2)])
# g.add_edges([(2, 0)])
# g.add_vertices(3)
# g.add_edges([(2, 3), (3, 4), (4, 5), (5, 3)])
# g.delete_edges(g.get_eid(2, 3))

# 确定图和随机图的一个实例
# 确定图
# g = ig.Graph.Tree(127, 2)
# g.get_edgelist()[0:10]
# 随即图
# g = ig.Graph.GRG(100, 0.2)

g = ig.Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
print(g.es[0].source)     # 返回边的源顶点
print(g.es[0].target)     # 返回边的目标顶点
print(g.es[0].tuple)      # 返回边的源顶点和目标顶点，以元组的形式
print(g.es[0].attributes())   # 返回边的属性
print(g.es[0].index)      # 返回边的ID

g['data'] = '2020-04-02'    # 图对象本身也可以作为字典使用
print(g['data'])

# 使用del关键字
g.vs[3]['foo'] = 'bar'
print(g.vs['foo'])
del g.vs['foo']
try:
    print(g.vs['foo'])
except Exception as e:
    print('-'*10)
    logging.exception(e)
    print('-'*10)

# print(g)
ig.summary(g)