# Public action staging

This repository exercises a small set of pinned GitHub Actions against an
independent synthetic Python project. It contains no private source files or
research data. Its checks qualify this fixture and cannot establish whether a
different repository's protected checks or full assurance suite have passed.

The privacy action runs its own pinned scanners; the runtime smoke test checks
CPython and environment isolation; dependency review runs on pull requests.
The fixture includes one pinned public package to exercise a dependency change.
