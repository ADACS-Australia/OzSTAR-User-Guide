// Persist left-hand navigation scroll position across page loads.
(() => {
  const KEY = "ozstar-sidebar-scroll";

  document.addEventListener("DOMContentLoaded", () => {
    const scroller = document.querySelector(".sidebar-scroll");
    if (!scroller) return;

    scroller.style.scrollBehavior = "auto";

    try {
      const saved = sessionStorage.getItem(KEY);
      if (saved !== null) {
        scroller.scrollTop = Number(saved);
      }
    } catch {}

    const active = scroller.querySelector(".current-page");
    if (active) {
      const sRect = scroller.getBoundingClientRect();
      const aRect = active.getBoundingClientRect();
      if (aRect.top < sRect.top || aRect.bottom > sRect.bottom) {
        active.scrollIntoView({ block: "nearest" });
      }
    }

    requestAnimationFrame(() => {
      scroller.style.scrollBehavior = "";
    });

    const save = () => {
      try {
        sessionStorage.setItem(KEY, String(scroller.scrollTop));
      } catch {}
    };

    scroller.addEventListener("scroll", save, { passive: true });
    window.addEventListener("pagehide", save);
  });
})();
