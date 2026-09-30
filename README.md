# Ranova TV website

Static HTML/CSS site for GitHub Pages: home, support, privacy policy, terms, and 404. No JavaScript, no external requests.

## Editing

Page content lives in `scripts/build_site.py`. Edit it there, then regenerate the pages:

```
python scripts/build_site.py --email alraoosh.studio@gmail.com --release-ready
```

Without `--release-ready`, the pages get pre-release notices and a `noindex` tag. Styles are in `assets/style.css`, and the script doesn't touch them. The fonts (Unbounded, Instrument Sans, OFL) are self-hosted in `assets/fonts/`. The home-screen images in `assets/app/` are copied from the app (`apps/tv-web/src/ui/brand`).

## Keep the privacy policy true

The privacy policy was checked against the app code at v0.2.0. Update it when any of the following changes:
- the Lorem Picsum home backgrounds (`src/app/ambient-backgrounds.ts`) or the YouTube trailer check (`src/app/trailer.ts`)
- credential storage, which is currently unencrypted `localStorage`
- deletion controls, which are currently per source only
- anything added later: pairing, accounts, activation, or analytics

## Publish on GitHub Pages

1. Create a public repository, for example `ranova-tv-website`.
2. Upload `index.html`, `support.html`, `privacy.html`, `terms.html`, `404.html`, `.nojekyll`, and `assets/` to the repository root. You don't need to publish `scripts/` or this README.
3. In Settings > Pages, choose Deploy from a branch, then `main` and `/ (root)`.
4. Use `https://YOUR_USERNAME.github.io/ranova-tv-website/privacy.html` (and `/terms.html`, `/support.html`) in the store listings.
