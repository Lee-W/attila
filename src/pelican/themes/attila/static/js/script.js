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
    const toggleText = toggle.find(".theme-text");

    const setDark = () => {
      html.removeClass("theme-light").addClass("theme-dark");
      localStorage.setItem("attila_theme", "dark");
      toggleText.text(toggle.attr("data-dark"));
    };

    const setLight = () => {
      html.removeClass("theme-dark").addClass("theme-light");
      localStorage.setItem("attila_theme", "light");
      toggleText.text(toggle.attr("data-light"));
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
