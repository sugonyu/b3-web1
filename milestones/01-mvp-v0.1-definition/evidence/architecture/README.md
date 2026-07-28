# Proposed Architecture

This folder contains the planned application structure and primary data flow
for the BookLoop Deliverable 1 proposal.

Expected evidence:

- approved frontend and backend approach
- main user workflow
- route, endpoint or data-operation list
- validation and authorization boundaries
- frontend-to-database flow
- proposed repository structure
- five-week implementation milestones

Current direction:

- React frontend consumes a Flask JSON API.
- Flask-SQLAlchemy and SQLite provide the initial relational data boundary.
- The primary flow is listing discovery → borrow request → owner approval →
  limited connection.

Status: the working stack is selected, but the final project scope and quote
still require instructor confirmation.
