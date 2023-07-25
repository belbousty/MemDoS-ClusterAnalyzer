import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' Launch Experiment.')
    parser.add_argument("--duration", type=int, help="Expirement duration in minutes", default= 5)
    parser.add_argument("--att-duration",type=int, help="Attacks duration in minutes", default= 1)

    # These two we could include them in installation process ?? 
    parser.add_argument("--app-types", required=True, nargs="+", help="Applications types")
    parser.add_argument("--attack-types",required=True , nargs="+", help="Attacks types")
    args = parser.parse_args()

    # verify number of victims with app-types argument

    # Verify number of attackers with --attack-types argument

    pass