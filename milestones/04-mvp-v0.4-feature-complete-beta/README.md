# MVP v0.4 — Feature-Complete Beta Candidate

Official checkpoint: 🔗 Deliverable 4 — Feature-Complete Beta
Review date: August 20, 2026
Status: D4 presentation delivered — final live walkthrough Wednesday, August 26 at 9:00 AM; GitHub closeout Friday, August 28 at 11:59 PM

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
- [x] Deliverable 4 presentation delivered and major feature scope frozen.

## Final-week closeout · August 24–28, 2026

- [x] Monday: confirm stable startup, demo accounts/data, routes and the complete BorrowRequest flow.
- [x] Tuesday: rehearse the final browser/database evidence order and record known limitations.
- [ ] Wednesday at 9:00 AM: deliver Presentation 5 as a live project walkthrough; no separate PPT is required.
- [ ] During the walkthrough: explain the biggest development Challenge and Surprise.
- [ ] Friday at 11:59 PM: submit the final GitHub repository and documentation; later changes do not count for grading.
- [ ] After submission: record official feedback, known limitations and the next-block handoff.

No major feature additions are planned for the final week. Only presentation-blocking defects
may change the frozen Beta baseline.

## Teacher's final submission guidance

The final presentation is a client-facing walkthrough of the running project,
not a separate slide-deck deliverable. The final repository handoff must make it
possible for another developer to continue the project without the original
author. README must clearly cover:

- installation;
- how to run the project;
- requirements;
- main features.

Keep the development journal maintained through the deadline. Existing
medium-fidelity wireframes are sufficient; a new high-fidelity wireframe is not
required. The test checklist is used during the walkthrough and does not need a
separate README section.

## Explicitly out of current Beta scope

- Automatic email notification service.
- Moderation audit log.
- Payment, card storage, deposits, refunds, or charging.
- React parity before the required Flask/Jinja evidence is stable.
- Unconfirmed post-presentation suggestions before the Deliverable 4 completion gates.

## Snapshot and evidence

- Private lab Beta4 snapshot: frozen post-presentation bugfix and pre-feedback D4 baseline
- Current journal: [August 22, 2026 — teacher closeout guidance](../../docs/journal/2026-08-22.md)
- Current board: [Final-week Project Kanban](../../docs/project-weekly-kanban-board.html)
- Final demo entry point: [Deliverable 4 presentation evidence](../../docs/presentations/deliverable-04/index.html)
- Application source: [`app/`](../../app/)

## Verification boundary

The recorded backend suite, D4 presentation and Beta4 snapshot verify the
current development direction. The live walkthrough at 9:00 AM on August 26 is
the presentation checkpoint; the final GitHub and documentation deadline is
11:59 PM on August 28. The public release claim must stay limited to browser and
database behavior that is actually demonstrated and verified.
