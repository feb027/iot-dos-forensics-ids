Title: UCI Machine Learning Repository

URL Source: http://archive.ics.uci.edu/dataset/942/rt-iot2022

Markdown Content:
![Image 1](https://archive.ics.uci.edu/static/public/default/Large.jpg?996)

## RT-IoT2022

## Donated on 1/4/2024

The RT-IoT2022, a proprietary dataset derived from a real-time IoT infrastructure, is introduced as a comprehensive resource integrating a diverse range of IoT devices and sophisticated network attack methodologies. This dataset encompasses both normal and adversarial network behaviours, providing a general representation of real-world scenarios. Incorporating data from IoT devices such as ThingSpeak-LED, Wipro-Bulb, and MQTT-Temp, as well as simulated attack scenarios involving Brute-Force SSH attacks, DDoS attacks using Hping and Slowloris, and Nmap patterns, RT-IoT2022 offers a detailed perspective on the complex nature of network traffic. The bidirectional attributes of network traffic are meticulously captured using the Zeek network monitoring tool and the Flowmeter plugin. Researchers can leverage the RT-IoT2022 dataset to advance the capabilities of Intrusion Detection Systems (IDS), fostering the development of robust and adaptive security solutions for real-time IoT networks.

## Dataset Characteristics

Tabular, Sequential, Multivariate

## Subject Area

Engineering

## Associated Tasks

Classification, Regression, Clustering

## Feature Type

Real, Categorical

## # Instances

123117

## # Features

83

## Dataset Information

Has Missing Values?

No

## Introductory Paper

## Variables Table

| Variable Name | Role | Type | Description | Units | Missing Values |
| --- | --- | --- | --- | --- | --- |
| id.orig_p | Feature | Integer |  |  | no |
| id.resp_p | Feature | Integer |  |  | no |
| proto | Feature | Categorical |  |  | no |
| service | Feature | Continuous |  |  | no |
| flow_duration | Feature | Continuous |  |  | no |
| fwd_pkts_tot | Feature | Integer |  |  | no |
| bwd_pkts_tot | Feature | Integer |  |  | no |
| fwd_data_pkts_tot | Feature | Integer |  |  | no |
| bwd_data_pkts_tot | Feature | Integer |  |  | no |
| fwd_pkts_per_sec | Feature | Continuous |  |  | no |

Rows per page

0 to 10 of 85

## Additional Variable Information

Column Details: id.orig_p id.resp_p proto service flow_duration fwd_pkts_tot bwd_pkts_tot fwd_data_pkts_tot bwd_data_pkts_tot fwd_pkts_per_sec bwd_pkts_per_sec flow_pkts_per_sec down_up_ratio fwd_header_size_tot fwd_header_size_min fwd_header_size_max bwd_header_size_tot bwd_header_size_min bwd_header_size_max flow_FIN_flag_count flow_SYN_flag_count flow_RST_flag_count fwd_PSH_flag_count bwd_PSH_flag_count flow_ACK_flag_count fwd_URG_flag_count bwd_URG_flag_count flow_CWR_flag_count flow_ECE_flag_count fwd_pkts_payload.min fwd_pkts_payload.max fwd_pkts_payload.tot fwd_pkts_payload.avg fwd_pkts_payload.std bwd_pkts_payload.min bwd_pkts_payload.max bwd_pkts_payload.tot bwd_pkts_payload.avg bwd_pkts_payload.std flow_pkts_payload.min flow_pkts_payload.max flow_pkts_payload.tot flow_pkts_payload.avg flow_pkts_payload.std fwd_iat.min fwd_iat.max fwd_iat.tot fwd_iat.avg fwd_iat.std bwd_iat.min bwd_iat.max bwd_iat.tot bwd_iat.avg bwd_iat.std flow_iat.min flow_iat.max flow_iat.tot flow_iat.avg flow_iat.std payload_bytes_per_second fwd_subflow_pkts bwd_subflow_pkts fwd_subflow_bytes bwd_subflow_bytes fwd_bulk_bytes bwd_bulk_bytes fwd_bulk_packets bwd_bulk_packets fwd_bulk_rate bwd_bulk_rate active.min active.max active.tot active.avg active.std idle.min idle.max idle.tot idle.avg idle.std fwd_init_window_size bwd_init_window_size fwd_last_window_size Attack_type

Class Labels

The Dataset contains both Attack patterns and Normal Patterns. Attacks patterns Details: 1. DOS_SYN_Hping------------------------94659 2. ARP_poisioning--------------------------7750 3. NMAP_UDP_SCAN--------------------2590 4. NMAP_XMAS_TREE_SCAN--------2010 5. NMAP_OS_DETECTION-------------2000 6. NMAP_TCP_scan-----------------------1002 7. DDOS_Slowloris------------------------534 8. Metasploit_Brute_Force_SSH---------37 9. NMAP_FIN_SCAN---------------------28 Normal Patterns Details: 1. MQTT -----------------------------------8108 2. Thing_speak-----------------------------4146 3. Wipro_bulb_Dataset-------------------253 4. Amazon-Alexa -----------------------86842

## Dataset Files

| File | Size |
| --- | --- |
| RT_IOT2022 | 52.2 MB |

[Download(3.3 MB)](https://archive.ics.uci.edu/static/public/942/rt-iot2022.zip)

Install the ucimlrepo package

pip install ucimlrepo

Import the dataset into your code

from ucimlrepo import fetch_ucirepo 
  
# fetch dataset 
rt_iot2022 = fetch_ucirepo(id=942) 
  
# data (as pandas dataframes) 
X = rt_iot2022.data.features 
y = rt_iot2022.data.targets 
  
# metadata 
print(rt_iot2022.metadata) 
  
# variable information 
print(rt_iot2022.variables) 

[View the full documentation](https://github.com/uci-ml-repo/ucimlrepo)

1 citations

50226 views

Citation

S., B. & Nagapadma, R. (2023). RT-IoT2022  [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5P338.

Style:

## Keywords

## Creators

B. S.

sharmilabs@nie.ac.in

The National Institute of Engineering, Mysuru

Rohini Nagapadma

rohini_nagapadma@nie.ac.in

The National Institute of Engineering, Mysuru

## DOI

## License

This dataset is licensed under a [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) (CC BY 4.0) license.

This allows for the sharing and adaptation of the datasets for any purpose, provided that the appropriate credit is given.

By using the UCI Machine Learning Repository, you acknowledge and accept the cookies and privacy practices used by the UCI Machine Learning Repository.
