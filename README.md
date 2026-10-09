Generated: 2026-10-09 07 America/Chicago

# Perla public website

This repository contains the built static publication for **perlahm.com**. The October 9 release restores nine missing editorial images, replaces the unconfigured contact form with email and the existing discovery-call link, and captures the dedicated S3/CloudFront deployment used for the authorized launch.

`public_html/` is the exact 34-file AWS upload payload, 4,632,783 bytes. The original React/Vite source project is not present in this repository; this release updates the existing built bundle. A source rebuild cannot be claimed or reproduced from these files. The deployed bundle retains unused third-party library code, but no configured Supabase URL/key, contact submission handler or customer portal is enabled.

- Public site: https://www.perlahm.com/
- Contact: `mailto:info@perlahm.com`
- Existing booking destination: https://calendly.com/mylaiviet/perla-discovery-call
- Hosting configuration and dated readback: [deployment/README.md](deployment/README.md)
- Exact file integrity: [deployment/site-manifest.json](deployment/site-manifest.json)
- Image provenance: [deployment/IMAGE-ASSETS.md](deployment/IMAGE-ASSETS.md)

Validate locally without cloud credentials:

```sh
python3 scripts/verify-site.py
python3 scripts/verify-site.py --url https://www.perlahm.com/
node --check deployment/cloudfront-spa-routing.js
```

The URL option performs only public HTTPS reads, keeping certificate validation enabled. It verifies response bodies against the manifest; it does not change hosting or DNS. The verifier uses only the Python standard library.

This release records a website already launched with explicit owner authorization. A PR merge does not redeploy it. The separate AWS-spend PR contains the dated account inventory and cost assumptions; this website repository does not become a financial or SOC 2 status register.
