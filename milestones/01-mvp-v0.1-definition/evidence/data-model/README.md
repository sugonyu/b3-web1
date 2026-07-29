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

- `User`: `id`, `username`, `email`, `password_hash`, and `general_area`.
- `BookListing`: `id`, `title`, `author`, `availability`, and `owner_id`.
- `BorrowRequest`: `id`, `status`, `listing_id`, and `borrower_id`.
- One user owns many listings and may create many borrow requests.
- One listing may receive many borrow requests.
- `owner_id`, `listing_id`, and `borrower_id` preserve these relationships.
- Trust rating remains optional and is based on completed request history.

Public presentation evidence:

- [Data model and relationship diagram](../../presentation.html#data)
- model fields and foreign-key roles
- one-to-many relationship cardinality
- privacy-safe public data boundary

Status: the fields and relationships are confirmed, privately verified, and
represented in the public presentation candidate. Instructor feedback remains
pending for Thursday.
