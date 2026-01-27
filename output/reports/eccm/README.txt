## Compliation 
This review was compiled using LaTeX and is best view in PDF format. The manuscript submitted in .docx format was compiled from LaTeX, so some features, such as section and figure referencing, do not work. Files for PDF LaTeX compilation are provided in saltb.zip and the structure and contents are outline below.

## File Structure 

eccm
|
manuscript.tex - manuscript LaTeX source code.
manuscript.pdf - manuscript in PDF format.
prisma_checklist.odt - PRISMA Checklist in ODT Format.
prisma_checklist.pdf - PRISMA Checklist in PDF format.
supplement.tex - supplementary material LaTeX source code.
supplement.pdf - supplementary material in PDF format.
|
taylor-and-francis-vancouver-national-library-of-medicine.csl - for reference styling with pandoc to .docx/.odt format.
bibliography.bib - bibliography.
|
...other auxiliary files from pdf generation
|
|----figures - figures in the journals desired format.
|----sections - LaTeX source code of sections used in manuscript.tex.
|----styles - Custom styles required for LaTeX compilation.
|----tables - LaTeX source code of tables used in manuscript.tex.