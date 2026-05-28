# FrontDoor Health Previews

Static HTML preview sites for small medical practices, deployed under:

```text
https://preview.frontdoor.health/<practice-slug>
```

Example:

```text
https://preview.frontdoor.health/northhillspsychiatry
```

## Repository Structure

Each practice preview lives in its own top-level folder. The folder name is the deployed URL slug.

```text
frontdoor-previews/
  AGENTS.md
  README.md
  drdronavalli/
    index.html      # shared render shell
    practice.json   # practice + provider content
    images/
    assets/fonts/
  northhillspsychiatry/
    index.html      # shared render shell
    practice.json   # practice + provider content
    images/
    assets/fonts/
  shared/
    home-page.js
    styles/frontdoor.css
    fonts/
    logos/
  scripts/
```

## Stack

- Static HTML
- Tailwind CSS compiled at build time
- Minimal JavaScript
- Static assets only
- Hosted on Cloudflare Pages

There is no backend, database, framework build step, or authenticated application code in this repository.

## Content and Build Process

Practice-specific content lives in each practice folder as `practice.json`. Shared homepage rendering lives in `shared/home-page.js`, provider profile rendering lives in `scripts/generate_provider_pages.py`, and shared Tailwind source styles live in `shared/styles/frontdoor.css`. The checked-in practice `index.html` files are generic render shells; practice-specific metadata and page content come from `practice.json` during the build.

Build flow:

```text
practice.json + shared/home-page.js + shared/styles/frontdoor.css
  -> scripts/generate_provider_pages.py
  -> scripts/embed_practice_json.py
  -> rendered HTML/CSS in dist/
  -> Cloudflare Pages
```

`npm run build` runs `scripts/build.sh`, which:

1. Compiles Tailwind CSS from `shared/styles/frontdoor.css`.
2. Verifies each practice with an `index.html` has a valid `practice.json`.
3. Copies deployable site files into `dist/`.
4. Creates each practice `assets/` directory in `dist/`, copies compiled CSS to `assets/styles.css`, and copies shared fonts to `assets/fonts/`.
5. Generates static provider profile pages under `dist/<practice-slug>/providers/<provider-slug>/` from provider data in `practice.json`.
6. Embeds `practice.json` content into each built homepage so there is no runtime JSON fetch.
7. Replaces generic shell metadata with `seo.title` and `seo.description` from `practice.json`.
8. Removes source-only files such as `practice.json`, Markdown files, and build-only artifacts from `dist/`.

## Cloudflare Pages Deployment

Use the build script so repository-only files such as `AGENTS.md`, `scripts/`, and `practice.json` are not published.

- Build command: `./scripts/build.sh`
- Build output directory: `dist`

Cloudflare Pages deploys the generated `dist/` directory.

## Image Optimization

Generate WebP copies of raster images and update HTML references with:

```bash
python3 scripts/convert_images_to_webp.py --update-html
```

The script scans source `images/` folders, skips SVG/WebP files, and ignores generated folders like `dist/`.

## Development Notes

- Use relative asset paths, because previews are served from subpaths.
- Keep previews mobile-first and accessible.
- Prefer optimized JPG/WebP images and SVG logos.
- Drive practice and provider-specific content from `practice.json`; avoid one-off HTML/CSS edits per practice or provider.
- Keep templates opinionated. Add new JSON knobs only when they are reusable across practices.
- Provider profile UI labels have defaults in `scripts/generate_provider_pages.py` and can be overridden with `providerProfileLabels` in `practice.json` when needed.
- Treat per-practice `assets/styles.css` as a build output, not source. Shared CSS source lives in `shared/styles/frontdoor.css`.
- Avoid production healthcare portal behavior or HIPAA-sensitive workflows in these previews.

See `AGENTS.md` for repository-specific implementation guidelines.
