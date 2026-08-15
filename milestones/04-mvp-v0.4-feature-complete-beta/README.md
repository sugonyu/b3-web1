# MVP v0.4 — Feature-Complete Beta Candidate

Official checkpoint: 🔗 Deliverable 4 — Feature-Complete Beta
Review date: August 20, 2026
Status: Week 4 planned — Beta v0.4.0-beta.4 development baseline active

Roadmap: [BookLoop Web1 Roadmap](../../docs/bookloop-web1-roadmap.md)

## Goal

Turn the verified Flask/Jinja prototype into a small, reviewable Beta by closing
the remaining user book-management and operator-inspection gaps.

## Current Beta checkpoint

`BookLoop Beta v0.4.0-beta.4` is the D4 starting baseline. It preserves the D3
delivery state plus the verified post-presentation UI bugfix, before unconfirmed
feedback features. The frozen snapshot remains in the private lab; the public
repository contains the selectively synchronized application source.

## Completed at this checkpoint

- [x] User can submit a Report from an authorized borrowing request.
- [x] Admin can see received Reports and the reporter in the queue.
- [x] Admin can open Report detail and change its status.
- [x] Reporter can see their own Report status and detail.
- [x] Admin can use external email links for follow-up outside BookLoop.
- [x] User can add, view, edit, change availability, and safely delete their book listing.
- [x] DB Inspector shows the Report table with privacy-safe fields and status.
- [x] Backend regression suite: `159 passed`.
- [x] Private lab snapshot created for Beta v0.4.0-beta.3.
- [x] Public application source synchronized from the lab without a public code snapshot.
- [x] Deliverable 3 presentation delivered and public closeout recorded.
- [x] Unofficial post-presentation feedback recorded separately from official grading.
- [x] Beta v0.4.0-beta.4 post-presentation bugfix snapshot selected as the D4 development baseline.

## Remaining Beta work

- [ ] Monday: complete remaining browser evidence and decide whether Beta is feature-complete.
- [ ] Tuesday: audit authentication, authorization, forms, validation, major errors, responsive layouts, accessibility and the test checklist.
- [ ] Wednesday: finish the README draft, setup instructions, known issues and D4 demonstration order.
- [ ] Thursday: demonstrate all required workflows, record feedback and freeze major feature scope.

## Explicitly out of current Beta scope

- Automatic email notification service.
- Moderation audit log.
- Payment, card storage, deposits, refunds, or charging.
- React parity before the required Flask/Jinja evidence is stable.
- Unconfirmed post-presentation suggestions before the Deliverable 4 completion gates.

## Snapshot and evidence

- Private lab Beta4 snapshot: frozen post-presentation bugfix and pre-feedback D4 baseline
- Current journal: [August 13, 2026](../../docs/journal/2026-08-13.md)
- Current board: [Project weekly Kanban](../../docs/project-weekly-kanban-board.html)
- Application source: [`app/`](../../app/)

## Verification boundary

The recorded backend suite and D3 presentation verify the integrated product;
the Beta4 snapshot adds the post-presentation UI bugfix baseline. Browser
evidence, the D4 quality audit, official feedback and the release decision remain
before calling it a feature-complete public release.
