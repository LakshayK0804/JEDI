public class javaTest1 {
    // Unused variable
    int a;
    public static void main(String[] args) {
        // Example 1: NullPointerException due to calling method on null object
        String str = null;
        System.out.println(str.length()); // Throws NullPointerException

        // Example 2: NullPointerException due to accessing a null element in an array
        String[] arr = new String[2];
        arr[0] = "Hello";
        arr[1] = null;
        System.out.println(arr[1].toUpperCase()); // Throws NullPointerException because arr[1] is null

        // Example 3: NullPointerException in a method call with null parameter
        printMessage(null); // Throws NullPointerException in printMessage

        // Example 4: NullPointerException when trying to access an element in a null
        // List
        java.util.List<String> list = null;
        System.out.println(list.size()); // Throws NullPointerException because list is null

        // Example 5: NullPointerException in a Map where key's value is null
        java.util.Map<String, String> map = new java.util.HashMap<>();
        map.put("key", null);
        System.out.println(map.get("key").length()); // Throws NullPointerException because value is null
        int a;
        // Example 6: NullPointerException when using null value in a method return
        String result = getNullValue();
        System.out.println(result.length()); // Throws NullPointerException because result is nulljavaTest1.java
    }

    // Example of a method that returns null
    public static String getNullValue() {
        return null;
    }

    // Method that throws NullPointerException if the parameter is null
    public static void printMessage(String message) {
        System.out.println(message.toUpperCase()); // Throws NullPointerException when message is null
    }
}