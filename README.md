# CR3 to PNG Converter

A high-performance Python utility for converting Canon RAW (CR3) image files to PNG format with support for batch processing and quality customization.

![CR3 to PNG Converter](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-orange)

## 🌟 Features

- 🚀 **Fast Batch Processing**: Convert multiple CR3 files simultaneously
- 🎨 **High-Quality Output**: Preserve image quality with customizable settings
- 📁 **Organized Workflow**: Automatic directory structure management
- 📊 **Progress Tracking**: Real-time progress bar for conversion tracking
- 🛠 **Robust Error Handling**: Comprehensive logging and error reporting
- 🖼 **Parallel Processing**: Utilizes multi-threading for faster conversions
- 🎚 **Customizable**: Adjust quality and optimization settings

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Trynityneo/Cr3-PNG.git
   cd Cr3-PNG
   ```

2. **Create and activate a virtual environment (recommended)**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Basic Usage

1. Place your CR3 files in the `cr3_images` directory
2. Run the converter:
   ```bash
   python converter.py
   ```
3. Find your converted PNG files in the `png_images` directory

### Advanced Options

```bash
python converter.py -i input_directory -o output_directory --quality 95 --no-optimize --overwrite
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-i`, `--input` | Input directory containing CR3 files | `cr3_images` |
| `-o`, `--output` | Output directory for PNG files | `png_images` |
| `-q`, `--quality` | PNG quality (1-100) | `95` |
| `--no-optimize` | Disable PNG optimization | `False` |
| `--overwrite` | Overwrite existing files | `False` |
| `-v`, `--verbose` | Enable verbose output | `False` |

## 📁 Project Structure

```
Cr3-PNG/
├── cr3_images/         # Input directory for CR3 files
├── png_images/         # Output directory for PNG files
├── .venv/             # Virtual environment (created during setup)
├── converter.py       # Main conversion script
├── requirements.txt    # Python dependencies
└── converter.log      # Log file (generated after first run)
```

## 🛠 Development

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests (when available):
   ```bash
   python -m pytest
   ```

### Code Style

This project follows PEP 8 style guidelines. To check and format the code:

```bash
# Check code style
flake8 .


# Auto-format code
black .
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Trynity Neo - [@Tryni18796313](https://twitter.com/Tryni18796313)

Project Link: [https://github.com/Trynityneo/Cr3-PNG](https://github.com/Trynityneo/Cr3-PNG)

## 🙏 Acknowledgments

- [rawpy](https://pypi.org/project/rawpy/) - For CR3 file processing
- [Pillow](https://python-pillow.org/) - For image processing
- [tqdm](https://github.com/tqdm/tqdm) - For progress bars
- [Choose an Open Source License](https://choosealicense.com)
- [Shields.io](https://shields.io/)

---

<div align="center">
  Made with ❤️ by VishnuXrobot
</div>
