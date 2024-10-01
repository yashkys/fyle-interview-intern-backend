from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_graded_submitted_assignments(p):
    submitted_graded_assignments = Assignment.get_graded_submitted_assignments()
    submitted_graded_assignments_dump = AssignmentSchema().dump(submitted_graded_assignments, many=True)
    return APIResponse.respond(data=submitted_graded_assignments_dump)