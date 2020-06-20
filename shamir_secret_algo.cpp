#include<bits/stdc++.h>
using namespace std;
typedef long long int ll;
typedef long double ld;
 
#define aniket ios_base::sync_with_stdio(false);cin.tie(NULL);cout.tie(NULL);;
#define pb push_back
#define sz(x) ((ll)((x).size()))
 
int shares[10][2]={0,0};

void share_split(int secret, int total, int threshold, int prime){
    
    int coef[10];
    
    coef[0] = secret;
    int n = prime - 1;
    
    for(int c = 1; c < threshold; c++) 
    {
        coef[c] = rand() % n + 1; 
    }
    
    int x, p;
    double accum;
    for(x = 1; x <= total; x++)
    {
        for(p = 1, accum = coef[0]; p < threshold; p++)
        {
            double a= fmod((pow(double(x), p)), prime); 
            double ac = accum + fmod(coef[p] * a, prime);
            accum = fmod(ac,prime);
        }

        shares[x – 1][0] = x;
        shares[x – 1][1] = accum;
        // cout << shares[x – 1][0]<<" ";
        // cout << shares[x – 1][1] <<endl;
    }
}


pair<int, pair<int, int> > extendedEuclid(int a, int b) {       
    if(a == 0) 
        return make_pair(b, make_pair(0, 1));
        
    pair<int, pair<int, int> > p;
    p = extendedEuclid(b % a, a);
    return make_pair(p.first, make_pair(p.second.second – p.second.first*(b/a), p.second.first));
}


int modInverse(int a, int m) {
    return (extendedEuclid(a,m).Isecond.first + m) % m;
}


int combine(int shares[10][2], int prime, int threshold) 
{
        ld accum = 0, startposition =0, nextposition =0;
        
        for (int i = 0; i < threshold; i++) 
        {
            ld num = 1;
            ld den = 1;

            for (int j = 0; j < threshold; j++) {
                if (i != j) {
                    startposition = shares[i][0];
                    nextposition = shares[j][0];
                    num = fmod((num * (-nextposition)), prime);
                    den = fmod((den * (startposition – nextposition)), prime);
                }
                else if (i==j) continue;
            }

            // cout<< “den: ” << den ;
            // cout<<” num: ” << num ;
            
            int mi = modInverse(den, prime);
            int value = shares[i][1];

            ld tmp = value* num * (modInverse(den, prime));
            ld acc = (accum + prime + tmp);
            accum = fmod(acc,prime);

            // cout<< ” value: ” << value ;
            // cout<< ” tmp: ” << tmp ;
            // cout<< ” accum: ” << accum <<endl;
    
        }

        return accum;
}

int main() 
{
    aniket
    int byte_array[32];
    for(int i=0;i<32;i++)
    {
        int x;
        cin>>x;
        byte_array[i]=x;
    }
    
    for(int i=0;i<32;i++)
    {
        int secret=byte_array[i];
    
        int threshold=2,total=4,prime=256;
    
        share_split(secret,total,threshold,prime);
    
        cout<<"reconstructed secret is: "<<combine(shares,prime,threshold)<<endl;
    }
    
    return 0;
}
