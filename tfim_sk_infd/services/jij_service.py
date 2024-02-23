import numpy as np
from tfim_sk_infd.models.Jij import Jij


def get_toy_Jij(index: int) -> Jij:
    match index:
        case 1:
            return Jij(np.array([[0, 1, 1, 1, 1], [-1, -1, 1, 0, 1]]))
        case 2:
            return Jij(np.array([[1, 2, -2, 1, -2], [2, 1, 1, -1, 2]]))
        case 3:
            return Jij(
                np.array(
                    [[0, 0, 0, -1, 1, 1], [0, 0, 1, 1, 1, -1], [0, 0, -1, 0, 0, -1]]
                )
            )
        case 4:
            return Jij(np.array([[0, 1, -1, -1], [0, -1, 0, -1]]))
        case _:
            raise Exception(f"Toy model for index {index} does not exist")
