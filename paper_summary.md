# Summaries

## HReplica: A Dynamic Data Replication Engine with Adaptive Compression for Multi-Tiered Storage
### Notes: A paper that looks at advanced application of data replication. Follow reference to learn more about data replication.
- Data replication helps solve conflicting big data application requirements by introducing low latency, read availability, durability etc.
- HReplica makes use of data compression and heirarchical storage to improve data replication.
- Data Replication: 
  - Purpose: decrease user waiting time by creating multiple copies of data and distributing them to different locations. 

- Works talking about data replication: 
20 21 22 23 24 25 26 27

## DATA REPLICATION STRATEGIES IN WIDE AREA DISTRIBUTED SYSTEMS 
http://jarrett.cis.unimelb.edu.au/papers/DataReplicationInDSChapter2006.pdf 
### Notes: Different replication protocols are suitable for different application. Paper covers distrubuted database management systems, service-oriented data grids, p2p systems, and storage area networks.
- Data sharing applications has scaled to patabytes of data per year. Sharing of data in distributed env raises many design issues like access permissions, consistency, security. 
- Replication helps increase availability, increase performance, and enhance reliability.
- At the expense of overhead of creating, maintaining and updating replicas.
- Replicas work best if the data is read only. (Usually isn't)
  - If replica needs to write, the benefits of replication is negated to some extent (overhead of maintaining consistency).
- Replication Protocols:
  - ROWA (Read One Write All): Read can happen at any replica, but updates must be applied to all replicas.
  - ROWA-Available: A variant that tried to write to all available replicas. Downside is if some replicas are down, it will be outdated.
  - Quorum-based protocols: A quorum is a non-negative vote. Each replica is assigned a quorum.
    - Q = total num of votes (num of sites in replicated system)
    - Q_R and Q_W = read and write quorums.
    1. Q_R + Q_W > Q and
    2. Q_W + Q_W > Q.
    - Basically, ensures that as long as the set of replicas you write to intersects with the set of replicas you read from, you will always get the most up to date value without having to update every single replica.

- Types of Replication Protocols:
  - Sync (Eager) Async (Lazy)
    - sync: all replicas are updated before a transaction completes (strong consistency, slower writes).
    - async: update one site first, then propagate changes later (faster write, but some replicas may be outdated).
  - Group (update anywhere) vs Master (primary copy)
    - Group: any replica can receive updates but must be synced everywhere.
    - Master: Only one designate site handles update, other handle reads. 
  
- Commit protocol in Distributed DBMS (2PC):
  - Standard method to make sure either all replica commit a transaction or all rolls back consistently.
  - Phase 1: collect yes or no vote from participants. (Even one no prompts a rollback)
  - Phase 2: send a global commit or abort based on phase 1.

- Storage Area Network (SAN):
  - High speed network that interconnects storage devices. Centralizes data managing (compared to direct attached storage where each server has its own dedicated storage device)


