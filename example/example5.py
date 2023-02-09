from sumoexporter import SUMOExporter
from yaramo.edge import Edge
from yaramo.geo_node import DbrefGeoNode
from yaramo.node import Node
from yaramo.topology import Topology

from track_signal_generator.generator import TrackSignalGenerator


def setup() -> Topology:
    node1 = Node()
    node2 = Node()
    node3 = Node()
    node4 = Node()
    node5 = Node()
    node6 = Node()
    node7 = Node()
    switch1 = Node()
    switch2 = Node()
    switch3 = Node()
    switch4 = Node()

    node1.geo_node = DbrefGeoNode(000, 10)
    node2.geo_node = DbrefGeoNode(250, 10)
    node3.geo_node = DbrefGeoNode(250, 20)
    node4.geo_node = DbrefGeoNode(250, 30)
    node5.geo_node = DbrefGeoNode(350, 20)
    node6.geo_node = DbrefGeoNode(75, 10)
    node7.geo_node = DbrefGeoNode(000, 00)
    switch1.geo_node = DbrefGeoNode(50, 10)
    switch2.geo_node = DbrefGeoNode(100, 20)
    switch3.geo_node = DbrefGeoNode(100, 10)
    switch4.geo_node = DbrefGeoNode(300, 20)

    edge1 = Edge(node1, switch1, length=50)
    edge2 = Edge(switch1, node6, length=25)
    edge3 = Edge(node6, switch3, length=25)
    edge4 = Edge(switch1, switch2, length=50)
    edge5 = Edge(switch3, node7, length=100)
    edge6 = Edge(switch3, node2, length=150)
    edge7 = Edge(switch2, node3, length=150)
    edge8 = Edge(switch2, node4, length=150)
    edge9 = Edge(node4, switch4, length=50)
    edge10 = Edge(node3, switch4, length=50)
    edge11 = Edge(switch4, node5, length=50)

    edge4.intermediate_geo_nodes.append(DbrefGeoNode(75, 20))
    edge5.intermediate_geo_nodes.append(DbrefGeoNode(75, 00))
    edge8.intermediate_geo_nodes.append(DbrefGeoNode(125, 30))
    edge9.intermediate_geo_nodes.append(DbrefGeoNode(275, 30))

    switch1.set_connection_head(node6)
    switch1.set_connection_left(switch2)
    node6.connected_nodes.append(switch1)
    switch2.connected_nodes.append(switch1)

    switch2.set_connection_head(node3)
    switch2.set_connection_left(node4)
    node3.connected_nodes.append(switch2)
    node4.connected_nodes.append(switch2)

    switch3.set_connection_head(node6)
    switch3.set_connection_right(node7)
    node6.connected_nodes.append(switch3)
    node7.connected_nodes.append(switch3)

    switch4.set_connection_head(node3)
    switch4.set_connection_right(node4)
    node3.connected_nodes.append(switch4)
    node4.connected_nodes.append(switch4)

    node1.set_connection_head(switch1)
    switch1.connected_nodes.append(node1)

    node7.set_connection_head(switch3)
    node2.set_connection_head(switch3)
    switch3.connected_nodes.append(node2)
    node5.set_connection_head(switch4)
    switch4.connected_nodes.append(node5)

    topology = Topology()
    topology.add_node(node1)
    topology.add_node(node2)
    topology.add_node(node3)
    topology.add_node(node4)
    topology.add_node(node5)
    topology.add_node(node6)
    topology.add_node(node7)
    topology.add_node(switch1)
    topology.add_node(switch2)
    topology.add_node(switch3)
    topology.add_node(switch4)

    topology.add_edge(edge1)
    topology.add_edge(edge2)
    topology.add_edge(edge3)
    topology.add_edge(edge4)
    topology.add_edge(edge5)
    topology.add_edge(edge6)
    topology.add_edge(edge7)
    topology.add_edge(edge8)
    topology.add_edge(edge9)
    topology.add_edge(edge10)
    topology.add_edge(edge11)

    return topology


if __name__ == "__main__":
    topology = setup()

    topology.name = "example5"

    tsg = TrackSignalGenerator(topology)
    tsg.place_switch_signals()
    tsg.place_edge_signals()

    sumo_exporter = SUMOExporter(topology)
    sumo_exporter.convert()
    sumo_exporter.write_output()
