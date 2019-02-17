import json


class Fast5:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath

class Read:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        
        filename = ""
        read_id = ""
        run_id = ""
        channel = ""
        start_time = ""
        duration = ""
        num_events = ""
        passes_filtering = ""
        template_start = ""
        num_events_template = ""
        template_duration = ""
        num_called_template = ""
        sequence_length_template = ""
        mean_qscore_template = ""
        strand_score_template = ""
        calibration_strand_genome_template = ""
        calibration_strand_identity_template = ""
        calibration_strand_accuracy_template = ""
        calibration_strand_speed_bps_template = ""
        barcode_arrangement = ""
        barcode_score = ""