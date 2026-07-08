# Attila Pelican Theme
A content-focused responsive Pelican theme.

![attila screenshot](attila.png)

## Attribution
This project is based on the original work by **arulrajnet**.

Original repository:  
<https://github.com/arulrajnet/attila>

This repository is a maintained fork that includes additional features, fixes, and packaging improvements.

The bundled icon sprite contains selected Font Awesome Free 6.7.2 icons and is distributed under its included license at `static/icons/LICENSE.txt`.

## Overview
A content-focused responsive theme for [Pelican](https://github.com/getpelican/pelican).

It is ported from the ghost theme:  
<https://github.com/zutrinken/attila>

## Features
- Responsive layout  
- Navigation support  
- Parallax cover images for posts, author archives, and blog (respects `prefers-reduced-motion`)
- Author information for posts and author archives  
- Featured posts (via [neighbors plugin](https://github.com/pelican-plugins/neighbors))  
- Series posts (via [series plugin](https://github.com/pelican-plugins/series))
- Reading progress for posts  
- Automatic code syntax highlighting at build time via Pygments (light/dark adaptive, no client-side JS)
- Disqus / [utterances](https://utteranc.es/) support
- Google Analytics, GAUGES, Piwik  
- Sharing buttons  
- Open Graph  
- Rich Snippets (JSON-LD)
- Article subtitle
- Writing heatmap (via [heatmap plugin](https://pypi.org/project/pelican-heatmap/))
- OpenStreetMap (via [osm plugin](https://pypi.org/project/pelican-osm/))
- [umami](https://umami.is/) support
- Full-text search via [Pagefind](https://pagefind.app/) (Ctrl/Cmd+K)
- CJK-aware reading time and word count (`pelican.themes.attila.readtime`)
- Print stylesheet — hides site chrome, prints external link URLs
- Lazy loading for images
- Self-hosted web fonts (Libre Baskerville + Fira Sans) — no third-party font CDN, no tracking
- Local SVG icon sprite — no render-blocking icon CDN
- SRI (Subresource Integrity) on third-party CSS/JS bundles (Leaflet, MathJax)
- No jQuery dependency — pure vanilla JavaScript

## Install

### Using `pip`

```sh
pip install git+https://github.com/Lee-W/attila.git@main
```

Then in your `pelicanconf.py`:

```python
from pelican.themes import attila

THEME = attila.get_path()
```

### Using `pelican-themes`

- Download the latest zip from <https://github.com/Lee-W/attila/releases>
- Unzip the file  
- Install:

```sh
pelican-themes -U attila
```

- List installed themes:

```sh
pelican-themes -l
```

- Use that theme name in your `pelicanconf.py`

### Article Subtitle
To set an article subtitle, set `subtitle` metadata in the front-matter.

```rst
:title: Page With Cover Images
:subtitle: article subtitle
:date: 2018-04-29 00:45
:author: arul
:category: foo
:tags: footag
:slug: page-with-cover-images
:cover: assets/images/page_cover.jpg
```

### Header Covers

You can set cover images for blog, article, page, tag, category, and author.  

#### Blog Cover
This is the cover image for your site's main index.html.
To set blog cover, set the property `HOME_COVER` in
`pelicanconf.py`:

```python
HOME_COVER = "/assets/images/blog_cover.png"
```

> **NOTE**  
> `HEADER_COVER` property is deprecated. Use `HOME_COVER` and article-level covers instead.

#### Article Cover
To set a different cover image for an article, set `cover` metadata in the front-matter.

```rst
:title: With Cover Images
:date: 2018-04-29 00:45
:author: arul
:category: foo
:tags: footag
:slug: with-cover-images
:cover: /assets/images/article_cover.jpg
```

#### Page Cover
To set a different cover image for a page, set `cover` metadata in the front-matter.

```rst
:title: Page With Cover Images
:date: 2018-04-29 00:45
:author: arul
:category: foo
:tags: footag
:slug: page-with-cover-images
:cover: assets/images/page_cover.jpg
```

#### Tag Cover
To set a cover image for a tag, set the property `TAG_META` in `pelicanconf.py`

```python
TAG_META = {
    "food": {
        "cover": "/images/food.png",
        "description": "Examples ipsum dolor sit amet. Topping",
    },
    "drinks": {
        "cover": "/images/orange-juice.png",
        "description": "Examples ipsum dolor sit amet. Juice",
    },
}
```

#### Category Cover
To set a cover image for a category, set the property `CATEGORY_META` in `pelicanconf.py`

```python
CATEGORY_META = {
    "food": {
        "cover": "/images/junkie-stuff.png",
        "description": "Examples ipsum dolor sit amet. Topping",
    }
}
```

#### Author Cover
To set a cover image for an author, set the property `AUTHOR_META` in `pelicanconf.py`:

```python
AUTHOR_META = {"zutrinken": {"cover": "/assets/images/zutrinken-cover.png"}}
```

### Header Color
To define a simple header background color, set the property `HOME_COLOR` in `pelicanconf.py`

```python
HOME_COLOR = "black"
```

You can use any valid CSS color. This will be used if there is no cover.

> **NOTE**  
> `HEADER_COLOR` is deprecated. Use `HOME_COLOR` and article-level colors instead.

### Social URLs
To use GitHub, Twitter, and Facebook URLs set these properties:

```python
SOCIAL = (
    ("twitter", "https://twitter.com/myprofile"),
    ("github", "https://github.com/myprofile"),
    ("facebook", "https://facebook.com/myprofile"),
    ("flickr", "https://www.flickr.com/myprofile/"),
    ("envelope", "mailto:my@mail.address"),
)
```

### External Feed URL
Specify external feed (FeedBurner, etc.) using `rss`, `rss-square`, or `feed` icons in `SOCIAL`. A `<link>` will be placed in `<head>`.

### User-defined CSS

Define `CSS_OVERRIDE` in `pelicanconf.py` to insert a user-defined CSS file after the theme CSS. Example:

```python
CSS_OVERRIDE = ["css/myblog.css"]
```

### User-defined JS

```python
JS_OVERRIDE = ["js/custom.js"]
```

### Author Bio

```python
AUTHOR_META = {
    "zutrinken": {
        "name": "Zutrinken",
        "cover": "https://attila.demo.arulraj.net/assets/images/avatar.png",
        "image": "https://attila.demo.arulraj.net/assets/images/avatar.png",
        "website": "http://blog.arulraj.net",
        "location": "Chennai",
        "bio": "This is the place for a small biography with max 200 characters.",
    }
}
```

Supported social profiles: Facebook, GitHub, LinkedIn, Twitter, and Instagram.

### Analytics
- Google Analytics: `GOOGLE_ANALYTICS`  
- Gauges: `GAUGES`  
- Piwik: `PIWIK_URL` + `PIWIK_SITE_ID`
- umami: `UMAMI_WEBSITE_ID`

### Menu Items
The menu item comes from the pelican config `MENUITEMS`.

```python
MENUITEMS = (
    ("Home", "/"),
    ("Tag", "/tag/getting-started/"),
    ("Author", "/author/pelican/"),
    ("Category", "/category/examples/"),
    ("Archives", "/2015/11/"),
    ("Plugins", "https://github.com/pelican-plugins"),
)
```

### Article Metadata
- `color` → customize header color  
- `cover` → customize article header cover  
- `og_image` → OpenGraph image (fallback: cover → HEADER_COVER → default)  
- `twitter_image` → Twitter card image (fallback: header_cover → HEADER_COVER → default)

All image paths are relative to the site root. Absolute URLs allowed.

### Tag Cloud
- Tags page renders as a cloud  
- Configure font steps:

```python
TAG_CLOUD_STEPS = 5
```

Default: 5, max supported by theme: 10.  
For more steps, use CSS_OVERRIDE.

### Language Switcher

To show a language switcher in the navigation, set `LANGUAGES` (list of `(code, url)` pairs) and `CURRENT_LANG` (the active language code):

```python
LANGUAGES = [
    ("zh-tw", "/zh-tw/"),
    ("en", "/"),
]
CURRENT_LANG = "zh-tw"
```

By default the switcher displays the raw language code. Use `LANGUAGE_NAMES` to map codes to human-readable labels:

```python
LANGUAGE_NAMES = {
    "zh-tw": "台灣漢語",
    "en": "English",
}
```

### Creative Commons License

To display a Creative Commons license badge on articles, set `CC_LICENSE` in `pelicanconf.py`:

```python
CC_LICENSE = {
    "slug": "by-nc-sa",  # CC license slug, e.g. "by", "by-nc", "by-nc-sa"
    "version": "4.0",  # license version
    "name": "CC BY-NC-SA",  # human-readable name shown in the link text
}
```

The `slug` is used to build the license URL (`https://creativecommons.org/licenses/<slug>/<version>/`) and to render the corresponding Font Awesome Creative Commons icons.

### Comments Intro

To show an introductory paragraph above the comments section, set `COMMENTS_INTRO` in `pelicanconf.py`:

```python
COMMENTS_INTRO = "Comments are moderated. Be kind."
```

### Search

Full-text search is powered by [Pagefind](https://pagefind.app/). Attila includes a Pelican post-build hook that creates the search bundle after Pelican finishes writing the site, so a separate Node.js build step is not required.

Install Pagefind's extended Python package (recommended for Chinese and Japanese content), then enable Attila's hook:

```sh
pip install 'pagefind[extended]>=1.5.2'
```

```python
PLUGINS = [
    # ...your other plugins...
    "pelican.themes.attila.pagefind",
]
PAGEFIND_ENABLED = True
```

Users can open the generated search modal by clicking the search icon or pressing `Ctrl+K` / `Cmd+K`. Search is disabled by default so sites that do not install Pagefind never emit broken `/pagefind/` asset links. Set `PAGEFIND_VERBOSE = True` to show Pagefind's detailed indexing output.

### Reading Time

Attila ships a CJK-aware reading-time plugin. Unlike word-per-minute plugins that split on whitespace (and therefore count an entire Chinese article as a handful of words), it counts CJK characters and non-CJK words separately and converts each with its own reading speed:

```python
PLUGINS = [
    # ...your other plugins...
    "pelican.themes.attila.readtime",
]
```

With the plugin enabled, the article page meta line shows the estimated reading time and the word count (CJK characters + non-CJK words). Speeds default to 300 CJK characters and 250 words per minute and can be tuned:

```python
READTIME_CJK_CPM = 300  # CJK characters per minute
READTIME_WPM = 250  # non-CJK words per minute
SHOW_READTIME_IN_ARTICLE_SUMMARY = True  # also show it on post cards in listings
```

Articles rendered by the [post_stats](https://github.com/pelican-plugins/post-stats) plugin keep working: its `read_mins` value is shown when Attila's plugin is not enabled.

For multilingual weekday and month names, give every language an explicit locale. Python's locale is process-global, so a bare format string can otherwise inherit the locale of the previously processed article (for example, rendering `日` instead of `Sun` in English):

```python
DATE_FORMATS = {
    "en": ("en_US.UTF-8", "%a, %d %b %Y"),
    "zh-tw": ("zh_TW.UTF-8", "%Y/%m/%d（%a）"),
}
```

The configured locales must be installed on the build host.

### Responsive Cover Images

Cover images always emit a `sizes` attribute. For manually generated derivatives, provide a `srcset` globally or per article/page:

```python
COVER_IMAGE_SRCSET = "/images/cover-640.jpg 640w, /images/cover-1280.jpg 1280w"
COVER_IMAGE_SIZES = "100vw"
COVER_IMAGE_WIDTH = 1280
COVER_IMAGE_HEIGHT = 720
```

Article and page metadata may override these with `cover_srcset`, `cover_width`, and `cover_height`. When using `pelican-image-process`, keep the existing `large-photo` responsive-image transformation; Attila supplies the `image-process-large-photo` class and preserves the generated `srcset`.

### Fonts

The theme ships self-hosted web fonts — **Libre Baskerville** (body) and **Fira Sans** (headings/UI) — bundled as `woff2` under `static/font/` and declared via `@font-face` in `style.css`. Nothing is fetched from a third-party font CDN, so there are no extra DNS lookups and no requests leaking to Google. To use different fonts, override the `font-family` declarations via `CSS_OVERRIDE`.

### Other Configuration

```python
FACEBOOK_ADMINS = ["12345"]
GOOGLE_SITE_VERIFICATION = "token"
SHOW_ARTICLE_MODIFIED_TIME = True
SHOW_AUTHOR_BIO_IN_ARTICLE = True
SHOW_CATEGORIES_ON_MENU = True
SHOW_COMMENTS_COUNT_IN_ARTICLE_SUMMARY = True
SHOW_CREDITS = True
SHOW_FULL_ARTICLE_IN_SUMMARY = False
SHOW_PAGES_ON_MENU = True
SHOW_SITESUBTITLE_IN_HTML_TITLE = True
SHOW_TAGS_IN_ARTICLE_SUMMARY = True

UTTERANCES_REPO = "Lee-W/attila"
# label on GitHub issue
UTTERANCES_LABEL = "blog-comment"
```

## Contributing

Always open an issue before sending a PR. Discuss the problem/feature first.  
If it's a good improvement, submit your PR. Otherwise, fork Attila and build your own theme.

### CSS

`static/css/style.css` is **generated** — edit the modules in [`css-src/`](css-src/) and run `uv run poe build-css` to regenerate it. A test (`tests/test_css_build.py`) fails if the two ever drift apart.

## Copyright & License

Copyright (c) 2015-2016 Peter Amende — MIT License  
Fork and updates (c) 2016- Arulraj V — MIT License  
Fork and updates (c) 2026- Wei Lee — MIT License  

Some background images used from: <https://github.com/gilsondev/pelican-clean-blog>
