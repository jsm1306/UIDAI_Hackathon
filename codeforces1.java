import java.util.*;

public class codeforces1 {
    public static void main(String[] a) {
        Scanner sc=new Scanner(System.in);
        int t=sc.nextInt();
        while(t-->0){
            int n = sc.nextInt();
            for(int i=1;i<=n;i++){
                System.out.print(i+(i<n ? " " : ""));
            }
            System.out.println();
        }
    }
}
