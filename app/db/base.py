# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base

from app.models.user import User
from app.models.institutions import Institution
from app.models.classes import ClassRoom
from app.models.teachers import Teacher
from app.models.courses import Courses
from app.models.parents import Parents
from app.models.students import Students