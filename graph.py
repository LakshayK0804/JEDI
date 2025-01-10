#Includes all functionality for visually displaying the AST
import graphviz
import javalang
#Create a Graphviz graph object
graph = graphviz.Digraph(format='png', engine='dot')

#Function to recursively create a Graphviz Digraph for the AST
def addGraphNodes(node, graph, parent=None):
    #Create a unique identifier for the node
    node_name = f"{id(node)}"  # Use the memory address as a unique identifier

    #Gather relevant information to label the node
    node_label = f"{node.__class__.__name__}"
    if hasattr(node, 'name'):  #Example: add variable/method name for better detail
        node_label += f": {node.name}"

    #Create the node in the graph
    graph.node(node_name, label=node_label, shape="box", style="rounded")

    #Add an edge from the parent to this node (if parent exists)
    if parent:
        graph.edge(parent, node_name)

    #Recursively process all the children of this node
    for child_name, child_node in vars(node).items():
        if isinstance(child_node, list):  #If it's a list, process each item
            for item in child_node:
                if isinstance(item, javalang.tree.Node):  #Check if the item is a node
                    addGraphNodes(item, graph, node_name)
        elif isinstance(child_node, javalang.tree.Node):  #If it's a single node, process it
            addGraphNodes(child_node, graph, node_name)

#renders and creates graph file
def renderGraph(tree):
    #Start the recursive process from the root of the AST
    addGraphNodes(tree, graph)

    #Render the graph to a file, cleanup removes previousely rendered graphs
    graph.render('astTree', cleanup=True)

#Traverse through and print all tree information in AST
def printJavaTree(tree):
    for path, node in tree:
        print("Path: ", path, " Node: ", node)
        print(vars(node))   #Printing all node attributes

#Prints all information of a node
def printNode(node):
    print(node)