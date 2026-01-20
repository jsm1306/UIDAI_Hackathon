import java.util.*;


public class codeforces1 {
    public static void main (String[] args) throws java.lang.Exception {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();  // number of test cases
        while(t-- > 0){
            int n = sc.nextInt();  // number of perfect roots to output
            List<Integer> res = new ArrayList<>();
            
            // Just take first n integers as perfect roots
            for(int i = 1; i <= n; i++){
                res.add(i);
            }
            
            // Print them space-separated
            for(int i = 0; i < res.size(); i++){
                System.out.print(res.get(i));
                if(i < res.size() - 1) System.out.print(" ");
            }
            System.out.println();
        }
    }
}