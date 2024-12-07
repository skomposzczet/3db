import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
matplotlib.use('QtAgg')

with open("./results/cassandra.json") as f:
    data_cassandra = json.load(f)
with open("./results/scylla.json") as f:
    data_scylla = json.load(f)
with open("./results/postgres.json") as f:
    data_postgress = json.load(f)
amounts = list(data_cassandra.keys())
operations = list(data_cassandra[amounts[0]].keys())
m_cassandra = {}
m_scylla = {}
m_postgress = {}
mea_in = {}

for db, m_db in zip([data_cassandra, data_scylla, data_postgress],
                    [m_cassandra, m_scylla, m_postgress]):
    for key in operations:
        for in_key in amounts:
            data = db[in_key]
            data = data[key]
            mea_in.update({in_key: data})
        m_db.update({key: mea_in})
        mea_in = {}


# op_n = 3
for op_n in range(4):
    array_cass = np.array(list(m_cassandra[operations[op_n]].values()),
                          dtype=float)
    array_scylla = np.array(list(m_scylla[operations[op_n]].values()),
                            dtype=float)
    array_postgre = np.array(list(m_postgress[operations[op_n]].values()),
                             dtype=float)

    measurements = {
        'Cassandra': array_cass * 1000,
        'Scylla': array_scylla * 1000,
        'Postgres': array_postgre * 1000,
    }

    x = np.arange(len(amounts))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    height = 0

    fig, ax = plt.subplots(layout='constrained')

    for systems, results in measurements.items():
        offset = width * multiplier
        if results.max() > height:
            height = round(results.max(), 2)
        results = np.round(results, 2)
        rects = ax.bar(x + offset, results, width, label=systems)
        ax.bar_label(rects, padding=3)
        ax.set_ylim(0, height+0.25)
        ax.set_yticks(np.arange(0, height+0.25, 0.25))
        multiplier += 1

    ax.set_ylabel('Time (ms)')
    ax.set_title(operations[op_n].title())
    ax.set_xticks(x+width, np.array(amounts, dtype=float).astype(int))
    ax.legend(loc='upper right', ncols=1)
    plt.savefig(f"./results/{operations[op_n]}.svg")
