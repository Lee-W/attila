document.addEventListener("DOMContentLoaded", () => {
  const html = document.documentElement;

  // Run all scroll/resize work behind a single requestAnimationFrame tick so
  // we never do layout-thrashing work more than once per frame.
  const scrollHandlers = [];
  let ticking = false;
  const runScrollHandlers = () => {
    ticking = false;
    scrollHandlers.forEach((fn) => fn());
  };
  const requestScrollTick = () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(runScrollHandlers);
  };
  // Register a handler and run it once for its initial state.
  const onScroll = (fn) => {
    scrollHandlers.push(fn);
    fn();
  };
  ["scroll", "resize", "orientationchange"].forEach((evt) =>
    window.addEventListener(evt, requestScrollTick),
  );

  // Menu
  const toggleMenu = () => html.classList.toggle("menu-active");
  document
    .querySelectorAll("#menu, .nav-menu, .nav-close")
    .forEach((el) => el.addEventListener("click", toggleMenu));
  window.addEventListener("resize", () => html.classList.remove("menu-active"));
  window.addEventListener("orientationchange", () =>
    html.classList.remove("menu-active"),
  );

  // Parallax cover
  const cover = document.querySelector(".cover");
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;

  if (cover) {
    onScroll(() => {
      if (!prefersReducedMotion) {
        const windowPosition = window.scrollY;
        const coverPosition =
          windowPosition > 0 ? Math.floor(windowPosition * 0.25) : 0;
        cover.style.transform = `translate3d(0, ${coverPosition}px, 0)`;
      }
      if (window.scrollY < cover.offsetHeight) {
        html.classList.add("cover-active");
      } else {
        html.classList.remove("cover-active");
      }
    });
  }

  // Reading progress bar (article pages only)
  const post = document.querySelector(".post-content");
  const progressBar = document.querySelector(".progress-bar");
  const progressContainer = document.querySelector(".progress-container");
  if (post && progressBar && progressContainer) {
    onScroll(() => {
      const postRect = post.getBoundingClientRect();
      const postBottom = postRect.top + window.scrollY + post.offsetHeight;
      const viewportHeight = window.innerHeight;
      const progress =
        100 -
        ((postBottom - (window.scrollY + viewportHeight) + viewportHeight / 3) /
          (postBottom - viewportHeight + viewportHeight / 3)) *
          100;
      progressBar.style.width = progress + "%";
      progressContainer.classList.toggle("complete", progress > 100);
    });
  }

  // Gallery
  const gallery = () => {
    document.querySelectorAll(".kg-gallery-image img").forEach((image) => {
      const container = image.closest(".kg-gallery-image");
      const width = parseInt(image.getAttribute("width"), 10);
      const height = parseInt(image.getAttribute("height"), 10);
      if (!container || !width || !height) return;
      const ratio = width / height;
      container.style.flex = `${ratio} 1 0%`;
    });
  };

  gallery();

  // Theme (Light/Dark)
  const initTheme = () => {
    const toggle = document.querySelector(".js-theme");
    if (!toggle) return;

    const setDark = () => {
      html.classList.remove("theme-light");
      html.classList.add("theme-dark");
      html.style.colorScheme = "dark";
      localStorage.setItem("attila_theme", "dark");
      toggle.setAttribute("title", toggle.getAttribute("data-dark"));
    };

    const setLight = () => {
      html.classList.remove("theme-dark");
      html.classList.add("theme-light");
      html.style.colorScheme = "light";
      localStorage.setItem("attila_theme", "light");
      toggle.setAttribute("title", toggle.getAttribute("data-light"));
    };

    const systemPref = () => {
      const prefersDark =
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
      prefersDark ? setDark() : setLight();
    };

    // Initialize theme
    switch (localStorage.getItem("attila_theme")) {
      case "dark":
        setDark();
        break;
      case "light":
        setLight();
        break;
      default:
        systemPref();
        break;
    }

    // Toggle click
    toggle.addEventListener("click", (e) => {
      e.preventDefault();
      if (html.classList.contains("theme-dark")) {
        setLight();
      } else if (html.classList.contains("theme-light")) {
        setDark();
      } else {
        systemPref();
      }
    });
  };

  initTheme();

  // Language dropdown
  const initLanguageDropdown = () => {
    const toggle = document.querySelector(".nav-language-toggle");
    if (!toggle) return;

    // Detect current language by longest matching URL prefix
    const currentPath = window.location.pathname;
    let best = { text: "", length: 0, li: null };
    document
      .querySelectorAll(".nav-language-dropdown li a")
      .forEach((link) => {
        const href = new URL(
          link.getAttribute("href"),
          window.location.origin,
        ).pathname;
        if (currentPath.startsWith(href) && href.length > best.length) {
          best = {
            text: link.textContent.trim(),
            length: href.length,
            li: link.closest("li"),
          };
        }
      });
    if (best.li) {
      best.li.setAttribute("aria-selected", "true");
      toggle
        .querySelector(".nav-language-icon")
        ?.setAttribute("data-lang", best.text);
    }

    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const li = toggle.closest(".nav-languages");
      const isOpen = li.classList.contains("open");
      li.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(!isOpen));
    });

    document.addEventListener("click", () => {
      document
        .querySelectorAll(".nav-languages")
        .forEach((el) => el.classList.remove("open"));
      toggle.setAttribute("aria-expanded", "false");
    });

    // Escape closes the dropdown and returns focus to the toggle.
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape") return;
      const li = toggle.closest(".nav-languages");
      if (!li.classList.contains("open")) return;
      li.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    });

    // For links with data-fallback, check if target exists; fall back if 404
    document
      .querySelectorAll(".nav-language-dropdown li a[data-fallback]")
      .forEach((link) => {
        link.addEventListener("click", (e) => {
          const href = link.getAttribute("href");
          const fallback = link.getAttribute("data-fallback");
          if (link.closest("li").getAttribute("aria-selected") === "true")
            return;

          e.preventDefault();
          fetch(href, { method: "HEAD" })
            .then((res) => {
              window.location.href = res.ok ? href : fallback;
            })
            .catch(() => {
              window.location.href = href; // network error: try anyway
            });
        });
      });
  };

  initLanguageDropdown();

  // Menu dropdowns (grouped MENUITEMS)
  const initMenuDropdowns = () => {
    const toggles = document.querySelectorAll(".nav-dropdown-toggle");
    if (!toggles.length) return;

    const closeAll = (except) => {
      document.querySelectorAll(".nav-dropdown.open").forEach((el) => {
        if (el === except) return;
        el.classList.remove("open");
        el
          .querySelector(".nav-dropdown-toggle")
          ?.setAttribute("aria-expanded", "false");
      });
    };

    toggles.forEach((toggle) => {
      toggle.addEventListener("click", (e) => {
        e.stopPropagation();
        const li = toggle.closest(".nav-dropdown");
        const isOpen = li.classList.contains("open");
        closeAll(li);
        li.classList.toggle("open");
        toggle.setAttribute("aria-expanded", String(!isOpen));
      });
    });

    document.addEventListener("click", () => closeAll());

    // Escape closes any open dropdown and returns focus to its toggle.
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape") return;
      const open = document.querySelector(".nav-dropdown.open");
      if (!open) return;
      closeAll();
      open.querySelector(".nav-dropdown-toggle")?.focus();
    });
  };

  initMenuDropdowns();

  // Comments
  const initComments = () => {
    if (
      typeof disqus === "undefined" &&
      typeof use_utterance === "undefined"
    ) {
      const postComments = document.querySelector(".post-comments");
      if (postComments) postComments.style.display = "none";
      return;
    }

    if (typeof use_utterance === "undefined") {
      const showBtn = document.getElementById("show-comments");
      if (showBtn) {
        showBtn.addEventListener("click", () => {
          const script = document.createElement("script");
          script.src = `//${disqus}.disqus.com/embed.js`;
          script.async = true;
          document.body.appendChild(script);
          showBtn.parentElement.classList.add("activated");
        });
      }
    }
  };

  initComments();
});
