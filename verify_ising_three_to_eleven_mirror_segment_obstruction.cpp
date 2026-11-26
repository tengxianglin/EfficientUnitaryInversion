#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
static constexpr int N=42,H=21;
static const int q[H]={-10,8,-6,6,-4,2,-2,2,0,2,0,0,0,0,0,0,2,-2,0,0,1};
static constexpr long long DEN=47LL*41*N;
long long internal_w[43],constant_term=0;
struct Stats{long long count=0,nonpositive=0,min_num=0,max_num=0,min_count=0,max_count=0;vector<int>min_example,max_example;};
Stats stats[12];vector<int>current;
long long gcdll(long long a,long long b){return std::gcd(a<0?-a:a,b<0?-b:b);}
string fraction(long long num,long long den=DEN){long long g=gcdll(num,den);return to_string(num/g)+"/"+to_string(den/g);}
long long fast_weighted_sum(const vector<int>&lengths){
 long long w=0;vector<pair<int,int>>centers;int start=0;
 for(int L:lengths){w+=internal_w[L];if(L&1){int pos=start+(L-1)/2,sign=(((L-1)/2)&1)?-1:1;for(auto[p,s]:centers){int sep=abs(pos-p),d=min(sep,N-sep),mult=(d==H)?2:1;w+=1LL*q[d-1]*mult*sign*s;}centers.push_back({pos,sign});}start+=L;}return w;
}
void enumerate(int remaining,int parts,int start,long long weightedS,vector<pair<int,int>>&centers){
 if(parts==1){int L=remaining;long long w=weightedS+internal_w[L];if(L&1){int pos=start+(L-1)/2,sign=(((L-1)/2)&1)?-1:1;for(auto[p,s]:centers){int sep=abs(pos-p),d=min(sep,N-sep),mult=(d==H)?2:1;w+=1LL*q[d-1]*mult*sign*s;}}
  current.push_back(L);long long num=constant_term-41*w;Stats&st=stats[current.size()];++st.count;if(num<=0)++st.nonpositive;
  if(st.count==1||num<st.min_num){st.min_num=num;st.min_count=1;st.min_example=current;}else if(num==st.min_num)++st.min_count;
  if(st.count==1||num>st.max_num){st.max_num=num;st.max_count=1;st.max_example=current;}else if(num==st.max_num)++st.max_count;current.pop_back();return;}
 for(int L=1;L<=remaining-(parts-1);++L){long long w=weightedS+internal_w[L];if(L&1){int pos=start+(L-1)/2,sign=(((L-1)/2)&1)?-1:1;for(auto[p,s]:centers){int sep=abs(pos-p),d=min(sep,N-sep),mult=(d==H)?2:1;w+=1LL*q[d-1]*mult*sign*s;}centers.push_back({pos,sign});}
  current.push_back(L);enumerate(remaining-L,parts-1,start+L,w,centers);current.pop_back();if(L&1)centers.pop_back();}
}
pair<int,vector<int>>direct_signed_permutation(const vector<int>&lengths){
 vector<int>p(N),s(N,1);int start=0;for(int L:lengths){for(int r=0;r<L;++r){p[start+r]=start+L-1-r;s[start+r]=(r&1)?-1:1;}start+=L;}
 long long inv=0;for(int i=0;i<N;++i)for(int j=i+1;j<N;++j)if(p[i]>p[j])++inv;int det=(inv&1)?-1:1;for(int x:s)det*=x;
 vector<int>sums(H,0);for(int d=1;d<=H;++d){int total=0;for(int i=0;i<N;++i){int j=(i+d)%N;int rii=(p[i]==i)?s[i]:0,rjj=(p[j]==j)?s[j]:0,rij=(p[i]==j)?s[i]:0,rji=(p[j]==i)?s[j]:0;total+=rii*rjj-rij*rji;}sums[d-1]=total;}return{det,sums};
}
long long direct_weighted_sum(const vector<int>&lengths){auto[det,sums]=direct_signed_permutation(lengths);if(det!=1)throw runtime_error("signed mirror determinant is not +1");long long w=0;for(int d=0;d<H;++d)w+=1LL*q[d]*sums[d];return w;}
vector<int>random_composition(mt19937_64&rng,int parts){vector<int>cuts(N-1);iota(cuts.begin(),cuts.end(),1);shuffle(cuts.begin(),cuts.end(),rng);cuts.resize(parts-1);sort(cuts.begin(),cuts.end());vector<int>lengths;int prev=0;for(int x:cuts){lengths.push_back(x-prev);prev=x;}lengths.push_back(N-prev);return lengths;}
string array_json(const vector<int>&xs){ostringstream o;o<<"[";for(size_t i=0;i<xs.size();++i){if(i)o<<",";o<<xs[i];}o<<"]";return o.str();}
int main(int argc,char**argv){
 string output="";if(argc==3&&string(argv[1])=="--output")output=argv[2];else if(argc!=1){cerr<<"usage: verifier [--output PATH]\n";return 2;}
 for(int d=1;d<=H;++d)constant_term+=1LL*q[d-1]*N*((d&1)?1:-1);
 for(int L=1;L<=N;++L){int sign=(L&1)?-1:1;long long w=0;for(int r=0;r<L/2;++r){int sep=L-1-2*r,d=min(sep,N-sep),mult=(d==H)?2:1;w+=1LL*q[d-1]*mult*sign;}internal_w[L]=w;}
 mt19937_64 rng(202611260834ULL);int crosschecks=0;for(int i=0;i<1000;++i){int k=1+int(rng()%11);auto lengths=random_composition(rng,k);if(fast_weighted_sum(lengths)!=direct_weighted_sum(lengths))throw runtime_error("fast/direct moment formula mismatch");++crosschecks;}
 for(int k=3;k<=11;++k){vector<pair<int,int>>centers;current.clear();enumerate(N,k,0,0,centers);}
 long long total=0,nonpositive=0,global_min=0,global_min_count=0;
 for(int k=3;k<=11;++k){auto&st=stats[k];total+=st.count;nonpositive+=st.nonpositive;if(k==3||st.min_num<global_min){global_min=st.min_num;global_min_count=st.min_count;}else if(st.min_num==global_min)global_min_count+=st.min_count;}
 if(total!=1594831694LL||nonpositive!=0||fraction(global_min)!="2/40467")throw runtime_error("global census mismatch");
 long long two_segment_num=constant_term-41*fast_weighted_sum(vector<int>{1,41});if(fraction(two_segment_num)!="-80/40467")throw runtime_error("two-segment scope counterexample changed");
 ostringstream out;out<<"{\n  \"status\": \"exact_rational_three_to_eleven_mirror_segment_obstruction\",\n  \"site_count\": 42,\n  \"segment_counts\": [3,4,5,6,7,8,9,10,11],\n  \"total_compositions\": "<<total<<",\n  \"dual_numerator\": [";for(int i=0;i<H;++i){if(i)out<<",";out<<q[i];}out<<"],\n  \"dual_denominator\": 47,\n  \"dual_l1_norm\": \"1\",\n  \"common_slack_denominator\": "<<DEN<<",\n  \"overall_minimum_slack\": \""<<fraction(global_min)<<"\",\n  \"overall_minimum_slack_attainers\": "<<global_min_count<<",\n  \"program_mass_tv_lower_bound\": \"1/40467\",\n  \"per_segment_count\": [\n";
 for(int k=3;k<=11;++k){auto&st=stats[k];out<<"    {\"segment_count\": "<<k<<", \"composition_count\": "<<st.count<<", \"minimum_slack\": \""<<fraction(st.min_num)<<"\", \"minimum_slack_attainers\": "<<st.min_count<<", \"minimum_example\": "<<array_json(st.min_example)<<", \"maximum_slack\": \""<<fraction(st.max_num)<<"\", \"maximum_slack_attainers\": "<<st.max_count<<", \"maximum_example\": "<<array_json(st.max_example)<<", \"nonpositive_count\": "<<st.nonpositive<<"}"<<(k<11?",":"")<<"\n";}
 out<<"  ],\n  \"two_segment_scope_counterexample\": {\"composition\": [1,41], \"same_dual_slack\": \""<<fraction(two_segment_num)<<"\"},\n  \"independent_direct_matrix_crosschecks\": "<<crosschecks<<",\n  \"crosscheck_rng_seed\": 202611260834,\n  \"arithmetic\": \"integer exact during exhaustive scan; exact rational output; no floating point\",\n  \"scope\": \"all ordered compositions of 42 into k=3,...,11 positive contiguous perfect-mirror blocks; convex mixtures, dihedral images, and vertex-sign gauges. This is not a theorem for arbitrary couplings or k>=12.\"\n}\n";
 if(output.empty())cout<<out.str();else{ofstream f(output);if(!f)throw runtime_error("cannot open output");f<<out.str();}
}