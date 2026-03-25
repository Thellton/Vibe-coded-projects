using System;
using PerfCalcV2.Calculators.Models;

namespace PerfCalcV2.Calculators.Logic;

public static class TrainingTimeCalc
{
    // MFU tiers - these are reasonable real-world values.
    // Optimistic reflects near-ideal conditions, probable is typical,
    // pessimistic accounts for overhead, communication, and inefficiency.
    private const double MfuOptimistic  = 0.55;
    private const double MfuProbable    = 0.40;
    private const double MfuPessimistic = 0.25;

    public static TrainingTimeResult Calculate(TrainingInputs inputs)
    {
        // --- Normalize parameter count ---
        double parameters = inputs.ParameterScale switch
        {
            ParameterScale.Billions => inputs.RawParameters * 1e9,
            ParameterScale.Raw     => inputs.RawParameters,
            _ => throw new ArgumentOutOfRangeException(nameof(inputs.ParameterScale))
        };

        // --- Step 1: Memory footprint ---
        // Bytes per param: model weights + gradients (both at training precision)
        // + AdamW optimizer states (always 2x fp32 regardless of training precision)
        int precisionBytes = PrecisionFactors.BytesPerParameter(inputs.Precision);
        double bytesPerParamTotal = (precisionBytes * 2.0) + 8.0; // weights+grads + adamw (2x fp32=8)
        double parameterMemoryBytes = parameters * bytesPerParamTotal;
        double parameterMemoryGb = parameterMemoryBytes / 1e9;

        // --- Step 2: VRAM budget for activations ---
        double totalVramBytes = inputs.VramGbPerDevice * inputs.NumberOfDevices * 1e9;
        double activationVramBytes = totalVramBytes - parameterMemoryBytes;

        // Activation memory per sample per layer at training precision:
        // sequence_length * embedding_dim * bytes_per_param * ~2 (forward pass storage)
        double activationBytesPerSample =
            inputs.AverageSequenceLengthTokens *
            inputs.EmbeddingDim *
            precisionBytes *
            2.0 *
            inputs.LayerCount;

        double activationMemoryGbPerSample = activationBytesPerSample / 1e9;

        // Max batch size floored at 1
        double maxBatchSize = activationVramBytes > 0 && activationBytesPerSample > 0
            ? Math.Max(1, Math.Floor(activationVramBytes / activationBytesPerSample))
            : 1;

        // --- Step 3: Total training FLOPs ---
        // Standard approximation: 6 * N * T, where T = N * tokens_per_parameter
        double totalTokens = parameters * inputs.TokensPerParameter;
        double totalFlops = 6.0 * parameters * totalTokens;

        // --- Step 4: Achieved throughput per MFU tier ---
        // Peak TFLOPs scaled across devices, then apply MFU
        double peakTflops = inputs.TflopsAtPrecision * inputs.NumberOfDevices;
        double peakFlopsPerSecond = peakTflops * 1e12;

        double achievedOptimistic  = peakFlopsPerSecond * MfuOptimistic;
        double achievedProbable    = peakFlopsPerSecond * MfuProbable;
        double achievedPessimistic = peakFlopsPerSecond * MfuPessimistic;

        // --- Step 5: Training time in seconds ---
        double timeOptimistic  = totalFlops / achievedOptimistic;
        double timeProbable    = totalFlops / achievedProbable;
        double timePessimistic = totalFlops / achievedPessimistic;

        return new TrainingTimeResult(
            OptimisticSeconds:            timeOptimistic,
            ProbableSeconds:              timeProbable,
            PessimisticSeconds:           timePessimistic,
            TotalTrainingFlops:           totalFlops,
            TotalTokens:                  totalTokens,
            MaxBatchSize:                 maxBatchSize,
            ParameterMemoryGb:            parameterMemoryGb,
            ActivationMemoryGbPerSample:  activationMemoryGbPerSample,
            MfuOptimistic:                MfuOptimistic,
            MfuProbable:                  MfuProbable,
            MfuPessimistic:               MfuPessimistic,
            AchievedTflopsOptimistic:     achievedOptimistic  / 1e12,
            AchievedTflopsProbable:       achievedProbable    / 1e12,
            AchievedTflopsPessimistic:    achievedPessimistic / 1e12
        );
    }
}