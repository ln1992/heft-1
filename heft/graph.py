# Functions associated with creating a Graph that can be used in the HEFT algorithm


import networkx as nx
from task import Task
import random
import ast

def create_processors(processors):
    """
    Function that creates a given number of processors
    
    :param processors: The number of processors 
    """
    processor_dict = dict() 
    for x in range(0,processors):
        processor_dict[x]=[] 

    return processor_dict

def random_comp_matrix(processors, nodes, cost):
    """
    Function that generates a random cost matrix for a number of tasks
    
    :param processors: Number of processors available
    :param nodes: Number of nodes with costs
    :param cost: A range that determines the maximum random cost that can be generated
    """
    
    # For each processor, we have a list of nodes with computation/communication costs 
    computation_matrix = dict()

    for x in range(nodes):
        computation_matrix[x] = random.sample(range(cost),processors)
    name = 'comp_matrix_{0}.txt'.format(processors)    
    file = open(name,'w')
    file.write("P1,P2,...,Pn\n") 
    for n in range(len(computation_matrix)):
        file.write(str(computation_matrix[n])+'\n')
    file.close()

    
    return computation_matrix

def read_comp_matrix(file_name):
    count = 0
    matrix = dict()
    with open(file_name) as f:
        for line in f:
            if count is 0:
                ## skip the first line
                count = count + 1
            else:
                matrix[count-1] = ast.literal_eval(line)
                count = count + 1


    return matrix

def random_comm_matrix(nodes, cost):
    """
    Function that generates a random communication cost (n x n) matrix for a number of tasks
    
    :param nodes: Number of nodes with costs
    :param cost: A range that determines the maximum random cost that can be generated
    """
    
    # For each processor, we have a list of nodes with communication costs 
    #communication_matrix = dict()
    communication_matrix = [[0 for x in range(nodes)] for x in range(nodes)] 
    for x in range(nodes-1):
        for y in range(x+1,nodes):
            communication_matrix[x][y]=random.randint(0,cost)
            communication_matrix[y][x]=communication_matrix[x][y]

    return communication_matrix

def init_tasks(graph, comp_matrix):
    for task in graph:
         task.comp_cost = comp_matrix[task.tid]    
 

def random_task_dag(nodes, edges):
    """Generate a random Directed Acyclic Graph (DAG) with a given number of nodes and edges.
    Modified from source: http://ipyparallel.readthedocs.io/en/latest/dag_dependencies.html
    """
    graph = nx.DiGraph()
    count = 0
    if nodes is 1:
        return graph
    for i in range(nodes):
        graph.add_node(Task(i))
    graph.add_edge(Task(0), Task(1))
    while edges > 0:
        a = Task(random.randint(0,nodes-1))
        b=a
        while b.tid==a.tid:
            b = Task(random.randint(1,nodes-1))
        if b.tid > 0 and a >=0 :
            graph.add_edge(a,b)
            if nx.is_directed_acyclic_graph(graph):
                edges -= 1
            else:
                # we closed a loop!
                graph.remove_edge(a,b)
        else:
            continue

    node_list = graph.nodes()
    count = 1
    for node in node_list:
        if node.tid != 0:
            predecessors = graph.predecessors(node)
            while predecessors is []:
                new_task = random.randint(1,nodes-1)
                graph.add_edge(new_task,node)
                if  nx.is_directed_acyclic_graph(graph):
                    predecessors = graph.predecessors(node)     
                else:
                    graph.remove_edge(new_task,node)
        else:
            continue

    return graph

def gen_test_graph():
    # Calc. rank by hand is a pain; the hard work is done here
    # 1 processor
    # Task A = 0, Task B = 1 etc. 
    # A comp_cost = 4
    # B comp_cost = 6
    # C comp_cost = 9
    # D comp_cost = 3
    # A->B; A->C; B->D; C->D
    nodes = [Task(x) for x in range(4)]

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    # init_tasks(graph,comp_matrix)
    graph.add_edge(nodes[0],nodes[1]) #A->B
    graph.add_edge(nodes[0],nodes[2]) #A->C
    graph.add_edge(nodes[1],nodes[3]) #B->D
    graph.add_edge(nodes[2],nodes[3]) #C->D
    comm = {0:[0,1,1,0],1:[0,0,0,2],2:[0,0,0,2],3:[0,0,0,0]} 
    comp = {0:[4,4],1:[6,6],2:[9,9],3:[3,3]}

    file = open('test_comp.txt','w')
    file.write("P1,P2,...,Pn\n") 
    for n in range(len(comp)):
        file.write(str(comp[n])+'\n')
    file.close()

    file = open('test_comm.txt','w')
    file.write("N1,N2,...,Nn\n") 
    for n in range(len(comm)):
        file.write(str(comm[n])+'\n')
    file.close()

    nx.write_graphml(graph, "unit_test.graphml")
    print 'Test' + str(graph.nodes())
    return graph

def seq_task_dag(nodes):
    """Generate a sequential Directed Acyclic Graph (DAG) with a given number of nodes and edges.
    """
    graph = nx.DiGraph()
    for i in range(nodes):
        graph.add_node(i)
    
    for i in range(nodes-1):
        graph.add_edge(i,i+1)

    return graph

if __name__ == "__main__":
    """
    Working with graphs
    """

    test = gen_test_graph()
    num_processors=3
    nodes=50    
    edges=100

#   comp_matrix = random_cost_matrix(processors, nodes,100) 
#   comm_matrix = random_cost_matrix(node, nodes,50) # Node x Node communication matrix
    processors = create_processors(num_processors)
    graph = random_task_dag(nodes,edges)
    nx.write_adjlist(graph,"test.adjlist")
    fh=open("test.adjlist", 'rb')
    G=nx.read_adjlist(fh)
    nx.write_graphml(G, "test.graphml")
    new_graph = nx.read_graphml("test.graphml")
   # print G.nodes()
    seq = seq_task_dag(10)
    nx.write_graphml(seq, "seq.graphml")
    seq_copy = nx.read_graphml("seq.graphml")
    # print seq.nodes()
    # print seq_copy.nodes()
    # print seq_copy.edges()
    # print test.nodes()

    # def parse_type(node_type):
    #     return node_type
    # val = 53
    # tmp_node = parse_type(Task)(val)  
    # print tmp_node.comp_cost

    gen_test_graph()
    #matrix=random_comp_matrix(2,10,10)
    val = read_comp_matrix('test_comp.txt')
    # print new_graph.nodes()
    # nodes = graph.nodes()
    # for node in nodes:
    #     print graph.predecessors(node)

        
