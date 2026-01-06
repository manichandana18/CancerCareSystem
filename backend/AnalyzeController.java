package com.example.backend;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@CrossOrigin(origins = "http://localhost:5174")
public class AnalyzeController {

    @PostMapping("/analyze")
    public ResponseEntity<String> analyzeImage(
            @RequestParam("image") MultipartFile image
    ) {
        System.out.println("Received image: " + image.getOriginalFilename());
        return ResponseEntity.ok("Image received successfully");
    }
}

