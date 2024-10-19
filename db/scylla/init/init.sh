#!/bin/bash

echo "Initializing ScyllaDB"
sleep 25

while ! cqlsh scylla -e 'describe cluster' ; do
     echo "Waiting for main instance to be ready..."
     sleep 5
done

cqlsh scylla -f ./init/init.cql ;
echo "ScyllaDB initialized"
