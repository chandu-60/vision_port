# VisionPort 🚦

**VisionPort** is a vision-based traffic object detection prototype built with **YOLOv8n, PyTorch, Streamlit, and FastAPI**. It accepts traffic images, detects objects, and provides an inference API with request-stage tracing. PyTorch uses CUDA when a compatible NVIDIA GPU setup is available, otherwise the application falls back to CPU.

> **Current release:** v0.1 — Initial Prototype  
> **Project status:** Core image inference and API gateway are implemented; training, evaluation, and deployment optimisation modules are planned.

## ✨ Features

- **Traffic image detection:** Upload a JPG, JPEG, or PNG image through the Streamlit interface.
- **YOLOv8n inference:** Uses Ultralytics' pretrained YOLOv8n model to identify objects.
- **Automatic device selection:** Uses CUDA when `torch.cuda.is_available()` is true; otherwise runs on CPU.
- **Streamlit interface:** Displays the uploaded image and the annotated detection result.
- **FastAPI inference gateway:** Provides a health endpoint and an image tracing endpoint.
- **Inference request tracing:** Reports processing stages, tensor shapes, execution device, detection results, and timings.

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Object detection | YOLOv8n / Ultralytics |
| Deep learning | PyTorch, Torchvision |
| Image processing | Pillow, NumPy |
| Web interface | Streamlit |
| API backend | FastAPI |
| ASGI server | Uvicorn |
| GPU acceleration | NVIDIA CUDA (when compatible) |

## 📁 Project Structure

```text
VisionPort/
├── app.py                  # Streamlit image detection application
├── env_check.py            # Environment and CUDA diagnostic script
├── env_report.md           # Environment report captured during development
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # Locked dependency versions
├── data/                   # Reserved for datasets
├── docs/                   # Project documentation
├── eval/                   # Reserved for evaluation tools
├── logs/                   # Reserved for application logs
├── models/                 # Model files (YOLO weights may be downloaded on first run)
├── optimise/               # Reserved for model optimisation
├── train/                  # Reserved for training pipeline
└── serve/
    ├── __init__.py
    ├── gateway.py          # FastAPI gateway
    └── gateway_trace.py    # FastAPI gateway with inference tracing
```

*The `train/`, `eval/`, and `optimise/` directories are placeholders for planned work; the corresponding full pipelines are not implemented in this prototype.*

## 💻 Development Environment

The project can use the following local hardware configuration:

| Component | Configuration |
|---|---|
| GPU | NVIDIA GeForce RTX 4060 |
| Deep learning framework | PyTorch |
| GPU compute | CUDA-enabled PyTorch build and compatible NVIDIA driver |
| Python | 3.11 or newer |
| Operating system | Windows / Linux |

**Important:** The RTX 4060 is the GPU in the target local setup. Actual CUDA use depends on the installed NVIDIA driver and a compatible PyTorch build. Run `python env_check.py` to inspect the active environment. The committed `env_report.md` is a snapshot from a different development machine, so its reported GPU may not match your computer.

## ⚙️ Installation

### 1. Open the project folder

Download or clone the repository, then open the `VisionPort` folder in PyCharm. In the terminal, move into the project root (the folder containing `app.py`).

### 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> **CUDA note:** `requirements.txt` contains pinned PyTorch/CUDA package versions from the development environment. If installation fails or PyTorch cannot detect your RTX 4060, install a PyTorch build compatible with your installed NVIDIA driver by following the official [PyTorch installation selector](https://pytorch.org/get-started/locally/). Then verify CUDA using the commands below.

## ▶️ How to Run

### Option 1: Streamlit application

From the project root, run:

```bash
streamlit run app.py
```

Open the local address printed in the terminal (usually `http://localhost:8501`). Upload a traffic image in JPG, JPEG, or PNG format to view the detection output.

### Option 2: FastAPI gateway

Open a second terminal in the project root and run:

```bash
python -m uvicorn serve.gateway_trace:app --reload
```

Open the interactive API documentation:

- `http://127.0.0.1:8000/docs`

Available endpoints in the tracing gateway:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check gateway status and selected device |
| `POST` | `/trace` | Upload a JPEG/PNG image and receive detections plus processing-stage timings |

The `/trace` endpoint accepts an image file and optional `conf` and `iou` query parameters.

## 🧪 Verify NVIDIA GPU / CUDA

Run the environment diagnostic script:

```bash
python env_check.py
```

You can also check PyTorch CUDA availability directly:

```bash
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU mode')"
```

Expected GPU name on the target machine: **NVIDIA GeForce RTX 4060**. If CUDA availability is `False`, the project can still run on CPU, but inference may be slower.

## ⚠️ Current Limitations & Planned Work

- The current application uses pretrained YOLOv8n weights; it is not yet trained specifically for Indian traffic conditions.
- The training, evaluation, and optimisation directories are currently placeholders.
- Custom dataset preparation and model training are future enhancements.
- mAP evaluation, latency benchmarking, and throughput reporting are planned.
- ONNX export, TensorRT optimisation, and Triton deployment are planned future enhancements.
- GPU acceleration requires compatible NVIDIA drivers and CUDA-enabled PyTorch.

## 📌 Version

**VisionPort v0.1 — Initial Prototype**

This README describes the functionality present in the current project files and distinguishes implemented features from planned modules.
