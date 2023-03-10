"""
A generator for yaramo which generates missing track signals ("Blocksignale")
on edges and around switches.
"""

from yaramo.edge import Edge
from yaramo.node import Node
from yaramo.signal import Signal, SignalDirection, SignalFunction, SignalKind
from yaramo.topology import Topology

DISTANCE_BEETWEEN_TRACK_SIGNALS = 500
DISTANCE_TO_SWITCH = 10


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
        for edge in self.topology.edges.values():
            # We found our incomming edge
            if edge.node_b == node:
                self._place_signal_on_edge(edge, edge.length - DISTANCE_TO_SWITCH)

            # We found the outgoing edge
            if edge.node_a == node:
                self._place_signal_on_edge(
                    edge, DISTANCE_TO_SWITCH, direction=SignalDirection.GEGEN
                )

    def _place_signals_on_edge(self, edge: Edge):
        first_signal = (
            1 if not edge.node_a.is_switch() else DISTANCE_BEETWEEN_TRACK_SIGNALS
        )
        for track_meter in range(
            first_signal, int(edge.length), DISTANCE_BEETWEEN_TRACK_SIGNALS
        ):  # we start at 1 as otherwise sumo gets confused and adds a steep turn
            self._place_signal_on_edge(edge, track_meter)

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
