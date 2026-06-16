# Deployment Setup

## Stack
- Astro 6 (static site generator)
- Cloudflare Pages (hosting, auto-deploys on push)
- GitHub: Nel-Etienne/Nel
- Obsidian Git plugin (auto-sync from vault)

## Cloudflare Pages Settings
When connecting the GitHub repo in the Cloudflare Pages dashboard:
- **Framework preset**: Astro
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Root directory**: `site`
- **Node.js version**: 22

Set these environment variables in CF Pages:
- NODE_VERSION=22

## Obsidian Git Plugin Setup
1. Open Obsidian → Settings → Community Plugins → Browse → search "Obsidian Git" → Install & Enable
2. Settings → Obsidian Git:
   - Auto pull interval: 0 (disabled)
   - Auto commit-and-sync interval: 5 (minutes)
   - Commit message: `vault: {{date}} {{hostname}}`
   - Push on auto commit: ✅ enabled
   - Pull before push: ✅ enabled

## Custom Domain
In Cloudflare Pages → project → Custom domains → add `etiennenel.com`
Then in Cloudflare DNS, add a CNAME record pointing etiennenel.com to your CF Pages URL.

## Adding New Content Sections
To publish a new vault folder (e.g. `Marathon Training/`):
1. Remove it from `.gitignore` (or don't add it)
2. Add a new collection in `site/src/content.config.ts`
3. Create pages in `site/src/pages/research/<folder-name>/`
4. Commit and push — CF Pages rebuilds automatically

## Local Development
```bash
cd site
npm install
npm run dev   # http://localhost:4321
```
