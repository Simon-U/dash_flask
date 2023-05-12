import importlib
import os


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    data_processing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data_processing)
    return data_processing
