import pickle
from os import path


def read_in_file(file, file_path):
    if path.isfile(path.join(file_path, file)):
        pickle_off = open(path.join(file_path, file), "rb")
        return_dict = pickle.load(pickle_off)
        pickle_off.close()
        return return_dict
    else:
        return {}


def save_out_file(dict_to_save, file, file_path):
    with open(path.join(file_path, file), 'wb') as fh:
        pickle.dump(dict_to_save, fh)
    fh.close()
