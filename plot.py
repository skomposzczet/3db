import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
matplotlib.use('QtAgg')
plt.style.use('bmh')
with open("./results/cassandra.json") as f:
    cassandra = json.load(f)
with open("./results/scylla.json") as f:
    scylla = json.load(f)
with open("./results/postgres.json") as f:
    postgress = json.load(f)
operations = list(cassandra.keys())
volumes = list(cassandra[operations[0]].keys())


for op_n in range(len(operations)):
    cass_results = np.array(list(cassandra[operations[op_n]].values()),
                            dtype=float)
    scylla_results = np.array(list(scylla[operations[op_n]].values()),
                              dtype=float)
    postgre_results = np.array(list(postgress[operations[op_n]].values()),
                               dtype=float)

    results = {
        'Cassandra': cass_results * 1000,
        'Scylla': scylla_results * 1000,
        'Postgres': postgre_results * 1000,
    }
    x = np.arange(len(volumes))  # label locations
    width = 0.25  # width of bars
    multiplier = 0  # for separation
    height = 0  # to specify maximum height for plot

    fig, ax = plt.subplots(layout='constrained')
    ax.grid(False)
    ax.set_title(operations[op_n].title())
    ax.set_xlabel('Number of samples (rows)')
    ax.set_ylabel('Time (ms)')
    ax.set_xticks(x+width, np.array(volumes, dtype=float).astype(int))
    for systems, result in results.items():
        offset = width * multiplier
        if result.max() > height:
            height = round(result.max(), 2)
        results = np.round(result, 2)
        rects = ax.bar(x + offset, results, width, label=systems)
        ax.bar_label(rects, padding=3)
        ax.set_ylim(0, height+0.25)
        ax.set_yticks(np.arange(0, height+0.25, 0.25))
        multiplier += 1

    ax.legend(loc='upper right', ncols=1)
    plt.savefig(f"./results/{operations[op_n]}.svg")
