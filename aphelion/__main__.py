"""Project Aphelion CLI.

Usage:
    aphelion run --scenario <scenario.yaml>
    python -m aphelion --scenario <scenario.yaml>
"""

import argparse
import sys
from pathlib import Path

import yaml

from aphelion.dynamics.suborbital import SuborbitalPropagator


def load_scenario(path: str) -> dict:
    """Load a scenario configuration from a YAML file.

    Parameters
    ----------
    path : str
        Path to the YAML scenario file.

    Returns
    -------
    dict
        Parsed scenario configuration.
    """
    scenario_path = Path(path)
    if not scenario_path.exists():
        raise FileNotFoundError(f"Scenario file not found: {path}")

    with open(scenario_path) as f:
        return yaml.safe_load(f)


def run_scenario(scenario: dict) -> tuple[SuborbitalPropagator, dict]:
    """Run a simulation from a loaded scenario configuration.

    Parameters
    ----------
    scenario : dict
        Scenario configuration with 'vehicle', 'initial_conditions', and 'simulation' keys.

    Returns
    -------
    propagator : SuborbitalPropagator
        The propagator instance used.
    results : dict
        Dictionary with states, times, and trajectory statistics.
    """
    vehicle = scenario["vehicle"]
    ic = scenario["initial_conditions"]
    sim = scenario["simulation"]

    propagator = SuborbitalPropagator(
        dry_mass=vehicle["dry_mass"],
        propellant_mass=vehicle["propellant_mass"],
        area=vehicle["area"],
        cd=vehicle["cd"],
        thrust_nominal=vehicle["thrust_nominal"],
        burn_time=vehicle["burn_time"],
    )

    import numpy as np

    angle_rad = np.radians(ic["launch_angle_deg"])
    rail_speed = ic.get("rail_speed", 0.1)

    initial_state = [
        0.0,  # x
        0.0,  # y
        0.0,  # z
        rail_speed * np.cos(angle_rad),  # vx
        0.0,  # vy
        rail_speed * np.sin(angle_rad),  # vz
    ]

    states, times = propagator.propagate(
        initial_state,
        dt=sim.get("dt", 0.01),
        max_duration=sim.get("max_duration", 100.0),
    )

    stats = propagator.get_trajectory_stats(states, times)

    return propagator, {"states": states, "times": times, "stats": stats}


def print_results(stats: dict) -> None:
    """Print trajectory statistics to stdout."""
    print("\n=== Trajectory Statistics ===")
    print(f"  Apogee altitude:   {stats['apogee_altitude_m']:.1f} m")
    print(f"  Apogee time:       {stats['apogee_time_s']:.2f} s")
    print(f"  Flight time:       {stats['flight_time_s']:.2f} s")
    print(f"  Downrange distance:{stats['downrange_distance_m']:.1f} m")
    print(f"  Impact velocity:   {stats['impact_velocity_mps']:.2f} m/s")
    print("=============================\n")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="aphelion",
        description="Project Aphelion — Flight dynamics simulation",
    )
    parser.add_argument(
        "--scenario",
        "-s",
        required=True,
        help="Path to scenario YAML file",
    )
    args = parser.parse_args()

    try:
        scenario = load_scenario(args.scenario)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing scenario: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        _, results = run_scenario(scenario)
    except (ValueError, KeyError) as e:
        print(f"Error running scenario: {e}", file=sys.stderr)
        sys.exit(1)

    print_results(results["stats"])


if __name__ == "__main__":
    main()
