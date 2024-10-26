from .scylla import Scylla
from cassandra.cluster import Cluster


class Cassandra(Scylla):
    def __init__(self):
        self.cluster = Cluster(['0.0.0.0'], port=9042)
        self.session = self.cluster.connect()
