import torch

def test_gpu():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"CUDA is available. Using device: {torch.cuda.get_device_name(device)}")
        x = torch.rand(3, 3, device=device)
        y = torch.rand(3, 3, device=device)
        z = x + y
        print("Tensor operation successful on GPU.")
    else:
        print("CUDA is not available. Using CPU.")
        device = torch.device("cpu")
        x = torch.rand(3, 3, device=device)
        y = torch.rand(3, 3, device=device)
        z = x + y
        print("Tensor operation successful on CPU.")

if __name__ == "__main__":
    test_gpu()
