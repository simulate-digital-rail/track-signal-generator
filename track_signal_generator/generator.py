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


class TrackSignalGenerator:
    """
    Generates track-signals ("Blocksignale") for the given topology by walking
    the edges and placing signals every `DISTANCE_BEETWEEN_TRACK_SIGNALS`m apart.
    Additionally, signals around switches are placed.
    """

    def __init__(self, topology: Topology):
        self.topology = topology

    def _place_signals_for_switch(self, node: Node):
        for edge in self.topology.edges:
            # We found our incomming edge
            if edge.node_b == node:
                self._place_signal_on_edge(edge, edge.length - DISTANCE_TO_SWITCH)

    def _place_signals_on_edge(self, edge: Edge):
        for track_meter in range(
            1, int(edge.length), DISTANCE_BEETWEEN_TRACK_SIGNALS
        ):  # we start at 1 as otherwise sumo gets confused and adds a steep turn
            self._place_signal_on_edge(edge, track_meter)

    def _place_signal_on_edge(self, edge: Edge, signal_km=0):
        signal = Signal(
            edge,
            signal_km,
            SignalDirection.IN,
            SignalFunction.Block_Signal,
            SignalKind.Hauptsignal,
        )
        signal.name = f"km-{signal_km}"
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
