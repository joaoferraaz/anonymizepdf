# Redator de PDF Gabinete Saboia

Este projeto é uma ferramenta de redação de PDFs que oculta informações pessoais, como CPFs, nomes e placas de carro, utilizando uma interface gráfica amigável.

## Bibliotecas Utilizadas

As seguintes bibliotecas são necessárias para executar este projeto:

- `pymupdf` (fitz)
- `werkzeug`
- `tkinterdnd2`
- `Pillow`
- `tkinter`

## Insttalação das Bibliotecas
```bash
pip install pymupdf
pip install werkzeug
pip install tkinterdnd2
pip install pillow
```


## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
    ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
    ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```
3. Execute o arquivo `interface.py`
    ```bash
    python interface.py
    ```

## Criar um executável
```bash
pyinstaller --onefile --windowed interface.py
pyinstaller --onefile --windowed --add-data "images/logo.png;images" --add-data "images/icon.ico;images" interface.py
```

## Funcionalidades
- Seleção de arquivos PDF para anonimizar.
- Insere uma tarja preta em dados sensiveis.
- Suporte a arrastar e soltar arquivos PDF na interface.