import cv2
import numpy as np
import os

INPUT_COLOR = r"C:\Users\narut\Desktop\Diat\sem 1\Robot vision\Assignemnt\Q2\img2.tif"
OUT_DIR     = r"C:\Users\narut\Desktop\Diat\sem 1\Robot vision\Assignemnt\Q2"

os.makedirs(OUT_DIR, exist_ok=True)

GAUSSIAN_KSIZE = (5,5)        # smoothing before threshold
MORPH_OPEN = (3,3)            # remove tiny noise
MORPH_CLOSE = (7,7)           # fill small holes
FIXED_THRESHOLD = 130

orig_color = cv2.imread(INPUT_COLOR, cv2.IMREAD_COLOR)
if orig_color is None:
    raise FileNotFoundError("Cannot read input image: " + INPUT_COLOR)

# grayscale copy for binarization
orig_gray = cv2.cvtColor(orig_color, cv2.COLOR_BGR2GRAY)

# ---------- FRESH BINARIZATION (50% cutoff) ----------
blur = cv2.GaussianBlur(orig_gray, GAUSSIAN_KSIZE, 0)

# Fixed 50% threshold: pixels >=128 -> white, else black
_, bin_mask = cv2.threshold(blur, FIXED_THRESHOLD, 255, cv2.THRESH_BINARY)

# Ensure objects are white on black background: if majority is white, invert
h, w = bin_mask.shape
white_ratio = (bin_mask == 255).sum() / (h*w)
if white_ratio > 0.6:
    bin_mask = cv2.bitwise_not(bin_mask)

# ---------- Morphological cleaning ----------
k_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, MORPH_OPEN)
k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, MORPH_CLOSE)

bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_OPEN, k_open, iterations=1)
bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, k_close, iterations=1)

# ---------- APPLY MASK TO ORIGINAL COLOR ----------
result = np.full_like(orig_color, 255)            # white background
mask3 = cv2.merge([bin_mask, bin_mask, bin_mask]) # 3-channel mask
result[mask3 == 255] = orig_color[mask3 == 255]

# ---------- SAVE OUTPUTS ----------
mask_file   = os.path.join(OUT_DIR, "img2_fixed50_mask.png")
result_file = os.path.join(OUT_DIR, "img2_fixed50_masked_result.png")

cv2.imwrite(mask_file, bin_mask)
cv2.imwrite(result_file, result)

# ---------- SUMMARY ----------
print("Saved mask:", mask_file)
print("Saved masked result (only white regions kept):", result_file)
print("Mask white pixels:", int(np.count_nonzero(bin_mask == 255)),
      " / ", (h*w), " total pixels")
print("White ratio (mask): {:.3f}".format((bin_mask == 255).sum() / (h*w)))
