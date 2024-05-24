from sqlalchemy import update, func
from database.models import InstancesN8
import data_service


with data_service.get_session() as session:
    statement = (
        update(InstancesN8)
        .where(InstancesN8.degeneracy.is_(None))
        .values(degeneracy=func.json_array_length(InstancesN8.ground_states))
    )

    session.execute(statement)

    session.commit()
    session.close()
