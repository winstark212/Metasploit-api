FROM kali-metasploit
ADD ./ /home/metasploit
WORKDIR /home/metasploit
RUN pip install --upgrade requests
RUN pip install -r requirements.txt
CMD ["python", "metasploit_observer.py"]

