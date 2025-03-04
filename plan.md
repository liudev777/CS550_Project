## Current Ideas
To keep the model simple, we will only be concerned with optimizing the replication policy for:
- How many copies of the data exists [1].
- Where to store them [1]. 

We will be measuring the effectiveness of these policy paremeters through performance first. This includes:
- Availability.
- Storage cost.
- Hamming distance / latency.

In the future we might include:
- Load balancing.
- Fault Tolerance.

For the sake of getting a prototype off the ground, we will get a simple implementation to work first, while attempting to maintain a modular system that enables addition of other replication policies as well as performance evaluation metrics.

We will use a centralized application (Master Slave) [1] where the master node keeps track of the up to date global view of data. This will be easier for our purpose since the replication parameters will be located in one place. If this goes well, the implementation can be extended to a decentralized application.

### Sources:
[1] Mokadem, R., Arar, F., & Zegour, D. E. (2024, October 7). Towards using reinforcement learning for scaling and data replication in Cloud Systems. arXiv.org. https://arxiv.org/abs/2410.11862 