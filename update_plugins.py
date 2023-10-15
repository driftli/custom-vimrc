try:
    import concurrent.futures as futures
except ImportError:
    try:
        import futures
    except ImportError:
        futures = None

import re
import shutil
import tempfile
import urllib.request
import zipfile
from io import BytesIO
from os import path

# --- Globals ----------------------------------------------
PLUGINS = """
vim-colors-dracula https://github.com/dracula/vim
vim-colors-gruvbox https://github.com/morhetz/gruvbox
vim-colors-solarized https://github.com/altercation/vim-colors-solarized
vim-syntax-rust https://github.com/rust-lang/rust.vim
vim-syntax-ruby https://github.com/vim-ruby/vim-ruby
vim-syntax-nginx https://github.com/chr4/nginx.vim
vim-syntax-less https://github.com/groenewege/vim-less
vim-syntax-javascript https://github.com/pangloss/vim-javascript
vim-syntax-typescript https://github.com/leafgarland/typescript-vim
auto-pairs https://github.com/jiangmiao/auto-pairs
ale https://github.com/dense-analysis/ale
vim-yankstack https://github.com/maxbrunsfeld/vim-yankstack
tabular https://github.com/godlygeek/tabular
vim-ack https://github.com/mileszs/ack.vim
bufexplorer https://github.com/jlanzarotta/bufexplorer
vim-ctrlp https://github.com/ctrlpvim/ctrlp.vim
vim-nerdtree https://github.com/preservim/nerdtree
vim-nerdtree-tabs https://github.com/jistr/vim-nerdtree-tabs
open_file_under_cursor.vim https://github.com/amix/open_file_under_cursor.vim
vim-tlib https://github.com/tomtom/tlib_vim
vim-addon-mw-utils https://github.com/MarcWeber/vim-addon-mw-utils
vim-indent-object https://github.com/michaeljsmith/vim-indent-object
vim-snipmate https://github.com/garbas/vim-snipmate
vim-snippets https://github.com/honza/vim-snippets
vim-surround https://github.com/tpope/vim-surround
vim-lastplace https://github.com/farmergreg/vim-lastplace
vim-expand-region https://github.com/terryma/vim-expand-region
vim-multiple-cursors https://github.com/terryma/vim-multiple-cursors
vim-fugitive https://github.com/tpope/vim-fugitive
vim-rhubarb https://github.com/tpope/vim-rhubarb
vim-goyo https://github.com/junegunn/goyo.vim
vim-repeat https://github.com/tpope/vim-repeat
vim-commentary https://github.com/tpope/vim-commentary
vim-gitgutter https://github.com/airblade/vim-gitgutter
vim-flake8 https://github.com/nvie/vim-flake8
vim-lightline https://github.com/itchyny/lightline.vim
vim-lightline-ale https://github.com/maximbaz/lightline-ale
vim-abolish https://github.com/tpope/vim-abolish
vim-markdown https://github.com/plasticboy/vim-markdown
vim-python-pep8-indent https://github.com/Vimjas/vim-python-pep8-indent
vim-indent-guides https://github.com/nathanaelkane/vim-indent-guides
vim-mru https://github.com/yegappan/mru
vim-editorconfig https://github.com/editorconfig/editorconfig-vim
a.vim https://github.com/vim-scripts/a.vim
vim-translator https://github.com/voldikss/vim-translator
tagbar https://github.com/preservim/tagbar
vim-go https://github.com/fatih/vim-go
vim-smoothie https://github.com/psliwka/vim-smoothie
supertab https://github.com/ervandew/supertab
""".strip()

GITHUB_ZIP = "%s/archive/master.zip"

SOURCE_DIR = path.join(path.dirname(__file__), "sources_non_forked")


def download_extract_replace(plugin_name, zip_path, temp_dir, source_dir):
    # Download and extract file in temp dir
    with urllib.request.urlopen(zip_path) as req:
        zip_f = zipfile.ZipFile(BytesIO(req.read()))
        zip_f.extractall(temp_dir)
        content_disp = req.headers.get("Content-Disposition")

    filename = re.findall("filename=(.+).zip", content_disp)[0]
    plugin_temp_path = path.join(temp_dir, path.join(temp_dir, filename))

    # Remove the current plugin and replace it with the extracted
    plugin_dest_path = path.join(source_dir, plugin_name)

    try:
        shutil.rmtree(plugin_dest_path)
    except OSError:
        pass

    shutil.move(plugin_temp_path, plugin_dest_path)
    print("Updated {0}".format(plugin_name))


def update(plugin):
    name, github_url = plugin.split(" ")
    zip_path = GITHUB_ZIP % github_url
    try:
        download_extract_replace(name, zip_path, temp_directory, SOURCE_DIR)
    except Exception as exp:
        print("Could not update {}. Error was: {}".format(name, str(exp)))


if __name__ == "__main__":
    temp_directory = tempfile.mkdtemp()

    try:
        if futures:
            with futures.ThreadPoolExecutor(16) as executor:
                executor.map(update, PLUGINS.splitlines())
        else:
            [update(x) for x in PLUGINS.splitlines()]
    finally:
        shutil.rmtree(temp_directory)
