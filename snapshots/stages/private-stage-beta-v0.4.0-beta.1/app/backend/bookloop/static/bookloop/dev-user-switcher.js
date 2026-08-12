const devPanel = document.querySelector("#dev-user-switcher");
const devToggle = document.querySelector("#dev-user-switcher-toggle");
const storageKey = "bookloop-dev-user-switcher-visible";

if (devPanel && devToggle) {
  const setPanelVisibility = (isVisible) => {
    devPanel.hidden = !isVisible;
    devToggle.setAttribute("aria-expanded", String(isVisible));
  };

  // 브라우저를 다시 열어도 Tony가 마지막으로 선택한 표시 상태를 복원한다.
  const savedVisibility = window.localStorage.getItem(storageKey) === "true";
  setPanelVisibility(savedVisibility);

  devToggle.addEventListener("click", () => {
    const nextVisibility = devPanel.hidden;
    setPanelVisibility(nextVisibility);
    window.localStorage.setItem(storageKey, String(nextVisibility));
  });
}
