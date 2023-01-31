from sumoexporter import SUMOExporter
from yaramo.edge import Edge
from yaramo.geo_node import DbrefGeoNode
from yaramo.node import Node
from yaramo.topology import Topology

from track_signal_generator.generator import TrackSignalGenerator


def setup() -> Topology:
    node1 = Node()
    node2 = Node()
    switch = Node()
    node3 = Node()

    node1.geo_node = DbrefGeoNode(0, 10)
    node2.geo_node = DbrefGeoNode(0, 20)
    switch.geo_node = DbrefGeoNode(50, 10)
    node3.geo_node = DbrefGeoNode(100, 10)

    edge1 = Edge(node1, switch, length=50)
    edge2 = Edge(node2, switch, length=50)
    edge3 = Edge(switch, node3, length=50)

    node1.set_connection_head(switch)
    node2.set_connection_head(switch)
    switch.set_connection_head(node3)
    #switch.set_connection_right(node2)

    topology = Topology()
    topology.add_node(node1)
    topology.add_node(node2)
    topology.add_node(switch)
    topology.add_node(node3)
    topology.add_edge(edge1)
    topology.add_edge(edge2)
    topology.add_edge(edge3)

    return topology


if __name__ == "__main__":
    topology = setup()

    topology.name = "track-signal-generator"

    TrackSignalGenerator(topology).place_switch_signals()

    sumo_exporter = SUMOExporter(topology)
    sumo_exporter.convert()
    sumo_exporter.write_output()
