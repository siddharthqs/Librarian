# Librarian
 
 ***
 
 This code is a relatively simple program that implements an intellegent chat bot named "Librarian"
 The program can "read" documents (.pdf,.txt) or code (.py,.hpp,.cpp) and accurately answer questions on the contents.

 The program requires an API Key to OpenAI. Place your key at the top of both read.py and chat.py files. Alternatively, add your key to your environment variables.
 
 The code is written in Python, and requires quite a few dependencies, run the following command to install all required modules.

 pip install -r requirements.txt
 
 ***
 
 To execute the program, first run the read.py program with the follwing arguments:
 
 python read.py <file_type> <directory>

 <file_type> can be code or docs
 <directory> is the directory containing the files of interest
 
 ***
 
 To run the chat bot, run the command:
 
 python chat.py

 The Librarian will greet you and you will be able to make queries. 
