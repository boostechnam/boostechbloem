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

## Content still awaiting branch details

The existing design, logos and copy are preserved. The contact section and footer
still state that branch details are pending. Add Pieter's confirmed contact and
booking details when supplied; they have not been invented during migration.

## References

- https://developers.cloudflare.com/workers/static-assets/get-started/
- https://developers.cloudflare.com/workers/ci-cd/builds/configuration/
- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
