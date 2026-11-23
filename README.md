# CV

Personal site of Sascha Meuser — Solution Architect for Microsoft Dynamics 365
and the Power Platform. Bilingual, static, no build step.

| | |
| --- | --- |
| **English** | https://miedon.github.io/CV/ |
| **Deutsch** | https://miedon.github.io/CV/de.html |

## Structure

| File | Purpose |
| --- | --- |
| `index.html` | English page — hero, career & projects, current focus, skills, education, contact |
| `de.html` | German page, same sections and same section `id`s |
| `styles.css` | All styling, shared by both pages |
| `app.js` | Progressive enhancement only: sticky-bar shadow, scroll reveal, nav highlight, footer year |
| `images/` | `portrait-400.jpg` and `portrait-800.jpg` are what the pages load via `srcset`; `portrait-source.jpg` is the full-size original kept for regenerating them |
| `tools/make-portrait.py` | Rebuilds the two portrait variants from a source photo |

GitHub Pages serves the repo root from `master`. To work on it, open the HTML
files directly in a browser — there is nothing to install or compile.

## Editing notes

- **Both languages must be edited together.** The pages are deliberate
  duplicates, not generated; a change to one belongs in the other. The section
  `id`s (`career`, `focus`, `skills`, `education`, `interests`, `contact`) are
  shared, so
  the `EN`/`DE` switch and the `hreflang` links keep working.
- Colours, spacing and type live as custom properties in `:root` at the top of
  `styles.css`, with a dark-mode override right below it. Light and dark follow
  the visitor's system setting via `prefers-color-scheme`.
- Skill levels are the `--lvl` percentage on each `.meter i`. Keep the
  `aria-label` in sync with the number next to it.
- A project is one `<li>` inside `.projects`: `<h4>` name, optional
  `.client` line, a sentence, then `.chips` for the stack.
- `@media print` is maintained: Ctrl+P gives a usable PDF — the bar, buttons
  and hero glows drop out, cards avoid page breaks, link URLs get spelled out.
- Fonts (Inter, Newsreader) come from Google Fonts with a `display=swap` and a
  system-font fallback, so the page stays readable if they fail to load.
- **Replacing the photo:** copy the new file to `images/portrait-source.jpg`
  and run `python tools/make-portrait.py images/portrait-source.jpg` (needs
  Pillow). It strips EXIF and writes both variants, so the HTML needs no
  change. Remember the `og:image` tag points at `portrait-800.jpg`.
  Without `--box` the script takes the centre square, which only works when the
  subject is centred. The current source is a portrait-orientation studio shot,
  so it is cropped to head and shoulders explicitly:

  ```
  python tools/make-portrait.py images/portrait-source.jpg --box 150,148,1500,1498
  ```

  Check the result before committing — the avatar is round, so the corners of
  the square are clipped and the head needs headroom.
- The LinkedIn and GitHub links carry `rel="me"`, which ties the three profiles
  together as the same person.
- The "current focus" section is marked **Learning**, not claimed as
  experience. Keep that badge until it genuinely is experience, and move the
  topic into the skills list when it is.

## Privacy

Two deliberate omissions. Keep both when editing.

**No contact details.** Postal address, mobile number and email address are
kept out of this repository on purpose. Do not add them, and do not commit the
source CV PDF or the project-list DOCX — they contain all three. The contact
section points to GitHub instead.

**No client names.** Employers are named (Cervus Consult, Team4, Flossbach von
Storch) — that is Sascha's own employment history. Clients of those employers
are described by sector plus a broad size band („parcel delivery provider,
5,000+ staff“), because the right to name a client as a reference generally
sits with the employer, not with the individual, and the former defence work
carries its own confidentiality. Project code names were replaced with neutral
titles for the same reason. The detailed list with real names stays offline,
for applications handed over on request.

Keep the size bands **broad**. They exist to convey project scale, and an exact
headcount combined with a sector and a region identifies a company outright —
which would defeat the point of the descriptor.
