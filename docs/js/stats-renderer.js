export class StatsRenderer {
  constructor() {
    this.totalModelsEl = document.getElementById("totalModels");
    this.avgImprovementEl = document.getElementById("avgImprovement");
    this.bestImprovementEl = document.getElementById("bestImprovement");
  }

  render(stats) {
    this.totalModelsEl.textContent = stats.totalModels;
    this.avgImprovementEl.textContent =
      "+" + stats.avgImprovement.toFixed(1) + "%";
    this.bestImprovementEl.textContent =
      "+" + stats.bestImprovement.toFixed(1) + "%";
  }
}
