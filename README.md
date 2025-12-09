
Methodology used

1.	Load Image
The original color image is read and converted to grayscale for processing.
2.	Noise Reduction
A Gaussian blur is applied to smooth the image and reduce noise before thresholding.
3.	50% Threshold Binarization
A fixed threshold at 128 (50% intensity) is applied so that all pixels ≥128 become white (foreground) and others become black (background).
4.	Morphological Cleaning
Morphological opening removes small noise, and closing fills small holes in the binary mask to make the foreground regions clean and continuous.
5.	Image Subtraction (Mask Application)
The binary mask is used to subtract/block unwanted regions: pixels in black areas are replaced with white, while pixels in white regions keep the original texture.
This produces an output where only the desired white-mask regions pass through from the original image.
6.	Save Output
The cleaned mask and the masked image are saved.

Change the file input path and output path according to need.

```python
py seperate.py
