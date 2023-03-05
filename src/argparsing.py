import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="Get slurk token, user and task, and ithor mission and variant"
    )

    parser.add_argument(
        "--token", type=str, help="the $ITHOR_TOKEN created in step 4.3"
    )
    parser.add_argument("--user", type=int, help="the $ITHOR_USER created in step 4.3")
    parser.add_argument("--task", type=int, help="the $TASK_ID created in step 4.2")

    parser.add_argument(
        "--level",
        type=str,
        default="l0",
        help="the mission level: l0-l10, or t for test configuration",
    )
    parser.add_argument(
        "--variant",
        type=str,
        default="v1",
        help="the variant of the mission level v1-v10, or t for test configuration",
    )

    args = parser.parse_args()

    return vars(args)
