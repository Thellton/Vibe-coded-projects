namespace PerfCalcV2.Calculators.Models;

public record TrainingInputs(
    double TflopsAtPrecision,       // Peak TFLOPs, user supplied
    double BandwidthGbps,           // Memory bandwidth, user supplied
    double VramGbPerDevice,         // VRAM per device in GB
    int NumberOfDevices,
    double RawParameters,           // Model size
    ParameterScale ParameterScale,
    ComputePrecision Precision,
    double TokensPerParameter,      // Training target
    int AverageSequenceLengthTokens,
    int EmbeddingDim,
    int LayerCount
);