import { leaderboardData } from "../data/leaderboard-data.js";
import { processData } from "./utils.js";
import { DataManager } from "./data-manager.js";
import { TableRenderer } from "./table-renderer.js";
import { SortIndicator } from "./sort-indicator.js";
import { StatsRenderer } from "./stats-renderer.js";

class LeaderboardApp {
  constructor() {
    this.data = processData(leaderboardData);
    this.dataManager = new DataManager(this.data);
    this.tableRenderer = new TableRenderer("leaderboardBody");
    this.sortIndicator = new SortIndicator();
    this.statsRenderer = new StatsRenderer();

    this.setupEventListeners();
    this.initialRender();
  }

  setupEventListeners() {
    // Dataset filter
    document.getElementById("datasetFilter").addEventListener("change", (e) => {
      this.handleFilter(e.target.value);
    });

    // Metric sort
    document.getElementById("metricSort").addEventListener("change", (e) => {
      this.handleSort(e.target.value, "desc");
    });

    // Column header sorting
    document.querySelectorAll("th.sortable").forEach((th) => {
      th.addEventListener("click", () => {
        this.handleSort(th.dataset.sort);
      });
    });
  }

  handleFilter(dataset) {
    this.dataManager.filter(dataset);
    const sortInfo = this.dataManager.getSort();
    this.handleSort(sortInfo.column, sortInfo.direction);
  }

  handleSort(column, direction = null) {
    this.dataManager.sort(column, direction);
    this.render();
  }

  render() {
    const data = this.dataManager.getData();
    const sortInfo = this.dataManager.getSort();
    const stats = this.dataManager.getStats();

    this.tableRenderer.render(data);
    this.sortIndicator.updateIndicators(sortInfo.column, sortInfo.direction);
    this.statsRenderer.render(stats);
  }

  initialRender() {
    this.handleSort("max_tdp", "desc");
  }
}

// Initialize the app when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  new LeaderboardApp();
});
