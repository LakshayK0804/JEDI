// Main class
public class javaTest1 {
    public static void main(String[] args) {
        // Create objects
        Person person = new Person("Alice", 25);
        Calculator calculator = new Calculator();

        // Test methods
        System.out.println(person.getGreeting());
        person.haveBirthday();
        System.out.println("After birthday: " + person.getAge());

        int sum = calculator.add(10, 20);
        System.out.println("Sum: " + sum);

        int product = calculator.multiply(5, 6);
        System.out.println("Product: " + product);

        Animal dog = new Animal("Dog", "Bark");
        dog.makeSound();
    }
}

// Person class
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getGreeting() {
        return "Hello, my name is " + name + " and I am " + age + " years old.";
    }

    public void haveBirthday() {
        age++;
    }

    public int getAge() {
        return age;
    }
}

// Calculator class
class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero is not allowed.");
        }
        return a / b;
    }
}

// Animal class
class Animal {
    private String species;
    private String sound;

    public Animal(String species, String sound) {
        this.species = species;
        this.sound = sound;
    }

    public void makeSound() {
        System.out.println("The " + species + " goes '" + sound + "'.");
    }
}
