import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import scipy.stats as stats
import math


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
                        convex_hull_vol = []
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            convex_hull_vol += [df["Volume"][x]]

                        all_data[subject][overview][tile].update({"Convex Hull Volume (" + df["Unit"][0] + ")": convex_hull_vol})

                    # Soma Volume
                    elif file.find("Soma_Volume.csv") >= 0:
                        print(file)
                        soma_vol = []
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            soma_vol += [df["Soma Volume"][x]]

                        all_data[subject][overview][tile].update({"Soma Volume (" + df["Unit"][0] + ")": soma_vol})

                    # Convex Hull Area
                    elif file.find("Area.csv") >= 0 and file.find("Spine") < 0 and file.find("Soma") < 0 and file.find("Segment") < 0 and file.find("Filament") < 0:
                        print(file)
                        convex_hull_area = []
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            convex_hull_area += [df["Area"][x]]

                        all_data[subject][overview][tile].update({"Convex Hull Area (" + df["Unit"][0] + ")": convex_hull_area})

                    # Filament Segment Length
                    elif file.find("Filament_Segment_Length_(sum).csv") >= 0:
                        print(file)
                        filament_seg_len = []
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            filament_seg_len += [df["Filament Segment Length (sum)"][x]]

                        all_data[subject][overview][tile].update({"Filament Segment Length (" + df["Unit"][0] + ")": filament_seg_len})

                    # Filament Segment Length
                    elif file.find("neuron contact volume_Detailed") >= 0:
                        print(file)
                        neuron_contact_vol = []
                        df = pd.read_csv(path + "\\" + subject + "\\" + overview + "\\" + tile + "\\" + file, skiprows=3, header=0)
                        for x in df.index:
                            neuron_contact_vol += [df["Volume"][x]]

                        all_data[subject][overview][tile].update({"Neuron Contact Volume (" + df["Unit"][0] + ")": neuron_contact_vol})

    new_dict = {}
    for outer_outer_key, outer_dict in all_data.items():
        for outer_key, inner_dict in outer_dict.items():
            for inner_key, values in inner_dict.items():
                new_dict[(outer_outer_key, outer_key, inner_key)] = values

    new_dict = pd.DataFrame(new_dict)
    new_dict = new_dict.transpose()

    with pd.ExcelWriter("Image Analysis Data.xlsx") as writer:
        new_dict.to_excel(writer, "Image Analysis Data.xlsx")

    return all_data


