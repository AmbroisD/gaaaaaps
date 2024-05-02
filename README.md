# Gaaaaaps

# Docker Configuration

To properly configure Docker for the Gaaaaaps application, you need to follow the steps below:

## Modifying the docker-compose.yml File

Edit the `docker-compose.yml` file to specify the paths of the `SDS` and `SQS` directories where you want to store the scan results. Here's an example of modification:


volumes:
  - /Users/ambrois/Documents/01_Scripts/data/SQS:/SQS
  - /Users/ambrois/Documents/01_Scripts/data/SDS:/SDS
  
Make sure to replace /Users/ambrois/Documents/01_Scripts/data/SQS and /Users/ambrois/Documents/01_Scripts/data/SDS with the appropriate paths on your system.

Modifying the gaps_config.json File
Edit the gaps_config.json file to configure the available years and the whitelist of items. Here's an example of modification:

{
    "available_year": ["2021"],
    "white_list": ["HBAR"]
}

Make sure to update the available years and the whitelist according to your requirements.


> #### Get dAtA AvAilAbility for ProjectS 

#### Install

```bash
npm install #install dependance 
npm run dev # to create .js

# then  
python ./site_routage.py
```



### Annexe

#### How to install the latest nodejs version in ubuntu

You can install the last using the distribution from NodeSource repository:

```bash
curl --silent --location https://deb.nodesource.com/setup_9.x | sudo bash -
sudo apt-get install nodejs

sudo npm i -g npm
```

You can find all the sources here, https://github.com/nodesource/distributions/tree/master/deb

Then, you have the latest version of node.js installed.