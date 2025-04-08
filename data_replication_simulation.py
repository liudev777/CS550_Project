from pprint import pp
import random
import networkx as nx
import matplotlib.pyplot as plt
import csv
from node import StorageNode, Master, ClientNode

class DataReplicationSim:
  def __init__(self, data_file, n_nodes=30, selected_client_nodes=[], write_actions=
  [], read_actions=[]):
    self.data_file = data_file
    seed = 10 # recreate randomness
    random.seed(seed) 
    self.graph = nx.random_geometric_graph(n_nodes, 0.1, seed=seed) # generate connected graph
    self.MAX_REPLICAS = 5

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
    with open(self.data_file, "r") as csvFile:
      reader = csv.DictReader(csvFile)
      for row in reader:
        key = row["key"]
        value = row["value"]
        storage_node = int(row["storage_node_id"])

        # we don't want to accidentally make a client node store stuff
        if storage_node in client_nodes:
          continue

        self.nodes[storage_node].storeData(key, value)
        # print(f"{storage_node}-> {key}")
        self.master.registerData(storage_node, key)

  # manually connected isolated nodes
  def connectAllNode(self):
    # get the different connected componets
    components = list(nx.connected_components(self.graph))
    # print("components:", components)
    largest_component = components[0] # we will connect everything to the larger component

    # find a random node within each component and join it with the larget component (pick node from each randomly)
    for i in range(1, len(components)):
      isolated_node = list(components[i])[0]
      main_component_node = random.choice(list(largest_component))

      self.graph.add_edge(isolated_node, main_component_node)
      largest_component.add(isolated_node)

  def simulateRequests(self):
    self.total_hops[0] = 0
    total_requests = 0

    for action in self.read_actions:
      key = action[2]
      for _ in range(key):
        client = self.nodes[action[0]]
        assert(client in self.clients)
        key = action[1]
        client.requestData(self.master, self.graph, key, self.total_hops)
        total_requests += 1

    # print(f"Total hops: {self.total_hops[0]}")
    # pp(self.master.read_access)

    avg_hops = self.total_hops[0] / total_requests if total_requests > 0 else float('inf')
    max_hops = nx.diameter(self.graph)
    normalized_hops = avg_hops / max_hops

    # print(f"Max hops: {max_hops} | normalized_hops: {normalized_hops}")
    return normalized_hops

  # visualize the network
  # lightblue are the storage nodes
  # red are the client nodes
  def displayTopology(self):
    pos = nx.spring_layout(self.graph)
    node_colors = ["red" if node in [node.node_id for node in self.clients] else "lightblue" for node in self.graph.nodes]
    nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, edge_color="gray")

    plt.show()

  # takes actions from RL model and applys it to network
  def applyPolicy(self, action): # action looks something like {"A1": [3, 5], "A2": [7]}
    for key, replica_nodes in action.items():
      original_nodes = self.master.data_locations.get(key, [])
      if not original_nodes:
        continue

      source_node = list(original_nodes)[0] # grab first instance of a node to get the value
      value = self.nodes[source_node].getData(key)

      for node_id in replica_nodes:
        if node_id not in self.nodes:
          continue
        if not self.nodes[node_id].hasData(key):
          self.nodes[node_id].storeData(key, value)
          self.master.registerData(node_id, key)

  def calculateStorageCost(self):
    total_replicas = 0
    max_storage = self.MAX_REPLICAS * (len(self.nodes) - len(self.clients))
    for node_ids in self.master.data_locations.values():
      total_replicas += len(node_ids)
    return total_replicas / max_storage

  def getState(self):
    adj = nx.to_numpy_array(self.graph)
    data_locations = {k: list(v) for k, v in self.master.data_locations.items()}
    access_freq = {k: self.master.read_access[k].total_accesses for k in self.master.read_access}
    return {
      "adjacency": adj,
      "data_locations": data_locations,
      "access_frequency": access_freq,
      "clients": [c.node_id for c in self.clients]
    }

  def step(self, action):
    self.applyPolicy(action)
    hop_cost = self.simulateRequests()
    storage_cost = self.calculateStorageCost()
    total_cost = 1.0 * hop_cost + 0.5 * storage_cost

    next_state = self.getState()
    return next_state, total_cost


if __name__ == "__main__":
  n_nodes = 50
  selected_client_nodes = [0, 20, 30, 40]
  write_actions = []
  # read_actions = [(11, "A1", 2), (23, "A1", 1), (23, "A3", 1)]
  read_actions = [
    (30, "movie:10", 1),
    (20, "movie:15", 1),
    (20, "movie:1000", 1),
    (0, "movie:333", 1)
  ]
  # remember to assert client node in write and read action exists in selected client nodes.
  m = DataReplicationSim("data2.csv", n_nodes, selected_client_nodes, write_actions, read_actions)
  m.simulateRequests()
  m.displayTopology()
