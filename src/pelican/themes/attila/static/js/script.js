jQuery(($) => {
  const html = $("html");
  const viewport = $(window);

  // Menu
  const toggleMenu = () => html.toggleClass("menu-active");
  $("#menu, .nav-menu, .nav-close").on("click", toggleMenu);
  viewport.on("resize orientationchange", () =>
    html.removeClass("menu-active"),
  );

  // Parallax cover
  const cover = $(".cover");
  let coverPosition = 0;

  const updateParallax = () => {
    if (!cover.length) return;
    const windowPosition = viewport.scrollTop();
    coverPosition = windowPosition > 0 ? Math.floor(windowPosition * 0.25) : 0;
    cover.css({
      "-webkit-transform": `translate3d(0, ${coverPosition}px, 0)`,
      transform: `translate3d(0, ${coverPosition}px, 0)`,
    });
    viewport.scrollTop() < cover.height()
      ? html.addClass("cover-active")
      : html.removeClass("cover-active");
  };

  updateParallax();
  viewport.on("scroll resize orientationchange", updateParallax);

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
    const toggle = $(".js-theme");
    if (!toggle.length) return;

    const setDark = () => {
      html.removeClass("theme-light").addClass("theme-dark");
      html[0].style.colorScheme = "dark";
      localStorage.setItem("attila_theme", "dark");
      toggle.attr("title", toggle.attr("data-dark"));
    };

    const setLight = () => {
      html.removeClass("theme-dark").addClass("theme-light");
      html[0].style.colorScheme = "light";
      localStorage.setItem("attila_theme", "light");
      toggle.attr("title", toggle.attr("data-light"));
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
    toggle.on("click", (e) => {
      e.preventDefault();
      if (html.hasClass("theme-dark")) {
        setLight();
      } else if (html.hasClass("theme-light")) {
        setDark();
      } else {
        systemPref();
      }
    });
  };

  initTheme();

  // Language dropdown
  const initLanguageDropdown = () => {
    const toggle = $(".nav-language-toggle");
    if (!toggle.length) return;

    // Detect current language by longest matching URL prefix
    const currentPath = window.location.pathname;
    let best = { text: "", length: 0, li: null };
    $(".nav-language-dropdown li a").each(function () {
      const href = new URL($(this).attr("href"), window.location.origin).pathname;
      if (currentPath.startsWith(href) && href.length > best.length) {
        best = { text: $(this).text().trim(), length: href.length, li: $(this).closest("li") };
      }
    });
    if (best.li) {
      best.li.attr("aria-selected", "true");
      toggle.find(".nav-language-icon").attr("data-lang", best.text);
    }

    toggle.on("click", (e) => {
      e.stopPropagation();
      const li = toggle.closest(".nav-languages");
      const isOpen = li.hasClass("open");
      li.toggleClass("open");
      toggle.attr("aria-expanded", String(!isOpen));
    });

    $(document).on("click", () => {
      $(".nav-languages").removeClass("open");
      toggle.attr("aria-expanded", "false");
    });

    // For links with data-fallback, check if target exists; fall back if 404
    $(".nav-language-dropdown li a[data-fallback]").on("click", function (e) {
      const link = $(this);
      const href = link.attr("href");
      const fallback = link.attr("data-fallback");
      if (link.closest("li").attr("aria-selected") === "true") return;

      e.preventDefault();
      fetch(href, { method: "HEAD" }).then((res) => {
        window.location.href = res.ok ? href : fallback;
      }).catch(() => {
        window.location.href = href; // network error: try anyway
      });
    });
  };

  initLanguageDropdown();

  // Comments
  const initComments = () => {
    if (typeof disqus === "undefined" && typeof use_utterance === "undefined") {
      $(".post-comments").hide();
      return;
    }

    if (typeof use_utterance === "undefined") {
      $("#show-comments").on("click", function () {
        $.ajax({
          type: "GET",
          url: `//${disqus}.disqus.com/embed.js`,
          dataType: "script",
          cache: true,
        });
        $(this).parent().addClass("activated");
      });
    }
  };

  initComments();
});
