# Hyperlink colors after a LibreOffice export

Regression for a bug found in the agentic robotics workshop flyer (Nov. 2026). The printed registration address
was a run hyperlink with an explicit gold color on the navy panel. `brand_check.py` passed it, because the XML
says gold. LibreOffice drew it in the theme's hyperlink color, `#1D65B9`, at about 2.0:1 on navy. Only the
rendered page showed it.

Run it from the skill root (LibreOffice and poppler needed):

```bash
python3 scripts/examples/regressions/hyperlink-colors/check_hyperlink_colors.py --out-dir <scratch folder>
```

It builds one slide from `spec.json`, exports it with `export_office.py`, renders it and samples the text pixels
of each case. Result with LibreOffice 26.8 (Nov. 3, 2026):

| Case | Set | Rendered | Contrast |
|---|---|---|---|
| Run hyperlink, gold on navy | `#EFAB00` | `#1D65B9` (theme link color) | 2.0:1, fails |
| Run hyperlink, navy on white | `#003976` | `#1D65B9` | 5.8:1, but not the color set |
| Run hyperlink with `hlinkClr val="tx"` | `#EFAB00` | `#EFAB00` | 5.7:1 |
| Plain text, no hyperlink | `#EFAB00` | `#EFAB00` | 5.7:1 |
| Hyperlink on the text box, not the run | `#EFAB00` | `#EFAB00` | 5.7:1 |

All three hyperlink variants produce a PDF link annotation.

## Recommended fix

1. On print pieces, print the address as plain text (no hyperlink) in an explicit brand color, and put the link
   on the QR picture. `project.py` does this: the QR picture is linked and the printed fallback is plain text.
2. When a printed address must also be clickable, put the hyperlink on the text box (shape click action), not on
   the run. If the link has to stay on the run, add the Office 2019 extension
   `<a:hlinkClr val="tx"/>` (namespace `http://schemas.microsoft.com/office/drawing/2018/hyperlinkcolor`) inside
   `a:hlinkClick`, so both PowerPoint and LibreOffice use the run's own color.
3. Always check the rendered page: a clean lint result is not a render check.
