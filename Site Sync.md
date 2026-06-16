---
type: operations
tags: [site, automation, reference]
---

# Site Sync — Auto-push to GitHub

The Python script below watches this vault for changes and automatically commits + pushes to GitHub, which triggers Cloudflare Pages to rebuild etiennenel.com.

## Script location

```
/Users/etienne/Documents/EtienneOBS/site/vault_sync.py
```

## How it runs — Mac launch agent

The script runs automatically as a Mac launch agent — it starts on boot and runs silently in the background. No terminal needed.

Launch agent plist: `~/Library/LaunchAgents/com.etiennenel.vaultsync.plist`
Log file: `~/Library/Logs/vaultsync.log`

## How it works

- Watches all `.md` files in this vault
- Waits 30 seconds after the last save (debounce) before pushing
- Auto-commits with a timestamp: `vault: 2026-06-16 14:30`
- Pushes to GitHub → Cloudflare Pages rebuilds → etiennenel.com is live within ~60 seconds

## Useful commands

```bash
# Check it's running (should show a PID)
launchctl list | grep vaultsync

# Watch the live log
tail -f ~/Library/Logs/vaultsync.log

# Stop it
launchctl unload ~/Library/LaunchAgents/com.etiennenel.vaultsync.plist

# Start it again
launchctl load ~/Library/LaunchAgents/com.etiennenel.vaultsync.plist
```

## If the push fails

Most likely the GitHub credentials need refreshing. Run:

```bash
gh auth login
```

Choose GitHub.com → HTTPS → Login with browser → log in as `Nel-Etienne-Nel`.

Then restart the script.

## GitHub repo

https://github.com/Nel-Etienne-Nel/personal-wiki

## Cloudflare Pages

Log in at dash.cloudflare.com → Pages → personal-wiki

Build settings:
- Build command: `npm run build`
- Output directory: `dist`
- Root directory: `site`
- Node.js: 22

## Adding new content

- **New lesson in existing section**: just create a `.md` file in `Cleef Notes/` with frontmatter — it appears on the site automatically on next push
- **New section entirely**: see `site/DEPLOYMENT.md` for the 3-step process

## Related

- Full deployment guide: `site/DEPLOYMENT.md`
- Astro site: `site/`
- Live site: https://etiennenel.com
