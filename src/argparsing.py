import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Get admin token, mission and variant')
    parser.add_argument('--token', type=str, nargs=1,
                        help='the admin token retrieved upon starting up slurk')
    # NOT SURE ABOUT THIS ONE / HAVE TO FIND OUT HOW USERS WORK
    parser.add_argument('--user', type=str, nargs=1,
                        help='the admin token retrieved upon starting up slurk')
    parser.add_argument('--level', type=str, nargs=1, default="t",
                        help='the mission level: l0-l9, or test for test configuration')
    parser.add_argument('--variant', type=str, nargs=1, default="t",
                        help='the variant of the mission level v0-19, or test for test configuration')
    
    args = parser.parse_args()
    print(f'running experiment for mission level {args[2]} variant {args[3]}')

    return args