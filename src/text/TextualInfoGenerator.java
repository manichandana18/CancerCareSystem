package text;

public class TextualInfoGenerator {

    public static void showInfo(String result) {

        System.out.println("\nTEXTUAL INFORMATION");
        System.out.println("-------------------");

        if (result.contains("Tumor")) {
            System.out.println("Possible bone tumor detected");
            System.out.println("Consult a specialist");
            System.out.println("Early detection helps");
            System.out.println("Stay strong and positive");
        } else {
            System.out.println("No tumor detected");
            System.out.println("Maintain healthy habits");
            System.out.println("Consult doctor if pain continues");
        }

        System.out.println("-------------------");
    }
}
