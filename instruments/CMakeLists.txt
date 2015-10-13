add_latex_document(questionnaire.tex)
add_custom_command(TARGET questionnaire_pdf POST_BUILD COMMAND
    ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/questionnaire.pdf
    ${CMAKE_BINARY_DIR}/pdf/instruments_questionnaire.pdf)
