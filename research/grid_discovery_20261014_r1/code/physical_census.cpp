// Independent exhaustive embedding census: no abstract realization predicate.
// Build: c++ -O2 -std=c++17 physical_census.cpp -o physical_census
// Run: ./physical_census 3 > fresh.json
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>
int parity(unsigned x) { return __builtin_popcount(x)&1; }
int main(int argc,char**argv) {
 if(argc!=2){std::cerr<<"n must be 2 or 3\n";return 2;}
 int n=std::atoi(argv[1]);if(n!=2&&n!=3)return 2;
 int N=1<<(2*n), mask=(1<<n)-1;
 std::vector<int> q(N), B(N*N);
 for(int u=0;u<N;++u){q[u]=parity((u&mask)&(u>>n));
  for(int v=0;v<N;++v)B[u*N+v]=parity(((u&mask)&(v>>n))^((u>>n)&(v&mask)));}
 std::array<uint64_t,1024> counts{};
 std::array<std::array<int,4>,1024> witness{};
 uint64_t total=0;
 for(int a=1;a<N;++a)for(int b=1;b<N;++b){if(b==a)continue;
  for(int c=1;c<N;++c){if(c==a||c==b||c==(a^b))continue;
   const std::array<int,8> span={0,a,b,a^b,c,a^c,b^c,a^b^c};
   for(int d=1;d<N;++d){bool dep=false;for(int v:span)if(v==d){dep=true;break;}if(dep)continue;
    int bm=B[a*N+b]|(B[a*N+c]<<1)|(B[a*N+d]<<2)|(B[b*N+c]<<3)|(B[b*N+d]<<4)|(B[c*N+d]<<5);
    int qm=q[a]|(q[b]<<1)|(q[c]<<2)|(q[d]<<3);
    int k=bm*16+qm;if(!counts[k])witness[k]={a,b,c,d};++counts[k];++total;
   }
  }
 }
 std::cout<<"{\"schema\":\"ordered-physical-embedding-census-v1\",\"n\":"<<n<<",\"total\":"<<total<<",\"cases\":[";
 for(int k=0;k<1024;++k){if(k)std::cout<<",";std::cout<<"{\"B\":"<<(k/16)<<",\"q\":"<<(k%16)<<",\"count\":"<<counts[k]<<",\"basis\":[";
  for(int j=0;j<4;++j){if(j)std::cout<<",";std::cout<<witness[k][j];}std::cout<<"]}";}
 std::cout<<"]}\n";
}
