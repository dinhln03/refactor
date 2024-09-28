

## Prerequisites

- Python 3.10+
- conda
- npm (see https://nodejs.org/en/download/package-manager )

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dinhln03/refactor.git
   cd refactor
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   conda create -n aic python=3.10 
   conda activate aic
   pip install -r requirements.txt
   ```

3. Import media-info, bin file and ison file into data dir
   ![alt text](image.png)
    Make sure that content of files look like this:
    - media-info
    ![alt text](image-1.png)
    - json
    ![alt text](image-2.png)
4. Import keyFrame folder into image-search-ui/public
![image](https://github.com/user-attachments/assets/0bcb07e1-cad0-4825-849d-ef76fdf7a8d7)
5. Run backend
   ```bash

   python app.py
   ```

6. Run frontend
   ```bash
   cd image-search-ui
   npm install
   npm start
   ```
Demo:
https://github.com/user-attachments/assets/7a13c8f5-4e91-424a-be80-e4487e8c448d
