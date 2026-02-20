.. _static_analysis:

#########################################
Static Analysis Tools and Code Formatters
#########################################

********
Overview
********

Static analysis tools (also called "linters") examine source code without executing it, identifying potential issues related to performance, correctness, maintainability, and security throughout the development process. These can help developers detect bugs,
ineﬃciencies, and parallelization opportunities before runtime–saving valuable time and computational resources. By automating code reviews and enforcing coding standards, static analysis tools are complementary to compilers, debuggers and proﬁlers, and contribute signiﬁcantly to producing reliable, optimized, and portable code.

Code formatting tools are utilities that automatically format source code to follow consistent style guidelines, and because of the commonalities in the underlying infrastructure, are often associated with static analysis tools. These tools adjust things like indentation, spacing, alignment, and the ordering of declarations, without changing the actual behavior of the code. They are invaluable for improving code readability, ensuring consistency across a project, reducing style-related errors, and making collaboration easier among developers. Formatting tools help maintain clean and maintainable code.


Clang-format (for C, C++)
============

`Clang-format <https://clang.llvm.org/docs/ClangFormat.html>`_ is a tool that automatically formats C, C++, and other code according to a set of style rules. It ensures consistent code formatting across a project by applying predeﬁned or custom coding style guidelines, such as the LLVM, Google, or Mozilla styles. By integrating into development workﬂows, clang-format helps maintain readable and uniform code, reducing the need for manual formatting during code reviews.


Clang-tidy (for C++)
==========

`Clang-tidy <https://clang.llvm.org/extra/clang-tidy/>`_ is a clang-based C++ “linter” tool. Its purpose is to provide an extensible framework for diagnosing and ﬁxing typical programming errors, like style violations, interface misuse, or bugs that can be deduced via static analysis.

Using the Clang tools
===========

To utilize clang-format or clang-tidy, you will need to load the modules:

.. code-block:: bash

    $ module load rocm rocm-llvm-toolchain

Codee Formatter (for Fortran)
===============

Codee offers powerful and highly customizable formatting capabilities for Fortran code, enabling development teams to enforce coding standards and maintain a consistent style across large codebases. To learn how to use Codee formatter capabilities, refer to this `introductory step-by-step guide <https://docs.codee.com/formatter/introduction/>`_. Additionally, Codee Formatter `guides <https://docs.codee.com/formatter/>`_ are available in the oﬃcial online documentation where you can also explore the `style options <https://docs.codee.com/formatter/style-options/>`_ section to review all available customization options.

Codee Analyzer (for C, C++, Fortran)
==============

Codee is an “all-in-one” tool to enhance correctness, modernization, security, portability and optimization in Fortran and C/C++ software applications. You can see the various checks that Codee Analyzer is capable of performing in their `Open Catalog <https://open-catalog.codee.com/>`_. To learn how to use Codee analyzer capabilities, refer to the `quickstart guides <https://docs.codee.com/quickstarts/>`_ available in Codee’s online documentation.

Using Codee
===========

To utilize Codee, you will need to load the module:

.. code-block:: bash

    $ module load codee