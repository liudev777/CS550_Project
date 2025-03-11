import random
import networkx as nx
import matplotlib.pyplot as plt
from node import StorageNode, Master, ClientNode

class DataReplicationSim:
  def __init__(self, n_nodes = 30, n_clients=3):
    seed = 1 # recreate randomness
    random.seed(seed) 
    self.graph = nx.random_geometric_graph(n_nodes, 0.4, seed=seed) # generate connected graph

    # radom_geometric_graph isn't guarenteed to generate a connected graph, so in the event that it doesn't, we will manually connect them.
    self.connectAllNode()

    self.nodes = {} # map of node Id to the Node object
    self.clients = [] # list of client nodes
    self.master = Master("M")

    # assign random nodes as client and storage node and add it to the self.nodes map
    client_nodes = random.sample(list(self.graph.nodes), n_clients)
    for node_id in self.graph.nodes:
      if node_id in client_nodes:
        node = ClientNode(node_id)
        self.clients.append(node)
      else:
        node = StorageNode(node_id)
      self.nodes[node_id] = node
      self.graph.nodes[node_id]["node_obj"] = node

    # store some data randomly
    for key in range(10): # store 10 data
      key = f"A{key}" # easier to distinguish as data key (ie A3)
      value = key * 10
      storage_node = random.choice([node for node in list(self.graph.nodes) if node not in client_nodes])
      # print(storage_node)
      self.nodes[storage_node].storeData(key, value)
      print(f"{storage_node}-> {key}: {self.nodes[storage_node].getData(key)}")
      self.master.registerData(storage_node, key)

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

  def simulateRequests(self, n_requests=1):
    for _ in range(n_requests):
      client = random.choice(self.clients)
      key = "A1"
      client.requestData(self.master, self.graph, key)

  # visualize the network
  # lightblue are the storage nodes
  # red are the client nodes
  def displayTopology(self):
    pos = nx.spring_layout(self.graph)
    node_colors = ["red" if node in [node.node_id for node in self.clients] else "lightblue" for node in self.graph.nodes]
    nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, edge_color="gray")

    plt.show()
    

if __name__ == "__main__":
  m = DataReplicationSim()
  m.simulateRequests()
  m.displayTopology()
