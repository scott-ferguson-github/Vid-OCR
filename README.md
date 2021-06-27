# Vid-OCR

The goal of the project is to convert a video of a text document
(or, possibly, someone turning pages of a book) and convert it
to text.

### Status

We have just begun.  As such there is no usable code.  We are
simply using github as a method to share our exploratory code.
As such we have no build/install info.

It may never turn into anything (e.g. an Android app).
What we have already noticed is that the "scan" video camera, although
1920 x 1080, has very inconsistent lighting and highly curved
pages.  One gets much higher quality from a simple flatbed scanner.

### Libraries We Intend to Use

We are using python3 and plan to use:

1.  opencv  (on Ubuntu/Debian the package is python3-opencv).  These
are the standard python bindings to the opencv library.

2.  tesserocr  (on Ubuntu/Debian the package in python3-tesserocr).  This
is a more recent set of bindings to the tesseract library.

