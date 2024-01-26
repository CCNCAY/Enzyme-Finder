import csv
import tkinter as tk
import os
import sys
from tkinter import ttk
from tkinter import messagebox

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

enzyme_list = []  # create a new empty list
enzyme_names = []
enzyme_lists = []



for file in os.listdir("lists"):
    if file.endswith(".elt"):
        enzyme_lists.append(file)
enzyme_lists.sort()



# here to decide which enzyme list to use, maybe a dropdown menu?
# available_enzymes = []
# longest expected fragment for the circularize function???
def enzymelist_reload(filename):
    enzyme_list.clear()
    enzyme_names.clear()
    with open("lists\\{}".format(filename), 'r') as f:
        next(
            f)  # skip heading row in text file (I cannot get csv.Dictreader instead to work as an alternative to this step)
        data = csv.reader(f, delimiter='\t')  # read text file with csv
        for row in data:
            enzyme_list.append(row)  # add the data from the text file to the list
    for enzyme in enzyme_list:
        enzyme_names.append(enzyme[0])
    initWindow.destroy()



initWindow = tk.Tk()
initWindow.geometry("200x100")
initWindow.resizable(False, False)
ttk.Label(initWindow, text="Init window", padding=(30, 10)).pack()

listchoicelabel = tk.Label(initWindow, text='Choose enzyme list:')
listchoicelabel.pack(ipadx=30)
currentlist = tk.StringVar()
currentlist.set(enzyme_lists[0])
enzyme_options_ = tk.OptionMenu(initWindow, currentlist, *enzyme_lists, command=enzymelist_reload)
enzyme_options_.pack(ipadx=30)

initWindow.mainloop()


if enzyme_list == []:
    sys.exit()

#print(enzyme_lists)







#enzymelist_reload(enzyme_lists[0])
#enzyme_dict = {enzyme_list[i][0]: enzyme_list[i][1] for i in range(0, len(enzyme_list))}




def enzymereturn (name):
    enzyme_dict = {enzyme_list[i][0]: enzyme_list[i][1] for i in range(0, len(enzyme_list))}
    name = name.replace("\n", "")
    print (enzyme_dict)
    return enzyme_dict.get(name)
# input checkeing functions





def DNA_check(seq):
    DNA_letters = {"A", "T", "G", "C", "N", "W", "S", "K", "M", "B", "R", "Y", "H", "V", "D", }
    for base in seq[:-1]:
        if base not in DNA_letters:
            return False
    return True


def protein_check(seq):
    protein_letters = {}
    for aa in seq[:-1]:
        if aa not in protein_letters:
            return False
    return True

def inputconverter (seq):
    seq = seq.upper()
    seq = seq.replace("\n", "")
    seq = seq.replace(" ", "")
    return seq


def input_validator(seq, intype="DNA"):
    errortype = "none"
    if intype == "DNA":
        if DNA_check(seq) == False:
            errortype = "Expected only DNA letters (including ambiguous bases such as N or W). Found other letters. Check your input."
    elif intype == "protein":
        if DNA_check(seq) == False:
            errortype = "Expected only single letter aminoacid codes (20 non-ambigous letters and asterisk (*) for stop. Please check, and change any other stop letters to asterisk (*)"
    else:
        errortype = "Cannot decide if DNA or protein input expected."
    if errortype == "none":
        return True
    else:
        messagebox.showerror("Error", errortype)
        return False




# Translates triplets to aminoacids. Uses ambigous bases and ambigous aminoacids.#
def trans_trip(triplet):
    if triplet[0] == "A":
        if triplet[1] == "A":
            if triplet[2] == "Y" or triplet[2] == "C" or triplet[2] == "T":
                return "Asn"
            elif triplet[2] == "R" or triplet[2] == "A" or triplet[2] == "G":
                return "Lys"
            else:
                return "N/K"
        if triplet[1] == "C":
            return "Thr"
        if triplet[1] == "G":
            if triplet[2] == "Y" or triplet[2] == "C" or triplet[2] == "T":
                return "Ser"
            elif triplet[2] == "R" or triplet[2] == "A" or triplet[2] == "G":
                return "Arg"
            else:
                return "S/R"
        if triplet[1] == "T":
            if triplet[2] == "G":
                return "Met"
            elif triplet[2] == "H" or triplet[2] == "A" or triplet[2] == "T" or triplet[2] == "C" or triplet[
                2] == "W" or triplet[2] == "Y" or triplet[2] == "M":
                return "Ile"
            else:
                return "M/I"
    if triplet[0] == "C":
        if triplet[1] == "A":
            if triplet[2] == "Y" or triplet[2] == "C" or triplet[2] == "T":
                return "His"
            elif triplet[2] == "R" or triplet[2] == "A" or triplet[2] == "G":
                return "Gln"
            else:
                return "H/Q"
        if triplet[1] == "C":
            return "Pro"
        if triplet[1] == "G":
            return "Arg"
        if triplet[1] == "T":
            return "Leu"
    if triplet[0] == "G":
        if triplet[1] == "A":
            if triplet[2] == "Y" or triplet[2] == "C" or triplet[2] == "T":
                return "Asp"
            elif triplet[2] == "R" or triplet[2] == "A" or triplet[2] == "G":
                return "Glu"
            else:
                return "D/E"
        if triplet[1] == "C":
            return "Ala"
        if triplet[1] == "G":
            return "Gly"
        if triplet[1] == "T":
            return "Val"
    if triplet[0] == "T":
        if triplet[1] == "A":
            if triplet[2] == "Y" or triplet[2] == "C" or triplet[2] == "T":
                return "Tyr"
            elif triplet[2] == "R" or triplet[2] == "A" or triplet[2] == "G":
                return " * "
            else:
                return "Y/*"
        if triplet[1] == "C":
            return "Ser"
        if triplet[1] == "G":
            if triplet[2] == "Y" or triplet[2] == "C" or triplet[2] == "T":
                return "Cys"
            elif triplet[2] == "G":
                return "Trp"
            elif triplet[2] == "A":
                return " * "
            else:
                return "C*W"
        if triplet[1] == "T":
            if triplet[2] == "Y" or triplet[2] == "C" or triplet[2] == "T":
                return "Phe"
            elif triplet[2] == "R" or triplet[2] == "A" or triplet[2] == "G":
                return "Leu"
            else:
                return "F/L"
        else:
            return "Unk"
    else:
        return "Unk"


