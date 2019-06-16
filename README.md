
------- Application Web Infra --------

How to deploy Infra Web 

git clone git@github.com:QLSCloud/InfraWeb.git

---------------------------

- For all the package 

	- VM Web x 2
	- App Web
	- VM Dns x2
	- Dns service

python3 infraweb.py -a --all


- For only Web Infra

        - VM Web x 2
        - App Web

python3 infraweb.py -vw --vmweb

- For only Web App

	- App Web

python3 infraweb.py -w --web

--------------------------

- For only DNS Infra

        - VM Dns x 2
        - Dns service

python3 infraweb.py -vd --vmdns

- For only Dns Service

        - Dns service

python3 infraweb.py -d --dns

