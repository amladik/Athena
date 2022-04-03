import os
import nltk
#nltk.download()
from google.cloud import speech
from google.cloud import storage
import pygame
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile

from nltk.corpus import wordnet as wn
from itertools import product
from nltk.corpus import stopwords

stops = stopwords.words('english')

def getCorrelation(word1, word2):
    
    try:
        sem1, sem2 = wn.synsets(word1), wn.synsets(word2)

        maxscore = 0
        for i,j in list(product(*[sem1,sem2])):
            score = i.wup_similarity(j) # Wu-Palmer Similarity
            maxscore = score if maxscore < score else maxscore
        return(maxscore)

    except:
        return .5
    


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\kunal\\Downloads\\versatile-hull-346018-eb6c07c0d0a0.json"

speech_client = speech.SpeechClient()
def upload_blob(bucket_name, source_file_name):
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_file_name)

    blob.upload_from_filename(source_file_name)
def readFile(name):
    file_name = name
    upload_blob('speech_to_text_mediafiles',file_name)
    media_uri = 'gs://speech_to_text_mediafiles/'+file_name
    long_audio = speech.RecognitionAudio(uri=media_uri)
    config_enhanced = speech.RecognitionConfig(
        sample_rate_hertz = 48000,
        enable_automatic_punctuation = True,
        language_code = 'en-US',
        use_enhanced = True,
        model = 'video'
    )
    operation = speech_client.long_running_recognize(
        config=config_enhanced,
        audio=long_audio
    )
    response = operation.result(timeout=300)
    
    str2 = ''
    
    for result in response.results:
        #print(result.alternatives[0].transcript)
        
        str2+=result.alternatives[0].transcript
    print('String Finished')
    
    
    return(str2)
    
    
    
    
    
    
        
def explore():
   file = filedialog.askopenfile(mode='r', filetypes=[('Audio Files', '*.mp3 *.wav')])
   if file:
        linkNameText.delete("1.0","end-1c")
        filepath = os.path.abspath(file.name)
        fname = os.path.basename(file.name)
        linkNameText.insert("1.0",filepath)
        file.close()
def getWords():
    num_s = int(T2.get("1.0","end-1c"))
    if(num_s > 9):
        num_s = 9
    str2 = T.get("1.0", "end-1c")
    ln_input = linkNameText.get("1.0","end-1c")
    text = readFile(ln_input)
    rel = T2.get("1.0","end-1c")
    
    
    
    
    
    
    
    stops = stopwords.words('english')




#print(getCorrelation('play' , 'gaming'))

    wordMatch = rel

    sentences = text

    for words in stops:
        sentences.replace(words, '')

    print('Step 0')
    sentences = sentences.replace(',','')
    sentences = sentences.replace('--','')
    sentences = sentences.replace('-',' ')
    sentences = sentences.replace('"' , '')
    sentences = sentences.replace('(' , '')
    sentences = sentences.replace('{' , '')
    sentences = sentences.replace('[' , '')
    sentences = sentences.replace(']' , '')
    sentences = sentences.replace('}' , '')
    sentences = sentences.replace(')' , '')
    sentences = sentences.replace('!' ,'.')
    sentences = sentences.replace('?' ,'.')

    #sentences = sentences.lower()
    sentence= sentences.replace('. ' , '')
    print('Stage 1')
    #print(sentence)

    #print(sentence.split('. '))

    listofwords = sentence.split(' ')
    freq = {}

    dictionary = {}

    counter = 0
    print(listofwords[1])
    listofwords = list(dict.fromkeys(listofwords))

    print('Number of Words: ' + str(len(listofwords)))
    for i in range(len(listofwords)):
        if(i%10 == 0):
            print(i)
        for j in range( i+1 , len(listofwords)):
            #print(listofwords[i] + '   ' + listofwords[j] + '    ' + str(getCorrelation(listofwords[i],listofwords[j])))

            if(getCorrelation(listofwords[i],listofwords[j]) >= .75 and listofwords[j] != listofwords[i]):
                dictionary[listofwords[j]] = listofwords[i]

                #listofwords[j] = listofwords[i]

    #print(dictionary)

    freq = {}
    print('Stage 2')

    for words in sentence.split(' '):
        if(words in stops):
            freq[words] = 0
        elif(words in dictionary.keys()):
            if(dictionary[words] not in freq.keys()):
                freq[dictionary[words]] = 1

            else:
                freq[dictionary[words]] +=1

        else:
            if(words not in freq.keys()):
                freq[words] = 1

            else:
                freq[words] +=1


    #`  print(freq)
    print('Stage 3')

    sentences = sentences.replace('!','.')
    listofsentences = sentences.split('. ')

    #print(listofsentences)

    scores = {}
    counter = 0
    for sentences in listofsentences:
        score = 0
        for words in sentences.split(' '):
            if(words in dictionary.keys()):
                try:
                    score += freq[dictionary[words.replace('.','')]] *getCorrelation(dictionary[words.replace('.','')],wordMatch)**2
                except:
                    pass
            else:
                try:
                    score += freq[words.replace('.','')] * getCorrelation(words.replace('.',''),wordMatch)**2
                except:
                    pass

        scores[counter] = score
        counter+=1


    #print(scores)
    print('Stage 4')

    print(len(listofsentences))
    num = num_s
    stree=''
    while(num!=0):
        max_value = max(scores, key=scores.get)
        print(listofsentences[max_value] + '.')
        stree+=str(abs(num-num_s) + 1)
        stree+= '.  '
        stree+=listofsentences[max_value] + '.'
        stree+='\n\n'
        scores.pop(max_value, None)
        num-=1
        print('\n\n')
    print('Stage 5')

    
    
    
    
    
    
    
    
    text_file = open("C:\\Users\\kunal\\OneDrive\\Desktop\\output.txt", "wt")
    n = text_file.write(stree)
    text_file.close()
    #print(text)
def helpMe():
   messagebox.showinfo("","Enter a file path or link for top box;\n\nSeperate words by comma and no spaces in between")
root = tk.Tk()
 
# specify size of window.
root.geometry("700x600")
 
# Create text widget and specify size.
T = tk.Text(root, height = 5, width = 52)
 
# Create label
linkName = tk.Label(root, text = "Enter File Path/Link")
linkName.config(font =("Courier", 14))
linkNameText = tk.Text(root, height = 5, width = 52)
linkNameText.text = "hi"

l = tk.Label(root, text = "Enter Subject")
l.config(font =("Courier", 14))

l3 = tk.Label(root,text = "Enter # sentences you want returned(<10)")
l3.config(font = ("Courier",14))

T2 = tk.Text(root, height = 5, width = 52)



Fact = """"""
 
 
# Create button for next text.
exploreButton = tk.Button(root, text="Explore", command = explore)
b1 = tk.Button(root, text = "Done", command=getWords)
 
b3 = tk.Button(root, text = "Help",
            command = helpMe)
# Create an Exit button.
b2 = tk.Button(root, text = "Exit",
            command = root.destroy)

linkName.pack()
linkNameText.pack()
l.pack()
T.pack()
l3.pack()
T2.pack()
b1.pack()
b2.pack()
b3.pack()
exploreButton.pack()

# Insert The Fact.
T.insert(tk.END, Fact)
 
tk.mainloop()
