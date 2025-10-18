import { formatPercent } from "./utils.js";

export class TableRenderer {
  constructor(tableBodyId) {
    this.tbody = document.getElementById(tableBodyId);
  }

  render(data) {
    this.tbody.innerHTML = "";

    data.forEach((row, index) => {
      const tr = document.createElement("tr");
      tr.className =
        "transition-colors hover:bg-gray-50 border-b border-gray-200";

      const rankColor = this.getRankColor(index);
      const datasetBadgeClass = this.getDatasetBadgeClass(row.dataset);

      tr.innerHTML = `
        <td class="py-3 px-3 text-center ${rankColor} text-base">#${
        index + 1
      }</td>
        <td class="py-3 px-3 text-center"><span class="inline-block py-1 px-3 rounded text-xs font-medium uppercase ${datasetBadgeClass}">${
        row.dataset
      }</span></td>
        <td class="py-3 px-3 text-center font-medium text-gray-800">${
          row.model
        }</td>
        <td class="py-3 px-3 text-center font-mono text-gray-700">${formatPercent(
          row.first_normal
        )}</td>
        <td class="py-3 px-3 text-center font-mono text-gray-700">${formatPercent(
          row.first_tdp
        )}</td>
        <td class="py-3 px-3 text-center font-mono font-medium ${this.getDeltaColor(
          row.first_delta
        )}">+${formatPercent(row.first_delta)}</td>
        <td class="py-3 px-3 text-center font-mono text-gray-700">${formatPercent(
          row.remediation_normal
        )}</td>
        <td class="py-3 px-3 text-center font-mono text-gray-700">${formatPercent(
          row.remediation_tdp
        )}</td>
        <td class="py-3 px-3 text-center font-mono font-medium ${this.getDeltaColor(
          row.remediation_delta
        )}">+${formatPercent(row.remediation_delta)}</td>
        <td class="py-3 px-3 text-center font-mono text-gray-700">${formatPercent(
          row.max_tdp
        )}</td>
        <td class="py-3 px-3 text-center font-mono font-semibold text-emerald-700">+${formatPercent(
          row.tdp_improvement
        )}</td>
      `;

      this.tbody.appendChild(tr);
    });
  }

  getRankColor(index) {
    switch (index) {
      case 0:
        return "text-amber-700 font-bold";
      case 1:
        return "text-gray-500 font-semibold";
      case 2:
        return "text-amber-800 font-semibold";
      default:
        return "text-slate-600 font-medium";
    }
  }

  getDatasetBadgeClass(dataset) {
    return dataset.toLowerCase() === "humaneval"
      ? "bg-blue-50 text-blue-800 border border-blue-200"
      : "bg-violet-50 text-violet-800 border border-violet-200";
  }

  getDeltaColor(delta) {
    return delta > 0 ? "text-emerald-700" : "text-gray-500";
  }
}
