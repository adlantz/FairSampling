from sqlalchemy import update, func
import data_service


import sys

N = int(sys.argv[1])
Instance = data_service.get_instance_class(N)


with data_service.get_session() as session:
    statement = (
        update(Instance)
        .where(Instance.degeneracy.is_(None))
        .values(degeneracy=func.json_array_length(Instance.ground_states))
    )

    session.execute(statement)

    session.commit()
    session.close()
