package preprocessing;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import utils.FileUtils;

public class ImageLoader {

    public String loadImage(String path) {
        // Check if file exists
        if (!FileUtils.fileExists(path)) {
            FileUtils.printError("Image file not found: " + path);
            return null;
        }
        
        // Check if it's a valid image file
        if (!FileUtils.isImageFile(path)) {
            FileUtils.printError("Invalid image file format. Supported: jpg, jpeg, png, bmp");
            return null;
        }
        
        File file = new File(path);
        try {
            FileInputStream fis = new FileInputStream(file);
            byte[] imageBytes = new byte[(int) file.length()];
            fis.read(imageBytes);
            fis.close();
            
            FileUtils.printSuccess("Image loaded successfully: " + file.getName() + 
                                  " (" + file.length() + " bytes)");
            return "image-loaded"; // Return success indicator
        } catch (IOException e) {
            FileUtils.printError("Failed to read image file: " + e.getMessage());
            return null;
        }
    }
}


