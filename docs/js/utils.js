/**
 * Utility functions for the leaderboard
 */

export function formatPercent(value) {
  return value.toFixed(1) + "%";
}

export function calculateTdpImprovement(row) {
  return Math.max(row.first_delta, row.remediation_delta);
}

export function processData(data) {
  return data.map((row) => ({
    ...row,
    tdp_improvement: calculateTdpImprovement(row),
  }));
}
