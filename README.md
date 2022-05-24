# Requirements

- requirements.txt

# Example
#### After `git pull` and install requirements

<br/>
<br/>

### view help

```commandline
python canttack.py 

or

python canttack.py [-h | --help]
```

### view command help
```commandline
python canttack.py dataset [-h | --help]

python canttack.py inject [-h | --help]
```

### check version
```commandline
python canttack.py [-V | --version]
```

### Create Normal Dataset (.txt to .csv)

```commandline
python canttack.py dataset [-T | --target] TARGET \
    [-n | --name] NAME (--can | --can-fd)
    
python canttack.py dataset -T normal_data -n dataset --can
```
- TARGET(essential) : Raw data file name (_e.g._, normal_data.txt)
- NAME(essential) : Export data file name (_e.g._, dataset.csv)

### Inject Attack

```commandline
python canttack.py inject [-T | --target] TARGET \
    [-c | --count] COUNT (--ddos | --fuzzing)

python canttack.py inject -T dataset -c 10 --ddos
python canttack.py inject -T dataset -c 10 --fuzzing
```
- TARGET(essential) : Dataset file name (_e.g._, dataset.csv)
- COUNT(optional) : Number of attacks to inject
    - default : 10