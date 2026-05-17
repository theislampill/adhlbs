# ADHLBS Publication Gate - 2026-05-17

Public provenance remains partial/not-run because this pass did not commit, push, tag, deploy, publish a release, or check the live Pages artifact.

| Gate | Status | Evidence | Next action |
| --- | --- | --- | --- |
| Commit hash embedded or source-content marker justified | PARTIAL | docs/index.html manifest uses deterministic-source-content with source_hash and fallback_dirty_tree_marker because no post-push commit hash was embedded in this local correction pass. | After an authorized commit, rebuild or record the committed artifact hash and verify the manifest against that commit. |
| GitHub Actions pass after push | NOT RUN | No push was performed in this pass; local workflow-equivalent commands were run only. | After authorized push, inspect the GitHub Actions run for the pushed commit and record the passing run URL. |
| Live Pages URL checked | NOT RUN | No deploy or live Pages verification was performed in this pass. | Open the GitHub Pages URL after deployment and record status, timestamp, and observed artifact identity. |
| Live HTML manifest matches repo artifact | NOT RUN | No live HTML was fetched or compared against docs/index.html. | Fetch the live Pages HTML, parse adhlbs-build-manifest, and compare it to the repository artifact manifest. |
| Live source/copy surfaces match generated artifact | NOT RUN | No live source table or copy surfaces were compared to the generated local artifact. | Run a live Pages browser smoke that checks source URLs are inert and copy surfaces match the generated local HTML. |
