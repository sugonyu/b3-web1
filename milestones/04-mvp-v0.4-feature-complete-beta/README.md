# MVP v0.4 — Feature-Complete Beta Candidate

Official checkpoint: 🔗 Deliverable 4 — Feature-Complete Beta
Review date: pending
Status: Beta checkpoint recorded — feature completion in progress

Roadmap: [BookLoop Web1 Roadmap](../../docs/bookloop-web1-roadmap.md)

## Goal

Turn the verified Flask/Jinja prototype into a small, reviewable Beta by closing
the remaining user book-management and operator-inspection gaps.

## Current Beta checkpoint

`BookLoop Beta v0.4.0-beta.1` is frozen in the Beta snapshot copied into this
public project folder. The Report workflow is connected from user submission
through Admin review and reporter status tracking.

## Completed at this checkpoint

- [x] User can submit a Report from an authorized borrowing request.
- [x] Admin can see received Reports and the reporter in the queue.
- [x] Admin can open Report detail and change its status.
- [x] Reporter can see their own Report status and detail.
- [x] Admin can use external email links for follow-up outside BookLoop.
- [x] Backend regression suite: `146 passed`.
- [x] Beta snapshot copied into the public project folder.

## Remaining Beta work

- [ ] User can add a book listing.
- [ ] User can edit their own book listing.
- [ ] DB Inspector shows the Report table with safe fields and status.
- [ ] Run focused and full verification after the remaining features.
- [ ] Review browser evidence and decide whether this is feature-complete.

## Explicitly out of current Beta scope

- Automatic email notification service.
- Moderation audit log.
- Payment, card storage, deposits, refunds, or charging.
- React parity before the required Flask/Jinja evidence is stable.

## Snapshot and evidence

- Beta snapshot: `../../snapshots/stages/private-stage-beta-v0.4.0-beta.1/`
- Current journal: [August 12, 2026](../../docs/journal/2026-08-12.md)
- Current board: [Project weekly Kanban](../../docs/project-weekly-kanban-board.html)
- Application source: [`app/`](../../app/)

## Verification boundary

The `146 passed` result verifies the current internal Beta checkpoint. It does not
complete the remaining book-management or DB Inspector Report requirements.
