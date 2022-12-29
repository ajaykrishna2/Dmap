from cassandra.cluster import Cluster
clstr=Cluster()
session=clstr.connect()
session.execute("create keyspace mykeyspace with replication={'class': 'SimpleStrategy', 'replication_factor' : 1};")


