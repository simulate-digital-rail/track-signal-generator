"""
A generator for yaramo which generates missing track signals ("Blocksignale")
on edges and around switches.
"""

from yaramo.edge import Edge
from yaramo.node import Node
from yaramo.signal import Signal, SignalDirection, SignalFunction, SignalKind
from yaramo.topology import Topology

DISTANCE_BEETWEEN_TRACK_SIGNALS = 1000
DISTANCE_TO_SWITCH = 25
DISTANCE_BETWEEN_SWITCHES = 100


def workaround(self) -> bool:
    """
    Returns true if this node is a switch.
    A switch is defined as a `Node` with a 2 connected tracks
    """
    return len(self.connected_nodes) >= 3


Node.is_switch = workaround


class TrackSignalGenerator:
    """
    Generates track-signals ("Blocksignale") for the given topology by walking
    the edges and placing signals every `DISTANCE_BEETWEEN_TRACK_SIGNALS`m apart.
    Additionally, signals around switches are placed.
    """

    def __init__(self, topology: Topology):
        self.topology = topology

    def _place_signals_for_switch(self, node: Node):
        for connected_node in node.connected_nodes:
            edge = self.topology.get_edge_by_nodes(node, connected_node)

            # We found our incomming edge
            if edge.node_b == node:
                # don't place signals between switches
                if (
                    not (
                        edge.node_a.is_switch()
                        and edge.length < DISTANCE_BETWEEN_SWITCHES
                    )
                    and edge.length - DISTANCE_TO_SWITCH > 0
                ):
                    self._place_signal_on_edge(edge, edge.length - DISTANCE_TO_SWITCH)

            # We found a outgoing edge
            if edge.node_a == node:
                # don't place signals between switches
                if (
                    not (
                        edge.node_b.is_switch()
                        and edge.length < DISTANCE_BETWEEN_SWITCHES
                    )
                    and edge.length > DISTANCE_TO_SWITCH
                ):
                    self._place_signal_on_edge(
                        edge, DISTANCE_TO_SWITCH, direction=SignalDirection.GEGEN
                    )

    def _calculate_distance_from_start(self, node: Node, edge: Edge) -> int:
        if node.is_switch():
            return DISTANCE_BEETWEEN_TRACK_SIGNALS
        if len(node.connected_nodes) == 2:  # "straight" track
            previous_node = next(
                filter(lambda x: edge.get_other_node(node) != x, node.connected_nodes)
            )  # we can do this because we have only two connected nodes
            previous_edge = self.topology.get_edge_by_nodes(previous_node, node)

            if previous_edge and len(previous_edge.signals) > 0:
                direction = previous_edge.get_direction_based_on_nodes(
                    previous_node, node
                )

                last_signals = previous_edge.get_signals_with_direction_in_order(
                    direction
                )

                if len(last_signals) == 0:
                    return 1

                last_signal = last_signals[-1]

                if direction == SignalDirection.IN:
                    distance_from_node = (
                        previous_edge.length - last_signal.distance_edge
                    )
                else:
                    distance_from_node = last_signal.distance_edge

                return DISTANCE_BEETWEEN_TRACK_SIGNALS - distance_from_node
        return 1

    def _place_signals_on_edge(self, edge: Edge):
        first_signal = self._calculate_distance_from_start(edge.node_a, edge)
        last_signal = (
            int(edge.length)
            if not edge.node_b.is_switch()
            else int(edge.length) - DISTANCE_BEETWEEN_TRACK_SIGNALS
        )
        for track_meter in range(
            first_signal, last_signal, DISTANCE_BEETWEEN_TRACK_SIGNALS
        ):  # we start at 1 as otherwise sumo gets confused and adds a steep turn
            self._place_two_way_signal_on_ege(edge, track_meter)

    def _place_two_way_signal_on_ege(self, edge: Edge, signal_km=0) -> None:
        self._place_signal_on_edge(edge, signal_km)
        self._place_signal_on_edge(edge, signal_km, direction=SignalDirection.GEGEN)
    

    def _place_signal_on_edge(
        self, edge: Edge, signal_km=0, direction=SignalDirection.IN
    ):
        signal = Signal(
            edge,
            signal_km,
            direction,
            SignalFunction.Block_Signal,
            SignalKind.Hauptsignal,
        )
        signal.name = f"{edge.uuid}-km-{signal_km}"
        self.topology.add_signal(signal)
        edge.signals.append(signal)

    def place_edge_signals(self):
        """
        Performs the signal placement along the edges
        """
        edges = self.topology.edges

        for edge in edges.values():  # We don't care about the edge-identifiers
            self._place_signals_on_edge(edge)

    def place_switch_signals(self):
        """
        Performs the signal placement around switches
        """
        nodes = self.topology.nodes

        for node in filter(lambda node: node.is_switch(), nodes.values()):
            self._place_signals_for_switch(node)
