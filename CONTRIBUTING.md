# Contributor Guide

## TDP Leaderboards

### Adding Your Results

To add your model results to the leaderboard:

1. Open `data/leaderboard-data.js`
2. Add a new entry to the `leaderboardData` array following this structure:

```javascript
{
  dataset: "HumanEval", // or "MBPP"
  model: "Your Model Name",
  first_normal: 85.0,
  first_tdp: 87.5,
  first_delta: 2.5,
  remediation_normal: 90.0,
  remediation_tdp: 92.0,
  remediation_delta: 2.0,
  max_tdp: 92.0,
}
```

3. Ensure all numeric values are numbers (not strings)
4. The system automatically calculates `tdp_improvement`
5. Test locally by opening `index.html` in a browser
6. Submit a pull request

### Project Structure

```
docs/
├── index.html              # Main HTML file
├── data/
│   └── leaderboard-data.js # All leaderboard data (EDIT THIS)
├── js/
│   ├── app.js             # Main application
│   ├── data-manager.js    # Filtering and sorting logic
│   ├── table-renderer.js  # Table rendering
│   ├── stats-renderer.js  # Statistics display
│   ├── sort-indicator.js  # Sort indicators
│   └── utils.js           # Utility functions
└── README.md              # This file
```

### Field Definitions

- **dataset**: "HumanEval" or "MBPP"
- **model**: Name of the LLM model
- **first_normal**: First attempt accuracy without TDP (%)
- **first_tdp**: First attempt accuracy with TDP (%)
- **first_delta**: Difference (first_tdp - first_normal)
- **remediation_normal**: Remediation accuracy without TDP (%)
- **remediation_tdp**: Remediation accuracy with TDP (%)
- **remediation_delta**: Difference (remediation_tdp - remediation_normal)
- **max_tdp**: Maximum TDP accuracy achieved (%)

### Development

The project uses ES6 modules. To develop locally:

1. Use a local server (e.g., `python -m http.server`)
2. Navigate to `http://localhost:8000`
3. Make changes to modules in `js/` directory
4. Refresh the page to see changes

## Questions?

Open an issue in the repository for any questions or problems.
