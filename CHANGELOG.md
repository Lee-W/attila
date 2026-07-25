## v3.3.0 (2026-07-25)

### Feat

- add admonition styles for !!! blocks

## v3.2.6 (2026-07-15)

### Fix

- prevent multiline banner titles from overlapping

## v3.2.5 (2026-07-13)

### Fix

- make first click flip the theme toggle for OS-dark visitors

## v3.2.4 (2026-07-13)

### Fix

- inline the icon sprite so icons render on iOS

## v3.2.3 (2026-07-12)

### Fix

- repair mobile menu rendering on real devices

## v3.2.2 (2026-07-10)

### Fix

- improve responsive navigation and theme controls

## v3.2.1 (2026-07-08)

### Fix

- restore newer older navigation direction
- restore cover behavior to v3.2.0
- restore article cover layout rules
- use listing banner for pages
- render page covers as compact banners
- avoid global covers on pages
- keep page cover headers compact

### Refactor

- simplify theme sources and templates

## v3.2.0 (2026-07-07)

### Feat

- **theme**: refresh Attila layout

## v3.1.0 (2026-07-03)

### Feat

- **theme**: improve reading and display experience

## v3.0.1 (2026-06-29)

### Fix

- **osm**: load assets for place lists

## v3.0.0 (2026-06-29)

### BREAKING CHANGE

- Pagefind search now requires explicit opt-in. Existing
sites that had search working must add "pelican.themes.attila.pagefind"
to PLUGINS and set PAGEFIND_ENABLED = True; otherwise search silently
stops working.

### Feat

- **theme**: modernize icons, search, images, i18n

### Fix

- **theme**: scope metadata and plugin assets per page
- **pagination**: flex layout with SVG icons, fix overlap

## v2.17.0 (2026-06-17)

### Feat

- **footnote**: add littlefoot popover footnotes

## v2.16.0 (2026-06-15)

### Feat

- **a11y**: add color-scheme and theme-color meta tags

### Fix

- **nav**: make mobile dropdown menus collapsible
- **css**: keep mobile menu links readable in light mode
- **a11y**: give listing pages a #site-main skip-link target
- **i18n**: set <html lang> from the article/page language
- **head**: valid og:type and standard referrer policy
- **template**: make footer credits left/right configurable
- **seo**: emit valid JSON-LD with ISO 8601 dates

### Refactor

- **css**: author style.css from modular css-src sources

### Perf

- **images**: prioritize LCP cover images
- **js**: throttle scroll handlers and de-inline article scripts
- **fonts**: self-host web fonts instead of Google CDN

## v2.15.0 (2026-06-14)

### Feat

- **nav**: support grouped MENUITEMS as dropdown menus

## v2.14.0 (2026-06-11)

### Feat

- **a11y**: add skip-to-content link
- **template**: add footer_extra hook for plugin content above the footer
- highlight code at build time with Pygments, drop highlight.js
- **i18n**: add zh-tw translation for "On This Day"

### Fix

- apply saved theme before first paint

## v2.13.0 (2026-06-01)

### Feat

- **template**: support HTML in COMMENTS_INTRO via safe filter

## v2.12.1 (2026-05-30)

### Fix

- **seo**: emit valid Article/OG metadata for rich results
- **template**: load pagefind assets from site root on i18n subsites

### Refactor

- **css**: fluid heading sizes via clamp, drop redundant prefix

### Perf

- **template**: modernize markup — drop dead refs, defer JS, async images

## v2.12.0 (2026-05-29)

### Feat

- **css**: add pages index card grid layout

### Fix

- **css**: add spacing for Spotify iframe embeds in post content

## v2.11.1 (2026-05-27)

### Fix

- **css,template**: improve search button tap target and add open() fallback for Firefox mobile

## v2.11.0 (2026-05-27)

### Feat

- **template**: add hover anchor links to article headings

## v2.10.0 (2026-05-27)

### Feat

- add random article button and style details elements

## v2.9.1 (2026-05-26)

### Fix

- fix search modal not opening on iOS Safari

## v2.9.0 (2026-05-14)

### Feat

- move tags to the top

## v2.8.1 (2026-05-13)

### Fix

- footnote style

## v2.8.0 (2026-05-05)

### Feat

- add og_page.html template for self-contained page metadata

## v2.7.8 (2026-05-03)

### Fix

- fix mobile search button not receiving click events in Firefox and Safari

## v2.7.7 (2026-04-29)

### Fix

- set table boarder for better visibility

## v2.7.6 (2026-04-29)

### Fix

- keep single-line code blocks below the copy button

## v2.7.5 (2026-04-29)

### Fix

- simplify post table borders and align with theme tokens

## v2.7.4 (2026-04-27)

### Fix

- tighten figcaption spacing and remove decorative line

## v2.7.3 (2026-04-26)

### Fix

- AUTHOR_META key handling and avatar/cover display

