from yaramo.signal import (
    Signal,
    SignalKind,
    SignalDirection,
    SignalFunction,
)
from yaramo.topology import Topology
from yaramo.edge import Edge

DISTANCE_BEETWEEN_TRACK_SIGNALS = 500

class TrackSignalGenerator:
    """
        Generates track-signals ("Blocksignale") for the given topology by walking
        the edges and placing signals every `DISTANCE_BEETWEEN_TRACK_SIGNALS`m apart.
        Additionally, signals around switches are placed.
    """

    def __init__(self, topology: Topology):
        self.topology = topology

    def _place_signals_for_switch(self, node):
        pass

    def _place_signals_on_edge(self, edge: Edge):
        for km in range(0, int(edge.length), DISTANCE_BEETWEEN_TRACK_SIGNALS):
            self._place_signal_on_edge(edge, km)

    def _place_signal_on_edge(self, edge: Edge, signal_km=0):
        signal = Signal(
            edge,
            signal_km,
            SignalDirection.IN,
            SignalFunction.Block_Signal,
            SignalKind.Hauptsignal,
        )
        self.topology.add_signal(signal)

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
