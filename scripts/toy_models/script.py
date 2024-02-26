import argparse
import progressbar
import data_service
import numpy as np

from scipy import linalg

from tfim_sk_infd.models.SKSpinGlass import SKSpinGlass
from tfim_sk_infd.services import jij_service, entropy_service


#########################################################################################################
def main():

    # Parse command line arguments
    ######################################################################
    parser = argparse.ArgumentParser(
        description=(
            "Calculates the classical ground state probabilities"
            " of toy models presented in the Konz paper"
        )
    )

    parser.add_argument("T", type=int, help=("Toy model (ranges from 1 to 4)"))
    parser.add_argument(
        "--h_min", type=float, default=0.1, help=("Minimum value of magnetic field h")
    )
    parser.add_argument(
        "--h_max", type=float, default=3.0, help=("Maximum value of magnetic field h")
    )
    parser.add_argument(
        "--dh", type=float, default=0.1, help=("Magnetic field step size")
    )
    parser.add_argument(
        "--log10h",
        action="store_true",
        help=("Iterate through magnetic field on log10 scale"),
    )

    args = parser.parse_args()
    ######################################################################

    # Set calculation Parameters
    ######################################################################

    T = int(args.T)
    log_scale = args.log10h

    h_arr = np.arange(args.h_min, args.h_max + args.dh / 2, args.dh)
    if log_scale:
        h_arr = 10**h_arr

    Jij_instance = jij_service.get_toy_Jij(T)
    SG = SKSpinGlass(Jij_instance)

    # Get indexes of classical ground states
    ground_states = [
        i for i, val in enumerate(SG.JZZ.diagonal()) if val == SG.JZZ.diagonal().max()
    ]

    ######################################################################

    # Iterate through h array
    ######################################################################

    out_obj = []
    bar = progressbar.ProgressBar()
    print("Iterating through h array...")
    for h in bar(h_arr):

        # Define Hamiltonian H at h
        H = SG.hamiltonian_at_h(h)

        # Diagonalize H and get ground state vector psi0
        E, v = linalg.eigh(H.todense())
        sort_order = np.argsort(E)
        v = v[:, sort_order]
        psi0 = v[:, 0]

        # retrieve and format probabilities of classical ground states in psi0
        gs_probs = np.array([psi0[g] ** 2 for g in ground_states])
        gs_probs_out = (
            gs_probs[: len(ground_states) // 2]
            + gs_probs[: len(ground_states) // 2 - 1 : -1]
        )

        # Calculate entanglement entropies and "energies"
        svn, s_eng = entropy_service.get_entanglement_entropy_information(
            SG.basis, psi0
        )

        out_obj.append(
            {
                "h": h,
                "groundStateProbabilities": gs_probs_out.tolist(),
                "entanglementEntropies": svn.tolist(),
                "entanglementEnergies": s_eng.tolist(),
            }
        )

    ######################################################################

    data_service.save_obj(
        "toy_models",
        str(T),
        f"h({args.h_min},{args.h_max},{args.dh}){'log10' if log_scale else ''}",
        out_obj,
    )


if __name__ == "__main__":
    main()
