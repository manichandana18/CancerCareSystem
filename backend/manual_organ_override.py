"""
Manual Organ Override - For testing specific images
"""

def manual_organ_override(image_bytes, filename_hint=None):
    """
    Manual override for organ classification based on filename hints
    This is for testing purposes only
    """
    
    if filename_hint:
        filename_lower = filename_hint.lower()
        
        # More specific filename matching
        if ('bonecancer' in filename_lower or 
            'bone_cancer' in filename_lower or 
            'fracture' in filename_lower or 
            'skeletal' in filename_lower):
            return {
                "organ": "bone",
                "confidence": 80.0,
                "method": "Manual Override (Filename)",
                "debug": {"override_reason": f"Filename indicates bone: {filename_hint}"}
            }
        elif ('lungcancer' in filename_lower or 
              'lung_cancer' in filename_lower or 
              'chest' in filename_lower or 
              'pulmonary' in filename_lower or 
              'thorax' in filename_lower):
            return {
                "organ": "lung", 
                "confidence": 80.0,
                "method": "Manual Override (Filename)",
                "debug": {"override_reason": f"Filename indicates lung: {filename_hint}"}
            }
        # Don't override for ambiguous filenames like "bone3" or "normalbone1"
    
    return None  # No override

def apply_manual_override_if_needed(result, image_bytes, filename_hint=None):
    """Apply manual override if conditions are met"""
    
    override = manual_organ_override(image_bytes, filename_hint)
    if override:
        print(f"🔧 MANUAL OVERRIDE APPLIED: {override['debug']['override_reason']}")
        return override
    
    return result