# Fills a string with N's until it is divideable by 3. Then cuts this string to units of 3 characters. Useful to get
# DNA triplets.
def slice_tri(seq):
    trip_arr = []
    while len(seq) % 3 > 0:
        seq = seq + "N"
    while len(seq) > 0:
        trip_arr.append(seq[0:3])
        seq = seq[3:]
    return trip_arr


# Translates DNA to aminoacids. Translation might contain ambigous aminoacids.
def translate(seq):
    aa_arr = []
    seq_arr = slice_tri(seq)
    for x in range(len(seq_arr)):
        aa_arr.append(trans_trip(seq_arr[x]))
    return aa_arr



def aa_check(orig, new):
    if orig == new:
        return True
    elif new == "N/K":
        if orig == "Asn" or orig == "Lys":
            return True
    elif new == "S/R":
        if orig == "Ser" or orig == "Arg":
            return True
    elif new == "M/I":
        if orig == "Met" or orig == "Ile":
            return True
    elif new == "H/Q":
        if orig == "His" or orig == "Gln":
            return True
    elif new == "D/E":
        if orig == "Asp" or orig == "Glu":
            return True
    elif new == "Y/*":
        if orig == "Tyr" or orig == " * ":
            return True
    elif new == "C*W":
        if orig == "Cys" or orig == " * " or orig == "Trp":
            return True
    elif new == "F/L":
        if orig == "Phe" or orig == "Leu":
            return True
    return False



def merge(orig, query):
    # Merges two of same long sequences using strength rules for ambigous bases.#
    # Rules:
    # 1 if nth base of the two sequences are equal, it takes the nth base as nth base of output
    # 2 if nth query is N it takes nth original whatever it is
    # 3a if nth query is ambigous (such as W), and nth original is one of the proper bases (such as A), then takes the original.
    # 3b if nth query is ambigous (such as W), and nth original is NOT one of the proper bases (e.g. it's a C), then it takes the ambiguous nth query.
    # 3c if both nth bases are ambigouus in a different way (such as W and Y), then it takes the nth query, even if it is a less strict aambiguous (such as N instead of W)
    # 4 if nth query is non-ambiguos (such as T), then it takes the nth query regardless the original
    # All in all, it always tries to take a strict base of original if query allows it, or query if there is a conflict.
    if len(orig) != len(query):
        print("The two sequences must be of same length.")
        return
    merged = ""
    for x in range(len(orig)):
        if query[x] == "N":
            merged = merged + orig[x]
        if query[x] == orig[x]:
            merged = merged + orig[x]
        elif query[x] == "A" or query[x] == "C" or query[x] == "G" or query[x] == "T":
            merged = merged + query[x]
        elif query[x] == "W":
            if orig[x] == "A" or orig[x] == "T":
                merged = merged + orig[x]
            else:
                merged = merged + "W"
        elif query[x] == "R":
            if orig[x] == "A" or orig[x] == "G":
                merged = merged + orig[x]
            else:
                merged = merged + "R"
        elif query[x] == "M":
            if orig[x] == "A" or orig[x] == "C":
                merged = merged + orig[x]
            else:
                merged = merged + "M"
        elif query[x] == "K":
            if orig[x] == "G" or orig[x] == "T":
                merged = merged + orig[x]
            else:
                merged = merged + "K"
        elif query[x] == "Y":
            if orig[x] == "C" or orig[x] == "T":
                merged = merged + orig[x]
            else:
                merged = merged + "Y"
        elif query[x] == "S":
            if orig[x] == "G" or orig[x] == "C":
                merged = merged + orig[x]
            else:
                merged = merged + "S"
    return merged

