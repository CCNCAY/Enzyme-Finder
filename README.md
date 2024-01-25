# Enzyme-Finder

This is a program I wrote to find cryptic restriction endonuclease enzyme sites in coding DNA sequences. 

The problem in a nutshell. 

DNA codes for amino acids. DNA is made of 4 chemical components abbreviated as A, T, G or C. Therefore a specific DNA can be described as a string of these letters, such as AAGGAATGCATTAGA. 
A functional piece of DNA that is responsible for making a specific protein is referred to as coding DNA or coding sequence (CDS). In a CDS, three consecutive letter of DNA (called codon) codes for one amino acid. 
There are 20 amino acids and a termination signal for 64 possible DNA codons. There are no "empty" codons, meaning that the 21 possible targets are encoded with by multiple codons. 
All amino acids are ancoded by 1 to 6 codons. SUch as the amino acid "Metionine" is encoded by only one codon (ATG), while "Threonine" is coded by ACA, ACG, ACC and ACT. 
It means that if a CDS has a bit that is an ACA, which is coding for Threonine, the last letter letter can be exchanged for any other letter and it is still a threonine.

Restriction endonucleases are enzymes that can cut DNA at a specific site. For example the enzyme called EcoRI cuts at GAATTC and nothing else. Cutting DNA at specific sites is an important tool in biotechnology.
In the old times, we could only cut DNA at naturally occuring restriction sites. For example we could cut a DNA using EcoRI if it had a naturally occuring GAATTC. Nowadays we can synthesize DNA and can introduce restriction sites at will. 

The problem emerges if I want a restriction site, any of it, in my DNA of interest, but I also want a specific amino acid coding sequence. I cannot simply add an EcoRI site because it will bring its own coded amino acids (in this case glutamic acid and phenilalanine) into the DNA. 
But I can try to take an existing coding sequence and try to change it in a way that it is coding for the same amino acids. For example two consecutive Threonines can be coded as follows:
ACA ACA
ACA ACG
ACA ACC
ACA ACT
ACG ACA
ACG ACG
etc. 
It is impossible to hand edit all of them and manually check all of them against an enzyme list of dozens of possible enzymes. 

I call a DNA sequence a "cryptic restriction site" if it can be edited into an actual site without changing the meaning of the DNA. For example the DNA "GGC AGC" codes for Glycine and Serine. It is a cryptic BamHI site, becasue it can be changed to "GGT ACC", still a Glycine and Serine, but now also a BamHI site. 
The main part of the code is to find all cryptic sites in a CDS. 

I wrote this code because I needed a tool to find as many cryptic enzyme sites along a CDS as possible. I could not find any such program online. Later I added other functions that are available online, such as DNA translation option, just for fun. 

I wrote this program for myself and originally did not intend to share. It has a lot of beginner solutions such as hard coded stuff that perhaps should not be, untested inputs etc. I also wrote this as first thing once I coule code a bit in python. Probably better code could be found. 

Anyways, now I share it and plan to upgrade it with better knowledge. 
