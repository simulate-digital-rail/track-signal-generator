from planpro_importer.reader import PlanProReader
from sumoexporter import SUMOExporter

from track_signal_generator.generator import TrackSignalGenerator

if __name__ == "__main__":
    topology = PlanProReader("lausitz simple.ppxml").read_topology_from_plan_pro_file()
    topology.name = "lausitz-simple"

    # topology.name = "track-signal-generator"
    TrackSignalGenerator(topology).place_edge_signals()

    sumo_exporter = SUMOExporter(topology)
    sumo_exporter.convert()
    sumo_exporter.write_output()
