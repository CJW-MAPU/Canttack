# Requirements

- requirements.txt

# Example
#### After `git pull` and install requirements

# Update
### 2.* : Implement inject attack about can-fd data

<br/>
<br/>

# Canntack Cookbook
### view help

```commandline
python canttack.py 

or

python canttack.py [-h | --help]
```

<br/>

### view command help
```commandline
python canttack.py dataset [-h | --help]

python canttack.py inject [-h | --help]
```

<br/>

### check version
```commandline
python canttack.py [-V | --version]
```

<br/>

### Create Normal Dataset (.txt to .csv)

```commandline
python canttack.py dataset [-T | --target] TARGET \
    [-n | --name] NAME (--can | --can-fd)
    
```
- TARGET(required) : Raw data file name (_e.g._, normal_data_filename)
- NAME(required) : Export data file name (_e.g._, dataset_filename)

<br/>

### Create Normal Dataset Example
Suppose you own a file called can_normal_data.txt and you want to convert it to can_data.csv.
```commandline
python canttack.py dataset -T can_normal_data -n can_data --can
```
Suppose you own a file called fd_normal_data.txt and you want to convert it to fd_data.csv.
```commandline
python canttack.py dataset -T fd_normal_data -n fd_data --can-fd
```

<br/>

### Inject Attack

```commandline
python canttack.py inject [-T | --target] TARGET [-n | --name] NAME \
        [-c | --count] COUNT [-p | --packet] PACKET \
        (--can | --can-fd) (--dos | --fuzzing | --replay | --spoofing)
```
- TARGET(required) : Dataset file name (_e.g._, dataset_filename)
- NAME(required) : Attack injected dataset file name (_e.g._, attack_dataset_filename)
- COUNT(optional) : Number of attacks to inject
    - default : 10 (If attack type is replay, default is 1.)
- Packet(optional) : The attack packet you want to inject
    - default : DefaultPacket.json

<br/>

### Inject Attack Example
* If you want inject a DoS attack defined by default into a CAN dataset called can_data.csv to output.csv.
```commandline
python canttack.py inject -T can_data -n output --can --dos
```
* If you want inject a DoS attack defined in CustomPacket.json directly into the CAN dataset called can_data.csv to output.csv
```commandline
python canttack.py inject -T can_data -n output -p CustomPacket --can --dos 
```
* If you want to inject 20 DoS attacks defined in CustomPacket.json directly into the CAN dataset called can_data.csv to output.csv
```commandline
python canttack.py inject -T can_data -n output -c 20 -p CustomPacket --can --dos
```
* etc.
```commandline
python canttack.py inject -T fd_data -n output -c 14 -p CustomPacket --can-fd --replay

python canttack.py inject -T can_data -n output --can --fuzzing

python canttack.py inject -T can_data -n output -p CustomPacket --can --spoofing
```

<br/>

### JSON file format (DefaultPacket.json)
* In the case of a fuzzing attack, (id, dlc, and payload) are randomly generated, so they are not defined.
```json
{
  "can": {
    "dos": {
      "id": CAN_ID(string),
      "dlc": CAN_DLC(string),
      // Configuration with reference to DLC
      "payload": CAN_PAYLOAD(string, delimeter = whitespace)
    },
    "replay": {
      "path": CAN_PACKET_CHUNKS_FILE_PATH(string, format = *.csv)
    },
    "spoofing": {
      "id": "...",
      "dlc": "...",
      "payload": "..."
    }
  },
  "can-fd": {
     "dos": {
       "id": CAN_FD_ID(string),
       "dlc": CAN_FD_DLC(string),
       "flg": CAN_FD_FLG(string),
       "dir": CAN_FD_DIR(string),
       // Configuration with reference to DLC
       "payload": CAN_FD_PAYLOAD(string, delimeter = whitespace)
    },
    "replay": {
      "path": CAN_FD_PACKET_CHUNKS_FILE_PATH(string, format = *.csv)
    },
    "spoofing": {
      "id": "...",
      "dlc": "...",
      "flg": "...",
      "dir": "...",
      "payload": "..."
    }
  }
}
```