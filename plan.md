## Current Ideas
To keep the model simple, we will only be concerned with optimizing the replication policy for:
- How many copies of the data exists [1].
- Where to store them [1]. 
- Decreasing hop distance

We will be measuring the effectiveness of these policy paremeters through performance first. This includes:
- Availability.
- Storage cost.
- Hamming distance / latency.

In the future we might include:
- Load balancing.
- Fault Tolerance.

For the sake of getting a prototype off the ground, we will get a simple implementation to work first, while attempting to maintain a modular system that enables addition of other replication policies as well as performance evaluation metrics.

We will use a centralized application (Master Slave) [1] where the master node keeps track of the up to date global view of data. This will be easier for our purpose since the replication parameters will be located in one place. If this goes well, the implementation can be extended to a decentralized application.

- Master node will provide lookup of where data is stored in other nodes.
- Client asks master where data x is and master node replies with node y.
- Client goes directly to node y to get data.

- Pull data from DB (CSV for now) and randomly assign it across nodes for initialization. 
- Each node can have more than 1 data item (maybe impose storage limit). 
- Each data item will mark one node as a primary node, which will replicate its data to other node. [2] *we will use the client server model in the paper. Note that the naming kind of conflicts with our naming. The server in the paper will be our primary node, and the client will be the replication nodes.
- In the even a primary node is down, the system will reassign that label to a replica. 
- All writes will go to the primary node. This is so we just have to implement a lock on the primary node during write and send out updates as a single source of truth, instead of having to reconcile differences as different nodes propagate.

### Might consider:
- Client-side caching for recently looked up node so it doesn't go through master again.
- Regional master in the scenario the master node is far away.

### Cost metric:
- We want to target availability (ability to r/w in the event of node failures), storage cost (number of replicas), and hop distance. 
- Increased availability decreases storage cost.
- We need the total cost that we want to min to be in the form of 
 
  T_Cost = (w1 * (1/availabilityCost)?) + (w2 * storageCost) + (w3 * hopDistanceCost)

* look into separating cost into a maximizing cost and minimizing cost for RL
- // availabilityCost = *
- storageCost = total_replicas / max_storage
- hopDistanceCost = avg(networkDistance(client, replica))/ max_possible_hop *just read cost for now. We may need to implement write cost to all replicas later.

### Factor influences:
// Availability:
- Increased replication factor.
- Fast recovery in the event of node failure.

Storage Cost:
- Decreased replication factor.
- Adjust replication based on data popularity (access freq).

Hop Distance:
- Replication placement in proximity to client that is accessing.

### input:
- Client placement -> input as a list of node IDs that we want designated as a client node. This influence where and how many clients. *maybe not
- Write Freq -> input as a list of tuple in the format [("data1", "client1", 10)] for writing 10 times to data1 from client1.
- Read Freq -> input as a list of tuple in the same format as write freq above.

- Overall node generation is randomized for now.

### simulated conditions:
- Random node failures to influence availability
- Shifting client distribution to influence where data is stored and influence hop distance
- 

output should work for any general graph.

### output:
- how many repl and where in relation to data and client
- output score that this generation produces

### Sources:
[1] Mokadem, R., Arar, F., & Zegour, D. E. (2024, October 7). Towards using reinforcement learning for scaling and data replication in Cloud Systems. arXiv.org. https://arxiv.org/abs/2410.11862 

[2] https://crystal.uta.edu/~kumar/cse6306/papers/Smita_RepDFS.pdf 