#fix this one!
def phrase_find(phrase, orig):
    #finds a phrase on an original sequence.
    #creates a version of the phrase for the first 3 frames
    #Then translates the frame, and checks if the translation fits the original AA-sequence.
    frame1 = phrase
    frame2 = "N" + phrase
    frame3 = "NN" + phrase
    # each frames is made to dividible by 3.
    while len(frame1) % 3 > 0:
        frame1 = frame1 + "N"
    while len(frame2) % 3 > 0:
        frame2 = frame2 + "N"
    while len(frame3) % 3 > 0:
        frame3 = frame3 + "N"
    #frame 3 is surely the longest and also it is dividible by 3. Here I fill up the other 2 frames with N's so they are equally lengthy and still div by 3.
    while len(frame3) > len(frame1):
        frame1 = frame1 + "N"
    while len(frame3) > len(frame2):
        frame2 = frame2 + "N"
    #I determine how long subfragment of the original sequence i need to take
    frag_size = len(frame1)
    pos = []
    cycle = 0
    while len(orig) >= len(frame1):
        #as long as i have enough length in the original, the cycles go on (in the later def I add Ns to the original)
        # print (cycle)
        in_fr1 = True
        in_fr2 = True
        in_fr3 = True
        frag = orig[0:frag_size]  #this is the fragment I am working with for the rest of the cycle
        orig = orig[3:] #preparation for the next cycle
        transl = translate(frag)
        #merge function uses 2 same lenght seqs and creates ambigous output using relaxed DNA letters
        #merge function tends to modify the seequence towards the 2nd input which is our frame.
        f_merged1 = merge(frag, frame1)
        f_merged2 = merge(frag, frame2)
        f_merged3 = merge(frag, frame3)
        tr1 = translate(f_merged1)
        tr2 = translate(f_merged2)
        tr3 = translate(f_merged3)
        for x in range(len(transl)):
            if aa_check(transl[x], tr1[x]) == False:
                in_fr1 = False
            if aa_check(transl[x], tr2[x]) == False:
                in_fr2 = False
            if aa_check(transl[x], tr3[x]) == False:
                in_fr3 = False
        if in_fr1:
            pos.append(cycle * 3 + 1)
        if in_fr2:
            pos.append(cycle * 3 + 2)
        if in_fr3:
            pos.append(cycle * 3 + 3)
        cycle += 1
    return (pos)
    # Note: transl will be already filled to 3's with N's#



def enzyme_finder(e_list, seq):
    # finds ambiguous seq while keeping translation
    seq = seq + "NNN"
    found_e = []
    positions = []
    pair = []
    # print (len(e_list))
    for x in range(len(e_list)):
        # print(positions)
        positions.append(phrase_find(e_list[x][1], seq))
        found_e.append(e_list[x][0] + " (" + e_list[x][1] + ")")

    for x in range(len(found_e)):
        if len(positions[x]) > 0:
            pair.append(str(found_e[x]) + " found at positions: " + str(positions[x]) + "\n")
    return pair




def show_enzymes():
    output_text_field = tk.Text(text_frame, height=15)
    output_text_field.grid(row=2, column=0)
    out = ""
    for item in enzyme_list:
        out += item[0] + " (" + item[1] + ")"
        out += "\n"
    output_text_field.insert("1.0", out)




def revcomp(seq):
    revseq = seq[::-1]
    out = ""
    revdictionary = {"A":"T", "T":"A", "G":"C", "C":"G", "N":"N", "H":"D", "D":"H", "V":"B", "B":"V", "Y":"R", "R":"Y", "W":"S", "S":"W", "K":"M", "M":"K",}
    for i in range (0, len(revseq)):
        if revseq[i] in revdictionary:
            out+= revdictionary[revseq[i]]
    return out


def translateoneletter(seq):
    outseq = ""
    primer_translation = translate(seq)
    for aminoacid in primer_translation:
        if aminoacid == "Asn":
            outseq += "N"
        elif aminoacid == "Lys":
            outseq += "K"
        elif aminoacid == "Arg":
            outseq += "R"
        elif aminoacid == "Ala":
            outseq += "A"
        elif aminoacid == "Asp":
            outseq += "D"
        elif aminoacid == "Glu":
            outseq += "E"
        elif aminoacid == "Gln":
            outseq += "Q"
        elif aminoacid == "Gly":
            outseq += "G"
        elif aminoacid == "His":
            outseq += "H"
        elif aminoacid == "Ile":
            outseq += "I"
        elif aminoacid == "Leu":
            outseq += "L"
        elif aminoacid == "Met":
            outseq += "M"
        elif aminoacid == "Phe":
            outseq += "F"
        elif aminoacid == "Pro":
            outseq += "P"
        elif aminoacid == "Ser":
            outseq += "S"
        elif aminoacid == "Thr":
            outseq += "T"
        elif aminoacid == "Trp":
            outseq += "W"
        elif aminoacid == "Tyr":
            outseq += "Y"
        elif aminoacid == "Val":
            outseq += "V"
        elif aminoacid == "Cys":
            outseq += "C"
        elif aminoacid == "Cys":
            outseq += "C"
        elif aminoacid == " * ":
            outseq += "*"
        else:
            outseq += "X"
    return outseq


def translate_sixfr(seq):
    revseq = revcomp(seq)
    out = ""
    for i in range(1, 4):
        out += "Frame %s: \n" % i
        out += translateoneletter(seq)
        out += "\n\n"
        seq = seq[1:]
    for i in range(1, 4):
        out += "Rev. frame %s: \n" % i
        out += translateoneletter(revseq)
        out += "\n\n"
        revseq = revseq[1:]
    return out

#rewrite using dict
def seqmatch(query, target):
    basedictionary = {"A":["R", "M", "W", "H", "V", "D", "N"], "T":["K", "Y", "W", "H", "B", "D", "N"], "G":["R", "K", "S", "B", "V", "D", "N"], "C":["M", "Y", "S", "H", "B", "V", "N"]}
    if len(query) > len(target):
        return False
    for i in range(0, len(query)):
        if query[i] == target[i]:
            pass
        elif query[i] == "N":
            pass
        elif query[i] == "R" and (target[i] == "A" or target[i] == "G"):
            pass
        elif query[i] == "M" and (target[i] == "A" or target[i] == "C"):
            pass
        elif query[i] == "K" and (target[i] == "T" or target[i] == "G"):
            pass
        elif query[i] == "Y" and (target[i] == "C" or target[i] == "T"):
            pass
        elif query[i] == "S" and (target[i] == "C" or target[i] == "G"):
            pass
        elif query[i] == "W" and (target[i] == "A" or target[i] == "T"):
            pass
        elif query[i] == "H" and target[i] != "G":
            pass
        elif query[i] == "B" and target[i] != "A":
            pass
        elif query[i] == "V" and target[i] != "T":
            pass
        elif query[i] == "D" and target[i] != "C":
            pass
        else:
            return False
    return True



