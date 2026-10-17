public class Palindrome {

    static boolean isPalindrome(String input) {
        String normalized = input.replaceAll("[^A-Za-z0-9]", "").toLowerCase();
        int left = 0;
        int right = normalized.length() - 1;
        while (left < right) {
            if (normalized.charAt(left) != normalized.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }

    public static void main(String[] args) {
        String[] samples = {"world", "hello", "radar", "noon", "level"};
        for (String sample : samples) {
            System.out.println(sample + " -> " + isPalindrome(sample));
        }
    }
}
