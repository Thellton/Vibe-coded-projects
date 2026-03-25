using System;

namespace PerfCalcV2.Calculators.Models; // Update this line
public static class PrecisionFactors
{
    public static double GetMultiplier(ComputePrecision precision)
    {
        return precision switch
        {
            ComputePrecision.FP64 => 0.5,
            ComputePrecision.FP32 => 1.0,
            ComputePrecision.FP16 => 2.0,
            ComputePrecision.BF16 => 2.0,
            ComputePrecision.INT8 => 4.0,
            _ => throw new ArgumentOutOfRangeException(nameof(precision))
        };
    }

    public static int BytesPerParameter(ComputePrecision precision)
    {
        return precision switch
        {
            ComputePrecision.FP64 => 8,
            ComputePrecision.FP32 => 4,
            ComputePrecision.FP16 => 2,
            ComputePrecision.BF16 => 2,
            ComputePrecision.INT8 => 1,
            _ => throw new ArgumentOutOfRangeException(nameof(precision))
        };
    }

}