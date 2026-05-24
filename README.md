# GraceMed Previews

Static HTML preview sites for small medical practices, deployed under:

```text
https://preview.gracemed.us/<practice-slug>
```

Example:

```text
https://preview.gracemed.us/northhillspsychiatry
```

## Repository Structure

Each practice preview lives in its own top-level folder. The folder name is the deployed URL slug.

```text
gracemed-previews/
  AGENTS.md
  README.md
  northhillspsychiatry/
    index.html
    images/
  shared/
```

## Stack

- Static HTML
- Tailwind CSS via CDN
- Minimal JavaScript
- Static assets only
- Hosted on Cloudflare Pages

There is no backend, database, framework build step, or authenticated application code in this repository.

## Development Notes

- Use relative asset paths, because previews are served from subpaths.
- Keep previews mobile-first and accessible.
- Prefer optimized JPG/WebP images and SVG logos.
- Avoid production healthcare portal behavior or HIPAA-sensitive workflows in these previews.

See `AGENTS.md` for repository-specific implementation guidelines.
