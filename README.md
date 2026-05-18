# oameye.github.io

Personal website of Orjan Ameye, built with the
[Hugo Blox academic-cv](https://hugoblox.com/templates/academic-cv/) template
on top of the [HugoBlox kit](https://github.com/HugoBlox/kit).

## Local development

Requirements: Hugo Extended `>= 0.161.1`, Node 22, pnpm.

```bash
pnpm install
hugo server -D
```

## Build

```bash
pnpm install
hugo --gc --minify
```

The output is generated into `public/`.

## Deployment

The site is deployed to GitHub Pages via `.github/workflows/deploy.yml` on every
push to `main`. Pull requests trigger a build-only check via
`.github/workflows/build.yml`.
