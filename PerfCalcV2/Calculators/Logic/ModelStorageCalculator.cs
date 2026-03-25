using System;
using PerfCalcV2.Calculators.Models;

namespace PerfCalcV2.Calculators.Logic; // Update this line

public static class ModelStorageCalculator
{
    public static ModelStorageResult Calculate(double rawParameters, ParameterScale parameterScale, ComputePrecision precision)
    {
        ///if (rawParameters < 0)
        ///    throw new ArgumentOutOfRangeException(nameof(rawParameters));
        
        Guard.AgainstNegative(rawParameters, nameof(rawParameters));
        
        double parameters = parameterScale switch
        {
            ParameterScale.Billions => rawParameters * 1e9,
            ParameterScale.Raw => rawParameters,
            _ => throw new ArgumentOutOfRangeException(nameof(parameterScale))
        };

        double bytesPerParameter = PrecisionFactors.BytesPerParameter(precision);

        double totalBytes = parameters * bytesPerParameter;

        double megabytes = totalBytes / 1e6;
        double gigabytes = totalBytes / 1e9;
        double terabytes = totalBytes / 1e12;   

        return new ModelStorageResult(
            totalBytes,
            megabytes,
            gigabytes,
            terabytes
        );
    }

    public static class Guard
    {
        public static void AgainstNegative(double value, string name)
        {
            if (value < 0)
                throw new ArgumentOutOfRangeException(name);
        }
    }
 
}