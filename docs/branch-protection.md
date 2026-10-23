
# Branch Protection Rules

The `main` branch is protected to maintain code quality, prevent accidental
changes, and ensure that contributions are reviewed before they are merged.

## Required Rules

1. **Require a pull request before merging:** All changes must be submitted
   through pull requests instead of being pushed directly to `main`.

2. **Require at least one approval:** Another team member must review and
   approve a pull request before it can be merged.

3. **Dismiss stale approvals:** New changes invalidate previous approvals
   so reviewers can reassess the updated code.

4. **Require status checks to pass:** Automated checks must pass before
   merging. This will be enabled when the CI workflow is configured.

5. **Require branches to be up to date:** Pull requests must include the
   latest changes from `main` before merging.

6. **Require conversation resolution:** Review comments and requested
   changes must be resolved before merging.

7. **Include administrators:** Repository administrators must follow the
   same rules, preventing routine bypasses of the protections.

## Maintenance

The team should review these settings when new CI checks are introduced
and verify that the required checks match the actual workflow names.
