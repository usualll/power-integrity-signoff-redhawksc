#!/bin/bash
# spr_violation_filter.sh
# Parses Ansys RedHawk-SC SPR (Supply Pin Resistance) reports to flag high-resistance nodes.

REPORT_FILE=${1:-"instance_pin_spr.rpt"}
THRESHOLD=${2:-500}
NET_NAME=${3:-"VDD"}

if [[ ! -f "$REPORT_FILE" ]]; then
    echo "Error: EDA report file '$REPORT_FILE' not found in current directory."
    exit 1
fi

echo "Scanning '$REPORT_FILE' for '$NET_NAME' nodes exceeding ${THRESHOLD} ohms..."

# Extract matching nets and filter based on resistance threshold (column 2)
grep "$NET_NAME" "$REPORT_FILE" | awk -v thresh="$THRESHOLD" '$2 > thresh' > flagged_spr_nodes.txt

VIOLATION_COUNT=$(wc -l < flagged_spr_nodes.txt)

echo "---------------------------------------------------"
echo "Analysis complete. Found $VIOLATION_COUNT vulnerable instances."
echo "Results exported to: flagged_spr_nodes.txt"
echo "Recommendation: Review layout for missing VDD straps or excessive distance from C4 bumps."