/**
 * Leaderboard Data
 *
 * To add new results:
 * 1. Add a new object to the array below
 * 2. Follow the exact structure of existing entries
 * 3. Ensure all numeric fields are numbers (not strings)
 * 4. The system will automatically calculate tdp_improvement
 *
 * Field definitions:
 * - dataset: "HumanEval" or "MBPP"
 * - model: Name of the model
 * - first_normal: First attempt accuracy without TDP (%)
 * - first_tdp: First attempt accuracy with TDP (%)
 * - first_delta: Difference between first_tdp and first_normal (%)
 * - remediation_normal: Remediation accuracy without TDP (%)
 * - remediation_tdp: Remediation accuracy with TDP (%)
 * - remediation_delta: Difference between remediation_tdp and remediation_normal (%)
 * - max_tdp: Maximum TDP accuracy achieved (%)
 */

export const leaderboardData = [
  // HumanEval Results
  {
    dataset: "HumanEval",
    model: "Claude 3.5 Sonnet",
    first_normal: 87.2,
    first_tdp: 88.4,
    first_delta: 1.2,
    remediation_normal: 95.7,
    remediation_tdp: 96.3,
    remediation_delta: 0.6,
    max_tdp: 96.3,
  },
  {
    dataset: "HumanEval",
    model: "Claude 3.5 Haiku",
    first_normal: 82.3,
    first_tdp: 85.4,
    first_delta: 3.1,
    remediation_normal: 92.7,
    remediation_tdp: 92.7,
    remediation_delta: 0.0,
    max_tdp: 92.7,
  },
  {
    dataset: "HumanEval",
    model: "GPT-4o",
    first_normal: 81.7,
    first_tdp: 83.5,
    first_delta: 1.8,
    remediation_normal: 91.5,
    remediation_tdp: 91.5,
    remediation_delta: 0.0,
    max_tdp: 91.5,
  },
  {
    dataset: "HumanEval",
    model: "GPT-4o-mini",
    first_normal: 79.9,
    first_tdp: 81.7,
    first_delta: 1.8,
    remediation_normal: 88.4,
    remediation_tdp: 88.4,
    remediation_delta: 0.0,
    max_tdp: 88.4,
  },
  {
    dataset: "HumanEval",
    model: "Qwen 32B Coder",
    first_normal: 81.7,
    first_tdp: 87.2,
    first_delta: 5.5,
    remediation_normal: 87.8,
    remediation_tdp: 91.5,
    remediation_delta: 3.7,
    max_tdp: 91.5,
  },
  {
    dataset: "HumanEval",
    model: "Qwen 14B Coder",
    first_normal: 80.5,
    first_tdp: 86.0,
    first_delta: 5.5,
    remediation_normal: 80.5,
    remediation_tdp: 86.6,
    remediation_delta: 6.1,
    max_tdp: 86.6,
  },
  {
    dataset: "HumanEval",
    model: "Qwen 7B Coder",
    first_normal: 79.3,
    first_tdp: 80.5,
    first_delta: 1.2,
    remediation_normal: 79.3,
    remediation_tdp: 80.5,
    remediation_delta: 1.2,
    max_tdp: 80.5,
  },
  {
    dataset: "HumanEval",
    model: "Qwen 3B Coder",
    first_normal: 76.2,
    first_tdp: 78.7,
    first_delta: 2.4,
    remediation_normal: 76.2,
    remediation_tdp: 78.7,
    remediation_delta: 2.4,
    max_tdp: 78.7,
  },

  // MBPP Results
  {
    dataset: "MBPP",
    model: "Claude 3.5 Sonnet",
    first_normal: 75.6,
    first_tdp: 86.0,
    first_delta: 10.3,
    remediation_normal: 93.0,
    remediation_tdp: 93.7,
    remediation_delta: 0.7,
    max_tdp: 93.7,
  },
  {
    dataset: "MBPP",
    model: "Claude 3.5 Haiku",
    first_normal: 73.8,
    first_tdp: 83.8,
    first_delta: 10.1,
    remediation_normal: 90.9,
    remediation_tdp: 92.7,
    remediation_delta: 1.9,
    max_tdp: 92.7,
  },
  {
    dataset: "MBPP",
    model: "GPT-4o",
    first_normal: 73.1,
    first_tdp: 84.3,
    first_delta: 11.2,
    remediation_normal: 88.5,
    remediation_tdp: 91.1,
    remediation_delta: 2.6,
    max_tdp: 91.1,
  },
  {
    dataset: "MBPP",
    model: "GPT-4o-mini",
    first_normal: 70.7,
    first_tdp: 79.6,
    first_delta: 8.9,
    remediation_normal: 82.7,
    remediation_tdp: 85.2,
    remediation_delta: 2.6,
    max_tdp: 85.2,
  },
  {
    dataset: "MBPP",
    model: "Qwen 32B Coder",
    first_normal: 73.5,
    first_tdp: 82.2,
    first_delta: 8.7,
    remediation_normal: 84.8,
    remediation_tdp: 88.1,
    remediation_delta: 3.3,
    max_tdp: 88.1,
  },
  {
    dataset: "MBPP",
    model: "Qwen 14B Coder",
    first_normal: 72.4,
    first_tdp: 81.7,
    first_delta: 9.4,
    remediation_normal: 73.8,
    remediation_tdp: 83.1,
    remediation_delta: 9.4,
    max_tdp: 83.1,
  },
  {
    dataset: "MBPP",
    model: "Qwen 7B Coder",
    first_normal: 65.3,
    first_tdp: 77.3,
    first_delta: 11.9,
    remediation_normal: 65.6,
    remediation_tdp: 77.8,
    remediation_delta: 12.2,
    max_tdp: 77.8,
  },
  {
    dataset: "MBPP",
    model: "Qwen 3B Coder",
    first_normal: 63.7,
    first_tdp: 68.2,
    first_delta: 4.5,
    remediation_normal: 63.7,
    remediation_tdp: 68.6,
    remediation_delta: 4.9,
    max_tdp: 68.6,
  },
];
