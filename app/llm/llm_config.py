class ModelConfig:
    """
    Configuration class for setting up parameters related to the LLM model.

    Attributes:
        model_name (str): The identifier or path of the model.
        model_file (str): Path or filename of the quantized model file.
        max_tokens (int): Maximum number of tokens to generate in a single output.
        temperature (float): Controls randomness in output; lower values produce more coherent responses.
        top_k (int): Limits token sampling to top_k most probable tokens after temperature scaling.
        top_p (float): Nucleus sampling threshold; cumulative probability to select tokens.
        repeat_penalty (float): Penalty applied to repeated tokens to reduce redundancy.
        num_beams (int): Number of beams used in beam search to improve output quality.
        n_gpu_layers (int): Number of model layers to offload to GPU (-1 for full GPU usage, -2 for auto).
        n_ctx (int): Context window size; max tokens model can handle at once.
        n_batch (int): Number of tokens processed simultaneously in a batch.
        verbose (bool): Enables verbose logging for debugging if True.
        use_mmap (bool): Enables memory-mapped loading of the model to reduce RAM usage.
        use_mlock (bool): Locks the model into RAM to prevent swapping for performance.
        offload_kqv (bool): Offloads key, query, value matrices to GPU to accelerate inference.
    """

    @staticmethod
    def create_default_instance():
        """
        Create a ModelConfig instance with default parameters.

        Returns:
            ModelConfig: A new ModelConfig object initialized with default values.
        """
        return ModelConfig()

    def __init__(
        self,
        model_name: str = "Raj-Maharajwala/Open-Insurance-LLM-Llama3-8B-GGUF",
        model_file: str = "./open-insurance-llm-q4_k_m.gguf",
        # model_file: str = "open-insurance-llm-q8_0.gguf",  # 8-bit quantization; higher precision, better quality, increased resource usage
        # model_file: str = "open-insurance-llm-q5_k_m.gguf",  # 5-bit quantization; balance between performance and resource efficiency
        max_tokens: int = 1000,
        temperature: float = 0.1,
        top_k: int = 15,
        top_p: float = 0.2,
        repeat_penalty: float = 2.2,
        num_beams: int = 4,
        n_gpu_layers: int = -2,
        n_ctx: int = 2048,
        n_batch: int = 256,
        verbose: bool = False,
        use_mmap: bool = False,
        use_mlock: bool = True,
        offload_kqv: bool = True
    ):
        """
        Initialize a ModelConfig instance with specified or default parameters.

        Args:
            model_name (str): Model identifier or path.
            model_file (str): Path to the quantized model file.
            max_tokens (int): Maximum tokens generated in one output.
            temperature (float): Sampling randomness control.
            top_k (int): Number of top tokens to consider during sampling.
            top_p (float): Cumulative probability for nucleus sampling.
            repeat_penalty (float): Penalty to reduce token repetition.
            num_beams (int): Beam search width.
            n_gpu_layers (int): Number of layers offloaded to GPU (-1 for all, -2 for auto).
            n_ctx (int): Context size for the model.
            n_batch (int): Tokens processed simultaneously in a batch.
            verbose (bool): Enable verbose debug logging.
            use_mmap (bool): Use memory-mapped loading.
            use_mlock (bool): Lock model in RAM.
            offload_kqv (bool): Offload key-query-value matrices to GPU.
        """
        self.model_name = model_name
        self.model_file = model_file
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.repeat_penalty = repeat_penalty
        self.num_beams = num_beams
        self.n_gpu_layers = n_gpu_layers
        self.n_ctx = n_ctx
        self.n_batch = n_batch
        self.verbose = verbose
        self.use_mmap = use_mmap
        self.use_mlock = use_mlock
        self.offload_kqv = offload_kqv

