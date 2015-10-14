add_latex_document(ess.tex)
add_custom_command(TARGET ess_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/ess.pdf
    ${CMAKE_BINARY_DIR}/pdf/mantid_ess.pdf)

add_latex_document(frontend-backend-architecture.tex)
add_custom_command(TARGET frontend-backend-architecture_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/frontend-backend-architecture.pdf
    ${CMAKE_BINARY_DIR}/pdf/mantid_frontend-backend-architecture.pdf)

add_latex_document(mpi.tex)
add_custom_command(TARGET mpi_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/mpi.pdf
    ${CMAKE_BINARY_DIR}/pdf/mantid_mpi.pdf)

add_latex_document(performance-projection.tex)
add_custom_command(TARGET performance-projection_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/performance-projection.pdf
    ${CMAKE_BINARY_DIR}/pdf/mantid_performance-projection.pdf)
