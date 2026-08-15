/* BookLoop light/dark preference shared by product and developer screens. */
(function () {
  const storageKey = "bookloop-theme";
  const root = document.documentElement;
  const savedTheme = window.localStorage.getItem(storageKey);

  if (savedTheme === "dark" || savedTheme === "light") {
    root.dataset.theme = savedTheme;
  }

  function updateToggle(button) {
    const isDark = root.dataset.theme === "dark";
    button.textContent = isDark ? "☀️ Light mode" : "🌙 Dark mode";
    button.setAttribute("aria-pressed", String(isDark));
    button.setAttribute(
      "aria-label",
      isDark ? "Switch to light mode" : "Switch to dark mode",
    );
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      updateToggle(button);
      button.addEventListener("click", function () {
        const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
        root.dataset.theme = nextTheme;
        window.localStorage.setItem(storageKey, nextTheme);
        document.querySelectorAll("[data-theme-toggle]").forEach(updateToggle);
      });
    });
  });
})();
