import distribution
import argparse
import correlation
import income_relation
import density_relation
import distribution

parser = argparse.ArgumentParser()
parser.add_argument("display",
        help="chooses where to obtain the data from, data relation or distribution")

if __name__=="__main__":
    args = parser.parse_args()
    display = args.display

    if display == 'relation':
        correlation.run_correlation_matrix()
        income_relation.run_income_relation()
        density_relation.run_density_relation()

    elif display == "distribution":

        distribution.run_distribution()
