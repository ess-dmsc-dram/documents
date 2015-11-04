add_latex_document(minimal-prototype.tex)
add_custom_command(TARGET minimal-prototype_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/minimal-prototype.pdf
    ${CMAKE_BINARY_DIR}/pdf/live_minimal-prototype.pdf)
