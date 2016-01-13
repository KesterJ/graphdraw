import networkx as nx
import csv


def normalise_dict(dict1):
	#Add description
	value_list = [float(i) for i in dict1.values()]
	dict_min = min(value_list)
	normal_dict = {}
	for key in dict1:
		normal_dict[key] = float(dict1[key])/dict_min
	return normal_dict


def set_node_sizes(dot1, dict1):
	#Needs to take a dot object (containing the graph) and a dictionary of values with same keys
	#as the node names in dot file, and set relative node sizes based on the values associated
	#with them in the dict. Modifies the dict sent in arguments rather than returning a new one.
	sizes = normalise_dict(dict1)
	for node in dot1.get_nodes():
		node.set_height(sizes[node.get_name()])
		node.set_width(sizes[node.get_name()])


def set_node_names(dot1, dict1):
	#Takes the same arguments as set_node_sizes, and simply adds the (original, not normalised) sizes
	#to the name of each node.
	for node in dot1.get_nodes():
		name = node.get_name()
		node.set_label(name[:-1]+'\n\nCount: '+dict1[name]+'"')
		print(node.get_label())

def produce_graph(nxgraph, sizedict, filename):
	#Takes a Networkx graph, and a series of numbers with the same indices as the node
	#names; writes a jpg file with nodes of size determined by the series.
	dotgraph = nx.to_pydot(nxgraph)
	set_node_sizes(dotgraph, sizedict)
	set_node_names(dotgraph, sizedict)
	dotgraph.set_nodesep(1)
	dotgraph.write_jpg(filename)
	"""
	x = [i.get_height() for i in dotgraph.get_nodes()]
	y = [i.get_width() for i in dotgraph.get_nodes()]
	z = [i.get_name() for i in dotgraph.get_nodes()]
	print("Names: ", z)
	print("Heights: ", x)
	print("Widths: ", y)
	"""

def main():
	cassettes = nx.read_graphml("cassettes.graphml")
	#pydotcassettes = nx.to_pydot(cassettes)
	with open('all-cassettes-table.csv', 'r') as in_hndl:
		csv1 = [r for r in csv.DictReader(in_hndl)]
	sizedict = {}
	for cassette in csv1:
		sizedict['"'+cassette['pattern']+'"'] = cassette['control']
	produce_graph(cassettes, sizedict, 'examplegraphcont2.jpg')


main()