def circularize (seq, requiredlen = 100):
    if len(seq) < requiredlen+1:
        seq = seq+seq
    else:
        seq = seq + seq[0:requiredlen]
    return seq

def digest (enzyme, seq, circular = True):
    original_length = len(seq)
    enzymesite = enzymereturn(enzyme)
    #print (enzymesite)
    revsite = revcomp(enzymesite)
    do_twice = False
    sites_found = []
    frag_sizes = []
    if enzymesite != revsite:
        do_twice = True
    seq = inputconverter(seq)
    if circular:
        seq = circularize(seq)
    if input_validator(seq):
        for i in range (0, original_length):
            if seqmatch(enzymesite, seq):
                sites_found.append(i + 1)
            if do_twice:
                if seqmatch(revsite, seq):
                    sites_found.append(i + 1)
            seq = seq[1::]
        if not circular:
            sites_found.append(0)
            sites_found.append(original_length)
            sites_found.sort()
            for i in range(1, len(sites_found)):
                frag_sizes.append(sites_found[i]-sites_found[i-1])
            return [sites_found[1:-1], frag_sizes]
        else:
            sites_found.sort()
            if len(sites_found) == 0:
                frag_sizes.append(0)
            elif len(sites_found) == 1:
                frag_sizes.append(original_length)
            else:
                for i in range(1, len(sites_found)):
                    frag_sizes.append(sites_found[i] - sites_found[i - 1])
                frag_sizes.append(original_length-sites_found[-1]+sites_found[0])
            frag_sizes.sort()
            return [sites_found, frag_sizes]


#for the enzyme button:
def run2():
    output_text_field = tk.Text(text_frame, height=15)
    output_text_field.grid(row=2, column=0)
    out = ""
    input = seq_entry_field.get("1.0", "end")
    input = inputconverter(input)
    if input_validator(input):
        for item in enzyme_finder(enzyme_list, input):
            out += item
        output_text_field.insert("1.0", out)

#for the translate button:
def run_translate():
    input = seq_entry_field.get("1.0", "end")
    input = inputconverter(input)
    if input_validator(input):
        output_text_field = tk.Text(text_frame, height=15)
        output_text_field.grid(row=2, column=0)
        output_text_field.insert("1.0", translate_sixfr(input))

#for the reverse button:
def run_reverse():
    input = seq_entry_field.get("1.0", "end")
    input = inputconverter(input)
    if input_validator(input):
        output_text_field = tk.Text(text_frame, height=15)
        output_text_field.grid(row=2, column=0)
        output_text_field.insert("1.0", revcomp(input))

#For the digest buttton:
def run_digest(e):
    output_text_field = tk.Text(text_frame, height=15)
    output_text_field.grid(row=2, column=0)
    input = seq_entry_field.get("1.0", "end")
    input = inputconverter(input)
    if input_validator(input):
        output_text_field.insert("1.0", "The site of {0} was found at positions:".format(e))
        output_text_field.insert("2.0", "\n")
        digestresult = digest(e, input, not linvalue.get())
        #print(digestresult)
        if linvalue.get():
            if digestresult[0]==[]:
                output_text_field.insert("3.0", "Non-cutter!")
            else:
                output_text_field.insert("3.0", digestresult[0])
            output_text_field.insert("4.0", "\n")
            output_text_field.insert("5.0", "Expected fragment sizes are:")
            output_text_field.insert("6.0", "\n")
            output_text_field.insert("7.0", digestresult[1])
        else:
            if digestresult[0] == []:
                output_text_field.insert("3.0", "Non-cutter, expected several (supercoil/uncut plasmid) fragments.")
            else:
                output_text_field.insert("3.0", digestresult[0])
                output_text_field.insert("4.0", "\n")
                output_text_field.insert("5.0", "Expected fragment sizes are:")
                output_text_field.insert("6.0", "\n")
                output_text_field.insert("7.0", digestresult[1])


def resolution_check(listof_fragments):
    min_res = 1.2
    max_fragments = 6
    out = True
    listof_fragments.sort()
    if max_fragments < len(listof_fragments) < 1:
        out = False
    for i in range(0, len(listof_fragments) - 1):
        if listof_fragments[i + 1] / listof_fragments[i] < min_res:
            out = False
    return out


def compare_pattern(pattern_a, pattern_b):
    pattern_a.sort()
    pattern_b.sort()
    min_size = 300
    max_size = 7000
    needed_ratio = 1.2
    good_frags_a = []
    good_frags_b = []
    dif_pairs = 0
    for i in range(0, len(pattern_a)):
        if min_size <= pattern_a[i] <= max_size:
            good_frags_a.append(pattern_a[i])
    for j in range(0, len(pattern_b)):
        if min_size <= pattern_b[j] <= max_size:
            good_frags_b.append(pattern_b[j])
    if len(good_frags_a) == len(good_frags_b):
        if len(good_frags_a) ==0:
            return False
        else:
            for k in range(0, len(good_frags_a)):
                next_pair = [good_frags_a[k], good_frags_b[k]]
                next_pair.sort()
                if next_pair[0]*needed_ratio <= next_pair[1]:
                    dif_pairs +=1
        if dif_pairs == 0:
            return False
        else:
            return True
    else:
        return True



