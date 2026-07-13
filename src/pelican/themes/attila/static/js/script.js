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
  const menuToggle = document.querySelector(".nav-menu");
  const menuClose = document.querySelector(".nav-close");
  const siteNavigation = document.getElementById("site-navigation");
  const pageWrapper = document.getElementById("wrapper");
  const menuFocusableSelector =
    'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';
  const menuFocusableItems = () =>
    Array.from(siteNavigation?.querySelectorAll(menuFocusableSelector) ?? []);
  const setMenuOpen = (open, returnFocus = false) => {
    html.classList.toggle("menu-active", open);
    menuToggle?.setAttribute("aria-expanded", String(open));
    if (pageWrapper) pageWrapper.inert = open;
    if (open) {
      menuFocusableItems()[0]?.focus();
    } else if (returnFocus) {
      menuToggle?.focus();
    }
  };
  menuToggle?.addEventListener("click", () => {
    setMenuOpen(!html.classList.contains("menu-active"));
  });
  menuClose?.addEventListener("click", () => setMenuOpen(false, true));
  document.addEventListener("keydown", (event) => {
    if (!html.classList.contains("menu-active")) return;
    if (event.key === "Escape") {
      setMenuOpen(false, true);
      return;
    }
    if (event.key !== "Tab") return;

    const items = menuFocusableItems();
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  // Phones fire `resize` whenever the URL bar slides in or out, which would
  // slam the menu shut while the user is scrolling inside it. Only a width
  // change means the layout actually crossed the mobile breakpoint.
  let lastViewportWidth = window.innerWidth;
  window.addEventListener("resize", () => {
    if (window.innerWidth === lastViewportWidth) return;
    lastViewportWidth = window.innerWidth;
    setMenuOpen(false);
  });
  window.addEventListener("orientationchange", () => setMenuOpen(false));

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

    const getSavedTheme = () => {
      try {
        return localStorage.getItem("attila_theme");
      } catch (error) {
        return null;
      }
    };

    const saveTheme = (theme) => {
      try {
        localStorage.setItem("attila_theme", theme);
      } catch (error) {
        // Theme switching still works for this page when storage is unavailable.
      }
    };

    const updateToggle = (theme) => {
      const label = toggle.getAttribute(`data-${theme}`);
      toggle.setAttribute("title", label);
      toggle.setAttribute("aria-label", label);
      toggle.setAttribute("aria-pressed", String(theme === "dark"));
    };

    const setDark = (persist = true) => {
      html.classList.remove("theme-light");
      html.classList.add("theme-dark");
      html.style.colorScheme = "dark";
      if (persist) saveTheme("dark");
      updateToggle("dark");
    };

    const setLight = (persist = true) => {
      html.classList.remove("theme-dark");
      html.classList.add("theme-light");
      html.style.colorScheme = "light";
      if (persist) saveTheme("light");
      updateToggle("light");
    };

    // Whether the OS currently prefers dark, used both to decide the
    // effective (unsaved) theme and as the flip basis for the first click.
    const prefersDarkQuery =
      typeof window.matchMedia === "function"
        ? window.matchMedia("(prefers-color-scheme: dark)")
        : null;

    // Initialize theme
    const savedTheme = getSavedTheme();
    if (savedTheme === "dark") {
      setDark(false);
    } else if (savedTheme === "light") {
      setLight(false);
    } else {
      // No saved preference: don't add a class, let color-scheme follow the
      // OS. Only sync the toggle's label/aria to match.
      updateToggle(
        prefersDarkQuery && prefersDarkQuery.matches ? "dark" : "light",
      );
    }

    // Toggle click: flip between light and dark based on the effective
    // (not just saved) theme, so an OS-dark visitor's first click is a
    // visible change rather than a no-op.
    toggle.addEventListener("click", (e) => {
      e.preventDefault();
      const isDark = html.classList.contains("theme-dark")
        ? true
        : html.classList.contains("theme-light")
          ? false
          : Boolean(prefersDarkQuery && prefersDarkQuery.matches);
      if (isDark) {
        setLight();
      } else {
        setDark();
      }
    });

    // While no preference is saved, keep the toggle's label/aria in sync
    // with OS changes. Once the visitor picks a theme, this no longer
    // applies (the choice is locked in).
    if (prefersDarkQuery && typeof prefersDarkQuery.addEventListener === "function") {
      prefersDarkQuery.addEventListener("change", (e) => {
        if (getSavedTheme()) return;
        updateToggle(e.matches ? "dark" : "light");
      });
    }
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
      best.li.querySelector("a")?.setAttribute("aria-current", "page");
      const label = toggle.querySelector(".nav-language-label");
      if (label) label.textContent = best.text;
    }

    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const li = toggle.closest(".nav-languages");
      const isOpen = li.classList.contains("open");
      li.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(!isOpen));
    });

    toggle.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowDown") return;
      e.preventDefault();
      const li = toggle.closest(".nav-languages");
      li.classList.add("open");
      toggle.setAttribute("aria-expanded", "true");
      li.querySelector(".nav-language-dropdown a")?.focus();
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
          if (link.getAttribute("aria-current") === "page") return;

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

      toggle.addEventListener("keydown", (e) => {
        if (e.key !== "ArrowDown") return;
        e.preventDefault();
        const li = toggle.closest(".nav-dropdown");
        closeAll(li);
        li.classList.add("open");
        toggle.setAttribute("aria-expanded", "true");
        li.querySelector(".nav-dropdown-menu a")?.focus();
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
