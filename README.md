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
  northhillspsychiatry/
    index.html
    images/
  shared/
```

## Stack

- Static HTML
- Tailwind CSS compiled at build time
- Minimal JavaScript
- Static assets only
- Hosted on Cloudflare Pages

There is no backend, database, framework build step, or authenticated application code in this repository.

## Content and Build Process

Practice-specific content lives in each practice folder as `practice.json`. The checked-in `index.html` files contain render placeholders that are populated during the build.

Build flow:

```text
practice.json -> scripts/embed_practice_json.py -> rendered HTML in dist/ -> Cloudflare Pages
```

`npm run build` runs `scripts/build.sh`, which:

1. Compiles Tailwind CSS.
2. Verifies each practice with an `index.html` has a valid `practice.json`.
3. Copies deployable site files into `dist/`.
4. Embeds `practice.json` content into each built HTML file.
5. Removes source-only files such as `practice.json`, Markdown files, and build-only artifacts from `dist/`.

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
- Avoid production healthcare portal behavior or HIPAA-sensitive workflows in these previews.

See `AGENTS.md` for repository-specific implementation guidelines.
