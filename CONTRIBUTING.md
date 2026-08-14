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

The supported Python versions are discussed in #1, and care needs to be
taken to not use features that are unavailable in the older supported
releases.

With the possible exception of major releases, all contributions must
maintain the existing API's syntax and semantics.

Dev Setup
-

1. Enable pre-commit hook and run manually.
   ```
   pre-commit install
   git add . && pre-commit run
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