## v2.7.2 (2026-04-25)

### Fix

- pin leaflet version with SRI, add reduced motion and lazy loading
- remove unused fonts, update vendored fonts to CDN, fix hardcoded paths
- update highlight.js theme to v11 scopes with dark mode support
- modernize outdated dependencies, remove jQuery, and clean up HTML/CSS
- color for series posts in dark mode
- modernize outdated dependencies and remove jQuery

## v2.7.1 (2026-04-20)

### Fix

- i18n, UX and series_list parsing issue

## v2.7.0 (2026-04-18)

### Feat

- **UX**: upgrade pagefind version and improve search UX (now we don't need a separate search page!)

## v2.6.2 (2026-04-18)

### Fix

- restore lang-specific font sizes for Firefox only

## v2.6.1 (2026-04-17)

### Fix

- remove en and zh-tw separate size setup

## v2.6.0 (2026-04-17)

### Feat

- add CC license display, comments intro, and improve navigation

## v2.5.0 (2026-04-17)

### Feat

- improve language button display

## v2.4.0 (2026-04-16)

### Feat

- modernize UI and add i18n support

## v2.3.0 (2026-04-15)

### Feat

- add umami support

## v2.2.1 (2026-03-14)

### Fix

- fix heatmap path

## v2.2.0 (2026-03-14)

### Feat

- add pelican-osm, pelican-heatmap support

## v2.10.0 (2026-05-27)

### Feat

- add random article button (requires pelican-random-article plugin, opt-in via `RANDOM_ARTICLE_BUTTON = True`)

## v2.9.1 (2026-05-26)

### Fix

- fix search modal not opening on iOS Safari

## v2.9.0 (2026-05-14)

### Feat

- move tags to the top

## v2.8.1 (2026-05-13)

### Fix

- footnote style

## v2.8.0 (2026-05-05)

### Feat

- add og_page.html template for self-contained page metadata

## v2.7.8 (2026-05-03)

### Fix

- fix mobile search button not receiving click events in Firefox and Safari

## v2.7.7 (2026-04-29)

### Fix

- set table boarder for better visibility

## v2.7.6 (2026-04-29)

### Fix

- keep single-line code blocks below the copy button

## v2.7.5 (2026-04-29)

### Fix

- simplify post table borders and align with theme tokens

## v2.7.4 (2026-04-27)

### Fix

- tighten figcaption spacing and remove decorative line

## v2.7.3 (2026-04-26)

### Fix

- AUTHOR_META key handling and avatar/cover display

## v2.7.2 (2026-04-25)

### Fix

- pin leaflet version with SRI, add reduced motion and lazy loading
- remove unused fonts, update vendored fonts to CDN, fix hardcoded paths
- update highlight.js theme to v11 scopes with dark mode support
- modernize outdated dependencies, remove jQuery, and clean up HTML/CSS
- color for series posts in dark mode
- modernize outdated dependencies and remove jQuery

## v2.7.1 (2026-04-20)

### Fix

- i18n, UX and series_list parsing issue

## v2.7.0 (2026-04-18)

### Feat

- **UX**: upgrade pagefind version and improve search UX (now we don't need a separate search page!)

## v2.6.2 (2026-04-18)

### Fix

- restore lang-specific font sizes for Firefox only

## v2.6.1 (2026-04-17)

### Fix

- remove en and zh-tw separate size setup

## v2.6.0 (2026-04-17)

### Feat

- add CC license display, comments intro, and improve navigation

## v2.5.0 (2026-04-17)

### Feat

- improve language button display

## v2.4.0 (2026-04-16)

### Feat

- modernize UI and add i18n support

## v2.3.0 (2026-04-15)

### Feat

- add umami support

## v2.2.1 (2026-03-14)

### Fix

- fix heatmap path

## v2.2.0 (2026-03-14)

### Feat

- add pelican-osm, pelican-heatmap support

## v2.1.0 (2026-03-10)

### Feat

- setup clipboard.css
- **style.css**: extend style
- **style.css**: increase tag-weight font-size
- **templates/archives**: rewrite archive format
- **css**: change code font-size to 1em
- **style.css**: change post-content pre margin to 0
- **style.css**: change code block margin
- remove highlight.js
- add pelican-osm support
- **article**: add mastodon to post_share and upgrade font-awesome
- **templates**: add series_list.html
- add pelican-series support
- **static**: detect whether the system is using dark mode
- add pagefind support
- add article.subtitle support
- add uterrances support

### Fix

- fix light-dark theme and restructure templates
- **article-selector**: Updated selector to .highlight pre code
- **copy-to-clipboard.js**: Narrow down the scope of copy targets
- **post-experpt**: fix post-experpt css

### Refactor

- extract head.html
- extract series as separate jinja modules

## v1.3 (2018-05-18)

## v1.2 (2017-12-02)

## v1.1 (2017-06-10)

## v1.0 (2016-09-19)
