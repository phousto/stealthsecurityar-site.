# stealthsecurityar.com

Static site for Stealth Security, LLC.

- Edit page text in `src/content.py`, styles in `src/assets/site.css`.
- Build: `python3 src/build.py` (outputs `public/`).
- Hosting: Cloudflare Pages or GitHub Pages, publish directory `public`.
- Quote form: posts leads to StealthOP at `https://app.stealthsecurityar.com/api/leads` (source `stealthsecurityar`, plus any `utm_*` from the page URL). Override with `FORM_ENDPOINT` at build time; set `FORM_ENDPOINT=""` to fall back to opening the visitor's email app addressed to support@. If the post fails, visitors are told to call or email.
- URLs match the previous Airo site so search rankings carry over.
