class ModelConfig:
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
        repeat_penalty: float = 1.2,
        num_beams: int = 4,
        n_gpu_layers: int = -2,
        n_ctx: int = 2048,
        n_batch: int = 256,
        verbose: bool = False,
        use_mmap: bool = False,
        use_mlock: bool = True,
        offload_kqv: bool = True
    ):
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

    @staticmethod
    def create_default_instance():
        return ModelConfig()
