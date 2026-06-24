#!/usr/bin/env python3
"""
extract_top_bottom_voltage.py

Parses RedHawk-SC static IR-drop reports (inst_voltage.rpt) to extract the 
most and least stressed instances. Useful for pinpointing strap gaps, dense 
switching clusters, or poorly connected clock-tree buffers.
"""

import sys
import argparse

def analyze_voltage(report_path, net_name="VDD", top_n=10):
    try:
        with open(report_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: Could not locate analysis report at '{report_path}'")
        sys.exit(1)

    # Filter for the target power net and ensure valid column counts
    valid_lines = [line for line in lines if net_name in line and len(line.split()) >= 5]

    if not valid_lines:
        print(f"No valid data found for net '{net_name}'. Check report formatting.")
        sys.exit(0)

    # Sort by voltage value (assuming voltage is extracted from the 5th column, index 4)
    try:
        sorted_instances = sorted(valid_lines, key=lambda x: float(x.split()[4]))
    except ValueError:
        print("Error: Unexpected report format. Ensure voltage float is in column 5.")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"--- BOTTOM {top_n} INSTANCES (Worst IR Drop / Lowest Voltage) ---")
    print(f"=======================================================")
    for inst in sorted_instances[:top_n]:
        cols = inst.split()
        print(f"Voltage: {cols[4]}V | Cell: {cols[1]:<20} | Inst: {cols[0]}")

    print(f"\n=======================================================")
    print(f"--- TOP {top_n} INSTANCES (Best Voltage / Near Nominal)   ---")
    print(f"=======================================================")
    # Reverse the last N elements for descending order
    for inst in sorted_instances[-top_n:][::-1]:
        cols = inst.split()
        print(f"Voltage: {cols[4]}V | Cell: {cols[1]:<20} | Inst: {cols[0]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract IR Drop extremes from RHSC reports.")
    parser.add_argument("report", nargs="?", default="static_analysis/inst_voltage.rpt", 
                        help="Path to the instance voltage report")
    parser.add_argument("--net", default="VDD", help="Net name to filter by (default: VDD)")
    parser.add_argument("--count", type=int, default=10, help="Number of instances to display")
    
    args = parser.parse_args()
    analyze_voltage(args.report, args.net, args.count)