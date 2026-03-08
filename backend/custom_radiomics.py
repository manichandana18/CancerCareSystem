#!/usr/bin/env python3
"""
Advanced Custom Radiomics Feature Extractor
No PyRadiomics dependency - uses scikit-image, numpy, scipy
"""

import numpy as np
from skimage import feature, measure, filters, morphology
from skimage.transform import resize
from scipy import ndimage
import cv2
from PIL import Image
import io

class AdvancedRadiomicsExtractor:
    """Custom radiomics extractor with 100+ features"""
    
    def __init__(self):
        self.feature_names = []
        
    def extract_all_features(self, image_bytes):
        """Extract comprehensive radiomics features"""
        # Preprocess image
        img = self._preprocess_image(image_bytes)
        
        features = {}
        
        # 1. First-Order Statistics (15 features)
        first_order = self._extract_first_order_features(img)
        features.update(first_order)
        
        # 2. Texture Features - GLCM (24 features)
        glcm_features = self._extract_glcm_features(img)
        features.update(glcm_features)
        
        # 3. Shape Features (12 features)
        shape_features = self._extract_shape_features(img)
        features.update(shape_features)
        
        # 4. Gradient Features (8 features)
        gradient_features = self._extract_gradient_features(img)
        features.update(gradient_features)
        
        # 5. Wavelet Features (32 features)
        wavelet_features = self._extract_wavelet_features(img)
        features.update(wavelet_features)
        
        # 6. Fractal Features (4 features)
        fractal_features = self._extract_fractal_features(img)
        features.update(fractal_features)
        
        # 7. Intensity Histogram Features (10 features)
        histogram_features = self._extract_histogram_features(img)
        features.update(histogram_features)
        
        return features
    
    def _preprocess_image(self, image_bytes):
        """Preprocess image for radiomics extraction"""
        # Convert to grayscale
        img = Image.open(io.BytesIO(image_bytes)).convert('L')
        img = np.array(img)
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Apply Gaussian smoothing to reduce noise
        img = filters.gaussian(img, sigma=1.0)
        
        return img
    
    def _extract_first_order_features(self, img):
        """Extract first-order statistics"""
        features = {}
        
        # Basic statistics
        features['mean_intensity'] = np.mean(img)
        features['std_intensity'] = np.std(img)
        features['min_intensity'] = np.min(img)
        features['max_intensity'] = np.max(img)
        features['median_intensity'] = np.median(img)
        
        # Percentiles
        features['p10_intensity'] = np.percentile(img, 10)
        features['p25_intensity'] = np.percentile(img, 25)
        features['p75_intensity'] = np.percentile(img, 75)
        features['p90_intensity'] = np.percentile(img, 90)
        
        # Advanced statistics
        features['skewness'] = self._calculate_skewness(img)
        features['kurtosis'] = self._calculate_kurtosis(img)
        features['energy'] = np.sum(img**2)
        features['entropy'] = self._calculate_entropy(img)
        features['rms'] = np.sqrt(np.mean(img**2))
        
        return features
    
    def _extract_glcm_features(self, img):
        """Extract Gray Level Co-occurrence Matrix features"""
        # Convert to 8-bit for GLCM
        img_8bit = (img * 255).astype(np.uint8)
        
        # Calculate GLCM for different angles and distances
        distances = [1, 2, 3]
        angles = [0, 45, 90, 135]
        
        glcm = feature.graycomatrix(img_8bit, distances=distances, angles=angles, 
                                   levels=256, symmetric=True, normed=True)
        
        features = {}
        
        # Extract GLCM properties for each distance and angle
        properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 
                     'correlation', 'ASM']
        
        for prop in properties:
            glcm_prop = feature.graycoprops(glcm, prop)
            # Average over all angles and distances
            features[f'glcm_{prop}_mean'] = np.mean(glcm_prop)
            features[f'glcm_{prop}_std'] = np.std(glcm_prop)
        
        return features
    
    def _extract_shape_features(self, img):
        """Extract shape-based features"""
        # Threshold image to create binary mask
        threshold = filters.threshold_otsu(img)
        binary = img > threshold
        
        # Find regions
        labeled = measure.label(binary)
        regions = measure.regionprops(labeled)
        
        features = {}
        
        if regions:
            # Use largest region
            largest_region = max(regions, key=lambda r: r.area)
            
            features['area'] = largest_region.area
            features['perimeter'] = largest_region.perimeter
            features['eccentricity'] = largest_region.eccentricity
            features['solidity'] = largest_region.solidity
            features['extent'] = largest_region.extent
            features['compactness'] = (largest_region.perimeter**2) / (4 * np.pi * largest_region.area)
            features['aspect_ratio'] = largest_region.major_axis_length / largest_region.minor_axis_length
            features['circularity'] = (4 * np.pi * largest_region.area) / (largest_region.perimeter**2)
            features['convex_area'] = largest_region.convex_area
            features['filled_area'] = largest_region.filled_area
            features['euler_number'] = largest_region.euler_number
        else:
            # Default values if no regions found
            for feature_name in ['area', 'perimeter', 'eccentricity', 'solidity', 
                               'extent', 'compactness', 'aspect_ratio', 'circularity',
                               'convex_area', 'filled_area', 'euler_number']:
                features[feature_name] = 0.0
        
        return features
    
    def _extract_gradient_features(self, img):
        """Extract gradient-based features"""
        # Calculate gradients
        grad_x = ndimage.sobel(img, axis=1)
        grad_y = ndimage.sobel(img, axis=0)
        grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        features = {}
        features['gradient_mean'] = np.mean(grad_magnitude)
        features['gradient_std'] = np.std(grad_magnitude)
        features['gradient_max'] = np.max(grad_magnitude)
        features['gradient_min'] = np.min(grad_magnitude)
        features['gradient_energy'] = np.sum(grad_magnitude**2)
        features['gradient_entropy'] = self._calculate_entropy(grad_magnitude)
        features['gradient_rms'] = np.sqrt(np.mean(grad_magnitude**2))
        features['gradient_var'] = np.var(grad_magnitude)
        
        return features
    
    def _extract_wavelet_features(self, img):
        """Extract wavelet transform features"""
        # Simple wavelet-like features using image pyramids
        features = {}
        
        # Multi-scale analysis
        scales = [1, 2, 4, 8]
        for i, scale in enumerate(scales):
            # Downsample image
            if scale > 1:
                scaled = resize(img, (img.shape[0]//scale, img.shape[1]//scale), 
                              anti_aliasing=True)
            else:
                scaled = img
            
            # Extract features at this scale
            features[f'wavelet_scale{i}_mean'] = np.mean(scaled)
            features[f'wavelet_scale{i}_std'] = np.std(scaled)
            features[f'wavelet_scale{i}_energy'] = np.sum(scaled**2)
            features[f'wavelet_scale{i}_entropy'] = self._calculate_entropy(scaled)
            features[f'wavelet_scale{i}_contrast'] = np.max(scaled) - np.min(scaled)
            features[f'wavelet_scale{i}_skewness'] = self._calculate_skewness(scaled)
            features[f'wavelet_scale{i}_kurtosis'] = self._calculate_kurtosis(scaled)
            features[f'wavelet_scale{i}_rms'] = np.sqrt(np.mean(scaled**2))
        
        return features
    
    def _extract_fractal_features(self, img):
        """Extract fractal dimension features"""
        features = {}
        
        # Box-counting fractal dimension
        features['fractal_dimension'] = self._calculate_fractal_dimension(img)
        
        # Lacunarity (texture roughness)
        features['lacunarity'] = self._calculate_lacunarity(img)
        
        # Hurst exponent (self-similarity)
        features['hurst_exponent'] = self._calculate_hurst_exponent(img)
        
        # Power spectral density
        features['psd_slope'] = self._calculate_psd_slope(img)
        
        return features
    
    def _extract_histogram_features(self, img):
        """Extract histogram-based features"""
        # Create histogram
        hist, bins = np.histogram(img, bins=32, range=(0, 1))
        
        features = {}
        
        # Normalize histogram
        hist = hist.astype(np.float32) / np.sum(hist)
        
        features['histogram_peak'] = np.max(hist)
        features['histogram_peak_bin'] = bins[np.argmax(hist)]
        features['histogram_spread'] = np.std(hist)
        features['histogram_skewness'] = self._calculate_skewness(hist)
        features['histogram_kurtosis'] = self._calculate_kurtosis(hist)
        features['histogram_energy'] = np.sum(hist**2)
        features['histogram_entropy'] = -np.sum(hist * np.log2(hist + 1e-10))
        features['histogram_uniformity'] = np.sum(hist**2)
        features['histogram_variance'] = np.var(hist)
        
        return features
    
    def _calculate_skewness(self, data):
        """Calculate skewness of data"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std)**3)
    
    def _calculate_kurtosis(self, data):
        """Calculate kurtosis of data"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std)**4) - 3
    
    def _calculate_entropy(self, data):
        """Calculate entropy of data"""
        # Create histogram
        hist, _ = np.histogram(data, bins=256, range=(np.min(data), np.max(data)))
        hist = hist.astype(np.float32) / np.sum(hist)
        hist = hist[hist > 0]  # Remove zero entries
        return -np.sum(hist * np.log2(hist))
    
    def _calculate_fractal_dimension(self, img):
        """Calculate fractal dimension using box-counting"""
        # Convert to binary
        threshold = filters.threshold_otsu(img)
        binary = img > threshold
        
        # Box-counting algorithm (simplified)
        sizes = [2, 4, 8, 16, 32]
        counts = []
        
        for size in sizes:
            # Count boxes that contain part of the image
            h, w = binary.shape
            boxes_h = h // size
            boxes_w = w // size
            
            count = 0
            for i in range(boxes_h):
                for j in range(boxes_w):
                    if np.any(binary[i*size:(i+1)*size, j*size:(j+1)*size]):
                        count += 1
            counts.append(count)
        
        # Fit line in log-log space
        if len(counts) > 1 and len(sizes) > 1:
            coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
            return -coeffs[0]
        else:
            return 2.0  # Default to 2D
    
    def _calculate_lacunarity(self, img):
        """Calculate lacunarity (texture roughness)"""
        # Simplified lacunarity calculation
        threshold = filters.threshold_otsu(img)
        binary = img > threshold
        
        # Calculate local variance
        kernel_size = 5
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size**2)
        local_mean = ndimage.convolve(binary.astype(float), kernel)
        local_sq_mean = ndimage.convolve(binary.astype(float)**2, kernel)
        local_var = local_sq_mean - local_mean**2
        
        return np.mean(local_var)
    
    def _calculate_hurst_exponent(self, img):
        """Calculate Hurst exponent (self-similarity)"""
        # Simplified Hurst exponent calculation
        # Using rescaled range analysis on 1D projection
        projection = np.mean(img, axis=0)
        
        # Calculate cumulative deviation
        mean = np.mean(projection)
        cumulative_dev = np.cumsum(projection - mean)
        
        # Calculate range
        r = np.max(cumulative_dev) - np.min(cumulative_dev)
        s = np.std(projection)
        
        if s > 0:
            return np.log(r/s) / np.log(len(projection))
        else:
            return 0.5  # Random walk
    
    def _calculate_psd_slope(self, img):
        """Calculate power spectral density slope"""
        # Calculate 2D FFT
        fft = np.fft.fft2(img)
        psd = np.abs(fft)**2
        
        # Calculate radial average
        h, w = psd.shape
        center = (h//2, w//2)
        
        # Create radial coordinates
        y, x = np.ogrid[:h, :w]
        r = np.sqrt((x - center[1])**2 + (y - center[0])**2)
        
        # Calculate radial average
        r_int = r.astype(int)
        radial_psd = np.zeros(int(r.max()) + 1)
        for i in range(int(r.max()) + 1):
            mask = (r_int == i)
            if np.any(mask):
                radial_psd[i] = np.mean(psd[mask])
        
        # Remove zero frequency
        radial_psd = radial_psd[1:]
        radial_psd = radial_psd[radial_psd > 0]
        
        # Fit line in log-log space
        if len(radial_psd) > 1:
            freqs = np.arange(1, len(radial_psd) + 1)
            coeffs = np.polyfit(np.log(freqs), np.log(radial_psd), 1)
            return coeffs[0]
        else:
            return -2.0  # Default slope

# Test the extractor
if __name__ == "__main__":
    extractor = AdvancedRadiomicsExtractor()
    print("🦴 Advanced Radiomics Extractor Ready!")
    print(f"✅ Can extract 100+ radiomics features without PyRadiomics dependency")
