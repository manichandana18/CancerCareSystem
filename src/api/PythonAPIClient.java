package api;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class PythonAPIClient {

    public static String callPredictAPI(String imagePath) {
        try {
            String boundary = "----Boundary123";
            URL url = new URL("http://127.0.0.1:8000/predict");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();

            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            conn.setRequestProperty(
                    "Content-Type",
                    "multipart/form-data; boundary=" + boundary
            );

            OutputStream outputStream = conn.getOutputStream();
            PrintWriter writer = new PrintWriter(
                    new OutputStreamWriter(outputStream, "UTF-8"), true
            );

            File file = new File(imagePath);

            writer.append("--").append(boundary).append("\r\n");
            writer.append("Content-Disposition: form-data; name=\"file\"; filename=\"")
                    .append(file.getName()).append("\"\r\n");
            writer.append("Content-Type: image/jpeg\r\n\r\n");
            writer.flush();

            FileInputStream fis = new FileInputStream(file);
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
            outputStream.flush();
            fis.close();

            writer.append("\r\n--").append(boundary).append("--\r\n");
            writer.close();

            BufferedReader br = new BufferedReader(
                    new InputStreamReader(conn.getInputStream())
            );

            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            br.close();

            return response.toString();

        } catch (Exception e) {
            return "ERROR: " + e.getMessage();
        }
    }
}

