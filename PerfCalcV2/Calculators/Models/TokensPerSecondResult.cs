namespace PerfCalcV2.Calculators.Models; // Update this line

public sealed record TokensPerSecondResult(
    double TokensPerSecond,
    double ComputeBoundTokensPerSecond,
    double BandwidthBoundTokensPerSecond
);
