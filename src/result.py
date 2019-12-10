import distribution
import argparse
import relation
import distribution

parser = argparse.ArgumentParser()
parser.add_argument("display",
        help="chooses where to obtain the data from, data relation or distribution")


if __name__=="__main__":
    args = parser.parse_args()
    display = args.display

    if display == 'relation':

        relation.run_relation()

    elif display == "distribution":

        distribution.run_distribution()
