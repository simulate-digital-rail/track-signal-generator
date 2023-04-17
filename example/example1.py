from sumoexporter import SUMOExporter
from yaramo.edge import Edge
from yaramo.geo_node import DbrefGeoNode
from yaramo.node import Node
from yaramo.topology import Topology

from track_signal_generator.generator import TrackSignalGenerator


def setup() -> Topology:
    node1 = Node()
    node2 = Node()

    node1.geo_node = DbrefGeoNode(0, 10)
    node2.geo_node = DbrefGeoNode(1002, 10)

    edge = Edge(node1, node2, length=1002)

    node1.set_connection_head_edge(edge)

    topology = Topology()
    topology.add_node(node1)
    topology.add_node(node2)
    topology.add_edge(edge)

    return topology


if __name__ == "__main__":
    topology = setup()

    topology.name = "track-signal-generator"

    TrackSignalGenerator(topology).place_edge_signals()

    sumo_exporter = SUMOExporter(topology)
    sumo_exporter.convert()
    sumo_exporter.write_output()
