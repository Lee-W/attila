document.addEventListener("DOMContentLoaded", () => {
  const html = document.documentElement;

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
  let coverPosition = 0;

  const updateParallax = () => {
    if (!cover) return;
    const windowPosition = window.scrollY;
    coverPosition = windowPosition > 0 ? Math.floor(windowPosition * 0.25) : 0;
    cover.style.transform = `translate3d(0, ${coverPosition}px, 0)`;
    if (window.scrollY < cover.offsetHeight) {
      html.classList.add("cover-active");
    } else {
      html.classList.remove("cover-active");
    }
  };

  updateParallax();
  window.addEventListener("scroll", updateParallax);
  window.addEventListener("resize", updateParallax);
  window.addEventListener("orientationchange", updateParallax);

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
