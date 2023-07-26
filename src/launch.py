import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' Launch Experiment.')
    parser.add_argument("--duration", type=int, help="Expirement duration in minutes", default= 5)
    parser.add_argument("--att-duration",type=int, help="Attacks duration in minutes", default= 1)

    args = parser.parse_args()

    # verify attack type

    # Verify benchmarks 

    # verify workload

    pass