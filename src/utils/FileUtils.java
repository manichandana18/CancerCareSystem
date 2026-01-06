package utils;

import java.io.File;

public class FileUtils {

    public static void printLine() {
        System.out.println("--------------------------------------");
    }

    public static void printTitle(String title) {
        printLine();
        System.out.println(title);
        printLine();
    }
    
    public static boolean fileExists(String filePath) {
        File file = new File(filePath);
        return file.exists() && file.isFile();
    }
    
    public static String getFileExtension(String fileName) {
        int lastDot = fileName.lastIndexOf('.');
        if (lastDot > 0 && lastDot < fileName.length() - 1) {
            return fileName.substring(lastDot + 1).toLowerCase();
        }
        return "";
    }
    
    public static boolean isImageFile(String fileName) {
        String extension = getFileExtension(fileName);
        return extension.equals("jpg") || extension.equals("jpeg") || 
               extension.equals("png") || extension.equals("bmp");
    }
    
    public static void printError(String message) {
        System.err.println("ERROR: " + message);
    }
    
    public static void printSuccess(String message) {
        System.out.println("SUCCESS: " + message);
    }
}
