# gTTS (Google Text-to-Speech)

### installation
```
sudo pip install gTTS --break-system-packages
```
and to play the audio from stdout or mp3 files:  
```
sudo apt install sox libsox-fmt-mp3
```

### write to file
```
gtts-cli -o test_gtts-cli.mp3 "This is a test of GTTS CLI"
```

### play from stdout with SoX
```
gtts-cli 'hello' | play -t mp3 -   
```
with no cmdline output:
```
gtts-cli 'hello' | play -t mp3 - > /dev/null 2>&1
```

### Use stdin
```
echo -n 'hello' | gtts-cli - --output from_stdin.mp3
echo -n 'hello' | gtts-cli --file - --output from_stdin.mp3  
```

### Useful Options

```
--all       Print available IETF language tags  
--version   Show version  
--lang      Language: Default English 'en', Hebrew 'iw'  
--slow      Read slower  
--nocheck   allow regional sub-tags such as 'en-gb' for 'en' (also speeds execution)  
--file      read text from a file  
```
