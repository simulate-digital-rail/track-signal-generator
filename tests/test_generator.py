from pickle import load

from track_signal_generator.generator import TrackSignalGenerator


def test_straight_track():
    topology = load(open("tests/topologies/straight_track.pickle", "rb"))

    TrackSignalGenerator(topology).place_edge_signals()
    assert len(topology.signals.keys()) == 20


def test_switch_simple():
    topology = load(open("tests/topologies/switch_simple.pickle", "rb"))

    TrackSignalGenerator(topology).place_switch_signals()
    assert len(topology.signals.keys()) == 3


def test_switch_both():
    topology = load(open("tests/topologies/switch_simple.pickle", "rb"))

    tsg = TrackSignalGenerator(topology)
    tsg.place_switch_signals()
    tsg.place_edge_signals()

    assert len(topology.signals.keys()) == 3
