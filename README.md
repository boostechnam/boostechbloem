# Boostech Bloemfontein

Static website prepared for https://boostechbloem.com/.
The complete public website is in `dist/`, including all images.
No build step or environment variables are required.
Google Analytics measurement ID: `G-SJ8RNZBRSJ`.

## Cloudflare Workers deployment from GitHub

1. In Workers & Pages, create an application and import the GitHub repository.
2. Use Worker name `boostechbloem` and production branch `main`.
3. Use the repository root as the root directory, leave the build command empty,
   and set the deploy command to `npx wrangler deploy`.
4. Deploy and check the returned workers.dev URL, the logos, Ranger artwork,
   navigation anchors and FAQ panels.
5. Once `boostechbloem.com` is active in the Cloudflare account, open the Worker's
   Settings → Domains & Routes and add `boostechbloem.com` as a Custom Domain.
6. Add `www.boostechbloem.com` as a Custom Domain too. Configure a Cloudflare
   redirect from www to https://boostechbloem.com, preserving path and query.
7. Verify HTTPS on both hostnames before redirecting the old Afrihost website.

The configuration deploys only `dist/`. The original Sites publication is
unchanged until separately published there. Its project metadata stays in the
original source checkout and is not included in the GitHub export.

## Articles and branch contacts

The article hub is `/news-advice/`, with 11 complete articles adapted from the
Namibia and Western Cape sites. Header navigation and homepage cards link to it.
Enquiries use a required vehicle form with a free-text location. Visitors choose
WhatsApp, Gmail in a browser, or their configured email app, review the prepared
message, and send it themselves. The email button reveals explicit options so
visitors without a configured mail app can use Gmail. No email is sent by the site.
Branch phone numbers and email addresses are not displayed on the pages.

To update article text, edit `content/articles.json` and run:

```sh
python scripts/build_articles.py
```

Commit the source data, generator and generated `dist/` files together. Cloudflare
continues deploying the static `dist/` folder without requiring Python at build time.
Photographs, vehicle logos and videos reuse media hosted on the existing Boostech
Namibia and Western Cape domains; maintain those shared media URLs when moving files.
Network customer stories and Australian builds retain their original context.

## References

- https://developers.cloudflare.com/workers/static-assets/get-started/
- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/

## ECU tuning page

The workshop ECU tuning page is `/ecu-remapping/`. Edit `content/ecu-page.html` and
`scripts/build_ecu.py`, then run `python3 scripts/build_ecu.py`. It reuses the
homepage navigation and vehicle enquiry form. Workshop photos with blurred
registration plates are served locally from `dist/assets/ecu/`.
