# diversostockapp
A shares brokering web application


Kindly follow me as I walk you through how I carried out this project. Trust me, it was frustrating for most of it but nothing beats the feeling of having everything
come together and work perfectly. The Architecture of this project can be seen in the image below.


Let me explain the architecture briefly. I built a simple web application for buying and selling of shares using Django framework with python. This web application
isn't built using the django rest framework however, the page was simply rendered to simple html and css template. The stock prices are live prices called from an API 
endpoint (finnhub), the exchange rate is also live called from another API endpoint, the latest news is also called from an API endpoint to display live news related
 to the stocks up for sale on the site.
The database is sqlite3 which is embedded within the
django framework. The application was containerised and deployed on an AWS EC2 instance (Ubuntu) and made publicly accessible to my friends to create accounts and have
 fun just buying and selling stocks from Apple, Tesla and UBER. As they had fun with the website, I was busy checking the moitoring logs and charts to observe the
 behaviour of EC2 instance whilst also constantly debugging issues that came up once in a while during the live running of the web application to ensure that all issues
 were dealt with immediately to ensure that there was minimal downtime.


Here's a step by step guide on how I containerised and deployed the web application.

STEP 1. Building the Dockerfile

![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/92bc3f47-94c7-4f45-92b2-c3e347211f19)

STEP 2. Building the docker-compose.yml file

![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/19a73b5d-5854-481f-9c50-cde903e3a9fb)

STEP 3. Next was to build the docker image and spin up the container in my local machine
- First in my powershell terminal, I cd into the directory of my web application, then I ran the docker-compose up command to build the image, spin up the container and run the appliaction.

![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/03401cb4-af19-40e2-a317-55301ed8ea71)

STEP 4. Pushing the docker image to docker hub
- I used the following commands
1. docker tag <docker image> <DockerHubUsername>/container name:latest

2. docker login

3. docker push <DockerHubUsername>/container name:latest
  
![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/1c583625-5f64-4b99-b173-ac2288e34b18)

STEP 5. Next was to login to my AWS account and create an instance.
  I created a VPC for this project, i experimented with the vpc by creating 3 privates subnest and 3 public subnest with NAT assigned to only one private subnet.
  I configured the security group of the instance to allow ssh, http traffic inbound whilst also allowing traffic inbound on port 8000 as that is the port mapped to 
  the EC2 instance by the container. Check the configurations in the figures below.
  
  ![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/9e4446e9-5cfd-4a7c-a0fe-57907a69b091)

  ![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/922974b5-9b12-4754-be58-fea5ae501a34)

  Below is an image of the EC2 instance (stockDiversoApp) already running
  ![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/5d968f04-1f77-4c4e-bc46-db897e1b5a53)

STEP 6. Initialise git repository in the web application directory of my local machine, commit code to staging area, create repository on github, and push code to github.
  
  ![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/c1937ebe-c087-4921-ae4e-fc0abe59ebaa)

STEP 7. SSH into Ubuntu EC2 instance from my local machine, clone git repository, install and update packages, install docker, and docker-compose.
  - command used: ssh -i path-to-private-keypair ubuntu@EC2-public-IP-address.
  - sudo apt update
  - sudo apt install apt-transport-https ca-certificates curl software-properties-common
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  - echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  - sudo apt update
  - sudo apt install docker-ce docker-ce-cli containerd.io
  - docker --version
  
STEP 8. Spin up docker container on the EC2 instance.
  
  ![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/dcc0a9bb-9569-4eb7-8bbe-6a7d25828236)

STEP 9. Access the web application from my local machine browser by inputing the address below.
  - http://EC2-instance-IP-address:8000/home/

 Below is an image of the web application fully running on my EC2 instance.
  
  ![image](https://github.com/ikezycloud/diversostockapp/assets/108793471/8da62d96-a57d-4890-9a28-043040d49378)

STEP 10. Monitoring and troubeshooting!!
  
 I had my friends all create accounts on my web application and make transactions by buying and selling stocks while I monitored the logs of the EC2 instance.
  The results of those logs and my troubleshooting on the issues that came out whilst the application was running live will be provided soon!!
  
  
  THANK YOU!!!
  
