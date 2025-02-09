import magic
import subprocess
import glob
import os
import img2pdf
from django.conf import settings
# Import the required libraries for using NLTK using the code below:
#import nltk
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize, sent_tokenize
# Import libraries for Google T5 code
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModelForSeq2SeqLM


FilePath_1 = "/var/www/html/devholos/assets/temp"
FilePath = settings.MEDIA_ROOT

def handle_uploaded_file(f,path):
    print("Full File Path"+FilePath_1+"/"+f.name)
    with open(FilePath_1  +"/"+ f.name, 'wb+') as destination:
        print("Hello")
        for chunk in f.chunks():
            destination.write(chunk)

def handle_uploaded_file_1(f):
    with open(FilePath_1 +"/"+ f.name, 'wb+') as destination:
        print("Hello")
        for chunk in f.chunks():
            destination.write(chunk)

def handle_uploaded_file_2(f,path):
    # print("Hello",FilFilePath_1ePath + path +"/"+ f.name)
    with open(FilePath_1+"/" + path +"/"+ f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def get_image_in_pdf(filename):
    curr_path = os.getcwd()
    os.chdir(FilePath_1)
    subprocess.run(['pdfimages','-png', FilePath_1 +"/" + filename, filename])
    for f in glob.glob(filename + "*.png"):
            os.remove(f)
    os.chdir(curr_path)

def merge_images_into_pdf(filename):
        filelist = glob.glob(filename + "*.png")
        with open("output.pdf", "wb") as f:
            imgs=[]
            for fname in sorted(filelist):
                if not fname.endswith(".png"):
                    continue
                if not fname.startswith(filename):
                    continue
                imgs.append(fname)
            f.write(img2pdf.convert(imgs))

#################
# Alternate way to merge_images_into_pdf
# from fpdf import FPDF
# pdf = FPDF()
# pdf.set_auto_page_break(0)
# imagelist = [i for i in os.listdir('.') if i.startswith('test7')
# for image in sorted(imagelist):
# pdf.add_page()
# pdf.image('./' + image, w=190, h=200)
# pdf.output('Transcript.pdf', “F”)
#################

def get_document_classification():
    print("Placeholder to get document classification")
# This is a placeholder

def get_document_summary_nltk(text):
    print("Placeholder to get document summary")
# General FLow
# get the text file that was created
# Organize it by lines and keep it aside for a minute. 
# Then I tokenize the words, eliminating stop words, stemmed words and such. 
# Then I figure out which words are repeated most in the text. Using the 
# highest number of repeats as the denominator calculate the weight of each word. 
# Another refinement would be to use a thesaurus to combine similar meaning words. 
# Now that each word has a weight, calculate the weight of each line. 
# Pick the top 10 lines with the most weight and that is the summary. 
# This is the extractive method (not the machine learning / understanding method). 
# I am sure if we think a bit more, we can tweak it to get better results, 
# but this could be a start. For example, if we knew the type of document 
# (document classification), then that could direct the summarization with 
# key words and phrases associated with that type of document. Similar case 
# with domain specific documents.

# Summarizing using NLTK
# The ‘Natural Language Toolkit’ is an NLP-based toolkit in Python that helps with text summarization.
# Here’s how to get it up and running.

# Input your text for summarizing below:
# text = """ """

# Next, you need to tokenize the text:
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

# Now, you will need to create a frequency table to keep a score of each word:
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
          continue
        if word in freqTable:
          freqTable[word] += 1
        else:
          freqTable[word] = 1

# Next, create a dictionary to keep the score of each sentence:
    #print("TEXT", text)
    sentences = sent_tokenize(text)
    #print("SENTENCES", sentences)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
          if word in sentence.lower():
# if word in sentence.lower():
            if sentence in sentenceValue:
              sentenceValue[sentence] += freq
            else:
              sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

# Now, we define the average value from the original text as such:
    average = int(sumValues / len(sentenceValue))
    print("average", average)

# And lastly, we need to store the sentences into our summary:
    nltk_summary = ''
    #print("before",nltk_summary)
    for sentence in sentences:
        #print("Sentence", sentence)
        print("sentence value", sentenceValue[sentence])
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            nltk_summary += " " + sentence + "\n"
            #print(nltk_summary)
    #print("after",nltk_summary)
    return nltk_summary


# Summarizing with Google T5
""" FutureWarning: This tokenizer was incorrectly instantiated with a model max length of 512 which will be corrected in Transformers v5.
For now, this behavior is kept to avoid breaking backwards compatibility when padding/encoding with `truncation is True`.
- Be aware that you SHOULD NOT rely on t5-base automatically truncating your input to 512 when padding/encoding.
- If you want to encode/pad to sequences longer than 512 you can either instantiate this tokenizer with `model_max_length` or pass `max_length` when encoding/padding.
- To avoid this warning, please instantiate this tokenizer with `model_max_length` set to your preferred value.
  warnings.warn( """
""" huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
        - Avoid using `tokenizers` before the fork if possible
        - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false) """
"""  FutureWarning: The class `AutoModelWithLMHead` is deprecated and will be removed in a future version. Please use `AutoModelForCausalLM` for causal language models, `AutoModelForMaskedLM` for masked language models and `AutoModelForSeq2SeqLM` for encoder-decoder models.
  warnings.warn( """

def get_document_summary_googleT5(text):
#To make use of Google’s T5 summarizer, there are a few prerequisites.
#First, you will need to install PyTorch and Hugging Face’s Transformers. You can install the transformers using the code below:
# pip install transformers
# Next, import PyTorch along with the AutoTokenizer and AutoModelWithLMHead objects:
# import torch
# from transformers, import AutoTokenizer, AutoModelWithLMHead
# Next, you need to initialize the tokenizer model:
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    #model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)
    model = AutoModelForSeq2SeqLM.from_pretrained('t5-base', return_dict=True)
    
# From here, you can use any data you like to summarize. Once you have gathered your data, input the code below to tokenize it:
    inputs = tokenizer.encode("summarize: " + text, return_tensors='pt',  max_length=512,  truncation=True)
# Now, you can generate the summary by using the model.generate function on T5:
    summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)
