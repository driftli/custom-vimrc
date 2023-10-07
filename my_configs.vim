set number
set wildmenu

let g:solarized_termcolors=256
set colorscheme solarized

""""""""""""""""""""""""""""""
" => taglist plugin
""""""""""""""""""""""""""""""
" Set taglist window toggle
nnoremap <leader>m :TlistToggle <CR> 
" Disable that vim window width can increased to accommodate the new taglist window
let Tlist_Inc_Winwidth=0
" Make the vertically split taglist window appear on the right
let Tlist_Use_Right_Window=1
" To automatically close the tags tree for inactive files
let Tlist_File_Fold_Auto_Close=1
" Exit vim if only the taglist window is currently opened
let Tlist_Exit_OnlyWindow=1


