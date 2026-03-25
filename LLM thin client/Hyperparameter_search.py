def calculate_params_intermediate(d_model, d_ffn_factor=4, num_layers=1):
    # Component calculations
    self_attention = 4 * d_model ** 2
    feedforward = 2 * d_model * (d_ffn_factor * d_model)
    layer_norm = 2 * d_model
    
    # Total parameters per layer
    params_per_layer = self_attention + feedforward + layer_norm
    
    # Total parameters for the model
    total_params = params_per_layer * num_layers
    
    return params_per_layer, total_params

def calculate_params_embedding(d_model, vocab_size)
	d_model*vocab_size

def calculate_params_output(output_d_model, vocab_size)
	output_d_model*vocab_size
	
# Example Usage
d_model = 1024
d_ffn_factor = 4
num_layers = 12

params_per_layer, total_params = calculate_params_intermediate(d_model, d_ffn_factor, num_layers)
print(f"Parameters per layer: {params_per_layer}")
print(f"Total model parameters: {total_params}")

#https://chatgpt.com/share/674af14a-8aa0-8003-b1d3-3b5e525c8b46