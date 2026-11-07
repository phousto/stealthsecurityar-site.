# stealthsecurityar.com

Static site for Stealth Security, LLC.

- Edit page text in `src/content.py`, styles in `src/assets/site.css`.
- Build: `python3 src/build.py` (outputs `public/`).
- Hosting: Cloudflare Pages or GitHub Pages, publish directory `public`.
- Quote form: set `FORM_ENDPOINT` at build time to post leads (e.g. a StealthOP endpoint). Without it the form opens the visitor's email app addressed to support@.
- URLs match the previous Airo site so search rankings carry over.
