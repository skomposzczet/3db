from modules.framework.test import Test
from modules.db.postgres import Postgres
from modules.db.scylla import Scylla
from modules.db.cassandra import Cassandra
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()

    parser.add_argument("-c", "--cassandra", action="store_true", help="run test for cassandra")
    parser.add_argument("-p", "--postgres", action="store_true", help="run test for postgres")
    parser.add_argument("-s", "--scylla", action="store_true", help="run test for scylla")
    
    return parser.parse_args()

def main():
    args = get_args()
    
    if args.cassandra:
        Test(Cassandra(), "./data/cars-in-movies.csv", "cassandra.json").run()
    elif args.postgres:
        Test(Postgres(), "./data/cars-in-movies.csv", "postgres.json").run()
    elif args.scylla:
        Test(Scylla(), "./data/cars-in-movies.csv", "scylla.json").run()
    else:
        print("Invalid argument, try --help.")

if __name__ == '__main__':
    main()

