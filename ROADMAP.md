Roadmap
=======

Immediate tasks, starting early 2024

- [ ] Apply all open good PRs
  - Add unit test coverage where missing
  - Add comments to _eventable_ repo, so people can see they're being
    fixed in the _py-vobject_ project
- [ ] Do a pass through the open issues at _eventable_
  - Fix anything easy
  - Copy the issue over to _py-vobject_ for bigger items that can't be
    fixed right away
- [ ] Renumber _master_ for 1.0.x
  - And rename to `main` while we're here?
- [ ] Set up GitHub issue triage, etc
  - Group members and permissions
  - Labels
  - Templates
  - Pinned discussions posts
  - Revamped README
  - CoC?
- [ ] Talk to downstream users about pain-points
  - Beyond just lack of maintenance
  - eg. Radicale, Debian

### Bigger projects

These should be prioritised once the basic maintenance and revamping work
has been completed.

- [ ] Create new Sphinx-based programmer's guide document
  - Publish via readthedocs
  - Move example code out of README.md
  - Publish automagically via GitHub Actions
- [ ] Begin removal of 2.x code
  - In particular, clean up `bytes` vs `str` everywhere
  - Remove `six`
  - Remove various `import` compatibility hacks
- [ ] Robust vCard 4.0 support
- [ ] Parsing performance
- [ ] Unit-test coverage
