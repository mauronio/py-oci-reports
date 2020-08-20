import oci_utils
import spreadsheet_utils
import os
import yaml
import report_builder

DEFAULT_WORK_PATH = os.path.join(os.path.dirname(__file__), 'workspace')
CONFIG_FILE_NAME = 'config.yaml'

def get_writers(working_path, config):

    writers = []

    for writer_name in config['writers']:

        if writer_name == 'spreadsheet':
            writers.append(spreadsheet_utils.SpreadSheetWriter(working_path, config))

    return writers

def close_writers(writers):

    for writer in writers:
        writer.close()


def get_config(working_path):

    config = None

    with open(os.path.join(working_path, CONFIG_FILE_NAME), 'r') as f:
        config = yaml.safe_load(f)

    return config

def process(base_path = DEFAULT_WORK_PATH):

    oci_client = oci_utils.OCIClient()

    config = get_config(base_path)
    writers = get_writers(base_path, config)

    for report_data in config['reports']:
        report_builder.process_compartment_tree(report_data, oci_client, writers)
        report_builder.process_vcn(report_data, oci_client, writers)

    close_writers(writers)

if __name__ == '__main__':

    process()