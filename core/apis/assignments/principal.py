from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema
from ..teachers.schema import TeacherSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_graded_submitted_assignments(p):
    submitted_graded_assignments = Assignment.get_graded_submitted_assignments()
    submitted_graded_assignments_dump = AssignmentSchema().dump(submitted_graded_assignments, many=True)
    return APIResponse.respond(data=submitted_graded_assignments_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.get_all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_regrade_assignment(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade_or_regrade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
