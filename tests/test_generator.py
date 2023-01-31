from yaramo.topology import Topology
from yaramo.node import Node
from yaramo.edge import Edge

from track_signal_generator.generator import TrackSignalGenerator

def setup() -> Topology:
    node1 = Node()
    node2 = Node()

    edge = Edge(node1, node2, length = 10_000)

    node1.set_connection_head(node2)

    topology = Topology()
    topology.add_node(node1)
    topology.add_node(node2)
    topology.add_edge(edge)

    return topology

def test_straight_track():
    topology = setup()

    TrackSignalGenerator(topology).place_edge_signals()
    assert len(topology.signals.keys()) == 20