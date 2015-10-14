add_latex_document(notes.tex)
add_custom_command(TARGET notes_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/notes.pdf
    ${CMAKE_BINARY_DIR}/pdf/mantid_frontend_backend_architecture.pdf)
