export class SortIndicator {
  updateIndicators(column, direction) {
    document.querySelectorAll("th.sortable").forEach((th) => {
      const existingIcon = th.querySelector(".sort-icon");
      if (existingIcon) existingIcon.remove();

      const icon = document.createElement("span");
      icon.className = "sort-icon ml-1 text-xs";

      if (th.dataset.sort === column) {
        icon.className += " opacity-100";
        icon.textContent = direction === "asc" ? "▲" : "▼";
      } else {
        icon.className += " opacity-50";
        icon.textContent = "⇅";
      }

      th.appendChild(icon);
    });
  }
}
