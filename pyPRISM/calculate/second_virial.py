#!python
from __future__ import division,print_function
from pyPRISM.core.Space import Space
from pyPRISM.core.PairTable import PairTable
import numpy as np

def second_virial(PRISM,extrapolate=True):
    r'''Calculate the second virial coefficient

    Parameters
    ----------
    PRISM: pyPRISM.core.PRISM
        A **solved** PRISM object.

    extrapolate: bool, *optional*
        If *True*, extrapolate :math:`h_{\alpha,\beta}` to :math:`k=0` rather
        than reporting the value at the lowest-k. Defaults to *True*.
    
    Returns
    -------
    B2: pyPRISM.core.PairTable
        Pairtable of B2 values


    **Mathematical Definition**

    .. math::

        B_{2}^{\alpha,\beta} = -0.5 \hat{h}_{\alpha,\beta}(k=0)

    
    **Variable Definitions**

        - :math:`B_{2}^{\alpha,\beta}`
            Second virial coefficient between site types :math:`\alpha` and
            :math:`\beta`

        - :math:`\hat{h}_{\alpha,\beta}(k)`
            Fourier-space total correlation function between site types
            :math:`\alpha` and :math:`\beta` at wavevector :math:`k`


    **Description**

        The second virial coefficient (:math:`B_{2}^{\alpha,\beta}`) is a 
        thermodynamic descriptor related to the pairwise interactions between 
        components in a system. In general, :math:`B_{2}^{\alpha,\beta}>0`
        signifies repulsive interactions between site types :math:`\alpha` and
        :math:`\beta`, and :math:`B_{2}^{\alpha,\beta}<0` signifies attractive
        interactions. For example, in a polymer-solvent system, one definition
        of the theta condition is when :math:`B_{2}^{\alpha,\beta}=0`.


    .. warning::

        Passing an unsolved PRISM object to this function will still produce
        output based on the default values of the attributes of the PRISM
        object.
    

    Example
    -------
    .. code-block:: python

        import pyPRISM

        sys = pyPRISM.System(['A','B'])

        # ** populate system variables **
        
        PRISM = sys.createPRISM()

        PRISM.solve()

        B2 = pyPRISM.calculate.second_virial(PRISM)

        B2_BB = B2['B','B']
    
    '''
    
    if PRISM.totalCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.totalCorr)
    
    B2 = PairTable(name='B2',types=PRISM.sys.types)
    for i,t1 in enumerate(PRISM.sys.types):
        for j,t2 in enumerate(PRISM.sys.types):
            if extrapolate:
                x = PRISM.sys.domain.k[:3]
                y = - 0.5 * PRISM.totalCorr[t1,t2][:3]
    
                fit = np.poly1d(np.polyfit(x,y,2))

                B2[t1,t2] = fit(0)
            else:
                B2[t1,t2] = - 0.5 * PRISM.totalCorr[t1,t2][0]

    return B2
