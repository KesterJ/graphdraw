import networkx as nx
#import graphviz
#import pydotplus as pydot
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
	#Needs to take a dot file (containing the graph) and a dictionary of values with same keys
	#as the node names in dot file, and set relative node sizes based on the values associated
	#with them in the dict. Modifies the dict sent in arguments rather than returning a new one.
	sizes = normalise_dict(dict1)
	for node in dot1.get_nodes():
		node.set_height(sizes[node.get_name()])
		node.set_width(sizes[node.get_name()])


def produce_graph(dotgraph, sizedict, filename):
	#Takes a Dot class produced by to_pydot, and a series of numbers with the same indices as the node
	#names in the Dot class; writes a jpg file with nodes of size determined by the series.
	set_node_sizes(dotgraph, sizedict)
	dotgraph.write_jpg(filename)
	x = [i.get_height() for i in dotgraph.get_nodes()]
	y = [i.get_width() for i in dotgraph.get_nodes()]
	z = [i.get_name() for i in dotgraph.get_nodes()]
	print("Names: ", z)
	print("Heights: ", x)
	print("Widths: ", y)



def main():
	cassettes = nx.read_graphml("cassettes.graphml")
	pydotcassettes = nx.to_pydot(cassettes)
	with open('all-cassettes-table.csv', 'r') as in_hndl:
		csv1 = [r for r in csv.DictReader(in_hndl)]
	sizedict = {}
	for cassette in csv1:
		sizedict['"'+cassette['pattern']+'"'] = cassette['control']
	pydotcassettes.set_nodesep(1)
	produce_graph(pydotcassettes, sizedict, 'examplegraphcont.jpg')


main()
