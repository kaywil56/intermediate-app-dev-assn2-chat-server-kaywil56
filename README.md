# Chat Server
--------------------
## Setup
Clone the repository and run the following command to install the required packages:
``` pip
$ pip install -r requirements.txt
```
## Running the server
navigate to the `Server` directory and run the following command:
``` pip
python chatserver.py
```
**OR**
``` pip
python3 chatserver.py
```
You should see the following: <br>
<br>
![image](https://user-images.githubusercontent.com/71423497/174513068-5e16210a-e1c7-4438-980c-7d68efc33a4a.png)
<br>
## Running the client
navigate to the `Client` directory and run the following command:
``` pip
python message_client.py
```
**OR**
``` pip
python3 message_client.py
```
You should get the following prompt: <br>
 <br>
![image](https://user-images.githubusercontent.com/71423497/174513328-7642988f-3be9-4720-91ac-5e7b41d44358.png)
 <br>
 ## Running tests
 Navigate to the root directory and run the following command:
 ``` pip
 python -m unittest tests/test_request_handler.py
 ```
 **OR**
  ``` pip
 python3 -m unittest tests/test_request_handler.py
 ```
 ![image](https://user-images.githubusercontent.com/71423497/174513837-94714d37-0eae-453f-bfc7-be3073d89b24.png)
