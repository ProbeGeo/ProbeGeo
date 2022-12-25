# ProbeGeo: A Comprehensive Landmark Mining Framework Based on Web Content and Online Retrieval
IP geolocation is essential for various location-aware Internet applications. High-quality IP geolocation landmarks play a decisive role in the accuracy of IP geolocation. However, the previous research works focusing on mining landmarks from the Internet are hampered by poor landmark types, limited quantity, insufficient accuracy, and restricted coverage. In this paper, we propose a new type of landmark called probe landmarks to utilize public VPs (Vantage Points) with geographical locations and active probe functions. We also expand traditional common landmarks by taking advantage of the exposure of multiple IoT (Internet-of-Things) devices on the Internet to improve the quantity and quality of landmarks. In particular, we present a new framework called ProbeGeo to detect high-quality landmarks automatically. On the one hand, ProbeGeo searches device websites online to discover common landmarks, increasing the quantity and coverage of landmarks. On the other hand, ProbeGeo constructs probe landmarks by extracting the geographical locations of VPs from existing VPs websites, improving the accuracy and stability of landmarks. We develop a prototype of ProbeGeo and conduct real-world experiments to validate its efficacy. Our results show that ProbeGeo can detect 89,849 high-quality landmarks, including 6,874 probe landmarks and 82,975 common landmarks. ProbeGeo landmarks are about 10x more than existing work, distributed in 181 countries and 7,094 cities. ProbeGeo landmarks cover more than 8 types of devices, and more than 58% of them remain stable over one month. Moreover, the accuracy of more than 40% of ProbeGeo landmarks is above street level, which has not been achieved in previous works. ProbeGeo can provide a geolocation service with high accuracy and broad coverage by correlating a large scale of landmarks. 

## Introduction
To make it easier for readers to reproduce our research, we make the source code, test data, and landmark datasets of ProbeGeo publically available. Please cite our paper if you use the ProbeGeo landmark dataset, thank you! 

Our project mainly consists of three parts: data, exp_code and modular_code. The directory tree and specific functions of the project are shown below. 

```
ProbeGeo
├── data    # include the landmark dataset obtained by ProbeGeo
│   └── landmark_dataset.csv    # 89,849 in total (type, IP, lat, lon)
├── exp_code    # the code and data needed to complete the experiment
│   ├── cdf     
│   │   ├── cdf.py  # the script to calculate the CDF curve
│   │   └── exp_result  # geolocation accuracy evaluation data, the source of CDF
│   └── cdf.py  # CDF function
├── modular_code    #　the ProbeGeo module code
│   ├── CLM-Common-Landmark-Miner   # common landmark miner, including process code, data and others
│   │   ├── multi-layer-miner   # search multi-layers of websites to discover more landmarks
│   │   ├── plot
│   │   │   ├── cdf # calculate the cdf curve of mined landmarks
│   │   │   ├── distribution    # analyse the distribution of common landmarks in geographic and network space
│   │   │   └── map # reflect the distribution on a world map, visualization
│   │   ├── retrieval-and-classify  # CLM main process
│   │   ├── validate    # check the common landmarks reliable or not
│   │   └── webseeds    # the input of CLM
│   ├── DLG-Device-Landmark-Generator   # generate landmarks from websites, finding geo-info and IPs
│   └── PLM-Probe-Landmark-Miner    # probe landmark miner, including process code, data and others
│       ├── classification  # classify public VPs websites into geo-contained or not
│       ├── crawling    # 
│       ├── evaluation  # 
│       └── webseeds    # the input of PLM
└── README.md
```

## Data
The data directory contains all the ProbeGeo landmark data that we mined. The data is stored in csv format and has four attributes. In order: landmark type, IP, latitude,and longitude. 

We are continuously performing updates and stability verification of ProbeGeo landmarks. We will update this document weekly, and if any researchers need it, please download it. Feel free to contact us if you need more granular data (probegeo2022@gmail.com). 

## Modular_code
The Modular_code contains the ProbeGeo module code. The subdirectories are common-crawler and probe-crawler, which are used to mine common landmarks and probe landmarks respectively. 

### Code and environment
The entire project is based on the python 3.8 implementation. The server system is Ubuntu 20.04. The server is configured with 2 16-core CPUs and 64GB memory. To run the entire project, you need to execute the following commands to install the dependency package. 
```
pip install sklearn
pip install json
pip install selenium
pip install urllib
```
The '.py' files in the project can all be run using the 'python3 xxx.py' command. Please see README under the path for the function of each directory. Note that running the source code requires large hard disk storage (around 300GB). 

## exp_code
The exp_code directory contains the data we used to complete the experiment, including the source code and the original data of CDF for geolocation accuracy. 

### Datasets and CDF
The exp_result directory contains all calculation results of geolocation accuracy. The file name of each '.txt' file consists of geolocation algorithms and landmark datasets. The calculation of CDFs can be done by command 'python3 cdf.py'. 

## Misc
### Ethical and Privacy Concerns
All code and data we publish has been desensitized and does not involve user privacy. Please cite our paper when using. 

### Future work
We are actively deploying the distributed ProbeGeo landmark mining system and are constantly updating our datasets and services. If you would like to join us, please send us emails. 