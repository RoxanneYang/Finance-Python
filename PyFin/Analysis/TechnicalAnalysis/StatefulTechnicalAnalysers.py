# -*- coding: utf-8 -*-
u"""
Created on 2015-8-8

@author: cheng.li
"""

import copy
import numpy as np
from PyFin.Analysis.SecurityValueHolders import SecurityValueHolder
from PyFin.Analysis.SecurityValueHolders import SecuritiesValues
from PyFin.Math.Accumulators.StatefulAccumulators import MovingAverage
from PyFin.Math.Accumulators.StatefulAccumulators import MovingMax
from PyFin.Math.Accumulators.StatefulAccumulators import MovingMinimum
from PyFin.Math.Accumulators.StatefulAccumulators import MovingSum
from PyFin.Math.Accumulators.StatefulAccumulators import MovingVariance
from PyFin.Math.Accumulators.StatefulAccumulators import MovingCountedPositive
from PyFin.Math.Accumulators.StatefulAccumulators import MovingPositiveAverage
from PyFin.Math.Accumulators.StatefulAccumulators import MovingCountedNegative
from PyFin.Math.Accumulators.StatefulAccumulators import MovingNegativeAverage
from PyFin.Math.Accumulators.StatefulAccumulators import MovingPositiveDifferenceAverage
from PyFin.Math.Accumulators.StatefulAccumulators import MovingNegativeDifferenceAverage
from PyFin.Math.Accumulators.StatefulAccumulators import MovingRSI
from PyFin.Math.Accumulators.StatefulAccumulators import MovingHistoricalWindow
from PyFin.Math.Accumulators.Performancers import MovingLogReturn


class SecuritySingleValueHolder(SecurityValueHolder):
    def __init__(self, window, HolderType, dependency='x',):
        super(SecuritySingleValueHolder, self).__init__(dependency)
        self._window = window

        if isinstance(dependency, SecurityValueHolder):
            self._symbolList = set(dependency.symbolList)
            self._window = window + dependency.window - 1
            self._dependency = dependency._dependency
            self._holderTemplate = HolderType(window=window, dependency=copy.deepcopy(dependency._holderTemplate))
            self._innerHolders = \
                {
                    name: HolderType(window, copy.deepcopy(dependency.holders[name])) for name in self._symbolList
                    }

        else:
            self._holderTemplate = HolderType(window=window, dependency=self._dependency)
        self._innerHolders = \
            {
                name: copy.deepcopy(self._holderTemplate) for name in self._symbolList
            }


class SecurityMovingAverage(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingAverage, self).__init__(window, MovingAverage, dependency)


class SecurityMovingMax(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingMax, self).__init__(window, MovingMax, dependency)


class SecurityMovingMinimum(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingMinimum, self).__init__(window, MovingMinimum, dependency)


class SecurityMovingSum(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingSum, self).__init__(window, MovingSum, dependency)


class SecurityMovingVariance(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingVariance, self).__init__(window, MovingVariance, dependency)


class SecurityMovingCountedPositive(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingCountedPositive, self).__init__(window, MovingCountedPositive, dependency)


class SecurityMovingPositiveAverage(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingPositiveAverage, self).__init__(window, MovingPositiveAverage, dependency)


class SecurityMovingCountedNegative(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingCountedNegative, self).__init__(window, MovingCountedNegative, dependency)


class SecurityMovingNegativeAverage(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingNegativeAverage, self).__init__(window, MovingNegativeAverage, dependency)


class SecurityMovingPositiveDifferenceAverage(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingPositiveDifferenceAverage, self).__init__(window, MovingPositiveDifferenceAverage, dependency)


class SecurityMovingNegativeDifferenceAverage(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingNegativeDifferenceAverage, self).__init__(window, MovingNegativeDifferenceAverage, dependency)


class SecurityMovingRSI(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingRSI, self).__init__(window, MovingRSI, dependency)


class SecurityMovingLogReturn(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingLogReturn, self).__init__(window, MovingLogReturn, dependency)


class SecurityMovingHistoricalWindow(SecuritySingleValueHolder):
    def __init__(self, window, dependency='x'):
        super(SecurityMovingHistoricalWindow, self).__init__(window, MovingHistoricalWindow, dependency)

    def __getitem__(self, item):
        if isinstance(item, str):
            return super(SecurityMovingHistoricalWindow, self).__getitem__(item)
        elif isinstance(item, int):
            res = {}
            for name in self._innerHolders:
                try:
                    res[name] = self._innerHolders[name].value[item]
                except ArithmeticError:
                    res[name] = np.nan
            return SecuritiesValues(res)
        else:
            raise ValueError("{0} is not recognized as valid int or string".format(item))
