import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import numpy as np
import math
from data_analysis import DataAnalysis

handler = DataAnalysis()
handler.data_analysis()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Helvetica', 'Arial', 'sans-serif']
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

BG_COLOR = '#0f1923'
ACCENT_COLOR = '#ff4655'
GRID_COLOR = '#ffffff'


def apply_theme(fig, ax):
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='y', linestyle='-', alpha=0.1, color=GRID_COLOR)


def time_histogram_func():
    match_times = handler.match_times
    try:
        hours = [int(time_str[:2]) for time_str in match_times]
        for index, hour in enumerate(hours):
            if hours[index] <= 5:
                hours[index] += 18
            else:
                hours[index] -= 6
    except ValueError:
        print("Error: Ensure your data is a list of strings (e.g., '14:30')")
        hours = []

    if hours:
        fig, ax = plt.subplots(figsize=(12, 7))
        apply_theme(fig, ax)

        ax.hist(hours, bins=range(0, 25), color=ACCENT_COLOR, edgecolor=BG_COLOR, alpha=1.0, align='left')
        ax.set_title("Distribution of Matches by Hour of Day", fontsize=18, fontweight='bold', pad=20, color='white')
        ax.set_xlabel("Hour of Day (CST)", fontsize=12, labelpad=10)
        ax.set_ylabel("Number of Matches", fontsize=12, labelpad=10)
        ax.set_xticks(range(0, 24))

        plt.tight_layout()
        plt.show()


def histogram_func(data, range_low, range_high, title, xlabel, ylabel, step=1):
    fig, ax = plt.subplots(figsize=(12, 7))
    apply_theme(fig, ax)

    weights = np.ones_like(data) / len(data) * 100

    ax.hist(data, bins=range(range_low, (range_high + step + 1), step),
            weights=weights,
            color=ACCENT_COLOR, edgecolor=BG_COLOR, alpha=1.0,
            align='mid' if step > 1 else 'left')

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20, color='white')
    ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=12, labelpad=10)
    ax.set_xticks(range(range_low, (range_high + step + 1), step))

    from matplotlib.ticker import PercentFormatter
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))

    plt.tight_layout()
    plt.show()


def create_pie_with_other(data_dict, title, cutoff_percentage=2, image_folder=None):
    total_sum = sum(data_dict.values())
    if total_sum == 0:
        return

    threshold = total_sum * (cutoff_percentage / 100.0)
    labels = []
    sizes = []
    other_total = 0

    for name, count in data_dict.items():
        if count >= threshold:
            labels.append(name)
            sizes.append(count)
        else:
            other_total += count

    if other_total > 0:
        labels.append(f"Other")
        sizes.append(other_total)

    sorted_pairs = sorted(zip(sizes, labels), reverse=True)
    sizes = [s for s, l in sorted_pairs]
    labels = [l for s, l in sorted_pairs]

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    colors = plt.cm.Set3(np.linspace(0, 1, len(sizes)))

    wedges, texts, autotexts = ax.pie(sizes, labels=labels if not image_folder else None,
                                      autopct='%1.1f%%', startangle=90, pctdistance=0.8,
                                      colors=colors, wedgeprops=dict(width=0.4, edgecolor=BG_COLOR, linewidth=2),
                                      textprops={'fontsize': 12, 'color': 'white', 'fontweight': 'bold'})

    plt.setp(autotexts, size=11, weight="bold", color='black')

    if image_folder:
        for i, wedge in enumerate(wedges):
            label = labels[i]
            image_path = os.path.join(image_folder, f"{label}.png")

            ang = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))

            radius = 1.35

            if os.path.exists(image_path) and "Other" not in label:
                try:
                    img = plt.imread(image_path)
                    zoom_factor = 40 / img.shape[0]
                    imagebox = OffsetImage(img, zoom=zoom_factor)
                    ab = AnnotationBbox(imagebox, (x * radius, y * radius),
                                        frameon=False, bboxprops=dict(edgecolor='none'))
                    ax.add_artist(ab)
                except Exception:
                    ax.text(x * radius, y * radius, label, ha='center', va='center',
                            fontsize=12, fontweight='bold', color='white')
            else:
                ax.text(x * radius, y * radius, label, ha='center', va='center',
                        fontsize=12, fontweight='bold', color='white')

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20, color='white')
    plt.tight_layout()
    plt.show()


