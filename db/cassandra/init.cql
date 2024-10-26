CREATE KEYSPACE sdb WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
create TABLE sdb.car (
    id uuid PRIMARY KEY,
    full_name text,
    movie_title text,
);
