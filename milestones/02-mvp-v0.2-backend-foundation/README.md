# MVP v0.2 — Backend Foundation and First Vertical Slice

Official checkpoint: 🗄️ Deliverable 2 — Backend and Database
Review date: August 6, 2026
Status: Ready to begin Monday, August 3

## Goal

Demonstrate a reproducible Flask backend with relational persistence,
validation, and one complete database-backed create/read workflow.

## Required Evidence

- [ ] Application starts correctly
- [ ] Environment configuration works without committed secrets
- [ ] Database can be created reproducibly
- [ ] Core models exist
- [ ] Model relationships function
- [ ] Authentication functions where the selected workflow requires it
- [ ] At least one create workflow works
- [ ] At least one read workflow works
- [ ] Validation success and failure are demonstrated
- [ ] Data persists in the database
- [ ] Git history shows meaningful progression

## Monday Start

1. Verify the current Flask startup and test commands.
2. Verify database creation and inspect the current model relationships.
3. Select one narrow vertical slice: create a borrow request and read its current
   state.
4. Define who may create and read that request before adding interface features.

## Scope Boundary

The Week 2 slice supports BookLoop's privacy direction but does not attempt to
finish the whole moderation system.

Included:

- Flask application and configuration
- relational models and persistence
- server-side validation
- authorization boundary needed by the selected workflow
- one create/read workflow

Not included in Deliverable 2:

- payment integration, card storage, deposits, refunds, or charging
- a complete reporting and Admin View implementation
- social-media or donation integrations
- broad frontend redesign

## Evidence Plan

Add evidence only after it exists and is verified. Preserve reproducible commands,
test results, database schema evidence, and the selected workflow under this
milestone. Do not copy secrets, real user data, dependency folders, or an
unverified private-lab snapshot.

## Thursday Definition of Done

- The application and database start from documented steps.
- The selected create/read workflow persists valid data.
- Invalid or unauthorized input is rejected visibly.
- Model relationships and authentication requirements can be explained.
- Required evidence and meaningful Git progression are ready for review.
