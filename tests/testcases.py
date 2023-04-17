from pickle import dump

from yaramo.edge import Edge
from yaramo.geo_node import DbrefGeoNode
from yaramo.node import Node
from yaramo.topology import Topology


def straight_track() -> None:
    node1 = Node()
    node2 = Node()

    edge = Edge(node1, node2, length=10_000)

    node1.set_connection_head_edge(edge)

    topology = Topology()
    topology.add_node(node1)
    topology.add_node(node2)
    topology.add_edge(edge)

    dump(topology, open("topologies/straight_track.pickle", "wb"))


def switch_simple() -> None:
    node1 = Node()
    switch = Node()
    node2 = Node()
    node3 = Node()

    node1.geo_node = DbrefGeoNode(0, 10)
    switch.geo_node = DbrefGeoNode(50, 10)
    node2.geo_node = DbrefGeoNode(100, 10)
    node3.geo_node = DbrefGeoNode(100, 20)

    edge1 = Edge(node1, switch, length=50)
    edge2 = Edge(switch, node2, length=50)
    edge3 = Edge(switch, node3, length=50)

    node1.set_connection_head_edge(edge1)
    switch.set_connection_head_edge(edge2)
    switch.set_connection_left_edge(edge3)

    switch.connected_edges.append(edge1)
    node2.connected_edges.append(edge2)
    node3.connected_edges.append(edge3)

    topology = Topology()
    topology.add_node(node1)
    topology.add_node(switch)
    topology.add_node(node2)
    topology.add_node(node3)
    topology.add_edge(edge1)
    topology.add_edge(edge2)
    topology.add_edge(edge3)

    dump(topology, open("topologies/switch_simple.pickle", "wb"))


if __name__ == "__main__":
    straight_track()
    switch_simple()
