public class CancerDetector {

    public String detect(String imageData) {
        if (imageData == null || imageData.length() == 0) {
            return "No Tumor";
        } else {
            return "Tumor";
        }
    }
}

