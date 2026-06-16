---
name: deploy-to-vercel
description: Deploy static or frontend projects to Vercel with CLI-based production deployment, required data-folder inclusion checks, GitHub auto-deploy connection verification, and post-deploy URL validation. Use when the user asks to deploy a site/app/dashboard to Vercel, fix Vercel GitHub auto deployments, confirm source/data files are included, or verify that commits and pushes will update the live Vercel site.
---

# Deploy To Vercel

## Overview

Deploy the current project to Vercel, verify important static assets and data files are available online, and connect the Vercel project to GitHub so future pushes can trigger automatic deployments.

## Workflow

1. Inspect the project and repository state:

```powershell
git status --short --branch
git remote -v
rg --files
```

Check for `.vercelignore`, `.gitignore`, `vercel.json`, framework files, and required data folders such as `source/`, `public/`, `data/`, or user-specified directories. Confirm required files are not ignored.

2. Deploy with an explicit scope when Vercel asks for one:

```powershell
npx vercel --prod --yes
npx vercel --prod --yes --scope <scope-name>
```

If the CLI returns `missing_scope`, use the listed `choices[].name` as `--scope`.

3. Verify deployment output:

Capture the production URL, alias URL, deployment ID, and inspector URL. Prefer the stable alias/custom domain for user-facing delivery.

4. Verify required files online:

```powershell
$base = 'https://example.vercel.app'
@(
  '/',
  '/source/example.csv'
) | ForEach-Object {
  $url = $base + $_
  $r = Invoke-WebRequest -Uri $url -UseBasicParsing
  [pscustomobject]@{ Path = $_; Status = $r.StatusCode; Bytes = $r.RawContentLength }
}
```

For non-ASCII filenames, use the exact repository path in the URL. A `200` response confirms Vercel deployed the file.

## GitHub Auto-Deploy

When the user wants commits to update the Vercel site automatically, connect the Vercel project to the GitHub repository:

```powershell
npx vercel git connect https://github.com/<owner>/<repo>.git --scope <scope-name> --yes
```

Interpret common failures:

- `You need to add a Login Connection to your GitHub account first`: the user must connect GitHub at `https://vercel.com/account/settings/login-connections`.
- `Make sure there aren't any typos and that you have access`: the Vercel GitHub App likely lacks access to that repo. Direct the user to `https://github.com/apps/vercel/installations/new` or `https://github.com/settings/installations`, then have them grant access to the repo.
- If `git ls-remote origin HEAD` fails only inside the sandbox because of network restrictions, retry with escalation before concluding the repo is inaccessible.

After the user completes browser authorization, rerun `vercel git connect` and expect `Connected`.

## Commit And Push

If the user asks to commit and push deployment-related changes, use the `git-commit-push` skill when available. Include all requested changes, especially updated data files, and push to the branch Vercel uses for production, usually `main`.

After pushing, confirm Vercel created a new deployment:

```powershell
npx vercel ls <project-name> --scope <scope-name>
```

## Reporting

In the final response, include:

- Production URL or stable alias.
- Whether required data/static folders were verified online.
- Whether GitHub auto-deploy is connected.
- Any user action still needed for browser-based GitHub or Vercel authorization.
