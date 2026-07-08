# CSS sources

The shipped stylesheet `src/pelican/themes/attila/static/css/style.css` is
**generated** by concatenating the modules in this directory, in filename
order:

| file | contents |
|------|----------|
| `01-reset.css` | vendored normalize.css + base reset |
| `02-tokens.css` | `:root` design tokens (light + dark) |
| `03-fonts.css` | self-hosted `@font-face` declarations |
| `04-pygments.css` | generated Pygments syntax-highlight theme (light/dark) |
| `05-theme.css` | the Attila theme itself |
| `05a-refresh.css` | refreshed theme overrides and component polish |
| `06-footnote.css` | vendored littlefoot.css + theme-token overrides |
| `07-print.css` | print stylesheet |

## Workflow

Edit the modules here — **never edit the generated `style.css` directly** —
then rebuild:

```sh
uv run poe build-css
```

`tests/test_css_build.py` fails if `style.css` ever drifts out of sync with
these sources, so the generated file can't be edited by accident.
