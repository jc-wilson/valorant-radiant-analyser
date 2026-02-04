import matplotlib.pyplot as plt
from data_analysis import DataAnalysis

handler = DataAnalysis()
handler.data_analysis()

def time_histogram_func():
    match_times = handler.match_times
    try:
        hours = [int(time_str[:2]) for time_str in match_times]
        for index, hour in enumerate(hours):
            if hours[index] == 23:
                hours[index] = 0
            else:
                hours[index] += 1
    except ValueError:
        print("Error: Ensure your data is a list of strings (e.g., '14:30')")
        hours = []

    if hours:
        plt.figure(figsize=(10, 6))

        plt.hist(hours, bins=range(0, 25), color='skyblue', edgecolor='black', align='left')

        plt.title("Distribution of Matches by Hour of Day", fontsize=16)
        plt.xlabel("Hour of Day (24h format)", fontsize=12)
        plt.ylabel("Number of Matches", fontsize=12)

        plt.xticks(range(0, 24))
        plt.grid(axis='y', alpha=0.5)

        plt.show()

def histogram_func(data, range_low, range_high, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))

    plt.hist(data, bins=range(range_low, (range_high + 2)), color='skyblue', edgecolor='black', align='left')

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    plt.xticks(range(range_low, (range_high + 2)))
    plt.grid(axis='y', alpha=0.5)

    plt.show()

def create_pie_with_other(data_dict, title, cutoff_percentage=2):
    total_sum = sum(data_dict.values())
    threshold = total_sum * (cutoff_percentage / 100.0)

    print(f"Total Sum: {total_sum}")
    print(f"Cutoff Threshold (2%): {threshold:.2f}")

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

    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()


def create_bar_with_other(data_dict, title, cutoff_percentage=2):

    total_sum = sum(data_dict.values())
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
    values = [item[1] for item in sorted_items]

    if other_total > 0:
        labels.append(f"Other (< {cutoff_percentage}%)")
        values.append(other_total)

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color='skyblue', edgecolor='black')

    # Formatting
    plt.title(title, fontsize=14)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()

histogram_func(handler.kill_list, handler.least_kills, handler.most_kills,
"Distribution of Kills per Match", "Kills per Match", "Number of Matches")
histogram_func(handler.death_list, handler.least_deaths, handler.most_deaths,
"Distribution of Deaths per Match", "Deaths per Match", "Number of Matches")
histogram_func(handler.match_length_data, handler.shortest_match, handler.longest_match,
"Distribution of Matches by Length", "Length of Match", "Number of Matches")
create_pie_with_other(handler.armor_choice, "Armor Distribution")
create_pie_with_other(handler.party_size, "Solo vs Duo Queue Distribution", 0)
create_bar_with_other(handler.weapon_choice, "Starting Weapon Distribution")
create_bar_with_other(handler.agent_count, "Agent Distribution", 0)
create_bar_with_other(handler.server_count, "Server Distribution", 0)
create_pie_with_other(handler.vandal_phantom, "Vandal vs Phantom Distribution")
create_bar_with_other(handler.pistol_round_choice, "Pistol Round Weapon Distribution", 0)
time_histogram_func()