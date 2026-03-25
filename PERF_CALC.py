import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

@dataclass
class PrecisionInfo:
    bytes_per_param: int
    name: str

class CalculatorTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.result_label = ttk.Label(self.frame, text="")
        
    def validate_positive_float(self, value: str) -> float:
        try:
            num = float(value)
            if num <= 0:
                raise ValueError("Value must be positive")
            return num
        except ValueError as e:
            messagebox.showerror("Invalid input", f"Please enter a positive number. Error: {str(e)}")
            raise

class RAMBandwidthCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        entries = [
            ("Bus Width (bits):", "bus_width"),
            ("Memory Clock Speed (MT/s):", "memory_clock"),
            ("Memory Channels:", "channels")
        ]
        
        for label_text, attr_name in entries:
            ttk.Label(self.frame, text=label_text).pack()
            setattr(self, f"{attr_name}_entry", ttk.Entry(self.frame))
            getattr(self, f"{attr_name}_entry").pack()
            
        ttk.Button(self.frame, text="Calculate Bandwidth", command=self.calculate).pack(pady=10)
        self.result_label.pack()
        
    def calculate(self):
        try:
            bus_width = self.validate_positive_float(self.bus_width_entry.get())
            memory_clock = self.validate_positive_float(self.memory_clock_entry.get())
            channels = self.validate_positive_float(self.channels_entry.get())
            
            bandwidth = (bus_width / 8) * memory_clock * channels / 1000  # GB/s
            self.result_label.config(text=f"Memory Bandwidth: {bandwidth:.2f} GB/s")
            return bandwidth
        except ValueError:
            return None

class FLOPSCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.precision_var = tk.StringVar(value="FP32 (Single)")
        self.setup_ui()
        
    def setup_ui(self):
        entries = [
            ("Number of Cores/Processing Units:", "cores"),
            ("Clock Speed (MHz):", "clock_speed"),
            ("Operations per Clock Cycle:", "operations")
        ]
        
        for label_text, attr_name in entries:
            ttk.Label(self.frame, text=label_text).pack()
            setattr(self, f"{attr_name}_entry", ttk.Entry(self.frame))
            getattr(self, f"{attr_name}_entry").pack()
            
        ttk.Label(self.frame, text="Computation Precision:").pack()
        precisions = ["FP64 (Double)", "FP32 (Single)", "FP16 (Half)", "INT8"]
        for precision in precisions:
            ttk.Radiobutton(self.frame, text=precision, variable=self.precision_var, 
                           value=precision).pack()
            
        ttk.Button(self.frame, text="Calculate FLOPS", command=self.calculate).pack(pady=10)
        self.result_label.pack()
        
    def calculate(self):
        try:
            cores = self.validate_positive_float(self.cores_entry.get())
            clock_speed = self.validate_positive_float(self.clock_speed_entry.get())
            operations = self.validate_positive_float(self.operations_entry.get())
            
            precision_multipliers = {
                "FP64 (Double)": 1, "FP32 (Single)": 2,
                "FP16 (Half)": 4, "INT8": 8
            }
            multiplier = precision_multipliers[self.precision_var.get()]
            
            flops = cores * clock_speed * 1e6 * operations * multiplier / 1e12  # TFLOPs
            self.result_label.config(text=f"Computing Power: {flops:.2f} TFLOPs")
            return flops
        except ValueError:
            return None

class TokensPerSecondCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent)
        # Update the dictionary to use the modified PrecisionInfo
        self.precision_info: Dict[str, PrecisionInfo] = {
            "FP32": PrecisionInfo(4, "32-bit Float"), # Removed flops_multiplier
            "FP16": PrecisionInfo(2, "16-bit Float"), # Removed flops_multiplier
            "INT8": PrecisionInfo(1, "8-bit Integer") # Removed flops_multiplier
        }
        self.precision_var = tk.StringVar(value="FP16") # Changed default to FP16 as common choice
        self.param_mode_var = tk.StringVar(value="billions")
        self.setup_ui()
        
    def setup_ui(self):
        entries = [
            # --- MODIFIED LABEL TEXT BELOW ---
            ("TFLOPs (at selected precision):", "tflops"),
            ("Bandwidth (GB/s):", "bandwidth")
        ]

        for label_text, attr_name in entries:
            # Use anchor='w' and padx for better alignment
            ttk.Label(self.frame, text=label_text).pack(pady=(5,0), anchor='w', padx=10)
            setattr(self, f"{attr_name}_entry", ttk.Entry(self.frame))
            # Example default values if desired
            # if attr_name == "tflops":
            #      getattr(self, f"{attr_name}_entry").insert(0, "312") # e.g., H100 FP16
            # elif attr_name == "bandwidth":
            #      getattr(self, f"{attr_name}_entry").insert(0, "2000") # e.g., HBM3
            getattr(self, f"{attr_name}_entry").pack(pady=(0,5), fill='x', padx=10)

        # Parameter input section (no changes needed here, but added padding/anchoring)
        param_frame = ttk.LabelFrame(self.frame, text="Model Parameter Count")
        param_frame.pack(pady=5, padx=10, fill="x") # Use padx consistent with above

        mode_frame = ttk.Frame(param_frame)
        mode_frame.pack(fill="x", pady=2)
        ttk.Radiobutton(mode_frame, text="Billions (e.g., 7 for 7B)",
                       variable=self.param_mode_var, value="billions").pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Absolute (e.g., 7000000000)",
                       variable=self.param_mode_var, value="absolute").pack(side="left", padx=5)

        self.parameters_entry = ttk.Entry(param_frame)
        # Example default
        # self.parameters_entry.insert(0, "7") # e.g., 7B model
        self.parameters_entry.pack(pady=(2, 5), fill='x', padx=5) # Added padding/fill


        # Precision selection (no changes needed here, but added padding/anchoring)
        precision_frame = ttk.LabelFrame(self.frame, text="Calculation Precision") # Renamed title
        precision_frame.pack(pady=5, padx=10, fill="x")
        for precision_key in self.precision_info.keys():
            # Show bytes per param in label for clarity
            info = self.precision_info[precision_key]
            ttk.Radiobutton(precision_frame, text=f"{precision_key} ({info.bytes_per_param} bytes/param)",
                           variable=self.precision_var,
                           value=precision_key).pack(anchor='w', padx=5) # Anchor west

        ttk.Button(self.frame, text="Calculate Tokens/s",
                   command=self.calculate).pack(pady=10)
        self.result_label = ttk.Label(self.frame, text="")
        self.result_label.pack(pady=(0, 5))
        self.bottleneck_label = ttk.Label(self.frame, text="")
        self.bottleneck_label.pack(pady=(0, 5))
        self.potential_label = ttk.Label(self.frame, text="")
        self.potential_label.pack(pady=(0, 5))
        
    def calculate(self) -> Optional[Tuple[float, float, float]]: # Added Optional return type hint
        try:
            # Get input values
            # User now provides TFLOPs specific to the selected precision
            tflops_at_precision = self.validate_positive_float(self.tflops_entry.get())
            bandwidth_gbps = self.validate_positive_float(self.bandwidth_entry.get())
            raw_parameters = self.validate_positive_float(self.parameters_entry.get())

            # Convert parameters based on selected mode
            if self.param_mode_var.get() == "billions":
                parameters = raw_parameters * 1e9
            else:
                parameters = raw_parameters

            precision = self.precision_info[self.precision_var.get()]

            print("\n=== Debug Information (Tokens/s - Corrected Compute) ===")
            print(f"Input - TFLOPS (at {self.precision_var.get()}): {tflops_at_precision}") # Updated label
            print(f"Input - Bandwidth GB/s: {bandwidth_gbps}")
            print(f"Input - Parameters ({self.param_mode_var.get()}): {raw_parameters}")
            print(f"Actual parameter count: {parameters:e}")
            print(f"Selected precision: {precision.name}")
            # print(f"FLOPS multiplier: {precision.flops_multiplier}") # Removed
            print(f"Bytes per parameter: {precision.bytes_per_param}")

            # Compute-bound calculation (Corrected)
            # Rule of thumb: 2 FLOPs per parameter per token for inference forward pass
            flops_per_token = 2 * parameters
            print(f"FLOPS per token (estimated): {flops_per_token:e}")

            # --- MODIFIED CALCULATION BELOW ---
            # Use the provided TFLOPs directly, assuming it matches the selected precision.
            # Remove the incorrect precision.flops_multiplier.
            if flops_per_token == 0: # Avoid division by zero if parameters=0
                 compute_bound_tokens = float('inf') # Or handle as error? Let's allow inf for now.
            else:
                 compute_bound_tokens = (tflops_at_precision * 1e12) / flops_per_token
            print(f"Compute-bound tokens/s: {compute_bound_tokens:.2f}")

            # Bandwidth-bound calculation (No changes needed here)
            bytes_per_token = parameters * precision.bytes_per_param
            print(f"Bytes per token: {bytes_per_token:e}")

            bandwidth_bytes_per_second = bandwidth_gbps * 1e9
            print(f"Bandwidth bytes/s: {bandwidth_bytes_per_second:e}")

            if bytes_per_token == 0: # Avoid division by zero
                bandwidth_bound_tokens = float('inf')
            else:
                bandwidth_bound_tokens = bandwidth_bytes_per_second / bytes_per_token
            print(f"Bandwidth-bound tokens/s: {bandwidth_bound_tokens:.2f}")

            # Determine limiting factor
            tokens_per_second = min(compute_bound_tokens, bandwidth_bound_tokens)
            if tokens_per_second == float('inf'): # Handle case where both are infinite (params=0)
                tokens_per_second = 0.0

            print(f"Final tokens/s: {tokens_per_second:.2f}")
            print("======================================================\n")

            # Update results
            self.result_label.config(
                text=f"Estimated Tokens Per Second: {tokens_per_second:,.2f} tokens/s"
            )

            # Show bottleneck analysis (Logic adjusted for potential inf values)
            # Check for edge case of zero parameters leading to 'inf' bounds
            if compute_bound_tokens == float('inf') and bandwidth_bound_tokens == float('inf'):
                 self.bottleneck_label.config(text="⚠️ Cannot determine bottleneck (likely zero parameters).")
                 self.potential_label.config(text="")
            elif compute_bound_tokens <= bandwidth_bound_tokens: # Use <= to prefer compute-limited in edge cases
                self.bottleneck_label.config(
                    text=f"⚠️ Compute-limited: current compute allows {compute_bound_tokens:,.2f} tokens/s"
                )
                if bandwidth_bound_tokens != float('inf') and flops_per_token > 0:
                    # Recalculate required TFLOPs based on bandwidth limit
                    required_tflops = (bandwidth_bound_tokens * flops_per_token) / 1e12
                    self.potential_label.config(
                        text=f"💡 {required_tflops:.2f} TFLOPs (at {self.precision_var.get()}) needed to match bandwidth limit ({bandwidth_bound_tokens:,.2f} tokens/s)."
                    )
                else:
                    self.potential_label.config(text="") # Cannot calculate potential if bandwidth bound is inf or flops_per_token is 0
            else: # Bandwidth-limited
                self.bottleneck_label.config(
                    text=f"⚠️ Memory-limited: current bandwidth allows {bandwidth_bound_tokens:,.2f} tokens/s"
                )
                if compute_bound_tokens != float('inf') and bytes_per_token > 0:
                    # Recalculate required Bandwidth based on compute limit
                    required_bandwidth = (compute_bound_tokens * bytes_per_token) / 1e9
                    self.potential_label.config(
                        text=f"💡 {required_bandwidth:.2f} GB/s bandwidth needed to match compute limit ({compute_bound_tokens:,.2f} tokens/s)."
                    )
                else:
                     self.potential_label.config(text="") # Cannot calculate potential if compute bound is inf or bytes_per_token is 0


            return tokens_per_second, compute_bound_tokens, bandwidth_bound_tokens
        except ValueError:
             self.result_label.config(text="Invalid input. Please check values.")
             self.bottleneck_label.config(text="")
             self.potential_label.config(text="")
             return None
        except KeyError: # Should not happen now with fixed precision handling
             messagebox.showerror("Internal Error", f"Selected precision '{self.precision_var.get()}' configuration error.")
             self.result_label.config(text="Error: Precision config error.")
             self.bottleneck_label.config(text="")
             self.potential_label.config(text="")
             return None

