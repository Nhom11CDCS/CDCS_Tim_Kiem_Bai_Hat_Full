# **Lời này bài gì?**(Finding songs through lyrics) :musical_note: 

## Description :memo:
A web application can be used to find songs by typing in the lyrics.

In this project, we used Flask for the front-end and Elastic for the database. Moreover, we had tried to take the advantage of the Quartznet module to build a simple AI. This artifical intelligence can convert speeches to texts from input files. In addition, we trained this AI to be the most suitable for Vietnamese.


## Installation :gear:
**1. Install the Quartznet**: :robot: 
+ Update & install linux libs:
```bash
apt-get update && apt-get install -y libsndfile1 ffmpeg
```
+ Install [recommend python>=3.8](https://www.python.org/downloads/release/python-385/)
* Python libs:
```bash
pip install -r requirements.txt
```
+ Install [torch 1.8.1](https://pytorch.org/get-started/previous-versions/#v181):
```bash
# cpu only, you can install CUDA version if you have NVidia GPU
pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```
+ Install [kemlm](https://github.com/kpu/kenlm) for LM decoding (only support Linux) 
```bash
pip install https://github.com/kpu/kenlm/archive/master.zip
```

**2. Install elasticSearch & kibana** :chart_with_downwards_trend:  
  2.1 ElasticSearch 
You can see the installation [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)
Or following these commands: 
+ Get the elastic key: 
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```
+ Install transport https: 
```
sudo apt-get install apt-transport-http
```
+ Install from the APT repository: 
``` 
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
``` 
+ Install elasticSearch: 
```
sudo apt-get update && sudo apt-get install elasticsearch
```
+ Let the elastich start up with your computer: 
```
sudo /bin/systemctl daemon-reload

sudo /bin/systemctl enable elasticsearch.service

sudo systemctl start elasticsearch.service
```  
2.2 Kibana  
You can see the installation [here](https://www.elastic.co/guide/en/kibana/8.13/deb.html#deb-repo)
Or follow these commands:
+ Get the Kibana key: 
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```

+ Install from the APT repository: 
```
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
```
+ Install Kibana
``` 
sudo apt-get update && sudo apt-get install kibana
```
+ Let the kibana start up with your computer: 
``` 
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
sudo systemctl start kibana.service 
```
**3. Install Flask**   
Use this command: 
```
sudo pip install Flask
```
or 
```
sudo pip3 install Flask 
``` 
