call CambiarIndentacion(2)

augroup Config
    autocmd!
    autocmd Filetype html,javascript,typescript :call CambiarIndentacion(2)
augroup END
