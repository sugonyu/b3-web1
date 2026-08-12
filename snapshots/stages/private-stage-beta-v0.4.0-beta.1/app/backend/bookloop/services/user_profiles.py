"""viewer와 profile owner 관계에 맞는 읽기 전용 profile context를 만든다."""

from sqlalchemy import and_, or_

from ..db import db
from ..db.models import BookListing, BorrowRequest, User


def get_public_user_profile_service(user_id, viewer_id):
    """본인 또는 approved 상대에게만 email을 포함한 profile을 반환한다."""
    user = db.session.get(User, user_id)
    if user is None:
        return None

    completed_exchanges = (
        BorrowRequest.query.join(BookListing)
        .filter(BorrowRequest.status == "returned")
        .filter(
            or_(
                BorrowRequest.borrower_id == user.id,
                BookListing.owner_id == user.id,
            )
        )
        .count()
    )
    available_listings = (
        BookListing.query.filter_by(owner_id=user.id, availability=True)
        .order_by(BookListing.id.desc())
        .all()
    )

    viewer = db.session.get(User, viewer_id)
    is_admin_view = viewer is not None and viewer.is_admin
    is_own_profile = viewer_id == user.id
    has_approved_exchange = False
    if not is_own_profile:
        has_approved_exchange = (
            BorrowRequest.query.join(BookListing)
            .filter(BorrowRequest.status.in_(("approved", "return_pending")))
            .filter(
                or_(
                    and_(
                        BorrowRequest.borrower_id == viewer_id,
                        BookListing.owner_id == user.id,
                    ),
                    and_(
                        BorrowRequest.borrower_id == user.id,
                        BookListing.owner_id == viewer_id,
                    ),
                )
            )
            .first()
            is not None
        )

    email_visibility = None
    if is_admin_view:
        email_visibility = "admin"
    elif is_own_profile:
        email_visibility = "own_profile"
    elif has_approved_exchange:
        email_visibility = "approved_exchange"

    return {
        # email을 숨겨야 할 때는 model 자체를 template에 넘기지 않는다.
        "user": {
            "id": user.id,
            "username": user.username,
            "general_area": user.general_area,
            "created_at": user.created_at,
        },
        "email": user.email if email_visibility else None,
        "email_visibility": email_visibility,
        "completed_exchanges": completed_exchanges,
        "available_listings": available_listings,
    }
