---
name: publish-pr-screenshots
description: Publish approved erArk pull-request screenshots without a browser by storing them on the public fork's append-only assets branch and embedding commit-pinned raw.githubusercontent.com URLs. Use when an upstream PR needs before/after images, when replacing local or Release Asset image links, or when migrating PR evidence away from a separate asset repository.
---

# Publish PR Screenshots

Publish screenshots through `meower-z/erArk-fork`'s orphan `assets` branch. Use the same commit-pinned `raw.githubusercontent.com` URL for the rendered image and its link so a click opens the original image instead of downloading a Release Asset or navigating to a repository page.

## Guardrails

- Obtain approval for the exact screenshots before uploading them and separate approval for each push and PR edit.
- Visually inspect every image. Exclude saves, credentials, private mods, debug-only artifacts, and unrelated evidence.
- Immediately before each outward action, confirm `gh auth status` has `meower-z` active and confirm `meower-z/erArk-fork` is public with parent `Godofcong-1/erArk`.
- Keep screenshots off the source PR branch and never push them to upstream. Do not open a PR from `assets`.
- Treat `assets` as append-only: do not force-push, rewrite, or delete it. Existing PRs depend on old commit SHAs remaining reachable.
- Do not use GitHub Release Assets: their download response forces attachment download. Do not create a helper repository or use browser-cookie attachment upload for this workflow.
- Preserve the PR's current base, head, Draft/ready state, title, commits, and changed-file scope unless the user separately requests a change.

## Publish Images

1. Choose a stable path. Prefer `pr-<number>/<descriptive-name>.png`; when the PR number does not exist yet, use `pr-<branch-slug>/` and keep that path after PR creation.
2. Work in a disposable clone. If `assets` exists, clone that branch alone. If it does not exist, clone with no checkout and create an orphan `assets` branch.
3. Copy only the approved images. Verify their format, dimensions, hashes, and the complete staged file list.
4. Commit with `meower-z <299913659+meower-z@users.noreply.github.com>`. Confirm both author and committer identities and confirm the tree contains only intended asset changes.
5. Re-check the active GitHub account, then push `assets` to `origin` without force.
6. Record the full asset commit SHA and construct each immutable URL:

```text
https://raw.githubusercontent.com/meower-z/erArk-fork/<full-asset-commit-sha>/<path>
```

Use an explicit linked image so GitHub renders the screenshot and clicking it opens the raw original:

```markdown
[![descriptive alt text](<raw-url>)](<raw-url>)
```

For before/after evidence, use a two-column table only when both images remain readable at that width.

## Update The PR

1. Read the live PR body and metadata immediately before editing. Work from that body so concurrent user changes are preserved.
2. Replace only local, Release Asset, or obsolete screenshot URLs. Keep all unrelated prose unchanged.
3. Render the proposed Markdown through GitHub before editing and inspect the generated `href` and `src`; both must equal the intended raw URL.
4. Re-check the active account, then update only the PR body. If `gh pr edit` fails while querying classic Projects, use the pull-request REST endpoint with only the `body` field:

```bash
gh api --method PATCH repos/Godofcong-1/erArk/pulls/<number> \
  --raw-field body="$(< /tmp/<final-pr-body>.md)"
```

5. Read the PR back with the full HTML media type. Confirm every rendered image has the expected raw `src` and `href`, and confirm no local paths or obsolete host URLs remain.

## Verification Gate

Before reporting completion, confirm all of the following from live state:

- Each raw URL returns HTTP 200 with `Content-Type: image/png` or the correct image type and no `Content-Disposition: attachment`.
- The rendered PR body displays every approved image and links each image to the same raw URL.
- The PR's base, head, Draft/ready state, commit identity, and changed-file count match the pre-edit values.
- The `assets` branch contains the uploaded files and the URLs use the full commit SHA rather than the movable branch name.

When migrating away from another host, update and verify the PR first. Delete the old repository, release, or asset only after the PR has no remaining reference to it and only when the user explicitly authorizes deletion.
