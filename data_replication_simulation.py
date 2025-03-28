from pprint import pp
import random
import networkx as nx
import matplotlib.pyplot as plt
import csv
from node import StorageNode, Master, ClientNode

class DataReplicationSim:
  def __init__(self, n_nodes=30, selected_client_nodes=[], write_actions=[], read_actions=[]):
    seed = 10 # recreate randomness
    random.seed(seed) 
    self.graph = nx.random_geometric_graph(n_nodes, 0.1, seed=seed) # generate connected graph

    self.write_actions = write_actions
    self.read_actions = read_actions
    self.total_hops = [0] # we put the int in a list so that we can pass by reference. I currently don't know of a better way to pass by ref

    # radom_geometric_graph isn't guarenteed to generate a connected graph, so in the event that it doesn't, we will manually connect them.
    self.connectAllNode()

    self.nodes = {} # map of node Id to the Node object
    self.clients = [] # list of client nodes
    self.master = Master("M")

    # # assign random nodes as client and storage node and add it to the self.nodes map
    # client_nodes = random.sample(list(self.graph.nodes), n_clients)
    node_list = list(self.graph.nodes)
    client_nodes = [node_list[node_N] for node_N in selected_client_nodes]
    for node_id in self.graph.nodes:
      if node_id in client_nodes:
        node = ClientNode(node_id)
        self.clients.append(node)
      else:
        node = StorageNode(node_id)
      self.nodes[node_id] = node
      self.graph.nodes[node_id]["node_obj"] = node
    
    # load data from csv and store in corresponding nodes
    with open("data.csv", "r") as csvFile:
      reader = csv.DictReader(csvFile)
      for row in reader:
        key = row["key"]
        value = row["value"]
        storage_node = int(row["storage_node_id"])

        # we don't want to accidentally make a client node store stuff
        if storage_node in client_nodes:
          continue

        self.nodes[storage_node].storeData(key, value)
        print(f"{storage_node}-> {key}: {self.nodes[storage_node].getData(key)}")
        self.master.registerData(storage_node, key)

    # # store some data randomly
    # for key in range(10): # store 10 data
    #   key = f"A{key}" # easier to distinguish as data key (ie A3)
    #   value = key * 10
    #   storage_node = random.choice([node for node in list(self.graph.nodes) if node not in client_nodes])
    #   # print(storage_node)
    #   self.nodes[storage_node].storeData(key, value)
    #   print(f"{storage_node}-> {key}: {self.nodes[storage_node].getData(key)}")
    #   self.master.registerData(storage_node, key)

  # manually connected isolated nodes
  def connectAllNode(self):
    # get the different connected componets
    components = list(nx.connected_components(self.graph))
    print("components:", components)
    largest_component = components[0] # we will connect everything to the larger component

    # find a random node within each component and join it with the larget component (pick node from each randomly)
    for i in range(1, len(components)):
      isolated_node = list(components[i])[0]
      main_component_node = random.choice(list(largest_component))

      self.graph.add_edge(isolated_node, main_component_node)
      largest_component.add(isolated_node)

  def simulateRequests(self):
    for action in read_actions:
      # client = random.choice(self.clients)
      for _ in range(action[2]):
        client = self.nodes[action[0]]
        assert(client in self.clients)
        key = action[1]
        client.requestData(self.master, self.graph, key, self.total_hops)
    print(f"Total hops: {self.total_hops[0]}")
    pp(self.master.read_access)
    return

  # visualize the network
  # lightblue are the storage nodes
  # red are the client nodes
  def displayTopology(self):
    pos = nx.spring_layout(self.graph)
    node_colors = ["red" if node in [node.node_id for node in self.clients] else "lightblue" for node in self.graph.nodes]
    nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, edge_color="gray")

    plt.show()
    

if __name__ == "__main__":
  n_nodes = 30
  selected_client_nodes = [0, 1, 11, 23]
  write_actions = [(1, "A0", 10)]
  read_actions = [(11, "A1", 2), (23, "A1", 1), (23, "A3", 1)]
  # remember to assert client node in write and read action exists in selected client nodes.
  m = DataReplicationSim(n_nodes, selected_client_nodes, write_actions, read_actions)
  m.simulateRequests()
  m.displayTopology()
