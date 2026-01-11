# Repository History Purge (January 2026)

What I did
- Purged all blobs larger than 10MB from the repository history using `git-filter-repo`.
- This removed large media files (video, images, exports) that were causing excessive repo size and prevented pushes (notably a ~1.8GB webm file).
- Repacked the repository and ran garbage collection to reclaim space.
- Force-pushed the cleaned refs to `origin` (this rewrote history on `main` and affected branches).

Why
- Large media files should not be stored directly in the repository. They bloat the repo and make cloning/pushing difficult.
- This project will not use Git LFS per maintainers' preference.

What was removed (examples)
- `downloads/JAREDSNOTFUNNY Feat The Roanoke Pisser #12_YC-oohVCGwA.webm` (~1.8GB)
- Multiple `downloads/*` and `exports/shorts/*` video and image files

Important: how to sync (for all collaborators)
1. Backup any local work not committed (use `git stash push -m "backup"` or create a patch).
2. Fetch the cleaned refs and hard-reset your local branches to origin:

```bash
git fetch origin --prune
git checkout main
git reset --hard origin/main
```

3. For local feature branches based off old history, rebase onto `origin/main` or re-create them:

```bash
# Option A: rebase
git checkout feature/your-branch
git rebase origin/main

# Option B: create a new branch from updated main
git checkout -b feature/your-branch-2 origin/main
# re-apply changes (cherry-pick, copy files, or use stash)
```

4. If you have local untracked media files that you no longer want, you can remove them safely:

```bash
git clean -fdX
```

Notes & follow-ups
- No Git LFS was used; if you need long-term storage for media, use an external bucket (S3, Cloudflare R2) or an artifact storage workflow.
- I added a small script (`scripts/check_no_media_in_commit.py`) you can use as a pre-commit hook to prevent accidentally committing media files in the future.
- The cleanup may have triggered GitHub security scanning and CI runs; check the Actions tab for any follow-up jobs.

If you want, I can:
- Add an automated pre-commit hook configuration (e.g., `.pre-commit-config.yaml`) to enforce the check, or
- Migrate selected files to an external storage and add helper upload scripts.

If you'd like, I can also open a short PR / changelog entry summarizing this work for maintainers to review.
