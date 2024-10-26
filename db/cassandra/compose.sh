#!/usr/bin/env bash

if [ "$1" == "up" ]; then
  docker compose up -d

  while [ "$(docker inspect -f '{{.State.Running}}' cassandra-load-keyspace)" == "true" ]; do
    sleep 5
  done

  volume_names=$(docker inspect cassandra-load-keyspace -f '{{range .Mounts}}{{println .Name}}{{end}}')

  docker rm -f cassandra-load-keyspace > /dev/null 2>&1

  for volume_name in $volume_names; do
    docker volume rm "$volume_name" > /dev/null 2>&1
  done
elif [ "$1" == "down" ]; then
  docker compose down
else
  echo "usage: $0 up|down"
fi
