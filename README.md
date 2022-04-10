# What is Athena?
Athena is a project built for HackRU Spring 2022. It algorithmically searches for the most important sentences in a YouTube video, and summarizes the video using these sentences.

# How Does It Work?
Athena's Algorithm Works as Following:

1. Athena turns the mp3 of a YouTube video into a string transcript using Google Cloud's API
2. It then parses through the transcript and calculates the frequency of each word - counting similar words (play, plays, player, playing, etc.) as the same word.
3. It then goes through these words and multiplies the frequency of each word by its correlation (from 0 to 1) to the main topic of the video, assigning this value as the 'score' of each word.
4. Then, Athena calculates which sentences contain the highest scoring words, and outputs the top n for the user to read

# What is Athena For?

Athena seeks to help students who are on a time-crunch during important study periods. Students are often given small 5 point assignments in classes that are to summarize or make some opinion of a video. Instead of taking 30-45 minutes watching these videos, students can simply use Athena to gain a basic understanding of the video.

# What Was Used to Build It?

1. Google Cloud API - Offloaded the speech detection and storage to Google Cloud to increase efficiency
2. NTLK - Used to calculate the correlation between various words in our algorithm. Also used to scrape the transcript for garbage words (the, then, before) and mark them as negligible
3. Python3

# Future Additions Coming Soon

1. Updated Framework using HTML
2. Optimization of the scoring algorithm to decrease waiting time
3. Chrome Extension to work directly in your browser
