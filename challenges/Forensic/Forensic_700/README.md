# My boyfriend's secret

Cheol-Soo and his girlfriend Young-Hee use Cheol-Soo's computer together. Cheol-Soo was used to use computer without setting passwords on his account, but from some day he set the password on his account, encrypting all his private files, and made a new privileged account for his girlfriend. Young-Hee thought that his boyfriend is hiding something from her, so she decided to break into the Cheol-Soo's account. One day, Cheol-Soo locked his account and left from computer for couple of minutes. Young-Hee logged into system using her account, and dumped whole system memory to the USB thumb drive. After comming back to her house, she started to analyze the memory dump to find the Cheol-Soo's password and remotely log into system with his account.

In this problem, you will play the Young-Hee's role. Let's analyze the memory dump, and connect to the system using Cheol-Soo's account, and find out his secret!

+ To solve this problem, you need to connect to the VPN. This VPN only can be connected from UNIST intranet.
+ Do not attack other systems on VPN, and do not modify answer file after solving problem. These actions will be treated as cheating, which will result in disqualification.
+ The form of answer is password:contents_of_secret_file. For example, if the login password for Cheol-Soo's account was qwerasdf1234 and contents of secret file was ZXCVZXCV, then the key is qwerasdf1234:ZXCVZXCV

VPN server: gamauzi.hexa.pro / no encryption

Account 1: HeXACTF1/ctfplayer  
Account 2: HeXACTF2/ctfplayer  
Account 3: HeXACTF3/ctfplayer  
Account 4: HeXACTF4/ctfplayer  

Hint 1: Google is your friend.  
Hint 2: Google knows everything.  
Hint 3: Cheol-Soo is using Windows PC.  
Hint 4: You won't need any paid tools. It can help you(maybe?) but open-source tools like volatility with some plugins would be enough.  
(You can write your own code to analyze this memory dump, of course.)  
Hint 5: With live system, we can collect clear-text password from wDigest using Mimikatz, but we're not online, right? Find out how we can perform Mimikatz with offline system memory image.  

If you have problem with VPN connection(living outside of school, etc), please contact me at CTF openchat.

- ksh7534