def create_violin(group_1, group_2, comparison, parameter, p):
    # group_1 = map(float, group_1)
    # group_2 = map(float, group_2)

    name_1 = comparison.split(" v. ")[0]
    name_2 = comparison.split(" v. ")[1]
    data = {name_1: group_1, name_2: group_2}
    while len(data[name_1]) > len(data[name_2]):
        data[name_2] += [np.nan]
    while len(data[name_2]) > len(data[name_1]):
        data[name_1] += [np.nan]

    data = pd.DataFrame(data)

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.15)

    # Set seaborn palette
    sns.set_palette("Set2", 80)

    # Create violins
    sns.violinplot(data, fill=False, linewidth=1.5, linecolor="k", palette=sns.color_palette()[4:], inner_kws=dict(box_width=15, whis_width=2), ax=ax)

    # Format axis labels
    ax.set_title(comparison, fontsize=16)
    ax.set_ylabel(parameter, fontsize=16)
    ax.set_xlabel("Group", fontsize=16)
    ax.set_ylim(0)

    # Format figure outline
    ax.spines["bottom"].set_linewidth(1)
    ax.spines["top"].set_linewidth(1)
    ax.spines["left"].set_linewidth(1)
    ax.spines["right"].set_linewidth(1)

    # Add significance
    p_text = "N/A"
    if 0.01 <= p < 0.05:
        p_text = "* p = " + str(round_to_n(p, 3))
    elif 0.001 <= p < 0.01:
        p_text = "** p = " + str(round_to_n(p, 3))
    elif p < 0.001:
        p_text = "*** p = " + str(round_to_n(p, 3))
    else:
        p_text = "p = " + str(round_to_n(p, 3))
    plt.text(0.5, 0.9, p_text, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    plt.savefig("Figures" + "\\" + comparison + " " + parameter + " Violin Plot.jpg")
    plt.show()


def compare_groups(group_1, group_2):
    t, p = stats.ttest_ind(group_1, group_2)
    print(p)
    return p


def access_data(group, parameter, all_data):
    data = []
    for subject in group:
        for overview in all_data[subject]:
            for tile in all_data[subject][overview]:
                for param in all_data[subject][overview][tile]:
                    if param.split(" (")[0] == parameter:
                        if all_data[subject][overview][tile][param]:
                            data += all_data[subject][overview][tile][param]

    return data


def select_groups(all_data, test=False):
    group_key = {"Male Control No Stim": ["BAH1"],
                 "Female Control No Stim": ["EAR1", "EAR2", "EAR3", "EAR5", "EAR6", "EAR7"],
                 "Male Control 10Hz": ["BEA1", "BEA4"],
                 "Female Control 40Hz": ["A1", "A2", "A4", "A5", "A8"],
                 "Male Stress No Stim": ["FALAK1", "FALAK2", "FALAK4", "FALAK5"],
                 "Female Stress No Stim": ["R2", "R3", "R5", "R6"],
                 "Male Stress 10Hz": ["LEV1", "LEV4", "LEV5", "LEV6"],
                 "Female Stress 40Hz": ["KAJ1", "KAJ4", "KAJ5", "KAJ6", "KAJ7", "KAJ8"]}

    print("GROUP KEY:\n"
          "Male Control No Stim\n"
          "Female Control No Stim\n"
          "\n"
          "Male Control 10Hz\n"
          "Female Control 40\n"
          "\n"
          "Male Stress No Stim\n"
          "Female Stress No Stim\n"
          "\n"
          "Male Stress 10Hz\n"
          "Female Stress 40Hz\n")

    # Get user input for groups
    if not test:
        input_group_1 = input("Input the first group of your comparison (indicate a combination of groups with a ' + '): ")
        input_group_2 = input("Input the second group of your comparison (indicate a combination of groups with a ' + '): ")
    else:
        input_group_1 = "Female Control No Stim"
        input_group_2 = "Female Control 40Hz"

    comparison = input_group_1 + " v. " + input_group_2

    # Find subjects corresponding to user group inputs
    group_1 = []
    if input_group_1.find("+") >= 0:
        for x in input_group_1.split(" + "):
            group_1 += group_key[x]
    else:
        group_1 += group_key[input_group_1]

    group_2 = []
    if input_group_2.find("+") >= 0:
        for x in input_group_2.split(" + "):
            group_2 += group_key[x]
    else:
        group_2 += group_key[input_group_2]

    # Get user input for parameters
    if not test:
        parameter = input("Input the parameters you would like to compare (indicate a combination of parameters with a ' + '): ")
    else:
        parameter = "Convex Hull Volume + Convex Hull Area + Soma Volume + Filament Segment Length"

    # Get data for the input parameters of the input subjects. Then, perform statistical comparisons and plot data
    unit = ""

    # If there are multiple parameters, iterate through each and set units
    if parameter.find("+") >= 0:
        for x in parameter.split(" + "):
            if x == "Convex Hull Area":
                unit = " (µm^2)"
            elif x == "Convex Hull Volume":
                unit = " (µm^3)"
            elif x == "Soma Volume":
                unit = " (µm^3)"
            elif x == "Neuron Contact Volume":
                unit = " (µm^3)"
            elif x == "Filament Segment Length":
                unit = " (µm)"
            p = compare_groups(access_data(group_1, x, all_data), access_data(group_2, x, all_data))
            create_violin(access_data(group_1, x, all_data), access_data(group_2, x, all_data), comparison, x + unit, p)
    else:
        # If there is one parameter, set units here
        if parameter == "Convex Hull Area":
            unit = " (µm^2)"
        elif parameter == "Convex Hull Volume":
            unit = " (µm^3)"
        elif parameter == "Soma Volume":
            unit = " (µm^3)"
        elif parameter == "Neuron Contact Volume":
            unit = " (µm^3)"
        elif parameter == "Filament Segment Length":
            unit = " (µm)"
        p = compare_groups(access_data(group_1, parameter, all_data), access_data(group_2, parameter, all_data))
        create_violin(access_data(group_1, parameter, all_data), access_data(group_2, parameter, all_data), comparison, parameter + unit, p)


def round_to_n(x, n):
    if not x:
        return 0
    print(type(x))
    if x == np.nan:
        return 0
    power = -int(math.floor(math.log10(abs(x)))) + (n - 1)
    factor = (10 ** power)
    return round(x * factor) / factor


# C:\Users\Luke\Desktop\College\Research\Dr. Franklin\Image Analysis Pipeline\Data
data_path = input("Input the path of the folder containing the image analysis files for which you would like to compute stats: ")
select_groups(get_data(data_path), test=True)
