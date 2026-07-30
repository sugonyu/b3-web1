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
- Seven product endpoints cover listing collection CRUD, one listing resource,
  request creation, and request status updates.
- Temporary user IDs support the private prototype. Deliverable 1 documents the
  authentication boundary; Flask-Login implementation is planned for
  🗄️ Deliverable 2 — Backend and Database.

Public presentation evidence:

- [Frontend and backend choice](../../presentation.html#stack)
- [Seven-endpoint contract](../../presentation.html#api)
- [Project tree and data flow](../../presentation.html#architecture)
- [Five-week milestone plan](../../presentation.html#plan)

Status: the stack, three-model boundary, seven-endpoint contract, proposed
project tree and five-week plan are included in the accepted v1.0
presentation baseline. The private implementation was previously verified with
24 passing tests. Thursday instructor feedback remains pending.