# Feel free to replace the values mentioned above with your desired values. Once it’s ready, you can move on to decode the tokenized summary using the tokenizer.decode function:
    gt5_summary = tokenizer.decode(summary_ids[0])
# And there you have it: a text summarizer with Google’s T5. You can replace the texts and values at any time to summarize various arrays of data.
    return gt5_summary

def get_search_results(text, search_string):
 if len(search_string) > 0:
   search_results = []
   temp_words = (search_string).split(":")
   temp_words_len = len(temp_words)
   if temp_words_len == 1:
       search_words = temp_words[0]
   elif temp_words_len == 2:
       search_words = temp_words[1]
   elif temp_words_len > 2:
       search_words = ''
   if len(search_words) > 0:
       wordlist = search_words.split(",")

   ftext = text.replace(","," ");
   ftext = ftext.replace("'"," ");
   ftext = ftext.replace("[","");
   ftext = ftext.replace("]","");
   ftext = ftext.replace("\"","");
   ftext = ftext.split("\\n")

   for line in ftext:
       #print("line in get search results",line)
       for wordi in wordlist:
          WORDI = wordi.upper()
          Wordi = wordi.title()
          if wordi in line or WORDI in line or Wordi in line:
               """ print("wordi", wordi)
               search_results.append("\n") """
               search_results.append(wordi+": ")
               search_results.append(line)
               search_results.append("\n")
   if len(search_results) == 0:
       search_results.append("Nothing found.\n")
       search_results.append("Either no search specified or search text not in file\n")
   #print("search_results in get", search_results)
   return(search_results)
           
   
