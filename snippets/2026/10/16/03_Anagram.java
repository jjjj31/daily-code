import java.util.Arrays;

public class Anagram {

    static boolean isAnagram(String left, String right) {
        char[] a = left.replaceAll("\\s", "").toLowerCase().toCharArray();
        char[] b = right.replaceAll("\\s", "").toLowerCase().toCharArray();
        Arrays.sort(a);
        Arrays.sort(b);
        return Arrays.equals(a, b);
    }

    public static void main(String[] args) {
        System.out.println(isAnagram("listen", "silent"));
    }
}
