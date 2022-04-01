## Bölüm 1 - Amazon Linux 2 EC2 Bulut Sunucusunu Başlatın ve SSH ile Bağlanın

- SSH bağlantılarına izin veren güvenlik grubuna sahip Amazon Linux 2 AMI'yi kullanarak bir EC2 bulut sunucusu başlatın.

- SSH ile ec2 instance bağlanalım.

```bash
ssh -i .ssh/xxxxx.pem ec2-user@ec2-3-133-106-98.us-east-.compute.amazonaws.com
```


## Bölüm 2 - Amazon Linux 2 EC2 İnstance Docker yükleyelim

- Kurulu paketleri ve paket önbelleğini güncelleyelim

```bash
sudo yum update -y
```

- En yeni Docker Community Edition paketini yüklüyoruz.

```bash
sudo amazon-linux-extras install docker -y
```

- Docker service başlatalım.

- Init System: Init (başlatmanın kısaltması), bilgisayar sisteminin önyüklemesi sırasında başlatılan ilk işlemdir. Sistem kapatılana kadar çalışmaya devam eden bir arka plan programıdır. Ayrıca arka planda hizmetleri kontrol eder. Docker servisini başlatmak için init sistemine bilgi verilmelidir.

```bash
sudo systemctl start docker
```

- Docker servisi yeniden başlatıldıktan sonra otomatik olarak yeniden başlayabilmesi için docker servisini etkinleştiriyoruz.

```bash
sudo systemctl enable docker
```

- Docker servisinin çalışır durumda olup olmadığını kontrol edin.

```bash
sudo systemctl status docker
```

- Docker komutlarını "sudo" kullanmadan çalıştırmak için "docker" grubuna "ec2-user"ı ekleyelim.

```bash
sudo usermod -a -G docker ec2-user
```

- Normalde, "docker" grubunun etkili olması için kullanıcının bash kabuğunda yeniden oturum açması gerekir, ancak "newgrp" komutu, "ec2-user" için "docker" grubunu etkinleştirmek için kullanılabilir, bash kabuğunda yeniden oturum açmak için değildir.

```bash
newgrp docker
```

- `sudo`olmadan Docker version ile sürümü kontrol edebiliriz.

```bash
docker version

Client:
 Version:           19.03.6-ce
 API version:       1.40
 Go version:        go1.13.4
 Git commit:        369ce74
 Built:             Fri May 29 04:01:26 2020
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          19.03.6-ce
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.13.4
  Git commit:       369ce74
  Built:            Fri May 29 04:01:57 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.3.2
  GitCommit:        ff48f57fc83a8c44cf4ad5d672424a98ba37ded6
 runc:
  Version:          1.0.0-rc10
  GitCommit:        dc9208a3303feef5b3839f4323d9beb36df0a9dd
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

- `sudo`olmadan Docker info ile docker bilgilerini kontrol edelim.

```bash
docker info

Client:
 Debug Mode: false

Server:
 Containers: 1
  Running: 0
  Paused: 0
  Stopped: 1
 Images: 2
 Server Version: 19.03.6-ce
 Storage Driver: overlay2
  Backing Filesystem: xfs
  Supports d_type: true
  Native Overlay Diff: true
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: ff48f57fc83a8c44cf4ad5d672424a98ba37ded6
 runc version: dc9208a3303feef5b3839f4323d9beb36df0a9dd
 init version: fec3683
 Security Options:
  seccomp
   Profile: default
 Kernel Version: 4.14.181-140.257.amzn2.x86_64
 Operating System: Amazon Linux 2
 OSType: linux
 Architecture: x86_64
 CPUs: 1
 Total Memory: 983.3MiB
 Name: ip-172-31-30-143.us-east-2.compute.internal
 ID: AK6G:E2CQ:G45L:SEJY:FH6K:Q2CX:MQC6:6WJV:NYH2:6WOQ:BLWZ:3I7F
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Registry: https://index.docker.io/v1/
 Labels:
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false
```

## Bölüm 3 - İsterseniz Docker makinesi için bir Cloudformation Template Oluşturabiliriz.  

Her yerden SSH bağlantılarına izin veren güvenlik grubuyla Amazon Linux 2 EC2 Eşgörünümünde hazır bir Docker makinesine sahip olmak için bir Cloudformation Template yazıp ,  yapılandırabiliriz.

```yaml
AWSTemplateFormatVersion: 2010-09-09

