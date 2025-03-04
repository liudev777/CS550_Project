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
- Latency.

"Performance objective such as response time [13], generally is not included and guaranteed in providers Service Level Agreements (SLAs) due to the heterogeneous workloads in cloud systems. Performance objective can conflict with the goal of maximizing economic benefits while minimizing operating costs [8]. Only few replication strategies include performance objectives" - [1]

For the sake of getting a prototype off the ground, we will get a simple implementation to work first, while attempting to maintain a modular system that enables addition of other replication policies as well as performance evaluation metrics.

We will use a centralized application (Master Slave) [1] where the master node keeps track of the up to date global view of data. This will be easier for our purpose since the replication parameters will be located in one place.

### Sources:
[1] Mokadem, R., Arar, F., & Zegour, D. E. (2024, October 7). Towards using reinforcement learning for scaling and data replication in Cloud Systems. arXiv.org. https://arxiv.org/abs/2410.11862 