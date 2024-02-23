import numpy as np

import itertools as it
from scipy import linalg

import argparse

import progressbar
import math

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

    parser.add_argument("T", help=("Toy model (ranges from 1 to 4)"))
    parser.add_argument(
        "--gsAmps",
        action="store_true",
        help=("Calcuate ground state probability ampltitudes"),
    )
    parser.add_argument(
        "--entropy", action="store_true", help=("Compute entanglement entropies")
    )
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
    ###################################

    # Define arg based variables
    T = int(args.T)
    log_scale = args.log10h
    gsAmps_on = args.gsAmps
    entropy_on = args.entropy

    # Define magnetic field array
    h_arr = np.arange(args.h_min, args.h_max + args.dh / 2, args.dh)
    if log_scale:
        h_arr = 10**h_arr

    # Retrieve Jij instance
    Jij_instance = jij_service.get_toy_Jij(T)

    # Build spin glass
    SG = SKSpinGlass(Jij_instance)

    # Get indexes of classical ground states
    gs_val = SG.JZZ.diagonal().max()
    ground_states = [i for i, val in enumerate(SG.JZZ.diagonal()) if val == gs_val]

    bar = progressbar.ProgressBar()
    print("Iterating through h array...")
    for h in h_arr:

        # Define Hamiltonian H
        H = SG.hamiltonian_at_h(h)

        # Diagonalize H
        E, v = linalg.eigh(H.todense())
        sort_order = np.argsort(E)
        E = E[sort_order]
        v = v[:, sort_order]
        psi0 = v[:, 0]

        # print(psi0**2)
        print([psi0[g] ** 2 for g in ground_states])

    # lattice = tfim.Lattice([N])
    # basis = tfim.IsingBasis(lattice)

    # # Create JZZ and Mx Matrices
    # print("Creating JZZ and Mx Matrices...")
    # JZZ = tfim.JZZ_SK(basis, Jij)
    # Mx = tfim.build_Mx(lattice, basis)

    # gs = np.where(JZZ.diagonal() == JZZ.diagonal().max())[0]
    # print(gs)
    # print([basis.state(g) for g in gs])

    # # Find ground states from JZZ matrix
    # if gsAmps_on:
    #     gs = np.where(JZZ.diagonal() == JZZ.diagonal().max())[0]

    # # Open files
    # if log_scale:
    #     if gsAmps_on:
    #         gsAmps_filename = (
    #             "OutData/gsAmps/"
    #             + str(T)
    #             + "/h("
    #             + str(args.h_min)
    #             + ","
    #             + str(args.h_max)
    #             + ","
    #             + str(args.dh)
    #             + ")log10.dat"
    #         )
    #     if entropy_on:
    #         Svn_filename = (
    #             "OutData/entropy/entropy/"
    #             + str(T)
    #             + "/h("
    #             + str(args.h_min)
    #             + ","
    #             + str(args.h_max)
    #             + ","
    #             + str(args.dh)
    #             + ")log10.dat"
    #         )
    #         sEng_filename = (
    #             "OutData/entropy/energies/"
    #             + str(T)
    #             + "/h("
    #             + str(args.h_min)
    #             + ","
    #             + str(args.h_max)
    #             + ","
    #             + str(args.dh)
    #             + ")log10.dat"
    #         )
    # else:
    #     if gsAmps_on:
    #         gsAmps_filename = (
    #             "OutData/gsAmps/"
    #             + str(T)
    #             + "/h("
    #             + str(args.h_min)
    #             + ","
    #             + str(args.h_max)
    #             + ","
    #             + str(args.dh)
    #             + ").dat"
    #         )
    #     if entropy_on:
    #         Svn_filename = (
    #             "OutData/entropy/entropy/"
    #             + str(T)
    #             + "/h("
    #             + str(args.h_min)
    #             + ","
    #             + str(args.h_max)
    #             + ","
    #             + str(args.dh)
    #             + ").dat"
    #         )
    #         sEng_filename = (
    #             "OutData/entropy/energies/"
    #             + str(T)
    #             + "/h("
    #             + str(args.h_min)
    #             + ","
    #             + str(args.h_max)
    #             + ","
    #             + str(args.dh)
    #             + ").dat"
    #         )
    # if gsAmps_on:
    #     gsAmps_file = open(gsAmps_filename, "w")
    # if entropy_on:

    # permlist = []

    # if N % 2 == 0:
    #     combos = list(it.combinations([i for i in range(N)], N // 2))
    #     num_bps = len(combos) // 2
    #     for i in range(num_bps):
    #         permlist.append(list(combos[i] + combos[-1 - i]))

    # else:
    #     combos1 = list(it.combinations([i for i in range(N)], N // 2))
    #     combos2 = list(it.combinations([i for i in range(N)], N // 2 + 1))
    #     num_bps = len(combos1)
    #     for i in range(num_bps):
    #         permlist.append(list(combos1[i] + combos2[-i - 1]))

    #     Svn_file = open(Svn_filename, "w")

    #     sEng_file = open(sEng_filename, "w")
    #     sEng_file.write(
    #         "#\ttfim_diag parameters:\t"
    #         + "h = "
    #         + str((args.h_min, args.h_max, args.dh))
    #         + " Bps = "
    #         + str(num_bps)
    #         + "\n"
    #     )

    # ##################################

    # print(np.where(JZZ.diagonal() == JZZ.diagonal().max())[0])

    # # Iterate through h_arr
    # ##################################
    # bar = progressbar.ProgressBar()
    # print("Iterating through h array...")
    # for h in bar(h_arr):

    #     # Define Hamiltonian H
    #     H = -JZZ - h * Mx

    #     # Diagonalize H
    #     E, v = linalg.eigh(H.todense())
    #     sort_order = np.argsort(E)
    #     E = E[sort_order]
    #     v = v[:, sort_order]
    #     psi0 = v[:, 0]

    #     print(psi0**2)
    #     print([psi0[g] ** 2 for g in gs])

    #     # Create gs amps array (to mirror those in Konz paper)
    #     if gsAmps_on:
    #         gv = np.array([psi0[g] ** 2 for g in gs])
    #         gvout = gv[: len(gs) // 2] + gv[: len(gs) // 2 - 1 : -1]
    #         np.savetxt(gsAmps_file, [np.concatenate(([h], gvout))])

    #     if entropy_on:
    # Svn = np.zeros(len(permlist))
    # sEng = np.zeros((len(permlist), 2 ** (N // 2)))
    # for i, P in enumerate(permlist):
    #     A = P[0 : (N // 2)]
    #     B = P[(N // 2) : N]
    #     S, U, V = tfim_rdm.svd(basis, A, B, psi0, True)

    #     Svn[i] = tfim_rdm.entropy(S)
    #     sEng[i] = np.sort(0 - 2 * np.log(S))

    #         np.savetxt(
    #             Svn_file,
    #             np.concatenate(([h], Svn)).reshape((1, Svn.shape[0] + 1)),
    #             fmt="%{}.{}e".format(25, 15),
    #         )

    #         sEng_file.write("#h = " + str(h) + "\n")
    #         np.savetxt(sEng_file, sEng)

    # ##################################

    # if gsAmps_on:
    #     gsAmps_file.close()
    # if entropy_on:
    #     Svn_file.close()
    #     sEng_file.close()


if __name__ == "__main__":
    main()
