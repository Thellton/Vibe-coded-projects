using System;
using PerfCalcV2.Calculators.Models;

namespace PerfCalcV2.Calculators.Logic; // Update this line

public static class TokensPerSecondCalc
{
    public static TokensPerSecondResult Calculate(double tflopsAtPrecision, double bandwidthGbps, double rawParameters, ParameterScale parameterScale, ComputePrecision precision)
    {
        if (tflopsAtPrecision < 0)
            throw new ArgumentOutOfRangeException(nameof(tflopsAtPrecision));
        if (bandwidthGbps < 0)
            throw new ArgumentOutOfRangeException(nameof(bandwidthGbps));
        if (rawParameters < 0)
            throw new ArgumentOutOfRangeException(nameof(rawParameters));

        // Normalize parameter count
        double parameters = parameterScale switch
        {
            ParameterScale.Billions => rawParameters * 1e9,
            ParameterScale.Raw => rawParameters,
            _ => throw new ArgumentOutOfRangeException(nameof(parameterScale))
        };

        // FLOPs per token (2 * parameters)
        double flopsPerToken = 2.0 * parameters;

        // Compute-bound tokens/s
        double computeBoundTokens =
            flopsPerToken == 0
                ? double.PositiveInfinity
                : (tflopsAtPrecision * 1e12) / flopsPerToken;

        // Bandwidth-bound tokens/s
        double bytesPerToken = parameters * PrecisionFactors.BytesPerParameter(precision);
        double bandwidthBytesPerSecond = bandwidthGbps * 1e9;

        double bandwidthBoundTokens =
            bytesPerToken == 0
                ? double.PositiveInfinity
                : bandwidthBytesPerSecond / bytesPerToken;

        // Limiting factor
        double tokensPerSecond = Math.Min(computeBoundTokens, bandwidthBoundTokens);

        if (double.IsPositiveInfinity(tokensPerSecond))
            tokensPerSecond = 0.0;

        return new TokensPerSecondResult(
            tokensPerSecond,
            computeBoundTokens,
            bandwidthBoundTokens
        );
    }
}


/*
the TokensPerSecCalc.cs 

takes as inputs: Tflops, BandwidthGBPS, Parameters, Billions
IsItRawOrBillions is a dependency for the below op

it does the following transformations:

determines whether to operate on the value inputted as is, or to convert to billions
    <example = python>
    if self.param_mode_var.get() == "billions":
            parameters = raw_parameters * 1e9
        else:
            parameters = raw_parameters
    </example>

calculates how many flops per token are needed for a given number of parameters
    <example>
        flops_per_token = 2 * parameters
    </example>

calculates the compute-bound tokens/s, checking that the result won't be zero
    <example>
    if flops_per_token == 0: # Avoid division by zero if parameters=0
                compute_bound_tokens = float('inf') # Or handle as error? Let's allow inf for now.
        else:
                compute_bound_tokens = (tflops_at_precision * 1e12) / flops_per_token
    </example>

calculate the bandwidth bound tokens/s
    <example>
        bytes_per_token = parameters * precision.bytes_per_param

        bandwidth_bytes_per_second = bandwidth_gbps * 1e9

        if bytes_per_token == 0: # Avoid division by zero
                bandwidth_bound_tokens = float('inf')
            else:
                bandwidth_bound_tokens = bandwidth_bytes_per_second / bytes_per_token
            print(f"Bandwidth-bound tokens/s: {bandwidth_bound_tokens:.2f}")
    </example

determine which is the limiting factor
    <example>
        tokens_per_second = min(compute_bound_tokens, bandwidth_bound_tokens)
        if tokens_per_second == float('inf'): # Handle case where both are infinite (params=0)
        tokens_per_second = 0.0
    </example>
    
returns a tokens per second value, the raw implied compute bound tokens, and the raw bandwidth bound tokens
*/