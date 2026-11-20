# tBookFold 📖✨

A simple Python tool to convert black-and-white images into custom **book folding patterns**.

## 🚀 Getting Started

### Prerequisites

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### Usage

Import and run the `create` function from `bookfold.py` to generate your pattern:

```python
from bookfold import create

# Example usage (see examples/ folder for full script)
create("examples/ornament.jpg")
```

## 📂 Examples

Check out the `examples/` folder for a sample input image, the corresponding Python script, and the generated PDF pattern.

<table>
  <tr>
    <th width="50%">Original Image</th>
    <th width="50%">Generated Fold Pattern (Page 1)</th>
  </tr>
  <tr>
    <td align="center">
      <img src="examples/ornament.jpg" alt="Original Ornament Image" width="100%">
    </td>
    <td align="center">
      <!-- Hinweis: GitHub rendert PDFs nicht direkt in <img>-Tags. 
           Speichere die 1. Seite als PNG (z. B. ornament_preview.png) für eine direkte Bildvorschau: -->
      <a href="examples/ornament_faltmuster.pdf#page=1">
        <img src="examples/ornament_preview.png" alt="Book Fold Pattern Preview (Page 1)" width="100%">
      </a>
      <br>
      <a href="examples/ornament_faltmuster.pdf#page=1">📄 View PDF (Page 1)</a>
    </td>
  </tr>
</table>