def compare_plasmids(seq1, seq2, enzyme):
    digest1 = digest(enzyme, seq1, True)
    digest2 = digest(enzyme, seq2, True)
    max_frag = 5
    if digest1[1] == [0]:
        return False
    if digest2[1] ==[0]:
        return False
    if len(digest1[1]) > max_frag:
        return False
    if len(digest2[1]) > max_frag:
        return False
    return compare_pattern(digest1[0], digest2[0])


#this one is to
def find_good_enzyme(seq_list):
    if len(seq_list) < 2:
        messagebox.showerror("Error", "You need 2 or 3 circular DNA sequences to compare. Please enter them in FASTA format. (For help, press the Help/Info button.)")
        return
    seq1 = seq_list[0]
    seq2 = seq_list[1]
    seq3 = ""
    if len(seq_list) > 2:
        seq3 = seq_list[2]
    candidate_list1 = []
    candidate_list2 = []
    candidate_list3 = []
    #narrow_list1 = []
    # checks!!!
    for e in enzyme_names:
        if compare_plasmids(seq1, seq2, e):
            candidate_list1.append(e)
        if seq3 != "":
            if compare_plasmids(seq2, seq3, e):
                candidate_list2.append(e)
            if compare_plasmids(seq1, seq3, e):
                candidate_list3.append(e)
    set1 = set(candidate_list1)
    set2 = set(candidate_list2)
    set3 = set(candidate_list3)
    if seq3 == "":
        if len(set1) > 0:
            outtext = ""
            for e in set1:
                outtext += str(e) + " " + enzymereturn(e)
                outtext += "\n SEQ1 fargs are: "
                outtext += str(digest(e, seq1)[1])
                outtext += "\n SEQ2 fargs are: "
                outtext += str(digest(e, seq2)[1])
                outtext += "\n"
            return outtext
    else:
        inter1 = set1.intersection(set2)
        if (len(inter1.intersection(set3)) > 0):
            outtext = ""
            for e in inter1.intersection(set3):
                outtext += str(e) + " " + enzymereturn(e)
                outtext += "\n SEQ1 fargs are: "
                outtext += str(digest(e, seq1)[1])
                outtext += "\n SEQ2 fargs are: "
                outtext += str(digest(e, seq2)[1])
                outtext += "\n SEQ3 fargs are: "
                outtext += str(digest(e, seq3)[1])
                outtext += "\n"
            return outtext
    return "No good enzyme found."


def serial_fasta_converter(fastaterms):
    input_list = fastaterms.split("\n")
    new_input_list = []
    for element in input_list:
        if element != "":
            new_input_list.append(element)
    seq_names = []
    seq_seqs = []
    for i in range(0, len(new_input_list)):
        if i % 2 == 0:
            seq_names.append(new_input_list[i])
        else:
            seq_seqs.append(new_input_list[i])
    return seq_seqs, seq_names


def fastarun():
    output_text_field = tk.Text(text_frame, height=15)
    output_text_field.grid(row=2, column=0)
    input = seq_entry_field.get("1.0", "end")
    out = serial_fasta_converter(input)
    output_text_field.insert("1.0", out)


def run_digestcompare():
    output_text_field = tk.Text(text_frame, height=15)
    output_text_field.grid(row=2, column=0)
    input = seq_entry_field.get("1.0", "end")
    inlist = serial_fasta_converter(input)[0]
    out = find_good_enzyme(inlist)
    output_text_field.insert("1.0", out)


mainWindow = tk.Tk()
mainWindow.geometry("800x600")  # might be too big
mainWindow.resizable(True, True)
ttk.Label(mainWindow, text="Enzyme Finder", padding=(30, 10)).pack()

# frames definition
text_frame = ttk.Frame(mainWindow)
text_frame.pack(side="left", fill="both", expand=True)
button_frame = ttk.Frame(mainWindow)
button_frame.pack(side="right", fill="both", expand=True)

# text definitions with scrollbars
entry_label = tk.Label(text_frame, text = "Input field: enter your sequence below.")
entry_label.grid(row=0, column=0)

seq_entry_field = tk.Text(text_frame,  height=15,)
seq_entry_field.grid(row=1, column=0)
input_seq = seq_entry_field.get("1.0", "end")

output_text_field = tk.Text(text_frame, height=15)
output_text_field.grid(row=2, column=0)
output_text_field.insert("1.0", "Here comes the output.")
# output_text_field["state"] = "disabled" #as oppose to "normal"


entry_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=seq_entry_field.yview)
entry_scroll.grid(row=1, column=1, sticky="ns")

output_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=output_text_field.yview)
output_scroll.grid(row=2, column=1, sticky="ns")
seq_entry_field["yscrollcommand"] = entry_scroll.set
output_text_field["yscrollcommand"] = output_scroll.set
# buttons definition


# run_button = ttk.Button(button_frame, text = "Run", command = run)
enz_button = ttk.Button(button_frame, text="Find enzymes", command=run2, )
enz_button.pack(ipadx=30)
trl_button = ttk.Button(button_frame, text="Translate", command=run_translate)
trl_button.pack(ipadx=30)
rev_button = ttk.Button(button_frame, text="Reverse seqeunce", command=run_reverse)
rev_button.pack(ipadx=30)
# digest_button = ttk.Button(button_frame, text="Digest with:", command=run_digest)
# digest_button.pack(ipadx = 30)
digestlabel = tk.Label(button_frame, text='Digest with:')
digestlabel.pack(ipadx=30)
enzvar = tk.StringVar()
enzvar.set("Choose enzyme")
enzyme_options = tk.OptionMenu(button_frame, enzvar, *enzyme_names, command=run_digest)
#enzyme_options.configure(*enzyme_names)
enzyme_options.pack(ipadx=30)