@dataclass
class MemoryConfig:
    dtype_size: int  # bytes per parameter
    gradient_memory_factor: float = 2.0  # typically 2x for backprop
    optimizer_memory_factor: float = 2.0  # typically 2x for Adam
    framework_overhead_factor: float = 1.1  # 10% overhead for framework

from dataclasses import dataclass
from typing import Dict, Tuple, Optional

@dataclass
class MemoryConfig:
    dtype_size: int  # bytes per parameter
    gradient_memory_factor: float = 2.0  # typically 2x for backprop
    optimizer_memory_factor: float = 2.0  # typically 2x for Adam
    framework_overhead_factor: float = 1.1  # 10% overhead for framework

class TrainingSpeedCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.dtype_var = tk.StringVar(value="FP16")
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container with padding
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Training Speed Section
        speed_frame = ttk.LabelFrame(main_frame, text="Training Speed Parameters")
        speed_frame.pack(fill="x", pady=(0, 10))

        speed_entries = [
            ("Tokens Per Second (Throughput):", "tokens_per_second"), # Renamed for clarity
            ("Dataset Size (Total Samples):", "dataset_size"), # <-- ** NEW ENTRY **
            ("Average Sample Length (Tokens):", "avg_sample_length"), # Renamed for clarity
            ("Samples per Mini-Batch:", "samples_per_batch"),
            ("Number of Epochs:", "epochs")
        ]

        for label_text, attr_name in speed_entries:
            ttk.Label(speed_frame, text=label_text).pack(pady=(5,0), anchor='w', padx=5) # anchor west
            setattr(self, f"{attr_name}_entry", ttk.Entry(speed_frame))
            # Set default values for demonstration if desired
            # if attr_name == "dataset_size":
            #     getattr(self, f"{attr_name}_entry").insert(0, "1000000") # Example: 1M samples
            # elif attr_name == "avg_sample_length":
            #      getattr(self, f"{attr_name}_entry").insert(0, "2048") # Example
            getattr(self, f"{attr_name}_entry").pack(pady=(0,5), fill='x', padx=5)

        ttk.Button(speed_frame, text="Calculate Training Time",
                   command=self.calculate_time).pack(pady=(5,10)) # Added padding
        self.time_result_label = ttk.Label(speed_frame, text="")
        self.time_result_label.pack(pady=(0,10))

        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

        # Memory Requirements Section (keep the rest as is)
        memory_frame = ttk.LabelFrame(main_frame, text="Memory Requirements")
        memory_frame.pack(fill="x", pady=(0, 10))

        # ... (rest of the memory section setup remains the same) ...
        # Note about shared parameters
        ttk.Label(memory_frame,
                 text="Note: Avg Sample Length and Batch Size are used from above", # Updated text
                 font=("TkDefaultFont", 9, "italic")).pack(pady=5)

        memory_entries = [
            ("Hidden Dimension Size:", "hidden_dim"),
            ("Number of Attention Layers:", "num_layers"),
            ("Vocabulary Size:", "vocab_size")
        ]

        for label_text, attr_name in memory_entries:
            ttk.Label(memory_frame, text=label_text).pack(pady=(5,0), anchor='w', padx=5) # anchor west
            setattr(self, f"{attr_name}_entry", ttk.Entry(memory_frame))
            getattr(self, f"{attr_name}_entry").pack(pady=(0,5), fill='x', padx=5)

        # Data type selection
        dtype_frame = ttk.Frame(memory_frame)
        dtype_frame.pack(fill="x", pady=5)
        ttk.Label(dtype_frame, text="Data Type:").pack(side="left", padx=5)
        for dtype in ["FP16", "FP32", "BF16"]:
            ttk.Radiobutton(dtype_frame, text=dtype, variable=self.dtype_var,
                           value=dtype).pack(side="left", padx=5)

        ttk.Button(memory_frame, text="Calculate Memory Requirements",
                   command=self.calculate_memory).pack(pady=(5,10))
        self.memory_result_label = ttk.Label(memory_frame, text="")
        self.memory_result_label.pack(pady=(0,5))
        self.memory_breakdown_label = ttk.Label(memory_frame, text="", justify="left")
        self.memory_breakdown_label.pack(pady=(0,10), anchor='w', padx=5) # anchor west

    def get_dtype_size(self) -> int:
        dtype_sizes = {"FP16": 2, "BF16": 2, "FP32": 4}
        return dtype_sizes[self.dtype_var.get()]
    
    def calculate_time(self):
        try:
            tps = self.validate_positive_float(self.tokens_per_second_entry.get())
            # --- Get the new dataset size ---
            dataset_size = self.validate_positive_float(self.dataset_size_entry.get())
            # --- Get other values ---
            avg_sample = self.validate_positive_float(self.avg_sample_length_entry.get())
            # samples_per_batch = self.validate_positive_float(self.samples_per_batch_entry.get()) # Still needed for memory calc, but not directly for time here
            epochs = self.validate_positive_float(self.epochs_entry.get())

            # --- Corrected Calculation ---
            # Tokens per epoch = total samples in dataset * average tokens per sample
            tokens_per_epoch = dataset_size * avg_sample
            total_training_tokens = tokens_per_epoch * epochs

            if tps == 0: # Avoid division by zero
                 self.time_result_label.config(text="Error: Tokens Per Second cannot be zero.")
                 return None

            time_seconds = total_training_tokens / tps

            # --- Time formatting (no changes needed here) ---
            days = int(time_seconds // (3600 * 24))
            time_seconds %= (3600 * 24)
            hours = int(time_seconds // 3600)
            time_seconds %= 3600
            minutes = int(time_seconds // 60)
            seconds = time_seconds % 60

            time_str = ""
            if days > 0:
                time_str += f"{days}d "
            if hours > 0 or days > 0: # Show hours if days > 0 even if hours is 0
                time_str += f"{hours}h "
            if minutes > 0 or hours > 0 or days > 0: # Show minutes if needed
                 time_str += f"{minutes}m "
            time_str += f"{seconds:.1f}s"


            self.time_result_label.config(
                # text=f"Estimated Training Time: {hours}h {minutes}m {seconds:.1f}s" # Old format
                text=f"Estimated Training Time: {time_str.strip()}" # New format
            )

            # --- Updated CLI output ---
            print("\n=== Training Speed Calculation (Corrected) ===")
            print(f"Input Parameters:")
            print(f"- Tokens per second (Throughput): {tps:,.2f}")
            print(f"- Dataset Size (Total Samples): {dataset_size:,.0f}") # New
            print(f"- Average Sample Length (Tokens): {avg_sample:,.0f}")
            # print(f"- Samples per batch: {samples_per_batch:,.0f}") # Not directly used in time calc now
            print(f"- Number of Epochs: {epochs:,.0f}")
            print(f"\nDerived Values:")
            print(f"- Tokens per Epoch: {tokens_per_epoch:,.0f}") # Corrected
            print(f"- Total Tokens to Process: {total_training_tokens:,.0f}") # Corrected
            print(f"\nResults:")
            # print(f"- Total training time: {hours}h {minutes}m {seconds:.1f}s") # Old format
            print(f"- Total training time: {time_str.strip()}") # New format
            print(f"- Time in seconds: {total_training_tokens / tps:.1f}s") # Use original time_seconds here
            print("=============================================\n")

            return total_training_tokens / tps # Return time in seconds
        except ValueError:
             self.time_result_label.config(text="Invalid input. Please check values.")
             return None
        except ZeroDivisionError: # Should be caught by tps == 0 check, but good practice
             self.time_result_label.config(text="Error: Tokens Per Second cannot be zero.")
             return None
    
    def calculate_memory(self) -> Optional[Dict[str, float]]:
        try:
            # Get all required values
            hidden_dim = self.validate_positive_float(self.hidden_dim_entry.get())
            num_layers = self.validate_positive_float(self.num_layers_entry.get())
            vocab_size = self.validate_positive_float(self.vocab_size_entry.get())
            
            # Get shared values from training speed section
            try:
                samples_per_batch = self.validate_positive_float(self.samples_per_batch_entry.get())
                seq_length = self.validate_positive_float(self.avg_sample_length_entry.get())
            except ValueError:
                messagebox.showerror("Missing Values", 
                                   "Please fill in Sample Length and Batch Size in the Training Speed section")
                return None
            
            config = MemoryConfig(dtype_size=self.get_dtype_size())
            
            # Calculate different memory components (in bytes)
            
            # Embedding layer (input + output embeddings)
            embedding_memory = vocab_size * hidden_dim * config.dtype_size * 2
            
            # Attention layer weights (Q,K,V matrices and output projection per layer)
            attention_weights_memory = num_layers * 4 * hidden_dim * hidden_dim * config.dtype_size
            
            # Feed-forward layer weights (two matrices per layer)
            ff_weights_memory = num_layers * 2 * hidden_dim * hidden_dim * 4 * config.dtype_size  # 4x hidden dim for FF
            
            # Memory for attention activations during forward pass
            attention_activations = (samples_per_batch * seq_length * hidden_dim * 4 * 
                                   config.dtype_size * num_layers)  # 4x for Q,K,V,O
            
            # Memory for feed-forward activations
            ff_activations = (samples_per_batch * seq_length * hidden_dim * 4 * 
                            config.dtype_size * num_layers)
            
            # Total weights memory
            weights_memory = attention_weights_memory + ff_weights_memory + embedding_memory
            
            # Total activations memory
            activations_memory = attention_activations + ff_activations
            
            # Memory for gradients (backward pass)
            gradient_memory = (weights_memory + activations_memory) * config.gradient_memory_factor
            
            # Memory for optimizer states
            optimizer_memory = weights_memory * config.optimizer_memory_factor
            
            # Total memory with framework overhead
            total_memory = ((weights_memory + activations_memory + gradient_memory + 
                           optimizer_memory) * config.framework_overhead_factor)
            
            # Convert to GB for display
            memory_components = {
                "Model Weights": weights_memory / (1024**3),
                "Activations": activations_memory / (1024**3),
                "Gradients": gradient_memory / (1024**3),
                "Optimizer States": optimizer_memory / (1024**3),
                "Total (with overhead)": total_memory / (1024**3)
            }
            
            # CLI output
            print("\n=== Memory Requirements Calculation ===")
            print(f"Model Architecture:")
            print(f"- Hidden dimension: {hidden_dim:,}")
            print(f"- Number of layers: {num_layers}")
            print(f"- Vocabulary size: {vocab_size:,}")
            print(f"- Data type: {self.dtype_var.get()} ({config.dtype_size} bytes)")
            
            print(f"\nBatch Configuration:")
            print(f"- Sequence length: {seq_length:,}")
            print(f"- Batch size: {samples_per_batch}")
            
            print(f"\nMemory Breakdown:")
            for component, size in memory_components.items():
                print(f"- {component}: {size:.2f} GB")
            
            print(f"\nMemory Factors Applied:")
            print(f"- Gradient memory factor: {config.gradient_memory_factor}x")
            print(f"- Optimizer memory factor: {config.optimizer_memory_factor}x")
            print(f"- Framework overhead factor: {config.framework_overhead_factor}x")
            print("====================================\n")
            
            # Update display
            self.memory_result_label.config(
                text=f"Total Memory Required: {memory_components['Total (with overhead)']:.2f} GB"
            )
            
            # Create detailed breakdown
            breakdown_text = "Memory Breakdown:\n"
            for component, size in memory_components.items():
                breakdown_text += f"  • {component}: {size:.2f} GB\n"
            self.memory_breakdown_label.config(text=breakdown_text)
            
            return memory_components
        except ValueError:
            return None 

@dataclass
class StoragePrecisionInfo:
    bytes_per_param: int
    name: str

class StorageRequirementsCalculator(CalculatorTab):
    def __init__(self, parent):
        super().__init__(parent)
        self.precision_info: Dict[str, StoragePrecisionInfo] = {
            "FP32": StoragePrecisionInfo(4, "32-bit Float (Single Precision)"),
            "FP16": StoragePrecisionInfo(2, "16-bit Float (Half Precision)"),
            "BF16": StoragePrecisionInfo(2, "BFloat16"),
            "INT8": StoragePrecisionInfo(1, "8-bit Integer"),
            # Add more if needed, e.g., INT4: StoragePrecisionInfo(0.5, "4-bit Integer")
        }
        self.precision_var = tk.StringVar(value="FP16")  # Default to a common storage format
        self.param_mode_var = tk.StringVar(value="billions") # Match other tabs
        self.setup_ui()

    def setup_ui(self):
        # Parameter input section
        param_frame = ttk.LabelFrame(self.frame, text="Model Parameter Count")
        param_frame.pack(pady=10, padx=10, fill="x")

        # Parameter mode selection
        mode_frame = ttk.Frame(param_frame)
        mode_frame.pack(fill="x", pady=(5, 2))
        ttk.Radiobutton(mode_frame, text="Billions (e.g., 7 for 7B)",
                       variable=self.param_mode_var, value="billions").pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Absolute (e.g., 7000000000)",
                       variable=self.param_mode_var, value="absolute").pack(side="left", padx=5)

        # Parameter entry
        self.parameters_entry = ttk.Entry(param_frame)
        self.parameters_entry.pack(pady=(2, 10), fill="x", padx=5)

        # Precision selection
        precision_frame = ttk.LabelFrame(self.frame, text="Storage Precision (Data Type)")
        precision_frame.pack(pady=5, padx=10, fill="x")

        for key, info in self.precision_info.items():
            ttk.Radiobutton(precision_frame, text=f"{key} ({info.bytes_per_param} bytes/param)",
                           variable=self.precision_var,
                           value=key).pack(anchor="w", padx=5)

        ttk.Button(self.frame, text="Calculate Storage Size",
                   command=self.calculate).pack(pady=15)

        # Result display
        self.result_label.pack(pady=(0, 5)) # Use the inherited result_label
        self.clarification_label = ttk.Label(self.frame,
                                            text="Note: This estimates raw weight storage size (e.g., for download/deployment).",
                                            font=("TkDefaultFont", 9, "italic"))
        self.clarification_label.pack(pady=(0, 10))


    def calculate(self) -> Optional[float]:
        try:
            # Get input values
            raw_parameters = self.validate_positive_float(self.parameters_entry.get())
            selected_precision_key = self.precision_var.get()

            # Convert parameters based on selected mode
            if self.param_mode_var.get() == "billions":
                parameters = raw_parameters * 1e9
            else:
                parameters = raw_parameters

            # Get bytes per parameter for the selected precision
            precision = self.precision_info[selected_precision_key]
            bytes_per_param = precision.bytes_per_param

            # Calculate total bytes
            total_bytes = parameters * bytes_per_param

            # Convert to Gigabytes (using decimal GB = 1e9 bytes, common for storage)
            total_gb = total_bytes / 1e9

            print("\n=== Storage Requirements Calculation ===")
            print(f"Input Parameters ({self.param_mode_var.get()}): {raw_parameters}")
            print(f"Actual Parameter Count: {parameters:e}")
            print(f"Selected Precision: {selected_precision_key} ({bytes_per_param} bytes/param)")
            print(f"Total Bytes: {total_bytes:e}")
            print(f"Total Gigabytes (GB): {total_gb:.2f}")
            print("====================================\n")

            # Update result label
            self.result_label.config(
                text=f"Estimated Storage Size: {total_gb:.2f} GB"
            )
            return total_gb

        except ValueError:
            self.result_label.config(text="Invalid input. Please check values.")
            return None
        except KeyError:
            messagebox.showerror("Internal Error", f"Selected precision '{selected_precision_key}' not found.")
            self.result_label.config(text="Error: Precision not found.")
            return None

class PerformanceCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LLM Performance & Resource Calculator") # Updated title slightly
        self.notebook = ttk.Notebook(self.root)

        # Initialize existing calculator tabs
        self.ram_calc = RAMBandwidthCalculator(self.notebook)
        self.flops_calc = FLOPSCalculator(self.notebook)
        self.tokens_calc = TokensPerSecondCalculator(self.notebook)
        self.training_speed_calc = TrainingSpeedCalculator(self.notebook)

        # *** Initialize the new storage calculator tab ***
        self.storage_calc = StorageRequirementsCalculator(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.ram_calc.frame, text="RAM Bandwidth")
        self.notebook.add(self.flops_calc.frame, text="FLOPS Calculator")
        self.notebook.add(self.tokens_calc.frame, text="Tokens Per Second (Inference)") # Clarified tab name
        self.notebook.add(self.training_speed_calc.frame, text="Training Estimates") # Clarified tab name
        # *** Add the new storage tab ***
        self.notebook.add(self.storage_calc.frame, text="Model Storage Size")

        self.notebook.pack(expand=True, fill="both", padx=5, pady=5) # Added padding

    def run(self):
        # Optional: Set a minimum size for the window
        self.root.minsize(450, 500)
        self.root.mainloop()


if __name__ == "__main__":
    app = PerformanceCalculator()
    app.run()