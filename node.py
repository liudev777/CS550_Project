from collections import defaultdict
from access import Access
import networkx as nx

"""
Node classes for data replication

- Master
- StorageNode
- ClientNode
"""

class Node:
  def __init__(self, node_id):
    self.node_id = node_id
  
  def __repr__(self):
    return f"<Type: Unassigned type | Node ID: {self.node_id}>"

class Master(Node):
  def __init__(self, node_id):
    super().__init__(node_id)
    self.data_locations = defaultdict(set)
    self.read_access = {}
  
  def updateAccess(self, key, client_id):
    if (key in self.read_access):
      self.read_access[key].updateAccessCount(client_id)

  def registerData(self, node_id, key):
    self.data_locations[key].add(node_id)
    self.read_access[key] = Access()

  def findClosestReplica(self, graph, source_node, key):
    if key not in self.data_locations:
      return None
    
    candidate_nodes = self.data_locations[key]
    shortest_path = float('inf')
    closest_node = None

    for node in candidate_nodes:
      try:
        path_length = nx.shortest_path_length(graph, source=source_node, target=node)
        if path_length < shortest_path:
          shortest_path = path_length
          closest_node = node
      except:
        continue
    
    return closest_node, shortest_path

  def __repr__(self):
    return f"<Type: Master | Node ID: {self.node_id}>"

class StorageNode(Node):
  def __init__(self, node_id):
    super().__init__(node_id)
    self.stored_data = {}

  def storeData(self, key, value):
    self.stored_data[key] = value
  
  def getData(self, key):
    return self.stored_data[key]
  
  def hasData(self, key):
    return key in self.stored_data
  
  def __repr__(self):
    return f"<Type: Slave | Node ID: {self.node_id}>"

class ClientNode(Node):
  def __init__(self, node_id):
    super().__init__(node_id)

  def requestData(self, master, graph, key, total_hops):
    response = master.findClosestReplica(graph, self.node_id, key)

    if response is not None:
      closest_replica, hops = response
      print(f"Client {self.node_id} retrieves data {key} from Node {closest_replica} in {hops} hops.")
      total_hops[0] += hops
      master.updateAccess(key, self.node_id)
    else:
      print(f"Client {self.node_id} requested Data {key}, but it is unavailable.")
  
  def __repr__(self):
    return f"<Type: Client | Node ID: {self.node_id}>"