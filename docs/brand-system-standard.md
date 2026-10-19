# Brand system standard

Status: v0.1 review criteria. These are original acceptance criteria, not a certification.
Scope: reusable quality criteria for brand guides, not permission to copy another brand's artwork, typography, colors, text or proprietary assets.

## Sources and adopted principles

| Official source | Adopted principle | Required evidence |
|---|---|---|
| [Dropbox](https://brand.dropbox.com/framework) | Connect strategic principles, voice and visual execution | Brand intent, audience, principles, channel examples and a rationale for decisions |
| [IBM](https://www.ibm.com/design/language/iconography/ui-icons/design/) | Specify icon geometry and optical consistency | Grid, padding, stroke, corners, caps, sizing, alignment and rendered examples |
| [Atlassian](https://atlassian.design/foundations/iconography) | Treat icons as functional communication | Meaning, labels, states, size and contrast rules; distinguish UI icons from brand marks |
| [Spotify](https://developer.spotify.com/documentation/design) | Define distinct logo and symbol use cases | Minimum size by medium, clear space, color variants and incorrect usage; Spotify source is an integration guide |
| [Slack](https://slack.com/media-kit) | Make approved assets easy to locate and use | Asset index, intended use, formats, version, approval status and canonical files |

These are our synthesized acceptance criteria, not endorsements or certifications by the referenced brands. Do not inherit their exact dimensions, palettes or icon designs.

## Release gates

1. **Identity fidelity.** One approved reference and one geometric master. Compare at equal scale. Every derivative preserves the approved paths unless an explicitly labeled optical variant is approved. Approval of a mockup is not approval of reconstructed paths.
2. **Portable typography.** Specify family, weight, kerning and tracking. Production wordmarks use approved outlined paths or an approved embedded-font export. A fallback font cannot silently change the mark. Keep editable source separately.
3. **Responsive mark.** Review 16/24/32/48/64 px on light, dark and monochrome surfaces at native sizes. Define validated minimums, avatar crop and optical small-size exceptions. Do not call a high-resolution lockup a favicon.
4. **Color and contrast.** Include numerical color values, background matrix and functional text/icon contrast. Logo treatment is evaluated separately from UI accessibility. Print colors and embroidery thread require physical proofs.
5. **UI iconography.** Define a fixed base grid, intended sizes, stroke behavior, corners/caps, source names/version/license, labels and state semantics. Use familiar metaphors. Export the approved set rather than only placing specimens in a guide.
6. **3D identity.** Derive geometry from the approved flat master. Record width normalization, extrusion, bevel, material, lighting, camera projection and angle conventions. Label every rendered view with actual model parameters. Independent image generations are concept references, not measurable views of one model.
7. **Applications and production.** Document front/back garment placement, logo dimensions and separation, website placement, printing/embroidery method and physical proof status. Label generated visualizations clearly. Never infer production readiness from a mockup.
8. **Guide integrity.** Written rules agree with rendered samples. Verify PDF page breaks, clipping, images and text after final export. Keep historical examples in an explicit archive. Provide a short operational guide before long supporting material.
9. **Governance.** Each asset has an owner, version, status and intended use. Maintain decision records and changelog. Unknown approval, licensing, repository destination, remote settings and history remain UNKNOWN until verified.

## 3D view sheet

Use [the 3D specification template](../templates/3d-spec.md). Sampling angles are proposed defaults, not reconstructed measurements or an approved animation range. Derive all views from one approved model.

## Evidence vocabulary

- VERIFIED: inspected artifact or measured result, with exact evidence.
- MISSING: absent within the inspected scope, with inventory/search evidence.
- UNKNOWN: approval, physical behavior or external state has not been checked.

Repository tooling checks are separate from visual/production checks. A documentation folder does not require an application manifest, empty environment file, invented license or a new remote repository.
