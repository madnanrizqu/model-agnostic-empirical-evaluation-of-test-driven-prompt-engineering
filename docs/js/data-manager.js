export class DataManager {
  constructor(data) {
    this.originalData = [...data];
    this.currentData = [...data];
    this.currentSort = { column: "tdp_improvement", direction: "desc" };
    this.currentFilter = { dataset: "all" };
  }

  filter(datasetFilter) {
    this.currentFilter.dataset = datasetFilter;

    this.currentData = this.originalData.filter((row) => {
      if (datasetFilter !== "all" && row.dataset !== datasetFilter) {
        return false;
      }
      return true;
    });

    return this.currentData;
  }

  sort(column, direction = null) {
    if (direction === null) {
      if (this.currentSort.column === column) {
        direction = this.currentSort.direction === "asc" ? "desc" : "asc";
      } else {
        direction = "desc";
      }
    }

    this.currentSort = { column, direction };

    this.currentData.sort((a, b) => {
      let aVal = a[column];
      let bVal = b[column];

      if (typeof aVal === "string") {
        aVal = aVal.toLowerCase();
        bVal = bVal.toLowerCase();
      }

      if (aVal === bVal) return 0;

      if (direction === "asc") {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });

    return this.currentData;
  }

  getData() {
    return this.currentData;
  }

  getSort() {
    return this.currentSort;
  }

  getStats() {
    const totalModels = this.currentData.length;
    const avgImprovement =
      this.currentData.reduce((sum, row) => sum + row.tdp_improvement, 0) /
      totalModels;
    const bestImprovement = Math.max(
      ...this.currentData.map((row) => row.tdp_improvement)
    );

    return {
      totalModels,
      avgImprovement,
      bestImprovement,
    };
  }
}
