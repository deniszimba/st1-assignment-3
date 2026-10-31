
"""Run the SmartCare demo or interactive appointment menu."""

import argparse

from smartcare.console import run_demo, run_menu


def main() -> None:
    """Start the demo by default or the interactive menu when requested."""
    parser = argparse.ArgumentParser(
        description='SmartCare teaching application',
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Launch the interactive appointment menu',
    )

    args = parser.parse_args()

    if args.interactive:
        run_menu()
    else:
        run_demo()


if __name__ == '__main__':
    main()