def create_bar_with_other(data_dict, title, cutoff_percentage=2, image_folder=None):
    total_sum = sum(data_dict.values())
    if total_sum == 0:
        return

    threshold = total_sum * (cutoff_percentage / 100.0)
    plot_data = {}
    other_total = 0
    for key, val in data_dict.items():
        if val >= threshold:
            plot_data[key] = val
        else:
            other_total += val

    sorted_items = sorted(plot_data.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_items]
    values = [(item[1] / total_sum) * 100 for item in sorted_items]

    if other_total > 0:
        labels.append(f"Other (< {cutoff_percentage}%)")
        values.append((other_total / total_sum) * 100)

    fig, ax = plt.subplots(figsize=(14, 8))
    apply_theme(fig, ax)

    bars = ax.bar(labels, values, color=ACCENT_COLOR, edgecolor=BG_COLOR, alpha=1.0, width=0.7)

    ax.set_title(title, fontsize=18, fontweight='bold', pad=30, color='white')
    ax.set_ylabel("Percentage (%)", fontsize=12, labelpad=10)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='white')

    if image_folder:
        ax.set_xticklabels([])
        ax.tick_params(axis='x', length=0)
        plt.subplots_adjust(bottom=0.2)

        for i, label in enumerate(labels):
            image_path = os.path.join(image_folder, f"{label}.png")
            if os.path.exists(image_path) and "Other" not in label:
                try:
                    img = plt.imread(image_path)

                    target_height = 40
                    target_width = 80

                    scale_h = target_height / img.shape[0]
                    scale_w = target_width / img.shape[1]

                    zoom_factor = min(scale_h, scale_w)

                    imagebox = OffsetImage(img, zoom=zoom_factor)
                    ab = AnnotationBbox(imagebox, (i, 0), xybox=(0, -30), xycoords='data', boxcoords="offset points",
                                        frameon=False)
                    ax.add_artist(ab)
                except Exception:
                    ax.text(i, -max(values) * 0.05, label, ha='center', va='top', rotation=0, fontsize=11)
            else:
                ax.text(i, -max(values) * 0.05, label, ha='center', va='top', rotation=0, fontsize=11)
    else:
        plt.xticks(rotation=0, ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()


create_bar_with_other(handler.weapon_kill_count, "Weapon Kill Distribution", 1, image_folder="assets/weapons")

histogram_func(handler.assist_list, 0, handler.most_assists,
               f"Distribution of Assists per Match (Average: {round(handler.average_assists, 1)})", "Assists per Match", "Number of Matches")

histogram_func(handler.kill_list, 0, handler.most_kills,
               f"Distribution of Kills per Match (Average: {round(handler.average_kills, 1)})", "Kills per Match", "Number of Matches")

histogram_func(handler.death_list, 0, handler.most_deaths,
               f"Distribution of Deaths per Match (Average: {round(handler.average_deaths, 1)})", "Deaths per Match", "Number of Matches")

histogram_func(handler.acs_list_rounded, 0, handler.most_acs_rounded,
               f"Distribution of ACS per Match (Average: {round(handler.average_acs, 1)})", "ACS per Match", "Number of Matches", step=20)

histogram_func(handler.match_length_data, 0, handler.longest_match,
               f"Distribution of Matches by Length (Average: {round(handler.average_match_length, 1)} Minutes)", "Length of Match (Minutes)", "Number of Matches")

histogram_func(handler.rounds_played_list, 0, handler.most_rounds,
               f"Distribution of Matches by Rounds Played (Average: {round(handler.average_rounds, 1)})", "Rounds Played", "Number of Matches")

create_bar_with_other(handler.armor_choice, "Armor Distribution", 0, image_folder="assets/armor")

create_pie_with_other(handler.party_size, "Solo vs Duo Queue Distribution", 0)

create_bar_with_other(handler.weapon_choice, "Weapon Distribution", 1, image_folder="assets/weapons")

create_bar_with_other(handler.agent_count, "Agent Distribution", 0, image_folder="assets/agents")

create_bar_with_other(handler.role_count, "Role Distribution", 0, image_folder="assets/roles")

create_bar_with_other(handler.server_count, "Server Distribution", 0)

create_pie_with_other(handler.vandal_phantom, "Vandal vs Phantom Distribution", image_folder="assets/weapons")

create_bar_with_other(handler.pistol_round_choice, "Pistol Round Weapon Distribution", 0, image_folder="assets/weapons")

time_histogram_func()