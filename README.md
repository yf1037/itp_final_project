# itp_final_project
This python program can design gRNA for different CRISPR/Cas systems.  

Input:  
  (required) a fasta file or a nucleic acid sequence  
  (optional) type of Cas. Default is Cas9, can switch to Cas12a (Cpf1) or Cas13a (C2c2)  
  (optional) length of gRNA. Default is 20, which works for all three CRISPR/Cas  
  (optional) application. Can design gRNAs for both imaging and editing, considering off-target rate within the given sequence  

Output:  
Default output will generate a csv file contain PAM seqence and gRNA seqence. Can also print PAM and gRNA sequence.  
  
