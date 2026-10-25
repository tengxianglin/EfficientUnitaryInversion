// Independent F2 RREF subspaces x ordered GL(4,2) bases census.
// Physical vector: low n bits x, high n bits z. No r1 code is used.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using Basis=std::array<int,4>;
int parity(unsigned v){return __builtin_parity(v);}
int q0(int v,int n){return parity((v&((1<<n)-1))&(v>>n));}
int omega(int a,int b,int n){int m=(1<<n)-1;return parity(((a&m)&(b>>n))^((b&m)&(a>>n)));}
void pivot_sets(int m,int start,std::vector<int>&p,std::vector<Basis>&rrefs){
 if(p.size()!=4){for(int j=start;j<m;j++){p.push_back(j);pivot_sets(m,j+1,p,rrefs);p.pop_back();}return;}
 Basis rows{};std::vector<std::pair<int,int>> free;
 for(int r=0;r<4;r++){rows[r]=1<<p[r];for(int c=p[r]+1;c<m;c++){bool pivot=false;for(int z:p)pivot|=(z==c);if(!pivot)free.push_back({r,c});}}
 for(unsigned f=0;f<(1u<<free.size());f++){Basis a=rows;for(unsigned k=0;k<free.size();k++)if((f>>k)&1)a[free[k].first]|=1<<free[k].second;rrefs.push_back(a);}
}
int main(int argc,char**argv){
 if(argc!=3){std::cerr<<"usage: rref_census n output.json\n";return 2;}int n=std::stoi(argv[1]);if(n!=2&&n!=3)return 2;
 std::vector<Basis> spaces;std::vector<int> piv;pivot_sets(2*n,0,piv,spaces);
 std::vector<Basis> gl;
 for(int a=1;a<16;a++)for(int b=1;b<16;b++)if(b!=a)
 for(int c=1;c<16;c++)if(c!=a&&c!=b&&c!=(a^b))
 for(int d=1;d<16;d++){bool independent=true;for(int v:{a,b,c,a^b,a^c,b^c,a^b^c})independent&=(d!=v);if(independent)gl.push_back({a,b,c,d});}
 if(gl.size()!=20160){std::cerr<<"GL size failed\n";return 3;}
 std::array<uint64_t,1024> counts{};std::array<Basis,1024>witness{};uint64_t total=0;
 const std::array<std::pair<int,int>,6>pairs={{{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}}};
 for(const Basis&rows:spaces){
  int physical[16]={},q[16]={},bil[16][16]={};
  for(int a=1;a<16;a++){for(int k=0;k<4;k++)if((a>>k)&1)physical[a]^=rows[k];q[a]=q0(physical[a],n);}
  for(int a=1;a<16;a++)for(int b=1;b<16;b++)bil[a][b]=omega(physical[a],physical[b],n);
  for(const Basis&coeff:gl){int bmask=0,qmask=0;for(int k=0;k<6;k++)bmask|=bil[coeff[pairs[k].first]][coeff[pairs[k].second]]<<k;for(int k=0;k<4;k++)qmask|=q[coeff[k]]<<k;int type=bmask*16+qmask;if(!counts[type])for(int k=0;k<4;k++)witness[type][k]=physical[coeff[k]];counts[type]++;total++;}
 }
 std::ofstream o(argv[2]);o<<"{\"n\":"<<n<<",\"method\":\"RREF_subspaces_times_GL4\",\"subspace_count\":"<<spaces.size()<<",\"GL4_count\":"<<gl.size()<<",\"ordered_basis_count\":"<<total<<",\"rref_rows\":[";
 for(unsigned i=0;i<spaces.size();i++){if(i)o<<',';o<<'[';for(int j=0;j<4;j++){if(j)o<<',';o<<spaces[i][j];}o<<']';}o<<"],\"type_counts\":[";
 for(int t=0;t<1024;t++){if(t)o<<',';o<<counts[t];}o<<"],\"physical_witnesses\":[";
 for(int t=0;t<1024;t++){if(t)o<<',';if(!counts[t])o<<"null";else{o<<'[';for(int k=0;k<4;k++){if(k)o<<',';o<<witness[t][k];}o<<']';}}o<<"]}\n";
 std::cout<<"n="<<n<<" RREF="<<spaces.size()<<" GL4="<<gl.size()<<" ordered_bases="<<total<<"\n";
 return 0;
}
