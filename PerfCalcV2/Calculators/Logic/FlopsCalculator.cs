using System;
using PerfCalcV2.Calculators.Models;

namespace PerfCalcV2.Calculators.Logic; // Update this line

public static class FlopsCalculator
{
    /// <summary>
    /// Calculates theoretical peak FLOPS.
    /// </summary>
    /// <param name="computeUnits">Number of compute units (e.g. cores / SMs)</param>
    /// <param name="opsPerCycle">Operations per cycle per unit</param>
    /// <param name="clockGHz">Clock speed in GHz</param>
    /// <param name="precision">Compute precision</param>
    /// <returns>FLOPS in TFLOPS</returns>
    public static double CalculateTflops(double computeUnits, double opsPerCycle, double clockGHz, ComputePrecision precision)
    {
        if (computeUnits <= 0)
            throw new ArgumentOutOfRangeException(nameof(computeUnits));
        if (opsPerCycle <= 0)
            throw new ArgumentOutOfRangeException(nameof(opsPerCycle));
        if (clockGHz <= 0)
            throw new ArgumentOutOfRangeException(nameof(clockGHz));
        
        double precisionMultiplier = PrecisionFactors.GetMultiplier(precision);

        // FLOPS = units × ops/cycle × clock × precision factor
        // GHz → 1e9, TFLOPS → 1e12 → net division by 1000

        return computeUnits * opsPerCycle * clockGHz * precisionMultiplier / 1000.0;
    }
}