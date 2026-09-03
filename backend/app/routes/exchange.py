from decimal import Decimal
from datetime import datetime
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.user import User
from app.models.skill import Skill, UserSkill
from app.models.session import SwapRequest, Session
from app.models.transaction import CreditTransaction
from app.models.review import Review
from app.models.utility import Notification
from app.utils.auth import login_required

exchange_bp = Blueprint('exchange', __name__)

@exchange_bp.route('/api/matches', methods=['GET'])
@login_required
def get_matches():
    """Retrieve suitable users based on teach/learn compatibility."""
    curr_user = g.current_user
    
    # 1. Fetch current user's skills
    curr_user_skills = UserSkill.query.filter_by(user_id=curr_user.id).all()
    curr_teach_ids = {us.skill_id for us in curr_user_skills if us.role == 'teach'}
    curr_learn_ids = {us.skill_id for us in curr_user_skills if us.role == 'learn'}
    
    if not curr_teach_ids and not curr_learn_ids:
        return jsonify([]), 200
        
    # 2. Query all other users
    all_users = User.query.filter(User.id != curr_user.id).all()
    matches_list = []
    
    for u in all_users:
        u_skills = UserSkill.query.filter_by(user_id=u.id).all()
        u_teach = {us.skill_id: us for us in u_skills if us.role == 'teach'}
        u_learn = {us.skill_id: us for us in u_skills if us.role == 'learn'}
        
        # Intersection: 
        # - Skills we teach that they want to learn
        we_teach_they_learn = curr_teach_ids.intersection(u_learn.keys())
        # - Skills they teach that we want to learn
        they_teach_we_learn = curr_learn_ids.intersection(u_teach.keys())
        
        if we_teach_they_learn or they_teach_we_learn:
            # We have a match!
            is_reciprocal = bool(we_teach_they_learn and they_teach_we_learn)
            match_score = 100 if is_reciprocal else 50
            
            # Map skill info details
            teach_skills_details = []
            for skill_id in u_teach.keys():
                sk = db.session.get(Skill, skill_id)
                if sk:
                    teach_skills_details.append({"id": sk.id, "name": sk.name, "category": sk.category, "proficiency": u_teach[skill_id].proficiency})
                    
            learn_skills_details = []
            for skill_id in u_learn.keys():
                sk = db.session.get(Skill, skill_id)
                if sk:
                    learn_skills_details.append({"id": sk.id, "name": sk.name, "category": sk.category, "proficiency": u_learn[skill_id].proficiency})
            
            matches_list.append({
                "user": {
                    "id": u.id,
                    "name": u.full_name,
                    "email": u.email,
                    "major": u.major,
                    "bio": u.bio,
                    "college": u.college
                },
                "teach_skills": teach_skills_details,
                "learn_skills": learn_skills_details,
                "reciprocal": is_reciprocal,
                "match_score": match_score
            })
            
    # Sort matches by score descending
    matches_list.sort(key=lambda x: x['match_score'], reverse=True)
    return jsonify(matches_list), 200

