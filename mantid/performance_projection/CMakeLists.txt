add_latex_document(performance_projection.tex)
add_custom_command(TARGET performance_projection_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/performance_projection.pdf
    ${CMAKE_BINARY_DIR}/pdf/mantid_performance_projection.pdf)
