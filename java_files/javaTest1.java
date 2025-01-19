public class javaTest1 {

    public static void main(String[] args) {
        // Variable Declarations and Initializations
        int num = 10;
        double pi = 3.14159;
        String message = "Hello, Java!";

        // Variable Usage in Expressions
        int doubledNum = num * 2;
        double area = pi * num * num;
        String upperMessage = message.toUpperCase();

        // Usage in Conditional Statements
        if (num > 5) {
            System.out.println("Num is greater than 5");
        }

        // Usage in Loops
        for (int i = 0; i < num; i++) {
            System.out.println("Loop iteration: " + i);
        }

        // Usage in Method Calls
        printMessage(message);
        System.out.println("Square of num: " + square(num));

        // Usage in Arrays
        int[] array = new int[num];
        for (int i = 0; i < array.length; i++) {
            array[i] = i * 2;
        }

        // Usage in Try-Catch
        try {
            int result = num / 0;
        } catch (ArithmeticException e) {
            System.out.println("Caught exception: " + e.getMessage());
        }
    }

    public static void printMessage(String msg) {
        System.out.println("Message: " + msg);
    }

    public static int square(int n) {
        return n * n;
    }
}
