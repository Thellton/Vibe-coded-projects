namespace PerfCalcV2.Calculators.Models; // Update this line

public sealed record ModelStorageResult(
    double Bytes,
    double Megabytes,
    double Gigabytes,
    double Terabytes
);
