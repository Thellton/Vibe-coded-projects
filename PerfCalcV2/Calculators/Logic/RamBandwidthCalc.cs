using System;

namespace PerfCalcV2.Calculators.Logic; // Update this line

public static class RamBandwidthCalculator
{
    /// <summary>
    /// Calculates Theoretical Memory Bandwidth as expressed in GB per second
    /// <param name=busWidthBits>bus width in bits (e.g. 128)</param>
    /// <param name=memoryClockMT>memory clock speed in MT per second (e.g. 3200)</param>
    /// <param name=channels>number of memory channels</param>
    /// <returns>Bandwidth in GB per second</returns>
    /// <exception cref="ArgumentOutOfRangeException">
    /// Thrown when any input is zero or negative
    /// </exception>
    public static double CalculateGbps(double busWidthBits, double memoryClockMt, double channels)
    {
        if (busWidthBits <= 0) {
            throw new ArgumentOutOfRangeException(nameof(busWidthBits));
        }
        if (memoryClockMt <= 0) {
            throw new ArgumentOutOfRangeException(nameof(memoryClockMt));
        }
        if (channels <= 0) {
            throw new ArgumentOutOfRangeException(nameof(channels));
        }
        
        //convert bits to bytes, MegaTransfers per s to transfers per second, then scale to GB per second.
        return busWidthBits/8.0 * memoryClockMt * channels / 1000.0;

    }
}