Description: >
  This Cloudformation Template creates a Docker machine on EC2 Instance.
  Docker Machine will run on Amazon Linux 2 (ami-026dea5602e368e96) EC2 Instance with
  custom security group allowing SSH connections from anywhere on port 22.

Parameters:
  KeyPairName:
    Description: Enter the name of your Key Pair for SSH connections.
    Type: String
    Default: call.training

Resources:
  DockerMachineSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH for Docker Machine
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
  DockerMachine:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-09d95fab7fff3776c
      InstanceType: t3a.medium
      KeyName: !Ref KeyPairName
      SecurityGroupIds:
        - !GetAtt DockerMachineSecurityGroup.GroupId
      Tags:
        -
          Key: Name
          Value: !Sub Docker Machine of ${AWS::StackName}
      UserData:
        Fn::Base64: |
          #! /bin/bash
          yum update -y
          amazon-linux-extras install docker -y
          systemctl start docker
          systemctl enable docker
          usermod -a -G docker ec2-user
          # install docker-compose
          curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" \
          -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose
Outputs:
  WebsiteURL:
    Description: Docker Machine DNS Name
    Value: !Sub
      - ${PublicAddress}
      - PublicAddress: !GetAtt DockerMachine.PublicDnsName
```
## Bölüm 4 - Yada aynı ortamı Docker için Terraform ile de oluşturabiliriz.  



terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.57.0"
    }
  }
}


provider "aws" {
  region  = "us-east-1"
}

variable "secgr-dynamic-ports" {
  default = [22,8080,5432,7990]
}

variable "instance-type" {
  default = "t3a.medium"
  sensitive = true
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  dynamic "ingress" {
    for_each = var.secgr-dynamic-ports
    content {
      from_port = ingress.value
      to_port = ingress.value
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
}

  egress {
    description = "Outbound Allowed"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "tf-ec2" {
  ami           = "ami-087c17d1fe0178315"
  instance_type = var.instance-type
  key_name = "xxxxx"
  vpc_security_group_ids = [ aws_security_group.allow_ssh.id ]
  iam_instance_profile = "terraform"
      tags = {
      Name = "Docker-engine"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              systemctl start docker
              systemctl enable docker
              usermod -a -G docker ec2-user
              # install docker-compose
              curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" \
              -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
	            EOF
}  
output "myec2-public-ip" {
  value = aws_instance.tf-ec2.public_ip
}

## Bölüm 5 -  PostgresSQl , Jira ve BitBucket container oluşturup bağlanalım. 

1 - Busybox'tan (çok az yer kaplayan) bir container oluşturun ve "jira_datastore" olarak adlandırın:
"""
docker run -v /data --name=jira_datastore -d busybox echo "PSQL Data"

"""
2-  Bir PostgreSQL container oluşturun. Eğer git kurulu değilse "sudo yum imstall git -y" ile git kurun ve sonra alttaki komutu girip çalıştırın. 
"""
git clone https://github.com/Painted-Fox/docker-postgresql.git

"""
3- Yeni konteynerı buradan çalıştırılabiliriz. "jira_datastore" volumedekini kullanmayı unutmayın. Environment-variables istediğiniz gibi değiştirilebilirsiniz.
"""
docker run -d --name postgresql -e USER="super" -e DB="jiradb" -e PASS="p4ssw0rd" --volumes-from jira_datastore paintedfox/postgresql

"""
4- Ardından, JIRA Docker image oluşturun
"""
git clone https://github.com/hbokh/docker-jira-postgresql.git
docker build --rm=true -t hbokh/docker-jira-postgresql .
"""
5- JIRA-container başlatalım
"""
docker run -d --name jira -p 8080:8080 --link postgresql:db hbokh/docker-jira-postgresql
"""
6- jiraya bağlanmak için  http://< ec2 public ıp >:8080

7- bitbucket container başlatalım
"""
$ docker run -d -p 7990:7990 --name bitbucket blacklabelops/bitbucket

"""
8- bitbucket bağlanmak için http://< ec2 public ıp >:7990
