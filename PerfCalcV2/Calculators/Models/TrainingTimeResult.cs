namespace PerfCalcV2.Calculators.Models;

public record TrainingTimeResult(
    // Core timing results (in seconds)
    double OptimisticSeconds,
    double ProbableSeconds,
    double PessimisticSeconds,

    // Intermediates exposed for the output panel
    double TotalTrainingFlops,
    double TotalTokens,
    double MaxBatchSize,
    double ParameterMemoryGb,
    double ActivationMemoryGbPerSample,

    // MFU values used
    double MfuOptimistic,
    double MfuProbable,
    double MfuPessimistic,

    // Achieved throughput tiers (TFLOPs)
    double AchievedTflopsOptimistic,
    double AchievedTflopsProbable,
    double AchievedTflopsPessimistic
);