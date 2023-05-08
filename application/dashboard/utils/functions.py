import os


def get_tab_names():
    excel_files = os.path.join(os.getcwd(), "application/data")
    list = os.listdir(excel_files)
    files = [f.split(".")[0] for f in list if os.path.isfile(excel_files + "/" + f)]
    return files
