#!/usr/bin/env bash

venv() {
    source .venv/bin/activate
}

cassandra() {
    echo 'Deploying Cassandra...'
    pushd db/cassandra/ || return
    ./compose.sh up
    popd || return
    echo 'Cassandra deployed'

    echo 'Running test...'
    python main.py --cassandra
    echo 'Finished test'

    pushd db/cassandra/ || return
    echo 'Removing Cassandra...'
    ./compose.sh down
    echo 'Cassandra done'
    popd || return
}

scylla() {
    echo 'Deploying Scylla...'
    pushd db/scylla/ || return
    ./compose.sh up
    popd || return
    echo 'Scylla deployed'

    echo 'Running test...'
    python main.py --scylla
    echo 'Finished test'

    pushd db/scylla/ || return
    echo 'Removing Scylla...'
    ./compose.sh down
    echo 'Scylla done'
    popd || return
}

postgres() {
    echo 'Deploying Postgres...'
    pushd db/postgres/ || return
    docker compose up -d
    popd || return
    echo 'Postgres deployed'

    echo 'Running test...'
    python main.py --postgres
    echo 'Finished test'

    pushd db/postgres/ || return
    echo 'Removing Postgres...'
    docker compose down
    echo 'Postgres done'
    popd || return
}

benchmark() {
    cassandra
    scylla
    postgres
}

plot() {
    echo 'Plotting...'
    python plot.py

}

benchmark
plot
