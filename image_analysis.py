import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def show_directories(path):
    a = "a"


def get_data(path):
    subjects = os.listdir(path)
    all_data = {}

    for subject in subjects:
        overviews = os.listdir(path + "\\" + subject)
        all_data.update({subject: {}})

        for overview in overviews:
            tiles = os.listdir(path + "\\" + subject + "\\" + overview)
            all_data[subject].update({overview: {}})

            for tile in tiles:
                files = os.listdir(path + "\\" + subject + "\\" + overview + "\\" + tile)
                all_data[subject][overview].update({tile: {}})

                for file in files:
                    # Convex Hull Volume
                    if file.find("Volume.csv") >= 0 and file.find("Spine") < 0 and file.find("Soma") < 0 and file.find("Segment") < 0 and file.find("Filament") < 0:
                        print(file)
                        convex_hull_vol_frame = {"Convex Hull Volume": [], "Units": []}
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            convex_hull_vol_frame["Convex Hull Volume"] += [df["Volume"][x]]
                            convex_hull_vol_frame["Units"] += [df["Unit"][x]]

                        all_data[subject][overview][tile].update({"Convex Hull Volume": convex_hull_vol_frame})

                    # Soma Volume
                    elif file.find("Soma_Volume.csv") >= 0:
                        print(file)
                        soma_vol_frame = {"Soma Volume": [], "Units": []}
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            soma_vol_frame["Soma Volume"] += [df["Soma Volume"][x]]
                            soma_vol_frame["Units"] += [df["Unit"][x]]

                        all_data[subject][overview][tile].update({"Soma Volume": soma_vol_frame})

                    # Convex Hull Area
                    elif file.find("Area.csv") >= 0 and file.find("Spine") < 0 and file.find("Soma") < 0 and file.find("Segment") < 0 and file.find("Filament") < 0:
                        print(file)
                        convex_hull_area_frame = {"Convex Hull Area": [], "Units": []}
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            convex_hull_area_frame["Convex Hull Area"] += [df["Area"][x]]
                            convex_hull_area_frame["Units"] += [df["Unit"][x]]

                        all_data[subject][overview][tile].update({"Convex Hull Area": convex_hull_area_frame})

                    # Filament Segment Length
                    elif file.find("Filament_Segment_Length_(sum).csv") >= 0:
                        print(file)
                        filament_seg_len_frame = {"Filament Segment Length": [], "Units": []}
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file,
                                         skiprows=3, header=0)
                        for x in df.index:
                            filament_seg_len_frame["Filament Segment Length"] += [df["Filament Segment Length (sum)"][x]]
                            filament_seg_len_frame["Units"] += [df["Unit"][x]]

                        all_data[subject][overview][tile].update({"Filament Segment Length": filament_seg_len_frame})

                    # Filament Segment Length
                    elif file.find("neuron contact volume_Detailed") >= 0:
                        print(file)
                        neuron_contact_vol_frame = {"Neuron Contact Volume": [], "Units": []}
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file,
                                         skiprows=3, header=0)
                        for x in df.index:
                            neuron_contact_vol_frame["Neuron Contact Volume"] += [df["Volume"][x]]
                            neuron_contact_vol_frame["Units"] += [df["Unit"][x]]

                        all_data[subject][overview][tile].update({"Neuron Contact Volume": neuron_contact_vol_frame})

    new_dict = {}
    for outer_outer_key, outer_dict in all_data.items():
        for outer_key, inner_dict in outer_dict.items():
            for inner_key, values in inner_dict.items():
                new_dict[(outer_outer_key, outer_key, inner_key)] = values

    new_dict = pd.DataFrame(new_dict)
    new_dict = new_dict.transpose()

    with pd.ExcelWriter("Image Analysis Data.xlsx") as writer:
        new_dict.to_excel(writer, "Image Analysis Data.xlsx")

    a = ""
    return a


# C:\Users\Luke\Desktop\College\Research\Dr. Franklin\Image Analysis Pipeline\Data
data_path = input("Input the path of the folder containing the image analysis files you would like to compute stats for: ")
get_data(data_path)