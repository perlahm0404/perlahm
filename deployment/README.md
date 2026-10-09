Generated: 2026-10-09 07 America/Chicago

# AWS static website launch — October 9, 2026

## Configuration represented here

The owner-authorized launch uses fresh, dedicated Perla resources in the existing shared AWS account: a private regular S3 REST origin in us-east-1, a separate CloudFront distribution, always-sign SigV4 OAC, a viewer-request routing function and an issued ACM certificate covering `perlahm.com` and `www.perlahm.com`. No EC2, database, VPC, IAM role/key, secret, hosted zone or WAF subscription was added for this static website.

The JSON examples preserve the settings used at launch while replacing account-specific identifiers with placeholders. They are configuration references, not a new provisioning system, an infrastructure import or a command to create duplicate resources. Resolve placeholders from approved private deployment metadata before any separately authorized cloud action. Existing deployed resources remain outside infrastructure-as-code state.

- `cloudfront-config.example.json`: HTTP-to-HTTPS redirect, TLS 1.2 minimum, SNI certificate, PriceClass100, HTTP/2, IPv6, GET/HEAD only, compression, managed CachingOptimized and SecurityHeaders policies, no attached WAF ACL, no Perla request access logging.
- `s3-origin-controls.example.json`: all four public-access blocks, BucketOwnerEnforced, SSE-S3/AES256 and OAC signing configuration. Each section corresponds to its own AWS API; the combined file is not one API request.
- `bucket-policy.example.json`: CloudFront GetObject only, conditioned on this site's exact distribution ARN. Do not use an S3 website endpoint or public ACL.
- `cloudfront-spa-routing.js`: extensionless paths return the SPA index; `/portal` and its children return 404; `/thank-you` redirects to `/#contact`; real asset paths retain origin errors.

## Upload and DNS behavior

Upload only `public_html/` contents while retaining relative paths. HTML uses `Cache-Control: public,max-age=60`; hashed JS/CSS use `public,max-age=31536000,immutable`; other assets use `public,max-age=86400`. AWS object content types must match extensions. A future changed file must also update the release manifest and receive appropriate cache treatment/invalidation; a Git commit alone does not update S3.

Namecheap nameservers remain in place. Apex is an ALIAS and www is a CNAME to the new distribution. ACM validation CNAMEs remain for renewal. Existing Google MX, SPF/DKIM/DMARC, verification and portal-host records were preserved. DNS rows, resource IDs, certificates, private metadata and root-session records remain outside this public repository. The old Namecheap files/subscription were preserved for rollback; no cancellation is recorded here.

Apache `.htaccess` is omitted because CloudFront handles routing. The old standalone `portal/index.html` is omitted from the public payload; the function rejects that route. The stale JS bundle is replaced by the launch bundle and index reference.

## Dated validation — PROVEN within these checks

The original launch readback verified all 34 CloudFront response bodies against SHA256, including the nine replacement images. The S3 public-access blocks, ownership, encryption, distribution-bound policy and deployed CloudFront configuration were read back. Anonymous direct S3 returned 403. Home, insights, representative service routes and an article rendered; asset errors and retired portal denials were checked. Security headers included HSTS, nosniff and SAMEORIGIN.

The public www hostname returned HTTP 200 with valid TLS. The new apex authoritative DNS target also returned HTTP 200 with valid TLS, and a public resolver returned AWS addresses. Some local cached apex DNS still reached the old host with its expired certificate at the observation; universal DNS propagation is not asserted. Browser security warnings and certificate validation were not bypassed. The candidate's fresh checks are recorded on its eventual PR checkpoint, rather than represented by this historical readback.

## Shared-account security impact — SUPPORTED with explicit limits

Current Foundation scope/access/supplier guidance was checked at accepted revision `6ace4b7ba8e346ab9192b214926db9515e218171`. Dedicated Perla resources and a private origin reduce accidental cross-use; the static website has no configured CM database/secret/application connection. Before/after observed properties of the five existing CloudFront distributions matched, and existing account CloudTrail remained logging with successful post-launch delivery. No CM logging, alarms, IAM, database or governance configuration was changed by the launch.

The site shares account administration with CredentialMate. The approved launch used temporary root CLI access, whose local login cache was removed afterward; a fresh CLI identity request was denied. This does not establish a least-privilege recurring publisher. Before routine publishing, the owner should approve a site-scoped identity and reconcile actual shared account/admin reliance in Foundation's existing scope/risk/supplier process. No role/access expansion or risk acceptance is made by this PR.

Perla distribution access logging is disabled. Account CloudTrail management events do not establish complete visitor logs, alerts, retention or operating review. Applicable monitoring responsibility and formal scope treatment remain UNVERIFIED. Marketing email and Calendly are not an approved credential-document intake path. No auditor-approved exclusion, SOC 2 readiness completion, certification or provider-collection restart is established.

Foundation owns its application/security/service boundary. This dated website assessment changes no Foundation governance and does not lift its held provider or real-data gates.

## Authoritative references

- [Foundation scope at the inspected revision](https://github.com/Credentialmate/CM-Foundation/blob/6ace4b7ba8e346ab9192b214926db9515e218171/docs/compliance/soc2/SCOPE.md)
- [Private S3 origins and CloudFront OAC](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
- [CloudFront monthly free allowances](https://aws.amazon.com/cloudfront/faqs/)
- [AWS account isolation guidance](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_multi_accounts.html)
