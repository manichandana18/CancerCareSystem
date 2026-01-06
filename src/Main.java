import preprocessing.ImageLoader;
import text.TextualInfoGenerator;
import utils.FileUtils;
import api.PythonAPIClient;

public class Main {
    public static void main(String[] args) {
        FileUtils.printTitle("BONE CANCER DETECTION SYSTEM");
        
        // Use command line argument if provided, otherwise use default
        String imagePath = args.length > 0 ? args[0] : "sample_xray.jpg";
        
        System.out.println("Loading image: " + imagePath);
        ImageLoader loader = new ImageLoader();
        String imageData = loader.loadImage(imagePath);
        
        if (imageData == null || imageData.isEmpty()) {
            System.out.println("ERROR: Could not load image file.");
            return;
        }
        
        System.out.println("Connecting to Python backend API...");
        String apiResponse = PythonAPIClient.callPredictAPI(imagePath);
        
        System.out.println("\nPYTHON BACKEND RESPONSE:");
        System.out.println(apiResponse);
        
        // Parse the API response to extract prediction result
        String result = parseApiResponse(apiResponse);
        
        // Display textual information based on the result
        TextualInfoGenerator.showInfo(result);
        
        FileUtils.printLine();
        System.out.println("Analysis complete!");
    }
    
    private static String parseApiResponse(String apiResponse) {
        // Parse JSON response to extract prediction
        if (apiResponse.contains("Tumor Detected") || apiResponse.contains("\"prediction\":\"Tumor")) {
            return "Tumor";
        } else if (apiResponse.contains("No Tumor") || apiResponse.contains("\"prediction\":\"No Tumor")) {
            return "No Tumor";
        } else if (apiResponse.contains("ERROR")) {
            return "Error";
        }
        return "Unknown";
    }
}