@exchange_bp.route('/api/swap-requests', methods=['POST'])
@login_required
def create_swap_request():
    """Send a new swap request invitation to a matched user."""
    data = request.get_json()
    if not data or 'receiver_id' not in data:
        return jsonify({"error": "Invalid request", "message": "receiver_id is required"}), 400
        
    receiver_id = int(data['receiver_id'])
    teach_skill_id = data.get('teach_skill_id')
    learn_skill_id = data.get('learn_skill_id')
    message = data.get('message', '')
    
    if receiver_id == g.current_user.id:
        return jsonify({"error": "Validation failed", "message": "Cannot swap with yourself"}), 400
        
    receiver = db.session.get(User, receiver_id)
    if not receiver:
        return jsonify({"error": "Resource not found", "message": "Receiver student not found"}), 404
        
    # Check if a pending swap request already exists between them
    existing = SwapRequest.query.filter(
        ((SwapRequest.sender_id == g.current_user.id) & (SwapRequest.receiver_id == receiver_id) & (SwapRequest.status == 'pending')) |
        ((SwapRequest.sender_id == receiver_id) & (SwapRequest.receiver_id == g.current_user.id) & (SwapRequest.status == 'pending'))
    ).first()
    
    if existing:
        return jsonify({"error": "Conflict error", "message": "A pending request already exists between you."}), 409
        
    req = SwapRequest(
        sender_id=g.current_user.id,
        receiver_id=receiver_id,
        teach_skill_id=teach_skill_id,
        learn_skill_id=learn_skill_id,
        status='pending',
        message=message
    )
    
    try:
        db.session.add(req)
        db.session.commit()
        return jsonify({"message": "Swap request sent successfully", "id": req.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": "Failed to create swap request."}), 500

@exchange_bp.route('/api/swap-requests', methods=['GET'])
@login_required
def get_swap_requests():
    """Retrieve incoming and outgoing swap requests."""
    curr_user = g.current_user
    
    # Outgoing
    outgoing = SwapRequest.query.filter_by(sender_id=curr_user.id).all()
    # Incoming
    incoming = SwapRequest.query.filter_by(receiver_id=curr_user.id).all()
    
    def serialize_req(r):
        t_sk = db.session.get(Skill, r.teach_skill_id) if r.teach_skill_id else None
        l_sk = db.session.get(Skill, r.learn_skill_id) if r.learn_skill_id else None
        
        sender_user = db.session.get(User, r.sender_id)
        receiver_user = db.session.get(User, r.receiver_id)
        
        return {
            "id": r.id,
            "sender": {
                "id": r.sender_id,
                "name": sender_user.full_name if sender_user else "Unknown",
                "major": sender_user.major if sender_user else ""
            },
            "receiver": {
                "id": r.receiver_id,
                "name": receiver_user.full_name if receiver_user else "Unknown",
                "major": receiver_user.major if receiver_user else ""
            },
            "teach_skill": {"id": t_sk.id, "name": t_sk.name} if t_sk else None,
            "learn_skill": {"id": l_sk.id, "name": l_sk.name} if l_sk else None,
            "status": r.status,
            "message": r.message,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    return jsonify({
        "incoming": [serialize_req(r) for r in incoming],
        "outgoing": [serialize_req(r) for r in outgoing]
    }), 200

@exchange_bp.route('/api/swap-requests/<int:request_id>/respond', methods=['POST'])
@login_required
def respond_swap_request(request_id):
    """Accept or reject an incoming swap request."""
    req = db.session.get(SwapRequest, request_id)
    if not req:
        return jsonify({"error": "Resource not found", "message": "Swap request not found"}), 404
        
    if req.receiver_id != g.current_user.id:
        return jsonify({"error": "Authorization failed", "message": "You can only respond to incoming requests"}), 403
        
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({"error": "Invalid request", "message": "action is required"}), 400
        
    action = data['action'].lower()
    if action not in ['accept', 'reject', 'cancel']:
        return jsonify({"error": "Validation failed", "message": "action must be accept, reject, or cancel"}), 400
        
    if action == 'accept':
        req.status = 'accepted'
    elif action == 'reject':
        req.status = 'rejected'
    elif action == 'cancel':
        req.status = 'cancelled'
        
    try:
        db.session.commit()
        return jsonify({"message": f"Swap request status updated to {req.status}", "status": req.status}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": "Failed to update request status."}), 500


@exchange_bp.route('/api/sessions', methods=['POST'])
@login_required
def create_session():
    """Schedule a new learning session, placing credits on hold."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request", "message": "JSON body is required"}), 400
        
    request_id = data.get('request_id')
    teacher_id = data.get('teacher_id')
    learner_id = data.get('learner_id')
    skill_id = data.get('skill_id')
    scheduled_at_str = data.get('scheduled_at')
    duration_val = data.get('duration_hours')
    venue = data.get('venue', 'Online / Campus Library')

    if not request_id or not teacher_id or not learner_id or not skill_id or not scheduled_at_str or not duration_val:
        return jsonify({"error": "Validation failed", "message": "All fields are required"}), 400

    try:
        duration_hours = Decimal(str(duration_val))
        if duration_hours <= 0:
            return jsonify({"error": "Validation failed", "message": "Duration must be greater than 0"}), 400
    except Exception:
        return jsonify({"error": "Validation failed", "message": "Duration must be a decimal value"}), 400

    try:
        scheduled_at = datetime.strptime(scheduled_at_str, "%Y-%m-%d %H:%M:%S")
        if scheduled_at < datetime.utcnow():
            return jsonify({"error": "Validation failed", "message": "Cannot schedule a session in the past"}), 400
    except ValueError:
        return jsonify({"error": "Validation failed", "message": "Date format must be YYYY-MM-DD HH:MM:SS"}), 400

    # Retrieve learner
    learner = db.session.get(User, learner_id)
    teacher = db.session.get(User, teacher_id)
    if not learner or not teacher:
        return jsonify({"error": "Resource not found", "message": "Teacher or learner not found"}), 404

    # Verify learner's credit balance
    if learner.credit_balance < duration_hours:
        return jsonify({
            "error": "Insufficient funds",
            "message": f"Learner has {float(learner.credit_balance)} credits, but session requires {float(duration_hours)}."
        }), 400

    # Place hold: deduct credits from learner immediately
    learner.credit_balance -= duration_hours

    # Create swap session
    sess = Session(
        request_id=request_id,
        teacher_id=teacher_id,
        learner_id=learner_id,
        skill_id=skill_id,
        scheduled_at=scheduled_at,
        duration_hours=duration_hours,
        venue=venue,
        status='scheduled'
    )

    try:
        db.session.add(sess)
        db.session.flush()

        # Record credit hold transaction
        db.session.add(CreditTransaction(
            user_id=learner.id,
            session_id=sess.id,
            amount=-duration_hours,
            type='hold_placement',
            description=f"Placed {float(duration_hours)} credits on hold for swap session {sess.id}"
        ))

        # Update swap request status
        swap_req = db.session.get(SwapRequest, request_id)
        if swap_req:
            swap_req.status = 'accepted'

        db.session.commit()
        return jsonify({"message": "Session scheduled successfully and credits placed on hold", "id": sess.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": f"Failed to schedule session: {str(e)}"}), 500


@exchange_bp.route('/api/sessions', methods=['GET'])
@login_required
def get_sessions():
    """Retrieve all upcoming, active, completed, or cancelled sessions for the user."""
    curr_user = g.current_user
    sessions = Session.query.filter((Session.teacher_id == curr_user.id) | (Session.learner_id == curr_user.id)).all()

    response = []
    for s in sessions:
        partner = db.session.get(User, s.learner_id if s.teacher_id == curr_user.id else s.teacher_id)
        skill = db.session.get(Skill, s.skill_id)
        response.append({
            "id": s.id,
            "partner_name": partner.full_name if partner else "Unknown",
            "skill_name": skill.name if skill else "Unknown",
            "scheduled_at": s.scheduled_at.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_hours": float(s.duration_hours),
            "venue": s.venue,
            "status": s.status,
            "role": "teacher" if s.teacher_id == curr_user.id else "learner"
        })
    return jsonify(response), 200


@exchange_bp.route('/api/sessions/<int:session_id>', methods=['GET'])
@login_required
def get_session_details(session_id):
    """Retrieve full details of a specific swap session."""
    s = db.session.get(Session, session_id)
    if not s:
        return jsonify({"error": "Resource not found", "message": "Session not found"}), 404

    if s.teacher_id != g.current_user.id and s.learner_id != g.current_user.id:
        return jsonify({"error": "Authorization failed", "message": "You are not a member of this session"}), 403

    teacher = db.session.get(User, s.teacher_id)
    learner = db.session.get(User, s.learner_id)
    skill = db.session.get(Skill, s.skill_id)

    return jsonify({
        "id": s.id,
        "teacher_name": teacher.full_name if teacher else "Unknown",
        "learner_name": learner.full_name if learner else "Unknown",
        "skill_name": skill.name if skill else "Unknown",
        "scheduled_at": s.scheduled_at.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_hours": float(s.duration_hours),
        "venue": s.venue,
        "status": s.status,
        "completed_at": s.completed_at.strftime("%Y-%m-%d %H:%M:%S") if s.completed_at else None,
        "cancelled_by": s.cancelled_by,
        "cancelled_reason": s.cancelled_reason
    }), 200


@exchange_bp.route('/api/sessions/<int:session_id>/respond', methods=['POST'])
@login_required
def respond_session(session_id):
    """Perform action transitions (complete, cancel) on a scheduled session."""
    s = db.session.get(Session, session_id)
    if not s:
        return jsonify({"error": "Resource not found", "message": "Session not found"}), 404

    if s.teacher_id != g.current_user.id and s.learner_id != g.current_user.id:
        return jsonify({"error": "Authorization failed", "message": "You are not a member of this session"}), 403

    data = request.get_json()
    action = data.get('action', '').lower()
    reason = data.get('reason', 'Cancelled by student request')

    if action not in ['complete', 'cancel']:
        return jsonify({"error": "Validation failed", "message": "Action must be 'complete' or 'cancel'"}), 400

    if s.status != 'scheduled':
        return jsonify({"error": "Conflict error", "message": f"Cannot transition session from state: {s.status}"}), 409

    teacher = db.session.get(User, s.teacher_id)
    learner = db.session.get(User, s.learner_id)

    if action == 'complete':
        # Teacher receives held credits
        teacher.credit_balance += s.duration_hours
        s.status = 'completed'
        s.completed_at = datetime.utcnow()

        # Audit ledger
        db.session.add(CreditTransaction(
            user_id=teacher.id,
            session_id=s.id,
            amount=s.duration_hours,
            type='session_earn',
            description=f"Earned {float(s.duration_hours)} credits for teaching session {s.id}"
        ))
        db.session.add(CreditTransaction(
            user_id=learner.id,
            session_id=s.id,
            amount=-s.duration_hours,
            type='session_spend',
            description=f"Spent {float(s.duration_hours)} credits for learning session {s.id}"
        ))

    elif action == 'cancel':
        # Learner receives credits back
        learner.credit_balance += s.duration_hours
        s.status = 'cancelled'
        s.cancelled_by = g.current_user.id
        s.cancelled_reason = reason

        # Release hold transaction
        db.session.add(CreditTransaction(
            user_id=learner.id,
            session_id=s.id,
            amount=s.duration_hours,
            type='hold_release',
            description=f"Released {float(s.duration_hours)} credits from cancelled session {s.id}"
        ))

    try:
        db.session.commit()
        return jsonify({"message": f"Session status successfully changed to {s.status}", "status": s.status}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": f"Failed to update session: {str(e)}"}), 500


@exchange_bp.route('/api/reviews', methods=['POST'])
@login_required
def create_review():
    """Submit a double-blind post-session rating and review."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request", "message": "JSON body required"}), 400

    session_id = data.get('session_id')
    rating = data.get('rating')
    comment = data.get('comment', '').strip()

    if not session_id or rating is None:
        return jsonify({"error": "Validation failed", "message": "session_id and rating are required"}), 400

    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            return jsonify({"error": "Validation failed", "message": "Rating must be between 1 and 5"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Validation failed", "message": "Rating must be an integer between 1 and 5"}), 400

    s = db.session.get(Session, session_id)
    if not s:
        return jsonify({"error": "Resource not found", "message": "Session not found"}), 404

    if s.status != 'completed':
        return jsonify({"error": "Conflict error", "message": "Reviews can only be submitted for completed sessions"}), 409

    curr_user_id = g.current_user.id
    if curr_user_id not in [s.teacher_id, s.learner_id]:
        return jsonify({"error": "Authorization failed", "message": "You are not a participant in this session"}), 403

    reviewee_id = s.learner_id if curr_user_id == s.teacher_id else s.teacher_id

    # Check for existing review by this reviewer
    existing = Review.query.filter_by(session_id=s.id, reviewer_id=curr_user_id).first()
    if existing:
        return jsonify({"error": "Conflict error", "message": "You have already submitted a review for this session"}), 409

    # Check if the counterparty has already submitted their review
    counterparty_review = Review.query.filter_by(session_id=s.id, reviewer_id=reviewee_id).first()

    # Double-blind rule: both become visible once both submit!
    both_submitted = counterparty_review is not None

    new_review = Review(
        session_id=s.id,
        reviewer_id=curr_user_id,
        reviewee_id=reviewee_id,
        rating=rating_int,
        comment=comment,
        is_visible=both_submitted
    )
    db.session.add(new_review)

    if both_submitted:
        counterparty_review.is_visible = True
        # Notify both users that mutual reviews are now unlocked
        db.session.add(Notification(
            user_id=curr_user_id,
            title="Review Unlocked",
            content=f"Both participants have submitted reviews for session #{s.id}. Your feedback is now public!"
        ))
        db.session.add(Notification(
            user_id=reviewee_id,
            title="Review Unlocked",
            content=f"Both participants have submitted reviews for session #{s.id}. Your feedback is now public!"
        ))
    else:
        # Blind submission notification
        db.session.add(Notification(
            user_id=reviewee_id,
            title="Review Pending",
            content=f"Your session partner submitted a review for session #{s.id}. Submit yours to unlock mutual feedback!"
        ))

    try:
        db.session.commit()
        return jsonify({
            "message": "Review submitted successfully",
            "id": new_review.id,
            "is_visible": new_review.is_visible
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": f"Failed to submit review: {str(e)}"}), 500


@exchange_bp.route('/api/reviews/user/<int:user_id>', methods=['GET'])
def get_user_reviews(user_id):
    """Retrieve visible reviews for a user profile."""
    reviews = Review.query.filter_by(reviewee_id=user_id, is_visible=True).order_by(Review.created_at.desc()).all()
    out = []
    for r in reviews:
        reviewer = db.session.get(User, r.reviewer_id)
        out.append({
            "id": r.id,
            "session_id": r.session_id,
            "reviewer_name": reviewer.full_name if reviewer else "Peer Student",
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({"reviews": out, "total": len(out)}), 200


@exchange_bp.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Retrieve all notifications for the current authenticated user."""
    notifs = Notification.query.filter_by(user_id=g.current_user.id).order_by(Notification.created_at.desc()).all()
    return jsonify({
        "notifications": [{
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for n in notifs]
    }), 200


@exchange_bp.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read."""
    n = db.session.get(Notification, notification_id)
    if not n or n.user_id != g.current_user.id:
        return jsonify({"error": "Resource not found", "message": "Notification not found"}), 404
    n.is_read = True
    db.session.commit()
    return jsonify({"message": "Notification marked as read", "id": n.id}), 200

