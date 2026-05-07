# LaTeX Report Package

This folder contains the final ARG-Test report migrated into the KR template style.

## Files
- `main.tex`: main report source
- `main.pdf`: compiled PDF
- `kr.sty`, `kr.bst`, `kr.bib`: template assets copied from `D:\»Ìº˛≤‚ ‘\kr`
- `figures/`: report figures used by the paper

## Compile
Run in this folder:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Notes
- The author block keeps the anonymous KR-style position and currently shows Team ID / Student ID placeholders.
- The content is adapted from `ARG-Test_final_report_full_en.md`.
- Appendix command blocks are intentionally preserved as literal verbatim text.