# enzyme_field = tk.Text(button_frame, height=1)
# enzyme_field.pack(ipadx = 30)
linvalue = tk.BooleanVar()
linvalue.set(False)
lin = ttk.Checkbutton(button_frame, text="Linear", variable=linvalue)
lin.pack()
show_e_button = ttk.Button(button_frame, text="Show enzymes", command=show_enzymes)
show_e_button.pack(ipadx=30)
fastabutton = ttk.Button(button_frame, text="DigestCompare", command=run_digestcompare)
fastabutton.pack(ipadx=30)
help_button = ttk.Button(button_frame, text="Help/Info",)
help_button.pack(ipadx=30)
quit_button = ttk.Button(button_frame, text="Quit", command=mainWindow.destroy)
quit_button.pack(ipadx=30)
mainWindow.mainloop()
# GGGGAATTCTATCCCATGCATAATATATATATAAAATTAAGGGTATCCCAATGCATAAATTTGGGAATTCTACCCA

# digest_circular("EcoRI", "GGGGAATTCTATCCCATGCATAATATATATATAAAATTAAGGGTATCCCAATGCATAAATTTGGGAATTCTACCCA")

# print(digest_circular("EcoRI", "GGGGAATTCTATCCCATGCATAATATATATATAAA"))

PKS = "ctaaattgtaagcgttaatattttgttaaaattcgcgttaaatttttgttaaatcagctcattttttaaccaataggccgaaatcggcaaaatcccttataaatcaaaagaatagaccgagatagggttgagtgttgttccagtttggaacaagagtccactattaaagaacgtggactccaacgtcaaagggcgaaaaaccgtctatcagggcgatggcccactacgtgaaccatcaccctaatcaagttttttggggtcgaggtgccgtaaagcactaaatcggaaccctaaagggagcccccgatttagagcttgacggggaaagccggcgaacgtggcgagaaaggaagggaagaaagcgaaaggagcgggcgctagggcgctggcaagtgtagcggtcacgctgcgcgtaaccaccacacccgccgcgcttaatgcgccgctacagggcgcgtcccattcgccattcaggctgcgcaactgttgggaagggcgatcggtgcgggcctcttcgctattacgccagctggcgaaagggggatgtgctgcaaggcgattaagttgggtaacgccagggttttcccagtcacgacgttgtaaaacgacggccagtgagcgcgcgtaatacgactcactatagggcgaattgggtaccgggccccccctcgaggtcgacggtatcgataagcttgatatcgaattcctgcagcccgggggatccactagttctagagcggccgccaccgcggtggagctccagcttttgttccctttagtgagggttaattgcgcgcttggcgtaatcatggtcatagctgtttcctgtgtgaaattgttatccgctcacaattccacacaacatacgagccggaagcataaagtgtaaagcctggggtgcctaatgagtgagctaactcacattaattgcgttgcgctcactgcccgctttccagtcgggaaacctgtcgtgccagctgcattaatgaatcggccaacgcgcggggagaggcggtttgcgtattgggcgctcttccgcttcctcgctcactgactcgctgcgctcggtcgttcggctgcggcgagcggtatcagctcactcaaaggcggtaatacggttatccacagaatcaggggataacgcaggaaagaacatgtgagcaaaaggccagcaaaaggccaggaaccgtaaaaaggccgcgttgctggcgtttttccataggctccgcccccctgacgagcatcacaaaaatcgacgctcaagtcagaggtggcgaaacccgacaggactataaagataccaggcgtttccccctggaagctccctcgtgcgctctcctgttccgaccctgccgcttaccggatacctgtccgcctttctcccttcgggaagcgtggcgctttctcatagctcacgctgtaggtatctcagttcggtgtaggtcgttcgctccaagctgggctgtgtgcacgaaccccccgttcagcccgaccgctgcgccttatccggtaactatcgtcttgagtccaacccggtaagacacgacttatcgccactggcagcagccactggtaacaggattagcagagcgaggtatgtaggcggtgctacagagttcttgaagtggtggcctaactacggctacactagaaggacagtatttggtatctgcgctctgctgaagccagttaccttcggaaaaagagttggtagctcttgatccggcaaacaaaccaccgctggtagcggtggtttttttgtttgcaagcagcagattacgcgcagaaaaaaaggatctcaagaagatcctttgatcttttctacggggtctgacgctcagtggaacgaaaactcacgttaagggattttggtcatgagattatcaaaaaggatcttcacctagatccttttaaattaaaaatgaagttttaaatcaatctaaagtatatatgagtaaacttggtctgacagttaccaatgcttaatcagtgaggcacctatctcagcgatctgtctatttcgttcatccatagttgcctgactccccgtcgtgtagataactacgatacgggagggcttaccatctggccccagtgctgcaatgataccgcgagacccacgctcaccggctccagatttatcagcaataaaccagccagccggaagggccgagcgcagaagtggtcctgcaactttatccgcctccatccagtctattaattgttgccgggaagctagagtaagtagttcgccagttaatagtttgcgcaacgttgttgccattgctacaggcatcgtggtgtcacgctcgtcgtttggtatggcttcattcagctccggttcccaacgatcaaggcgagttacatgatcccccatgttgtgcaaaaaagcggttagctccttcggtcctccgatcgttgtcagaagtaagttggccgcagtgttatcactcatggttatggcagcactgcataattctcttactgtcatgccatccgtaagatgcttttctgtgactggtgagtactcaaccaagtcattctgagaatagtgtatgcggcgaccgagttgctcttgcccggcgtcaatacgggataataccgcgccacatagcagaactttaaaagtgctcatcattggaaaacgttcttcggggcgaaaactctcaaggatcttaccgctgttgagatccagttcgatgtaacccactcgtgcacccaactgatcttcagcatcttttactttcaccagcgtttctgggtgagcaaaaacaggaaggcaaaatgccgcaaaaaagggaataagggcgacacggaaatgttgaatactcatactcttcctttttcaatattattgaagcatttatcagggttattgtctcatgagcggatacatatttgaatgtatttagaaaaataaacaaataggggttccgcgcacatttccccgaaaagtgccac"
PKS_HX = "ctcgagctaaattgtaagcgttaatattttgttaaaattcgcgttaaatttttgttaaatcagctcattttttaaccaataggccgaaatcggcaaaatcccttataaatcaaaagaatagaccgagatagggttgagtgttgttccagtttggaacaagagtccactattaaagaacgtggactccaacgtcaaagggcgaaaaaccgtctatcagggcgatggcccactacgtgaaccatcaccctaatcaagttttttggggtcgaggtgccgtaaagcactaaatcggaaccctaaagggagcccccgatttagagcttgacggggaaagccggcgaacgtggcgagaaaggaagggaagaaagcgaaaggagcgggcgctagggcgctggcaagtgtagcggtcacgctgcgcgtaaccaccacacccgccgcgcttaatgcgccgctacagggcgcgtcccattcgccattcaggctgcgcaactgttgggaagggcgatcggtgcgggcctcttcgctattacgccagctggcgaaagggggatgtgctgcaaggcgattaagttgggtaacgccagggttttcccagtcacgacgttgtaaaacgacggccagtgagcgcgcgtaatacgactcactatagggcgaattgggtaccgggccccccctcgaggtcgacggtatcgataagcttgatatcgaattcctgcagcccgggggatccactagttctagagcggccgccaccgcggtggagctccagcttttgttccctttagtgagggttaattgcgcgcttggcgtaatcatggtcatagctgtttcctgtgtgaaattgttatccgctcacaattccacacaacatacgagccggaagcataaagtgtaaagcctggggtgcctaatgagtgagctaactcacattaattgcgttgcgctcactgcccgctttccagtcgggaaacctgtcgtgccagctgcattaatgaatcggccaacgcgcggggagaggcggtttgcgtattgggcgctcttccgcttcctcgctcactgactcgctgcgctcggtcgttcggctgcggcgagcggtatcagctcactcaaaggcggtaatacggttatccacagaatcaggggataacgcaggaaagaacatgtgagcaaaaggccagcaaaaggccaggaaccgtaaaaaggccgcgttgctggcgtttttccataggctcaagcttcgcccccctgacgagcatcacaaaaatcgacgctcaagtcagaggtggcgaaacccgacaggactataaagataccaggcgtttccccctggaagctccctcgtgcgctctcctgttccgaccctgccgcttaccggatacctgtccgcctttctcccttcgggaagcgtggcgctttctcatagctcacgctgtaggtatctcagttcggtgtaggtcgttcgctccaagctgggctgtgtgcacgaaccccccgttcagcccgaccgctgcgccttatccggtaactatcgtcttgagtccaacccggtaagacacgacttatcgccactggcagcagccactggtaacaggattagcagagcgaggtatgtaggcggtgctacagagttcttgaagtggtggcctaactacggctacactagaaggacagtatttggtatctgcgctctgctgaagccagttaccttcggaaaaagagttggtagctcttgatccggcaaacaaaccaccgctggtagcggtggtttttttgtttgcaagcagcagattacgcgcagaaaaaaaggatctcaagaagatcctttgatcttttctacggggtctgacgctcagtggaacgaaaactcacgttaagggattttggtcatgagattatcaaaaaggatcttcacctagatccttttaaattaaaaatgaagttttaaatcaatctaaagtatatatgagtaaacttggtctgacagttaccaatgcttaatcagtgaggcacctatctcagcgatctgtctatttcgttcatccatagttgcctgactccccgtcgtgtagataactacgatacgggagggcttaccatctggccccagtgctgcaatgataccgcgagacccacgctcaccggctccagatttatcagcaataaaccagccagccggaagggccgagcgcagaagtggtcctgcaactttatccgcctccatccagtctattaattgttgccgggaagctagagtaagtagttcgccagttaatagtttgcgcaacgttgttgccattgctacaggcatcgtggtgtcacgctcgtcgtttggtatggcttcattcagctccggttcccaacgatcaaggcgagttacatgatcccccatgttgtgcaaaaaagcggttagctccttcggtcctccgatcgttgtcagaagtaagttggccgcagtgttatcactcatggttatggcagcactgcataattctcttactgtcatgccatccgtaagatgcttttctgtgactggtgagtactcaaccaagtcattctgagaatagtgtatgcggcgaccgagttgctcttgcccggcgtcaatacgggataataccgcgccacatagcagaactttaaaagtgctcatcattggaaaacgttcttcggggcgaaaactctcaaggatcttaccgctgttgagatccagttcgatgtaacccactcgtgcacccaactgatcttcagcatcttttactttcaccagcgtttctgggtgagcaaaaacaggaaggcaaaatgccgcaaaaaagggaataagggcgacacggaaatgttgaatactcatactcttcctttttcaatattattgaagcatttatcagggttattgtctcatgagcggatacatatttgaatgtatttagaaaaataaacaaataggggttccgcgcacatttccccgaaaagtgccac"
PKS_H = "aagcttctaaattgtaagcgttaatattttgttaaaattcgcgttaaatttttgttaaatcagctcattttttaaccaataggccgaaatcggcaaaatcccttataaatcaaaagaatagaccgagatagggttgagtgttgttccagtttggaacaagagtccactattaaagaacgtggactccaacgtcaaagggcgaaaaaccgtctatcagggcgatggcccactacgtgaaccatcaccctaatcaagttttttggggtcgaggtgccgtaaagcactaaatcggaaccctaaagggagcccccgatttagagcttgacggggaaagccggcgaacgtggcgagaaaggaagggaagaaagcgaaaggagcgggcgctagggcgctggcaagtgtagcggtcacgctgcgcgtaaccaccacacccgccgcgcttaatgcgccgctacagggcgcgtcccattcgccattcaggctgcgcaactgttgggaagggcgatcggtgcgggcctcttcgctattacgccagctggcgaaagggggatgtgctgcaaggcgattaagttgggtaacgccagggttttcccagtcacgacgttgtaaaacgacggccagtgagcgcgcgtaatacgactcactatagggcgaattgggtaccgggccccccctcgaggtcgacggtatcgataagcttgatatcgaattcctgcagcccgggggatccactagttctagagcggccgccaccgcggtggagctccagcttttgttccctttagtgagggttaattgcgcgcttggcgtaatcatggtcatagctgtttcctgtgtgaaattgttatccgctcacaattccacacaacatacgagccggaagcataaagtgtaaagcctggggtgcctaatgagtgagctaactcacattaattgcgttgcgctcactgcccgctttccagtcgggaaacctgtcgtgccagctgcattaatgaatcggccaacgcgcggggagaggcggtttgcgtattgggcgctcttccgcttcctcgctcactgactcgctgcgctcggtcgttcggctgcggcgagcggtatcagctcactcaaaggcggtaatacggttatccacagaatcaggggataacgcaggaaagaacatgtgagcaaaaggccagcaaaaggccaggaaccgtaaaaaggccgcgttgctggcgtttttccataggctccgcccccctgacgagcatcacaaaaatcgacgctcaagtcagaggtggcgaaacccgacaggactataaagataccaggcgtttccccctggaagctccctcgtgcgctctcctgttccgaccctgccgcttaccggatacctgtccgcctttctcccttcgggaagcgtggcgctttctcatagctcacgctgtaggtatctcagttcggtgtaggtcgttcgctccaagctgggctgtgtgcacgaaccccccgttcagcccgaccgctgcgccttatccggtaactatcgtcttgagtccaacccggtaagacacgacttatcgccactggcagcagccactggtaacaggattagcagagcgaggtatgtaggcggtgctacagagttcttgaagtggtggcctaactacggctacactagaaggacagtatttggtatctgcgctctgctgaagccagttaccttcggaaaaagagttggtagctcttgatccggcaaacaaaccaccgctggtagcggtggtttttttgtttgcaagcagcagattacgcgcagaaaaaaaggatctcaagaagatcctttgatcttttctacggggtctgacgctcagtggaacgaaaactcacgttaagggattttggtcatgagattatcaaaaaggatcttcacctagatccttttaaattaaaaatgaagttttaaatcaatctaaagtatatatgagtaaacttggtctgacagttaccaatgcttaatcagtgaggcacctatctcagcgatctgtctatttcgttcatccatagttgcctgactccccgtcgtgtagataactacgatacgggagggcttaccatctggccccagtgctgcaatgataccgcgagacccacgctcaccggctccagatttatcagcaataaaccagccagccggaagggccgagcgcagaagtggtcctgcaactttatccgcctccatccagtctattaattgttgccgggaagctagagtaagtagttcgccagttaatagtttgcgcaacgttgttgccattgctacaggcatcgtggtgtcacgctcgtcgtttggtatggcttcattcagctccggttcccaacgatcaaggcgagttacatgatcccccatgttgtgcaaaaaagcggttagctccttcggtcctccgatcgttgtcagaagtaagttggccgcagtgttatcactcatggttatggcagcactgcataattctcttactgtcatgccatccgtaagatgcttttctgtgactggtgagtactcaaccaagtcattctgagaatagtgtatgcggcgaccgagttgctcttgcccggcgtcaatacgggataataccgcgccacatagcagaactttaaaagtgctcatcattggaaaacgttcttcggggcgaaaactctcaaggatcttaccgctgttgagatccagttcgatgtaacccactcgtgcacccaactgatcttcagcatcttttactttcaccagcgtttctgggtgagcaaaaacaggaaggcaaaatgccgcaaaaaagggaataagggcgacacggaaatgttgaatactcatactcttcctttttcaatattattgaagcatttatcagggttattgtctcatgagcggatacatatttgaatgtatttagaaaaataaacaaataggggttccgcgcacatttccccgaaaagtgccacaattgtaagcgttaatattttgttaaaattcgcgttaaatttttgttaaatcagctcattttttaaccaataggccgaaatcggcaaaatcccttataaatcaaaagaatagaccgagatagggttgagtgttgttccagtttggaac"

# print (find_good_enzyme([PKS,PKS_HX, PKS_H]))

