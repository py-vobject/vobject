Contributing to vObject
=======================

Welcome, and thanks for considering contributing to vObject!

**_This document is an incomplete draft_**

Contributions can take many forms, from coding major features, through
triaging issues, writing documentation, assisting users, etc, etc. You
can, of course, just dive right in, but it's generally a good idea to
open an issue (if the contribution addresses a problem) or a discussion
to discuss your plans first. This avoids duplicate effort, and builds
the community of contributors.

In all interactions, contributors should be polite, kind, and respectful
of others. Remember that not everyone lives in the same country, speaks
English as their native language, or has the same level of experience and
confidence.

Python Code
-----------
vObject is licensed under the Apache 2.0 License, and any code or
documentation can only be accepted under those terms. You do _not_ need
a formal statement of origin, and are not required to sign over your
copyright.

All new code should adhere to the PEP-8 conventions, with some exceptions
possible when extending older APIs for consistency with what's already
there.

After a discussion (see #1), the project decided on a support policy:
we will maintain support for a CPython version for one year after it
becomes unsupported.  In practice, that means two things:
- Every November, we drop the oldest supported release
- Language feature usage and tools should target the oldest supported
  release.

Note that the 0.9.x releases continue to support Python 2.7 (!): 1.0
and later follow the "plus one year" policy.

With the possible exception of major releases, all contributions must
maintain the existing API's syntax and semantics.

Dev Setup
---------
The vast majority of development work should target the _master_
branch.  When working there, it's recommended that you use `uv` (if
you would rather do something else, you'll have to figure it out
yourself).

1. Install
   [uv](https://docs.astral.sh/uv/getting-started/installation/) (if
   not already done)

1. Install the developer tools (once):
   ```
   uv tool install pre-commit --with pre-commit-uv
   uv tool install tox --with tox-uv
   ```

1. Enable the `pre-commit` hook in your clone, and run it once
   ```
   pre-commit install
   pre-commit run --all-files
   ```

1. Run tests on demand:
   ```
   tox -p
   ```

Release Process
---------------
0.9.x Branch
- Run tests with CPython 2.7
- Run tests with current minimum supported CPython 3
- Run tests with current latest CPython 3
- Update CHANGELOG.md
- Check VERSION in vobject/base.py
- Tag release like "v0.9.x"
- Make source distribution `python setup.py sdist`
- Make binary distribution `python setup.py bdist_wheel`
- Upload both dists (from `dist/`) to PyPI.org with `twine`
- Create release from tag at GitHub, and copy CHANGELOG notes to release notes
- Update release notes list on `py-vobject.github.io`

1.x and later branches
- Run tests with `tox -p`
- TBC
