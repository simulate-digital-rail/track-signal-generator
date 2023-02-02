from track_signal_generator.generator import TrackSignalGenerator

from pickle import load


def test_straight_track():
    topology = load(open("tests/topologies/straight_track.pickle", "rb"))

    TrackSignalGenerator(topology).place_edge_signals()
    assert len(topology.signals.keys()) == 20


def test_switch_simple():
    topology = load(open("tests/topologies/switch_simple.pickle", "rb"))

    TrackSignalGenerator(topology).place_switch_signals()
    assert len(topology.signals.keys()) == 3
