# Proposed Data Model

This folder contains the proposed models, fields, relationships and validation
rules for the BookLoop Deliverable 1 proposal.

Expected evidence:

- one primary content model
- one supporting model
- a user model where appropriate
- fields and data types
- primary and foreign keys
- relationship cardinality
- validation constraints

Current direction:

- `User` stores the minimum member identity and general area.
- `BookListing` stores a book and its owner.
- `BorrowRequest` records the request, approval, rejection, and return state.
- Trust rating remains optional and is based on completed request history.

Status: the model direction is drafted; fields and constraints will be finalized
after the client quote and primary workflow are confirmed.
