# Data Flow: Image → K-Means → Recommendation

## Step 1: User uploads an outfit photo
The photo is temporarily saved to disk (e.g. `data/temp_clothing.jpg`) because
OpenCV cannot read a Streamlit upload object directly — it needs a real file path.

## Step 2: K-Means extracts dominant colors
The image is loaded with OpenCV, converted from BGR to RGB, then reshaped from
a 3D array (height x width x 3) into a 2D list of individual pixels using
`.reshape(-1, 3)`. K-Means groups these pixels into 5 clusters, and the center
of each cluster becomes one dominant color.

## Step 3: The most dominant color is identified
Using `np.bincount()` on the cluster labels, we count how many pixels belong
to each cluster and pick the cluster with the most pixels as the outfit's
single dominant color.

## Step 4: Compared against skin tone recommendations
Separately, the user's selfie goes through face detection and HSV analysis to
classify their skin tone as warm/cool/neutral. This lookup returns a list of
recommended colors from `color_rules.json`.

## Step 5: Compatibility verdict shown
The outfit's dominant color is matched to its closest named color (using
Euclidean distance), then checked against the recommended list. The result is
shown as a ✓ or ✗ message in the Streamlit UI.
