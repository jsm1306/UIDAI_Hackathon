import java.util.*;

public class codeforces1 {
    public static void main(String[] a) {
        Scanner s = new Scanner(System.in);
        int t = s.nextInt();
        while (t-- > 0) {
            int n = s.nextInt();
            for (int i = 1; i <= n; i++) {
                System.out.print(i + (i < n ? " " : ""));
            }
            System.out.println();
        }
    }
}
