from pprint import pp
from data_replication_simulation import DataReplicationSim

if __name__ == "__main__":
  # some default parameters that we can change
  data_file = "data2.csv"
  n_nodes = 50
  selected_client_nodes =  [0, 20, 30, 40]
  write_actions = []
  read_actions = [
    (30, "movie:10", 1),
    (20, "movie:15", 1),
    (20, "movie:1000", 100),
    (0, "movie:333", 1)
  ]

  sim = DataReplicationSim(
    data_file=data_file,
    n_nodes=n_nodes,
    selected_client_nodes=selected_client_nodes,
    write_actions=write_actions,
    read_actions=read_actions
  )

  # get store before any changes to the system
  baseline_hop_cost = sim.simulateRequests()
  baseline_state = sim.getState()
  baseline_storage_cost = sim.calculateStorageCost()
  baseline_total_cost = 1.0 * baseline_hop_cost + 0.5 * baseline_storage_cost

  print("\n======== BEFORE REPLICATION ==========")
  print("Total Cost (before):", baseline_total_cost)
  # print("State:")
  # pp(baseline_state)
  print("Normalized Replication Storage Cost:", baseline_storage_cost)
  print("Normalized Hop Cost:", baseline_hop_cost)

  manual_action = {
    # "A1": [2, 5, 7],
    # "A3": [10, 15]
    # "A9": [9]
    # "A2": [20, 28, 14, 15]
    "movie:1000": [14]
  }

  next_state, total_cost = sim.step(manual_action)
  # get score after we manually do some replication
  print("\n======== AFTER MANUAL REPLICATION ==========")
  print("Total Cost (after):", total_cost)
  # print("State:")
  # pp(next_state)
  print("Normalized Replication Storage Cost:", sim.calculateStorageCost())
  print("Normalized Hop Cost:", sim.simulateRequests())

  sim.displayTopology()
