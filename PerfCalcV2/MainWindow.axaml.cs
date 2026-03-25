using System;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;
using PerfCalcV2.Calculators.Logic;
using PerfCalcV2.Calculators.Models;

namespace PerfCalcV2;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    // --- HELPER: Safe Enum Parsing ---
    // Helper to safely extract string from ComboBox and parse to Enum
    private T ParseEnumFromCombo<T>(ComboBox combo, T defaultValue) where T : struct
    {
        var item = combo.SelectedItem as ComboBoxItem;
        if (item?.Content == null) return defaultValue;
        
        string content = item.Content.ToString()!;
        if (Enum.TryParse<T>(content, out var result))
        {
            return result;
        }
        return defaultValue;
    }

     // --- TAB 1: RAM BANDWIDTH ---
    private void OnCalculateRamClick(object sender, RoutedEventArgs e)
    {
        try
        {
            // FIX: Use '?? string.Empty' to handle potential nulls safely.
            // If the box is empty/null, Parse throws FormatException, which we catch below.
            double bus = double.Parse(RamBusWidthBox.Text ?? string.Empty);
            double clock = double.Parse(RamClockBox.Text ?? string.Empty);
            double channels = double.Parse(RamChannelsBox.Text ?? string.Empty);

            // 2. Call Logic
            double bandwidth = RamBandwidthCalculator.CalculateGbps(bus, clock, channels);

            // 3. Update UI
            RamResultLabel.Text = $"Bandwidth: {bandwidth:F2} GB/s";
        }
        catch (FormatException)
        {
            RamResultLabel.Text = "Error: Please check your input numbers.";
        }
        catch (Exception ex)
        {
            RamResultLabel.Text = $"Error: {ex.Message}";
        }
    }

    // --- TAB 2: FLOPS ---
    private void OnCalculateFlopsClick(object sender, RoutedEventArgs e)
    {
        try
        {
            // FIX: Handle null text inputs
            double cores = double.Parse(FlopsCoresBox.Text ?? string.Empty);
            double clock = double.Parse(FlopsClockBox.Text ?? string.Empty);
            double ops = double.Parse(FlopsOpsBox.Text ?? string.Empty);

            // FIX: Handle ComboBox null safety
            var selectedItem = FlopsPrecisionCombo.SelectedItem as ComboBoxItem;
            
            // Check if nothing is selected or the content is somehow null
            if (selectedItem?.Content == null) 
            {
                FlopsResultLabel.Text = "Error: Please select a precision.";
                return;
            }

            // We now know Content is not null, so ToString() is safe.
            string precisionString = selectedItem.Content.ToString()!; 
            
            // Convert string "FP16" -> Enum ComputePrecision.FP16
            ComputePrecision precision = Enum.Parse<ComputePrecision>(precisionString);

            // Call Logic
            double tflops = FlopsCalculator.CalculateTflops(cores, ops, clock, precision);

            FlopsResultLabel.Text = $"Performance: {tflops:F2} TFLOPS";
        }
        catch (FormatException)
        {
            FlopsResultLabel.Text = "Error: Invalid numbers entered.";
        }
        catch (Exception ex)
        {
            FlopsResultLabel.Text = $"Error: {ex.Message}";
        }
    }

    // --- TAB 3: TOKENS PER SECOND ---
    private void OnCalculateTokensClick(object sender, RoutedEventArgs e)
    {
        try
        {
            // 1. Get Inputs
            double tflops = double.Parse(TpsTflopsBox.Text ?? string.Empty);
            double bw = double.Parse(TpsBandwidthBox.Text ?? string.Empty);
            double paramsVal = double.Parse(TpsParamsBox.Text ?? string.Empty);

            // 2. Get Enums
            ParameterScale scale = ParseEnumFromCombo(TpsScaleCombo, ParameterScale.Billions);
            ComputePrecision precision = ParseEnumFromCombo(TpsPrecisionCombo, ComputePrecision.FP16);

            // 3. Calculate
            var result = TokensPerSecondCalc.Calculate(tflops, bw, paramsVal, scale, precision);

            // 4. Update UI
            TpsResultLabel.Text = $"{result.TokensPerSecond:F2} tokens/s";

            // 5. Bottleneck Logic
            if (result.ComputeBoundTokensPerSecond < result.BandwidthBoundTokensPerSecond)
            {
                // Compute Bound
                TpsResultLabel.Foreground = Brushes.OrangeRed;
                TpsBottleneckLabel.Text = $"⚠️ Compute Limited\n(Bandwidth allows up to {result.BandwidthBoundTokensPerSecond:F2} t/s)";
            }
            else
            {
                // Memory Bound
                TpsResultLabel.Foreground = Brushes.DodgerBlue;
                TpsBottleneckLabel.Text = $"⚠️ Memory Bandwidth Limited\n(Compute allows up to {result.ComputeBoundTokensPerSecond:F2} t/s)";
            }
        }
        catch (Exception ex)
        {
            TpsResultLabel.Text = "Error";
            TpsBottleneckLabel.Text = ex.Message;
        }
    }

    // --- TAB 4: TRAINING TIME ---
    private void OnCalculateTrainingClick(object sender, RoutedEventArgs e)
    {
        try
        {
            // 1. Parse inputs
            double tflops      = double.Parse(TrainTflopsBox.Text     ?? string.Empty);
            double bandwidth   = double.Parse(TrainBandwidthBox.Text  ?? string.Empty);
            double vram        = double.Parse(TrainVramBox.Text       ?? string.Empty);
            int    devices     = int.Parse(TrainDevicesBox.Text       ?? string.Empty);
            double parameters  = double.Parse(TrainParamsBox.Text     ?? string.Empty);
            double tokensPerP  = double.Parse(TrainTokensPerParamBox.Text ?? string.Empty);
            int    seqLen      = int.Parse(TrainSeqLenBox.Text        ?? string.Empty);
            int    embedDim    = int.Parse(TrainEmbedDimBox.Text      ?? string.Empty);
            int    layerCount  = int.Parse(TrainLayerCountBox.Text    ?? string.Empty);

            ParameterScale  scale     = ParseEnumFromCombo(TrainScaleCombo,     ParameterScale.Billions);
            ComputePrecision precision = ParseEnumFromCombo(TrainPrecisionCombo, ComputePrecision.BF16);

            // 2. Build inputs record and calculate
            var inputs = new TrainingInputs(
                TflopsAtPrecision:            tflops,
                BandwidthGbps:                bandwidth,
                VramGbPerDevice:              vram,
                NumberOfDevices:              devices,
                RawParameters:                parameters,
                ParameterScale:               scale,
                Precision:                    precision,
                TokensPerParameter:           tokensPerP,
                AverageSequenceLengthTokens:  seqLen,
                EmbeddingDim:                 embedDim,
                LayerCount:                   layerCount
            );

            var result = TrainingTimeCalc.Calculate(inputs);

            // 3. Format time as days / hours / minutes
            TrainOptimisticLabel.Text  = $"⚡ Optimistic:   {FormatDuration(result.OptimisticSeconds)}";
            TrainProbableLabel.Text    = $"📊 Probable:     {FormatDuration(result.ProbableSeconds)}";
            TrainPessimisticLabel.Text = $"🐢 Pessimistic:  {FormatDuration(result.PessimisticSeconds)}";

            // 4. Explanatory breakdown
            TrainExplanationLabel.Text =
                $"Total tokens: {result.TotalTokens:E2}  |  Total FLOPs: {result.TotalTrainingFlops:E2}\n" +
                $"Parameter memory (weights + grads + AdamW): {result.ParameterMemoryGb:F1} GB\n" +
                $"Activation memory per sample: {result.ActivationMemoryGbPerSample:F3} GB\n" +
                $"Max batch size (VRAM-limited): {result.MaxBatchSize:F0}\n" +
                $"Achieved TFLOPs — Optimistic: {result.AchievedTflopsOptimistic:F1} " +
                $"| Probable: {result.AchievedTflopsProbable:F1} " +
                $"| Pessimistic: {result.AchievedTflopsPessimistic:F1}\n" +
                $"MFU tiers: {result.MfuOptimistic:P0} / {result.MfuProbable:P0} / {result.MfuPessimistic:P0}\n" +
                $"Assumes AdamW optimizer, no gradient checkpointing, ideal device parallelism.";
        }
        catch (FormatException)
        {
            TrainOptimisticLabel.Text  = "Error: Please check your input numbers.";
            TrainProbableLabel.Text    = string.Empty;
            TrainPessimisticLabel.Text = string.Empty;
            TrainExplanationLabel.Text = string.Empty;
        }
        catch (Exception ex)
        {
            TrainOptimisticLabel.Text  = $"Error: {ex.Message}";
            TrainProbableLabel.Text    = string.Empty;
            TrainPessimisticLabel.Text = string.Empty;
            TrainExplanationLabel.Text = string.Empty;
        }
    }

    // --- HELPER: Format seconds as Xd Xh Xm ---
    private static string FormatDuration(double totalSeconds)
    {
        if (double.IsInfinity(totalSeconds) || double.IsNaN(totalSeconds))
            return "N/A";

        int days    = (int)(totalSeconds / 86400);
        int hours   = (int)((totalSeconds % 86400) / 3600);
        int minutes = (int)((totalSeconds % 3600) / 60);

        if (days > 0)
            return $"{days}d {hours}h {minutes}m";
        if (hours > 0)
            return $"{hours}h {minutes}m";
        return $"{minutes}m";
    }

    // --- TAB 5: STORAGE ---
    private void OnCalculateStorageClick(object sender, RoutedEventArgs e)
    {
        try
        {
            double rawParams = double.Parse(StorageParamsBox.Text ?? string.Empty);
            
            ParameterScale scale = ParseEnumFromCombo(StorageScaleCombo, ParameterScale.Billions);
            ComputePrecision precision = ParseEnumFromCombo(StoragePrecisionCombo, ComputePrecision.FP16);

            var result = ModelStorageCalculator.Calculate(rawParams, scale, precision);

            // Display in GB if big enough, otherwise MB
            if (result.Gigabytes >= 1.0)
                StorageResultLabel.Text = $"Est. Size: {result.Gigabytes:F2} GB";
            else
                StorageResultLabel.Text = $"Est. Size: {result.Megabytes:F2} MB";
        }
        catch { StorageResultLabel.Text = "Error: Check inputs"; }
    }

}